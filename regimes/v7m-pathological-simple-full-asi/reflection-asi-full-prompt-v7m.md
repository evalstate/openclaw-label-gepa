# Prompt-Focused Reflection ASI

Use this as optimizer/reflection side information only. Do not insert it verbatim into the task prompt.

## Optimization Target

Optimize exact topic-set selection for OpenClaw maintainer-interest routing.

The task model starts with a deliberately minimal prompt: choose up to 3 labels from the allowed label list for the supplied GitHub issue. There are no task-facing topic definitions, boundary overlays, examples, or routing rules at the start of this ablation.

GEPA may edit only one text component. It is named `policy` internally for runner compatibility, but treat it as the entire task-facing prompt body.

The row score is:

```text
row_composite_score = 0.60*row_jaccard + 0.20*row_topic_f1 + 0.20*row_exact
final_score = max(0.0, row_composite_score - hygiene_penalty)
```

## Feedback Use

Use the evaluator side information as evidence: failed GitHub issue context, expected labels, chosen labels, false positives, false negatives, row metrics, minibatch label-error patterns, co-error patterns, prompt-hygiene warnings, and actionable feedback.

Prefer durable issue-understanding rules over label-name, filename, package-name, PR-label, or keyword triggers. Treat co-error pairs as directional hints, not as a formal substitution matrix. A proposal that fixes false negatives by adding weak secondary labels is likely to lose precision.

Reflection may infer and write useful label definitions, centrality rules, exclusion rules, and co-label guidance into the prompt when they are supported by minibatch evidence. Keep the rules general and task-facing.

## Edit Discipline

Allowed changes:

- rewrite the prompt body freely;
- add compact reusable rules that help choose among existing label IDs;
- clarify when to include or exclude labels based on issue content;
- add co-label guidance only when it is general and evidence-backed;
- remove duplicated or low-signal wording.

Forbidden changes:

- do not add, remove, rename, alias, reorder, or duplicate label IDs;
- do not add row IDs, issue numbers, exact titles, URLs, copied examples, or memorized examples;
- do not include corpus-building notes, experiment bookkeeping, or label-source bookkeeping;
- do not turn the prompt into a sampled-row repair table or one-off keyword table;
- do not add JSON schema text, output-format instructions, or provider-specific response-format instructions to the prompt.
