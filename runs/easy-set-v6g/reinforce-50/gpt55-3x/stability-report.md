# OpenClaw easy-set stability report

Rows: `50`  Repeats: `3`

## Prediction stability

- pairwise exact: `0.840`
- pairwise Jaccard: `0.940`
- pairwise symdiff: `0.200`

## Buckets

- `review`: 9
- `stable_wrong`: 38
- `unstable_boundary`: 3

## Repeat metric summary

- `avg_expected_topics`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `avg_predicted_topics`: mean `2.5333`, pstdev `0.0094`, values `[2.54, 2.52, 2.54]`
- `avg_row_jaccard`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `avg_row_symdiff`: mean `2.5333`, pstdev `0.0094`, values `[2.54, 2.52, 2.54]`
- `exact_match`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `gepa_score`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `row_exact_accuracy`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `row_symdiff_score`: mean `0.2830`, pstdev `0.0008`, values `[0.2825, 0.2841, 0.2825]`
- `topic_micro_f1`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `topic_micro_precision`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `topic_micro_recall`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0, 1.0]`
- `valid_json`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0, 1.0]`

## Least stable / review rows

### 1. openclaw-openclaw-82596 — unstable_boundary

Title: Feature/exec denylist

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `2`

Most common predictions: `[{'topics': ['config', 'exec_tools', 'security'], 'count': 2}, {'topics': ['approvals', 'exec_tools', 'security'], 'count': 1}]`

FP: `[('exec_tools', 3), ('security', 3), ('config', 2), ('approvals', 1)]`

FN: `[]`

Volatile: `[('config', 2), ('approvals', 1)]`

- repeat 1: `['approvals', 'exec_tools', 'security']` exact=False
- repeat 2: `['config', 'exec_tools', 'security']` exact=False
- repeat 3: `['config', 'exec_tools', 'security']` exact=False

### 2. openclaw-openclaw-84709 — unstable_boundary

Title: fix(cron): fail closed when required tools are unavailable

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `2`

Most common predictions: `[{'topics': ['codex', 'cron_automation', 'exec_tools'], 'count': 2}, {'topics': ['codex', 'cron_automation', 'tool_calling'], 'count': 1}]`

FP: `[('codex', 3), ('cron_automation', 3), ('exec_tools', 2), ('tool_calling', 1)]`

FN: `[]`

Volatile: `[('exec_tools', 2), ('tool_calling', 1)]`

- repeat 1: `['codex', 'cron_automation', 'exec_tools']` exact=False
- repeat 2: `['codex', 'cron_automation', 'tool_calling']` exact=False
- repeat 3: `['codex', 'cron_automation', 'exec_tools']` exact=False

### 3. openclaw-openclaw-90146 — unstable_boundary

Title: google-vertex: Missing gemini-3.1-flash-lite in provider catalog causes silent failure instead of error

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `2`

Most common predictions: `[{'topics': ['inference_api', 'model_lifecycle', 'reliability'], 'count': 2}, {'topics': ['agent_runtime', 'model_lifecycle', 'reliability'], 'count': 1}]`

FP: `[('model_lifecycle', 3), ('reliability', 3), ('inference_api', 2), ('agent_runtime', 1)]`

FN: `[]`

Volatile: `[('inference_api', 2), ('agent_runtime', 1)]`

- repeat 1: `['agent_runtime', 'model_lifecycle', 'reliability']` exact=False
- repeat 2: `['inference_api', 'model_lifecycle', 'reliability']` exact=False
- repeat 3: `['inference_api', 'model_lifecycle', 'reliability']` exact=False

### 4. openclaw-openclaw-42606 — review

Title: Browser: harden noVNC bootstrap headers

Expected: `[]`

pairwise Jaccard `0.778`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.33`, unique sets `2`

Most common predictions: `[{'topics': ['browser_automation', 'security'], 'count': 2}, {'topics': ['api_surface', 'browser_automation', 'security'], 'count': 1}]`

FP: `[('browser_automation', 3), ('security', 3), ('api_surface', 1)]`

FN: `[]`

Volatile: `[('api_surface', 1)]`

- repeat 1: `['browser_automation', 'security']` exact=False
- repeat 2: `['browser_automation', 'security']` exact=False
- repeat 3: `['api_surface', 'browser_automation', 'security']` exact=False

### 5. openclaw-openclaw-47285 — review

Title: feat(memory-lancedb): native Azure OpenAI support

Expected: `[]`

pairwise Jaccard `0.778`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.33`, unique sets `2`

Most common predictions: `[{'topics': ['inference_api', 'memory'], 'count': 2}, {'topics': ['inference_api', 'memory', 'skills_plugins'], 'count': 1}]`

