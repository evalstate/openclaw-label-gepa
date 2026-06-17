# V6 pre-review packet: convergent model disagreements on v5 test gold

Source: runs/easy-set-v5 GEPA-best test repeats (3 models x 3 repeats). Each row
below has at least 2 of 3 models stably converging (modal prediction in >=2/3
repeats) on the same label set that differs from the current gold. In every case
the difference is a dropped gold co-label, so the question per row is whether the
co-label meets the v6 centrality bar (see co-label cardinality rules in
topic-boundary-guidance-v6.md).

For each row decide: KEEP gold (models under-label; the v6 guidance/cardinality
rules should teach it) or FLIP gold (the co-label was an anchoring/centrality
artifact). Record decisions in v6-prereview-decisions.jsonl as
{"id": ..., "decision": "keep|flip", "labels": [...], "note": ...}.

## openclaw-openclaw-52249

**Title:** ACP parent session stuck until refresh when yielded waiting for child completion

**Gold:** `['acp', 'queueing', 'reliability', 'sessions']`

- gpt-5.4-mini: `['acp', 'reliability', 'sessions']` (3/3 repeats)
- deepseek4: `['acp', 'agent_runtime', 'reliability', 'sessions']` (3/3 repeats)
- gemma-e4: `['acp', 'reliability', 'sessions']` (3/3 repeats)

**Disputed co-label(s):** `['queueing']`

<details><summary>Context excerpt</summary>

> GitHub item:
> - Repository: openclaw/openclaw
> - Type: issue
> - Number: 52249
> - URL: https://github.com/openclaw/openclaw/issues/52249
> - Title: ACP parent session stuck until refresh when yielded waiting for child completion
> - State: OPEN
> - Author: dapzthelegend
> - Labels: P1, clawsweeper:no-new-fix-pr, clawsweeper:fix-shape-clear, clawsweeper:needs-maintainer-review, clawsweeper:needs-product-decision, clawsweeper:source-repro, impact:session-state, impact:message-loss, issue-rating: 🦞 diamond lobster
> 
> Body:
> ```markdown
> When an ACP child session completes while a parent session is yielded waiting

</details>

## openclaw-openclaw-56613

**Title:** [Feature]: Talk/Voice tab — agent/session switching + per-agent TTS voice

**Gold:** `['config', 'sessions', 'ui_tui']`

- gpt-5.4-mini: `['sessions', 'ui_tui']` (3/3 repeats)
- deepseek4: `['sessions', 'ui_tui']` (3/3 repeats)
- gemma-e4: `['config', 'sessions', 'ui_tui']` (3/3 repeats)

**Disputed co-label(s):** `see per-model sets`

<details><summary>Context excerpt</summary>

> GitHub item:
> - Repository: openclaw/openclaw
> - Type: issue
> - Number: 56613
> - URL: https://github.com/openclaw/openclaw/issues/56613
> - Title: [Feature]: Talk/Voice tab — agent/session switching + per-agent TTS voice
> - State: OPEN
> - Author: kenchen3000
> - Labels: P3, clawsweeper:no-new-fix-pr, clawsweeper:fix-shape-clear, clawsweeper:needs-maintainer-review, clawsweeper:needs-product-decision, clawsweeper:source-repro, impact:session-state, issue-rating: 🦞 diamond lobster
> 
> Body:
> ```markdown
> ### Summary
> 
> Two related feature requests for the Android (and iOS/macOS) Talk/Voice mode:
> 
> ## 1. Voice/Tal

</details>

## openclaw-openclaw-66327

**Title:** feat(msteams): implement sendPayload for interactive approval cards

**Gold:** `['approvals', 'chat_integrations', 'notifications']`

- gpt-5.4-mini: `['approvals', 'chat_integrations']` (3/3 repeats)
- deepseek4: `['approvals', 'chat_integrations']` (2/3 repeats)
- gemma-e4: `['approvals', 'chat_integrations', 'reliability']` (3/3 repeats)

**Disputed co-label(s):** `['notifications']`

<details><summary>Context excerpt</summary>

> GitHub item:
> - Repository: openclaw/openclaw
> - Type: pull_request
> - Number: 66327
> - URL: https://github.com/openclaw/openclaw/pull/66327
> - Title: feat(msteams): implement sendPayload for interactive approval cards
> - State: OPEN
> - Author: johnturek
> - Labels: channel: msteams, size: M, triage: needs-real-behavior-proof, P2, rating: 🧂 unranked krab, merge-risk: 🚨 message-delivery, status: 📣 needs proof
> - Changed file count available to wrapper: 3
> - Changed files: extensions/msteams/src/channel.ts, extensions/msteams/src/outbound.test.ts, extensions/msteams/src/outbound.ts
> 
> Body:
> ```markdown
> ## Su

</details>

## openclaw-openclaw-70882

**Title:** fix(bundle-mcp): coerce stringified object/array params before MCP tool calls

**Gold:** `['mcp_tooling', 'security', 'tool_calling']`

- gpt-5.4-mini: `['mcp_tooling', 'security']` (2/3 repeats)
- deepseek4: `['mcp_tooling', 'security']` (2/3 repeats)
- gemma-e4: `['mcp_tooling', 'security', 'tool_calling']` (3/3 repeats)

**Disputed co-label(s):** `see per-model sets`

<details><summary>Context excerpt</summary>

> GitHub item:
> - Repository: openclaw/openclaw
> - Type: pull_request
> - Number: 70882
> - URL: https://github.com/openclaw/openclaw/pull/70882
> - Title: fix(bundle-mcp): coerce stringified object/array params before MCP tool calls
> - State: OPEN
> - Author: Sanjays2402
> - Labels: agents, size: M, triage: needs-real-behavior-proof, P2, rating: 🧂 unranked krab, merge-risk: 🚨 compatibility, status: 📣 needs proof
> - Changed file count available to wrapper: 3
> - Changed files: CHANGELOG.md, src/agents/pi-bundle-mcp-materialize.ts, src/agents/pi-bundle-mcp-tools.materialize.test.ts
> 
> Body:
> ```markdown
> ## Summary
> 

