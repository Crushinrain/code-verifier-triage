#!/usr/bin/env python3
"""Verify the ordered digest manifest for the active contract set."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path


ACTIVE_CONTRACT_PATHS = (
    "contracts/claims.yaml",
    "contracts/dataset_split.yaml",
    "contracts/evaluation.yaml",
    "contracts/execution.yaml",
    "contracts/extraction.yaml",
    "contracts/generation.yaml",
    "contracts/project.yaml",
    "contracts/resources_4x4090d.yaml",
    "contracts/reward.yaml",
    "contracts/risk_model.yaml",
    "contracts/rm_scoring.yaml",
    "contracts/routing.yaml",
    "contracts/security.yaml",
    "contracts/upstream.lock.yaml",
)
LINE = re.compile(r"^([0-9a-f]{64})  ([^\s]+)$")


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def parse_manifest(path: Path) -> list[tuple[str, str]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        fail(f"cannot read active contract digest {path}: {exc}")
    if not lines:
        fail("active contract digest is empty")
    records: list[tuple[str, str]] = []
    for number, line in enumerate(lines, start=1):
        match = LINE.fullmatch(line)
        if not match:
            fail(f"invalid digest line {number}: {line!r}")
        records.append((match.group(2), match.group(1)))
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", type=Path)
    parser.add_argument(
        "--manifest",
        default=".workflow/contracts.sha256",
        help="project-relative ordered digest manifest",
    )
    args = parser.parse_args()
    root = args.project_root.expanduser().resolve()
    if not root.is_dir():
        fail(f"project root is not a directory: {root}")

    actual_paths = tuple(
        path.relative_to(root).as_posix()
        for path in sorted((root / "contracts").glob("*.yaml"))
    )
    if actual_paths != ACTIVE_CONTRACT_PATHS:
        fail(
            "active contract path set differs from the explicit ordered set: "
            f"expected={ACTIVE_CONTRACT_PATHS!r}, actual={actual_paths!r}"
        )

    manifest_path = (root / args.manifest).resolve()
    try:
        manifest_path.relative_to(root)
    except ValueError:
        fail("digest manifest must stay inside the project root")
    records = parse_manifest(manifest_path)
    manifest_paths = tuple(path for path, _digest in records)
    if manifest_paths != ACTIVE_CONTRACT_PATHS:
        fail("digest manifest paths do not match the explicit ordered set")

    aggregate = hashlib.sha256()
    for relative, expected in records:
        content = (root / relative).read_bytes()
        actual = hashlib.sha256(content).hexdigest()
        if actual != expected:
            fail(
                f"active contract digest mismatch for {relative}: "
                f"expected {expected}, got {actual}"
            )
        aggregate.update(relative.encode("utf-8"))
        aggregate.update(b"\0")
        aggregate.update(content)
        aggregate.update(b"\0")
    print(
        f"OK: {len(records)} active contracts; "
        f"aggregate SHA-256 {aggregate.hexdigest()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