FP: `[('inference_api', 3), ('memory', 3), ('skills_plugins', 1)]`

FN: `[]`

Volatile: `[('skills_plugins', 1)]`

- repeat 1: `['inference_api', 'memory']` exact=False
- repeat 2: `['inference_api', 'memory']` exact=False
- repeat 3: `['inference_api', 'memory', 'skills_plugins']` exact=False

### 6. openclaw-openclaw-66327 — review

Title: feat(msteams): implement sendPayload for interactive approval cards

Expected: `[]`

pairwise Jaccard `0.778`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.67`, unique sets `2`

Most common predictions: `[{'topics': ['approvals', 'chat_integrations', 'notifications'], 'count': 2}, {'topics': ['approvals', 'chat_integrations'], 'count': 1}]`

FP: `[('approvals', 3), ('chat_integrations', 3), ('notifications', 2)]`

FN: `[]`

Volatile: `[('notifications', 2)]`

- repeat 1: `['approvals', 'chat_integrations', 'notifications']` exact=False
- repeat 2: `['approvals', 'chat_integrations', 'notifications']` exact=False
- repeat 3: `['approvals', 'chat_integrations']` exact=False

### 7. openclaw-openclaw-72001 — review

Title: fix(hooks): write allowedSessionKeyPrefixes from gmail wizard

Expected: `[]`

pairwise Jaccard `0.778`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.67`, unique sets `2`

Most common predictions: `[{'topics': ['config', 'hooks', 'security'], 'count': 2}, {'topics': ['config', 'hooks'], 'count': 1}]`

FP: `[('config', 3), ('hooks', 3), ('security', 2)]`

FN: `[]`

Volatile: `[('security', 2)]`

- repeat 1: `['config', 'hooks']` exact=False
- repeat 2: `['config', 'hooks', 'security']` exact=False
- repeat 3: `['config', 'hooks', 'security']` exact=False

### 8. openclaw-openclaw-81200 — review

Title: fix(acpx): strip provider API keys from child harness env

Expected: `[]`

pairwise Jaccard `0.778`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.33`, unique sets `2`

Most common predictions: `[{'topics': ['acpx', 'security'], 'count': 2}, {'topics': ['acpx', 'coding_agent_integrations', 'security'], 'count': 1}]`

FP: `[('acpx', 3), ('security', 3), ('coding_agent_integrations', 1)]`

FN: `[]`

Volatile: `[('coding_agent_integrations', 1)]`

- repeat 1: `['acpx', 'coding_agent_integrations', 'security']` exact=False
- repeat 2: `['acpx', 'security']` exact=False
- repeat 3: `['acpx', 'security']` exact=False

### 9. openclaw-openclaw-84038 — review

Title: [Bug]: doctor --fix silently migrates intentional openai-codex/ config to openai/, breaking PI+OAuth runtime and causing 3-4x token inflation

Expected: `[]`

pairwise Jaccard `0.778`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.67`, unique sets `2`

Most common predictions: `[{'topics': ['codex', 'config', 'model_lifecycle'], 'count': 2}, {'topics': ['codex', 'config'], 'count': 1}]`

FP: `[('codex', 3), ('config', 3), ('model_lifecycle', 2)]`

FN: `[]`

Volatile: `[('model_lifecycle', 2)]`

- repeat 1: `['codex', 'config', 'model_lifecycle']` exact=False
- repeat 2: `['codex', 'config']` exact=False
- repeat 3: `['codex', 'config', 'model_lifecycle']` exact=False

### 10. openclaw-openclaw-84648 — review

Title: Add SafeOps preflight hook for exec tool

Expected: `[]`

pairwise Jaccard `0.778`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.33`, unique sets `2`

Most common predictions: `[{'topics': ['exec_tools', 'security'], 'count': 2}, {'topics': ['exec_tools', 'hooks', 'security'], 'count': 1}]`

FP: `[('exec_tools', 3), ('security', 3), ('hooks', 1)]`

FN: `[]`

Volatile: `[('hooks', 1)]`

- repeat 1: `['exec_tools', 'security']` exact=False
- repeat 2: `['exec_tools', 'security']` exact=False
- repeat 3: `['exec_tools', 'hooks', 'security']` exact=False

### 11. openclaw-openclaw-84681 — review

Title: fix(codex): stabilize heartbeat dynamic tool schema

Expected: `[]`

pairwise Jaccard `0.778`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.67`, unique sets `2`

Most common predictions: `[{'topics': ['codex', 'security', 'tool_calling'], 'count': 2}, {'topics': ['codex', 'tool_calling'], 'count': 1}]`

FP: `[('codex', 3), ('tool_calling', 3), ('security', 2)]`

FN: `[]`

Volatile: `[('security', 2)]`

