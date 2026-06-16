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
    assert (
        plan.command[plan.command.index("--output-schema") + 1]
        == "regimes/v6o/schemas/teacher-output-v6h.schema.json"
    )
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
    assert "regimes/v7a/prompts/vanilla-labeler-plain-v7a.md" in plan.command
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
    assert (
        plan.command[plan.command.index("--output-schema") + 1]
        == "regimes/v6p/schemas/teacher-output-v6h.schema.json"
    )
    assert plan.command[plan.command.index("--reflection-env-dir") + 1] == ".fast-agent"
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


def test_v7c_run_plan_uses_custom_proposer() -> None:
    regime = load_regime(Path("regimes/v7c-custom-proposer/regime.yaml"))

    plan = build_run_plan(regime, model="codexresponses.gpt-5.4-mini", run_index=4)

    assert plan.trackio_project == "easy-v7c-custom-proposer-gepa"
    assert plan.trackio_group == "v7c-custom-proposer"
    assert (
        plan.run_name
        == "gpt-5-4-mini-v7c-custom-proposer-soft-exact-structured-full-"
        "openclaw-compact-mb20-mc1400-004"
    )
    proposer_index = plan.command.index("--candidate-proposer")
    assert plan.command[proposer_index + 1] == "openclaw-compact"
    feedback_index = plan.command.index("--feedback-profile")
    assert plan.command[feedback_index + 1] == "full"
    assert "--plain-labels" not in plan.command


def test_v7d_final_run_plan_is_compact_default() -> None:
    regime = load_regime(Path("regimes/v7d-final/regime.yaml"))

    plan = build_run_plan(
        regime,
        model="gemma-e4",
        variant=str(regime.raw.get("default_variant", "structured")),
        run_index=5,
    )

    assert plan.trackio_project == "easy-v7d-final-gepa"
    assert plan.trackio_group == "v7d-final"
    assert plan.run_name == "gemma-e4-v7d-final-soft-exact-structured-compact-mb20-mc1400-005"
    assert plan.command[plan.command.index("--feedback-profile") + 1] == "compact"
    assert plan.command[plan.command.index("--candidate-proposer") + 1] == "default"
    assert plan.command[plan.command.index("--policy-char-budget") + 1] == "5000"
    assert (
        plan.command[plan.command.index("--reflection-env-dir") + 1]
        == "regimes/v7d-final/.fast-agent"
    )
    assert "--plain-labels" not in plan.command
    assert (
        plan.command[plan.command.index("--output-schema") + 1]
        == "regimes/v7d-final/schemas/output-v7d.schema.json"
    )


def test_v7d_final_benchmark_plan_uses_regime_local_reflection_env() -> None:
    regime = load_regime(Path("regimes/v7d-final/regime.yaml"))

    plan = build_benchmark_plan(
        regime,
        candidate="base",
        variant=str(regime.raw.get("default_variant", "structured")),
    )

    assert plan.trackio_group == "v7d-final-benchmark"
    assert (
        plan.run_name
        == "gpt-5-5-reasoning-high-v7d-final-row-soft-exact-structured-base-bench-001"
    )
    assert "--plain-labels" not in plan.command
    assert (
        plan.command[plan.command.index("--reflection-env-dir") + 1]
        == "regimes/v7d-final/.fast-agent"
    )


def test_v7e_benchmark_plan_uses_candidate_topic_definitions(tmp_path: Path) -> None:
    regime = load_regime(Path("regimes/v7e-mutable-definitions/regime.yaml"))
    run_dir = tmp_path / "candidate-0004"
    run_dir.mkdir()
    policy_path = run_dir / "best-policy.md"
    definitions_path = run_dir / "best-topic-definitions.md"
    policy_path.write_text("candidate policy\n", encoding="utf-8")
    definitions_path.write_text("candidate definitions\n", encoding="utf-8")

    plan = build_benchmark_plan(regime, candidate=str(run_dir), variant="plain", model="gemma-e4")

    assert "--mutable-topic-definitions" in plan.command
    assert plan.command[plan.command.index("--mutable-topic-definitions") + 1] == str(
        definitions_path
    )
    assert str(policy_path) in plan.command
    assert "--plain-labels" in plan.command


