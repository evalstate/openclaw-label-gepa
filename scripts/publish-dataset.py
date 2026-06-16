#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shlex
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish a frozen OpenClaw label dataset bundle.")
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--repo-id", required=True)
    parser.add_argument(
        "--write-manifest",
        action="store_true",
        help="Write publication-manifest.json into the bundle.",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def jsonl_rows(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def bundle_manifest(bundle: Path) -> dict[str, Any]:
    files = sorted(
        path
        for path in bundle.rglob("*")
        if path.is_file() and path.name != "publication-manifest.json"
    )
    jsonl_files = [path for path in files if path.suffix == ".jsonl"]
    return {
        "bundle": bundle.as_posix(),
        "file_count": len(files),
        "jsonl_row_counts": {rel(path, bundle): jsonl_rows(path) for path in jsonl_files},
        "files": [
            {
                "path": rel(path, bundle),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in files
        ],
    }


def print_commands(bundle: Path, repo_id: str) -> None:
    quoted_repo = shlex.quote(repo_id)
    quoted_bundle = shlex.quote(bundle.as_posix())
    print()
    print("Publish commands:")
    print("hf auth login")
    print(f"hf repos create {quoted_repo} --type dataset --private --exist-ok")
    print(
        "hf upload "
        f"{quoted_repo} {quoted_bundle} "
        "--type dataset "
        "--commit-message 'Publish OpenClaw label v7a dataset'"
    )
    print()
    print("Download command:")
    print(
        "hf download "
        f"{quoted_repo} "
        "--type dataset "
        "--local-dir .hf/openclaw-label-v7a"
    )


def main() -> int:
    args = parse_args()
    bundle = args.bundle
    manifest = bundle_manifest(bundle)
    print(f"repo_id={args.repo_id}")
    print(f"bundle={bundle}")
    print(f"files={manifest['file_count']}")
    print("jsonl_row_counts:")
    for path, rows in manifest["jsonl_row_counts"].items():
        print(f"  {path}: {rows}")
    if args.write_manifest:
        output = bundle / "publication-manifest.json"
        output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {output}")
    print_commands(bundle, args.repo_id)
    if args.dry_run:
        return 0
    msg = "publishing is command-only for now; run the emitted hf commands after review"
    raise SystemExit(msg)


if __name__ == "__main__":
    raise SystemExit(main())