- repeat 1: `['codex', 'security', 'tool_calling']` exact=False
- repeat 2: `['codex', 'security', 'tool_calling']` exact=False
- repeat 3: `['codex', 'tool_calling']` exact=False

### 12. openclaw-openclaw-85999 — review

Title: [Bug]: 2026.5.22 gateway pre-warm (warmCurrentProviderAuthState) blocks event loop ~60s on startup, breaks channel handshakes

Expected: `[]`

pairwise Jaccard `0.778`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.67`, unique sets `2`

Most common predictions: `[{'topics': ['gateway', 'inference_api', 'reliability'], 'count': 2}, {'topics': ['gateway', 'reliability'], 'count': 1}]`

FP: `[('gateway', 3), ('reliability', 3), ('inference_api', 2)]`

FN: `[]`

Volatile: `[('inference_api', 2)]`

- repeat 1: `['gateway', 'inference_api', 'reliability']` exact=False
- repeat 2: `['gateway', 'inference_api', 'reliability']` exact=False
- repeat 3: `['gateway', 'reliability']` exact=False

### 13. openclaw-openclaw-39714 — stable_wrong

Title: Sandbox: fix Dockerized browser bridge and tab creation

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['browser_automation', 'config', 'sandboxing'], 'count': 3}]`

FP: `[('browser_automation', 3), ('config', 3), ('sandboxing', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['browser_automation', 'config', 'sandboxing']` exact=False
- repeat 2: `['browser_automation', 'config', 'sandboxing']` exact=False
- repeat 3: `['browser_automation', 'config', 'sandboxing']` exact=False

### 14. openclaw-openclaw-43246 — stable_wrong

