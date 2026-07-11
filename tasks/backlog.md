# CodeVerifier-Triage Agent Backlog

> 每项任务只允许解决一个明确问题。完成任务必须提交代码、测试、产物索引和简短结论。

## T000 — 初始化仓库、分支保护与目录结构

- 阶段：`G0-Governance`；Gate：`0`；负责人角色：`Planner`；估算：2h。
- 依赖：无。
- GPU：否；人工批准：否。

**执行动作**
- 从执行包复制 contracts/schemas/templates
- 初始化 Git；启用 pre-commit 与 CI
- 创建 THIRD_PARTY_NOTICES 与 LICENSE_AUDIT

**验收标准**
- [ ] bundle validator 通过
- [ ] main 分支禁止 Agent 直接提交
- [ ] 一次任务对应一个 commit/PR

**产物**
- `README.md`
- `.gitignore`
- `pyproject.toml`
- `THIRD_PARTY_NOTICES.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T001 — 采集主机、GPU、CPU、磁盘与拓扑清单

- 阶段：`G0-Governance`；Gate：`0`；负责人角色：`ExperimentOperator`；估算：2h。
- 依赖：T000。
- GPU：否；人工批准：否。

**执行动作**
- 运行 host inventory 命令
- 记录 nvidia-smi topo -m
- 确认 cgroups v2、Docker 与磁盘文件系统

**验收标准**
- [ ] 生成 machine_inventory.json
- [ ] 四卡均通过 30 分钟显存与通信 smoke
- [ ] 磁盘满足最低空间

**产物**
- `artifacts/inventory/machine_inventory.json`
- `reports/gate0/hardware.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T002 — 克隆并锁定上游 revision

- 阶段：`G0-Governance`；Gate：`0`；负责人角色：`DataSteward`；估算：3h。
- 依赖：T000。
- GPU：否；人工批准：否。

**执行动作**
- 克隆 CodeScaler/RewardUQ/SandboxFusion
- 记录完整 SHA 与 diff 状态
- 用 HF API 锁定模型和数据 revision

**验收标准**
- [ ] upstream.lock.yaml 无 main/RESOLVE 占位
- [ ] 所有 remote URL 与 SHA 可复现
- [ ] 生成锁文件哈希

**产物**
- `contracts/upstream.lock.yaml`
- `artifacts/provenance/upstream_manifest.json`

**回滚：** Revert task commit; preserve logs and failure report.

## T003 — 许可证与可分发边界审计

- 阶段：`G0-Governance`；Gate：`0`；负责人角色：`Reviewer`；估算：3h。
- 依赖：T002。
- GPU：否；人工批准：否。

**执行动作**
- 核验仓库、模型、数据及其来源子集许可证
- 明确复制源码、发布补丁、发布模型/数据的边界

**验收标准**
- [ ] 每个依赖有 license_status 与证据 URL
- [ ] CodeScaler 根仓许可证不明时只发布适配层/补丁
- [ ] 无未经授权的权重或测试数据进入 Git

**产物**
- `LICENSE_AUDIT.md`
- `THIRD_PARTY_NOTICES.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T004 — 建立隔离 Python/容器环境

- 阶段：`G0-Governance`；Gate：`0`；负责人角色：`Implementer`；估算：6h。
- 依赖：T001, T002。
- GPU：否；人工批准：否。

**执行动作**
- 建立 codescaler、rewarduq、orchestrator 三个环境
- 优先复现上游 pin，不盲目升级依赖
- 记录 pip/conda lock

**验收标准**
- [ ] import smoke 通过
- [ ] torch 能识别四卡
- [ ] 环境 lock 与镜像 digest 入库

**产物**
- `env/`
- `artifacts/provenance/environment.json`

**回滚：** Revert task commit; preserve logs and failure report.

## T005 — 实现合同、Schema 与任务图 CI 校验

- 阶段：`G0-Governance`；Gate：`0`；负责人角色：`Implementer`；估算：4h。
- 依赖：T000。
- GPU：否；人工批准：否。

**执行动作**
- 接入 scripts/validate_bundle.py
- 新增 CI 检查 YAML/JSON/任务依赖
- 检查冻结 contract hash

**验收标准**
- [ ] CI 对故意损坏的 schema/循环依赖会失败
- [ ] 正常执行包全通过

**产物**
- `.github/workflows/contracts.yml`
- `tests/test_contracts.py`

**回滚：** Revert task commit; preserve logs and failure report.

## T010 — 导入 DeepCoder 问题注册表

- 阶段：`G0-Data`；Gate：`0`；负责人角色：`DataSteward`；估算：6h。
- 依赖：T004, T005。
- GPU：否；人工批准：否。

**执行动作**
- 下载 pin revision
- 只提取问题元数据与测试引用
- 生成 problem_hash

**验收标准**
- [ ] 记录数与上游数据卡/脚本一致或解释差异
- [ ] 测试文本不写入 prompt 字段
- [ ] schema 验证通过

**产物**
- `artifacts/registries/problems.parquet`
- `reports/gate0/dataset_inventory.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T011 — 去重、重叠与泄漏审计

- 阶段：`G0-Data`；Gate：`0`；负责人角色：`DataSteward`；估算：6h。
- 依赖：T010。
- GPU：否；人工批准：否。

**执行动作**
- exact/normalized hash 去重
- 检查 source/time 重叠
- 输出 overlap matrix

**验收标准**
- [ ] 同一 hash 不跨 split
- [ ] 所有删除/合并有映射表
- [ ] 外部 benchmark 重叠被记录

