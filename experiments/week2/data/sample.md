# 第 2 周：框架 + RAG（学习摘录）

## 目标

掌握主流框架，理解检索增强（RAG）与记忆机制。

## 框架入门

- 框架选型对比：LangChain / LangGraph / LlamaIndex
- 用 LangGraph 重写第 1 周的 Agent
- 理解 Agent 编排：节点、状态、条件分支

## RAG 核心

- Embedding 原理与模型选择
- 向量数据库：Chroma / FAISS（本地起步）
- RAG 完整流程：切分 → 向量化 → 检索 → 注入

## 记忆机制

- 短期记忆：会话历史管理、上下文裁剪
- 长期记忆：持久化、跨会话
- 给 Agent 加多轮记忆

## MCP 认知

- 理解 Model Context Protocol
- 跑通一个 MCP server 连接

## 本周产出

一个带 RAG + 记忆的问答 Agent。
