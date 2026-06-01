"""
Function Calling — 单次工具调用流程

运行: python function_call.py

流程:
  用户提问 → LLM 返回 tool_call → 执行工具 → 结果回传 → LLM 生成最终回答

注意: 这里没有 Agent 循环，只是一次工具调用。
"""

import json

from _config import MODEL, client
from tools.weather import WEATHER_TOOL_SCHEMA, get_weather


def run_function_call(user_query: str) -> None:
    messages = [
        {"role": "system", "content": "你是一个天气助手，可以查询城市天气。"},
        {"role": "user", "content": user_query},
    ]

    print(f"用户: {user_query}\n")

    # Step 1: LLM 决定是否调用工具
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=[WEATHER_TOOL_SCHEMA],
    )

    assistant_message = response.choices[0].message
    print(f"LLM 回复类型: {'tool_call' if assistant_message.tool_calls else 'text'}")

    if not assistant_message.tool_calls:
        print(f"直接回答: {assistant_message.content}")
        return

    # Step 2: 执行工具
    messages.append(assistant_message)

    for tool_call in assistant_message.tool_calls:
        args = json.loads(tool_call.function.arguments)
        city = args["city"]
        print(f"工具调用: get_weather(city={city!r})")

        result = get_weather(city)
        print(f"工具结果: {result}")

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
        )

    # Step 3: 把工具结果回传，让 LLM 生成最终回答
    final_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=[WEATHER_TOOL_SCHEMA],
    )

    final_answer = final_response.choices[0].message.content
    print(f"\n最终回答: {final_answer}")


def main() -> None:
    run_function_call("北京今天天气怎么样？")
    print("\n✓ function_call 完成！")


if __name__ == "__main__":
    main()
