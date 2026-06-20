---
type: agent
name: openclaw_vanilla_labeler
model: "$system.default"
skills: []
use_history: false
variables:
  policy: ""
  topic_definitions: ""
---

Classify the GitHub issue from these topics. Use between 0 and 3 labels.

{{topic_definitions}}

{{policy}}
