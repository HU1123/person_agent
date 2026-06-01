"""
手写 ReAct Agent — 最小 Agent 循环（不用框架）

运行: python mini_agent.py

Agent = LLM + Tools + Loop

循环:
  Thought → Action (tool_call) → Observation → ... → Final Answer

与 function_call.py 的区别: 这里会循环多次，直到 LLM 不再调用工具。
"""

import json

from _config import MODEL, client
from tools.weather import WEATHER_TOOL_SCHEMA, get_weather

MAX_ITERATIONS = 5


def execute_tool(tool_name: str, arguments: str) -> str:
    args = json.loads(arguments)
    if tool_name == "get_weather":
        return get_weather(args["city"])
    return f"未知工具: {tool_name}"


def run_agent(user_query: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个天气助手。你可以查询城市天气并回答用户问题。"
                "如果需要查多个城市，请逐个调用工具。"
            ),
        },
        {"role": "user", "content": user_query},
    ]

    print(f"用户: {user_query}\n")

    for iteration in range(1, MAX_ITERATIONS + 1):
        print(f"--- 迭代 {iteration} ---")

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=[WEATHER_TOOL_SCHEMA],
        )

        assistant_message = response.choices[0].message

        if not assistant_message.tool_calls:
            answer = assistant_message.content or ""
            print(f"Final Answer: {answer}")
            return answer

        messages.append(assistant_message)

        for tool_call in assistant_message.tool_calls:
            fn_name = tool_call.function.name
            fn_args = tool_call.function.arguments
            print(f"Action: {fn_name}({fn_args})")

            observation = execute_tool(fn_name, fn_args)
            print(f"Observation: {observation}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": observation,
                }
            )

    print(f"\n⚠ 达到最大迭代次数 ({MAX_ITERATIONS})，Agent 未能得出最终答案。")
    return ""


def main() -> None:
    run_agent("北京和上海的天气哪个更暖？差几度？")
    print("\n✓ mini_agent 完成！")


if __name__ == "__main__":
    main()
