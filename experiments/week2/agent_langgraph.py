"""
LangGraph 重写第 1 周 mini_agent — 天气 ReAct 循环

运行: cd experiments/week2 && python agent_langgraph.py
"""

from typing import Annotated

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict

from _config import add_week1_to_path, get_llm
from lib.routing import should_call_tools

add_week1_to_path()
from tools.weather import get_weather as _get_weather  # noqa: E402

RECURSION_LIMIT = 5


@tool
def get_weather(city: str) -> str:
    """查询指定城市的当前天气信息，包括温度、天气状况和湿度。"""
    return _get_weather(city)


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


tools = [get_weather]
llm_with_tools = get_llm().bind_tools(tools)


def agent_node(state: AgentState) -> dict:
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


def route_after_agent(state: AgentState) -> str:
    last = state["messages"][-1]
    return "tool" if should_call_tools(last) else END


def build_graph():
    builder = StateGraph(AgentState)
    builder.add_node("agent", agent_node)
    builder.add_node("tool", ToolNode(tools))
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", route_after_agent, {"tool": "tool", END: END})
    builder.add_edge("tool", "agent")
    return builder.compile()


def run_agent(user_query: str) -> str:
    graph = build_graph()
    messages = [
        SystemMessage(
            content=(
                "你是一个天气助手。你可以查询城市天气并回答用户问题。"
                "如果需要查多个城市，请逐个调用工具。"
            )
        ),
        HumanMessage(content=user_query),
    ]
    print(f"用户: {user_query}\n")
    result = graph.invoke(
        {"messages": messages},
        config={"recursion_limit": RECURSION_LIMIT},
    )
    final = result["messages"][-1]
    answer = final.content or ""
    print(f"Final Answer: {answer}")
    return answer


def main() -> None:
    run_agent("北京和上海的天气哪个更暖？差几度？")
    print("\n✓ agent_langgraph 完成！")


if __name__ == "__main__":
    main()
