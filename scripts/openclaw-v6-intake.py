#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
V6_DIR = ROOT / "eval/openclaw/easy-set-pilot/v6"
DEFAULT_SOURCE = V6_DIR / "revalidation-input.jsonl"
DEFAULT_V5_GOLD = V6_DIR / "v5-gold-reference.jsonl"
DEFAULT_OUT_ROOT = ROOT / "runs/easy-set-v6a/v6a-databuild/intake"
DEFAULT_STABILITY_RECORDS = (
    ROOT
    / "runs/easy-set-v5/label-audit/blind-stability-train-gpt55-opus/stability-records.jsonl"
)
SPEC_FILES = [
    V6_DIR / "allowed-topics-v6a.md",
    V6_DIR / "topic-boundary-guidance-v6a.md",
    V6_DIR / "task-boundary-overlay-v6.md",
    V6_DIR / "teacher-card-v6.md",
    V6_DIR / "teacher-template-v6-anchor-free.md",
    V6_DIR / "teacher-output.schema.json",
    V6_DIR / "V6_SPEC_CHANGELOG.md",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_id_file(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def stability_ids(path: Path, bucket: str) -> list[str]:
    if not path.exists():
        return []
    ids = []
    for row in load_jsonl(path):
        if row.get("bucket") == bucket:
            ids.append(str(row["id"]))
    return ids


def unique_in_order(ids: list[str]) -> list[str]:
    seen = set()
    out = []
    for rid in ids:
        if rid not in seen:
            seen.add(rid)
            out.append(rid)
    return out


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Create reproducible v6 intake batch directories.")
    p.add_argument("--batch", required=True, help="Batch name, e.g. batch-001.")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--v5-gold", type=Path, default=DEFAULT_V5_GOLD)
    p.add_argument("--out-root", type=Path, default=DEFAULT_OUT_ROOT)
    p.add_argument("--row-ids-file", type=Path, default=None)
    p.add_argument("--row-id", action="append", default=[])
    p.add_argument("--include-blind-agree-20", action="store_true")
    p.add_argument(
        "--control-from-all-equal",
        type=int,
        default=0,
        help="Add N deterministic controls from v5 blind all_equal rows.",
    )
    p.add_argument("--stability-records", type=Path, default=DEFAULT_STABILITY_RECORDS)
    p.add_argument("--seed", type=int, default=611)
    p.add_argument("--overwrite", action="store_true")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    batch_dir = args.out_root / args.batch
    if batch_dir.exists() and not args.overwrite:
        raise SystemExit(f"{batch_dir} exists; pass --overwrite to replace batch files")
    batch_dir.mkdir(parents=True, exist_ok=True)

    source_rows = load_jsonl(args.source)
    source_by_id = {row["id"]: row for row in source_rows}
    if len(source_by_id) != len(source_rows):
        raise SystemExit("source has duplicate ids")
    gold_by_id = {row["id"]: row for row in load_jsonl(args.v5_gold)}

    ids: list[str] = []
    if args.row_ids_file:
        ids.extend(read_id_file(args.row_ids_file))
    ids.extend(args.row_id)
    if args.include_blind_agree_20:
        ids.extend(stability_ids(args.stability_records, "blind_agree_not_current"))
    ids = unique_in_order(ids)

    if args.control_from_all_equal:
        controls = [rid for rid in stability_ids(args.stability_records, "all_equal") if rid not in set(ids)]
        rng = random.Random(args.seed)
        rng.shuffle(controls)
        ids.extend(sorted(controls[: args.control_from_all_equal]))

    if not ids:
        raise SystemExit("no row ids selected")
    missing = sorted(set(ids) - set(source_by_id))
    if missing:
        raise SystemExit(f"row ids missing from source: {missing[:20]}")

    selected = [source_by_id[row["id"]] for row in source_rows if row["id"] in set(ids)]
    selected_ids = [row["id"] for row in selected]
    selected_gold = [gold_by_id[rid] for rid in selected_ids if rid in gold_by_id]

    (batch_dir / "row-ids.txt").write_text("".join(f"{rid}\n" for rid in selected_ids), encoding="utf-8")
    write_jsonl(batch_dir / "input.jsonl", selected)
    write_jsonl(batch_dir / "v5-gold-reference.jsonl", selected_gold)

    manifest = {
        "batch": args.batch,
        "source": str(args.source),
        "v5_gold": str(args.v5_gold),
        "row_count": len(selected),
        "row_ids_sha256": hashlib.sha256("\n".join(selected_ids).encode("utf-8")).hexdigest(),
        "spec_files": [
            {"path": str(path), "sha256": sha256(path), "bytes": path.stat().st_size}
            for path in SPEC_FILES
        ],
    }
    (batch_dir / "spec-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({"batch_dir": str(batch_dir), "rows": len(selected)}, indent=2))


if __name__ == "__main__":
    main()
