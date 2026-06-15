import subprocess
from dataclasses import replace
from pathlib import Path
from typing import Any

from openclaw_label_gepa import cli
from openclaw_label_gepa.regimes import load_regime
from openclaw_label_gepa.runplan import build_run_plan


def test_shell_line_cd_to_project_root_and_uses_absolute_trackio_dir() -> None:
    regime = load_regime(Path("regimes/v7a/regime.yaml"))
    plan = build_run_plan(
        regime,
        model="gemma-e4",
        variant="plain",
        run_index=3,
        overrides={"max_metric_calls": 1600},
    )

    line = cli.shell_line(plan)

    assert line.startswith(f"cd {Path.cwd()} && TRACKIO_DIR={Path.cwd() / 'runs/v7a/trackio'}")
    assert "--max-metric-calls 1600" in line
    assert "--run-name gemma-e4-v7a-soft-exact-plain-compact-mb15-mc1600-003" in line
    assert "--reflection-env-dir .fast-agent" in line


def test_shell_line_can_append_runner_preflight_flag() -> None:
    regime = load_regime(Path("regimes/v7a/regime.yaml"))
    plan = build_run_plan(regime, model="gemma-e4", variant="plain")

    line = cli.shell_line(plan, extra_args=("--preflight-only",))

    assert line.endswith("--plain-labels --preflight-only")


def test_trackio_command_uses_regime_project_and_absolute_dir() -> None:
    regime = load_regime(Path("regimes/v7a/regime.yaml"))

    line = cli.trackio_shell_line(regime)

    assert line == (
        f"cd {Path.cwd()} && "
        f"BROWSER=/bin/true TRACKIO_DIR={Path.cwd() / 'runs/v7a/trackio'} "
        "uv run trackio show --project easy-v7a-plain-gepa"
    )


def test_validate_regime_accepts_v7a() -> None:
    regime = load_regime(Path("regimes/v7a/regime.yaml"))

    assert cli.validate_regime(regime) == []


def test_default_regime_is_v7a() -> None:
    args = cli.parse_args(["--validate"])

    assert args.regime == Path("regimes/v7a/regime.yaml")


def test_list_regimes_prints_available_regimes(capsys: Any) -> None:
    status = cli.main(["--list-regimes"])

    out = capsys.readouterr().out
    assert status == 0
    assert '"name": "v7a"' in out
    assert '"default_variant": "plain"' in out
    assert '"benchmark_rows": 78' in out


def test_regime_info_prints_selected_regime(capsys: Any) -> None:
    status = cli.main(["regimes/v7a/regime.yaml", "--regime-info"])

    out = capsys.readouterr().out
    assert status == 0
    assert '"name": "v7a"' in out
    assert '"score_mode": "row-soft-exact"' in out
    assert '"trackio"' in out


def test_audit_stale_paths_allows_hygiene_assertions_only() -> None:
    check = cli._audit_stale_paths(Path.cwd())

    assert check.ok
    assert check.detail == "none"


def test_audit_prints_success_payload(monkeypatch: Any, capsys: Any) -> None:
    def fake_preflight(_regime: Any, *, benchmark: bool) -> cli.AuditCheck:
        return cli.AuditCheck(
            name="benchmark_preflight" if benchmark else "gepa_preflight",
            ok=True,
            detail="ok",
        )

    monkeypatch.setattr(cli, "_audit_runner_preflight", fake_preflight)

    status = cli.main(["--audit"])

    out = capsys.readouterr().out
    assert status == 0
    assert '"ok": true' in out
    assert '"name": "regimes"' in out
    assert '"name": "gepa_preflight"' in out


def test_validate_regime_accepts_plain_only_v6h() -> None:
    regime = load_regime(Path("regimes/v6h/regime.yaml"))

    problems = cli.validate_regime(regime)

    assert not [problem for problem in problems if "agent_cards.structured" in problem]


def test_doctor_flag_uses_default_regime() -> None:
    args = cli.parse_args(["--doctor"])

    assert args.doctor is True
    assert args.regime == Path("regimes/v7a/regime.yaml")


def test_run_flag_requires_action() -> None:
    args = cli.parse_args(["--run"])
    regime = load_regime(Path("regimes/v7a/regime.yaml"))

    try:
        cli.dispatch(args, regime, cli.regime_summary(regime))
    except SystemExit as exc:
        assert "--run requires" in str(exc)
    else:
        raise AssertionError("dispatch should reject --run without an executable action")


def test_run_and_shell_are_mutually_exclusive() -> None:
    args = cli.parse_args(["--plan-gepa", "--run", "--shell"])
    regime = load_regime(Path("regimes/v7a/regime.yaml"))

    try:
        cli.dispatch(args, regime, cli.regime_summary(regime))
    except SystemExit as exc:
        assert "--run and --shell" in str(exc)
    else:
        raise AssertionError("dispatch should reject --run --shell")


