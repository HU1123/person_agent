"""FastAPI Agent 服务：GET /health + POST /chat（SSE 流式）。"""

import json
from collections.abc import AsyncIterator

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from agent import get_agent
from observability.tracing import get_callbacks
from resilience.cache import ResponseCache
from resilience.rate_limit import RateLimitExceeded, TokenBucket
from resilience.retry import with_retry_and_fallback
from security.guard import guard_input
from _config import MissingApiKeyError

app = FastAPI(title="Week3 Agent Service", version="0.1.0")

rate_limiter = TokenBucket(capacity=10, refill_rate=2.0)
response_cache = ResponseCache()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: str = "default"


class HealthResponse(BaseModel):
    status: str = "ok"


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse()


def _sse_event(data: str) -> str:
    return f"data: {json.dumps({'token': data}, ensure_ascii=False)}\n\n"


def _sse_done() -> str:
    return "data: [DONE]\n\n"


async def _stream_agent(message: str, session_id: str) -> AsyncIterator[str]:
    agent = get_agent()
    async for token in agent.astream(message, session_id=session_id):
        yield _sse_event(token)
    yield _sse_done()


@app.post("/chat")
async def chat(req: ChatRequest) -> StreamingResponse:
    # ① security guard
    guard = guard_input(req.message)
    if not guard.allowed:
        raise HTTPException(status_code=400, detail=guard.message)

    message = guard.message

    # ② rate limit
    try:
        rate_limiter.acquire_or_raise()
    except RateLimitExceeded as exc:
        raise HTTPException(status_code=429, detail=str(exc)) from exc

    # ③ cache hit → 直接 SSE 返回
    cached = response_cache.get(message, req.session_id)
    if cached is not None:

        async def cached_stream() -> AsyncIterator[str]:
            yield _sse_event(cached)
            yield _sse_done()

        return StreamingResponse(cached_stream(), media_type="text/event-stream")

    # ④ retry wraps agent stream; ⑤ agent; ⑥ langfuse via callbacks in agent
    collected: list[str] = []

    async def collect_stream() -> AsyncIterator[str]:
        agent = get_agent()

        async def _run_stream():
            nonlocal collected
            async for token in agent.astream(message, session_id=req.session_id):
                collected.append(token)
                yield token

        async for token in _run_stream():
            yield _sse_event(token)
        yield _sse_done()

    async def safe_stream() -> AsyncIterator[str]:
        try:
            async for chunk in collect_stream():
                yield chunk
        except MissingApiKeyError as exc:
            yield _sse_event(str(exc).split("\n")[0])
            yield _sse_done()
        except Exception:
            fallback = "抱歉，服务暂时不可用，请稍后再试。"
            response_cache.set(message, fallback, req.session_id)
            yield _sse_event(fallback)
            yield _sse_done()
            return

        if collected:
            response_cache.set(message, "".join(collected), req.session_id)

    # Wrap with retry for non-streaming fallback path
    _ = get_callbacks()  # ensure handler init

    return StreamingResponse(safe_stream(), media_type="text/event-stream")


async def invoke_with_pipeline(message: str, session_id: str = "default") -> str:
    """非 SSE 调用链（供 eval / 并发 demo 使用）。"""
    guard = guard_input(message)
    if not guard.allowed:
        return guard.message

    message = guard.message
    if not rate_limiter.try_acquire():
        return "请求过于频繁，请稍后再试。"

    cached = response_cache.get(message, session_id)
    if cached is not None:
        return cached

    agent = get_agent()

    async def _call():
        return await agent.ainvoke(message, session_id=session_id)

    try:
        result = await with_retry_and_fallback(_call)
    except MissingApiKeyError as exc:
        return str(exc).split("\n")[0]
    if isinstance(result, str):
        response_cache.set(message, result, session_id)
    return str(result)
