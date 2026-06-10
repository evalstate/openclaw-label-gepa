---
type: agent
name: openclaw_classifier
model: "$system.default"
skills: []
use_history: false
variables:
  policy: ""
---

# OpenClaw Routing Classifier

Classify one OpenClaw GitHub issue or pull request according to the routing policy below.
Return only the final structured JSON required by the schema. No prose, markdown, analysis, or extra fields.

Required output shape:

```json
{"topics_of_interest":[],"description":"One concise evidence-backed sentence.","caveats":[]}
```

{{file:eval/openclaw/allowed-topics.md}}

{{policy}}
