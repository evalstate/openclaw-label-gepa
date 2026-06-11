#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Representative multilabel train/dev/test splitter.")
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output-prefix", type=Path, required=True)
    p.add_argument("--train-fraction", type=float, default=0.70)
    p.add_argument("--dev-fraction", type=float, default=0.15)
    p.add_argument("--seed", type=int, default=20260610)
    p.add_argument("--restarts", type=int, default=80)
    p.add_argument("--swap-passes", type=int, default=40)
    return p.parse_args()


def row_source(row: dict[str, Any]) -> str:
    combined = row.get("easy_set_400_combined_source")
    if isinstance(combined, str) and combined:
        return "new" if combined.startswith("new_") else "legacy"
    return "new" if row.get("easy_set_pilot_final_source") == "easy_set_400_consensus" else "v4"


def strata(row: dict[str, Any]) -> dict[str, list[str]]:
    return {
        "topic": list(row.get("expected_topics") or []),
        "item_type": [str(row.get("item_type") or "unknown")],
        "source": [row_source(row)],
        "confusion_family": list(row.get("confusion_families") or []),
        "label_count": [str(len(row.get("expected_topics") or []))],
    }


WEIGHTS = {
    "topic": 10.0,
    "item_type": 2.0,
    "source": 3.0,
    "confusion_family": 1.5,
    "label_count": 1.0,
}


def split_sizes(n: int, train_fraction: float, dev_fraction: float) -> dict[str, int]:
    train = round(n * train_fraction)
    dev = round(n * dev_fraction)
    test = n - train - dev
    return {"train": train, "dev": dev, "test": test}


def totals(rows: list[dict[str, Any]]) -> dict[str, Counter[str]]:
    out = {k: Counter() for k in WEIGHTS}
    for row in rows:
        for kind, vals in strata(row).items():
            out[kind].update(vals)
    return out


def counts_for(rows: list[dict[str, Any]]) -> dict[str, Counter[str]]:
    return totals(rows)


def objective(
    splits: dict[str, list[dict[str, Any]]],
    *,
    total: dict[str, Counter[str]],
    sizes: dict[str, int],
    n: int,
) -> float:
    score = 0.0
    for split, rows in splits.items():
        frac = sizes[split] / n
        actual = counts_for(rows)
        for kind, weight in WEIGHTS.items():
            for key, total_count in total[kind].items():
                desired = total_count * frac
                got = actual[kind][key]
                denom = max(1.0, total_count)
                score += weight * ((got - desired) ** 2) / denom
                # If a stratum is common enough to appear in every split, heavily
                # discourage zero coverage anywhere.  This is especially important
                # for topics: train should see every feasible label, and dev/test
                # should have at least one example when possible.
                if total_count >= 3 and got == 0:
                    score += weight * (8.0 if kind == "topic" else 3.0)
    return score


def initial_split(rows: list[dict[str, Any]], *, sizes: dict[str, int], seed: int) -> dict[str, list[dict[str, Any]]]:
    rng = random.Random(seed)
    ordered = rows[:]
    rng.shuffle(ordered)
    total = totals(rows)
    # Place rare/high-density rows first.
    ordered.sort(
        key=lambda r: (
            sum(1 / max(1, total["topic"][t]) for t in r.get("expected_topics", [])),
            len(r.get("expected_topics", [])),
            rng.random(),
        ),
        reverse=True,
    )
    splits = {"train": [], "dev": [], "test": []}
    for row in ordered:
        best = None
        for split in splits:
            if len(splits[split]) >= sizes[split]:
                continue
            trial = {k: v[:] for k, v in splits.items()}
            trial[split].append(row)
            # Partial objective plus fill pressure.
            filled = len(trial[split]) / max(1, sizes[split])
            score = objective(trial, total=total, sizes=sizes, n=len(rows)) - 0.01 * filled
            if best is None or score < best[0]:
                best = (score, split)
        assert best is not None
        splits[best[1]].append(row)
    return splits


