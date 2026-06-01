"""DeepSeek 共享配置 — week1 实验脚本统一从此模块导入 client 和 MODEL。"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# 加载 experiments/.env（week1 脚本在 week1/ 目录下运行）
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_path)

MODEL = "deepseek-chat"

_api_key = os.getenv("DEEPSEEK_API_KEY")
if not _api_key:
    print(
        "错误: 未找到 DEEPSEEK_API_KEY。\n"
        "请复制 experiments/.env.example 为 experiments/.env 并填入 API Key。\n"
        "注册地址: https://platform.deepseek.com/",
        file=sys.stderr,
    )
    sys.exit(1)

client = OpenAI(
    api_key=_api_key,
    base_url="https://api.deepseek.com",
)
