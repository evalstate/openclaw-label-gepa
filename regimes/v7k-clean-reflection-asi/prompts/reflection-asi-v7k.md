# OpenClaw Reflection ASI

Use this as reflection side information only. Do not insert it verbatim into the task prompt.

## Optimization Target

Optimize exact topic-set selection for OpenClaw maintainer-interest routing. The task model sees
an output contract plus three editable task-facing guidance components:

- `topic_definitions`: the topic IDs and definitions. Topic IDs are fixed.
- `boundary_overlay`: reusable boundary and co-label guidance.
- `policy`: compact routing behavior.

The goal is not to make every component longer. Allocate the available prompt budget across the
components that need wording changes, remove duplicated guidance, and keep topic meanings stable.

The row score is:

```text
row_composite_score = 0.60*row_jaccard + 0.20*row_topic_f1 + 0.20*row_exact
final_score = max(0.0, row_composite_score - hygiene_penalty - total_mutable_length_penalty)
```

## Feedback Use

Use the evaluator side information as evidence: expected vs actual labels, false positives, false
negatives, row metrics, over-applied and under-applied topics, co-error patterns, prompt-hygiene
warnings, and aggregate diagnostics. Compact feedback may omit row identifiers or long examples;
do not infer that omitted rows or omitted topic details are absent errors.

Treat co-error pairs as directional hints, not as a formal substitution matrix. Prefer durable
issue-understanding rules over label-name, filename, package-name, PR-label, or keyword triggers.
A proposal that fixes false negatives by adding weak secondary labels is likely to lose precision.

## Edit Discipline

Allowed changes:

- clarify topic definitions while keeping the exact topic IDs and one definition per topic;
- revise the boundary overlay when a reusable boundary or co-label rule belongs there;
- revise the routing policy when the rule is model-facing routing behavior;
- remove duplicated guidance when two components say the same thing.

Forbidden changes:

- do not add, remove, rename, alias, reorder, or duplicate topic IDs;
- do not add row IDs, issue numbers, exact titles, URLs, copied examples, or memorized examples;
- do not include corpus-building notes, experiment bookkeeping, or label-source bookkeeping;
- do not turn the prompt into a keyword table, sampled-row repair table, or topic-by-topic trigger catalogue;
- do not add schema text or output-format instructions to topic definitions or boundary rules.
