from __future__ import annotations

import re
import shlex
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from openclaw_label_gepa.regimes import Regime


@dataclass(frozen=True)
class RunPlan:
    project_root: Path
    regime: str
    model: str
    reflection_model: str
    variant: str
    run_name: str
    run_root: Path
    trackio_project: str
    trackio_group: str
    trackio_dir: Path
    command: list[str]

    def shell_command(self) -> str:
        return " ".join(shlex.quote(part) for part in self.command)


@dataclass(frozen=True)
class BenchmarkPlan:
    project_root: Path
    regime: str
    candidate: str
    model: str
    variant: str
    run_name: str
    run_root: Path
    trackio_project: str
    trackio_group: str
    trackio_dir: Path
    command: list[str]

    def shell_command(self) -> str:
        return " ".join(shlex.quote(part) for part in self.command)


@dataclass(frozen=True)
class _GepaCommandArgs:
    defaults: dict[str, Any]
    task_model: str
    reflect_model: str
    variant: str
    trackio_project: str
    trackio_group: str
    run_root: Path
    run_name: str


def model_slug(model: str) -> str:
    value = model
    for prefix in ("codexresponses.", "responses."):
        value = value.removeprefix(prefix)
    value = value.replace("?reasoning=", "-reasoning-")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value or "model"


def _value(mapping: dict[str, Any], key: str, default: Any) -> Any:
    value = mapping.get(key)
    return default if value is None else value


def _path_arg(path: Path | None) -> str | None:
    return str(path) if path is not None else None


def _base_command(regime: Regime) -> list[str]:
    return [
        "uv",
        "run",
        "python",
        "tools/runners/gepa-runner.py",
        "--input",
        str(regime.train_path),
        "--feedback-input",
        str(regime.split_path("feedback") or regime.train_path),
    ]


def _extend_optional_paths(command: list[str], regime: Regime) -> None:
    pareto = _path_arg(regime.split_path("pareto"))
    bench = _path_arg(regime.split_path("benchmark"))
    if pareto is not None:
        command.extend(["--pareto-input", pareto])
    if bench is not None:
        command.extend(["--test-input", bench])


def _extend_gepa_args(
    command: list[str],
    regime: Regime,
    args: _GepaCommandArgs,
) -> None:
    defaults = args.defaults
    reflection_env_dir = regime.path_value("reflection_env_dir") or (
        regime.root.parents[1] / ".fast-agent"
    )
    command.extend(
        [
            "--agent-card",
            str(regime.agent_card_path(args.variant)),
            "--task-template",
            str(regime.task_template_path),
            "--allowed-topics",
            str(regime.label_order_path),
            "--output-schema",
            str(regime.schema_path),
            "--model",
            args.task_model,
            "--reflection-model",
            args.reflect_model,
            "--reflection-agent",
            str(regime.raw.get("reflection_agent", "openclaw_gepa_reflector")),
            "--reflection-env-dir",
            str(reflection_env_dir),
            "--gepa-mode",
            str(_value(defaults, "gepa_mode", "row-wise")),
            "--score-mode",
            str(regime.raw.get("score_mode", regime.metric)),
            "--feedback-profile",
            str(_value(defaults, "feedback_profile", "compact")),
            "--candidate-proposer",
            str(_value(defaults, "candidate_proposer", "default")),
            "--frontier-type",
            str(_value(defaults, "frontier_type", "hybrid")),
            "--candidate-selection-strategy",
            str(_value(defaults, "candidate_selection_strategy", "pareto")),
            "--acceptance-criterion",
            str(_value(defaults, "acceptance_criterion", "strict_improvement")),
            "--max-metric-calls",
            str(int(_value(defaults, "max_metric_calls", 12))),
            "--parallel",
            str(int(_value(defaults, "parallel", 4))),
            "--project",
            args.trackio_project,
            "--trackio-group",
            args.trackio_group,
            "--run-root",
            str(args.run_root),
            "--run-name",
            args.run_name,
        ]
    )
    reflection_minibatch_size = int(_value(defaults, "reflection_minibatch_size", 0))
    if reflection_minibatch_size:
        command.extend(["--reflection-minibatch-size", str(reflection_minibatch_size)])


def _extend_regime_artifacts(command: list[str], regime: Regime, variant: str) -> None:
    defaults = regime.mapping("run_defaults")
    for regime_key, arg_name in (
        ("seed_policy", "--seed-policy"),
        ("boundary_guidance", "--boundary-guidance"),
        ("static_asi", "--static-asi"),
        ("mutable_boundary_overlay", "--mutable-boundary-overlay"),
        ("mutable_topic_definitions", "--mutable-topic-definitions"),
    ):
        path = _path_arg(regime.path_value(regime_key))
        if path is not None:
            command.extend([arg_name, path])
    for default_key, arg_name in (
        ("hygiene_penalty", "--hygiene-penalty"),
        ("policy_char_budget", "--policy-char-budget"),
        ("topic_definitions_char_budget", "--topic-definitions-char-budget"),
        ("total_mutable_char_budget", "--total-mutable-char-budget"),
    ):
        if default_key in defaults:
            command.extend([arg_name, str(defaults[default_key])])
    if variant == "plain":
        command.append("--plain-labels")


