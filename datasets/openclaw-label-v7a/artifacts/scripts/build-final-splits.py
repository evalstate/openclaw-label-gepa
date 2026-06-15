#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_ROOT = (
    PROJECT_ROOT
    if (PROJECT_ROOT / "data").exists() and (PROJECT_ROOT / "artifacts").exists()
    else PROJECT_ROOT / "datasets/openclaw-label-v7a"
)
ARTIFACT_ROOT = DATASET_ROOT / "artifacts"
ROOT = PROJECT_ROOT
BUILD_ROOT = ROOT / "runs/data-build/final-splits"
FINAL = DATASET_ROOT / "data/final"
DEFAULT_LEDGER = FINAL / "final-ledger.jsonl"
DEFAULT_GEPA = FINAL / "final-gepa-train.jsonl"
DEFAULT_OUTPUT = BUILD_ROOT / "pilot-splits"


def parse_cardinality_targets(value: str) -> dict[int, int]:
    targets: dict[int, int] = {}
    if not value:
        return targets
    for part in value.split(","):
        key, raw = part.split(":", 1)
        targets[int(key)] = int(raw)
    return targets


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build final-data feedback/Pareto/bench splits.")
    p.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    p.add_argument("--gepa-input", type=Path, default=DEFAULT_GEPA)
    p.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--seed", type=int, default=20260613)
    p.add_argument("--bench-size", type=int, default=80)
    p.add_argument("--pareto-size", type=int, default=60)
    p.add_argument("--bench-cardinality", default="1:32,2:28,3:20")
    p.add_argument("--pareto-cardinality", default="1:18,2:24,3:18")
    p.add_argument("--bench-target-per-topic", type=int, default=1)
    p.add_argument("--pareto-target-per-topic", type=int, default=1)
    p.add_argument(
        "--reserve-feedback-labels",
        default="",
        help="Comma-separated labels to reserve into feedback before bench/Pareto selection.",
    )
    p.add_argument("--feedback-reserve-per-topic", type=int, default=1)
    p.add_argument("--prefix", default="final")
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


def labels(row: dict[str, Any]) -> list[str]:
    value = row.get("expected_topics")
    if not isinstance(value, list):
        value = row.get("labels")
    return [label for label in value or [] if isinstance(label, str)]


def ledger_labels(row: dict[str, Any]) -> list[str]:
    return [label for label in row.get("labels") or [] if isinstance(label, str)]


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = [len(labels(row)) for row in rows]
    topic_counts = Counter(topic for row in rows for topic in labels(row))
    return {
        "rows": len(rows),
        "label_instances": sum(counts),
        "avg_labels_per_row": round((sum(counts) / len(counts)) if counts else 0.0, 6),
        "cardinality_counts": dict(sorted(Counter(counts).items())),
        "labels_covered": len(topic_counts),
        "low_label_counts_lt2": dict(sorted((topic, count) for topic, count in topic_counts.items() if count < 2)),
        "low_label_counts_lt4": dict(sorted((topic, count) for topic, count in topic_counts.items() if count < 4)),
        "topic_counts": dict(sorted(topic_counts.items())),
    }


def quality_weight(row: dict[str, Any], *, bench: bool) -> float:
    quality = row.get("_quality_indicator")
    strict = bool(row.get("_strict_benchmark_quality"))
    soft = bool(row.get("_soft_disagreement"))
    if bench:
        if strict:
            return 8.0
        if quality == "five_model_consensus_train":
            return 4.0
        if quality == "slim_consensus_train":
            return 1.0
        if quality == "five_model_soft_modal_train" or soft:
            return -4.0
        return -1.0
    if quality == "five_model_consensus_train":
        return 4.0
    if quality == "slim_consensus_train":
        return 2.0
    if strict:
        return 1.5
    if quality == "five_model_soft_modal_train" or soft:
        return -1.0
    return 0.0


