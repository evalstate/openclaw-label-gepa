from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

from openclaw_gepa.evaluator import EvalPaths, build_evaluator
from openclaw_gepa.fast_agent_lm import FastAgentReflectionLM

ROOT = Path(__file__).resolve().parents[2]
ENV_DIR = ROOT / ".fast-agent"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run fast-agent driven GEPA evaluations with Trackio tracking.")
    parser.add_argument("--model", default="passthrough", help="Task model for `fast-agent batch run`.")
    parser.add_argument("--reflection-model", default="$system.default", help="fast-agent model alias for GEPA reflection.")
    parser.add_argument("--max-metric-calls", type=int, default=12, help="GEPA evaluation budget.")
    parser.add_argument("--evaluate-only", action="store_true", help="Evaluate the seed candidate and exit.")
    parser.add_argument("--fast-agent-bin", default="fast-agent")
    parser.add_argument("--parallel", type=int, default=4, help="fast-agent batch parallelism.")
    parser.add_argument("--run-name", default=None)
    parser.add_argument("--project", default="openclaw-gepa", help="Trackio project name.")
    parser.add_argument("--group", default=None, help="Optional Trackio group.")
    parser.add_argument("--trackio-space-id", default=os.environ.get("TRACKIO_SPACE_ID"))
    parser.add_argument("--trackio-server-url", default=os.environ.get("TRACKIO_SERVER_URL"))
    parser.add_argument("--no-trackio", action="store_true", help="Disable Trackio for this run.")
    parser.add_argument("--input", type=Path, default=ROOT / "eval" / "input.jsonl")
    parser.add_argument("--task-template", type=Path, default=ROOT / "eval" / "task-template.md")
    parser.add_argument("--smoke-template", type=Path, default=ROOT / "eval" / "smoke-template.md")
    parser.add_argument("--schema", type=Path, default=ROOT / "eval" / "output.schema.json")
    parser.add_argument("--seed", type=Path, default=ROOT / "seed" / "instructions.md")
    return parser.parse_args()


def init_trackio(args: argparse.Namespace, run_name: str, run_dir: Path) -> None:
    if args.no_trackio:
        return
    import trackio

    init_kwargs: dict[str, Any] = {
        "project": args.project,
        "name": run_name,
        "group": args.group,
        "config": {
            "task_model": args.model,
            "reflection_model": args.reflection_model,
            "max_metric_calls": args.max_metric_calls,
            "input": str(args.input),
            "schema": str(args.schema),
            "run_dir": str(run_dir),
        },
        "embed": False,
        "auto_log_gpu": False,
    }
    if args.trackio_space_id:
        init_kwargs["space_id"] = args.trackio_space_id
    if args.trackio_server_url:
        init_kwargs["server_url"] = args.trackio_server_url
    trackio.init(**init_kwargs)


def finish_trackio(enabled: bool) -> None:
    if not enabled:
        return
    try:
        import trackio

        trackio.finish()
    except Exception:
        pass


def write_best(run_dir: Path, result: Any) -> None:
    best = result.best_candidate
    (run_dir / "best-candidate.json").write_text(json.dumps(best, indent=2), encoding="utf-8")
    if isinstance(best, dict) and "instructions" in best:
        (run_dir / "best-instructions.md").write_text(best["instructions"], encoding="utf-8")


def main() -> int:
    args = parse_args()
    run_name = args.run_name or time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    run_dir = ROOT / "runs" / run_name
    run_dir.mkdir(parents=True, exist_ok=True)

    paths = EvalPaths(
        root=ROOT,
        env_dir=ENV_DIR,
        input_path=args.input,
        task_template=args.task_template,
        smoke_template=args.smoke_template,
        schema_path=args.schema,
    )
    seed = {"instructions": args.seed.read_text(encoding="utf-8")}
    evaluator = build_evaluator(
        run_dir=run_dir,
        paths=paths,
        model=args.model,
        fast_agent_bin=args.fast_agent_bin,
        parallel=args.parallel,
    )

    trackio_enabled = not args.no_trackio
    try:
        init_trackio(args, run_name, run_dir)

        if args.evaluate_only:
            score, side_info = evaluator(seed)
            payload = {"score": score, "run_dir": str(run_dir), **side_info}
            (run_dir / "evaluate-only.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
            print(json.dumps(payload, indent=2))
            return 0

        if args.model == "passthrough":
            print("Use --evaluate-only for passthrough smoke tests, or pass --model with a real LLM.", file=sys.stderr)
            return 2

        try:
            from gepa.optimize_anything import (  # type: ignore[import-not-found]
                EngineConfig,
                GEPAConfig,
                ReflectionConfig,
                TrackingConfig,
                optimize_anything,
            )
        except ImportError:
            print("GEPA is not installed. Run: uv sync", file=sys.stderr)
            return 2

        reflection_lm = FastAgentReflectionLM(
            model=args.reflection_model,
            run_dir=run_dir / "reflection",
            env_dir=ENV_DIR,
            fast_agent_bin=args.fast_agent_bin,
        )
        result = optimize_anything(
            seed_candidate=seed,
            evaluator=evaluator,
            objective=(
                "Improve the support-request classification instructions. Preserve the JSON schema, "
                "make category boundaries explicit, and use ASI failure evidence to fix recurring mistakes."
            ),
            config=GEPAConfig(
                engine=EngineConfig(max_metric_calls=args.max_metric_calls, cache_evaluation=True),
                reflection=ReflectionConfig(reflection_lm=reflection_lm),
                tracking=TrackingConfig(
                    use_trackio=trackio_enabled,
                    trackio_attach_existing=trackio_enabled,
                    trackio_step_metric="gepa/iteration",
                    key_prefix="gepa/",
                ),
            ),
        )
        write_best(run_dir, result)
        print(f"Best candidate written under {run_dir}")
        print(f"Trackio dashboard: trackio show --project {args.project!r}")
        return 0
    finally:
        finish_trackio(trackio_enabled)


if __name__ == "__main__":
    raise SystemExit(main())
