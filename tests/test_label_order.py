from __future__ import annotations

from typing import TYPE_CHECKING

from openclaw_label_gepa.label_order import labels_are_ordered, load_label_order, normalize_labels

if TYPE_CHECKING:
    from pathlib import Path


def test_normalize_labels_uses_priority_order() -> None:
    order = ["inference_api", "gateway", "docs", "reliability"]

    assert normalize_labels(["docs", "gateway", "docs"], order) == ["gateway", "docs"]
    assert labels_are_ordered(["gateway", "docs"], order)
    assert not labels_are_ordered(["docs", "gateway"], order)


def test_load_label_order_from_markdown(tmp_path: Path) -> None:
    path = tmp_path / "allowed.md"
    path.write_text('```json\n["a", "b"]\n```\n', encoding="utf-8")

    assert load_label_order(path) == ["a", "b"]