def choose_balanced(
    rows: list[dict[str, Any]],
    *,
    size: int,
    cardinality_targets: dict[int, int],
    target_per_topic: int,
    seed: int,
    bench: bool,
) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    selected: list[dict[str, Any]] = []
    selected_ids: set[str] = set()
    topic_counts: Counter[str] = Counter()
    card_counts: Counter[int] = Counter()
    all_topics = sorted({topic for row in rows for topic in labels(row)})

    def score(row: dict[str, Any]) -> float:
        row_labels = labels(row)
        row_topics = set(row_labels)
        card = len(row_labels)
        topic_deficit = sum(max(0, target_per_topic - topic_counts[topic]) for topic in row_topics)
        rare_coverage = sum(1.0 / (1.0 + topic_counts[topic]) for topic in row_topics)
        card_need = cardinality_targets.get(card, 0) - card_counts[card]
        card_score = 3.5 if card_need > 0 else -2.0 * abs(card_need)
        overcommon_penalty = 0.03 * sum(topic_counts[topic] for topic in row_topics)
        return (
            14.0 * topic_deficit
            + 1.5 * rare_coverage
            + card_score
            + quality_weight(row, bench=bench)
            - overcommon_penalty
            + rng.random() * 0.01
        )

    while len(selected) < size:
        remaining = [row for row in rows if row["id"] not in selected_ids]
        if not remaining:
            break
        best = max(remaining, key=score)
        selected.append(best)
        selected_ids.add(best["id"])
        topic_counts.update(labels(best))
        card_counts.update([len(labels(best))])

        # If all topic targets are met and cardinality buckets are filled, finish
        # with quality-weighted natural rows.
        if all(topic_counts[topic] >= target_per_topic for topic in all_topics) and all(
            card_counts[card] >= target for card, target in cardinality_targets.items()
        ):
            break

    while len(selected) < size:
        remaining = [row for row in rows if row["id"] not in selected_ids]
        if not remaining:
            break

        def fill_score(row: dict[str, Any]) -> float:
            card = len(labels(row))
            card_need = cardinality_targets.get(card, 0) - card_counts[card]
            return (
                (4.0 if card_need > 0 else -1.0 * abs(card_need))
                + quality_weight(row, bench=bench)
                - 0.02 * sum(topic_counts[topic] for topic in labels(row))
                + rng.random() * 0.01
            )

        best = max(remaining, key=fill_score)
        selected.append(best)
        selected_ids.add(best["id"])
        topic_counts.update(labels(best))
        card_counts.update([len(labels(best))])

    return selected[:size]


def choose_feedback_reserve(
    rows: list[dict[str, Any]],
    *,
    reserve_labels: set[str],
    target_per_topic: int,
    seed: int,
) -> list[dict[str, Any]]:
    if not reserve_labels or target_per_topic <= 0:
        return []
    rng = random.Random(seed)
    selected: list[dict[str, Any]] = []
    selected_ids: set[str] = set()
    topic_counts: Counter[str] = Counter()

    def score(row: dict[str, Any]) -> float:
        row_topics = set(labels(row))
        deficit = sum(max(0, target_per_topic - topic_counts[topic]) for topic in row_topics & reserve_labels)
        collateral = len(row_topics - reserve_labels)
        return 100.0 * deficit - 0.5 * collateral + quality_weight(row, bench=False) + rng.random() * 0.01

    while any(topic_counts[topic] < target_per_topic for topic in reserve_labels):
        candidates = [
            row
            for row in rows
            if row["id"] not in selected_ids
            and any(topic in reserve_labels and topic_counts[topic] < target_per_topic for topic in labels(row))
        ]
        if not candidates:
            missing = sorted(topic for topic in reserve_labels if topic_counts[topic] < target_per_topic)
            raise SystemExit(f"Unable to reserve feedback rows for labels: {missing}")
        best = max(candidates, key=score)
        selected.append(best)
        selected_ids.add(best["id"])
        topic_counts.update(topic for topic in labels(best) if topic in reserve_labels)
    return selected


def attach_ledger_metadata(gepa_rows: list[dict[str, Any]], ledger_by_id: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in gepa_rows:
        ledger = ledger_by_id[row["id"]]
        merged = dict(row)
        merged["_quality_indicator"] = ledger.get("quality_indicator")
        merged["_strict_benchmark_quality"] = ledger.get("strict_benchmark_quality")
        merged["_soft_disagreement"] = ledger.get("soft_disagreement")
        merged["_evidence_level"] = ledger.get("evidence_level")
        out.append(merged)
    return out


def strip_metadata(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{key: value for key, value in row.items() if not key.startswith("_")} for row in rows]


def quality_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "quality_indicator": dict(sorted(Counter(row.get("_quality_indicator") for row in rows).items())),
        "evidence_level": dict(sorted(Counter(row.get("_evidence_level") for row in rows).items())),
        "strict_benchmark_quality": dict(sorted(Counter(bool(row.get("_strict_benchmark_quality")) for row in rows).items())),
        "soft_disagreement": dict(sorted(Counter(bool(row.get("_soft_disagreement")) for row in rows).items())),
    }


