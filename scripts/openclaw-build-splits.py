#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "reference/openclaw-classification-dataset/ds4.jsonl"
DEFAULT_OUT = ROOT / "eval" / "openclaw" / "splits"
DEFAULT_CONTEXT_SOURCE = ROOT / "eval/openclaw/easy-set-pilot/v6/revalidation-input.jsonl"
DEFAULT_TOPICS = ROOT / "eval/openclaw/easy-set-pilot/v6/allowed-topics-v6f.md"

CONFUSION_FAMILIES = [
    {"inference_api", "self_hosted_inference", "model_lifecycle", "agent_runtime"},
    {"coding_agent_integrations", "agent_runtime", "sessions", "acp", "acpx"},
    {"exec_tools", "tool_calling", "mcp_tooling"},
    {"notifications", "chat_integrations", "reliability"},
    {"api_surface", "config", "ui_tui"},
    {"memory", "sessions", "reliability"},
    {"inference_api", "config", "model_lifecycle"},
    {"reliability", "sessions", "agent_runtime", "gateway"},
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def truncate(text: str, max_chars: int, label: str) -> str:
    text = text or ""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"\n\n[{label} truncated after {max_chars} chars]"


def neutralize_control_tags(text: str) -> str:
    return (
        str(text or "")
        .replace("<system", "< system")
        .replace("</system", "</ system")
        .replace("<developer", "< developer")
        .replace("</developer", "</ developer")
    )


def comments_text(comments: list[dict[str, Any]]) -> str:
    parts = []
    for comment in comments:
        author = comment.get("author") or "unknown"
        created = f" at {comment.get('created_at')}" if comment.get("created_at") else ""
        parts.append(f"- {author}{created}:\n{comment.get('body') or ''}")
    return "\n\n".join(parts)


def github_context(row: dict[str, Any]) -> str:
    existing = row.get("github_context")
    if isinstance(existing, str) and existing:
        return existing
    labels = neutralize_control_tags(", ".join(row.get("labels") or []))
    changed = truncate(neutralize_control_tags(", ".join(row.get("changed_files") or [])), 2000, "changed files")
    body = truncate(neutralize_control_tags(row.get("body") or ""), 2500, "body")
    ctext = truncate(neutralize_control_tags(comments_text(row.get("comments") or [])), 1500, "comments/context")
    parts = [
        "GitHub item:",
        f"- Repository: {row.get('repo')}",
        f"- Type: {'pull_request' if row.get('item_type') == 'github_pr' else 'issue'}",
        f"- Number: {row.get('number')}",
        f"- URL: {row.get('url')}",
        f"- Title: {neutralize_control_tags(row.get('title') or '')}",
        f"- State: {row.get('state')}",
        f"- Author: {row.get('author')}",
    ]
    if labels:
        parts.append(f"- Labels: {labels}")
    if changed:
        parts.append(f"- Changed files: {changed}")
    parts.extend(["", "Body:", "```markdown", body, "```"])
    if ctext:
        parts.extend(["", "Comments/context:", "```markdown", ctext, "```"])
    return "\n".join(parts)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build OpenClaw GEPA train/validation splits.")
    p.add_argument("--source", type=Path, default=SOURCE)
    p.add_argument(
        "--context-source",
        type=Path,
        default=DEFAULT_CONTEXT_SOURCE,
        help="Optional stripped-row source used to attach target/github_context to ledger rows by id.",
    )
    p.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    p.add_argument("--train-size", type=int, default=120)
    p.add_argument("--validation-size", "--test-size", dest="validation_size", type=int, default=300)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--target-per-topic", type=int, default=4)
    p.add_argument(
        "--validation-target-per-topic",
        type=int,
        default=None,
        help=(
            "Target topic coverage count when --stratify-validation is set. "
            "Defaults to --target-per-topic."
        ),
    )
    p.add_argument("--stratified-fraction", type=float, default=0.75)
    p.add_argument("--random-train-fraction", type=float, default=0.0, help="Fill this fraction of train rows from random/natural rows after coverage selection.")
    p.add_argument("--max-dense-fraction", type=float, default=None, help="Soft cap on train rows with >=N labels.")
    p.add_argument("--dense-label-threshold", type=int, default=4, help="Label count treated as dense for --max-dense-fraction.")
    p.add_argument("--target-train-avg-labels", type=float, default=None, help="Prefer random-fill rows that move train avg label count toward this value.")
    p.add_argument("--allowed-topics", type=Path, default=DEFAULT_TOPICS)
    p.add_argument("--train-name", default=None)
    p.add_argument("--validation-name", "--test-name", dest="validation_name", default=None)
    p.add_argument("--strict-benchmark-only", action="store_true", help="Keep only rows whose quality.strict_benchmark_quality is true.")
    p.add_argument(
        "--stratify-validation",
        action="store_true",
        help="Select validation/test rows with stratified topic coverage before selecting train rows from the remainder.",
    )
    return p.parse_args()


def topic_order(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"```json\n(.*?)\n```", text, re.S)
    if not match:
        raise SystemExit(f"could not find topic JSON block in {path}")
    return list(json.loads(match.group(1)))


def priority_topics(value: Any, order: list[str]) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
        return []
    rank = {label: index for index, label in enumerate(order)}
    return sorted(value, key=lambda label: rank.get(label, len(rank)))


def row_topics(row: dict[str, Any], order: list[str]) -> list[str]:
    value = row.get("topics_of_interest")
    if value is None:
        value = row.get("expected_topics")
    if value is None:
        value = row.get("labels")
    return priority_topics(value, order)


def merge_context(row: dict[str, Any], context_by_id: dict[str, dict[str, Any]], order: list[str]) -> dict[str, Any]:
    context = context_by_id.get(row["id"], {})
    merged = dict(context)
    merged.update(row)
    if "github_context" not in merged and isinstance(context.get("github_context"), str):
        merged["github_context"] = context["github_context"]
    if "target" not in merged and isinstance(context.get("target"), str):
        merged["target"] = context["target"]
    for key in ("repo", "item_type", "number", "title"):
        if key not in merged and key in context:
            merged[key] = context[key]
    merged["topics_of_interest"] = row_topics(row, order)
    return merged


def prepared_row(row: dict[str, Any], order: list[str]) -> dict[str, Any]:
    expected = row_topics(row, order)
    target = row.get("target")
    if not isinstance(target, str) or not target:
        target = f"{row.get('repo')} {row.get('item_type')} #{row.get('number')}: {row.get('title')}"
    context = row.get("github_context")
    if not isinstance(context, str):
        context = github_context(row)
    return {
        "id": row["id"],
        "target": target,
        "github_context": context,
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
    order: list[str],
) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    shuffled = rows[:]
    rng.shuffle(shuffled)

    all_topics = sorted({t for row in rows for t in row_topics(row, order)})
    total_freq = Counter(t for row in rows for t in row_topics(row, order))
    rare_topics = {t for t, n in total_freq.items() if n <= target_per_topic}
    target = {t: min(target_per_topic, total_freq[t]) for t in all_topics}
    selected: list[dict[str, Any]] = []
    selected_ids: set[str] = set()
    counts: Counter[str] = Counter()

    stratified_slots = min(train_size, max(0, round(train_size * stratified_fraction)))

    # Seed the selection with rows that cover all very rare labels.
    for topic in sorted(rare_topics):
        candidates = [r for r in shuffled if topic in row_topics(r, order) and r["id"] not in selected_ids]
        candidates.sort(key=lambda r: (-len(row_topics(r, order)), r["id"]))
        for row in candidates[: target[topic]]:
            if len(selected) >= stratified_slots:
                break
            selected.append(row)
            selected_ids.add(row["id"])
            counts.update(row_topics(row, order))

    while len(selected) < stratified_slots:
        best: tuple[float, float, dict[str, Any]] | None = None
        for row in shuffled:
            if row["id"] in selected_ids:
                continue
            topics = set(row_topics(row, order))
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
        counts.update(row_topics(row, order))

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
    dense_label_threshold: int,
    order: list[str],
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
        order=order,
    )
    selected_ids = {r["id"] for r in selected}
    max_dense = round(train_size * max_dense_fraction) if max_dense_fraction is not None else None

    def label_count(row: dict[str, Any]) -> int:
        return len(row_topics(row, order))

    def dense_count(rs: list[dict[str, Any]]) -> int:
        return sum(1 for r in rs if label_count(r) >= dense_label_threshold)

    remaining = [r for r in rows if r["id"] not in selected_ids]
    rng.shuffle(remaining)
    while len(selected) < train_size and remaining:
        best_i = 0
        best_score: float | None = None
        for i, row in enumerate(remaining):
            lc = label_count(row)
            dense_after = dense_count(selected) + int(lc >= dense_label_threshold)
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


