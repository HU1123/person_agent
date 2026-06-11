# week2-experiments Specification

## Purpose
TBD - created by archiving change week2-learning-experiments. Update Purpose after archive.
## Requirements
### Requirement: 第 2 周 Python 依赖可安装

实验目录 SHALL 在 `experiments/requirements.txt` 中声明第 2 周所需依赖（含 langgraph、langchain 相关包、chromadb、sentence-transformers），使学习者在已有 week1 venv 中升级安装后即可运行 week2 脚本。

#### Scenario: 升级安装依赖

- **WHEN** 学习者执行 `pip install -r experiments/requirements.txt`
- **THEN** week2 全部脚本所需的 Python 包被安装且无版本冲突报错

### Requirement: LangGraph 重写天气 Agent

系统 SHALL 提供 `agent_langgraph.py`，使用 LangGraph 实现与 week1 `mini_agent.py` 等价的 ReAct 流程（DeepSeek chat + `get_weather` 工具），State 使用 `messages`，并设置 recursion_limit 防止死循环。

#### Scenario: 多城市天气比较

- **WHEN** 学习者执行 `python agent_langgraph.py` 并提出需多次查天气的问题
- **THEN** 图在 agent 与 tools 节点间循环直至 LLM 返回无 tool_calls 的最终答案

#### Scenario: 循环上限保护

- **WHEN** 图执行达到 recursion_limit 仍未结束
- **THEN** 运行终止并输出可理解的超限提示

### Requirement: RAG 文档问答实验

系统 SHALL 提供 `rag_qa.py`，对 `experiments/week2/data/` 下示例文档完成切分、本地 embedding、Chroma 持久化索引、相似度检索与 LLM 问答，并在检索后打印所用 chunk 摘要便于调试。

#### Scenario: 首次建库并提问

- **WHEN** 学习者执行 `python rag_qa.py` 并询问与示例文档相关的事实性问题
- **THEN** 系统从 Chroma 检索 top-k 片段、注入 prompt 并返回基于文档内容的回答

#### Scenario: 检索可观测

- **WHEN** RAG 管线完成检索
- **THEN** 脚本向控制台输出本次使用的 chunk 来源或内容摘要

### Requirement: 带 RAG 与记忆的合体 Agent

系统 SHALL 提供 `agent_memory.py`，在 LangGraph 编排下集成 RAG 检索、CLI 多轮短期会话历史，以及基于本地文件（JSON 或 SQLite）的长期记忆读写，使 Agent 能结合文档知识与跨轮用户事实回答问题。

#### Scenario: 多轮对话保持上下文

- **WHEN** 学习者在同一进程内连续输入多轮问题
- **THEN** Agent 能引用先前轮次中已确立的对话内容作答

#### Scenario: 长期记忆写入与召回

- **WHEN** 学习者提供应持久化的事实（如姓名、偏好）并在后续轮次询问
- **THEN** Agent 从长期记忆存储召回该事实并用于回答

#### Scenario: RAG 与记忆协同

- **WHEN** 用户问题同时涉及示例文档知识与已存储的长期事实
- **THEN** Agent 在生成回答时同时利用检索到的文档片段与长期记忆

### Requirement: 第 2 周学习文档

系统 SHALL 在 `experiments/week2/README.md` 提供完整教程，涵盖 LangChain/LangGraph/LlamaIndex 选型对比、Embedding 与 Chroma、RAG 全流程、短期/长期记忆、MCP 协议认知（含与 Function Calling 对比），以及各实验的运行方式、观察要点、思考题与常见坑。

#### Scenario: 按文档完成第 2 周学习

- **WHEN** 学习者阅读 `experiments/week2/README.md` 并按顺序运行全部 week2 实验
- **THEN** 学习者能解释 RAG 流程与记忆分层，并完成 `docs/learning-plan.md` 第 2 周 checklist 对应项

### Requirement: 学习计划第 2 周链接闭环

`docs/learning-plan.md` 第 2 周 checklist 中的产出文件项（`agent_langgraph.py`、`rag_qa.py`、`agent_memory.py`）SHALL 链接到 `experiments/week2/README.md` 对应章节锚点。

#### Scenario: 从计划跳转到 week2 教程

- **WHEN** 学习者在 learning-plan 中点击第 2 周某实验项链接
- **THEN** 跳转到 week2 README 中该实验的指南章节

### Requirement: week2 共享配置与示例数据

系统 SHALL 提供 `experiments/week2/_config.py`（DeepSeek client / ChatOpenAI、embedding 与 Chroma 路径常量）及 `experiments/week2/data/sample.md` 作为默认索引语料。

#### Scenario: 缺少 API Key 时友好失败

- **WHEN** 学习者未配置 `DEEPSEEK_API_KEY` 即运行 week2 脚本
- **THEN** 脚本在启动时输出与 week1 一致风格的配置指引并退出

