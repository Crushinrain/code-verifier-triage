# HANDOFF - Current batch

## Batch identity

- Repair batch: T000-R3
- Parent Task ID: T000
- Title: Authenticate the dedicated deploy key and perform the bounded initial push
- Active role: EXECUTOR
- Required context: a fresh role-locked Executor that did not perform the T000-R2
  formal review
- Base: current tip of `review/t000-r2`
- Required work branch: `fix/t000-r3-initial-publish`
- GPU required: no
- T001 authorization: no

## New Human Owner fact

After T000-R2 commit `6f679b557e3b99f154e4cfbf3247e116da4904f9`,
the Human Owner explicitly confirmed that the delivered deploy public key was
added to `Crushinrain/code-verifier-triage` with write access. This is
authorization to test that dedicated identity and perform only the bounded
initial publication below; it is not evidence of successful authentication or
branch protection.

## Single objective

Using the already verified repository-local SSH configuration, authenticate the
dedicated deploy key, prove the GitHub repository has no refs, then make one
non-forced initial push of the explicitly listed governed branches. Record exact
evidence and stop. Do not configure hosting settings.

## Authorized writes and network actions

- Repository-local Git metadata needed to create
  `fix/t000-r3-initial-publish`
- One GitHub SSH authentication test using the exact dedicated identity and
  strict project-local known-hosts file
- One read-only `git ls-remote origin` before any push
- If and only if that command succeeds with completely empty stdout, one
  non-forced push containing only the branch refspecs listed below
- `PROGRESS.md`, tail append only, followed by one local T000-R3 handback commit

No package installation is needed or authorized. The standing safe-tool
authorization does not expand this HANDOFF.

## Required preflight

1. Start from a clean `review/t000-r2` tip and create
   `fix/t000-r3-initial-publish`. Record all local branch SHAs before network
   access and confirm local `main` remains
   `90fc21ec1a4f3acce23ad13dc66f7af66c55bd94`.
2. Confirm `origin` is exactly
   `git@github.com:Crushinrain/code-verifier-triage.git`.
3. Confirm local `core.sshCommand` still specifies only
   `/data3/xc/.ssh/code_verifier_triage_github_ed25519`,
   `IdentitiesOnly=yes`, `BatchMode=yes`,
   `StrictHostKeyChecking=yes`, and
   `/data3/xc/code-verifier-triage/.git/github_known_hosts`.
4. Confirm the public-key fingerprint remains
   `SHA256:uEvYGvdUeVBES69/F5njgZcSIKJm+mGZrqyrx33iEoA`, the known-host
   fingerprint remains
   `SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU`, and the private
   key mode remains 600. Never print or inspect private-key content.

## Required network sequence

1. Run the explicit SSH authentication test with the same key and options as
   local `core.sshCommand`, adding only `-T git@github.com`. Accept GitHub's
   documented no-shell nonzero exit only when stderr unambiguously states that
   authentication succeeded for the expected repository deploy identity.
   Otherwise stop without `ls-remote` or push.
2. Run exactly one pre-push `git ls-remote origin`. It must exit 0 and emit no
   refs and no stdout. Any existing branch, tag, symbolic ref, error, or
   credential prompt is a fail-closed stop.
3. Only after both checks pass, run one `git push --porcelain origin` with
   exactly these source/destination refspecs:
   - `refs/heads/main:refs/heads/main`
   - `refs/heads/review/t000-initial:refs/heads/review/t000-initial`
   - `refs/heads/fix/t000-r1-controls:refs/heads/fix/t000-r1-controls`
   - `refs/heads/review/t000-r1:refs/heads/review/t000-r1`
   - `refs/heads/fix/t000-r2-github-transport:refs/heads/fix/t000-r2-github-transport`
   - `refs/heads/review/t000-r2:refs/heads/review/t000-r2`
4. Do not add `--force`, `--force-with-lease`, `--mirror`, `--tags`,
   `--all`, or `--set-upstream`. Do not push the new
   `fix/t000-r3-initial-publish` branch in this batch.

## Forbidden actions

- Merge, rebase, cherry-pick, reset, ref rewrite, force push, deletion, tag
  creation/publication, fetch, pull, clone, submodule operations, or a second
  push
- GitHub API/CLI mutation, rulesets, branch protection, PR creation/merge,
  repository settings, visibility, collaborators, secrets, or Deploy-key changes
- Changing `origin`, `core.sshCommand`, keys, known-hosts, global Git/SSH
  state, parent Git metadata, sibling projects, implementation, raw evidence,
  contracts, approvals, Claims, T001/T005, research Gate 0, GPU/model/data/Docker
- Printing or transmitting the private key, accepting a new host key, using any
  credential other than the dedicated deploy identity, or responding to a
  credential prompt

## Acceptance

- The dedicated identity authenticates as the expected GitHub repository deploy
  identity under strict host-key checking.
- The sole pre-push `git ls-remote origin` succeeds with empty stdout.
- The sole push reports success for all and only the six listed branches, with no
  forced update, tag, deletion, merge, or upstream configuration.
- Exact commands, exit codes, bounded stdout/stderr, pre-push branch SHAs, and
  push porcelain output are appended to the ledger without secrets.
- Local `main`, parent repository state, and all prohibited project paths remain
  unchanged. Hosted ruleset/branch protection remains unverified, and T001 stays
  unauthorized.

## Stop conditions

- Any preflight mismatch, authentication ambiguity, nonempty `ls-remote`,
  network/host-key error, credential prompt, unexpected remote ref, rejected or
  non-fast-forward update, or push result outside the six explicit refspecs
- Any step would require a second network attempt, force, merge, hosting/API
  mutation, installation, global/root change, or broader scope

## Required handback

Append one `Batch T000-R3 - initial publication handback` block to
`PROGRESS.md` with exact evidence for every Acceptance item and any failure.
Create one local commit on `fix/t000-r3-initial-publish`, set
`Status: HANDED BACK FOR REVIEW`, and stop. A fresh Reviewer must inspect the
result before any further authentication, remote read/write, ruleset,
branch-protection, PR, T001, or Gate 0 action.
