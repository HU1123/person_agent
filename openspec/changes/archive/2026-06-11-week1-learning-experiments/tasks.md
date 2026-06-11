## 1. 基础设施

- [x] 1.1 创建 `experiments/requirements.txt`（openai、pydantic、python-dotenv）
- [x] 1.2 创建 `experiments/.env.example`（DEEPSEEK_API_KEY 模板）
- [x] 1.3 创建 `experiments/README.md`（venv 搭建、DeepSeek 配置、运行说明）
- [x] 1.4 创建 `experiments/week1/_config.py`（DeepSeek client + MODEL 共享配置，含 API Key 缺失友好提示）

## 2. Python 预热

- [x] 2.1 创建 `experiments/week1/00_python_warmup.py`（类型注解、asyncio、Pydantic 三个 section，含 Node.js 对照注释）

## 3. LLM 基础实验

- [x] 3.1 创建 `experiments/week1/llm_hello.py`（messages 结构、token 用量、temperature 对比）
- [x] 3.2 创建 `experiments/week1/structured_output.py`（JSON mode + Pydantic 结构化输出，含 CoT 注释示例）

## 4. Agent 雏形实验

- [x] 4.1 创建 `experiments/week1/tools/weather.py`（硬编码城市温度模拟工具）
- [x] 4.2 创建 `experiments/week1/function_call.py`（单次 Function Calling 查天气流程）
- [x] 4.3 创建 `experiments/week1/mini_agent.py`（手写 ReAct 循环，max_iterations 保护）

## 5. 学习文档

- [x] 5.1 创建 `experiments/week1/README.md`（环境搭建、LLM 认知、提示工程、Agent 概念、各实验指南、思考题、常见坑）
- [x] 5.2 更新 `docs/learning-plan.md`（第 1 周 checklist 项链接到 week1 README 锚点）

## 6. 验证

- [x] 6.1 本地安装依赖并配置 .env，依次跑通全部 week1 脚本
