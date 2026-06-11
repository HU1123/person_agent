"""超时 + 指数退避重试 + 失败降级。"""

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

from tenacity import (
    AsyncRetrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

T = TypeVar("T")

FALLBACK_REPLY = "抱歉，服务暂时不可用，请稍后再试。"


async def with_retry_and_fallback(
    fn: Callable[[], Awaitable[T]],
    *,
    max_attempts: int = 3,
    fallback: T | None = None,
) -> T:
    """包裹异步调用：超时/异常时指数退避重试，耗尽后返回降级结果。"""
    fallback_value = fallback if fallback is not None else FALLBACK_REPLY  # type: ignore[assignment]

    try:
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
            retry=retry_if_exception_type((TimeoutError, asyncio.TimeoutError, OSError)),
            reraise=True,
        ):
            with attempt:
                return await fn()
    except Exception:
        return fallback_value  # type: ignore[return-value]
