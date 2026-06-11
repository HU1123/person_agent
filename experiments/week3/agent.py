"""自包含 RAG + 极简记忆 Agent（async ainvoke / astream）。"""

import json
from collections import defaultdict
from collections.abc import AsyncIterator
from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.vectorstores import VectorStore

from _config import (
    CHROMA_DIR,
    DATA_DIR, 
    MEMORY_STORE_PATH,
    get_embeddings,
    get_llm,
)
from observability.tracing import get_callbacks

# --- RAG 辅助（week3 自包含，不 import week1/week2） ---


def split_markdown(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[Document]:
    if chunk_size <= chunk_overlap:
        raise ValueError("chunk_size must be greater than chunk_overlap")
    chunks: list[Document] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(Document(page_content=text[start:end]))
        if end >= len(text):
            break
        start = end - chunk_overlap
    return chunks


def load_documents(data_dir: Path) -> list[Document]:
    docs: list[Document] = []
    for path in sorted(data_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for doc in split_markdown(text):
            doc.metadata["source"] = path.name
            docs.append(doc)
    return docs


def build_vector_store(docs: list[Document], persist_directory: Path) -> VectorStore:
    persist_directory.mkdir(parents=True, exist_ok=True)
    return Chroma.from_documents(
        documents=docs,
        embedding=get_embeddings(),
        persist_directory=str(persist_directory),
    )


def retrieve_context(store: VectorStore, query: str, k: int = 3) -> str:
    hits = store.similarity_search(query, k=k)
    return "\n\n---\n\n".join(doc.page_content for doc in hits)


# --- 记忆 ---


class MemoryStore:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    def _load_raw(self) -> dict[str, str]:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save_fact(self, key: str, value: str) -> None:
        data = self._load_raw()
        data[key] = value
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def format_for_prompt(self) -> str:
        data = self._load_raw()
        if not data:
            return ""
        lines = [f"- {k}: {v}" for k, v in data.items()]
        return "已知用户长期信息:\n" + "\n".join(lines)


class SessionHistory:
    """会话内短期记忆。"""

    def __init__(self, max_turns: int = 10) -> None:
        self._sessions: dict[str, list[BaseMessage]] = defaultdict(list)
        self.max_turns = max_turns

    def get(self, session_id: str) -> list[BaseMessage]:
        return list(self._sessions[session_id])

    def append(self, session_id: str, *messages: BaseMessage) -> None:
        self._sessions[session_id].extend(messages)
        non_system = [m for m in self._sessions[session_id] if not isinstance(m, SystemMessage)]
        if len(non_system) > self.max_turns * 2:
            trimmed = non_system[-(self.max_turns * 2) :]
            self._sessions[session_id] = trimmed


# --- Agent ---


class Week3Agent:
    def __init__(self) -> None:
        self._vector_store: VectorStore | None = None
        self.memory_store = MemoryStore(MEMORY_STORE_PATH)
        self.session_history = SessionHistory()
        self.llm = get_llm()

    def get_vector_store(self) -> VectorStore:
        if self._vector_store is None:
            docs = load_documents(DATA_DIR)
            self._vector_store = build_vector_store(docs, CHROMA_DIR)
        return self._vector_store

    def _build_system_prompt(self, rag_context: str) -> str:
        parts = [
            "你是学习助手，结合检索到的文档与长期记忆回答用户。",
            "仅根据提供的文档片段作答；若文档中没有相关信息，请如实说明。",
        ]
        memory_text = self.memory_store.format_for_prompt()
        if memory_text:
            parts.append(memory_text)
        if rag_context:
            parts.append(f"检索到的文档片段:\n{rag_context}")
        return "\n\n".join(parts)

    def _build_messages(self, user_message: str, session_id: str) -> list[BaseMessage]:
        rag_context = retrieve_context(self.get_vector_store(), user_message, k=2)
        system = SystemMessage(content=self._build_system_prompt(rag_context))
        history = self.session_history.get(session_id)
        return [system, *history, HumanMessage(content=user_message)]

    async def ainvoke(self, message: str, session_id: str = "default") -> str:
        messages = self._build_messages(message, session_id)
        callbacks = get_callbacks()
        response = await self.llm.ainvoke(messages, config={"callbacks": callbacks})
        content = str(response.content)
        self.session_history.append(
            session_id,
            HumanMessage(content=message),
            AIMessage(content=content),
        )
        return content

    async def astream(self, message: str, session_id: str = "default") -> AsyncIterator[str]:
        messages = self._build_messages(message, session_id)
        callbacks = get_callbacks()
        chunks: list[str] = []
        async for chunk in self.llm.astream(messages, config={"callbacks": callbacks}):
            token = chunk.content if isinstance(chunk.content, str) else str(chunk.content)
            if token:
                chunks.append(token)
                yield token
        full = "".join(chunks)
        self.session_history.append(
            session_id,
            HumanMessage(content=message),
            AIMessage(content=full),
        )


_agent: Week3Agent | None = None


def get_agent() -> Week3Agent:
    global _agent
    if _agent is None:
        _agent = Week3Agent()
    return _agent


async def verify_rag() -> None:
    """用 data/ 中的问题验证检索与回答（CLI 入口）。"""
    agent = get_agent()
    questions = [
        "第 3 周的学习目标是什么？",
        "SSE 是用来做什么的？",
        "LLM-as-judge 评测是什么？",
    ]
    for q in questions:
        print(f"\n问: {q}")
        answer = await agent.ainvoke(q, session_id="verify")
        print(f"答: {answer}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(verify_rag())
