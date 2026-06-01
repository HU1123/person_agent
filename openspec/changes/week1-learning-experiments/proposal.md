## Why

学习计划第 1 周要求跑通 LLM 调用并手写最小 Agent 循环，但仓库目前只有文档规划、没有可运行的实验代码。需要一次性搭建 `experiments/week1/` 基础设施与教程，让学习者能按递进顺序动手实践，并沉淀为作品集素材。

## What Changes

- 新增 `experiments/` 目录：Python 依赖、环境变量模板、总览 README
- 新增第 1 周实验代码（DeepSeek + OpenAI 兼容 SDK）：
  - `00_python_warmup.py` — Python 类型注解、asyncio、Pydantic 预热
  - `llm_hello.py` — 第一次 LLM API 调用
  - `structured_output.py` — JSON mode + Pydantic 结构化输出
  - `function_call.py` — Function Calling 查天气
  - `mini_agent.py` — 手写 ReAct Agent 循环
  - `tools/weather.py` — 模拟天气工具（硬编码，无真实 API）
  - `_config.py` — DeepSeek client 共享配置
- 新增 `experiments/week1/README.md` — 第 1 周完整学习文档（概念 + 实验指南 + 思考题）
- 更新 `docs/learning-plan.md` — 将 checklist 项链接到 week1 教程对应章节

## Capabilities

### New Capabilities

- `week1-experiments`: 第 1 周 LLM 与 Agent 基础实验能力，包含 Python 预热、LLM 调用、提示工程、Function Calling 与手写 ReAct Agent 循环的可运行脚本及配套学习文档

### Modified Capabilities

（无 — 当前 `openspec/specs/` 为空，无既有 capability 需变更）

## Impact

- **新增文件**: `experiments/` 下约 10 个文件（代码、文档、配置）
- **修改文件**: `docs/learning-plan.md`（添加教程链接）
- **依赖**: Python 3.11+、`openai`、`pydantic`、`python-dotenv`
- **外部服务**: DeepSeek API（需用户自行配置 `DEEPSEEK_API_KEY`）
- **Out of scope**: 真实天气 API、LangGraph/LangChain、FastAPI 服务化、第 2–4 周内容
