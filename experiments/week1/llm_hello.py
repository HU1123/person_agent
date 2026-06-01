"""
LLM 基础调用 — 第一次 DeepSeek API 调用

运行: python llm_hello.py

演示:
  - messages 结构 (system / user / assistant)
  - token 用量
  - temperature 参数效果
"""

from _config import MODEL, client


def chat(messages: list[dict], temperature: float = 0.7) -> tuple[str, dict]:
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
    )
    content = response.choices[0].message.content or ""
    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    }
    return content, usage


def demo_basic_call() -> None:
    print("=" * 50)
    print("Demo 1: 基础对话 + messages 结构")
    print("=" * 50)

    messages = [
        {"role": "system", "content": "你是一个简洁的助手，回答不超过 50 字。"},
        {"role": "user", "content": "用一句话解释什么是 LLM？"},
    ]

    print("\n发送 messages:")
    for msg in messages:
        print(f"  [{msg['role']}] {msg['content']}")

    content, usage = chat(messages)
    print(f"\n回复: {content}")
    print(f"Token 用量: {usage}")


def demo_temperature() -> None:
    print("\n" + "=" * 50)
    print("Demo 2: Temperature 对比")
    print("=" * 50)

    prompt = "用一个词形容编程。"
    print(f'\nPrompt: "{prompt}"\n')

    for temp in [0.0, 1.0]:
        messages = [{"role": "user", "content": prompt}]
        content, _ = chat(messages, temperature=temp)
        print(f"  temperature={temp}: {content}")


def main() -> None:
    demo_basic_call()
    demo_temperature()
    print("\n✓ llm_hello 完成！")


if __name__ == "__main__":
    main()
