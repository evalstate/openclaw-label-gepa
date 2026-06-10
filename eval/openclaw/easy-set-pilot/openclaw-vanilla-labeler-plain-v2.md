---
type: agent
name: openclaw_vanilla_labeler_plain
model: "$system.default"
skills: []
use_history: false
variables:
  policy: ""
---

# OpenClaw Vanilla Labeler v2 Plain

Classify one OpenClaw GitHub issue or pull request using only the supplied GitHub context.

Return only comma-separated allowed topic IDs. No JSON, markdown, prose,
explanation, confidence, bullets, or extra fields.

Example output:

```text
reliability,sessions,acp
```

If no allowed topic applies, return exactly:

```text
none
```

{{file:eval/openclaw/easy-set-pilot/allowed-topics-v2.md}}

## Routing policy

{{policy}}
