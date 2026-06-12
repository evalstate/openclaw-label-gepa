# OpenClaw easy-set stability report

Rows: `50`  Repeats: `2`

## Prediction stability

- pairwise exact: `0.900`
- pairwise Jaccard: `0.967`
- pairwise symdiff: `0.100`

## Buckets

- `stable_wrong`: 45
- `unstable_boundary`: 5

## Repeat metric summary

- `avg_expected_topics`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `avg_predicted_topics`: mean `2.5100`, pstdev `0.0300`, values `[2.54, 2.48]`
- `avg_row_jaccard`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `avg_row_symdiff`: mean `2.5100`, pstdev `0.0300`, values `[2.54, 2.48]`
- `exact_match`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `gepa_score`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `row_exact_accuracy`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `row_symdiff_score`: mean `0.2849`, pstdev `0.0024`, values `[0.2825, 0.2874]`
- `topic_micro_f1`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `topic_micro_precision`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `topic_micro_recall`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0]`
- `valid_json`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0]`

## Least stable / review rows

### 1. openclaw-openclaw-47285 — unstable_boundary

Title: feat(memory-lancedb): native Azure OpenAI support

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['inference_api', 'memory', 'skills_plugins'], 'count': 1}, {'topics': ['inference_api', 'memory'], 'count': 1}]`

FP: `[('inference_api', 2), ('memory', 2), ('skills_plugins', 1)]`

FN: `[]`

Volatile: `[('skills_plugins', 1)]`

- repeat 1: `['inference_api', 'memory', 'skills_plugins']` exact=False
- repeat 2: `['inference_api', 'memory']` exact=False

### 2. openclaw-openclaw-84038 — unstable_boundary

Title: [Bug]: doctor --fix silently migrates intentional openai-codex/ config to openai/, breaking PI+OAuth runtime and causing 3-4x token inflation

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['codex', 'config', 'model_lifecycle'], 'count': 1}, {'topics': ['codex', 'config'], 'count': 1}]`

FP: `[('codex', 2), ('config', 2), ('model_lifecycle', 1)]`

FN: `[]`

Volatile: `[('model_lifecycle', 1)]`

- repeat 1: `['codex', 'config', 'model_lifecycle']` exact=False
- repeat 2: `['codex', 'config']` exact=False

### 3. openclaw-openclaw-84570 — unstable_boundary

Title: Remove skill prelude exec allowlist

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['approvals', 'exec_tools', 'skills_plugins'], 'count': 1}, {'topics': ['approvals', 'exec_tools'], 'count': 1}]`

FP: `[('approvals', 2), ('exec_tools', 2), ('skills_plugins', 1)]`

FN: `[]`

Volatile: `[('skills_plugins', 1)]`

- repeat 1: `['approvals', 'exec_tools', 'skills_plugins']` exact=False
- repeat 2: `['approvals', 'exec_tools']` exact=False

### 4. openclaw-openclaw-84648 — unstable_boundary

Title: Add SafeOps preflight hook for exec tool

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['exec_tools', 'hooks', 'security'], 'count': 1}, {'topics': ['exec_tools', 'security'], 'count': 1}]`

FP: `[('exec_tools', 2), ('security', 2), ('hooks', 1)]`

FN: `[]`

Volatile: `[('hooks', 1)]`

- repeat 1: `['exec_tools', 'hooks', 'security']` exact=False
- repeat 2: `['exec_tools', 'security']` exact=False

### 5. openclaw-openclaw-84681 — unstable_boundary

Title: fix(codex): stabilize heartbeat dynamic tool schema

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['codex', 'tool_calling'], 'count': 1}, {'topics': ['codex', 'sessions', 'tool_calling'], 'count': 1}]`

FP: `[('codex', 2), ('tool_calling', 2), ('sessions', 1)]`

FN: `[]`

Volatile: `[('sessions', 1)]`

- repeat 1: `['codex', 'tool_calling']` exact=False
- repeat 2: `['codex', 'sessions', 'tool_calling']` exact=False

### 6. openclaw-openclaw-39714 — stable_wrong

Title: Sandbox: fix Dockerized browser bridge and tab creation

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['browser_automation', 'config', 'sandboxing'], 'count': 2}]`

FP: `[('browser_automation', 2), ('config', 2), ('sandboxing', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['browser_automation', 'config', 'sandboxing']` exact=False
- repeat 2: `['browser_automation', 'config', 'sandboxing']` exact=False

### 7. openclaw-openclaw-42606 — stable_wrong

