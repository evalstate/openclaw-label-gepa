#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from openclaw_gepa.openclaw_benchmark import ENV_DIR, SOURCE, evidence_excerpt, load_jsonl


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Ask a strong model for topic-boundary guidance from scored failures.")
    p.add_argument("score", type=Path, help="candidate score.json")
    p.add_argument("--source", type=Path, default=SOURCE)
    p.add_argument("--model", default="codexresponses.gpt-5.5?reasoning=high")
    p.add_argument("--fast-agent-bin", default="fast-agent")
    p.add_argument("--topics", nargs="*", default=None, help="Optional topics to focus on; defaults to top error patterns.")
    p.add_argument("--examples-per-topic", type=int, default=4)
    p.add_argument("--output", type=Path, default=None, help="Write guidance markdown here.")
    p.add_argument("--prompt-output", type=Path, default=None, help="Write the model prompt here.")
    p.add_argument("--no-call", action="store_true", help="Only write/print the prompt; do not call fast-agent.")
    return p.parse_args()


def raw_by_id(path: Path) -> dict[str, dict[str, Any]]:
    return {row["id"]: row for row in load_jsonl(path)}


def row_context(row: dict[str, Any]) -> str:
    parts = [
        f"id: {row.get('id')}",
        f"title: {row.get('title')}",
        f"expected_topics: {row.get('topics_of_interest')}",
        f"keywords: {row.get('keywords')}",
        "",
        "body_excerpt:",
        evidence_excerpt(row.get("body") or "", 1200),
    ]
    comments = row.get("comments") or []
    if comments:
        parts.extend(["", "comment_excerpt:", evidence_excerpt(comments[0].get("body") or "", 700)])
    diff = row.get("diff") or ""
    if diff:
        parts.extend(["", "diff_excerpt:", evidence_excerpt(diff, 1000)])
    return "\n".join(parts)


def build_prompt(score: dict[str, Any], source_rows: dict[str, dict[str, Any]], topics: list[str], per_topic: int) -> str:
    sections = [
        "# Task",
        "You are improving ASI guidance for an OpenClaw GitHub issue/PR topic classifier.",
        "For each topic below, infer crisp positive and negative rules from the labeled seed rows and scored model errors.",
        "Return concise markdown with: positive cues, false-positive exclusions, false-negative rescue cues, and 2-4 boundary examples.",
        "Do not rewrite the full policy; produce guidance snippets suitable for evaluator side-info/topic hints.",
        "",
        "# Current aggregate scores",
        "```json",
        json.dumps(score.get("scores", {}), indent=2),
        "```",
    ]
    patterns = {p["topic"]: p for p in score.get("topic_error_patterns", [])}
    for topic in topics:
        ptn = patterns.get(topic, {"topic": topic})
        sections.extend(["", f"# Topic: `{topic}`", "```json", json.dumps({
            k: ptn.get(k)
            for k in ["problem", "expected", "actual", "true_positives", "false_positives", "false_negatives", "precision", "recall", "action"]
        }, indent=2), "```"])
        ids: list[str] = []
        for key in ("false_positive_examples", "false_negative_examples", "true_positive_examples", "examples"):
            for ex in ptn.get(key, []) or []:
                if ex.get("id") and ex["id"] not in ids:
                    ids.append(ex["id"])
                if len(ids) >= per_topic:
                    break
            if len(ids) >= per_topic:
                break
        for row_id in ids:
            raw = source_rows.get(row_id)
            if raw:
                sections.extend(["", f"## Seed row {row_id}", "```text", row_context(raw), "```"])
    return "\n".join(sections) + "\n"


def main() -> int:
    args = parse_args()
    score = json.loads(args.score.read_text(encoding="utf-8"))
    topics = args.topics or [p["topic"] for p in score.get("topic_error_patterns", [])[:8]]
    prompt = build_prompt(score, raw_by_id(args.source), topics, args.examples_per_topic)
    if args.prompt_output:
        args.prompt_output.parent.mkdir(parents=True, exist_ok=True)
        args.prompt_output.write_text(prompt, encoding="utf-8")
    if args.no_call:
        print(prompt)
        return 0

    out = args.output or args.score.with_name("topic-guidance.md")
    prompt_path = args.prompt_output or args.score.with_name("topic-guidance.prompt.md")
    prompt_path.write_text(prompt, encoding="utf-8")
    cmd = [
        args.fast_agent_bin,
        "--no-update-check",
        "--env",
        str(ENV_DIR),
        "go",
        "--prompt-file",
        str(prompt_path),
        "--model",
        args.model,
        "--quiet",
    ]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)
    if proc.returncode:
        raise SystemExit(f"fast-agent failed with exit {proc.returncode}\n{proc.stderr[-4000:]}")
    out.write_text(proc.stdout, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
