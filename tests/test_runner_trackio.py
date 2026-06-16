from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest


def _module(name: str) -> ModuleType:
    return ModuleType(name)


def _install_runner_import_stubs(monkeypatch: pytest.MonkeyPatch) -> None:
    fast_agent = _module("fast_agent")
    fast_agent_batch = _module("fast_agent.batch")
    fast_agent_eval = _module("fast_agent.eval")
    fast_agent_gepa = _module("fast_agent.integrations.gepa")
    fast_agent_integrations = _module("fast_agent.integrations")

    vars(fast_agent_batch)["BatchRunResult"] = object
    vars(fast_agent_eval)["CandidateRun"] = object
    for name in (
        "FastAgentBatchEvaluator",
        "FastAgentGEPATrackioCallback",
        "FastAgentReflectionLM",
        "FastAgentRowWiseBatchAdapter",
        "RowWiseEvaluationRun",
        "RowWiseScore",
    ):
        setattr(fast_agent_gepa, name, object)
    vars(fast_agent_gepa)["gepa_numeric_metrics"] = lambda report: {}
    vars(fast_agent_gepa)["safe_trackio_log"] = lambda payload: None

    for module in (
        fast_agent,
        fast_agent_batch,
        fast_agent_eval,
        fast_agent_integrations,
        fast_agent_gepa,
    ):
        monkeypatch.setitem(sys.modules, module.__name__, module)


