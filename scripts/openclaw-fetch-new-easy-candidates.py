#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import subprocess
from pathlib import Path
from typing import Any

from openclaw_gepa.openclaw_benchmark import github_context, write_jsonl

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "eval/openclaw/easy-set-pilot"
DEFAULT_EXCLUDES = [
    PILOT / "easy-final-v4.jsonl",
    PILOT / "easy-final-v4-confusion-bucket.jsonl",
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Fetch reproducible OpenClaw GitHub rows for new easy-set teacher labeling.")
    p.add_argument("--repo", default="openclaw/openclaw")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--pool-limit", type=int, default=500)
    p.add_argument("--seed", type=int, default=20260610)
    p.add_argument("--search", default="updated:<2026-06-11 sort:updated-desc")
    p.add_argument("--exclude", type=Path, action="append", default=list(DEFAULT_EXCLUDES))
    p.add_argument("--selection", choices=["sample", "newest"], default="sample")
    return p.parse_args()


def load_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    ids = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if isinstance(row.get("id"), str):
            ids.add(row["id"])
    return ids


def gh_json(args: list[str]) -> list[dict[str, Any]]:
    completed = subprocess.run(["gh", *args], cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
    data = json.loads(completed.stdout or "[]")
    if not isinstance(data, list):
        raise RuntimeError(f"expected list from gh, got {type(data).__name__}")
    return data


def norm_user(value: Any) -> str | None:
    if isinstance(value, dict):
        login = value.get("login")
        return login if isinstance(login, str) else None
    return None


def norm_labels(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    out = []
    for item in value:
        if isinstance(item, dict) and isinstance(item.get("name"), str):
            out.append(item["name"])
        elif isinstance(item, str):
            out.append(item)
    return out


def norm_comments(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    comments = []
    for item in value[-8:]:
        if not isinstance(item, dict):
            continue
        comments.append(
            {
                "author": norm_user(item.get("author")),
                "created_at": item.get("createdAt"),
                "body": item.get("body") or "",
            }
        )
    return comments


def norm_files(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    paths = []
    for item in value[:80]:
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            paths.append(item["path"])
        elif isinstance(item, str):
            paths.append(item)
    return paths


def prepared(row: dict[str, Any], *, repo: str, item_type: str) -> dict[str, Any]:
    number = row["number"]
    title = row.get("title") or ""
    raw = {
        "repo": repo,
        "item_type": item_type,
        "number": number,
        "url": row.get("url"),
        "title": title,
        "state": row.get("state"),
        "author": norm_user(row.get("author")),
        "labels": norm_labels(row.get("labels")),
        "body": row.get("body") or "",
        "comments": norm_comments(row.get("comments")),
        "changed_files": norm_files(row.get("files")),
        "changed_file_count": len(norm_files(row.get("files"))),
        "diff": "",
        "context_caveats": ["fetched_from_github_without_diff"],
    }
    rid = f"{repo.replace('/', '-')}-{number}"
    target = f"{repo} {'github_pr' if item_type == 'github_pr' else 'github_issue'} #{number}: {title}"
    return {
        "id": rid,
        "repo": repo,
        "item_type": item_type,
        "number": number,
        "url": row.get("url"),
        "title": title,
        "target": target,
        "github_context": github_context(raw),
        "expected_topics": [],
        "expected_topics_json": "[]",
        "teacher_source": "github_fetch_v4_expansion",
        "fetched_updated_at": row.get("updatedAt"),
        "fetched_created_at": row.get("createdAt"),
    }


def main() -> int:
    args = parse_args()
    excluded = set().union(*(load_ids(path) for path in args.exclude))
    common_fields = "number,title,url,state,author,labels,body,comments,createdAt,updatedAt"
    issue_rows = gh_json(
        [
            "issue",
            "list",
            "--repo",
            args.repo,
            "--state",
            "all",
            "--limit",
            str(args.pool_limit),
            "--search",
            args.search,
            "--json",
            common_fields,
        ]
    )
    pr_rows = gh_json(
        [
            "pr",
            "list",
            "--repo",
            args.repo,
            "--state",
            "all",
            "--limit",
            str(args.pool_limit),
            "--search",
            args.search,
            "--json",
            common_fields,
        ]
    )
    rows = [prepared(r, repo=args.repo, item_type="github_issue") for r in issue_rows]
    rows.extend(prepared(r, repo=args.repo, item_type="github_pr") for r in pr_rows)
    by_id = {r["id"]: r for r in rows if r["id"] not in excluded}
    pool = sorted(by_id.values(), key=lambda r: (r.get("fetched_updated_at") or "", r["id"]), reverse=True)
    if args.selection == "sample":
        rng = random.Random(args.seed)
        selected = rng.sample(pool, min(args.limit, len(pool)))
        selected.sort(key=lambda r: r["id"])
    else:
        selected = pool[: args.limit]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output, selected)
    manifest = {
        "repo": args.repo,
        "search": args.search,
        "seed": args.seed,
        "selection": args.selection,
        "pool_limit_per_kind": args.pool_limit,
        "issue_rows_fetched": len(issue_rows),
        "pr_rows_fetched": len(pr_rows),
        "excluded_ids": len(excluded),
        "candidate_pool_after_excludes": len(pool),
        "selected_rows": len(selected),
        "output": str(args.output),
        "exclude_files": [str(p) for p in args.exclude],
    }
    args.output.with_suffix(".manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
