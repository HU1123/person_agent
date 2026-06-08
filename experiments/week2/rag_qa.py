"""
RAG 文档问答 — 切分 → 向量化 → Chroma 检索 → LLM 回答

运行: cd experiments/week2 && python rag_qa.py
"""

from langchain_core.messages import HumanMessage, SystemMessage

from _config import CHROMA_DIR, SAMPLE_MD, get_embeddings, get_llm
from lib.rag import (
    build_rag_context,
    build_vector_store,
    format_chunks_for_display,
    load_sample_documents,
    retrieve_documents,
)


def answer_with_rag(question: str, k: int = 3) -> str:
    docs = load_sample_documents(SAMPLE_MD)
    store = build_vector_store(docs, CHROMA_DIR, get_embeddings())
    hits = retrieve_documents(store, question, k=k)

    print("--- 检索到的片段 ---")
    print(format_chunks_for_display(hits))
    print()

    context = build_rag_context(hits)
    llm = get_llm()
    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    "你是文档问答助手。仅根据下列参考资料回答；"
                    "若资料中没有答案，请明确说不知道。\n\n"
                    f"参考资料:\n{context}"
                )
            ),
            HumanMessage(content=question),
        ]
    )
    return str(response.content)


def main() -> None:
    question = "第 2 周的学习产出是什么？"
    print(f"问题: {question}\n")
    answer = answer_with_rag(question)
    print(f"回答: {answer}")
    print("\n✓ rag_qa 完成！")


if __name__ == "__main__":
    main()
