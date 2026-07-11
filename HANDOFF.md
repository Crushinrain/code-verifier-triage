# HANDOFF - Current batch

## Batch identity

- Repair batch: T000-R1
- Parent Task ID: T000
- Title: Add the missing minimal pre-commit and CI bootstrap controls
- Active role: EXECUTOR
- Required context: a fresh role-locked Executor that did not perform the T000
  formal review
- Base: current tip of `review/t000-initial`
- Required work branch: `fix/t000-r1-controls` (must be created before edits)
- GPU required: no
- T001 authorization: no

## Single objective

Repair only the missing T000 pre-commit and CI implementation on a non-main
feature branch, validate it with already-installed tooling, append one bounded
handback, and stop. The unavailable hosted main-protection control remains an
explicit blocker and must not be reported as passed.

## Authorized writes

- `.pre-commit-config.yaml`
- `.github/workflows/contracts.yml`
- `PROGRESS.md`, tail append only for execution facts and the T000-R1 handback
- Repository-local Git metadata only as needed to create
  `fix/t000-r1-controls`, stage the two implementation files plus ledger append,
  and create one repair commit; `refs/heads/main` must not change

## Required implementation

1. Create `fix/t000-r1-controls` from the current
   `review/t000-initial` tip before changing files.
2. Add a minimal local pre-commit configuration that invokes the existing
   `scripts/validate_bundle.py .`, uses no remote hook repository, and does not
   install or upgrade dependencies.
3. Add a minimal hosted CI workflow that runs the existing bundle validator for
   pull requests and records the intended main-branch check. Do not expand into
   T005 negative tests, schema changes, or contract-freeze implementation.
4. Validate syntax and the underlying command with the existing
   `/data3/xc/.conda/envs/d2l/bin/python`. Run `pre-commit` only if it is already
   installed; otherwise record that tooling limitation without installing it.

## Forbidden writes and actions

- Any working-tree path other than the three authorized paths above
- Any commit, merge, rebase, reset, or ref update on `main`
- Creating, guessing, or pushing a Git remote; claiming hosted protection passed
- `/data3/xc/.git/**`, `/data3/xc/PV_forecast/**`, sibling projects, or global
  Git configuration
- `contracts/**`, `approvals/**`, Claims, `MANIFEST.sha256`, task graph, schemas,
  starter-pack files, or raw evidence
- Dependency/environment installation, network fetches, Docker changes,
  candidate execution, upstream clone, model/data/final access, GPU use, T001,
  T005, research Gate 0, or any other gated action

## Acceptance

- Work begins and ends on `fix/t000-r1-controls`; `main` remains exactly
  `90fc21ec1a4f3acce23ad13dc66f7af66c55bd94`.
- The committed tree contains `.pre-commit-config.yaml` and
  `.github/workflows/contracts.yml`; both are syntactically valid and invoke the
  existing bundle validator without changing its semantics.
- `sha256sum -c MANIFEST.sha256` still passes 91/91, and
  `scripts/validate_bundle.py` still reports 14 contracts, 6 schemas, 69 tasks,
  and 7 Gate checklists.
- Workflow validate returns zero errors/warnings before handback; after the
  handback, inspect reports review required for a fresh Reviewer.
- Exactly one T000-R1 repair commit exists on the feature branch, the worktree is
  clean, and no generated/heavy artifact is tracked.
- Hosted main protection remains `fail/block` unless the Human Owner supplies
  the external information below; this repair does not authorize T001.

## Stop conditions

- The current branch is `main`, the review base is missing, or the worktree is
  not clean before repair.
- A requested change exceeds the two implementation files and ledger tail
  append, requires installation/network access, or touches a forbidden path.
- Any instruction asks the Executor to approve its own repair, begin T001/T005,
  or reinterpret the branch-protection blocker as passed.

## Required handback

Append one `Batch T000-R1 - self-check & handback` block to `PROGRESS.md` with
exact commands and outcomes, both implementation file hashes, branch/commit
evidence, the unchanged `main` SHA, and the still-blocked hosted-protection item.
Set status to `HANDED BACK FOR REVIEW`, then stop for a fresh Reviewer.

## External information still required

The Human Owner must provide either:

1. the real Git remote URL, hosting provider/repository identity, and
   administrator able to configure and expose branch-protection evidence; or
2. an explicitly approved formal change request/waiver whose scope replaces the
   hosted-protection acceptance item.

The Executor must not infer either option from prose or create it independently.
