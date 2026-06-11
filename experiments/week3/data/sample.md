# 第 3 周：工程化（学习摘录）

## 目标

从「能跑」到「能交付」，补齐 Agent 特有的工程能力：流式、异步、健壮性、可观测、评测、安全。

## 流式与异步

- SSE（Server-Sent Events）实现打字机效果
- FastAPI StreamingResponse 逐 token 推送
- asyncio.gather 并发处理多个请求，对比串行吞吐

## 健壮性

- 超时、指数退避重试、失败降级
- 进程内令牌桶限流
- 精确缓存：相同输入命中即跳过 LLM 调用

## 可观测

- Langfuse 记录 trace、latency、token、cost
- 本地 Docker 自部署或 Cloud 接入
- 未配置凭据时优雅降级为 no-op

## 评测

- LLM-as-judge：固定 rubric、低 temperature 打分
- 规则匹配基线对照
- 离线 dataset.jsonl 批量评测

## 安全

- Prompt Injection 启发式检测
- 敏感信息（手机号、邮箱）脱敏

## 本周产出

一个健壮、可观测、有评测的 Agent 服务雏形。