def _run_name(
    regime: Regime,
    task_model: str,
    variant: str,
    run_index: int,
    defaults: dict[str, Any],
) -> str:
    max_metric_calls = int(_value(defaults, "max_metric_calls", 12))
    reflection_minibatch_size = int(_value(defaults, "reflection_minibatch_size", 0))
    run_name_template = str(
        _value(
            defaults,
            "run_name_template",
            "{model_slug}-{regime}-{score_mode}-{variant}-mc{max_metric_calls}-{run_index:03d}",
        )
    )
    return run_name_template.format(
        model_slug=model_slug(task_model),
        regime=regime.name,
        score_mode=str(regime.raw.get("score_mode", regime.metric)).replace("_", "-"),
        variant=variant,
        feedback_profile=str(_value(defaults, "feedback_profile", "compact")),
        candidate_proposer=str(_value(defaults, "candidate_proposer", "default")),
        reflection_minibatch_size=reflection_minibatch_size,
        max_metric_calls=max_metric_calls,
        total_mutable_char_budget=int(_value(defaults, "total_mutable_char_budget", 0)),
        parallel=int(_value(defaults, "parallel", 4)),
        run_index=run_index,
    )


def _candidate_slug(value: str) -> str:
    if value == "base":
        return "base"
    path_name = value.rstrip("/").split("/")[-1] or "candidate"
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", path_name).strip("-").lower()
    return slug or "candidate"


def _resolve_candidate_policy(regime: Regime, candidate: str) -> Path:
    if candidate == "base":
        seed_policy = regime.path_value("seed_policy")
        if seed_policy is None:
            msg = f"regime {regime.name} has no seed_policy for base benchmarking"
            raise ValueError(msg)
        return seed_policy
    path = Path(candidate)
    if path.is_file():
        return path
    for name in ("best-policy.md", "policy.md"):
        policy_path = path / name
        if policy_path.exists():
            return policy_path
    msg = f"benchmark candidate must be 'base', a policy file, or a run directory: {candidate}"
    raise ValueError(msg)


def _resolve_candidate_overlay(regime: Regime, candidate: str) -> Path | None:
    if candidate == "base":
        return regime.path_value("mutable_boundary_overlay")
    path = Path(candidate)
    if path.is_file():
        return regime.path_value("mutable_boundary_overlay")
    for name in ("best-boundary-overlay.md", "boundary-overlay.md"):
        overlay_path = path / name
        if overlay_path.exists():
            return overlay_path
    return regime.path_value("mutable_boundary_overlay")


def _resolve_candidate_topic_definitions(regime: Regime, candidate: str) -> Path | None:
    if candidate == "base":
        return regime.path_value("mutable_topic_definitions")
    path = Path(candidate)
    if path.is_file():
        return regime.path_value("mutable_topic_definitions")
    for name in ("best-topic-definitions.md", "topic-definitions.md"):
        definitions_path = path / name
        if definitions_path.exists():
            return definitions_path
    return regime.path_value("mutable_topic_definitions")


def _benchmark_run_name(
    regime: Regime,
    task_model: str,
    variant: str,
    candidate: str,
    run_index: int,
) -> str:
    score_mode = str(regime.raw.get("score_mode", regime.metric)).replace("_", "-")
    return (
        f"{model_slug(task_model)}-{regime.name}-{score_mode}-{variant}-"
        f"{_candidate_slug(candidate)}-bench-{run_index:03d}"
    )


def _benchmark_base_command(
    regime: Regime,
    *,
    benchmark_path: Path,
    task_model: str,
    variant: str,
    run_root: Path,
    run_name: str,
    trackio_project: str,
    trackio_group: str,
) -> list[str]:
    defaults = regime.mapping("run_defaults")
    reflection_env_dir = regime.path_value("reflection_env_dir") or (
        regime.root.parents[1] / ".fast-agent"
    )
    return [
        "uv",
        "run",
        "python",
        "tools/runners/gepa-runner.py",
        "--evaluate-only",
        "--input",
        str(benchmark_path),
        "--agent-card",
        str(regime.agent_card_path(variant)),
        "--task-template",
        str(regime.task_template_path),
        "--allowed-topics",
        str(regime.label_order_path),
        "--output-schema",
        str(regime.schema_path),
        "--model",
        task_model,
        "--reflection-agent",
        str(regime.raw.get("reflection_agent", "openclaw_gepa_reflector")),
        "--reflection-env-dir",
        str(reflection_env_dir),
        "--score-mode",
        str(regime.raw.get("score_mode", regime.metric)),
        "--parallel",
        str(int(_value(defaults, "parallel", 4))),
        "--project",
        trackio_project,
        "--trackio-group",
        trackio_group,
        "--run-root",
        str(run_root),
        "--run-name",
        run_name,
    ]


