from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LabelScore:
    topic_micro_precision: float
    topic_micro_recall: float
    topic_micro_f1: float
    topic_macro_f1: float
    row_exact_accuracy: float
    avg_row_jaccard: float
    rows: int


def f1(precision: float, recall: float) -> float:
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def jaccard(expected: set[str], predicted: set[str]) -> float:
    if not expected and not predicted:
        return 1.0
    return len(expected & predicted) / len(expected | predicted)


def score_labels(expected_rows: list[list[str]], predicted_rows: list[list[str]]) -> LabelScore:
    if len(expected_rows) != len(predicted_rows):
        msg = "expected_rows and predicted_rows must have the same length"
        raise ValueError(msg)
    if not expected_rows:
        return LabelScore(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0)

    all_labels = sorted({label for row in expected_rows + predicted_rows for label in row})
    tp = fp = fn = 0
    per_label_f1 = []
    exact = 0
    total_jaccard = 0.0
    row_pairs = list(zip(expected_rows, predicted_rows, strict=True))

    for expected_list, predicted_list in row_pairs:
        expected = set(expected_list)
        predicted = set(predicted_list)
        tp += len(expected & predicted)
        fp += len(predicted - expected)
        fn += len(expected - predicted)
        exact += int(expected == predicted)
        total_jaccard += jaccard(expected, predicted)

    for label in all_labels:
        label_tp = sum(label in exp and label in pred for exp, pred in row_pairs)
        label_fp = sum(label not in exp and label in pred for exp, pred in row_pairs)
        label_fn = sum(label in exp and label not in pred for exp, pred in row_pairs)
        precision = label_tp / (label_tp + label_fp) if label_tp + label_fp else 0.0
        recall = label_tp / (label_tp + label_fn) if label_tp + label_fn else 0.0
        per_label_f1.append(f1(precision, recall))

    micro_precision = tp / (tp + fp) if tp + fp else 0.0
    micro_recall = tp / (tp + fn) if tp + fn else 0.0
    rows = len(expected_rows)
    return LabelScore(
        topic_micro_precision=micro_precision,
        topic_micro_recall=micro_recall,
        topic_micro_f1=f1(micro_precision, micro_recall),
        topic_macro_f1=sum(per_label_f1) / len(per_label_f1) if per_label_f1 else 0.0,
        row_exact_accuracy=exact / rows,
        avg_row_jaccard=total_jaccard / rows,
        rows=rows,
    )
