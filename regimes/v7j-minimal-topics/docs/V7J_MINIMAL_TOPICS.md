# V7J Minimal Topics

V7J is a sparse-prompt ablation built from the V7I guarded data split.

The task-facing structured prompt is intentionally minimal:

```text
Classify the GitHub issue from these topics. Use between 0 and 3 labels.
```

The prompt then includes the topic list and definitions. It does not include the
boundary overlay, JSON wording, or the longer routing policy used by V7I.

GEPA may mutate:

- `policy`
- `topic_definitions`

The boundary overlay is deliberately not task-facing in this regime. The fixed
boundary guidance file is still used by evaluator-side diagnostics and reflection
ASI.

The data position is unchanged from V7I:

- feedback: `data/feedback240.jsonl`
- Pareto guard: `data/pareto60.jsonl`
- benchmark: `data/bench78.jsonl`

Use this regime to test whether GPT-5.4-mini benefits from starting with a much
less prescriptive task prompt while retaining the guarded Pareto split.
