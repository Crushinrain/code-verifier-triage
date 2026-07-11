# Gate 0 hardware inventory and NCCL smoke (T001)

## Outcome

T001 passed its Executor self-check on 2026-07-12 (+08:00). Run
`T001-nccl-20260711T195259Z-full1800` completed one uninterrupted four-rank
NCCL synthetic smoke. Every rank ran for at least 1800 seconds, stayed below
the 16 GiB/GPU limit, and released its CUDA process and memory afterward.
This is execution evidence for independent review; it is not a Gate 0 decision.

## Machine inventory

- Inventory: `artifacts/inventory/machine_inventory.json`
- Inventory SHA-256:
  `312e328b269d1f1a4dcd2f6dde5e41f415cbf07dc4d9e4ca62b769df19b7aa88`
- Host: `test-ESC4000A-E10`; Ubuntu 22.04.4 LTS; Linux
  `6.8.0-107-generic`; x86-64.
- CPU/RAM: AMD EPYC 7K62, 48 physical cores / 96 logical CPUs, one NUMA node;
  251 GiB RAM.
- Storage: ext4 on `/dev/nvme0n1p2`; minimum free space observed during the
  smoke was 1,195,287,941,120 bytes (greater than the 500 GiB requirement).
- cgroups: v2 mounted (`cgroup2fs`) with cpuset, cpu, io, memory, hugetlb,
  pids, rdma, and misc controllers.
- Docker: client/server 29.1.3, API 1.52; containerd 2.2.1; runc 1.3.4.
- NVIDIA: driver 580.105.08; Torch 2.12.0+cu130; CUDA 13.0; NCCL 2.29.7.
- GPUs: four NVIDIA GeForce RTX 4090 D devices, 24,564 MiB each. UUIDs and
  complete pre/post process state are in the inventory and run summary.
- Topology: every cross-GPU edge is `NODE`; all GPUs have CPU affinity 0-95
  and NUMA affinity 0. The complete `nvidia-smi topo -m` output is retained in
  the inventory JSON.

## Reproducible run

The controller launched this exact worker command (also recorded as an argv
array in `manifest.json`):

```text
/data3/xc/.conda/envs/d2l/bin/torchrun --standalone --nproc-per-node=4 --monitor-interval=5 /tmp/code-verifier-triage-T001/scripts/t001_hardware_smoke.py worker --run-dir artifacts/gate0/t001/T001-nccl-20260711T195259Z-full1800 --duration 1800.0 --allocation-gib 14.0 --memory-limit-gib 16.0 --heartbeat-seconds 60.0
```

No model, dataset, optimizer, trainer, candidate program, Docker image, or
network service was used. Each rank allocated a 14 GiB byte buffer, repeatedly
wrote and read rotating 64 MiB windows, and performed a checked NCCL all-reduce.
The controller monitored NVML critical Xid events, temperature, ECC fields,
GPU processes/memory, disk space, and per-rank heartbeat age.

| Rank / GPU | PID | Elapsed (s) | NCCL checks | Peak allocated bytes | Result |
|---|---:|---:|---:|---:|---|
| 0 / 0 | 2968561 | 1800.194691 | 8,767 | 15,040,777,216 | COMPLETED |
| 1 / 1 | 2968562 | 1800.194721 | 8,767 | 15,040,777,216 | COMPLETED |
| 2 / 2 | 2968563 | 1800.194724 | 8,767 | 15,040,777,216 | COMPLETED |
| 3 / 3 | 2968564 | 1800.194720 | 8,767 | 15,040,777,216 | COMPLETED |

Offline audit of 179 monitor samples found zero foreign compute processes and
zero Xid events. Maximum temperature was 41 C, maximum task process memory was
14,912 MiB, maximum observed heartbeat age was 60.122 seconds, and the minimum
disk-free value is recorded above. Consumer RTX 4090 D ECC counters report
`N/A`; NVML critical-Xid event monitoring was active for all four devices.

## Pause, stop, and release behavior

The fixed control sentinel is
`/data3/xc/code-verifier-triage/.git/T001.PAUSE`. The controller maps sentinel
or `SIGUSR1` to `PAUSED`, and `SIGTERM` to `STOPPED`; it atomically writes the
stop request. Workers reconcile the request with a bounded NCCL collective,
atomically flush rank evidence, destroy the process group, and empty CUDA
caches. The controller then checks both `/proc` and `nvidia-smi`. Unit tests
verify that an interrupted or shorter-than-1800-second run cannot be promoted
to PASS and that failed release overrides PAUSED/STOPPED.

For the required full run, release proof found PIDs 2968561-2968564 absent from
both `/proc` and `nvidia-smi` on its first poll. The post-run state had zero
compute applications and 15 MiB used / 24,067 MiB free on each GPU. A separate
post-run recheck produced the same result.

## Evidence and checksums

- Run directory:
  `artifacts/gate0/t001/T001-nccl-20260711T195259Z-full1800/`
- Summary SHA-256:
  `992b9875d053bf7bd794949ed740ed158345adc560c785d653f163c5ffbcc577`
- Evidence checksum-list SHA-256:
  `ef8dc48ec0a90ebc961346ec0ceaedc254ff8b5bc244cc05c619cc78a9f140bc`
- Run-scoped source and committed script candidate SHA-256:
  `a4529b94b9f40ad762fc49c54bcb8fbcad75e38fad6e5e37c72cb337c2ccbc55`
- `sha256sum -c evidence.sha256`: all 20 named files passed.
- `scripts/t001_hardware_smoke.py validate --run-dir <run-dir>`:
  `{"errors": [], "valid": true}`.

Generated inventory and raw run evidence remain ignored/untracked. The report,
reproducible controller/worker, tests, and the append-only handback are the
reviewable Git boundary.
