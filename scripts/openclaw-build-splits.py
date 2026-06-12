#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any

from openclaw_gepa.openclaw_benchmark import SOURCE, github_context, load_jsonl, write_jsonl


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "eval" / "openclaw" / "splits"

CONFUSION_FAMILIES = [
    {"model_serving", "local_model_providers", "local_models", "open_weight_models", "model_releases"},
    {"coding_agents", "agent_runtime", "sessions", "acp", "acpx"},
    {"exec_tools", "tool_calling", "mcp_tooling"},
    {"notifications", "chat_integrations", "reliability"},
    {"api_surface", "config", "ui_tui"},
    {"memory", "sessions", "reliability"},
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build OpenClaw GEPA train/validation splits.")
    p.add_argument("--source", type=Path, default=SOURCE)
    p.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    p.add_argument("--train-size", type=int, default=120)
    p.add_argument("--validation-size", type=int, default=300)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--target-per-topic", type=int, default=4)
    p.add_argument("--stratified-fraction", type=float, default=0.75)
    p.add_argument("--random-train-fraction", type=float, default=0.0, help="Fill this fraction of train rows from random/natural rows after coverage selection.")
    p.add_argument("--max-dense-fraction", type=float, default=None, help="Soft cap on train rows with >=5 labels.")
    p.add_argument("--target-train-avg-labels", type=float, default=None, help="Prefer random-fill rows that move train avg label count toward this value.")
    p.add_argument("--train-name", default=None)
    p.add_argument("--validation-name", default=None)
    return p.parse_args()


def prepared_row(row: dict[str, Any]) -> dict[str, Any]:
    expected = list(row.get("topics_of_interest") or [])
    return {
        "id": row["id"],
        "target": f"{row.get('repo')} {row.get('item_type')} #{row.get('number')}: {row.get('title')}",
        "github_context": github_context(row),
        "expected_topics": expected,
        "expected_topics_json": json.dumps(expected),
        "keywords": list(row.get("keywords") or []),
        "title": row.get("title") or "",
    }


def family_bonus(topics: set[str]) -> float:
    bonus = 0.0
    for family in CONFUSION_FAMILIES:
        if len(topics & family) >= 2:
            bonus += 0.6
    return bonus


def select_stratified(
    rows: list[dict[str, Any]],
    *,
    train_size: int,
    seed: int,
    target_per_topic: int,
    stratified_fraction: float,
) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    shuffled = rows[:]
    rng.shuffle(shuffled)

    all_topics = sorted({t for row in rows for t in row.get("topics_of_interest", [])})
    total_freq = Counter(t for row in rows for t in row.get("topics_of_interest", []))
    rare_topics = {t for t, n in total_freq.items() if n <= target_per_topic}
    target = {t: min(target_per_topic, total_freq[t]) for t in all_topics}
    selected: list[dict[str, Any]] = []
    selected_ids: set[str] = set()
    counts: Counter[str] = Counter()

    stratified_slots = min(train_size, max(0, round(train_size * stratified_fraction)))

    # Seed the selection with rows that cover all very rare labels.
    for topic in sorted(rare_topics):
        candidates = [r for r in shuffled if topic in (r.get("topics_of_interest") or []) and r["id"] not in selected_ids]
        candidates.sort(key=lambda r: (-len(r.get("topics_of_interest") or []), r["id"]))
        for row in candidates[: target[topic]]:
            if len(selected) >= stratified_slots:
                break
            selected.append(row)
            selected_ids.add(row["id"])
            counts.update(row.get("topics_of_interest") or [])

    while len(selected) < stratified_slots:
        best: tuple[float, float, dict[str, Any]] | None = None
        for row in shuffled:
            if row["id"] in selected_ids:
                continue
            topics = set(row.get("topics_of_interest") or [])
            deficits = sum(max(0, target[t] - counts[t]) for t in topics)
            if deficits <= 0 and all(counts[t] >= target[t] for t in all_topics):
                break
            density = 0.3 * min(len(topics), 4)
            sparse_bonus = 0.4 if len(topics) <= 1 else 0.0
            score = deficits + density + family_bonus(topics) + sparse_bonus + rng.random() * 0.01
            if best is None or score > best[0]:
                best = (score, rng.random(), row)
        if best is None:
            break
        row = best[2]
        selected.append(row)
        selected_ids.add(row["id"])
        counts.update(row.get("topics_of_interest") or [])

    remaining = [r for r in shuffled if r["id"] not in selected_ids]
    rng.shuffle(remaining)
    selected.extend(remaining[: max(0, train_size - len(selected))])
    return selected[:train_size]


def select_mixed(
    rows: list[dict[str, Any]],
    *,
    train_size: int,
    seed: int,
    target_per_topic: int,
    random_train_fraction: float,
    max_dense_fraction: float | None,
    target_train_avg_labels: float | None,
) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    random_slots = min(train_size, max(0, round(train_size * random_train_fraction)))
    coverage_slots = max(0, train_size - random_slots)
    selected = select_stratified(
        rows,
        train_size=coverage_slots,
        seed=seed,
        target_per_topic=target_per_topic,
        stratified_fraction=1.0,
    )
    selected_ids = {r["id"] for r in selected}
    max_dense = round(train_size * max_dense_fraction) if max_dense_fraction is not None else None

    def label_count(row: dict[str, Any]) -> int:
        return len(row.get("topics_of_interest") or [])

    def dense_count(rs: list[dict[str, Any]]) -> int:
        return sum(1 for r in rs if label_count(r) >= 5)

    remaining = [r for r in rows if r["id"] not in selected_ids]
    rng.shuffle(remaining)
    while len(selected) < train_size and remaining:
        best_i = 0
        best_score: float | None = None
        for i, row in enumerate(remaining):
            lc = label_count(row)
            dense_after = dense_count(selected) + int(lc >= 5)
            dense_penalty = 0.0
            if max_dense is not None and dense_after > max_dense:
                dense_penalty = 10.0 + (dense_after - max_dense)
            avg_penalty = 0.0
            if target_train_avg_labels is not None:
                avg_after = (sum(label_count(r) for r in selected) + lc) / (len(selected) + 1)
                avg_penalty = abs(avg_after - target_train_avg_labels)
            # Small deterministic random jitter preserves natural variation.
            score = dense_penalty + avg_penalty + rng.random() * 0.001
            if best_score is None or score < best_score:
                best_i = i
                best_score = score
        selected.append(remaining.pop(best_i))
    return selected[:train_size]


def topic_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(t for r in rows for t in r.get("topics_of_interest", [])).items()))


