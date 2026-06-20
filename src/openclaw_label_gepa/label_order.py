from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path


TOPIC_BLOCK_RE = re.compile(r"```json\n(.*?)\n```", re.S)
TOPIC_BULLET_RE = re.compile(r"^-\s+`([a-z][a-z0-9_]*)`(?::|\s*$)", re.M)


def load_label_order(path: Path) -> list[str]:
    if path.suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        labels = payload["properties"]["labels"]["items"]["enum"]
        return [label for label in labels if isinstance(label, str)]

    text = path.read_text(encoding="utf-8")
    match = TOPIC_BLOCK_RE.search(text)
    if match is not None:
        labels = json.loads(match.group(1))
        return [label for label in labels if isinstance(label, str)]
    topic_list_text = text.split("## Topic definitions", 1)[0]
    labels = TOPIC_BULLET_RE.findall(topic_list_text)
    if labels:
        return labels
    labels = TOPIC_BULLET_RE.findall(text)
    if labels:
        return labels
    msg = f"could not find topic list in {path}"
    raise ValueError(msg)


def normalize_labels(labels: Any, order: list[str]) -> list[str]:
    if not isinstance(labels, list):
        return []
    rank = {label: index for index, label in enumerate(order)}
    unique = []
    seen: set[str] = set()
    for label in labels:
        if isinstance(label, str) and label not in seen:
            unique.append(label)
            seen.add(label)
    return sorted(unique, key=lambda label: rank.get(label, len(rank)))


def labels_are_ordered(labels: Any, order: list[str]) -> bool:
    return labels == normalize_labels(labels, order)
