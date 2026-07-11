# HANDOFF - Current batch

## Batch identity

- Task ID: T000
- Title: Initialize repository, governance control plane, and minimal structure
- Active role: EXECUTOR
- Authorization: Human Owner continuation on 2026-07-11, relayed by the
  role-locked Reviewer, explicitly including `git init` and workflow init.
- GPU required: no
- Human approval flag in task graph: false
- Completion boundary: hand back T000 and stop; T001 is not authorized.

## Single objective

Copy the verified starter pack into an independent nested Git repository at
`/data3/xc/code-verifier-triage`, initialize the governed workflow, add the
minimum missing T000 records, validate the result, and bind it in one root commit.

## Authorized writes

- `/data3/xc/code-verifier-triage/**`
- `/data3/xc/.agents/skills/governing-project-workflows/**` only for the
  non-overwriting skill installation authorized for this batch

## Forbidden writes and actions

- `/data3/xc/.git/**`, `/data3/xc/PV_forecast/**`, and every sibling project
- Existing remote skills other than the new named skill directory
- `contracts/**`, `approvals/**`, and the legacy planning Claim/task files
- Any final-test path, GPU task, candidate-code execution, Docker change,
  upstream clone, model/data download, or dependency/environment installation
- CI or pre-commit implementation reserved for T005
- Creating or guessing a Git remote, changing global Git config, or starting T001

## Required outputs

- The verified starter pack and independent `.git` repository on branch `main`
- `.workflow/project.json`, `PLAN.md`, `HANDOFF.md`, `PROGRESS.md`, and
  `REVIEW_PROTOCOL.md`
- `pyproject.toml`, `THIRD_PARTY_NOTICES.md`, and `LICENSE_AUDIT.md`
- `tasks/tickets/T000.md` and
  `docs/governance/T000_GOVERNANCE_GAPS.md`
- One meaningful T000 root commit and an append-only handback

## Acceptance

| Criterion | Required evidence |
|---|---|
| Starter-pack integrity | 91/91 entries pass `sha256sum -c MANIFEST.sha256` |
| Bundle structure | Remote `scripts/validate_bundle.py` passes using an already-existing interpreter |
| Workflow health | `workflow.py inspect` and `workflow.py validate` return no validation/approval errors after handback |
| Skill integrity | 18 installed files match local SHA-256 values; 28 tests and 10 subtests pass |
| Git boundary | Branch is `main`; one root commit contains T000; worktree is clean |
| Artifact hygiene | Heavy/generated paths remain ignored and no such artifact is committed |
| Parent isolation | Parent HEAD/config/index hashes are unchanged; pre-existing `M PV_forecast` is untouched |
| Main protection | Hosting-level protection proves Agents cannot commit directly to `main` |

## Known blocking limitation

No Git remote URL or hosting administrator authority was supplied. Therefore
hosting-level `main` branch protection and a PR rule cannot be configured or
verified in T000. The bootstrap root commit is an explicitly authorized local
exception; all subsequent work must use a task branch/PR once a remote exists.

## Gates

No governed action is configured or authorized by this HANDOFF. T000 does not
approve research Gate 0 or any later task.
