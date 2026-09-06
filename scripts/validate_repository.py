#!/usr/bin/env python3
"""Validate the FormaFlow Data repository without external dependencies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {
    ".git", ".idea", "_inputs", "dist", "build", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".tox", ".venv", "venv", "node_modules", "volumes",
}
TEXT_EXTENSIONS = frozenset({
    ".cql", ".csv", ".cypher", ".example", ".js", ".json", ".md", ".mmd",
    ".py", ".redis", ".sql", ".txt", ".yaml", ".yml",
})
TEXT_FILENAMES = frozenset({".gitattributes", ".gitignore", "Makefile", "VERSION"})
BASE_REQUIRED = (
    "README.md", "CHANGELOG.md", "VERSION", "manifest.yml", "CHECKPOINTS.md", "compose.yml",
    "Makefile", ".env.example", ".gitignore", "image-lock.yml",
    "inputs/formaflow-reference/PROVENANCE.md", "inputs/formaflow-reference/VERSION",
    "fixtures/nominal/dataset.json", "fixtures/edge-cases/dataset.json",
    "fixtures/flawed-schema/enrollment-export.csv", "fixtures/benchmark/profiles.json",
    "briefs/session-01/README.md", "briefs/session-02/README.md",
    "briefs/session-03/README.md", "briefs/session-04/README.md",
    "docs/templates/glossary.md", "docs/templates/assumptions.md", "docs/templates/invariants.md",
    "docs/templates/models.md", "docs/templates/functional-dependencies.md", "docs/templates/benchmark.md",
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


def validate_schedule(root: Path, errors: list[str]) -> None:
    manifest_path = root / "manifest.yml"
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
        brief_path = root / "briefs" / session_id / "README.md"
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
RELATIONAL_REQUIRED = (
    "docs/glossary.md", "docs/assumptions.md", "docs/invariants.md", "docs/data-dictionary.md",
    "docs/normalization.md", "diagrams/mcd.mmd", "diagrams/mld.mmd", "diagrams/mpd.mmd",
    "sql/schema/000_reset.sql", "sql/schema/010_types_and_schemas.sql", "sql/schema/020_tables.sql",
    "sql/constraints/030_capacity_guard.sql", "sql/indexes/040_indexes.sql",
    "sql/reporting/050_views.sql", "sql/seed/nominal.sql", "sql/seed/edge-cases.sql",
    "sql/seed/benchmark.sql", "sql/tests/001_smoke.sql", "sql/tests/010_integrity.sql",
    "sql/tests/020_reporting.sql", "benchmarks/protocols/relational-index.md",
    "benchmarks/results/reference-small/result.json", "benchmarks/results/prepared-large-trace.json",
    "scripts/run_benchmark.py",
)
NOSQL_REQUIRED = (
    "docs/nosql-comparison.md", "docs/adr/0002-nosql-projections-not-sources.md", "nosql/execution-status.md",
    "nosql/mongodb/README.md", "nosql/mongodb/model.json", "nosql/mongodb/init.js", "nosql/mongodb/queries.js",
    "nosql/redis/README.md", "nosql/redis/keys.md", "nosql/redis/init.redis",
    "nosql/cassandra/README.md", "nosql/cassandra/schema.cql", "nosql/cassandra/queries.cql",
    "nosql/cassandra/prepared-trace.json", "nosql/neo4j/README.md",
    "nosql/neo4j/init.cypher", "nosql/neo4j/queries.cypher",
)
FINAL_REQUIRED = (
    "docs/architecture.md", "diagrams/polyglot-architecture.mmd",
    "docs/adr/0003-outbox-and-rebuildable-projections.md", "docs/cdan/transfer.md", "docs/release.md",
    "scripts/build_handoff.py", "scripts/validate_handoff.py", "scripts/package_repository.py",
    "handoff/data-reference/README.md", "handoff/data-reference/manifest.yml",
    "handoff/data-reference/source-version.txt", "handoff/data-reference/glossary.md",
    "handoff/data-reference/invariants.md", "handoff/data-reference/examples-and-counterexamples.md",
    "handoff/data-reference/assumptions.md", "handoff/data-reference/open-questions.md",
    "handoff/data-reference/data-dictionary.md", "handoff/data-reference/ownership-hypotheses.md",
    "handoff/data-reference/known-limitations.md", "handoff/data-reference/models/mcd.mmd",
    "handoff/data-reference/models/mld.mmd", "handoff/data-reference/models/mpd.sql",
    "handoff/data-reference/decisions/normalization.md",
    "handoff/data-reference/decisions/storage-and-price.md",
    "handoff/data-reference/decisions/denormalization-and-projections.md",
    "handoff/data-reference/evidence/benchmark-result.json",
    "handoff/data-reference/evidence/integrity-tests.md",
    "tests/test_validate_repository.py", "tests/test_package_repository.py",
)


def source_files(root: Path):
    for path in sorted(root.rglob("*")):
        try:
            relative = path.relative_to(root)
        except ValueError:
            continue
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        if path.is_file():
            yield path


def is_text_path(path: Path) -> bool:
    return path.name in TEXT_FILENAMES or path.suffix.lower() in TEXT_EXTENSIONS


def required_for(stage: str) -> tuple[str, ...]:
    required = list(BASE_REQUIRED)
    if stage in {"relational", "nosql", "final"}:
        required.extend(RELATIONAL_REQUIRED)
    if stage in {"nosql", "final"}:
        required.extend(NOSQL_REQUIRED)
    if stage == "final":
        required.extend(FINAL_REQUIRED)
    return tuple(required)


def validate_links(root: Path, errors: list[str]) -> None:
    pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for path in source_files(root):
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        for raw_target in pattern.findall(text):
            target = raw_target.strip().strip("<>").split(maxsplit=1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            candidate = (path.parent / target_path).resolve()
            if not candidate.exists():
                errors.append(f"lien Markdown local cassé dans {path.relative_to(root)}: {target}")


def validate_json(root: Path, errors: list[str]) -> None:
    for path in source_files(root):
        if path.suffix.lower() != ".json":
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"JSON invalide {path.relative_to(root)}: {exc}")


def validate_versions(root: Path, errors: list[str]) -> None:
    if (root / "VERSION").is_file() and (root / "VERSION").read_text(encoding="utf-8").strip() != "1.0.0":
        errors.append("VERSION doit être 1.0.0")
    manifest = (root / "manifest.yml").read_text(encoding="utf-8") if (root / "manifest.yml").is_file() else ""
    for marker in ("name: ynov-b3-formaflow-data", "version: 1.0.0", "status: ready-for-release"):
        if marker not in manifest:
            errors.append(f"manifest.yml incomplet: {marker}")
    provenance = (root / "inputs/formaflow-reference/PROVENANCE.md")
    if provenance.is_file():
        text = provenance.read_text(encoding="utf-8")
        markers = (
            "Version : `1.0.0`", "reference-v1.0.0",
            "9de0223729f0aa4b99c7d5d2ff260cd25f7540401566bb033b7a383c57b4d921",
            "sans dépôt Git imbriqué ni dépendance dynamique",
        )
        for marker in markers:
            if marker not in text:
                errors.append(f"provenance FormaFlow incomplète: {marker}")
    lock = (root / "image-lock.yml")
    if lock.is_file():
        digests = re.findall(r"digest:\s*sha256:([0-9a-f]+)", lock.read_text(encoding="utf-8"))
        if len(digests) != 5 or any(len(value) != 64 for value in digests):
            errors.append("image-lock.yml doit contenir cinq digests SHA-256 complets réellement résolus")


def validate_identifiers(root: Path, errors: list[str]) -> None:
    path = root / "fixtures/nominal/dataset.json"
    if not path.is_file():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return
    collections = {key: value for key, value in data.items() if isinstance(value, list)}
    for name, records in collections.items():
        ids = [record.get("id") for record in records if isinstance(record, dict) and "id" in record]
        if len(ids) != len(set(ids)):
            errors.append(f"identifiants dupliqués dans fixtures nominales: {name}")
    identifiers = {name: {record.get("id") for record in records if isinstance(record, dict)} for name, records in collections.items()}
    checks = (
        ("sessions", "trainingId", "trainings"), ("sessions", "currentTariffId", "tariffs"),
        ("tariffs", "trainingId", "trainings"), ("orderLines", "orderId", "orders"),
        ("orderLines", "sessionId", "sessions"), ("orderLines", "participantId", "participants"),
        ("enrollments", "orderLineId", "orderLines"), ("enrollments", "sessionId", "sessions"),
        ("enrollments", "participantId", "participants"), ("payments", "orderId", "orders"),
        ("invoices", "orderId", "orders"), ("consultations", "trainingId", "trainings"),
        ("recommendations", "trainingId", "trainings"),
    )
    for collection, field, target in checks:
        for record in collections.get(collection, []):
            value = record.get(field)
            if value is not None and value not in identifiers.get(target, set()):
                errors.append(f"référence inconnue {collection}.{field}={value} vers {target}")
    edge_path = root / "fixtures/edge-cases/dataset.json"
    if edge_path.is_file():
        try:
            edge = json.loads(edge_path.read_text(encoding="utf-8"))
            ids = edge.get("boundaryCaseIds", [])
            case_ids = [case.get("id") for case in edge.get("cases", [])]
            if len(ids) != len(set(ids)) or set(ids) != set(case_ids):
                errors.append("identifiants des cas limites incohérents")
        except json.JSONDecodeError:
            pass


def validate_sensitive_content(root: Path, errors: list[str]) -> None:
    secret_patterns = (
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
        re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
        re.compile(r"(?i)\b(?:password|passwd|api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"]?[A-Za-z0-9+/_.-]{12,}"),
    )
    forbidden_assessment = re.compile(r"(?i)(correct_answer\s*[:=]|answer_key\s*[:=]|qcm-question-\d+|distractor_bank)")
    email_pattern = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+)")
    for path in source_files(root):
        relative = path.relative_to(root)
        if path.suffix.lower() not in {".md", ".txt", ".json", ".yml", ".yaml", ".csv", ".sql", ".py", ".js", ".cql", ".cypher", ".redis", ".example"} and path.name != "Makefile":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in secret_patterns:
            if pattern.search(text):
                errors.append(f"secret manifeste potentiel: {relative}")
                break
        is_validator_source = relative.as_posix() in {"scripts/validate_repository.py", "tests/test_validate_repository.py"}
        if not is_validator_source and forbidden_assessment.search(text):
            errors.append(f"contenu d'évaluation réel potentiel: {relative}")
        if relative.parts and relative.parts[0] == "fixtures":
            for domain in email_pattern.findall(text):
                if not domain.lower().endswith("example.test"):
                    errors.append(f"email non synthétique dans {relative}: domaine {domain}")
    for path in source_files(root):
        lowered = path.name.lower()
        if any(token in lowered for token in ("answer-key", "qcm-correction", "distractor-bank", "assessment-variant", "hidden-grading")):
            errors.append(f"fichier d'évaluation interdit: {path.relative_to(root)}")


def validate_contracts(root: Path, errors: list[str]) -> None:
    compose = (root / "compose.yml").read_text(encoding="utf-8") if (root / "compose.yml").is_file() else ""
    for profile in ("mongodb", "redis", "cassandra", "neo4j"):
        if f"profiles: [{profile}]" not in compose:
            errors.append(f"profil Compose absent: {profile}")
    if "profiles:" in re.search(r"(?ms)^  postgres:.*?(?=^  \w|\Z)", compose).group(0) if "  postgres:" in compose else "":
        errors.append("PostgreSQL ne doit pas être placé dans un profil")
    invariants = (root / "docs/invariants.md").read_text(encoding="utf-8") if (root / "docs/invariants.md").is_file() else ""
    integrity = (root / "sql/tests/010_integrity.sql").read_text(encoding="utf-8") if (root / "sql/tests/010_integrity.sql").is_file() else ""
    for marker in ("INV-CAPACITY", "INV-ENROLLMENT-UNIQUE", "INV-PRICE-SNAPSHOT"):
        if marker not in invariants:
            errors.append(f"invariant documenté absent: {marker}")
    for marker in ("capacity violation", "duplicate enrollment", "historical price"):
        if marker not in integrity:
            errors.append(f"preuve SQL d'invariant absente: {marker}")
    transfer = (root / "docs/cdan/transfer.md").read_text(encoding="utf-8") if (root / "docs/cdan/transfer.md").is_file() else ""
    cdan_markers = (
        "Evidence Kit : `1.0.0`", "Profil : `data`", "formative et non notée", "aucune seconde notation",
        "données synthétiques ou explicitement autorisées", "Problème ou hypothèse", "Décision ou conclusion",
        "Contribution personnelle", "Outils et assistants", "Preuves sélectionnées", "Limites",
        "Transfert vers le projet CDAN", "Action suivante",
    )
    for marker in cdan_markers:
        if marker not in transfer:
            errors.append(f"contrat CDAN incomplet: {marker}")
    handoff_manifest = root / "handoff/data-reference/manifest.yml"
    if handoff_manifest.is_file():
        handoff = handoff_manifest.read_text(encoding="utf-8")
        for marker in ("defines_aggregates: false", "defines_value_objects: false", "defines_bounded_contexts: false", "defines_ports_or_adapters: false"):
            if marker not in handoff:
                errors.append(f"garde-fou handoff absent: {marker}")


def validate_handoff_generated(root: Path, errors: list[str]) -> None:
    target = root / "handoff/data-reference/models/mpd.sql"
    if not target.is_file():
        return
    sources = (
        "sql/schema/000_reset.sql", "sql/schema/010_types_and_schemas.sql", "sql/schema/020_tables.sql",
        "sql/constraints/030_capacity_guard.sql", "sql/indexes/040_indexes.sql", "sql/reporting/050_views.sql",
    )
    for source in sources:
        if f"-- BEGIN {source}" not in target.read_text(encoding="utf-8"):
            errors.append(f"MPD handoff incomplet: {source}")


def validate_archive(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"archive absente: {path}"]
    try:
        with zipfile.ZipFile(path) as archive:
            bad = archive.testzip()
            if bad:
                errors.append(f"entrée ZIP corrompue: {bad}")
            names = [name for name in archive.namelist() if name]
            roots = {name.split("/", 1)[0] for name in names}
            if roots != {"ynov-b3-formaflow-data-v1.0.0"}:
                errors.append(f"racine ZIP inattendue: {sorted(roots)}")
            for name in names:
                parts = set(Path(name).parts)
                if parts & EXCLUDED_DIRS or Path(name).name == ".env":
                    errors.append(f"entrée exclue présente dans le ZIP: {name}")
                if name.endswith((".zip", ".bundle", ".pyc", ".log")):
                    errors.append(f"artefact interdit présent dans le ZIP: {name}")
                if is_text_path(Path(name)):
                    payload = archive.read(name)
                    try:
                        payload.decode("utf-8")
                    except UnicodeDecodeError:
                        errors.append(f"fichier texte non UTF-8 dans le ZIP: {name}")
                    if b"\r" in payload:
                        errors.append(f"fin de ligne non LF dans le ZIP: {name}")
    except zipfile.BadZipFile as exc:
        errors.append(f"ZIP invalide: {exc}")
    return errors


def validate(root: Path = ROOT, stage: str = "final") -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    for relative in required_for(stage):
        if not (root / relative).is_file():
            errors.append(f"fichier obligatoire absent: {relative}")
    validate_json(root, errors)
    validate_versions(root, errors)
    validate_schedule(root, errors)
    validate_links(root, errors)
    validate_identifiers(root, errors)
    validate_sensitive_content(root, errors)
    if stage in {"nosql", "final"}:
        validate_contracts(root, errors)
    if stage == "final":
        validate_handoff_generated(root, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("course-start", "relational", "nosql", "final"), default="final")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--archive", type=Path)
    args = parser.parse_args()
    errors = validate(args.root, args.stage)
    if args.archive:
        errors.extend(validate_archive(args.archive.resolve()))
    if errors:
        print(f"VALIDATION ÉCHOUÉE - {len(errors)} erreur(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"VALIDATION OK - stage={args.stage} - {len(required_for(args.stage))} fichiers obligatoires et contrôles de cohérence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
