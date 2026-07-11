---
title: "CodeVerifier-Triage：Agent 执行手册"
subtitle: "任务图、权限边界、验收标准与运行 SOP"
date: "2026-07-11"
version: "1.0"
---

> 本手册的目标是让 Coding Agent 能够在不依赖隐含上下文的情况下逐项实现项目，同时阻止 Agent 擅自扩大 scope、启动昂贵训练、修改最终评测或用结果反向调整协议。

# 1. 如何使用这份执行包

## 1.1 启动顺序

1. 解压执行包并初始化 Git；
2. 阅读 `contracts/project.yaml`；
3. 运行 `python scripts/validate_bundle.py`；
4. 读取当前 Gate checklist；
5. 从 `tasks/task_graph.yaml` 选择依赖已完成的 Task ID；
6. 将 `prompts/AGENT_SYSTEM.md` 与对应角色 prompt 提供给 Agent；
7. 一个 Task ID 对应一个 branch、commit 或 PR；
8. 验收通过后更新 task status 和 evidence index；
9. 只有人工 Gate review 可以授权下一阶段。

## 1.2 推荐仓库布局

```text
code-verifier-triage/
├── contracts/                 # 冻结实验合同
├── schemas/                   # 数据与运行记录 Schema
├── tasks/                     # 任务图、Backlog、Gate 矩阵
├── prompts/                   # Agent 角色提示词
├── templates/                 # Run/Gate/Failure/Claim 模板
├── src/
│   ├── prompts/
│   ├── extraction/
│   ├── scoring/
│   ├── execution/
│   ├── labels/
│   ├── risk/
│   ├── routing/
│   ├── evaluation/
│   └── training/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── golden/
│   └── security/
├── infra/sandbox/
├── patches/                   # 对上游最小补丁，不大规模复制未明许可源码
├── artifacts/                 # Git 忽略；有 hash/manifest
├── runs/                      # 每个 run 独立目录
├── reports/gates/
└── docs/
```

## 1.3 Agent 的权限分级

| 权限 | Agent 可做 | Agent 不可做 |
|---|---|---|
| L0 阅读 | 读代码、文档、合同、日志 | 修改文件 |
| L1 实现 | 修改任务范围内代码、写测试 | 改冻结合同、访问 final |
| L2 离线运行 | CPU 测试、小规模 RM scoring | 启动 policy RL |
| L3 GPU smoke | 明确命令和预算内运行 | 自动扩大 step、模型或 seed |
| L4 正式实验 | 只执行已签署预注册 | 换 seed、挑结果、重跑 final |

GPU、final test 和合同修改均需要人类显式授权。

# 2. Agent 角色

## 2.1 Planner

负责：任务拆分、依赖检查、Gate 材料、scope 控制。不能同时担任最终 Gate Reviewer。

## 2.2 Implementer

负责：单一 Task ID 的代码和测试。必须提供回滚和 failure path。

## 2.3 Data Steward

负责：revision、许可、problem hash、去重、split、测试泄漏、数据卡和 retention。

## 2.4 Security Reviewer

负责：沙箱、容器、cgroups、恶意代码样例、密钥和日志。安全审查不得由实现 Agent 自己批准。

## 2.5 Experiment Operator

负责：按冻结 manifest 运行命令、记录资源和故障；不得解释性修改配置。

## 2.6 Experiment Reviewer

负责：matched budget、seed、checkpoint、统计、protocol deviation 和 Claim。结果为正不降低审查标准。

# 3. 一次任务的标准生命周期

## 3.1 Before

Agent 必须输出：

- Task ID；
- 单一目标；
- 非目标；
- 依赖文件及 hash；
- 将修改的文件；
- 验收测试；
- 是否需要 GPU/安全权限。

任何依赖缺失时停止，不自行生成“看起来合理”的替代产物。

## 3.2 Implement

- 先补测试；
- 做最小实现；
- 所有随机性可设 seed；
- 所有数据记录 schema version；
- 失败必须显式抛出，不静默 fallback；
- 不在日志打印测试内容、密钥或完整大样本。

## 3.3 Verify

至少运行：

```bash
python scripts/validate_bundle.py
pytest -q tests/<task_related_tests>
python scripts/check_contract_freeze.py
```

涉及数据的任务还要：

