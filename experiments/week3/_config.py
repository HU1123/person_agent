"""第 3 周共享配置 — DeepSeek LLM、Embedding、Langfuse（可选）。"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_openai import ChatOpenAI

WEEK3_DIR = Path(__file__).resolve().parent
EXPERIMENTS_DIR = WEEK3_DIR.parent
CHROMA_DIR = WEEK3_DIR / ".chroma"
MEMORY_DIR = WEEK3_DIR / ".memory"
MEMORY_STORE_PATH = MEMORY_DIR / "store.json"
DATA_DIR = WEEK3_DIR / "data"
EMBEDDING_MODEL = "BAAI/bge-small-zh-v1.5"
CHAT_MODEL = "deepseek-chat"
CHAT_BASE_URL = "https://api.deepseek.com"

_env_path = EXPERIMENTS_DIR / ".env"
load_dotenv(_env_path)


class MissingApiKeyError(RuntimeError):
    """缺少 DEEPSEEK_API_KEY。"""


def require_api_key() -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise MissingApiKeyError(
            "错误: 未找到 DEEPSEEK_API_KEY。\n"
            "请复制 experiments/.env.example 为 experiments/.env 并填入 API Key。\n"
            "注册地址: https://platform.deepseek.com/"
        )
    return api_key


def ensure_api_key() -> str:
    try:
        return require_api_key()
    except MissingApiKeyError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)


def get_llm(*, temperature: float = 0) -> ChatOpenAI:
    return ChatOpenAI(
        model=CHAT_MODEL,
        api_key=require_api_key(),
        base_url=CHAT_BASE_URL,
        temperature=temperature,
    )


def get_embeddings() -> FastEmbedEmbeddings:
    return FastEmbedEmbeddings(model_name=EMBEDDING_MODEL)


def get_langfuse_config() -> dict | None:
    """返回 Langfuse 配置；凭据缺失时返回 None（no-op 降级）。"""
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    host = os.getenv("LANGFUSE_HOST", "http://localhost:3000")
    if not public_key or not secret_key:
        return None
    return {
        "public_key": public_key,
        "secret_key": secret_key,
        "host": host,
    }


def is_langfuse_enabled() -> bool:
    return get_langfuse_config() is not None
