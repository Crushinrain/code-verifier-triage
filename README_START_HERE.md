# CodeVerifier-Triage Agent Starter Pack

版本：v1.0  
日期：2026-07-11  
状态：PLANNED；尚无本项目实验结果。

## 从这里开始

本包将项目拆成六类材料：

1. `docx/`：三份已排版、已完成渲染检查的主文档；
2. `docs/`：总体研究设计、Agent 执行手册、实验、安全和求职/论文材料；
3. `contracts/`：14 份版本化、机器可读合同；
4. `schemas/`：6 份核心数据对象 Schema；
5. `tasks/` 与 `checklists/`：69 项依赖任务和 Gate 验收；
6. `prompts/`、`templates/`、`planning/`：Agent 角色、运行证据、审批和恢复模板。

## 最初执行顺序

1. 阅读 `docs/00_阅读导航.md`；
2. 阅读 `docs/06_Agent运行环境与工具能力清单.md`，并将 `prompts/FIRST_SESSION_PROMPT.md` 粘贴给首个 Agent；
3. 填写 `approvals/HUMAN_APPROVALS.yaml`；
4. 安装 `requirements-agent.txt`，执行能力检查、bundle validator 与 manifest 校验；
5. 领取 T000，严格按 `tasks/task_graph.yaml` 的依赖推进；
6. 完成上游 SHA、模型/数据 revision、容器 digest 和许可证审计；
7. 完成 canonical extractor、RM adapter、sandbox security suite 和成本审计；
8. Reviewer 审批 Gate 0 后，才允许扩大候选生成；
9. Gate 1–3 通过后，才允许修改 veRL 或启动 policy RL。

## 人工审批边界

高成本训练、final evaluation、删除大文件、改变 frozen contract、发布结果均要求 `approvals/HUMAN_APPROVALS.yaml` 中对应项为 `APPROVED`。Agent 不得自我批准 Gate。

## 事实边界

- 文档中的门槛是预注册目标，不是已实现结果；
- 上游结果必须标明来源和版本；
- 所有本项目 Claim 从 `PROPOSED` 开始；
- 只有 final protocol 下的证据才能升级为 `SUPPORTED_FINAL`。
