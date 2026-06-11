# week3-experiments Specification

## Purpose
TBD - created by archiving change week3-learning-experiments. Update Purpose after archive.
## Requirements
### Requirement: 自包含的 RAG + 极简记忆 Agent

`experiments/week3/agent.py` SHALL 在 week3 目录内自包含地实现一个紧凑 Agent,完成「加载 `data/` 示例文档 → Chroma 检索 → 注入 prompt → DeepSeek 生成」,并附带极简会话记忆。该 Agent MUST NOT import `experiments/week2/` 或 `experiments/week1/` 的代码,以保证每周可独立阅读。

#### Scenario: 文档相关问题被正确回答

- **WHEN** 用户就 `data/` 中已索引文档的内容提问
- **THEN** Agent 检索到相关片段并据此生成回答,且不 import week1/week2 模块

#### Scenario: 异步调用接口可用

- **WHEN** 调用方使用异步入口(`ainvoke`/`astream`)运行 Agent
- **THEN** Agent 以协程方式返回结果或逐 token 流,可被 FastAPI 复用

### Requirement: FastAPI SSE 流式服务

`experiments/week3/app.py` SHALL 提供 FastAPI 应用,暴露 `POST /chat`(以 SSE 流式逐 token 返回 Agent 回答)与 `GET /health`(健康检查)。

#### Scenario: 流式返回回答

- **WHEN** 客户端向 `POST /chat` 发送一条问题
- **THEN** 服务以 `text/event-stream` 逐 token 推送回答,形成打字机效果

#### Scenario: 健康检查

- **WHEN** 客户端请求 `GET /health`
- **THEN** 服务返回 200 与简单状态体(如 `{"status":"ok"}`)

### Requirement: 异步并发演示

`experiments/week3/` SHALL 提供一个并发演示脚本,使用 `asyncio.gather` 并发发起多个 Agent 请求,展示异步相对串行的吞吐收益,用于对照 Node.js 异步心智。

#### Scenario: 并发优于串行

- **WHEN** 运行并发演示脚本对 N 个问题发起请求
- **THEN** 脚本以 `asyncio.gather` 并发执行并打印总耗时,体现相对逐个串行的加速

### Requirement: 健壮性夹层

`experiments/week3/resilience/` SHALL 实现三类健壮性能力:`retry.py`(超时 + 指数退避重试 + 失败降级)、`rate_limit.py`(进程内令牌桶限流)、`cache.py`(命中即跳过 LLM 调用的缓存)。这些能力 MUST 以可被请求链路串联的方式提供,且核心逻辑可被纯逻辑测试覆盖(免 API)。

#### Scenario: 失败重试后降级

- **WHEN** 被包裹的调用持续超时/失败超过重试上限
- **THEN** 重试逻辑停止重试并返回降级结果(缓存或兜底回复),不抛出未处理异常

#### Scenario: 限流拦截超额请求

- **WHEN** 单位时间内请求数超过令牌桶容量
- **THEN** 限流器拒绝超额请求(供上层返回 429)

#### Scenario: 缓存命中跳过 LLM

- **WHEN** 相同输入再次到达且已存在缓存
- **THEN** 直接返回缓存结果,不发起新的 LLM 调用

### Requirement: Langfuse 可观测(可选启用)

`experiments/week3/observability/tracing.py` SHALL 提供 Langfuse 接入,记录每次请求的链路、延迟与 token/成本信息;当未配置 Langfuse 凭据时,MUST 优雅降级为 no-op,保证主流程仍可运行。

#### Scenario: 配置缺失时不影响主流程

- **WHEN** 环境未配置 Langfuse 凭据
- **THEN** tracing 以 no-op 方式运行,Agent 与服务仍正常工作

#### Scenario: 配置后产生 trace

- **WHEN** 配置了 Langfuse 凭据并发起一次请求
- **THEN** 该请求的链路与指标被上报到 Langfuse

### Requirement: 输入侧安全防护

`experiments/week3/security/guard.py` SHALL 在请求进入 Agent 前进行 (a) prompt injection 启发式检测与 (b) 敏感信息(如手机号/邮箱)识别;命中时 MUST 拦截或脱敏。

#### Scenario: 拦截注入尝试

- **WHEN** 输入包含典型指令覆盖类注入(如「忽略以上指令」)
- **THEN** guard 标记为风险并按策略拦截或清洗,阻止其直达 Agent

#### Scenario: 敏感信息脱敏

- **WHEN** 输入包含手机号或邮箱等敏感信息
- **THEN** guard 对其脱敏后再继续处理

### Requirement: LLM-as-judge 评测闭环

`experiments/week3/eval/` SHALL 提供离线评测:`dataset.jsonl`(问题 + 参考答案)、`judge.py`(以 LLM 按固定 rubric、低 temperature 对准确率/相关性打分)、`run_eval.py`(批量调用 Agent、汇总评分与客观指标并输出报告)。评测 SHALL 同时包含规则匹配基线以作对照。

#### Scenario: 批量评测产出报告

- **WHEN** 对 `dataset.jsonl` 运行 `run_eval.py`
- **THEN** 输出包含每条样本评分与汇总指标(准确率/相关性/token/成本)的报告

#### Scenario: LLM 判分与规则基线对照

- **WHEN** 评测同时运行 LLM-as-judge 与规则匹配基线
- **THEN** 报告分别呈现两种方法的结果,便于对比其差异

### Requirement: 配置与依赖

`experiments/week3/_config.py` SHALL 复用 DeepSeek chat 配置并新增 Langfuse 配置(凭据缺失时降级);`experiments/requirements.txt` SHALL 新增 `fastapi`、`uvicorn[standard]`、`tenacity`、`langfuse` 依赖。

#### Scenario: 缺少 API Key 时给出明确提示

- **WHEN** 运行需要 LLM 的 week3 脚本但未配置 `DEEPSEEK_API_KEY`
- **THEN** 程序给出明确的中文错误提示并安全退出

### Requirement: 学习文档与计划更新

`experiments/week3/README.md` SHALL 覆盖流式/异步、健壮性、Langfuse 可观测(本地 docker 接法)、LLM-as-judge 评测方法论、安全防护、实验指南与思考题;`docs/learning-plan.md` 第 3 周 checklist SHALL 链接到 week3 教程锚点。

#### Scenario: 文档可指导独立跑通

- **WHEN** 读者按 `experiments/week3/README.md` 操作
- **THEN** 能在不阅读 week1/week2 代码的前提下启动服务、跑通评测并理解各工程化板块

