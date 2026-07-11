# Verification Checklists

## Before any data generation

- [ ] Upstream exact SHA locked
- [ ] Model/tokenizer exact revision locked
- [ ] License reviewed
- [ ] Generation config hash frozen
- [ ] Extractor golden tests pass
- [ ] Disk safety margin checked
- [ ] Human approval present

## Before any code execution

- [ ] Sandbox has no network
- [ ] Non-root and read-only root filesystem
- [ ] CPU/memory/PID/time/file limits
- [ ] Security attack suite passes
- [ ] Image digest locked
- [ ] No secrets mounted
- [ ] Executor error mapping tested

## Before risk model training

- [ ] Problem-level split locked
- [ ] Near duplicates do not cross splits
- [ ] At least 200 dangerous FP groups or approved alternative
- [ ] Oracle-derived features prohibited
- [ ] Margin/logistic baselines implemented
- [ ] Calibration split separate

## Before RL smoke

- [ ] Gate 3 approved
- [ ] Hybrid reward interface typed
- [ ] Golden advantage test passes
- [ ] KL appears exactly once
- [ ] Random audit propensity tested
- [ ] Zero-variance handling tested
- [ ] Stop conditions configured

## Before final evaluation

- [ ] Final protocol lock verified
- [ ] Git worktree clean
- [ ] Three independent training seeds complete
- [ ] Checkpoint selection already applied on dev
- [ ] Final directory read-only
- [ ] Human final-eval approval present
- [ ] Claims remain PROPOSED until review

## Before publication or resume use

- [ ] Every number has run IDs
- [ ] Absolute pp and relative % distinguished
- [ ] Failed runs/seeds disclosed
- [ ] Cost includes all components
- [ ] Test-suite success wording accurate
- [ ] Limitations included
- [ ] Claim status is SUPPORTED_FINAL
