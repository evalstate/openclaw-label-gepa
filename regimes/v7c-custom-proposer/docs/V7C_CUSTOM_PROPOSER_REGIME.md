# V7c Custom-Proposer GEPA Regime

v7c-custom-proposer keeps the v7b generator-prompt seed and the same feedback/Pareto/bench split, but changes how GEPA asks the reflection model to mutate the policy.

The sampled-row scorer remains:

```text
0.60 * row_jaccard + 0.20 * row_topic_f1 + 0.20 * row_exact
```

## Purpose

This is the cleanest experiment for the question: are we fighting GEPA's default instruction proposer? The regime gives the reflection model full ASI, then routes candidate generation through `--candidate-proposer openclaw-compact`. That proposer asks for a complete replacement policy, but constrains the edit to a small number of general behavioral changes, forbids row memorization/taxonomy copying, and repairs candidates that breach the policy hygiene or length checks before scoring.

## Defaults

- structured JSON output protocol
- `feedback_profile: full`
- `candidate_proposer: openclaw-compact`
- minibatch size 20
- soft-exact row score
- policy budget 4500 chars

## Artifacts

- static ASI: `regimes/v7c-custom-proposer/prompts/vanilla-asi-v7c-custom-proposer-slim.md`
- structured AgentCard: `regimes/v7c-custom-proposer/prompts/openclaw-vanilla-labeler-v7c-custom-proposer.md`
- plain-label AgentCard, available only with `--variant plain`: `regimes/v7c-custom-proposer/prompts/openclaw-vanilla-labeler-plain-v7c-custom-proposer.md`
- seed prompt: `regimes/v7c-custom-proposer/prompts/seed-policy-vanilla-v7c-custom-proposer.md`
- feedback split: `regimes/v7c-custom-proposer/data/feedback300.jsonl`
- Pareto split: `regimes/v7c-custom-proposer/data/pareto60.jsonl`
- bench split: `regimes/v7c-custom-proposer/data/bench78.jsonl`

## Split

The data is intentionally unchanged from v7b so the proposer effect is isolated from the data mix. Feedback/Pareto/bench overlap is zero in the split manifest.

## Trackio

Use `gepa/iteration` or `gepa/total_metric_calls` as the x-axis. The run name includes the feedback profile and proposer.

```text
project: easy-v7c-custom-proposer-gepa
group: v7c-custom-proposer
local dir: runs/v7c-custom-proposer/trackio
```

## Commands

Print the default GEPA command:

```bash
uv run python scripts/run-regime.py regimes/v7c-custom-proposer/regime.yaml --plan-gepa --shell
```

Print a base benchmark replay command:

```bash
uv run python scripts/run-regime.py regimes/v7c-custom-proposer/regime.yaml --plan-benchmark --benchmark-run base --shell
```

Start the local Trackio dashboard:

```bash
TRACKIO_DIR=runs/v7c-custom-proposer/trackio uv run trackio show --project easy-v7c-custom-proposer-gepa
```
