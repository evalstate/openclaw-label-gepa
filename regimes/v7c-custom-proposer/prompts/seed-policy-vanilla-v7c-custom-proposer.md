Classify the GitHub issue or pull request for OpenClaw maintainer-interest routing.

Use only the supplied GitHub context and the fixed topic taxonomy. Choose labels by central
maintainer-routing concern, not by keyword match, file path, PR label, test name, package name,
or incidental implementation detail.

Ask what behavior, contract, artifact, lifecycle, integration, or operator-visible surface would
need maintainer ownership if this lands. Include every central label when multiple independent
maintainer-owned concerns are explicit. Do not collapse a multi-surface row to one broad label
when 2-3 separate surfaces have their own acceptance condition.

Default to 1-3 topics in priority order, with the primary changed surface first. Do not pad.
Add a secondary label only when the item explicitly changes that surface's own contract, not
merely because that surface transports, hosts, logs, tests, documents, configures, or implements
another change. Return an empty list only if no allowed topic centrally applies.

Use the generation/adjudication standard, adapted for vanilla inference: be conservative about
false positives, but do not require an "easy row" confidence threshold before adding a clearly
central secondary owner. If the evidence explicitly says a second or third maintainer surface
changes, include it.

High-risk checks before finalizing:
- If delivery involves an external chat/channel, scheduled job, and delivered notification content,
  keep all independently changed owners rather than reducing to a generic API or cron label.
- If a report/system prompt/tool inventory exposes Codex, MCP tools, and usage/diagnostic summary
  behavior, keep the central secondary owners rather than returning only the broad product name.
- If command execution, approval policy, and skill/plugin behavior all change, include each central
  owner; do not hide approval or skill/plugin changes under exec alone.

Return only the required JSON, with no rationale.
