"""Small Trackio conveniences for GEPA talk examples."""

from __future__ import annotations

import os
import shlex
import sys
from argparse import Namespace
from pathlib import Path
from typing import Any, Mapping

from fast_agent.integrations.gepa import gepa_trackio_init_kwargs


def jsonable_args(args: Namespace) -> dict[str, Any]:
    return {key: str(value) if isinstance(value, Path) else value for key, value in vars(args).items()}


def trackio_show_command(*, trackio_dir: Path, project: str) -> str:
    return (
        f"TRACKIO_DIR={shlex.quote(str(trackio_dir.resolve()))} "
        f"uv run trackio show --project {shlex.quote(project)}"
    )


def init_trackio(
    *,
    project: str,
    name: str,
    group: str | None,
    trackio_dir: Path,
    config: Mapping[str, Any],
    enabled: bool = True,
) -> bool:
    if not enabled:
        return False
    os.environ.setdefault("TRACKIO_DIR", str(trackio_dir.resolve()))
    try:
        import trackio
    except ImportError:
        print("Trackio is not installed; continuing without Trackio.", file=sys.stderr)
        return False
    trackio.init(
        **gepa_trackio_init_kwargs(
            project=project,
            name=name,
            group=group,
            config=config,
        )
    )
    print(f"Trackio: {trackio_show_command(trackio_dir=trackio_dir, project=project)}")
    return True


def finish_trackio(enabled: bool) -> None:
    if not enabled:
        return
    try:
        import trackio

        trackio.finish()
    except Exception as exc:  # noqa: BLE001
        print(f"Trackio finish failed: {exc}", file=sys.stderr)