Title: Browser: harden noVNC bootstrap headers

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['browser_automation', 'security'], 'count': 2}]`

FP: `[('browser_automation', 2), ('security', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['browser_automation', 'security']` exact=False
- repeat 2: `['browser_automation', 'security']` exact=False

### 8. openclaw-openclaw-43246 — stable_wrong

Title: fix(message): deny same-provider cross-context sends by default [AI-assisted]

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'notifications', 'security'], 'count': 2}]`

FP: `[('config', 2), ('notifications', 2), ('security', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'notifications', 'security']` exact=False
- repeat 2: `['config', 'notifications', 'security']` exact=False

### 9. openclaw-openclaw-44202 — stable_wrong

Title: [Bug]: local memory embeddings on Apple Silicon can crash gateway in ggml-metal / node-llama-cpp; need official Metal/GPU guidance

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['memory', 'reliability', 'self_hosted_inference'], 'count': 2}]`

FP: `[('memory', 2), ('reliability', 2), ('self_hosted_inference', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['memory', 'reliability', 'self_hosted_inference']` exact=False
- repeat 2: `['memory', 'reliability', 'self_hosted_inference']` exact=False

### 10. openclaw-openclaw-47187 — stable_wrong

Title: fix(ui): reset transient chat overlays and style context notice

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['ui_tui'], 'count': 2}]`

FP: `[('ui_tui', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['ui_tui']` exact=False
- repeat 2: `['ui_tui']` exact=False

### 11. openclaw-openclaw-47446 — stable_wrong

Title: fix(gateway/discord): respect env proxy vars and prevent ECONNRESET

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'gateway', 'reliability'], 'count': 2}]`

FP: `[('chat_integrations', 2), ('gateway', 2), ('reliability', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'gateway', 'reliability']` exact=False
- repeat 2: `['chat_integrations', 'gateway', 'reliability']` exact=False

### 12. openclaw-openclaw-48260 — stable_wrong

Title: feat(ui): add active time summary to usage overview

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['telemetry_usage', 'ui_tui'], 'count': 2}]`

FP: `[('telemetry_usage', 2), ('ui_tui', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['telemetry_usage', 'ui_tui']` exact=False
- repeat 2: `['telemetry_usage', 'ui_tui']` exact=False

### 13. openclaw-openclaw-49310 — stable_wrong

Title: fix: keep tui busy during follow-up waits

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['ui_tui'], 'count': 2}]`

FP: `[('ui_tui', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['ui_tui']` exact=False
- repeat 2: `['ui_tui']` exact=False

### 14. openclaw-openclaw-57597 — stable_wrong

Title: fix(acp): persist spawn labels in target session store

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'sessions'], 'count': 2}]`

FP: `[('acp', 2), ('sessions', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'sessions']` exact=False
- repeat 2: `['acp', 'sessions']` exact=False

### 15. openclaw-openclaw-58411 — stable_wrong

Title: sessions_spawn lacks --bind here equivalent — agent cannot bind ACP session to existing Discord thread

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'chat_integrations', 'tool_calling'], 'count': 2}]`

FP: `[('acp', 2), ('chat_integrations', 2), ('tool_calling', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'chat_integrations', 'tool_calling']` exact=False
- repeat 2: `['acp', 'chat_integrations', 'tool_calling']` exact=False

### 16. openclaw-openclaw-59878 — stable_wrong

Title: Session lane stuck in 'running' after run dies — sessions.abort + gateway restart fail to clear stale state

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['queueing', 'reliability', 'sessions'], 'count': 2}]`

FP: `[('queueing', 2), ('reliability', 2), ('sessions', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['queueing', 'reliability', 'sessions']` exact=False
- repeat 2: `['queueing', 'reliability', 'sessions']` exact=False

### 17. openclaw-openclaw-62769 — stable_wrong

Title: [Feature]: Support ACP configured bindings for Telegram DMs (not just groups/topics)

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'chat_integrations'], 'count': 2}]`

FP: `[('acp', 2), ('chat_integrations', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'chat_integrations']` exact=False
- repeat 2: `['acp', 'chat_integrations']` exact=False

### 18. openclaw-openclaw-63007 — stable_wrong

Title: Pass outbound session identity into message_sending and surface guarded gateway send denial

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['gateway', 'hooks', 'notifications'], 'count': 2}]`

FP: `[('gateway', 2), ('hooks', 2), ('notifications', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['gateway', 'hooks', 'notifications']` exact=False
- repeat 2: `['gateway', 'hooks', 'notifications']` exact=False

### 19. openclaw-openclaw-64718 — stable_wrong

Title: fix(security): default exec to deny for non-owner auto-reply senders

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['approvals', 'exec_tools', 'security'], 'count': 2}]`

FP: `[('approvals', 2), ('exec_tools', 2), ('security', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['approvals', 'exec_tools', 'security']` exact=False
- repeat 2: `['approvals', 'exec_tools', 'security']` exact=False

### 20. openclaw-openclaw-65187 — stable_wrong

Title: test: add regression tests for <final> tag stripping in UI message extraction

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['tests_ci'], 'count': 2}]`

FP: `[('tests_ci', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['tests_ci']` exact=False
- repeat 2: `['tests_ci']` exact=False

### 21. openclaw-openclaw-65364 — stable_wrong

Title: feat(plugins): add registerProviderRuntimeAuthOverride API

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['inference_api', 'security', 'skills_plugins'], 'count': 2}]`

FP: `[('inference_api', 2), ('security', 2), ('skills_plugins', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['inference_api', 'security', 'skills_plugins']` exact=False
- repeat 2: `['inference_api', 'security', 'skills_plugins']` exact=False

### 22. openclaw-openclaw-66327 — stable_wrong

Title: feat(msteams): implement sendPayload for interactive approval cards

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['approvals', 'chat_integrations', 'notifications'], 'count': 2}]`

FP: `[('approvals', 2), ('chat_integrations', 2), ('notifications', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['approvals', 'chat_integrations', 'notifications']` exact=False
- repeat 2: `['approvals', 'chat_integrations', 'notifications']` exact=False

### 23. openclaw-openclaw-68187 — stable_wrong

Title: SSE-backed MCP sessions can stay stale after server restart and fail with 'Session not found'

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['mcp_tooling', 'reliability'], 'count': 2}]`

FP: `[('mcp_tooling', 2), ('reliability', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['mcp_tooling', 'reliability']` exact=False
- repeat 2: `['mcp_tooling', 'reliability']` exact=False

### 24. openclaw-openclaw-69256 — stable_wrong

Title: fix(cron): prevent premature session cleanup when subagents are running

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['cron_automation', 'reliability', 'sessions'], 'count': 2}]`

FP: `[('cron_automation', 2), ('reliability', 2), ('sessions', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['cron_automation', 'reliability', 'sessions']` exact=False
- repeat 2: `['cron_automation', 'reliability', 'sessions']` exact=False

### 25. openclaw-openclaw-71594 — stable_wrong

Title: docs(gateway): clarify IPv4-only BYOH bind path

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['docs', 'gateway'], 'count': 2}]`

FP: `[('docs', 2), ('gateway', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['docs', 'gateway']` exact=False
- repeat 2: `['docs', 'gateway']` exact=False

### 26. openclaw-openclaw-72001 — stable_wrong

Title: fix(hooks): write allowedSessionKeyPrefixes from gmail wizard

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'hooks'], 'count': 2}]`

FP: `[('config', 2), ('hooks', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'hooks']` exact=False
- repeat 2: `['config', 'hooks']` exact=False

### 27. openclaw-openclaw-72016 — stable_wrong

Title: [Feature]: doctor api/extendability

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['skills_plugins'], 'count': 2}]`

FP: `[('skills_plugins', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['skills_plugins']` exact=False
- repeat 2: `['skills_plugins']` exact=False

### 28. openclaw-openclaw-72262 — stable_wrong

Title: docs: add WhatsApp 408 disconnect troubleshooting runbook

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'docs', 'reliability'], 'count': 2}]`

FP: `[('chat_integrations', 2), ('docs', 2), ('reliability', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'docs', 'reliability']` exact=False
- repeat 2: `['chat_integrations', 'docs', 'reliability']` exact=False

### 29. openclaw-openclaw-74204 — stable_wrong

Title: memory.qmd.update.embedTimeoutMs default (120 s) is too low for local GGUF; error message doesn't surface the fix

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'memory', 'self_hosted_inference'], 'count': 2}]`

FP: `[('config', 2), ('memory', 2), ('self_hosted_inference', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'memory', 'self_hosted_inference']` exact=False
- repeat 2: `['config', 'memory', 'self_hosted_inference']` exact=False

### 30. openclaw-openclaw-74305 — stable_wrong

Title: [Bug]: ACPX Codex worker fails when model/thinking overrides are configured

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['acpx', 'codex'], 'count': 2}]`

FP: `[('acpx', 2), ('codex', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acpx', 'codex']` exact=False
- repeat 2: `['acpx', 'codex']` exact=False
