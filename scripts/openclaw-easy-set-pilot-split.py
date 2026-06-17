#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "eval/openclaw/easy-set-pilot"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Create deterministic easy-set-pilot train/test splits.")
    p.add_argument("--input", type=Path, default=DEFAULT_OUTDIR / "easy-all.jsonl")
    p.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    p.add_argument("--prefix", default="easy", help="Output filename prefix, e.g. easy-final-v2.")
    p.add_argument("--seed", type=int, default=55)
    p.add_argument("--test-size", type=int, default=None)
    p.add_argument("--train-size", type=int, default=None)
    return p.parse_args()


def split_sizes(n: int, requested_test: int | None, requested_train: int | None) -> tuple[int, int]:
    if requested_test is not None:
        test = min(requested_test, n)
    elif n >= 100:
        test = 40
    elif n >= 80:
        test = 30
    elif n >= 60:
        test = 20
    elif n >= 50:
        test = 20
    else:
        test = max(0, min(20, n // 3))
    train_avail = max(0, n - test)
    if requested_train is not None:
        train = min(requested_train, train_avail)
    elif n >= 100:
        train = min(80, train_avail)
    elif n >= 80:
        train = min(60, train_avail)
    elif n >= 60:
        train = min(40, train_avail)
    else:
        train = train_avail
    return train, test


def stable_key(row: dict[str, Any], seed: int) -> str:
    return hashlib.sha256(f"{seed}:{row['id']}".encode()).hexdigest()


def main() -> int:
    args = parse_args()
    rows = load_jsonl(args.input)
    rows = sorted(rows, key=lambda r: stable_key(r, args.seed))
    train_n, test_n = split_sizes(len(rows), args.test_size, args.train_size)
    test = rows[:test_n]
    train = rows[test_n:test_n + train_n]
    unused = rows[test_n + train_n:]

    write_jsonl(args.outdir / f"{args.prefix}-train.jsonl", train)
    write_jsonl(args.outdir / f"{args.prefix}-test.jsonl", test)
    if unused:
        write_jsonl(args.outdir / f"{args.prefix}-unused.jsonl", unused)

    label_counts = Counter(label for row in rows for label in row.get("gpt55_labels", []))
    summary = {
        "input": str(args.input),
        "seed": args.seed,
        "easy_rows": len(rows),
        "easy_train": len(train),
        "easy_test": len(test),
        "easy_unused": len(unused),
        "top_labels": label_counts.most_common(20),
        "train_ids": [r["id"] for r in train],
        "test_ids": [r["id"] for r in test],
    }
    (args.outdir / f"{args.prefix}-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ["easy_rows", "easy_train", "easy_test", "easy_unused", "top_labels"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
