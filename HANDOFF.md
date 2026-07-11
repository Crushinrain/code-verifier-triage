# HANDOFF - Current batch

## Batch identity

- Repair batch: T000-R4
- Parent Task ID: T000
- Title: Retry authentication through a fixed argv-safe probe and conditionally publish
- Active role: EXECUTOR
- Required context: a fresh role-locked Executor that did not perform the T000-R3
  formal review
- Base: current tip of `review/t000-r3`
- Required work branch: `fix/t000-r4-safe-probe`
- GPU required: no
- T001 authorization: no

## Failure context and single objective

T000-R3 stopped safely because its sole authentication attempt returned no
child exit/output markers. Authentication, remote emptiness, and publication
remain unproven. Perform one bounded retry through a fixed repository-local
Python controller using safe argv only; conditionally run one empty-remote check
and one atomic non-forced push; record durable evidence and stop.

## Authorized writes and network budget

- Repository-local Git metadata needed to create `fix/t000-r4-safe-probe`
- Fixed controller and temporary evidence files only under
  `/data3/xc/code-verifier-triage/.git/t000-r4-*`
- One GitHub SSH authentication retry, at most one `git ls-remote origin`, and,
  only after both exact gates pass, one non-forced atomic push
- `PROGRESS.md`, tail append only, and one local T000-R4 handback commit

No package installation, key/config change, or broader network action is
authorized.

## Mandatory offline preflight

1. Start from clean `review/t000-r3`, create
   `fix/t000-r4-safe-probe`, record all listed source SHAs, and confirm local
   `main` remains `90fc21ec1a4f3acce23ad13dc66f7af66c55bd94`.
2. Reverify exact `origin`, repository-local `core.sshCommand`, public-key and
   known-host fingerprints, and private-key mode 600 without reading private-key
   content.
3. Require `/usr/bin/ssh`, `/usr/bin/git`, and GNU `/usr/bin/timeout`.
   Confirm every `.git/t000-r4-*` output path is absent; never overwrite prior
   evidence or retry after creation.
4. Create one fixed
   `.git/t000-r4-network-probe.py` using only the Python standard library.
   It accepts no arguments or stdin, has mode 700, uses absolute executable and
   file paths, and invokes every child with `subprocess.Popen(argv,
   shell=False, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
   stderr=subprocess.PIPE)`.
5. The controller must use `communicate(timeout=25)` for authentication and
   `ls-remote`; include SSH `ConnectTimeout=15`; use a bounded timeout no
   greater than 60 seconds for the sole push. On timeout it must kill and reap
   the child, set `timed_out=true`, and never retry.
6. Run `python -m py_compile` on the controller, record its SHA-256 and
   permissions, review its fixed argv/refspec constants, and confirm it contains
   no private-key bytes, credential value, shell invocation, inline Bash,
   command substitution, `eval`, or user-controlled argument.
7. Invoke only the fixed controller through GNU timeout. The outer PowerShell/SSH
   command must contain no `$()`, `$?`, nested quotes carrying shell state,
   or inline remote logic.

## Controller evidence contract

For each attempted stage, create separate exclusive mode-600 files under
`.git/`: `t000-r4-<stage>.stdout`, `.stderr`, and `.rc`. Also create one
`t000-r4-result.json` and print exactly that single JSON object after all
children are reaped. Do not include private-key content or arbitrary stderr text
in JSON; include only stage, child rc, timed_out, byte counts, SHA-256 hashes,
and exact-match booleans.

Authentication argv is fixed to:

- `/usr/bin/ssh`
- `-i /data3/xc/.ssh/code_verifier_triage_github_ed25519`
- `-o IdentitiesOnly=yes`
- `-o UserKnownHostsFile=/data3/xc/code-verifier-triage/.git/github_known_hosts`
- `-o StrictHostKeyChecking=yes`
- `-o BatchMode=yes`
- `-o ConnectTimeout=15`
- `-T git@github.com`

Authentication succeeds only when the outer controller exits 0, child rc is
exactly 1, `timed_out=false`, stdout is empty, and stderr bytes exactly equal
this one newline-terminated line:
`Hi Crushinrain/code-verifier-triage! You've successfully authenticated, but
GitHub does not provide shell access.`

If any condition differs, write diagnostic metadata, do not run `ls-remote` or
push, hand back FAIL, and stop.

## Conditional remote-empty check and push

Only after exact authentication success, the same controller may run safe argv
`/usr/bin/git -C /data3/xc/code-verifier-triage ls-remote origin` once.
Require child rc 0, `timed_out=false`, and empty stdout; any ref, symbolic ref,
error, prompt, or timeout stops before push.

Only after that exact empty result, run one
`git push --porcelain --atomic origin` with exactly these eight refspecs:

- `refs/heads/main:refs/heads/main`
- `refs/heads/review/t000-initial:refs/heads/review/t000-initial`
- `refs/heads/fix/t000-r1-controls:refs/heads/fix/t000-r1-controls`
- `refs/heads/review/t000-r1:refs/heads/review/t000-r1`
- `refs/heads/fix/t000-r2-github-transport:refs/heads/fix/t000-r2-github-transport`
- `refs/heads/review/t000-r2:refs/heads/review/t000-r2`
- `refs/heads/fix/t000-r3-initial-publish:refs/heads/fix/t000-r3-initial-publish`
- `refs/heads/review/t000-r3:refs/heads/review/t000-r3`

The last two are the minimum additional governance evidence: the R3 failed
handback and its formal R3 review/R4 authorization. Do not push the new
`fix/t000-r4-safe-probe` branch because its evidence commit is created only
after the network sequence.

## Forbidden actions

- Inline Bash/PowerShell capture logic, shell=True, nested command substitution,
  dynamic argv/refspecs, a credential prompt, reading/logging the private key, or
  accepting a new host key
- Any retry beyond the one controller invocation; a second auth, `ls-remote`,
  or push; fetch, pull, clone, merge, rebase, reset, force, deletion, tags,
  upstream setup, mirror, or all-branches push
- GitHub API/CLI mutation, PR, ruleset, branch protection, repository settings,
  Deploy-key change, global/root mutation, installation, implementation/raw
  evidence/contracts/approvals/Claims, T001/T005, Gate 0, GPU/model/data/Docker

## Acceptance and handback

- Offline controller validation and every child result satisfy the evidence
  contract; the sole push succeeds atomically for all and only eight listed refs.
- Local `main`, parent repository, keys/config, and prohibited paths remain
  unchanged. Hosted ruleset/branch protection remains unverified.
- Append one `Batch T000-R4 - safe probe handback` block with controller hash,
  exact JSON, result-file hashes/sizes/rc values, source SHAs, push porcelain
  evidence or fail-closed reason, and all scope checks. Never append private-key
  or unexpected raw stderr content.
- Create one local commit on `fix/t000-r4-safe-probe`, set
  `Status: HANDED BACK FOR REVIEW`, and stop for a fresh Reviewer. No further
  authentication, remote access, hosted settings, T001, or Gate 0 action is
  authorized.
