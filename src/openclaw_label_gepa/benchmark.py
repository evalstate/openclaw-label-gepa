from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Any

from openclaw_label_gepa.jsonl import read_jsonl
from openclaw_label_gepa.label_order import normalize_labels
from openclaw_label_gepa.outputs import parse_output, row_id
from openclaw_label_gepa.scoring import LabelScore, score_labels

if TYPE_CHECKING:
    from pathlib import Path

    from openclaw_label_gepa.regimes import Regime


@dataclass(frozen=True)
class RowResult:
    id: str
    expected: list[str]
    predicted: list[str]
    false_positives: list[str]
    false_negatives: list[str]
    invalid_labels: list[str]
    valid_contract: bool
    exact: bool
    jaccard: float


@dataclass(frozen=True)
class BenchmarkReport:
    regime: str
    split: str
    output_path: str
    score: LabelScore
    valid_contract_rate: float
    missing_output_rows: list[str]
    extra_output_rows: list[str]
    invalid_label_counts: dict[str, int]
    false_positive_counts: dict[str, int]
    false_negative_counts: dict[str, int]
    row_results: list[RowResult]

    def to_dict(self) -> dict[str, Any]:
        return {
            "regime": self.regime,
            "split": self.split,
            "output_path": self.output_path,
            "scores": asdict(self.score),
            "valid_contract_rate": self.valid_contract_rate,
            "missing_output_rows": self.missing_output_rows,
            "extra_output_rows": self.extra_output_rows,
            "invalid_label_counts": self.invalid_label_counts,
            "false_positive_counts": self.false_positive_counts,
            "false_negative_counts": self.false_negative_counts,
            "row_results": [asdict(row) for row in self.row_results],
        }

    def write_json(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False) + "\n")


def _row_jaccard(expected: set[str], predicted: set[str]) -> float:
    if not expected and not predicted:
        return 1.0
    return len(expected & predicted) / len(expected | predicted)


def _split_rows(regime: Regime, split: str) -> list[dict[str, object]]:
    if split == "train":
        return regime.load_train().rows
    if split == "benchmark" and regime.benchmark_path is not None:
        return read_jsonl(regime.benchmark_path)
    msg = f"unsupported or unavailable split: {split}"
    raise ValueError(msg)


def score_output_file(
    regime: Regime,
    output_path: Path,
    *,
    split: str = "train",
) -> BenchmarkReport:
    label_order = regime.label_order
    expected_rows = _split_rows(regime, split)
    output_rows = read_jsonl(output_path)
    outputs_by_id = {
        rid: row
        for row in output_rows
        if (rid := row_id(row)) is not None
    }
    expected_ids = [
        str(row["id"])
        for row in expected_rows
        if isinstance(row.get("id"), str)
    ]
    missing = [rid for rid in expected_ids if rid not in outputs_by_id]
    extra = sorted(set(outputs_by_id) - set(expected_ids))

    expected_labels: list[list[str]] = []
    predicted_labels: list[list[str]] = []
    row_results: list[RowResult] = []
    invalid_counts: Counter[str] = Counter()
    fp_counts: Counter[str] = Counter()
    fn_counts: Counter[str] = Counter()
    valid_contracts = 0

    for expected_row in expected_rows:
        rid = str(expected_row["id"])
        expected = normalize_labels(expected_row.get("expected_topics"), label_order)
        parsed = parse_output(outputs_by_id.get(rid, {}), label_order)
        predicted = parsed.labels
        expected_set = set(expected)
        predicted_set = set(predicted)
        false_positives = normalize_labels(list(predicted_set - expected_set), label_order)
        false_negatives = normalize_labels(list(expected_set - predicted_set), label_order)
        invalid_counts.update(parsed.invalid_labels)
        fp_counts.update(false_positives)
        fn_counts.update(false_negatives)
        valid_contracts += int(parsed.valid_contract)
        expected_labels.append(expected)
        predicted_labels.append(predicted)
        row_results.append(
            RowResult(
                id=rid,
                expected=expected,
                predicted=predicted,
                false_positives=false_positives,
                false_negatives=false_negatives,
                invalid_labels=parsed.invalid_labels,
                valid_contract=parsed.valid_contract,
                exact=expected == predicted and parsed.valid_contract,
                jaccard=_row_jaccard(expected_set, predicted_set),
            )
        )

    score = score_labels(expected_labels, predicted_labels)
    return BenchmarkReport(
        regime=regime.name,
        split=split,
        output_path=str(output_path),
        score=score,
        valid_contract_rate=valid_contracts / len(expected_rows) if expected_rows else 0.0,
        missing_output_rows=missing,
        extra_output_rows=extra,
        invalid_label_counts=dict(sorted(invalid_counts.items())),
        false_positive_counts=dict(sorted(fp_counts.items())),
        false_negative_counts=dict(sorted(fn_counts.items())),
        row_results=row_results,
    )
