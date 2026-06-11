# 第 3 周：工程化

> 目标：从「能跑」到「能交付」，补齐流式、异步、健壮性、可观测、评测、安全。

## 快速开始

```bash
cd experiments
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# 确保 experiments/.env 已配置 DEEPSEEK_API_KEY

# 单元测试（纯逻辑，无需 API）
pytest tests/ -v

cd week3

# 验证 RAG Agent（需 API Key）
python agent.py

# 启动 FastAPI 服务
uvicorn app:app --reload --port 8000

# 另开终端：SSE 流式对话
curl -N -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"第 3 周的学习目标是什么？"}'

# 并发演示
python concurrency_demo.py

# 离线评测（需 API）
python eval/run_eval.py
```

**首次运行 RAG**：会下载 FastEmbed 模型 `BAAI/bge-small-zh-v1.5`。

---

## 1. 规范驱动开发

本目录通过 OpenSpec 变更 `week3-learning-experiments` 落地，完整走 propose → apply → archive 流程。

---

## 2. 流式与异步 {#2-流式与异步}

### 2.1 SSE 打字机效果

`app.py` 暴露 `POST /chat`，返回 `text/event-stream`：

```
data: {"token": "第"}
data: {"token": " 3"}
...
data: [DONE]
```

底层 `agent.py` 使用 `ChatOpenAI.astream` 逐 token 透传。

### 2.2 asyncio 并发

`concurrency_demo.py` 用 `asyncio.gather` 并发 3 个问题，对比串行总耗时，体会 Node.js 式异步心智。

---

## 3. 健壮性 {#3-健壮性}

请求链路（`app.py`）：

```
guard → rate_limit → cache → retry → agent
```

| 模块 | 文件 | 说明 |
|------|------|------|
| 重试/降级 | `resilience/retry.py` | tenacity 指数退避，失败返回兜底回复 |
| 限流 | `resilience/rate_limit.py` | 进程内令牌桶，超额 429 |
| 缓存 | `resilience/cache.py` | 相同输入命中即跳过 LLM |

### 成本控制讨论

- **已实现**：精确缓存（SHA256 key）
- **文档延伸**：prompt 压缩、模型分级路由（小模型路由 + 大模型精答）

---

## 4. 可观测（Langfuse） {#4-可观测langfuse}

`observability/tracing.py` 提供 Langfuse `CallbackHandler`；未配置凭据时 no-op，主流程不受影响。

### 4.1 本地 Docker 启动

```bash
git clone https://github.com/langfuse/langfuse.git
cd langfuse
docker compose up -d
# 访问 http://localhost:3000 创建项目，获取 public/secret key
```

在 `experiments/.env` 填入：

```
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=http://localhost:3000
```

### 4.2 Langfuse Cloud

在 [cloud.langfuse.com](https://cloud.langfuse.com) 创建项目，将 key 写入 `.env`，`LANGFUSE_HOST` 可省略（使用默认 Cloud 地址）。

---

## 5. 安全防护 {#5-安全防护}

`security/guard.py` 在 `/chat` 入口执行：

1. **Prompt Injection**：启发式检测「忽略以上指令」等模式 → 400 拦截
2. **敏感信息脱敏**：手机号、邮箱正则替换后继续处理

> 生产环境需结合模型护栏、专用 WAF；此处为认知 + 第一道防线。

---

## 6. 评测（LLM-as-judge） {#6-评测llm-as-judge}

```
eval/dataset.jsonl → run_eval.py → agent → judge.py
                                              └→ 规则基线对照
```

- `dataset.jsonl`：~10 条问题 + 参考答案
- `judge.py`：固定 rubric、temperature=0 打分（accuracy / relevance 1-5）
- `rule_baseline`：关键词命中率对照
- 报告输出到 `eval/reports/report_*.json`

---

## 7. 目录结构

```
week3/
├── _config.py              # DeepSeek + Langfuse 配置
├── agent.py                # 自包含 RAG + 记忆 Agent
├── app.py                  # FastAPI SSE 服务
├── concurrency_demo.py     # 并发 vs 串行
├── data/sample.md          # RAG 示例文档
├── resilience/             # 重试、限流、缓存
├── observability/tracing.py
├── security/guard.py
├── eval/                   # 离线评测
└── README.md
```

---

## 8. 实验指南

| 顺序 | 操作 | 观察点 |
|------|------|--------|
| 1 | `pytest ../tests/test_week3_resilience.py -v` | 令牌桶、缓存、guard、retry |
| 2 | `python agent.py` | RAG 检索是否引用 data/ 内容 |
| 3 | `uvicorn app:app --port 8000` + curl SSE | 打字机逐 token |
| 4 | 连续快速 curl | 429 限流 |
| 5 | 相同问题 curl 两次 | 第二次 cache 命中（响应更快） |
| 6 | 发送「忽略以上指令」 | 400 拦截 |
| 7 | `python concurrency_demo.py` | 并发加速比 |
| 8 | 配置 Langfuse 后请求 | trace 面板出现记录 |
| 9 | `python eval/run_eval.py` | 评测报告 JSON |

---

## 9. 思考题

1. SSE 与 WebSocket 各适合什么场景？Agent 聊天为什么常用 SSE？
2. 进程内令牌桶 vs Redis 分布式限流，何时需要升级？
3. LLM-as-judge 与规则基线各有什么偏差？如何降低 judge 方差？
4. 精确缓存 vs 语义缓存，后者如何解决「同义不同表述」？
5. 启发式 prompt injection 检测的盲区是什么？生产如何补强？

---

## 10. 常见坑

| 现象 | 原因 | 解决 |
|------|------|------|
| `DEEPSEEK_API_KEY` 报错 | 未配置 `.env` | 复制 `.env.example` |
| 首次 RAG 很慢 | 下载 embedding 模型 | 保持网络，耐心等待 |
| astream 不逐 token | API 批量返回 | 检查 DeepSeek 流式支持；可降级 OpenAI SDK |
| Langfuse 无 trace | 未配 key 或服务未起 | 检查 `.env` 与 docker compose |
| eval 成本高 | 每条样本 2 次 LLM | 数据集控制在 ~10 条演示 |
| import 失败 | 工作目录不对 | `cd experiments/week3` 再运行 |

---

## 与第 4 周边界

- **本周**：单一 `/chat` + 中间件夹层 + 最小 Agent 内核
- **第 4 周**：分层架构、Docker 部署、前端界面
