from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path


TOPIC_BLOCK_RE = re.compile(r"```json\n(.*?)\n```", re.S)


def load_label_order(path: Path) -> list[str]:
    if path.suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        labels = payload["properties"]["labels"]["items"]["enum"]
        return [label for label in labels if isinstance(label, str)]

    text = path.read_text(encoding="utf-8")
    match = TOPIC_BLOCK_RE.search(text)
    if match is None:
        msg = f"could not find JSON topic block in {path}"
        raise ValueError(msg)
    labels = json.loads(match.group(1))
    return [label for label in labels if isinstance(label, str)]


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
