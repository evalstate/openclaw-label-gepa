from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shlex
import shutil
import subprocess
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from openclaw_label_gepa.benchmark import score_output_file
from openclaw_label_gepa.regimes import load_regime
from openclaw_label_gepa.runplan import build_benchmark_plan, build_run_plan

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

DEFAULT_REGIME = Path("regimes/v7i-guarded-generator-mutate-all/regime.yaml")
FILE_PLACEHOLDER_RE = re.compile(r"\{\{file:([^}]+)\}\}")


@dataclass(frozen=True)
class DoctorReport:
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


@dataclass(frozen=True)
class AuditCheck:
    name: str
    ok: bool
    detail: str


@dataclass(frozen=True)
class AuditReport:
    checks: list[AuditCheck]

    @property
    def ok(self) -> bool:
        return all(check.ok for check in self.checks)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect or run an OpenClaw label GEPA regime.")
    parser.add_argument("regime", nargs="?", type=Path, default=DEFAULT_REGIME)
    parser.add_argument(
        "--list-regimes",
        action="store_true",
        help="List available regimes under ./regimes and their basic run settings.",
    )
    parser.add_argument(
        "--regime-info",
        action="store_true",
        help="Print detailed information for the selected regime.",
    )
    parser.add_argument("--summary", action="store_true", help="Print regime/data summary only.")
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate regime paths and command plans.",
    )
    parser.add_argument(
        "--doctor",
        action="store_true",
        help="Check environment, local dependencies, imports, and the active regime.",
    )
    parser.add_argument(
        "--audit",
        action="store_true",
        help="Run the repo usability audit: regimes, paths, preflights, and Trackio wiring.",
    )
    parser.add_argument("--score-output", type=Path, default=None, help="Score an output JSONL.")
    parser.add_argument("--split", choices=["train", "benchmark"], default="train")
    parser.add_argument("--report-output", type=Path, default=None)
    parser.add_argument("--plan-gepa", action="store_true", help="Print the GEPA run plan.")
    parser.add_argument(
        "--plan-benchmark",
        action="store_true",
        help="Print benchmark replay command(s) for the regime benchmark split.",
    )
    parser.add_argument(
        "--benchmark-run",
        default="base",
        help="'base', a policy markdown file, or a GEPA run/candidate directory.",
    )
    parser.add_argument(
        "--repeat",
        type=int,
        default=1,
        help="Number of benchmark replay commands to emit.",
    )
    parser.add_argument("--model", default=None, help="Override task model for run plans.")
    parser.add_argument("--reflection-model", default=None, help="Override reflection model.")
    parser.add_argument(
        "--variant",
        choices=["structured", "plain"],
        default=None,
        help="Override the regime default output variant.",
    )
    parser.add_argument("--run-index", type=int, default=1)
    parser.add_argument(
        "--max-metric-calls",
        type=int,
        default=None,
        help="Override run_defaults.max_metric_calls for a GEPA plan.",
    )
    parser.add_argument(
        "--shell",
        action="store_true",
        help="Print shell command(s) only for run plans.",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help=(
            "Execute the selected GEPA, benchmark, or Trackio command directly. "
            "Use --runner-preflight with --run for a no-model-call runner preflight."
        ),
    )
    parser.add_argument(
        "--runner-preflight",
        action="store_true",
        help="Append --preflight-only to generated runner command(s).",
    )
    parser.add_argument(
        "--trackio-command",
        action="store_true",
        help="Print the Trackio dashboard command for the regime.",
    )
    return parser.parse_args(argv)


def regime_summary(regime: Any) -> dict[str, str | int | None]:
    train = regime.load_train()
    return {
        "name": regime.name,
        "metric": regime.metric,
        "labels": len(regime.label_order),
        "train_rows": len(train.rows),
        "base_prompt": str(regime.base_prompt_path),
        "schema": str(regime.schema_path),
        "train_split": str(regime.train_path),
        "benchmark_split": str(regime.benchmark_path) if regime.benchmark_path else None,
    }


def _jsonl_row_count(path: Path | None) -> int | None:
    if path is None:
        return None
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def discover_regimes(project_root: Path) -> list[Path]:
    return sorted((project_root / "regimes").glob("*/regime.yaml"))


