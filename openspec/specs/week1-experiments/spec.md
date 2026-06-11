# week1-experiments Specification

## Purpose
TBD - created by archiving change week1-learning-experiments. Update Purpose after archive.
## Requirements
### Requirement: Python 环境可一键搭建

实验目录 SHALL 提供 Python 依赖清单、环境变量模板和总览 README，使学习者能在本地 venv 中安装依赖并配置 DeepSeek API Key。

#### Scenario: 首次环境搭建

- **WHEN** 学习者克隆仓库并执行 `pip install -r requirements.txt`
- **THEN** 所有 week1 脚本所需的 Python 包（openai、pydantic、python-dotenv）被安装

#### Scenario: API Key 配置

- **WHEN** 学习者复制 `.env.example` 为 `.env` 并填入 `DEEPSEEK_API_KEY`
- **THEN** week1 脚本通过 `_config.py` 读取 Key 并成功连接 DeepSeek API

### Requirement: Python 预热实验

系统 SHALL 提供 `00_python_warmup.py`，演示类型注解、`async def`/`await` 和 Pydantic 模型校验，面向 Node.js 开发者并附带对照说明。

#### Scenario: 运行预热脚本

- **WHEN** 学习者执行 `python 00_python_warmup.py`
- **THEN** 脚本依次演示类型注解、asyncio 异步、Pydantic 校验并通过全部示例

### Requirement: LLM 基础调用实验

系统 SHALL 提供 `llm_hello.py`，演示 messages 结构（system/user/assistant）、token 用量输出和 temperature 参数效果。

#### Scenario: 首次 LLM 调用

- **WHEN** 学习者执行 `python llm_hello.py`
- **THEN** 脚本向 DeepSeek 发送对话请求并打印响应内容与 token 用量

#### Scenario: Temperature 对比

- **WHEN** 脚本以不同 temperature 值发送相同 prompt
- **THEN** 学习者能观察到输出确定性与随机性的差异

### Requirement: 结构化输出实验

系统 SHALL 提供 `structured_output.py`，使用 JSON mode 和 Pydantic 模型约束 LLM 输出为结构化数据。

#### Scenario: JSON 结构化解析

- **WHEN** 学习者执行 `python structured_output.py`
- **THEN** LLM 返回 JSON 字符串，脚本用 Pydantic `model_validate_json()` 校验并输出结构化对象

### Requirement: Function Calling 实验

系统 SHALL 提供 `function_call.py` 和 `tools/weather.py`，演示单次工具调用流程：用户提问 → LLM 返回 tool_call → 执行工具 → 结果回传 → LLM 生成最终回答。

#### Scenario: 查天气工具调用

- **WHEN** 学习者执行 `python function_call.py` 并询问某城市天气
- **THEN** LLM 调用 `get_weather` 工具，脚本执行 `weather.py` 返回模拟数据，LLM 基于结果生成自然语言回答

### Requirement: 手写 ReAct Agent 循环

系统 SHALL 提供 `mini_agent.py`，实现不依赖框架的多轮 Agent 循环，支持多次工具调用直到 LLM 给出最终答案，并设置 max_iterations 防止死循环。

#### Scenario: 多步推理与工具调用

- **WHEN** 学习者执行 `python mini_agent.py` 并提出需要多次查天气的问题（如比较两城市温度）
- **THEN** Agent 循环执行多次 tool_call，每次将 observation 追加到 messages，最终返回综合答案

#### Scenario: 循环上限保护

- **WHEN** Agent 达到 max_iterations 仍未得出最终答案
- **THEN** 脚本终止循环并输出超时提示

### Requirement: 第 1 周学习文档

系统 SHALL 在 `experiments/week1/README.md` 提供完整教程，涵盖环境搭建、LLM 基础认知、提示工程、Agent 概念，以及每个实验的运行方式、观察要点和思考题。

#### Scenario: 按文档完成学习

- **WHEN** 学习者阅读 `experiments/week1/README.md` 并按顺序运行全部实验
- **THEN** 学习者能解释 Agent 概念（LLM + Tools + Loop）并完成 `docs/learning-plan.md` 第 1 周 checklist

### Requirement: 学习计划链接闭环

`docs/learning-plan.md` 第 1 周 checklist 中的产出文件项 SHALL 链接到 `experiments/week1/README.md` 对应章节锚点。

#### Scenario: 从计划跳转到教程

- **WHEN** 学习者在 learning-plan 中点击某实验项链接
- **THEN** 浏览器/编辑器跳转到 week1 README 中该实验的指南章节

