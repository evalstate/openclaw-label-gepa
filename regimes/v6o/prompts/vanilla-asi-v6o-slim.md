# OpenClaw reflection ASI

Use this as GEPA/reflection side information. Do not insert it verbatim into the
task AgentCard.

## Optimization target

Optimize exact topic membership for maintainer-interest routing against the
current reference labels: at most 3 topics per row, priority-ordered, selected by
the deliverable test. Label only surfaces whose behavior contract the item
changes.

For row-wise GEPA, the main sampled-row score is:

```text
0.70 * row_jaccard + 0.30 * row_exact
```

Jaccard is the primary partial-match signal because it measures the fraction of
the expected/predicted label union that was correct. Exact match is a hard bonus
for reproducing the whole row label set. Do not pad labels to improve apparent
recall; exact topic membership matters.

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
