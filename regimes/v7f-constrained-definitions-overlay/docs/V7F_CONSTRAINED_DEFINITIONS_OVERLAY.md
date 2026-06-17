# v7f Constrained Definitions + Overlay

Purpose: test the larger mutable surface after v7e showed that unconstrained mutable definitions can grow into an oversized rulebook.

This is not the clean v7f comparison. It exposes `policy`, `topic_definitions`, and `boundary_overlay` as mutable components. Use it to test whether coordinated wording changes across the taxonomy definitions and task overlay help a smaller task model.

Key controls:

- Data, schema, static ASI, boundary guidance, seed policy, and score mode are inherited from `v7d-final`.
- Topic IDs are frozen by schema and contract validation.
- `topic_definitions` must contain exactly one bullet for every schema topic ID.
- Invalid topic-definition contracts score zero.
- `topic_definitions` has a 9500 character budget; over-budget definitions receive a GEPA score penalty.
- The task overlay seed is the v7d final overlay.

Default run:

```bash
uv run python scripts/run-regime.py regimes/v7f-constrained-definitions-overlay/regime.yaml \
  --plan-gepa \
  --model gemma-e4 \
  --variant plain \
  --max-metric-calls 2400 \
  --run-index 1 \
  --run
```
