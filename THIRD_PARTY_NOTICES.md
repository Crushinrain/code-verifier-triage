# Third-Party Notices

Status: preliminary T000 inventory, 2026-07-11.

This file records third-party components named by the starter pack. It is not a
license clearance, and it does not authorize redistribution. T003 must verify
each license against the pinned upstream source before code, weights, datasets,
or derived distributions are published.

## Declared components

| Component | Declared source | Revision in starter contract | Starter-pack license declaration | T000 use |
|---|---|---|---|---|
| CodeScaler | `https://github.com/LARK-AI-Lab/CodeScaler` | `e1717833cf88a6bac3630af697f899e49493e8f5` | Root repository license unresolved | Reference metadata only; do not vendor or redistribute |
| RewardUQ | `https://github.com/lasgroup/rewarduq` | `7224a1d35849e608fbe92a3bf2292028d8b39787` | Apache-2.0, pending source verification | Reference metadata only |
| SandboxFusion | `https://github.com/bytedance/SandboxFusion` | `add46a79a614f84a64f80b4b59002fefeb4b7607` | Apache-2.0, pending source verification | Reference metadata only |
| Qwen3-1.7B-Base | `Qwen/Qwen3-1.7B-Base` | unresolved until Gate 0 | Verify model card | No download or use in T000 |
| CodeScaler-1.7B | `LARK-Lab/CodeScaler-1.7B` | unresolved until Gate 0 | MIT per model-card declaration; not independently verified | No download or use in T000 |
| Qwen3-4B-Base | `Qwen/Qwen3-4B-Base` | optional and unresolved | Verify model card | No download or use in T000 |
| DeepCoder Preview Dataset | `agentica-org/DeepCoder-Preview-Dataset` | `e0c06632fc6cda32a81827a63308505fc0a67abb` | Verify dataset card and source subsets | No download or use in T000 |
| CodeScalerPair-51K | `LARK-Lab/CodeScalerPair-51K` | unresolved until Gate 0 | MIT per dataset-card declaration; not independently verified | No download or use in T000 |

All names and revision declarations above come from
`contracts/upstream.lock.yaml`; no upstream repository, model, or dataset was
accessed during T000. Preserve upstream copyright and notice files when T003
establishes that copying is permitted.
