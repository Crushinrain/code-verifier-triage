from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "scripts/verify_starter_manifest.py"
STARTER_MANIFEST = ROOT / "MANIFEST.sha256"
ACTIVE_MANIFEST = ".workflow/contracts.sha256"
EXCEPTION_PATH = "contracts/upstream.lock.yaml"
STARTER_HASH = (
    "d848388cef39739aed392a82f72d88515045220fcbc102568e6da4103783626f"
)
ACTIVE_HASH = (
    "c741c645cb07f7418dda3afe71a2e669e56fd00050601279cda3598a977b55bb"
)


def run_cli(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VERIFIER), str(root)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def assert_failed_for(
    result: subprocess.CompletedProcess[str], expected: str
) -> None:
    output = result.stdout + result.stderr
    assert result.returncode != 0, output
    assert expected in output, output


def isolated_snapshot(tmp_path: Path) -> Path:
    root = tmp_path / "snapshot"
    root.mkdir()
    for line in STARTER_MANIFEST.read_text(encoding="utf-8").splitlines():
        _expected, relative = line.split("  ", 1)
        source = ROOT / relative.removeprefix("./")
        target = root / relative.removeprefix("./")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    shutil.copy2(STARTER_MANIFEST, root / "MANIFEST.sha256")
    active_target = root / ACTIVE_MANIFEST
    active_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / ACTIVE_MANIFEST, active_target)
    return root


def replace_once(path: Path, old: str, new: str) -> None:
    content = path.read_text(encoding="utf-8")
    assert content.count(old) == 1
    path.write_text(content.replace(old, new), encoding="utf-8")


def test_current_t002_snapshot_passes_through_real_cli() -> None:
    result = run_cli(ROOT)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK: 90 immutable starter entries; 1 declared" in result.stdout


def test_second_delta_fails_through_real_cli(tmp_path: Path) -> None:
    root = isolated_snapshot(tmp_path)
    path = root / "contracts/project.yaml"
    path.write_bytes(path.read_bytes() + b"\n# second unauthorized delta\n")

    assert_failed_for(
        run_cli(root),
        "unexpected starter-manifest delta for ./contracts/project.yaml",
    )


def test_wrong_exception_path_fails_through_real_cli(tmp_path: Path) -> None:
    root = isolated_snapshot(tmp_path)
    replace_once(
        root / "MANIFEST.sha256",
        f"{STARTER_HASH}  ./{EXCEPTION_PATH}",
        f"{STARTER_HASH}  ./contracts/not-upstream.lock.yaml",
    )

    assert_failed_for(run_cli(root), "declared starter exception path is missing")


def test_wrong_baseline_hash_fails_through_real_cli(tmp_path: Path) -> None:
    root = isolated_snapshot(tmp_path)
    replace_once(root / "MANIFEST.sha256", STARTER_HASH, "0" * 64)

    assert_failed_for(run_cli(root), "starter exception baseline hash mismatch")


def test_wrong_active_hash_fails_through_real_cli(tmp_path: Path) -> None:
    root = isolated_snapshot(tmp_path)
    replace_once(root / ACTIVE_MANIFEST, ACTIVE_HASH, "f" * 64)

    assert_failed_for(run_cli(root), "active exception hash mismatch")


def test_workflow_uses_baseline_verifier_before_active_checks() -> None:
    workflow_text = (ROOT / ".github/workflows/contracts.yml").read_text(
        encoding="utf-8"
    )
    workflow = yaml.load(workflow_text, Loader=yaml.BaseLoader)
    runs = [
        step["run"]
        for step in workflow["jobs"]["contracts"]["steps"]
        if "run" in step
    ]
    starter = "python scripts/verify_starter_manifest.py ."
    active = "python scripts/check_active_contract_digest.py ."
    tests = "python -m pytest -q tests/test_contracts.py"

    assert "sha256sum --check MANIFEST.sha256" not in runs
    assert runs.count(starter) == 1
    assert runs.count(active) == 1
    assert runs.count(tests) == 1
    assert runs.index(starter) < runs.index(active) < runs.index(tests)
