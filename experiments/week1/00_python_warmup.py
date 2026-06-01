"""
Python 预热 — 面向 Node.js 开发者的快速对照实验

运行: python 00_python_warmup.py

本节不涉及 LLM，纯 Python 语法预热。
"""

import asyncio
from typing import Optional

from pydantic import BaseModel, ValidationError


# ── Section 1: 类型注解 ──────────────────────────────────────
# Node.js 对照: TypeScript 的 function greet(name: string): string


def greet(name: str) -> str:
    return f"Hello, {name}!"


def find_user(user_id: int) -> Optional[dict]:
    """Optional[T] 等价于 TypeScript 的 T | null | undefined"""
    users = {1: {"name": "Alice"}, 2: {"name": "Bob"}}
    return users.get(user_id)


# ── Section 2: asyncio 异步 ───────────────────────────────────
# Node.js 对照: async function delay(ms) { await sleep(ms) }


async def fetch_data(delay: float) -> str:
    await asyncio.sleep(delay)
    return f"data after {delay}s"


async def run_async_demo() -> None:
    print("  并发执行两个异步任务...")
    results = await asyncio.gather(
        fetch_data(0.1),
        fetch_data(0.2),
    )
    for r in results:
        print(f"  → {r}")


# ── Section 3: Pydantic 模型校验 ─────────────────────────────
# Node.js 对照: class-validator + DTO class


class User(BaseModel):
    name: str
    age: int
    email: Optional[str] = None


def run_pydantic_demo() -> None:
    # 正常校验
    user = User(name="Alice", age=25, email="alice@example.com")
    print(f"  合法用户: {user.model_dump()}")

    # 类型自动转换（"25" → 25）
    user2 = User(name="Bob", age="30")
    print(f"  自动转换: age={user2.age} (type={type(user2.age).__name__})")

    # 校验失败
    try:
        User(name="Charlie", age="not-a-number")
    except ValidationError as e:
        print(f"  校验失败（预期）: {e.error_count()} 个错误")


# ── Main ──────────────────────────────────────────────────────


def main() -> None:
    print("=" * 50)
    print("Section 1: 类型注解")
    print("=" * 50)
    print(f"  {greet('World')}")
    print(f"  find_user(1) = {find_user(1)}")
    print(f"  find_user(99) = {find_user(99)}")

    print("\n" + "=" * 50)
    print("Section 2: asyncio 异步")
    print("=" * 50)
    asyncio.run(run_async_demo())

    print("\n" + "=" * 50)
    print("Section 3: Pydantic 模型校验")
    print("=" * 50)
    run_pydantic_demo()

    print("\n✓ Python 预热完成！可以继续 llm_hello.py")


if __name__ == "__main__":
    main()
