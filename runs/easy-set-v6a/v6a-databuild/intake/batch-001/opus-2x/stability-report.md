# OpenClaw easy-set stability report

Rows: `30`  Repeats: `2`

## Prediction stability

- pairwise exact: `0.867`
- pairwise Jaccard: `0.961`
- pairwise symdiff: `0.133`

## Buckets

- `stable_wrong`: 26
- `unstable_boundary`: 4

## Repeat metric summary

- `avg_expected_topics`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `avg_predicted_topics`: mean `2.3333`, pstdev `0.0333`, values `[2.3, 2.3667]`
- `avg_row_jaccard`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `avg_row_symdiff`: mean `2.3333`, pstdev `0.0333`, values `[2.3, 2.3667]`
- `exact_match`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `gepa_score`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `row_exact_accuracy`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `row_symdiff_score`: mean `0.3000`, pstdev `0.0030`, values `[0.303, 0.297]`
- `topic_micro_f1`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `topic_micro_precision`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `topic_micro_recall`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0]`
- `valid_json`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0]`

## Least stable / review rows

### 1. openclaw-openclaw-71487 — unstable_boundary

Title: Web UI: add a clear TTS toggle and default voice picker in Settings

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['config', 'ui_tui'], 'count': 1}, {'topics': ['config', 'inference_api', 'ui_tui'], 'count': 1}]`

FP: `[('config', 2), ('ui_tui', 2), ('inference_api', 1)]`

FN: `[]`

Volatile: `[('inference_api', 1)]`

- repeat 1: `['config', 'ui_tui']` exact=False
- repeat 2: `['config', 'inference_api', 'ui_tui']` exact=False

### 2. openclaw-openclaw-84648 — unstable_boundary

Title: Add SafeOps preflight hook for exec tool

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['exec_tools', 'security'], 'count': 1}, {'topics': ['exec_tools', 'hooks', 'security'], 'count': 1}]`

FP: `[('exec_tools', 2), ('security', 2), ('hooks', 1)]`

FN: `[]`

Volatile: `[('hooks', 1)]`

- repeat 1: `['exec_tools', 'security']` exact=False
- repeat 2: `['exec_tools', 'hooks', 'security']` exact=False

### 3. openclaw-openclaw-68916 — unstable_boundary

Title: [Bug]: ACP oneshot sessions leave orphaned processes — session reset does not clean up child ACP session keys

Expected: `[]`

pairwise Jaccard `0.750`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.50`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'gateway', 'reliability', 'sessions'], 'count': 1}, {'topics': ['acp', 'reliability', 'sessions'], 'count': 1}]`

FP: `[('acp', 2), ('reliability', 2), ('sessions', 2), ('gateway', 1)]`

FN: `[]`

Volatile: `[('gateway', 1)]`

- repeat 1: `['acp', 'gateway', 'reliability', 'sessions']` exact=False
- repeat 2: `['acp', 'reliability', 'sessions']` exact=False

### 4. openclaw-openclaw-82145 — unstable_boundary

Title: cron: allow retries for local model preflight

Expected: `[]`

pairwise Jaccard `0.750`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.50`, unique sets `2`

Most common predictions: `[{'topics': ['config', 'cron_automation', 'reliability'], 'count': 1}, {'topics': ['config', 'cron_automation', 'reliability', 'self_hosted_inference'], 'count': 1}]`

FP: `[('config', 2), ('cron_automation', 2), ('reliability', 2), ('self_hosted_inference', 1)]`

FN: `[]`

Volatile: `[('self_hosted_inference', 1)]`

- repeat 1: `['config', 'cron_automation', 'reliability']` exact=False
- repeat 2: `['config', 'cron_automation', 'reliability', 'self_hosted_inference']` exact=False

### 5. openclaw-openclaw-41892 — stable_wrong

Title: feat(control-ui): add cron calendar timeline view

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['cron_automation', 'ui_tui'], 'count': 2}]`

FP: `[('cron_automation', 2), ('ui_tui', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['cron_automation', 'ui_tui']` exact=False
- repeat 2: `['cron_automation', 'ui_tui']` exact=False

### 6. openclaw-openclaw-42408 — stable_wrong

