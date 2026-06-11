## Why

学习计划第 3 周主题是「工程化」,要求把第 2 周「能跑」的 RAG + 记忆 Agent 升级为「能交付」的服务——补齐流式、异步、健壮性、可观测、评测、安全这些 Agent 特有的工程能力。但仓库目前只有 week1/week2 实验代码,缺少 `experiments/week3/` 的可运行示例与配套教程,也未沉淀工程化最佳实践。

## What Changes

- 扩展 `experiments/requirements.txt`:新增 `fastapi`、`uvicorn[standard]`、`tenacity`、`langfuse` 等第 3 周依赖
- 新增 `experiments/week3/` 实验代码(**自包含**,不依赖 week2 代码):
  - `_config.py` — 复用 DeepSeek chat;新增 Langfuse 配置(key 缺失时优雅降级为 no-op)
  - `agent.py` — 紧凑的「RAG + 极简记忆」Agent(加载 `data/` → Chroma 检索 → 注入 → DeepSeek 生成),async 化
  - `app.py` — FastAPI:`POST /chat`(SSE 流式)+ `/health`
  - `resilience/{retry,rate_limit,cache}.py` — 超时/重试/降级、令牌桶限流、缓存
  - `observability/tracing.py` — Langfuse CallbackHandler 接入(可选启用)
  - `security/guard.py` — prompt injection 启发式检测 + 敏感信息脱敏
  - `eval/{dataset.jsonl,judge.py,run_eval.py}` — 以 LLM-as-judge 为核心的离线评测闭环 + 规则基线
  - `data/` — RAG 示例文档
  - `concurrency_demo.py`(或同义脚本)— `asyncio.gather` 并发对照
- 新增 `experiments/week3/README.md` — 流式/异步、健壮性、可观测(Langfuse 本地 docker)、评测方法论、安全、实验指南与思考题
- 更新 `docs/learning-plan.md` — 第 3 周 checklist 链接到 week3 教程锚点,并补 `experiments/week3/` 文件名
- 更新 `experiments/README.md` — week3 运行说明与新增依赖
- 更新 `.gitignore` — 忽略 week3 运行产物(`.chroma/`、`.memory/`、评测报告等)
- 走一次完整 OpenSpec 流程(propose → apply → archive),作为「规范驱动开发」板块的亲身体验

## Capabilities

### New Capabilities

- `week3-experiments`: 第 3 周工程化实验能力,包含自包含 RAG+记忆 Agent 的 FastAPI/SSE 服务化、健壮性夹层(超时/重试/降级/限流/缓存)、Langfuse 可观测、LLM-as-judge 评测闭环、输入侧安全防护,以及配套学习文档与思考题

### Modified Capabilities

(无 — `week1-experiments`、`week2-experiments` 需求不变;第 3 周为新增 capability,不修改前两周 spec)

## Impact

- **新增文件**: `experiments/week3/` 下约 15 个文件(代码、示例数据、评测集、文档)
- **修改文件**: `experiments/requirements.txt`、`experiments/README.md`、`docs/learning-plan.md`、`.gitignore`
- **新增依赖**: `fastapi`、`uvicorn[standard]`、`tenacity`、`langfuse`(流式优先用 FastAPI 内置 `StreamingResponse`)
- **外部服务**: DeepSeek chat API(延续前两周);Langfuse 本地 docker 自部署(可选,未配置时 trace 降级为 no-op)
- **Out of scope**: 完整分层架构(Controller/Service/Repo)、业务服务 Docker 化与云部署、前端界面、rerank/混合检索等 RAG 进阶、分布式限流/缓存(Redis)——均留待第 4 周或后续重构
