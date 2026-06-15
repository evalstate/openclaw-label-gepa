from openclaw_label_gepa.scoring import score_labels


def test_score_labels_micro_and_row_metrics() -> None:
    score = score_labels(
        [["gateway", "reliability"], ["docs"]],
        [["gateway"], ["docs", "config"]],
    )

    assert score.rows == 2
    assert round(score.topic_micro_f1, 6) == 0.666667
    assert score.row_exact_accuracy == 0.0
    assert round(score.avg_row_jaccard, 6) == 0.5
