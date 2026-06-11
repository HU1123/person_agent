## 1. 依赖与基础设施

- [ ] 1.1 更新 `experiments/requirements.txt`(新增 `fastapi`、`uvicorn[standard]`、`tenacity`、`langfuse`)
- [ ] 1.2 创建 `experiments/week3/_config.py`(复用 DeepSeek ChatOpenAI + API Key 检查;新增 Langfuse 配置,凭据缺失则降级为 no-op)
- [ ] 1.3 在 `.gitignore` 增加 week3 运行产物(`experiments/week3/.chroma/`、`.memory/`、评测报告输出)
- [ ] 1.4 创建 `experiments/week3/data/`(放入 RAG 示例文档)

## 2. 自包含 Agent 内核

- [ ] 2.1 创建 `experiments/week3/agent.py`:加载 `data/` → Chroma 检索 → 注入 prompt → DeepSeek 生成(不 import week1/week2)
- [ ] 2.2 增加极简记忆(会话内 + 跨会话 JSON),并提供 `ainvoke`/`astream` 异步入口
- [ ] 2.3 用 `data/` 中的问题验证检索与回答准确性

## 3. FastAPI SSE 服务

- [ ] 3.1 创建 `experiments/week3/app.py`:`GET /health` + `POST /chat`(SSE 流式)
- [ ] 3.2 接通 `agent.astream`,逐 token 以 `text/event-stream` 推送
- [ ] 3.3 验证流式打字机效果(curl 或浏览器)

## 4. 异步并发演示

- [ ] 4.1 创建并发演示脚本(`asyncio.gather` 并发多请求,打印总耗时)
- [ ] 4.2 与串行对照,观察加速

## 5. 健壮性夹层

- [ ] 5.1 创建 `experiments/week3/resilience/retry.py`(超时 + 指数退避重试 + 失败降级)
- [ ] 5.2 创建 `experiments/week3/resilience/rate_limit.py`(进程内令牌桶)
- [ ] 5.3 创建 `experiments/week3/resilience/cache.py`(命中即跳过 LLM)
- [ ] 5.4 将三者串入 `/chat` 请求链路(guard → rate_limit → cache → retry → agent)

## 6. 可观测(Langfuse)

- [ ] 6.1 创建 `experiments/week3/observability/tracing.py`(Langfuse CallbackHandler;无凭据时 no-op)
- [ ] 6.2 接入 Agent/服务,记录 latency / token / cost
- [ ] 6.3 README 写明 Langfuse 本地 docker 启动与 Cloud 两种接法

## 7. 安全防护

- [ ] 7.1 创建 `experiments/week3/security/guard.py`(prompt injection 启发式检测 + 敏感信息脱敏)
- [ ] 7.2 接入 `/chat` 入口,命中即拦截/脱敏

## 8. 评测闭环(LLM-as-judge)

- [ ] 8.1 创建 `experiments/week3/eval/dataset.jsonl`(~10 条:问题 + 参考答案)
- [ ] 8.2 创建 `experiments/week3/eval/judge.py`(固定 rubric、低 temperature 打分)
- [ ] 8.3 创建 `experiments/week3/eval/run_eval.py`(批量调 agent + 汇总报告 + 规则匹配基线)
- [ ] 8.4 跑通一次评测,产出报告

## 9. 测试

- [ ] 9.1 在 `experiments/tests/` 增加纯逻辑测试:`rate_limit`(令牌桶)、`cache`(命中/未命中)、`guard`(注入/脱敏)、`retry`(降级)
- [ ] 9.2 `pytest tests/` 全绿(免 API)

## 10. 文档与计划更新

- [ ] 10.1 创建 `experiments/week3/README.md`(流式/异步、健壮性、可观测、评测方法论、安全、实验指南、思考题、常见坑)
- [ ] 10.2 更新 `experiments/README.md`(week3 运行说明与新增依赖)
- [ ] 10.3 更新 `docs/learning-plan.md`(第 3 周 checklist 链接到 week3 README 锚点,状态改为进行中)

## 11. 验证

- [ ] 11.1 venv 安装新依赖;`pytest tests/` 全绿
- [ ] 11.2 启动 `uvicorn` 跑通 `/health` 与 `/chat` 流式;跑通 `eval/run_eval.py`
