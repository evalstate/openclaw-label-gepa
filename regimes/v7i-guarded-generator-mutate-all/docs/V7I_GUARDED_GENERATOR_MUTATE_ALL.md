# v7i Guarded Generator Mutate All

Purpose: v7h successor for testing whether candidate overfit to the original Pareto set caused the DeepSeek transfer regression. It keeps the clean v7h prompt shell, but uses a second bench-like Pareto guard held out from feedback rows.

The task prompt uses neutral model-facing headings:

- `Topic List and Definitions`
- `Boundary Rules`
- `Routing Policy`


Data layout:

- `feedback240.jsonl`: active reflection/training rows.
- `pareto60.jsonl`: active GEPA Pareto/validation guard, held out from v7h feedback.
- `pareto-guard60.jsonl`: same guard set, named explicitly for audit.
- `pareto-v7h-original60.jsonl`: original v7h Pareto set, retained for audit-only comparison.
- `bench78.jsonl`: unchanged final benchmark; not used by GEPA candidate selection.

The guard set uses cardinality `1:25,2:20,3:15`, close to the benchmark distribution, to make recall-padding candidates less attractive than they were under the original `1:18,2:24,3:18` Pareto shape.

The optimizable components are:

- `policy`: seeded from `prompts/seed-policy-v7i.md`
- `topic_definitions`: seeded from `prompts/allowed-topics-v7i.md`
- `boundary_overlay`: seeded from `prompts/task-boundary-overlay-v7i.md`

The fixed AgentCard shell owns the output contract, topic ordering limit, and the placement of the
task guidance. GEPA may rewrite the policy, topic definitions, and boundary rules, but may not
change the output schema or topic IDs.

Scoring uses the v7g setup:

```text
row_composite_score = 0.60*row_jaccard + 0.20*row_topic_f1 + 0.20*row_exact
gepa_score = max(0.0, row_composite_score - hygiene_penalty - total_mutable_length_penalty)
```

Budget settings:

- `policy_char_budget`: `0` (disabled)
- `topic_definitions_char_budget`: `0` (disabled)
- `total_mutable_char_budget`: `20000`
- `hygiene_penalty`: `0.06`

The reflection model should decide how to balance the policy, topic definitions, and boundary
rules within the combined prompt budget.

Default gpt-5.4-mini run:

```bash
uv run python scripts/run-regime.py regimes/v7i-guarded-generator-mutate-all/regime.yaml \
  --plan-gepa \
  --model codexresponses.gpt-5.4-mini \
  --variant structured \
  --run-index 1 \
  --run
```

Benchmark a candidate:

```bash
uv run python scripts/run-regime.py regimes/v7i-guarded-generator-mutate-all/regime.yaml \
  --plan-benchmark \
  --benchmark-run runs/v7i-guarded-generator-mutate-all/gepa/<run-name> \
  --model codexresponses.gpt-5.4-mini \
  --variant structured \
  --run-index 1 \
  --run
```
