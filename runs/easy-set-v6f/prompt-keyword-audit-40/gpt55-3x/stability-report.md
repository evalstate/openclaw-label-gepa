# OpenClaw easy-set stability report

Rows: `40`  Repeats: `3`

## Prediction stability

- pairwise exact: `0.867`
- pairwise Jaccard: `0.954`
- pairwise symdiff: `0.150`

## Buckets

- `review`: 5
- `stable_wrong`: 32
- `unstable_boundary`: 3

## Repeat metric summary

- `avg_expected_topics`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `avg_predicted_topics`: mean `2.5000`, pstdev `0.0204`, values `[2.475, 2.5, 2.525]`
- `avg_row_jaccard`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `avg_row_symdiff`: mean `2.5000`, pstdev `0.0204`, values `[2.475, 2.5, 2.525]`
- `exact_match`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `gepa_score`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `row_exact_accuracy`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `row_symdiff_score`: mean `0.2857`, pstdev `0.0017`, values `[0.2878, 0.2857, 0.2837]`
- `topic_micro_f1`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `topic_micro_precision`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `topic_micro_recall`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0, 1.0]`
- `valid_json`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0, 1.0]`

## Least stable / review rows

### 1. openclaw-openclaw-82642 — unstable_boundary

Title: Fix iMessage slash command acknowledgements

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.33`, unique sets `2`

Most common predictions: `[{'topics': ['chat_integrations'], 'count': 2}, {'topics': ['chat_integrations', 'notifications'], 'count': 1}]`

FP: `[('chat_integrations', 3), ('notifications', 1)]`

FN: `[]`

Volatile: `[('notifications', 1)]`

- repeat 1: `['chat_integrations']` exact=False
- repeat 2: `['chat_integrations']` exact=False
- repeat 3: `['chat_integrations', 'notifications']` exact=False

### 2. openclaw-openclaw-54471 — unstable_boundary

Title: fix(acp): add system_event stream relay to parent session for ACP spawn

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.33`, unique sets `2`

Most common predictions: `[{'topics': ['acp'], 'count': 2}, {'topics': ['acp', 'codex'], 'count': 1}]`

FP: `[('acp', 3), ('codex', 1)]`

FN: `[]`

Volatile: `[('codex', 1)]`

- repeat 1: `['acp', 'codex']` exact=False
- repeat 2: `['acp']` exact=False
- repeat 3: `['acp']` exact=False

### 3. openclaw-openclaw-48406 — unstable_boundary

Title: Docs: add saturated session recovery guide

Expected: `[]`

pairwise Jaccard `0.733`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `2`

Most common predictions: `[{'topics': ['agent_runtime', 'config', 'docs', 'reliability'], 'count': 2}, {'topics': ['config', 'docs', 'reliability', 'sessions'], 'count': 1}]`

FP: `[('config', 3), ('docs', 3), ('reliability', 3), ('agent_runtime', 2), ('sessions', 1)]`

FN: `[]`

Volatile: `[('agent_runtime', 2), ('sessions', 1)]`

- repeat 1: `['agent_runtime', 'config', 'docs', 'reliability']` exact=False
- repeat 2: `['agent_runtime', 'config', 'docs', 'reliability']` exact=False
- repeat 3: `['config', 'docs', 'reliability', 'sessions']` exact=False

### 4. openclaw-openclaw-46740 — review

Title: ACP: classify silent acpx exits as backend unavailable

Expected: `[]`

pairwise Jaccard `0.778`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.67`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'acpx', 'reliability'], 'count': 2}, {'topics': ['acpx', 'reliability'], 'count': 1}]`

FP: `[('acpx', 3), ('reliability', 3), ('acp', 2)]`

FN: `[]`

Volatile: `[('acp', 2)]`

- repeat 1: `['acpx', 'reliability']` exact=False
- repeat 2: `['acp', 'acpx', 'reliability']` exact=False
- repeat 3: `['acp', 'acpx', 'reliability']` exact=False

