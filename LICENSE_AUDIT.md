# License Audit

Audit stage: T000 bootstrap inventory only.

Decision status: **NOT CLEARED FOR EXTERNAL DISTRIBUTION**.

Next binding task: T003 after T002 pins and locally records upstream evidence.

## Repository-level finding

The starter pack contains no project `LICENSE` file. T000 does not infer or
select a license for the Human Owner. Until a license is selected and approved,
this repository is for internal project execution only; external release is
also blocked by the `external_release: PENDING` approval.

## Dependency findings

| Asset | Evidence available in T000 | Status | Required next evidence |
|---|---|---|---|
| Starter pack | `MANIFEST.sha256` verifies integrity; no license file is included | UNRESOLVED | Human Owner selects project license and confirms ownership of authored material |
| CodeScaler source | Pinned URL/SHA and an unresolved-license warning in `contracts/upstream.lock.yaml` | BLOCKED | Inspect the pinned tree, root/subdirectory licenses, notices, and copied-file provenance |
| RewardUQ source | Apache-2.0 is declared in the starter contract | PENDING VERIFICATION | Capture the pinned license text and copyright notice |
| SandboxFusion source | Apache-2.0 is declared in the starter contract | PENDING VERIFICATION | Capture the pinned license text, NOTICE obligations, and container redistribution terms |
| Qwen models | Model-card license verification is explicitly pending | BLOCKED | Resolve immutable model/tokenizer revisions and archive license evidence |
| CodeScaler model/data | MIT is declared per remote cards, but T000 made no remote access | PENDING VERIFICATION | Archive the exact card/revision and inspect linked dataset sources |
| DeepCoder Preview Dataset | Source-subset licensing is explicitly unresolved | BLOCKED | Audit the dataset card, constituent sources, test-data restrictions, and redistribution boundary |

## T000 restrictions

- No third-party repository was cloned or vendored.
- No model, tokenizer, dataset, container, or candidate program was downloaded or executed.
- Only adapter code or patches may be considered later when a source repository
  does not establish a clear redistribution license.
- No result or artifact may be externally released from this inventory.

This document must not be treated as the completed T003 audit.