**产物**
- `artifacts/registries/dedup_map.parquet`
- `reports/gate0/overlap_report.json`

**回滚：** Revert task commit; preserve logs and failure report.

## T012 — 冻结 risk/RL/final split

- 阶段：`G0-Data`；Gate：`0`；负责人角色：`DataSteward`；估算：4h。
- 依赖：T011。
- GPU：否；人工批准：否。

**执行动作**
- 按 problem_hash/source 分层切分
- 密封 final registry
- 计算 split manifest hash

**验收标准**
- [ ] row-level random split 被测试禁止
- [ ] final 文件只读且 hash 固定
- [ ] split balance 报告完成

**产物**
- `contracts/dataset_split.lock.yaml`
- `artifacts/registries/*.parquet`

**回滚：** Revert task commit; preserve logs and failure report.

## T013 — 实现统一 prompt renderer

- 阶段：`G0-Protocol`；Gate：`0`；负责人角色：`Implementer`；估算：6h。
- 依赖：T012。
- GPU：否；人工批准：否。

**执行动作**
- 复现上游 prompt
- 确保测试用例不进入 prompt
- 保存 rendered prompt 与 hash

**验收标准**
- [ ] 100 个样本与上游预期格式对齐
- [ ] prompt 中无 test 字段
- [ ] token 长度统计完整

**产物**
- `src/prompts/renderer.py`
- `tests/test_prompt_no_leakage.py`

**回滚：** Revert task commit; preserve logs and failure report.

## T014 — 实现 canonical code extractor

- 阶段：`G0-Protocol`；Gate：`0`；负责人角色：`Implementer`；估算：6h。
- 依赖：T013。
- GPU：否；人工批准：否。

**执行动作**
- 实现单代码块规则
- 定义错误枚举
- 保留 raw response 与 extracted code

**验收标准**
- [ ] 所有 golden cases 通过
- [ ] 无 train/eval 分支函数
- [ ] 确定性与幂等性通过

**产物**
- `src/extraction/canonical.py`
- `tests/test_extraction_golden.py`

**回滚：** Revert task commit; preserve logs and failure report.

## T015 — 审计并统一上游 train/eval 提取差异

- 阶段：`G0-Protocol`；Gate：`0`；负责人角色：`Reviewer`；估算：4h。
- 依赖：T014。
- GPU：否；人工批准：否。

**执行动作**
- 对上游两个 extractor 做差分测试
- 统计 1000 样本分歧
- 提交适配补丁

**验收标准**
- [ ] 分歧原因有分类
- [ ] 本项目所有路径只调用 canonical extractor
- [ ] 回归测试覆盖

**产物**
- `reports/gate0/extraction_parity.md`
- `patches/codescaler_extraction.patch`

**回滚：** Revert task commit; preserve logs and failure report.

## T016 — 实现 CodeScaler-1.7B scoring adapter

- 阶段：`G0-Protocol`；Gate：`0`；负责人角色：`Implementer`；估算：8h。
- 依赖：T004, T014。
- GPU：是；人工批准：是。

**执行动作**
- 封装 chat template、batching 与分数输出
- 保存 actual RM input/token/hash
- 实现 OOM backoff

**验收标准**
- [ ] 重复性、批序、单/批 parity 通过
- [ ] NaN/Inf 触发失败
- [ ] 每个分数可追溯到输入 hash

**产物**
- `src/scoring/codescaler_adapter.py`
- `tests/test_rm_scoring.py`

**回滚：** Revert task commit; preserve logs and failure report.

## T017 — RM 输入模式与截断审计

- 阶段：`G0-Protocol`；Gate：`0`；负责人角色：`ExperimentOperator`；估算：6h。
- 依赖：T016。
- GPU：是；人工批准：是。

**执行动作**
- 比较 upstream exact 与 question+code
- 检查 2K/3K/4K 生成上限
- 统计代码尾部可见率与 rank 变化

**验收标准**
- [ ] 冻结 input_mode/max_length/truncation_side
- [ ] silent truncation 为零或明确隔离
- [ ] cap-hit <5% 或说明上调

