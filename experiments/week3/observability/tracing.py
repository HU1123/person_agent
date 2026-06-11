"""Langfuse 可观测：CallbackHandler；无凭据时 no-op。"""

from langchain_core.callbacks import BaseCallbackHandler

from _config import get_langfuse_config


class NoOpCallbackHandler(BaseCallbackHandler):
    """无 Langfuse 凭据时的空实现。"""


def get_langfuse_handler() -> BaseCallbackHandler:
    """返回 Langfuse CallbackHandler；凭据缺失时返回 no-op。"""
    config = get_langfuse_config()
    if config is None:
        return NoOpCallbackHandler()

    try:
        from langfuse.callback import CallbackHandler

        return CallbackHandler(
            public_key=config["public_key"],
            secret_key=config["secret_key"],
            host=config["host"],
        )
    except Exception:
        return NoOpCallbackHandler()


def get_callbacks() -> list[BaseCallbackHandler]:
    handler = get_langfuse_handler()
    return [handler]
