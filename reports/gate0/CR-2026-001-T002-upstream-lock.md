# Contract Change Request — CR-2026-001

## Requested change

Task T002 requests one bounded revision-lock update to
`contracts/upstream.lock.yaml` after the independently reviewed T005 active
contract-digest mechanism is available:

- add an explicit lock version and update the lock generation date;
- preserve the three existing official repository URLs and their already pinned
  full commits;
- replace only the model and dataset `RESOLVE*` placeholders with immutable
  revisions observed from the official Hugging Face API;
- replace model/dataset `VERIFY_*_CARD` license placeholders only with the
  license identifiers returned in the same official metadata;
- leave the SandboxFusion image and digest unresolved for T018, without claiming
  that T002 built or inspected a container.

Proposed immutable revisions:

| Kind | Canonical ID | Revision | Card license |
|---|---|---|---|
| model | `Qwen/Qwen3-1.7B-Base` | `ea980cb0a6c2ae4b936e82123acc929f1cec04c1` | `apache-2.0` |
| model | `LARK-Lab/CodeScaler-1.7B` | `3db4f021f8e8b7b94549577de0175cfea5514dfc` | `mit` |
| model | `Qwen/Qwen3-4B-Base` | `906bfd4b4dc7f14ee4320094d8b41684abff8539` | `apache-2.0` |
| dataset | `agentica-org/DeepCoder-Preview-Dataset` | `e0c06632fc6cda32a81827a63308505fc0a67abb` | `mit` |
| dataset | `LARK-Lab/CodeScalerPair-51K` | `f171a14323c0a7858261cfce2d4e8a0ab177c06e` | `mit` |

## Reason and new evidence

The existing contract intentionally contains Gate-0 placeholders. Official
metadata resolution and exact-revision repository verification are now complete.
The ignored provenance artifact is
`artifacts/provenance/upstream_manifest.json`, SHA-256
`75e1a6a7144541acbc55339f1de0449d05ac0373ad95cf77035c84ec7b6bf7ed`.

Direct server HTTPS attempts timed out and are retained as negative evidence.
The same Executor therefore exact-fetched each named official GitHub HTTPS URL
from the Windows controller, transferred checksum-bound complete Git bundles,
and independently verified each bundle, detached revision, origin URL, clean
status, tree, and `git fsck` on the server. No mirror or alternate upstream was
used. Raw official Hugging Face JSON responses and response headers are retained
under the ignored T002 provenance directory and bound by hashes in the manifest.

## Frozen files affected

- `contracts/upstream.lock.yaml`
- the T005-owned active-contract expected digest, updated atomically only after
  the reviewed T005 mechanism exists

No other contract, approval, task graph, Claim, starter manifest, or protocol is
requested for change.

## Expected effect on comparability

Positive: future runs can bind repositories, model cards, and dataset cards to
immutable source revisions. The requested change does not alter model choice,
data role, metric, split, reward, execution budget, or training configuration.

## Runs invalidated or requiring rerun

None. No project experiment, model load, data payload access, candidate execution,
or training run has occurred.

## Migration plan

1. Wait for an independently reviewed T005 commit that defines the active digest.
2. Apply only the exact placeholder replacements above on top of that reviewed SHA.
3. Regenerate the active contract digest atomically with the contract change.
4. Re-run bundle validation, active-digest validation, workflow inspect/validate,
   and verify that no repository/model/dataset entry contains `main`, `latest`, or
   `RESOLVE*`.
5. Submit the single T002 boundary for fresh independent review.

## Reviewer decision

- [ ] APPROVED as contract version __
- [ ] REJECTED
