#!/usr/bin/env python3
from __future__ import annotations

import runpy
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BUILDER = ROOT / "tools/data-build/openclaw-v6n-feedback300.py"
OUTPUT = ROOT / "runs/data-build/splits/v6o-final-feedback300.jsonl"


def main() -> int:
    sys.argv = [
        str(BUILDER),
        "--regime",
        "v6o",
        "--output",
        str(OUTPUT),
        *sys.argv[1:],
    ]
    runpy.run_path(str(BUILDER), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
