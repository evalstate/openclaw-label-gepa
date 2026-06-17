# Setup

The active default regime is `v7i-guarded-generator-mutate-all`. The retained comparison regime is `v7h-clean-generator-mutate-all`. Legacy `eval/openclaw` assets and earlier regimes have been removed from the active tree.

## Quick start

```bash
uv sync --dev
uv run openclaw-label-gepa --list-regimes
uv run openclaw-label-gepa --regime-info
uv run openclaw-label-gepa --doctor
uv run openclaw-label-gepa --validate
uv run pytest
```

## Active regimes

```text
regimes/v7h-clean-generator-mutate-all/
regimes/v7i-guarded-generator-mutate-all/
```

Each regime contains its own local prompt, schema, and split bundle under the regime directory.

## GEPA plans

Default v7i plan:

```bash
uv run openclaw-label-gepa --plan-gepa --shell
```

Explicit v7h plan:

```bash
uv run openclaw-label-gepa regimes/v7h-clean-generator-mutate-all/regime.yaml --plan-gepa --shell
```

Gemma v7i preflight:

```bash
uv run openclaw-label-gepa \
  --plan-gepa \
  --model gemma-e4 \
  --max-metric-calls 1600 \
  --run-index 3 \
  --runner-preflight \
  --shell
```

## Trackio

```bash
uv run openclaw-label-gepa --trackio-command
uv run openclaw-label-gepa --trackio-command --run
```

The v7i defaults are:

```yaml
project: easy-v7i-guarded-generator-mutate-all-gepa
group: v7i-guarded-generator-mutate-all
run_root: runs/v7i-guarded-generator-mutate-all/gepa
```