- 行数和唯一键检查；
- problem overlap=0；
- schema validation；
- artifact hash。

涉及 GPU 的任务还要：

- 最大显存；
- GPU-seconds；
- batch/throughput；
- 温度/Xid；
- run manifest。

## 3.4 Review

PR 必须回答：

- 唯一变化是什么；
- 哪个测试证明成功；
- 是否触碰冻结合同；
- 数据泄漏/安全影响；
- 失败模式；
- 如何回滚；
- 产物和 hash。

# 4. Gate 0 详细执行 SOP

## 4.1 主机检查

建议命令：

```bash
nvidia-smi
nvidia-smi topo -m
nvidia-smi -q -d TEMPERATURE,POWER,MEMORY
uname -a
lsb_release -a || cat /etc/os-release
lscpu
free -h
df -hT
docker info
stat -fc %T /sys/fs/cgroup
```

输出写入 `artifacts/inventory/`。不得只在聊天中描述。

## 4.2 上游锁定

```bash
git clone https://github.com/LARK-AI-Lab/CodeScaler.git upstream/CodeScaler
cd upstream/CodeScaler
git checkout e1717833cf88a6bac3630af697f899e49493e8f5
git rev-parse HEAD
git status --porcelain
```

RewardUQ 与 SandboxFusion 同理。模型与数据使用 Hugging Face API 解析实际 SHA。任何 `main`、`latest` 或只有 Docker tag 的记录都不满足验收。

## 4.3 环境策略

不要把三个仓库强行装入一个环境：

- `env-codescaler`：复现上游；
- `env-rewarduq`：UQ baseline；
- `env-orchestrator`：数据、router、统计；
- `sandbox image`：完全隔离。

先复现上游 pin，再考虑兼容升级。FlashAttention wheel 与 CUDA/torch 不匹配时，可暂时使用 SDPA 完成协议 smoke；不要为追新版本同时升级 torch、vLLM、transformers。

## 4.4 数据注册表

Agent 不能直接把原始 Dataset object 当长期事实源。必须生成：

- `problem_id`；
- `problem_hash`；
- source；
- split；
- prompt text hash；
- starter code hash；
- test suite hash；
- dataset revision；
- license source。

测试正文与公开 registry 分离。

## 4.5 Canonical extractor 流程

1. 收集上游 train/eval extractor；
2. 对相同 1000 响应做差分；
3. 建立至少 20 个 golden cases；
4. 实现单一 canonical extractor；
5. 将所有路径改为调用它；
6. 对上游 patch 做最小化；
7. 固定 extractor version/hash。

## 4.6 RM adapter 流程

需要返回：

```python
@dataclass
class RMScore:
    candidate_id: str
    raw_score: float
    shaped_score: float
    input_tokens: int
    truncated: bool
    code_tail_visible: bool
    actual_input_hash: str
    model_revision: str
    tokenizer_revision: str
    adapter_version: str
```

测试：重复评分、批序、单/批 parity、不同 max length、NaN、空代码。

## 4.7 Sandbox 验收

任何候选代码执行前，Security Reviewer 必须签署 `sandbox_acceptance.md`。重点不是“能运行 Python”，而是：

- 恶意代码被限制；
- timeout 后没有孤儿进程；
- OOM 不拖垮宿主；
- stdout 不撑爆日志；
- network 和 host mount 不可用；
- infra failure 与 wrong answer 可区分。

## 4.8 成本审计

同一批至少 1000 candidates 分别测：

```text
RM scoring only
execution only
RM + router
RM + router + selected execution
full execution
```

保持硬件、并发、warm-up 和缓存状态一致。输出 raw parquet，不只给平均数。

# 5. Gate 1 数据闭环 SOP

## 5.1 生成 runner 必须支持

- problem shard；
- stable seed；
- 原子写；
- 断点恢复；
- 去重；
- 幂等；
- 每个候选唯一 ID；
- 生成 config hash；
- policy revision；
- cap-hit 与 stop reason。

## 5.2 全量标注顺序

```text
raw response
  -> canonical extraction
  -> RM score
  -> sandbox execution
  -> candidate record
  -> group labels
  -> pre-execution features
```

严禁先看到执行结果再修改提取或特征规则；需要修改必须创建新 version 并重新处理全部样本。

## 5.3 危险 FP 人工复核

