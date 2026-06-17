# OpenClaw GEPA Reflection ASI

Use this as reflection side information only. Do not insert it verbatim into the task AgentCard.

## Optimization Target

Optimize label-set selection for OpenClaw maintainer-interest routing. The task model already sees
the fixed taxonomy, the fixed boundary overlay, and the output contract. The mutable policy is a
small overlay on top of those fixed inputs, not a replacement taxonomy.

The desired behavior is the correct set of topic IDs for each row. The GEPA optimization scalar is a
soft row-set score, not pure exact-match accuracy:

```text
row_topic_f1 = 2*true_positives / (2*true_positives + false_positives + false_negatives)
row_jaccard = true_positives / (true_positives + false_positives + false_negatives)
row_exact = 1.0 only when the output is valid and has no false positives or false negatives; else 0.0
row_composite_score = 0.60*row_jaccard + 0.20*row_topic_f1 + 0.20*row_exact
gepa_score = max(0.0, row_composite_score - policy_length_penalty - hygiene_penalty)
```

Jaccard is the primary set-overlap signal, so both missing labels and extra labels are costly. Row
topic F1 gives additional partial credit for precision/recall repairs. Exact match is a 20% bonus,
not the whole objective. Held-out reporting should still include row-exact, row-Jaccard, micro-F1,
and macro-F1 separately.

## What To Mutate

Find one or two general policy edits that improve label set selection. Prefer centrality tests,
boundary tie-breakers, and compact suppression rules over keyword rules.

Do not copy row IDs, issue numbers, URLs, exact titles, examples, topic definitions, cue lists, the
allowed-topic enum, or the fixed boundary overlay. Do not expand the policy into a topic guide. If
the feedback is mixed, make no broad change.

Keep the complete mutable policy under 5,000 characters.

## Feedback To Use

Reflection receives compact diagnostics:

- per-row expected labels, predicted labels, false positives, false negatives, and row score parts;
- minibatch aggregates such as row-exact, average Jaccard, micro-F1, and macro-F1 diagnostics;
- label over-application and under-application counts;
- directional co-error pairs where a missed expected label and an extra predicted label appeared on
  the same row;
- policy hygiene and policy length diagnostics.

Use label over/under counts to decide whether recall or precision is the dominant issue. Co-error
pairs are evidence for reusable boundary confusion only when the distinction generalizes; they are
not a formal substitution table.

Compact feedback intentionally omits row text to reduce memorization. Use expected/predicted labels
and aggregate patterns to infer durable rules.

## Boundary Traps To Preserve

- `reliability` requires a changed recovery, retry, cleanup, lifecycle, hardening, timeout, leak,
  watchdog, or failure-handling mechanism, not just a crash, hang, flake, race, or message-loss symptom.
- `config` requires user/operator-facing settings, persisted config shape, validation, defaults, or
  policy settings, not a config key as another surface's internal mechanism.
- `telemetry_usage` requires OpenClaw's own accounting, diagnostics, traces, metrics, cost/usage, or
  status-reporting surface, not benchmark vocabulary beside another change.
- `tool_calling` requires model-facing tool-call protocol, schema, delta, replay, result, or call-ID
  behavior, not generic command output or ACP/session transport.
- `acp` owns message semantics and delivery; `sessions` owns stored session identity, lifecycle,
  state, transcript, persistence, resume/reset, cleanup, and stores.
- If Pi is OpenClaw's internal runner/backend/orchestration path, route to `agent_runtime`, not
  `coding_agent_integrations`. Use `coding_agent_integrations` only when OpenClaw's contract with an
  external coding-agent runtime or CLI changes.
