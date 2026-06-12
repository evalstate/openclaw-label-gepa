# OpenClaw easy-set stability report

Rows: `30`  Repeats: `3`

## Prediction stability

- pairwise exact: `0.922`
- pairwise Jaccard: `0.969`
- pairwise symdiff: `0.111`

## Buckets

- `review`: 2
- `stable_wrong`: 27
- `unstable_boundary`: 1

## Repeat metric summary

- `avg_expected_topics`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `avg_predicted_topics`: mean `2.2222`, pstdev `0.0314`, values `[2.2, 2.2667, 2.2]`
- `avg_row_jaccard`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `avg_row_symdiff`: mean `2.2222`, pstdev `0.0314`, values `[2.2, 2.2667, 2.2]`
- `exact_match`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `gepa_score`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `row_exact_accuracy`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `row_symdiff_score`: mean `0.3104`, pstdev `0.0030`, values `[0.3125, 0.3061, 0.3125]`
- `topic_micro_f1`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `topic_micro_precision`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `topic_micro_recall`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0, 1.0]`
- `valid_json`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0, 1.0]`

## Least stable / review rows

### 1. openclaw-openclaw-68204 — unstable_boundary

Title: Unified run trace schema across agent, ACP, subagent, and task flows

Expected: `[]`

pairwise Jaccard `0.444`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.67`, unique sets `3`

Most common predictions: `[{'topics': ['telemetry_usage'], 'count': 1}, {'topics': ['acp', 'agent_runtime', 'queueing', 'telemetry_usage'], 'count': 1}, {'topics': ['acp', 'agent_runtime', 'telemetry_usage'], 'count': 1}]`

FP: `[('telemetry_usage', 3), ('acp', 2), ('agent_runtime', 2), ('queueing', 1)]`

FN: `[]`

Volatile: `[('acp', 2), ('agent_runtime', 2), ('queueing', 1)]`

- repeat 1: `['telemetry_usage']` exact=False
- repeat 2: `['acp', 'agent_runtime', 'queueing', 'telemetry_usage']` exact=False
- repeat 3: `['acp', 'agent_runtime', 'telemetry_usage']` exact=False

### 2. openclaw-openclaw-71157 — review

Title: [Feature]: Support WhatsApp disappearing-message expiration for outbound replies

Expected: `[]`

pairwise Jaccard `0.778`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.33`, unique sets `2`

Most common predictions: `[{'topics': ['chat_integrations', 'config'], 'count': 2}, {'topics': ['chat_integrations', 'config', 'notifications'], 'count': 1}]`

FP: `[('chat_integrations', 3), ('config', 3), ('notifications', 1)]`

FN: `[]`

Volatile: `[('notifications', 1)]`

- repeat 1: `['chat_integrations', 'config', 'notifications']` exact=False
- repeat 2: `['chat_integrations', 'config']` exact=False
- repeat 3: `['chat_integrations', 'config']` exact=False

### 3. openclaw-openclaw-84771 — review

Title: Event loop saturation during startup: synchronous model-prewarm and session-locks block event loop for 28-64 seconds

Expected: `[]`

pairwise Jaccard `0.833`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.67`, unique sets `2`

Most common predictions: `[{'topics': ['agent_runtime', 'gateway', 'reliability', 'sessions'], 'count': 2}, {'topics': ['agent_runtime', 'reliability', 'sessions'], 'count': 1}]`

FP: `[('agent_runtime', 3), ('reliability', 3), ('sessions', 3), ('gateway', 2)]`

FN: `[]`

Volatile: `[('gateway', 2)]`

- repeat 1: `['agent_runtime', 'gateway', 'reliability', 'sessions']` exact=False
- repeat 2: `['agent_runtime', 'gateway', 'reliability', 'sessions']` exact=False
- repeat 3: `['agent_runtime', 'reliability', 'sessions']` exact=False

### 4. openclaw-openclaw-41892 — stable_wrong

Title: feat(control-ui): add cron calendar timeline view

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['cron_automation', 'ui_tui'], 'count': 3}]`