**产物**
- `contracts/rm_scoring.lock.yaml`
- `reports/gate0/rm_input_audit.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T018 — 部署并锁定隔离执行服务

- 阶段：`G0-Security`；Gate：`0`；负责人角色：`SecurityReviewer`；估算：8h。
- 依赖：T001, T002, T004。
- GPU：否；人工批准：否。

**执行动作**
- 从 pin 源码构建镜像
- 记录 Dockerfile/image digest
- 配置无网络、非 root、cgroups v2 与输出限制

**验收标准**
- [ ] 服务健康检查通过
- [ ] 容器无项目源码/密钥挂载
- [ ] 镜像 digest 固定

**产物**
- `infra/sandbox/`
- `artifacts/provenance/sandbox_image.json`

**回滚：** Revert task commit; preserve logs and failure report.

## T019 — 执行沙箱安全与故障语义验收

- 阶段：`G0-Security`；Gate：`0`；负责人角色：`SecurityReviewer`；估算：8h。
- 依赖：T018。
- GPU：否；人工批准：否。

**执行动作**
- 运行全部 adversarial fixtures
- 验证 timeout/OOM 后服务恢复
- 区分答案错误与 INFRA_ERROR

**验收标准**
- [ ] 无宿主文件/网络访问
- [ ] fork/memory/output bomb 被限制
- [ ] INFRA_ERROR 不映射 reward=0

**产物**
- `reports/gate0/sandbox_acceptance.md`
- `tests/security/`

**回滚：** Revert task commit; preserve logs and failure report.

## T020 — 实现 execution adapter、缓存与状态枚举

- 阶段：`G0-Protocol`；Gate：`0`；负责人角色：`Implementer`；估算：8h。
- 依赖：T014, T019。
- GPU：否；人工批准：否。

**执行动作**
- 实现请求/重试/缓存
- cache key 包含 code/test/image/limits
- 限制 stdout/stderr

**验收标准**
- [ ] 已知正确/错误样本结果确定
- [ ] infra error 不缓存
- [ ] timeout 清理整个进程树

**产物**
- `src/execution/adapter.py`
- `src/execution/cache.py`
- `tests/test_execution.py`

**回滚：** Revert task commit; preserve logs and failure report.

## T021 — 建立 evaluator parity 与 Oracle 强度审计

- 阶段：`G0-Protocol`；Gate：`0`；负责人角色：`Reviewer`；估算：6h。
- 依赖：T020。
- GPU：否；人工批准：否。

**执行动作**
- 比较本地 evaluator 与上游评测
- 定义 train/audit/final suite
- 对已知解和 mutation 样本做敏感性检查

**验收标准**
- [ ] parity 差异为零或有书面豁免
- [ ] 有限测试通过只称 test-suite success
- [ ] final evaluator 冻结

**产物**
- `contracts/evaluation.lock.yaml`
- `reports/gate0/evaluator_parity.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T022 — 全链路资源与成本审计

- 阶段：`G0-Cost`；Gate：`0`；负责人角色：`ExperimentOperator`；估算：8h。
- 依赖：T016, T020, T021。
- GPU：是；人工批准：是。

**执行动作**
- 对至少 1000 candidates 测 RM 与执行
- 记录 GPU-s/CPU-s/wall-clock/p50/p95
- 测并发与 timeout

**验收标准**
- [ ] 混合系统成本公式可计算
- [ ] 明确 cost claim 是否允许
- [ ] 同一硬件和并发配置

**产物**
- `reports/gate0/cost_audit.md`
- `artifacts/metrics/cost_raw.parquet`

**回滚：** Revert task commit; preserve logs and failure report.

## T023 — Gate 0 评审与合同冻结

- 阶段：`G0-Review`；Gate：`0`；负责人角色：`ExperimentReviewer`；估算：4h。
- 依赖：T003, T005, T012, T015, T017, T019, T021, T022。
- GPU：否；人工批准：是。

**执行动作**
- 汇总协议、成本、安全与差异
- 冻结 contracts hash
- 形成 go/no-go

**验收标准**
- [ ] 所有阻断问题关闭
- [ ] 存在明确主 claim（cost 或 reliability）
- [ ] 人工签署 gate review

**产物**
- `reports/gates/GATE0.md`
- `artifacts/provenance/contracts.sha256`

**回滚：** Revert task commit; preserve logs and failure report.

## T100 — 实现可恢复的 group generation runner

- 阶段：`G1-FailureAudit`；Gate：`1`；负责人角色：`Implementer`；估算：8h。
- 依赖：T023。
- GPU：否；人工批准：否。

**执行动作**
- 按 problem shard/seed 生成
- 原子写入与断点恢复
- schema 校验

**验收标准**
- [ ] 中断后无重复/缺失
- [ ] 固定 seed 可复现
- [ ] 每候选有完整 provenance

**产物**
- `src/generation/runner.py`
- `tests/test_generation_resume.py`

**回滚：** Revert task commit; preserve logs and failure report.

## T101 — 生成 100 prompts × 4 smoke corpus

- 阶段：`G1-FailureAudit`；Gate：`1`；负责人角色：`ExperimentOperator`；估算：4h。
- 依赖：T100。
- GPU：是；人工批准：是。

**执行动作**
- 执行生成并检查格式/长度
- 人工抽查 20 题

**验收标准**
- [ ] 无批量空输出
- [ ] cap-hit/invalid 可解释
- [ ] 无测试泄漏

**产物**
- `artifacts/corpus/smoke_candidates.parquet`

**回滚：** Revert task commit; preserve logs and failure report.

## T102 — 对 smoke corpus 全量 RM 打分与执行

- 阶段：`G1-FailureAudit`；Gate：`1`；负责人角色：`ExperimentOperator`；估算：4h。
- 依赖：T101。
- GPU：是；人工批准：是。

**执行动作**
- RM 批量评分
- 全量安全执行
- 联结 candidate/group records

**验收标准**
- [ ] 记录数一一对应
- [ ] 无静默 infra error
- [ ] top1 标签可构造

**产物**
- `artifacts/corpus/smoke_labeled.parquet`

**回滚：** Revert task commit; preserve logs and failure report.

## T103 — 危险错误 prevalence 与伪影审计

- 阶段：`G1-FailureAudit`；Gate：`1`；负责人角色：`ExperimentReviewer`；估算：6h。
- 依赖：T102。
- GPU：否；人工批准：否。

**执行动作**
- 统计 optimization/selection FP
- 按截断/extractor/source 切片
- 人工复核至少 50 个 FP

**验收标准**
- [ ] FP 不是主要由协议 bug 造成
- [ ] 报告置信区间
- [ ] 决定是否扩大数据

