"""批量评测：调 agent + LLM judge + 规则基线 → 汇总报告。"""

import argparse
import asyncio
import json
import sys
import time
from datetime import datetime
from pathlib import Path

WEEK3_DIR = Path(__file__).resolve().parent.parent
if str(WEEK3_DIR) not in sys.path:
    sys.path.insert(0, str(WEEK3_DIR))

from app import invoke_with_pipeline
from eval.judge import judge_with_llm, rule_baseline

EVAL_DIR = Path(__file__).resolve().parent
DATASET_PATH = EVAL_DIR / "dataset.jsonl"
REPORTS_DIR = EVAL_DIR / "reports"


def load_dataset(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


async def evaluate_one(item: dict) -> dict:
    question = item["question"]
    reference = item["reference"]
    start = time.perf_counter()
    answer = await invoke_with_pipeline(question, session_id=f"eval-{item['id']}")
    latency_ms = (time.perf_counter() - start) * 1000

    llm_scores = await judge_with_llm(question, answer, reference)
    rule_scores = rule_baseline(answer, reference)

    return {
        "id": item["id"],
        "question": question,
        "reference": reference,
        "answer": answer,
        "latency_ms": round(latency_ms, 1),
        "llm_judge": llm_scores,
        "rule_baseline": rule_scores,
    }


def summarize(results: list[dict]) -> dict:
    n = len(results)
    if n == 0:
        return {}

    def avg(key: str, method: str) -> float:
        return sum(r[method][key] for r in results) / n

    return {
        "count": n,
        "avg_latency_ms": round(sum(r["latency_ms"] for r in results) / n, 1),
        "llm_avg_accuracy": round(avg("accuracy", "llm_judge"), 2),
        "llm_avg_relevance": round(avg("relevance", "llm_judge"), 2),
        "rule_avg_accuracy": round(avg("accuracy", "rule_baseline"), 2),
        "rule_avg_relevance": round(avg("relevance", "rule_baseline"), 2),
    }


async def run_eval(dataset_path: Path = DATASET_PATH) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    items = load_dataset(dataset_path)
    results: list[dict] = []
    for item in items:
        print(f"评测 {item['id']}: {item['question'][:30]}...")
        results.append(await evaluate_one(item))

    summary = summarize(results)
    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "summary": summary,
        "results": results,
    }
    out_path = REPORTS_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n=== 评测汇总 ===")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    print(f"\n报告已写入: {out_path}")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Week3 离线评测")
    parser.add_argument("--dataset", type=Path, default=DATASET_PATH)
    args = parser.parse_args()
    asyncio.run(run_eval(args.dataset))


if __name__ == "__main__":
    main()