def _load_runner(monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    _install_runner_import_stubs(monkeypatch)
    path = Path("tools/runners/gepa-runner.py")
    spec = importlib.util.spec_from_file_location("openclaw_gepa_runner", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_valset_callback_logs_seed_objective_without_outputs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load_runner(monkeypatch)
    logged: list[dict[str, int | float]] = []
    monkeypatch.setattr(module, "safe_trackio_log", logged.append)
    callback = module.OpenClawValsetAggregateCallback(
        val_rows=[],
        allowed_topics=set(),
        score_mode="row-soft-exact",
    )

    callback.on_valset_evaluated(
        {
            "iteration": 0,
            "candidate_idx": 0,
            "average_score": 0.7195555556,
            "outputs_by_val_id": None,
            "num_examples_evaluated": 60,
            "total_valset_size": 60,
            "is_best_program": True,
        }
    )
    callback.on_valset_evaluated(
        {
            "iteration": 1,
            "candidate_idx": 1,
            "average_score": 0.6596111111,
            "outputs_by_val_id": None,
        }
    )
    callback.on_valset_evaluated(
        {
            "iteration": 5,
            "candidate_idx": 5,
            "average_score": 0.7205,
            "outputs_by_val_id": None,
        }
    )

    assert len(logged) == 3
    assert logged[0]["gepa/iteration"] == 0
    assert logged[0]["openclaw/objective/val/proposal_gepa_score"] == pytest.approx(
        0.7195555556
    )
    assert logged[0]["openclaw/objective/val/gepa_score"] == pytest.approx(0.7195555556)
    assert "openclaw/objective/val/proposal_delta_vs_best_before" not in logged[0]

    assert logged[1]["openclaw/objective/val/proposal_gepa_score"] == pytest.approx(
        0.6596111111
    )
    assert logged[1]["openclaw/objective/val/best_gepa_score"] == pytest.approx(0.7195555556)
    assert logged[1]["openclaw/objective/val/gepa_score"] == pytest.approx(0.7195555556)
    assert logged[1]["openclaw/objective/val/proposal_delta_vs_best_before"] == pytest.approx(
        0.6596111111 - 0.7195555556
    )

    assert logged[2]["openclaw/objective/val/proposal_gepa_score"] == pytest.approx(0.7205)
    assert logged[2]["openclaw/objective/val/best_gepa_score"] == pytest.approx(0.7205)
    assert logged[2]["openclaw/objective/val/gepa_score"] == pytest.approx(0.7205)


def test_candidate_policy_trackio_payload_includes_length_and_penalty_score(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load_runner(monkeypatch)
    policy = "## Allowed Topics\n" + ("x" * 1100)
    penalties = module.policy_penalty_details(
        policy,
        hygiene_penalty_weight=0.03,
        policy_char_budget=100,
    )

    payload = module.candidate_policy_trackio_payload(penalties)

    assert payload["candidate/policy_length"] == len(policy)
    assert payload["candidate/policy_chars"] == len(policy)
    assert payload["candidate/policy_char_budget"] == 100
    assert payload["candidate/policy_length_over_budget"] == len(policy) - 100
    assert payload["candidate/policy_length_penalty"] == pytest.approx(
        penalties["policy_length_penalty"]
    )
    assert payload["candidate/hygiene_penalty"] == pytest.approx(0.03)
    assert payload["candidate/policy_penalty_score"] == pytest.approx(
        penalties["total_policy_penalty"]
    )
    assert payload["candidate/total_policy_penalty"] == pytest.approx(
        penalties["total_policy_penalty"]
    )


def test_topic_definition_penalty_details_prices_over_budget(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load_runner(monkeypatch)
    definitions = "- `docs`: Documentation.\n- `memory`: Memory.\n" + ("x" * 200)

    penalties = module.topic_definition_penalty_details(
        definitions,
        {"docs", "memory"},
        char_budget=100,
    )

    assert penalties["contract"]["ok"] is True
    assert penalties["topic_definitions_chars"] == len(definitions)
    assert penalties["topic_definitions_char_budget"] == 100
    assert penalties["topic_definitions_length_over_budget"] == len(definitions) - 100
    assert penalties["topic_definitions_length_penalty"] > 0
    assert penalties["topic_definition_compliance"] == 1.0


def test_topic_definition_penalty_details_detects_contract_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load_runner(monkeypatch)

    penalties = module.topic_definition_penalty_details(
        "- `docs`: Documentation.\n",
        {"docs", "memory"},
        char_budget=9500,
    )

    assert penalties["contract"]["ok"] is False
    assert penalties["contract"]["missing_topics"] == ["memory"]
    assert penalties["topic_definition_compliance"] == 0.0


def test_total_mutable_penalty_details_prices_combined_components(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load_runner(monkeypatch)

    penalties = module.total_mutable_penalty_details(
        {
            "policy": "p" * 40,
            "topic_definitions": "d" * 50,
            "boundary_overlay": "o" * 60,
        },
        char_budget=100,
    )

    assert penalties["component_chars"] == {
        "policy": 40,
        "topic_definitions": 50,
        "boundary_overlay": 60,
    }
    assert penalties["total_mutable_chars"] == 150
    assert penalties["total_mutable_char_budget"] == 100
    assert penalties["total_mutable_length_over_budget"] == 50
    assert penalties["total_mutable_length_penalty"] > 0


def test_surgical_feedback_profile_exposes_confusions_without_row_context(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load_runner(monkeypatch)

    args = module.parse_args(["--feedback-profile", "surgical"])
    assert args.feedback_profile == "surgical"

    report = {
        "scores": {"gepa_score": 0.42},
        "score_details": {"false_positives": 1, "false_negatives": 1},
        "evaluated": 2,
        "topic_error_patterns": [
            {"topic": "memory", "false_positives": 0, "false_negatives": 1},
            {"topic": "docs", "false_positives": 1, "false_negatives": 0},
        ],
        "confusions": [
            {"missed_topic": "memory", "extra_topic": "docs", "count": 1},
            {"missed_topic": "config", "extra_topic": "docs", "count": 1},
            {"missed_topic": "tests_ci", "extra_topic": "docs", "count": 1},
            {"missed_topic": "gateway", "extra_topic": "docs", "count": 1},
        ],
        "actionable_feedback": ["tighten docs", "recover memory", "avoid row facts", "extra"],
        "vanilla_f1_asi": {
            "global_diagnosis": {"diagnosis": "balanced"},
            "topic_priorities": [{"topic": "memory"}],
            "prompt_hygiene": {"findings": []},
        },
    }

    profiled = module.apply_feedback_profile(report, "surgical", mutable_overlay=False)

    assert profiled["feedback_profile"] == "surgical"
    assert len(profiled["confusions"]) == 3
    assert len(profiled["actionable_feedback"]) == 3
    assert "row_examples" not in profiled["vanilla_f1_asi"]
    assert "row failures" not in profiled["evaluation_context"]["feedback_profile_description"]

    row_profile = module.apply_row_feedback_profile(
        {
            "scores": {
                "gepa_score": 0.5,
                "row_topic_f1": 0.67,
                "row_exact": 0.0,
                "row_jaccard": 0.5,
                "valid_json": 1.0,
            },
            "expected": ["memory"],
            "actual": ["docs"],
            "false_positives": ["docs"],
            "false_negatives": ["memory"],
            "row_metrics": {
                "score_mode": "row-soft-exact",
                "row_symdiff": 2,
                "expected_topic_count": 1,
                "actual_topic_count": 1,
                "extra_detail": "not exposed",
            },
            "row_context": {"target": "openclaw/openclaw #123", "title": "not exposed"},
        },
        "surgical",
        include_row_identifiers=False,
    )

    assert row_profile["feedback_profile"] == "surgical"
    assert row_profile["scores"] == {
        "gepa_score": 0.5,
        "row_topic_f1": 0.67,
        "row_exact": 0.0,
        "row_jaccard": 0.5,
    }
    assert row_profile["row_metrics"] == {
        "score_mode": "row-soft-exact",
        "row_symdiff": 2,
        "expected_topic_count": 1,
        "actual_topic_count": 1,
    }
    assert "row_context" not in row_profile


def test_aggregate_scorer_populates_confusion_pairs(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    module = _load_runner(monkeypatch)
    input_path = tmp_path / "input.jsonl"
    output_path = tmp_path / "output.jsonl"
    input_path.write_text(
        '{"id": "1", "expected_topics": ["memory"], "title": "Memory fix"}\n',
        encoding="utf-8",
    )
    output_path.write_text(
        '{"id": "1", "result": "docs"}\n',
        encoding="utf-8",
    )

    report = module.score_output_against_input(
        input_path=input_path,
        output_path=output_path,
        allowed={"docs", "memory"},
        score_mode="row-soft-exact",
        policy="central routing policy",
        hygiene_penalty_weight=0.0,
        policy_char_budget=5000,
    )

    assert report["confusions"] == [
        {
            "missed_topic": "memory",
            "extra_topic": "docs",
            "count": 1,
            "diagnosis": "same-row false negative and false positive co-occurred",
            "suggested_mutation": (
                "Clarify the boundary between `memory` and `docs` only if this pair reflects "
                "a reusable ownership distinction."
            ),
        }
    ]
