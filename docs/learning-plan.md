# Agent 应用开发 · 一个月学习计划

> 转行目标:**Agent 应用开发**(国内方向,偏 Python)
> 已有基础:**Node.js 后端开发**(工程能力可迁移)
> 进度管理:勾选 `- [ ]` 跟踪;每个任务尽量关联一个产出文件,便于沉淀作品集

---

## 进度总览

| 周次 | 主题 | 状态 |
|------|------|------|
| 第 1 周 | LLM 与 Agent 基础 | ✅ 未开始 |
| 第 2 周 | 框架 + RAG | ✅ 进行中 |
| 第 3 周 | 工程化 | ⬜ 未开始 |
| 第 4 周 | 实战项目(含前端) | ⬜ 未开始 |

> 完成一周后把对应状态改为 ✅,便于一眼看进度。🔄、✅、⬜

---

## 学习策略(基于你的背景)

| 模块 | 策略 | 原因 |
|------|------|------|
| Agent 机制 + RAG | 🎯 重点突破 | 核心壁垒,决定能否胜任 |
| 提示工程 | 贯穿全程,边学边练 | 是 Agent 的「编程语言」 |
| 工程化 | ⚡ 快速过 | 后端经验已覆盖大半 |
| 前端 | 📦 够用就行 | 能演示即可,非专业前端 |
| LLM 底层原理 | 理解概念即可 | 不需深入算法 |

### Node.js → Python 迁移对照

| Node.js | Python 对应 | 用途 |
|---------|------------|------|
| Express / NestJS | FastAPI | Web 框架 |
| async/await | `asyncio` / `async def` | 异步 |
| Joi / class-validator | Pydantic | 参数校验 |
| Jest | pytest | 测试 |
| npm | pip / uv / poetry | 包管理 |

---

## 第 1 周:LLM 与 Agent 基础

**目标**:搞懂 Agent 是什么,跑通第一个调用 LLM 的程序,手写最小 Agent 循环。

> 详细教程见 [experiments/week1/README.md](../experiments/week1/README.md)

