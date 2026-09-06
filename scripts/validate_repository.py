#!/usr/bin/env python3
"""Stage-aware local repository validator; expanded in the final checkpoint."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
BASE_REQUIRED = (
    "README.md", "VERSION", "manifest.yml", "CHECKPOINTS.md", "compose.yml", "Makefile",
    ".env.example", ".gitignore", "inputs/formaflow-reference/PROVENANCE.md",
    "fixtures/nominal/dataset.json", "fixtures/edge-cases/dataset.json",
    "fixtures/flawed-schema/enrollment-export.csv", "fixtures/benchmark/profiles.json",
    "briefs/session-01/README.md", "briefs/session-02/README.md",
    "briefs/session-03/README.md", "briefs/session-04/README.md",
    "docs/templates/glossary.md", "docs/templates/assumptions.md",
    "docs/templates/invariants.md", "docs/templates/models.md",
    "docs/templates/functional-dependencies.md", "docs/templates/benchmark.md",
    "docs/templates/comparison-matrix.md", "docs/templates/adr.md",
    "docs/templates/polyglot-architecture.md", "docs/templates/cdan-transfer.md",
    "sql/course-start/001_flawed_schema.sql", "sql/course-start/003_smoke.sql",
)
SESSION_SCHEDULE = {
    "session-01": (240, 135, 105, "**Durée indicative :** 4 h, dont 2 h 15 FFP et 1 h 45 TDP."),
    "session-02": (180, 90, 90, "**Durée indicative :** 3 h, dont 1 h 30 FFP et 1 h 30 TDP."),
    "session-03": (240, 135, 105, "**Durée indicative :** 4 h, dont 2 h 15 FFP et 1 h 45 TDP."),
    "session-04": (
        180,
        60,
        120,
        "**Durée indicative :** 3 h, dont 1 h FFP et 2 h TDP. "
        "Le QCM individuel contextualisé de 45 minutes est inclus dans ces 2 h de TDP.",
    ),
}


def parse_sessions(manifest: str) -> dict[str, dict[str, int]]:
    sessions: dict[str, dict[str, int]] = {}
    current: dict[str, int] | None = None
    current_id: str | None = None
    in_sessions = False
    for line in manifest.splitlines():
        if line == "sessions:":
            in_sessions = True
            continue
        if in_sessions and line and not line.startswith(" "):
            break
        match_id = re.fullmatch(r"  - id: (session-[0-9]{2})", line)
        if match_id:
            current_id = match_id.group(1)
            current = {}
            sessions[current_id] = current
            continue
        match_value = re.fullmatch(r"    (duration_minutes|ffp_minutes|tdp_minutes): ([0-9]+)", line)
        if current is not None and match_value:
            current[match_value.group(1)] = int(match_value.group(2))
    return sessions


def validate_schedule(errors: list[str]) -> None:
    manifest_path = ROOT / "manifest.yml"
    try:
        manifest = manifest_path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"manifeste illisible: {exc}")
        return
    sessions = parse_sessions(manifest)
    expected_ids = set(SESSION_SCHEDULE)
    if set(sessions) != expected_ids:
        errors.append(
            "identifiants de séance invalides: "
            f"attendus={sorted(expected_ids)}, obtenus={sorted(sessions)}"
        )
    totals = {"duration_minutes": 0, "ffp_minutes": 0, "tdp_minutes": 0}
    for session_id, (duration, ffp, tdp, brief_line) in SESSION_SCHEDULE.items():
        values = sessions.get(session_id, {})
        for key in totals:
            value = values.get(key)
            if value is None:
                errors.append(f"{session_id}: champ {key} absent")
            else:
                totals[key] += value
        if values.get("duration_minutes") != values.get("ffp_minutes", -1) + values.get("tdp_minutes", -1):
            errors.append(f"{session_id}: duration_minutes doit égaler ffp_minutes + tdp_minutes")
        if (values.get("duration_minutes"), values.get("ffp_minutes"), values.get("tdp_minutes")) != (duration, ffp, tdp):
            errors.append(f"{session_id}: ventilation différente de la progression pédagogique V3")
        brief_path = ROOT / "briefs" / session_id / "README.md"
        try:
            brief = brief_path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"brief illisible {session_id}: {exc}")
        else:
            if brief_line not in brief:
                errors.append(f"{session_id}: ligne de durée du brief non concordante")
    expected_totals = {"duration_minutes": 840, "ffp_minutes": 420, "tdp_minutes": 420}
    for key, expected in expected_totals.items():
        if totals[key] != expected:
            errors.append(f"total {key} invalide: attendu={expected}, obtenu={totals[key]}")
    if not re.search(r"(?ms)^assessment:\n(?:  .*\n)*?  duration_minutes: 45$", manifest):
        errors.append("la durée du QCM doit être de 45 minutes")
    if "  scheduled_session: session-04" not in manifest or "  included_in_tdp: true" not in manifest:
        errors.append("le QCM doit être déclaré dans le TDP de la séance 4")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("course-start", "relational", "nosql", "final"), default="course-start")
    args = parser.parse_args()
    errors: list[str] = []
    required = list(BASE_REQUIRED)
    if args.stage in {"relational", "nosql", "final"}:
        required.extend((
            "docs/glossary.md", "docs/assumptions.md", "docs/invariants.md",
            "docs/data-dictionary.md", "docs/normalization.md",
            "diagrams/mcd.mmd", "diagrams/mld.mmd", "diagrams/mpd.mmd",
            "sql/schema/000_reset.sql", "sql/schema/020_tables.sql",
            "sql/constraints/030_capacity_guard.sql", "sql/indexes/040_indexes.sql",
            "sql/reporting/050_views.sql", "sql/seed/nominal.sql",
            "sql/tests/010_integrity.sql", "sql/tests/020_reporting.sql",
            "benchmarks/protocols/relational-index.md", "scripts/run_benchmark.py",
            "benchmarks/results/reference-small/result.json",
        ))
    if args.stage in {"nosql", "final"}:
        required.extend((
            "docs/nosql-comparison.md", "docs/adr/0002-nosql-projections-not-sources.md",
            "nosql/execution-status.md",
            "nosql/mongodb/README.md", "nosql/mongodb/model.json", "nosql/mongodb/init.js", "nosql/mongodb/queries.js",
            "nosql/redis/README.md", "nosql/redis/keys.md", "nosql/redis/init.redis",
            "nosql/cassandra/README.md", "nosql/cassandra/schema.cql", "nosql/cassandra/queries.cql", "nosql/cassandra/prepared-trace.json",
            "nosql/neo4j/README.md", "nosql/neo4j/init.cypher", "nosql/neo4j/queries.cypher",
        ))
    for relative in required:
        if not (ROOT / relative).is_file():
            errors.append(f"fichier obligatoire absent: {relative}")
    for relative in ("fixtures/nominal/dataset.json", "fixtures/edge-cases/dataset.json"):
        try:
            json.loads((ROOT / relative).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"JSON invalide {relative}: {exc}")
    validate_schedule(errors)
    forbidden = re.compile(r"(?i)(assessment[-_ ]?answer|qcm[-_ ]?correction|distractor[-_ ]?bank|bar[eè]me cach[eé])")
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in {".git", ".idea", "_inputs", "build", "dist"} for part in path.parts):
            continue
        if forbidden.search(path.as_posix()):
            errors.append(f"contenu d'évaluation interdit: {path.relative_to(ROOT)}")
    if errors:
        print("VALIDATION ÉCHOUÉE")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"VALIDATION OK - stage={args.stage} - {len(required)} contrôles de présence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
