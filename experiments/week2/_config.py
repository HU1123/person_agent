"""第 2 周共享配置 — DeepSeek LLM、Embedding、路径常量。"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_openai import ChatOpenAI

WEEK2_DIR = Path(__file__).resolve().parent
EXPERIMENTS_DIR = WEEK2_DIR.parent
WEEK1_DIR = EXPERIMENTS_DIR / "week1"
CHROMA_DIR = WEEK2_DIR / ".chroma"
MEMORY_DIR = WEEK2_DIR / ".memory"
MEMORY_STORE_PATH = MEMORY_DIR / "store.json"
SAMPLE_MD = WEEK2_DIR / "data" / "sample.md"
EMBEDDING_MODEL = "BAAI/bge-small-zh-v1.5"
CHAT_MODEL = "deepseek-chat"
CHAT_BASE_URL = "https://api.deepseek.com"

_env_path = EXPERIMENTS_DIR / ".env"
load_dotenv(_env_path)


def ensure_api_key() -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print(
            "错误: 未找到 DEEPSEEK_API_KEY。\n"
            "请复制 experiments/.env.example 为 experiments/.env 并填入 API Key。\n"
            "注册地址: https://platform.deepseek.com/",
            file=sys.stderr,
        )
        sys.exit(1)
    return api_key


def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=CHAT_MODEL,
        api_key=ensure_api_key(),
        base_url=CHAT_BASE_URL,
        temperature=0,
    )


def get_embeddings() -> FastEmbedEmbeddings:
    return FastEmbedEmbeddings(model_name=EMBEDDING_MODEL)


def add_week1_to_path() -> None:
    week1 = str(WEEK1_DIR)
    if week1 not in sys.path:
        sys.path.insert(0, week1)
