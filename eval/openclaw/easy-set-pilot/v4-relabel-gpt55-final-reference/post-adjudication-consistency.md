# v4 GPT-5.5 final-reference consistency

This comparison uses the corrected source-label extraction rule:

- source/current labels come from `expected_topics`;
- teacher labels come from `gpt55_labels` / `labels`.

The earlier comparison helper incorrectly preferred stale `gpt55_labels` in source rows,
which made `openclaw-openclaw-90146` appear changed even after its adjudicated
`expected_topics` had been updated.

## Result

Compared against current `easy-final-v4.jsonl`:

```text
source rows:        125
teacher rows:       125
exact agreement:    125 / 125
changed rows:       0
teacher buckets:    easy: 125
strict easy rows:   123
```

## 90146

Current adjudicated source labels:

```text
agent_runtime, model_releases, model_serving, reliability
```

GPT-5.5 final-reference labels:

```text
agent_runtime, model_releases, model_serving, reliability
```

The final-reference generation is exact-consistent with the adjudicated source.
