"""短期记忆：裁剪会话历史。"""

from langchain_core.messages import BaseMessage, SystemMessage


def trim_messages(messages: list[BaseMessage], max_non_system: int = 20) -> list[BaseMessage]:
    """保留全部 system 消息，仅保留最近 max_non_system 条非 system 消息。"""
    system_msgs = [m for m in messages if isinstance(m, SystemMessage)]
    non_system = [m for m in messages if not isinstance(m, SystemMessage)]
    if len(non_system) <= max_non_system:
        return messages
    return system_msgs + non_system[-max_non_system:]
