---
type: agent
name: openclaw_vanilla_labeler
model: "$system.default"
skills: []
use_history: false
variables:
  policy: ""
---

# OpenClaw Vanilla Labeler

Classify one OpenClaw GitHub issue or pull request using only the supplied GitHub context.
Return only the final structured JSON required by the schema. No prose, markdown, analysis, or extra fields.

Required output shape:

```json
{"topics_of_interest":[],"description":"One concise evidence-backed sentence.","caveats":[]}
```

Use only topic IDs from the allowed list below. Never invent a topic ID.

{{file:eval/openclaw/easy-set-pilot/v6/allowed-topics-v6.md}}

## Routing policy

{{policy}}
