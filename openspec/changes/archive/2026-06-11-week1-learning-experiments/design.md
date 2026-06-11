## Context

本项目是个人 Agent 学习仓库，已有 `docs/learning-plan.md` 规划四周学习路径，但缺少可运行代码。学习者背景为 Node.js 后端开发者，第 1 周目标是理解 LLM 基础、提示工程，并手写最小 ReAct Agent 循环（不使用框架）。

当前仓库无 Python 代码、无 `experiments/` 目录。OpenSpec 用于规范驱动开发，本次变更是首次向仓库引入实验性 Python 代码。

## Goals / Non-Goals

**Goals:**

- 提供按复杂度递进的可运行 Python 实验脚本
- 使用 DeepSeek API（OpenAI 兼容 SDK），降低国内学习成本
- 共享 `_config.py` 避免各脚本重复配置
- 在 `experiments/week1/README.md` 提供完整教程（概念 + 实验 + 思考题）
- 更新 `learning-plan.md` 链接，形成「计划 ↔ 教程 ↔ 代码」闭环

**Non-Goals:**

- 真实天气 API 集成
- LangChain / LangGraph 框架
- FastAPI 服务化或部署
- 第 2–4 周实验内容
- 自动化测试套件（手动运行验证即可）

## Decisions

### 1. LLM 提供商：DeepSeek

**选择**: DeepSeek + `openai` Python SDK，`base_url=https://api.deepseek.com`，模型 `deepseek-chat`。

**理由**: 国内可访问、OpenAI 兼容、计费低，适合学习阶段反复调用。

**备选**: OpenAI（文档最全但需代理且贵）、通义/Kimi（SDK 略有差异）。

### 2. 文档组织：方案 A

**选择**: 详细教程放在 `experiments/week1/README.md`，`docs/learning-plan.md` 保留总览与 checklist 并链接到教程锚点。

**理由**: 跑实验时文档与代码同目录，减少上下文切换。

### 3. 共享配置模块 `_config.py`

**选择**: 在 `experiments/week1/_config.py` 集中初始化 OpenAI client 和 MODEL 常量。

**理由**: 5 个脚本共用同一配置，改 provider 只改一处。各实验脚本 `from _config import client, MODEL` 即可。

### 4. 天气工具：硬编码模拟

**选择**: `tools/weather.py` 返回预设城市温度字典，不调用外部 API。

**理由**: 第 1 周重点是 Function Calling 协议和 Agent 循环，不是 API 集成。

### 5. Agent 实现：手写 ReAct 循环

**选择**: `mini_agent.py` 用 while 循环 + max_iterations，不使用 LangGraph。

**理由**: 让学习者看见 Thought → Action → Observation 的每一步；第 2 周再用 LangGraph 重写形成对比。

### 6. Python 包管理：requirements.txt + venv

**选择**: 最小依赖 `openai`、`pydantic`、`python-dotenv`，用 venv 隔离。

**理由**: 第 1 周快速上手；工程化包管理留到第 3 周。

### 7. CoT 演示位置

**选择**: CoT 示例写在 `structured_output.py` 注释和 README 中，不单独建文件。

**理由**: 控制第 1 周文件数量，避免碎片化。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| DeepSeek API 变更或不可用 | 使用 OpenAI 兼容接口，文档说明如何通过 env 切换 base_url |
| 用户未配置 API Key 导致脚本报错 | `.env.example` + README 明确配置步骤；脚本启动时检查 key 并给出友好提示 |
| 手写 ReAct 与框架行为不一致 | README 说明这是教学简化版；第 2 周 LangGraph 对比 |
| `_config.py` 导入路径问题 | 所有 week1 脚本在同一目录运行；README 说明 `cd experiments/week1` 后执行 |

## Migration Plan

无需迁移——全部为新增文件。实施步骤：

1. 创建 `experiments/` 基础设施
2. 按递进顺序编写 week1 脚本
3. 编写 week1 README 教程
4. 更新 learning-plan 链接
5. 本地跑通全部脚本验证

## Open Questions

（无 — explore 阶段已确认 DeepSeek、方案 A、完整预热脚本、共享 `_config.py`）
