from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


class FastAgentReflectionLM:
    """GEPA-compatible reflection LM backed by `fast-agent go`.

    GEPA calls this object with a reflection prompt. The wrapper writes each
    prompt/stdout/stderr to disk so reflection behavior is audit-friendly and
    uses the same fast-agent model aliases/config as the benchmark evaluator.
    """

    def __init__(
        self,
        *,
        model: str,
        run_dir: Path,
        env_dir: Path,
        fast_agent_bin: str = "fast-agent",
    ) -> None:
        self.model = model
        self.run_dir = run_dir
        self.env_dir = env_dir
        self.fast_agent_bin = fast_agent_bin
        self.count = 0
        self.total_cost = 0.0
        self.run_dir.mkdir(parents=True, exist_ok=True)

    def __call__(self, prompt: str | list[dict[str, Any]]) -> str:
        self.count += 1
        call_dir = self.run_dir / f"call-{self.count:04d}"
        call_dir.mkdir(parents=True, exist_ok=True)

        prompt_text = prompt if isinstance(prompt, str) else json.dumps(prompt, indent=2)
        prompt_path = call_dir / "prompt.md"
        prompt_path.write_text(prompt_text, encoding="utf-8")

        cmd = [
            self.fast_agent_bin,
            "--no-update-check",
            "--env",
            str(self.env_dir),
            "go",
            "--prompt-file",
            str(prompt_path),
            "--model",
            self.model,
            "--quiet",
        ]
        proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
        (call_dir / "command.json").write_text(json.dumps(cmd, indent=2), encoding="utf-8")
        (call_dir / "stdout.txt").write_text(proc.stdout, encoding="utf-8")
        (call_dir / "stderr.txt").write_text(proc.stderr, encoding="utf-8")
        if proc.returncode:
            raise RuntimeError(f"fast-agent reflection failed with exit {proc.returncode}: {proc.stderr[-2000:]}")
        return proc.stdout.strip()
