"""RAG：切分、Chroma 向量库、检索与展示。"""

from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore


def split_markdown(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[Document]:
    """按字符窗口切分（教学用简化实现，避免 text_splitters 重依赖链）。"""
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


def format_chunks_for_display(docs: list[Document], preview_len: int = 80) -> str:
    lines: list[str] = []
    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "unknown")
        preview = doc.page_content.replace("\n", " ")[:preview_len]
        lines.append(f"[{i}] source={source} | {preview}...")
    return "\n".join(lines)


def build_rag_context(docs: list[Document]) -> str:
    parts = [doc.page_content for doc in docs]
    return "\n\n---\n\n".join(parts)


def build_vector_store(
    docs: list[Document],
    persist_directory: Path,
    embedding: Embeddings,
) -> VectorStore:
    persist_directory.mkdir(parents=True, exist_ok=True)
    return Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        persist_directory=str(persist_directory),
    )


def retrieve_documents(store: VectorStore, query: str, k: int = 3) -> list[Document]:
    return store.similarity_search(query, k=k)


def load_sample_documents(sample_path: Path) -> list[Document]:
    text = sample_path.read_text(encoding="utf-8")
    docs = split_markdown(text)
    for doc in docs:
        doc.metadata["source"] = sample_path.name
    return docs
