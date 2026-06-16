#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

PLACEHOLDER_RE = re.compile(r"{{\s*([A-Za-z0-9_.:/-]+)\s*}}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a captured OpenClaw labeler prompt from its agent card and variables."
    )
    parser.add_argument(
        "run_dir",
        nargs="?",
        type=Path,
        help=(
            "Captured run directory containing vanilla-labeler.md and "
            "candidate-0001/variables.json."
        ),
    )
    parser.add_argument("--agent-card", type=Path, help="Agent card/template to render.")
    parser.add_argument("--variables", type=Path, help="JSON file containing template variables.")
    parser.add_argument(
        "--candidate",
        default="candidate-0001",
        help="Candidate subdirectory name.",
    )
    parser.add_argument("--output", type=Path, help="Write rendered prompt to this file.")
    parser.add_argument(
        "--keep-file-placeholders",
        action="store_true",
        help="Leave {{file:path}} placeholders unresolved instead of inlining files.",
    )
    return parser.parse_args()


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    if end == -1:
        return text
    return text[end + len("\n---\n") :]


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"Expected a JSON object in {path}")
    return data


def resolve_paths(args: argparse.Namespace) -> tuple[Path, Path]:
    if args.run_dir:
        run_dir = args.run_dir
        agent_card = args.agent_card or run_dir / "vanilla-labeler.md"
        variables = args.variables or run_dir / args.candidate / "variables.json"
    else:
        if not args.agent_card or not args.variables:
            raise SystemExit("Provide either run_dir or both --agent-card and --variables.")
        agent_card = args.agent_card
        variables = args.variables
    return agent_card, variables


def find_project_root(path: Path) -> Path:
    for parent in [path, *path.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    return Path.cwd()


def render_template(
    template: str,
    variables: dict[str, Any],
    *,
    base_dir: Path,
    keep_file_placeholders: bool,
) -> str:
    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        replacement = match.group(0)
        if key.startswith("file:"):
            if keep_file_placeholders:
                return replacement
            file_path = Path(key.removeprefix("file:"))
            if not file_path.is_absolute():
                file_path = base_dir / file_path
            replacement = file_path.read_text(encoding="utf-8").strip()
        else:
            value = variables.get(key)
            if isinstance(value, str):
                replacement = value.rstrip()
            elif value is not None:
                replacement = json.dumps(value, indent=2, sort_keys=True)
        return replacement

    return PLACEHOLDER_RE.sub(replace, template).strip() + "\n"


def main() -> int:
    args = parse_args()
    agent_card, variables_path = resolve_paths(args)
    template = strip_frontmatter(agent_card.read_text(encoding="utf-8"))
    variables = load_json(variables_path)
    rendered = render_template(
        template,
        variables,
        base_dir=find_project_root(agent_card.resolve()),
        keep_file_placeholders=args.keep_file_placeholders,
    )
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
        print(args.output)
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
