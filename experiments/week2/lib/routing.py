"""LangGraph 条件边辅助。"""

from langchain_core.messages import BaseMessage


def should_call_tools(message: BaseMessage) -> bool:
    tool_calls = getattr(message, "tool_calls", None)
    return bool(tool_calls)
