# HANDOFF - T004 environments and Gate 0 hosted publication

## Reviewed boundary and parallel authorization

- Closed batch: Gate 0 accepted-tree integration commit
  `3e2b749aa5f4862e844d906c874763483c238831`, formally APPROVED on
  `review/integration-g0` by the sole commit containing this HANDOFF.
- Dispatcher binding: resolve `review/integration-g0^{commit}` once after this
  Reviewer commit and give that identical full SHA to both fresh role-locked
  Executors. Each Executor records it before mutation and fails closed if the
  branch or worktree is not clean or the ancestry differs.
- Authorized lanes: (A) T004 isolated Python environments and (B) Gate 0 hosted
  publication/CI observation. They may run concurrently because T001 and T002
  are locally approved and serialized. Neither lane may approve itself.
- Human approval: not required for T004 or publication under the authoritative
  task graph and the Human Owner's standing autonomous-execution instruction.
- Gate 0 as a whole is not granted. No merge, `main` update, model/data payload,
  training, candidate execution, final access, contract change, or Claim is
  authorized.

## Isolation and ledger serialization

| Lane | Branch | Worktree |
|---|---|---|
| T004 | `task/t004-isolated-environments` | `/tmp/code-verifier-triage-T004` |
| hosted publication | `ops/g0-hosted-publication` | `/tmp/code-verifier-triage-publish-g0` |

- Create both from the one resolved Reviewer SHA. The primary worktree and the
  integration/review worktree remain Reviewer-owned and must not be switched,
  staged, or edited.
- Each Executor appends exactly one handback to its branch copy of
  `PROGRESS.md`, commits one reviewable boundary, and stops. A later fresh
  Reviewer serializes accepted tails; concurrent ledger cherry-picks are banned.

## Lane A - T004 isolated environments

### Fixed inputs and safe setup

1. Reverify the clean detached upstreams and fail closed on any mismatch:
   - CodeScaler commit `e1717833cf88a6bac3630af697f899e49493e8f5`,
     `/tmp/code-verifier-triage-T002-upstreams-verified-full/CodeScaler`;
     `requirements.txt` SHA-256
     `4561895474d0020431bf522f68790985fc2bd650a89d9778d64cfd81400a9655`.
   - RewardUQ commit `7224a1d35849e608fbe92a3bf2292028d8b39787`,
     `/tmp/code-verifier-triage-T002-upstreams-verified-full/RewardUQ`;
     `uv.lock` SHA-256
     `0a16c669a84e4677a997234a6b3b8a76d79a1c86ff15e0ab7e87997d91db934e`
     and `pyproject.toml` SHA-256
     `2490e0503417aaee90e0dfe5a41fd970fde70b772e03ea873ecffc9862783e89`.
   - Orchestrator `requirements-agent.txt` SHA-256
     `a4a4392dcc08f2d745527ca862c72ce3f7c82f32813a3f994f31138a61c97e83`.
2. Use Python 3.10 and only these new user-owned prefixes:
   - `/data3/xc/.conda/envs/code-verifier-codescaler-py310`
   - `/data3/xc/.conda/envs/code-verifier-rewarduq-py310`
   - `/data3/xc/.conda/envs/code-verifier-orchestrator-py310`
   No root/global install, existing-environment mutation, unknown installer, or
   credential material is permitted.
3. CodeScaler's fixed file contains exactly one `logoru==0.7.3`. Create an
   env-only derived input that replaces exactly that line with
   `loguru==0.7.3`; preserve the upstream checkout byte-for-byte, record input
   and derived hashes/diff, and never install `logoru`. Preserve the upstream
   torch 2.6.0 / torchvision 0.21.0 / torchaudio 2.6.0 / vLLM 0.8.3 pins and
   official CUDA 12.4 PyTorch wheels. Any resolver drift fails closed.
4. Resolve RewardUQ independently from its frozen `uv.lock`; do not combine its
   dependency graph with CodeScaler. The orchestrator installs only the fixed
   agent requirements. Use official package indexes only and retain resolver
   command/version plus complete lock/freeze evidence.
5. Defer FlashAttention; do not build/install `flash-attn`. Use the supported
   SDPA path for this bootstrap. No Docker or SandboxFusion build is authorized.

### Evidence and acceptance

- Track only reproducible files under `env/`, `env/README.md`, and
  `reports/gate0/environment.md`; keep raw machine evidence at ignored
  `artifacts/provenance/environment.json`. Record tool versions, commands,
  sources, package hashes/locks, prefix hashes, and limitations without secrets.
- Import smokes must cover each environment's declared core packages. Torch may
  perform metadata-only four-device discovery, but no tensor, collective, model,
  dataset, optimizer, trainer, or CUDA-memory allocation is allowed. Capture
  pre/post `nvidia-smi` and prove no T004 compute process remains.
- Acceptance requires three isolated Python 3.10 prefixes, reproducible locks,
  successful imports, Torch seeing exactly four GPUs from the relevant ML
  environments, a clean tracked diff, and workflow inspect/validate success.

## Lane B - non-force hosted publication and exact CI

1. Read-only preflight must verify `origin` is exactly
   `git@github.com:Crushinrain/code-verifier-triage.git`, authentication succeeds,
   remote `main` remains `f34dbbaa5c643b7ec2b59a9df0587eef9af50bda`, and
   PR #1 head branch `fix/t000-r5-hosted-controls` remains exactly
   `1360e76dad6eb13f9495a17b35088f274dd218cd`. Unexpected refs fail closed.
2. Verify the resolved Reviewer SHA is a descendant of both that PR head and
   integration commit `3e2b749`. Then perform one atomic, non-force push:
   - `integration/g0` -> exact `3e2b749aa5f4862e844d906c874763483c238831`;
   - `review/integration-g0` -> exact resolved Reviewer SHA;
   - existing PR #1 head `fix/t000-r5-hosted-controls` -> the same Reviewer SHA.
   Never use force, delete a ref, open a second PR, merge PR #1, mutate `main`,
   change repository settings/rules, or print authentication material.
3. Poll at a reasonable interval until the exact Reviewer SHA has terminal
   hosted status. The required context/job `contracts` must conclude SUCCESS;
   bind run URL/ID, workflow revision, head SHA, attempt, timestamps, and all job
   conclusions. Failure, cancellation, timeout, ambiguity, or a different SHA
   fails closed and blocks all later integration and Claims, although Lane A may
   finish its isolated handback and review.

## Shared GPU pause/checkpoint boundary

This HANDOFF authorizes no training. Every later training HANDOFF must retain:
LoRA/smoke atomic checkpoints every 10 minutes or 50 optimizer steps; full/FSDP
checkpoints every 20 minutes or 100 steps and never over 30 minutes apart; on
`SIGUSR1`, `SIGTERM`, or declared `PAUSE`, finish the current atomic optimizer
step, atomically checkpoint, stop all children, and prove GPU release; retain
`latest3` plus milestones and verify full model/optimizer/scheduler/scaler,
position, RNG, router, cache, source/config/data hashes, and checkpoint checksum
before resume. T004 and publication must never kill or preempt another user's GPU
process.

## Common handback

Each Executor runs relevant tests plus workflow inspect/validate, checks the full
diff and clean worktree, records exact commands/evidence/limitations, commits its
single task boundary, appends one `HANDED BACK FOR REVIEW` block, and stops for a
fresh independent Reviewer. No dependent task or hosted merge begins from an
Executor handback.