FP: `[('cron_automation', 3), ('ui_tui', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['cron_automation', 'ui_tui']` exact=False
- repeat 2: `['cron_automation', 'ui_tui']` exact=False
- repeat 3: `['cron_automation', 'ui_tui']` exact=False

### 5. openclaw-openclaw-42408 — stable_wrong

Title: [Bug/Docs]: local+hybrid memory_search quality can appear unstable due to extraPaths path drift + benchmark-file contamination

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'docs', 'memory'], 'count': 3}]`

FP: `[('config', 3), ('docs', 3), ('memory', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'docs', 'memory']` exact=False
- repeat 2: `['config', 'docs', 'memory']` exact=False
- repeat 3: `['config', 'docs', 'memory']` exact=False

### 6. openclaw-openclaw-43416 — stable_wrong

Title: feat(ui): add copy button for assistant messages

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['ui_tui'], 'count': 3}]`

FP: `[('ui_tui', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['ui_tui']` exact=False
- repeat 2: `['ui_tui']` exact=False
- repeat 3: `['ui_tui']` exact=False

### 7. openclaw-openclaw-47083 — stable_wrong

Title: fix: respect totalTokensFresh flag to avoid showing stale token counts

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['telemetry_usage', 'ui_tui'], 'count': 3}]`

FP: `[('telemetry_usage', 3), ('ui_tui', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['telemetry_usage', 'ui_tui']` exact=False
- repeat 2: `['telemetry_usage', 'ui_tui']` exact=False
- repeat 3: `['telemetry_usage', 'ui_tui']` exact=False

### 8. openclaw-openclaw-48877 — stable_wrong

Title: feat(telegram): add multi-level menu support to customCommands

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'config'], 'count': 3}]`

FP: `[('chat_integrations', 3), ('config', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'config']` exact=False
- repeat 2: `['chat_integrations', 'config']` exact=False
- repeat 3: `['chat_integrations', 'config']` exact=False

### 9. openclaw-openclaw-51849 — stable_wrong

Title: Docs: add freeCodeCamp OpenClaw full tutorial to showcase

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['docs'], 'count': 3}]`

FP: `[('docs', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['docs']` exact=False
- repeat 2: `['docs']` exact=False
- repeat 3: `['docs']` exact=False

### 10. openclaw-openclaw-53997 — stable_wrong

Title: acpx: add terminal-truth artifacts and strict terminal states

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['acpx', 'reliability'], 'count': 3}]`

FP: `[('acpx', 3), ('reliability', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acpx', 'reliability']` exact=False
- repeat 2: `['acpx', 'reliability']` exact=False
- repeat 3: `['acpx', 'reliability']` exact=False

### 11. openclaw-openclaw-65640 — stable_wrong

Title: fix(acp): persistent session recovery for --bind here sessions

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'reliability', 'sessions'], 'count': 3}]`

FP: `[('acp', 3), ('reliability', 3), ('sessions', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'reliability', 'sessions']` exact=False
- repeat 2: `['acp', 'reliability', 'sessions']` exact=False
- repeat 3: `['acp', 'reliability', 'sessions']` exact=False

### 12. openclaw-openclaw-68916 — stable_wrong

Title: [Bug]: ACP oneshot sessions leave orphaned processes — session reset does not clean up child ACP session keys

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'reliability', 'sessions'], 'count': 3}]`

FP: `[('acp', 3), ('reliability', 3), ('sessions', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'reliability', 'sessions']` exact=False
- repeat 2: `['acp', 'reliability', 'sessions']` exact=False
- repeat 3: `['acp', 'reliability', 'sessions']` exact=False

### 13. openclaw-openclaw-71487 — stable_wrong

Title: Web UI: add a clear TTS toggle and default voice picker in Settings

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'inference_api', 'ui_tui'], 'count': 3}]`

FP: `[('config', 3), ('inference_api', 3), ('ui_tui', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'inference_api', 'ui_tui']` exact=False
- repeat 2: `['config', 'inference_api', 'ui_tui']` exact=False
- repeat 3: `['config', 'inference_api', 'ui_tui']` exact=False

### 14. openclaw-openclaw-71646 — stable_wrong

Title: mcp/channel-bridge: pendingClaudePermissions / pendingApprovals leak — no TTL, no close-clear, no cap

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['approvals', 'mcp_tooling', 'reliability'], 'count': 3}]`

FP: `[('approvals', 3), ('mcp_tooling', 3), ('reliability', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['approvals', 'mcp_tooling', 'reliability']` exact=False
- repeat 2: `['approvals', 'mcp_tooling', 'reliability']` exact=False
- repeat 3: `['approvals', 'mcp_tooling', 'reliability']` exact=False

### 15. openclaw-openclaw-71976 — stable_wrong

Title: Memory Dreaming: Light sleep sort prioritizes recency over recallCount, hiding real recall data

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['memory'], 'count': 3}]`

FP: `[('memory', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['memory']` exact=False
- repeat 2: `['memory']` exact=False
- repeat 3: `['memory']` exact=False

### 16. openclaw-openclaw-72138 — stable_wrong

Title: fix(feishu): emit sent hooks for normal replies

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'hooks'], 'count': 3}]`

FP: `[('chat_integrations', 3), ('hooks', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'hooks']` exact=False
- repeat 2: `['chat_integrations', 'hooks']` exact=False
- repeat 3: `['chat_integrations', 'hooks']` exact=False

### 17. openclaw-openclaw-76724 — stable_wrong

Title: [Bug]: MCP tools not discovered by Agent despite successful handshake (200 OK)

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['mcp_tooling'], 'count': 3}]`

FP: `[('mcp_tooling', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['mcp_tooling']` exact=False
- repeat 2: `['mcp_tooling']` exact=False
- repeat 3: `['mcp_tooling']` exact=False

### 18. openclaw-openclaw-77694 — stable_wrong

Title: [Bug]: acpx flow run ACP node outputs return empty strings instead of agent replies

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['acpx'], 'count': 3}]`

FP: `[('acpx', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acpx']` exact=False
- repeat 2: `['acpx']` exact=False
- repeat 3: `['acpx']` exact=False

### 19. openclaw-openclaw-78528 — stable_wrong

Title: Security: skill SecretRef API keys still leak into exec child environments

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['exec_tools', 'security', 'skills_plugins'], 'count': 3}]`

FP: `[('exec_tools', 3), ('security', 3), ('skills_plugins', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['exec_tools', 'security', 'skills_plugins']` exact=False
- repeat 2: `['exec_tools', 'security', 'skills_plugins']` exact=False
- repeat 3: `['exec_tools', 'security', 'skills_plugins']` exact=False

### 20. openclaw-openclaw-81488 — stable_wrong

Title: Harden node exec approval precheck env [AI]

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['approvals', 'exec_tools', 'security'], 'count': 3}]`

FP: `[('approvals', 3), ('exec_tools', 3), ('security', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['approvals', 'exec_tools', 'security']` exact=False
- repeat 2: `['approvals', 'exec_tools', 'security']` exact=False
- repeat 3: `['approvals', 'exec_tools', 'security']` exact=False

### 21. openclaw-openclaw-82145 — stable_wrong

Title: cron: allow retries for local model preflight

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'cron_automation', 'reliability', 'self_hosted_inference'], 'count': 3}]`

FP: `[('config', 3), ('cron_automation', 3), ('reliability', 3), ('self_hosted_inference', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'cron_automation', 'reliability', 'self_hosted_inference']` exact=False
- repeat 2: `['config', 'cron_automation', 'reliability', 'self_hosted_inference']` exact=False
- repeat 3: `['config', 'cron_automation', 'reliability', 'self_hosted_inference']` exact=False

### 22. openclaw-openclaw-82642 — stable_wrong

Title: Fix iMessage slash command acknowledgements

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'notifications'], 'count': 3}]`

FP: `[('chat_integrations', 3), ('notifications', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'notifications']` exact=False
- repeat 2: `['chat_integrations', 'notifications']` exact=False
- repeat 3: `['chat_integrations', 'notifications']` exact=False

### 23. openclaw-openclaw-84385 — stable_wrong

Title: [codex] Fix macOS app copyright year

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['ui_tui'], 'count': 3}]`

FP: `[('ui_tui', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['ui_tui']` exact=False
- repeat 2: `['ui_tui']` exact=False
- repeat 3: `['ui_tui']` exact=False

### 24. openclaw-openclaw-84648 — stable_wrong

Title: Add SafeOps preflight hook for exec tool

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['exec_tools', 'hooks', 'security'], 'count': 3}]`

FP: `[('exec_tools', 3), ('hooks', 3), ('security', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['exec_tools', 'hooks', 'security']` exact=False
- repeat 2: `['exec_tools', 'hooks', 'security']` exact=False
- repeat 3: `['exec_tools', 'hooks', 'security']` exact=False

### 25. openclaw-openclaw-84732 — stable_wrong

Title: Slack channel sends fail: `reconcileUnknownSend` required but no channel adapter implements it

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'notifications', 'reliability'], 'count': 3}]`

FP: `[('chat_integrations', 3), ('notifications', 3), ('reliability', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'notifications', 'reliability']` exact=False
- repeat 2: `['chat_integrations', 'notifications', 'reliability']` exact=False
- repeat 3: `['chat_integrations', 'notifications', 'reliability']` exact=False

### 26. openclaw-openclaw-84740 — stable_wrong

Title: Feature Request: Option to hide/suppress certain sessions from the session list

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['sessions', 'ui_tui'], 'count': 3}]`

FP: `[('sessions', 3), ('ui_tui', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['sessions', 'ui_tui']` exact=False
- repeat 2: `['sessions', 'ui_tui']` exact=False
- repeat 3: `['sessions', 'ui_tui']` exact=False

### 27. openclaw-openclaw-84761 — stable_wrong

Title: feat(secrets): scan backup files for plaintext provider apiKey values

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['security'], 'count': 3}]`

FP: `[('security', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['security']` exact=False
- repeat 2: `['security']` exact=False
- repeat 3: `['security']` exact=False

### 28. openclaw-openclaw-84997 — stable_wrong

Title: [AI-assisted] Add NEAR AI Cloud provider

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['inference_api', 'model_lifecycle'], 'count': 3}]`

FP: `[('inference_api', 3), ('model_lifecycle', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['inference_api', 'model_lifecycle']` exact=False
- repeat 2: `['inference_api', 'model_lifecycle']` exact=False
- repeat 3: `['inference_api', 'model_lifecycle']` exact=False

### 29. openclaw-openclaw-87277 — stable_wrong

Title: [Feature] Add MiMo-V2.5 to Xiaomi catalog + automatic multimodal routing when DeepSeek V4-Pro is primary model

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['inference_api', 'model_lifecycle'], 'count': 3}]`

FP: `[('inference_api', 3), ('model_lifecycle', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['inference_api', 'model_lifecycle']` exact=False
- repeat 2: `['inference_api', 'model_lifecycle']` exact=False
- repeat 3: `['inference_api', 'model_lifecycle']` exact=False

### 30. openclaw-openclaw-88400 — stable_wrong

Title: fix(config): accept overlays for bundled provider aliases

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'inference_api'], 'count': 3}]`

FP: `[('config', 3), ('inference_api', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'inference_api']` exact=False
- repeat 2: `['config', 'inference_api']` exact=False
- repeat 3: `['config', 'inference_api']` exact=False
