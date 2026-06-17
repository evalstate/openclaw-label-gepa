import json
from pathlib import Path

from openclaw_label_gepa.benchmark import score_output_file
from openclaw_label_gepa.regimes import load_regime


def test_score_output_file_against_regime(tmp_path: Path) -> None:
    regime = load_regime(Path("regimes/v7i-guarded-generator-mutate-all/regime.yaml"))
    train = regime.load_train()
    rows = []
    for row, expected in zip(train.rows[:2], train.expected_topics[:2], strict=True):
        rows.append(
            {
                "input": {"id": row["id"]},
                "output": json.dumps({"labels": expected}),
            }
        )
    output_path = tmp_path / "outputs.jsonl"
    output_path.write_text(
        "".join(json.dumps(row) + "\n" for row in rows),
        encoding="utf-8",
    )

    report = score_output_file(regime, output_path)

    assert report.score.rows == 240
    assert report.score.topic_micro_f1 < 1.0
    assert report.row_results[0].exact
    assert len(report.missing_output_rows) == 238