</details>

## openclaw-openclaw-71648

**Title:** fix(mcp): bound pendingClaudePermissions / pendingApprovals via TTL sweeper + close clear

**Gold:** `['approvals', 'mcp_tooling', 'reliability']`

- gpt-5.4-mini: `['mcp_tooling', 'reliability']` (3/3 repeats)
- deepseek4: `['approvals', 'mcp_tooling', 'reliability']` (2/3 repeats)
- gemma-e4: `['mcp_tooling', 'reliability']` (2/3 repeats)

**Disputed co-label(s):** `see per-model sets`

<details><summary>Context excerpt</summary>

> GitHub item:
> - Repository: openclaw/openclaw
> - Type: pull_request
> - Number: 71648
> - URL: https://github.com/openclaw/openclaw/pull/71648
> - Title: fix(mcp): bound pendingClaudePermissions / pendingApprovals via TTL sweeper + close clear
> - State: OPEN
> - Author: Feelw00
> - Labels: size: M, proof: supplied, proof: sufficient, P2, rating: 🐚 platinum hermit, merge-risk: 🚨 compatibility, status: 👀 ready for maintainer look
> - Changed file count available to wrapper: 3
> - Changed files: src/mcp/channel-bridge.test.ts, src/mcp/channel-bridge.ts, src/mcp/channel-server.test.ts
> 
> Body:
> ```markdown
> ## Summary

</details>

## openclaw-openclaw-72262

**Title:** docs: add WhatsApp 408 disconnect troubleshooting runbook

**Gold:** `['chat_integrations', 'docs', 'reliability']`

- gpt-5.4-mini: `['chat_integrations', 'docs']` (3/3 repeats)
- deepseek4: `['chat_integrations', 'docs']` (3/3 repeats)
- gemma-e4: `['docs']` (3/3 repeats)

**Disputed co-label(s):** `['reliability']`

<details><summary>Context excerpt</summary>

> GitHub item:
> - Repository: openclaw/openclaw
> - Type: issue
> - Number: 72262
> - URL: https://github.com/openclaw/openclaw/issues/72262
> - Title: docs: add WhatsApp 408 disconnect troubleshooting runbook
> - State: OPEN
> - Author: Iman-Sharif
> - Labels: P3, clawsweeper:no-new-fix-pr, clawsweeper:source-repro, clawsweeper:linked-pr-open, issue-rating: 🦞 diamond lobster
> 
> Body:
> ```markdown
> ## Problem
> 
> The current WhatsApp/channel troubleshooting docs mention random disconnect/relogin loops, but the guidance is too shallow for the common Baileys/WhatsApp Web failure signature:
> 
> ```text
> WhatsApp default: en

</details>

## openclaw-openclaw-74305

**Title:** [Bug]: ACPX Codex worker fails when model/thinking overrides are configured

**Gold:** `['acp', 'acpx', 'codex', 'reliability']`

- gpt-5.4-mini: `['acpx', 'codex', 'reliability']` (2/3 repeats)
- deepseek4: `['acpx', 'codex', 'config', 'reliability']` (2/3 repeats)
- gemma-e4: `['acpx', 'codex', 'reliability']` (3/3 repeats)

**Disputed co-label(s):** `['acp']`

<details><summary>Context excerpt</summary>

> GitHub item:
> - Repository: openclaw/openclaw
> - Type: issue
> - Number: 74305
> - URL: https://github.com/openclaw/openclaw/issues/74305
> - Title: [Bug]: ACPX Codex worker fails when model/thinking overrides are configured
> - State: OPEN
> - Author: SimSef
> - Labels: bug, bug:crash
> 
> Body:
> ```markdown
> ### Bug type
> 
> Crash (process/app exits or hangs)
> 
> ### Beta release blocker
> 
> No
> 
> ### Summary
> 
> Codex ACP worker runs succeed without internal model/thinking overrides, but fail with AcpRuntimeError: Internal error when model and model_reasoning_effort overrides are passed to codex-acp.
> 
> ### Steps to reproduce

</details>

## openclaw-openclaw-83333

**Title:** [Bug]: Memory provider cutover to Ollama leaves production index in mixed OpenAI/Ollama vector state after live sync/reload

**Gold:** `['memory', 'reliability', 'self_hosted_inference']`

- gpt-5.4-mini: `['config', 'memory', 'reliability']` (2/3 repeats)
- deepseek4: `['memory', 'reliability']` (2/3 repeats)
- gemma-e4: `['config', 'memory', 'reliability']` (3/3 repeats)

**Disputed co-label(s):** `['self_hosted_inference']`

<details><summary>Context excerpt</summary>

> GitHub item:
> - Repository: openclaw/openclaw
> - Type: issue
> - Number: 83333
> - URL: https://github.com/openclaw/openclaw/issues/83333
> - Title: [Bug]: Memory provider cutover to Ollama leaves production index in mixed OpenAI/Ollama vector state after live sync/reload
> - State: OPEN
> - Author: jacka-L
> - Labels: bug, P2, clawsweeper:needs-live-repro, impact:session-state, impact:auth-provider
> 
> Body:
> ```markdown
> ### Bug type
> 
> Crash (process/app exits or hangs)
> 
> ### Beta release blocker
> 
> No
> 
> ### Summary
> 
> # Bug: Memory provider cutover to Ollama leaves production index in mixed OpenAI/Ollama vector stat

</details>

