from __future__ import annotations

import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
from package_repository import archive_payload  # noqa: E402
from validate_repository import EXCLUDED_DIRS, is_text_path  # noqa: E402

ARCHIVE_NAME = "ynov-b3-formaflow-data-v1.0.0.zip"
ARCHIVE_ROOT = "ynov-b3-formaflow-data-v1.0.0"
CRLF_SAMPLES = (
    "README.md",
    "manifest.yml",
    "fixtures/nominal/dataset.json",
    "scripts/package_repository.py",
    "sql/schema/020_tables.sql",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_repository(source: Path, target: Path) -> None:
    def ignore(_directory: str, names: list[str]) -> set[str]:
        return {name for name in names if name in EXCLUDED_DIRS or name == ".env"}

    shutil.copytree(source, target, ignore=ignore)


def run_package(root: Path) -> Path:
    result = subprocess.run(
        [sys.executable, "scripts/package_repository.py"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        raise AssertionError(result.stdout + result.stderr)
    return root / "dist" / ARCHIVE_NAME


class DeterministicPackagingIntegrationTests(unittest.TestCase):
    def assert_valid_archive(self, path: Path) -> None:
        with zipfile.ZipFile(path) as archive:
            self.assertIsNone(archive.testzip())
            names = archive.namelist()
            self.assertEqual({ARCHIVE_ROOT}, {name.split("/", 1)[0] for name in names})
            self.assertFalse(
                any(
                    "/_inputs/" in name
                    or "/dist/" in name
                    or "/build/" in name
                    or "/.git/" in name
                    or "/.idea/" in name
                    for name in names
                )
            )
            for name in names:
                if is_text_path(Path(name)):
                    payload = archive.read(name)
                    payload.decode("utf-8")
                    self.assertNotIn(b"\r", payload, name)

    def test_worktree_git_archive_crlf_and_extracted_rebuild_are_identical(self) -> None:
        original = run_package(ROOT)
        self.assert_valid_archive(original)
        expected_hash = sha256(original)
        git_ref = os.environ.get("PACKAGE_GIT_REF", "HEAD")

        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            git_zip = temporary / "git-archive.zip"
            archived = subprocess.run(
                ["git", "archive", "--format=zip", "--output", str(git_zip), git_ref],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, archived.returncode, archived.stdout + archived.stderr)
            git_root = temporary / "git-checkout"
            git_root.mkdir()
            with zipfile.ZipFile(git_zip) as archive:
                archive.extractall(git_root)
            git_package = run_package(git_root)

            crlf_root = temporary / "crlf-checkout"
            copy_repository(ROOT, crlf_root)
            for relative in CRLF_SAMPLES:
                path = crlf_root / relative
                payload = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
                path.write_bytes(payload.replace(b"\n", b"\r\n"))
            crlf_package = run_package(crlf_root)

            extracted_root = temporary / "zip-extraction"
            with zipfile.ZipFile(original) as archive:
                archive.extractall(extracted_root)
            extracted = extracted_root / ARCHIVE_ROOT
            validation = subprocess.run(
                [sys.executable, "scripts/validate_repository.py"],
                cwd=extracted,
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, validation.returncode, validation.stdout + validation.stderr)
            rebuilt_package = run_package(extracted)

            for package in (git_package, crlf_package, rebuilt_package):
                self.assert_valid_archive(package)
                self.assertEqual(expected_hash, sha256(package), package)

    def test_binary_payload_is_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.png"
            payload = b"\x89PNG\r\n\x1a\n\x00\xff\r\n"
            path.write_bytes(payload)
            self.assertEqual(payload, archive_payload(path))


if __name__ == "__main__":
    unittest.main()
