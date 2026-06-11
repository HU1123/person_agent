# 第 3 周「工程化」设计文档

> 本文件先行沉淀技术选型与取舍,`proposal.md` / `tasks.md` 待确认后再补。
> 探索结论来自 [openspec-explore] 会话的三项关键决策。

## Context

第 1 周手写 ReAct Agent,第 2 周用 LangGraph 完成「RAG + 记忆」问答 Agent。
现在要把这个「能跑」的 Agent 升级到「能交付」:补齐流式、异步、健壮性、可观测、评测、安全这些 Agent 特有的工程能力,产出**一个健壮、可观测、有评测的 Agent 服务雏形**,并为第 4 周的完整 FastAPI 应用打底。

延续 week1/week2 模式:落在 `experiments/week3/`,共享 `_config.py`,配 `README.md` 教程与思考题,关键逻辑进 `experiments/tests/`(纯逻辑、免 API)。

## Goals

- 在 `week3/` 内**自包含**实现一个紧凑的「RAG + 极简记忆」Agent,并包成 FastAPI 服务提供 SSE 流式接口
- 用「中间件夹层」串起健壮性(超时/重试/降级/限流/缓存)、安全(prompt injection / 敏感信息)、可观测(Langfuse trace)
- 落地一条**离线评测闭环**,以 **LLM-as-judge** 为核心(准确率 / 相关性 / 成本)
- 走一次完整 OpenSpec 流程(propose → apply → archive)作为「规范驱动开发」板块的亲身体验

## Non-Goals

- 不做生产级部署(Docker 化业务服务、云部署留到第 4 周)
- 不做完整分层架构(Controller/Service/Repo 留到第 4 周)
- 不做前端界面(第 4 周)
- 不追求 rerank、混合检索等 RAG 进阶(第 2 周已标记可选)
- 评测不追求大规模数据集与统计显著性,够演示方法论即可

## Key Decisions

### D1. 产出形态:重产出(FastAPI 服务雏形 + 中间件夹层)

**选择**:搭一个最小但「五脏俱全」的 Agent 服务,外层 FastAPI + SSE,中间是健壮性/安全/可观测的夹层,内核为 week3 自包含的紧凑 Agent。

**理由**:第 3 周产出目标本就是「Agent 服务」;流式 SSE、异步并发、限流/重试中间件都需要一个 server 承载才有真实落点;同时为第 4 周 FastAPI 应用打底。

**取舍**:会与第 4 周 FastAPI 有部分重叠。通过 Non-Goals 划清边界——第 3 周只做「能力夹层 + 单一 /chat 接口」,不做分层架构、不做部署、不做前端。

**备选(未采纳)**:纯脚本路线(各能力独立 demo)。概念聚焦但「服务感」弱,SSE 没有承载体,与重产出目标不符。

### D2. Agent 内核:week3 **自包含**的「紧凑 RAG + 极简记忆」Agent

**选择**:`week3/agent.py` 自己实现一个紧凑 Agent(加载 `data/` 示例文档 → Chroma 检索 → 注入 prompt → DeepSeek 生成 + 一个极简的会话内/跨会话记忆),**复用 week2 的思路而非代码**,async 化以支持流式与并发。

**理由**:学习项目里每周应当能**独立读懂**。若 `week3` import `week2` 的 `agent_memory`,会叠成 `week3 → week2 → week1` 的依赖链,读单周也要跨文件跳转,可读性差。第 3 周主角是外层「健壮性/可观测/评测/安全」夹层,内核只需够撑起端到端 demo 即可。

**取舍**:RAG/记忆逻辑与 week2 有少量重复,但换来 `week3/` 目录从上到下自洽可读。异步化用 `ainvoke` / `astream`。

**备选(未采纳)**:① import week2 代码——跨周依赖、可读性差;② 抽公共 `lib` 给 week2/week3 共用——最「正确」但要回头重构 week2,scope 变大,本周不做(可作为后续重构)。

### D3. 流式与异步:FastAPI StreamingResponse + LangGraph `astream`

**选择**:`POST /chat` 返回 SSE;底层用 LangGraph 的 `astream`(`stream_mode="messages"`)逐 token 透传。并发用 `asyncio.gather` 做一个压测小脚本对照 Node.js 异步心智。

**取舍**:LangChain `ChatOpenAI` 的 `astream` 需确认 DeepSeek 兼容流式;若有问题,降级为直接用 OpenAI SDK `stream=True`。

### D4. 健壮性:tenacity 重试 + 令牌桶限流 + 缓存

| 能力 | 方案 | 落点 |
|---|---|---|
| 超时 / 重试 / 降级 | `tenacity`(指数退避 + 重试上限),失败降级到缓存/兜底回复 | `resilience/retry.py` |
| 限流 | 进程内令牌桶 | `resilience/rate_limit.py` |
| 成本控制 | 精确缓存(命中即跳过 LLM)+ 可选语义缓存;prompt 压缩、模型分级路由作为文档讨论 | `resilience/cache.py` |

