# Benchmark Eligibility Policy v6f

This policy is a post-pass over teacher outputs. It must not change, suppress,
or add topic labels. The teacher decides what labels are true; this policy only
decides whether a labelled row is suitable for easy-set train/test use.

## Inputs

- teacher labels, bucket, confidence, ambiguity, and `needs_human_review`
- stability/consensus metadata across repeated teacher runs
- label-count and low-support/high-confusion topic checks

## Deterministic Exclusions

Exclude from automatic train/test selection when any of these are true:

- teacher output is invalid or incomplete
- no cross-model accepted consensus exists
- any accepted modal label set has more than 3 labels, unless manually approved
- any teacher run sets `needs_human_review`
- ambiguity is `high`
- confidence is below the easy-set threshold chosen for the split
- GPT/Opus modal labels disagree
- repeated runs are not exact-stable for the model family required by the split

## Review-First Topics

Rows containing these topics should require manual review before train/test
selection unless later data shows stable support:

- `coding_agent_integrations`
- `model_lifecycle`
- `skills_plugins`
- `sandboxing`
- `queueing`
- `tool_calling`
- `auth_identity`
- `codex`

These topics remain valid labels. Their presence affects only benchmark
eligibility, not teacher labelling.
