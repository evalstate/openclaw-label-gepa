# OpenClaw GEPA Reflection ASI

Use this as reflection side information only. Do not insert it verbatim into the task AgentCard.

## Optimization Target

Optimize exact topic-set selection for OpenClaw maintainer-interest routing. The task model sees
a fixed output contract plus three mutable task-facing components:

- `topic_definitions`: the allowed topic list and definitions. Topic IDs are frozen.
- `boundary_overlay`: reusable boundary and co-label guidance.
- `policy`: the compact generator/adjudication routing policy.

The goal is not to make all components longer. It is to allocate the available prompt budget across
the components that need wording changes.

The sampled-row scorer is:

```text
row_composite_score = 0.60*row_jaccard + 0.20*row_topic_f1 + 0.20*row_exact
gepa_score = max(0.0, row_composite_score - hygiene_penalty - total_mutable_length_penalty)
```

The original generator prompt is intentionally allowed to start slightly over the combined mutable
budget. Mutations should compress, merge, or replace wording rather than moving bloat from one
component to another.

## Mutation Discipline

Preserve the generator-prompt behavior that worked well for deepseek4flash: high precision,
central maintainer ownership, and willingness to include explicit secondary owners. The current
main failure mode is under-labelling: missing central secondary labels more often than adding extra
labels.

Allowed changes:

- clarify topic definitions while keeping the exact topic IDs and one bullet per topic;
- revise the boundary overlay when a reusable boundary or co-label rule belongs there;
- revise the routing policy when the rule is model-facing adjudication behavior;
- remove duplicated guidance when two components say the same thing.

Forbidden changes:

- do not add, remove, rename, alias, or duplicate topic IDs;
- do not add row IDs, issue numbers, exact titles, URLs, or memorized examples;
- do not include data-build notes, split names, teacher/adjudication bookkeeping, or GEPA run names;
- do not turn the prompt into a keyword table or a sampled-row repair table.

Use compact feedback as evidence about reusable over/under-labeling patterns. Treat co-error pairs
as directional hints, not as a formal substitution matrix.
