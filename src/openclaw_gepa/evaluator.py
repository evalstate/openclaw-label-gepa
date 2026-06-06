from __future__ import annotations

import json
import subprocess
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class EvalPaths:
    root: Path
    env_dir: Path
    input_path: Path
    task_template: Path
    smoke_template: Path
    schema_path: Path


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            value = json.loads(line)
            if isinstance(value, dict):
                rows.append(value)
    return rows


def next_candidate_dir(run_dir: Path) -> tuple[int, Path]:
    index = 1
    while (run_dir / f"candidate-{index:04d}").exists():
        index += 1
    path = run_dir / f"candidate-{index:04d}"
    path.mkdir(parents=True, exist_ok=True)
    return index, path


def _jsonish(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return {}
        return parsed if isinstance(parsed, dict) else {}
    return {}


def _extract_result(row: dict[str, Any]) -> dict[str, Any]:
    for key in ("result", "output", "response", "structured_output"):
        result = _jsonish(row.get(key))
        if result:
            return result
    return {}


def run_fast_agent_batch(
    *,
    candidate: dict[str, str],
    candidate_dir: Path,
    paths: EvalPaths,
    model: str,
    fast_agent_bin: str,
    parallel: int,
) -> Path:
    instruction_path = candidate_dir / "instructions.md"
    output_path = candidate_dir / "results.jsonl"
    summary_path = candidate_dir / "summary.json"
    telemetry_path = candidate_dir / "telemetry.jsonl"
    instruction_path.write_text(candidate["instructions"], encoding="utf-8")

    template = paths.smoke_template if model == "passthrough" else paths.task_template
    cmd = [
        fast_agent_bin,
        "--no-update-check",
        "--env",
        str(paths.env_dir),
        "batch",
        "run",
        "--input",
        str(paths.input_path),
        "--output",
        str(output_path),
        "--instruction",
        str(instruction_path),
        "--template",
        str(template),
        "--json-schema",
        str(paths.schema_path),
        "--model",
        model,
        "--id-field",
        "id",
        "--include-input",
        "--summary-output",
        str(summary_path),
        "--telemetry-output",
        str(telemetry_path),
        "--parallel",
        str(parallel),
        "--overwrite",
        "--no-final-summary",
    ]
    proc = subprocess.run(cmd, cwd=paths.root, text=True, capture_output=True, check=False)
    (candidate_dir / "command.json").write_text(json.dumps(cmd, indent=2), encoding="utf-8")
    (candidate_dir / "batch.stdout.txt").write_text(proc.stdout, encoding="utf-8")
    (candidate_dir / "batch.stderr.txt").write_text(proc.stderr, encoding="utf-8")
    if proc.returncode:
        raise RuntimeError(f"fast-agent batch failed with exit {proc.returncode}\n{proc.stderr[-2000:]}")
    return output_path


def score_results(output_path: Path) -> tuple[float, dict[str, Any]]:
    rows = load_jsonl(output_path)
    failures: list[dict[str, Any]] = []
    confusion: Counter[tuple[str | None, str | None]] = Counter()
    ok = 0
    valid_json = 0

    for row in rows:
        source = row.get("input") if isinstance(row.get("input"), dict) else row
        result = _extract_result(row)
        expected = source.get("expected")
        actual = result.get("category")
        row_ok = row.get("ok") is not False and bool(result)
        if row_ok:
            valid_json += 1
        if row_ok and actual == expected:
            ok += 1
            continue

        confusion[(expected, actual)] += 1
        failures.append(
            {
                "id": row.get("id") or source.get("id"),
                "type": "wrong_label" if actual else "missing_or_invalid_output",
                "expected": expected,
                "actual": actual,
                "request": source.get("text"),
                "evidence": result.get("rationale") or row.get("error") or "No usable rationale/result was returned.",
            }
        )

    total = max(1, len(rows))
    accuracy = ok / total
    valid_json_rate = valid_json / total
    diagnostic_coverage = _diagnostic_coverage(failures)
    actionable_feedback = summarize_failures(failures, confusion)
    asi_score = (diagnostic_coverage + (1.0 if actionable_feedback else 0.0)) / 2.0

    side_info = {
        "scores": {
            "gepa_score": accuracy,
            "accuracy": accuracy,
            "valid_json": valid_json_rate,
            "failure_count": len(failures),
            "asi_score": asi_score,
            "asi_diagnostic_coverage": diagnostic_coverage,
        },
        "failures": failures[:25],
        "confusion": {f"{expected}->{actual}": count for (expected, actual), count in confusion.items()},
        "actionable_feedback": actionable_feedback,
    }
    return accuracy, side_info


def _diagnostic_coverage(failures: list[dict[str, Any]]) -> float:
    if not failures:
        return 1.0
    required = ("id", "expected", "actual", "request", "evidence")
    covered = 0
    for failure in failures:
        covered += sum(1 for key in required if failure.get(key)) / len(required)
    return covered / len(failures)


def summarize_failures(
    failures: list[dict[str, Any]],
    confusion: Counter[tuple[str | None, str | None]] | None = None,
) -> list[str]:
    if not failures:
        return ["All rows passed. Preserve the current category boundaries and JSON schema."]

    hints: list[str] = []
    if confusion:
        for (expected, actual), count in confusion.most_common(3):
            hints.append(f"Boundary issue: {count} row(s) expected {expected!r} but returned {actual!r}.")
    for failure in failures[:8]:
        hints.append(
            "Row {id}: expected {expected}, got {actual}. Request: {request}. Evidence: {evidence}".format(
                id=failure.get("id"),
                expected=failure.get("expected"),
                actual=failure.get("actual"),
                request=failure.get("request"),
                evidence=failure.get("evidence"),
            )
        )
    hints.append("Keep output schema unchanged; improve only the optimized instruction text unless the benchmark changes.")
    return hints


def safe_trackio_log(payload: dict[str, Any], *, step: int | None = None) -> None:
    try:
        import trackio

        trackio.log(payload, step=step)
    except Exception:
        return


def log_candidate_to_trackio(candidate_idx: int, candidate_dir: Path, score: float, side_info: dict[str, Any]) -> None:
    try:
        import trackio

        program_idx = candidate_idx - 1
        scores = side_info.get("scores", {}) if isinstance(side_info.get("scores"), dict) else {}
        metrics = {f"eval/{key}": value for key, value in scores.items() if isinstance(value, int | float)}
        metrics["eval/local_candidate_idx"] = candidate_idx
        metrics["eval/program_idx"] = program_idx
        metrics["gepa/iteration"] = program_idx
        trackio.log(metrics)

        trackio.log(
            {
                "gepa/iteration": program_idx,
                "eval/candidates": trackio.Table(
                    columns=["candidate_idx", "score", "candidate_dir", "failure_count", "asi_score"],
                    data=[
                        [
                            program_idx,
                            score,
                            str(candidate_dir),
                            scores.get("failure_count"),
                            scores.get("asi_score"),
                        ]
                    ],
                )
            },
        )

        failures = side_info.get("failures", [])
        if failures:
            trackio.log(
                {
                    "gepa/iteration": program_idx,
                    "asi/failures": trackio.Table(
                        columns=["candidate_idx", "id", "type", "expected", "actual", "request", "evidence"],
                        data=[
                            [
                                program_idx,
                                f.get("id"),
                                f.get("type"),
                                f.get("expected"),
                                f.get("actual"),
                                f.get("request"),
                                f.get("evidence"),
                            ]
                            for f in failures
                        ],
                    )
                }
            )
    except Exception:
        return


def build_evaluator(
    *,
    run_dir: Path,
    paths: EvalPaths,
    model: str,
    fast_agent_bin: str,
    parallel: int,
):
    def evaluate(candidate: dict[str, str]) -> tuple[float, dict[str, Any]]:
        candidate_idx, candidate_dir = next_candidate_dir(run_dir)
        (candidate_dir / "candidate.json").write_text(json.dumps(candidate, indent=2), encoding="utf-8")
        output_path = run_fast_agent_batch(
            candidate=candidate,
            candidate_dir=candidate_dir,
            paths=paths,
            model=model,
            fast_agent_bin=fast_agent_bin,
            parallel=parallel,
        )
        score, side_info = score_results(output_path)
        side_info["candidate_idx"] = candidate_idx
        side_info["candidate_dir"] = str(candidate_dir)
        side_info["result_jsonl"] = str(output_path)
        (candidate_dir / "score.json").write_text(json.dumps(side_info, indent=2), encoding="utf-8")
        log_candidate_to_trackio(candidate_idx, candidate_dir, score, side_info)
        print(f"candidate-{candidate_idx:04d}: score={score:.3f} asi={side_info['scores']['asi_score']:.3f}")
        return score, side_info

    return evaluate
