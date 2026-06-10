#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "eval/openclaw/label-generator/teacher-stable-best-v1-good200.jsonl"
DEFAULT_OUTDIR = ROOT / "eval/openclaw/easy-set-pilot"
CARD = DEFAULT_OUTDIR / "teacher-card.md"
TEMPLATE = DEFAULT_OUTDIR / "teacher-template.md"
TEACHER_SCHEMA = DEFAULT_OUTDIR / "teacher-output.schema.json"
CLASSIFIER_SCHEMA = ROOT / "eval/openclaw/output.schema.json"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run/postprocess GPT-5.5 easy-set-pilot teacher stratification.")
    p.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    p.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    p.add_argument("--model", default="codexresponses.gpt-5.5?reasoning=high")
    p.add_argument("--parallel", type=int, default=4)
    p.add_argument("--fast-agent-bin", default="fast-agent")
    p.add_argument("--agent-card", "--card", dest="agent_card", type=Path, default=CARD)
    p.add_argument("--run", action="store_true", help="Run fast-agent batch before postprocessing.")
    p.add_argument("--raw-output", type=Path, default=None, help="Existing or target raw fast-agent output JSONL.")
    p.add_argument("--strict-confidence", type=float, default=0.93)
    p.add_argument("--relaxed-confidence", type=float, default=0.90)
    p.add_argument("--overwrite", action="store_true")
    return p.parse_args()


def allowed_topics() -> set[str]:
    schema = json.loads(CLASSIFIER_SCHEMA.read_text(encoding="utf-8"))
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


def jaccard(a: set[str], b: set[str]) -> float:
    return 1.0 if not a and not b else len(a & b) / len(a | b)


def agreement(previous: list[str], labels: list[str]) -> dict[str, Any]:
    prev, cur = set(previous), set(labels)
    return {
        "exact": prev == cur,
        "jaccard": jaccard(prev, cur),
        "false_positives_vs_previous": sorted(cur - prev),
        "false_negatives_vs_previous": sorted(prev - cur),
    }


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


def valid_easy(obj: dict[str, Any], *, min_confidence: float, allowed: set[str]) -> bool:
    labels = obj.get("labels")
    rats = rationale_map(obj.get("per_label_rationale"))
    ambiguity = obj.get("ambiguity") if isinstance(obj.get("ambiguity"), dict) else {}
    confusions = ambiguity.get("possible_confusions") if isinstance(ambiguity.get("possible_confusions"), list) else []
    return (
        obj.get("bucket") == "easy"
        and isinstance(obj.get("confidence"), int | float)
        and float(obj["confidence"]) >= min_confidence
        and ambiguity.get("level") == "low"
        and obj.get("needs_human_review") is False
        and isinstance(labels, list)
        and 1 <= len(labels) <= 5
        and all(isinstance(x, str) and x in allowed for x in labels)
        and all(isinstance(rats.get(x), str) and rats[x].strip() for x in labels)
        and len(confusions) <= 1
    )


