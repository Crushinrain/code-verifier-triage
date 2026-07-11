# Agent 运行环境与工具能力清单

版本：v1.0  
状态：执行前检查，不替代人工审批。

## 1. 必需能力

| 阶段 | Agent/运行环境必须具备 | 缺失时处理 |
|---|---|---|
| 规划与 Gate 0 | 读写项目目录、Git、Python 3.10+、可运行测试、可保存命令输出 | 只允许阅读与生成计划，不得声称已完成任务 |
| 上游锁定 | 访问 Git 仓库与 Hugging Face 元数据；能够记录完整 commit/revision | 无网络时不得用 `main`、`latest` 或记忆中的版本代替 |
| 沙箱验收 | Docker 或等价隔离执行服务、cgroups/资源限制、无网络运行能力 | 禁止在宿主机执行任何候选代码；Gate 0 BLOCK |
| 候选生成与 RM | 4 张 GPU 可见、足够磁盘、可记录 GPU 拓扑和驱动/CUDA | 先做 CPU/协议任务；不得伪造 GPU smoke 结果 |
| 在线 RL | 可控制 GPU 独占、日志、checkpoint、自动停止和恢复 | 未满足时只允许离线 risk/BoN 版本 |
| Final/发布 | Human Owner、密封 final split、许可证审计、复现包和 Claim review | 任一缺失则不允许发布效果数字 |

## 2. 建议的 Agent 形态

- **Architect/Planner Agent**：只读全局状态，拆 Task、维护依赖与变更请求；不直接改实验结果。
- **Implementer Agent**：一次只领取一个 Task ID，只能写入任务票据允许的路径。
- **Experiment Agent**：只能运行已批准 manifest；不得临时改 seed、数据、阈值或 checkpoint 选择规则。
- **Reviewer Agent**：独立读取 diff、测试和 artifact；不得把 Implementer 的总结当作唯一证据。
- **Human Owner**：审批 Gate、高成本运行、final、删除和外部发布。

同一个 Agent 可顺序扮演多个角色，但每次切换必须开启新上下文并重新读取事实源；Reviewer 不得依赖上一角色的未验证记忆。

## 3. 首次能力检查

在解压后的根目录运行：

```bash
python scripts/check_agent_capabilities.py --output capability_report.json
python scripts/validate_bundle.py
sha256sum -c MANIFEST.sha256
```

能力报告只说明“工具可见”，不说明环境已经安全、版本已经兼容或实验已复现。

## 4. 明确禁止的替代行为

- 没有 Docker/沙箱时，用本地 `subprocess` 执行模型代码；
- 没有网络时，把未解析的模型 revision 写成 `main` 或 `latest`；
- 没有 GPU 时，用伪日志或历史日志填充 smoke 结果；
- 缺少 final 访问权限时，用 development 结果替代 final；
- 缺少 Human Owner 审批时，由 Agent 自行把 `PENDING` 改为 `APPROVED`；
- 工具调用失败时静默跳过样本、修改分母或重采样直到成功。

## 5. 上下文管理

长任务应按 Task ID 切分会话。每次新会话只注入：

1. `prompts/AGENT_SYSTEM.md`；
2. 当前 task ticket；
3. 依赖任务的 handoff；
4. 相关 contracts 的 hash；
5. 必要源文件，不注入整个历史聊天；
6. 当前 Gate review 与 Human approval 状态。

这样可以减少 Agent 因上下文过长而忽略约束、混淆旧版本或修改无关模块的概率。
