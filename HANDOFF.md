# HANDOFF - Current batch

## Batch identity

- Repair batch: T000-R5
- Parent Task ID: T000
- Title: Close hosted PR, CI, and protected-main controls
- Active role: EXECUTOR
- Required context: a fresh role-locked Executor that did not perform the
  T000-R4 formal review
- Base: current tip of `review/t000-r4`
- Required work branch: `fix/t000-r5-hosted-controls`
- GPU required: no
- T001 authorization: no

## Single objective

Publish the reviewed R4 boundary, create exactly one pull request into `main`,
run the repository's real CI, and establish active hosted enforcement that
requires pull requests, blocks force-push and deletion, has no bypass actor,
and binds the actual passing CI check. Record evidence and stop without merging.

## Authorized writes and hosted actions

- Repository-local branch metadata needed to create
  `fix/t000-r5-hosted-controls` from clean `review/t000-r4`
- Mode-600 temporary evidence only under `.git/t000-r5-*`
- `PROGRESS.md`, tail append only, and one T000-R5 handback commit
- The exact non-forced branch publications, unique PR creation, CI observation,
  and ruleset/branch-protection mutation listed below
- If neither an official `gh` binary nor an authenticated browser session is
  available, one reversible project-local installation of the official GitHub
  CLI under `.git/t000-r5-tools/` as bounded below

No system/global package installation, key/config change, token creation,
repository content implementation, merge, or broader hosted mutation is
authorized.

## Mandatory local preflight

1. Start from clean `review/t000-r4`; verify its parent is R4 commit
   `4cfd5cbcf1c9689b1017db549924be10864c8293`, create only
   `fix/t000-r5-hosted-controls`, and confirm local `main` remains
   `90fc21ec1a4f3acce23ad13dc66f7af66c55bd94`.
2. Reverify exact origin and repository-local strict SSH command, key/known-host
   fingerprints, and that the eight already-published remote-tracking refs
   remain at the R4-reviewed SHAs. Do not contact GitHub during this step.
3. Verify the R4 execution and review branches do not yet have corresponding
   remote-tracking refs. Publish only these non-forced refspecs, plus the new PR
   head at its initial review tip:
   - `refs/heads/fix/t000-r4-safe-probe:refs/heads/fix/t000-r4-safe-probe`
   - `refs/heads/review/t000-r4:refs/heads/review/t000-r4`
   - `refs/heads/fix/t000-r5-hosted-controls:refs/heads/fix/t000-r5-hosted-controls`
4. Every push must omit force, deletion, tags, mirror, all-branches, and
   upstream-setting options. Any non-fast-forward or unexpected remote state
   fails closed.

## Administrative-session boundary

Use only an already-authenticated GitHub browser session or an installed
official `gh` client whose `gh auth status` proves access to
`Crushinrain/code-verifier-triage` and sufficient repository-administration
authority. A deploy key alone is not administrative authority.

If `gh` is absent and no authenticated browser session is usable, the Executor
may download one pinned official GitHub CLI release archive plus its official
checksum file, verify the archive checksum before extraction, and place only
the binary under `.git/t000-r5-tools/` with no PATH/profile/package-database
mutation. Do not use a shell installer, package manager, `sudo`, root, or an
unverified mirror. Record version, official URLs, and checksum. Installation
does not authorize login; continue only if pre-existing authentication is then
proved, otherwise hand back blocked.

- Begin with read-only identity, repository, existing-PR, workflow, and
  ruleset/protection probes.
- Never request, accept, print, copy, persist, or place a token/password/cookie
  in commands, files, logs, the ledger, chat, or Git configuration.
- Do not start device authorization or create/refresh credentials. If no usable
  existing administrative session is available, record only non-sensitive
  status metadata, hand back FAIL/blocked, and stop after the branch publication.
- Fail closed if the repository identity, default branch, existing PR state, or
  current protection differs from the expected target.

## Unique PR and CI

1. Prove there is no open PR with head
   `Crushinrain:fix/t000-r5-hosted-controls` and base `main`; reuse an exact
   already-existing match only if all identity fields agree, otherwise stop.
2. Create at most one PR from `fix/t000-r5-hosted-controls` into `main`, with a
   T000 bootstrap/control title and body that states: no merge is authorized,
   T001 is not included, and hosted-control evidence is pending.
3. Observe the PR-triggered `.github/workflows/contracts.yml` run. Record the
   repository, PR number/URL, base/head refs and SHAs, workflow/run/check URLs,
   exact check context, conclusion, and timestamps. Never infer a check name
   from YAML; bind only a context returned by GitHub for this PR commit.
4. If CI fails or does not produce a stable real check context, do not weaken
   the workflow or protection. Record the failure and stop.

## Protected-main enforcement

After the real CI context is known, create or update one active ruleset targeting
only `refs/heads/main`; if rulesets are unavailable, use equivalent classic
branch protection. The effective hosted state must prove all of:

- pull requests are required before updates to `main` (zero approving reviews
  is acceptable for this bootstrap; direct pushes are not)
- branch deletion and non-fast-forward/force-push are blocked
- bypass actors are empty and no administrator/repository-role bypass applies
- the exact successful CI context from this PR is a required status check

Do not configure wildcard targets, merge queues, signed-commit requirements,
deployment gates, code-owner review, or unrelated repository settings. Reread
the effective hosted configuration after mutation and save only non-sensitive
JSON/page evidence with rule/ruleset or protection identifiers and enforcement
fields.

## Final ledger, commit, and PR-head update

1. Append one `Batch T000-R5 - hosted controls handback` block with local source
   SHAs, non-forced push results, administrative-session status without secrets,
   PR identity, final head SHA, CI run/check identity and conclusion, effective
   protected-main fields, isolation checks, and any fail-closed reason.
2. Create exactly one local T000-R5 commit on
   `fix/t000-r5-hosted-controls`; do not alter implementation, contracts,
   approvals, raw starter evidence, or Claims.
3. If hosted controls succeeded, non-force push only
   `refs/heads/fix/t000-r5-hosted-controls:refs/heads/fix/t000-r5-hosted-controls`,
   wait for the PR's CI on this final commit, and require the bound check to pass
   under the active protection. If the handback is blocked, the same single
   non-force branch update is allowed solely to preserve the negative evidence.
4. Verify PR head equals the handback commit, the PR remains open, `main` is
   unchanged, and the effective protected-main configuration remains active.
   Set `Status: HANDED BACK FOR REVIEW` and stop for a fresh Reviewer.

## Forbidden actions

- Merge, auto-merge, close/reopen an unrelated PR, direct or force push to
  `main`, deletion, tag, release, fetch/pull/rebase/reset, or branch-history
  rewrite
- Credential/device-login flow, token/cookie output, deploy-key change, SSH or
  Git config change, system/global installation, or any unverified CLI/script
- Workflow/code/schema/contract/approval/Claim edits; T001/T005; Gate 0;
  GPU/model/data/Docker; candidate execution; final access; external release

## Acceptance

- The exact R4 execution/review branches and single R5 PR head are published
  non-forced; exactly one open PR targets `main`.
- The final PR-head commit has the repository's real contracts CI check passing.
- Hosted evidence proves active PR-required, no-bypass, no-force, no-delete,
  exact-required-check enforcement on `main`.
- Local/remote `main`, parent repository, keys/config, implementation, frozen
  content, approvals, Claims, and prohibited resources remain unchanged.
- One bounded handback commit records evidence; the PR stays open and unmerged.
