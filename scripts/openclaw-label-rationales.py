#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from openclaw_gepa.openclaw_benchmark import ENV_DIR, REF, evidence_excerpt, load_jsonl


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_CUES: dict[str, list[str]] = {
    "agent_runtime": ["agent runtime", "RuntimePlan", "runtime plan", "harness", "embedded runner", "attempt", "agent transport", "child task", "finalLlmOutcome", "model turn", "assistant message", "agent cli", "runner", "pi"],
    "queueing": ["queue", "queued", "queueing", "yield", "yielded", "waiting", "pending", "concurrency", "serial", "backpressure", "dispatch", "fan-out", "startup ordering", "child completion", "sidecar startup"],
    "exec_tools": ["exec", "command", "shell", "pty", "subprocess", "spawn", "stdio", "allowlist", "allowedHosts", "browser command", "mcp stdio", "exit code", "sigkill", "env vars", "process"],
    "skills_plugins": ["skill", "skills", "plugin", "plugins", "extension", "memory-core", "skill prelude", "managed skills", "SecretRef"],
    "api_surface": ["api", "http", "endpoint", "/v1", "sse", "schema", "request", "response", "contract", "cli flag", "payload", "streaming", "event"],
    "coding_agents": ["codex", "acp", "acpx", "subagent", "sub-agent", "agent runtime", "RuntimePlan", "runtime plan", "harness", "embedded runner", "pi", "claude code", "approvals", "sandbox", "child task", "runner", "compaction", "durable", "coding agent", "agent orchestration", "tool-use"],
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Distill human label rationales from seed rows using a strong model.")
    p.add_argument("labels", nargs="+")
    p.add_argument("--source", type=Path, default=REF / "seed.jsonl")
    p.add_argument("--score", type=Path, default=None, help="Optional score.json with validation failures.")
    p.add_argument("--model", default="codexresponses.gpt-5.5?reasoning=high")
    p.add_argument("--fast-agent-bin", default="fast-agent")
    p.add_argument("--output-dir", type=Path, default=ROOT / "eval" / "openclaw" / "label-rationales" / "generated")
    p.add_argument("--examples", type=int, default=14)
    p.add_argument("--negative-examples", type=int, default=8)
    p.add_argument("--structured-json", action="store_true", help="Ask for strict compact JSON instead of freeform markdown.")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def raw_context(row: dict[str, Any], max_body: int = 900) -> str:
    parts = [
        f"id: {row.get('id')}",
        f"title: {row.get('title')}",
        f"labels: {row.get('topics_of_interest')}",
        f"keywords: {row.get('keywords')}",
        "",
        "body excerpt:",
        evidence_excerpt(row.get("body") or "", max_body),
    ]
    return "\n".join(parts)


def load_score_examples(path: Path | None, label: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if path is None or not path.exists():
        return [], []
    score = json.loads(path.read_text(encoding="utf-8"))
    false_negatives: list[dict[str, Any]] = []
    false_positives: list[dict[str, Any]] = []
    seen_fn: set[str] = set()
    seen_fp: set[str] = set()
    for key in ("worst_failures", "failures"):
        for fail in score.get(key, []) or []:
            row_id = fail.get("id")
            if label in fail.get("false_negatives", []) and row_id not in seen_fn:
                false_negatives.append(fail)
                seen_fn.add(row_id)
            if label in fail.get("false_positives", []) and row_id not in seen_fp:
                false_positives.append(fail)
                seen_fp.add(row_id)
    return false_negatives, false_positives


def choose_positive_rows(rows: list[dict[str, Any]], label: str, limit: int) -> list[dict[str, Any]]:
    positives = [r for r in rows if label in (r.get("topics_of_interest") or [])]
    # Prefer diverse co-label/cardinality examples.
    positives.sort(key=lambda r: (-len(r.get("topics_of_interest") or []), r.get("id", "")))
    picked: list[dict[str, Any]] = []
    seen_shapes: set[tuple[str, ...]] = set()
    for row in positives:
        shape = tuple(sorted(t for t in row.get("topics_of_interest", []) if t != label))
        if shape in seen_shapes and len(picked) >= limit // 2:
            continue
        picked.append(row)
        seen_shapes.add(shape)
        if len(picked) >= limit:
            break
    return picked


def choose_negative_rows(rows: list[dict[str, Any]], label: str, limit: int) -> list[dict[str, Any]]:
    cues = [c.lower() for c in DEFAULT_CUES.get(label, [])]
    negatives = [r for r in rows if label not in (r.get("topics_of_interest") or [])]
    scored = []
    for row in negatives:
        text = " ".join([row.get("title", ""), " ".join(row.get("keywords") or []), (row.get("body") or "")[:800]]).lower()
        cue_hits = sum(1 for cue in cues if cue in text)
        scored.append((cue_hits, -len(row.get("topics_of_interest") or []), row.get("id", ""), row))
    scored.sort(reverse=True)
    return [row for cue_hits, _, _, row in scored if cue_hits > 0][:limit]


def build_prompt(
    *,
    label: str,
    rows: list[dict[str, Any]],
    positives: list[dict[str, Any]],
    negatives: list[dict[str, Any]],
    score_fns: list[dict[str, Any]],
    score_fps: list[dict[str, Any]],
) -> str:
    subset = [r for r in rows if label in (r.get("topics_of_interest") or [])]
    co_labels = Counter(t for r in subset for t in (r.get("topics_of_interest") or []) if t != label)
    cues = Counter()
    for row in subset:
        text = " ".join([row.get("title", ""), " ".join(row.get("keywords") or []), (row.get("body") or "")[:1500]]).lower()
        for cue in DEFAULT_CUES.get(label, []):
            if cue.lower() in text:
                cues[cue] += 1

    parts = [
        f"# Distill rationale for `{label}`",
        "",
        "You are helping improve static ASI for an OpenClaw multi-label GitHub classifier.",
        "Infer the human labeling concept from seed rows. The seed labels are ground truth; do not relabel them.",
        "",
        "Return concise markdown with these sections:",
        "1. Human concept represented by the label",
        "2. Positive assignment rules",
        "3. False-positive exclusions",
        "4. False-negative rescue cues",
        "5. Common co-labels and when to include both",
        "6. Adjacent-label tie-breakers",
        "7. A final GEPA-ready guidance block of 6-10 bullets",
        "",
        "Focus on reusable boundary rules, not row memorization.",
        "",
        "## Aggregate seed stats",
        "```json",
        json.dumps(
            {
                "label": label,
                "positive_rows": len(subset),
                "co_labels": co_labels.most_common(25),
                "cue_counts": cues.most_common(),
            },
            indent=2,
        ),
        "```",
    ]

    parts.extend(["", "## Positive seed rows"])
    for row in positives:
        parts.extend(["", "```text", raw_context(row), "```"])

    if negatives:
        parts.extend(["", "## Cue-bearing negative seed rows (label absent)"])
        for row in negatives:
            parts.extend(["", "```text", raw_context(row, 650), "```"])

    if score_fns or score_fps:
        parts.extend(["", "## Current validation mistakes involving this label"])
        if score_fns:
            parts.extend(["", "### False negatives"])
            for fail in score_fns[:8]:
                parts.extend(["", "```json", json.dumps(fail, indent=2, ensure_ascii=False)[:2200], "```"])
        if score_fps:
            parts.extend(["", "### False positives"])
            for fail in score_fps[:8]:
                parts.extend(["", "```json", json.dumps(fail, indent=2, ensure_ascii=False)[:2200], "```"])

    return "\n".join(parts) + "\n"


def build_structured_prompt(
    *,
    label: str,
    rows: list[dict[str, Any]],
    positives: list[dict[str, Any]],
    negatives: list[dict[str, Any]],
    score_fns: list[dict[str, Any]],
    score_fps: list[dict[str, Any]],
) -> str:
    prompt = build_prompt(
        label=label,
        rows=rows,
        positives=positives,
        negatives=negatives,
        score_fns=score_fns,
        score_fps=score_fps,
    )
    return (
        prompt
        + "\n"
        + "# Structured-output requirements\n\n"
        + "Return only JSON matching the provided schema. Keep it compact and reusable.\n"
        + "Do not include row IDs, issue/PR numbers, URLs, exact issue titles, or copied example text.\n"
        + "Do not write scenario-specific exact label bundles; generalize to cue classes and boundaries.\n"
    )


def structured_schema(label: str) -> dict[str, Any]:
    string_array = {
        "type": "array",
        "items": {"type": "string"},
        "maxItems": 8,
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": f"OpenClawLabelRationale_{label}",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "label",
            "concept",
            "positive_rules",
            "false_positive_exclusions",
            "false_negative_rescue_cues",
            "co_label_rules",
            "adjacent_tie_breakers",
            "gepa_ready_bullets",
        ],
        "properties": {
            "label": {"type": "string", "const": label},
            "concept": {"type": "string", "maxLength": 600},
            "positive_rules": string_array,
            "false_positive_exclusions": string_array,
            "false_negative_rescue_cues": string_array,
            "co_label_rules": {
                "type": "array",
                "maxItems": 8,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["with_label", "when"],
                    "properties": {
                        "with_label": {"type": "string"},
                        "when": {"type": "string", "maxLength": 300},
                    },
                },
            },
            "adjacent_tie_breakers": {
                "type": "array",
                "maxItems": 8,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["against_label", "rule"],
                    "properties": {
                        "against_label": {"type": "string"},
                        "rule": {"type": "string", "maxLength": 300},
                    },
                },
            },
            "gepa_ready_bullets": string_array,
        },
    }