def main() -> int:
    args = parse_args()
    ledger_rows = load_jsonl(args.ledger)
    gepa_rows = load_jsonl(args.gepa_input)
    ledger_by_id = {row["id"]: row for row in ledger_rows}
    missing = sorted(row["id"] for row in gepa_rows if row["id"] not in ledger_by_id)
    if missing:
        raise SystemExit(f"GEPA rows missing from ledger: {missing[:10]}")
    rows = attach_ledger_metadata(gepa_rows, ledger_by_id)
    reserve_labels = {label.strip() for label in args.reserve_feedback_labels.split(",") if label.strip()}
    feedback_reserve = choose_feedback_reserve(
        rows,
        reserve_labels=reserve_labels,
        target_per_topic=args.feedback_reserve_per_topic,
        seed=args.seed,
    )
    feedback_reserve_ids = {row["id"] for row in feedback_reserve}
    selectable_rows = [row for row in rows if row["id"] not in feedback_reserve_ids]

    bench = choose_balanced(
        selectable_rows,
        size=args.bench_size,
        cardinality_targets=parse_cardinality_targets(args.bench_cardinality),
        target_per_topic=args.bench_target_per_topic,
        seed=args.seed + 1,
        bench=True,
    )
    bench_ids = {row["id"] for row in bench}
    remaining_after_bench = [row for row in selectable_rows if row["id"] not in bench_ids]
    pareto = choose_balanced(
        remaining_after_bench,
        size=args.pareto_size,
        cardinality_targets=parse_cardinality_targets(args.pareto_cardinality),
        target_per_topic=args.pareto_target_per_topic,
        seed=args.seed + 2,
        bench=False,
    )
    pareto_ids = {row["id"] for row in pareto}
    feedback = feedback_reserve + [row for row in remaining_after_bench if row["id"] not in pareto_ids]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    feedback_path = args.output_dir / f"{args.prefix}-feedback{len(feedback)}.jsonl"
    pareto_path = args.output_dir / f"{args.prefix}-pareto{len(pareto)}.jsonl"
    bench_path = args.output_dir / f"{args.prefix}-bench{len(bench)}.jsonl"
    write_jsonl(feedback_path, strip_metadata(feedback))
    write_jsonl(pareto_path, strip_metadata(pareto))
    write_jsonl(bench_path, strip_metadata(bench))

    all_ids = {
        "feedback": {row["id"] for row in feedback},
        "pareto": {row["id"] for row in pareto},
        "bench": {row["id"] for row in bench},
    }
    manifest = {
        "dataset": str(DATASET_ROOT),
        "source_final_ledger": str(args.ledger),
        "source_gepa_input": str(args.gepa_input),
        "seed": args.seed,
        "outputs": {
            "feedback": str(feedback_path),
            "pareto": str(pareto_path),
            "bench": str(bench_path),
        },
        "hashes": {
            "feedback": sha256(feedback_path),
            "pareto": sha256(pareto_path),
            "bench": sha256(bench_path),
        },
        "requested": {
            "bench_size": args.bench_size,
            "pareto_size": args.pareto_size,
            "bench_cardinality": args.bench_cardinality,
            "pareto_cardinality": args.pareto_cardinality,
            "bench_target_per_topic": args.bench_target_per_topic,
            "pareto_target_per_topic": args.pareto_target_per_topic,
        },
        "overlaps": {
            "feedback_pareto": len(all_ids["feedback"] & all_ids["pareto"]),
            "feedback_bench": len(all_ids["feedback"] & all_ids["bench"]),
            "pareto_bench": len(all_ids["pareto"] & all_ids["bench"]),
        },
        "feedback_reserve": {
            "labels": sorted(reserve_labels),
            "target_per_topic": args.feedback_reserve_per_topic,
            "rows": [row["id"] for row in feedback_reserve],
        },
        "feedback": summarize(feedback),
        "pareto": summarize(pareto),
        "bench": summarize(bench),
        "quality": {
            "feedback": quality_summary(feedback),
            "pareto": quality_summary(pareto),
            "bench": quality_summary(bench),
        },
        "ids": {
            "feedback": [row["id"] for row in feedback],
            "pareto": [row["id"] for row in pareto],
            "bench": [row["id"] for row in bench],
        },
    }
    manifest_path = args.output_dir / f"{feedback_path.stem}__{pareto_path.stem}__{bench_path.stem}.manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: manifest[key] for key in ("outputs", "hashes", "overlaps", "feedback", "pareto", "bench", "quality")}, indent=2))
    print(f"manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
