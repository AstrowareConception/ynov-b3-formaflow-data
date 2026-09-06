#!/usr/bin/env python3
"""Build the deterministic FormaFlow Data educational ZIP."""

from __future__ import annotations

import hashlib
from pathlib import Path
import sys
import zipfile

from validate_repository import EXCLUDED_DIRS, is_text_path, validate, validate_archive


ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.0.0"
ARCHIVE_ROOT = f"ynov-b3-formaflow-data-v{VERSION}"
ARCHIVE_NAME = f"ynov-b3-formaflow-data-v{VERSION}.zip"
REVIEW_BUNDLE_NAME = f"ynov-b3-formaflow-data-v{VERSION}-review.bundle"
NORMALIZED_TIME = (2026, 1, 1, 0, 0, 0)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def distributable_files(root: Path):
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        if not path.is_file():
            continue
        name = path.name
        if name == ".env" or (name.startswith(".env.") and name != ".env.example"):
            continue
        if name.endswith((".zip", ".bundle", ".pyc", ".pyo", ".log", ".tmp", ".temp", "~")):
            continue
        yield path


def archive_payload(path: Path) -> bytes:
    payload = path.read_bytes()
    if not is_text_path(path):
        return payload
    try:
        text = payload.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"declared text file is not UTF-8: {path}") from exc
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def write_checksums(dist: Path, archive_path: Path) -> None:
    artifacts = [archive_path]
    bundle = dist / REVIEW_BUNDLE_NAME
    if bundle.is_file():
        artifacts.append(bundle)
    lines = [f"{sha256(path)}  {path.name}" for path in sorted(artifacts, key=lambda item: item.name)]
    (dist / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")


def build(root: Path = ROOT) -> Path:
    root = root.resolve()
    errors = validate(root, "final")
    if errors:
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise RuntimeError(f"packaging refused: {len(errors)} validation error(s)")
    dist = root / "dist"
    dist.mkdir(parents=True, exist_ok=True)
    target = dist / ARCHIVE_NAME
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in distributable_files(root):
            relative = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(f"{ARCHIVE_ROOT}/{relative}", date_time=NORMALIZED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (0o100644 & 0xFFFF) << 16
            info.flag_bits |= 0x800
            archive.writestr(info, archive_payload(path), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    archive_errors = validate_archive(target)
    if archive_errors:
        raise RuntimeError("archive validation failed: " + "; ".join(archive_errors))
    digest = sha256(target)
    write_checksums(dist, target)
    print(f"Archive: {target}")
    print(f"Files: {sum(1 for _ in distributable_files(root))}")
    print(f"SHA-256: {digest}")
    return target


if __name__ == "__main__":
    try:
        build()
    except RuntimeError as exc:
        print(f"ERREUR: {exc}", file=sys.stderr)
        raise SystemExit(1)
