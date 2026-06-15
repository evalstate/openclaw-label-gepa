from pathlib import Path

from openclaw_label_gepa.regimes import load_regime
from openclaw_label_gepa.runplan import build_benchmark_plan, build_run_plan, model_slug


def test_model_slug_removes_provider_prefix() -> None:
    assert model_slug("codexresponses.gpt-5.4-mini") == "gpt-5-4-mini"
    assert model_slug("codexresponses.gpt-5.5?reasoning=high") == "gpt-5-5-reasoning-high"


def test_v6o_run_plan_has_trackio_and_clear_name() -> None:
    regime = load_regime(Path("regimes/v6o/regime.yaml"))

    plan = build_run_plan(regime, model="gemma-e4", variant="plain", run_index=7)

    assert plan.trackio_project == "easy-v6o-jaccard-gepa"
    assert plan.trackio_group == "v6o"
    assert plan.trackio_dir.as_posix().endswith(".trackio/v6o")
    assert plan.run_name == "gemma-e4-v6o-jaccard-exact-plain-compact-mb15-mc2600-007"
    assert "--plain-labels" in plan.command
    assert "--trackio-group" in plan.command
    assert "v6o" in plan.command
    assert "regimes/v6o/data/feedback300.jsonl" in plan.command


def test_v6p_run_plan_uses_soft_exact_regime() -> None:
    regime = load_regime(Path("regimes/v6p/regime.yaml"))

    plan = build_run_plan(regime, run_index=3)

    assert plan.trackio_project == "easy-v6p-soft-gepa"
    assert plan.trackio_group == "v6p"
    assert (
        plan.run_name
        == "gpt-5-5-reasoning-high-v6p-soft-exact-structured-compact-mb15-mc1400-003"
    )
    assert "--score-mode" in plan.command
    assert "row-soft-exact" in plan.command
    assert "--max-metric-calls" in plan.command
    assert "1400" in plan.command


def test_v7a_run_plan_can_use_plain_promoted_regime() -> None:
    regime = load_regime(Path("regimes/v7a/regime.yaml"))

    plan = build_run_plan(
        regime,
        variant=str(regime.raw.get("default_variant", "structured")),
        run_index=1,
    )

    assert plan.trackio_project == "easy-v7a-plain-gepa"
    assert plan.trackio_group == "v7a"
    assert plan.trackio_dir.as_posix().endswith("runs/v7a/trackio")
    assert plan.run_name == "gpt-5-5-reasoning-high-v7a-soft-exact-plain-compact-mb15-mc1400-001"
    assert "regimes/v7a/prompts/openclaw-vanilla-labeler-plain-v7a.md" in plan.command
    assert "--plain-labels" in plan.command
    assert str(Path.cwd() / "runs/v7a/gepa") in plan.command


def test_v7a_run_plan_allows_metric_call_override() -> None:
    regime = load_regime(Path("regimes/v7a/regime.yaml"))

    plan = build_run_plan(
        regime,
        model="gemma-e4",
        variant="plain",
        run_index=3,
        overrides={"max_metric_calls": 1600},
    )

    assert plan.run_name == "gemma-e4-v7a-soft-exact-plain-compact-mb15-mc1600-003"
    max_calls_index = plan.command.index("--max-metric-calls")
    assert plan.command[max_calls_index + 1] == "1600"


def test_v6p_base_benchmark_plan_uses_benchmark_split() -> None:
    regime = load_regime(Path("regimes/v6p/regime.yaml"))

    plan = build_benchmark_plan(regime, candidate="base", run_index=2)

    assert plan.trackio_project == "easy-v6p-soft-gepa"
    assert plan.trackio_group == "v6p-benchmark"
    assert plan.run_name == "gpt-5-5-reasoning-high-v6p-row-soft-exact-structured-base-bench-002"
    assert "--evaluate-only" in plan.command
    assert "regimes/v6p/data/bench78.jsonl" in plan.command
    assert "regimes/v6p/prompts/seed-policy-vanilla-v6p.md" in plan.command
    assert "--parallel" in plan.command
    assert "4" in plan.command


def test_candidate_benchmark_plan_accepts_run_directory(tmp_path: Path) -> None:
    regime = load_regime(Path("regimes/v6p/regime.yaml"))
    run_dir = tmp_path / "candidate-0007"
    run_dir.mkdir()
    policy_path = run_dir / "best-policy.md"
    overlay_path = run_dir / "best-boundary-overlay.md"
    policy_path.write_text("candidate policy\n", encoding="utf-8")
    overlay_path.write_text("candidate overlay\n", encoding="utf-8")

    plan = build_benchmark_plan(regime, candidate=str(run_dir), variant="plain", model="gemma-e4")

    assert plan.run_name.endswith("plain-candidate-0007-bench-001")
    assert str(policy_path) in plan.command
    assert str(overlay_path) in plan.command
    assert "--mutable-boundary-overlay" in plan.command
    assert "--plain-labels" in plan.command