def test_v7f_run_plan_includes_topic_definition_budget() -> None:
    regime = load_regime(Path("regimes/v7f-constrained-definitions/regime.yaml"))

    plan = build_run_plan(regime, variant="plain", model="gemma-e4")

    assert "--mutable-topic-definitions" in plan.command
    assert "--topic-definitions-char-budget" in plan.command
    assert plan.command[plan.command.index("--topic-definitions-char-budget") + 1] == "9500"
    assert "--mutable-boundary-overlay" not in plan.command


def test_v7f_overlay_benchmark_plan_uses_candidate_overlay_and_budget(tmp_path: Path) -> None:
    regime = load_regime(Path("regimes/v7f-constrained-definitions-overlay/regime.yaml"))
    run_dir = tmp_path / "candidate-0004"
    run_dir.mkdir()
    policy_path = run_dir / "best-policy.md"
    definitions_path = run_dir / "best-topic-definitions.md"
    overlay_path = run_dir / "best-boundary-overlay.md"
    policy_path.write_text("candidate policy\n", encoding="utf-8")
    definitions_path.write_text("candidate definitions\n", encoding="utf-8")
    overlay_path.write_text("candidate overlay\n", encoding="utf-8")

    plan = build_benchmark_plan(regime, candidate=str(run_dir), variant="plain", model="gemma-e4")

    assert "--mutable-boundary-overlay" in plan.command
    assert plan.command[plan.command.index("--mutable-boundary-overlay") + 1] == str(overlay_path)
    assert "--mutable-topic-definitions" in plan.command
    assert plan.command[plan.command.index("--mutable-topic-definitions") + 1] == str(
        definitions_path
    )
    assert "--topic-definitions-char-budget" in plan.command
    assert plan.command[plan.command.index("--topic-definitions-char-budget") + 1] == "9500"


def test_v7g_generator_mutate_all_plan_uses_total_mutable_budget() -> None:
    regime = load_regime(Path("regimes/v7g-generator-mutate-all/regime.yaml"))

    plan = build_run_plan(regime, variant="plain", model="deepseek4flash")

    assert (
        plan.run_name
        == "deepseek4flash-v7g-generator-mutate-all-soft-exact-plain-compact-"
        "allmut-tot20000-mb30-mc2400-001"
    )
    assert "--mutable-boundary-overlay" in plan.command
    assert "--mutable-topic-definitions" in plan.command
    assert "--total-mutable-char-budget" in plan.command
    assert plan.command[plan.command.index("--total-mutable-char-budget") + 1] == "20000"
    assert plan.command[plan.command.index("--policy-char-budget") + 1] == "4500"
    assert plan.command[plan.command.index("--topic-definitions-char-budget") + 1] == "0"
    assert (
        plan.command[plan.command.index("--seed-policy") + 1]
        == "regimes/v7g-generator-mutate-all/../v7b-generator-prompt-seed/prompts/seed-policy-vanilla-v7b-generator-prompt-seed.md"
    )


def test_v7g_benchmark_plan_uses_all_candidate_mutable_components(tmp_path: Path) -> None:
    regime = load_regime(Path("regimes/v7g-generator-mutate-all/regime.yaml"))
    run_dir = tmp_path / "candidate-0010"
    run_dir.mkdir()
    policy_path = run_dir / "best-policy.md"
    definitions_path = run_dir / "best-topic-definitions.md"
    overlay_path = run_dir / "best-boundary-overlay.md"
    policy_path.write_text("candidate policy\n", encoding="utf-8")
    definitions_path.write_text("candidate definitions\n", encoding="utf-8")
    overlay_path.write_text("candidate overlay\n", encoding="utf-8")

    plan = build_benchmark_plan(
        regime,
        candidate=str(run_dir),
        variant="plain",
        model="deepseek4flash",
    )

    assert plan.command[plan.command.index("--seed-policy") + 1] == str(policy_path)
    assert plan.command[plan.command.index("--mutable-topic-definitions") + 1] == str(
        definitions_path
    )
    assert plan.command[plan.command.index("--mutable-boundary-overlay") + 1] == str(
        overlay_path
    )
    assert plan.command[plan.command.index("--total-mutable-char-budget") + 1] == "20000"
