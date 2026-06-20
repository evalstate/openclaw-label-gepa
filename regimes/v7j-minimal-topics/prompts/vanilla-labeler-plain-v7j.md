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

Classify the GitHub issue from these topics. Use between 0 and 3 labels.

Return only the selected topic IDs separated by commas.

{{topic_definitions}}

{{policy}}
