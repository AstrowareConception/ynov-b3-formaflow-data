#!/usr/bin/env python3
"""Apply the autonomous handoff MPD to an explicit empty PostgreSQL database."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
DATABASE = "formaflow_handoff_validation"
COMPOSE = ["docker", "compose", "--project-directory", str(ROOT), "-f", str(ROOT / "compose.yml")]


def run(command: list[str], *, capture: bool = False) -> str:
    print("$ " + " ".join(command), flush=True)
    result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE if capture else None, stderr=subprocess.STDOUT if capture else None)
    if capture and result.stdout:
        print(result.stdout, end="")
    if result.returncode:
        raise RuntimeError(f"command failed with code {result.returncode}")
    return result.stdout or ""


def admin(sql: str) -> None:
    run(COMPOSE + ["exec", "-T", "postgres", "psql", "-v", "ON_ERROR_STOP=1", "-U", "formaflow", "-d", "postgres", "-c", sql])


def main() -> int:
    run(COMPOSE + ["up", "-d", "--wait", "postgres"])
    admin(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{DATABASE}';")
    admin(f"DROP DATABASE IF EXISTS {DATABASE};")
    try:
        admin(f"CREATE DATABASE {DATABASE} TEMPLATE template0;")
        run(COMPOSE + ["exec", "-T", "postgres", "psql", "-v", "ON_ERROR_STOP=1", "-U", "formaflow", "-d", DATABASE, "-f", "/workspace/handoff/data-reference/models/mpd.sql"])
        output = run(COMPOSE + ["exec", "-T", "postgres", "psql", "-A", "-t", "-U", "formaflow", "-d", DATABASE, "-c", "SELECT count(*) FROM information_schema.tables WHERE table_schema IN ('core','analytics');"], capture=True)
        count = int(output.strip().splitlines()[-1])
        if count != 16:
            raise RuntimeError(f"handoff MPD expected 16 base tables, found {count}")
        print("HANDOFF EMPTY-DATABASE VALIDATION OK: 16 base tables plus reporting views")
    finally:
        admin(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{DATABASE}';")
        admin(f"DROP DATABASE IF EXISTS {DATABASE};")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"ERREUR: {exc}", file=sys.stderr)
        raise SystemExit(1)
