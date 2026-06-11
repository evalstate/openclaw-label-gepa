#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any

from openclaw_gepa.openclaw_benchmark import github_context, write_jsonl

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "eval/openclaw/easy-set-pilot"

CONFUSION_FAMILIES = [
    {"model_serving", "local_model_providers", "local_models", "open_weight_models", "model_releases"},
    {"coding_agents", "agent_runtime", "sessions", "acp", "acpx"},
    {"exec_tools", "tool_calling", "mcp_tooling"},
    {"notifications", "chat_integrations", "reliability"},
    {"api_surface", "config", "ui_tui"},
    {"memory", "sessions", "reliability"},
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ids_in(paths: list[Path]) -> set[str]:
    return {row["id"] for path in paths for row in load_jsonl(path) if isinstance(row.get("id"), str)}


def jaccard(a: set[str], b: set[str]) -> float:
    return 1.0 if not a and not b else len(a & b) / len(a | b)


def inferred_confusion_families(labels: list[str]) -> list[str]:
    topics = set(labels)
    out = []
    for family in CONFUSION_FAMILIES:
        hit = sorted(topics & family)
        if len(hit) >= 2:
            out.append("+".join(hit))
    return out


def target(row: dict[str, Any]) -> str:
    kind = "github_pr" if row.get("item_type") == "github_pr" else "github_issue"
    return f"{row.get('repo')} {kind} #{row.get('number')}: {row.get('title')}"


def prepared_candidate(row: dict[str, Any], *, source: Path) -> dict[str, Any]:
    legacy = list(row.get("topics_of_interest") or [])
    return {
        "id": row["id"],
        "target": target(row),
        "github_context": github_context(row),
        # Legacy ds4 labels are shown to the teacher for comparison only by the
        # v4 clean template.  Consensus labels replace these during finalization.
        "expected_topics": legacy,
        "expected_topics_json": json.dumps(legacy),
        "legacy_expected_topics": legacy,
        "ds4_topics": legacy,
        "ds4_description": row.get("description") or "",
        "ds4_caveats": list(row.get("caveats") or []),
        "repo": row.get("repo"),
        "item_type": row.get("item_type"),
        "number": row.get("number"),
        "url": row.get("url"),
        "title": row.get("title") or "",
        "state": row.get("state"),
        "source_path": str(source),
        "easy_set_400_candidate_source": "ds4_stratified_sample",
        "confusion_families": inferred_confusion_families(legacy),
    }


def select_stratified(rows: list[dict[str, Any]], *, limit: int, seed: int) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    shuffled = rows[:]
    rng.shuffle(shuffled)

    all_topics = sorted({t for row in rows for t in row.get("topics_of_interest", [])})
    total = Counter(t for row in rows for t in row.get("topics_of_interest", []))
    # Target a representative sample, but force a small floor for rare topics.
    target_counts = {
        t: min(total[t], max(2, round(total[t] * min(1.0, limit / max(1, len(rows))))))
        for t in all_topics
    }
    selected: list[dict[str, Any]] = []
    selected_ids: set[str] = set()
    counts: Counter[str] = Counter()

    rare_topics = [t for t, n in sorted(total.items(), key=lambda kv: (kv[1], kv[0])) if n <= 5]
    for topic in rare_topics:
        candidates = [r for r in shuffled if topic in (r.get("topics_of_interest") or []) and r["id"] not in selected_ids]
        candidates.sort(key=lambda r: (-len(r.get("topics_of_interest") or []), r["id"]))
        for row in candidates[: target_counts[topic]]:
            if len(selected) >= limit:
                break
            selected.append(row)
            selected_ids.add(row["id"])
            counts.update(row.get("topics_of_interest") or [])

    while len(selected) < limit:
        best: tuple[float, str, dict[str, Any]] | None = None
        for row in shuffled:
            if row["id"] in selected_ids:
                continue
            topics = set(row.get("topics_of_interest") or [])
            deficits = sum(max(0, target_counts[t] - counts[t]) for t in topics)
            # Keep some boundary-rich rows in the labeling pool; final consensus
            # decides whether they are easy, medium, or review material.
            boundary_bonus = 0.6 * len(inferred_confusion_families(list(topics)))
            density_bonus = 0.2 * min(len(topics), 4)
            issue_bonus = 0.15 if row.get("item_type") == "github_issue" else 0.0
            score = deficits + boundary_bonus + density_bonus + issue_bonus + rng.random() * 0.001
            if best is None or score > best[0]:
                best = (score, row["id"], row)
        if best is None:
            break
        row = best[2]
        selected.append(row)
        selected_ids.add(row["id"])
        counts.update(row.get("topics_of_interest") or [])

    return sorted(selected[:limit], key=lambda r: r["id"])


def cmd_prepare_sample(args: argparse.Namespace) -> int:
    excluded = ids_in(args.exclude)
    source_rows = load_jsonl(args.source)
    candidates = [r for r in source_rows if r.get("id") not in excluded]
    if args.require_legacy_labels:
        candidates = [r for r in candidates if r.get("topics_of_interest")]
    selected = select_stratified(candidates, limit=args.sample_size, seed=args.seed)
    prepared = [prepared_candidate(row, source=args.source) for row in selected]

    write_jsonl(args.output, prepared)
    topic_counts = Counter(t for r in prepared for t in r.get("legacy_expected_topics", []))
    manifest = {
        "source": str(args.source),
        "output": str(args.output),
        "sample_size": len(prepared),
        "seed": args.seed,
        "source_rows": len(source_rows),
        "excluded_rows": len(excluded),
        "candidate_rows": len(candidates),
        "require_legacy_labels": args.require_legacy_labels,
        "exclude_files": [str(p) for p in args.exclude],
        "topic_counts": dict(sorted(topic_counts.items())),
        "item_type_counts": dict(Counter(r.get("item_type") for r in prepared)),
        "confusion_family_rows": sum(bool(r.get("confusion_families")) for r in prepared),
        "confusion_family_counts": dict(Counter(f for r in prepared for f in r.get("confusion_families", []))),
        "selected_ids": [r["id"] for r in prepared],
    }
    args.output.with_suffix(".manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


def consensus_votes(row: dict[str, Any]) -> dict[str, Any]:
    votes = row.get("teacher_votes") if isinstance(row.get("teacher_votes"), dict) else {}
    label_sets = {
        name: {
            "labels": vote.get("labels") or [],
            "bucket": vote.get("bucket"),
            "confidence": vote.get("confidence"),
            "strict_easy": vote.get("strict_easy"),
            "possible_confusions": (vote.get("ambiguity") or {}).get("possible_confusions", []),
        }
        for name, vote in votes.items()
        if isinstance(vote, dict)
    }
    confidences = [v.get("confidence") for v in label_sets.values() if isinstance(v.get("confidence"), int | float)]
    return {
        "stable": bool(row.get("consensus_bucket") == "easy"),
        "runs": {name: value["labels"] for name, value in label_sets.items()},
        "details": label_sets,
        "min_confidence": min(confidences) if confidences else None,
    }


def finalized_new_easy(row: dict[str, Any]) -> dict[str, Any]:
    labels = list(row.get("expected_topics") or row.get("consensus_labels") or [])
    legacy = list(row.get("legacy_expected_topics") or row.get("ds4_topics") or [])
    out = {
        **row,
        "expected_topics": labels,
        "expected_topics_json": json.dumps(labels),
        "topics_of_interest": labels,
        "previous_expected_topics": legacy,
        "teacher_topics": labels,
        "gpt55_labels": labels,
        "bucket": "easy",
        "teacher_source": "gpt55x2_opus_consensus_easy_set_400",
        "teacher_stability": consensus_votes(row),
        "agreement_with_previous": {
            "exact": set(legacy) == set(labels),
            "jaccard": jaccard(set(legacy), set(labels)),
            "false_positives_vs_previous": sorted(set(labels) - set(legacy)),
            "false_negatives_vs_previous": sorted(set(legacy) - set(labels)),
        },
        "teacher_validation": {
            "invalid_labels": [],
            "strict_easy": True,
            "relaxed_easy": True,
            "consensus_easy": True,
        },
        "easy_set_pilot_final_source": "easy_set_400_consensus",
        "easy_set_pilot_label_version": "easy-set-400",
        "confusion_families": inferred_confusion_families(labels),
    }
    out.pop("teacher_votes", None)
    return out


def split_strata(row: dict[str, Any]) -> list[str]:
    labels = list(row.get("expected_topics") or [])
    out = [f"topic:{t}" for t in labels]
    if row.get("item_type"):
        out.append(f"kind:{row['item_type']}")
    source = "new" if row.get("easy_set_pilot_final_source") == "easy_set_400_consensus" else "v4"
    out.append(f"source:{source}")
    out.extend(f"confusion:{f}" for f in row.get("confusion_families") or [])
    return out


def stratified_three_way(
    rows: list[dict[str, Any]],
    *,
    train_fraction: float,
    validate_fraction: float,
    seed: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    n = len(rows)
    train_size = round(n * train_fraction)
    validate_size = round(n * validate_fraction)
    test_size = n - train_size - validate_size
    sizes = {"train": train_size, "validate": validate_size, "test": test_size}
    fractions = {k: v / max(1, n) for k, v in sizes.items()}
    buckets: dict[str, list[dict[str, Any]]] = {"train": [], "validate": [], "test": []}
    counts: dict[str, Counter[str]] = {k: Counter() for k in buckets}

    total = Counter(s for row in rows for s in split_strata(row))
    desired = {
        split: {key: round(value * fractions[split]) for key, value in total.items()}
        for split in buckets
    }
    rng = random.Random(seed)
    ordered = rows[:]
    rng.shuffle(ordered)
    ordered.sort(key=lambda r: (sum(1 / max(1, total[s]) for s in split_strata(r)), len(split_strata(r))), reverse=True)

    for row in ordered:
        strata = split_strata(row)
        choices = [name for name, rs in buckets.items() if len(rs) < sizes[name]]
        best = max(
            choices,
            key=lambda name: (
                sum(max(0, desired[name].get(s, 0) - counts[name][s]) for s in strata),
                sizes[name] - len(buckets[name]),
                rng.random(),
            ),
        )
        buckets[best].append(row)
        counts[best].update(strata)

    for rs in buckets.values():
        rs.sort(key=lambda r: r["id"])

    manifest = {
        "rows": n,
        "seed": seed,
        "train_fraction": train_fraction,
        "validate_fraction": validate_fraction,
        "test_fraction": test_size / max(1, n),
        "sizes": {k: len(v) for k, v in buckets.items()},
        "topic_counts": {
            split: dict(sorted(Counter(t for r in rs for t in r.get("expected_topics", [])).items()))
            for split, rs in buckets.items()
        },
        "item_type_counts": {split: dict(Counter(r.get("item_type") for r in rs)) for split, rs in buckets.items()},
        "source_counts": {
            split: dict(Counter("new" if r.get("easy_set_pilot_final_source") == "easy_set_400_consensus" else "v4" for r in rs))
            for split, rs in buckets.items()
        },
        "ids": {split: [r["id"] for r in rs] for split, rs in buckets.items()},
    }
    return buckets["train"], buckets["validate"], buckets["test"], manifest


def cmd_finalize(args: argparse.Namespace) -> int:
    v4 = load_jsonl(args.v4)
    consensus_easy = [finalized_new_easy(row) for row in load_jsonl(args.consensus_dir / "easy-consensus.jsonl")]
    medium = load_jsonl(args.consensus_dir / "medium-stable.jsonl")
    review = load_jsonl(args.consensus_dir / "review-needed.jsonl")
    invalid = load_jsonl(args.consensus_dir / "invalid.jsonl")
    known_confusion = load_jsonl(args.v4_confusion_bucket)

    by_id: dict[str, dict[str, Any]] = {}
    duplicate_ids = []
    for row in [*v4, *consensus_easy]:
        if row["id"] in by_id:
            duplicate_ids.append(row["id"])
            continue
        by_id[row["id"]] = row
    final_rows = sorted(by_id.values(), key=lambda r: r["id"])

    prefix = args.output_prefix
    write_jsonl(prefix.with_suffix(".jsonl"), final_rows)
    write_jsonl(prefix.with_name(prefix.name + "-new-easy.jsonl"), consensus_easy)
    write_jsonl(prefix.with_name(prefix.name + "-consensus-medium.jsonl"), medium)
    write_jsonl(prefix.with_name(prefix.name + "-review-needed.jsonl"), review)
    write_jsonl(prefix.with_name(prefix.name + "-invalid.jsonl"), invalid)
    write_jsonl(prefix.with_name(prefix.name + "-confusion-bucket.jsonl"), [*known_confusion, *medium, *review, *invalid])

    train, validate, test, split_manifest = stratified_three_way(
        final_rows,
        train_fraction=args.train_fraction,
        validate_fraction=args.validate_fraction,
        seed=args.seed,
    )
    write_jsonl(prefix.with_name(prefix.name + "-train.jsonl"), train)
    write_jsonl(prefix.with_name(prefix.name + "-validate.jsonl"), validate)
    write_jsonl(prefix.with_name(prefix.name + "-test.jsonl"), test)

    summary = {
        "v4_rows": len(v4),
        "new_consensus_easy_rows": len(consensus_easy),
        "easy_set_400_rows": len(final_rows),
        "duplicate_ids_skipped": duplicate_ids,
        "medium_stable_rows": len(medium),
        "review_needed_rows": len(review),
        "invalid_rows": len(invalid),
        "known_v4_confusion_rows": len(known_confusion),
        "output": str(prefix.with_suffix(".jsonl")),
        "splits": split_manifest,
        "topic_counts": dict(sorted(Counter(t for r in final_rows for t in r.get("expected_topics", [])).items())),
        "confusion_family_rows": sum(bool(r.get("confusion_families")) for r in final_rows),
    }
    prefix.with_name(prefix.name + "-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Build easy-set-400 candidates and finalized consensus splits.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sample = sub.add_parser("prepare-sample", help="Sample ds4 rows and prepare teacher input.")
    sample.add_argument("--source", type=Path, default=ROOT / "refdata/ds4.jsonl")
    sample.add_argument("--output", type=Path, default=PILOT / "easy-set-400-candidates-200.jsonl")
    sample.add_argument("--sample-size", type=int, default=200)
    sample.add_argument("--seed", type=int, default=20260610)
    sample.add_argument("--exclude", type=Path, action="append", default=[PILOT / "easy-final-v4.jsonl", PILOT / "easy-final-v4-confusion-bucket.jsonl"])
    sample.add_argument("--require-legacy-labels", action=argparse.BooleanOptionalAction, default=True)
    sample.set_defaults(func=cmd_prepare_sample)

    finalize = sub.add_parser("finalize", help="Merge 3-teacher consensus with v4 and emit train/validate/test.")
    finalize.add_argument("--v4", type=Path, default=PILOT / "easy-final-v4.jsonl")
    finalize.add_argument("--v4-confusion-bucket", type=Path, default=PILOT / "easy-final-v4-confusion-bucket.jsonl")
    finalize.add_argument("--consensus-dir", type=Path, required=True)
    finalize.add_argument("--output-prefix", type=Path, default=PILOT / "easy-set-400")
    finalize.add_argument("--train-fraction", type=float, default=0.70)
    finalize.add_argument("--validate-fraction", type=float, default=0.15)
    finalize.add_argument("--seed", type=int, default=20260610)
    finalize.set_defaults(func=cmd_finalize)
    return p


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
