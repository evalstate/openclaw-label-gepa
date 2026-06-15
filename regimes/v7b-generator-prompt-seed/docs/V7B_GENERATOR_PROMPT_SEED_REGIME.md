# V7b Generator-Prompt-Seed GEPA Regime

v7b-generator-prompt-seed tests a distilled version of the gold-label generation prompt as the
vanilla seed policy. It uses the structured JSON protocol and soft-exact objective, plus an
alternate disjoint feedback/Pareto split so the Pareto set differs materially from v7a.

The sampled-row scorer is:

```text
0.60 * row_jaccard + 0.20 * row_topic_f1 + 0.20 * row_exact
```

## Purpose

The generation prompt showed strong precision and better overall behavior, with remaining errors
mostly under-labelling secondary central owners. This regime asks GEPA to start from that stronger
adjudication framing instead of a very sparse seed.

## Artifacts

- static ASI: `regimes/v7b-generator-prompt-seed/prompts/vanilla-asi-v7b-generator-prompt-seed-slim.md`
- structured AgentCard: `regimes/v7b-generator-prompt-seed/prompts/openclaw-vanilla-labeler-v7b-generator-prompt-seed.md`
- plain-label AgentCard, available only with `--variant plain`: `regimes/v7b-generator-prompt-seed/prompts/openclaw-vanilla-labeler-plain-v7b-generator-prompt-seed.md`
- seed prompt: `regimes/v7b-generator-prompt-seed/prompts/seed-policy-vanilla-v7b-generator-prompt-seed.md`
- feedback split: `regimes/v7b-generator-prompt-seed/data/feedback300.jsonl`
- Pareto split: `regimes/v7b-generator-prompt-seed/data/pareto60.jsonl`
- bench split: `regimes/v7b-generator-prompt-seed/data/bench78.jsonl`

## Split

The feedback and Pareto files are the alternate mix001 split created from the final v6 gold pool.
Benchmark remains the held-out bench78 split. Feedback/Pareto/bench overlap is zero in the split
manifest.

## Trackio

Use `gepa/iteration` as the x-axis.

```text
project: easy-v7b-generator-prompt-seed-gepa
group: v7b-generator-prompt-seed
local dir: runs/v7b-generator-prompt-seed/trackio
```

## Commands

Print the default GEPA command:

```bash
uv run python scripts/run-regime.py regimes/v7b-generator-prompt-seed/regime.yaml --plan-gepa --shell
```

Print a base benchmark replay command:

```bash
uv run python scripts/run-regime.py regimes/v7b-generator-prompt-seed/regime.yaml --plan-benchmark --benchmark-run base --shell
```

Start the local Trackio dashboard:

```bash
TRACKIO_DIR=runs/v7b-generator-prompt-seed/trackio uv run trackio show --project easy-v7b-generator-prompt-seed-gepa
```
