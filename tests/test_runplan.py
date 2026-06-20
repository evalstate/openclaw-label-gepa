from pathlib import Path

from openclaw_label_gepa.regimes import load_regime
from openclaw_label_gepa.runplan import build_benchmark_plan, build_run_plan, model_slug

V7H = Path("regimes/v7h-clean-generator-mutate-all/regime.yaml")
V7I = Path("regimes/v7i-guarded-generator-mutate-all/regime.yaml")


def test_model_slug_removes_provider_prefix() -> None:
    assert model_slug("codexresponses.gpt-5.4-mini") == "gpt-5-4-mini"
    assert model_slug("codexresponses.gpt-5.5?reasoning=high") == "gpt-5-5-reasoning-high"


def test_v7i_default_run_plan_uses_guarded_regime() -> None:
    regime = load_regime(V7I)

    plan = build_run_plan(regime, model="gemma-e4", run_index=3, overrides={"max_metric_calls": 1600})

    assert plan.trackio_project == "easy-v7i-guarded-generator-mutate-all-gepa"
    assert plan.trackio_group == "v7i-guarded-generator-mutate-all"
    assert plan.trackio_dir.as_posix().endswith("runs/v7i-guarded-generator-mutate-all/trackio")
    assert plan.run_name == "gemma-e4-v7i-structured-compact-tot20000-mb30-mc1600-003"
    assert "regimes/v7i-guarded-generator-mutate-all/prompts/vanilla-labeler-v7i.md" in plan.command
    assert "regimes/v7i-guarded-generator-mutate-all/data/feedback240.jsonl" in plan.command
    assert "--mutable-topic-definitions" in plan.command
    assert "--mutable-boundary-overlay" in plan.command
    assert "--total-mutable-char-budget" in plan.command
    assert plan.command[plan.command.index("--total-mutable-char-budget") + 1] == "20000"
    assert "--plain-labels" not in plan.command


def test_run_plan_can_override_trackio_project() -> None:
    regime = load_regime(V7I)

    plan = build_run_plan(regime, trackio_project="fresh-project")

    assert plan.trackio_project == "fresh-project"
    assert plan.command[plan.command.index("--project") + 1] == "fresh-project"


def test_v7h_run_plan_is_retained_for_comparison() -> None:
    regime = load_regime(V7H)

    plan = build_run_plan(regime, model="deepseek4flash", variant="plain", run_index=2)

    assert plan.trackio_project == "easy-v7h-clean-generator-mutate-all-gepa"
    assert plan.trackio_group == "v7h-clean-generator-mutate-all"
    assert plan.run_name == "deepseek4flash-v7h-plain-compact-tot20000-mb30-mc2400-002"
    assert "regimes/v7h-clean-generator-mutate-all/data/feedback300.jsonl" in plan.command
    assert "--plain-labels" in plan.command


def test_v7i_base_benchmark_plan_uses_benchmark_split() -> None:
    regime = load_regime(V7I)

    plan = build_benchmark_plan(regime, candidate="base", run_index=2)

    assert plan.trackio_project == "easy-v7i-guarded-generator-mutate-all-gepa"
    assert plan.trackio_group == "v7i-guarded-generator-mutate-all-benchmark"
    assert plan.run_name == "gpt-5-4-mini-v7i-guarded-generator-mutate-all-row-soft-exact-structured-base-bench-002"
    assert "--evaluate-only" in plan.command
    assert "regimes/v7i-guarded-generator-mutate-all/data/bench78.jsonl" in plan.command
    assert (
        plan.command[plan.command.index("--output-schema") + 1]
        == "regimes/v7i-guarded-generator-mutate-all/schemas/output-v7i.schema.json"
    )


def test_benchmark_plan_can_override_trackio_project() -> None:
    regime = load_regime(V7I)

    plan = build_benchmark_plan(regime, candidate="base", trackio_project="fresh-project")

    assert plan.trackio_project == "fresh-project"
    assert plan.command[plan.command.index("--project") + 1] == "fresh-project"


def test_candidate_benchmark_plan_accepts_all_mutable_components(tmp_path: Path) -> None:
    regime = load_regime(V7I)
    run_dir = tmp_path / "candidate-0007"
    run_dir.mkdir()
    policy_path = run_dir / "best-policy.md"
    definitions_path = run_dir / "best-topic-definitions.md"
    overlay_path = run_dir / "best-boundary-overlay.md"
    policy_path.write_text("candidate policy\n", encoding="utf-8")
    definitions_path.write_text("candidate definitions\n", encoding="utf-8")
    overlay_path.write_text("candidate overlay\n", encoding="utf-8")

    plan = build_benchmark_plan(regime, candidate=str(run_dir), variant="plain", model="gemma-e4")

    assert plan.run_name.endswith("plain-candidate-0007-bench-001")
    assert plan.command[plan.command.index("--seed-policy") + 1] == str(policy_path)
    assert plan.command[plan.command.index("--mutable-topic-definitions") + 1] == str(
        definitions_path
    )
    assert plan.command[plan.command.index("--mutable-boundary-overlay") + 1] == str(overlay_path)
    assert "--plain-labels" in plan.command
