#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "src/openclaw_gepa/openclaw_benchmark.py"
DEFAULT_OUTPUT = ROOT / "eval/openclaw/topic-boundary-guidance.md"


def load_topic_hints() -> dict[str, dict[str, str]]:
    spec = importlib.util.spec_from_file_location("openclaw_benchmark", BENCHMARK)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {BENCHMARK}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.TOPIC_HINTS


def render(topic_hints: dict[str, dict[str, str]]) -> str:
    lines = [
        "# OpenClaw topic-boundary guidance",
        "",
        "Generated from `src/openclaw_gepa/openclaw_benchmark.py` `TOPIC_HINTS`.",
        "Keep this file synchronized with the benchmark dynamic ASI; do not hand-edit",
        "topic guidance here without updating/checking the source hints.",
        "",
        "Use these as boundary overlays on top of the allowed-topic taxonomy. They are",
        "not extra labels and do not replace the topic definitions.",
        "",
    ]
    for topic, hints in topic_hints.items():
        lines.extend([
            f"## `{topic}`",
            "",
            f"- False-positive guard: {hints['fp']}",
            f"- False-negative guard: {hints['fn']}",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description="Sync topic-boundary guidance from openclaw_benchmark.TOPIC_HINTS.")
    p.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--check", action="store_true", help="Fail if output is not synchronized.")
    args = p.parse_args()

    expected = render(load_topic_hints())
    if args.check:
        actual = args.output.read_text(encoding="utf-8") if args.output.exists() else ""
        if actual != expected:
            print(f"not synchronized: {args.output}")
            return 1
        print(f"synchronized: {args.output}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(expected, encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
