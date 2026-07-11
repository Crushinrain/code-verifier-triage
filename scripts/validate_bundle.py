#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import re
import sys
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


contracts = sorted((ROOT / "contracts").glob("*.yaml"))
for p in contracts:
    try:
        obj = yaml.safe_load(p.read_text(encoding="utf-8"))
        if obj is None:
            fail(f"empty YAML {p}")
    except Exception as e:
        fail(f"invalid YAML {p}: {e}")

schemas = sorted((ROOT / "schemas").glob("*.json"))
for p in schemas:
    try:
        schema = json.loads(p.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except Exception as e:
        fail(f"invalid JSON Schema {p}: {e}")

graph = yaml.safe_load((ROOT / "tasks/task_graph.yaml").read_text(encoding="utf-8"))
if not isinstance(graph, dict) or not isinstance(graph.get("tasks"), list):
    fail("task_graph.yaml must contain a tasks list")

task_list = graph["tasks"]
tasks = {t.get("id"): t for t in task_list}
if None in tasks:
    fail("task without id")
if len(tasks) != len(task_list):
    fail("duplicate task IDs")

required = {
    "id", "title", "phase", "depends_on", "owner_role", "estimate_hours", "gate",
    "gpu_required", "human_approval_required", "actions", "acceptance_criteria", "outputs", "rollback",
}
for tid, t in tasks.items():
    missing_fields = sorted(required - set(t))
    if missing_fields:
        fail(f"{tid} missing fields {missing_fields}")
    if not re.fullmatch(r"T\d{3}", tid):
        fail(f"invalid task ID {tid}")
    if not isinstance(t["gate"], int) or not (0 <= t["gate"] <= 6):
        fail(f"{tid} invalid gate {t['gate']}")
    if not isinstance(t["estimate_hours"], (int, float)) or t["estimate_hours"] <= 0:
        fail(f"{tid} invalid estimate_hours")
    for key in ["actions", "acceptance_criteria", "outputs"]:
        if not isinstance(t[key], list) or not t[key]:
            fail(f"{tid} {key} must be non-empty list")
    if t["gpu_required"] and not t["human_approval_required"]:
        fail(f"{tid} GPU task lacks human approval")
    missing_deps = [d for d in t.get("depends_on", []) if d not in tasks]
    if missing_deps:
        fail(f"{tid} has missing dependencies {missing_deps}")
    if tid in t.get("depends_on", []):
        fail(f"{tid} depends on itself")

visiting, visited = set(), set()

def dfs(tid: str) -> None:
    if tid in visiting:
        fail(f"dependency cycle at {tid}")
    if tid in visited:
        return
    visiting.add(tid)
    for dep in tasks[tid].get("depends_on", []):
        dfs(dep)
    visiting.remove(tid)
    visited.add(tid)

for tid in tasks:
    dfs(tid)

for gate in range(7):
    if not (ROOT / f"checklists/gate{gate}.md").is_file():
        fail(f"missing Gate {gate} checklist")

approvals_path = ROOT / "approvals/HUMAN_APPROVALS.yaml"
approvals = yaml.safe_load(approvals_path.read_text(encoding="utf-8"))
allowed_status = {"PENDING", "APPROVED", "DENIED", "REVOKED"}
for key, record in approvals.get("approvals", {}).items():
    if record.get("status") not in allowed_status:
        fail(f"approval {key} has invalid status {record.get('status')}")

print(f"OK: {len(contracts)} contracts, {len(schemas)} schemas, {len(tasks)} tasks, 7 Gate checklists")
