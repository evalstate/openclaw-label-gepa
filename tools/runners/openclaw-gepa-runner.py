#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import inspect
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from collections.abc import Mapping
from typing import Any

from fast_agent.batch import BatchRunResult
from fast_agent.eval import CandidateRun
from fast_agent.integrations.gepa import (
    FastAgentBatchEvaluator,
    FastAgentGEPATrackioCallback,
    FastAgentReflectionLM,
    FastAgentRowWiseBatchAdapter,
    RowWiseEvaluationRun,
    RowWiseScore,
    gepa_numeric_metrics,
    safe_trackio_log,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ROOT = PROJECT_ROOT
ENV_DIR = PROJECT_ROOT / ".fast-agent"
DEFAULT_REGIME_ROOT = PROJECT_ROOT / "regimes" / "v7a"
SCHEMA = DEFAULT_REGIME_ROOT / "schemas" / "teacher-output-v6h.schema.json"
TASK_TEMPLATE = DEFAULT_REGIME_ROOT / "prompts" / "task-template-v7a.md"
DEFAULT_REFLECTION_AGENT = "openclaw_gepa_reflector"
RUN_ROOT = ROOT / "runs" / "openclaw-gepa-runner"
CARD = DEFAULT_REGIME_ROOT / "prompts" / "openclaw-vanilla-labeler-v7a.md"
PLAIN_CARD = DEFAULT_REGIME_ROOT / "prompts" / "openclaw-vanilla-labeler-plain-v7a.md"
SEED_POLICY = DEFAULT_REGIME_ROOT / "prompts" / "seed-policy-vanilla-v7a.md"
DEFAULT_INPUT = DEFAULT_REGIME_ROOT / "data" / "feedback300.jsonl"
ALLOWED_TOPICS = DEFAULT_REGIME_ROOT / "prompts" / "allowed-topics-v6h.md"
DEFAULT_POLICY_CHAR_BUDGET = 12_500
ROW_WISE_FRONTIER_OBJECTIVE_KEYS_BY_SCORE_MODE = {
    "f1": ("gepa_score", "row_topic_f1"),
    "row-aware": ("gepa_score", "row_topic_f1", "row_exact", "row_jaccard"),
    "row-jaccard-exact": ("gepa_score", "row_jaccard", "row_exact"),
    "row-soft-exact": ("gepa_score", "row_jaccard", "row_topic_f1", "row_exact"),
}

LABEL_TOKEN_RE = re.compile(r"[a-z][a-z0-9_]*")


def extract_result(row: dict[str, Any]) -> dict[str, Any]:
    for key in ("result", "output", "response", "structured_output"):
        value = row.get(key)
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                return parsed
    return {}


def extract_output_text(row: dict[str, Any]) -> str:
    for key in ("result", "output", "response", "structured_output"):
        value = row.get(key)
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            return json.dumps(value, ensure_ascii=False)
    return ""


def parse_label_text(text: str, allowed: set[str]) -> list[str]:
    text = text.strip()
    if not text:
        return []
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        parsed = None
    if isinstance(parsed, dict):
        value = parsed.get("topics_of_interest", parsed.get("labels", []))
        return [label for label in value if isinstance(label, str)] if isinstance(value, list) else []
    if isinstance(parsed, list):
        return [label for label in parsed if isinstance(label, str)]
    label_line = text
    for line in text.splitlines():
        if re.match(r"^\s*(labels|topics_of_interest|topics)\s*:", line, re.I):
            label_line = line.split(":", 1)[1]
            break
    return [label for label in LABEL_TOKEN_RE.findall(label_line.lower()) if label in allowed]


def topic_f1(tp: int, fp: int, fn: int) -> float:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0


def topic_hint(topic: str, direction: str) -> str:
    if direction == "over_predicted":
        return f"tighten `{topic}` to central ownership, not mentions or implementation side effects"
    if direction == "under_predicted":
        return f"include `{topic}` when it is a central maintainer-owned surface"
    return "re-check the topic boundary against the fixed guidance"


def load_topic_hints_from_guidance(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    hints: dict[str, str] = {}
    current: str | None = None
    parts: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^##\s+`?([a-z][a-z0-9_]*)`?\s*$", line)
        if match:
            if current is not None:
                hints[current] = "\n".join(parts).strip()
            current = match.group(1)
            parts = []
            continue
        if current is not None:
            if line.startswith("## "):
                hints[current] = "\n".join(parts).strip()
                current = None
                parts = []
            else:
                parts.append(line)
    if current is not None:
        hints[current] = "\n".join(parts).strip()
    return hints


def row_wise_frontier_objective_keys(score_mode: str) -> tuple[str, ...]:
    return ROW_WISE_FRONTIER_OBJECTIVE_KEYS_BY_SCORE_MODE.get(score_mode, ("gepa_score",))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="GEPA-optimize a vanilla OpenClaw labeler.")
    p.add_argument("--model", default="codexresponses.gpt-5.5?reasoning=high")
    p.add_argument("--reflection-model", default="codexresponses.gpt-5.5?reasoning=high")
    p.add_argument("--reflection-agent", default=DEFAULT_REFLECTION_AGENT)
    p.add_argument("--reflection-env-dir", type=Path, default=ENV_DIR)
    p.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    p.add_argument(
        "--feedback-input",
        type=Path,
        default=None,
        help="Row-wise GEPA Dfeedback JSONL. Defaults to --input.",
    )
    p.add_argument(
        "--pareto-input",
        type=Path,
        default=None,
        help="Row-wise GEPA Dpareto JSONL. Defaults to the feedback input for debug/smoke runs.",
    )
    p.add_argument(
        "--test-input",
        type=Path,
        default=None,
        help="Optional final benchmark JSONL recorded in run metadata; not used during GEPA optimization.",
    )
    p.add_argument("--seed-policy", type=Path, default=SEED_POLICY)
    p.add_argument("--static-asi", type=Path, default=None, help="Optional static ASI markdown to include in score/reflection side-info.")
    p.add_argument(
        "--optimizer-cues",
        type=Path,
        default=None,
        help="Optional cue/reference markdown shown to GEPA reflection only; not inserted into the task AgentCard.",
    )
    p.add_argument("--agent-card", type=Path, default=CARD)
    p.add_argument("--allowed-topics", type=Path, default=ALLOWED_TOPICS)
    p.add_argument("--plain-labels", action="store_true", help="Ask for comma-separated topic IDs instead of structured JSON.")
    p.add_argument(
        "--mutable-boundary-overlay",
        type=Path,
        default=None,
        help=(
            "Optional seed markdown for a second GEPA candidate variable named "
            "boundary_overlay. Use with an AgentCard containing {{boundary_overlay}}."
        ),
    )
    p.add_argument("--run-name", default=None)
    p.add_argument("--run-root", type=Path, default=RUN_ROOT, help="Directory under which this run directory is created.")
    p.add_argument("--parallel", type=int, default=4)
    p.add_argument("--max-metric-calls", type=int, default=12)
    p.add_argument(
        "--score-mode",
        choices=["f1", "row-aware", "row-jaccard-exact", "row-soft-exact"],
        default="f1",
        help=(
            "GEPA scoring mode. In row-wise mode, row-aware uses "
            "0.50*row_topic_f1 + 0.20*row_exact + 0.30*row_jaccard; "
            "row-jaccard-exact uses 0.70*row_jaccard + 0.30*row_exact; "
            "row-soft-exact uses 0.60*row_jaccard + 0.20*row_topic_f1 + 0.20*row_exact."
        ),
    )
    p.add_argument(
        "--boundary-guidance",
        type=Path,
        default=None,
        help=(
            "Frozen boundary-guidance markdown to use as the single source of truth for "
            "dynamic-ASI topic hints (replaces the in-code TOPIC_HINTS). Copied into the "
            "run directory and recorded in run.json."
        ),
    )
    p.add_argument(
        "--hygiene-penalty",
        type=float,
        default=0.0,
        help=(
            "Per-finding gepa_score penalty for policy-hygiene violations (taxonomy copying, "
            "cue tables, row memorization). 0.0 keeps v5 behavior (warning-only ASI). "
            "Applied in batch and row-wise candidate scoring."
        ),
    )
    p.add_argument(
        "--policy-char-budget",
        type=int,
        default=DEFAULT_POLICY_CHAR_BUDGET,
        help=f"Policy length budget in characters before the length penalty starts (default {DEFAULT_POLICY_CHAR_BUDGET}).",
    )
    p.add_argument(
        "--gepa-mode",
        choices=["batch", "row-wise"],
        default="batch",
        help=(
            "batch preserves the historical single-instance GEPA loop over the whole input. "
            "row-wise exposes each input row as a GEPA validation instance and scores row-level mutations."
        ),
    )
    p.add_argument(
        "--feedback-profile",
        choices=["full", "compact", "metrics-only"],
        default="full",
        help=(
            "Reflection side-info profile. full preserves current detailed row/topic feedback; "
            "compact keeps bounded feedback while redacting row identifiers; metrics-only "
            "keeps score/cardinality/hygiene diagnostics only."
        ),
    )
    p.add_argument(
        "--candidate-proposer",
        choices=["default", "openclaw-compact"],
        default="default",
        help=(
            "Instruction proposer used by row-wise GEPA. default uses GEPA's reflective "
            "mutation proposer; openclaw-compact wraps the reflection LM with stricter "
            "OpenClaw anti-memorization and policy-length constraints."
        ),
    )
    p.add_argument(
        "--reflection-minibatch-size",
        type=int,
        default=None,
        help="GEPA reflection minibatch size. Useful with --gepa-mode row-wise.",
    )
    p.add_argument(
        "--allow-padded-minibatches",
        action="store_true",
        help=(
            "Allow GEPA epoch-shuffled minibatches to pad with duplicate row IDs when "
            "the feedback row count is not divisible by --reflection-minibatch-size."
        ),
    )
    p.add_argument(
        "--frontier-type",
        choices=["instance", "objective", "hybrid", "cartesian"],
        default="hybrid",
        help="GEPA Pareto frontier type for row-wise mode.",
    )
    p.add_argument(
        "--candidate-selection-strategy",
        choices=["pareto", "current_best", "epsilon_greedy", "top_k_pareto"],
        default="pareto",
        help="GEPA candidate selector for row-wise mode.",
    )
    p.add_argument(
        "--acceptance-criterion",
        choices=["strict_improvement", "improvement", "improvement_or_equal"],
        default="strict_improvement",
        help="GEPA row-wise proposal acceptance criterion. 'improvement' is accepted as an alias for strict_improvement.",
    )
    p.add_argument(
        "--reflection-include-row-identifiers",
        action="store_true",
        help="Debug only: include row targets/titles in row-wise reflection ASI.",
    )
    p.add_argument("--evaluate-only", action="store_true")
    p.add_argument("--no-trackio", action="store_true")
    p.add_argument("--project", default="openclaw-vanilla-f1")
    p.add_argument("--trackio-group", default="openclaw-gepa-runner")
    p.add_argument("--trackio-space-id", default=os.environ.get("TRACKIO_SPACE_ID"))
    p.add_argument("--trackio-server-url", default=os.environ.get("TRACKIO_SERVER_URL"))
    p.add_argument(
        "--preflight-only",
        action="store_true",
        help="Validate inputs/configuration and exit before creating run artifacts or calling models.",
    )
    return p.parse_args(argv)


def openclaw_row_gepa_score(
    *,
    row_topic_f1: float,
    row_exact: float,
    row_jaccard: float,
    policy_penalty: float = 0.0,
    score_mode: str = "row-aware",
) -> float:
    if score_mode == "f1":
        composite = row_topic_f1
    elif score_mode == "row-jaccard-exact":
        composite = 0.70 * row_jaccard + 0.30 * row_exact
    elif score_mode == "row-soft-exact":
        composite = 0.60 * row_jaccard + 0.20 * row_topic_f1 + 0.20 * row_exact
    else:
        composite = 0.50 * row_topic_f1 + 0.20 * row_exact + 0.30 * row_jaccard
    return max(0.0, composite - policy_penalty)


def score_formula_title(*, gepa_mode: str, score_mode: str) -> str:
    if gepa_mode == "row-wise":
        if score_mode == "f1":
            return "row_topic_f1"
        if score_mode == "row-jaccard-exact":
            return "0.70*row_jaccard+0.30*row_exact-policy_penalties"
        if score_mode == "row-soft-exact":
            return "0.60*row_jaccard+0.20*row_topic_f1+0.20*row_exact-policy_penalties"
        return "0.50*row_topic_f1+0.20*row_exact+0.30*row_jaccard-policy_penalties"
    if score_mode == "f1":
        return "topic_micro_f1"
    if score_mode == "row-jaccard-exact":
        return "0.70*avg_row_jaccard+0.30*row_exact_accuracy-policy_penalties"
    if score_mode == "row-soft-exact":
        return "0.60*avg_row_jaccard+0.20*topic_micro_f1+0.20*row_exact_accuracy-policy_penalties"
    return "0.50*topic_micro_f1+0.20*row_exact_accuracy+0.30*avg_row_jaccard-policy_penalties"


def init_trackio(args: argparse.Namespace, run_name: str, run_dir: Path) -> bool:
    if args.no_trackio:
        return False
    trackio_dir = os.environ.get("TRACKIO_DIR")
    if not trackio_dir:
        trackio_dir = str((args.run_root.parent / "trackio").resolve())
        os.environ["TRACKIO_DIR"] = trackio_dir
    try:
        import trackio
    except Exception as e:
        print(f"Trackio unavailable; continuing without it: {e}", file=sys.stderr)
        return False
    effective_input = args.feedback_input if args.gepa_mode == "row-wise" and args.feedback_input else args.input
    kwargs: dict[str, Any] = {
        "project": args.project,
        "name": run_name,
        "group": args.trackio_group,
        "embed": False,
        "auto_log_gpu": False,
        "config": {
            "task_model": args.model,
            "reflection_model": args.reflection_model,
            "input": str(effective_input),
            "input_arg": str(args.input),
            "feedback_input": str(args.feedback_input) if args.feedback_input else None,
            "pareto_input": str(args.pareto_input) if args.pareto_input else None,
            "test_input": str(args.test_input) if args.test_input else None,
            "seed_policy": str(args.seed_policy),
            "static_asi": str(args.static_asi) if args.static_asi else None,
            "optimizer_cues": str(args.optimizer_cues) if args.optimizer_cues else None,
            "max_metric_calls": args.max_metric_calls,
            "score_mode": args.score_mode,
            "gepa_mode": args.gepa_mode,
            "feedback_profile": args.feedback_profile,
            "reflection_minibatch_size": args.reflection_minibatch_size,
            "allow_padded_minibatches": args.allow_padded_minibatches,
            "frontier_type": args.frontier_type,
            "candidate_selection_strategy": args.candidate_selection_strategy,
            "acceptance_criterion": _rowwise_acceptance_criterion(args.acceptance_criterion),
            "policy_char_budget": args.policy_char_budget,
            "mutable_boundary_overlay": str(args.mutable_boundary_overlay) if args.mutable_boundary_overlay else None,
            "run_dir": str(run_dir),
            "run_root": str(args.run_root),
            "score": score_formula_title(gepa_mode=args.gepa_mode, score_mode=args.score_mode),
            "plain_labels": args.plain_labels,
            "trackio_dir": trackio_dir,
        },
    }
    if args.trackio_space_id:
        kwargs["space_id"] = args.trackio_space_id
    if args.trackio_server_url:
        kwargs["server_url"] = args.trackio_server_url
    trackio.init(**kwargs)
    print(
        "OpenClaw Trackio dashboard command: "
        f"TRACKIO_DIR={trackio_dir} trackio show --project {args.project!r}",
        file=sys.stderr,
    )
    return True


def finish_trackio(enabled: bool) -> None:
    if not enabled:
        return
    try:
        import trackio

        trackio.finish()
    except Exception:
        pass


def log_candidate(candidate_idx: int, candidate_dir: Path, report: dict[str, Any]) -> None:
    program_idx = candidate_idx - 1
    payload: dict[str, Any] = {
        "gepa/iteration": program_idx,
        "candidate/local_idx": candidate_idx,
        "candidate/program_idx": program_idx,
    }
    numeric_metrics = gepa_numeric_metrics(report)
    noisy_policy_suffixes = (
        "policy_char_budget",
        "policy_budget_usage",
        "policy_chars_remaining",
        "policy_length_over_budget",
        "policy_length_compliance",
        "policy_hygiene_compliance",
    )
    for key, value in numeric_metrics.items():
        if any(key.endswith(suffix) for suffix in noisy_policy_suffixes):
            continue
        payload[key] = value
    safe_trackio_log(payload)


def _num(value: Any, default: float = 0.0) -> float:
    return float(value) if isinstance(value, int | float) else default


def policy_hygiene(policy: str) -> dict[str, Any]:
    lower = policy.lower()
    findings = []
    if "## allowed topics" in lower:
        findings.append("Policy appears to copy the fixed Allowed Topics section.")
    if "## topic definitions and cue words" in lower or "cue words:" in lower:
        findings.append("Policy appears to copy or redefine the fixed cue/keyword taxonomy.")
    if len(re.findall(r"openclaw-[a-z0-9_-]+-[0-9]{3,}", lower)) >= 3:
        findings.append("Policy may contain row IDs or issue-number-specific memorization.")
    if re.search(r"\b(easy-final|confusion-bucket|demoted rows|promotion rule|adjudicated source)\b", lower):
        findings.append("Policy appears to include data-build or adjudication notes; keep task guidance model-facing.")
    if len(re.findall(r"(?m)^- `?[a-z][a-z0-9_]+`?:", policy)) > 25:
        findings.append("Policy has a large topic-by-topic table; prefer concise reusable rules.")
    if "false-positive guard" in lower or "false-negative guard" in lower:
        findings.append("Policy appears to copy fixed boundary-guard text; write compact overlay rules instead.")
    if len(re.findall(r"(?m)^#{2,3} `[a-z][a-z0-9_]+`", policy)) >= 8:
        findings.append("Policy has per-topic guide sections; it should be a decision overlay, not a label guide.")
    return {
        "ok": not findings,
        "findings": findings,
        "policy_chars": len(policy),
    }


def policy_penalty_details(
    policy: str,
    *,
    hygiene_penalty_weight: float,
    policy_char_budget: int,
) -> dict[str, Any]:
    hygiene = policy_hygiene(policy)
    policy_chars = hygiene["policy_chars"]
    policy_length_over_budget = max(0, policy_chars - policy_char_budget)
    policy_length_penalty = min(0.10, (policy_length_over_budget / 10_000) * 0.05)
    hygiene_penalty = hygiene_penalty_weight * len(hygiene["findings"])
    return {
        "hygiene": hygiene,
        "policy_chars": policy_chars,
        "policy_char_budget": policy_char_budget,
        "policy_length_over_budget": policy_length_over_budget,
        "policy_length_penalty": policy_length_penalty,
        "policy_length_compliance": 1.0 - (policy_length_penalty / 0.10),
        "hygiene_penalty": hygiene_penalty,
        "policy_hygiene_compliance": 1.0 if hygiene["ok"] else max(0.0, 1.0 - hygiene_penalty / 0.10),
        "total_policy_penalty": policy_length_penalty + hygiene_penalty,
    }


def add_vanilla_asi(
    report: dict[str, Any],
    policy: str,
    *,
    score_mode: str = "f1",
    hygiene_penalty_weight: float = 0.0,
    policy_char_budget: int = DEFAULT_POLICY_CHAR_BUDGET,
) -> dict[str, Any]:
    original_scores = dict(report.get("scores", {}))
    details = report.setdefault("score_details", {})

    precision = _num(original_scores.get("topic_micro_precision"))
    recall = _num(original_scores.get("topic_micro_recall"))
    f1 = _num(original_scores.get("topic_micro_f1"))
    macro_precision = _num(original_scores.get("topic_macro_precision"))
    macro_recall = _num(original_scores.get("topic_macro_recall"))
    macro_f1 = _num(original_scores.get("topic_macro_f1"))
    exact = _num(original_scores.get("exact_match"))
    row_exact = _num(original_scores.get("row_exact_accuracy"), exact)
    avg_row_jaccard = _num(original_scores.get("avg_row_jaccard"))
    avg_row_symdiff = _num(details.get("avg_row_symdiff"))
    row_symdiff_score = 1.0 / (1.0 + avg_row_symdiff)
    valid_json = _num(original_scores.get("valid_json"), 1.0)
    card = _num(original_scores.get("cardinality_closeness"))
    avg_expected = _num(details.get("avg_expected_topics"))
    avg_predicted = _num(details.get("avg_predicted_topics"))
    fp = int(_num(details.get("false_positives")))
    fn = int(_num(details.get("false_negatives")))
    penalties = policy_penalty_details(
        policy,
        hygiene_penalty_weight=hygiene_penalty_weight,
        policy_char_budget=policy_char_budget,
    )
    hygiene = penalties["hygiene"]
    policy_chars = penalties["policy_chars"]
    policy_length_over_budget = penalties["policy_length_over_budget"]
    policy_length_penalty = penalties["policy_length_penalty"]
    policy_length_compliance = penalties["policy_length_compliance"]
    hygiene_penalty = penalties["hygiene_penalty"]
    hygiene_compliance = penalties["policy_hygiene_compliance"]

    if score_mode in ("row-aware", "row-jaccard-exact", "row-soft-exact"):
        if score_mode == "row-jaccard-exact":
            composite_score = 0.70 * avg_row_jaccard + 0.30 * row_exact
        elif score_mode == "row-soft-exact":
            composite_score = 0.60 * avg_row_jaccard + 0.20 * f1 + 0.20 * row_exact
        else:
            composite_score = 0.50 * f1 + 0.20 * row_exact + 0.30 * avg_row_jaccard
        gepa_score = max(0.0, composite_score - policy_length_penalty - hygiene_penalty)
        # Frontier-safe: all values in scores are higher-is-better.
        report["scores"] = {
            "gepa_score": gepa_score,
            "composite_score": composite_score,
            "topic_micro_f1": f1,
            "topic_macro_f1": macro_f1,
            "row_exact_accuracy": row_exact,
            "avg_row_jaccard": avg_row_jaccard,
            "row_symdiff_score": row_symdiff_score,
            "policy_length_compliance": policy_length_compliance,
        }
        if hygiene_penalty_weight > 0:
            report["scores"]["policy_hygiene_compliance"] = hygiene_compliance
    else:
        composite_score = f1
        gepa_score = max(0.0, composite_score - policy_length_penalty - hygiene_penalty)
        # Historical F1-only mode; row metrics remain diagnostics.
        report["scores"] = {
            "gepa_score": gepa_score,
            "composite_score": composite_score,
            "topic_micro_f1": f1,
            "topic_macro_f1": macro_f1,
            "policy_length_compliance": policy_length_compliance,
        }
        if hygiene_penalty_weight > 0:
            report["scores"]["policy_hygiene_compliance"] = hygiene_compliance
    details.update(
        {
            "topic_micro_precision": precision,
            "topic_micro_recall": recall,
            "topic_macro_precision": macro_precision,
            "topic_macro_recall": macro_recall,
            "topic_macro_f1": macro_f1,
            "exact_match": exact,
            "row_exact_accuracy": row_exact,
            "avg_row_jaccard": avg_row_jaccard,
            "avg_row_symdiff": avg_row_symdiff,
            "row_symdiff_score": row_symdiff_score,
            "composite_score": composite_score,
            "gepa_score": gepa_score,
            "score_mode": score_mode,
            "valid_json": valid_json,
            "cardinality_closeness": card,
            "avg_topic_count_delta": avg_predicted - avg_expected,
            "policy_chars": policy_chars,
            "policy_char_budget": policy_char_budget,
            "policy_length_over_budget": policy_length_over_budget,
            "policy_length_penalty": policy_length_penalty,
            "policy_length_compliance": policy_length_compliance,
            "hygiene_penalty": hygiene_penalty,
            "hygiene_findings_count": len(hygiene["findings"]),
        }
    )

    if avg_predicted < avg_expected - 0.25 or fn > fp * 1.25:
        diagnosis = "under_labeling"
        cardinality_action = "Add central co-labels when multiple maintainer interests are explicit; avoid single-label collapse."
    elif avg_predicted > avg_expected + 0.25 or fp > fn * 1.25:
        diagnosis = "over_labeling"
        cardinality_action = "Tighten incidental-evidence gates and remove labels supported only by files, tests, examples, or side effects."
    else:
        diagnosis = "balanced"
        cardinality_action = "Cardinality is close; focus on label-specific boundary errors."

    topic_priorities = []
    for pattern in report.get("topic_error_patterns", [])[:10]:
        topic_priorities.append(
            {
                "topic": pattern.get("topic"),
                "problem": pattern.get("problem"),
                "false_positives": pattern.get("false_positives"),
                "false_negatives": pattern.get("false_negatives"),
                "precision": pattern.get("precision"),
                "recall": pattern.get("recall"),
                "action": pattern.get("action"),
            }
        )

    row_examples = []
    for failure in (report.get("worst_failures") or report.get("failures") or [])[:10]:
        row_examples.append(
            {
                "id": failure.get("id"),
                "title": failure.get("title"),
                "expected": failure.get("expected"),
                "actual": failure.get("actual"),
                "false_positives": failure.get("false_positives"),
                "false_negatives": failure.get("false_negatives"),
                "row_score": failure.get("row_score"),
            }
        )

    feedback = list(report.get("actionable_feedback") or [])
    feedback.insert(
        0,
        f"Objective: optimize exact topic membership with balanced precision and recall. "
        f"Current precision={precision:.3f}, recall={recall:.3f}, F1={f1:.3f}.",
    )
    feedback.insert(
        1,
        f"Cardinality diagnosis: {diagnosis}; avg predicted {avg_predicted:.2f} vs expected {avg_expected:.2f}. {cardinality_action}",
    )
    if hygiene["findings"]:
        feedback.insert(2, "Prompt hygiene warning: " + " ".join(hygiene["findings"]))
    if policy_length_penalty:
        feedback.insert(
            2,
            f"Policy length penalty: policy is {policy_length_over_budget} chars over the "
            f"{policy_char_budget} char budget; GEPA score was reduced by {policy_length_penalty:.4f}.",
        )

    report["vanilla_f1_asi"] = {
        "global_diagnosis": {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "macro_f1": macro_f1,
            "gepa_score": gepa_score,
            "score_mode": score_mode,
            "exact_match": exact,
            "row_exact_accuracy": row_exact,
            "avg_row_jaccard": avg_row_jaccard,
            "avg_row_symdiff": avg_row_symdiff,
            "row_symdiff_score": row_symdiff_score,
            "composite_score": composite_score,
            "valid_json": valid_json,
            "cardinality_closeness": card,
            "avg_expected_topics": avg_expected,
            "avg_predicted_topics": avg_predicted,
            "false_positives": fp,
            "false_negatives": fn,
            "policy_chars": policy_chars,
            "policy_char_budget": policy_char_budget,
            "policy_length_over_budget": policy_length_over_budget,
            "policy_length_penalty": policy_length_penalty,
            "policy_length_compliance": policy_length_compliance,
            "diagnosis": diagnosis,
            "action": cardinality_action,
        },
        "topic_priorities": topic_priorities,
        "confusions": report.get("confusions", [])[:8],
        "row_examples": row_examples,
        "prompt_hygiene": hygiene,
        "reflection_hint": (
            "Make concise reusable routing rules. Do not copy the fixed allowed-topic taxonomy, "
            "do not add row-specific examples, and do not optimize for recall at the expense of F1."
        ),
    }
    report["actionable_feedback"] = feedback[:14]
    return report


def brief_reflection_text(text: Any, *, max_chars: int = 520) -> str:
    flat = " ".join(str(text or "").split())
    if not flat:
        return ""
    flat = re.sub(
        r"^`[^`]+`\s+[^:]+:\s+expected in \d+ rows, predicted in \d+, "
        r"TP=\d+, FP=\d+, FN=\d+, precision=[0-9.]+, recall=[0-9.]+\.\s*",
        "",
        flat,
    )
    chunks = re.split(r"(?<=[.!?])\s+", flat)
    seen: set[str] = set()
    deduped: list[str] = []
    for chunk in chunks:
        norm = re.sub(r"\s+", " ", chunk.lower()).strip()
        if not norm or norm in seen:
            continue
        seen.add(norm)
        deduped.append(chunk)
    out = " ".join(deduped)
    if len(out) <= max_chars:
        return out
    return out[:max_chars].rsplit(" ", 1)[0].rstrip() + " [truncated]"


def clean_topic_items(items: list[Any], *, keep_examples: bool, limit: int, max_action_chars: int = 320) -> list[Any]:
    cleaned: list[Any] = []
    for item in items[:limit]:
        if not isinstance(item, Mapping):
            continue
        out = dict(item)
        if "action" in out:
            out["suggested_mutation"] = brief_reflection_text(out.pop("action"), max_chars=max_action_chars)
        if not keep_examples:
            for key in ("examples", "true_positive_examples", "false_positive_examples", "false_negative_examples"):
                out.pop(key, None)
        cleaned.append(out)
    return cleaned


def clean_reflection_report(report: dict[str, Any], *, keep_examples: bool) -> dict[str, Any]:
    out = dict(report)
    global_feedback = [
        item for item in list(out.get("actionable_feedback") or []) if not str(item).lstrip().startswith("`")
    ]
    out["actionable_feedback"] = [brief_reflection_text(item, max_chars=420) for item in global_feedback[:5]]
    out["topic_error_patterns"] = clean_topic_items(
        list(out.get("topic_error_patterns") or []),
        keep_examples=keep_examples,
        limit=8 if keep_examples else 6,
        max_action_chars=420 if keep_examples else 260,
    )
    out["confusions"] = clean_topic_items(
        list(out.get("confusions") or []),
        keep_examples=keep_examples,
        limit=6 if keep_examples else 4,
        max_action_chars=420 if keep_examples else 260,
    )
    asi = dict(out.get("vanilla_f1_asi") or {})
    if "topic_priorities" in asi:
        asi["topic_priorities"] = clean_topic_items(
            list(asi.get("topic_priorities") or []),
            keep_examples=False,
            limit=8 if keep_examples else 6,
            max_action_chars=260,
        )
    out["vanilla_f1_asi"] = asi
    return out


def summarize_batch_summary(summary: Mapping[str, Any]) -> dict[str, Any]:
    usage = summary.get("usage") if isinstance(summary.get("usage"), Mapping) else {}
    cache = summary.get("cache") if isinstance(summary.get("cache"), Mapping) else {}
    return {
        "input_rows": summary.get("input_rows"),
        "processed_rows": summary.get("processed_rows"),
        "skipped_rows": summary.get("skipped_rows"),
        "failed_rows": summary.get("failed_rows"),
        "duration_ms": summary.get("duration_ms"),
        "usage": {
            "input_tokens": usage.get("input_tokens"),
            "output_tokens": usage.get("output_tokens"),
            "total_tokens": usage.get("total_tokens"),
            "reasoning_tokens": usage.get("reasoning_tokens"),
            "rows_with_usage": usage.get("rows_with_usage"),
        },
        "cache": {
            "read_tokens": cache.get("read_tokens"),
            "write_tokens": cache.get("write_tokens"),
            "hit_tokens": cache.get("hit_tokens"),
            "served_tokens": cache.get("served_tokens"),
        },
    }


def feedback_profile_description(profile: str) -> str:
    if profile == "full":
        return (
            "full: detailed topic patterns, confusions, row failures, worst rows, "
            "and actionable feedback are exposed to reflection."
        )
    if profile == "compact":
        return (
            "compact: bounded feedback is exposed to reflection while row identifiers "
            "and long examples are redacted."
        )
    if profile == "metrics-only":
        return (
            "metrics-only: reflection receives global score/cardinality/hygiene "
            "diagnostics only, without topic actions or row examples."
        )
    raise ValueError(f"Unknown feedback profile: {profile}")


def apply_feedback_profile(report: dict[str, Any], profile: str, *, mutable_overlay: bool) -> dict[str, Any]:
    if profile == "full":
        out = clean_reflection_report(report, keep_examples=True)
        out["feedback_profile"] = profile
        out["evaluation_context"] = {
            "feedback_profile": profile,
            "feedback_profile_description": feedback_profile_description(profile),
            "mutable_boundary_overlay": mutable_overlay,
            "side_info_contract": "Clean evaluator/reflection payload; execution artifacts are stored separately.",
        }
        return out

    cleaned = clean_reflection_report(report, keep_examples=False)
    scores = dict(cleaned.get("scores") or {})
    details = dict(cleaned.get("score_details") or {})
    global_diagnosis = dict((cleaned.get("vanilla_f1_asi") or {}).get("global_diagnosis") or {})
    base: dict[str, Any] = {
        "scores": scores,
        "score_details": details,
        "evaluated": report.get("evaluated"),
        "invalid_topics": report.get("invalid_topics", {}),
        "feedback_profile": profile,
        "evaluation_context": {
            "feedback_profile": profile,
            "feedback_profile_description": feedback_profile_description(profile),
            "mutable_boundary_overlay": mutable_overlay,
            "side_info_contract": "Clean evaluator/reflection payload; execution artifacts are stored separately.",
        },
        "actionable_feedback": list(cleaned.get("actionable_feedback") or [])[:2],
        "vanilla_f1_asi": {
            "global_diagnosis": global_diagnosis,
            "prompt_hygiene": (cleaned.get("vanilla_f1_asi") or {}).get("prompt_hygiene"),
            "reflection_hint": (
                "Use global metrics to propose reusable rules. Avoid row-specific examples, "
                "issue numbers, or copying fixed guidance."
            ),
        },
    }
    for key in ("static_asi_path", "benchmark_static_asi_path"):
        if key in report:
            base[key] = report[key]

    if profile == "metrics-only":
        return base

    if profile != "compact":
        raise ValueError(f"Unknown feedback profile: {profile}")

    topic_priorities = list((cleaned.get("vanilla_f1_asi") or {}).get("topic_priorities") or [])[:6]
    base["vanilla_f1_asi"]["topic_priorities"] = topic_priorities
    base["topic_error_patterns"] = list(cleaned.get("topic_error_patterns") or [])[:6]
    base["confusions"] = list(cleaned.get("confusions") or [])[:4]
    base["actionable_feedback"] = list(cleaned.get("actionable_feedback") or [])[:8]
    return base


def resolve_agent_card(args: argparse.Namespace) -> Path:
    if not args.plain_labels:
        return args.agent_card
    if args.agent_card == CARD:
        return PLAIN_CARD
    if "-plain" in args.agent_card.stem:
        return args.agent_card

    name = args.agent_card.name
    candidates = []
    if "labeler-" in name:
        candidates.append(args.agent_card.with_name(name.replace("labeler-", "labeler-plain-", 1)))
    candidates.append(args.agent_card.with_name(args.agent_card.stem + "-plain" + args.agent_card.suffix))
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return args.agent_card


def score_row_output(
    row: dict[str, Any],
    *,
    allowed: set[str],
    score_mode: str,
    policy: str = "",
    hygiene_penalty_weight: float = 0.0,
    policy_char_budget: int = DEFAULT_POLICY_CHAR_BUDGET,
) -> tuple[float, dict[str, Any]]:
    inp = row.get("input") if isinstance(row.get("input"), dict) else row
    expected = {x for x in (inp.get("expected_topics") or []) if isinstance(x, str)}
    result = extract_result(row)
    actual_raw = result.get("topics_of_interest") if isinstance(result, dict) else None
    if isinstance(actual_raw, list):
        actual_list = actual_raw
    else:
        actual_list = parse_label_text(extract_output_text(row), allowed)

    actual = {x for x in actual_list if isinstance(x, str) and x in allowed}
    invalid = [x for x in actual_list if not isinstance(x, str) or x not in allowed]
    row_valid = (
        ((isinstance(result, dict) and isinstance(actual_raw, list)) or bool(extract_output_text(row).strip()))
        and not invalid
    )

    row_tp = expected & actual
    row_fp = actual - expected
    row_fn = expected - actual
    row_union = expected | actual
    row_f1 = topic_f1(len(row_tp), len(row_fp), len(row_fn))
    row_exact = 1.0 if row_valid and not row_fp and not row_fn else 0.0
    row_jaccard = 1.0 if not row_union else len(row_tp) / len(row_union)
    row_symdiff = len(expected ^ actual)
    valid_json = 1.0 if row_valid else 0.0
    composite_score = openclaw_row_gepa_score(
        row_topic_f1=row_f1,
        row_exact=row_exact,
        row_jaccard=row_jaccard,
        policy_penalty=0.0,
        score_mode=score_mode,
    )
    penalties = policy_penalty_details(
        policy,
        hygiene_penalty_weight=hygiene_penalty_weight,
        policy_char_budget=policy_char_budget,
    )
    gepa_score = openclaw_row_gepa_score(
        row_topic_f1=row_f1,
        row_exact=row_exact,
        row_jaccard=row_jaccard,
        policy_penalty=penalties["total_policy_penalty"],
        score_mode=score_mode,
    )

    feedback = []
    if row_fp:
        feedback.append(
            "False positives: "
            + "; ".join(f"{topic}: {topic_hint(topic, 'over_predicted')}" for topic in sorted(row_fp))
        )
    if row_fn:
        feedback.append(
            "False negatives: "
            + "; ".join(f"{topic}: {topic_hint(topic, 'under_predicted')}" for topic in sorted(row_fn))
        )
    if not row_valid:
        feedback.append("Output contract problem: return only valid enum topic IDs in the required format.")
    if not feedback:
        feedback.append("Row matched exactly. Preserve the boundary behavior that produced this label set.")

    side_info = {
        "scores": {
            "gepa_score": gepa_score,
            "row_composite_score": composite_score,
            "row_topic_f1": row_f1,
            "row_exact": row_exact,
            "row_jaccard": row_jaccard,
            "valid_json": valid_json,
            "policy_length_compliance": penalties["policy_length_compliance"],
        },
        "row_feedback": feedback,
        "expected": sorted(expected),
        "actual": sorted(actual),
        "false_positives": sorted(row_fp),
        "false_negatives": sorted(row_fn),
        "invalid_topics": invalid,
        "row_metrics": {
            "score_mode": score_mode,
            "row_symdiff": row_symdiff,
            "expected_topic_count": len(expected),
            "actual_topic_count": len(actual),
            "policy_chars": penalties["policy_chars"],
            "policy_char_budget": penalties["policy_char_budget"],
            "policy_length_over_budget": penalties["policy_length_over_budget"],
            "policy_length_penalty": penalties["policy_length_penalty"],
            "hygiene_penalty": penalties["hygiene_penalty"],
            "hygiene_findings_count": len(penalties["hygiene"]["findings"]),
        },
        "row_context": {
            "target": inp.get("target"),
            "keywords": (inp.get("keywords") or [])[:8],
        },
        "model_description": result.get("description") if isinstance(result, dict) else None,
        "reflection_hint": (
            "Infer reusable centrality/co-label rules from this row. Do not copy row IDs, issue numbers, "
            "URLs, exact titles, or one-off examples into the policy."
        ),
    }
    if hygiene_penalty_weight > 0:
        side_info["scores"]["policy_hygiene_compliance"] = penalties["policy_hygiene_compliance"]
    if penalties["hygiene"]["findings"]:
        side_info["prompt_hygiene"] = penalties["hygiene"]
    return gepa_score, side_info


def _row_identifier(row: Mapping[str, Any]) -> str | None:
    input_row = row.get("input")
    if isinstance(input_row, Mapping) and isinstance(input_row.get("id"), str):
        return input_row["id"]
    if isinstance(row.get("id"), str):
        return row["id"]
    result = extract_result(dict(row))
    if isinstance(result.get("id"), str):
        return result["id"]
    return None


def score_output_against_input(
    *,
    input_path: Path,
    output_path: Path,
    allowed: set[str],
    score_mode: str,
    policy: str,
    hygiene_penalty_weight: float,
    policy_char_budget: int,
) -> dict[str, Any]:
    input_rows = [
        json.loads(line)
        for line in input_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    output_rows = [
        json.loads(line)
        for line in output_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    outputs_by_id = {
        rid: row
        for row in output_rows
        if (rid := _row_identifier(row)) is not None
    }
    topic_stats: dict[str, Counter[str]] = defaultdict(Counter)
    failures: list[dict[str, Any]] = []
    row_scores: list[dict[str, Any]] = []
    valid_rows = 0
    total_tp = total_fp = total_fn = exact_rows = 0
    expected_counts: list[int] = []
    predicted_counts: list[int] = []
    row_jaccards: list[float] = []
    row_symdiffs: list[int] = []

    for input_row in input_rows:
        rid = str(input_row.get("id", ""))
        output_row = outputs_by_id.get(rid, {})
        expected_labels = _expected_topics_for_input_row(input_row)
        scorer_input = dict(input_row)
        scorer_input["expected_topics"] = expected_labels
        scorer_row = dict(output_row)
        scorer_row["input"] = scorer_input
        _, side_info = score_row_output(
            scorer_row,
            allowed=allowed,
            score_mode=score_mode,
            policy=policy,
            hygiene_penalty_weight=hygiene_penalty_weight,
            policy_char_budget=policy_char_budget,
        )
        expected = {x for x in side_info["expected"] if isinstance(x, str)}
        actual = {x for x in side_info["actual"] if isinstance(x, str)}
        fp_topics = set(side_info["false_positives"])
        fn_topics = set(side_info["false_negatives"])
        tp_topics = expected & actual
        row_metric = side_info["row_metrics"]
        scores = side_info["scores"]
        row_scores.append(side_info)
        valid_rows += int(scores["valid_json"] == 1.0)
        exact_rows += int(not fp_topics and not fn_topics and scores["valid_json"] == 1.0)
        total_tp += len(tp_topics)
        total_fp += len(fp_topics)
        total_fn += len(fn_topics)
        expected_counts.append(len(expected))
        predicted_counts.append(len(actual))
        row_jaccards.append(float(scores["row_jaccard"]))
        row_symdiffs.append(int(row_metric["row_symdiff"]))
        for topic in expected | actual:
            topic_stats[topic]["tp"] += int(topic in tp_topics)
            topic_stats[topic]["fp"] += int(topic in fp_topics)
            topic_stats[topic]["fn"] += int(topic in fn_topics)
        if fp_topics or fn_topics or scores["valid_json"] != 1.0:
            failures.append(
                {
                    "id": rid,
                    "title": input_row.get("title") or input_row.get("target", ""),
                    "expected": sorted(expected),
                    "actual": sorted(actual),
                    "false_positives": sorted(fp_topics),
                    "false_negatives": sorted(fn_topics),
                    "row_score": scores["row_jaccard"],
                }
            )

    rows = len(input_rows)
    micro_precision = total_tp / (total_tp + total_fp) if total_tp + total_fp else 0.0
    micro_recall = total_tp / (total_tp + total_fn) if total_tp + total_fn else 0.0
    micro_f1 = topic_f1(total_tp, total_fp, total_fn)
    per_topic = []
    topic_error_patterns = []
    for topic, counts in topic_stats.items():
        tp = counts["tp"]
        fp = counts["fp"]
        fn = counts["fn"]
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        label_f1 = topic_f1(tp, fp, fn)
        per_topic.append((precision, recall, label_f1))
        if fp or fn:
            problem = "over_applied" if fp > fn else "under_applied" if fn > fp else "mixed"
            topic_error_patterns.append(
                {
                    "topic": topic,
                    "problem": problem,
                    "false_positives": fp,
                    "false_negatives": fn,
                    "precision": precision,
                    "recall": recall,
                    "action": topic_hint(topic, "over_predicted" if fp >= fn else "under_predicted"),
                }
            )
    avg_expected = sum(expected_counts) / rows if rows else 0.0
    avg_predicted = sum(predicted_counts) / rows if rows else 0.0
    cardinality_closeness = 1.0 / (1.0 + abs(avg_predicted - avg_expected))
    topic_error_patterns.sort(
        key=lambda item: (item["false_positives"] + item["false_negatives"], item["topic"]),
        reverse=True,
    )
    failures.sort(key=lambda item: float(item["row_score"]))
    return {
        "scores": {
            "topic_micro_precision": micro_precision,
            "topic_micro_recall": micro_recall,
            "topic_micro_f1": micro_f1,
            "topic_macro_precision": (
                sum(item[0] for item in per_topic) / len(per_topic) if per_topic else 0.0
            ),
            "topic_macro_recall": (
                sum(item[1] for item in per_topic) / len(per_topic) if per_topic else 0.0
            ),
            "topic_macro_f1": (
                sum(item[2] for item in per_topic) / len(per_topic) if per_topic else 0.0
            ),
            "exact_match": exact_rows / rows if rows else 0.0,
            "row_exact_accuracy": exact_rows / rows if rows else 0.0,
            "avg_row_jaccard": sum(row_jaccards) / rows if rows else 0.0,
            "valid_json": valid_rows / rows if rows else 0.0,
            "cardinality_closeness": cardinality_closeness,
        },
        "score_details": {
            "topic_micro_precision": micro_precision,
            "topic_micro_recall": micro_recall,
            "topic_macro_precision": (
                sum(item[0] for item in per_topic) / len(per_topic) if per_topic else 0.0
            ),
            "topic_macro_recall": (
                sum(item[1] for item in per_topic) / len(per_topic) if per_topic else 0.0
            ),
            "topic_macro_f1": (
                sum(item[2] for item in per_topic) / len(per_topic) if per_topic else 0.0
            ),
            "exact_match": exact_rows / rows if rows else 0.0,
            "row_exact_accuracy": exact_rows / rows if rows else 0.0,
            "avg_row_jaccard": sum(row_jaccards) / rows if rows else 0.0,
            "avg_row_symdiff": sum(row_symdiffs) / rows if rows else 0.0,
            "false_positives": total_fp,
            "false_negatives": total_fn,
            "avg_expected_topics": avg_expected,
            "avg_predicted_topics": avg_predicted,
        },
        "evaluated": rows,
        "failures": failures[:20],
        "worst_failures": failures[:20],
        "topic_error_patterns": topic_error_patterns[:20],
        "invalid_topics": {},
        "row_scores": row_scores,
    }


def summarize_rowwise_reflection_batch(trajectories: list[Any], *, limit: int = 10) -> dict[str, Any]:
    """Summarize a GEPA row-wise minibatch for reflection.

    Row-wise GEPA gives reflection a small sample of per-row trajectories. This
    aggregate packet makes the sample's label-level shape explicit without
    changing the deterministic scorer.
    """
    label_stats: dict[str, Counter[str]] = defaultdict(Counter)
    co_error: Counter[tuple[str, str]] = Counter()
    rows = 0
    exact_rows = 0
    total_row_score = 0.0
    total_row_jaccard = 0.0

    for item in trajectories:
        if not isinstance(item, Mapping):
            continue
        expected = {x for x in item.get("expected") or [] if isinstance(x, str)}
        actual = {x for x in item.get("actual") or [] if isinstance(x, str)}
        false_positives = {x for x in item.get("false_positives") or [] if isinstance(x, str)}
        false_negatives = {x for x in item.get("false_negatives") or [] if isinstance(x, str)}
        true_positives = expected & actual
        row_scores = item.get("scores") if isinstance(item.get("scores"), Mapping) else {}
        rows += 1
        exact_rows += 1 if not false_positives and not false_negatives else 0
        total_row_score += _num(row_scores.get("row_topic_f1"))
        total_row_jaccard += _num(row_scores.get("row_jaccard"))

        for topic in expected | actual:
            label_stats[topic]["expected"] += 1 if topic in expected else 0
            label_stats[topic]["actual"] += 1 if topic in actual else 0
            label_stats[topic]["tp"] += 1 if topic in true_positives else 0
            label_stats[topic]["fp"] += 1 if topic in false_positives else 0
            label_stats[topic]["fn"] += 1 if topic in false_negatives else 0

        for missed in false_negatives:
            for extra in false_positives:
                co_error[(missed, extra)] += 1

    label_diagnostics: list[dict[str, Any]] = []
    per_label_f1: list[float] = []
    for topic, counts in label_stats.items():
        tp = counts["tp"]
        fp = counts["fp"]
        fn = counts["fn"]
        precision = tp / (tp + fp) if tp + fp else (1.0 if fn == 0 else 0.0)
        recall = tp / (tp + fn) if tp + fn else (1.0 if fp == 0 else 0.0)
        label_f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        per_label_f1.append(label_f1)
        if fp > fn:
            problem = "over_applied"
            action = f"Tighten inclusion for `{topic}`; it appeared as an extra label more often than it was missed."
        elif fn > fp:
            problem = "under_applied"
            action = f"Loosen or clarify inclusion for `{topic}`; it was missed more often than it appeared as an extra label."
        elif fp or fn:
            problem = "mixed_confusion"
            action = f"Clarify boundary use for `{topic}`; it has both false positives and false negatives."
        else:
            problem = "stable"
            action = f"Preserve current behavior for `{topic}` in this minibatch."
        label_diagnostics.append(
            {
                "topic": topic,
                "problem": problem,
                "expected_rows": counts["expected"],
                "predicted_rows": counts["actual"],
                "true_positives": tp,
                "false_positives": fp,
                "false_negatives": fn,
                "precision": round(precision, 6),
                "recall": round(recall, 6),
                "f1": round(label_f1, 6),
                "suggested_mutation": action,
            }
        )

    label_diagnostics.sort(
        key=lambda x: (
            x["false_positives"] + x["false_negatives"],
            abs(x["false_positives"] - x["false_negatives"]),
            x["expected_rows"] + x["predicted_rows"],
        ),
        reverse=True,
    )

    co_error_patterns = [
        {
            "missed_topic": expected_topic,
            "extra_topic": predicted_topic,
            "count": count,
            "diagnosis": "same-row false negative and false positive co-occurred",
            "suggested_mutation": f"Clarify the boundary between `{expected_topic}` and `{predicted_topic}` only if this pair reflects a reusable ownership distinction.",
        }
        for (expected_topic, predicted_topic), count in co_error.most_common(limit)
    ]

    return {
        "batch_rows": rows,
        "macro_f1": round(sum(per_label_f1) / len(per_label_f1), 6) if per_label_f1 else 0.0,
        "active_labels": len(per_label_f1),
        "avg_row_topic_f1": round(total_row_score / rows, 6) if rows else 0.0,
        "row_exact_accuracy": round(exact_rows / rows, 6) if rows else 0.0,
        "avg_row_jaccard": round(total_row_jaccard / rows, 6) if rows else 0.0,
        "label_error_patterns": label_diagnostics[:limit],
        "co_error_patterns": co_error_patterns,
        "reflection_hint": (
            "Use this minibatch aggregate to decide whether labels are over-applied, under-applied, "
            "or repeatedly paired with same-row false positives/negatives. Treat co-error pairs as "
            "directional evidence, not as a formal substitution matrix. Do not turn these counts into "
            "row-specific memorization."
        ),
    }




def _render_for_proposer(value: Any, level: int = 3) -> str:
    if isinstance(value, Mapping):
        if not value:
            return "\n"
        parts: list[str] = []
        for key, item in value.items():
            parts.append(f"{'#' * level} {key}\n")
            parts.append(_render_for_proposer(item, min(level + 1, 6)))
        return "".join(parts)
    if isinstance(value, list | tuple):
        if not value:
            return "\n"
        parts = []
        for i, item in enumerate(value, start=1):
            parts.append(f"{'#' * level} Item {i}\n")
            parts.append(_render_for_proposer(item, min(level + 1, 6)))
        return "".join(parts)
    return f"{str(value).strip()}\n\n"


def _format_reflective_examples_for_proposer(records: Sequence[Mapping[str, Any]], *, limit: int = 24) -> str:
    examples = list(records)[:limit]
    parts: list[str] = []
    for i, record in enumerate(examples, start=1):
        parts.append(f"# Example {i}\n")
        parts.append(_render_for_proposer(record, level=2))
    if len(records) > limit:
        parts.append(f"\n# Omitted\n{len(records) - limit} additional reflective records omitted by proposer cap.\n")
    return "\n".join(parts)


def _extract_instruction_block(text: str) -> str:
    stripped = text.strip()
    start = stripped.find("```")
    end = stripped.rfind("```")
    if start == -1 or end <= start:
        return stripped
    content = stripped[start + 3 : end]
    content = re.sub(r"^\S+\n", "", content, count=1)
    return content.strip()


class OpenClawCompactCandidateProposer:
    """Constrain GEPA reflection to small, general OpenClaw policy edits."""

    def __init__(self, *, reflection_lm: Any, policy_char_budget: int) -> None:
        self.reflection_lm = reflection_lm
        self.policy_char_budget = policy_char_budget

    def __call__(
        self,
        candidate: dict[str, str],
        reflective_dataset: Mapping[str, Sequence[Mapping[str, Any]]],
        components_to_update: list[str],
    ) -> dict[str, str]:
        updates: dict[str, str] = {}
        for component in components_to_update:
            current = candidate.get(component)
            records = reflective_dataset.get(component)
            if not isinstance(current, str) or not records:
                continue
            prompt = self._proposal_prompt(component=component, current=current, records=records)
            proposed = _extract_instruction_block(self.reflection_lm(prompt))
            updates[component] = self._repair_if_needed(component=component, proposed=proposed, records=records)
        return updates

    def _proposal_prompt(
        self,
        *,
        component: str,
        current: str,
        records: Sequence[Mapping[str, Any]],
    ) -> str:
        side_info = _format_reflective_examples_for_proposer(records)
        return f"""You are improving one mutable OpenClaw label-routing component: `{component}`.

Current component:
```text
{current}
```

Reflective ASI from the sampled rows follows. It may include aggregate diagnostics,
expected/actual labels, false positives/false negatives, row metrics, and model feedback.
Use it to infer general failure patterns. Do not memorize row facts.

```text
{side_info}
```

Write a complete drop-in replacement for `{component}`.

Hard constraints:
- Make at most 3 substantive behavior changes.
- Prefer replacing or tightening existing rules over appending new sections.
- Target the dominant aggregate error pattern, especially under-labelling only when false positives are low.
- Do not include row IDs, issue numbers, exact titles, URLs, copied examples, or memorized row-specific facts.
- Do not create a topic-by-topic taxonomy, cue table, keyword table, or long boundary-overlay clone.
- Do not copy the fixed allowed-topic list or topic definitions.
- Keep it under {self.policy_char_budget} characters.
- Preserve the task output contract already specified outside this component.

Return only the replacement component within ``` blocks.
"""

    def _repair_if_needed(
        self,
        *,
        component: str,
        proposed: str,
        records: Sequence[Mapping[str, Any]],
    ) -> str:
        penalties = policy_penalty_details(
            proposed,
            hygiene_penalty_weight=1.0,
            policy_char_budget=self.policy_char_budget,
        )
        findings = penalties["hygiene"]["findings"]
        over_budget = int(penalties["policy_length_over_budget"])
        if not findings and over_budget <= 0:
            return proposed

        feedback = {
            "policy_chars": penalties["policy_chars"],
            "policy_char_budget": self.policy_char_budget,
            "policy_length_over_budget": over_budget,
            "hygiene_findings": findings,
        }
        side_info = _format_reflective_examples_for_proposer(records, limit=6)
        repair_prompt = f"""Repair this proposed OpenClaw `{component}` component so it satisfies the constraints.

Constraint violations:
```json
{json.dumps(feedback, indent=2)}
```

Proposed component:
```text
{proposed}
```

Small ASI reminder:
```text
{side_info}
```

Return a complete replacement within ``` blocks. Keep the useful behavioral change,
remove row-specific or taxonomy-copying content, and stay under {self.policy_char_budget} characters.
"""
        repaired = _extract_instruction_block(self.reflection_lm(repair_prompt))
        return repaired or proposed


def build_custom_candidate_proposer(args: argparse.Namespace, reflection_lm: Any) -> Any | None:
    if args.candidate_proposer == "default":
        return None
    if args.candidate_proposer == "openclaw-compact":
        return OpenClawCompactCandidateProposer(
            reflection_lm=reflection_lm,
            policy_char_budget=args.policy_char_budget,
        )
    raise ValueError(f"Unknown candidate proposer: {args.candidate_proposer}")

def apply_row_feedback_profile(
    side_info: dict[str, Any],
    profile: str,
    *,
    include_row_identifiers: bool,
) -> dict[str, Any]:
    row_context = dict(side_info.get("row_context") or {})
    if not include_row_identifiers:
        row_context.pop("target", None)

    if profile == "metrics-only":
        return {
            "scores": side_info.get("scores"),
            "row_metrics": side_info.get("row_metrics"),
            "prompt_hygiene": side_info.get("prompt_hygiene"),
            "feedback_profile": profile,
            "reflection_hint": "Metrics-only control: use score movement only; no row labels or examples are provided.",
        }

    base = {
        "scores": side_info.get("scores"),
        "row_feedback": side_info.get("row_feedback"),
        "expected": side_info.get("expected"),
        "actual": side_info.get("actual"),
        "false_positives": side_info.get("false_positives"),
        "false_negatives": side_info.get("false_negatives"),
        "invalid_topics": side_info.get("invalid_topics"),
        "row_metrics": side_info.get("row_metrics"),
        "row_context": row_context,
        "prompt_hygiene": side_info.get("prompt_hygiene"),
        "feedback_profile": profile,
        "reflection_hint": side_info.get("reflection_hint"),
    }
    if profile == "compact":
        return {key: value for key, value in base.items() if value not in (None, [], {})}
    if profile == "full":
        out = dict(side_info)
        out["row_context"] = row_context
        out["feedback_profile"] = profile
        return out
    raise ValueError(f"Unknown feedback profile: {profile}")


class OpenClawRowWiseBatchAdapter(FastAgentRowWiseBatchAdapter):
    """Add OpenClaw candidate diagnostics to row-wise GEPA eval artifacts.

    GEPA treats ``objective_scores`` as higher-is-better values for frontier logic, so
    raw policy length should not be added there. This wrapper writes and logs those
    diagnostics separately after the upstream row-wise evaluation completes.
    """

    def __init__(
        self,
        *,
        policy_char_budget: int,
        hygiene_penalty_weight: float,
        mutable_boundary_overlay: bool,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.policy_char_budget = policy_char_budget
        self.hygiene_penalty_weight = hygiene_penalty_weight
        self.mutable_boundary_overlay = mutable_boundary_overlay
        self._pending_candidate_trackio_payloads: list[dict[str, int | float]] = []

    def pop_pending_candidate_trackio_payload(self) -> dict[str, int | float] | None:
        if not self._pending_candidate_trackio_payloads:
            return None
        return self._pending_candidate_trackio_payloads.pop(0)

    def evaluate(
        self,
        batch: list[dict[str, Any]],
        candidate: dict[str, str],
        capture_traces: bool = False,
    ) -> Any:
        eval_batch = super().evaluate(batch, candidate, capture_traces=capture_traces)
        self._record_candidate_diagnostics(candidate)
        return eval_batch

    def _record_candidate_diagnostics(self, candidate: dict[str, str]) -> None:
        policy = str(candidate.get("policy", ""))
        penalties = policy_penalty_details(
            policy,
            hygiene_penalty_weight=self.hygiene_penalty_weight,
            policy_char_budget=self.policy_char_budget,
        )
        policy_chars = int(penalties["policy_chars"])
        policy_char_budget = int(penalties["policy_char_budget"])
        policy_budget_usage = policy_chars / policy_char_budget if policy_char_budget else 0.0
        policy_stats: dict[str, int | float] = {
            "policy_chars": policy_chars,
            "policy_char_budget": policy_char_budget,
            "policy_budget_usage": policy_budget_usage,
            "policy_chars_remaining": max(0, policy_char_budget - policy_chars),
            "policy_length_over_budget": int(penalties["policy_length_over_budget"]),
            "policy_length_penalty": float(penalties["policy_length_penalty"]),
            "policy_length_compliance": float(penalties["policy_length_compliance"]),
            "hygiene_penalty": float(penalties["hygiene_penalty"]),
            "hygiene_findings_count": len(penalties["hygiene"]["findings"]),
            "policy_hygiene_compliance": float(penalties["policy_hygiene_compliance"]),
        }

        candidate_diagnostics: dict[str, dict[str, int | float]] = {"policy": policy_stats}
        trackio_payload: dict[str, int | float] = {
            "candidate/policy_chars": policy_chars,
            "candidate/policy_length_penalty": float(penalties["policy_length_penalty"]),
            "candidate/hygiene_penalty": float(penalties["hygiene_penalty"]),
            "candidate/hygiene_findings_count": len(penalties["hygiene"]["findings"]),
        }

        if self.mutable_boundary_overlay:
            overlay = str(candidate.get("boundary_overlay", ""))
            overlay_chars = len(overlay)
            overlay_stats = {"boundary_overlay_chars": overlay_chars}
            candidate_diagnostics["boundary_overlay"] = overlay_stats
            trackio_payload["candidate/boundary_overlay_chars"] = overlay_chars
            trackio_payload["candidate/total_mutable_chars"] = policy_chars + overlay_chars

        eval_dir = self.run_dir / "row-wise-evals" / f"eval-{self._evaluations:05d}"
        score_path = eval_dir / "row-wise-score.json"
        try:
            summary = json.loads(score_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            summary = {"eval_index": self._evaluations}
        summary["candidate_diagnostics"] = candidate_diagnostics
        score_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        self._pending_candidate_trackio_payloads.append(trackio_payload)


class OpenClawCandidateDiagnosticsCallback:
    def __init__(self, adapter: OpenClawRowWiseBatchAdapter) -> None:
        self.adapter = adapter

    def on_evaluation_end(self, event: Mapping[str, Any]) -> None:
        payload = self.adapter.pop_pending_candidate_trackio_payload()
        if payload is None:
            return
        context: dict[str, int | float] = {}
        for source_key, metric_key in (
            ("iteration", "gepa/iteration"),
            ("candidate_idx", "gepa/candidate_idx"),
        ):
            value = event.get(source_key)
            if isinstance(value, bool):
                context[metric_key] = int(value)
            elif isinstance(value, (int, float)):
                context[metric_key] = value
        safe_trackio_log({**context, **payload})


def openclaw_valset_dashboard_metrics(trajectories: list[Mapping[str, Any]]) -> dict[str, int | float]:
    label_stats: dict[str, dict[str, int]] = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})
    rows = 0
    exact_rows = 0
    total_row_f1 = 0.0
    total_row_jaccard = 0.0
    total_tp = 0
    total_fp = 0
    total_fn = 0

    for item in trajectories:
        expected = {x for x in item.get("expected") or [] if isinstance(x, str)}
        actual = {x for x in item.get("actual") or [] if isinstance(x, str)}
        fp_topics = {x for x in item.get("false_positives") or [] if isinstance(x, str)}
        fn_topics = {x for x in item.get("false_negatives") or [] if isinstance(x, str)}
        tp_topics = expected & actual
        row_scores = item.get("scores") if isinstance(item.get("scores"), Mapping) else {}

        rows += 1
        exact_rows += 1 if not fp_topics and not fn_topics else 0
        total_row_f1 += _num(row_scores.get("row_topic_f1"))
        total_row_jaccard += _num(row_scores.get("row_jaccard"))
        total_tp += len(tp_topics)
        total_fp += len(fp_topics)
        total_fn += len(fn_topics)

        for topic in expected | actual:
            label_stats[topic]["tp"] += 1 if topic in tp_topics else 0
            label_stats[topic]["fp"] += 1 if topic in fp_topics else 0
            label_stats[topic]["fn"] += 1 if topic in fn_topics else 0

    per_label_precision: list[float] = []
    per_label_recall: list[float] = []
    per_label_f1: list[float] = []
    for counts in label_stats.values():
        tp = counts["tp"]
        fp = counts["fp"]
        fn = counts["fn"]
        if tp + fp + fn == 0:
            continue
        precision = 0.0 if tp + fp == 0 else tp / (tp + fp)
        recall = 0.0 if tp + fn == 0 else tp / (tp + fn)
        per_label_precision.append(precision)
        per_label_recall.append(recall)
        per_label_f1.append(topic_f1(tp, fp, fn))

    micro_precision = 0.0 if total_tp + total_fp == 0 else total_tp / (total_tp + total_fp)
    micro_recall = 0.0 if total_tp + total_fn == 0 else total_tp / (total_tp + total_fn)
    micro_f1 = topic_f1(total_tp, total_fp, total_fn)
    total_expected = total_tp + total_fn
    total_predicted = total_tp + total_fp
    return {
        "rows": rows,
        "topic_micro_f1": micro_f1,
        "topic_micro_precision": micro_precision,
        "topic_micro_recall": micro_recall,
        "topic_macro_f1": sum(per_label_f1) / len(per_label_f1) if per_label_f1 else 0.0,
        "topic_macro_precision": (
            sum(per_label_precision) / len(per_label_precision) if per_label_precision else 0.0
        ),
        "topic_macro_recall": sum(per_label_recall) / len(per_label_recall) if per_label_recall else 0.0,
        "topic_macro_active_labels": len(per_label_f1),
        "topic_true_positives": total_tp,
        "topic_false_positives": total_fp,
        "topic_false_negatives": total_fn,
        "topic_expected_labels": total_expected,
        "topic_predicted_labels": total_predicted,
        "topic_false_positive_rate": total_fp / total_predicted if total_predicted else 0.0,
        "topic_false_negative_rate": total_fn / total_expected if total_expected else 0.0,
        "row_exact_accuracy": exact_rows / rows if rows else 0.0,
        "avg_row_topic_f1": total_row_f1 / rows if rows else 0.0,
        "avg_row_jaccard": total_row_jaccard / rows if rows else 0.0,
    }


class OpenClawValsetAggregateCallback:
    def __init__(
        self,
        *,
        val_rows: list[dict[str, Any]],
        allowed_topics: set[str],
        score_mode: str,
    ) -> None:
        self.val_rows = val_rows
        self.allowed_topics = allowed_topics
        self.score_mode = score_mode
        self.best_gepa_score: float | None = None

    def on_valset_evaluated(self, event: Mapping[str, Any]) -> None:
        payload = self._objective_payload(event)
        outputs_by_val_id = event.get("outputs_by_val_id")
        if not isinstance(outputs_by_val_id, Mapping):
            if payload:
                safe_trackio_log(payload)
            return

        trajectories: list[dict[str, Any]] = []
        for val_id, output_row in outputs_by_val_id.items():
            if not isinstance(output_row, dict):
                continue
            merged = dict(output_row)
            if not isinstance(merged.get("input"), dict):
                input_row = self._input_for_val_id(val_id)
                if input_row is not None:
                    merged["input"] = input_row.get("input") if isinstance(input_row.get("input"), dict) else input_row
            _, side_info = score_row_output(
                merged,
                allowed=self.allowed_topics,
                score_mode=self.score_mode,
            )
            trajectories.append(side_info)

        if not trajectories:
            return

        aggregate = openclaw_valset_dashboard_metrics(trajectories)
        payload.update({
            "openclaw/diagnostic/val/topic_micro_f1": float(aggregate["topic_micro_f1"]),
            "openclaw/diagnostic/val/topic_micro_precision": float(aggregate["topic_micro_precision"]),
            "openclaw/diagnostic/val/topic_micro_recall": float(aggregate["topic_micro_recall"]),
            "openclaw/diagnostic/val/topic_macro_f1": float(aggregate["topic_macro_f1"]),
            "openclaw/diagnostic/val/topic_macro_precision": float(aggregate["topic_macro_precision"]),
            "openclaw/diagnostic/val/topic_macro_recall": float(aggregate["topic_macro_recall"]),
            "openclaw/diagnostic/val/topic_macro_active_labels": int(aggregate["topic_macro_active_labels"]),
            "openclaw/diagnostic/val/topic_true_positives": int(aggregate["topic_true_positives"]),
            "openclaw/diagnostic/val/topic_false_positives": int(aggregate["topic_false_positives"]),
            "openclaw/diagnostic/val/topic_false_negatives": int(aggregate["topic_false_negatives"]),
            "openclaw/diagnostic/val/topic_expected_labels": int(aggregate["topic_expected_labels"]),
            "openclaw/diagnostic/val/topic_predicted_labels": int(aggregate["topic_predicted_labels"]),
            "openclaw/diagnostic/val/topic_false_positive_rate": float(
                aggregate["topic_false_positive_rate"]
            ),
            "openclaw/diagnostic/val/topic_false_negative_rate": float(
                aggregate["topic_false_negative_rate"]
            ),
            "openclaw/diagnostic/val/avg_row_topic_f1": float(aggregate["avg_row_topic_f1"]),
            "openclaw/diagnostic/val/row_exact_accuracy": float(aggregate["row_exact_accuracy"]),
            "openclaw/diagnostic/val/avg_row_jaccard": float(aggregate["avg_row_jaccard"]),
            "openclaw/diagnostic/val/evaluated_rows": int(aggregate["rows"]),
        })
        safe_trackio_log(payload)

    def _objective_payload(self, event: Mapping[str, Any]) -> dict[str, int | float]:
        payload: dict[str, int | float] = {}
        for source_key, metric_key in (
            ("iteration", "gepa/iteration"),
            ("candidate_idx", "gepa/candidate_idx"),
            ("num_examples_evaluated", "openclaw/diagnostic/val/num_examples_evaluated"),
            ("total_valset_size", "openclaw/diagnostic/val/total_valset_size"),
        ):
            value = event.get(source_key)
            if isinstance(value, bool):
                payload[metric_key] = int(value)
            elif isinstance(value, (int, float)):
                payload[metric_key] = value

        is_best = event.get("is_best_program")
        if isinstance(is_best, bool):
            payload["openclaw/objective/val/is_best_program"] = int(is_best)

        score = event.get("average_score")
        if not isinstance(score, (int, float)):
            return payload

        proposal_score = float(score)
        best_before = self.best_gepa_score
        if best_before is None or proposal_score > best_before:
            self.best_gepa_score = proposal_score
        best_score = self.best_gepa_score

        payload["openclaw/objective/val/proposal_gepa_score"] = proposal_score
        payload["openclaw/objective/val/best_gepa_score"] = best_score
        payload["openclaw/objective/val/gepa_score"] = best_score
        if best_before is not None:
            payload["openclaw/objective/val/proposal_delta_vs_best_before"] = (
                proposal_score - best_before
            )
        return payload

    def _input_for_val_id(self, val_id: Any) -> dict[str, Any] | None:
        if isinstance(val_id, int) and 0 <= val_id < len(self.val_rows):
            return self.val_rows[val_id]
        if isinstance(val_id, str):
            try:
                index = int(val_id)
            except ValueError:
                return None
            if 0 <= index < len(self.val_rows):
                return self.val_rows[index]
        return None


def build_row_wise_adapter(run_dir: Path, args: argparse.Namespace) -> FastAgentRowWiseBatchAdapter:
    """Wire the upstream row-wise adapter to OpenClaw row scoring and reflection ASI."""
    allowed = set(_schema_topic_contract()[0])
    plain_labels = args.plain_labels
    candidate_variables = {"policy": "policy"}
    if args.mutable_boundary_overlay:
        candidate_variables["boundary_overlay"] = "boundary_overlay"

    def row_scorer(
        output_row: dict[str, Any],
        input_row: dict[str, Any],
        candidate: dict[str, str],
        evaluation: RowWiseEvaluationRun,
    ) -> RowWiseScore:
        row_score, side_info = score_row_output(
            output_row,
            allowed=allowed,
            score_mode=args.score_mode,
            policy=str(candidate.get("policy", "")),
            hygiene_penalty_weight=args.hygiene_penalty,
            policy_char_budget=args.policy_char_budget,
        )
        objective_scores = {
            key: float(value)
            for key, value in (side_info.get("scores") or {}).items()
            if key in row_wise_frontier_objective_keys(args.score_mode) and isinstance(value, int | float)
        }
        return RowWiseScore(score=row_score, trajectory=side_info, objective_scores=objective_scores)

    def reflective_dataset_builder(
        candidate: dict[str, str],
        eval_batch: Any,
        components_to_update: list[str],
    ) -> dict[str, list[dict[str, Any]]]:
        scores = eval_batch.scores
        trajectories = eval_batch.trajectories or []
        batch_diagnostics = summarize_rowwise_reflection_batch(list(trajectories))
        out: dict[str, list[dict[str, Any]]] = {}
        for component in components_to_update:
            rows = [
                {
                    "minibatch_diagnostics": batch_diagnostics,
                    "selected_row_score": sum(scores) / max(1, len(scores)),
                    "reflection_hint": (
                        "This is aggregate context for the sampled rows. Use it to write "
                        "general boundary rules before inspecting individual row failures."
                    ),
                }
            ]
            for score_value, side_info in zip(scores, trajectories, strict=False):
                profiled = apply_row_feedback_profile(
                    side_info or {},
                    args.feedback_profile,
                    include_row_identifiers=args.reflection_include_row_identifiers,
                )
                row = {}
                for key, value in profiled.items():
                    row["Scores (Higher is Better)" if key == "scores" else key] = value
                row["selected_row_score"] = score_value
                rows.append(row)
            out[component] = rows
        return out

    return OpenClawRowWiseBatchAdapter(
        policy_char_budget=args.policy_char_budget,
        hygiene_penalty_weight=args.hygiene_penalty,
        mutable_boundary_overlay=bool(args.mutable_boundary_overlay),
        env_dir=ENV_DIR,
        agent_card=resolve_agent_card(args),
        agent="openclaw_vanilla_labeler_plain" if plain_labels else "openclaw_vanilla_labeler",
        candidate_variables=candidate_variables,
        template_source=TASK_TEMPLATE,
        schema=None if plain_labels else SCHEMA,
        model=args.model,
        parallel=args.parallel,
        row_scorer=row_scorer,
        run_dir=run_dir,
        id_field="id",
        backend="process",
        reflective_dataset_builder=reflective_dataset_builder,
    )


def resolve_parent_lineage(
    run_dir: Path,
    idx: int,
    seen_policies: list[tuple[int, str, str]],
) -> dict[str, Any]:
    """Attribute a candidate to the reflection call and parent policy that produced it.

    GEPA batch mode evaluates candidates sequentially, so the newest reflection
    call at scoring time is the proposal for this candidate. The reflection
    prompt embeds the parent policy verbatim; if several earlier policies
    substring-match, the longest match is the direct parent.
    """
    lineage: dict[str, Any] = {"parent_candidate_idx": None, "reflection_call": None}
    reflection_root = run_dir / "reflection"
    calls = sorted(reflection_root.glob("call-*")) if reflection_root.is_dir() else []
    if idx <= 1 or not calls:
        return lineage
    newest = calls[-1]
    lineage["reflection_call"] = newest.name
    try:
        prompt = (newest / "prompt.md").read_text(encoding="utf-8")
    except OSError:
        return lineage
    matches = [(p_idx, p_text) for p_idx, p_text, _ in seen_policies if p_text.strip() and p_text.strip() in prompt]
    if matches:
        parent_idx, _ = max(matches, key=lambda m: len(m[1]))
        lineage["parent_candidate_idx"] = parent_idx
    return lineage


def build_evaluator(run_dir: Path, input_path: Path, args: argparse.Namespace):
    plain_labels = args.plain_labels
    agent_card = resolve_agent_card(args)
    agent_name = "openclaw_vanilla_labeler_plain" if plain_labels else "openclaw_vanilla_labeler"
    candidate_variables = {"policy": "policy"}
    if args.mutable_boundary_overlay:
        candidate_variables["boundary_overlay"] = "boundary_overlay"

    fixed_asset_hashes = {
        name: {"path": str(path), "sha256": _sha256(path)}
        for name, path in {
            "agent_card": agent_card,
            "allowed_topics": args.allowed_topics,
            "seed_policy": args.seed_policy,
            "mutable_boundary_overlay_seed": args.mutable_boundary_overlay,
            "static_asi": args.static_asi,
            "optimizer_cues": args.optimizer_cues,
            "boundary_guidance": args.boundary_guidance,
            "input": input_path,
        }.items()
        if path is not None
    }
    seen_policies: list[tuple[int, str, str]] = []  # (candidate_idx, policy_text, policy_sha256)

    def resolve_parent(idx: int) -> dict[str, Any]:
        return resolve_parent_lineage(run_dir, idx, seen_policies)

    def score_candidate(
        result: BatchRunResult,
        candidate: Mapping[str, str],
        candidate_run: CandidateRun,
    ) -> tuple[float, dict[str, Any]]:
        policy = str(candidate.get("policy", ""))
        report = add_vanilla_asi(
            score_output_against_input(
                input_path=input_path,
                output_path=result.output_path,
                allowed=set(_schema_topic_contract()[0]),
                score_mode=args.score_mode,
                policy=policy,
                hygiene_penalty_weight=args.hygiene_penalty,
                policy_char_budget=args.policy_char_budget,
            ),
            policy,
            score_mode=args.score_mode,
            hygiene_penalty_weight=args.hygiene_penalty,
            policy_char_budget=args.policy_char_budget,
        )
        # The benchmark scorer may attach a static ASI pack as side-info. In
        # this runner, static domain context is supplied through GEPA's
        # background channel instead, so avoid duplicating that large pack in
        # every candidate trajectory.
        if report.pop("static_asi_pack", None) is not None:
            report["benchmark_static_asi_pack_omitted"] = True
        if args.static_asi:
            report["static_asi_path"] = str(args.static_asi)
        (candidate_run.path / "raw-evaluator-report.json").write_text(
            json.dumps(report, indent=2) + "\n",
            encoding="utf-8",
        )
        report = apply_feedback_profile(
            report,
            args.feedback_profile,
            mutable_overlay=bool(args.mutable_boundary_overlay),
        )
        idx = candidate_run.index or 0
        report["candidate_idx"] = idx
        report["execution_summary"] = summarize_batch_summary(result.summary)
        report["candidate_artifacts"] = {
            "results_jsonl": result.output_path.name,
            "policy": "policy.md",
            "boundary_overlay": "boundary-overlay.md" if args.mutable_boundary_overlay else None,
            "lineage": "lineage.json",
            "batch_summary": "batch-summary.json",
            "raw_evaluator_report": "raw-evaluator-report.json",
        }
        (candidate_run.path / "batch-summary.json").write_text(
            json.dumps(result.summary, indent=2) + "\n",
            encoding="utf-8",
        )
        (candidate_run.path / "policy.md").write_text(policy, encoding="utf-8")
        policy_sha = hashlib.sha256(policy.encode("utf-8")).hexdigest()
        boundary_overlay = str(candidate.get("boundary_overlay", ""))
        boundary_overlay_sha = None
        if args.mutable_boundary_overlay:
            (candidate_run.path / "boundary-overlay.md").write_text(boundary_overlay, encoding="utf-8")
            boundary_overlay_sha = hashlib.sha256(boundary_overlay.encode("utf-8")).hexdigest()
        lineage = {
            "candidate_idx": idx,
            "policy_sha256": policy_sha,
            "policy_chars": len(policy),
            "boundary_overlay_sha256": boundary_overlay_sha,
            "boundary_overlay_chars": len(boundary_overlay) if args.mutable_boundary_overlay else None,
            **resolve_parent(idx),
            "fixed_assets": fixed_asset_hashes,
            "task_model": args.model,
            "reflection_model": args.reflection_model,
            "score_mode": args.score_mode,
            "feedback_profile": args.feedback_profile,
        }
        (candidate_run.path / "lineage.json").write_text(json.dumps(lineage, indent=2), encoding="utf-8")
        seen_policies.append((idx, policy, policy_sha))
        report["lineage"] = {
            k: lineage[k]
            for k in (
                "policy_sha256",
                "boundary_overlay_sha256",
                "boundary_overlay_chars",
                "parent_candidate_idx",
                "reflection_call",
            )
        }
        log_candidate(idx, candidate_run.path, report)
        s = report["scores"]
        d = report["score_details"]
        print(
            f"candidate-{idx:04d}: f1={s['topic_micro_f1']:.4f} "
            f"p={d['topic_micro_precision']:.4f} r={d['topic_micro_recall']:.4f} "
            f"exact={d['exact_match']:.4f} chars={d['policy_chars']}"
        )
        side_info = dict(report)
        return float(s["gepa_score"]), side_info

    return FastAgentBatchEvaluator(
        env_dir=ENV_DIR,
        agent_card=agent_card,
        agent=agent_name,
        candidate_variables=candidate_variables,
        input=input_path,
        template_source=TASK_TEMPLATE,
        schema=None if args.plain_labels else SCHEMA,
        model=args.model,
        parallel=args.parallel,
        scorer=score_candidate,
        run_dir=run_dir,
        backend="process",
    )


def objective_text(
    *,
    plain_labels: bool,
    gepa_mode: str,
    score_mode: str,
    policy_char_budget: int,
    mutable_overlay: bool,
    feedback_profile: str,
) -> str:
    output_contract = (
        "plain comma-separated topic-ID output contract"
        if plain_labels
        else "JSON output contract"
    )
    mutable_scope = (
        "Improve only the mutable OpenClaw vanilla labeler routing policy and boundary_overlay components."
        if mutable_overlay
        else "Improve only the mutable OpenClaw vanilla labeler routing policy."
    )
    overlay_scope = (
        "\nThe boundary_overlay component is editable in this run. Keep it a general task-facing "
        "boundary overlay on top of the fixed taxonomy; do not change topic names, output format, "
        "schema constraints, or encode row-specific examples there.\n"
        if mutable_overlay
        else ""
    )
    feedback_clause = (
        "Use precision, recall, exact match, row Jaccard, row symdiff, cardinality, "
        "label error patterns, co-error pairs, row examples, and prompt-hygiene ASI to understand how "
        "to improve reliable row-level reproduction."
        if feedback_profile == "full"
        else "Use the shaped reflection side-info for this run; do not infer that omitted row examples or topic details are absent errors."
    )
    if gepa_mode == "row-wise":
        if score_mode == "f1":
            primary_objective = "maximize row-wise label membership F1 (`row_topic_f1`) on sampled rows"
        elif score_mode == "row-jaccard-exact":
            primary_objective = (
                "maximize strict row set score = 0.70*row_jaccard + 0.30*row_exact"
            )
        elif score_mode == "row-soft-exact":
            primary_objective = (
                "maximize softened row set score = "
                "0.60*row_jaccard + 0.20*row_topic_f1 + 0.20*row_exact"
            )
        else:
            primary_objective = (
                "maximize row-wise GEPA score = 0.50*row_topic_f1 + 0.20*row_exact + 0.30*row_jaccard"
            )
        objective_guard = (
            "This rewards finding every central qualifying label while penalizing extra labels. "
            "Do not improve apparent recall by padding labels; exact topic membership matters."
        )
    else:
        if score_mode == "f1":
            primary_objective = "maximize pure topic_micro_f1 against the frozen teacher/adjudicated labels"
        elif score_mode == "row-jaccard-exact":
            primary_objective = (
                "maximize strict aggregate row set score = "
                "0.70*avg_row_jaccard + 0.30*row_exact_accuracy"
            )
        elif score_mode == "row-soft-exact":
            primary_objective = (
                "maximize softened aggregate row set score = "
                "0.60*avg_row_jaccard + 0.20*topic_micro_f1 + 0.20*row_exact_accuracy"
            )
        else:
            primary_objective = (
                "maximize aggregate row-aware score = "
                "0.50*topic_micro_f1 + 0.20*row_exact_accuracy + 0.30*avg_row_jaccard"
            )
        objective_guard = "Do not improve apparent recall by padding labels; exact topic membership matters."
    return f"""{mutable_scope}

The fixed AgentCard header, {output_contract}, schema enum, GitHub context renderer,
and allowed-topic taxonomy are not editable.
{overlay_scope}

Primary objective: {primary_objective}. {objective_guard}

Feedback profile: {feedback_profile_description(feedback_profile)}
{feedback_clause}

Keep the policy vanilla and compact. Prefer short reusable centrality/cardinality rules
over a long topic-by-topic rulebook.

Keep the mutable policy under {policy_char_budget:,} characters; over-budget policies receive a small
GEPA score penalty, so compress rules instead of accumulating exhaustive topic tables.

{"Preserve comma-separated topic-ID-only behavior; do not ask for JSON, prose, bullets, or explanations." if plain_labels else "Preserve concise JSON-only behavior."}

Do not copy, rewrite, reorder, rename, delete, extend, or replace the fixed allowed-topic
list, topic definitions, or cue/keyword list. Reference exact existing topic IDs only
when a concise reusable boundary rule needs them.

Do not include row IDs, issue numbers, exact titles, URLs, or copied examples. Do not add
memorized issue/title/keyword tables.

Do not include data-build notes, version-history commentary, teacher/adjudication
procedure, promotion rules, or confusion-bucket bookkeeping in the task policy.
"""


def background_text(
    *,
    allowed_topics: Path,
    static_asi: Path | None,
    optimizer_cues: Path | None,
    mutable_boundary_overlay: Path | None,
    feedback_profile: str,
) -> str:
    sections = [
        f"""The task model sees this fixed taxonomy before the mutable policy:

```md
{allowed_topics.read_text(encoding="utf-8").strip()}
```"""
    ]
    sections.append(
        f"""Reflection feedback profile for this run:

{feedback_profile_description(feedback_profile)}

This profile controls only the optimizer/reflection side-info. It does not change
the deterministic scorer, train rows, benchmark rows, labels, schema, or task
model output contract."""
    )
    if mutable_boundary_overlay:
        sections.append(
            f"""This run has a second mutable GEPA component named `boundary_overlay`, seeded from
`{mutable_boundary_overlay}`. Treat it as task-facing boundary guidance, not as a
place to change the taxonomy, output contract, schema, or train-row facts. Use this
only to test whether the fixed v6h task overlay is holding back generalization."""
        )
    if static_asi:
        sections.append(
            f"""Static reflection/evaluator guidance follows. The task model does not see this
file unless GEPA distills a small piece of it into the mutable policy.

```md
{static_asi.read_text(encoding="utf-8").strip()}
```"""
        )
    if optimizer_cues:
        sections.append(
            f"""Optimizer-only cue/reference material follows. The task model does not see this file
unless you distill a small piece of it into the mutable policy. Use it to identify
transferable evidence patterns and topic-boundary distinctions. Do not copy or recreate
the cue table in the candidate policy.

```md
{optimizer_cues.read_text(encoding="utf-8").strip()}
```"""
        )
    return "\n\n".join(sections)


def _rel(path: Path | None) -> str | None:
    if path is None:
        return None
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return str(path)


def _sha256(path: Path) -> str | None:
    try:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def write_scoring_contract(run_dir: Path, args: argparse.Namespace) -> None:
    helper_source = inspect.getsource(openclaw_row_gepa_score).strip()
    py_text = f'''"""OpenClaw GEPA scoring contract emitted at run creation.

This file is an audit artifact. The active runner uses the same
`openclaw_row_gepa_score` helper for row-wise candidate scoring.
"""

ROW_WISE_FRONTIER_OBJECTIVE_KEYS = {row_wise_frontier_objective_keys(args.score_mode)!r}


{helper_source}
'''
    py_path = run_dir / "scoring-contract.py"
    py_path.write_text(py_text, encoding="utf-8")
    py_sha = hashlib.sha256(py_text.encode("utf-8")).hexdigest()

    payload = {
        "gepa_mode": args.gepa_mode,
        "score_mode": args.score_mode,
        "score_formula": score_formula_title(gepa_mode=args.gepa_mode, score_mode=args.score_mode),
        "row_wise": {
            "optimized_metric": "gepa_score",
            "formula": (
                "max(0.0, 0.70*row_jaccard + 0.30*row_exact - policy_penalty)"
                if args.score_mode == "row-jaccard-exact"
                else (
                    "max(0.0, 0.60*row_jaccard + 0.20*row_topic_f1 + 0.20*row_exact - policy_penalty)"
                    if args.score_mode == "row-soft-exact"
                    else "max(0.0, row_topic_f1 - policy_penalty)"
                    if args.score_mode == "f1"
                    else "max(0.0, 0.50*row_topic_f1 + 0.20*row_exact + 0.30*row_jaccard - policy_penalty)"
                )
            ),
            "frontier_objective_keys": list(row_wise_frontier_objective_keys(args.score_mode)),
            "all_values_are_higher_is_better": True,
            "policy_penalty_components": ["policy_length_penalty", "hygiene_penalty"],
        },
        "frontier": {
            "frontier_type": args.frontier_type,
            "candidate_selection_strategy": args.candidate_selection_strategy,
            "acceptance_criterion": _rowwise_acceptance_criterion(args.acceptance_criterion),
            "valid_frontier_types": ["instance", "objective", "hybrid", "cartesian"],
            "valid_candidate_selection_strategies": [
                "pareto",
                "current_best",
                "epsilon_greedy",
                "top_k_pareto",
            ],
            "valid_acceptance_criteria": ["strict_improvement", "improvement_or_equal"],
        },
        "python_contract": {
            "path": "scoring-contract.py",
            "sha256": py_sha,
            "function": "openclaw_row_gepa_score",
        },
    }
    json_path = run_dir / "scoring-contract.json"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (run_dir / "scoring-contract.sha256").write_text(
        f"{py_sha}  scoring-contract.py\n{_sha256(json_path)}  scoring-contract.json\n",
        encoding="utf-8",
    )


def _schema_topic_contract() -> tuple[list[str], int | None, int | None]:
    properties = json.loads(SCHEMA.read_text(encoding="utf-8"))["properties"]
    prop = properties.get("topics_of_interest") or properties.get("labels")
    if not isinstance(prop, dict):
        raise SystemExit(
            f"{SCHEMA} must define either properties.topics_of_interest or properties.labels"
        )
    enum = prop["items"]["enum"]
    return enum, prop.get("minItems"), prop.get("maxItems")


def validate_allowed_topics_against_schema(path: Path) -> None:
    if not path.exists():
        raise SystemExit(
            f"Allowed-topics file does not exist: {path}. "
            "Use a regime command or pass --allowed-topics explicitly."
        )
    if not SCHEMA.exists():
        raise SystemExit(f"Output schema file does not exist: {SCHEMA}")
    text = path.read_text(encoding="utf-8")
    match = re.search(r"```json\s*(\[.*?\])\s*```", text, re.S)
    if not match:
        raise SystemExit(f"{path} must contain a JSON topic list fenced as ```json ... ```")
    try:
        topics = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path} contains an invalid JSON topic list: {exc}") from exc
    if not isinstance(topics, list) or not all(isinstance(topic, str) for topic in topics):
        raise SystemExit(f"{path} JSON topic list must be a list of strings")

    schema_topics, _, _ = _schema_topic_contract()
    if topics != schema_topics:
        missing = [topic for topic in schema_topics if topic not in topics]
        extra = [topic for topic in topics if topic not in schema_topics]
        raise SystemExit(
            f"{path} does not match {SCHEMA}. "
            f"Missing from allowed-topics: {missing}; extra in allowed-topics: {extra}."
        )


def _expected_topics_for_input_row(row: Mapping[str, Any]) -> Any:
    inp = row.get("input") if isinstance(row.get("input"), dict) else row
    for key in ("expected_topics", "topics_of_interest", "labels"):
        if key in inp:
            return inp[key]
    return None


def _require_file_arg(name: str, path: Path | None) -> Path | None:
    if path is None:
        return None
    try:
        return path.resolve(strict=True)
    except FileNotFoundError as exc:
        raise SystemExit(f"{name} does not exist: {path}") from exc
    except OSError as exc:
        raise SystemExit(f"{name} is not readable: {path}: {exc}") from exc


def resolve_file_args(args: argparse.Namespace) -> None:
    for name in (
        "input",
        "feedback_input",
        "pareto_input",
        "test_input",
        "seed_policy",
        "static_asi",
        "optimizer_cues",
        "agent_card",
        "allowed_topics",
        "mutable_boundary_overlay",
        "boundary_guidance",
    ):
        setattr(args, name, _require_file_arg(f"--{name.replace('_', '-')}", getattr(args, name)))


def validate_input_labels_against_schema(path: Path) -> None:
    schema_topics, min_items, max_items = _schema_topic_contract()
    allowed = set(schema_topics)
    problems: list[str] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            problems.append(f"line {line_no}: invalid JSON: {exc}")
            continue
        if not isinstance(row, dict):
            problems.append(f"line {line_no}: row must be a JSON object")
            continue

        labels = _expected_topics_for_input_row(row)
        row_id = row.get("id")
        if not row_id and isinstance(row.get("input"), dict):
            row_id = row["input"].get("id")
        prefix = f"line {line_no}" + (f" ({row_id})" if row_id else "")
        if not isinstance(labels, list) or not all(isinstance(label, str) for label in labels):
            problems.append(f"{prefix}: expected_topics/topics_of_interest/labels must be a list of strings")
            continue
        invalid = sorted(set(labels) - allowed)
        if invalid:
            problems.append(f"{prefix}: labels not in {SCHEMA.name}: {invalid}")
        if min_items is not None and len(labels) < min_items:
            problems.append(f"{prefix}: has {len(labels)} labels, below schema minItems={min_items}")
        if max_items is not None and len(labels) > max_items:
            problems.append(f"{prefix}: has {len(labels)} labels, above schema maxItems={max_items}: {labels}")
        if len(problems) >= 12:
            break

    if problems:
        joined = "\n- ".join(problems)
        raise SystemExit(f"Input labels violate the active output schema {SCHEMA}:\n- {joined}")


def validate_boundary_guidance(path: Path | None) -> int | None:
    if path is None:
        return None
    hints = load_topic_hints_from_guidance(path)
    allowed_enum = set(_schema_topic_contract()[0])
    unknown = sorted(set(hints) - allowed_enum)
    if unknown:
        raise SystemExit(
            f"--boundary-guidance contains topics not in the schema enum: {unknown}; "
            "reconcile the frozen spec with the taxonomy before running."
        )
    return len(hints)


def validate_reflection_agent(args: argparse.Namespace) -> None:
    env_config = args.reflection_env_dir / "fast-agent.yaml"
    agent_card = args.reflection_env_dir / "agent-cards" / f"{args.reflection_agent}.md"
    if not env_config.exists():
        raise SystemExit(f"--reflection-env-dir is missing fast-agent.yaml: {env_config}")
    if not agent_card.exists():
        raise SystemExit(f"--reflection-agent card does not exist: {agent_card}")


def print_preflight_result(
    *,
    args: argparse.Namespace,
    run_input_source: Path,
    active_card: Path,
    boundary_hint_count: int | None,
) -> None:
    payload = {
        "ok": True,
        "mode": "preflight",
        "gepa_mode": args.gepa_mode,
        "evaluate_only": args.evaluate_only,
        "score_mode": args.score_mode,
        "plain_labels": args.plain_labels,
        "input": str(run_input_source),
        "input_rows": _jsonl_rows(run_input_source),
        "feedback_input": str(args.feedback_input) if args.feedback_input else None,
        "pareto_input": str(args.pareto_input) if args.pareto_input else None,
        "test_input": str(args.test_input) if args.test_input else None,
        "agent_card": str(active_card),
        "allowed_topics": str(args.allowed_topics),
        "seed_policy": str(args.seed_policy),
        "boundary_guidance": str(args.boundary_guidance) if args.boundary_guidance else None,
        "boundary_guidance_topics": boundary_hint_count,
        "reflection_env_dir": str(args.reflection_env_dir),
        "reflection_agent": args.reflection_agent,
        "project": args.project,
        "trackio_group": args.trackio_group,
        "run_root": str(args.run_root),
        "run_name": args.run_name,
    }
    if args.gepa_mode == "row-wise" and not args.evaluate_only:
        try:
            from gepa.api import optimize

            planned_kwargs = rowwise_optimize_kwargs(
                args=args,
                seed={},
                feedback_rows=[],
                pareto_rows=[],
                adapter=None,
                reflection_lm=None,
                reflection_prompt_template="",
                reflection_minibatch_size=args.reflection_minibatch_size or 3,
                custom_candidate_proposer=None,
                run_dir=args.run_root,
                trackio_enabled=False,
                callbacks=[],
            )
            _, unsupported = filter_supported_kwargs(optimize, planned_kwargs)
            payload["gepa_optimize_signature"] = {
                "unsupported_runner_kwargs": sorted(unsupported),
            }
        except ImportError:
            payload["gepa_optimize_signature"] = {"error": "gepa.api.optimize is not importable"}
    print(json.dumps(payload, indent=2))


def _jsonl_rows(path: Path | None) -> int | None:
    if path is None or not path.exists():
        return None
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def _rowwise_acceptance_criterion(value: str) -> str:
    return "strict_improvement" if value == "improvement" else value


def filter_supported_kwargs(fn: Any, kwargs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    signature = inspect.signature(fn)
    if any(param.kind == inspect.Parameter.VAR_KEYWORD for param in signature.parameters.values()):
        return kwargs, {}
    supported = set(signature.parameters)
    accepted = {key: value for key, value in kwargs.items() if key in supported}
    dropped = {key: value for key, value in kwargs.items() if key not in supported}
    return accepted, dropped


def warn_unsupported_gepa_kwargs(fn: Any, kwargs: dict[str, Any]) -> None:
    _, dropped = filter_supported_kwargs(fn, kwargs)
    if dropped:
        print(
            "Installed GEPA optimize() does not accept these runner kwargs; "
            f"continuing without them: {', '.join(sorted(dropped))}",
            file=sys.stderr,
        )


def rowwise_optimize_kwargs(
    *,
    args: argparse.Namespace,
    seed: dict[str, str],
    feedback_rows: list[dict[str, Any]],
    pareto_rows: list[dict[str, Any]],
    adapter: Any,
    reflection_lm: Any,
    reflection_prompt_template: str,
    reflection_minibatch_size: int,
    custom_candidate_proposer: Any | None,
    run_dir: Path,
    trackio_enabled: bool,
    callbacks: list[Any],
) -> dict[str, Any]:
    return {
        "seed_candidate": seed,
        "trainset": feedback_rows,
        "valset": pareto_rows,
        "adapter": adapter,
        "reflection_lm": reflection_lm,
        "reflection_prompt_template": reflection_prompt_template,
        "reflection_minibatch_size": reflection_minibatch_size,
        "custom_candidate_proposer": custom_candidate_proposer,
        "candidate_selection_strategy": args.candidate_selection_strategy,
        "frontier_type": args.frontier_type,
        "acceptance_criterion": _rowwise_acceptance_criterion(args.acceptance_criterion),
        "skip_perfect_score": False,
        "max_metric_calls": args.max_metric_calls,
        "run_dir": str(run_dir),
        "cache_evaluation": True,
        "use_trackio": trackio_enabled,
        "trackio_attach_existing": trackio_enabled,
        "trackio_step_metric": "gepa/iteration",
        "tracking_key_prefix": "gepa/",
        "track_best_outputs": True,
        "display_progress_bar": False,
        "callbacks": callbacks,
    }


def _version(package: str) -> str | None:
    try:
        return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return None


def _git_info() -> dict[str, Any]:
    def run(*cmd: str) -> str | None:
        proc = subprocess.run(
            ["git", "-C", str(ROOT), *cmd],
            text=True,
            capture_output=True,
            check=False,
        )
        return proc.stdout.strip() if proc.returncode == 0 else None

    status = run("status", "--short")
    return {
        "commit": run("rev-parse", "HEAD"),
        "branch": run("branch", "--show-current"),
        "dirty": bool(status),
        "status_short": status,
    }


def write_run_metadata(
    *,
    args: argparse.Namespace,
    run_name: str,
    run_dir: Path,
    active_card: Path,
    objective: str,
    background: str,
) -> None:
    input_rows = sum(1 for line in (run_dir / "input.jsonl").read_text(encoding="utf-8").splitlines() if line.strip())
    copied = {
        "input": run_dir / "input.jsonl",
        "agent_card": run_dir / "openclaw-vanilla-labeler.md",
        "seed_policy": run_dir / "seed-policy.md",
        "allowed_topics": run_dir / "allowed-topics.md",
        "objective": run_dir / "objective.md",
        "background": run_dir / "background.md",
        "scoring_contract_python": run_dir / "scoring-contract.py",
        "scoring_contract_json": run_dir / "scoring-contract.json",
        "scoring_contract_sha256": run_dir / "scoring-contract.sha256",
        "mutable_boundary_overlay_seed": (
            run_dir / "mutable-boundary-overlay-seed.md" if args.mutable_boundary_overlay else None
        ),
        "static_asi": run_dir / "static-asi.md" if args.static_asi else None,
        "optimizer_cues": run_dir / "optimizer-cues.md" if args.optimizer_cues else None,
        "boundary_guidance": run_dir / "boundary-guidance.md" if args.boundary_guidance else None,
        "feedback_input": run_dir / "feedback-input.jsonl" if args.feedback_input else None,
        "pareto_input": run_dir / "pareto-input.jsonl" if args.pareto_input else None,
        "test_input": run_dir / "test-input.jsonl" if args.test_input else None,
    }
    feedback_run_path = run_dir / "feedback-input.jsonl" if args.feedback_input else run_dir / "input.jsonl"
    pareto_run_path = run_dir / "pareto-input.jsonl" if args.pareto_input else feedback_run_path
    effective_input = args.feedback_input if args.gepa_mode == "row-wise" and args.feedback_input else args.input
    payload = {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "run_name": run_name,
        "run_dir": _rel(run_dir),
        "script": _rel(Path(__file__)),
        "command": sys.argv,
        "mode": {
            "gepa_mode": args.gepa_mode,
            "score_mode": args.score_mode,
            "plain_labels": args.plain_labels,
            "feedback_profile": args.feedback_profile,
            "candidate_proposer": args.candidate_proposer,
            "mutable_boundary_overlay": bool(args.mutable_boundary_overlay),
            "frontier_type": args.frontier_type,
            "candidate_selection_strategy": args.candidate_selection_strategy,
            "acceptance_criterion": _rowwise_acceptance_criterion(args.acceptance_criterion),
            "allow_padded_minibatches": args.allow_padded_minibatches,
            "reflection_include_row_identifiers": args.reflection_include_row_identifiers,
            "output_contract": "comma-separated topic IDs" if args.plain_labels else "structured JSON",
            "score": score_formula_title(gepa_mode=args.gepa_mode, score_mode=args.score_mode),
        },
        "models": {
            "task_model": args.model,
            "reflection_model": args.reflection_model,
            "reflection_agent": args.reflection_agent,
            "reflection_env_dir": _rel(args.reflection_env_dir),
            "reflection_agent_card": _rel(
                args.reflection_env_dir / "agent-cards" / f"{args.reflection_agent}.md"
            ),
        },
        "budget": {
            "max_metric_calls": args.max_metric_calls,
            "reflection_minibatch_size": args.reflection_minibatch_size,
            "parallel": args.parallel,
        },
        "inputs": {
            "input": _rel(effective_input),
            "input_arg": _rel(args.input),
            "input_rows": input_rows,
            "feedback_input": _rel(args.feedback_input),
            "feedback_rows": _jsonl_rows(feedback_run_path),
            "pareto_input": _rel(args.pareto_input),
            "pareto_rows": _jsonl_rows(pareto_run_path),
            "test_input": _rel(args.test_input),
            "test_rows": _jsonl_rows(args.test_input),
            "seed_policy": _rel(args.seed_policy),
            "mutable_boundary_overlay_seed": _rel(args.mutable_boundary_overlay),
            "static_asi": _rel(args.static_asi),
            "optimizer_cues": _rel(args.optimizer_cues),
            "boundary_guidance": _rel(args.boundary_guidance),
            "agent_card_requested": _rel(args.agent_card),
            "agent_card_resolved": _rel(active_card),
            "allowed_topics": _rel(args.allowed_topics),
        },
        "artifacts": {
            name: {"path": _rel(path), "sha256": _sha256(path)} for name, path in copied.items() if path is not None
        },
        "prompt_sizes": {
            "objective_chars": len(objective),
            "background_chars": len(background),
        },
        "tracking": {
            "trackio_enabled": not args.no_trackio,
            "project": args.project,
            "group": args.trackio_group,
            "trackio_space_id": args.trackio_space_id,
            "trackio_server_url": args.trackio_server_url,
        },
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "packages": {
                "gepa": _version("gepa"),
                "fast-agent-mcp": _version("fast-agent-mcp"),
                "trackio": _version("trackio"),
            },
        },
        "git": _git_info(),
    }
    (run_dir / "run.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    resolve_file_args(args)
    validate_allowed_topics_against_schema(args.allowed_topics)
    run_input_source = args.feedback_input if args.gepa_mode == "row-wise" and args.feedback_input else args.input
    validate_input_labels_against_schema(run_input_source)
    if args.pareto_input:
        validate_input_labels_against_schema(args.pareto_input)
    if args.test_input:
        validate_input_labels_against_schema(args.test_input)
    active_card = resolve_agent_card(args)
    if not active_card.exists():
        raise SystemExit(f"resolved AgentCard does not exist: {active_card}")
    boundary_hint_count = validate_boundary_guidance(args.boundary_guidance)
    validate_reflection_agent(args)
    if args.preflight_only:
        print_preflight_result(
            args=args,
            run_input_source=run_input_source,
            active_card=active_card,
            boundary_hint_count=boundary_hint_count,
        )
        return 0
    run_name = args.run_name or time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    run_dir = args.run_root / run_name
    run_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(run_input_source, run_dir / "input.jsonl")
    if args.feedback_input:
        shutil.copy2(args.feedback_input, run_dir / "feedback-input.jsonl")
    if args.pareto_input:
        shutil.copy2(args.pareto_input, run_dir / "pareto-input.jsonl")
    if args.test_input:
        shutil.copy2(args.test_input, run_dir / "test-input.jsonl")
    shutil.copy2(active_card, run_dir / "openclaw-vanilla-labeler.md")
    shutil.copy2(args.seed_policy, run_dir / "seed-policy.md")
    shutil.copy2(args.allowed_topics, run_dir / "allowed-topics.md")
    if args.mutable_boundary_overlay:
        shutil.copy2(args.mutable_boundary_overlay, run_dir / "mutable-boundary-overlay-seed.md")
    if args.static_asi:
        shutil.copy2(args.static_asi, run_dir / "static-asi.md")
    if args.optimizer_cues:
        shutil.copy2(args.optimizer_cues, run_dir / "optimizer-cues.md")
    if args.boundary_guidance:
        shutil.copy2(args.boundary_guidance, run_dir / "boundary-guidance.md")
        print(
            f"boundary guidance: TOPIC_HINTS replaced from "
            f"{args.boundary_guidance} ({boundary_hint_count} topics)"
        )
    objective = objective_text(
        plain_labels=args.plain_labels,
        gepa_mode=args.gepa_mode,
        score_mode=args.score_mode,
        policy_char_budget=args.policy_char_budget,
        mutable_overlay=bool(args.mutable_boundary_overlay),
        feedback_profile=args.feedback_profile,
    )
    background = background_text(
        allowed_topics=args.allowed_topics,
        static_asi=args.static_asi,
        optimizer_cues=args.optimizer_cues,
        mutable_boundary_overlay=args.mutable_boundary_overlay,
        feedback_profile=args.feedback_profile,
    )
    (run_dir / "objective.md").write_text(objective, encoding="utf-8")
    (run_dir / "background.md").write_text(background, encoding="utf-8")
    write_scoring_contract(run_dir, args)
    write_run_metadata(
        args=args,
        run_name=run_name,
        run_dir=run_dir,
        active_card=active_card,
        objective=objective,
        background=background,
    )
    trackio_enabled = init_trackio(args, run_name, run_dir)

    seed = {"policy": args.seed_policy.read_text(encoding="utf-8")}
    if args.mutable_boundary_overlay:
        seed["boundary_overlay"] = args.mutable_boundary_overlay.read_text(encoding="utf-8")
    evaluator = build_evaluator(run_dir, run_dir / "input.jsonl", args)
    try:
        if args.evaluate_only:
            score_value, report = evaluator(seed)
            payload = {"score": score_value, "run_dir": str(run_dir), **report}
            (run_dir / "evaluate-only.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
            print(json.dumps(payload, indent=2))
            return 0

        try:
            from gepa.optimize_anything import EngineConfig, GEPAConfig, ReflectionConfig, TrackingConfig, optimize_anything
        except ImportError:
            print("GEPA is not importable. Run with uv sync or PYTHONPATH including GEPA.", file=sys.stderr)
            return 2

        if args.gepa_mode == "row-wise":
            try:
                from gepa.api import optimize
                from gepa.optimize_anything import _build_reflection_prompt_template
            except ImportError:
                print("GEPA adapter API is not importable. Run with PYTHONPATH including GEPA.", file=sys.stderr)
                return 2

            feedback_path = run_dir / "feedback-input.jsonl" if (run_dir / "feedback-input.jsonl").exists() else run_dir / "input.jsonl"
            pareto_path = run_dir / "pareto-input.jsonl" if (run_dir / "pareto-input.jsonl").exists() else feedback_path
            feedback_rows = [json.loads(line) for line in feedback_path.read_text(encoding="utf-8").splitlines() if line.strip()]
            pareto_rows = [json.loads(line) for line in pareto_path.read_text(encoding="utf-8").splitlines() if line.strip()]
            reflection_minibatch_size = args.reflection_minibatch_size or 3
            if len(feedback_rows) % reflection_minibatch_size != 0 and not args.allow_padded_minibatches:
                raise SystemExit(
                    "Refusing to run row-wise GEPA with padded epoch minibatches: "
                    f"feedback rows={len(feedback_rows)} is not divisible by "
                    f"--reflection-minibatch-size={reflection_minibatch_size}. "
                    "Choose a divisor of the feedback row count or pass --allow-padded-minibatches "
                    "for a smoke/debug run."
                )
            min_calls = len(pareto_rows)
            approx_calls_per_accepted = (2 * reflection_minibatch_size) + len(pareto_rows)
            recommended_min = min_calls + 10 * approx_calls_per_accepted
            if args.max_metric_calls <= len(pareto_rows):
                print(
                    f"Warning: row-wise mode counts one metric call per row. "
                    f"--max-metric-calls={args.max_metric_calls} is <= {len(pareto_rows)} Pareto rows, "
                    "so the run may stop after the seed Pareto evaluation.",
                    file=sys.stderr,
                )
            elif args.max_metric_calls < recommended_min:
                print(
                    f"Warning: row-wise clean-regime budget is low for multiple accepted proposals. "
                    f"Dpareto={len(pareto_rows)}, reflection_minibatch_size={reflection_minibatch_size}, "
                    f"approx accepted proposal cost={approx_calls_per_accepted}; "
                    f"recommended minimum for ~10 accepted proposals is {recommended_min}, "
                    f"got --max-metric-calls={args.max_metric_calls}.",
                    file=sys.stderr,
                )
            adapter = build_row_wise_adapter(run_dir, args)
            reflection_lm = FastAgentReflectionLM(
                env_dir=args.reflection_env_dir,
                model=args.reflection_model,
                agent=args.reflection_agent,
                audit_dir=run_dir / "reflection",
            )
            allowed_enum = set(_schema_topic_contract()[0])
            custom_candidate_proposer = build_custom_candidate_proposer(args, reflection_lm)
            callbacks = [
                FastAgentGEPATrackioCallback(
                    row_wise_adapter=adapter,
                    reflection_lm=reflection_lm,
                    include_gepa_context=False,
                    include_eval_score_summary=False,
                ),
                OpenClawCandidateDiagnosticsCallback(adapter),
                OpenClawValsetAggregateCallback(
                    val_rows=pareto_rows,
                    allowed_topics=allowed_enum,
                    score_mode=args.score_mode,
                ),
            ]
            optimize_kwargs = rowwise_optimize_kwargs(
                args=args,
                seed=seed,
                feedback_rows=feedback_rows,
                pareto_rows=pareto_rows,
                adapter=adapter,
                reflection_lm=reflection_lm,
                reflection_prompt_template=_build_reflection_prompt_template(
                    objective=objective,
                    background=background,
                ),
                reflection_minibatch_size=reflection_minibatch_size,
                custom_candidate_proposer=custom_candidate_proposer,
                run_dir=run_dir,
                trackio_enabled=trackio_enabled,
                callbacks=callbacks,
            )
            warn_unsupported_gepa_kwargs(optimize, optimize_kwargs)
            supported_kwargs, _ = filter_supported_kwargs(optimize, optimize_kwargs)
            result = optimize(**supported_kwargs)
            best = result.best_candidate
            (run_dir / "best-candidate.json").write_text(json.dumps(best, indent=2), encoding="utf-8")
            if isinstance(best, dict) and "policy" in best:
                (run_dir / "best-policy.md").write_text(best["policy"], encoding="utf-8")
            if isinstance(best, dict) and "boundary_overlay" in best:
                (run_dir / "best-boundary-overlay.md").write_text(best["boundary_overlay"], encoding="utf-8")
            (run_dir / "row-wise-result.json").write_text(
                json.dumps(
                    {
                        "best_idx": result.best_idx,
                        "best_score": result.val_aggregate_scores[result.best_idx],
                        "val_aggregate_scores": result.val_aggregate_scores,
                        "total_metric_calls": result.total_metric_calls,
                        "gepa_mode": args.gepa_mode,
                        "feedback_rows": len(feedback_rows),
                        "pareto_rows": len(pareto_rows),
                        "frontier_type": args.frontier_type,
                        "candidate_selection_strategy": args.candidate_selection_strategy,
                        "acceptance_criterion": _rowwise_acceptance_criterion(args.acceptance_criterion),
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            print(f"Best row-wise GEPA policy written under {run_dir}")
            return 0

        result = optimize_anything(
            seed_candidate=seed,
            evaluator=evaluator,
            objective=objective,
            background=background,
            config=GEPAConfig(
                engine=EngineConfig(max_metric_calls=args.max_metric_calls, cache_evaluation=True),
                reflection=ReflectionConfig(
                    reflection_minibatch_size=args.reflection_minibatch_size,
                    reflection_lm=FastAgentReflectionLM(
                        env_dir=args.reflection_env_dir,
                        model=args.reflection_model,
                        agent=args.reflection_agent,
                        audit_dir=run_dir / "reflection",
                    )
                ),
                tracking=TrackingConfig(
                    use_trackio=trackio_enabled,
                    trackio_attach_existing=trackio_enabled,
                    trackio_step_metric="gepa/iteration",
                    key_prefix="gepa/",
                ),
            ),
        )
        best = result.best_candidate
        (run_dir / "best-candidate.json").write_text(json.dumps(best, indent=2), encoding="utf-8")
        if isinstance(best, dict) and "policy" in best:
            (run_dir / "best-policy.md").write_text(best["policy"], encoding="utf-8")
        if isinstance(best, dict) and "boundary_overlay" in best:
            (run_dir / "best-boundary-overlay.md").write_text(best["boundary_overlay"], encoding="utf-8")
        print(f"Best vanilla F1 policy written under {run_dir}")
        return 0
    finally:
        finish_trackio(trackio_enabled)


if __name__ == "__main__":
    raise SystemExit(main())