随机抽取并分层抽取至少 50 个：

- 高分错误；
- 高分正确；
- 低 margin；
- 长代码；
- 截断；
- compile/runtime/logic error；
- 不同 source。

复核问题：

- 是真正逻辑错，还是 evaluator/测试不完整；
- extractor 是否拿错代码；
- RM 是否看不到代码尾部；
- 测试是否 infra failure；
- 是否存在明显长度/术语 shortcut。

# 6. Gate 2 风险模型 SOP

## 6.1 简单 baseline 先行

Agent 先输出无需训练的 risk–coverage：

- 负 margin；
- 小 margin；
- score std；
- invalid/AST；
- response length；
- static-analysis warning count。

只有在这些基线被正确实现后，才训练 Logistic/GBDT/MLP。

## 6.2 双头模型接口

```python
@dataclass
class RiskPrediction:
    group_id: str
    p_optimization_fp: float
    p_avoidable_selection_fp: float
    p_mixed_outcome: float | None
    calibration_revision: str
    feature_version: str
    model_revision: str
```

MVP corrective routing 使用 `p_avoidable_selection_fp`。`p_optimization_fp` 主要控制 audit strata 和监控。

## 6.3 校准边界

- 训练模型只用 risk_train；
- Platt/isotonic 只用 calibration；
- dev 选择模型/预算；
- final 禁止访问；
- 不在同一 dev 上无限尝试大量 feature 组合；
- 每次 feature change 记录 experiment card。

## 6.4 成功判据

主要看固定预算下捕获危险错误的能力，不看单一 AUROC。报告：

- PR-AUC；
- recall@10/25/50% candidate-execution budget；
- precision@k；
- risk–coverage；
- Brier/ECE；
- source/length/checkpoint slice；
- problem bootstrap CI。

# 7. Gate 3 路由模拟与 BoN SOP

## 7.1 预算控制

假设 group size=4、1000 groups、25% 执行比例，则预算是 1000 candidate executions，即 250 groups。random audit 必须包含在这 250 groups 中，不能额外免费执行。

## 7.2 对照

所有路由方法接收相同 group 和 RM score；只改变被执行的 group。不得让方法间生成不同候选。

## 7.3 选择逻辑

- 未执行 group：选择 RM top1；
- 已执行 group：选择任一通过候选；若多个通过，使用冻结 tie-break；
- 全错 group：选择规则保持一致，不假设执行能创造正确答案；
- infra error group：从本次对比中剔除并报告。

## 7.4 固定输出

每个预算点输出：

- selected groups；
- candidate executions；
- caught optimization FP；
- caught avoidable FP；
- BoN accuracy；
- selection regret；
- CPU/GPU/wall-clock；
- IPW population risk；
- bootstrap CI。

# 8. Gate 4 RL 接入 SOP

## 8.1 先画数据流

Agent 在修改代码前必须给出：

```text
rollout responses
 -> canonical extractor
 -> router features
 -> route decisions
 -> RM or execution rewards
 -> reward tensor
 -> group normalization
 -> group filtering/resampling
 -> actor loss
```

指出每个字段在 DataProto 中的名字和 shape。

## 8.2 Reward manager 必须满足

- route decision 发生在执行前；
- 整组同一 reward mode；
- execution/MR 原始值、最终 reward、advantage 可追踪；
- router disabled 精确退化；
- infra error 不更新；
- uniform execution group 明确 skip；
- route/audit propensity 写入日志；
- 测试正文不进入 actor/RM/router 日志。

## 8.3 Golden batch

建立固定的 synthetic batch，至少 6 个 group：

```text
G1: execution [0,1,0,1]
G2: execution [0,0,0,0]
G3: execution [1,1,1,1]
G4: RM [0.1,0.2,0.4,0.3]
G5: invalid candidate included
G6: infra error
```

测试最终 reward、group variance、skip mask、advantage、有效 group count。

## 8.4 Smoke 递进

1. CPU/单元测试；
2. 1 GPU、1 batch、1 update；
3. 1 GPU、5 steps；
4. 4 GPU、5 steps；
5. 4 GPU、20–30 steps；
6. 只有 Gate 4 才能进入 50-step pilot。

每一步失败都从最近的最小规模复现，不直接重复四卡长跑。

# 9. Gate 5/6 正式实验 SOP

