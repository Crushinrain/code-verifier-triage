# Decision Log

## Template

```text
DEC-ID:
Decision:
Date:
Alternatives considered:
Evidence:
Reason:
Impact:
Rollback condition:
Approved by:
```

## Initial decisions

```text
DEC-001
Decision: MVP uses group-level routing, not candidate-level mixed rewards.
Reason: isolate reward-scale confounds within GRPO groups.
Rollback: only as a post-Gate-5 ablation.
```

```text
DEC-002
Decision: Start with Qwen3-1.7B policy and CodeScaler-1.7B.
Reason: fit 4x24GB hardware and maximize experiment throughput.
Rollback: 4B only after 1.7B evidence passes Gate 6.
```
