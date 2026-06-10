#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Any

from fast_agent.batch import BatchRunResult
from fast_agent.eval import CandidateRun
from fast_agent.integrations.gepa import FastAgentBatchEvaluator, FastAgentReflectionLM
from openclaw_gepa.openclaw_benchmark import ENV_DIR, ROOT, SCHEMA, TASK_TEMPLATE, score


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
    p.add_argument("--agent-card", type=Path, default=CARD)
    p.add_argument("--allowed-topics", type=Path, default=ALLOWED_TOPICS)
    p.add_argument("--plain-labels", action="store_true", help="Ask for comma-separated topic IDs instead of structured JSON.")
    p.add_argument("--run-name", default=None)
    p.add_argument("--parallel", type=int, default=4)
    p.add_argument("--max-metric-calls", type=int, default=12)
    p.add_argument(
        "--score-mode",
        choices=["f1", "row-aware"],
        default="f1",
        help="GEPA scoring mode. row-aware uses 0.50*micro-F1 + 0.20*row-exact + 0.30*row-Jaccard and exposes row metrics as frontier scores.",
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
            "max_metric_calls": args.max_metric_calls,
            "score_mode": args.score_mode,
            "run_dir": str(run_dir),
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
    if len(re.findall(r"(?m)^- `?[a-z][a-z0-9_]+`?:", policy)) > 25:
        findings.append("Policy has a large topic-by-topic table; prefer concise reusable rules.")
    return {
        "ok": not findings,
        "findings": findings,
        "policy_chars": len(policy),
    }


def add_vanilla_asi(report: dict[str, Any], policy: str, *, score_mode: str = "f1") -> dict[str, Any]:
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

    if score_mode == "row-aware":
        gepa_score = 0.50 * f1 + 0.20 * row_exact + 0.30 * avg_row_jaccard
        # Frontier-safe: all values in scores are higher-is-better.
        report["scores"] = {
            "gepa_score": gepa_score,
            "topic_micro_f1": f1,
            "row_exact_accuracy": row_exact,
            "avg_row_jaccard": avg_row_jaccard,
            "row_symdiff_score": row_symdiff_score,
        }
    else:
        gepa_score = f1
        # Historical F1-only mode; row metrics remain diagnostics.
        report["scores"] = {
            "gepa_score": gepa_score,
            "topic_micro_f1": f1,
        }
    details.update(
        {
            "topic_micro_precision": precision,
            "topic_micro_recall": recall,
            "exact_match": exact,
            "row_exact_accuracy": row_exact,
            "avg_row_jaccard": avg_row_jaccard,
            "avg_row_symdiff": avg_row_symdiff,
            "row_symdiff_score": row_symdiff_score,
            "gepa_score": gepa_score,
            "score_mode": score_mode,
            "valid_json": valid_json,
            "cardinality_closeness": card,
            "avg_topic_count_delta": avg_predicted - avg_expected,
            "policy_chars": hygiene["policy_chars"],
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
            "valid_json": valid_json,
            "cardinality_closeness": card,
            "avg_expected_topics": avg_expected,
            "avg_predicted_topics": avg_predicted,
            "false_positives": fp,
            "false_negatives": fn,
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


def build_evaluator(run_dir: Path, input_path: Path, args: argparse.Namespace):
    plain_labels = args.plain_labels
    agent_card = PLAIN_CARD if args.plain_labels and args.agent_card == CARD else args.agent_card
    agent_name = "openclaw_vanilla_labeler_plain" if plain_labels else "openclaw_vanilla_labeler"

    def score_candidate(
        result: BatchRunResult,
        candidate: dict[str, str],
        candidate_run: CandidateRun,
    ) -> tuple[float, dict[str, Any]]:
        policy = str(candidate.get("policy", ""))
        report = add_vanilla_asi(score(result.output_path), policy, score_mode=args.score_mode)
        if args.static_asi:
            report["static_asi_pack"] = args.static_asi.read_text(encoding="utf-8").strip()
        idx = candidate_run.index or 0
        report["candidate_idx"] = idx
        report["candidate_dir"] = str(candidate_run.path)
        report["result_jsonl"] = str(result.output_path)
        report["batch_summary"] = result.summary
        (candidate_run.path / "policy.md").write_text(policy, encoding="utf-8")
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


def objective_text(*, plain_labels: bool, allowed_topics: Path, score_mode: str) -> str:
    output_contract = (
        "plain comma-separated topic-ID output contract"
        if plain_labels
        else "JSON output contract"
    )
    return f"""Improve only the mutable OpenClaw vanilla labeler routing policy.

The fixed AgentCard header, {output_contract}, schema enum, GitHub context renderer,
and allowed-topic taxonomy in `{allowed_topics}` are not editable.

Primary objective: {
    "maximize pure topic_micro_f1 against the frozen teacher/adjudicated labels"
    if score_mode == "f1"
    else "maximize row-aware GEPA score = 0.50*topic_micro_f1 + 0.20*row_exact_accuracy + 0.30*avg_row_jaccard"
}. Do not optimize for recall-biased F-beta. Use precision, recall, exact match,
row Jaccard, row symdiff, cardinality, topic confusions, row examples, and
prompt-hygiene ASI to understand how to improve reliable row-level reproduction.

Keep the policy vanilla and compact. Prefer short reusable centrality/cardinality rules
over a long topic-by-topic rulebook.

{"Preserve comma-separated topic-ID-only behavior; do not ask for JSON, prose, bullets, or explanations." if plain_labels else "Preserve concise JSON-only behavior."}

Do not copy, rewrite, reorder, rename, delete, extend, or replace the fixed allowed-topic
list, topic definitions, or cue/keyword list. Reference exact existing topic IDs only
when a concise reusable boundary rule needs them.

Do not include row IDs, issue numbers, exact titles, URLs, or copied examples. Do not add
memorized issue/title/keyword tables.

The task model sees this fixed taxonomy before the mutable policy:

```md
{allowed_topics.read_text(encoding="utf-8").strip()}
```
"""


def main() -> int:
    args = parse_args()
    run_name = args.run_name or time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    run_dir = RUN_ROOT / run_name
    run_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(args.input, run_dir / "input.jsonl")
    active_card = PLAIN_CARD if args.plain_labels and args.agent_card == CARD else args.agent_card
    shutil.copy2(active_card, run_dir / "openclaw-vanilla-labeler.md")
    shutil.copy2(args.seed_policy, run_dir / "seed-policy.md")
    shutil.copy2(args.allowed_topics, run_dir / "allowed-topics.md")
    if args.static_asi:
        shutil.copy2(args.static_asi, run_dir / "static-asi.md")
    objective = objective_text(plain_labels=args.plain_labels, allowed_topics=args.allowed_topics, score_mode=args.score_mode)
    (run_dir / "objective.md").write_text(objective, encoding="utf-8")
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

        result = optimize_anything(
            seed_candidate=seed,
            evaluator=evaluator,
            objective=objective,
            config=GEPAConfig(
                engine=EngineConfig(max_metric_calls=args.max_metric_calls, cache_evaluation=True),
                reflection=ReflectionConfig(
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