### 5. openclaw-openclaw-43564 — review

Title: [Feature Request] ACP Session Skill Context Injection

Expected: `[]`

pairwise Jaccard `0.833`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.33`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'coding_agent_integrations', 'skills_plugins'], 'count': 2}, {'topics': ['acp', 'coding_agent_integrations', 'skills_plugins', 'tool_calling'], 'count': 1}]`

FP: `[('acp', 3), ('coding_agent_integrations', 3), ('skills_plugins', 3), ('tool_calling', 1)]`

FN: `[]`

Volatile: `[('tool_calling', 1)]`

- repeat 1: `['acp', 'coding_agent_integrations', 'skills_plugins']` exact=False
- repeat 2: `['acp', 'coding_agent_integrations', 'skills_plugins', 'tool_calling']` exact=False
- repeat 3: `['acp', 'coding_agent_integrations', 'skills_plugins']` exact=False

### 6. openclaw-openclaw-84771 — review

Title: Event loop saturation during startup: synchronous model-prewarm and session-locks block event loop for 28-64 seconds

Expected: `[]`

pairwise Jaccard `0.833`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.33`, unique sets `2`

Most common predictions: `[{'topics': ['agent_runtime', 'reliability', 'sessions'], 'count': 2}, {'topics': ['agent_runtime', 'gateway', 'reliability', 'sessions'], 'count': 1}]`

FP: `[('agent_runtime', 3), ('reliability', 3), ('sessions', 3), ('gateway', 1)]`

FN: `[]`

Volatile: `[('gateway', 1)]`

- repeat 1: `['agent_runtime', 'reliability', 'sessions']` exact=False
- repeat 2: `['agent_runtime', 'reliability', 'sessions']` exact=False
- repeat 3: `['agent_runtime', 'gateway', 'reliability', 'sessions']` exact=False

### 7. openclaw-openclaw-10467 — review

Title: [Feature Request]: Multi-lane concurrency support for sub-agents via sessions_spawn

Expected: `[]`

pairwise Jaccard `0.833`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.67`, unique sets `2`

Most common predictions: `[{'topics': ['agent_runtime', 'config', 'queueing', 'tool_calling'], 'count': 2}, {'topics': ['config', 'queueing', 'tool_calling'], 'count': 1}]`

FP: `[('config', 3), ('queueing', 3), ('tool_calling', 3), ('agent_runtime', 2)]`

FN: `[]`

Volatile: `[('agent_runtime', 2)]`

- repeat 1: `['config', 'queueing', 'tool_calling']` exact=False
- repeat 2: `['agent_runtime', 'config', 'queueing', 'tool_calling']` exact=False
- repeat 3: `['agent_runtime', 'config', 'queueing', 'tool_calling']` exact=False

### 8. openclaw-openclaw-39248 — review

Title: Bug: sandbox.mode: "non-main" silently breaks sessions_spawn subagent initialization

Expected: `[]`

pairwise Jaccard `0.833`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.33`, unique sets `2`

Most common predictions: `[{'topics': ['agent_runtime', 'reliability', 'sandboxing'], 'count': 2}, {'topics': ['agent_runtime', 'reliability', 'sandboxing', 'sessions'], 'count': 1}]`

FP: `[('agent_runtime', 3), ('reliability', 3), ('sandboxing', 3), ('sessions', 1)]`

FN: `[]`

Volatile: `[('sessions', 1)]`

- repeat 1: `['agent_runtime', 'reliability', 'sandboxing', 'sessions']` exact=False
- repeat 2: `['agent_runtime', 'reliability', 'sandboxing']` exact=False
- repeat 3: `['agent_runtime', 'reliability', 'sandboxing']` exact=False

### 9. openclaw-openclaw-42408 — stable_wrong

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

### 10. openclaw-openclaw-43416 — stable_wrong

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

### 11. openclaw-openclaw-47083 — stable_wrong

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

### 12. openclaw-openclaw-48877 — stable_wrong

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

### 13. openclaw-openclaw-51849 — stable_wrong

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

### 14. openclaw-openclaw-71487 — stable_wrong

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

### 15. openclaw-openclaw-71646 — stable_wrong

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

### 16. openclaw-openclaw-71976 — stable_wrong

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

### 17. openclaw-openclaw-72138 — stable_wrong

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

### 18. openclaw-openclaw-76724 — stable_wrong

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

### 21. openclaw-openclaw-84385 — stable_wrong

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

### 22. openclaw-openclaw-84761 — stable_wrong

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

### 23. openclaw-openclaw-88400 — stable_wrong

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

### 24. openclaw-openclaw-42122 — stable_wrong

Title: Speed up install smoke Docker builds

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['packaging_deployment', 'tests_ci'], 'count': 3}]`

