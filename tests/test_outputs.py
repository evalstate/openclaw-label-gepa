from openclaw_label_gepa.outputs import (
    parse_label_text,
    parse_output,
    row_id,
)

ORDER = ["inference_api", "gateway", "docs", "reliability"]


def test_parse_plain_label_text() -> None:
    assert parse_label_text("labels: docs, gateway", ORDER) == ["gateway", "docs"]


def test_parse_json_label_text() -> None:
    assert parse_label_text('{"labels": ["docs", "gateway"]}', ORDER) == ["gateway", "docs"]


def test_parse_fast_agent_row() -> None:
    row = {
        "input": {"id": "row-1"},
        "result": {"topics_of_interest": ["docs", "gateway"]},
    }

    parsed = parse_output(row, ORDER)

    assert row_id(row) == "row-1"
    assert parsed.labels == ["gateway", "docs"]
    assert parsed.valid_contract
