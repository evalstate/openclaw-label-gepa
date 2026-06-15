#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DATA = ROOT / "datasets/openclaw-label-v7a/data"
SPLITS = SOURCE_DATA / "splits"
DEFAULT_SOURCE = SOURCE_DATA / "final/final-gepa-train.jsonl"
DEFAULT_PARETO = SPLITS / "pareto60.jsonl"
DEFAULT_BENCH = SPLITS / "bench78.jsonl"
DEFAULT_OUTPUT = ROOT / "runs/data-build/splits/v6n-final-feedback300.jsonl"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build a 300-row GEPA feedback split.")
    p.add_argument("--regime", default="v6n")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--pareto", type=Path, default=DEFAULT_PARETO)
    p.add_argument("--bench", type=Path, default=DEFAULT_BENCH)
    p.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--size", type=int, default=300)
    return p.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def row_id(row: dict[str, Any]) -> str:
    inp = row.get("input") if isinstance(row.get("input"), dict) else row
    value = inp.get("id") or row.get("id")
    if not isinstance(value, str):
        raise ValueError(f"Row has no string id: {row}")
    return value


def row_labels(row: dict[str, Any]) -> list[str]:
    inp = row.get("input") if isinstance(row.get("input"), dict) else row
    value = inp.get("expected_topics") or inp.get("labels") or row.get("expected_topics") or row.get("labels") or []
    return [label for label in value if isinstance(label, str)]


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    cards = [len(row_labels(row)) for row in rows]
    topics = Counter(topic for row in rows for topic in row_labels(row))
    return {
        "rows": len(rows),
        "label_instances": sum(cards),
        "avg_labels_per_row": round(sum(cards) / len(cards), 6) if cards else 0.0,
        "cardinality_counts": dict(sorted(Counter(cards).items())),
        "labels_covered": len(topics),
        "low_label_counts_lt4": dict(sorted((topic, count) for topic, count in topics.items() if count < 4)),
        "topic_counts": dict(sorted(topics.items())),
    }


def choose_drop_rows(rows: list[dict[str, Any]], *, target_size: int) -> list[dict[str, Any]]:
    if len(rows) <= target_size:
        return []
    topic_counts = Counter(topic for row in rows for topic in row_labels(row))

    def drop_rank(row: dict[str, Any]) -> tuple[int, int, int, str]:
        labels = row_labels(row)
        # Drop rows whose labels are most over-represented. Prefer single-label
        # rows when ties occur, so rare multi-label boundary examples stay in feedback.
        min_topic_count = min((topic_counts[label] for label in labels), default=999)
        sum_topic_count = sum(topic_counts[label] for label in labels)
        return (min_topic_count, sum_topic_count, -len(labels), row_id(row))

    return sorted(rows, key=drop_rank, reverse=True)[: len(rows) - target_size]


def main() -> int:
    args = parse_args()
    source_rows = load_jsonl(args.source)
    pareto_rows = load_jsonl(args.pareto)
    bench_rows = load_jsonl(args.bench)
    heldout_ids = {row_id(row) for row in pareto_rows} | {row_id(row) for row in bench_rows}
    candidates = [row for row in source_rows if row_id(row) not in heldout_ids]
    if len(candidates) < args.size:
        raise SystemExit(
            f"Only {len(candidates)} rows remain after excluding Pareto/bench IDs; "
            f"cannot build feedback size {args.size}."
        )

    dropped = choose_drop_rows(candidates, target_size=args.size)
    dropped_ids = {row_id(row) for row in dropped}
    feedback = [row for row in candidates if row_id(row) not in dropped_ids]
    if len(feedback) != args.size:
        raise SystemExit(f"Internal split error: expected {args.size} feedback rows, got {len(feedback)}")

    feedback_ids = {row_id(row) for row in feedback}
    overlaps = {
        "feedback_pareto": len(feedback_ids & {row_id(row) for row in pareto_rows}),
        "feedback_bench": len(feedback_ids & {row_id(row) for row in bench_rows}),
        "pareto_bench": len({row_id(row) for row in pareto_rows} & {row_id(row) for row in bench_rows}),
    }
    if overlaps["feedback_pareto"] or overlaps["feedback_bench"] or overlaps["pareto_bench"]:
        raise SystemExit(f"Split overlap detected: {overlaps}")

    write_jsonl(args.output, feedback)
    manifest_path = args.output.with_name(
        f"{args.output.stem}__{args.pareto.stem}__{args.bench.stem}.manifest.json"
    )
    manifest = {
        "regime": args.regime,
        "source": str(args.source),
        "source_rows": len(source_rows),
        "excluded": {
            "pareto": str(args.pareto),
            "bench": str(args.bench),
            "heldout_ids": len(heldout_ids),
        },
        "candidate_rows_after_exclusion": len(candidates),
        "requested_feedback_rows": args.size,
        "outputs": {
            "feedback": str(args.output),
            "pareto": str(args.pareto),
            "bench": str(args.bench),
        },
        "hashes": {
            "feedback": sha256(args.output),
            "pareto": sha256(args.pareto),
            "bench": sha256(args.bench),
        },
        "overlaps": overlaps,
        "dropped_rows": [{"id": row_id(row), "labels": row_labels(row)} for row in dropped],
        "feedback": summarize(feedback),
        "pareto": summarize(pareto_rows),
        "bench": summarize(bench_rows),
        "ids": {
            "feedback": [row_id(row) for row in feedback],
            "pareto": [row_id(row) for row in pareto_rows],
            "bench": [row_id(row) for row in bench_rows],
        },
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: manifest[key] for key in ("outputs", "hashes", "overlaps", "feedback")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
