# 首次会话可直接粘贴给 Coding/Research Agent 的提示词

你正在初始化 `CodeVerifier-Triage`，目标是按证据和 Gate 推进，而不是立即训练。

请严格执行以下顺序：

1. 读取 `README_START_HERE.md`、`prompts/AGENT_SYSTEM.md`、`docs/00_阅读导航.md`、`docs/06_Agent运行环境与工具能力清单.md`、`approvals/HUMAN_APPROVALS.yaml`、`contracts/project.yaml`、`contracts/upstream.lock.yaml` 和 `tasks/task_graph.yaml`。
2. 以只读方式运行：
   - `python scripts/check_agent_capabilities.py --output capability_report.json`
   - `python scripts/validate_bundle.py`
   - `sha256sum -c MANIFEST.sha256`
3. 不要下载模型/数据，不要克隆上游，不要运行候选代码，不要启动 GPU，不要改任何 approval、frozen contract 或 final 文件。
4. 只领取 `T000`。根据 `templates/task_ticket.md` 生成完整 task ticket，列出：单一目标、非目标、依赖、允许/禁止路径、预期命令、验收、停止条件、回滚和需要的人类确认。
5. 检查 T000 的实现是否会覆盖现有文件；任何覆盖、删除、网络访问或权限变更都先列为待审批动作。
6. 输出以下五节后停止，等待 Human Owner 决定是否执行：
   - 已核验事实；
   - 能力与阻塞项；
   - T000 task ticket；
   - 精确变更计划和命令；
   - 风险、回滚与审批点。

禁止把计划写成已完成事实；禁止自动进入 T001；禁止自行批准任何 Gate。
