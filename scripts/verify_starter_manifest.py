#!/usr/bin/env python3
"""Verify the immutable starter snapshot with one declared T002 exception."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path, PurePosixPath


STARTER_MANIFEST = "MANIFEST.sha256"
ACTIVE_CONTRACT_MANIFEST = ".workflow/contracts.sha256"
STARTER_RECORD_COUNT = 91
EXCEPTION_PATH = "contracts/upstream.lock.yaml"
EXCEPTION_STARTER_PATH = f"./{EXCEPTION_PATH}"
EXCEPTION_STARTER_SHA256 = (
    "d848388cef39739aed392a82f72d88515045220fcbc102568e6da4103783626f"
)
EXCEPTION_ACTIVE_SHA256 = (
    "c741c645cb07f7418dda3afe71a2e669e56fd00050601279cda3598a977b55bb"
)
LINE = re.compile(r"^([0-9a-f]{64})  ([^\s]+)$")


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def digest(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        fail(f"cannot read {path}: {exc}")


def parse_manifest(path: Path, label: str) -> list[tuple[str, str]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        fail(f"cannot read {label} {path}: {exc}")
    if not lines:
        fail(f"{label} is empty")

    records: list[tuple[str, str]] = []
    seen: set[str] = set()
    for number, line in enumerate(lines, start=1):
        match = LINE.fullmatch(line)
        if not match:
            fail(f"invalid {label} line {number}: {line!r}")
        expected, relative = match.groups()
        if relative in seen:
            fail(f"duplicate path in {label}: {relative}")
        seen.add(relative)
        records.append((relative, expected))
    return records


def project_path(root: Path, relative: str) -> Path:
    if not relative.startswith("./"):
        fail(f"starter manifest path must start with './': {relative}")
    clean = relative[2:]
    pure = PurePosixPath(clean)
    if not clean or pure.is_absolute() or ".." in pure.parts:
        fail(f"unsafe starter manifest path: {relative}")
    path = (root / Path(*pure.parts)).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        fail(f"starter manifest path escapes project root: {relative}")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", type=Path)
    args = parser.parse_args()

    root = args.project_root.expanduser().resolve()
    if not root.is_dir():
        fail(f"project root is not a directory: {root}")

    starter_records = parse_manifest(root / STARTER_MANIFEST, "starter manifest")
    if len(starter_records) != STARTER_RECORD_COUNT:
        fail(
            "starter manifest record count changed: "
            f"expected {STARTER_RECORD_COUNT}, got {len(starter_records)}"
        )

    starter_exceptions = [
        expected
        for relative, expected in starter_records
        if relative == EXCEPTION_STARTER_PATH
    ]
    if len(starter_exceptions) != 1:
        fail(
            "declared starter exception path is missing or altered: "
            f"{EXCEPTION_STARTER_PATH}"
        )
    if starter_exceptions[0] != EXCEPTION_STARTER_SHA256:
        fail(
            "starter exception baseline hash mismatch: "
            f"expected {EXCEPTION_STARTER_SHA256}, got {starter_exceptions[0]}"
        )

    active_records = parse_manifest(
        root / ACTIVE_CONTRACT_MANIFEST, "active contract manifest"
    )
    active_hashes = {
        expected
        for relative, expected in active_records
        if relative == EXCEPTION_PATH
    }
    if active_hashes != {EXCEPTION_ACTIVE_SHA256}:
        fail(
            "active exception hash mismatch: "
            f"{EXCEPTION_PATH} must be {EXCEPTION_ACTIVE_SHA256}, "
            f"got {sorted(active_hashes)!r}"
        )

    exception_actual = digest(root / EXCEPTION_PATH)
    if exception_actual != EXCEPTION_ACTIVE_SHA256:
        fail(
            "current exception content hash mismatch: "
            f"expected {EXCEPTION_ACTIVE_SHA256}, got {exception_actual}"
        )

    mismatches: list[tuple[str, str, str]] = []
    for relative, expected in starter_records:
        actual = digest(project_path(root, relative))
        if actual != expected:
            mismatches.append((relative, expected, actual))

    unexpected = [item for item in mismatches if item[0] != EXCEPTION_STARTER_PATH]
    if unexpected:
        relative, expected, actual = unexpected[0]
        fail(
            f"unexpected starter-manifest delta for {relative}: "
            f"expected {expected}, got {actual}"
        )
    if mismatches != [
        (
            EXCEPTION_STARTER_PATH,
            EXCEPTION_STARTER_SHA256,
            EXCEPTION_ACTIVE_SHA256,
        )
    ]:
        fail(
            "declared starter exception is not the sole exact baseline-to-active "
            f"delta: {mismatches!r}"
        )

    print(
        "OK: 90 immutable starter entries; 1 declared baseline-to-active "
        f"exception for {EXCEPTION_PATH}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
