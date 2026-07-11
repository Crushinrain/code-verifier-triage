# HANDOFF - Current batch

## Batch identity

- Repair batch: T000-R6
- Parent Task ID: T000
- Title: Bootstrap default-branch CI and enforce public protected main
- Active role: EXECUTOR
- Required context: a fresh role-locked Executor that did not perform the
  T000-R5 formal review
- Base: current tip of `review/t000-r5`
- Required work branch: `fix/t000-r6-public-controls`
- GPU required: no
- T001 authorization: no; the four-GPU 30-minute T001 smoke becomes eligible
  only after a fresh Reviewer closes T000

## Single objective

Use the Human Owner's completed private-to-public visibility change to close
the remaining T000 hosted-control condition with the smallest reproducible
bootstrap: install the already-reviewed workflow commit on `main` by one exact
fast-forward, reuse PR #1 to obtain a real passing check on its unchanged R5
head, enforce public protected-main controls against that exact check, record
evidence, and stop without merging or editing implementation.

## Why this bootstrap is necessary and bounded

The fresh R5 review observed a public repository with administrative access,
PR #1 open and unmerged at head `1360e76dad6eb13f9495a17b35088f274dd218cd`,
but zero registered workflows, zero runs/checks for that head, no ruleset, and
unprotected `main`. The workflow exists in reviewed commit
`f34dbbaa5c643b7ec2b59a9df0587eef9af50bda` but not in current `main` at
`90fc21ec1a4f3acce23ad13dc66f7af66c55bd94`.

GitHub's official event documentation states that a `pull_request` workflow
without explicit activity types runs for `opened`, `synchronize`, and
`reopened`, while the workflow must exist on the default branch. Therefore the
only authorized default-branch update is the already-reviewed fast-forward to
`f34dbba`; after it registers, PR #1 may be closed and immediately reopened
once to produce the documented `reopened` event. No new commit, workflow edit,
empty commit, or implementation change is needed.

Official basis:
`https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request`.

## Authorized writes and hosted actions

- Create `fix/t000-r6-public-controls` from clean `review/t000-r5`
- Mode-600 temporary evidence only under `.git/t000-r6-*`
- `PROGRESS.md`, tail append only, and exactly one T000-R6 handback commit
- Non-forced publication of `review/t000-r5` and the R6 branch
- Exactly one guarded fast-forward update of remote `main` from `90fc21e` to
  existing reviewed commit `f34dbba`
- Exactly one close then one reopen of PR #1, only after the default-branch
  workflow is registered and only while the PR is open, unmerged, and at the
  expected immutable head
- Read-only CI observation followed by one classic branch-protection mutation
  on `main`, or one main-only active ruleset if classic protection is
  unavailable, using the exact successful check context returned by GitHub

No source/workflow/schema/contract/approval/Claim edit, PR merge, visibility
change, credential action, package installation, or GPU action is authorized.

## Mandatory preflight and fail-closed boundary

1. Start at clean `review/t000-r5`; create only
   `fix/t000-r6-public-controls`. Verify local `main` is `90fc21e`, R5 is
   `1360e76`, and reviewed workflow bootstrap commit is exactly `f34dbba`.
2. Re-run workflow `inspect` and `validate`; verify the R5 commit is a single
   append-only `PROGRESS.md` change over `fa79194` and all starter validation
   checks still pass.
3. Reverify exact origin, repository-local SSH command, host/deploy-key
   fingerprints, project/parent worktree isolation, and that no key/config or
   implementation file changed.
4. With the pinned official `.git/t000-r5-tools/gh`, prove the active account,
   exact repository, `visibility=public`, `permissions.admin=true`, default
   branch `main`, remote `main=90fc21e`, PR #1 open/unmerged with base `main`
   and head `1360e76`, and no unexpected PR/ruleset/protection state. Never
   print or persist any token/cookie/password.
5. Re-query workflows, runs, and check-runs before mutation. If a genuine
   successful PR-head check already exists, skip the main bootstrap and PR
   state cycle and proceed to enforcement. Any conflicting or failing state
   fails closed.

## Minimal default-branch and PR trigger sequence

Only when no real PR-head check exists:

1. Confirm `f34dbba` is a descendant of `90fc21e`, contains the reviewed
   `.github/workflows/contracts.yml`, and remote `main` still equals `90fc21e`.
