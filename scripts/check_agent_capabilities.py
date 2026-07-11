#!/usr/bin/env python3
"""Non-destructive local capability inventory for the Agent starter pack."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
from typing import Any


def run(cmd: list[str], timeout: int = 10) -> dict[str, Any]:
    try:
        p = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout, check=False)
        return {
            "returncode": p.returncode,
            "stdout": p.stdout.strip()[:8000],
            "stderr": p.stderr.strip()[:4000],
        }
    except Exception as exc:  # inventory must report, not hide, failures
        return {"error": type(exc).__name__, "message": str(exc)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=None)
    ap.add_argument("--deep", action="store_true", help="also probe Docker daemon and nvidia-smi")
    args = ap.parse_args()

    root = Path.cwd()
    tools = {name: shutil.which(name) for name in ["git", "docker", "nvidia-smi", "make", "bash"]}
    disk = shutil.disk_usage(root)
    report: dict[str, Any] = {
        "schema_version": 1,
        "cwd": str(root.resolve()),
        "python": {"version": sys.version, "executable": sys.executable},
        "platform": platform.platform(),
        "user": {"uid": getattr(os, "getuid", lambda: None)(), "euid": getattr(os, "geteuid", lambda: None)()},
        "writable_cwd": os.access(root, os.W_OK),
        "tools": tools,
        "disk": {
            "total_gb": round(disk.total / 2**30, 2),
            "free_gb": round(disk.free / 2**30, 2),
        },
        "notes": [
            "Tool visibility is not a security or compatibility approval.",
            "Candidate code must never be executed on the host merely because Python/subprocess is available.",
        ],
    }
    if args.deep:
        if tools["git"]:
            report["git_version"] = run([tools["git"], "--version"])
        if tools["docker"]:
            report["docker_version"] = run([tools["docker"], "version", "--format", "{{json .}}"], timeout=15)
        if tools["nvidia-smi"]:
            report["gpu_inventory"] = run([
                tools["nvidia-smi"],
                "--query-gpu=index,name,memory.total,driver_version,uuid",
                "--format=csv,noheader",
            ], timeout=15)
            report["gpu_topology"] = run([tools["nvidia-smi"], "topo", "-m"], timeout=15)

    text = json.dumps(report, ensure_ascii=False, indent=2)
    print(text)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
