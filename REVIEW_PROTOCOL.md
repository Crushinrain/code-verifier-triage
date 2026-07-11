# Review Protocol

## Independence

T000 must be reviewed in a fresh, role-locked Reviewer context. The Executor's
summary is navigation only; the Reviewer rereads repository state, semantic
documents, staged/committed source, and primary command evidence.

Every formal review appended to `PROGRESS.md` must contain exactly one of each:

- `Reviewer platform: Codex|Claude`
- `Reviewer independence: PASS - <evidence this context did not perform T000>`
- `Gate decision: APPROVE|CONDITIONAL APPROVE|REJECT|NOT READY FOR REVIEW`

## T000 review procedure

1. Confirm `.workflow/project.json` resolves four distinct semantic documents
   and that `PROGRESS.md` contains exactly one Reviewer identity policy activation.
2. Confirm branch `main`, exactly one root commit, a clean worktree, and no Git
   remote invented by the Executor.
3. Inspect the complete root commit and verify that frozen contracts, approvals,
   and legacy planning Claim/task files equal the 91-entry starter manifest.
4. Re-run:
   - `sha256sum -c MANIFEST.sha256`
   - `/data3/xc/.conda/envs/d2l/bin/python scripts/validate_bundle.py`
   - `python3 /data3/xc/.agents/skills/governing-project-workflows/scripts/workflow.py inspect . --json`
   - `python3 /data3/xc/.agents/skills/governing-project-workflows/scripts/workflow.py validate . --json`
   - the workflow skill test suite with the existing `d2l` interpreter
5. Verify the installed skill contains only the 18 expected files with the
   recorded hashes and did not overwrite sibling skills.
6. Compare `/data3/xc/.git/HEAD`, `config`, and `index` hashes to the preflight
   values in the ledger; inspect parent status and ensure `PV_forecast` was not
   changed by T000.
7. Verify ignored/generated paths are not tracked and no GPU, model, data,
   Docker, upstream, candidate execution, or final access occurred.
8. Mark hosting-level branch protection as failed/blocked unless a real remote
   and protection evidence are supplied; do not infer protection from prose.

## Decision boundary

T000 may be accepted only for local bootstrap evidence. Missing branch
protection must remain an explicit limitation or condition. A T000 verdict does
not authorize T001, research Gate 0, a contract change, or any gated action.

After the verdict, only the Reviewer may prepare the next HANDOFF. Ledger edits
are tail appends; history is never rewritten.
