# V6p Soft Exact Regime

`v6p` keeps the v6o data split but uses a softer row-wise optimization scorer:

```text
0.60 * row_jaccard + 0.20 * row_topic_f1 + 0.20 * row_exact
```

This makes partial precision/recall repairs visible to GEPA while final
benchmark reporting should still include strict row-exact, row-Jaccard,
micro-F1, and macro-F1. The stable source of truth is
`regimes/v6p/regime.yaml`.

## Data

```text
regimes/v6p/data/feedback300.jsonl
regimes/v6p/data/pareto60.jsonl
regimes/v6p/data/bench78.jsonl
regimes/v6p/data/split-manifest.json
```

## Commands

Inspect the regime:

```bash
uv run openclaw-label-gepa regimes/v6p/regime.yaml --regime-info
uv run openclaw-label-gepa regimes/v6p/regime.yaml --validate
```

Print a GEPA command:

```bash
uv run openclaw-label-gepa regimes/v6p/regime.yaml --plan-gepa --shell
```

Run a no-model preflight:

```bash
uv run openclaw-label-gepa regimes/v6p/regime.yaml --plan-gepa --runner-preflight --run
```

Run GEPA:

```bash
uv run openclaw-label-gepa regimes/v6p/regime.yaml --plan-gepa --run
```

Benchmark the base policy:

```bash
uv run openclaw-label-gepa regimes/v6p/regime.yaml --plan-benchmark --benchmark-run base --run
```

Start Trackio:

```bash
uv run openclaw-label-gepa regimes/v6p/regime.yaml --trackio-command --run
```

Use `gepa/iteration` as the Trackio x-axis. The main streams are
`gepa/objective/*`, `openclaw/objective/val/*`, and
`openclaw/diagnostic/val/*`, including topic FP/FN counts.
