"""短期记忆：消息历史裁剪。"""

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from lib.history import trim_messages


def test_trim_messages_keeps_system_and_recent():
    messages = [
        SystemMessage(content="你是助手"),
        HumanMessage(content="旧问题 1"),
        AIMessage(content="旧回答 1"),
        HumanMessage(content="旧问题 2"),
        AIMessage(content="旧回答 2"),
        HumanMessage(content="最新问题"),
    ]
    trimmed = trim_messages(messages, max_non_system=2)
    roles = [type(m).__name__ for m in trimmed]
    assert roles[0] == "SystemMessage"
    assert len(trimmed) == 3
    assert trimmed[-1].content == "最新问题"


def test_trim_messages_noop_when_under_limit():
    messages = [SystemMessage(content="sys"), HumanMessage(content="hi")]
    assert trim_messages(messages, max_non_system=10) == messages
