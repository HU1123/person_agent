"""RAG：切分、检索展示、向量库（FakeEmbeddings）。"""

from pathlib import Path

from langchain_core.embeddings import FakeEmbeddings
from langchain_core.documents import Document

from lib.rag import (
    build_vector_store,
    format_chunks_for_display,
    retrieve_documents,
    split_markdown,
)


def test_split_markdown_produces_multiple_chunks():
    text = "段落一。" * 200 + "\n\n" + "段落二。" * 200
    chunks = split_markdown(text, chunk_size=100, chunk_overlap=10)
    assert len(chunks) >= 2
    assert all(isinstance(c, Document) for c in chunks)


def test_format_chunks_for_display_shows_source_and_preview():
    docs = [
        Document(page_content="第 2 周产出是带 RAG 的 Agent", metadata={"source": "sample.md"}),
    ]
    output = format_chunks_for_display(docs)
    assert "sample.md" in output
    assert "RAG" in output


def test_build_and_retrieve_from_chroma(tmp_path):
    docs = [
        Document(page_content="本周产出：带 RAG + 记忆的问答 Agent", metadata={"source": "a.md"}),
        Document(page_content="无关内容：数据库索引优化", metadata={"source": "b.md"}),
    ]
    embedding = FakeEmbeddings(size=8)
    store = build_vector_store(docs, persist_directory=tmp_path / "chroma", embedding=embedding)
    query = "本周产出：带 RAG + 记忆的问答 Agent"
    hits = retrieve_documents(store, query, k=1)
    assert len(hits) == 1
    assert hits[0].metadata["source"] == "a.md"


def test_load_sample_markdown_exists():
    sample = Path(__file__).resolve().parent.parent / "week2" / "data" / "sample.md"
    assert sample.is_file()
    assert "第 2 周" in sample.read_text(encoding="utf-8")