## 9.1 Arm 固定

最终核心：

- P1 full execution；
- P2 RM-only；
- P4 random hybrid；
- P6 drift-aware router。

各 arm 匹配：

- train problems/order；
- group size；
- candidates；
- max tokens；
- optimizer steps；
- adaptation method；
- KL；
- checkpoint/eval frequency；
- 总生成候选/token；
- P4/P6 执行预算。

P1 执行预算天然更高，必须作为可靠性上限而不是成本匹配对照。

## 9.2 Seed

`seed1/2/3` 必须控制完整训练随机性。任何失败 seed 不能用 `seed4` 静默替换；需要在 failure report 说明是否重跑同 seed。

## 9.3 Checkpoint

只允许：

- 固定 final step；或
- 预注册 dev 指标选择。

不得在 final 上挑 checkpoint，不得把最好单 seed 写成平均结果。

## 9.4 Final

- final registry Gate 6 前不可读；
- 解封后只跑一次冻结 evaluator；
- 运行失败若是 infra，按预注册规则重试；
- 结果差不能重跑或改 sampling；
- 原始输出、日志、config、hash 只读归档。

# 10. 运行与故障管理

## 10.1 Run 目录

```text
runs/<run_id>/
├── run_manifest.yaml
├── resolved_config.yaml
├── command.sh
├── stdout.log
├── stderr.log
├── metrics.jsonl
├── resource.jsonl
├── artifacts.json
├── protocol_deviations.md
└── failure_report.md  # 如需要
```

## 10.2 自动停止条件

- NaN/Inf；
- GPU OOM 连续两次；
- sandbox infra error 超过预设比例；
- candidate/group 对齐错误；
- tests 泄漏；
- router execute-all/none 非预期；
- reward 或 advantage no-op；
- 温度/Xid/磁盘异常；
- config hash 与 manifest 不一致。

Agent 不能通过降低日志、跳过样本或更换 seed “修复”这些问题。

## 10.3 恢复

恢复必须验证：

- checkpoint hash；
- optimizer state；
- dataloader/problem cursor；
- RNG state；
- router revision；
- budget window；
- execution cache revision。

不能只加载模型权重然后称为同一 run 继续。

# 11. Agent 交付格式

每个 Task 完成后，Agent 用以下结构回复：

```text
Task ID / commit
目标与非目标
变更文件
测试命令与结果
生成 artifacts + SHA256
资源消耗
Protocol deviations
剩余风险
回滚
是否满足验收
是否请求下一任务（不等于批准）
```

# 12. 最小启动清单

从零开始时只授权以下任务：

```text
T000 初始化仓库
T001 主机清单
T002 上游锁定
T003 许可证审计
T004 环境
T005 合同 CI
```

完成后再授权数据和安全任务。第一周不得启动 policy RL。

# 13. 常见 Agent 失败模式

| 失败模式 | 阻止方式 |
|---|---|
| 看到错误就顺手改 prompt | prompt 是冻结 contract；提交 CR |
| 自动升级依赖解决冲突 | 先复现 pin；升级需单独任务 |
| 用 final 验证修复 | final 密封；用 golden/dev |
| 忽略 infra error | schema 强制独立状态 |
| 只报告 W&B 最好曲线 | run manifest + raw metrics +统计脚本 |
| 用更多生成预算赢 baseline | exposure ledger 强制匹配 |
| 把 UQ variance 当概率 | calibration +事件标签 |
| 在宿主 subprocess 执行 | security CI 与独立 sandbox |
| 为了有效梯度自动重采样 | 默认关 filter；预算账本 |
| 结果不好换 seed | seed registry 与 failure report |

# 14. 文件导航

- `contracts/`：不可随意修改的实验事实合同；
- `tasks/task_graph.yaml`：Agent 唯一任务源；
- `tasks/backlog.md`：69 个任务的可读版本；
- `checklists/`：Gate 人工验收；
- `prompts/`：角色提示词；
- `schemas/`：数据格式；
- `templates/`：run、实验、Gate、failure、claim；
- `scripts/validate_bundle.py`：执行包一致性；
- `scripts/new_run.py`：创建 run 目录；
- `scripts/hash_artifacts.py`：产物 hash；
- `templates/risk_register.csv`：风险台账；
- `templates/metrics_dictionary.csv`：指标口径。
