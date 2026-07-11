# HANDOFF - Gate 0 parallel launch wave

## Authorization

- Closed predecessor: T000 (formal APPROVE in `review/t000-r6`)
- Authorized tasks: T001, T002, and T005 only
- Active roles: three fresh role-locked EXECUTOR contexts, one task per context
- Reviewed base: the single commit containing this HANDOFF and the T000-R6
  formal review on `review/t000-r6`; the dispatcher MUST resolve and give the
  same exact SHA to all three Executors before any work begins
- Human approval: not required by the authoritative task graph; the Human Owner
  explicitly requested autonomous execution and the shortest safe path to GPU use
- Gate 0 decision: not granted; this wave produces evidence for later review

No Executor may switch roles, approve its own task, start a dependent task, merge
to `main`, use final data, execute candidate code, or start policy/model training.

## Isolation and ledger serialization

Create three independent worktrees from the exact reviewed base:

| Task | Branch | Worktree |
|---|---|---|
| T001 | `task/t001-hardware-smoke` | `/tmp/code-verifier-triage-T001` |
| T002 | `task/t002-upstream-lock` | `/tmp/code-verifier-triage-T002` |
| T005 | `task/t005-contract-ci` | `/tmp/code-verifier-triage-T005` |

- The primary worktree `/data3/xc/code-verifier-triage` is Reviewer-owned during
  this wave. Executors MUST NOT switch it, stage in it, or edit its files.
- Each Executor edits and commits only its isolated branch/worktree, including
  exactly one tail handback block in that branch's copy of `PROGRESS.md`.
- No shared file outside Git metadata may be used as a ledger. After independent
  reviews, a Reviewer will serialize accepted task commits and replay the exact
  ledger tails in task-ID order; concurrent cherry-picks of `PROGRESS.md` are
  forbidden.
- One Task ID maps to one reviewable commit boundary. Generated evidence remains
  ignored/untracked unless the task graph names a tracked report or contract.

## T001 - immediate four-GPU inventory and synthetic smoke

### Scope

1. Record host/OS/kernel, CPU/RAM, filesystems/free space, cgroups v2, Docker
   client/server state, NVIDIA driver/runtime, GPU UUID/name/total memory/current
   processes, and `nvidia-smi topo -m` in:
   - `artifacts/inventory/machine_inventory.json`
   - `reports/gate0/hardware.md`
2. Reconfirm all four GPUs are available without evicting another user's process.
   If any GPU has an active foreign compute process or insufficient headroom,
   wait without mutation and retry at bounded intervals; never kill or preempt it.
3. Run one reproducible four-rank NCCL synthetic smoke for 1800 uninterrupted
   seconds, allocating at most 16 GiB per GPU. Exercise allocation/read-write and
   repeated all-reduce with integrity checks and 60-second heartbeats. Use no
   model, dataset, optimizer, trainer, candidate program, Docker image, or network
   service. Record exact command, interpreter/Torch/CUDA/NCCL versions, rank/PID,
   elapsed time, failures, peak memory, and pre/post GPU process state.

### Shared-GPU pause/stop contract

- Control sentinel: `/data3/xc/code-verifier-triage/.git/T001.PAUSE`.
- On `SIGUSR1`, `SIGTERM`, or sentinel detection, finish only the current bounded
  collective, atomically flush partial evidence with status `PAUSED` or `STOPPED`,
  terminate all ranks/children, and poll `nvidia-smi` until the four task PIDs are
  absent. Record release proof and stop.
- A paused/stopped run MUST NOT be reported as the required 1800-second PASS.
  Resume means a fresh uninterrupted 1800-second smoke with a new Run ID after
  the sentinel is removed; preserve the partial run as negative/partial evidence.
- Any OOM, NCCL error/hang, integrity mismatch, thermal/ECC issue, foreign-process
  conflict, or failure to release GPUs fails closed and is recorded.

### Acceptance

