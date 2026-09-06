from __future__ import annotations

from pathlib import Path
import shutil
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_repository import EXCLUDED_DIRS, validate  # noqa: E402


def copy_repository(target: Path) -> None:
    def ignore(_directory: str, names: list[str]) -> set[str]:
        return {name for name in names if name in EXCLUDED_DIRS or name == ".env"}

    shutil.copytree(ROOT, target, ignore=ignore)


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise AssertionError(f"expected one occurrence of {old!r} in {path}")
    path.write_text(text.replace(old, new), encoding="utf-8", newline="\n")


class RepositoryValidatorTests(unittest.TestCase):
    def validate_changed_copy(self, mutate) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "repository"
            copy_repository(copy)
            mutate(copy)
            return validate(copy, "final")

    def test_current_repository_and_schedule_are_valid(self) -> None:
        self.assertEqual([], validate(ROOT, "final"))

    def test_missing_required_file_is_rejected(self) -> None:
        errors = self.validate_changed_copy(lambda copy: (copy / "VERSION").unlink())
        self.assertTrue(any("VERSION" in error for error in errors), errors)

    def test_invalid_json_is_rejected(self) -> None:
        def mutate(copy: Path) -> None:
            (copy / "fixtures/nominal/dataset.json").write_text("{invalid", encoding="utf-8", newline="\n")

        errors = self.validate_changed_copy(mutate)
        self.assertTrue(any("JSON invalide" in error for error in errors), errors)

    def test_manifest_secret_is_rejected(self) -> None:
        def mutate(copy: Path) -> None:
            payload = "api_" + "key = \"" + ("A" * 24) + "\"\n"
            (copy / "leak.txt").write_text(payload, encoding="utf-8", newline="\n")

        errors = self.validate_changed_copy(mutate)
        self.assertTrue(any("secret manifeste" in error for error in errors), errors)

    def test_session_duration_must_equal_ffp_plus_tdp(self) -> None:
        def mutate(copy: Path) -> None:
            replace_once(
                copy / "manifest.yml",
                "  - id: session-01\n    duration_minutes: 240\n    ffp_minutes: 135\n    tdp_minutes: 105",
                "  - id: session-01\n    duration_minutes: 240\n    ffp_minutes: 135\n    tdp_minutes: 104",
            )

        errors = self.validate_changed_copy(mutate)
        self.assertTrue(any("duration_minutes doit égaler" in error for error in errors), errors)

    def test_session_totals_are_checked(self) -> None:
        def mutate(copy: Path) -> None:
            manifest = copy / "manifest.yml"
            replace_once(
                manifest,
                "  - id: session-01\n    duration_minutes: 240\n    ffp_minutes: 135\n    tdp_minutes: 105",
                "  - id: session-01\n    duration_minutes: 241\n    ffp_minutes: 135\n    tdp_minutes: 106",
            )

        errors = self.validate_changed_copy(mutate)
        self.assertTrue(any("total duration_minutes invalide" in error for error in errors), errors)
        self.assertTrue(any("total tdp_minutes invalide" in error for error in errors), errors)

    def test_ffp_and_tdp_totals_are_checked(self) -> None:
        def mutate(copy: Path) -> None:
            replace_once(
                copy / "manifest.yml",
                "  - id: session-02\n    duration_minutes: 180\n    ffp_minutes: 90\n    tdp_minutes: 90",
                "  - id: session-02\n    duration_minutes: 180\n    ffp_minutes: 91\n    tdp_minutes: 89",
            )

        errors = self.validate_changed_copy(mutate)
        self.assertTrue(any("total ffp_minutes invalide" in error for error in errors), errors)
        self.assertTrue(any("total tdp_minutes invalide" in error for error in errors), errors)

    def test_all_four_session_identifiers_are_required(self) -> None:
        def mutate(copy: Path) -> None:
            replace_once(copy / "manifest.yml", "  - id: session-04", "  - id: session-05")

        errors = self.validate_changed_copy(mutate)
        self.assertTrue(any("identifiants de séance invalides" in error for error in errors), errors)

    def test_brief_duration_must_match_manifest(self) -> None:
        def mutate(copy: Path) -> None:
            replace_once(copy / "briefs/session-02/README.md", "**Durée indicative :** 3 h", "**Durée indicative :** 4 h")

        errors = self.validate_changed_copy(mutate)
        self.assertTrue(any("session-02: ligne de durée" in error for error in errors), errors)

    def test_qcm_duration_is_45_minutes(self) -> None:
        def mutate(copy: Path) -> None:
            replace_once(copy / "manifest.yml", "  duration_minutes: 45", "  duration_minutes: 30")

        errors = self.validate_changed_copy(mutate)
        self.assertTrue(any("durée du QCM" in error for error in errors), errors)

    def test_qcm_is_included_in_session_04_tdp(self) -> None:
        def mutate(copy: Path) -> None:
            replace_once(copy / "manifest.yml", "  included_in_tdp: true", "  included_in_tdp: false")

        errors = self.validate_changed_copy(mutate)
        self.assertTrue(any("TDP de la séance 4" in error for error in errors), errors)

    def test_qcm_is_scheduled_in_session_04(self) -> None:
        def mutate(copy: Path) -> None:
            replace_once(copy / "manifest.yml", "  scheduled_session: session-04", "  scheduled_session: session-03")

        errors = self.validate_changed_copy(mutate)
        self.assertTrue(any("TDP de la séance 4" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
