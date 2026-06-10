#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "eval/openclaw/easy-set-pilot"

PRIOR_SCORE_PATHS = [
    ROOT / "runs/openclaw/validation-300-new-gemma-e4-mixed-asi-v5-plain-best/score.json",
    ROOT / "runs/openclaw/validation-300-new-deepseek4flash-mixed-asi-v5-best/score.json",
    ROOT / "runs/openclaw/validation-300-new-gpt-5.4-mini-mixed-asi-v5-best/score.json",
    ROOT / "runs/openclaw/validation-200-comprehensive-best/score.json",
    ROOT / "runs/openclaw/validation-200-gpt-5.4-mini-refctx-guidance-frontierfix-best/score.json",
]

HOSTED_PROVIDER_RE = re.compile(
    r"\b(vertex|bedrock|azure|deepinfra|near ai cloud|anthropic|google|gemini|deepinfra)\b",
    re.I,
)
LOCAL_PROVIDER_RE = re.compile(
    r"\b(llama\.cpp|ollama|lm studio|lmstudio|vllm|tgi|localai|self-host|self hosted)\b",
    re.I,
)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def prior_failure_hits(paths: list[Path]) -> dict[str, dict[str, Any]]:
    hits: dict[str, dict[str, Any]] = defaultdict(lambda: {
        "count": 0,
        "worst_count": 0,
        "false_positives": Counter(),
        "false_negatives": Counter(),
        "runs": [],
    })
    for path in paths:
        if not path.exists():
            continue
        score = json.loads(path.read_text(encoding="utf-8"))
        for key, is_worst in [("failures", False), ("worst_failures", True)]:
            for fail in score.get(key) or []:
                row_id = fail.get("id")
                if not row_id:
                    continue
                hit = hits[row_id]
                hit["count"] += 1
                hit["worst_count"] += int(is_worst)
                hit["runs"].append(str(path))
                hit["false_positives"].update(fail.get("false_positives") or [])
                hit["false_negatives"].update(fail.get("false_negatives") or [])
    out = {}
    for row_id, hit in hits.items():
        out[row_id] = {
            "count": hit["count"],
            "worst_count": hit["worst_count"],
            "false_positives": hit["false_positives"].most_common(8),
            "false_negatives": hit["false_negatives"].most_common(8),
            "runs": hit["runs"][:8],
        }
    return out


def audit_reasons(row: dict[str, Any], hits: dict[str, dict[str, Any]]) -> list[str]:
    reasons = []
    confusions = row.get("ambiguity", {}).get("possible_confusions") or []
    if len(confusions) > 1:
        reasons.append("multiple_possible_confusions")
    if not row.get("agreement_with_previous", {}).get("exact"):
        reasons.append("teacher_previous_label_disagreement")
    if row.get("agreement_with_previous", {}).get("jaccard", 1.0) < 0.80:
        reasons.append("low_previous_label_jaccard")
    if row["id"] in hits:
        hit = hits[row["id"]]
        if hit["worst_count"]:
            reasons.append("prior_benchmark_worst_failure")
        elif hit["count"] >= 2:
            reasons.append("repeated_prior_benchmark_failure")
    labels = set(row.get("gpt55_labels") or [])
    text = f"{row.get('title') or ''}\n{row.get('github_context') or ''}"[:10000]
    if "local_model_providers" in labels and HOSTED_PROVIDER_RE.search(text) and not LOCAL_PROVIDER_RE.search(text):
        reasons.append("hosted_cloud_provider_not_local_model_provider")
    return reasons


def main() -> int:
    p = argparse.ArgumentParser(description="Audit easy-set-pilot rows and build a more conservative easy split source.")
    p.add_argument("--outdir", type=Path, default=OUTDIR)
    args = p.parse_args()
    rows = load_jsonl(args.outdir / "teacher-labels.jsonl")
    strict = [r for r in rows if r.get("teacher_validation", {}).get("strict_easy") and r.get("bucket") == "easy"]
    hits = prior_failure_hits(PRIOR_SCORE_PATHS)

    audited = []
    conservative = []
    review = []
    for row in strict:
        reasons = audit_reasons(row, hits)
        enriched = {
            **row,
            "easy_set_pilot_audit": {
                "reasons": reasons,
                "prior_failure_hit": hits.get(row["id"]),
            },
        }
        if reasons:
            review.append(enriched)
        else:
            conservative.append(enriched)
        audited.append(enriched)

    write_jsonl(args.outdir / "easy-all-audited.jsonl", audited)
    write_jsonl(args.outdir / "easy-review-candidates.jsonl", review)
    write_jsonl(args.outdir / "easy-conservative.jsonl", conservative)

    summary = {
        "strict_easy_rows": len(strict),
        "conservative_easy_rows": len(conservative),
        "review_candidate_rows": len(review),
        "reason_counts": Counter(reason for row in review for reason in row["easy_set_pilot_audit"]["reasons"]),
        "review_ids": [row["id"] for row in review],
    }
    summary["reason_counts"] = dict(summary["reason_counts"])
    (args.outdir / "audit-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
