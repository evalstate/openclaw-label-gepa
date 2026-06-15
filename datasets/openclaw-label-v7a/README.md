---
pretty_name: OpenClaw Labels V7A
task_categories:
- text-classification
language:
- en
tags:
- openclaw
- multilabel-classification
- gepa
- evaluation
- weak-supervision
- synthetic-data
---

# OpenClaw Label V7A

This dataset is the publication bundle for the OpenClaw topic-label benchmark
and GEPA optimization regimes.

## Contents

```text
data/splits/feedback300.jsonl       GEPA feedback/train rows
data/splits/pareto60.jsonl          GEPA Pareto validation rows
data/splits/bench78.jsonl           held-out benchmark rows
data/splits/split-manifest.json     split hashes, overlaps, and label counts
data/final/final-ledger.jsonl       final 330-row five-model ledger
data/final/final-gepa-train.jsonl   final 330-row GEPA-compatible train view
data/final/source-gpt-*.jsonl       GPT teacher/source reservoirs
data/final/source-opus-*.jsonl      Opus teacher/source reservoirs
data/final/manifest.json            final bundle manifest
artifacts/                          build specs and data-build scripts
```

Row counts:

```text
feedback300: 300
pareto60: 60
bench78: 78
final-ledger: 330
final-gepa-train: 330
source reservoirs: 5 x 330
```

## Label Frequencies

The final 330-row ledger contains 633 label assignments across 33 labels.
Rows are multi-label with a maximum cardinality of 3.

Final-cardinality distribution:

```text
1 label: 117 rows
2 labels: 123 rows
3 labels: 90 rows
```

Final label counts:

| Label | Count |
|---|---:|
| inference_api | 61 |
| config | 57 |
| security | 41 |
| reliability | 35 |
| chat_integrations | 32 |
| acp | 27 |
| agent_runtime | 25 |
| tests_ci | 24 |
| gateway | 23 |
| skills_plugins | 23 |
| ui_tui | 23 |
| memory | 21 |
| telemetry_usage | 18 |
| model_lifecycle | 18 |
| mcp_tooling | 16 |
| packaging_deployment | 16 |
| docs | 15 |
| codex | 14 |
| exec_tools | 14 |
| tool_calling | 13 |
| self_hosted_inference | 12 |
| cron_automation | 12 |
| approvals | 12 |
| sessions | 12 |
| hooks | 12 |
| acpx | 11 |
| notifications | 10 |
| api_surface | 8 |
| sandboxing | 8 |
| queueing | 8 |
| browser_automation | 7 |
| auth_identity | 3 |
| coding_agent_integrations | 2 |

Split summary:

| Split | Rows | Label assignments | Cardinality distribution |
|---|---:|---:|---|
| feedback300 | 300 | 603 | 1: 90, 2: 117, 3: 93 |
| pareto60 | 60 | 120 | 1: 18, 2: 24, 3: 18 |
| bench78 | 78 | 144 | 1: 32, 2: 26, 3: 20 |

The held-out benchmark split was deliberately more balanced than the training
feedback split. The final ledger still has a long tail: `auth_identity` and
`coding_agent_integrations` have fewer than four examples and should be treated
as under-supported labels for optimization and benchmark interpretation.

## Labeling Approach

The generation prompts are designed as understanding-based topic classification,
not keyword matching. The model is asked to infer the central maintainer-owned
surface changed or discussed by an issue/PR, apply suppression rules for
incidental mentions, and keep labels in the allowed-topic priority order. File
paths, package names, examples, and source labels are evidence, but are not by
themselves sufficient for a label.

Source teacher records include confidence, ambiguity, possible-confusion, batch,
repeat, and run-source information so downstream users can audit soft
disagreements and instability signals rather than treating every row as equally
certain.

## Known Limitations

- The dataset is small relative to the number of labels, and further taxonomy
  upates are recommended to simplify the task.
- Some labels are rare, especially `auth_identity` and
  `coding_agent_integrations`.
- Several labels are semantically adjacent (`inference_api`,
  `self_hosted_inference`, `model_lifecycle`, `agent_runtime`; also `acp`,
  `acpx`, `sessions`, and `queueing`), so boundary quality matters as much as
  raw examples.
- Labels are generated from a five-model process and source evidence, not hand
  adjudicated ground truth for every possible ambiguity.

## Improvements

- Hand-adjudicate high-impact disagreements and the lowest-frequency labels.
- Add or recover targeted rows for under-supported labels to improve label mix
  and reduce frequency skew.
- Revisit whether the schema should be simplified by merging labels that remain
  hard to distinguish operationally.
- Keep improving boundary guidance for common soft-confusion pairs, especially
  provider/model/runtime labels and ACP/session/queue labels.
- Use benchmark results and GEPA diagnostics to identify labels that need more
  examples rather than only changing prompts.

## Download

```bash
export OPENCLAW_LABEL_DATASET_REPO=<namespace/openclaw-label-v7a>
hf download "$OPENCLAW_LABEL_DATASET_REPO" \
  --type dataset \
  --local-dir .hf/openclaw-label-v7a
```

Refresh the local v7a regime bundle from a downloaded copy:

```bash
cp .hf/openclaw-label-v7a/data/splits/feedback300.jsonl regimes/v7a/data/feedback300.jsonl
cp .hf/openclaw-label-v7a/data/splits/pareto60.jsonl regimes/v7a/data/pareto60.jsonl
cp .hf/openclaw-label-v7a/data/splits/bench78.jsonl regimes/v7a/data/bench78.jsonl
cp .hf/openclaw-label-v7a/data/splits/split-manifest.json regimes/v7a/data/split-manifest.json
```

## Publish

From the repo root:

```bash
export OPENCLAW_LABEL_DATASET_REPO=<namespace/openclaw-label-v7a>
uv run python scripts/publish-dataset.py \
  datasets/openclaw-label-v7a \
  --repo-id "$OPENCLAW_LABEL_DATASET_REPO" \
  --write-manifest \
  --dry-run
hf repos create "$OPENCLAW_LABEL_DATASET_REPO" --type dataset --private --exist-ok
hf upload "$OPENCLAW_LABEL_DATASET_REPO" datasets/openclaw-label-v7a \
  --type dataset \
  --commit-message "Publish OpenClaw label v7a dataset"
```

## Construction

The dataset bundle keeps the data, the source model outputs used to derive it,
the label/spec files, and the repo-owned construction scripts. It intentionally
does not publish old intermediate batch ledgers or reservoir paths.

Construction scripts in `artifacts/scripts/` use consistent descriptive names:

```text
analyze-easy-set-stability.py   repeated-run stability analysis
build-consensus.py              intake consensus/adjudication artifacts
build-dataset-splits.py         feedback/Pareto/benchmark split builder
build-feedback300.py            300-row GEPA feedback builder
build-feedback300-v7a.py        v7a feedback wrapper with v7a defaults
build-final-splits.py           final feedback/Pareto/benchmark split builder
build-intake.py                 source intake bundle builder
build-slim-tiers.py             slim consensus tier router
build-train-ledger.py           train-quality ledger builder
```

The final-data summary is `data/final/manifest.json`. The split summary is
`data/splits/split-manifest.json`.
