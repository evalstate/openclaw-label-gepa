# V6o Strict Jaccard/Exact Regime

`v6o` is the strict row-set regime. It uses the 300-row feedback split, 60-row
Pareto split, and 78-row benchmark split with the `row-jaccard-exact` scorer:

```text
0.70 * row_jaccard + 0.30 * row_exact
```

The stable source of truth is `regimes/v6o/regime.yaml`.

## Data

```text
regimes/v6o/data/feedback300.jsonl
regimes/v6o/data/pareto60.jsonl
regimes/v6o/data/bench78.jsonl
regimes/v6o/data/split-manifest.json
```

## Commands

Inspect the regime:

```bash
uv run openclaw-label-gepa regimes/v6o/regime.yaml --regime-info
uv run openclaw-label-gepa regimes/v6o/regime.yaml --validate
```

Print a GEPA command:

```bash
uv run openclaw-label-gepa regimes/v6o/regime.yaml --plan-gepa --shell
```

Run a no-model preflight:

```bash
uv run openclaw-label-gepa regimes/v6o/regime.yaml --plan-gepa --runner-preflight --run
```

Run GEPA:

```bash
uv run openclaw-label-gepa regimes/v6o/regime.yaml --plan-gepa --run
```

Benchmark the base policy:

```bash
uv run openclaw-label-gepa regimes/v6o/regime.yaml --plan-benchmark --benchmark-run base --run
```

Start Trackio:

```bash
uv run openclaw-label-gepa regimes/v6o/regime.yaml --trackio-command --run
```

Use `gepa/iteration` as the Trackio x-axis. Treat `gepa/objective/*` as GEPA
frontier objectives and `openclaw/objective/val/*` plus
`openclaw/diagnostic/val/*` as full-valset OpenClaw diagnostics.
