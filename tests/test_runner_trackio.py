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
    path = Path("tools/runners/openclaw-gepa-runner.py")
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
