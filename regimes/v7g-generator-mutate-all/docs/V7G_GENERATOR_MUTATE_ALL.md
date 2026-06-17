# v7g Generator Mutate All

Purpose: start from the original generator/adjudication prompt that performed best for
`deepseek4flash`, then let GEPA mutate all task-facing guidance under a single combined prompt
budget.

This regime exposes three mutable components:

- `policy`: seeded from `v7b-generator-prompt-seed/prompts/seed-policy-vanilla-v7b-generator-prompt-seed.md`
- `topic_definitions`: seeded from `v7d-final/prompts/allowed-topics-v7d.md`
- `boundary_overlay`: seeded from `v7d-final/prompts/task-boundary-overlay-v7d.md`

The fixed AgentCard shell owns only the output contract, topic ordering limit, and the placement of
the mutable components. This keeps the fixed/free split explicit: GEPA can rewrite task guidance,
but cannot change the output protocol or schema.

Scoring adds one combined mutable-material budget:

```text
total_mutable_chars = len(policy) + len(topic_definitions) + len(boundary_overlay)
gepa_score = row_soft_exact - hygiene_penalty - total_mutable_length_penalty
```

The mutable policy budget is `4500` characters; the original generator/adjudication seed policy is
about `1981` characters, so it starts comfortably inside that cap. The combined mutable-material
budget is `20000` characters. The full seed material is intentionally allowed to start slightly above
the combined budget because the seeded topic definitions and boundary overlay are already large;
candidates are penalized, not rejected. Topic definitions do not have a separate length cap in this
regime because the combined cap is the main pressure on the definition/overlay material.

Default run:

```bash
uv run python scripts/run-regime.py regimes/v7g-generator-mutate-all/regime.yaml \
  --plan-gepa \
  --model deepseek4flash \
  --variant plain \
  --max-metric-calls 2400 \
  --run-index 1 \
  --run
```

Benchmark a candidate:

```bash
uv run python scripts/run-regime.py regimes/v7g-generator-mutate-all/regime.yaml \
  --plan-benchmark \
  --benchmark-run runs/v7g-generator-mutate-all/gepa/<run-name> \
  --model deepseek4flash \
  --variant plain \
  --run-index 1 \
  --run
```
