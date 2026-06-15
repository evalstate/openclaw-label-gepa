from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from openclaw_label_gepa.label_order import normalize_labels


@dataclass(frozen=True)
class ParsedOutput:
    labels: list[str]
    invalid_labels: list[str]
    valid_contract: bool
    raw_text: str


def extract_result(row: dict[str, Any]) -> dict[str, Any]:
    for key in ("result", "output", "response", "structured_output"):
        value = row.get(key)
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                return parsed
    return {}


def extract_output_text(row: dict[str, Any]) -> str:
    for key in ("result", "output", "response", "structured_output"):
        value = row.get(key)
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            return json.dumps(value, ensure_ascii=False)
    return ""


def parse_label_text(text: str, label_order: list[str]) -> list[str]:
    allowed = set(label_order)
    text = text.strip()
    if not text:
        return []

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        parsed = None

    if isinstance(parsed, dict):
        value = parsed.get("topics_of_interest", parsed.get("labels", []))
        return normalize_labels(value, label_order)
    if isinstance(parsed, list):
        return normalize_labels(parsed, label_order)

    label_line = text
    for line in text.splitlines():
        if re.match(r"^\s*(labels|topics_of_interest|topics)\s*:", line, re.I):
            label_line = line.split(":", 1)[1]
            break
    found = re.findall(r"[a-z][a-z0-9_]*", label_line.lower())
    return normalize_labels([label for label in found if label in allowed], label_order)


def parse_output(row: dict[str, Any], label_order: list[str]) -> ParsedOutput:
    allowed = set(label_order)
    result = extract_result(row)
    raw_text = extract_output_text(row)
    raw_labels = result.get("topics_of_interest", result.get("labels"))
    structured = isinstance(raw_labels, list)
    label_values = raw_labels if structured else parse_label_text(raw_text, label_order)

    invalid = [
        label
        for label in label_values
        if not isinstance(label, str) or label not in allowed
    ]
    labels = normalize_labels(label_values, label_order)
    has_output = structured or bool(raw_text.strip())
    return ParsedOutput(
        labels=labels,
        invalid_labels=[str(label) for label in invalid],
        valid_contract=has_output and not invalid,
        raw_text=raw_text,
    )


def row_id(row: dict[str, Any]) -> str | None:
    input_row = row.get("input")
    if isinstance(input_row, dict) and isinstance(input_row.get("id"), str):
        return input_row["id"]
    if isinstance(row.get("id"), str):
        return row["id"]
    result = extract_result(row)
    if isinstance(result.get("id"), str):
        return result["id"]
    return None
