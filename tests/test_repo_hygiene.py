from __future__ import annotations

from pathlib import Path


def _repo_text_files() -> list[Path]:
    roots = [
        Path("README.md"),
        Path("docs"),
        Path("datasets"),
        Path("regimes"),
        Path("scripts"),
        Path("src"),
        Path("tests"),
        Path("tools"),
        Path("pyproject.toml"),
    ]
    files: list[Path] = []
    for root in roots:
        if root.is_file():
            files.append(root)
        elif root.exists():
            files.extend(path for path in root.rglob("*") if path.is_file())
    return [
        path
        for path in files
        if "__pycache__" not in path.parts
        and ".pytest_cache" not in path.parts
        and ".ruff_cache" not in path.parts
        and not (path.suffix == ".jsonl" and "data" in path.parts)
    ]


def test_executable_metadata_does_not_reference_old_temp_workspace() -> None:
    checked = [
        Path("pyproject.toml"),
        Path("uv.lock"),
        Path("src/openclaw_label_gepa/cli.py"),
        Path("scripts/run-regime.py"),
        Path("src/openclaw_label_gepa/runplan.py"),
        Path("tools/runners/gepa-runner.py"),
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in checked)

    assert "/home/ssmith/temp/gepa-batch-openclaw" not in combined
    assert "../../temp/gepa-batch-openclaw" not in combined


def test_repo_does_not_reference_retired_workspace_or_lineage_terms() -> None:
    allowed = {Path("tests/test_repo_hygiene.py")}
    patterns = [
        "/home/ssmith/temp/gepa-batch-openclaw",
        "eval/openclaw/easy-set-pilot",
        "artifacts/batch-manifests",
        "artifacts/lineage",
        "source_ledger",
        "gold5",
        "gold-5",
        "gold labels",
        "runs/easy-set",
        "v6b-databuild",
    ]
    hits = []
    for path in _repo_text_files():
        if path in allowed:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in patterns:
            if pattern in text:
                hits.append(f"{path}: {pattern}")

    assert hits == []


def test_data_build_scripts_do_not_default_to_old_eval_tree() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(Path("tools/data-build").glob("*.py"))
    )

    assert 'ROOT / "eval' not in combined
    assert 'ROOT / "scripts"' not in combined
    assert "eval/openclaw/easy-set-pilot" not in combined
    assert "regimes/" not in combined
    assert "regimes" not in combined


def test_current_data_build_default_inputs_exist_or_are_explicitly_required() -> None:
    required = [
        Path("datasets/openclaw-label-v7a/data/final/final-gepa-train.jsonl"),
        Path("datasets/openclaw-label-v7a/data/final/final-ledger.jsonl"),
        Path("datasets/openclaw-label-v7a/data/splits/bench78.jsonl"),
        Path("datasets/openclaw-label-v7a/data/splits/pareto60.jsonl"),
        Path("datasets/openclaw-label-v7a/artifacts/spec/allowed-topics-v7a.md"),
        Path("datasets/openclaw-label-v7a/artifacts/spec/teacher-card-v7a.md"),
        Path("datasets/openclaw-label-v7a/artifacts/spec/teacher-template-v7a.md"),
        Path("datasets/openclaw-label-v7a/artifacts/spec/teacher-output-v7a.schema.json"),
        Path("datasets/openclaw-label-v7a/artifacts/spec/seed-policy-vanilla-v7a.md"),
    ]

    missing = [str(path) for path in required if not path.exists()]
    assert missing == []
