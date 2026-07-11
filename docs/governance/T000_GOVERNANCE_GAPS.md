# T000 Governance Gaps

Date recorded: 2026-07-11

Scope: observations only; no frozen contract, approval, or legacy planning file
was changed. These items require separately authorized repair tasks.

## G-001 - Governed control plane was absent

The starter pack did not include `.workflow/project.json` or the four semantic
workflow documents. T000 explicitly initialized them after Human authorization.
The structural gap is resolved for bootstrap, but no formal T000 review or
research Gate decision is implied.

## G-002 - Conflicting task and Gate systems

`tasks/task_graph.yaml` defines 69 tasks and Gates 0-6, while
`planning/PHASES_AND_GATES.md` adds Gates -1 and 7 and
`planning/BACKLOG.csv` uses unrelated `P-1-*` task IDs. For active execution,
`tasks/task_graph.yaml` is the sole authority; `planning/` cannot authorize work
until a migration task reconciles or clearly archives the legacy scheme.

## G-003 - Claim identifiers do not join

`contracts/claims.yaml` uses `CLAIM-*` identifiers and
`planning/CLAIMS.yaml` uses `CVT-*` identifiers with no stable mapping. Claims
features remain disabled in `.workflow/project.json`. A later change must define
one authority and an auditable migration before evidence or resume mapping uses
either set.

## G-004 - Human approvals are not task-bound

Twenty-seven task records declare `human_approval_required: true`, but task
records have no `approval_key` linking them to entries in
`approvals/HUMAN_APPROVALS.yaml`. All approval entries remain unchanged and
PENDING. No prose or status is treated as action authorization.

## G-005 - Planned roles violate independent review

Examples include T018/T019 assigning the same SecurityReviewer role to deploy
and accept the sandbox, T015 asking a Reviewer to submit a patch, and T209 asking
an ExperimentReviewer to produce the final model directory. Later task repair
must split Executor artifacts from independent Reviewer verdicts.

## G-006 - Run and schema helpers are not closed

`scripts/new_run.py` can emit null `git_commit`, `contracts_hash`, and
`upstream_lock_hash` although `schemas/run_manifest.schema.json` requires
strings. Group/candidate schemas also do not fully enforce the fixed group-size
and provenance/hash assumptions described by the contracts. T000 records the
gap but reserves implementation and negative tests for T005 or another explicit
repair task.

## T000 operational blockers outside the six gaps

- No Git remote exists, so hosted `main` branch protection and PR enforcement
  cannot be configured or verified.
- Pre-commit and CI are intentionally deferred to T005 to avoid overlapping
  implementation scope.
- Project and third-party licensing remain uncleared; see `LICENSE_AUDIT.md`.
