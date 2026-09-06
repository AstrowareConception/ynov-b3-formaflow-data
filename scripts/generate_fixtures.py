#!/usr/bin/env python3
"""Generate deterministic classroom benchmark data and verifiable inventories."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "build" / "generated"
LOGICAL_DATE = "2027-01-20T12:00:00Z"
DEFAULT_SEED = 20260906
SIZES = {"small": 10_000, "medium": 100_000, "large-trace": 1_000_000}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def benchmark(size: str = "small", seed: int = DEFAULT_SEED) -> dict[str, object]:
    if size == "large-trace":
        return {
            "dataset": "benchmark",
            "profile": size,
            "rows": SIZES[size],
            "generated": False,
            "representation": "prepared-trace",
            "seed": seed,
            "logicalDate": LOGICAL_DATE,
            "boundaryCaseIds": ["BENCH-HOT-TRAINING", "BENCH-EMPTY-OPTIONAL"],
        }
    rows = SIZES[size]
    rng = random.Random(seed)
    path = OUTPUT / f"benchmark-consultations-{size}.csv"
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["consultation_id", "training_id", "profile_id", "occurred_at", "source"])
        for index in range(1, rows + 1):
            training = "TRN-0001" if index % 5 == 0 else f"TRN-{rng.randint(1, 500):04d}"
            profile = "" if index % 97 == 0 else f"PRO-{rng.randint(1, 5000):05d}"
            writer.writerow([f"CST-{index:09d}", training, profile, f"2027-01-{1 + index % 20:02d}T{index % 24:02d}:{index % 60:02d}:00Z", "catalog"])
    return {
        "dataset": "benchmark",
        "profile": size,
        "rows": rows,
        "generated": True,
        "file": path.relative_to(ROOT).as_posix(),
        "sha256": sha256(path),
        "seed": seed,
        "logicalDate": LOGICAL_DATE,
        "boundaryCaseIds": ["BENCH-HOT-TRAINING", "BENCH-EMPTY-OPTIONAL"],
    }


def static_inventory(dataset: str) -> dict[str, object]:
    source = ROOT / "fixtures" / dataset / "dataset.json"
    payload = json.loads(source.read_text(encoding="utf-8"))
    counts = {key: len(value) for key, value in payload.items() if isinstance(value, list)}
    return {
        "dataset": dataset,
        "source": source.relative_to(ROOT).as_posix(),
        "sha256": sha256(source),
        "seed": payload.get("seed", DEFAULT_SEED),
        "logicalDate": payload.get("logicalDate", LOGICAL_DATE),
        "counts": counts,
        "boundaryCaseIds": payload.get("boundaryCaseIds", []),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", choices=("all", "nominal", "edge-cases", "benchmark"), default="all")
    parser.add_argument("--size", choices=tuple(SIZES), default="small")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    inventories = []
    if args.dataset in ("all", "nominal"):
        inventories.append(static_inventory("nominal"))
    if args.dataset in ("all", "edge-cases"):
        inventories.append(static_inventory("edge-cases"))
    if args.dataset in ("all", "benchmark"):
        inventories.extend(benchmark(size, args.seed) for size in SIZES)
    inventory_path = OUTPUT / "inventory.json"
    inventory_path.write_text(json.dumps({"inventories": inventories}, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Inventaire écrit : {inventory_path.relative_to(ROOT)} ({len(inventories)} entrées)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
