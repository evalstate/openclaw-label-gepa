# V7E Mutable Definitions Regime

V7E tests whether the fixed topic-definition wording is holding back GEPA.

The schema enum, topic IDs, label order, scoring, data splits, static ASI, and task boundary overlay are inherited from `v7d-final`. The new mutable GEPA component is `topic_definitions`, seeded from `v7d-final/prompts/allowed-topics-v7d.md`.

Candidates that add, remove, duplicate, rename, or omit topic definition bullets score zero. The intended mutation is wording nuance only: centrality, exclusions, and label-boundary alignment for the existing topic IDs.
