## Why

学习计划第 2 周要求掌握 LangGraph 编排、RAG 检索增强与 Agent 记忆机制，但仓库目前仅有第 1 周实验代码，缺少 `experiments/week2/` 可运行示例与配套教程。第 1 周已手写 ReAct 循环，现在需要引入框架对照、向量检索与多轮记忆，形成「带 RAG + 记忆的问答 Agent」这一可展示产出。

## What Changes

- 扩展 `experiments/requirements.txt`：LangGraph、LangChain 文档处理、Chroma、本地 embedding 等第 2 周依赖
- 新增 `experiments/week2/` 实验代码：
  - `agent_langgraph.py` — 用 LangGraph 重写第 1 周 `mini_agent.py`（天气工具）
  - `rag_qa.py` — 文档切分 → 向量化 → Chroma 检索 → 问答 Demo
  - `agent_memory.py` — LangGraph + RAG + 短期/长期记忆的合体 Agent
  - `_config.py` — 复用 DeepSeek chat；embedding 与向量库配置
  - `tools/` — 复用或引用 week1 天气工具（可选 symlink/import 说明）
  - `data/` — 示例文档（如 `learning-plan.md` 片段）供 RAG 索引
- 新增 `experiments/week2/README.md` — 框架对比、RAG 流程、记忆分层、MCP 认知、实验指南与思考题
- 更新 `docs/learning-plan.md` — 第 2 周 checklist 链接到 week2 教程锚点
- 更新 `experiments/README.md` — week2 运行说明与新增依赖

## Capabilities

### New Capabilities

- `week2-experiments`: 第 2 周框架 + RAG + 记忆实验能力，包含 LangGraph Agent 重写、Chroma RAG 文档问答、带多轮记忆的合体 Agent、配套学习文档及 MCP 认知章节

### Modified Capabilities

（无 — `week1-experiments` 需求不变；第 2 周为新增 capability，不修改第 1 周 spec）

## Impact

- **新增文件**: `experiments/week2/` 下约 12 个文件（代码、示例数据、文档）
- **修改文件**: `experiments/requirements.txt`、`experiments/README.md`、`docs/learning-plan.md`
- **依赖**: 在 week1 基础上新增 `langgraph`、`langchain`、`langchain-openai`（或兼容层）、`chromadb`、本地 embedding（`sentence-transformers` 或 API embedding，见 design.md）
- **外部服务**: DeepSeek chat API（延续 week1）；embedding 可能使用本地模型或额外 API Key
- **Out of scope**: FastAPI 服务化、rerank 生产级实现、自建 MCP server 生产部署、第 3–4 周内容
