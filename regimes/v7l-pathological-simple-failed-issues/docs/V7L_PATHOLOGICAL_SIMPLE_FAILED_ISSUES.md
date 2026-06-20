# V7L Pathological Simple Failed-Issues Ablation

This regime reuses the v7k data/schema but starts from a deliberately minimal task prompt:
choose up to three labels from the topic ID list for the supplied GitHub issue.

Only `policy` is mutable. The task-facing prompt does not include topic definitions,
boundary overlays, or routing rules. Reflection uses the `failed-issues` profile.