**产物**
- `reports/gate1/prevalence_audit.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T104 — 生成并执行 500 prompts × 4 pilot corpus

- 阶段：`G1-FailureAudit`；Gate：`1`；负责人角色：`ExperimentOperator`；估算：12h。
- 依赖：T103。
- GPU：是；人工批准：是。

**执行动作**
- 按 frozen contract 扩大生成
- 全部执行并缓存
- 构建 group labels

**验收标准**
- [ ] 至少 2000 candidates
- [ ] 数据完整率 >99.5%
- [ ] 失败可重跑

**产物**
- `artifacts/corpus/pilot_labeled.parquet`

**回滚：** Revert task commit; preserve logs and failure report.

## T105 — 条件扩展至 1500–2500 prompts

- 阶段：`G1-FailureAudit`；Gate：`1`；负责人角色：`ExperimentOperator`；估算：24h。
- 依赖：T104。
- GPU：是；人工批准：是。

**执行动作**
- 仅当危险 FP 数不足时扩展
- 按来源和难度补样
- 避免 dev/final

**验收标准**
- [ ] 危险 FP group >=200 或正式 no-go
- [ ] 总候选 6K–10K
- [ ] problem split 无泄漏

**产物**
- `artifacts/corpus/risk_full_labeled.parquet`

**回滚：** Revert task commit; preserve logs and failure report.

## T106 — 建立 candidate/group label builder

- 阶段：`G1-FailureAudit`；Gate：`1`；负责人角色：`Implementer`；估算：6h。
- 依赖：T102。
- GPU：否；人工批准：否。

**执行动作**
- 实现三种 label
- 处理 infra error 与 ties
- 验证 top1 规则

**验收标准**
- [ ] synthetic golden groups 通过
- [ ] softplus 单调不改 top1
- [ ] infra group 不产标签

**产物**
- `src/labels/builder.py`
- `tests/test_labels.py`

**回滚：** Revert task commit; preserve logs and failure report.

## T107 — 构建失败类型 taxonomy 与标注抽样

- 阶段：`G1-FailureAudit`；Gate：`1`；负责人角色：`DataSteward`；估算：8h。
- 依赖：T104, T106。
- GPU：否；人工批准：否。

**执行动作**
- 定义 compile/runtime/logic/timeout/format/RM-shortcut 类别
- 双人或 Agent+人工复核样本

**验收标准**
- [ ] taxonomy 互斥/可多标签规则明确
- [ ] 抽样记录可追溯
- [ ] 表面特征偏置单独报告

**产物**
- `reports/gate1/failure_taxonomy.md`
- `artifacts/annotations/fp_review.parquet`

**回滚：** Revert task commit; preserve logs and failure report.

## T108 — Gate 1 评审：问题是否真实且规模足够

- 阶段：`G1-FailureAudit`；Gate：`1`；负责人角色：`ExperimentReviewer`；估算：4h。
- 依赖：T103, T105, T107。
- GPU：否；人工批准：是。

**执行动作**
- 检查危险 FP 率/数量/来源
- 检查成本主张
- 选择继续或 pivot

**验收标准**
- [ ] 危险 FP >=约5%且至少200组，或存在更强可解释分布
- [ ] 伪影已排除
- [ ] 人工签署

**产物**
- `reports/gates/GATE1.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T200 — 实现无泄漏特征流水线

- 阶段：`G2-RiskModel`；Gate：`2`；负责人角色：`Implementer`；估算：10h。
- 依赖：T108。
- GPU：否；人工批准：否。

**执行动作**
- 实现 score/validity/length/truncation/diversity 特征
- 缓存特征版本
- 禁止 oracle 字段

**验收标准**
- [ ] feature schema 固定
- [ ] 单元测试证明无 execution 字段
- [ ] 同输入确定

**产物**
- `src/risk/features.py`
- `tests/test_feature_no_leakage.py`

**回滚：** Revert task commit; preserve logs and failure report.

## T201 — 验证 problem-level risk split

- 阶段：`G2-RiskModel`；Gate：`2`；负责人角色：`DataSteward`；估算：4h。
- 依赖：T200。
- GPU：否；人工批准：否。

**执行动作**
- 生成 train/calibration/dev
- 检查 source/difficulty balance
- 检测 hash 重叠

**验收标准**
- [ ] 跨 split problem overlap=0
- [ ] candidate/pair 不跨 split
- [ ] split manifest 冻结

**产物**
- `artifacts/registries/risk_split.parquet`

**回滚：** Revert task commit; preserve logs and failure report.

## T202 — margin/dispersion/static-analysis 基线

- 阶段：`G2-RiskModel`；Gate：`2`；负责人角色：`Implementer`；估算：6h。
- 依赖：T201。
- GPU：否；人工批准：否。

**执行动作**
- 实现无训练基线
- 固定预算评估
- 生成曲线

**验收标准**
- [ ] 每个 baseline 可复现
- [ ] 预算严格匹配
- [ ] 指标定义一致

