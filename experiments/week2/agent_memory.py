"""
带 RAG + 记忆的问答 Agent — LangGraph + 多轮 CLI

运行: cd experiments/week2 && python agent_memory.py
输入 quit 退出。
"""

from typing import Annotated

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict

from _config import CHROMA_DIR, MEMORY_STORE_PATH, SAMPLE_MD, get_embeddings, get_llm
from lib.history import trim_messages
from lib.memory_store import MemoryStore
from lib.rag import (
    build_rag_context,
    build_vector_store,
    load_sample_documents,
    retrieve_documents,
)
from lib.routing import should_call_tools

RECURSION_LIMIT = 8
_vector_store = None


def get_vector_store():
    global _vector_store
    if _vector_store is None:
        docs = load_sample_documents(SAMPLE_MD)
        _vector_store = build_vector_store(docs, CHROMA_DIR, get_embeddings())
    return _vector_store


def build_system_content(rag_context: str, memory_text: str) -> str:
    parts = [
        "你是学习助手，结合检索到的文档与长期记忆回答用户。",
        "需要保存用户信息时使用 remember_fact 工具。",
    ]
    if memory_text:
        parts.append(memory_text)
    if rag_context:
        parts.append(f"检索到的文档片段:\n{rag_context}")
    return "\n\n".join(parts)


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    rag_context: str


@tool
def remember_fact(key: str, value: str) -> str:
    """将用户事实写入长期记忆"""
    MemoryStore(MEMORY_STORE_PATH).save_fact(key, value)
    return f"已记住: {key} = {value}"


tools = [remember_fact]
llm_with_tools = get_llm().bind_tools(tools)


def retrieve_node(state: AgentState) -> dict:
    last_human = ""
    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage):
            last_human = str(msg.content)
            break
    hits = retrieve_documents(get_vector_store(), last_human, k=2)
    return {"rag_context": build_rag_context(hits)}


def agent_node(state: AgentState) -> dict:
    memory_text = MemoryStore(MEMORY_STORE_PATH).format_for_prompt()
    system = SystemMessage(
        content=build_system_content(state.get("rag_context", ""), memory_text)
    )
    # 除 system 外的对话历史
    dialog = [m for m in state["messages"] if not isinstance(m, SystemMessage)]
    response = llm_with_tools.invoke([system, *dialog])
    return {"messages": [response]}


def route_after_agent(state: AgentState) -> str:
    last = state["messages"][-1]
    return "tools" if should_call_tools(last) else END


def build_graph():
    builder = StateGraph(AgentState)
    builder.add_node("retrieve", retrieve_node)
    builder.add_node("agent", agent_node)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "agent")
    builder.add_conditional_edges("agent", route_after_agent, {"tools": "tools", END: END})
    builder.add_edge("tools", "agent")
    return builder.compile()


def run_turn(graph, messages: list) -> list:
    trimmed = trim_messages(messages, max_non_system=20)
    result = graph.invoke(
        {"messages": trimmed, "rag_context": ""},
        config={"recursion_limit": RECURSION_LIMIT},
    )
    return list(result["messages"])


def main() -> None:
    graph = build_graph()
    messages: list = []
    print("带 RAG + 记忆的 Agent（输入 quit 退出）\n")

    while True:
        user_input = input("你: ").strip()
        if user_input.lower() in {"quit", "exit", "q"}:
            print("再见！")
            break
        if not user_input:
            continue
        messages.append(HumanMessage(content=user_input))
        messages = run_turn(graph, messages)
        reply = messages[-1]
        print(f"助手: {reply.content}\n")

    print("\n✓ agent_memory 会话结束")


if __name__ == "__main__":
    main()