def improve(
    splits: dict[str, list[dict[str, Any]]],
    *,
    total: dict[str, Counter[str]],
    sizes: dict[str, int],
    n: int,
    seed: int,
    passes: int,
) -> dict[str, list[dict[str, Any]]]:
    rng = random.Random(seed)
    best_score = objective(splits, total=total, sizes=sizes, n=n)
    names = list(splits)
    for _ in range(passes):
        improved = False
        for a in names:
            for b in names:
                if a >= b:
                    continue
                ai = list(range(len(splits[a])))
                bi = list(range(len(splits[b])))
                rng.shuffle(ai)
                rng.shuffle(bi)
                for i in ai:
                    for j in bi:
                        trial = {k: v[:] for k, v in splits.items()}
                        trial[a][i], trial[b][j] = trial[b][j], trial[a][i]
                        score = objective(trial, total=total, sizes=sizes, n=n)
                        if score + 1e-9 < best_score:
                            splits = trial
                            best_score = score
                            improved = True
                            break
                    if improved:
                        break
                if improved:
                    break
            if improved:
                break
        if not improved:
            break
    return splits


def best_split(args: argparse.Namespace, rows: list[dict[str, Any]]) -> tuple[dict[str, list[dict[str, Any]]], float]:
    sizes = split_sizes(len(rows), args.train_fraction, args.dev_fraction)
    total = totals(rows)
    best: tuple[dict[str, list[dict[str, Any]]], float] | None = None
    for r in range(args.restarts):
        splits = initial_split(rows, sizes=sizes, seed=args.seed + r * 7919)
        splits = improve(splits, total=total, sizes=sizes, n=len(rows), seed=args.seed + r * 104729, passes=args.swap_passes)
        score = objective(splits, total=total, sizes=sizes, n=len(rows))
        if best is None or score < best[1]:
            best = (splits, score)
    assert best is not None
    return best


def summarize(splits: dict[str, list[dict[str, Any]]], *, score: float, args: argparse.Namespace) -> dict[str, Any]:
    all_rows = [row for rows in splits.values() for row in rows]
    total = totals(all_rows)
    sizes = {k: len(v) for k, v in splits.items()}
    n = len(all_rows)
    by_split = {name: counts_for(rows) for name, rows in splits.items()}
    deviations: dict[str, dict[str, dict[str, float]]] = {}
    for kind in WEIGHTS:
        deviations[kind] = {}
        for key, total_count in sorted(total[kind].items()):
            deviations[kind][key] = {}
            for split in splits:
                desired = total_count * sizes[split] / n
                deviations[kind][key][split] = by_split[split][kind][key] - desired
    return {
        "input": str(args.input),
        "output_prefix": str(args.output_prefix),
        "seed": args.seed,
        "objective": score,
        "rows": n,
        "sizes": sizes,
        "fractions": {k: sizes[k] / n for k in sizes},
        "counts": {
            split: {kind: dict(sorted(counter.items())) for kind, counter in by_split[split].items()}
            for split in splits
        },
        "deviations": deviations,
        "ids": {split: [r["id"] for r in rows] for split, rows in splits.items()},
    }


def main() -> int:
    args = parse_args()
    rows = load_jsonl(args.input)
    if len({r["id"] for r in rows}) != len(rows):
        raise SystemExit("input contains duplicate ids")
    splits, score = best_split(args, rows)
    for rows_for_split in splits.values():
        rows_for_split.sort(key=lambda r: r["id"])
    write_jsonl(args.output_prefix.with_name(args.output_prefix.name + "-train.jsonl"), splits["train"])
    write_jsonl(args.output_prefix.with_name(args.output_prefix.name + "-dev.jsonl"), splits["dev"])
    write_jsonl(args.output_prefix.with_name(args.output_prefix.name + "-test.jsonl"), splits["test"])
    summary = summarize(splits, score=score, args=args)
    args.output_prefix.with_name(args.output_prefix.name + "-split-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "input": str(args.input),
        "train": len(splits["train"]),
        "dev": len(splits["dev"]),
        "test": len(splits["test"]),
        "objective": score,
        "summary": str(args.output_prefix.with_name(args.output_prefix.name + "-split-summary.json")),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
