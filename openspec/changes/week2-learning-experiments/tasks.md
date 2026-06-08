## 1. 依赖与基础设施

- [x] 1.1 更新 `experiments/requirements.txt`（langgraph、langchain-core、langchain、langchain-openai、langchain-community、chromadb、fastembed）
- [x] 1.2 更新 `experiments/README.md`（week2 依赖说明、运行目录、模型首次下载提示）
- [x] 1.3 在 `.gitignore` 增加 `experiments/week2/.chroma/`、`experiments/week2/.memory/`
- [x] 1.4 创建 `experiments/week2/_config.py`（DeepSeek ChatOpenAI、FastEmbedEmbeddings、Chroma 路径、API Key 检查）
- [x] 1.5 创建 `experiments/week2/data/sample.md`（learning-plan 第 2 周摘录）

## 2. LangGraph Agent

- [x] 2.1 创建 `experiments/week2/agent_langgraph.py`（StateGraph + ToolNode + 条件边，复用 week1 weather 工具）
- [x] 2.2 验证与 `mini_agent.py` 同等场景（如北京上海温度比较）可跑通

## 3. RAG 文档问答

- [x] 3.1 创建 `experiments/week2/rag_qa.py`（加载 sample.md → split → embed → Chroma 持久化 → retrieve → LLM 问答）
- [x] 3.2 实现检索结果打印（chunk 来源/摘要）便于调试
- [x] 3.3 用文档相关问题验证回答准确性（如第 2 周产出描述）

## 4. 记忆合体 Agent

- [x] 4.1 创建 `experiments/week2/agent_memory.py`（LangGraph + RAG 注入 + CLI 多轮）
- [x] 4.2 实现短期记忆：messages 追加与 history 裁剪
- [x] 4.3 实现长期记忆：JSON 读写与注入 system prompt（remember_fact 工具）
- [x] 4.4 验证多轮 + 文档问答 + 长期事实召回场景（CLI 手动验证）

## 5. 学习文档

- [x] 5.1 创建 `experiments/week2/README.md`（框架对比、Embedding/Chroma、RAG 流程、记忆分层、MCP 认知、实验指南、思考题、常见坑）
- [x] 5.2 更新 `docs/learning-plan.md`（第 2 周 checklist 链接到 week2 README 锚点）

## 6. 验证

- [x] 6.1 在 venv 中安装新依赖，`pytest tests/` 全绿；跑通 `agent_langgraph.py`、`rag_qa.py`