def write_split(path: Path, rows: list[dict[str, Any]]) -> None:
    write_jsonl(path, [prepared_row(row) for row in rows])


def main() -> int:
    args = parse_args()
    rows = load_jsonl(args.source)
    by_id = {r["id"]: r for r in rows}
    if len(by_id) != len(rows):
        raise SystemExit("source contains duplicate ids")

    if args.random_train_fraction > 0:
        train = select_mixed(
            rows,
            train_size=args.train_size,
            seed=args.seed,
            target_per_topic=args.target_per_topic,
            random_train_fraction=args.random_train_fraction,
            max_dense_fraction=args.max_dense_fraction,
            target_train_avg_labels=args.target_train_avg_labels,
        )
    else:
        train = select_stratified(
            rows,
            train_size=args.train_size,
            seed=args.seed,
            target_per_topic=args.target_per_topic,
            stratified_fraction=args.stratified_fraction,
        )
    train_ids = {r["id"] for r in train}

    rng = random.Random(args.seed + 100_000)
    eligible_validation = [r for r in rows if r["id"] not in train_ids]
    rng.shuffle(eligible_validation)
    validation = eligible_validation[: args.validation_size]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    train_name = args.train_name or f"gepa-train-stratified-{args.train_size}-seed{args.seed}.jsonl"
    validation_name = args.validation_name or f"validation-random-{args.validation_size}-seed{args.seed + 100_000}-disjoint-from-train{args.train_size}.jsonl"
    train_path = args.output_dir / train_name
    validation_path = args.output_dir / validation_name
    write_split(train_path, train)
    write_split(validation_path, validation)

    train_counts = topic_counts(train)
    validation_counts = topic_counts(validation)
    manifest = {
        "source": str(args.source),
        "train_output": str(train_path),
        "validation_output": str(validation_path),
        "source_rows": len(rows),
        "train_size": len(train),
        "validation_size": len(validation),
        "seed": args.seed,
        "validation_seed": args.seed + 100_000,
        "target_per_topic": args.target_per_topic,
        "stratified_fraction": args.stratified_fraction,
        "random_train_fraction": args.random_train_fraction,
        "max_dense_fraction": args.max_dense_fraction,
        "target_train_avg_labels": args.target_train_avg_labels,
        "overlap": len(train_ids & {r["id"] for r in validation}),
        "train_topic_counts": train_counts,
        "validation_topic_counts": validation_counts,
        "train_ids": [r["id"] for r in train],
        "validation_ids": [r["id"] for r in validation],
    }
    manifest_path = args.output_dir / f"{Path(train_name).stem}__{Path(validation_name).stem}.manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(json.dumps({
        "train": str(train_path),
        "validation": str(validation_path),
        "manifest": str(manifest_path),
        "train_rows": len(train),
        "validation_rows": len(validation),
        "overlap": manifest["overlap"],
        "train_topics": len(train_counts),
        "validation_topics": len(validation_counts),
        "train_low_counts": {k: v for k, v in train_counts.items() if v < args.target_per_topic},
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
