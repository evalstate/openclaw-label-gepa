# Setup Guide

This guide is for running the current OpenClaw label GEPA regime from this repo.
The promoted active regime is `v7a`: v6p data and soft-exact objective, with the
plain-label protocol as the default.

## Prerequisites

- `uv`
- `hf`, from the Hugging Face CLI, if you want to download the published dataset
- Model credentials/configuration for the models you intend to run through `fast-agent`
- Access to the local `fast-agent` fork configured in `pyproject.toml`

If the Hugging Face dataset is private, authenticate first:

```bash
hf auth login
```

or make sure `HF_TOKEN` is set in your shell.

## Install

```bash
cd ~/source/openclaw-label-gepa
uv sync --dev
```

Run the local checks before starting a long run:

```bash
uv run openclaw-label-gepa --list-regimes
uv run openclaw-label-gepa --regime-info
uv run openclaw-label-gepa --doctor
uv run openclaw-label-gepa --audit
uv run ruff check .
uv run ty check
uv run pytest
uv run openclaw-label-gepa --validate
```

## Download the Published Dataset

Set the dataset repo id to the published Hugging Face dataset slug:

```bash
export OPENCLAW_LABEL_DATASET_REPO=<namespace/dataset-repo>
mkdir -p .hf/openclaw-label-dataset
hf download "$OPENCLAW_LABEL_DATASET_REPO" --type dataset --local-dir .hf/openclaw-label-dataset
```

For a narrower refresh, download only JSON artifacts:

```bash
hf download "$OPENCLAW_LABEL_DATASET_REPO" \
  --type dataset \
  --local-dir .hf/openclaw-label-dataset \
  --include "*.jsonl" \
  --include "*.json" \
  --include "*.md"
```

The v7a regime expects these split files:

```text
regimes/v7a/data/feedback300.jsonl
regimes/v7a/data/pareto60.jsonl
regimes/v7a/data/bench78.jsonl
regimes/v7a/data/split-manifest.json
```

This repo already includes a local copy of those files. The Hugging Face download
is mainly for refreshing, auditing, or rebuilding the local bundle. If the dataset
stores files under `v7a/data/`, refresh the local regime bundle with:

```bash
cp .hf/openclaw-label-dataset/v7a/data/feedback300.jsonl regimes/v7a/data/feedback300.jsonl
cp .hf/openclaw-label-dataset/v7a/data/pareto60.jsonl regimes/v7a/data/pareto60.jsonl
cp .hf/openclaw-label-dataset/v7a/data/bench78.jsonl regimes/v7a/data/bench78.jsonl
cp .hf/openclaw-label-dataset/v7a/data/split-manifest.json regimes/v7a/data/split-manifest.json
```

If the dataset stores the split files at its repo root, use the same commands
without `v6p/data/` in the source path.

## Inspect the Regime

Print the v7a summary:

```bash
uv run openclaw-label-gepa --summary
uv run openclaw-label-gepa --regime-info
uv run openclaw-label-gepa --list-regimes
uv run openclaw-label-gepa --audit
```

Print the full GEPA command without starting it:

```bash
uv run openclaw-label-gepa --plan-gepa --shell
```

The generated command starts with `cd <repo-root>` and sets:

- absolute `TRACKIO_DIR`
- Trackio project `easy-v7a-plain-gepa`
- Trackio group `v7a`
- run root `runs/v7a/gepa`
- score mode `row-soft-exact`
- x-axis metric `gepa/iteration`

## Start a GEPA Run

Default v7a plain-label run:

```bash
uv run openclaw-label-gepa --plan-gepa --shell
```

Copy and run the printed command. It changes into the repo root before starting.

Gemma run:

```bash
uv run openclaw-label-gepa \
  --plan-gepa \
  --model gemma-e4 \
  --run-index 1 \
  --shell
```

Gemma run with a 1600-call budget:

```bash
uv run openclaw-label-gepa \
  --plan-gepa \
  --model gemma-e4 \
  --max-metric-calls 1600 \
  --run-index 3 \
  --shell
```

No-model runner preflight for the same command:

```bash
uv run openclaw-label-gepa \
  --plan-gepa \
  --model gemma-e4 \
  --max-metric-calls 1600 \
  --run-index 3 \
  --runner-preflight \
  --shell
```

Run that preflight directly:

```bash
uv run openclaw-label-gepa \
  --plan-gepa \
  --model gemma-e4 \
  --max-metric-calls 1600 \
  --run-index 3 \
  --runner-preflight \
  --run
```

Start the real GEPA loop by removing `--runner-preflight`:

```bash
uv run openclaw-label-gepa \
  --plan-gepa \
  --model gemma-e4 \
  --max-metric-calls 1600 \
  --run-index 3 \
  --run
```

Mini model structured run:

```bash
uv run openclaw-label-gepa \
  --plan-gepa \
  --model codexresponses.gpt-5.4-mini \
  --run-index 1 \
  --shell
```

Use `--run-index` to create stable, distinct run names for repeated attempts.

## Benchmark a Base Prompt or Candidate

Benchmark commands are generated from the regime defaults, so `parallel`, Trackio
project, score mode, ASI, boundary guidance, hygiene penalty, and policy budget
come from `regimes/v7a/regime.yaml`.

Print three benchmark commands for the base v7a policy:

```bash
uv run openclaw-label-gepa \
  --plan-benchmark \
  --benchmark-run base \
  --repeat 3 \
  --shell
```

Benchmark a GEPA run's best candidate three times:

```bash
uv run openclaw-label-gepa \
  --plan-benchmark \
  --benchmark-run runs/v7a/gepa/<run-name> \
  --repeat 3 \
  --shell
```

`--benchmark-run` accepts:

- `base`
- a policy markdown file
- a run or candidate directory containing `best-policy.md` or `policy.md`

If the directory also contains `best-boundary-overlay.md` or
`boundary-overlay.md`, the benchmark command includes it automatically. Repeated
commands use consecutive run names starting at `--run-index`, defaulting to `1`.

## Trackio

Use the v7a Trackio project and group when comparing runs:

```text
project: easy-v7a-plain-gepa
group: v7a
x-axis: gepa/iteration
```

Start the local dashboard with:

```bash
uv run openclaw-label-gepa --trackio-command
uv run openclaw-label-gepa --trackio-command --run
```

Main streams to compare:

- `gepa/objective/*`: GEPA frontier objectives from the GEPA fork
- `openclaw/objective/val/gepa_score`: full-valset OpenClaw best-so-far objective
- `openclaw/objective/val/proposal_gepa_score`: full-valset score for the candidate just evaluated
- `openclaw/diagnostic/val/*`: OpenClaw diagnostic metrics, including FP/FN counts
- `candidate/*`: compact candidate policy health telemetry

Local Trackio state, downloaded HF artifacts, and GEPA run outputs are ignored by
git via `.trackio/`, `.hf/`, and `runs/`.