def _extend_benchmark_regime_args(command: list[str], regime: Regime) -> None:
    defaults = regime.mapping("run_defaults")
    for regime_key, arg_name in (
        ("boundary_guidance", "--boundary-guidance"),
        ("static_asi", "--static-asi"),
    ):
        path = _path_arg(regime.path_value(regime_key))
        if path is not None:
            command.extend([arg_name, path])
    for default_key, arg_name in (
        ("hygiene_penalty", "--hygiene-penalty"),
        ("policy_char_budget", "--policy-char-budget"),
        ("topic_definitions_char_budget", "--topic-definitions-char-budget"),
        ("total_mutable_char_budget", "--total-mutable-char-budget"),
    ):
        if default_key in defaults:
            command.extend([arg_name, str(defaults[default_key])])


def _extend_benchmark_candidate_args(
    command: list[str],
    *,
    policy_path: Path,
    overlay_path: Path | None,
    topic_definitions_path: Path | None,
    variant: str,
) -> None:
    command.extend(["--seed-policy", str(policy_path)])
    if overlay_path is not None:
        command.extend(["--mutable-boundary-overlay", str(overlay_path)])
    if topic_definitions_path is not None:
        command.extend(["--mutable-topic-definitions", str(topic_definitions_path)])
    if variant == "plain":
        command.append("--plain-labels")


def build_benchmark_plan(
    regime: Regime,
    *,
    candidate: str = "base",
    model: str | None = None,
    variant: str = "structured",
    run_index: int = 1,
    trackio_project: str | None = None,
) -> BenchmarkPlan:
    benchmark_path = regime.split_path("benchmark")
    if benchmark_path is None:
        msg = f"regime {regime.name} has no benchmark_split"
        raise ValueError(msg)
    trackio = regime.mapping("trackio")
    models = regime.mapping("models")
    task_model = model or str(models.get("default_task") or "codexresponses.gpt-5.4-mini")
    project_root = regime.root.parents[1].resolve()
    run_root = project_root / f"runs/{regime.name}/benchmark"
    trackio_project = trackio_project or str(_value(trackio, "project", f"{regime.name}-gepa"))
    trackio_group = f"{_value(trackio, 'group', regime.name)}-benchmark"
    trackio_dir = project_root / str(_value(trackio, "local_dir", f".trackio/{regime.name}"))
    run_name = _benchmark_run_name(regime, task_model, variant, candidate, run_index)
    policy_path = _resolve_candidate_policy(regime, candidate)
    overlay_path = _resolve_candidate_overlay(regime, candidate)
    topic_definitions_path = _resolve_candidate_topic_definitions(regime, candidate)
    command = _benchmark_base_command(
        regime,
        benchmark_path=benchmark_path,
        task_model=task_model,
        variant=variant,
        run_root=run_root,
        run_name=run_name,
        trackio_project=trackio_project,
        trackio_group=trackio_group,
    )
    _extend_benchmark_regime_args(command, regime)
    _extend_benchmark_candidate_args(
        command,
        policy_path=policy_path,
        overlay_path=overlay_path,
        topic_definitions_path=topic_definitions_path,
        variant=variant,
    )
    return BenchmarkPlan(
        project_root=project_root,
        regime=regime.name,
        candidate=candidate,
        model=task_model,
        variant=variant,
        run_name=run_name,
        run_root=run_root,
        trackio_project=trackio_project,
        trackio_group=trackio_group,
        trackio_dir=trackio_dir,
        command=command,
    )


def build_run_plan(
    regime: Regime,
    *,
    model: str | None = None,
    reflection_model: str | None = None,
    variant: str = "structured",
    run_index: int = 1,
    trackio_project: str | None = None,
    overrides: dict[str, Any] | None = None,
) -> RunPlan:
    defaults = {**regime.mapping("run_defaults"), **(overrides or {})}
    trackio = regime.mapping("trackio")
    models = regime.mapping("models")
    task_model = model or str(models.get("default_task") or "codexresponses.gpt-5.4-mini")
    reflect_model = reflection_model or str(
        models.get("default_reflection") or "codexresponses.gpt-5.5?reasoning=high"
    )
    project_root = regime.root.parents[1].resolve()
    run_root = project_root / str(_value(defaults, "run_root", f"runs/{regime.name}/gepa"))
    trackio_group = str(_value(trackio, "group", regime.name))
    trackio_project = trackio_project or str(_value(trackio, "project", f"{regime.name}-gepa"))
    trackio_dir = project_root / str(_value(trackio, "local_dir", f".trackio/{regime.name}"))
    run_name = _run_name(regime, task_model, variant, run_index, defaults)
    command = _base_command(regime)
    _extend_optional_paths(command, regime)
    _extend_gepa_args(
        command,
        regime,
        _GepaCommandArgs(
            defaults=defaults,
            task_model=task_model,
            reflect_model=reflect_model,
            variant=variant,
            trackio_project=trackio_project,
            trackio_group=trackio_group,
            run_root=run_root,
            run_name=run_name,
        ),
    )
    _extend_regime_artifacts(command, regime, variant)
    return RunPlan(
        project_root=project_root,
        regime=regime.name,
        model=task_model,
        reflection_model=reflect_model,
        variant=variant,
        run_name=run_name,
        run_root=run_root,
        trackio_project=trackio_project,
        trackio_group=trackio_group,
        trackio_dir=trackio_dir,
        command=command,
    )
