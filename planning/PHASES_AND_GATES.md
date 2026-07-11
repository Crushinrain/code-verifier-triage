# Phases and Gates

| Gate | Goal | Required report | Human approval | Next action if failed |
|---|---|---|---|---|
| -1 | Legal, security, hardware | `gate_minus1_report.md` | Yes | Stop or fix environment |
| 0 | Reproduce upstream, protocol, cost | `gate0_protocol_and_cost.md` | Yes | Fix protocol, no data scale-up |
| 1 | Verify dangerous FP prevalence | `gate1_failure_audit.md` | Yes | Stop or pivot |
| 2 | Beat random/margin offline | `gate2_selective_risk.md` | Yes | RM repair or stop |
| 3 | Improve BoN at fixed budget | `gate3_bon.md` | Yes | Keep offline project only |
| 4 | 20–30 step RL smoke | `gate4_rl_smoke.md` | Yes | Debug, no pilot |
| 5 | Two independent seed pilot | `gate5_pilot.md` | Yes | Stop online claim |
| 6 | 3-seed final | `gate6_final.md` | Final approval | Freeze claims |
| 7 | 4B/cross-RM confirmation | `gate7_extension.md` | Yes | Optional |

## Universal stop conditions

- final test access before approval;
- split/config/data hash drift;
- sandbox isolation failure;
- executor errors mislabeled as failures;
- missing run manifest;
- unsupported claim;
- repeated OOM/deadlock after defined fallback;
- lack of disk safety margin;
- missing human approval.
