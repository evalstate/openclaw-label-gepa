#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from openclaw_gepa.openclaw_benchmark import REF, load_jsonl


DEFAULT_CUES: dict[str, list[str]] = {
    "agent_runtime": ["agent runtime", "RuntimePlan", "runtime plan", "harness", "embedded runner", "attempt", "agent transport", "child task", "finalLlmOutcome", "model turn", "assistant message", "agent cli", "runner", "pi"],
    "queueing": ["queue", "queued", "queueing", "yield", "yielded", "waiting", "pending", "concurrency", "serial", "backpressure", "dispatch", "fan-out", "startup ordering", "child completion", "sidecar startup"],
    "exec_tools": ["exec", "command", "shell", "pty", "subprocess", "spawn", "stdio", "allowlist", "allowedHosts", "browser command", "mcp stdio", "exit code", "sigkill", "env vars", "process"],
    "skills_plugins": ["skill", "skills", "plugin", "plugins", "extension", "memory-core", "skill prelude", "managed skills", "SecretRef"],
    "api_surface": ["api", "http", "endpoint", "/v1", "sse", "schema", "request", "response", "contract", "cli flag", "payload", "streaming", "event"],
    "coding_agents": ["codex", "acp", "acpx", "subagent", "sub-agent", "agent runtime", "RuntimePlan", "runtime plan", "harness", "embedded runner", "pi", "claude code", "approvals", "sandbox", "child task", "runner", "compaction", "durable", "coding agent", "agent orchestration", "tool-use"],
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Summarize seed rows for selected OpenClaw labels.")
    p.add_argument("labels", nargs="+")
    p.add_argument("--source", type=Path, default=REF / "seed.jsonl")
    p.add_argument("--examples", type=int, default=20)
    p.add_argument("--json", action="store_true", help="Emit JSON instead of markdown-ish text.")
    return p.parse_args()


def analyze(rows: list[dict], label: str, examples: int) -> dict:
    subset = [r for r in rows if label in (r.get("topics_of_interest") or [])]
    co_labels = Counter(t for r in subset for t in (r.get("topics_of_interest") or []) if t != label)
    cues = Counter()
    cue_terms = DEFAULT_CUES.get(label, [])
    for r in subset:
        text = " ".join([r.get("title", ""), " ".join(r.get("keywords") or []), (r.get("body") or "")[:1500]]).lower()
        for cue in cue_terms:
            if cue.lower() in text:
                cues[cue] += 1
    return {
        "label": label,
        "count": len(subset),
        "co_labels": co_labels.most_common(25),
        "cue_counts": cues.most_common(),
        "examples": [
            {
                "id": r["id"],
                "title": r.get("title"),
                "topics": r.get("topics_of_interest") or [],
                "keywords": r.get("keywords") or [],
            }
            for r in subset[:examples]
        ],
    }


def main() -> int:
    args = parse_args()
    rows = load_jsonl(args.source)
    payload = [analyze(rows, label, args.examples) for label in args.labels]
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    for item in payload:
        print(f"\n## {item['label']} ({item['count']} rows)")
        print("co-labels:", item["co_labels"])
        print("cue counts:", item["cue_counts"])
        for ex in item["examples"]:
            print(f"- {ex['id']} | {ex['title']} | labels={ex['topics']} | keywords={ex['keywords']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
