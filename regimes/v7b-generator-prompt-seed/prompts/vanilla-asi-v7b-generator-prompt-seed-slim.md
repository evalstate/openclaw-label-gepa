# OpenClaw reflection ASI

Use this as GEPA/reflection side information. Do not insert it verbatim into the
task AgentCard.

## Optimization target

Optimize exact topic membership for maintainer-interest routing against the
current reference labels: at most 3 topics per row, priority-ordered, selected by
the deliverable test. Label only surfaces whose behavior contract the item
changes.

For v7b-generator-prompt-seed row-wise GEPA, the sampled-row score is softened to reduce exact-match
cliffs during search:

```text
0.60 * row_jaccard + 0.20 * row_topic_f1 + 0.20 * row_exact
```

Jaccard remains the primary set-overlap signal. Row topic F1 gives the optimizer
a smoother partial-credit signal when a mutation fixes precision or recall but
does not yet flip the whole row to exact. Exact match remains a meaningful bonus,
but it is not allowed to dominate early search.

This is an optimization ablation, not a benchmark relaxation. Continue to report
row-exact, row-Jaccard, micro-F1, and macro-F1 separately on Pareto and held-out
benchmarks.

The task model already sees the fixed taxonomy, the fixed boundary overlay, and
the deliverable test. The mutable candidate is an overlay on top of those fixed
inputs.

Hard constraints on the candidate policy:

- Do not restate topic definitions, the allowed-topic enum, cue-word lists, the
  deliverable test, or the cardinality law.
- Add only compact decision rules that change behavior beyond the fixed inputs:
  centrality tests, targeted boundary tie-breakers, suppression rules, and
  corrections for observed failure patterns.
- Keep the section structure of the seed policy: Decision Procedure,
  Cardinality Rules, Boundary Overlays, and Suppression Rules.
- Prefer editing or replacing an existing rule over appending a new one.
- Respect the fixed cardinality law: at most 3 topics, priority-ordered.
  Within that cap, include every central qualifying topic; do not trade clearly
  qualifying co-labels away for precision, and do not pad to 3 when fewer are
  central.
- Preserve the Pi/internal-runner distinction from the labeling task: if Pi is
  acting as OpenClaw's internal runner/backend/orchestration path, route to
  `agent_runtime`, not `coding_agent_integrations`; use
  `coding_agent_integrations` only when OpenClaw's contract with an external
  coding-agent runtime or CLI changes.
- Preserve these high-risk boundary traps when proposing policy mutations:
  `reliability` requires a changed recovery/retry/cleanup/lifecycle/hardening
  mechanism, not just a crash, hang, race, flake, or message-loss symptom;
  `config` requires user/operator-facing settings, persisted shape, validation,
  defaults, or policy settings, not a config key as another surface's internal
  mechanism; `telemetry_usage` requires OpenClaw's own accounting, diagnostics,
  traces, metrics, cost/usage, or status-reporting surface, not benchmark or
  measurement vocabulary next to another change; `tool_calling` requires
  model-facing tool-call protocol/schema/deltas/result handling, not generic
  command output or ACP/session transport; and `acp` owns message semantics and
  delivery while `sessions` owns stored session identity, lifecycle, state,
  transcript, persistence, resume/reset, cleanup, and stores.

## Using row-wise feedback

Reflection receives two levels of feedback:

- per-row errors: expected labels, actual labels, false positives, false
  negatives, and row metrics for the sampled rows;
- minibatch diagnostics: macro-F1 over active sampled labels, per-label
  over/under-application counts, and directional co-error pairs where a missed
  expected label and an extra predicted label appeared on the same row.

Use the minibatch diagnostics to decide whether a label is being over-applied,
under-applied, or involved in a reusable boundary error. Co-error pairs are not
a formal substitution matrix; they are evidence that two labels may need a
clearer ownership rule only when the same distinction generalizes.

Use the row-level feedback only to infer reusable centrality or boundary rules.
Do not memorize row IDs, issue numbers, exact titles, URLs, or copied examples.
Compact feedback intentionally omits exact row text to reduce row memorization;
expected labels, actual labels, false positives, and false negatives are the
signal to act on.

Do not assume suppression is higher value unless current false-positive evidence
supports it. Do not assume recall expansion is higher value unless current
false-negative evidence supports it. Preserve all central qualifying co-labels
up to the 3-label cap.


## v7b seed note

This regime starts from a distilled version of the gold-label generation/adjudication prompt.
The seed should preserve high precision while improving recall of explicit secondary owners.
Reflection should tune durable centrality rules, especially under-labelling, without rebuilding
the taxonomy or adding row-specific examples.
