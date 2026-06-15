from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from openclaw_label_gepa.jsonl import read_jsonl
from openclaw_label_gepa.label_order import normalize_labels

if TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True)
class DatasetRows:
    rows: list[dict[str, object]]
    expected_topics: list[list[str]]


def load_local_split(path: Path, label_order: list[str]) -> DatasetRows:
    rows = read_jsonl(path)
    expected = []
    for row in rows:
        labels = row.get("expected_topics")
        if labels is None:
            labels = row.get("labels")
        expected.append(normalize_labels(labels, label_order))
    return DatasetRows(rows=rows, expected_topics=expected)
