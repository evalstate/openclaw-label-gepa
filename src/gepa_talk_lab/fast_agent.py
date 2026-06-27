"""fast-agent helpers for GEPA Single-Task Search examples."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fast_agent.batch import BatchRunResult, BatchRunner
from fast_agent.eval import ArtifactRun, CandidateRun
from fast_agent.integrations.gepa import FastAgentBatchEvaluator
from fast_agent.utils.async_utils import run_coroutine


SingleTaskScorer = Any


@dataclass(frozen=True)
class SingleTaskSpec:
    """A single task rendered as one fast-agent batch row."""

    id: str
    task: str
    metadata: Mapping[str, Any] | None = None

    def row(self) -> dict[str, Any]:
        return {"id": self.id, "task": self.task, **dict(self.metadata or {})}


class FastAgentSingleTaskEvaluator:
    """GEPA Single-Task Search evaluator backed by fast-agent.

    GEPA Single-Task Search means ``optimize_anything`` is called without a
    GEPA dataset or valset. This helper still uses fast-agent's existing batch
    execution path internally, but writes/runs exactly one JSONL row so examples
    can say what they mean:

        candidate -> fast-agent task run -> one score + ASI

    The wrapped object is a normal ``FastAgentBatchEvaluator`` and can be
    accessed through ``.batch_evaluator`` for debugging.
    """

    def __init__(
        self,
        *,
        task: SingleTaskSpec | Mapping[str, Any] | str,
        task_input_path: str | Path,
        env_dir: str | Path | None,
        agent_card: str | Path,
        candidate_variables: Mapping[str, str],
        scorer: SingleTaskScorer,
        run_dir: str | Path,
        agent: str | None = None,
        model: str | None = None,
        template: str = "{{task}}",
        parallel: int | None = 1,
        backend: str = "process",
        include_input: bool = True,
    ) -> None:
        self.task_input_path = Path(task_input_path)
        self.task_row = normalize_task(task)
        write_single_task_jsonl(self.task_input_path, self.task_row)
        self.batch_evaluator = FastAgentBatchEvaluator(
            env_dir=env_dir,
            agent_card=agent_card,
            agent=agent,
            candidate_variables=candidate_variables,
            input=self.task_input_path,
            template=template,
            model=model,
            parallel=parallel,
            scorer=scorer,
            run_dir=run_dir,
            backend=backend,  # type: ignore[arg-type]
            include_input=include_input,
        )

    def __call__(self, candidate: Mapping[str, str]) -> tuple[float, Any]:
        return self.batch_evaluator(candidate)


class FastAgentSingleTaskPromptEvaluator:
    """GEPA Single-Task Search evaluator where GEPA optimizes the user task.

    This is the simplest presentation-friendly form:

    - the fast-agent AgentCard is static and ordinary;
    - GEPA candidate text is written into the single row's ``task`` field;
    - fast-agent receives that task as the row prompt;
    - the scorer returns one aggregate score + ASI;
    - GEPA reflects on the ASI and updates the task text.

    Use this when you want to demonstrate prompt optimization directly, before
    introducing multi-component candidates or AgentCard variables.
    """

    def __init__(
        self,
        *,
        base_row: SingleTaskSpec | Mapping[str, Any] | str,
        task_candidate_key: str,
        env_dir: str | Path | None,
        agent_card: str | Path,
        scorer: SingleTaskScorer,
        run_dir: str | Path,
        agent: str | None = None,
        model: str | None = None,
        template: str = "{{task}}",
        parallel: int | None = 1,
        backend: str = "process",
        include_input: bool = True,
    ) -> None:
        self.base_row = normalize_task(base_row)
        self.task_candidate_key = task_candidate_key
        self.env_dir = Path(env_dir) if env_dir is not None else None
        self.agent_card = agent_card
        self.agent = agent
        self.model = model
        self.template = template
        self.parallel = parallel
        self.backend = backend
        self.include_input = include_input
        self.scorer = scorer
        self.run = ArtifactRun(run_dir)

    def __call__(self, candidate: Mapping[str, str]) -> tuple[float, Any]:
        candidate_run = self.run.candidate()
        candidate_run.materialize_candidate(candidate)
        task = candidate[self.task_candidate_key]
        input_path = candidate_run.path / "single-task-input.jsonl"
        row = {**self.base_row, "task": task}
        write_single_task_jsonl(input_path, row)
        candidate_run.write_json("input-row.json", row)
        result = run_coroutine(self._run_fast_agent(candidate_run, input_path))
        score_result = self.scorer(result, candidate, candidate_run)
        if len(score_result) == 2:
            score, side_info = score_result
            metadata: Mapping[str, Any] = {}
        else:
            score, side_info, metadata = score_result
        candidate_run.write_score(score, side_info, metadata=metadata)
        return score, side_info

    async def _run_fast_agent(self, candidate_run: CandidateRun, input_path: Path) -> BatchRunResult:
        runner = BatchRunner(env_dir=self.env_dir, backend=self.backend)  # type: ignore[arg-type]
        return await runner.run(
            input=input_path,
            output_path=candidate_run.path / "results.jsonl",
            agent_card=self.agent_card,
            agent=self.agent,
            template=self.template,
            model=self.model,
            parallel=self.parallel,
            include_input=self.include_input,
            summary_path=candidate_run.path / "batch-summary.json",
            telemetry_path=candidate_run.path / "telemetry.jsonl",
            overwrite=True,
        )


def normalize_task(task: SingleTaskSpec | Mapping[str, Any] | str) -> dict[str, Any]:
    if isinstance(task, SingleTaskSpec):
        return task.row()
    if isinstance(task, str):
        return {"id": "single-task", "task": task}
    row = dict(task)
    row.setdefault("id", "single-task")
    if "task" not in row:
        raise ValueError("single-task row must include a 'task' field")
    return row


def write_single_task_jsonl(path: Path, row: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(row), ensure_ascii=False) + "\n", encoding="utf-8")


def single_row_text(result: BatchRunResult) -> str:
    """Return the text output for the single row in a fast-agent batch result."""

    from fast_agent.batch import extract_text_output

    if len(result.rows) != 1:
        raise ValueError(f"single-task evaluator expected one result row, got {len(result.rows)}")
    return extract_text_output(result.rows[0])


def candidate_iteration(candidate_run: CandidateRun) -> int:
    return (candidate_run.index or 1) - 1
