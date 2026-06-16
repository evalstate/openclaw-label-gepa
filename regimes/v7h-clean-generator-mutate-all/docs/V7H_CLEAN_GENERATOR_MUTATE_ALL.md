# v7h Clean Generator Mutate All

Purpose: pristine v7g successor for final runs. It starts from the generator/adjudication seed that
worked best for `deepseek4flash`, but keeps local copies of the prompt, policy, schema, topic
definitions, boundary rules, and final data splits.

The task prompt uses neutral model-facing headings:

- `Topic List and Definitions`
- `Boundary Rules`
- `Routing Policy`

The optimizable components are:

- `policy`: seeded from `prompts/seed-policy-v7h.md`
- `topic_definitions`: seeded from `prompts/allowed-topics-v7h.md`
- `boundary_overlay`: seeded from `prompts/task-boundary-overlay-v7h.md`

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
uv run python scripts/run-regime.py regimes/v7h-clean-generator-mutate-all/regime.yaml \
  --plan-gepa \
  --model codexresponses.gpt-5.4-mini \
  --variant structured \
  --run-index 1 \
  --run
```

Benchmark a candidate:

```bash
uv run python scripts/run-regime.py regimes/v7h-clean-generator-mutate-all/regime.yaml \
  --plan-benchmark \
  --benchmark-run runs/v7h-clean-generator-mutate-all/gepa/<run-name> \
  --model codexresponses.gpt-5.4-mini \
  --variant structured \
  --run-index 1 \
  --run
```