def regime_info(regime: Any) -> dict[str, object]:
    defaults = regime.mapping("run_defaults")
    trackio = regime.mapping("trackio")
    models = regime.raw.get("models")
    supported_models = models.get("supported", []) if isinstance(models, dict) else models
    return {
        "name": regime.name,
        "description": regime.raw.get("description"),
        "path": str(regime.root / "regime.yaml"),
        "default_variant": regime.raw.get("default_variant", "structured"),
        "score_mode": regime.raw.get("score_mode", regime.metric),
        "train_rows": _jsonl_row_count(regime.train_path),
        "feedback_rows": _jsonl_row_count(regime.split_path("feedback")),
        "pareto_rows": _jsonl_row_count(regime.split_path("pareto")),
        "benchmark_rows": _jsonl_row_count(regime.benchmark_path),
        "trackio": {
            "project": trackio.get("project"),
            "group": trackio.get("group"),
            "local_dir": trackio.get("local_dir"),
            "step_metric": trackio.get("step_metric"),
        },
        "run_defaults": {
            "run_root": defaults.get("run_root"),
            "max_metric_calls": defaults.get("max_metric_calls"),
            "parallel": defaults.get("parallel"),
            "gepa_mode": defaults.get("gepa_mode"),
            "feedback_profile": defaults.get("feedback_profile"),
        },
        "models": supported_models,
    }


def print_regime_list(project_root: Path) -> int:
    rows = []
    for path in discover_regimes(project_root):
        try:
            regime = load_regime(path)
            rows.append(regime_info(regime))
        except (OSError, TypeError, ValueError, KeyError) as exc:
            rows.append({"name": path.parent.name, "path": str(path), "error": str(exc)})
    print(json.dumps(rows, indent=2))
    return 0


def shell_line(plan: Any, *, extra_args: tuple[str, ...] = ()) -> str:
    command = " ".join(shlex.quote(part) for part in [*plan.command, *extra_args])
    return (
        f"cd {shlex.quote(str(plan.project_root))} && "
        f"TRACKIO_DIR={shlex.quote(str(plan.trackio_dir.resolve()))} {command}"
    )


def trackio_shell_line(regime: Any) -> str:
    trackio = regime.mapping("trackio")
    project_root = regime.root.parents[1].resolve()
    trackio_dir = project_root / str(trackio.get("local_dir", f".trackio/{regime.name}"))
    project = str(trackio.get("project", f"{regime.name}-gepa"))
    return (
        f"cd {shlex.quote(str(project_root))} && "
        "BROWSER=/bin/true "
        f"TRACKIO_DIR={shlex.quote(str(trackio_dir.resolve()))} "
        f"uv run trackio show --project {shlex.quote(project)}"
    )


def trackio_command(regime: Any) -> tuple[Path, Path, list[str]]:
    trackio = regime.mapping("trackio")
    project_root = regime.root.parents[1].resolve()
    trackio_dir = project_root / str(trackio.get("local_dir", f".trackio/{regime.name}"))
    project = str(trackio.get("project", f"{regime.name}-gepa"))
    return (
        project_root,
        trackio_dir.resolve(),
        ["uv", "run", "trackio", "show", "--project", project],
    )


def project_root_for_regime(regime: Any) -> Path:
    return regime.root.parents[1].resolve()


def plan_payload(plan: Any, *, extra_args: tuple[str, ...] = ()) -> dict[str, Any]:
    command = [*plan.command, *extra_args]
    payload = {
        "run_name": plan.run_name,
        "run_root": str(plan.run_root),
        "project_root": str(plan.project_root),
        "trackio": {
            "project": plan.trackio_project,
            "group": plan.trackio_group,
            "dir": str(plan.trackio_dir),
        },
        "command": command,
        "shell": shell_line(plan, extra_args=extra_args),
    }
    if hasattr(plan, "candidate"):
        payload["candidate"] = plan.candidate
    return payload


def _run_command(
    command: list[str],
    *,
    project_root: Path,
    trackio_dir: Path,
    extra_env: Mapping[str, str] | None = None,
) -> int:
    env = os.environ.copy()
    env["TRACKIO_DIR"] = str(trackio_dir.resolve())
    if extra_env:
        env.update(extra_env)
    print(f"cwd={project_root}")
    print(f"TRACKIO_DIR={env['TRACKIO_DIR']}")
    print("command=" + " ".join(shlex.quote(part) for part in command))
    try:
        completed = subprocess.run(command, cwd=project_root, env=env, check=False)  # noqa: S603
    except KeyboardInterrupt:
        print("interrupted")
        return 130
    return completed.returncode


