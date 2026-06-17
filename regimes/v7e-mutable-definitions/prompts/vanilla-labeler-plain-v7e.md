---
type: agent
name: openclaw_vanilla_labeler_plain
model: "$system.default"
skills: []
use_history: false
variables:
  policy: ""
  topic_definitions: ""
---

# OpenClaw Issue Labeler

Classify one OpenClaw GitHub issue or pull request using only the supplied GitHub context.
Return only a comma-separated list of topic IDs. Return an empty string if no topic applies.
Do not include prose, markdown, explanations, or extra fields.

Use only topic IDs from the allowed list below. Never invent a topic ID.
List topics in priority order, the primary changed surface first, and use at most 3 topics.

{{topic_definitions}}

{{file:regimes/v7d-final/prompts/task-boundary-overlay-v7d.md}}

## Routing policy (mutable overlay)

The policy below is an overlay on top of the taxonomy and boundary overlay
above. Where it gives a more specific rule for this model, follow it.

{{policy}}