**产物**
- `artifacts/models/baselines/`
- `reports/gate2/simple_baselines.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T203 — 训练 Logistic 与 GBDT 风险模型

- 阶段：`G2-RiskModel`；Gate：`2`；负责人角色：`Implementer`；估算：8h。
- 依赖：T201。
- GPU：否；人工批准：否。

**执行动作**
- 分别预测 opt/selection/mixed
- 仅用 risk_train
- 保存模型与特征列表

**验收标准**
- [ ] 不访问 calibration/dev 标签调参
- [ ] PR-AUC 与 recall@budget 完整
- [ ] 模型可加载复现

**产物**
- `artifacts/models/risk_simple/`

**回滚：** Revert task commit; preserve logs and failure report.

## T204 — 提取冻结 RM embedding 并训练 MLP

- 阶段：`G2-RiskModel`；Gate：`2`；负责人角色：`Implementer`；估算：10h。
- 依赖：T201。
- GPU：是；人工批准：是。

**执行动作**
- 定义 pooling
- 批量提取并 hash
- 训练小型 MLP

**验收标准**
- [ ] embedding 不含 test
- [ ] 存储规模受控
- [ ] 与简单模型公平比较

**产物**
- `artifacts/features/rm_embeddings/`
- `artifacts/models/risk_mlp/`

**回滚：** Revert task commit; preserve logs and failure report.

## T205 — 接入 RewardUQ 多头方差 baseline

- 阶段：`G2-RiskModel`；Gate：`2`；负责人角色：`Implementer`；估算：12h。
- 依赖：T201。
- GPU：是；人工批准：是。

**执行动作**
- 优先共享冻结 backbone 多头
- 将 variance 作为 baseline/feature
- 不改主 RM

**验收标准**
- [ ] 额外推理开销被测量
- [ ] raw variance 不被称为概率
- [ ] 可完全关闭

**产物**
- `src/risk/rewarduq_adapter.py`
- `artifacts/models/rewarduq/`

**回滚：** Revert task commit; preserve logs and failure report.

## T206 — 校准风险概率

- 阶段：`G2-RiskModel`；Gate：`2`；负责人角色：`Implementer`；估算：6h。
- 依赖：T203, T204, T205。
- GPU：否；人工批准：否。

**执行动作**
- 在 calibration split 做 Platt/isotonic
- 比较 Brier/ECE
- 冻结校准器

**验收标准**
- [ ] dev 未用于拟合校准器
- [ ] 可靠性图输出
- [ ] 概率范围与 NaN 测试通过

**产物**
- `artifacts/models/calibrators/`
- `reports/gate2/calibration.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T207 — Risk–coverage 与 recall@budget 评估

- 阶段：`G2-RiskModel`；Gate：`2`；负责人角色：`ExperimentReviewer`；估算：8h。
- 依赖：T202, T206。
- GPU：否；人工批准：否。

**执行动作**
- 在 dev 上计算 PR-AUC/AURC/eAURC
- 预算 10/25/50%
- problem bootstrap

**验收标准**
- [ ] 优于 random
- [ ] 与 margin/GBDT/RewardUQ 比较
- [ ] 95% CI 输出

**产物**
- `reports/gate2/risk_coverage.md`
- `artifacts/metrics/risk_dev.parquet`

**回滚：** Revert task commit; preserve logs and failure report.

## T208 — 反 shortcut 与 shift 切片

- 阶段：`G2-RiskModel`；Gate：`2`；负责人角色：`ExperimentReviewer`；估算：8h。
- 依赖：T207。
- GPU：否；人工批准：否。

**执行动作**
- 长度匹配
- 移除长度特征
- source-held-out
- truncation/checkpoint slice

**验收标准**
- [ ] 收益不只来自长度
- [ ] 至少两个 shift slice 方向一致
- [ ] 失败切片被记录

**产物**
- `reports/gate2/shift_and_ablation.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T209 — 选择双头 router 版本

- 阶段：`G2-RiskModel`；Gate：`2`；负责人角色：`ExperimentReviewer`；估算：4h。
- 依赖：T207, T208。
- GPU：否；人工批准：否。

**执行动作**
- 比较 opt/selection/mixed heads
- 选择 corrective 与 audit score
- 冻结 router revision

**验收标准**
- [ ] 选择规则预注册
- [ ] 模型复杂度有必要性
- [ ] router model card 完成

**产物**
- `artifacts/models/router_final/`
- `reports/gate2/router_model_card.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T210 — Gate 2 评审：离线路由是否有效

- 阶段：`G2-RiskModel`；Gate：`2`；负责人角色：`ExperimentReviewer`；估算：4h。
- 依赖：T209。
- GPU：否；人工批准：是。

**执行动作**
- 检查相对随机危险错误捕获
- 检查 margin/RewardUQ 差异
- 决定继续或 pivot

**验收标准**
- [ ] 同预算相对 random 捕获提升约20%或更强证据
- [ ] 显著优于 margin 或给出可解释价值
- [ ] 人工签署

