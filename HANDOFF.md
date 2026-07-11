# HANDOFF - Current batch

## Batch identity

- Repair batch: T000-R2
- Parent Task ID: T000
- Title: Establish repository-scoped GitHub transport and deliver the deploy public key
- Active role: EXECUTOR
- Required context: a fresh role-locked Executor that did not perform the T000-R1
  formal review
- Base: current tip of `review/t000-r1`
- Required work branch: `fix/t000-r2-github-transport`
- GPU required: no
- T001 authorization: no

## Single objective

Configure only the repository-scoped SSH transport for
`git@github.com:Crushinrain/code-verifier-triage.git`, generate and disclose
only its dedicated deploy public key, then stop before authentication, fetch,
push, or any hosting-setting change. Hosted main protection remains the sole
unmet T000 condition.

## Human authorization and safe-tool boundary

- The Human Owner supplied the exact GitHub remote URL above and authorized this
  bounded key/transport preparation.
- The Human Owner also gave standing authorization for future safe tooling.
  This is not blanket installation authority: a tool must be necessary,
  well-known, fixed-version, reversible, installed without root into a
  project-isolated environment, and have its source, command, version, and
  outcome recorded.
- T000-R2 requires no installation. It does not authorize sudo/root, global or
  system mutation, unknown downloaded scripts, pipe-to-shell installers, or an
  installation outside the current HANDOFF scope.

## Authorized writes and network reads

- Repository-local Git metadata needed to create
  `fix/t000-r2-github-transport`, add `origin`, set local
  `core.sshCommand`, and store a project-local verified known-hosts file under
  `.git/`
- A new dedicated key pair only at
  `/data3/xc/.ssh/code_verifier_triage_github_ed25519` and its `.pub` file;
  neither path may pre-exist or be overwritten
- `PROGRESS.md`, tail append only for the pre-authentication handback
- Read-only network access limited to obtaining GitHub's officially published
  SSH host-key evidence and scanning `github.com:22` for comparison

## Required implementation

1. Begin from a clean `review/t000-r1` tip, create
   `fix/t000-r2-github-transport`, and confirm `main` is unchanged.
2. Confirm the dedicated private/public key paths do not exist. Never inspect,
   copy, or reuse the XC login key or any other private key.
3. Obtain the current GitHub ED25519 host-key fingerprint from an official
   GitHub source, record its URL, scan `github.com:22` for ED25519 only, and
   fail closed unless the observed fingerprint exactly matches. Store only the
   verified host line in a project-local `.git/github_known_hosts`.
4. Generate a new ED25519 key with a repository-specific comment, keep the
   private key on the server with mode 600, and set the public key mode to 644.
5. Add project-local `origin` with the exact authorized URL. Configure local
   `core.sshCommand` to use only the new private key,
   `IdentitiesOnly=yes`, `StrictHostKeyChecking=yes`, and the project-local
   known-hosts file.
6. Verify the local remote/config, host-key fingerprint, key fingerprint, and
   permissions without contacting the Git repository.
7. Print the complete `.pub` line and its SHA-256 fingerprint for the Human
   Owner, append the bounded handback, and stop.

## Forbidden writes and actions

- Printing, copying, uploading, or exposing the private key; reusing the XC
  server login identity
- `ssh -T`, `git ls-remote`, fetch, pull, push, force-push, tag publication,
  GitHub API mutation, `gh auth`, credential prompts, or any other repository
  authentication attempt
- Adding the Deploy key on behalf of the Human Owner or changing GitHub rulesets,
  branch protection, repository visibility, collaborators, secrets, or settings
- Global Git/SSH configuration, the user's global known-hosts file, parent Git
  metadata, sibling projects, implementation, raw evidence, contracts,
  approvals, Claims, T001/T005, research Gate 0, GPU/model/data/Docker work
- Any package/tool installation in this batch

## Acceptance

- The public key and its fingerprint are delivered; the private key remains only
  at the dedicated server path with restrictive permissions.
- GitHub's scanned ED25519 host key matches an official GitHub source, and the
  repository-local SSH command enforces strict checking against that exact key.
- `origin` equals the authorized URL; no authentication or push has occurred.
- `main` and the parent repository remain unchanged; the worktree contains
  only the permitted ledger handback.
- Hosted CI and branch protection remain unverified and conditional. T001 is not
  authorized.

## Stop conditions

- Either dedicated key path already exists, the official/scanned host
  fingerprints differ, `origin` exists with another URL, or strict host-key
  checking cannot be made project-local
- Any step requires root/global mutation, an installation, an unknown script,
  broader network access, a credential prompt, authentication, or push
- Immediately after the public key is displayed: wait for the Human Owner to add
  it under GitHub Repository Settings -> Deploy keys with write access

## Required handback and next authority

Append one `Batch T000-R2 - pre-authentication handback` block to
`PROGRESS.md` with exact commands/outcomes, the public-key fingerprint,
official host-key source and matched fingerprint, permissions, local remote/SSH
configuration evidence, unchanged `main`, and explicit confirmation that no
authentication or push was attempted. Set `Status: HANDED BACK FOR REVIEW` and
stop.

The Human Owner must add the displayed public key and explicitly reply that it
has been added. That confirmation does not retroactively authorize
authentication, push, or hosting-setting changes; a fresh Reviewer must prepare
the next HANDOFF. Hosted branch protection remains a T000 condition.