2. Execute one non-forced explicit fast-forward refspec only:
   `git push --porcelain origin
   f34dbbaa5c643b7ec2b59a9df0587eef9af50bda:refs/heads/main`.
   No force, deletion, tags, mirror, all-branches, upstream, fetch, pull,
   merge, rebase, or reset is allowed.
3. Reread remote `main`; require exactly `f34dbba`. Wait until GitHub registers
   `.github/workflows/contracts.yml`. The push may produce a main-branch run;
   record it but do not use it as proof of the PR-head requirement.
4. Reread PR #1 and require open, unmerged, base `main`, head ref
   `fix/t000-r5-hosted-controls`, and immutable head `1360e76`. Close exactly
   PR #1, verify closed and unmerged, then immediately reopen exactly PR #1 and
   verify open/unmerged with the same head. Do not close any other PR.
5. Poll only the resulting PR/head workflow run and check-runs with bounded
   intervals and an overall 20-minute deadline. Require a completed successful
   real check on exact head `1360e76`; record workflow/run/job/check IDs, URLs,
   event, timestamps, head/base, and exact context. Do not rerun, approve,
   cancel, edit, or weaken a failed/pending workflow.

## Protected-main enforcement

After the exact successful PR-head context is known, establish protection only
for `main`. Prefer classic branch protection with:

- required status checks enabled, strict/up-to-date, containing only the exact
  successful check context observed on PR head `1360e76`
- pull request required before updates, with zero required approving reviews
- administrator enforcement enabled
- restrictions absent and no bypass actor/role
- force pushes disabled and deletions disabled
- no signed-commit, merge-queue, deployment, code-owner, conversation,
  linear-history, lock, or unrelated rule

If classic protection is unavailable, one active ruleset targeting exactly
`refs/heads/main` with equivalent fields and empty bypass actors is authorized.
Do not create both. Reread the effective hosted configuration and prove direct
updates, force pushes, and deletion are blocked for all actors, including
administrators, and the exact passing check is required.

## Final ledger and branch publication

1. Append one `Batch T000-R6 - public hosted controls handback` block recording
   exact local/remote SHAs, public/admin and PR facts, every mutation, CI
   identity/conclusion, effective protection fields, checksums of mode-600
   evidence, isolation, and any fail-closed reason.
2. Create exactly one local handback commit on
   `fix/t000-r6-public-controls`; no implementation or semantic-document edit
   other than the ledger tail is allowed.
3. Non-force publish `review/t000-r5`, publish the R6 branch at its review base,
   then update the R6 branch once to the handback commit so evidence is durable.
   Never update `main` beyond exact `f34dbba`.
4. Final reread must prove PR #1 open/unmerged at head `1360e76`, its exact
   check passing, remote `main=f34dbba`, effective protection active, branch
   refs correct, local worktree clean, and project/parent isolation intact.
5. Set `Status: HANDED BACK FOR REVIEW` and stop. Only a fresh Reviewer may
   close T000 and authorize T001/T002/T005; the Executor must not use GPUs.

## Forbidden actions

- Merge/auto-merge PR #1, merge any branch, or direct-update `main` to any SHA
  other than the single exact `90fc21e -> f34dbba` fast-forward
- Any force push, deletion, tag, release, default-branch/visibility/billing
  change, wildcard ruleset, bypass, weakened CI/protection, or fabricated status
- New commit used only to trigger CI, workflow/source/config/schema/contract/
  approval/Claim edit, or implementation repair
- Login/device flow, token/cookie/password output, key/Git/SSH config change,
  installation, sudo/root/system/global mutation
- T001/T002/T005 execution, Gate 0, GPU/model/data/Docker, candidate execution,
  final access, long training, or external release

## Acceptance

- Public/admin repository identity, exact refs, single PR, workflow/run/check,
  and every hosted mutation are independently reproducible from saved evidence.
- Remote `main` moves once and only by the exact reviewed fast-forward to
  `f34dbba`; PR #1 remains open/unmerged at immutable head `1360e76`.
- A real PR-triggered check on exact head `1360e76` completes successfully.
- Main-only enforcement requires PRs and that exact check, enforces admins,
  blocks force/deletion, and has no bypass actor or unrelated rule.
- One bounded R6 ledger-only handback commit exists; worktrees, keys/config,
  frozen content, approvals, Claims, implementation, and prohibited resources
  remain isolated.
