#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Route v6h slim 1x/1x consensus rows into data-build tiers.")
    p.add_argument("--consensus", type=Path, required=True)
    p.add_argument("--outdir", type=Path, default=None)
    p.add_argument("--bench-min-confidence", type=float, default=0.70)
    p.add_argument("--overwrite", action="store_true")
    return p.parse_args()


def first_run(summary: dict[str, Any]) -> dict[str, Any]:
    runs = summary.get("runs")
    if isinstance(runs, list) and runs and isinstance(runs[0], dict):
        return runs[0]
    return {}


def min_confidence(row: dict[str, Any]) -> float:
    values = []
    for teacher in ("gpt", "opus"):
        value = first_run(row.get(teacher, {})).get("confidence")
        if isinstance(value, int | float):
            values.append(float(value))
    return min(values) if values else 0.0


def ambiguity_levels(row: dict[str, Any]) -> tuple[str | None, str | None]:
    return (
        first_run(row.get("gpt", {})).get("ambiguity_level"),
        first_run(row.get("opus", {})).get("ambiguity_level"),
    )


def has_failed_or_invalid(row: dict[str, Any]) -> bool:
    for teacher in ("gpt", "opus"):
        summary = row.get(teacher, {})
        if summary.get("failed_runs") or summary.get("invalid_labels") or not summary.get("complete"):
            return True
    return False


def compact(row: dict[str, Any], tier: str, reason: str) -> dict[str, Any]:
    labels = row.get("labels") or []
    if not labels and row.get("gpt_opus_exact_modal_match"):
        labels = (row.get("gpt") or {}).get("modal_labels") or []
    return {
        "id": row["id"],
        "tier": tier,
        "labels": labels,
        "title": row.get("title"),
        "target": row.get("target"),
        "github_url": row.get("github_url"),
        "reason": reason,
        "min_teacher_confidence": min_confidence(row),
        "gpt_ambiguity": ambiguity_levels(row)[0],
        "opus_ambiguity": ambiguity_levels(row)[1],
        "gpt_modal_labels": (row.get("gpt") or {}).get("modal_labels", []),
        "opus_modal_labels": (row.get("opus") or {}).get("modal_labels", []),
        "gpt_opus_modal_jaccard": row.get("gpt_opus_modal_jaccard"),
        "review_reasons": row.get("review_reasons", []),
        "any_teacher_modal_at_label_cap": row.get("any_teacher_modal_at_label_cap", False),
    }


def route(row: dict[str, Any], bench_min_confidence: float) -> tuple[str, str]:
    if has_failed_or_invalid(row):
        return "remove", "missing_failed_or_invalid_teacher_output"

    gpt_labels = (row.get("gpt") or {}).get("modal_labels") or []
    opus_labels = (row.get("opus") or {}).get("modal_labels") or []
    if not gpt_labels and not opus_labels:
        return "remove", "both_teachers_empty"

    if row.get("status") == "accepted_consensus" and not row.get("review_reasons"):
        levels = ambiguity_levels(row)
        if (
            all(level == "low" for level in levels)
            and min_confidence(row) >= bench_min_confidence
            and not row.get("any_teacher_modal_at_label_cap")
        ):
            return "bench_candidates", "exact_match_low_ambiguity_high_confidence"
        return "train_candidates", "exact_match_useful_but_not_bench_clean"

    if row.get("gpt_opus_exact_modal_match") and row.get("review_reasons"):
        return "review", "exact_match_but_teacher_review_or_hardness_flag"

    return "review", "gpt_opus_modal_disagreement"


def main() -> int:
    args = parse_args()
    outdir = args.outdir or args.consensus.parent
    outputs = {
        "bench_candidates": outdir / "bench-candidates.jsonl",
        "train_candidates": outdir / "train-candidates.jsonl",
        "review": outdir / "review.jsonl",
        "remove": outdir / "remove.jsonl",
    }
    summary_path = outdir / "slim-tier-summary.json"
    for path in [*outputs.values(), summary_path]:
        if path.exists() and not args.overwrite:
            raise SystemExit(f"{path} exists; pass --overwrite")

    tiers: dict[str, list[dict[str, Any]]] = {key: [] for key in outputs}
    reason_counts = Counter()
    label_counts = Counter()
    for row in load_jsonl(args.consensus):
        tier, reason = route(row, args.bench_min_confidence)
        tiers[tier].append(compact(row, tier, reason))
        reason_counts[reason] += 1
        for label in row.get("labels") or (row.get("gpt") or {}).get("modal_labels") or []:
            label_counts[label] += 1

    for tier, rows in tiers.items():
        write_jsonl(outputs[tier], rows)

    summary = {
        "consensus": str(args.consensus),
        "rows": sum(len(rows) for rows in tiers.values()),
        "tiers": {tier: len(rows) for tier, rows in tiers.items()},
        "reason_counts": dict(reason_counts),
        "label_counts_from_agreed_or_gpt_modal": dict(label_counts),
        "bench_min_confidence": args.bench_min_confidence,
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