- Inventory JSON is machine-readable and the report binds its checksum.
- Exactly four ranks complete an uninterrupted >=1800-second synthetic smoke;
  each GPU demonstrates the bounded memory and NCCL integrity checks.
- Final evidence proves no T001 process remains and GPU memory is released.

## T002 - official upstream and Hugging Face metadata lock

### Scope

1. Resolve and shallow/full clone only the official URLs already named in
   `contracts/upstream.lock.yaml`: CodeScaler, RewardUQ, and SandboxFusion.
   Verify full immutable commit SHAs, origin URLs, reachability, and clean state.
   Store clones outside Git-tracked paths; do not vendor source.
2. Query official Hugging Face API metadata only (no weights or dataset payloads)
   for Qwen/Qwen3-1.7B-Base, LARK-Lab/CodeScaler-1.7B,
   Qwen/Qwen3-4B-Base, agentica-org/DeepCoder-Preview-Dataset, and
   LARK-Lab/CodeScalerPair-51K. Record immutable revisions, canonical IDs,
   request URLs/timestamps, and card/license metadata with raw-response hashes.
3. Replace every repository/model/dataset `main` or `RESOLVE*` placeholder in
   `contracts/upstream.lock.yaml` using only observed official metadata. Do not
   claim a container digest before T018 builds it. Emit
   `artifacts/provenance/upstream_manifest.json` and bind the lock-file hash.

### Acceptance

- All official repository URLs and full SHAs are reproducible and clean.
- No repository/model/dataset entry contains `main`, `latest`, or `RESOLVE*`.
- Manifest and lock hashes agree; no weight, data payload, token, or copied
  upstream source enters Git.

## T005 - contract, schema, task-graph CI negatives and active digest

### Scope

1. Extend the existing bundle validator/CI without weakening the reviewed
   `contracts` check. Add `tests/test_contracts.py` covering the valid starter
   bundle plus isolated negative fixtures for malformed schema, schema-invalid
   documents, missing dependency, and cyclic task dependencies.
2. Add a deterministic active-contract digest over the authoritative contract
   set, with explicit ordered paths and SHA-256, and verify it in CI. Do not edit
   contract meaning merely to satisfy a test.
3. Keep CI least-privilege, PR/push triggered, pinned where practical, and free
   of secrets/network-dependent tests. Re-run the 91-entry starter manifest,
   bundle validator, positive tests, every negative test, workflow inspect, and
   workflow validate.

### Acceptance

- Normal bundle and active digest pass; every specified corruption fails for the
  intended reason, including dependency-cycle rejection.
- CI configuration invokes those checks and remains compatible with required
  protected-main context `contracts`.
- Frozen approvals, Claims, data, and unrelated implementation are unchanged.

## Binding checkpoint policy for every later model-training HANDOFF

This wave does not authorize training. A future Reviewer MUST carry these exact
minimums into any training manifest before GPUs are used for model optimization:

- LoRA/smoke: atomic checkpoint every 10 minutes or 50 optimizer steps,
  whichever occurs first.
- Full/FSDP: atomic checkpoint every 20 minutes or 100 optimizer steps,
  whichever occurs first, and never more than 30 minutes between checkpoints.
- `SIGUSR1`, `SIGTERM`, or the declared `PAUSE` sentinel: complete the current
  atomic optimizer step, atomically checkpoint, stop all children, and prove GPU
  release. Retain `latest3` plus named milestones.
- Resume validation MUST restore and verify model/adapters, optimizer, scheduler,
  scaler, global/micro step, epoch, dataloader/sampler cursor, all RNG states,
  router/budget state, cache identity, code/config/contract/upstream/data hashes,
  and checkpoint checksum before continuing. Any mismatch fails closed.

## Common handback

Each Executor runs workflow `inspect` and `validate`, task-specific tests, checks
its complete diff and clean worktree, commits one task boundary, appends exactly
one self-check/handback block with primary evidence and limitations, then stops
for a fresh independent Reviewer. No Executor may begin T003, T004, T010, T018,
T023, training, or another wave.
