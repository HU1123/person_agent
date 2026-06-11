"""LLM-as-judge：固定 rubric、低 temperature 打分。"""

import json
import re

from langchain_core.messages import HumanMessage, SystemMessage

from _config import get_llm

JUDGE_RUBRIC = """你是评测裁判。根据「参考答案」对「Agent 回答」打分。

评分维度（各 1-5 分）：
- accuracy（准确性）：事实是否与参考答案一致
- relevance（相关性）：是否切题、无跑题

仅输出 JSON，格式：
{"accuracy": <1-5>, "relevance": <1-5>, "reason": "<简短理由>"}
"""


def rule_baseline(answer: str, reference: str) -> dict[str, float | str]:
    """规则匹配基线：包含关键词则视为命中。"""
    keywords = [w for w in re.split(r"[，。、\s]+", reference) if len(w) >= 2]
    hits = sum(1 for kw in keywords if kw in answer)
    ratio = hits / max(len(keywords), 1)
    score = 1.0 if ratio >= 0.3 else 0.0
    return {
        "accuracy": score,
        "relevance": score,
        "method": "rule_baseline",
        "hit_ratio": round(ratio, 2),
    }


async def judge_with_llm(question: str, answer: str, reference: str) -> dict:
    llm = get_llm(temperature=0)
    prompt = (
        f"问题: {question}\n"
        f"参考答案: {reference}\n"
        f"Agent 回答: {answer}\n"
    )
    response = await llm.ainvoke(
        [SystemMessage(content=JUDGE_RUBRIC), HumanMessage(content=prompt)]
    )
    text = str(response.content)
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            data = json.loads(match.group())
            return {
                "accuracy": float(data.get("accuracy", 0)),
                "relevance": float(data.get("relevance", 0)),
                "reason": data.get("reason", ""),
                "method": "llm_judge",
            }
    except (json.JSONDecodeError, ValueError):
        pass
    return {
        "accuracy": 0.0,
        "relevance": 0.0,
        "reason": f"解析失败: {text[:100]}",
        "method": "llm_judge",
    }
