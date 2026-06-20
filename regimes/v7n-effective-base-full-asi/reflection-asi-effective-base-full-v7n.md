# Effective-Base Full Reflection ASI

Use this as optimizer/reflection side information only. Do not insert it verbatim into the task AgentCard.

## Optimization Target

Optimize exact topic-set selection for OpenClaw maintainer-interest routing. The task model starts from the strong v7h base prompt and sees three task-facing guidance components that GEPA may rewrite:

- `topic_definitions`: the allowed topic list and definitions. Topic IDs are frozen.
- `boundary_overlay`: reusable boundary and co-label guidance.
- `policy`: compact routing/adjudication behavior.

The goal is not to make every component longer. Allocate the prompt budget across the components that need wording changes, remove duplicated guidance, and preserve the high-performing central-maintainer-ownership behavior of the base prompt.

The sampled-row scorer is:

```text
row_composite_score = 0.60*row_jaccard + 0.20*row_topic_f1 + 0.20*row_exact
gepa_score = max(0.0, row_composite_score - hygiene_penalty - total_mutable_length_penalty)
```

## Feedback Use

Use the reflection payload as evidence: failed GitHub issue context, expected labels, chosen labels, false positives, false negatives, row metrics, minibatch label-error patterns, co-error patterns, prompt-hygiene warnings, and actionable feedback.

Prefer durable issue-understanding rules over label-name, filename, package-name, PR-label, test-name, or keyword triggers. Treat co-error pairs as directional hints, not as a formal substitution matrix. A proposal that fixes false negatives by adding weak secondary labels is likely to lose precision.

Preserve the v7h base prompt's useful behavior:

- label central maintainer-owned surfaces, not incidental implementation details;
- include explicit secondary owners when an issue changes multiple independent surfaces;
- avoid padding to three labels;
- keep topic IDs stable and definitions concise.

## Mutation Discipline

Allowed changes:

- clarify topic definitions while keeping the exact topic IDs and one definition per topic;
- revise the boundary overlay when a reusable boundary or co-label rule belongs there;
- revise the routing policy when the rule is model-facing routing behavior;
- remove duplicated or low-signal guidance when two components say the same thing.

Forbidden changes:

- do not add, remove, rename, alias, reorder, or duplicate topic IDs;
- do not add row IDs, issue numbers, exact titles, URLs, copied examples, or memorized examples;
- do not include data-build notes, split names, teacher/adjudication bookkeeping, experiment bookkeeping, or GEPA run names;
- do not turn the prompt into a keyword table, sampled-row repair table, or topic-by-topic trigger catalogue;
- do not add provider-specific response-format instructions to topic definitions or boundary rules.
