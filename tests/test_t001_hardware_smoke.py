from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "t001_hardware_smoke", ROOT / "scripts" / "t001_hardware_smoke.py"
)
assert SPEC and SPEC.loader
smoke = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(smoke)


def completed_rank(rank: int) -> dict:
    return {
        "rank": rank,
        "local_rank": rank,
        "pid": 1000 + rank,
        "gpu_index": rank,
        "status": "COMPLETED",
        "elapsed_seconds": 1800.25,
        "collectives": 900,
        "integrity_checks": 900,
        "peak_allocated_bytes": 15 * smoke.GIB,
        "error": None,
    }


def test_atomic_json_is_immediately_machine_readable(tmp_path: Path) -> None:
    target = tmp_path / "nested" / "evidence.json"
    smoke.atomic_write_json(target, {"status": "RUNNING", "sequence": 1})
    smoke.atomic_write_json(target, {"status": "PASS", "sequence": 2})
    assert json.loads(target.read_text(encoding="utf-8")) == {
        "status": "PASS",
        "sequence": 2,
    }
    assert list(target.parent.glob("*.tmp")) == []


def test_compute_process_parser_handles_empty_and_real_rows() -> None:
    assert smoke.parse_compute_apps("") == []
    rows = smoke.parse_compute_apps(
        "GPU-a, 123, /usr/bin/python, 4096 MiB\nGPU-b, 456, python, 8192 MiB\n"
    )
    assert rows == [
        {
            "gpu_uuid": "GPU-a",
            "pid": 123,
            "process_name": "/usr/bin/python",
            "used_gpu_memory_mib": 4096,
        },
        {
            "gpu_uuid": "GPU-b",
            "pid": 456,
            "process_name": "python",
            "used_gpu_memory_mib": 8192,
        },
    ]


def test_four_complete_ranks_and_release_are_required_for_pass() -> None:
    result = smoke.assess_run(
        ranks=[completed_rank(i) for i in range(4)],
        requested_duration=1800,
        memory_limit_bytes=16 * smoke.GIB,
        controller_rc=0,
        monitor_issues=[],
        release={"released": True, "remaining_task_pids": []},
        stop_reason=None,
    )
    assert result == {"status": "PASS", "failures": []}


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [
        (lambda ranks: ranks[:3], "expected exactly four rank records"),
        (
            lambda ranks: [dict(ranks[0], elapsed_seconds=1799.99), *ranks[1:]],
            "rank 0 elapsed below required duration",
        ),
        (
            lambda ranks: [dict(ranks[0], peak_allocated_bytes=16 * smoke.GIB + 1), *ranks[1:]],
            "rank 0 exceeded memory limit",
        ),
    ],
)
def test_run_assessment_fails_closed(mutation, expected: str) -> None:
    result = smoke.assess_run(
        ranks=mutation([completed_rank(i) for i in range(4)]),
        requested_duration=1800,
        memory_limit_bytes=16 * smoke.GIB,
        controller_rc=0,
        monitor_issues=[],
        release={"released": True, "remaining_task_pids": []},
        stop_reason=None,
    )
    assert result["status"] == "FAILED"
    assert expected in result["failures"]


def test_pause_can_never_be_promoted_to_pass() -> None:
    result = smoke.assess_run(
        ranks=[dict(completed_rank(i), status="PAUSED", elapsed_seconds=600) for i in range(4)],
        requested_duration=1800,
        memory_limit_bytes=16 * smoke.GIB,
        controller_rc=0,
        monitor_issues=[],
        release={"released": True, "remaining_task_pids": []},
        stop_reason="PAUSED",
    )
    assert result["status"] == "PAUSED"
    assert result["failures"]


def test_failed_release_overrides_pause_status() -> None:
    result = smoke.assess_run(
        ranks=[dict(completed_rank(i), status="PAUSED") for i in range(4)],
        requested_duration=1800,
        memory_limit_bytes=16 * smoke.GIB,
        controller_rc=0,
        monitor_issues=[],
        release={"released": False, "remaining_task_pids": [1000]},
        stop_reason="PAUSED",
    )
    assert result["status"] == "FAILED"
