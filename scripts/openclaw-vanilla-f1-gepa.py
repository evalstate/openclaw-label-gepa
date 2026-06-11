#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from fast_agent.batch import BatchRunResult, BatchRunner
from fast_agent.eval import CandidateRun
from fast_agent.integrations.gepa import FastAgentBatchEvaluator, FastAgentReflectionLM
from fast_agent.utils.async_utils import run_coroutine
from openclaw_gepa.openclaw_benchmark import (
    ENV_DIR,
    ROOT,
    SCHEMA,
    TASK_TEMPLATE,
    extract_output_text,
    extract_result,
    f1 as topic_f1,
    load_topic_hints_from_guidance,
    parse_label_text,
    score,
    topic_hint,
    write_jsonl,
)


RUN_ROOT = ROOT / "runs" / "openclaw-vanilla-f1-gepa"
CARD = ROOT / ".fast-agent" / "agent-cards" / "openclaw-vanilla-labeler.md"
PLAIN_CARD = ROOT / ".fast-agent" / "agent-cards" / "openclaw-vanilla-labeler-plain.md"
SEED_POLICY = ROOT / "seed" / "openclaw-vanilla-f1" / "policy.md"
DEFAULT_INPUT = ROOT / "eval" / "openclaw" / "label-generator" / "gepa-good-60.jsonl"
ALLOWED_TOPICS = ROOT / "eval" / "openclaw" / "allowed-topics.md"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="GEPA-optimize a vanilla OpenClaw labeler with pure micro-F1 scoring.")
    p.add_argument("--model", default="codexresponses.gpt-5.5?reasoning=high")
    p.add_argument("--reflection-model", default="codexresponses.gpt-5.5?reasoning=high")
    p.add_argument("--input", type=Path, default=DEFAULT_INPUT)
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
    p.add_argument("--run-name", default=None)
    p.add_argument("--run-root", type=Path, default=RUN_ROOT, help="Directory under which this run directory is created.")
    p.add_argument("--parallel", type=int, default=4)
    p.add_argument("--max-metric-calls", type=int, default=12)
    p.add_argument(
        "--score-mode",
        choices=["f1", "row-aware"],
        default="f1",
        help="GEPA scoring mode. row-aware uses 0.50*micro-F1 + 0.20*row-exact + 0.30*row-Jaccard and exposes row metrics as frontier scores.",
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
            "Applied in batch mode candidate scoring."
        ),
    )
    p.add_argument(
        "--policy-char-budget",
        type=int,
        default=12_000,
        help="Policy length budget in characters before the length penalty starts (v5 default 12000).",
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
        "--reflection-minibatch-size",
        type=int,
        default=None,
        help="GEPA reflection minibatch size. Useful with --gepa-mode row-wise.",
    )
    p.add_argument("--evaluate-only", action="store_true")
    p.add_argument("--no-trackio", action="store_true")
    p.add_argument("--project", default="openclaw-vanilla-f1")
    p.add_argument("--trackio-space-id", default=os.environ.get("TRACKIO_SPACE_ID"))
    p.add_argument("--trackio-server-url", default=os.environ.get("TRACKIO_SERVER_URL"))
    return p.parse_args()


