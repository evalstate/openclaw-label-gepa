# v7f Constrained Definitions

Purpose: test whether GEPA can improve topic-definition wording without allowing the definitions file to become a second policy document.

This is the controlled v7f ablation. It exposes `policy` and `topic_definitions` as mutable components. The task boundary overlay remains fixed.

Key controls:

- Data, schema, static ASI, boundary guidance, seed policy, and score mode are inherited from `v7d-final`.
- Topic IDs are frozen by schema and contract validation.
- `topic_definitions` must contain exactly one bullet for every schema topic ID.
- Invalid topic-definition contracts score zero.
- `topic_definitions` has a 9500 character budget; over-budget definitions receive a GEPA score penalty.
- Policy remains constrained to the 5000 character budget and hygiene penalty.

Default run:

```bash
uv run python scripts/run-regime.py regimes/v7f-constrained-definitions/regime.yaml \
  --plan-gepa \
  --model gemma-e4 \
  --variant plain \
  --max-metric-calls 2400 \
  --run-index 1 \
  --run
```

Benchmark a candidate run:

```bash
uv run python scripts/run-regime.py regimes/v7f-constrained-definitions/regime.yaml \
  --plan-benchmark \
  --benchmark-run runs/v7f-constrained-definitions/gepa/<run-name> \
  --model gemma-e4 \
  --variant plain \
  --run-index 1 \
  --run
```
