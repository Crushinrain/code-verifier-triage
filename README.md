# CodeVerifier-Triage 执行包

本执行包用于实现“面向策略漂移的风险校准选择性验证代码强化学习”。它不是一键训练脚本，而是一套把研究问题、实验合同、Agent 任务、验收门槛和复现证据绑定起来的工程基线。

## 先读

1. `docs/00_阅读导航.md`
2. `docs/06_Agent运行环境与工具能力清单.md`
3. `docs/01_总体方案与研究设计.md`
4. `docs/02_Agent执行手册.md`
5. `contracts/project.yaml`
6. `tasks/task_graph.yaml`
7. `checklists/gate0.md`

## 验证执行包

```bash
python -m pip install -r requirements-agent.txt
python scripts/validate_bundle.py
python scripts/check_agent_capabilities.py --output capability_report.json
make contracts-hash
```

## 创建一次运行

```bash
python scripts/new_run.py --stage G0 --method rm_cost_audit --seed 1
```

## 规则

- 一个 Task ID 一个 commit/PR；
- Agent 不能自行批准 Gate 或启动 GPU 训练；
- final test 在 Gate 6 前密封；
- frozen contract 只能通过 change request 修改；
- 未受信任代码只能进入通过安全验收的执行服务；
- 所有 Claim 必须有 evidence index、run manifest 和统计产物。

## 内容

- `docx/`：三份已排版的对外主文档；
- `docs/`：设计、执行、实验、安全、求职/论文的可版本控制 Markdown；
- `contracts/`：14 份机器可读合同；
- `schemas/`：6 份 JSON Schema；
- `tasks/`：69 项任务、Gate 与周计划；
- `prompts/`：Agent 角色提示词与可直接粘贴的首次会话提示；
- `templates/`：运行、评审、失败、Claim、风险模板；
- `scripts/`：校验、hash、run 初始化工具。

## 当前允许的第一批任务

只执行 T000–T005。第一周不授权 policy RL。
