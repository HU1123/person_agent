"""
结构化输出 — JSON mode + Pydantic 约束 LLM 输出

运行: python structured_output.py

演示:
  - 用 system prompt 要求 JSON 格式输出
  - Pydantic model_validate_json() 校验
  - CoT（思维链）提示技巧（见 COT_SYSTEM_PROMPT）

CoT 技巧: 在 prompt 中要求 LLM「先一步步思考，再给出最终 JSON」，
可提升复杂推理任务的准确率。DeepSeek 也提供 deepseek-reasoner 模型
专门做推理，本实验用 prompt 方式演示。
"""

from pydantic import BaseModel, Field

from _config import MODEL, client

COT_SYSTEM_PROMPT = """你是一个电影评论分析助手。
请按以下步骤思考，然后输出 JSON：
1. 分析评论的情感倾向（正面/负面/中性）
2. 提取关键观点
3. 给出 1-10 的评分

最终只输出 JSON，格式如下：
{"rating": <int>, "sentiment": "<str>", "summary": "<str>"}"""


class MovieReview(BaseModel):
    rating: int = Field(ge=1, le=10, description="评分 1-10")
    sentiment: str = Field(description="情感倾向: 正面/负面/中性")
    summary: str = Field(description="一句话总结")


def analyze_review(review_text: str) -> MovieReview:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": COT_SYSTEM_PROMPT},
            {"role": "user", "content": f"请分析这条评论：\n\n{review_text}"},
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
        # response_format={"type": "json_schema", "json_schema": {
        #     "name": "MovieReview",
        #     "schema": {
        #         "type": "object",
        #         "properties": {
        #             "sentiment": {"type": "string", "enum": ["正面", "负面", "中性"]},
        #             "rating": {"type": "integer", "minimum": 1, "maximum": 10},
        #             "summary": {"type": "string", "description": "一句话总结"},
        #         },
        #         "required": ["rating", "sentiment", "summary"],
        #     },
        # }}
    )

    raw_json = response.choices[0].message.content or "{}"
    print(f"  LLM 原始 JSON: {raw_json}")

    return MovieReview.model_validate_json(raw_json)


def main() -> None:
    reviews = [
        "这部电影太棒了！剧情紧凑，演员演技在线，强烈推荐！",
        "浪费时间，剧情拖沓，特效也很假，不建议观看。",
    ]

    for i, review in enumerate(reviews, 1):
        print(f"\n{'=' * 50}")
        print(f"评论 {i}: {review[:30]}...")
        print("=" * 50)

        result = analyze_review(review)
        print(f"  评分: {result.rating}/10")
        print(f"  情感: {result.sentiment}")
        print(f"  总结: {result.summary}")

    print("\n✓ structured_output 完成！")


if __name__ == "__main__":
    main()
