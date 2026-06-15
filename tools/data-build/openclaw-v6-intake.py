#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
V6_DIR = ROOT / "datasets/openclaw-label-v7a/artifacts/spec"
V6_DOCS = ROOT / "datasets/openclaw-label-v7a/artifacts/docs"
DEFAULT_SOURCE = None
DEFAULT_COMPARISON_REFERENCE = None
DEFAULT_OUT_ROOT = ROOT / "runs/data-build/intake"
DEFAULT_STABILITY_RECORDS = None
SPEC_FILES = [
    V6_DIR / "allowed-topics-v6f.md",
    V6_DIR / "topic-boundary-guidance-v6h.md",
    V6_DIR / "task-boundary-overlay-v6h.md",
    V6_DIR / "teacher-card-v6h.md",
    V6_DIR / "teacher-template-v6-anchor-free.md",
    V6_DIR / "teacher-output-v6h.schema.json",
    V6_DIR / "seed-policy-overlay-v6h.md",
    V6_DIR / "seed-policy-vanilla-v6h.md",
    V6_DIR / "vanilla-asi-v6h-slim.md",
    V6_DOCS / "V6_SPEC_CHANGELOG.md",
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


def ids_from_jsonl(path: Path) -> list[str]:
    ids = []
    for row in load_jsonl(path):
        rid = row.get("id")
        if rid is None and isinstance(row.get("input"), dict):
            rid = row["input"].get("id")
        if rid is not None:
            ids.append(str(rid))
    return ids


def stability_ids(path: Path | None, bucket: str) -> list[str]:
    if path is None:
        raise SystemExit("--stability-records is required for stability-control selection.")
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


FOCUS_PROFILES: dict[str, list[tuple[str, int, list[str]]]] = {
    "v6h-slim": [
        (
            "tie_break_reliability_inference",
            42,
            [
                r"\breliabil",
                r"\btimeout\b",
                r"\bretry\b",
                r"\bhung\b|\bhang\b|\bfreeze\b",
                r"\binference\b",
                r"openai.compatible",
                r"\bollama\b|\blmstudio\b|\bvllm\b|\btgi\b|llama\.cpp",
                r"\bembedding",
                r"\bprovider\b",
            ],
        ),
        (
            "security_auth_sandbox",
            38,
            [
                r"\bsecurity\b",
                r"\bssrf\b",
                r"\bauth\b|\boauth\b|\bidentity\b",
                r"\btoken\b|\bsecret\b|\bapi key\b",
                r"\bsandbox",
                r"\bproxy\b|\begress\b|\ballowlist\b|\bbypass\b",
            ],
        ),
        (
            "agent_tooling_runtime",
            34,
            [
                r"\bagent",
                r"\btool calling\b|\btool.call",
                r"\bmcp\b",
                r"\bexec\b|\bcommand\b|\bshell\b",
                r"\bhook\b",
                r"\bskill\b|\bplugin\b|\bextension\b",
                r"\bcodex\b",
            ],
        ),
        (
            "sessions_gateway_queue",
            34,
            [
                r"\bsession",
                r"\bgateway\b",
                r"\bqueue\b|\bbacklog\b",
                r"\bparallel\b|\bconcurr",
                r"\brate.?limit\b",
                r"\bmessage.delivery\b|\bmessage delivery\b",
            ],
        ),
        (
            "config_api_surface",
            28,
            [
                r"\bconfig\b|\bsettings\b|openclaw\.json",
                r"\bschema\b",
                r"\bapi\b|\bcontract\b",
                r"\bcompatib",
                r"\bmodel lifecycle\b|\bmodel.lifecycle\b",
            ],
        ),
        (
            "ui_docs_ci_packaging",
            24,
            [
                r"\bui\b|\btui\b|\bdx\b",
                r"\bdoc\b|\breadme\b",
                r"\btest\b|\bci\b|\bworkflow\b",
                r"\bpackage\b|\bdeploy\b|\bdocker\b",
                r"\btelemetry\b|\busage\b",
            ],
        ),
    ]
}


def row_text(row: dict[str, Any]) -> str:
    values = []
    for key in ("id", "title", "target", "github_context", "body", "description", "diff"):
        value = row.get(key)
        if isinstance(value, str):
            values.append(value)
    labels = row.get("labels")
    if isinstance(labels, list):
        values.extend(str(label) for label in labels)
    return "\n".join(values).lower()


def select_sample_ids(
    source_rows: list[dict[str, Any]],
    *,
    sample_size: int,
    seed: int,
    excluded_ids: set[str],
    already_selected: list[str],
    focus_profile: str | None,
) -> tuple[list[str], dict[str, Any]]:
    selected = unique_in_order([rid for rid in already_selected if rid not in excluded_ids])
    selected_set = set(selected)
    available = [row for row in source_rows if row["id"] not in excluded_ids and row["id"] not in selected_set]
    if sample_size < len(selected):
        raise SystemExit(f"explicit row ids ({len(selected)}) exceed --sample-size {sample_size}")
    if sample_size > len(selected) + len(available):
        raise SystemExit(
            f"--sample-size {sample_size} exceeds available rows after exclusions "
            f"({len(selected) + len(available)})"
        )

    rng = random.Random(seed)
    bucket_counts: dict[str, int] = {}
    bucket_matches: dict[str, int] = {}

    if focus_profile:
        if focus_profile not in FOCUS_PROFILES:
            raise SystemExit(f"unknown --focus-profile {focus_profile}; options: {sorted(FOCUS_PROFILES)}")
        text_by_id = {row["id"]: row_text(row) for row in available}
        for bucket, quota, patterns in FOCUS_PROFILES[focus_profile]:
            candidates = [
                row["id"]
                for row in available
                if row["id"] not in selected_set
                and any(re.search(pattern, text_by_id[row["id"]]) for pattern in patterns)
            ]
            bucket_matches[bucket] = len(candidates)
            rng.shuffle(candidates)
            take = candidates[: max(0, min(quota, sample_size - len(selected)))]
            selected.extend(take)
            selected_set.update(take)
            bucket_counts[bucket] = len(take)
            if len(selected) >= sample_size:
                break

    remaining = [row["id"] for row in available if row["id"] not in selected_set]
    rng.shuffle(remaining)
    fill = remaining[: sample_size - len(selected)]
    selected.extend(fill)
    bucket_counts["deterministic_fill"] = len(fill)

    return selected, {
        "sample_size": sample_size,
        "seed": seed,
        "focus_profile": focus_profile,
        "excluded_ids": len(excluded_ids),
        "bucket_matches": bucket_matches,
        "bucket_selected": bucket_counts,
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Create reproducible v6 intake batch directories.")
    p.add_argument("--batch", required=True, help="Batch name, e.g. batch-001.")
    p.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    p.add_argument("--comparison-reference", type=Path, default=DEFAULT_COMPARISON_REFERENCE)
    p.add_argument("--out-root", type=Path, default=DEFAULT_OUT_ROOT)
    p.add_argument("--row-ids-file", type=Path, default=None)
    p.add_argument("--row-id", action="append", default=[])
    p.add_argument("--sample-size", type=int, default=None)
    p.add_argument("--exclude-ids-file", action="append", type=Path, default=[])
    p.add_argument("--exclude-jsonl", action="append", type=Path, default=[])
    p.add_argument(
        "--focus-profile",
        choices=sorted(FOCUS_PROFILES),
        default=None,
        help="Bias sampled rows toward a deterministic coverage profile before random fill.",
    )
    p.add_argument("--include-blind-agree-20", action="store_true")
    p.add_argument(
        "--control-from-all-equal",
        type=int,
        default=0,
        help="Add N deterministic controls from the stability records' all_equal bucket.",
    )
    p.add_argument("--stability-records", type=Path, default=DEFAULT_STABILITY_RECORDS)
    p.add_argument("--seed", type=int, default=611)
    p.add_argument("--overwrite", action="store_true")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if args.source is None:
        raise SystemExit(
            "--source is required. The raw v6 revalidation reservoir is not bundled in this clean repo."
        )
    if args.comparison_reference is None:
        raise SystemExit(
            "--comparison-reference is required. The comparison reference is not bundled in this clean repo."
        )
    batch_dir = args.out_root / args.batch
    if batch_dir.exists() and not args.overwrite:
        raise SystemExit(f"{batch_dir} exists; pass --overwrite to replace batch files")
    batch_dir.mkdir(parents=True, exist_ok=True)

    source_rows = load_jsonl(args.source)
    source_by_id = {row["id"]: row for row in source_rows}
    if len(source_by_id) != len(source_rows):
        raise SystemExit("source has duplicate ids")
    comparison_by_id = {row["id"]: row for row in load_jsonl(args.comparison_reference)}

    ids: list[str] = []
    if args.row_ids_file:
        ids.extend(read_id_file(args.row_ids_file))
    ids.extend(args.row_id)
    if args.include_blind_agree_20:
        ids.extend(stability_ids(args.stability_records, "blind_agree_not_current"))
    ids = unique_in_order(ids)

    excluded_ids: set[str] = set()
    for path in args.exclude_ids_file:
        excluded_ids.update(read_id_file(path))
    for path in args.exclude_jsonl:
        excluded_ids.update(ids_from_jsonl(path))

    if args.control_from_all_equal:
        controls = [
            rid
            for rid in stability_ids(args.stability_records, "all_equal")
            if rid not in set(ids) and rid not in excluded_ids
        ]
        rng = random.Random(args.seed)
        rng.shuffle(controls)
        ids.extend(sorted(controls[: args.control_from_all_equal]))

    selection_summary: dict[str, Any] = {}
    if args.sample_size is not None:
        ids, selection_summary = select_sample_ids(
            source_rows,
            sample_size=args.sample_size,
            seed=args.seed,
            excluded_ids=excluded_ids,
            already_selected=ids,
            focus_profile=args.focus_profile,
        )

    if not ids:
        raise SystemExit("no row ids selected")
    missing = sorted(set(ids) - set(source_by_id))
    if missing:
        raise SystemExit(f"row ids missing from source: {missing[:20]}")

    selected = [source_by_id[row["id"]] for row in source_rows if row["id"] in set(ids)]
    selected_ids = [row["id"] for row in selected]
    selected_comparison = [
        comparison_by_id[rid] for rid in selected_ids if rid in comparison_by_id
    ]

    (batch_dir / "row-ids.txt").write_text("".join(f"{rid}\n" for rid in selected_ids), encoding="utf-8")
    write_jsonl(batch_dir / "input.jsonl", selected)
    write_jsonl(batch_dir / "comparison-reference.jsonl", selected_comparison)

    manifest = {
        "batch": args.batch,
        "source": str(args.source),
        "comparison_reference": str(args.comparison_reference),
        "row_count": len(selected),
        "row_ids_sha256": hashlib.sha256("\n".join(selected_ids).encode("utf-8")).hexdigest(),
        "selection": selection_summary
        or {
            "explicit_rows": len(selected_ids),
            "excluded_ids": len(excluded_ids),
        },
        "spec_files": [
            {"path": str(path), "sha256": sha256(path), "bytes": path.stat().st_size}
            for path in SPEC_FILES
        ],
    }
    (batch_dir / "spec-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (batch_dir / "selection-summary.json").write_text(
        json.dumps(manifest["selection"], indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"batch_dir": str(batch_dir), "rows": len(selected)}, indent=2))


if __name__ == "__main__":
    main()
