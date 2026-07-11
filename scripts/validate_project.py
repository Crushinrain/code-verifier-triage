#!/usr/bin/env python3
"""Validate a CodeVerifier-Triage bundle at an explicit project root."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


REQUIRED_TASK_FIELDS = {
    "id",
    "title",
    "phase",
    "depends_on",
    "owner_role",
    "estimate_hours",
    "gate",
    "gpu_required",
    "human_approval_required",
    "actions",
    "acceptance_criteria",
    "outputs",
    "rollback",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def load_yaml(path: Path, label: str) -> object:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid YAML {label} {path}: {exc}")


def validate(root: Path) -> tuple[int, int, int]:
    contracts = sorted((root / "contracts").glob("*.yaml"))
    if not contracts:
        fail("no contracts found")
    for path in contracts:
        document = load_yaml(path, "contract")
        if not isinstance(document, dict) or not document:
            fail(f"contract must be a non-empty mapping: {path}")

    schemas = sorted((root / "schemas").glob("*.json"))
    if not schemas:
        fail("no schemas found")
    for path in schemas:
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            fail(f"invalid JSON Schema {path}: {exc}")

    graph_path = root / "tasks/task_graph.yaml"
    graph = load_yaml(graph_path, "task graph")
    if not isinstance(graph, dict) or not isinstance(graph.get("tasks"), list):
        fail("task_graph.yaml must contain a tasks list")
    task_list = graph["tasks"]
    if any(not isinstance(task, dict) for task in task_list):
        fail("each task must be a mapping")
    tasks = {task.get("id"): task for task in task_list}
    if None in tasks:
        fail("task without id")
    if len(tasks) != len(task_list):
        fail("duplicate task IDs")

    for task_id, task in tasks.items():
        missing_fields = sorted(REQUIRED_TASK_FIELDS - set(task))
        if missing_fields:
            fail(f"{task_id} missing fields {missing_fields}")
        if not isinstance(task_id, str) or not re.fullmatch(r"T\d{3}", task_id):
            fail(f"invalid task ID {task_id}")
        dependencies = task["depends_on"]
        if not isinstance(dependencies, list) or any(
            not isinstance(dependency, str) for dependency in dependencies
        ):
            fail(f"{task_id} depends_on must be a string list")
        if not isinstance(task["gate"], int) or isinstance(task["gate"], bool):
            fail(f"{task_id} invalid gate {task['gate']}")
        if not 0 <= task["gate"] <= 6:
            fail(f"{task_id} invalid gate {task['gate']}")
        estimate = task["estimate_hours"]
        if (
            not isinstance(estimate, (int, float))
            or isinstance(estimate, bool)
            or estimate <= 0
        ):
            fail(f"{task_id} invalid estimate_hours")
        for key in ("actions", "acceptance_criteria", "outputs"):
            if not isinstance(task[key], list) or not task[key]:
                fail(f"{task_id} {key} must be a non-empty list")
        if task["gpu_required"] and not task["human_approval_required"]:
            fail(f"{task_id} GPU task lacks human approval")
        missing_dependencies = [
            dependency for dependency in dependencies if dependency not in tasks
        ]
        if missing_dependencies:
            fail(f"{task_id} has missing dependencies {missing_dependencies}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str) -> None:
        if task_id in visiting:
            fail(f"dependency cycle at {task_id}")
        if task_id in visited:
            return
        visiting.add(task_id)
        for dependency in tasks[task_id]["depends_on"]:
            visit(dependency)
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in tasks:
        visit(task_id)

    for gate in range(7):
        if not (root / f"checklists/gate{gate}.md").is_file():
            fail(f"missing Gate {gate} checklist")

    approvals = load_yaml(root / "approvals/HUMAN_APPROVALS.yaml", "approvals")
    if not isinstance(approvals, dict):
        fail("approvals document must be a mapping")
    approval_records = approvals.get("approvals", {})
    if not isinstance(approval_records, dict):
        fail("approvals must be a mapping")
    allowed_status = {"PENDING", "APPROVED", "DENIED", "REVOKED"}
    for key, record in approval_records.items():
        if not isinstance(record, dict) or record.get("status") not in allowed_status:
            fail(f"approval {key} has invalid status")

    return len(contracts), len(schemas), len(tasks)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", type=Path)
    args = parser.parse_args()
    root = args.project_root.expanduser().resolve()
    if not root.is_dir():
        fail(f"project root is not a directory: {root}")
    counts = validate(root)
    print(
        f"OK: {counts[0]} contracts, {counts[1]} schemas, "
        f"{counts[2]} tasks, 7 Gate checklists"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
