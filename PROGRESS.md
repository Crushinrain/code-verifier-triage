# Progress Ledger

Append execution facts, handbacks, formal reviews, and corrections. Do not rewrite history.

### Reviewer identity policy activation
- Reviewer identity policy: required

### [2026-07-11 20:24 +08:00] T000 execution authorization and scope
- Active role: EXECUTOR; the context remained role-locked for the full batch.
- Authorization fact: the Human Owner continued the Reviewer-prepared T000 plan,
  explicitly authorizing creation of `/data3/xc/code-verifier-triage`, `git init`,
  and governing-project-workflows initialization.
- Authorized external skill path:
  `/data3/xc/.agents/skills/governing-project-workflows` (new path only).
- Prohibited actions remained prohibited: T001, GPU, model/data access, upstream
  clone, Docker change, candidate execution, final access, approval/contract
  mutation, environment installation, and writes to sibling projects or the
  parent Git control directory.

### [2026-07-11 20:25 +08:00] T000 copy and skill evidence
- Source facts: local `python scripts/validate_bundle.py .` returned
  `OK: 14 contracts, 6 schemas, 69 tasks, 7 Gate checklists`; a separate local
  parser verified 91/91 `MANIFEST.sha256` entries.
- Copy fact: the starter pack was copied to
  `/data3/xc/code-verifier-triage`; the destination did not exist at preflight.
- Remote integrity: `sha256sum -c MANIFEST.sha256` returned 91 checks and exit 0.
- Remote bundle validation: existing interpreter
  `/data3/xc/.conda/envs/d2l/bin/python` ran
  `scripts/validate_bundle.py` with the same OK result and exit 0. No package was
  installed and no environment was created.
- Skill installation: 18/18 remote files matched the local per-file SHA-256
  list. `pytest -q -p no:cacheprovider` returned
  `28 passed, 10 subtests passed` in 0.12 seconds.
- Workflow precondition: pre-init `workflow.py inspect` and `validate` each
  failed closed with the expected missing `.workflow/project.json` error.

### [2026-07-11 20:30 +08:00] T000 initialization and bounded changes
- Git fact: `git init -b main` created an independent nested repository. No
  identity existed, so only repository-local identity was set to
  `CodeVerifier-Triage-Executor <executor@local.invalid>`; global config was not
  changed. `git remote` returned zero entries.
- Workflow fact: explicit `workflow.py init` created one project contract and
  four semantic documents. Post-init `inspect --json` reported
  `READY_FOR_EXECUTION`; `validate --json` returned no errors or warnings.
- Added T000 files: `pyproject.toml`, `THIRD_PARTY_NOTICES.md`,
  `LICENSE_AUDIT.md`, `tasks/tickets/T000.md`, and
  `docs/governance/T000_GOVERNANCE_GAPS.md`; initialized semantic documents were
  concretized without changing `.workflow/project.json` defaults.
- Frozen-source evidence: the final pre-handback starter check still returned
  91/91 and the bundle validator still passed. Thus no file covered by the
  starter `MANIFEST.sha256`, including contracts and approvals, changed.
- Artifact hygiene: `git check-ignore -v` confirmed `artifacts/`, `runs/`,
  `outputs/`, `checkpoints/`, `*.parquet`, `*.safetensors`, and `*.pt`; no heavy
  artifact exists in those paths.
- Staged-tree hygiene: tracked counts for generated/heavy directories and
  `*.parquet`, `*.safetensors`, `*.pt`, and `*.bin` were all zero; the largest
  tracked file was 70,051 bytes. `git diff --cached --check` returned 2 because
  the immutable starter pack contains pre-existing Markdown hard breaks and
  UTF-8 CSV line endings flagged as trailing whitespace. New T000 Markdown was
  cleaned; manifest-covered files were preserved byte-for-byte.
- Parent isolation: parent HEAD stayed
  `4ecbc0f2bc7788a877684f7c896607a9bba78fb2`; SHA-256 values for parent
  `.git/HEAD`, `.git/config`, and `.git/index` remained respectively
  `f6f2b945f6c411b02ba3da9c7ace88dcf71b6af65ba2e0d89aa82900042b5a10`,
  `fe3ec500476aa33501be53335083aac4e5bf9827d7ae56b5610adb59b81dd49b`,
  and `93a62a777a2c738097a8183fc52c4130d5e0ade0a81d2c3174115c8dcee9195e`.
  Parent status retained the pre-existing `M PV_forecast`; expected new
  untracked paths are only the authorized project and workflow skill.
- Scope limitation: pre-commit and CI implementation were reserved for T005.
  No remote was guessed or created, so hosting-level main protection is blocked.

### [2026-07-11] Batch T000 - self-check & handback
- Task T000: fail - seven local-bootstrap criteria pass, but the mandatory
  hosting-level main-branch protection criterion is blocked by the absence of a
  Git remote URL and hosting administrator authority.
- Acceptance starter-pack integrity: pass - 91/91 SHA-256 checks, exit 0.
- Acceptance bundle validator: pass - 14 contracts, 6 schemas, 69 tasks, and 7
  Gate checklists validated remotely, exit 0.
- Acceptance workflow health: pass - one project contract/four distinct semantic
  documents; final inspect/validate must show no validation or approval errors.
- Acceptance skill integrity: pass - 18/18 hashes match; 28 tests and 10
  subtests pass.
- Acceptance Git boundary: pass - this handback is bound by the containing T000
  root commit on `main`; Reviewer must resolve the SHA with `git rev-parse HEAD`
  and verify one root commit plus a clean worktree.
- Acceptance artifact hygiene: pass - generated/heavy paths are ignored and no
  generated/heavy artifact is included.
- Acceptance parent isolation: pass - parent HEAD/config/index hashes are
  unchanged and `PV_forecast` remains the pre-existing user modification.
- Acceptance main protection: fail/block - zero remotes; no branch-protection or
  PR enforcement evidence can exist. The directly created root commit is only
  the explicitly authorized bootstrap exception.
- Protocol deviations: none hidden. The preserved starter-pack whitespace
  baseline, CI/pre-commit deferral, and absent branch protection are explicit
  limitations; no research Gate decision was written.
- Reviewer attention: independently verify the containing commit, final workflow
  state, parent hashes, unchanged 91-entry manifest, and the branch-protection
  blocker. Do not authorize or begin T001 from this handback.
- Status: HANDED BACK FOR REVIEW
