# V7M Pathological Simple Full-ASI Ablation

This regime keeps the v7l pathologically simple task seed but gives reflection a richer actionable packet.

- Task seed: choose up to 3 labels from the allowed label list.
- No task-facing definitions, boundary overlays, examples, routing rules, or JSON wording in the seed prompt.
- Internal mutable component remains `policy` for runner compatibility, but it represents the entire prompt body.
- Reflection profile: `failed-issues-asi`, which expands only failed GitHub issues and includes expected/chosen labels, row diagnostics, and minibatch actionable label-error summaries.
