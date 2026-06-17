# V7d Final GEPA Regime

v7d-final is the handover/default regime after the v6/v7 experiments. It keeps the strong final
v7a/v6p data split and uses the simplest setup that still gave useful GEPA behavior without hiding
task information in the mutable seed.

## Position

The fixed AgentCard supplies the taxonomy, output contract, and boundary overlay. The reflection fast-agent environment is regime-local, so the handover run is self-contained. GEPA may only tune
a compact routing policy overlay. Overlay mutation remains an ablation, not the default.

Default settings:

```text
score_mode: row-soft-exact
feedback_profile: compact
candidate_proposer: default
reflection_minibatch_size: 20
max_metric_calls: 1400
policy_char_budget: 5000
default_variant: structured
```

The sampled-row objective is a soft row-set score:

```text
row_composite_score = 0.60*row_jaccard + 0.20*row_topic_f1 + 0.20*row_exact
gepa_score = max(0.0, row_composite_score - policy_length_penalty - hygiene_penalty)
```

`row_exact` is only 20% of the shaped scalar. Jaccard is dominant, so both false positives and false
negatives matter throughout optimization.

## Why This Shape

Recent v7 runs showed that once the seed is sane, GEPA often finds minibatch improvements that do not
transfer past the seed on full Pareto/bench. This regime therefore avoids elaborate reflection or
large mutable prompts. It uses compact feedback, a small but real policy budget, and a seed that
states centrality/cardinality rules without row examples or hidden topic definitions.

## Artifacts

- seed policy: `regimes/v7d-final/prompts/seed-policy-vanilla-v7d-final.md`
- compact ASI: `regimes/v7d-final/prompts/vanilla-asi-v7d-final-compact.md`
- output schema: `regimes/v7d-final/schemas/output-v7d.schema.json`
- plain AgentCard: `regimes/v7d-final/prompts/vanilla-labeler-plain-v7d-final.md`
- structured AgentCard: `regimes/v7d-final/prompts/vanilla-labeler-v7d-final.md`
- reflection env: `regimes/v7d-final/.fast-agent/`
- feedback split: `regimes/v7d-final/data/feedback300.jsonl`
- Pareto split: `regimes/v7d-final/data/pareto60.jsonl`
- bench split: `regimes/v7d-final/data/bench78.jsonl`

## Recommended Commands

Plan/run the default GEPA pass:

```bash
uv run python scripts/run-regime.py regimes/v7d-final/regime.yaml --plan-gepa --shell
```

Preflight it:

```bash
uv run python scripts/run-regime.py regimes/v7d-final/regime.yaml --plan-gepa --runner-preflight --run
```

Benchmark the base seed:

```bash
uv run python scripts/run-regime.py regimes/v7d-final/regime.yaml --plan-benchmark --benchmark-run base --shell
```

Start Trackio:

```bash
TRACKIO_DIR=runs/v7d-final/trackio uv run trackio show --project easy-v7d-final-gepa
```

## Intended Ablations

Keep ablations explicit in the run name and notes:

- plain output vs structured output;
- custom proposer vs default proposer;
- full ASI vs compact ASI;
- mutable boundary overlay vs static overlay;
- 3,000 vs 5,000 vs 8,000 policy budget.
