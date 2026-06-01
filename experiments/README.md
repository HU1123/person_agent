# Agent 学习实验

本目录包含 Agent 应用开发学习计划的动手实验代码，按周组织。

## 环境要求

- Python 3.11+
- DeepSeek API Key（[开放平台](https://platform.deepseek.com/) 注册）

## 快速开始

```bash
# 1. 进入实验目录
cd experiments

# 2. 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置 API Key
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY

# 5. 第 1 周
cd week1
python 00_python_warmup.py

# 6. 第 2 周（需先完成 pip install）
cd ../week2
pytest ../tests/ -v          # 单元测试，无需 API
python agent_langgraph.py
```

## 目录结构

```
experiments/
├── requirements.txt
├── .env.example
├── tests/              # week2 TDD 单元测试
├── week1/              # LLM 与 Agent 基础
└── week2/              # 框架 + RAG + 记忆
```

## 运行说明

| 周次 | 工作目录 | 说明 |
|------|----------|------|
| week1 | `experiments/week1/` | 见 [week1/README.md](week1/README.md) |
| week2 | `experiments/week2/` | 见 [week2/README.md](week2/README.md) |

- LLM 脚本加载 `experiments/.env`
- week2 首次 RAG 会下载 embedding 模型（见 week2 README）
