from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from openclaw_label_gepa.datasets import DatasetRows, load_local_split
from openclaw_label_gepa.label_order import load_label_order


@dataclass(frozen=True)
class Regime:
    name: str
    root: Path
    label_order_path: Path
    base_prompt_path: Path
    task_template_path: Path | None
    schema_path: Path
    train_path: Path
    benchmark_path: Path | None
    metric: str
    raw: dict[str, Any]

    @property
    def label_order(self) -> list[str]:
        return load_label_order(self.label_order_path)

    def load_train(self) -> DatasetRows:
        return load_local_split(self.train_path, self.label_order)

    def path_value(self, key: str) -> Path | None:
        value = self.raw.get(key)
        return resolve_path(self.root, value) if isinstance(value, str) else None

    def split_path(self, key: str) -> Path | None:
        if key == "train":
            return self.train_path
        if key == "benchmark":
            return self.benchmark_path
        return self.path_value(f"{key}_split")

    def agent_card_path(self, variant: str) -> Path:
        cards = self.raw.get("agent_cards")
        if isinstance(cards, dict) and isinstance(cards.get(variant), str):
            return require_path(f"agent_cards.{variant}", resolve_path(self.root, cards[variant]))
        if variant == "plain":
            return self.base_prompt_path
        msg = f"regime {self.name} has no agent card for variant {variant!r}"
        raise ValueError(msg)

    def mapping(self, key: str) -> dict[str, Any]:
        value = self.raw.get(key)
        return value if isinstance(value, dict) else {}


def resolve_path(root: Path, value: str | None) -> Path | None:
    if value is None:
        return None
    path = Path(value)
    return path if path.is_absolute() else root / path


def require_path(field: str, path: Path | None) -> Path:
    if path is None:
        msg = f"regime missing required path: {field}"
        raise ValueError(msg)
    return path


def load_regime(path: Path) -> Regime:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        msg = f"regime file must contain a mapping: {path}"
        raise ValueError(msg)
    root = path.parent
    name = raw.get("name")
    if not isinstance(name, str):
        msg = "regime requires a string name"
        raise ValueError(msg)
    label_order_path = resolve_path(root, raw.get("label_order"))
    base_prompt_path = resolve_path(root, raw.get("base_prompt"))
    task_template_path = resolve_path(root, raw.get("task_template"))
    schema_path = resolve_path(root, raw.get("schema"))
    train_path = resolve_path(root, raw.get("train_split"))
    benchmark_path = resolve_path(root, raw.get("benchmark_split"))
    required = {
        "label_order": label_order_path,
        "base_prompt": base_prompt_path,
        "schema": schema_path,
        "train_split": train_path,
    }
    missing = [field for field, field_path in required.items() if field_path is None]
    if missing:
        msg = f"regime missing required paths: {', '.join(missing)}"
        raise ValueError(msg)
    return Regime(
        name=name,
        root=root,
        label_order_path=require_path("label_order", label_order_path),
        base_prompt_path=require_path("base_prompt", base_prompt_path),
        task_template_path=task_template_path,
        schema_path=require_path("schema", schema_path),
        train_path=require_path("train_split", train_path),
        benchmark_path=benchmark_path,
        metric=str(raw.get("metric", "micro_f1")),
        raw=raw,
    )
