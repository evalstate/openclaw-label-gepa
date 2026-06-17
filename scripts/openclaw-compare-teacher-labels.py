#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def source_labels(row: dict[str, Any]) -> list[str]:
    value = row.get("expected_topics") or row.get("topics_of_interest") or []
    return [x for x in value if isinstance(x, str)] if isinstance(value, list) else []


def teacher_labels(row: dict[str, Any]) -> list[str]:
    value = row.get("gpt55_labels") or row.get("labels") or row.get("expected_topics") or []
    return [x for x in value if isinstance(x, str)] if isinstance(value, list) else []


def main() -> int:
    p = argparse.ArgumentParser(description="Compare teacher relabel output to a source label JSONL.")
    p.add_argument("--source", type=Path, required=True)
    p.add_argument("--teacher", type=Path, required=True)
    p.add_argument("--outdir", type=Path, required=True)
    p.add_argument("--name", default="teacher-comparison")
    args = p.parse_args()

    source = load_jsonl(args.source)
    teacher = load_jsonl(args.teacher)
    by_teacher = {r["id"]: r for r in teacher}
    changed: list[dict[str, Any]] = []
    unchanged: list[dict[str, Any]] = []
    missing = []
    for row in source:
        rid = row["id"]
        tr = by_teacher.get(rid)
        if tr is None:
            missing.append(rid)
            continue
        cur = source_labels(row)
        new = teacher_labels(tr)
        rec = {
            "id": rid,
            "number": row.get("number"),
            "title": row.get("title"),
            "current_expected_topics": cur,
            "teacher_labels": new,
            "bucket": tr.get("bucket"),
            "confidence": tr.get("confidence"),
            "strict_easy": tr.get("teacher_validation", {}).get("strict_easy"),
            "relaxed_easy": tr.get("teacher_validation", {}).get("relaxed_easy"),
            "jaccard": 1.0 if not (set(cur) | set(new)) else len(set(cur) & set(new)) / len(set(cur) | set(new)),
            "teacher_additions": sorted(set(new) - set(cur)),
            "teacher_removals": sorted(set(cur) - set(new)),
            "ambiguity": tr.get("ambiguity"),
            "needs_human_review": tr.get("needs_human_review"),
            "per_label_rationale": tr.get("per_label_rationale"),
            "excluded_label_rationale": tr.get("excluded_label_rationale"),
        }
        (unchanged if set(cur) == set(new) else changed).append(rec)

    args.outdir.mkdir(parents=True, exist_ok=True)
    summary = {
        "name": args.name,
        "source": str(args.source),
        "teacher": str(args.teacher),
        "source_rows": len(source),
        "teacher_rows": len(teacher),
        "missing_teacher_rows": missing,
        "exact_agreement_rows": len(unchanged),
        "changed_rows": len(changed),
        "bucket_counts": dict(Counter(r.get("bucket") for r in teacher)),
        "strict_easy_rows": sum(1 for r in teacher if r.get("teacher_validation", {}).get("strict_easy")),
        "changed": changed,
    }
    (args.outdir / "comparison-to-source.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    (args.outdir / "changed-rows.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in changed), encoding="utf-8")
    (args.outdir / "unchanged-rows.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in unchanged), encoding="utf-8")

    lines = [f"# {args.name} label comparison", "", f"- source rows: {len(source)}", f"- teacher rows: {len(teacher)}", f"- exact agreement: {len(unchanged)}", f"- changed rows: {len(changed)}", "", "## Changed rows", ""]
    for r in changed:
        lines.extend([
            f"### {r['id']} / #{r.get('number')} — {r.get('title') or ''}",
            "",
            f"- bucket: `{r.get('bucket')}` confidence: `{r.get('confidence')}` strict_easy: `{r.get('strict_easy')}`",
            f"- current: `{', '.join(r['current_expected_topics'])}`",
            f"- teacher: `{', '.join(r['teacher_labels'])}`",
            f"- additions: `{', '.join(r['teacher_additions'])}`",
            f"- removals: `{', '.join(r['teacher_removals'])}`",
            "",
        ])
    (args.outdir / "changed-rows.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ["source_rows", "teacher_rows", "exact_agreement_rows", "changed_rows", "bucket_counts", "strict_easy_rows"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
