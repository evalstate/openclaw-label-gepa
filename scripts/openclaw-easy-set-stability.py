#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import itertools
import json
import os
import random
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, pstdev
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STABILITY_ROOT = ROOT / "runs" / "openclaw-easy-set-stability"
VANILLA_RUN_ROOT = ROOT / "runs" / "openclaw-vanilla-f1-gepa"
DEFAULT_INPUT = ROOT / "eval/openclaw/easy-set-pilot/easy-final-v2-test.jsonl"
DEFAULT_CARD = ROOT / "eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v2.md"
DEFAULT_PLAIN_CARD = ROOT / "eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-plain-v2.md"
DEFAULT_TOPICS = ROOT / "eval/openclaw/easy-set-pilot/allowed-topics-v2.md"
DEFAULT_POLICY = ROOT / "eval/openclaw/easy-set-pilot/seed-policy-vanilla-v3.md"
DEFAULT_TEMPLATE = ROOT / "eval/openclaw/task-template.md"
DEFAULT_SCHEMA = ROOT / "eval/openclaw/output.schema.json"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run repeated OpenClaw easy-set evaluations and report row-level stability.")
    p.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    p.add_argument("--agent-card", type=Path, default=DEFAULT_CARD)
    p.add_argument("--allowed-topics", type=Path, default=DEFAULT_TOPICS)
    p.add_argument("--seed-policy", type=Path, default=DEFAULT_POLICY)
    p.add_argument("--agent-name", default=None, help="Agent name in the AgentCard. Defaults to vanilla/plain agent names.")
    p.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    p.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    p.add_argument("--model", required=True)
    p.add_argument("--runs", type=int, default=3)
    p.add_argument("--parallel", type=int, default=4)
    p.add_argument(
        "--repeat-parallel",
        type=int,
        default=1,
        help="Run this many repeat jobs concurrently. Total row concurrency is repeat_parallel * parallel.",
    )
    p.add_argument("--run-name", required=True)
    p.add_argument("--run-root", type=Path, default=STABILITY_ROOT, help="Directory under which the stability run directory is created.")
    p.add_argument(
        "--wrapped-run-root",
        type=Path,
        default=VANILLA_RUN_ROOT,
        help="Directory for wrapped openclaw-vanilla-f1-gepa.py evaluate-only repeats.",
    )
    p.add_argument("--plain-labels", action="store_true")
    p.add_argument("--score-mode", choices=["f1", "row-aware"], default="row-aware")
    p.add_argument("--no-trackio", action="store_true", default=True, help="Disable Trackio for repeat stability runs (default).")
    p.add_argument("--trackio", dest="no_trackio", action="store_false", help="Enable Trackio in wrapped repeat runs.")
    p.add_argument(
        "--trackio-project",
        default=None,
        help="Enable fast-agent batch Trackio monitoring for --direct-batch repeats and log under this project.",
    )
    p.add_argument("--trackio-group", default=None, help="Trackio group tag; defaults to --run-name.")
    p.add_argument("--trackio-space-id", default=None)
    p.add_argument("--trackio-server-url", default=None)
    p.add_argument("--trackio-every", type=int, default=None, help="Log batch metrics every N rows.")
    p.add_argument("--sample-size", type=int, default=None)
    p.add_argument("--seed", type=int, default=55)
    p.add_argument("--row-ids", nargs="*", default=None)
    p.add_argument("--row-ids-file", type=Path, default=None)
    p.add_argument("--overwrite", action="store_true")
    p.add_argument(
        "--direct-batch",
        action="store_true",
        help="Run fast-agent batch directly instead of wrapping openclaw-vanilla-f1-gepa.py. Use for teacher/generator cards.",
    )
    p.add_argument("--keep-vanilla-runs", action="store_true", help="Do not copy/delete wrapped openclaw-vanilla-f1-gepa run dirs; reports still reference them.")
    return p.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def select_rows(rows: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    wanted: set[str] | None = None
    if args.row_ids:
        wanted = set(args.row_ids)
    if args.row_ids_file:
        file_ids = {line.strip() for line in args.row_ids_file.read_text(encoding="utf-8").splitlines() if line.strip()}
        wanted = file_ids if wanted is None else wanted | file_ids
    if wanted is not None:
        by_id = {row["id"]: row for row in rows}
        missing = sorted(wanted - set(by_id))
        if missing:
            raise SystemExit(f"row IDs not found in input: {missing[:10]}")
        rows = [by_id[rid] for rid in rows_ids_in_input_order(rows, wanted)]
    if args.sample_size is not None:
        if args.sample_size > len(rows):
            raise SystemExit(f"--sample-size {args.sample_size} exceeds selected rows {len(rows)}")
        rng = random.Random(args.seed)
        rows = rng.sample(rows, args.sample_size)
        rows.sort(key=lambda r: r["id"])
    return rows


def rows_ids_in_input_order(rows: list[dict[str, Any]], wanted: set[str]) -> list[str]:
    return [row["id"] for row in rows if row["id"] in wanted]


def norm_topics(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        parts = [x.strip().strip("`'") for x in re.split(r"[,\n]", value) if x.strip()]
        return tuple(sorted(set(parts)))
    if isinstance(value, list):
        return tuple(sorted({str(x).strip() for x in value if str(x).strip()}))
    return ()


def expected_topics(row: dict[str, Any]) -> tuple[str, ...]:
    return norm_topics(row.get("expected_topics") or row.get("topics_of_interest") or row.get("ds4_topics"))


def predicted_topics(result_row: dict[str, Any]) -> tuple[str, ...]:
    result = result_row.get("result")
    if isinstance(result, dict):
        return norm_topics(result.get("topics_of_interest") or result.get("topics") or result.get("labels"))
    return norm_topics(result)


def jaccard(a: tuple[str, ...], b: tuple[str, ...]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / len(sa | sb)


def symdiff(a: tuple[str, ...], b: tuple[str, ...]) -> int:
    return len(set(a) ^ set(b))


def load_score(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    side = data.get("side_info", data)
    scores = side.get("scores", {})
    details = side.get("score_details", {})
    return {"raw": data, "scores": scores, "details": details}


def numeric_metric(score: dict[str, Any], key: str) -> float | None:
    for section in ("scores", "details"):
        value = score.get(section, {}).get(key)
        if isinstance(value, int | float):
            return float(value)
    return None


def run_repeat(args: argparse.Namespace, stability_dir: Path, selected_input: Path, idx: int) -> dict[str, Any]:
    repeat_name = f"{args.run_name}-repeat-{idx:02d}"
    vanilla_dir = args.wrapped_run_root / repeat_name
    repeat_dir = stability_dir / f"repeat-{idx:02d}"
    if args.overwrite:
        shutil.rmtree(vanilla_dir, ignore_errors=True)
        shutil.rmtree(repeat_dir, ignore_errors=True)
    if (repeat_dir / "score.json").exists() and (repeat_dir / "results.jsonl").exists():
        return {"repeat": idx, "run_name": repeat_name, "vanilla_run_dir": str(vanilla_dir), "repeat_dir": str(repeat_dir), "status": "cached"}

    if args.direct_batch:
        return run_direct_batch_repeat(args, stability_dir, selected_input, idx, repeat_name, repeat_dir)

    cmd = [
        sys.executable,
        str(ROOT / "scripts/openclaw-vanilla-f1-gepa.py"),
        "--evaluate-only",
        "--input",
        str(selected_input),
        "--agent-card",
        str(args.agent_card),
        "--allowed-topics",
        str(args.allowed_topics),
        "--seed-policy",
        str(args.seed_policy),
        "--model",
        args.model,
        "--run-name",
        repeat_name,
        "--run-root",
        str(args.wrapped_run_root),
        "--parallel",
        str(args.parallel),
        "--score-mode",
        args.score_mode,
    ]
    if args.plain_labels:
        cmd.append("--plain-labels")
    if args.no_trackio:
        cmd.append("--no-trackio")

    log_path = stability_dir / f"repeat-{idx:02d}.log"
    with log_path.open("w", encoding="utf-8") as log:
        proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=log, stderr=subprocess.STDOUT)
    if proc.returncode != 0:
        raise SystemExit(f"repeat {idx} failed with exit {proc.returncode}; see {log_path}")

    candidate = vanilla_dir / "candidate-0001"
    repeat_dir.mkdir(parents=True, exist_ok=True)
    for name in ["results.jsonl", "score.json", "batch-summary.json", "telemetry.jsonl", "policy.md", "variables.json"]:
        src = candidate / name
        if src.exists():
            shutil.copy2(src, repeat_dir / name)
    for name in ["evaluate-only.json", "input.jsonl", "seed-policy.md", "allowed-topics.md", "openclaw-vanilla-labeler.md"]:
        src = vanilla_dir / name
        if src.exists():
            shutil.copy2(src, repeat_dir / name)
    (repeat_dir / "vanilla-run-dir.txt").write_text(str(vanilla_dir) + "\n", encoding="utf-8")
    return {"repeat": idx, "run_name": repeat_name, "vanilla_run_dir": str(vanilla_dir), "repeat_dir": str(repeat_dir), "status": "complete"}


def infer_agent_name(args: argparse.Namespace) -> str:
    if args.agent_name:
        return args.agent_name
    return "openclaw_vanilla_labeler_plain" if args.plain_labels else "openclaw_vanilla_labeler"


def run_direct_batch_repeat(
    args: argparse.Namespace,
    stability_dir: Path,
    selected_input: Path,
    idx: int,
    repeat_name: str,
    repeat_dir: Path,
) -> dict[str, Any]:
    repeat_dir.mkdir(parents=True, exist_ok=True)
    output = repeat_dir / "results.jsonl"
    summary = repeat_dir / "batch-summary.json"
    telemetry = repeat_dir / "telemetry.jsonl"
    log_path = stability_dir / f"repeat-{idx:02d}.log"
    cmd = [
        os.environ.get("FAST_AGENT_BIN", "fast-agent"),
        "--no-update-check",
        "--env",
        str(ROOT / ".fast-agent"),
        "batch",
        "run",
        "--input",
        str(selected_input),
        "--output",
        str(output),
        "--agent-card",
        str(args.agent_card),
        "--agent",
        infer_agent_name(args),
        "--template",
        str(args.template),
        "--model",
        args.model,
        "--parallel",
        str(args.parallel),
        "--summary-output",
        str(summary),
        "--telemetry-output",
        str(telemetry),
        "--include-input",
        "--overwrite",
        "--no-progress",
        "--no-final-summary",
    ]
    if args.schema and not args.plain_labels:
        cmd.extend(["--json-schema", str(args.schema)])
    if args.trackio_project:
        cmd.extend(["--project", args.trackio_project, "--run-name", repeat_name])
        cmd.extend(["--group", args.trackio_group or args.run_name])
        if args.trackio_space_id:
            cmd.extend(["--trackio-space-id", args.trackio_space_id])
        if args.trackio_server_url:
            cmd.extend(["--trackio-server-url", args.trackio_server_url])
        if args.trackio_every:
            cmd.extend(["--trackio-every", str(args.trackio_every)])
    with log_path.open("w", encoding="utf-8") as log:
        proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=log, stderr=subprocess.STDOUT)
    if proc.returncode != 0:
        raise SystemExit(f"repeat {idx} failed with exit {proc.returncode}; see {log_path}")
    shutil.copy2(args.agent_card, repeat_dir / "agent-card.md")
    shutil.copy2(args.template, repeat_dir / "template.md")
    if args.schema and args.schema.exists():
        shutil.copy2(args.schema, repeat_dir / "schema.json")
    score_direct_repeat(selected_input, output, repeat_dir / "score.json", args.score_mode)
    return {"repeat": idx, "run_name": repeat_name, "vanilla_run_dir": None, "repeat_dir": str(repeat_dir), "status": "complete"}


def score_direct_repeat(input_path: Path, result_path: Path, score_path: Path, score_mode: str) -> None:
    expected = {row["id"]: expected_topics(row) for row in load_jsonl(input_path)}
    rows = load_jsonl(result_path)
    tp = fp = fn = exact = 0
    row_jaccards: list[float] = []
    row_symdiffs: list[int] = []
    predicted_counts: list[int] = []
    expected_counts: list[int] = []
    valid = 0
    failures = []
    for rr in rows:
        rid = (rr.get("input") or {}).get("id")
        if rid not in expected:
            continue
        pred = predicted_topics(rr)
        exp = expected[rid]
        ok = bool(rr.get("ok")) and bool(pred or not exp)
        valid += int(bool(rr.get("ok")))
        sp, se = set(pred), set(exp)
        tp += len(sp & se)
        fp += len(sp - se)
        fn += len(se - sp)
        exact += int(sp == se)
        row_jaccards.append(jaccard(pred, exp))
        row_symdiffs.append(symdiff(pred, exp))
        predicted_counts.append(len(pred))
        expected_counts.append(len(exp))
        if sp != se:
            failures.append(
                {
                    "id": rid,
                    "title": (rr.get("input") or {}).get("title") or (rr.get("input") or {}).get("target", ""),
                    "expected": list(exp),
                    "actual": list(pred),
                    "false_positives": sorted(sp - se),
                    "false_negatives": sorted(se - sp),
                    "row_score": jaccard(pred, exp),
                }
            )
    precision = tp / (tp + fp) if tp + fp else 1.0
    recall = tp / (tp + fn) if tp + fn else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    avg_sym = mean(row_symdiffs) if row_symdiffs else 0.0
    row_exact = exact / max(len(expected), 1)
    avg_jaccard = mean(row_jaccards) if row_jaccards else 0.0
    if score_mode == "row-aware":
        gepa_score = 0.50 * f1 + 0.20 * row_exact + 0.30 * avg_jaccard
    else:
        gepa_score = 0.70 * f1 + 0.20 * row_exact + 0.10 * avg_jaccard
    report = {
        "score": gepa_score,
        "side_info": {
            "scores": {
                "gepa_score": gepa_score,
                "topic_micro_f1": f1,
                "row_exact_accuracy": row_exact,
                "avg_row_jaccard": avg_jaccard,
                "row_symdiff_score": 1.0 / (1.0 + avg_sym),
            },
            "score_details": {
                "topic_micro_precision": precision,
                "topic_micro_recall": recall,
                "exact_match": row_exact,
                "row_exact_accuracy": row_exact,
                "avg_row_jaccard": avg_jaccard,
                "avg_row_symdiff": avg_sym,
                "valid_json": valid / max(len(expected), 1),
                "false_positives": fp,
                "false_negatives": fn,
                "avg_predicted_topics": mean(predicted_counts) if predicted_counts else 0.0,
                "avg_expected_topics": mean(expected_counts) if expected_counts else 0.0,
            },
            "evaluated": len(expected),
            "failures": sorted(failures, key=lambda r: r["row_score"])[:20],
        },
    }
    score_path.write_text(json.dumps(report, indent=2), encoding="utf-8")


def classify_row(exact_rate: float, pairwise_j: float, avg_sym: float, unique_sets: int, runs: int, invalid: bool) -> str:
    if invalid:
        return "invalid_or_failed"
    if exact_rate >= 0.90 and pairwise_j >= 0.95:
        return "stable_correct"
    if exact_rate < 0.50 and pairwise_j >= 0.90:
        return "stable_wrong"
    if pairwise_j >= 0.75 and avg_sym <= 1.25:
        return "unstable_near"
    if pairwise_j < 0.75 or unique_sets >= min(3, runs):
        return "unstable_boundary"
    return "review"


def build_report(stability_dir: Path, selected_rows: list[dict[str, Any]], repeats: list[dict[str, Any]]) -> tuple[dict[str, Any], str, list[dict[str, Any]]]:
    expected_by_id = {row["id"]: expected_topics(row) for row in selected_rows}
    title_by_id = {row["id"]: row.get("title") or row.get("target", "") for row in selected_rows}
    observations: dict[str, list[dict[str, Any]]] = defaultdict(list)
    repeat_metrics = []

    for rep in repeats:
        repeat_dir = Path(rep["repeat_dir"])
        score_path = repeat_dir / "score.json"
        result_path = repeat_dir / "results.jsonl"
        if score_path.exists():
            score = load_score(score_path)
            repeat_metrics.append(
                {
                    "repeat": rep["repeat"],
                    "run_name": rep["run_name"],
                    **{k: numeric_metric(score, k) for k in [
                        "gepa_score",
                        "topic_micro_f1",
                        "topic_micro_precision",
                        "topic_micro_recall",
                        "row_exact_accuracy",
                        "exact_match",
                        "avg_row_jaccard",
                        "avg_row_symdiff",
                        "row_symdiff_score",
                        "valid_json",
                        "avg_predicted_topics",
                        "avg_expected_topics",
                    ]},
                }
            )
        for rr in load_jsonl(result_path):
            inp = rr.get("input") or {}
            rid = inp.get("id")
            if rid not in expected_by_id:
                continue
            pred = predicted_topics(rr)
            exp = expected_by_id[rid]
            observations[rid].append(
                {
                    "repeat": rep["repeat"],
                    "run_name": rep["run_name"],
                    "ok": bool(rr.get("ok")),
                    "predicted": pred,
                    "exact": pred == exp,
                    "jaccard_vs_expected": jaccard(pred, exp),
                    "symdiff_vs_expected": symdiff(pred, exp),
                    "false_positives": tuple(sorted(set(pred) - set(exp))),
                    "false_negatives": tuple(sorted(set(exp) - set(pred))),
                }
            )

    row_reports = []
    for rid, exp in expected_by_id.items():
        obs = observations.get(rid, [])
        preds = [o["predicted"] for o in obs]
        pairs = list(itertools.combinations(preds, 2))
        pair_j = mean([jaccard(a, b) for a, b in pairs]) if pairs else 1.0
        pair_exact = mean([a == b for a, b in pairs]) if pairs else 1.0
        pair_sym = mean([symdiff(a, b) for a, b in pairs]) if pairs else 0.0
        exact_rate = mean([o["exact"] for o in obs]) if obs else 0.0
        avg_j = mean([o["jaccard_vs_expected"] for o in obs]) if obs else 0.0
        avg_sym = mean([o["symdiff_vs_expected"] for o in obs]) if obs else 0.0
        unique = Counter(preds)
        fp = Counter(t for o in obs for t in o["false_positives"])
        fn = Counter(t for o in obs for t in o["false_negatives"])
        volatile = Counter()
        for topic in sorted(set(exp).union(*(set(p) for p in preds))):
            count = sum(topic in p for p in preds)
            if 0 < count < len(preds):
                volatile[topic] = count
        invalid = len(obs) != len(repeats) or any(not o["ok"] for o in obs)
        bucket = classify_row(exact_rate, pair_j, avg_sym, len(unique), len(repeats), invalid)
        row_reports.append(
            {
                "id": rid,
                "title": title_by_id.get(rid, ""),
                "bucket": bucket,
                "expected_topics": list(exp),
                "runs": len(obs),
                "unique_prediction_sets": len(unique),
                "exact_rate_vs_expected": exact_rate,
                "avg_jaccard_vs_expected": avg_j,
                "avg_symdiff_vs_expected": avg_sym,
                "pairwise_prediction_exact_rate": pair_exact,
                "pairwise_prediction_jaccard": pair_j,
                "pairwise_prediction_symdiff": pair_sym,
                "most_common_predictions": [{"topics": list(k), "count": v} for k, v in unique.most_common()],
                "recurring_false_positives": fp.most_common(),
                "recurring_false_negatives": fn.most_common(),
                "volatile_topics": volatile.most_common(),
                "predictions_by_run": [
                    {
                        "repeat": o["repeat"],
                        "run_name": o["run_name"],
                        "topics": list(o["predicted"]),
                        "exact": o["exact"],
                        "false_positives": list(o["false_positives"]),
                        "false_negatives": list(o["false_negatives"]),
                    }
                    for o in obs
                ],
            }
        )
    row_reports.sort(key=lambda r: (r["bucket"] == "stable_correct", r["pairwise_prediction_jaccard"], r["exact_rate_vs_expected"], -r["unique_prediction_sets"]))

    unstable = [r for r in row_reports if r["bucket"] != "stable_correct"]
    bucket_counts = Counter(r["bucket"] for r in row_reports)
    aggregate_pair_j = mean([r["pairwise_prediction_jaccard"] for r in row_reports]) if row_reports else 0.0
    aggregate_pair_exact = mean([r["pairwise_prediction_exact_rate"] for r in row_reports]) if row_reports else 0.0
    aggregate_pair_sym = mean([r["pairwise_prediction_symdiff"] for r in row_reports]) if row_reports else 0.0

    metric_summary = {}
    metric_keys = sorted({k for m in repeat_metrics for k, v in m.items() if isinstance(v, int | float) and k != "repeat"})
    for key in metric_keys:
        vals = [m[key] for m in repeat_metrics if isinstance(m.get(key), int | float)]
        if vals:
            metric_summary[key] = {"mean": mean(vals), "pstdev": pstdev(vals) if len(vals) > 1 else 0.0, "values": vals}

    report = {
        "stability_dir": str(stability_dir),
        "selected_rows": len(selected_rows),
        "completed_repeats": len(repeats),
        "repeat_metrics": repeat_metrics,
        "metric_summary": metric_summary,
        "prediction_stability": {
            "pairwise_prediction_exact_rate": aggregate_pair_exact,
            "pairwise_prediction_jaccard": aggregate_pair_j,
            "pairwise_prediction_symdiff": aggregate_pair_sym,
        },
        "bucket_counts": dict(bucket_counts),
        "rows": row_reports,
    }

    md = render_markdown(report, unstable)
    return report, md, unstable


def render_markdown(report: dict[str, Any], unstable: list[dict[str, Any]]) -> str:
    lines = ["# OpenClaw easy-set stability report\n\n"]
    lines.append(f"Rows: `{report['selected_rows']}`  Repeats: `{report['completed_repeats']}`\n\n")
    ps = report["prediction_stability"]
    lines.append("## Prediction stability\n\n")
    lines.append(f"- pairwise exact: `{ps['pairwise_prediction_exact_rate']:.3f}`\n")
    lines.append(f"- pairwise Jaccard: `{ps['pairwise_prediction_jaccard']:.3f}`\n")
    lines.append(f"- pairwise symdiff: `{ps['pairwise_prediction_symdiff']:.3f}`\n\n")
    lines.append("## Buckets\n\n")
    for bucket, count in sorted(report["bucket_counts"].items()):
        lines.append(f"- `{bucket}`: {count}\n")
    lines.append("\n## Repeat metric summary\n\n")
    for key, data in sorted(report["metric_summary"].items()):
        lines.append(f"- `{key}`: mean `{data['mean']:.4f}`, pstdev `{data['pstdev']:.4f}`, values `{[round(v,4) for v in data['values']]}`\n")
    lines.append("\n## Least stable / review rows\n")
    for i, row in enumerate(unstable[:30], 1):
        lines.append(
            f"\n### {i}. {row['id']} — {row['bucket']}\n\n"
            f"Title: {row['title']}\n\n"
            f"Expected: `{row['expected_topics']}`\n\n"
            f"pairwise Jaccard `{row['pairwise_prediction_jaccard']:.3f}`, "
            f"pairwise exact `{row['pairwise_prediction_exact_rate']:.3f}`, "
            f"exact vs expected `{row['exact_rate_vs_expected']:.3f}`, "
            f"avg Jaccard vs expected `{row['avg_jaccard_vs_expected']:.3f}`, "
            f"avg symdiff `{row['avg_symdiff_vs_expected']:.2f}`, "
            f"unique sets `{row['unique_prediction_sets']}`\n\n"
        )
        lines.append(f"Most common predictions: `{row['most_common_predictions'][:5]}`\n\n")
        lines.append(f"FP: `{row['recurring_false_positives'][:8]}`\n\n")
        lines.append(f"FN: `{row['recurring_false_negatives'][:8]}`\n\n")
        lines.append(f"Volatile: `{row['volatile_topics'][:8]}`\n\n")
        for pred in row["predictions_by_run"]:
            lines.append(f"- repeat {pred['repeat']}: `{pred['topics']}` exact={pred['exact']}\n")
    return "".join(lines)


def main() -> int:
    args = parse_args()
    if args.runs < 1:
        raise SystemExit("--runs must be >= 1")
    if args.repeat_parallel < 1:
        raise SystemExit("--repeat-parallel must be >= 1")
    rows = load_jsonl(args.input)
    selected = select_rows(rows, args)
    if not selected:
        raise SystemExit("no rows selected")

    stability_dir = args.run_root / args.run_name
    if args.overwrite:
        shutil.rmtree(stability_dir, ignore_errors=True)
    stability_dir.mkdir(parents=True, exist_ok=True)
    selected_input = stability_dir / "selected-input.jsonl"
    write_jsonl(selected_input, selected)
    config = {
        **vars(args),
        "input": str(args.input),
        "agent_card": str(args.agent_card),
        "allowed_topics": str(args.allowed_topics),
        "seed_policy": str(args.seed_policy),
        "run_root": str(args.run_root),
        "wrapped_run_root": str(args.wrapped_run_root),
        "selected_input": str(selected_input),
        "selected_rows": len(selected),
    }
    (stability_dir / "config.json").write_text(json.dumps(config, indent=2, default=str), encoding="utf-8")

    repeats = []
    if args.repeat_parallel == 1:
        for idx in range(1, args.runs + 1):
            print(f"repeat {idx}/{args.runs}: {args.run_name}-repeat-{idx:02d}", flush=True)
            repeats.append(run_repeat(args, stability_dir, selected_input, idx))
    else:
        max_workers = min(args.repeat_parallel, args.runs)
        print(
            f"running {args.runs} repeats with repeat_parallel={max_workers}; "
            f"total row concurrency <= {max_workers * args.parallel}",
            flush=True,
        )
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {}
            for idx in range(1, args.runs + 1):
                print(f"repeat {idx}/{args.runs}: {args.run_name}-repeat-{idx:02d}", flush=True)
                futures[executor.submit(run_repeat, args, stability_dir, selected_input, idx)] = idx
            for future in concurrent.futures.as_completed(futures):
                repeats.append(future.result())
        repeats.sort(key=lambda item: int(item["repeat"]))

    report, markdown, unstable = build_report(stability_dir, selected, repeats)
    (stability_dir / "stability-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (stability_dir / "stability-report.md").write_text(markdown, encoding="utf-8")
    write_jsonl(stability_dir / "unstable-rows.jsonl", unstable)
    (stability_dir / "unstable-row-ids.txt").write_text("".join(row["id"] + "\n" for row in unstable), encoding="utf-8")
    print(json.dumps({"stability_dir": str(stability_dir), "rows": len(selected), "runs": len(repeats), "bucket_counts": report["bucket_counts"], "prediction_stability": report["prediction_stability"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