**产物**
- `reports/gates/GATE2.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T300 — 实现固定 candidate-execution 预算控制器

- 阶段：`G3-SelectiveVerification`；Gate：`3`；负责人角色：`Implementer`；估算：6h。
- 依赖：T210。
- GPU：否；人工批准：否。

**执行动作**
- 预算按候选执行数而非 group 数
- 支持 10/25/50/100%
- 稳定 tie break

**验收标准**
- [ ] 绝不超预算
- [ ] group size 变化时报错
- [ ] 预算利用率可审计

**产物**
- `src/routing/budget_controller.py`
- `tests/test_budget.py`

**回滚：** Revert task commit; preserve logs and failure report.

## T301 — 实现分层随机审计与 propensity 记录

- 阶段：`G3-SelectiveVerification`；Gate：`3`；负责人角色：`Implementer`；估算：6h。
- 依赖：T300。
- GPU：否；人工批准：否。

**执行动作**
- risk decile/source/length/checkpoint 分层
- 最小审计率
- 记录 route probability

**验收标准**
- [ ] 每层有审计样本
- [ ] propensity>0
- [ ] 固定 seed 可复现

**产物**
- `src/routing/audit_sampler.py`
- `tests/test_propensity.py`

**回滚：** Revert task commit; preserve logs and failure report.

## T302 — 实现离线路由模拟器

- 阶段：`G3-SelectiveVerification`；Gate：`3`；负责人角色：`Implementer`；估算：8h。
- 依赖：T300, T301。
- GPU：否；人工批准：否。

**执行动作**
- 模拟 random/margin/UQ/router
- 选择已执行结果作为 oracle
- 计算 IPW 与未加权指标

**验收标准**
- [ ] 相同预算严格一致
- [ ] 全执行与 oracle 对齐
- [ ] 缓存不影响结果

**产物**
- `src/routing/simulator.py`
- `tests/test_routing_simulator.py`

**回滚：** Revert task commit; preserve logs and failure report.

## T303 — 固定预算 Best-of-N 评测

- 阶段：`G3-SelectiveVerification`；Gate：`3`；负责人角色：`ExperimentReviewer`；估算：8h。
- 依赖：T302。
- GPU：否；人工批准：否。

**执行动作**
- BoN@4/8
- selection regret
- 多预算 Pareto

**验收标准**
- [ ] 比 CodeScaler-only 与 random 报告配对 CI
- [ ] 不使用 final test
- [ ] 所有候选生成预算匹配

**产物**
- `reports/gate3/bon_results.md`
- `artifacts/metrics/bon_dev.parquet`

**回滚：** Revert task commit; preserve logs and failure report.

## T304 — 验证总体资源成本与并行流水

- 阶段：`G3-SelectiveVerification`；Gate：`3`；负责人角色：`ExperimentOperator`；估算：6h。
- 依赖：T303。
- GPU：是；人工批准：是。

**执行动作**
- 计入 RM+router+execution 全成本
- 测 CPU/GPU overlap
- 按预算画成本曲线

**验收标准**
- [ ] 不沿用上游10x数字
- [ ] 明确是否允许 cost claim
- [ ] 执行次数与 wall-clock 分开

**产物**
- `reports/gate3/system_cost.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T305 — Gate 3 评审：是否值得进入 RL

- 阶段：`G3-SelectiveVerification`；Gate：`3`；负责人角色：`ExperimentReviewer`；估算：4h。
- 依赖：T303, T304。
- GPU：否；人工批准：是。

**执行动作**
- 检查 BoN 与成本
- 检查 router 稳定性
- 冻结 RL 方法

**验收标准**
- [ ] 满足 +1~2pp 或非劣0.5pp下执行减少约30%等预注册条件之一
- [ ] 人工批准 GPU RL

**产物**
- `reports/gates/GATE3.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T400 — 冻结在线 RL baseline 与预算合同

- 阶段：`G4-RLIntegration`；Gate：`4`；负责人角色：`Planner`；估算：4h。
- 依赖：T305。
- GPU：否；人工批准：否。

**执行动作**
- 确定 P1/P2/P4/P5/P6
- 冻结 token/rollout/execution budget
- 选择 LoRA/full 与 KL

**验收标准**
- [ ] 所有 arm 仅方法变量不同
- [ ] 动态 group filtering 默认关闭
- [ ] 合同 hash 更新

**产物**
- `contracts/rl_experiment.lock.yaml`

**回滚：** Revert task commit; preserve logs and failure report.

## T401 — 定位 veRL reward/advantage/group-filter hook

- 阶段：`G4-RLIntegration`；Gate：`4`；负责人角色：`Implementer`；估算：6h。
- 依赖：T400。
- GPU：否；人工批准：否。

**执行动作**
- 追踪 DataProto 字段
- 绘制 reward 到 advantage 数据流
- 识别 resampling/filter 位置

**验收标准**
- [ ] 有调用图与字段表
- [ ] router 在正确阶段执行
- [ ] 无测试数据进入 actor

**产物**
- `reports/gate4/verl_dataflow.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T402 — 实现 group-level hybrid reward manager

- 阶段：`G4-RLIntegration`；Gate：`4`；负责人角色：`Implementer`；估算：12h。
- 依赖：T401。
- GPU：否；人工批准：否。

**执行动作**
- 整组路由
- 执行组 binary，非执行组 RM
- 记录 route/reward provenance

**验收标准**
- [ ] 同组不混 reward 类型
- [ ] router disabled 精确退化上游
- [ ] infra error 不更新

**产物**
- `src/training/hybrid_reward.py`
- `tests/test_hybrid_reward.py`

**回滚：** Revert task commit; preserve logs and failure report.

## T403 — 实现 synthetic golden advantage tests

- 阶段：`G4-RLIntegration`；Gate：`4`；负责人角色：`Implementer`；估算：8h。
- 依赖：T402。
- GPU：否；人工批准：否。

**执行动作**
- 构造 mixed/all-pass/all-fail/RM groups
- 验证归一化/skip
- 检查 no-op

**验收标准**
- [ ] 预期 advantage 精确匹配
- [ ] 零方差被识别
- [ ] 路由改动产生非恒定变化

**产物**
- `tests/test_advantage_golden.py`

**回滚：** Revert task commit; preserve logs and failure report.

## T404 — 实现 effective-gradient 与 resampling 账本

- 阶段：`G4-RLIntegration`；Gate：`4`；负责人角色：`Implementer`；估算：6h。
- 依赖：T402。
- GPU：否；人工批准：否。

