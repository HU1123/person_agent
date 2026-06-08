"""LangGraph 条件路由。"""

from langchain_core.messages import AIMessage, HumanMessage

from lib.routing import should_call_tools


def test_should_call_tools_true_when_tool_calls_present():
    msg = AIMessage(content="", tool_calls=[{"name": "get_weather", "args": {}, "id": "1"}])
    assert should_call_tools(msg) is True


def test_should_call_tools_false_for_plain_reply():
    msg = AIMessage(content="北京今天 15 度")
    assert should_call_tools(msg) is False


def test_should_call_tools_false_for_human_message():
    assert should_call_tools(HumanMessage(content="你好")) is False
