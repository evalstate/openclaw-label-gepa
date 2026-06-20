# Policy-Only Reflection ASI

Use this as optimizer/reflection side information only. Do not insert it verbatim into the task prompt.

The task-facing seed prompt is intentionally minimal: it gives the model only a GitHub issue, a list
of allowed label IDs, and an instruction to choose up to 3 labels. There are no task-facing topic
definitions, boundary rules, examples, or routing rules at the start of this ablation.

GEPA may edit only the `policy` text. Improve it by deriving reusable labeling rules from failed
issues and their expected vs actual labels.

The row score is:

```text
row_composite_score = 0.60*row_jaccard + 0.20*row_topic_f1 + 0.20*row_exact
final_score = max(0.0, row_composite_score - hygiene_penalty)
```

Reflection feedback is intentionally sparse. For failed rows, use the issue context, expected labels,
actual/chosen labels, and row score to infer general rules.

Allowed changes:

- add compact, reusable policy rules that help choose among existing label IDs;
- clarify when to include or exclude labels based on issue content;
- add co-label guidance only when it is general and evidence-backed;
- keep the policy concise enough to remain useful as a task prompt.

Forbidden changes:

- do not add, remove, rename, alias, reorder, or duplicate label IDs;
- do not add row IDs, issue numbers, exact titles, URLs, copied examples, or memorized examples;
- do not turn the prompt into a sampled-row repair table or topic-by-topic keyword trigger catalogue;
- do not claim access to topic definitions or boundary guidance unless you wrote those rules into the policy.
