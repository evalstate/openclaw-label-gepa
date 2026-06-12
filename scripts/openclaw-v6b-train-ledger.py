#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INTAKE = ROOT / "runs/easy-set-v6b/v6b-databuild/intake"
DEFAULT_OUTDIR = ROOT / "eval/openclaw/easy-set-pilot/v6"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a v6b train-quality ledger from intake consensus rows.")
    parser.add_argument("--intake-root", type=Path, default=DEFAULT_INTAKE)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--prefix", default="v6b")
    return parser.parse_args()


def label_tuple(labels: Any) -> tuple[str, ...]:
    return tuple(labels) if isinstance(labels, list) and all(isinstance(x, str) for x in labels) else ()


def basic_teacher_ok(summary: dict[str, Any]) -> bool:
    return bool(
        summary.get("complete")
        and summary.get("failed_runs", 0) == 0
        and not summary.get("invalid_labels")
        and not summary.get("too_many_labels")
        and not summary.get("hit_label_cap")
        and not summary.get("needs_human_review")
    )


def strict_teacher_ok(summary: dict[str, Any]) -> bool:
    if not basic_teacher_ok(summary):
        return False
    for run in summary.get("runs", []):
        if not run.get("ok"):
            return False
        if run.get("needs_human_review"):
            return False
        if run.get("invalid_labels"):
            return False
        if run.get("confidence", 0.0) < 0.90:
            return False
        if run.get("ambiguity_level") != "low":
            return False
    return True


def train_quality(row: dict[str, Any]) -> bool:
    gpt = row["gpt"]
    opus = row["opus"]
    return bool(
        basic_teacher_ok(gpt)
        and basic_teacher_ok(opus)
        and gpt.get("exact_stable")
        and label_tuple(gpt.get("modal_labels")) == label_tuple(opus.get("modal_labels"))
        and 1 <= len(gpt.get("modal_labels", [])) <= 5
    )


def strict_benchmark_quality(row: dict[str, Any]) -> bool:
    gpt = row["gpt"]
    opus = row["opus"]
    return bool(
        train_quality(row)
        and opus.get("exact_stable")
        and strict_teacher_ok(gpt)
        and strict_teacher_ok(opus)
    )


def ledger_row(row: dict[str, Any], batch: str) -> dict[str, Any]:
    accepted = row.get("status") == "accepted_consensus"
    labels = row["gpt"]["modal_labels"]
    source = "teacher_consensus" if accepted else "teacher_modal_soft_train_only"
    decision_note = (
        "GPT and Opus modal labels are exact-stable and matched under the current spec."
        if accepted
        else (
            "Train-only soft modal row: GPT was exact-stable 3/3 and Opus modal matched GPT; "
            "excluded from benchmark/adjudicated ledgers because Opus was not exact-stable."
        )
    )
    return {
        "id": row["id"],
        "batch": batch,
        "status": "accepted_consensus" if accepted else "train_only_modal_soft",
        "labels": labels,
        "source": source,
        "github_url": row.get("github_url"),
        "title": row.get("title"),
        "spec_manifest": str(DEFAULT_INTAKE / batch / "spec-manifest.json"),
        "legacy_v5_labels": row.get("legacy_v5_labels", []),
        "quality": {
            "train_quality": True,
            "strict_benchmark_quality": strict_benchmark_quality(row),
            "gpt_exact_stable": row["gpt"].get("exact_stable"),
            "opus_exact_stable": row["opus"].get("exact_stable"),
            "gpt_modal_count": row["gpt"].get("modal_count"),
            "opus_modal_count": row["opus"].get("modal_count"),
            "gpt_opus_modal_match": label_tuple(row["gpt"].get("modal_labels"))
            == label_tuple(row["opus"].get("modal_labels")),
            "review_reasons": row.get("review_reasons", []),
        },
        "decision_note": decision_note,
    }


def markdown_summary(summary: dict[str, Any], extra_rows: list[dict[str, Any]]) -> str:
    lines = [
        "# V6b Train-Quality Ledger",
        "",
        "This artifact is for sharing and early investigation. It does not change the adjudicated v6b set.",
        "",
        "## Gates",
        "",
        "- Benchmark/adjudicated rows require GPT 3/3 exact stability, Opus 2/2 exact stability, matching modal label sets, and no teacher validity flags.",
        "- Strict benchmark-quality rows additionally require every teacher run to have confidence >= 0.90 and low ambiguity.",
        "- Train-only rows require GPT 3/3 exact stability and an Opus modal set matching GPT. Opus may wobble across its two repeats.",
        "- Deferred rows with GPT/Opus modal disagreement, invalid labels, over-cardinality, failed runs, or human-review flags are excluded.",
        "",
        "## Counts",
        "",
        f"- Attempted rows: {summary['attempted_rows']}",
        f"- Existing accepted consensus rows: {summary['accepted_consensus_rows']}",
        f"- Strict benchmark-quality rows: {summary['strict_benchmark_quality_rows']}",
        f"- Train-quality rows total: {summary['train_quality_rows']}",
        f"- Additional train-only soft-modal rows: {summary['train_only_soft_rows']}",
        "",
        "## Additional Train-Only Rows",
        "",
    ]
    if not extra_rows:
        lines.append("No additional train-only rows found.")
    for row in extra_rows:
        labels = ", ".join(f"`{label}`" for label in row["labels"])
        lines.extend(
            [
                f"### {row['id']}",
                "",
                f"- Batch: `{row['batch']}`",
                f"- Title: {row.get('title', '')}",
                f"- GitHub: {row.get('github_url') or 'unavailable'}",
                f"- Labels: {labels}",
                f"- Review reasons retained for provenance: `{row['quality']['review_reasons']}`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    consensus_paths = sorted(args.intake_root.glob("batch-*/consensus.jsonl"))
    if not consensus_paths:
        raise SystemExit(f"no consensus files found under {args.intake_root}")

    all_rows: list[tuple[str, dict[str, Any]]] = []
    for path in consensus_paths:
        batch = path.parent.name
        all_rows.extend((batch, row) for row in load_jsonl(path))

    train_rows = [ledger_row(row, batch) for batch, row in all_rows if train_quality(row)]
    extra_rows = [row for row in train_rows if row["status"] == "train_only_modal_soft"]
    accepted_rows = [row for _, row in all_rows if row.get("status") == "accepted_consensus"]
    strict_rows = [row for _, row in all_rows if strict_benchmark_quality(row)]

    summary = {
        "attempted_rows": len(all_rows),
        "accepted_consensus_rows": len(accepted_rows),
        "strict_benchmark_quality_rows": len(strict_rows),
        "train_quality_rows": len(train_rows),
        "train_only_soft_rows": len(extra_rows),
        "train_quality_by_status": dict(Counter(row["status"] for row in train_rows)),
        "train_only_soft_by_batch": dict(Counter(row["batch"] for row in extra_rows)),
        "train_quality_label_counts": dict(Counter(label for row in train_rows for label in row["labels"])),
        "train_only_soft_label_counts": dict(Counter(label for row in extra_rows for label in row["labels"])),
    }

    prefix = args.prefix
    write_jsonl(args.outdir / f"{prefix}-train-ledger.jsonl", train_rows)
    write_jsonl(args.outdir / f"{prefix}-train-only-soft.jsonl", extra_rows)
    (args.outdir / f"{prefix}-train-ledger-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (args.outdir / f"{prefix}-train-ledger-summary.md").write_text(
        markdown_summary(summary, extra_rows), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