**执行动作**
- 记录生成组/更新组/零方差
- 统计 resample count
- 匹配总生成预算

**验收标准**
- [ ] 每一步可算 effective ratio
- [ ] 无隐式丢组
- [ ] baseline exposure 可核对

**产物**
- `src/training/exposure_ledger.py`

**回滚：** Revert task commit; preserve logs and failure report.

## T405 — 实现 checkpoint 级 random audit/drift trace

- 阶段：`G4-RLIntegration`；Gate：`4`；负责人角色：`Implementer`；估算：8h。
- 依赖：T402。
- GPU：否；人工批准：否。

**执行动作**
- 保存 router score/route/propensity
- checkpoint 分层 audit
- 生成校准输入

**验收标准**
- [ ] 低风险区持续有标签
- [ ] 日志无测试内容
- [ ] router revision 可追踪

**产物**
- `src/training/audit_trace.py`

**回滚：** Revert task commit; preserve logs and failure report.

## T406 — 5-step 单卡/小批功能 smoke

- 阶段：`G4-RLIntegration`；Gate：`4`；负责人角色：`ExperimentOperator`；估算：6h。
- 依赖：T403, T404, T405。
- GPU：是；人工批准：是。

**执行动作**
- 最小数据训练
- 检查 loss/reward/advantage
- 故障注入

**验收标准**
- [ ] 无 NaN/OOM/死锁
- [ ] 所有 trace 对齐
- [ ] 故障能安全退出

**产物**
- `reports/gate4/smoke5.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T407 — 20–30 step 四卡 RL smoke

- 阶段：`G4-RLIntegration`；Gate：`4`；负责人角色：`ExperimentOperator`；估算：12h。
- 依赖：T406。
- GPU：是；人工批准：是。

**执行动作**
- 按资源 profile 训练
- 监控温度/显存/吞吐
- 验证 router 不退化

**验收标准**
- [ ] 完成 checkpoint/eval
- [ ] execute-all/none 未非预期发生
- [ ] route 与 reward 证据完整

**产物**
- `reports/gate4/smoke30.md`
- `artifacts/runs/`

**回滚：** Revert task commit; preserve logs and failure report.

## T408 — Gate 4 评审：实现是否可信

- 阶段：`G4-RLIntegration`；Gate：`4`；负责人角色：`ExperimentReviewer`；估算：4h。
- 依赖：T407。
- GPU：否；人工批准：是。

**执行动作**
- 代码/实验双 review
- 核对 advantage 与预算
- 冻结 pilot config

**验收标准**
- [ ] 所有 golden tests 通过
- [ ] 协议无漂移
- [ ] 人工批准两 seed pilot

**产物**
- `reports/gates/GATE4.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T500 — 运行 P1 full-execution pilot

- 阶段：`G5-Pilot`；Gate：`5`；负责人角色：`ExperimentOperator`；估算：16h。
- 依赖：T408。
- GPU：是；人工批准：是。

**执行动作**
- 固定 seed1/2
- 执行全部 group
- 保存 exposure/cost

**验收标准**
- [ ] 两个 seed 完成
- [ ] budget/step/问题曝光记录完整
- [ ] 无 final test

**产物**
- `artifacts/runs/P1_pilot/`

**回滚：** Revert task commit; preserve logs and failure report.

## T501 — 运行 P2 CodeScaler-only pilot

- 阶段：`G5-Pilot`；Gate：`5`；负责人角色：`ExperimentOperator`；估算：16h。
- 依赖：T408。
- GPU：是；人工批准：是。

**执行动作**
- 固定相同 seed1/2
- 无执行 reward
- 仍做离线 audit 但不影响 reward

**验收标准**
- [ ] 匹配生成/token预算
- [ ] RM 输入合同一致
- [ ] checkpoint 可评测

**产物**
- `artifacts/runs/P2_pilot/`

**回滚：** Revert task commit; preserve logs and failure report.

## T502 — 运行 P4 random-hybrid pilot

- 阶段：`G5-Pilot`；Gate：`5`；负责人角色：`ExperimentOperator`；估算：16h。
- 依赖：T408。
- GPU：是；人工批准：是。

**执行动作**
- 匹配 P6 执行预算
- 随机整组执行
- 记录 propensity

**验收标准**
- [ ] 执行数与 P6 容差内一致
- [ ] 随机种子独立
- [ ] 无风险特征使用

**产物**
- `artifacts/runs/P4_pilot/`

**回滚：** Revert task commit; preserve logs and failure report.

## T503 — 运行 P5 static-router pilot

- 阶段：`G5-Pilot`；Gate：`5`；负责人角色：`ExperimentOperator`；估算：16h。
- 依赖：T408。
- GPU：是；人工批准：是。

**执行动作**
- 冻结 Gate2 router
- 不重校准
- 执行预算匹配

**验收标准**
- [ ] router revision 固定
- [ ] audit 保留
- [ ] 数据完整

**产物**
- `artifacts/runs/P5_pilot/`

**回滚：** Revert task commit; preserve logs and failure report.

## T504 — 运行 P6 drift-aware pilot

- 阶段：`G5-Pilot`；Gate：`5`；负责人角色：`ExperimentOperator`；估算：20h。
- 依赖：T408。
- GPU：是；人工批准：是。

**执行动作**
- 训练窗口间校准
- 分层随机 audit
- propensity correction

**验收标准**
- [ ] 无同步不稳定更新
- [ ] 校准数据仅来自允许标签
- [ ] 预算匹配

