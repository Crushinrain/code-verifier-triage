# Project Plan

## Durable goal

Build CodeVerifier-Triage as a governed, reproducible research system for
risk-calibrated selective execution under policy shift. Evidence must establish
protocol validity, safety, fixed-budget comparisons, and Claim boundaries before
any result is promoted.

The project is currently **PLANNED**. No project experiment result, Gate
approval, final-test authorization, or external-release authorization exists.

## Authority and control plane

1. `.workflow/project.json` defines the four semantic workflow documents.
2. `HANDOFF.md` defines the only currently authorized batch.
3. `PROGRESS.md` is the single append-only execution/review ledger.
4. `REVIEW_PROTOCOL.md` defines independent acceptance review.
5. `tasks/task_graph.yaml` is the sole operational task/dependency/Gate-number
   authority. Files under `planning/` are retained as non-authoritative planning
   references until a separately authorized migration reconciles them.
6. Frozen files under `contracts/` and approval state under
   `approvals/HUMAN_APPROVALS.yaml` are never changed by inference.

## Current phase boundary

Only T000 is authorized. T000 may bootstrap an independent Git repository,
install the generic workflow skill at its approved path, initialize the governed
control plane, add minimal packaging/license-inventory records, validate the
starter pack, and create one root commit. It may not begin T001 or implement T005.

## Durable acceptance principles

- One Task ID maps to one reviewable commit/PR boundary.
- A fresh, role-locked Reviewer independently reads primary evidence.
- GPU work, candidate execution, model/data access, final access, contract
  changes, deletion, and external release require their explicit approvals.
- Generated datasets, run outputs, checkpoints, caches, and large artifacts stay
  outside normal Git and retain provenance through manifests and hashes.
- Negative or blocked results remain in the ledger; preliminary evidence never
  becomes a confirmed Claim without formal review.

## Major risks

- The starter pack contains conflicting legacy planning IDs/Gate ranges and
  Claim IDs; the active authority rule above prevents accidental authorization.
- Task-level approval keys are not yet machine-bound.
- Several planned tasks conflate implementation and independent review roles.
- Run/schema helpers have known closure gaps that require a later authorized task.
- Main-branch protection cannot be established without a Git remote and hosting
  administrator; this blocks that T000 acceptance item but not local bootstrap.
- Third-party and project licensing are not cleared for external distribution.

See `docs/governance/T000_GOVERNANCE_GAPS.md` for the bounded remediation queue.