**取舍**:限流/缓存先做单进程内存版(教学够用);分布式(Redis)留作文档延伸,不实现。

### D5. 可观测:Langfuse,本地 Docker 自部署

**选择**:Langfuse `CallbackHandler` 接入 LangGraph,记录每次请求的 latency / token / cost / trace 树;Langfuse 本体用官方 `docker compose` 本地起。

**理由**:延续 week2「自己掌控全链路」风格;开源、数据本地、可反复实验。

**取舍**:比 LangSmith 多一步起容器。`tracing.py` 设计为「配了 key 才启用」,无 key 时优雅降级为 no-op,保证无 Langfuse 也能跑通主流程。README 同时给出 Cloud 与 docker 两种接法。

**备选(未采纳)**:LangSmith。设环境变量即用,但 SaaS、国内访问、风格不符。

### D6. 评测:以 LLM-as-judge 为核心

**选择**:`eval/dataset.jsonl`(问题 + 参考答案)→ `run_eval.py` 批量调 agent → `judge.py` 用 LLM 对「准确率 / 相关性」打分(1–5 或 0/1),叠加客观指标(token / 估算成本 / 延迟)→ 输出汇总报告。

**取舍**:LLM-as-judge 有主观性与成本;通过固定 judge prompt、低 temperature、给出评分 rubric 降低方差。规则匹配(精确/包含)作为对照基线一起跑,凸显两种方法差异。

### D7. 安全:输入侧 guard

**选择**:`security/guard.py` 在请求进入 agent 前做 (a) prompt injection 启发式检测(关键词/指令覆盖模式),(b) 敏感信息正则过滤(手机号/邮箱等),命中则拦截或脱敏。

**取舍**:启发式无法覆盖所有注入;定位为「认知 + 第一道防线」,文档说明生产需结合模型护栏 / 专用服务。

## Request Lifecycle(请求穿过夹层)

```
client(SSE)
  └─► POST /chat
        ├─ ① security.guard      注入/敏感词 → 命中即拒绝/脱敏
        ├─ ② rate_limit          令牌桶 → 超额 429
        ├─ ③ cache               命中 → 直接返回(省 token)
        ├─ ④ retry/fallback      包住 LLM 调用(超时→重试→降级)
        ├─ ⑤ agent(week3 自包含 RAG+极简记忆) async astream
        └─ ⑥ langfuse trace      全程 latency/token/cost
  ◄── SSE 逐 token 吐字(打字机)

离线评测闭环:
dataset.jsonl → run_eval.py → agent → judge.py(LLM 打分)
                                         └► 报告:准确率/相关性/token/成本
```

## 目录结构(拟)

```
experiments/week3/
├── _config.py            # 复用 DeepSeek + Langfuse 配置(key 缺失则 no-op)
├── app.py                # FastAPI:POST /chat (SSE) + /health
├── agent.py              # 自包含紧凑 RAG + 极简记忆(async)
├── data/                 # 示例文档,供 RAG 索引
├── resilience/{retry,rate_limit,cache}.py
├── observability/tracing.py
├── security/guard.py
├── eval/{dataset.jsonl,judge.py,run_eval.py}
└── README.md
```

## 新增依赖(拟)

`fastapi`、`uvicorn[standard]`、`tenacity`、`langfuse`。流式优先用 FastAPI 内置 `StreamingResponse`(必要时加 `sse-starlette`)。

## Risks / Open Questions

- **DeepSeek 流式兼容**:`langchain-openai` 的 `astream` 对 DeepSeek 是否稳定逐 token,需先验证;否则降级 OpenAI SDK 原生 stream。
- **代码重复**:自包含使 RAG/记忆逻辑与 week2 有少量重复;接受此代价换可读性,后续可抽公共 `lib` 统一。
- **Langfuse docker 资源**:本地起 Postgres + Langfuse 容器,确认机器可承受;提供 Cloud 兜底路径。
- **评测成本**:LLM-as-judge 每条都要额外 LLM 调用,数据集规模控制在 ~10 条以内做演示。
- **范围蔓延**:与第 4 周 FastAPI 边界需持续守住,见 Non-Goals。

## 与计划 checklist 的映射

| 计划条目 | 落点 |
|---|---|
| 1.1/1.2 规范驱动开发 | 本变更走 propose→apply→archive 全流程 |
| 2.1 流式 SSE | `app.py` + `agent.py` astream |
| 2.2 asyncio 并发 | 并发压测小脚本 |
| 3.1 超时/限流/重试/降级 | `resilience/` |
| 3.2 成本控制 | `resilience/cache.py` + README 讨论 |
| 4.1 Tracing | `observability/tracing.py`(Langfuse) |
| 4.2 评测集 | `eval/`(LLM-as-judge 为主) |
| 4.3 安全 | `security/guard.py` |
