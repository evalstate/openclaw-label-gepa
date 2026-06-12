#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "eval/openclaw/easy-set-pilot/v6/teacher-output-v6b.schema.json"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build v6 intake consensus/adjudication artifacts.")
    p.add_argument("--batch-dir", type=Path, required=True)
    p.add_argument("--gpt-run", default="gpt55-3x")
    p.add_argument("--opus-run", default="opus-2x")
    p.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    p.add_argument("--outdir", type=Path, default=None)
    p.add_argument("--overwrite", action="store_true")
    return p.parse_args()


def allowed_topics(schema_path: Path) -> set[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return set(schema["properties"]["labels"]["items"]["enum"])


def result_obj(row: dict[str, Any]) -> dict[str, Any]:
    value = row.get("result")
    return value if isinstance(value, dict) else {}


def label_key(labels: Any) -> tuple[str, ...]:
    if not isinstance(labels, list):
        return ()
    return tuple(sorted(x for x in labels if isinstance(x, str)))


def ambiguity_level(result: dict[str, Any]) -> str | None:
    ambiguity = result.get("ambiguity")
    if isinstance(ambiguity, dict) and isinstance(ambiguity.get("level"), str):
        return ambiguity["level"]
    return None


def possible_confusions(result: dict[str, Any]) -> list[str]:
    ambiguity = result.get("ambiguity")
    if not isinstance(ambiguity, dict) or not isinstance(ambiguity.get("possible_confusions"), list):
        return []
    return [x for x in ambiguity["possible_confusions"] if isinstance(x, str)]


def read_repeats(run_dir: Path) -> dict[str, list[dict[str, Any]]]:
    by_id: dict[str, list[dict[str, Any]]] = {}
    repeat_paths = sorted(run_dir.glob("repeat-*/results.jsonl"))
    if not repeat_paths:
        raise SystemExit(f"no repeat results found under {run_dir}")
    for path in repeat_paths:
        repeat_name = path.parent.name
        for raw in load_jsonl(path):
            inp = raw.get("input") if isinstance(raw.get("input"), dict) else {}
            result = result_obj(raw)
            rid = result.get("id") or inp.get("id")
            if not isinstance(rid, str):
                continue
            by_id.setdefault(rid, []).append(
                {
                    "repeat": repeat_name,
                    "ok": raw.get("ok") is True,
                    "labels": list(label_key(result.get("labels"))),
                    "bucket": result.get("bucket"),
                    "confidence": result.get("confidence"),
                    "ambiguity_level": ambiguity_level(result),
                    "possible_confusions": possible_confusions(result),
                    "needs_human_review": result.get("needs_human_review"),
                    "invalid_labels": [],
                }
            )
    return by_id


def summarize_teacher(
    rows: list[dict[str, Any]],
    *,
    expected_runs: int,
    allowed: set[str],
) -> dict[str, Any]:
    counts = Counter(tuple(row["labels"]) for row in rows)
    modal_key, modal_count = counts.most_common(1)[0] if counts else ((), 0)
    invalid = sorted({label for row in rows for label in row["labels"] if label not in allowed})
    too_many = any(len(row["labels"]) > 5 for row in rows)
    human_review = any(row.get("needs_human_review") is True for row in rows)
    failed = sum(1 for row in rows if not row.get("ok"))
    return {
        "runs_seen": len(rows),
        "expected_runs": expected_runs,
        "complete": len(rows) == expected_runs,
        "modal_labels": list(modal_key),
        "modal_count": modal_count,
        "exact_stable": len(rows) == expected_runs and modal_count == expected_runs,
        "label_set_counts": {"|".join(key): value for key, value in counts.items()},
        "avg_label_count": sum(len(row["labels"]) for row in rows) / len(rows) if rows else 0.0,
        "hit_label_cap": any(len(row["labels"]) == 5 for row in rows),
        "too_many_labels": too_many,
        "invalid_labels": invalid,
        "needs_human_review": human_review,
        "failed_runs": failed,
        "runs": rows,
    }


def jaccard(a: list[str], b: list[str]) -> float:
    aset = set(a)
    bset = set(b)
    if not aset and not bset:
        return 1.0
    return len(aset & bset) / len(aset | bset)


def github_url(source: dict[str, Any]) -> str | None:
    context = source.get("github_context")
    if not isinstance(context, str):
        return None
    match = re.search(r"(?m)^- URL: (https://github\.com/\S+)\s*$", context)
    return match.group(1) if match else None


def load_v5(batch_dir: Path) -> dict[str, list[str]]:
    path = batch_dir / "v5-gold-reference.jsonl"
    if not path.exists():
        return {}
    out: dict[str, list[str]] = {}
    for row in load_jsonl(path):
        if isinstance(row.get("id"), str):
            labels = row.get("v5_expected_topics", [])
            out[row["id"]] = [x for x in labels if isinstance(x, str)]
    return out


def review_reasons(gpt: dict[str, Any], opus: dict[str, Any], exact_match: bool) -> list[str]:
    reasons = []
    for name, summary in (("gpt", gpt), ("opus", opus)):
        if not summary["complete"]:
            reasons.append(f"{name}_missing_repeats")
        if not summary["exact_stable"]:
            reasons.append(f"{name}_unstable")
        if summary["failed_runs"]:
            reasons.append(f"{name}_failed_runs")
        if summary["invalid_labels"]:
            reasons.append(f"{name}_invalid_labels")
        if summary["too_many_labels"]:
            reasons.append(f"{name}_over_cardinality")
        if summary["needs_human_review"]:
            reasons.append(f"{name}_flagged_human_review")
    if not exact_match:
        reasons.append("gpt_opus_modal_disagreement")
    return reasons


def make_review_packet(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    lines = [
        "# V6 batch consensus review",
        "",
        f"- Batch: `{summary['batch']}`",
        f"- Rows: {summary['rows']}",
        f"- Accepted consensus: {summary['accepted_consensus']}",
        f"- Deferred/review: {summary['deferred']}",
        f"- GPT/Opus exact modal matches: {summary['gpt_opus_exact_modal_matches']}",
        f"- Exact modal matches with 5 labels: {summary['exact_modal_matches_with_5_labels']}",
        f"- Rows where either teacher hit the 5-label cap: {summary['rows_with_any_5_label_teacher_modal']}",
        f"- Mean GPT/Opus modal Jaccard: {summary['mean_gpt_opus_modal_jaccard']:.3f}",
        "",
        "## Review rows",
        "",
    ]
    review_rows = [row for row in rows if row["status"] != "accepted_consensus"]
    if not review_rows:
        lines.append("No review rows.")
    for row in review_rows:
        lines.extend(
            [
                f"### {row['id']}",
                "",
                f"- Title: {row.get('title', '')}",
                f"- GitHub: {row['github_url']}" if row.get("github_url") else "- GitHub: unavailable",
                f"- Reasons: {', '.join(row['review_reasons'])}",
                f"- GPT modal: `{row['gpt']['modal_labels']}` ({row['gpt']['modal_count']}/{row['gpt']['expected_runs']})",
                "- GPT label-set votes:",
                *label_set_lines(row["gpt"]),
                f"- Opus modal: `{row['opus']['modal_labels']}` ({row['opus']['modal_count']}/{row['opus']['expected_runs']})",
                "- Opus label-set votes:",
                *label_set_lines(row["opus"]),
                f"- Modal Jaccard: {row['gpt_opus_modal_jaccard']:.3f}",
                f"- Legacy v5: `{row.get('legacy_v5_labels', [])}`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def label_set_lines(summary: dict[str, Any]) -> list[str]:
    lines = []
    for label_key, count in summary["label_set_counts"].items():
        labels = label_key.split("|") if label_key else []
        lines.append(f"  - `{labels}`: {count}")
    return lines


def main() -> int:
    args = parse_args()
    batch_dir = args.batch_dir
    outdir = args.outdir or batch_dir
    for name in ("consensus.jsonl", "accepted.jsonl", "deferred.jsonl", "adjudication.jsonl", "review-packet.md"):
        path = outdir / name
        if path.exists() and not args.overwrite:
            raise SystemExit(f"{path} exists; pass --overwrite")

    allowed = allowed_topics(args.schema)
    input_rows = load_jsonl(batch_dir / "input.jsonl")
    v5_by_id = load_v5(batch_dir)
    gpt_by_id = read_repeats(batch_dir / args.gpt_run)
    opus_by_id = read_repeats(batch_dir / args.opus_run)

    consensus_rows: list[dict[str, Any]] = []
    accepted: list[dict[str, Any]] = []
    deferred: list[dict[str, Any]] = []
    adjudication: list[dict[str, Any]] = []

    for source in input_rows:
        rid = source["id"]
        gpt = summarize_teacher(gpt_by_id.get(rid, []), expected_runs=3, allowed=allowed)
        opus = summarize_teacher(opus_by_id.get(rid, []), expected_runs=2, allowed=allowed)
        exact_match = gpt["modal_labels"] == opus["modal_labels"]
        agreed_labels = gpt["modal_labels"] if exact_match else []
        reasons = review_reasons(gpt, opus, exact_match)
        accept = (
            not reasons
            and gpt["exact_stable"]
            and opus["exact_stable"]
            and exact_match
            and 1 <= len(agreed_labels) <= 5
        )
        status = "accepted_consensus" if accept else "deferred"
        row = {
            "id": rid,
            "title": source.get("title"),
            "number": source.get("number"),
            "target": source.get("target"),
            "github_url": github_url(source),
            "status": status,
            "labels": agreed_labels if accept else [],
            "gpt": gpt,
            "opus": opus,
            "gpt_opus_exact_modal_match": exact_match,
            "gpt_opus_modal_jaccard": jaccard(gpt["modal_labels"], opus["modal_labels"]),
            "agreed_label_count": len(agreed_labels),
            "any_teacher_modal_label_count_5": len(gpt["modal_labels"]) == 5 or len(opus["modal_labels"]) == 5,
            "review_reasons": reasons,
            "legacy_v5_labels": v5_by_id.get(rid, []),
        }
        consensus_rows.append(row)
        if accept:
            accepted.append(
                {
                    "id": rid,
                    "status": status,
                    "labels": agreed_labels,
                    "source": "teacher_consensus",
                    "legacy_v5_labels": v5_by_id.get(rid, []),
                    "decision_note": "GPT and Opus modal labels are exact-stable and matched under the current spec.",
                }
            )
        else:
            deferred.append(row)
            adjudication.append(
                {
                    "id": rid,
                    "status": "needs_adjudication",
                    "proposed_labels": [],
                    "decision_disposition": "",
                    "decision_note": "",
                    "gpt_modal_labels": gpt["modal_labels"],
                    "opus_modal_labels": opus["modal_labels"],
                    "review_reasons": reasons,
                    "legacy_v5_labels": v5_by_id.get(rid, []),
                }
            )

    exact_matches = [row for row in consensus_rows if row["gpt_opus_exact_modal_match"]]
    summary = {
        "batch": batch_dir.name,
        "rows": len(consensus_rows),
        "accepted_consensus": len(accepted),
        "deferred": len(deferred),
        "gpt_exact_stable_rows": sum(1 for row in consensus_rows if row["gpt"]["exact_stable"]),
        "opus_exact_stable_rows": sum(1 for row in consensus_rows if row["opus"]["exact_stable"]),
        "gpt_opus_exact_modal_matches": len(exact_matches),
        "exact_modal_matches_with_5_labels": sum(1 for row in exact_matches if row["agreed_label_count"] == 5),
        "rows_with_any_5_label_teacher_modal": sum(
            1 for row in consensus_rows if row["any_teacher_modal_label_count_5"]
        ),
        "mean_gpt_opus_modal_jaccard": sum(row["gpt_opus_modal_jaccard"] for row in consensus_rows)
        / len(consensus_rows)
        if consensus_rows
        else 0.0,
        "review_reason_counts": dict(Counter(reason for row in deferred for reason in row["review_reasons"])),
        "accepted_label_counts": dict(Counter(len(row["labels"]) for row in accepted)),
    }

    write_jsonl(outdir / "consensus.jsonl", consensus_rows)
    write_jsonl(outdir / "accepted.jsonl", accepted)
    write_jsonl(outdir / "deferred.jsonl", deferred)
    write_jsonl(outdir / "adjudication.jsonl", adjudication)
    (outdir / "consensus-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (outdir / "review-packet.md").write_text(make_review_packet(summary, consensus_rows), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
