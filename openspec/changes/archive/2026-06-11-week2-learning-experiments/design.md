## Context

本项目是个人 Agent 学习仓库。第 1 周变更 `week1-learning-experiments` 已完成：`experiments/week1/` 含 DeepSeek 调用、Function Calling 与手写 `mini_agent.py` ReAct 循环。学习者背景为 Node.js 后端开发者。

第 2 周学习计划在 `docs/learning-plan.md` 中定义：LangGraph 框架、RAG（Embedding + 向量库）、短期/长期记忆、MCP 认知。当前无 `experiments/week2/` 代码与教程。探索阶段已确认：LangGraph 对照 week1 循环、Chroma 本地向量库、RAG 与记忆分文件递进、MCP 以文档认知为主。

## Goals / Non-Goals

**Goals:**

- 用 LangGraph 重写 `mini_agent.py`，使学习者理解 State、Node、Conditional Edge
- 实现完整 RAG 管线（切分 → embedding → Chroma 存储 → 检索 → 注入 prompt）的 `rag_qa.py`
- 实现 `agent_memory.py`：LangGraph Agent + RAG 检索 + 短期会话历史 + 简单长期记忆持久化
- 在 `experiments/week2/README.md` 提供框架对比、RAG/记忆概念、MCP 认知与实验指南
- 更新 `learning-plan.md` 第 2 周链接，延续「计划 ↔ 教程 ↔ 代码」闭环
- 扩展 `requirements.txt`，文档说明 venv 升级安装

**Non-Goals:**

- FastAPI / SSE 服务化（第 3 周）
- 生产级 rerank、混合检索、多租户
- 自建并部署 MCP server（第 2 周 README 说明协议 + Cursor 现有 MCP 即可；可选附录命令）
- 真实天气 API、替换 week1 硬编码工具逻辑
- 自动化 pytest 套件（手动跑通验证）
- 修改 week1 脚本行为（仅允许 README 交叉引用）

## Decisions

### 1. Agent 框架：LangGraph + 最小 LangChain 积木

**选择**: `langgraph` 负责 `agent_langgraph.py` 与 `agent_memory.py` 的控制流；`langchain`、`langchain-core`、`langchain-text-splitters` 负责 Document Loader 与 Text Splitter；`langchain-openai` 的 `ChatOpenAI` 指向 DeepSeek（与 week1 相同 base_url）。

**理由**: 与学习计划一致；LangGraph 是第 2 周核心；文档处理用 LangChain 生态最常见，避免同时引入 LlamaIndex 双栈。

**备选**: LlamaIndex 专精 RAG——若 RAG 脚本过长可后续 refactor，本次不默认。

### 2. LLM：延续 DeepSeek chat

**选择**: `experiments/week2/_config.py` 初始化 `ChatOpenAI`（或保留 `OpenAI` client 供 rag 纯 completion），`model=deepseek-chat`，`base_url=https://api.deepseek.com`，从 `experiments/.env` 读取 `DEEPSEEK_API_KEY`。

**理由**: 与 week1 一致，降低配置成本。

### 3. Embedding：本地 FastEmbed

**选择**: 默认 `fastembed` + 模型 `BAAI/bge-small-zh-v1.5`；通过 `langchain_community.embeddings.fastembed.FastEmbedEmbeddings` 接入。

**理由**: 学习阶段无需第二套 API Key；避免 macOS 上 `sentence-transformers` 与 PyTorch 2.4+ 的版本冲突；中文友好。

**备选**: HuggingFaceEmbeddings / OpenAI 兼容 embedding API——在 README 标注切换方式。

### 4. 向量数据库：Chroma 持久化

**选择**: `chromadb` 持久化目录 `experiments/week2/.chroma/`（加入 `.gitignore`）；`rag_qa.py` 建库与查询；`agent_memory.py` 复用同一 collection 或按脚本重建。

**理由**: 学习计划点名 Chroma；自带元数据与持久化，比裸 FAISS 适合教学。

**备选**: FAISS——README 对比表说明，不实现。

### 5. 示例文档与 chunk 策略

**选择**: `experiments/week2/data/sample.md`（从 `docs/learning-plan.md` 摘录第 2 周章节，避免索引整个仓库）；`RecursiveCharacterTextSplitter`，`chunk_size=500`，`chunk_overlap=50`。

