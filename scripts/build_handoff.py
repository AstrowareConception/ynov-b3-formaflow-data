#!/usr/bin/env python3
"""Build the standalone handoff MPD from canonical ordered SQL sources."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    "sql/schema/000_reset.sql",
    "sql/schema/010_types_and_schemas.sql",
    "sql/schema/020_tables.sql",
    "sql/constraints/030_capacity_guard.sql",
    "sql/indexes/040_indexes.sql",
    "sql/reporting/050_views.sql",
)


def render() -> str:
    chunks = [
        "-- FormaFlow Data Reference 1.0.0 - standalone PostgreSQL 16 MPD",
        "-- Generated deterministically by scripts/build_handoff.py; do not edit this copy directly.",
        "",
    ]
    for relative in SOURCES:
        chunks.extend((f"-- BEGIN {relative}", (ROOT / relative).read_text(encoding="utf-8").rstrip(), f"-- END {relative}", ""))
    return "\n".join(chunks)


def main() -> int:
    target = ROOT / "handoff" / "data-reference" / "models" / "mpd.sql"
    target.parent.mkdir(parents=True, exist_ok=True)
    content = render()
    if not target.exists() or target.read_text(encoding="utf-8") != content:
        target.write_text(content, encoding="utf-8", newline="\n")
        print(f"Handoff MPD generated: {target.relative_to(ROOT)}")
    else:
        print(f"Handoff MPD already current: {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