**产物**
- `artifacts/runs/P6_pilot/`

**回滚：** Revert task commit; preserve logs and failure report.

## T505 — 两 seed pilot 统一评测与漂移分析

- 阶段：`G5-Pilot`；Gate：`5`；负责人角色：`ExperimentReviewer`；估算：12h。
- 依赖：T500, T501, T502, T503, T504。
- GPU：否；人工批准：否。

**执行动作**
- 固定 checkpoint 规则
- 能力/风险/成本评测
- checkpoint calibration/drift

**验收标准**
- [ ] P6 相对 P2/P4 方向一致或停止
- [ ] 无长度/格式作弊
- [ ] 报告 seed 个体结果

**产物**
- `reports/gate5/pilot_results.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T506 — Gate 5 评审：是否进入三 seed正式实验

- 阶段：`G5-Pilot`；Gate：`5`；负责人角色：`ExperimentReviewer`；估算：4h。
- 依赖：T505。
- GPU：否；人工批准：是。

**执行动作**
- 评估主指标与失败模式
- 删减最终 arm
- 冻结 final protocol

**验收标准**
- [ ] P6 能力不明显退化且危险 FP/最终通过率至少一项改善
- [ ] 人工签署

**产物**
- `reports/gates/GATE5.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T600 — 冻结最终配置、预注册与 sealed test

- 阶段：`G6-Final`；Gate：`6`；负责人角色：`Planner`；估算：4h。
- 依赖：T506。
- GPU：否；人工批准：否。

**执行动作**
- 冻结所有 config/阈值/checkpoint rule
- 计算 hash
- 设 final access policy

**验收标准**
- [ ] 任何后续变更触发新版本
- [ ] final test 未打开
- [ ] 预注册签署

**产物**
- `contracts/final_experiment.lock.yaml`
- `reports/preregistration.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T601 — 运行三 seed 核心四 arm

- 阶段：`G6-Final`；Gate：`6`；负责人角色：`ExperimentOperator`；估算：60h。
- 依赖：T600。
- GPU：是；人工批准：是。

**执行动作**
- P1/P2/P4/P6 三个独立训练 seed
- 自动恢复与健康监控
- 严格资源账本

**验收标准**
- [ ] 12 个计划 run 完成或透明报告失败
- [ ] 无 seed 替换
- [ ] 相同预算

**产物**
- `artifacts/runs/final/`

**回滚：** Revert task commit; preserve logs and failure report.

## T602 — 开发集 checkpoint 选择并冻结

- 阶段：`G6-Final`；Gate：`6`；负责人角色：`ExperimentReviewer`；估算：8h。
- 依赖：T601。
- GPU：否；人工批准：否。

**执行动作**
- 按预注册规则选 checkpoint
- 记录所有候选
- 禁止 final 信息

**验收标准**
- [ ] 选择可程序化复现
- [ ] 没有挑峰值例外
- [ ] manifest 更新

**产物**
- `artifacts/selections/checkpoints.json`

**回滚：** Revert task commit; preserve logs and failure report.

## T603 — 一次性 final 与外部评测

- 阶段：`G6-Final`；Gate：`6`；负责人角色：`ExperimentOperator`；估算：16h。
- 依赖：T602。
- GPU：是；人工批准：是。

**执行动作**
- 解封 final
- 每模型固定采样协议
- 外部 benchmark 仅一次

**验收标准**
- [ ] final 只跑一次
- [ ] 原始输出只读归档
- [ ] 无重调

**产物**
- `artifacts/eval/final/`

**回滚：** Revert task commit; preserve logs and failure report.

## T604 — 统计、成本与 failure analysis

- 阶段：`G6-Final`；Gate：`6`；负责人角色：`ExperimentReviewer`；估算：16h。
- 依赖：T603。
- GPU：否；人工批准：否。

**执行动作**
- problem bootstrap
- 3 seed mean/std
- risk/cost Pareto
- 失败 taxonomy

**验收标准**
- [ ] 95% CI
- [ ] 绝对pp与相对值分开
- [ ] 不把 test pass称语义证明

**产物**
- `reports/final/results.md`
- `reports/final/statistics.json`

**回滚：** Revert task commit; preserve logs and failure report.

## T605 — Claim 审核、证据索引与复现包

- 阶段：`G6-Final`；Gate：`6`；负责人角色：`Reviewer`；估算：10h。
- 依赖：T604。
- GPU：否；人工批准：是。

**执行动作**
- 逐条更新 claims status
- 链接 run manifest
- 生成 artifact hashes

**验收标准**
- [ ] 无无证据 claim
- [ ] 所有图表可由脚本重建
- [ ] 敏感/大文件排除 Git

**产物**
- `reports/final/CLAIMS.md`
- `EVIDENCE_INDEX.csv`
- `REPRODUCIBILITY.md`

**回滚：** Revert task commit; preserve logs and failure report.

## T606 — 简历、技术报告、开源与论文草案

- 阶段：`G6-Final`；Gate：`6`；负责人角色：`Planner`；估算：12h。
- 依赖：T605。
- GPU：否；人工批准：否。

**执行动作**
- 写事实边界简历条目
- 技术报告
- 开源说明/论文 outline

**验收标准**
- [ ] 数字来自 final 表
- [ ] 负结果和限制保留
- [ ] 许可证边界满足

**产物**
- `docs/final_report.md`
- `docs/resume_project.md`
- `docs/paper_outline.md`

**回滚：** Revert task commit; preserve logs and failure report.