### 0. Python 预热(0.5 天,你有编程基础可快速过)
- [ ] 0.1 Python 语法差异:类型注解、`asyncio`、`async def` → [预热实验](../experiments/week1/README.md#0-python-预热)
- [ ] 0.2 `pydantic` 基础(对标 class-validator) → [预热实验](../experiments/week1/README.md#0-python-预热)

### 1. LLM 基础认知
- [ ] 1.1 Token、上下文窗口、计费模型 → [1.1 Token 与上下文窗口](../experiments/week1/README.md#11-token-与上下文窗口)
- [ ] 1.2 采样参数:temperature、top_p、max_tokens → [1.2 采样参数](../experiments/week1/README.md#12-采样参数)
- [ ] 1.3 模型选型:GPT / Claude / DeepSeek / 通义 / Kimi 能力与成本 → [1.3 模型选型速查](../experiments/week1/README.md#13-模型选型速查)
- [ ] 1.4 能力边界:幻觉、知识截止 → 为什么需要工具和 RAG → [1.4 能力边界](../experiments/week1/README.md#14-能力边界)

### 2. 提示工程入门
- [ ] 2.1 System / User / Assistant 角色与消息结构 → [2.1 消息角色](../experiments/week1/README.md#21-消息角色)
- [ ] 2.2 Few-shot、CoT(思维链) → [2.2 Few-shot 与 CoT](../experiments/week1/README.md#22-few-shot-与-cot)
- [ ] 2.3 结构化输出:JSON mode → [structured_output.py](../experiments/week1/README.md#23-实验structured_outputpy)

### 3. 第一个程序与 Agent 雏形
- [ ] 3.1 跑通 LLM API 调用 → [llm_hello.py](../experiments/week1/README.md#31-实验llm_hellopy)
- [ ] 3.2 实现 Function Calling「查天气」工具 → [function_call.py](../experiments/week1/README.md#32-实验function_callpy)
- [ ] 3.3 手写最小 ReAct Agent 循环(不用框架) → [mini_agent.py](../experiments/week1/README.md#33-实验mini_agentpy)

**本周产出**:能解释 Agent 概念 + 一个手写的最小 Agent

---

## 第 2 周:框架 + RAG

**目标**:掌握主流框架,理解检索增强(RAG)与记忆机制。

> 详细教程见 [experiments/week2/README.md](../experiments/week2/README.md)

### 1. 框架入门
- [ ] 1.1 框架选型对比:LangChain / LangGraph / LlamaIndex → [1.1 框架选型对比](../experiments/week2/README.md#11-框架选型对比)
- [ ] 1.2 用 LangGraph 重写第 1 周的 Agent → [agent_langgraph.py](../experiments/week2/README.md#12-实验agent_langgraphpy)
- [ ] 1.3 理解 Agent 编排:节点、状态、条件分支 → [1.3 Agent 编排概念](../experiments/week2/README.md#13-agent-编排概念)

### 2. RAG 核心
- [ ] 2.1 Embedding 原理与模型选择 → [2.1 Embedding](../experiments/week2/README.md#21-embedding)
- [ ] 2.2 向量数据库:Chroma / FAISS(本地起步) → [2.2 向量数据库 Chroma](../experiments/week2/README.md#22-向量数据库-chroma)
- [ ] 2.3 RAG 完整流程:切分 → 向量化 → 检索 → 注入 → [2.3 RAG 流程](../experiments/week2/README.md#23-rag-流程)
- [ ] 2.4 实现文档问答 Demo → [rag_qa.py](../experiments/week2/README.md#24-实验rag_qapy)
- [ ] 2.5 检索优化:chunk 策略、rerank(进阶,可选)

### 3. 记忆机制
- [ ] 3.1 短期记忆:会话历史管理、上下文裁剪 → [记忆机制](../experiments/week2/README.md#3-记忆机制)
- [ ] 3.2 长期记忆:持久化、跨会话 → [记忆机制](../experiments/week2/README.md#3-记忆机制)
- [ ] 3.3 给 Agent 加多轮记忆 → [agent_memory.py](../experiments/week2/README.md#33-实验agent_memorypy)

### 4. MCP 认知(结合本项目)
- [ ] 4.1 理解 Model Context Protocol → [4. MCP 认知](../experiments/week2/README.md#4-mcp-认知)
- [ ] 4.2 跑通一个 MCP server 连接 → [4. MCP 认知](../experiments/week2/README.md#4-mcp-认知)

**本周产出**:一个带 RAG + 记忆的问答 Agent

---

## 第 3 周:工程化(你的后端经验大有用武之地)

**目标**:从「能跑」到「能交付」,补齐 Agent 特有的工程能力。

### 1. 规范驱动开发(用本项目的 OpenSpec)
- [ ] 1.1 用 `/opsx:propose` 提一个实验变更
- [ ] 1.2 体验 `/opsx:apply` → `/opsx:archive` 流程

### 2. 流式与异步
- [ ] 2.1 流式输出:SSE 实现打字机效果 → `experiments/week3/streaming.py`
- [ ] 2.2 `asyncio` 高并发请求处理(对标 Node.js 异步)

### 3. 健壮性(你后端经验可快速过)
- [ ] 3.1 错误处理:超时、限流、重试、降级
- [ ] 3.2 成本控制:缓存、prompt 压缩、模型分级路由

### 4. 评测与可观测(Agent 特有,重点)
- [ ] 4.1 接入 Tracing:LangSmith 或 Langfuse
- [ ] 4.2 构建评测集:准确率、相关性、成本
- [ ] 4.3 安全:敏感信息、内容审核、Prompt Injection 防护

**本周产出**:一个健壮、可观测、有评测的 Agent 服务

---

## 第 4 周:实战项目(含前端)

**目标**:独立完成一个完整 Agent 应用并部署,作为转行作品集核心。

### 选题(挑一个)
- [ ] 0.1 确定选题:
  - 个人知识库助手(RAG + 多轮对话)
  - 自动化任务 Agent(多工具调用 + 规划)
  - **Coding 助手(最贴合你 Cursor/MCP 现状)**

### 1. 后端开发(发挥你的强项)
- [ ] 1.1 FastAPI 搭建 Agent 后端接口
- [ ] 1.2 按分层架构组织:Controller / Service / Repo
- [ ] 1.3 集成工具调用 / RAG / 记忆
- [ ] 1.4 流式输出接口

### 2. 前端界面(够用就行)
- [ ] 2.1 选路线:
  - **快速路线**:Streamlit / Chainlit(几十行 Python 出界面)
  - **精品路线**:Next.js + Vercel AI SDK(发挥 Node.js 优势)
- [ ] 2.2 实现对话界面 + 流式展示
- [ ] 2.3 前后端联调

### 3. 部署与交付
- [ ] 3.1 Docker 容器化
- [ ] 3.2 部署到云服务 / Serverless
- [ ] 3.3 线上可访问验证

### 4. 文档与作品集
- [ ] 4.1 项目 README + 架构图
- [ ] 4.2 踩坑记录 / 复盘
- [ ] 4.3 简历包装,整理作品集

**本周产出**:一个线上可访问的完整 Agent 应用 + 作品集

---

## 知识点 → 学习周 对照

| 知识模块 | 主要覆盖周 | 重要程度 |
|----------|-----------|---------|
| LLM 基础认知 | 第 1 周 | ⭐⭐⭐ |
| 提示工程 | 全程 | ⭐⭐⭐ |
| Agent 机制(ReAct/Tool/Planning) | 第 1-2 周 | ⭐⭐⭐ |
| RAG 与记忆 | 第 2 周 | ⭐⭐⭐ |
| 工程化(异步/部署/评测/可观测) | 第 3 周 | ⭐⭐ |
| 应用层(FastAPI + 前端) | 第 4 周 | ⭐⭐ |

---

## 推荐资料

- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [LangGraph 官方教程](https://langchain-ai.github.io/langgraph/)
- [LlamaIndex 文档](https://docs.llamaindex.ai/)
- [Vercel AI SDK](https://sdk.vercel.ai/)
- Anthropic / OpenAI 官方 Function Calling 与 MCP 文档

---

## 学习笔记

> 在此记录每周心得、踩坑与最佳实践。

- (待补充)
