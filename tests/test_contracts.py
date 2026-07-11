from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_project.py"
DIGEST_CHECKER = ROOT / "scripts/check_active_contract_digest.py"
FIXTURE_PATHS = (
    "contracts",
    "schemas",
    "tasks",
    "checklists",
    "approvals",
    ".workflow",
)


def run_cli(script: Path, root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), str(root)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def isolated_bundle(tmp_path: Path) -> Path:
    root = tmp_path / "bundle"
    root.mkdir()
    for relative in FIXTURE_PATHS:
        source = ROOT / relative
        target = root / relative
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    return root


def assert_failed_for(
    result: subprocess.CompletedProcess[str], expected: str
) -> None:
    output = result.stdout + result.stderr
    assert result.returncode != 0, output
    assert expected in output, output


def load_task_graph(root: Path) -> tuple[Path, dict[str, object]]:
    path = root / "tasks/task_graph.yaml"
    graph = yaml.safe_load(path.read_text(encoding="utf-8"))
    return path, graph


def write_task_graph(path: Path, graph: dict[str, object]) -> None:
    path.write_text(
        yaml.safe_dump(graph, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def task(graph: dict[str, object], task_id: str) -> dict[str, object]:
    return next(item for item in graph["tasks"] if item["id"] == task_id)


def test_valid_starter_bundle_and_active_digest() -> None:
    validation = run_cli(VALIDATOR, ROOT)
    assert validation.returncode == 0, validation.stdout + validation.stderr
    assert "OK: 14 contracts, 6 schemas, 69 tasks" in validation.stdout

    digest = run_cli(DIGEST_CHECKER, ROOT)
    assert digest.returncode == 0, digest.stdout + digest.stderr
    assert "OK: 14 active contracts" in digest.stdout


def test_malformed_schema_fails_through_real_cli(tmp_path: Path) -> None:
    root = isolated_bundle(tmp_path)
    path = root / "schemas/candidate.schema.json"
    path.write_text('{"type": "not-a-json-schema-type"}\n', encoding="utf-8")

    assert_failed_for(run_cli(VALIDATOR, root), "invalid JSON Schema")


def test_schema_invalid_document_fails_through_real_cli(tmp_path: Path) -> None:
    root = isolated_bundle(tmp_path)
    path, graph = load_task_graph(root)
    task(graph, "T005")["gate"] = "zero"
    write_task_graph(path, graph)

    assert_failed_for(run_cli(VALIDATOR, root), "T005 invalid gate")


def test_missing_dependency_fails_through_real_cli(tmp_path: Path) -> None:
    root = isolated_bundle(tmp_path)
    path, graph = load_task_graph(root)
    task(graph, "T005")["depends_on"].append("T999")
    write_task_graph(path, graph)

    assert_failed_for(run_cli(VALIDATOR, root), "missing dependencies ['T999']")


def test_dependency_cycle_fails_through_real_cli(tmp_path: Path) -> None:
    root = isolated_bundle(tmp_path)
    path, graph = load_task_graph(root)
    task(graph, "T000")["depends_on"].append("T005")
    write_task_graph(path, graph)

    assert_failed_for(run_cli(VALIDATOR, root), "dependency cycle")


def test_active_contract_freeze_drift_fails_through_real_cli(
    tmp_path: Path,
) -> None:
    root = isolated_bundle(tmp_path)
