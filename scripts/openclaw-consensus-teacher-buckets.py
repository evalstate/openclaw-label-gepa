#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

SCHEMA = Path("eval/openclaw/output.schema.json")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Merge repeated OpenClaw teacher labeling runs into consensus buckets.")
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--teacher", action="append", required=True, help="NAME=raw-output.jsonl")
    p.add_argument("--outdir", type=Path, required=True)
    p.add_argument("--strict-confidence", type=float, default=0.93)
    p.add_argument("--relaxed-confidence", type=float, default=0.90)
    p.add_argument("--target-easy", type=int, default=100)
    return p.parse_args()


def allowed_topics() -> set[str]:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    return set(schema["properties"]["topics_of_interest"]["items"]["enum"])


def result_obj(row: dict[str, Any]) -> dict[str, Any]:
    for key in ("result", "output", "response", "structured_output"):
        value = row.get(key)
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                return parsed
    return {}


def rationale_map(value: Any) -> dict[str, str]:
    if isinstance(value, dict):
        return {str(k): str(v) for k, v in value.items() if str(k) and str(v).strip()}
    if not isinstance(value, list):
        return {}
    out: dict[str, str] = {}
    for item in value:
        if not isinstance(item, dict):
            continue
        label = item.get("label")
        rationale = item.get("rationale")
        if isinstance(label, str) and isinstance(rationale, str) and label and rationale.strip():
            out[label] = rationale
    return out


def parse_teacher_arg(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise SystemExit(f"--teacher must be NAME=path, got {value!r}")
    name, path = value.split("=", 1)
    name = name.strip()
    if not name:
        raise SystemExit(f"empty teacher name in {value!r}")
    return name, Path(path)


def vote_from_raw(raw: dict[str, Any], *, allowed: set[str], strict_confidence: float) -> dict[str, Any]:
    obj = result_obj(raw)
    labels = [x for x in obj.get("labels", []) if isinstance(x, str)] if obj else []
    bad_labels = [x for x in labels if x not in allowed]
    ambiguity = obj.get("ambiguity") if isinstance(obj.get("ambiguity"), dict) else {}
    confusions = ambiguity.get("possible_confusions") if isinstance(ambiguity.get("possible_confusions"), list) else []
    rats = rationale_map(obj.get("per_label_rationale")) if obj else {}
    strict_easy = (
        obj.get("bucket") == "easy"
        and isinstance(obj.get("confidence"), int | float)
        and float(obj["confidence"]) >= strict_confidence
        and ambiguity.get("level") == "low"
        and obj.get("needs_human_review") is False
        and 1 <= len(labels) <= 5
        and not bad_labels
        and all(rats.get(x, "").strip() for x in labels)
        and len(confusions) <= 1
    )
    return {
        "labels": labels,
        "label_key": tuple(sorted(labels)),
        "bucket": obj.get("bucket") if obj else None,
        "confidence": obj.get("confidence") if obj else None,
        "ambiguity": ambiguity,
        "needs_human_review": obj.get("needs_human_review") if obj else None,
        "per_label_rationale": rats,
        "excluded_label_rationale": rationale_map(obj.get("excluded_label_rationale")) if obj else {},
        "invalid_labels": bad_labels,
        "strict_easy": strict_easy,
        "raw_result": obj,
    }


def main() -> int:
    args = parse_args()
    allowed = allowed_topics()
    base_rows = load_jsonl(args.input)
    by_id = {row["id"]: row for row in base_rows}
    teachers = [parse_teacher_arg(x) for x in args.teacher]

    votes_by_id: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    invalid_raw = []
    for name, path in teachers:
        for raw in load_jsonl(path):
            inp = raw.get("input") if isinstance(raw.get("input"), dict) else {}
            row_id = raw.get("id") or inp.get("id")
            if row_id not in by_id:
                invalid_raw.append({"teacher": name, "id": row_id, "reason": "raw_row_not_in_input"})
                continue
            votes_by_id[row_id][name] = vote_from_raw(raw, allowed=allowed, strict_confidence=args.strict_confidence)

    merged = []
    consensus_easy = []
    stable_medium = []
    review_needed = []
    invalid = []
    for row in base_rows:
        rid = row["id"]
        votes = votes_by_id.get(rid, {})
        missing = [name for name, _ in teachers if name not in votes]
        label_counts = Counter(v["label_key"] for v in votes.values())
        most_common_labels, most_common_count = label_counts.most_common(1)[0] if label_counts else ((), 0)
        strict_easy_votes = sum(1 for v in votes.values() if v["strict_easy"])
        easy_same = (
            not missing
            and len(votes) == len(teachers)
            and strict_easy_votes == len(teachers)
            and most_common_count == len(teachers)
            and 1 <= len(most_common_labels) <= 5
        )
        relaxed_stable = (
            not easy_same
            and not missing
            and most_common_count >= max(3, len(teachers) - 1)
            and strict_easy_votes >= max(3, len(teachers) - 1)
            and 1 <= len(most_common_labels) <= 5
        )
        rec = {
            **row,
            "teacher_votes": votes,
            "teacher_missing": missing,
            "teacher_label_set_counts": {"|".join(k): v for k, v in label_counts.items()},
            "consensus_labels": list(most_common_labels),
            "consensus_vote_count": most_common_count,
            "strict_easy_votes": strict_easy_votes,
        }
        if missing:
            rec["consensus_bucket"] = "invalid"
            invalid.append(rec)
        elif easy_same:
            rec["consensus_bucket"] = "easy"
            rec["expected_topics"] = list(most_common_labels)
            rec["expected_topics_json"] = json.dumps(list(most_common_labels))
            rec["topics_of_interest"] = list(most_common_labels)
            consensus_easy.append(rec)
        elif relaxed_stable:
            rec["consensus_bucket"] = "medium"
            stable_medium.append(rec)
        else:
            rec["consensus_bucket"] = "review"
            review_needed.append(rec)
        merged.append(rec)

    args.outdir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.outdir / "teacher-consensus.jsonl", merged)
    write_jsonl(args.outdir / "easy-consensus.jsonl", consensus_easy)
    write_jsonl(args.outdir / "easy-consensus-target.jsonl", consensus_easy[: args.target_easy])
    write_jsonl(args.outdir / "medium-stable.jsonl", stable_medium)
    write_jsonl(args.outdir / "review-needed.jsonl", review_needed)
    write_jsonl(args.outdir / "invalid.jsonl", invalid + invalid_raw)
    summary = {
        "input": str(args.input),
        "teachers": [{"name": name, "path": str(path)} for name, path in teachers],
        "rows_input": len(base_rows),
        "rows_merged": len(merged),
        "easy_consensus_rows": len(consensus_easy),
        "easy_target_rows": min(args.target_easy, len(consensus_easy)),
        "medium_stable_rows": len(stable_medium),
        "review_needed_rows": len(review_needed),
        "invalid_rows": len(invalid) + len(invalid_raw),
        "strict_confidence": args.strict_confidence,
        "relaxed_confidence": args.relaxed_confidence,
        "bucket_counts": dict(Counter(r["consensus_bucket"] for r in merged)),
        "top_consensus_labels": Counter(t for r in consensus_easy for t in r["expected_topics"]).most_common(30),
    }
    (args.outdir / "consensus-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
