#!/usr/bin/env python3
"""T001 machine inventory and four-rank NCCL synthetic smoke.

The controller owns evidence, pause/stop handling, health monitoring, and GPU
release proof.  The worker is launched only through torchrun and uses no model,
dataset, optimizer, trainer, candidate program, Docker image, or network service.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
import traceback
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

GIB = 1024**3
MIB = 1024**2
GPU_COUNT = 4
PAUSE_SENTINEL = Path("/data3/xc/code-verifier-triage/.git/T001.PAUSE")
NVIDIA_SMI = "/usr/bin/nvidia-smi"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass


def atomic_write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass


def command(argv: list[str], timeout: float = 30) -> dict[str, Any]:
    started = time.monotonic()
    try:
        proc = subprocess.run(
            argv,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "argv": argv,
            "rc": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "elapsed_seconds": round(time.monotonic() - started, 6),
        }
    except Exception as exc:
        return {
            "argv": argv,
            "rc": None,
            "stdout": "",
            "stderr": f"{type(exc).__name__}: {exc}",
            "elapsed_seconds": round(time.monotonic() - started, 6),
        }


def parse_compute_apps(text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in csv.reader(line for line in text.splitlines() if line.strip()):
        if len(row) != 4:
            continue
        gpu_uuid, pid, process_name, memory = (part.strip() for part in row)
        try:
            rows.append(
                {
                    "gpu_uuid": gpu_uuid,
                    "pid": int(pid),
                    "process_name": process_name,
                    "used_gpu_memory_mib": int(memory.removesuffix(" MiB").strip()),
                }
            )
        except ValueError:
            continue
    return rows


def compute_apps() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    result = command(
        [
            NVIDIA_SMI,
            "--query-compute-apps=gpu_uuid,pid,process_name,used_gpu_memory",
            "--format=csv,noheader,nounits",
        ]
    )
    return parse_compute_apps(result["stdout"]), result


def gpu_snapshot() -> dict[str, Any]:
    query = command(
        [
            NVIDIA_SMI,
            "--query-gpu=index,uuid,name,driver_version,memory.total,memory.used,memory.free,temperature.gpu,pstate,power.draw,ecc.errors.corrected.volatile.total,ecc.errors.uncorrected.volatile.total",
            "--format=csv,noheader,nounits",
        ]
    )
    fields = [
        "index", "uuid", "name", "driver_version", "memory_total_mib",
        "memory_used_mib", "memory_free_mib", "temperature_c", "pstate",
        "power_w", "ecc_corrected_volatile", "ecc_uncorrected_volatile",
    ]
    gpus: list[dict[str, Any]] = []
    for row in csv.reader(line for line in query["stdout"].splitlines() if line.strip()):
        if len(row) == len(fields):
            gpus.append(dict(zip(fields, (cell.strip() for cell in row))))
    apps, apps_raw = compute_apps()
    return {"observed_at": utc_now(), "query": query, "gpus": gpus, "compute_apps": apps, "compute_apps_query": apps_raw}


def filesystem_snapshot(path: str) -> dict[str, Any]:
    usage = shutil.disk_usage(path)
    return {
        "path": path,
        "total_bytes": usage.total,
        "used_bytes": usage.used,
        "free_bytes": usage.free,
        "df": command(["/usr/bin/df", "-PT", "-B1", path]),
    }


def collect_inventory(output: Path) -> dict[str, Any]:
    meminfo: dict[str, str] = {}
    for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meminfo[key] = value.strip()
    cgroup_controllers = Path("/sys/fs/cgroup/cgroup.controllers")
    docker = {
        "executable": shutil.which("docker"),
        "client_server": command([shutil.which("docker") or "/usr/bin/docker", "version", "--format", "{{json .}}"]),
        "info": command([shutil.which("docker") or "/usr/bin/docker", "info", "--format", "{{json .}}"]),
    }
    inventory = {
        "schema_version": 1,
        "generated_at": utc_now(),
        "host": {
            "hostname": socket.gethostname(),
            "fqdn": socket.getfqdn(),
            "platform": platform.platform(),
            "os_release": dict(line.split("=", 1) for line in Path("/etc/os-release").read_text(encoding="utf-8").splitlines() if "=" in line),
            "kernel": platform.release(),
            "machine": platform.machine(),
        },
        "cpu": {
            "logical_count": os.cpu_count(),
            "lscpu": command(["/usr/bin/lscpu", "--json"]),
        },
        "memory": {"meminfo": meminfo, "free": command(["/usr/bin/free", "-b"])},
        "filesystems": [filesystem_snapshot("/"), filesystem_snapshot("/tmp"), filesystem_snapshot("/data3")],
        "cgroups_v2": {
            "mounted": cgroup_controllers.exists(),
            "controllers": cgroup_controllers.read_text(encoding="utf-8").strip().split() if cgroup_controllers.exists() else [],
            "mount": command(["/usr/bin/findmnt", "-J", "-t", "cgroup2"]),
        },
        "docker": docker,
        "nvidia": {
            "snapshot": gpu_snapshot(),
            "smi": command([NVIDIA_SMI]),
            "topology": command([NVIDIA_SMI, "topo", "-m"]),
            "driver_runtime": command([NVIDIA_SMI, "-q"]),
        },
    }
    atomic_write_json(output, inventory)
    return inventory


def assess_run(
    *, ranks: list[dict[str, Any]], requested_duration: float,
    memory_limit_bytes: int, controller_rc: int | None,
    monitor_issues: list[str], release: dict[str, Any], stop_reason: str | None,
) -> dict[str, Any]:
    failures: list[str] = []
    if len(ranks) != GPU_COUNT:
        failures.append("expected exactly four rank records")
    seen = set()
    for item in ranks:
        rank = item.get("rank")
        if rank in seen:
            failures.append(f"duplicate rank {rank}")
        seen.add(rank)
        if item.get("status") != "COMPLETED":
            failures.append(f"rank {rank} status is {item.get('status')}")
        if float(item.get("elapsed_seconds", 0)) < requested_duration:
            failures.append(f"rank {rank} elapsed below required duration")
        if int(item.get("peak_allocated_bytes", memory_limit_bytes + 1)) > memory_limit_bytes:
            failures.append(f"rank {rank} exceeded memory limit")
        if int(item.get("collectives", 0)) <= 0 or int(item.get("integrity_checks", 0)) <= 0:
            failures.append(f"rank {rank} missing NCCL integrity evidence")
        if item.get("error"):
            failures.append(f"rank {rank} error: {item['error']}")
    if controller_rc not in (0, None):
        failures.append(f"torchrun exited {controller_rc}")
    failures.extend(f"monitor: {issue}" for issue in monitor_issues)
    if not release.get("released") or release.get("remaining_task_pids"):
        failures.append("GPU release proof failed")
    if stop_reason:
        failures.append(f"run interrupted with {stop_reason}")
    if failures:
        status = stop_reason if stop_reason in {"PAUSED", "STOPPED"} and "GPU release proof failed" not in failures else "FAILED"
    else:
        status = "PASS"
    return {"status": status, "failures": failures}


class XidMonitor:
    def __init__(self) -> None:
        import pynvml
        self.nvml = pynvml
        pynvml.nvmlInit()
        self.event_set = pynvml.nvmlEventSetCreate()
        self.devices = []
        for index in range(GPU_COUNT):
            handle = pynvml.nvmlDeviceGetHandleByIndex(index)
            pynvml.nvmlDeviceRegisterEvents(handle, pynvml.nvmlEventTypeXidCriticalError, self.event_set)
            self.devices.append(handle)

    def poll(self) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []
        while True:
            try:
                data = self.nvml.nvmlEventSetWait_v2(self.event_set, 1)
                events.append({"device_index": data.device, "event_type": data.eventType, "event_data": data.eventData})
            except self.nvml.NVMLError_Timeout:
                break
        return events

    def close(self) -> None:
        try:
            self.nvml.nvmlEventSetFree(self.event_set)
        finally:
            self.nvml.nvmlShutdown()


def wait_for_idle(timeout_seconds: float, interval_seconds: float, sentinel: Path) -> dict[str, Any]:
    started = time.monotonic()
    observations = []
    while True:
        apps, raw = compute_apps()
        observations.append({"at": utc_now(), "apps": apps, "query_rc": raw["rc"]})
        if raw["rc"] != 0:
            raise RuntimeError(f"nvidia-smi compute query failed: {raw['stderr']}")
        if not apps:
            snap = gpu_snapshot()
            if len(snap["gpus"]) != GPU_COUNT:
                raise RuntimeError(f"expected four GPUs, observed {len(snap['gpus'])}")
            if any(int(gpu["memory_free_mib"]) < 17 * 1024 for gpu in snap["gpus"]):
                apps = [{"reason": "insufficient memory headroom", "gpu": gpu} for gpu in snap["gpus"] if int(gpu["memory_free_mib"]) < 17 * 1024]
            else:
                return {"idle": True, "observations": observations, "snapshot": snap}
        if sentinel.exists():
            return {"idle": False, "paused": True, "observations": observations}
        if timeout_seconds >= 0 and time.monotonic() - started >= timeout_seconds:
            return {"idle": False, "timed_out": True, "observations": observations, "foreign_processes": apps}
        time.sleep(interval_seconds)


def read_rank_records(run_dir: Path) -> list[dict[str, Any]]:
    records = []
    for path in sorted(run_dir.glob("rank_*.final.json")):
        try:
            records.append(json.loads(path.read_text(encoding="utf-8")))
        except Exception:
            continue
    return sorted(records, key=lambda item: item.get("rank", -1))


def known_task_pids(run_dir: Path) -> set[int]:
    pids: set[int] = set()
    for pattern in ("rank_*.start.json", "rank_*.heartbeat.json", "rank_*.final.json"):
        for path in run_dir.glob(pattern):
            try:
                pids.add(int(json.loads(path.read_text(encoding="utf-8"))["pid"]))
            except Exception:
                pass
    return pids


def prove_release(run_dir: Path, timeout_seconds: float = 120) -> dict[str, Any]:
    task_pids = known_task_pids(run_dir)
    observations = []
    deadline = time.monotonic() + timeout_seconds
    while True:
        apps, raw = compute_apps()
        active_gpu = sorted({item["pid"] for item in apps} & task_pids)
        active_os = sorted(pid for pid in task_pids if Path(f"/proc/{pid}").exists())
        observations.append({"at": utc_now(), "active_gpu_pids": active_gpu, "active_os_pids": active_os, "query_rc": raw["rc"]})
        if raw["rc"] == 0 and not active_gpu and not active_os:
            return {"released": True, "task_pids": sorted(task_pids), "remaining_task_pids": [], "observations": observations}
        if time.monotonic() >= deadline:
            return {"released": False, "task_pids": sorted(task_pids), "remaining_task_pids": sorted(set(active_gpu + active_os)), "observations": observations}
        time.sleep(2)


def hash_evidence(run_dir: Path) -> Path:
    output = run_dir / "evidence.sha256"
    lines = []
    for path in sorted(p for p in run_dir.rglob("*") if p.is_file() and p != output):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(run_dir)}")
    atomic_write_text(output, "\n".join(lines) + "\n")
    return output


def controller(args: argparse.Namespace) -> int:
    run_id = args.run_id or f"T001-nccl-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    run_dir = Path(args.output_root) / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    atomic_write_text(run_dir / "controller.pid", f"{os.getpid()}\n")
    sentinel = Path(args.pause_sentinel)
    state = {"stop_reason": None}
    stop_file = run_dir / "stop_request.json"

    def request_stop(reason: str, detail: str) -> None:
        if state["stop_reason"] is None:
            state["stop_reason"] = reason
            atomic_write_json(stop_file, {"status": reason, "detail": detail, "requested_at": utc_now()})

    signal.signal(signal.SIGUSR1, lambda *_: request_stop("PAUSED", "controller received SIGUSR1"))
    signal.signal(signal.SIGTERM, lambda *_: request_stop("STOPPED", "controller received SIGTERM"))

    pre = wait_for_idle(args.availability_timeout, args.availability_interval, sentinel)
    atomic_write_json(run_dir / "preflight.json", pre)
    if not pre.get("idle"):
        reason = "PAUSED" if pre.get("paused") else "FAILED"
        summary = {"schema_version": 1, "run_id": run_id, "status": reason, "started_at": None, "finished_at": utc_now(), "failures": ["GPU availability preflight did not pass"], "release": {"released": True, "remaining_task_pids": []}}
        atomic_write_json(run_dir / "summary.json", summary)
        hash_evidence(run_dir)
        return 2

    try:
        xid = XidMonitor()
    except Exception as exc:
        summary = {"schema_version": 1, "run_id": run_id, "status": "FAILED", "started_at": None, "finished_at": utc_now(), "failures": [f"NVML Xid monitor setup failed: {type(exc).__name__}: {exc}"], "release": {"released": True, "remaining_task_pids": []}}
        atomic_write_json(run_dir / "summary.json", summary)
        hash_evidence(run_dir)
        return 3

    script = Path(__file__).resolve()
    torchrun = Path(args.torchrun).resolve()
    child_argv = [
        str(torchrun), "--standalone", f"--nproc-per-node={GPU_COUNT}", "--monitor-interval=5",
        str(script), "worker", "--run-dir", str(run_dir), "--duration", str(args.duration),
        "--allocation-gib", str(args.allocation_gib), "--memory-limit-gib", str(args.memory_limit_gib),
        "--heartbeat-seconds", str(args.heartbeat_seconds),
    ]
    manifest = {
        "schema_version": 1, "run_id": run_id, "status": "RUNNING", "created_at": utc_now(),
        "source_revision": command(["/usr/bin/git", "-C", str(script.parents[1]), "rev-parse", "HEAD"]),
        "command": child_argv, "controller_pid": os.getpid(), "pause_sentinel": str(sentinel),
        "constraints": {"ranks": GPU_COUNT, "duration_seconds": args.duration, "allocation_gib_per_gpu": args.allocation_gib, "memory_limit_gib_per_gpu": args.memory_limit_gib},
        "versions": command([str(torchrun.parent / "python"), "-c", "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.nccl.version())"]),
        "pre_gpu_process_state": pre["snapshot"],
    }
    atomic_write_json(run_dir / "manifest.json", manifest)
    stdout_handle = (run_dir / "torchrun.stdout.log").open("w", encoding="utf-8")
    stderr_handle = (run_dir / "torchrun.stderr.log").open("w", encoding="utf-8")
    proc = subprocess.Popen(child_argv, stdin=subprocess.DEVNULL, stdout=stdout_handle, stderr=stderr_handle, text=True, start_new_session=True)
    atomic_write_text(run_dir / "torchrun.pid", f"{proc.pid}\n")
    started_mono = time.monotonic()
    monitor_issues: list[str] = []
    monitor_path = run_dir / "monitor.jsonl"
    stop_requested_at: float | None = None
    try:
        with monitor_path.open("a", encoding="utf-8", buffering=1) as monitor:
            while proc.poll() is None:
                if sentinel.exists():
                    request_stop("PAUSED", f"sentinel detected at {sentinel}")
                try:
                    xid_events = xid.poll()
                except Exception as exc:
                    xid_events = []
                    monitor_issues.append(f"Xid polling failed: {type(exc).__name__}: {exc}")
                    request_stop("FAILED", monitor_issues[-1])
                snap = gpu_snapshot()
                disk = filesystem_snapshot(str(run_dir))
                heartbeat = {}
                for rank in range(GPU_COUNT):
                    path = run_dir / f"rank_{rank}.heartbeat.json"
                    heartbeat[str(rank)] = None if not path.exists() else round(time.time() - path.stat().st_mtime, 3)
                sample = {"at": utc_now(), "elapsed_seconds": round(time.monotonic() - started_mono, 3), "gpu": snap, "disk": disk, "heartbeat_age_seconds": heartbeat, "xid_events": xid_events}
                monitor.write(json.dumps(sample, sort_keys=True) + "\n")
                monitor.flush()
                os.fsync(monitor.fileno())
                if xid_events:
                    monitor_issues.append(f"critical Xid event(s): {xid_events}")
                    request_stop("FAILED", monitor_issues[-1])
                if snap["query"]["rc"] != 0 or snap["compute_apps_query"]["rc"] != 0:
                    monitor_issues.append("nvidia-smi health query failed")
                    request_stop("FAILED", monitor_issues[-1])
                for gpu in snap["gpus"]:
                    if int(float(gpu["temperature_c"])) > args.max_temperature_c:
                        monitor_issues.append(f"GPU {gpu['index']} temperature exceeded limit: {gpu['temperature_c']} C")
                        request_stop("FAILED", monitor_issues[-1])
                task_pids = known_task_pids(run_dir)
                for app in snap["compute_apps"]:
                    if app["pid"] in task_pids and app["used_gpu_memory_mib"] > int(args.memory_limit_gib * 1024):
                        monitor_issues.append(f"PID {app['pid']} exceeded GPU memory limit: {app['used_gpu_memory_mib']} MiB")
                        request_stop("FAILED", monitor_issues[-1])
                if disk["free_bytes"] < args.minimum_free_gib * GIB:
                    monitor_issues.append(f"disk free below {args.minimum_free_gib} GiB")
                    request_stop("FAILED", monitor_issues[-1])
                elapsed = time.monotonic() - started_mono
                if elapsed > args.heartbeat_grace_seconds:
                    stale = [rank for rank, age in heartbeat.items() if age is None or age > args.heartbeat_timeout_seconds]
                    if stale:
                        monitor_issues.append(f"stale/missing rank heartbeat(s): {stale}")
                        request_stop("FAILED", monitor_issues[-1])
                if state["stop_reason"] is not None:
                    stop_requested_at = stop_requested_at or time.monotonic()
                    if time.monotonic() - stop_requested_at > args.stop_grace_seconds:
                        os.killpg(proc.pid, signal.SIGTERM)
                        time.sleep(5)
                        if proc.poll() is None:
                            os.killpg(proc.pid, signal.SIGKILL)
                time.sleep(args.monitor_seconds)
        child_rc = proc.wait(timeout=15)
    finally:
        stdout_handle.flush(); stderr_handle.flush()
        os.fsync(stdout_handle.fileno()); os.fsync(stderr_handle.fileno())
        stdout_handle.close(); stderr_handle.close()
        xid.close()

    ranks = read_rank_records(run_dir)
    release = prove_release(run_dir, args.release_timeout_seconds)
    post = gpu_snapshot()
    result = assess_run(
        ranks=ranks, requested_duration=args.duration,
        memory_limit_bytes=int(args.memory_limit_gib * GIB), controller_rc=child_rc,
        monitor_issues=monitor_issues, release=release, stop_reason=state["stop_reason"],
    )
    summary = {
        "schema_version": 1, "run_id": run_id, **result,
        "started_at": manifest["created_at"], "finished_at": utc_now(),
        "controller_pid": os.getpid(), "torchrun_pid": proc.pid, "torchrun_rc": child_rc,
        "requested_duration_seconds": args.duration, "memory_limit_bytes": int(args.memory_limit_gib * GIB),
        "ranks": ranks, "monitor_issues": monitor_issues, "release": release,
        "pre_gpu_process_state": pre["snapshot"], "post_gpu_process_state": post,
    }
    atomic_write_json(run_dir / "summary.json", summary)
    hash_evidence(run_dir)
    return 0 if result["status"] == "PASS" else 4


def worker(args: argparse.Namespace) -> int:
    import torch
    import torch.distributed as dist

    run_dir = Path(args.run_dir)
    rank = int(os.environ["RANK"])
    local_rank = int(os.environ["LOCAL_RANK"])
    world_size = int(os.environ["WORLD_SIZE"])
    pid = os.getpid()
    local_stop = {"value": False, "status": "STOPPED"}
    signal.signal(signal.SIGUSR1, lambda *_: local_stop.update(value=True, status="PAUSED"))
    signal.signal(signal.SIGTERM, lambda *_: local_stop.update(value=True, status="STOPPED"))
    atomic_write_json(run_dir / f"rank_{rank}.start.json", {"rank": rank, "local_rank": local_rank, "pid": pid, "started_at": utc_now()})
    record: dict[str, Any] = {
        "rank": rank, "local_rank": local_rank, "pid": pid, "gpu_index": local_rank,
        "status": "FAILED", "elapsed_seconds": 0.0, "collectives": 0,
        "integrity_checks": 0, "peak_allocated_bytes": 0, "error": None,
    }
    started = None
    buffer = None
    try:
        if world_size != GPU_COUNT:
            raise RuntimeError(f"expected world size {GPU_COUNT}, got {world_size}")
        torch.cuda.set_device(local_rank)
        props = torch.cuda.get_device_properties(local_rank)
        fraction = min(0.99, (args.memory_limit_gib * GIB) / props.total_memory)
        torch.cuda.set_per_process_memory_fraction(fraction, local_rank)
        dist.init_process_group("nccl", timeout=__import__("datetime").timedelta(seconds=120))
        allocation_bytes = int(args.allocation_gib * GIB)
        buffer = torch.empty(allocation_bytes, dtype=torch.uint8, device=local_rank)
        collective = torch.empty(2 * MIB, dtype=torch.float32, device=local_rank)
        chunk_bytes = 64 * MIB
        chunks = max(1, allocation_bytes // chunk_bytes)
        torch.cuda.synchronize(local_rank)
        dist.barrier()
        started = time.monotonic()
        last_heartbeat = 0.0
        step = 0
        status = "COMPLETED"
        while True:
            request_path = run_dir / "stop_request.json"
            if request_path.exists():
                try:
                    request = json.loads(request_path.read_text(encoding="utf-8"))
                    local_stop.update(value=True, status=request.get("status", "STOPPED"))
                except Exception:
                    local_stop.update(value=True, status="STOPPED")
            stop_tensor = torch.tensor([1 if local_stop["value"] else 0], dtype=torch.int32, device=local_rank)
            dist.all_reduce(stop_tensor, op=dist.ReduceOp.MAX)
            if int(stop_tensor.item()):
                status = local_stop["status"]
                if status not in {"PAUSED", "STOPPED", "FAILED"}:
                    status = "STOPPED"
                break
            done = torch.tensor([1 if time.monotonic() - started >= args.duration else 0], dtype=torch.int32, device=local_rank)
            dist.all_reduce(done, op=dist.ReduceOp.MIN)
            if int(done.item()):
                break
            offset = (step % chunks) * chunk_bytes
            view = buffer[offset: min(offset + chunk_bytes, allocation_bytes)]
            marker = (rank * 17 + step) % 251
            view.fill_(marker)
            if int(view[0].item()) != marker or int(view[-1].item()) != marker:
                raise RuntimeError(f"allocation read/write integrity mismatch at step {step}")
            value = float((step % 100) + rank)
            collective.fill_(value)
            dist.all_reduce(collective, op=dist.ReduceOp.SUM)
            expected = float(world_size * (step % 100) + sum(range(world_size)))
            observed_min = float(collective.min().item())
            observed_max = float(collective.max().item())
            if observed_min != expected or observed_max != expected:
                raise RuntimeError(f"NCCL integrity mismatch step={step} expected={expected} min={observed_min} max={observed_max}")
            step += 1
            record["collectives"] = step
            record["integrity_checks"] = step
            now = time.monotonic()
            if now - last_heartbeat >= args.heartbeat_seconds:
                atomic_write_json(run_dir / f"rank_{rank}.heartbeat.json", {"rank": rank, "local_rank": local_rank, "pid": pid, "at": utc_now(), "elapsed_seconds": round(now - started, 3), "collectives": step, "integrity_checks": step, "peak_allocated_bytes": torch.cuda.max_memory_allocated(local_rank)})
                last_heartbeat = now
            time.sleep(0.2)
        torch.cuda.synchronize(local_rank)
        record["status"] = status
    except BaseException as exc:
        record["status"] = "FAILED"
        record["error"] = f"{type(exc).__name__}: {exc}"
        record["traceback"] = traceback.format_exc()
    finally:
        if started is not None:
            record["elapsed_seconds"] = round(time.monotonic() - started, 6)
        try:
            record["peak_allocated_bytes"] = int(torch.cuda.max_memory_allocated(local_rank))
        except Exception:
            pass
        buffer = None
        try:
            if dist.is_initialized():
                dist.destroy_process_group()
        except Exception as exc:
            record["error"] = record.get("error") or f"destroy_process_group: {exc}"
            record["status"] = "FAILED"
        try:
            torch.cuda.empty_cache()
        except Exception:
            pass
        record["finished_at"] = utc_now()
        atomic_write_json(run_dir / f"rank_{rank}.final.json", record)
    return 0 if record["status"] in {"COMPLETED", "PAUSED", "STOPPED"} else 1


def validate_run(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    errors = []
    if summary.get("status") != "PASS":
        errors.append(f"summary status is {summary.get('status')}")
    if len(summary.get("ranks", [])) != GPU_COUNT:
        errors.append("summary does not contain exactly four ranks")
    if not summary.get("release", {}).get("released"):
        errors.append("release proof did not pass")
    for rank in summary.get("ranks", []):
        if rank.get("status") != "COMPLETED" or rank.get("elapsed_seconds", 0) < summary.get("requested_duration_seconds", 1800):
            errors.append(f"rank {rank.get('rank')} is incomplete")
    print(json.dumps({"valid": not errors, "errors": errors}, sort_keys=True))
    return 0 if not errors else 1


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="command", required=True)
    inv = sub.add_parser("inventory")
    inv.add_argument("--output", default="artifacts/inventory/machine_inventory.json")
    run = sub.add_parser("smoke")
    run.add_argument("--run-id")
    run.add_argument("--output-root", default="artifacts/gate0/t001")
    run.add_argument("--torchrun", default="/data3/xc/.conda/envs/d2l/bin/torchrun")
    run.add_argument("--duration", type=float, default=1800)
    run.add_argument("--allocation-gib", type=float, default=14.0)
    run.add_argument("--memory-limit-gib", type=float, default=16.0)
    run.add_argument("--heartbeat-seconds", type=float, default=60)
    run.add_argument("--monitor-seconds", type=float, default=10)
    run.add_argument("--heartbeat-grace-seconds", type=float, default=240)
    run.add_argument("--heartbeat-timeout-seconds", type=float, default=120)
    run.add_argument("--stop-grace-seconds", type=float, default=120)
    run.add_argument("--release-timeout-seconds", type=float, default=120)
    run.add_argument("--max-temperature-c", type=float, default=88)
    run.add_argument("--minimum-free-gib", type=float, default=500)
    run.add_argument("--availability-timeout", type=float, default=3600)
    run.add_argument("--availability-interval", type=float, default=30)
    run.add_argument("--pause-sentinel", default=str(PAUSE_SENTINEL))
    work = sub.add_parser("worker")
    work.add_argument("--run-dir", required=True)
    work.add_argument("--duration", type=float, required=True)
    work.add_argument("--allocation-gib", type=float, required=True)
    work.add_argument("--memory-limit-gib", type=float, required=True)
    work.add_argument("--heartbeat-seconds", type=float, required=True)
    val = sub.add_parser("validate")
    val.add_argument("--run-dir", required=True)
    return ap


def main() -> int:
    args = parser().parse_args()
    if args.command == "inventory":
        collect_inventory(Path(args.output))
        return 0
    if args.command == "smoke":
        return controller(args)
    if args.command == "worker":
        return worker(args)
    return validate_run(args)


if __name__ == "__main__":
    raise SystemExit(main())
