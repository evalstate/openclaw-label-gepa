# V7N Effective-Base Full-ASI Ablation

This regime starts from the strongest observed gpt-5.4-mini base prompt family, v7h, and runs GEPA with richer issue-context reflection.

- Initial task prompt/components: v7h base AgentCard, topic definitions, boundary overlay, and routing policy.
- Mutable components: `policy`, `topic_definitions`, and `boundary_overlay`.
- Reflection profile: `failed-issues-asi`, which expands only failed GitHub issues and includes expected/chosen labels, row diagnostics, and minibatch actionable label-error summaries.
- Splits: v7h feedback300 / pareto60 / bench78 for direct comparison to the v7h base 3x benchmark mean of 0.809586.