FP: `[('packaging_deployment', 3), ('tests_ci', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['packaging_deployment', 'tests_ci']` exact=False
- repeat 2: `['packaging_deployment', 'tests_ci']` exact=False
- repeat 3: `['packaging_deployment', 'tests_ci']` exact=False

### 25. openclaw-openclaw-46552 — stable_wrong

Title: docs(queue): clarify steer behavior with partial streaming and tool boundaries

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['docs', 'queueing'], 'count': 3}]`

FP: `[('docs', 3), ('queueing', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['docs', 'queueing']` exact=False
- repeat 2: `['docs', 'queueing']` exact=False
- repeat 3: `['docs', 'queueing']` exact=False

### 26. openclaw-openclaw-49502 — stable_wrong

Title: feat(gateway): include usage/cost metadata in agent.wait terminal response

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['api_surface', 'gateway', 'telemetry_usage'], 'count': 3}]`

FP: `[('api_surface', 3), ('gateway', 3), ('telemetry_usage', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['api_surface', 'gateway', 'telemetry_usage']` exact=False
- repeat 2: `['api_surface', 'gateway', 'telemetry_usage']` exact=False
- repeat 3: `['api_surface', 'gateway', 'telemetry_usage']` exact=False

### 27. openclaw-openclaw-59208 — stable_wrong

Title: fix(status): honor selected usage auth profile

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['auth_identity', 'telemetry_usage'], 'count': 3}]`

FP: `[('auth_identity', 3), ('telemetry_usage', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['auth_identity', 'telemetry_usage']` exact=False
- repeat 2: `['auth_identity', 'telemetry_usage']` exact=False
- repeat 3: `['auth_identity', 'telemetry_usage']` exact=False

### 28. openclaw-openclaw-51654 — stable_wrong

Title: Support session-level environment variables for ACP sessions

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'acpx', 'security', 'tool_calling'], 'count': 3}]`

FP: `[('acp', 3), ('acpx', 3), ('security', 3), ('tool_calling', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'acpx', 'security', 'tool_calling']` exact=False
- repeat 2: `['acp', 'acpx', 'security', 'tool_calling']` exact=False
- repeat 3: `['acp', 'acpx', 'security', 'tool_calling']` exact=False

### 29. openclaw-openclaw-56442 — stable_wrong

Title: feat: Add opt-in ACP parent completion notify for sessions_spawn

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'notifications', 'tool_calling'], 'count': 3}]`

FP: `[('acp', 3), ('notifications', 3), ('tool_calling', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'notifications', 'tool_calling']` exact=False
- repeat 2: `['acp', 'notifications', 'tool_calling']` exact=False
- repeat 3: `['acp', 'notifications', 'tool_calling']` exact=False

### 30. openclaw-openclaw-68204 — stable_wrong

Title: Unified run trace schema across agent, ACP, subagent, and task flows

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['telemetry_usage'], 'count': 3}]`

FP: `[('telemetry_usage', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['telemetry_usage']` exact=False
- repeat 2: `['telemetry_usage']` exact=False
- repeat 3: `['telemetry_usage']` exact=False
