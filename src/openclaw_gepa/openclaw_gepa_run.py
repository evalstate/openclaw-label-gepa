from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from openclaw_gepa.fast_agent_lm import FastAgentReflectionLM
from openclaw_gepa.openclaw_benchmark import (
    ENV_DIR,
    EVAL,
    REF,
    ROOT,
    SCHEMA,
    TASK_TEMPLATE,
    prepare_dataset,
    refresh_github_context,
    score,
)

RUN_ROOT = ROOT / "runs" / "openclaw-gepa"
SEED_POLICY = ROOT / "seed" / "openclaw" / "policy.md"
ALLOWED_TOPICS = ROOT / "eval" / "openclaw" / "allowed-topics.md"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run GEPA over the OpenClaw routing policy prompt.")
    p.add_argument("--model", default="gpt-oss", help="Task model for fast-agent batch evaluation.")
    p.add_argument("--reflection-model", default="codexresponses.gpt-5.5?reasoning=high", help="fast-agent model for GEPA reflection.")
    p.add_argument("--sample", type=int, default=80)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--input", type=Path, default=None, help="Prepared benchmark JSONL to use instead of sampling.")
    p.add_argument("--seed-policy", type=Path, default=SEED_POLICY, help="Initial policy file for GEPA.")
    p.add_argument("--plain-labels", action="store_true", help="Use comma-separated label output instead of structured JSON.")
    p.add_argument("--max-metric-calls", type=int, default=8)
    p.add_argument("--parallel", type=int, default=4)
    p.add_argument("--fast-agent-bin", default="fast-agent")
    p.add_argument("--run-name", default=None)
    p.add_argument("--evaluate-only", action="store_true")
    p.add_argument("--policy-char-budget", type=int, default=12_326, help="No GEPA score penalty up to this many policy chars.")
    p.add_argument(
        "--policy-over-budget-penalty-per-10k",
        type=float,
        default=0.02,
        help="Soft GEPA score penalty per 10K policy chars over --policy-char-budget.",
    )
    p.add_argument("--max-policy-length-penalty", type=float, default=0.12, help="Cap for the soft policy length penalty.")
    p.add_argument("--no-trackio", action="store_true")
    p.add_argument("--project", default="openclaw-gepa")
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
        "group": "openclaw-gepa",
        "embed": False,
        "auto_log_gpu": False,
        "config": {
            "task_model": args.model,
            "reflection_model": args.reflection_model,
            "sample": args.sample,
            "seed": args.seed,
            "input": str(args.input) if args.input else None,
            "seed_policy": str(args.seed_policy),
            "plain_labels": args.plain_labels,
            "max_metric_calls": args.max_metric_calls,
            "policy_char_budget": args.policy_char_budget,
            "policy_over_budget_penalty_per_10k": args.policy_over_budget_penalty_per_10k,
            "max_policy_length_penalty": args.max_policy_length_penalty,
            "run_dir": str(run_dir),
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


def log_trackio_candidate(candidate_idx: int, candidate_dir: Path, report: dict[str, Any]) -> None:
    try:
        import trackio

        # GEPA's internal program candidates are zero-based: seed program = 0.
        # Our local candidate directories are one-based (candidate-0001), so
        # use program_idx for Trackio alignment to avoid apparent n-1 plots.
        program_idx = candidate_idx - 1
        scores = report.get("scores", {})
        details = report.get("score_details", {})
        metric_keys = [
            "gepa_score",
            "topic_micro_f1",
            "topic_micro_precision",
            "topic_micro_recall",
            "exact_match",
            "valid_json",
            "cardinality_closeness",
            "policy_length_compliance",
        ]
        detail_keys = [
            "avg_expected_topics",
            "avg_predicted_topics",
            "policy_chars",
            "classifier_card_chars",
            "policy_length_over_budget",
            "policy_length_penalty",
        ]
        metrics = {
            f"candidate/{k}": scores[k]
            for k in metric_keys
            if isinstance(scores.get(k), int | float)
        }
        metrics.update({
            f"candidate/detail/{k}": details[k]
            for k in detail_keys
            if isinstance(details.get(k), int | float)
        })
        metrics["candidate/local_idx"] = candidate_idx
        metrics["candidate/program_idx"] = program_idx
        metrics["gepa/iteration"] = program_idx
        # Match GEPA's Trackio custom-step convention: inject `gepa/iteration`
        # as a metric rather than passing step=, so the host/global step stream
        # does not drift relative to GEPA's own logs.
        trackio.log(metrics)
        patterns = report.get("topic_error_patterns", [])[:8]
        if patterns:
            trackio.log(
                {
                    "gepa/iteration": program_idx,
                    "asi/topic_error_patterns": trackio.Table(
                        columns=["candidate_idx", "topic", "problem", "fp", "fn", "precision", "recall", "f1", "action"],
                        data=[
                            [
                                program_idx,
                                p.get("topic"),
                                p.get("problem"),
                                p.get("false_positives"),
                                p.get("false_negatives"),
                                p.get("precision"),
                                p.get("recall"),
                                p.get("f1"),
                                str(p.get("action") or "")[:300],
                            ]
                            for p in patterns
                        ],
                    )
                }
            )
    except Exception:
        return


def next_candidate_dir(run_dir: Path) -> tuple[int, Path]:
    i = 1
    while (run_dir / f"candidate-{i:04d}").exists():
        i += 1
    path = run_dir / f"candidate-{i:04d}"
    path.mkdir(parents=True, exist_ok=True)
    return i, path


def render_candidate_card(policy: str, path: Path) -> None:
    allowed = ALLOWED_TOPICS.read_text(encoding="utf-8")
    body = f"""---
type: agent
name: openclaw_classifier
model: "$system.default"
skills: []
use_history: false
---

# OpenClaw Routing Classifier

Classify one OpenClaw GitHub issue or pull request according to the routing policy below.
Return only the final structured JSON required by the schema. No prose, markdown, analysis, or extra fields.

Required output shape:

```json
{{"topics_of_interest":[],"description":"One concise evidence-backed sentence.","caveats":[]}}
```

{allowed}

{policy.strip()}
"""
    path.write_text(body, encoding="utf-8")


def render_candidate_plain_label_card(policy: str, path: Path) -> None:
    allowed = ALLOWED_TOPICS.read_text(encoding="utf-8")
    topics = json.loads(SCHEMA.read_text(encoding="utf-8"))["properties"]["topics_of_interest"]["items"]["enum"]
    body = f"""---
type: agent
name: openclaw_classifier
model: "$system.default"
skills: []
use_history: false
---

# OpenClaw Routing Classifier

Classify one OpenClaw GitHub issue or pull request according to the routing policy below.
Return only comma-separated topic IDs. No JSON, markdown, prose, explanation, confidence, or extra fields.

Example output:
reliability,browser_automation,exec_tools

Allowed topic IDs:
{", ".join(topics)}

If no listed topic applies, return exactly:
none

{allowed}

{policy.strip()}

Reminder: ignore any policy wording about structured JSON output; for this local-model run, comma-separated topic IDs are the required output format.
"""
    path.write_text(body, encoding="utf-8")


def render_readonly_reflection_context(*, plain_labels: bool) -> str:
    allowed = ALLOWED_TOPICS.read_text(encoding="utf-8").strip()
    task_template = TASK_TEMPLATE.read_text(encoding="utf-8").strip()
    schema = SCHEMA.read_text(encoding="utf-8").strip()
    if plain_labels:
        topics = json.loads(schema)["properties"]["topics_of_interest"]["items"]["enum"]
        output_contract = f"""Return only comma-separated topic IDs. No JSON, markdown, prose, explanation, confidence, or extra fields.

Example output:
reliability,browser_automation,exec_tools

Allowed topic IDs:
{", ".join(topics)}

If no listed topic applies, return exactly:
none"""
    else:
        output_contract = f"""Return only the final structured JSON required by this schema. No prose, markdown, analysis, or extra fields.

```json
{schema}
```"""
    return f"""## Read-only task prompt context

The reflection LM may use this to understand what the task model sees, but must not edit it.
Only the policy component is mutable. Task framing, routing intent, evidence hierarchy, and cardinality
calibration belong in the mutable policy. The fixed context below is only the output/schema/topic/template contract.

### Fixed classifier header/output contract

Classify one OpenClaw GitHub issue or pull request according to the routing policy.

{output_contract}

### Fixed allowed-topic definitions

{allowed}

### Fixed per-row user template

```md
{task_template}
```

### GitHub context shape

The `github_context` template variable is a pre-rendered Markdown block with:

- GitHub item metadata: repository, type, number, URL, title, state, author, labels, changed-file count/files, context caveats.
- `Body` fenced as markdown, truncated at the benchmark body budget.
- `Comments/context` fenced as markdown when available, truncated at the benchmark comments budget.
- `Diff/context` fenced as diff when available, selected/truncated by benchmark keywords and diff budget.
"""


def build_reflection_objective(*, task_model: str, plain_labels: bool, policy_char_budget: int) -> str:
    behavior = (
        "Preserve comma-separated topic-ID-only behavior; do not ask for JSON or prose."
        if plain_labels
        else "Preserve concise JSON-only behavior."
    )
    return (
        "Improve only the OpenClaw routing decision policy, including task framing, routing intent, evidence "
        "hierarchy, cardinality calibration, and topic boundary rules. The fixed header, allowed topics, output "
        "format, output schema, GitHub context renderer, and GitHub context template are not editable. Optimize "
        f"the GEPA score on {task_model} outputs: raw topic_micro_f1 minus any soft policy-length penalty. "
        "Use ASI about false positives, false negatives, topic confusions, cardinality, and policy length. "
        f"{behavior}\n\n"
        "Generalization constraints: prefer concise reusable boundary rules over row-specific exceptions. "
        "Never include row-identifying information in the policy: no row IDs, issue/PR numbers, exact issue "
        "titles, URLs, or copied example text. Do not add memorized issue/title/keyword tables. Keep the policy "
        f"compact, ideally within the no-penalty budget of {policy_char_budget} chars, unless a longer rule is clearly reusable across many future rows. "
        "Balance precision with recall: "
        "when ASI shows under-labeling or low predicted cardinality, loosen gates for central co-label families "
        "instead of adding only false-positive suppressions.\n\n"
        f"{render_readonly_reflection_context(plain_labels=plain_labels)}"
    )


def run_candidate_batch(
    *,
    candidate: dict[str, str],
    candidate_dir: Path,
    input_path: Path,
    model: str,
    parallel: int,
    fast_agent_bin: str,
    plain_labels: bool = False,
) -> Path:
    policy = candidate["policy"]
    (candidate_dir / "policy.md").write_text(policy, encoding="utf-8")
    card = candidate_dir / "openclaw-classifier.md"
    if plain_labels:
        render_candidate_plain_label_card(policy, card)
    else:
        render_candidate_card(policy, card)
    output = candidate_dir / "results.jsonl"
    summary = candidate_dir / "batch-summary.json"
    telemetry = candidate_dir / "telemetry.jsonl"
    cmd = [
        fast_agent_bin,
        "--no-update-check",
        "--env",
        str(ENV_DIR),
        "batch",
        "run",
        "--agent-card",
        str(card),
        "--agent",
        "openclaw_classifier",
        "--input",
        str(input_path),
        "--output",
        str(output),
        "--template",
        str(TASK_TEMPLATE),
    ]
    if not plain_labels:
        cmd.extend(["--json-schema", str(SCHEMA)])
    cmd.extend([
        "--model",
        model,
        "--id-field",
        "id",
        "--include-input",
        "--summary-output",
        str(summary),
        "--telemetry-output",
        str(telemetry),
        "--parallel",
        str(parallel),
        "--overwrite",
        "--no-final-summary",
    ])
    (candidate_dir / "command.json").write_text(json.dumps(cmd, indent=2), encoding="utf-8")
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)
    (candidate_dir / "stdout.txt").write_text(proc.stdout, encoding="utf-8")
    (candidate_dir / "stderr.txt").write_text(proc.stderr, encoding="utf-8")
    if proc.returncode:
        raise RuntimeError(f"fast-agent batch failed with exit {proc.returncode}\n{proc.stderr[-4000:]}")
    return output