Title: fix(message): deny same-provider cross-context sends by default [AI-assisted]

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'notifications', 'security'], 'count': 3}]`

FP: `[('config', 3), ('notifications', 3), ('security', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'notifications', 'security']` exact=False
- repeat 2: `['config', 'notifications', 'security']` exact=False
- repeat 3: `['config', 'notifications', 'security']` exact=False

### 15. openclaw-openclaw-44202 — stable_wrong

Title: [Bug]: local memory embeddings on Apple Silicon can crash gateway in ggml-metal / node-llama-cpp; need official Metal/GPU guidance

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['memory', 'reliability', 'self_hosted_inference'], 'count': 3}]`

FP: `[('memory', 3), ('reliability', 3), ('self_hosted_inference', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['memory', 'reliability', 'self_hosted_inference']` exact=False
- repeat 2: `['memory', 'reliability', 'self_hosted_inference']` exact=False
- repeat 3: `['memory', 'reliability', 'self_hosted_inference']` exact=False

### 16. openclaw-openclaw-47187 — stable_wrong

Title: fix(ui): reset transient chat overlays and style context notice

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['ui_tui'], 'count': 3}]`

FP: `[('ui_tui', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['ui_tui']` exact=False
- repeat 2: `['ui_tui']` exact=False
- repeat 3: `['ui_tui']` exact=False

### 17. openclaw-openclaw-47446 — stable_wrong

Title: fix(gateway/discord): respect env proxy vars and prevent ECONNRESET

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'gateway', 'reliability'], 'count': 3}]`

FP: `[('chat_integrations', 3), ('gateway', 3), ('reliability', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'gateway', 'reliability']` exact=False
- repeat 2: `['chat_integrations', 'gateway', 'reliability']` exact=False
- repeat 3: `['chat_integrations', 'gateway', 'reliability']` exact=False

### 18. openclaw-openclaw-48260 — stable_wrong

Title: feat(ui): add active time summary to usage overview

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['telemetry_usage', 'ui_tui'], 'count': 3}]`

FP: `[('telemetry_usage', 3), ('ui_tui', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['telemetry_usage', 'ui_tui']` exact=False
- repeat 2: `['telemetry_usage', 'ui_tui']` exact=False
- repeat 3: `['telemetry_usage', 'ui_tui']` exact=False

### 19. openclaw-openclaw-49310 — stable_wrong

Title: fix: keep tui busy during follow-up waits

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['ui_tui'], 'count': 3}]`

FP: `[('ui_tui', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['ui_tui']` exact=False
- repeat 2: `['ui_tui']` exact=False
- repeat 3: `['ui_tui']` exact=False

### 20. openclaw-openclaw-57597 — stable_wrong

Title: fix(acp): persist spawn labels in target session store

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'sessions'], 'count': 3}]`

FP: `[('acp', 3), ('sessions', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'sessions']` exact=False
- repeat 2: `['acp', 'sessions']` exact=False
- repeat 3: `['acp', 'sessions']` exact=False

### 21. openclaw-openclaw-58411 — stable_wrong

Title: sessions_spawn lacks --bind here equivalent — agent cannot bind ACP session to existing Discord thread

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'chat_integrations', 'tool_calling'], 'count': 3}]`

FP: `[('acp', 3), ('chat_integrations', 3), ('tool_calling', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'chat_integrations', 'tool_calling']` exact=False
- repeat 2: `['acp', 'chat_integrations', 'tool_calling']` exact=False
- repeat 3: `['acp', 'chat_integrations', 'tool_calling']` exact=False

### 22. openclaw-openclaw-59878 — stable_wrong

Title: Session lane stuck in 'running' after run dies — sessions.abort + gateway restart fail to clear stale state

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['queueing', 'reliability', 'sessions'], 'count': 3}]`

FP: `[('queueing', 3), ('reliability', 3), ('sessions', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['queueing', 'reliability', 'sessions']` exact=False
- repeat 2: `['queueing', 'reliability', 'sessions']` exact=False
- repeat 3: `['queueing', 'reliability', 'sessions']` exact=False

### 23. openclaw-openclaw-62769 — stable_wrong

Title: [Feature]: Support ACP configured bindings for Telegram DMs (not just groups/topics)

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'chat_integrations'], 'count': 3}]`

FP: `[('acp', 3), ('chat_integrations', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'chat_integrations']` exact=False
- repeat 2: `['acp', 'chat_integrations']` exact=False
- repeat 3: `['acp', 'chat_integrations']` exact=False

### 24. openclaw-openclaw-63007 — stable_wrong

Title: Pass outbound session identity into message_sending and surface guarded gateway send denial

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['gateway', 'hooks', 'notifications'], 'count': 3}]`

FP: `[('gateway', 3), ('hooks', 3), ('notifications', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['gateway', 'hooks', 'notifications']` exact=False
- repeat 2: `['gateway', 'hooks', 'notifications']` exact=False
- repeat 3: `['gateway', 'hooks', 'notifications']` exact=False

### 25. openclaw-openclaw-64718 — stable_wrong

Title: fix(security): default exec to deny for non-owner auto-reply senders

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['approvals', 'exec_tools', 'security'], 'count': 3}]`

FP: `[('approvals', 3), ('exec_tools', 3), ('security', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['approvals', 'exec_tools', 'security']` exact=False
- repeat 2: `['approvals', 'exec_tools', 'security']` exact=False
- repeat 3: `['approvals', 'exec_tools', 'security']` exact=False

### 26. openclaw-openclaw-65187 — stable_wrong

Title: test: add regression tests for <final> tag stripping in UI message extraction

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['tests_ci'], 'count': 3}]`

FP: `[('tests_ci', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['tests_ci']` exact=False
- repeat 2: `['tests_ci']` exact=False
- repeat 3: `['tests_ci']` exact=False

### 27. openclaw-openclaw-65364 — stable_wrong

Title: feat(plugins): add registerProviderRuntimeAuthOverride API

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['inference_api', 'security', 'skills_plugins'], 'count': 3}]`

FP: `[('inference_api', 3), ('security', 3), ('skills_plugins', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['inference_api', 'security', 'skills_plugins']` exact=False
- repeat 2: `['inference_api', 'security', 'skills_plugins']` exact=False
- repeat 3: `['inference_api', 'security', 'skills_plugins']` exact=False

### 28. openclaw-openclaw-68187 — stable_wrong

Title: SSE-backed MCP sessions can stay stale after server restart and fail with 'Session not found'

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['mcp_tooling', 'reliability'], 'count': 3}]`

FP: `[('mcp_tooling', 3), ('reliability', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['mcp_tooling', 'reliability']` exact=False
- repeat 2: `['mcp_tooling', 'reliability']` exact=False
- repeat 3: `['mcp_tooling', 'reliability']` exact=False

### 29. openclaw-openclaw-69256 — stable_wrong

Title: fix(cron): prevent premature session cleanup when subagents are running

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['cron_automation', 'reliability', 'sessions'], 'count': 3}]`

FP: `[('cron_automation', 3), ('reliability', 3), ('sessions', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['cron_automation', 'reliability', 'sessions']` exact=False
- repeat 2: `['cron_automation', 'reliability', 'sessions']` exact=False
- repeat 3: `['cron_automation', 'reliability', 'sessions']` exact=False

### 30. openclaw-openclaw-71594 — stable_wrong

Title: docs(gateway): clarify IPv4-only BYOH bind path

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['docs', 'gateway'], 'count': 3}]`

FP: `[('docs', 3), ('gateway', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['docs', 'gateway']` exact=False
- repeat 2: `['docs', 'gateway']` exact=False
- repeat 3: `['docs', 'gateway']` exact=False
