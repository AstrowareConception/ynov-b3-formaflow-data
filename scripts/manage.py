#!/usr/bin/env python3
"""Stable command interface used by the Makefile on every supported platform."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
COMPOSE = ["docker", "compose", "--project-directory", str(ROOT), "-f", str(ROOT / "compose.yml")]
EXPECTED_INPUTS = {
    "ynov-b3-formaflow-reference-v1.0.0.zip": "9de0223729f0aa4b99c7d5d2ff260cd25f7540401566bb033b7a383c57b4d921",
    "ynov-b3-cdan-evidence-kit-v1.0.0.zip": "845ff950bf6be288715b6edb0c4a84457c7827bb40caca238a411ba188e6665a",
}


class CommandError(RuntimeError):
    pass


def display(command: list[str]) -> str:
    return " ".join(f'"{part}"' if " " in part else part for part in command)


def run(command: list[str], *, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess[str]:
    print(f"$ {display(command)}", flush=True)
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.STDOUT if capture else None,
        )
    except FileNotFoundError as exc:
        raise CommandError(f"Commande introuvable : {command[0]}. Vérifiez les prérequis documentés.") from exc
    if capture and result.stdout:
        print(result.stdout, end="")
    if check and result.returncode != 0:
        raise CommandError(f"Échec avec le code {result.returncode} : {display(command)}")
    return result


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_source_archives_if_present() -> None:
    inputs = ROOT / "_inputs"
    if not inputs.exists():
        print("[setup] _inputs absent: normal dans une archive distribuée autonome.")
        return
    for name, expected in EXPECTED_INPUTS.items():
        path = inputs / name
        if not path.is_file():
            raise CommandError(f"Dépendance canonique absente : {path}")
        actual = sha256(path)
        if actual != expected:
            raise CommandError(f"Empreinte invalide pour {name}: attendu {expected}, obtenu {actual}")
        print(f"[setup] SHA-256 vérifié : {name}")


def ensure_docker_client() -> None:
    if not shutil.which("docker"):
        raise CommandError("Docker CLI est requis. Installez Docker Desktop ou un moteur compatible avec Compose.")
    run(["docker", "compose", "version"])


def setup() -> None:
    if sys.version_info < (3, 10):
        raise CommandError("Python 3.10 ou plus récent est requis.")
    ensure_docker_client()
    verify_source_archives_if_present()
    env_file = ROOT / ".env"
    if not env_file.exists():
        shutil.copyfile(ROOT / ".env.example", env_file)
        print("[setup] .env local créé depuis .env.example (valeurs locales sans secret).")
    else:
        print("[setup] .env local déjà présent, aucun écrasement.")
    run(COMPOSE + ["config", "--quiet"])
    run([sys.executable, str(ROOT / "scripts" / "generate_fixtures.py"), "--dataset", "all"])


def start() -> None:
    ensure_docker_client()
    run(COMPOSE + ["up", "-d", "--wait", "postgres"])


def stop() -> None:
    ensure_docker_client()
    run(COMPOSE + ["down", "--remove-orphans"])


def psql_file(path: Path) -> None:
    if not path.is_file():
        raise CommandError(f"Script SQL absent : {path.relative_to(ROOT)}")
    container_path = "/workspace/" + path.relative_to(ROOT).as_posix()
    run(COMPOSE + ["exec", "-T", "postgres", "psql", "-v", "ON_ERROR_STOP=1", "-U", "formaflow", "-d", "formaflow", "-f", container_path])


def reset_data() -> None:
    start()
    canonical = ROOT / "sql" / "schema" / "000_reset.sql"
    if canonical.exists():
        for relative in (
            "sql/schema/000_reset.sql",
            "sql/schema/010_types_and_schemas.sql",
            "sql/schema/020_tables.sql",
            "sql/constraints/030_capacity_guard.sql",
            "sql/indexes/040_indexes.sql",
            "sql/reporting/050_views.sql",
        ):
            psql_file(ROOT / relative)
        seed("nominal")
    else:
        psql_file(ROOT / "sql" / "course-start" / "001_flawed_schema.sql")
        psql_file(ROOT / "sql" / "course-start" / "002_load_flawed.sql")
        print("[reset-data] État étudiant chargé : export redondant volontairement fragile.")


def seed(dataset: str) -> None:
    allowed = {"nominal", "edge-cases", "benchmark"}
    if dataset not in allowed:
        raise CommandError(f"Dataset inconnu {dataset!r}; valeurs autorisées : {', '.join(sorted(allowed))}.")
    run([sys.executable, str(ROOT / "scripts" / "generate_fixtures.py"), "--dataset", dataset])
    seed_sql = ROOT / "sql" / "seed" / f"{dataset}.sql"
    if seed_sql.exists():
        psql_file(seed_sql)
    elif dataset == "nominal":
        psql_file(ROOT / "sql" / "course-start" / "001_flawed_schema.sql")
        psql_file(ROOT / "sql" / "course-start" / "002_load_flawed.sql")
    else:
        print(f"[seed] {dataset} préparé dans build/generated ; l'état course-start laisse le chargement comme activité.")


def smoke() -> None:
    test = ROOT / "sql" / "tests" / "001_smoke.sql"
    psql_file(test if test.exists() else ROOT / "sql" / "course-start" / "003_smoke.sql")


def unit_tests() -> None:
    tests = ROOT / "tests"
    if tests.exists():
        run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])
    else:
        print("[test] Aucun test Python à cet état pédagogique.")


def test() -> None:
    run([sys.executable, str(ROOT / "scripts" / "validate_repository.py")])
    unit_tests()
    if (ROOT / "sql" / "tests" / "010_integrity.sql").exists():
        psql_file(ROOT / "sql" / "tests" / "010_integrity.sql")
        psql_file(ROOT / "sql" / "tests" / "020_reporting.sql")
    else:
        smoke()


def benchmark() -> None:
    script = ROOT / "scripts" / "run_benchmark.py"
    if not script.exists():
        raise CommandError("Le benchmark canonique devient disponible au checkpoint relationnel.")
    run([sys.executable, str(script)])


def nosql(profile: str) -> None:
    services = {"mongodb": "mongodb", "redis": "redis", "cassandra": "cassandra", "neo4j": "neo4j"}
    if profile not in services:
        raise CommandError(f"PROFILE requis parmi : {', '.join(services)}.")
    init_files = {
        "mongodb": ("mongosh", "/workspace/nosql/mongodb/init.js"),
        "redis": ("redis-cli", "--pipe"),
        "cassandra": ("cqlsh", "-f", "/workspace/nosql/cassandra/schema.cql"),
        "neo4j": ("cypher-shell", "-f", "/workspace/nosql/neo4j/init.cypher"),
    }
    init_path = {
        "mongodb": ROOT / "nosql/mongodb/init.js",
        "redis": ROOT / "nosql/redis/init.redis",
        "cassandra": ROOT / "nosql/cassandra/schema.cql",
        "neo4j": ROOT / "nosql/neo4j/init.cypher",
    }[profile]
    if not init_path.exists():
        raise CommandError(f"Le profil {profile} devient disponible au checkpoint NoSQL.")
    run(COMPOSE + ["--profile", profile, "up", "-d", "--wait", services[profile]])
    if profile == "redis":
        payload = init_path.read_text(encoding="utf-8")
        command = COMPOSE + ["exec", "-T", "redis", *init_files[profile]]
        print(f"$ {display(command)} < nosql/redis/init.redis", flush=True)
        result = subprocess.run(command, cwd=ROOT, input=payload, text=True, check=False)
        if result.returncode:
            raise CommandError("L'initialisation Redis a échoué.")
    else:
        run(COMPOSE + ["exec", "-T", services[profile], *init_files[profile]])
    print(f"[nosql] Profil {profile} exécuté seul et initialisation validée.")


def quality() -> None:
    run([sys.executable, str(ROOT / "scripts" / "validate_repository.py")])
    unit_tests()
    ensure_docker_client()
    run(COMPOSE + ["config", "--quiet"])


def package() -> None:
    script = ROOT / "scripts" / "package_repository.py"
    if not script.exists():
        raise CommandError("Le packageur est ajouté dans l'état final.")
    run([sys.executable, str(script)])


def clean() -> None:
    for name in ("build", "dist"):
        target = (ROOT / name).resolve()
        if target.parent != ROOT.resolve():
            raise CommandError(f"Cible de nettoyage refusée : {target}")
        if target.exists():
            shutil.rmtree(target)
            print(f"[clean] Supprimé : {target}")
        else:
            print(f"[clean] Déjà absent : {target}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("setup", "start", "stop", "reset-data", "seed", "smoke", "test", "benchmark", "nosql", "quality", "package", "clean"))
    parser.add_argument("--dataset", default="nominal")
    parser.add_argument("--profile", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    actions = {
        "setup": setup,
        "start": start,
        "stop": stop,
        "reset-data": reset_data,
        "seed": lambda: seed(args.dataset),
        "smoke": smoke,
        "test": test,
        "benchmark": benchmark,
        "nosql": lambda: nosql(args.profile),
        "quality": quality,
        "package": package,
        "clean": clean,
    }
    try:
        actions[args.command]()
    except CommandError as exc:
        print(f"ERREUR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