Title: [Bug/Docs]: local+hybrid memory_search quality can appear unstable due to extraPaths path drift + benchmark-file contamination

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'docs', 'memory'], 'count': 2}]`

FP: `[('config', 2), ('docs', 2), ('memory', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'docs', 'memory']` exact=False
- repeat 2: `['config', 'docs', 'memory']` exact=False

### 7. openclaw-openclaw-43416 — stable_wrong

Title: feat(ui): add copy button for assistant messages

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['ui_tui'], 'count': 2}]`

FP: `[('ui_tui', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['ui_tui']` exact=False
- repeat 2: `['ui_tui']` exact=False

### 8. openclaw-openclaw-47083 — stable_wrong

Title: fix: respect totalTokensFresh flag to avoid showing stale token counts

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['telemetry_usage', 'ui_tui'], 'count': 2}]`

FP: `[('telemetry_usage', 2), ('ui_tui', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['telemetry_usage', 'ui_tui']` exact=False
- repeat 2: `['telemetry_usage', 'ui_tui']` exact=False

### 9. openclaw-openclaw-48877 — stable_wrong

Title: feat(telegram): add multi-level menu support to customCommands

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'config'], 'count': 2}]`

FP: `[('chat_integrations', 2), ('config', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'config']` exact=False
- repeat 2: `['chat_integrations', 'config']` exact=False

### 10. openclaw-openclaw-51849 — stable_wrong

Title: Docs: add freeCodeCamp OpenClaw full tutorial to showcase

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['docs'], 'count': 2}]`

FP: `[('docs', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['docs']` exact=False
- repeat 2: `['docs']` exact=False

### 11. openclaw-openclaw-53997 — stable_wrong

Title: acpx: add terminal-truth artifacts and strict terminal states

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['acpx', 'reliability'], 'count': 2}]`

FP: `[('acpx', 2), ('reliability', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acpx', 'reliability']` exact=False
- repeat 2: `['acpx', 'reliability']` exact=False

### 12. openclaw-openclaw-65640 — stable_wrong

Title: fix(acp): persistent session recovery for --bind here sessions

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'reliability', 'sessions'], 'count': 2}]`

FP: `[('acp', 2), ('reliability', 2), ('sessions', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'reliability', 'sessions']` exact=False
- repeat 2: `['acp', 'reliability', 'sessions']` exact=False

### 13. openclaw-openclaw-68204 — stable_wrong

Title: Unified run trace schema across agent, ACP, subagent, and task flows

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'agent_runtime', 'telemetry_usage'], 'count': 2}]`

FP: `[('acp', 2), ('agent_runtime', 2), ('telemetry_usage', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'agent_runtime', 'telemetry_usage']` exact=False
- repeat 2: `['acp', 'agent_runtime', 'telemetry_usage']` exact=False

### 14. openclaw-openclaw-71157 — stable_wrong

Title: [Feature]: Support WhatsApp disappearing-message expiration for outbound replies

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'config', 'notifications'], 'count': 2}]`

FP: `[('chat_integrations', 2), ('config', 2), ('notifications', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'config', 'notifications']` exact=False
- repeat 2: `['chat_integrations', 'config', 'notifications']` exact=False

### 15. openclaw-openclaw-71646 — stable_wrong

Title: mcp/channel-bridge: pendingClaudePermissions / pendingApprovals leak — no TTL, no close-clear, no cap

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['approvals', 'mcp_tooling', 'reliability'], 'count': 2}]`

FP: `[('approvals', 2), ('mcp_tooling', 2), ('reliability', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['approvals', 'mcp_tooling', 'reliability']` exact=False
- repeat 2: `['approvals', 'mcp_tooling', 'reliability']` exact=False

### 16. openclaw-openclaw-71976 — stable_wrong

Title: Memory Dreaming: Light sleep sort prioritizes recency over recallCount, hiding real recall data

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['memory'], 'count': 2}]`

FP: `[('memory', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['memory']` exact=False
- repeat 2: `['memory']` exact=False

### 17. openclaw-openclaw-72138 — stable_wrong

Title: fix(feishu): emit sent hooks for normal replies

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'hooks', 'notifications'], 'count': 2}]`

FP: `[('chat_integrations', 2), ('hooks', 2), ('notifications', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'hooks', 'notifications']` exact=False
- repeat 2: `['chat_integrations', 'hooks', 'notifications']` exact=False

### 18. openclaw-openclaw-76724 — stable_wrong

Title: [Bug]: MCP tools not discovered by Agent despite successful handshake (200 OK)

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['mcp_tooling'], 'count': 2}]`

FP: `[('mcp_tooling', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['mcp_tooling']` exact=False
- repeat 2: `['mcp_tooling']` exact=False

### 19. openclaw-openclaw-77694 — stable_wrong

Title: [Bug]: acpx flow run ACP node outputs return empty strings instead of agent replies

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'acpx'], 'count': 2}]`

FP: `[('acp', 2), ('acpx', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'acpx']` exact=False
- repeat 2: `['acp', 'acpx']` exact=False

### 20. openclaw-openclaw-78528 — stable_wrong

Title: Security: skill SecretRef API keys still leak into exec child environments

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['exec_tools', 'security', 'skills_plugins'], 'count': 2}]`

FP: `[('exec_tools', 2), ('security', 2), ('skills_plugins', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['exec_tools', 'security', 'skills_plugins']` exact=False
- repeat 2: `['exec_tools', 'security', 'skills_plugins']` exact=False

### 21. openclaw-openclaw-81488 — stable_wrong

Title: Harden node exec approval precheck env [AI]

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['approvals', 'exec_tools', 'security'], 'count': 2}]`

FP: `[('approvals', 2), ('exec_tools', 2), ('security', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['approvals', 'exec_tools', 'security']` exact=False
- repeat 2: `['approvals', 'exec_tools', 'security']` exact=False

### 22. openclaw-openclaw-82642 — stable_wrong

Title: Fix iMessage slash command acknowledgements

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'notifications'], 'count': 2}]`

FP: `[('chat_integrations', 2), ('notifications', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'notifications']` exact=False
- repeat 2: `['chat_integrations', 'notifications']` exact=False

### 23. openclaw-openclaw-84385 — stable_wrong

Title: [codex] Fix macOS app copyright year

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['ui_tui'], 'count': 2}]`

FP: `[('ui_tui', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['ui_tui']` exact=False
- repeat 2: `['ui_tui']` exact=False

### 24. openclaw-openclaw-84732 — stable_wrong

Title: Slack channel sends fail: `reconcileUnknownSend` required but no channel adapter implements it

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'notifications', 'reliability'], 'count': 2}]`

FP: `[('chat_integrations', 2), ('notifications', 2), ('reliability', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'notifications', 'reliability']` exact=False
- repeat 2: `['chat_integrations', 'notifications', 'reliability']` exact=False

### 25. openclaw-openclaw-84740 — stable_wrong

Title: Feature Request: Option to hide/suppress certain sessions from the session list

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'sessions', 'ui_tui'], 'count': 2}]`

FP: `[('config', 2), ('sessions', 2), ('ui_tui', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'sessions', 'ui_tui']` exact=False
- repeat 2: `['config', 'sessions', 'ui_tui']` exact=False

### 26. openclaw-openclaw-84761 — stable_wrong

Title: feat(secrets): scan backup files for plaintext provider apiKey values

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['security'], 'count': 2}]`

FP: `[('security', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['security']` exact=False
- repeat 2: `['security']` exact=False

### 27. openclaw-openclaw-84771 — stable_wrong

Title: Event loop saturation during startup: synchronous model-prewarm and session-locks block event loop for 28-64 seconds

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `1`

Most common predictions: `[{'topics': ['agent_runtime', 'gateway', 'reliability', 'sessions'], 'count': 2}]`

FP: `[('agent_runtime', 2), ('gateway', 2), ('reliability', 2), ('sessions', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['agent_runtime', 'gateway', 'reliability', 'sessions']` exact=False
- repeat 2: `['agent_runtime', 'gateway', 'reliability', 'sessions']` exact=False

### 28. openclaw-openclaw-84997 — stable_wrong

Title: [AI-assisted] Add NEAR AI Cloud provider

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['inference_api', 'model_lifecycle'], 'count': 2}]`

FP: `[('inference_api', 2), ('model_lifecycle', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['inference_api', 'model_lifecycle']` exact=False
- repeat 2: `['inference_api', 'model_lifecycle']` exact=False

### 29. openclaw-openclaw-87277 — stable_wrong

Title: [Feature] Add MiMo-V2.5 to Xiaomi catalog + automatic multimodal routing when DeepSeek V4-Pro is primary model

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['agent_runtime', 'model_lifecycle'], 'count': 2}]`

FP: `[('agent_runtime', 2), ('model_lifecycle', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['agent_runtime', 'model_lifecycle']` exact=False
- repeat 2: `['agent_runtime', 'model_lifecycle']` exact=False

### 30. openclaw-openclaw-88400 — stable_wrong

Title: fix(config): accept overlays for bundled provider aliases

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'inference_api'], 'count': 2}]`

FP: `[('config', 2), ('inference_api', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'inference_api']` exact=False
- repeat 2: `['config', 'inference_api']` exact=False