def call_model(args: argparse.Namespace, prompt_path: Path, schema_path: Path | None = None) -> str:
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
    if schema_path is not None:
        cmd.extend(["--json-schema", str(schema_path)])
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)
    if proc.returncode:
        raise RuntimeError(f"fast-agent failed for {prompt_path} with exit {proc.returncode}\n{proc.stderr[-4000:]}")
    return proc.stdout


def main() -> int:
    args = parse_args()
    rows = load_jsonl(args.source)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for label in args.labels:
        positives = choose_positive_rows(rows, label, args.examples)
        negatives = choose_negative_rows(rows, label, args.negative_examples)
        score_fns, score_fps = load_score_examples(args.score, label)
        prompt = (build_structured_prompt if args.structured_json else build_prompt)(
            label=label,
            rows=rows,
            positives=positives,
            negatives=negatives,
            score_fns=score_fns,
            score_fps=score_fps,
        )
        prompt_path = args.output_dir / f"{label}.prompt.md"
        output_path = args.output_dir / f"{label}.json" if args.structured_json else args.output_dir / f"{label}.md"
        prompt_path.write_text(prompt, encoding="utf-8")
        schema_path = None
        if args.structured_json:
            schema_path = args.output_dir / f"{label}.schema.json"
            schema_path.write_text(json.dumps(structured_schema(label), indent=2), encoding="utf-8")
        if args.dry_run:
            print(f"wrote {prompt_path}")
            continue
        output = call_model(args, prompt_path, schema_path)
        output_path.write_text(output, encoding="utf-8")
        print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