def init_trackio(args: argparse.Namespace, run_name: str, run_dir: Path) -> bool:
    if args.no_trackio:
        return False
    try:
        import trackio
    except Exception as e:
        print(f"Trackio unavailable; continuing without it: {e}", file=sys.stderr)
        return False
    kwargs: dict[str, Any] = {
        "project": args.project,
        "name": run_name,
        "group": "openclaw-vanilla-f1-gepa",
        "embed": False,
        "auto_log_gpu": False,
        "config": {
            "task_model": args.model,
            "reflection_model": args.reflection_model,
            "input": str(args.input),
            "seed_policy": str(args.seed_policy),
            "static_asi": str(args.static_asi) if args.static_asi else None,
            "optimizer_cues": str(args.optimizer_cues) if args.optimizer_cues else None,
            "max_metric_calls": args.max_metric_calls,
            "score_mode": args.score_mode,
            "gepa_mode": args.gepa_mode,
            "reflection_minibatch_size": args.reflection_minibatch_size,
            "run_dir": str(run_dir),
            "run_root": str(args.run_root),
            "score": "topic_micro_f1" if args.score_mode == "f1" else "0.50*topic_micro_f1+0.20*row_exact_accuracy+0.30*avg_row_jaccard",
            "plain_labels": args.plain_labels,
        },
    }
    if args.trackio_space_id:
        kwargs["space_id"] = args.trackio_space_id
    if args.trackio_server_url:
        kwargs["server_url"] = args.trackio_server_url
    trackio.init(**kwargs)
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
    try:
        import trackio

        scores = report.get("scores", {})
        details = report.get("score_details", {})
        program_idx = candidate_idx - 1
        payload: dict[str, int | float] = {
            "gepa/iteration": program_idx,
            "candidate/local_idx": candidate_idx,
            "candidate/program_idx": program_idx,
        }
        for key in ["gepa_score", "topic_micro_f1", "row_exact_accuracy", "avg_row_jaccard", "row_symdiff_score"]:
            if isinstance(scores.get(key), int | float):
                payload[f"candidate/{key}"] = scores[key]
        for key in [
            "topic_micro_precision",
            "topic_micro_recall",
            "exact_match",
            "row_exact_accuracy",
            "avg_row_jaccard",
            "avg_row_symdiff",
            "row_symdiff_score",
            "valid_json",
            "cardinality_closeness",
            "avg_expected_topics",
            "avg_predicted_topics",
            "false_positives",
            "false_negatives",
            "policy_chars",
        ]:
            if isinstance(details.get(key), int | float):
                payload[f"candidate/detail/{key}"] = details[key]
        trackio.log(payload)
    except Exception:
        return


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


