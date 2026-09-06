#!/usr/bin/env python3
"""Run a bounded PostgreSQL benchmark and persist machine-readable evidence."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import statistics
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "build" / "benchmark"
COMPOSE = ["docker", "compose", "--project-directory", str(ROOT), "-f", str(ROOT / "compose.yml")]
QUERY = "SELECT training_id, count(*) FROM analytics.consultation WHERE training_id = 'TRN-0001' AND occurred_at >= '2027-01-01T00:00:00Z' GROUP BY training_id"


def run(command: list[str], *, capture: bool = False) -> str:
    print("$ " + " ".join(command), flush=True)
    result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE if capture else None, stderr=subprocess.PIPE if capture else None)
    if result.returncode:
        detail = (result.stdout or "") + (result.stderr or "")
        raise RuntimeError(f"command failed ({result.returncode}): {detail.strip()}")
    return (result.stdout or "").strip()


def psql(sql: str, *, capture: bool = False) -> str:
    return run(COMPOSE + ["exec", "-T", "postgres", "psql", "-X", "-q", "-A", "-t", "-v", "ON_ERROR_STOP=1", "-U", "formaflow", "-d", "formaflow", "-c", sql], capture=capture)


def measure(label: str, repetitions: int = 5, warmups: int = 1) -> dict[str, object]:
    for _ in range(warmups):
        psql(f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {QUERY}", capture=True)
    times = []
    plans = []
    for index in range(1, repetitions + 1):
        raw = psql(f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {QUERY}", capture=True)
        plan = json.loads(raw)
        path = OUTPUT / f"{label}-plan-{index}.json"
        path.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        plans.append(path.relative_to(ROOT).as_posix())
        times.append(float(plan[0]["Execution Time"]))
    return {
        "warmups": warmups,
        "repetitions": repetitions,
        "executionTimesMs": times,
        "medianMs": statistics.median(times),
        "plans": plans,
    }


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    run([sys.executable, str(ROOT / "scripts" / "manage.py"), "reset-data"])
    run([sys.executable, str(ROOT / "scripts" / "manage.py"), "seed", "--dataset", "benchmark"])
    postgres_version = psql("SHOW server_version", capture=True)
    docker_environment = run(["docker", "info", "--format", "{{.ServerVersion}}|{{.OperatingSystem}}|{{.Architecture}}|{{.NCPU}}|{{.MemTotal}}"], capture=True)

    psql("DROP INDEX IF EXISTS analytics.idx_consultation_training_time; ANALYZE analytics.consultation")
    before_result = psql(QUERY, capture=True)
    before = measure("before-index")

    psql("CREATE INDEX idx_consultation_training_time ON analytics.consultation (training_id, occurred_at DESC); ANALYZE analytics.consultation")
    after_result = psql(QUERY, capture=True)
    after = measure("after-index")
    if before_result != after_result:
        raise RuntimeError(f"functional mismatch: before={before_result!r}, after={after_result!r}")

    inventory = json.loads((ROOT / "build" / "generated" / "inventory.json").read_text(encoding="utf-8"))
    result = {
        "protocolVersion": "1.0.0",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "postgresVersion": postgres_version,
        "dockerEnvironment": docker_environment,
        "dataset": "benchmark-small",
        "seed": 20260906,
        "logicalDate": "2027-01-20T12:00:00Z",
        "rows": 10000,
        "query": QUERY,
        "functionalResult": before_result,
        "functionallyEquivalent": True,
        "beforeIndex": before,
        "afterIndex": after,
        "limitations": [
            "local Docker execution, not a production workload",
            "short run sensitive to cache and host activity",
            "index write and maintenance costs are not measured",
            "no universal performance conclusion is claimed"
        ],
        "inventory": inventory,
    }
    output = OUTPUT / "result.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(f"Benchmark evidence: {output}")
    print(f"Functional result: {before_result}")
    print(f"Median before/after (ms): {before['medianMs']} / {after['medianMs']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
