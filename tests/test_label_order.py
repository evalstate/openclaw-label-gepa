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


def test_load_label_order_from_plain_topic_bullets(tmp_path: Path) -> None:
    path = tmp_path / "allowed.md"
    path.write_text(
        "\n".join(
            [
                "## Allowed Topics",
                "",
                "- `inference_api`",
                "- `self_hosted_inference`",
                "- `tool_calling`",
                "",
                "## Topic definitions",
                "",
                "- `inference_api`: Provider API integration.",
            ]
        ),
        encoding="utf-8",
    )

    assert load_label_order(path) == [
        "inference_api",
        "self_hosted_inference",
        "tool_calling",
    ]


def test_load_label_order_from_definition_only_bullets(tmp_path: Path) -> None:
    path = tmp_path / "topics.md"
    path.write_text(
        "\n".join(
            [
                "## Topic List and Definitions",
                "",
                "Use only these topic IDs.",
                "",
                "- `inference_api`: Provider API integration.",
                "- `self_hosted_inference`: Local inference engines.",
                "- `tool_calling`: Model tool-call protocol.",
            ]
        ),
        encoding="utf-8",
    )

    assert load_label_order(path) == [
        "inference_api",
        "self_hosted_inference",
        "tool_calling",
    ]