def add_vanilla_asi(
    report: dict[str, Any],
    policy: str,
    *,
    score_mode: str = "f1",
    hygiene_penalty_weight: float = 0.0,
    policy_char_budget: int = 12_000,
) -> dict[str, Any]:
    original_scores = dict(report.get("scores", {}))
    details = report.setdefault("score_details", {})

    precision = _num(original_scores.get("topic_micro_precision"))
    recall = _num(original_scores.get("topic_micro_recall"))
    f1 = _num(original_scores.get("topic_micro_f1"))
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
    hygiene = policy_hygiene(policy)
    policy_chars = hygiene["policy_chars"]
    policy_length_over_budget = max(0, policy_chars - policy_char_budget)
    policy_length_penalty = min(0.10, (policy_length_over_budget / 10_000) * 0.05)
    policy_length_compliance = 1.0 - (policy_length_penalty / 0.10)
    hygiene_penalty = hygiene_penalty_weight * len(hygiene["findings"])
    hygiene_compliance = 1.0 if hygiene["ok"] else max(0.0, 1.0 - hygiene_penalty / 0.10)

    if score_mode == "row-aware":
        composite_score = 0.50 * f1 + 0.20 * row_exact + 0.30 * avg_row_jaccard
        gepa_score = max(0.0, composite_score - policy_length_penalty - hygiene_penalty)
        # Frontier-safe: all values in scores are higher-is-better.
        report["scores"] = {
            "gepa_score": gepa_score,
            "composite_score": composite_score,
            "topic_micro_f1": f1,
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
            "policy_length_compliance": policy_length_compliance,
        }
        if hygiene_penalty_weight > 0:
            report["scores"]["policy_hygiene_compliance"] = hygiene_compliance
    details.update(
        {
            "topic_micro_precision": precision,
            "topic_micro_recall": recall,
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
        cardinality_action = "Cardinality is close; focus on topic-specific confusions and boundary errors."

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
        f"Pure-F1 objective: optimize exact topic membership, not recall-biased F-beta. "
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


def score_row_output(row: dict[str, Any], *, allowed: set[str], score_mode: str) -> tuple[float, dict[str, Any]]:
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
    gepa_score = row_f1 if score_mode == "f1" else 0.50 * row_f1 + 0.20 * row_exact + 0.30 * row_jaccard

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
            "row_topic_f1": row_f1,
            "row_exact": row_exact,
            "row_jaccard": row_jaccard,
            "valid_json": valid_json,
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
    return gepa_score, side_info


class OpenClawRowWiseAdapter:
    """GEPA adapter that exposes OpenClaw rows as individual validation instances."""

    propose_new_texts = None

    def __init__(self, *, run_dir: Path, args: argparse.Namespace):
        self.run_dir = run_dir
        self.args = args
        self.plain_labels = args.plain_labels
        self.agent_card = resolve_agent_card(args)
        self.agent_name = "openclaw_vanilla_labeler_plain" if self.plain_labels else "openclaw_vanilla_labeler"
        self.allowed = set(json.loads(SCHEMA.read_text())["properties"]["topics_of_interest"]["items"]["enum"])
        self.eval_idx = 0

    def evaluate(self, batch: list[dict[str, Any]], candidate: dict[str, str], capture_traces: bool = False):
        from gepa.core.adapter import EvaluationBatch

        self.eval_idx += 1
        eval_dir = self.run_dir / "row-wise-evals" / f"eval-{self.eval_idx:05d}"
        eval_dir.mkdir(parents=True, exist_ok=True)
        input_path = eval_dir / "input.jsonl"
        write_jsonl(input_path, [dict(row) for row in batch])

        result = run_coroutine(
            BatchRunner(env_dir=ENV_DIR, backend="process").run(
                input=input_path,
                output_path=eval_dir / "results.jsonl",
                agent_card=self.agent_card,
                agent=self.agent_name,
                template_source=TASK_TEMPLATE,
                json_schema=None if self.plain_labels else SCHEMA,
                model=self.args.model,
                parallel=min(self.args.parallel, max(1, len(batch))),
                include_input=True,
                variables={"policy": candidate.get("policy", "")},
                summary_path=eval_dir / "batch-summary.json",
                telemetry_path=eval_dir / "telemetry.jsonl",
                overwrite=True,
            )
        )

        scores: list[float] = []
        trajectories: list[dict[str, Any]] = []
        for output_row in result.rows:
            row_score, side_info = score_row_output(output_row, allowed=self.allowed, score_mode=self.args.score_mode)
            scores.append(row_score)
            trajectories.append(side_info)

        # Be defensive if the batch runner returns fewer rows after a systemic row failure.
        while len(scores) < len(batch):
            scores.append(0.0)
            trajectories.append(
                {
                    "scores": {"gepa_score": 0.0, "row_topic_f1": 0.0, "row_exact": 0.0, "row_jaccard": 0.0},
                    "row_feedback": ["No usable output row was returned for this input."],
                }
            )

        objective_scores = [dict(t.get("scores", {})) for t in trajectories]
        summary = {
            "eval_idx": self.eval_idx,
            "batch_size": len(batch),
            "avg_score": sum(scores) / max(1, len(scores)),
            "exact": sum(1 for t in trajectories if t.get("scores", {}).get("row_exact") == 1.0),
            "candidate_policy_chars": len(candidate.get("policy", "")),
        }
        (eval_dir / "row-wise-score.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(
            f"row-wise-eval-{self.eval_idx:05d}: n={len(batch)} "
            f"avg={summary['avg_score']:.4f} exact={summary['exact']}/{len(batch)}"
        )

        return EvaluationBatch(
            outputs=result.rows,
            scores=scores,
            trajectories=trajectories if capture_traces else None,
            objective_scores=objective_scores,
            num_metric_calls=len(batch),
        )

    def make_reflective_dataset(self, candidate, eval_batch, components_to_update):
        scores = eval_batch.scores
        trajectories = eval_batch.trajectories or []
        out: dict[str, list[dict[str, Any]]] = {}
        for component in components_to_update:
            rows = []
            for score_value, side_info in zip(scores, trajectories, strict=False):
                row = {}
                for key, value in side_info.items():
                    row["Scores (Higher is Better)" if key == "scores" else key] = value
                row["selected_row_score"] = score_value
                rows.append(row)
            out[component] = rows
        return out


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

    fixed_asset_hashes = {
        name: {"path": str(path), "sha256": _sha256(path)}
        for name, path in {
            "agent_card": agent_card,
            "allowed_topics": args.allowed_topics,
            "seed_policy": args.seed_policy,
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
        candidate: dict[str, str],
        candidate_run: CandidateRun,
    ) -> tuple[float, dict[str, Any]]:
        policy = str(candidate.get("policy", ""))
        report = add_vanilla_asi(
            score(result.output_path),
            policy,
            score_mode=args.score_mode,
            hygiene_penalty_weight=args.hygiene_penalty,
            policy_char_budget=args.policy_char_budget,
        )
        # The benchmark scorer may attach eval/openclaw/asi-pack-v4.md as static
        # side-info. In this runner, static domain context is supplied through
        # GEPA's background channel instead, so avoid duplicating that large pack
        # in every candidate trajectory.
        if report.pop("static_asi_pack", None) is not None:
            report["benchmark_static_asi_path"] = str(ROOT / "eval/openclaw/asi-pack-v4.md")
        if args.static_asi:
            report["static_asi_path"] = str(args.static_asi)
        idx = candidate_run.index or 0
        report["candidate_idx"] = idx
        report["candidate_dir"] = str(candidate_run.path)
        report["result_jsonl"] = str(result.output_path)
        report["batch_summary"] = result.summary
        (candidate_run.path / "policy.md").write_text(policy, encoding="utf-8")
        policy_sha = hashlib.sha256(policy.encode("utf-8")).hexdigest()
        lineage = {
            "candidate_idx": idx,
            "policy_sha256": policy_sha,
            "policy_chars": len(policy),
            **resolve_parent(idx),
            "fixed_assets": fixed_asset_hashes,
            "task_model": args.model,
            "reflection_model": args.reflection_model,
            "score_mode": args.score_mode,
        }
        (candidate_run.path / "lineage.json").write_text(json.dumps(lineage, indent=2), encoding="utf-8")
        seen_policies.append((idx, policy, policy_sha))
        report["lineage"] = {k: lineage[k] for k in ("policy_sha256", "parent_candidate_idx", "reflection_call")}
        log_candidate(idx, candidate_run.path, report)
        s = report["scores"]
        d = report["score_details"]
        print(
            f"candidate-{idx:04d}: f1={s['topic_micro_f1']:.4f} "
            f"p={d['topic_micro_precision']:.4f} r={d['topic_micro_recall']:.4f} "
            f"exact={d['exact_match']:.4f} chars={d['policy_chars']}"
        )
        side_info = dict(report)
        side_info.pop("candidate_dir", None)
        side_info.pop("result_jsonl", None)
        return float(s["gepa_score"]), side_info

    return FastAgentBatchEvaluator(
        env_dir=ENV_DIR,
        agent_card=agent_card,
        agent=agent_name,
        candidate_variables={"policy": "policy"},
        input=input_path,
        template_source=TASK_TEMPLATE,
        schema=None if args.plain_labels else SCHEMA,
        model=args.model,
        parallel=args.parallel,
        scorer=score_candidate,
        run_dir=run_dir,
        backend="process",
    )


def objective_text(*, plain_labels: bool, score_mode: str) -> str:
    output_contract = (
        "plain comma-separated topic-ID output contract"
        if plain_labels
        else "JSON output contract"
    )
    return f"""Improve only the mutable OpenClaw vanilla labeler routing policy.

The fixed AgentCard header, {output_contract}, schema enum, GitHub context renderer,
and allowed-topic taxonomy are not editable.

Primary objective: {
    "maximize pure topic_micro_f1 against the frozen teacher/adjudicated labels"
    if score_mode == "f1"
    else "maximize row-aware GEPA score = 0.50*topic_micro_f1 + 0.20*row_exact_accuracy + 0.30*avg_row_jaccard"
}. Do not optimize for recall-biased F-beta. Use precision, recall, exact match,
row Jaccard, row symdiff, cardinality, topic confusions, row examples, and
prompt-hygiene ASI to understand how to improve reliable row-level reproduction.

Keep the policy vanilla and compact. Prefer short reusable centrality/cardinality rules
over a long topic-by-topic rulebook.

Keep the mutable policy under 12,000 characters; over-budget policies receive a small
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


def background_text(*, allowed_topics: Path, static_asi: Path | None, optimizer_cues: Path | None) -> str:
    sections = [
        f"""The task model sees this fixed taxonomy before the mutable policy:

```md
{allowed_topics.read_text(encoding="utf-8").strip()}
```"""
    ]
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
        "static_asi": run_dir / "static-asi.md" if args.static_asi else None,
        "optimizer_cues": run_dir / "optimizer-cues.md" if args.optimizer_cues else None,
        "boundary_guidance": run_dir / "boundary-guidance.md" if args.boundary_guidance else None,
    }
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
            "output_contract": "comma-separated topic IDs" if args.plain_labels else "structured JSON",
            "score": (
                "topic_micro_f1"
                if args.score_mode == "f1"
                else "0.50*topic_micro_f1+0.20*row_exact_accuracy+0.30*avg_row_jaccard"
            ),
        },
        "models": {
            "task_model": args.model,
            "reflection_model": args.reflection_model,
        },
        "budget": {
            "max_metric_calls": args.max_metric_calls,
            "reflection_minibatch_size": args.reflection_minibatch_size,
            "parallel": args.parallel,
        },
        "inputs": {
            "input": _rel(args.input),
            "input_rows": input_rows,
            "seed_policy": _rel(args.seed_policy),
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
    run_name = args.run_name or time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    run_dir = args.run_root / run_name
    run_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(args.input, run_dir / "input.jsonl")
    active_card = resolve_agent_card(args)
    shutil.copy2(active_card, run_dir / "openclaw-vanilla-labeler.md")
    shutil.copy2(args.seed_policy, run_dir / "seed-policy.md")
    shutil.copy2(args.allowed_topics, run_dir / "allowed-topics.md")
    if args.static_asi:
        shutil.copy2(args.static_asi, run_dir / "static-asi.md")
    if args.optimizer_cues:
        shutil.copy2(args.optimizer_cues, run_dir / "optimizer-cues.md")
    if args.boundary_guidance:
        hints = load_topic_hints_from_guidance(args.boundary_guidance)
        allowed_enum = set(json.loads(SCHEMA.read_text())["properties"]["topics_of_interest"]["items"]["enum"])
        unknown = sorted(set(hints) - allowed_enum)
        if unknown:
            raise SystemExit(
                f"--boundary-guidance contains topics not in the schema enum: {unknown}; "
                "reconcile the frozen spec with the taxonomy before running."
            )
        shutil.copy2(args.boundary_guidance, run_dir / "boundary-guidance.md")
        print(f"boundary guidance: TOPIC_HINTS replaced from {args.boundary_guidance} ({len(hints)} topics)")
    objective = objective_text(plain_labels=args.plain_labels, score_mode=args.score_mode)
    background = background_text(
        allowed_topics=args.allowed_topics,
        static_asi=args.static_asi,
        optimizer_cues=args.optimizer_cues,
    )
    (run_dir / "objective.md").write_text(objective, encoding="utf-8")
    (run_dir / "background.md").write_text(background, encoding="utf-8")
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

            rows = [json.loads(line) for line in (run_dir / "input.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
            if args.max_metric_calls <= len(rows):
                print(
                    f"Warning: row-wise mode counts one metric call per row. "
                    f"--max-metric-calls={args.max_metric_calls} is <= {len(rows)} train rows, "
                    "so the run may stop after the seed/full-val evaluation.",
                    file=sys.stderr,
                )
            adapter = OpenClawRowWiseAdapter(run_dir=run_dir, args=args)
            result = optimize(
                seed_candidate=seed,
                trainset=rows,
                valset=rows,
                adapter=adapter,
                reflection_lm=FastAgentReflectionLM(
                    env_dir=ENV_DIR,
                    model=args.reflection_model,
                    audit_dir=run_dir / "reflection",
                ),
                reflection_prompt_template=_build_reflection_prompt_template(
                    objective=objective,
                    background=background,
                ),
                reflection_minibatch_size=args.reflection_minibatch_size or 3,
                skip_perfect_score=False,
                max_metric_calls=args.max_metric_calls,
                run_dir=str(run_dir),
                cache_evaluation=True,
                use_trackio=trackio_enabled,
                trackio_attach_existing=trackio_enabled,
                tracking_key_prefix="gepa/",
                track_best_outputs=True,
                display_progress_bar=False,
            )
            best = result.best_candidate
            (run_dir / "best-candidate.json").write_text(json.dumps(best, indent=2), encoding="utf-8")
            if isinstance(best, dict) and "policy" in best:
                (run_dir / "best-policy.md").write_text(best["policy"], encoding="utf-8")
            (run_dir / "row-wise-result.json").write_text(
                json.dumps(
                    {
                        "best_idx": result.best_idx,
                        "best_score": result.val_aggregate_scores[result.best_idx],
                        "val_aggregate_scores": result.val_aggregate_scores,
                        "total_metric_calls": result.total_metric_calls,
                        "gepa_mode": args.gepa_mode,
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
                        env_dir=ENV_DIR,
                        model=args.reflection_model,
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
        print(f"Best vanilla F1 policy written under {run_dir}")
        return 0
    finally:
        finish_trackio(trackio_enabled)


if __name__ == "__main__":
    raise SystemExit(main())