def topic_counts(rows: list[dict[str, Any]], order: list[str]) -> dict[str, int]:
    return dict(sorted(Counter(t for r in rows for t in row_topics(r, order)).items()))


def write_split(path: Path, rows: list[dict[str, Any]], order: list[str]) -> None:
    write_jsonl(path, [prepared_row(row, order) for row in rows])


def main() -> int:
    args = parse_args()
    order = topic_order(args.allowed_topics)
    raw_rows = load_jsonl(args.source)
    if args.strict_benchmark_only:
        raw_rows = [row for row in raw_rows if row.get("quality", {}).get("strict_benchmark_quality") is True]
    context_by_id: dict[str, dict[str, Any]] = {}
    if args.context_source and args.context_source.exists() and args.context_source != args.source:
        context_rows = load_jsonl(args.context_source)
        context_by_id = {row["id"]: row for row in context_rows if isinstance(row.get("id"), str)}
    rows = [merge_context(row, context_by_id, order) for row in raw_rows]
    rows = [row for row in rows if row_topics(row, order)]
    by_id = {r["id"]: r for r in rows}
    if len(by_id) != len(rows):
        raise SystemExit("source contains duplicate ids")
    if not rows:
        raise SystemExit("no labelled rows found in source")

    validation: list[dict[str, Any]]
    if args.stratify_validation:
        if args.validation_size > len(rows):
            raise SystemExit(f"--validation-size {args.validation_size} exceeds available rows {len(rows)}")
        validation = select_stratified(
            rows,
            train_size=args.validation_size,
            seed=args.seed + 100_000,
            target_per_topic=args.validation_target_per_topic or args.target_per_topic,
            stratified_fraction=1.0,
            order=order,
        )
        validation_ids = {r["id"] for r in validation}
        train_source = [r for r in rows if r["id"] not in validation_ids]
        if args.train_size > len(train_source):
            raise SystemExit(
                f"--train-size {args.train_size} exceeds remaining rows after stratified validation "
                f"selection ({len(train_source)})"
            )
    else:
        train_source = rows

    if args.random_train_fraction > 0:
        train = select_mixed(
            train_source,
            train_size=args.train_size,
            seed=args.seed,
            target_per_topic=args.target_per_topic,
            random_train_fraction=args.random_train_fraction,
            max_dense_fraction=args.max_dense_fraction,
            target_train_avg_labels=args.target_train_avg_labels,
            dense_label_threshold=args.dense_label_threshold,
            order=order,
        )
    else:
        train = select_stratified(
            train_source,
            train_size=args.train_size,
            seed=args.seed,
            target_per_topic=args.target_per_topic,
            stratified_fraction=args.stratified_fraction,
            order=order,
        )
    train_ids = {r["id"] for r in train}

    if not args.stratify_validation:
        rng = random.Random(args.seed + 100_000)
        eligible_validation = [r for r in rows if r["id"] not in train_ids]
        rng.shuffle(eligible_validation)
        validation = eligible_validation[: args.validation_size]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    train_name = args.train_name or f"gepa-train-stratified-{args.train_size}-seed{args.seed}.jsonl"
    validation_name = args.validation_name or f"validation-random-{args.validation_size}-seed{args.seed + 100_000}-disjoint-from-train{args.train_size}.jsonl"
    train_path = args.output_dir / train_name
    validation_path = args.output_dir / validation_name
    write_split(train_path, train, order)
    write_split(validation_path, validation, order)

    train_counts = topic_counts(train, order)
    validation_counts = topic_counts(validation, order)
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
        "validation_target_per_topic": args.validation_target_per_topic,
        "stratified_fraction": args.stratified_fraction,
        "random_train_fraction": args.random_train_fraction,
        "max_dense_fraction": args.max_dense_fraction,
        "target_train_avg_labels": args.target_train_avg_labels,
        "dense_label_threshold": args.dense_label_threshold,
        "context_source": str(args.context_source) if args.context_source else None,
        "strict_benchmark_only": args.strict_benchmark_only,
        "stratify_validation": args.stratify_validation,
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