def _capture_command(
    command: list[str],
    *,
    project_root: Path,
    trackio_dir: Path,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["TRACKIO_DIR"] = str(trackio_dir.resolve())
    return subprocess.run(  # noqa: S603
        command,
        cwd=project_root,
        env=env,
        check=False,
        text=True,
        capture_output=True,
    )


def _required_regime_paths(regime: Any) -> dict[str, Path | None]:
    return {
        "label_order": regime.label_order_path,
        "base_prompt": regime.base_prompt_path,
        "schema": regime.schema_path,
        "train_split": regime.train_path,
        "benchmark_split": regime.benchmark_path,
        "task_template": regime.task_template_path,
        "seed_policy": regime.path_value("seed_policy"),
        "boundary_guidance": regime.path_value("boundary_guidance"),
        "static_asi": regime.path_value("static_asi"),
        "feedback_split": regime.split_path("feedback"),
        "pareto_split": regime.split_path("pareto"),
    }


def _prompt_paths(regime: Any) -> dict[str, Path | None]:
    return {
        "base_prompt": regime.base_prompt_path,
        "task_template": regime.task_template_path,
        "agent_cards.structured": _agent_card_path_or_none(regime, "structured"),
        "agent_cards.plain": _agent_card_path_or_none(regime, "plain"),
        "seed_policy": regime.path_value("seed_policy"),
        "boundary_guidance": regime.path_value("boundary_guidance"),
        "static_asi": regime.path_value("static_asi"),
    }


def _agent_card_path_or_none(regime: Any, variant: str) -> Path | None:
    try:
        return regime.agent_card_path(variant)
    except (TypeError, ValueError):
        return None


def _validate_required_paths(regime: Any) -> list[str]:
    return [
        f"{name} does not exist: {path}"
        for name, path in _required_regime_paths(regime).items()
        if path is not None and not path.exists()
    ]


def _schema_label_order(regime: Any) -> list[str]:
    schema = json.loads(regime.schema_path.read_text(encoding="utf-8"))
    properties = schema.get("properties", {})
    label_prop = properties.get("labels") or properties.get("topics_of_interest")
    return list(label_prop["items"]["enum"])


def _validate_label_contract(regime: Any) -> list[str]:
    problems: list[str] = []
    try:
        labels = regime.label_order
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        return [f"label_order is not readable: {exc}"]
    try:
        schema_labels = _schema_label_order(regime)
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        return [f"schema label enum is not readable: {exc}"]
    if labels != schema_labels:
        problems.append("label_order does not exactly match schema enum order")
    return problems


def _validate_agent_cards(regime: Any) -> list[str]:
    problems: list[str] = []
    variants = {"structured", "plain"}
    default_variant = regime.raw.get("default_variant")
    if isinstance(default_variant, str):
        variants.add(default_variant)
    for variant in sorted(variants):
        cards = regime.raw.get("agent_cards")
        if isinstance(cards, dict) and cards.get(variant) is None and variant != default_variant:
            continue
        try:
            card = regime.agent_card_path(variant)
        except (TypeError, ValueError) as exc:
            problems.append(f"agent_cards.{variant} is invalid: {exc}")
            continue
        if not card.exists():
            problems.append(f"agent_cards.{variant} does not exist: {card}")
    return problems


def _validate_prompt_placeholders(regime: Any) -> list[str]:
    problems: list[str] = []
    project_root = project_root_for_regime(regime)
    for name, path in _prompt_paths(regime).items():
        if path is None or not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            problems.append(f"{name} is not readable: {path}: {exc}")
            continue
        for raw_ref in FILE_PLACEHOLDER_RE.findall(text):
            ref = Path(raw_ref.strip())
            ref_path = ref if ref.is_absolute() else project_root / ref
            if not ref_path.exists():
                problems.append(f"{name} has missing file placeholder {raw_ref!r}: {ref_path}")
    return problems


def _validate_reflection_agent(regime: Any) -> list[str]:
    project_root = project_root_for_regime(regime)
    agent_name = str(regime.raw.get("reflection_agent", "openclaw_gepa_reflector"))
    env_dir = regime.path_value("reflection_env_dir") or (project_root / ".fast-agent")
    card = env_dir / "agent-cards" / f"{agent_name}.md"
    problems = []
    if not (env_dir / "fast-agent.yaml").exists():
        problems.append(f"reflection env missing fast-agent.yaml: {env_dir / 'fast-agent.yaml'}")
    if not card.exists():
        problems.append(f"reflection AgentCard missing for {agent_name}: {card}")
    return problems


def _validate_trackio_config(regime: Any) -> list[str]:
    trackio = regime.mapping("trackio")
    problems = []
    for key in ("project", "group", "local_dir"):
        value = trackio.get(key)
        if not isinstance(value, str) or not value.strip():
            problems.append(f"trackio.{key} must be a non-empty string")
    return problems


def _validate_plan_builds(regime: Any) -> list[str]:
    try:
        variant = str(regime.raw.get("default_variant") or "structured")
        build_run_plan(regime, variant=variant)
        if regime.benchmark_path is not None:
            build_benchmark_plan(regime, candidate="base", variant=variant)
    except (OSError, TypeError, ValueError) as exc:
        return [f"could not build run/benchmark plan: {exc}"]
    return []


def validate_regime(regime: Any) -> list[str]:
    problems: list[str] = []
    problems.extend(_validate_required_paths(regime))
    problems.extend(_validate_label_contract(regime))
    problems.extend(_validate_agent_cards(regime))
    problems.extend(_validate_prompt_placeholders(regime))
    problems.extend(_validate_reflection_agent(regime))
    problems.extend(_validate_trackio_config(regime))
    problems.extend(_validate_plan_builds(regime))
    return problems


def _pyproject_sources(project_root: Path) -> dict[str, Any]:
    pyproject = project_root / "pyproject.toml"
    payload = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    return dict(payload.get("tool", {}).get("uv", {}).get("sources", {}))


def _doctor_editable_sources(project_root: Path) -> list[str]:
    errors = []
    for package, source in _pyproject_sources(project_root).items():
        if not isinstance(source, dict):
            continue
        raw_path = source.get("path")
        if not isinstance(raw_path, str):
            continue
        source_path = (project_root / raw_path).resolve()
        if not source_path.exists():
            errors.append(f"editable dependency {package!r} path does not exist: {source_path}")
    return errors


def _doctor_imports() -> list[str]:
    errors = []
    for module in ("fast_agent", "gepa", "trackio"):
        if importlib.util.find_spec(module) is None:
            errors.append(f"required import is unavailable: {module}")
    return errors


def _doctor_executables() -> list[str]:
    errors = []
    for executable in ("fast-agent", "trackio"):
        if shutil.which(executable) is None:
            errors.append(f"required executable is not on PATH: {executable}")
    return errors


def _doctor_venv(project_root: Path, env: Mapping[str, str]) -> list[str]:
    active = env.get("VIRTUAL_ENV")
    expected = str(project_root / ".venv")
    if active and Path(active).resolve() != Path(expected).resolve():
        return [
            f"VIRTUAL_ENV points outside this repo: {active}. "
            "Run `deactivate 2>/dev/null || true; unset VIRTUAL_ENV` before `uv run`."
        ]
    return []


def doctor_report(regime: Any, env: Mapping[str, str] | None = None) -> DoctorReport:
    project_root = project_root_for_regime(regime)
    active_env = os.environ if env is None else env
    errors = []
    warnings = []
    errors.extend(_doctor_editable_sources(project_root))
    errors.extend(_doctor_imports())
    errors.extend(_doctor_executables())
    errors.extend(f"regime: {problem}" for problem in validate_regime(regime))
    warnings.extend(_doctor_venv(project_root, active_env))
    if not (project_root / ".venv").exists():
        warnings.append(f"project virtualenv does not exist yet: {project_root / '.venv'}")
    return DoctorReport(errors=errors, warnings=warnings)


def print_doctor(regime: Any) -> int:
    report = doctor_report(regime)
    if report.errors:
        print("Doctor failed:")
        for error in report.errors:
            print(f"- ERROR: {error}")
    else:
        print("Doctor passed.")
    for warning in report.warnings:
        print(f"- WARNING: {warning}")
    return 0 if report.ok else 1


def _audit_regimes(project_root: Path) -> AuditCheck:
    problems = []
    regime_paths = discover_regimes(project_root)
    for path in regime_paths:
        try:
            regime = load_regime(path)
        except (OSError, TypeError, ValueError, KeyError) as exc:
            problems.append(f"{path}: {exc}")
            continue
        problems.extend(f"{regime.name}: {problem}" for problem in validate_regime(regime))
    detail = f"{len(regime_paths)} regimes valid" if not problems else "; ".join(problems)
    return AuditCheck(name="regimes", ok=not problems, detail=detail)


def _audit_doctor(regime: Any) -> AuditCheck:
    report = doctor_report(regime)
    details = [*report.errors, *[f"WARNING: {warning}" for warning in report.warnings]]
    return AuditCheck(
        name="doctor",
        ok=report.ok,
        detail="passed" if not details else "; ".join(details),
    )


def _stale_path_patterns() -> tuple[str, ...]:
    return (
        "/" + "/".join(("home", "ssmith", "temp", "gepa-batch-openclaw")),
        "/".join(("eval", "openclaw", "easy-set-pilot")),
        "/".join(("artifacts", "batch-manifests")),
        "/".join(("artifacts", "lineage")),
        "source" + "_ledger",
        "gold" + "5",
        "gold" + "-5",
    )


def _audit_roots(project_root: Path) -> list[Path]:
    names = (
        "README.md",
        "docs",
        "datasets",
        "regimes",
        "tools",
        "src",
        "scripts",
        "pyproject.toml",
    )
    return [project_root / name for name in names]


def _audit_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    if root.exists():
        return [path for path in root.rglob("*") if path.is_file()]
    return []


def _stale_hits_for_file(project_root: Path, path: Path, patterns: tuple[str, ...]) -> list[str]:
    if "__pycache__" in path.parts:
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    return [
        f"{path.relative_to(project_root)}: {pattern}"
        for pattern in patterns
        if pattern in text
    ]


def _audit_stale_paths(project_root: Path) -> AuditCheck:
    patterns = _stale_path_patterns()
    allowed = {project_root / "tests/test_repo_hygiene.py"}
    hits = [
        hit
        for root in _audit_roots(project_root)
        for path in _audit_files(root)
        if path not in allowed
        for hit in _stale_hits_for_file(project_root, path, patterns)
    ]
    return AuditCheck(
        name="stale_paths",
        ok=not hits,
        detail="none" if not hits else "; ".join(hits[:10]),
    )


def _audit_runner_preflight(regime: Any, *, benchmark: bool) -> AuditCheck:
    if benchmark:
        plan = build_benchmark_plan(
            regime,
            candidate="base",
            variant=str(regime.raw.get("default_variant") or "structured"),
        )
        name = "benchmark_preflight"
    else:
        plan = build_run_plan(
            regime,
            model="gemma-e4",
            variant=str(regime.raw.get("default_variant") or "structured"),
            overrides={"max_metric_calls": 1600},
        )
        name = "gepa_preflight"
    completed = _capture_command(
        [*plan.command, "--preflight-only"],
        project_root=plan.project_root,
        trackio_dir=plan.trackio_dir,
    )
    detail = "ok" if completed.returncode == 0 else (completed.stderr or completed.stdout).strip()
    return AuditCheck(name=name, ok=completed.returncode == 0, detail=detail)


def audit_report(regime: Any) -> AuditReport:
    project_root = project_root_for_regime(regime)
    checks = [
        _audit_regimes(project_root),
        _audit_doctor(regime),
        _audit_stale_paths(project_root),
        _audit_runner_preflight(regime, benchmark=False),
        _audit_runner_preflight(regime, benchmark=True),
    ]
    return AuditReport(checks=checks)


def print_audit(regime: Any) -> int:
    report = audit_report(regime)
    payload = {
        "ok": report.ok,
        "checks": [
            {"name": check.name, "ok": check.ok, "detail": check.detail}
            for check in report.checks
        ],
    }
    print(json.dumps(payload, indent=2))
    return 0 if report.ok else 1


def run_plan_command(plan: Any, *, extra_args: tuple[str, ...] = ()) -> int:
    return _run_command(
        [*plan.command, *extra_args],
        project_root=plan.project_root,
        trackio_dir=plan.trackio_dir,
    )


def print_or_run_gepa_plan(
    args: argparse.Namespace,
    regime: Any,
    summary: Mapping[str, object],
) -> int:
    variant = args.variant or regime.raw.get("default_variant") or "structured"
    plan = build_run_plan(
        regime,
        model=args.model,
        reflection_model=args.reflection_model,
        variant=variant,
        run_index=args.run_index,
        overrides={"max_metric_calls": args.max_metric_calls}
        if args.max_metric_calls is not None
        else None,
    )
    extra_args = ("--preflight-only",) if args.runner_preflight else ()
    if args.run:
        return run_plan_command(plan, extra_args=extra_args)
    if args.shell:
        print(shell_line(plan, extra_args=extra_args))
        return 0
    print(json.dumps(summary, indent=2))
    print(json.dumps(plan_payload(plan, extra_args=extra_args), indent=2))
    return 0


def benchmark_plans(args: argparse.Namespace, regime: Any) -> list[Any]:
    if args.repeat < 1:
        msg = "--repeat must be >= 1"
        raise ValueError(msg)
    return [
        build_benchmark_plan(
            regime,
            candidate=args.benchmark_run,
            model=args.model,
            variant=args.variant or regime.raw.get("default_variant") or "structured",
            run_index=args.run_index + offset,
        )
        for offset in range(args.repeat)
    ]


def print_benchmark_plans(
    args: argparse.Namespace,
    regime: Any,
    summary: Mapping[str, object],
) -> int:
    plans = benchmark_plans(args, regime)
    extra_args = ("--preflight-only",) if args.runner_preflight else ()
    if args.run:
        for plan in plans:
            status = run_plan_command(plan, extra_args=extra_args)
            if status != 0:
                return status
        return 0
    if args.shell:
        for plan in plans:
            print(shell_line(plan, extra_args=extra_args))
        return 0
    print(json.dumps(summary, indent=2))
    print(json.dumps([plan_payload(plan, extra_args=extra_args) for plan in plans], indent=2))
    return 0


def score_outputs(args: argparse.Namespace, regime: Any) -> int:
    report = score_output_file(regime, args.score_output, split=args.split)
    payload = report.to_dict()
    print(json.dumps(payload["scores"], indent=2))
    if args.report_output is not None:
        report.write_json(args.report_output)
        print(f"wrote report to {args.report_output}")
    return 0


def print_validation(regime: Any) -> int:
    problems = validate_regime(regime)
    if problems:
        print("Regime validation failed:")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print(f"Regime {regime.name} is valid.")
    return 0


def _dispatch_requested_action(
    args: argparse.Namespace,
    regime: Any,
    summary: Mapping[str, object],
) -> int | None:
    if args.run and args.shell:
        raise SystemExit("--run and --shell cannot be used together")

    def trackio_action() -> int:
        if not args.run:
            print(trackio_shell_line(regime))
            return 0
        project_root, trackio_dir, command = trackio_command(regime)
        return _run_command(
            command,
            project_root=project_root,
            trackio_dir=trackio_dir,
            extra_env={"BROWSER": "/bin/true"},
        )

    def score_action() -> int:
        print(json.dumps(summary, indent=2))
        return score_outputs(args, regime)

    actions: tuple[tuple[bool, Callable[[], int]], ...] = (
        (args.regime_info, lambda: (print(json.dumps(regime_info(regime), indent=2)) or 0)),
        (args.doctor, lambda: print_doctor(regime)),
        (args.audit, lambda: print_audit(regime)),
        (args.validate, lambda: print_validation(regime)),
        (args.trackio_command, trackio_action),
        (args.plan_gepa, lambda: print_or_run_gepa_plan(args, regime, summary)),
        (args.plan_benchmark, lambda: print_benchmark_plans(args, regime, summary)),
        (args.score_output is not None, score_action),
    )
    for enabled, action in actions:
        if enabled:
            return action()
    return None


def dispatch(args: argparse.Namespace, regime: Any, summary: Mapping[str, object]) -> int:
    status = _dispatch_requested_action(args, regime, summary)
    if status is not None:
        return status
    if args.run:
        raise SystemExit("--run requires --plan-gepa, --plan-benchmark, or --trackio-command")
    print(json.dumps(summary, indent=2))
    if not args.summary:
        print("Use --plan-gepa or --plan-benchmark to emit runnable commands.")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.list_regimes:
        return print_regime_list(Path.cwd())
    regime = load_regime(args.regime)
    return dispatch(args, regime, regime_summary(regime))