def test_run_gepa_preflight_executes_plan(monkeypatch: Any) -> None:
    calls: list[dict[str, Any]] = []

    def fake_run(command: list[str], *, cwd: Path, env: dict[str, str], check: bool) -> Any:
        calls.append({"command": command, "cwd": cwd, "env": env, "check": check})
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(cli.subprocess, "run", fake_run)
    args = cli.parse_args(
        [
            "--plan-gepa",
            "--model",
            "gemma-e4",
            "--max-metric-calls",
            "1600",
            "--run-index",
            "3",
            "--runner-preflight",
            "--run",
        ]
    )
    regime = load_regime(Path("regimes/v7a/regime.yaml"))

    status = cli.dispatch(args, regime, cli.regime_summary(regime))

    assert status == 0
    assert len(calls) == 1
    assert calls[0]["cwd"] == Path.cwd()
    assert calls[0]["env"]["TRACKIO_DIR"] == str(Path.cwd() / "runs/v7a/trackio")
    assert calls[0]["check"] is False
    assert calls[0]["command"][-1] == "--preflight-only"
    assert "--max-metric-calls" in calls[0]["command"]
    assert "1600" in calls[0]["command"]


def test_trackio_command_can_execute(monkeypatch: Any) -> None:
    calls: list[dict[str, Any]] = []

    def fake_run(command: list[str], *, cwd: Path, env: dict[str, str], check: bool) -> Any:
        calls.append({"command": command, "cwd": cwd, "env": env, "check": check})
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(cli.subprocess, "run", fake_run)
    args = cli.parse_args(["--trackio-command", "--run"])
    regime = load_regime(Path("regimes/v7a/regime.yaml"))

    status = cli.dispatch(args, regime, cli.regime_summary(regime))

    assert status == 0
    assert len(calls) == 1
    assert calls[0]["command"] == [
        "uv",
        "run",
        "trackio",
        "show",
        "--project",
        "easy-v7a-plain-gepa",
    ]
    assert calls[0]["cwd"] == Path.cwd()
    assert calls[0]["check"] is False
    assert calls[0]["env"]["TRACKIO_DIR"] == str(Path.cwd() / "runs/v7a/trackio")
    assert calls[0]["env"]["BROWSER"] == "/bin/true"


def test_run_command_handles_keyboard_interrupt(monkeypatch: Any, capsys: Any) -> None:
    def fake_run(*_args: Any, **_kwargs: Any) -> Any:
        raise KeyboardInterrupt

    monkeypatch.setattr(cli.subprocess, "run", fake_run)

    status = cli._run_command(
        ["uv", "run", "trackio", "show"],
        project_root=Path.cwd(),
        trackio_dir=Path.cwd() / "runs/v7a/trackio",
    )

    assert status == 130
    assert "interrupted" in capsys.readouterr().out


def test_doctor_venv_warns_for_foreign_virtualenv(tmp_path: Path) -> None:
    project = tmp_path / "project"
    other = tmp_path / "other" / ".venv"
    project.mkdir()

    warnings = cli._doctor_venv(project, {"VIRTUAL_ENV": str(other)})

    assert len(warnings) == 1
    assert "VIRTUAL_ENV points outside this repo" in warnings[0]


def test_doctor_editable_sources_reports_missing_path(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    (project / "pyproject.toml").write_text(
        """
[tool.uv.sources]
fast-agent-mcp = { path = "../missing-fast-agent", editable = true }
""".strip(),
        encoding="utf-8",
    )

    errors = cli._doctor_editable_sources(project)

    assert len(errors) == 1
    assert "editable dependency 'fast-agent-mcp' path does not exist" in errors[0]


def test_prompt_placeholder_validation_reports_missing_file(tmp_path: Path) -> None:
    regime = load_regime(Path("regimes/v7a/regime.yaml"))
    project = tmp_path / "project"
    regime_root = project / "regimes" / "bad"
    prompt = regime_root / "prompts" / "labeler.md"
    prompt.parent.mkdir(parents=True)
    prompt.write_text("{{file:regimes/bad/prompts/missing.md}}\n", encoding="utf-8")
    bad_regime = replace(regime, root=regime_root, base_prompt_path=prompt)

    problems = cli._validate_prompt_placeholders(bad_regime)

    assert len(problems) == 1
    assert "missing file placeholder" in problems[0]
    assert "missing.md" in problems[0]


def test_reflection_agent_validation_reports_missing_card(tmp_path: Path) -> None:
    regime = load_regime(Path("regimes/v7a/regime.yaml"))
    project = tmp_path / "project"
    regime_root = project / "regimes" / "bad"
    (project / ".fast-agent").mkdir(parents=True)
    (project / ".fast-agent" / "fast-agent.yaml").write_text("default_model: test\n")
    bad_regime = replace(regime, root=regime_root)

    problems = cli._validate_reflection_agent(bad_regime)

    assert len(problems) == 1
    assert "reflection AgentCard missing" in problems[0]