**理由**: 可预测的问答评测（如「第 2 周产出是什么」）；chunk 参数可在 README 做实验说明。

### 6. week1 工具复用

**选择**: `agent_langgraph.py` 通过 `sys.path` 将 `experiments/week1` 加入路径，`from tools.weather import ...` 复用 `WEATHER_TOOL_SCHEMA` 与 `get_weather`。

**理由**: 与 `mini_agent.py` 行为一致，强化「框架重写」对比；不复制 weather 代码。

### 7. LangGraph 图结构（天气 Agent）

**选择**: State 含 `messages: Annotated[list, add_messages]`；节点 `agent`（bind tools 的 LLM）、`tools`（`ToolNode`）；边：`agent` → 条件（有 tool_calls → `tools` → `agent`，否则 END）；`recursion_limit` 对标 week1 `MAX_ITERATIONS=5`。

**理由**: 与官方 ReAct 教程一致，便于对照 week1 的 for 循环。

### 8. 记忆分层

**选择**:

- **短期**: `agent_memory.py` 的 State 中 `messages` 跨 CLI 多轮 append；进入 LLM 前对超长 history 做条数裁剪（如保留最近 20 条）或简单 token 估算截断。
- **长期**: `experiments/week2/.memory/store.json`（或 SQLite 单表）存储用户声明的事实（如「我叫小明」）；每轮可选检索注入 system prompt；提供 `remember` 工具或命令让 LLM 写入。

**理由**: 分离关注点；长期记忆先用 JSON 降低依赖，符合学习阶段。

### 9. RAG 注入方式

**选择**: `rag_qa.py` 为**无工具**的检索链：retrieve → 拼接 context → 单次 LLM 回答。`agent_memory.py` 在 `agent` 节点前增加 `retrieve` 节点或 middleware：将 top-k chunks 注入 system message。

**理由**: `rag_qa.py` 独立可调试；合体脚本专注编排。

### 10. MCP 认知

**选择**: 仅在 `week2/README.md` 增加 MCP 章节：Host/Server/Tool 模型、与 Function Calling 对比、指向 Cursor 已启用 MCP；**不**强制新增可运行 MCP server 代码（避免 scope 膨胀）。

**理由**: 学习计划 4.2「跑通 MCP」在 Cursor 环境已满足；仓库无 MCP 运行时依赖。

### 11. 文档组织：延续 week1 方案 A

**选择**: 详细教程在 `experiments/week2/README.md`；`docs/learning-plan.md` 第 2 周 checklist 链到锚点。

### 12. 配置与运行约定

**选择**: 脚本在 `experiments/week2/` 目录下执行（`cd experiments/week2`）；`.env` 仍在 `experiments/.env`；`.gitignore` 增加 `week2/.chroma/`、`week2/.memory/`。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| sentence-transformers 首次下载慢/失败 | README 说明镜像与离线；提供最小 `sample.md` |
| LangGraph API 版本漂移 | requirements.txt 锁定次版本；README 注明文档日期 |
| Chroma 与 Python 3.11+ 兼容性 | 实施时 pin chromadb 版本并在 6.x 验证任务中跑通 |
| week1 import 路径错误 | README 强调运行目录；脚本启动时检测 import 并提示 |
| RAG 检索不准 | 实验要求打印 retrieved chunks；README 常见坑 |
| 长期记忆与 RAG 混淆 | README 对比表 + 不同存储路径 |
| 依赖体积增大 | README 说明可选 uv；第 2 周单独 venv 亦可 |

## Migration Plan

1. 更新 `experiments/requirements.txt` 并 `pip install -r requirements.txt`
2. 创建 `week2/_config.py`、`data/sample.md`
3. 实现 `agent_langgraph.py` → `rag_qa.py` → `agent_memory.py`
4. 编写 `week2/README.md`，更新 `experiments/README.md` 与 `learning-plan.md`
5. 配置 `.gitignore`，本地依次跑通三脚本

无破坏性变更；week1 脚本不受影响。

## Open Questions

- （无阻塞项）embedding 若 HuggingFace 下载困难，实施阶段可在 design 备选路径切换为 DeepSeek/OpenAI 兼容 embedding API，需额外 env 变量。