def build_evaluator(run_dir: Path, input_path: Path, args: argparse.Namespace):
    def evaluate(candidate: dict[str, str]) -> tuple[float, dict[str, Any]]:
        idx, candidate_dir = next_candidate_dir(run_dir)
        (candidate_dir / "candidate.json").write_text(json.dumps(candidate, indent=2), encoding="utf-8")
        output = run_candidate_batch(
            candidate=candidate,
            candidate_dir=candidate_dir,
            input_path=input_path,
            model=args.model,
            parallel=args.parallel,
            fast_agent_bin=args.fast_agent_bin,
            plain_labels=args.plain_labels,
        )
        report = score(output)
        policy_chars = len(candidate.get("policy", ""))
        classifier_card_chars = len((candidate_dir / "openclaw-classifier.md").read_text(encoding="utf-8"))
        over_budget = max(0, policy_chars - args.policy_char_budget)
        length_penalty = min(
            args.max_policy_length_penalty,
            (over_budget / 10_000) * args.policy_over_budget_penalty_per_10k,
        )
        raw_f1 = float(report["scores"]["topic_micro_f1"])
        gepa_score = max(0.0, raw_f1 - length_penalty)
        report["scores"]["gepa_score"] = gepa_score
        report["scores"]["policy_length_compliance"] = 1.0 - (length_penalty / max(args.max_policy_length_penalty, 1e-9))
        report["score_details"]["policy_chars"] = policy_chars
        report["score_details"]["classifier_card_chars"] = classifier_card_chars
        report["score_details"]["policy_char_budget"] = args.policy_char_budget
        report["score_details"]["policy_length_over_budget"] = over_budget
        report["score_details"]["policy_length_penalty"] = length_penalty
        report["candidate_idx"] = idx
        report["candidate_dir"] = str(candidate_dir)
        report["result_jsonl"] = str(output)
        (candidate_dir / "score.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        log_trackio_candidate(idx, candidate_dir, report)
        print(
            f"candidate-{idx:04d}: gepa={gepa_score:.4f} "
            f"f1={raw_f1:.4f} precision={report['scores']['topic_micro_precision']:.4f} "
            f"recall={report['scores']['topic_micro_recall']:.4f} chars={policy_chars} "
            f"length_penalty={length_penalty:.4f}"
        )
        side_info = dict(report)
        side_info.pop("candidate_dir", None)
        side_info.pop("result_jsonl", None)
        return gepa_score, side_info

    return evaluate


def main() -> int:
    args = parse_args()
    run_name = args.run_name or time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    run_dir = RUN_ROOT / run_name
    run_dir.mkdir(parents=True, exist_ok=True)
    input_path = run_dir / "input.jsonl"
    if args.input is None:
        prepare_dataset(REF / "seed.jsonl", input_path, limit=args.sample, sample=args.sample, seed=args.seed)
    else:
        refresh_github_context(args.input, input_path, REF / "seed.jsonl")
    shutil.copy2(SCHEMA, run_dir / "output.schema.json")
    shutil.copy2(args.seed_policy, run_dir / "seed-policy.md")

    trackio_enabled = init_trackio(args, run_name, run_dir)
    seed_candidate = {"policy": args.seed_policy.read_text(encoding="utf-8")}
    evaluator = build_evaluator(run_dir, input_path, args)
    try:
        if args.evaluate_only:
            score_value, report = evaluator(seed_candidate)
            payload = {"score": score_value, "run_dir": str(run_dir), **report}
            (run_dir / "evaluate-only.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
            print(json.dumps(payload, indent=2))
            return 0

        try:
            from gepa.optimize_anything import EngineConfig, GEPAConfig, ReflectionConfig, TrackingConfig, optimize_anything
        except ImportError:
            print("GEPA is not importable. Run with PYTHONPATH=src:/home/shaun/temp/gepa/src or uv sync.", file=sys.stderr)
            return 2

        reflection_lm = FastAgentReflectionLM(
            model=args.reflection_model,
            run_dir=run_dir / "reflection",
            env_dir=ENV_DIR,
            fast_agent_bin=args.fast_agent_bin,
        )
        reflection_objective = build_reflection_objective(
            task_model=args.model,
            plain_labels=args.plain_labels,
            policy_char_budget=args.policy_char_budget,
        )
        (run_dir / "reflection-objective.md").write_text(reflection_objective, encoding="utf-8")
        result = optimize_anything(
            seed_candidate=seed_candidate,
            evaluator=evaluator,
            objective=reflection_objective,
            config=GEPAConfig(
                engine=EngineConfig(
                    max_metric_calls=args.max_metric_calls,
                    cache_evaluation=True,
                    frontier_type="hybrid",
                    candidate_selection_strategy="pareto",
                ),
                reflection=ReflectionConfig(reflection_lm=reflection_lm),
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
        print(f"Best policy written under {run_dir}")
        return 0
    finally:
        finish_trackio(trackio_enabled)


if __name__ == "__main__":
    raise SystemExit(main())