def merge_and_write(args: argparse.Namespace) -> dict[str, Any]:
    raw_path = args.raw_output or args.outdir / "teacher-labels.raw.jsonl"
    inputs = load_jsonl(args.input)
    by_id = {r["id"]: r for r in inputs}
    raw_rows = load_jsonl(raw_path)
    allowed = allowed_topics()

    merged = []
    invalid = []
    for raw in raw_rows:
        inp = raw.get("input") if isinstance(raw.get("input"), dict) else {}
        row_id = raw.get("id") or inp.get("id")
        base = by_id.get(row_id)
        obj = result_obj(raw)
        if not base or not obj:
            invalid.append({"id": row_id, "reason": "missing_input_or_result", "raw": raw})
            continue
        labels = [x for x in obj.get("labels", []) if isinstance(x, str)]
        bad_labels = [x for x in labels if x not in allowed]
        row = {
            **base,
            "previous_expected_topics": list(base.get("expected_topics") or []),
            "gpt55_labels": labels,
            "bucket": obj.get("bucket"),
            "confidence": obj.get("confidence"),
            "per_label_rationale": rationale_map(obj.get("per_label_rationale")),
            "excluded_label_rationale": rationale_map(obj.get("excluded_label_rationale")),
            "ambiguity": obj.get("ambiguity") if isinstance(obj.get("ambiguity"), dict) else {},
            "needs_human_review": obj.get("needs_human_review"),
            "agreement_with_previous": agreement(list(base.get("expected_topics") or []), labels),
            "teacher_validation": {
                "invalid_labels": bad_labels,
                "strict_easy": valid_easy(obj, min_confidence=args.strict_confidence, allowed=allowed),
                "relaxed_easy": valid_easy(obj, min_confidence=args.relaxed_confidence, allowed=allowed),
            },
        }
        if bad_labels:
            row["needs_human_review"] = True
            row["bucket"] = "hard"
        if row["bucket"] == "easy" and row["agreement_with_previous"]["jaccard"] < 0.50:
            row["teacher_validation"]["strong_previous_disagreement"] = True
            row["bucket"] = "medium"
            row["needs_human_review"] = True
        merged.append(row)

    out = args.outdir
    write_jsonl(out / "teacher-labels.jsonl", merged)
    write_jsonl(out / "easy-all.jsonl", [r for r in merged if r["teacher_validation"]["strict_easy"] and r["bucket"] == "easy"])
    write_jsonl(out / "easy-all-relaxed.jsonl", [r for r in merged if r["teacher_validation"]["relaxed_easy"] and r["bucket"] == "easy"])
    write_jsonl(out / "medium.jsonl", [r for r in merged if r.get("bucket") == "medium"])
    write_jsonl(out / "hard.jsonl", [r for r in merged if r.get("bucket") == "hard"])
    write_jsonl(out / "review-needed.jsonl", [r for r in merged if r.get("needs_human_review")])
    write_jsonl(out / "teacher-invalid.jsonl", invalid)

    counts = Counter(r.get("bucket") for r in merged)
    summary = {
        "name": "easy-set-pilot",
        "input": str(args.input),
        "raw_output": str(raw_path),
        "rows_input": len(inputs),
        "rows_teacher_output": len(raw_rows),
        "rows_merged": len(merged),
        "invalid_raw_rows": len(invalid),
        "bucket_counts": dict(counts),
        "strict_confidence": args.strict_confidence,
        "relaxed_confidence": args.relaxed_confidence,
        "strict_easy_rows": sum(1 for r in merged if r["teacher_validation"]["strict_easy"] and r["bucket"] == "easy"),
        "relaxed_easy_rows": sum(1 for r in merged if r["teacher_validation"]["relaxed_easy"] and r["bucket"] == "easy"),
        "review_needed_rows": sum(1 for r in merged if r.get("needs_human_review")),
        "strong_previous_disagreement_rows": sum(1 for r in merged if r["teacher_validation"].get("strong_previous_disagreement")),
    }
    (out / "stratification-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = ["# easy-set-pilot rationales", ""]
    for r in merged:
        if not (r["teacher_validation"]["strict_easy"] and r["bucket"] == "easy"):
            continue
        lines.extend([f"## {r['id']} — {r.get('title') or ''}", "", f"- labels: `{', '.join(r['gpt55_labels'])}`"])
        for label, rationale in r.get("per_label_rationale", {}).items():
            lines.append(f"- `{label}`: {rationale}")
        lines.append("")
    (out / "easy-rationales.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


def run_batch(args: argparse.Namespace) -> None:
    raw_path = args.raw_output or args.outdir / "teacher-labels.raw.jsonl"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        args.fast_agent_bin, "--no-update-check", "--env", str(ROOT / ".fast-agent"), "batch", "run",
        "--agent-card", str(args.agent_card),
        "--agent", "openclaw_easy_set_pilot_teacher",
        "--input", str(args.input),
        "--output", str(raw_path),
        "--template", str(TEMPLATE),
        "--json-schema", str(TEACHER_SCHEMA),
        "--model", args.model,
        "--id-field", "id",
        "--include-input",
        "--parallel", str(args.parallel),
        "--no-final-summary",
    ]
    if args.overwrite:
        cmd.append("--overwrite")
    print(" ".join(cmd), file=sys.stderr)
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    if args.run:
        run_batch(args)
    summary = merge_and_write(args)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
