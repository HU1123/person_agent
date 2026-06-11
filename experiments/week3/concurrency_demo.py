"""asyncio.gather 并发 vs 串行对照演示。"""

import asyncio
import sys
import time
from pathlib import Path

WEEK3_DIR = Path(__file__).resolve().parent
if str(WEEK3_DIR) not in sys.path:
    sys.path.insert(0, str(WEEK3_DIR))

from app import invoke_with_pipeline

QUESTIONS = [
    "第 3 周的学习目标是什么？",
    "什么是 SSE 流式输出？",
    "令牌桶限流如何工作？",
]


async def run_serial() -> float:
    start = time.perf_counter()
    for q in QUESTIONS:
        await invoke_with_pipeline(q, session_id="serial")
    return time.perf_counter() - start


async def run_concurrent() -> float:
    start = time.perf_counter()
    await asyncio.gather(*[invoke_with_pipeline(q, session_id="concurrent") for q in QUESTIONS])
    return time.perf_counter() - start


async def main() -> None:
    print("=== 串行执行 ===")
    serial_time = await run_serial()
    print(f"串行总耗时: {serial_time:.2f}s\n")

    print("=== 并发执行 (asyncio.gather) ===")
    concurrent_time = await run_concurrent()
    print(f"并发总耗时: {concurrent_time:.2f}s\n")

    if concurrent_time < serial_time:
        speedup = serial_time / concurrent_time
        print(f"加速比: {speedup:.2f}x")
    else:
        print("提示: 若并发未加速，可能是 API 限流或网络瓶颈。")


if __name__ == "__main__":
    asyncio.run(main())
