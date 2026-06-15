# V7a Plain Soft-Exact GEPA Regime

v7a promotes the v6p plain-label protocol as the default runnable regime.
It keeps the v6p/v6o split data and soft-exact row-wise objective, but starts
from the plain AgentCard and emits `--plain-labels` without requiring a manual
variant override.

The sampled-row scorer is:

```text
0.60 * row_jaccard + 0.20 * row_topic_f1 + 0.20 * row_exact
```

Final reporting should still include strict row-exact, row-Jaccard, micro-F1,
and macro-F1 on Pareto and held-out benchmark rows.

## Artifacts

- static ASI: `regimes/v7a/prompts/vanilla-asi-v7a-slim.md`
- plain-label AgentCard: `regimes/v7a/prompts/openclaw-vanilla-labeler-plain-v7a.md`
- structured AgentCard: `regimes/v7a/prompts/openclaw-vanilla-labeler-v7a.md`
- seed prompt: `regimes/v7a/prompts/seed-policy-vanilla-v7a.md`
- feedback split: `regimes/v7a/data/feedback300.jsonl`
- Pareto split: `regimes/v7a/data/pareto60.jsonl`
- bench split: `regimes/v7a/data/bench78.jsonl`

## Trackio

Use `gepa/iteration` as the x-axis.

```text
project: easy-v7a-plain-gepa
group: v7a
local dir: runs/v7a/trackio
```

Primary objective streams:

```text
gepa/objective/gepa_score
gepa/objective/row_jaccard
gepa/objective/row_topic_f1
gepa/objective/row_exact
openclaw/objective/val/gepa_score
openclaw/objective/val/best_gepa_score
openclaw/objective/val/proposal_gepa_score
openclaw/objective/val/proposal_delta_vs_best_before
```

`openclaw/objective/val/gepa_score` is logged as best-so-far so the main
Trackio objective chart includes the seed baseline and tracks incumbent quality.
Use `proposal_gepa_score` to inspect the candidate just evaluated.

## Commands

Print the default v7a GEPA command:

```bash
uv run python scripts/run-regime.py regimes/v7a/regime.yaml --plan-gepa --shell
```

Print a base benchmark replay command:

```bash
uv run python scripts/run-regime.py regimes/v7a/regime.yaml --plan-benchmark --benchmark-run base --shell
```

Start the local Trackio dashboard:

```bash
TRACKIO_DIR=runs/v7a/trackio uv run trackio show --project easy-v7a-plain-gepa
```
