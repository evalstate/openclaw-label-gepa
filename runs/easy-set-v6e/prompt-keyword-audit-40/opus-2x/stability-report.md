# OpenClaw easy-set stability report

Rows: `40`  Repeats: `2`

## Prediction stability

- pairwise exact: `0.850`
- pairwise Jaccard: `0.946`
- pairwise symdiff: `0.175`

## Buckets

- `stable_wrong`: 34
- `unstable_boundary`: 6

## Repeat metric summary

- `avg_expected_topics`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `avg_predicted_topics`: mean `2.2125`, pstdev `0.0875`, values `[2.3, 2.125]`
- `avg_row_jaccard`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `avg_row_symdiff`: mean `2.2125`, pstdev `0.0875`, values `[2.3, 2.125]`
- `exact_match`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `gepa_score`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `row_exact_accuracy`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `row_symdiff_score`: mean `0.3115`, pstdev `0.0085`, values `[0.303, 0.32]`
- `topic_micro_f1`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `topic_micro_precision`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `topic_micro_recall`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0]`
- `valid_json`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0]`

## Least stable / review rows

### 1. openclaw-openclaw-47083 — unstable_boundary

Title: fix: respect totalTokensFresh flag to avoid showing stale token counts

Expected: `[]`

pairwise Jaccard `0.500`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.50`, unique sets `2`

Most common predictions: `[{'topics': ['telemetry_usage', 'ui_tui'], 'count': 1}, {'topics': ['ui_tui'], 'count': 1}]`

FP: `[('ui_tui', 2), ('telemetry_usage', 1)]`

FN: `[]`

Volatile: `[('telemetry_usage', 1)]`

- repeat 1: `['telemetry_usage', 'ui_tui']` exact=False
- repeat 2: `['ui_tui']` exact=False

### 2. openclaw-openclaw-40332 — unstable_boundary

Title: [Feature]: Per-binding and per-agent permissionMode for ACP sessions

Expected: `[]`

pairwise Jaccard `0.600`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'acpx', 'approvals', 'config', 'security'], 'count': 1}, {'topics': ['acp', 'approvals', 'config'], 'count': 1}]`

FP: `[('acp', 2), ('approvals', 2), ('config', 2), ('acpx', 1), ('security', 1)]`

FN: `[]`

Volatile: `[('acpx', 1), ('security', 1)]`

- repeat 1: `['acp', 'acpx', 'approvals', 'config', 'security']` exact=False
- repeat 2: `['acp', 'approvals', 'config']` exact=False

### 3. openclaw-openclaw-43564 — unstable_boundary

Title: [Feature Request] ACP Session Skill Context Injection

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'coding_agent_integrations', 'skills_plugins'], 'count': 1}, {'topics': ['acp', 'skills_plugins'], 'count': 1}]`

FP: `[('acp', 2), ('skills_plugins', 2), ('coding_agent_integrations', 1)]`

FN: `[]`

Volatile: `[('coding_agent_integrations', 1)]`

- repeat 1: `['acp', 'coding_agent_integrations', 'skills_plugins']` exact=False
- repeat 2: `['acp', 'skills_plugins']` exact=False

### 4. openclaw-openclaw-48406 — unstable_boundary

Title: Docs: add saturated session recovery guide

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['docs', 'reliability', 'sessions'], 'count': 1}, {'topics': ['docs', 'reliability'], 'count': 1}]`

FP: `[('docs', 2), ('reliability', 2), ('sessions', 1)]`

FN: `[]`

Volatile: `[('sessions', 1)]`

- repeat 1: `['docs', 'reliability', 'sessions']` exact=False
- repeat 2: `['docs', 'reliability']` exact=False

### 5. openclaw-openclaw-82880 — unstable_boundary

Title: security: harden ACPX proxy and Firecrawl SSRF protection

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['acpx', 'exec_tools', 'security'], 'count': 1}, {'topics': ['acpx', 'security'], 'count': 1}]`

FP: `[('acpx', 2), ('security', 2), ('exec_tools', 1)]`

FN: `[]`

Volatile: `[('exec_tools', 1)]`

- repeat 1: `['acpx', 'exec_tools', 'security']` exact=False
- repeat 2: `['acpx', 'security']` exact=False

### 6. openclaw-openclaw-51654 — unstable_boundary

Title: Support session-level environment variables for ACP sessions

Expected: `[]`

pairwise Jaccard `0.750`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.50`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'acpx', 'security', 'sessions'], 'count': 1}, {'topics': ['acp', 'acpx', 'security'], 'count': 1}]`

FP: `[('acp', 2), ('acpx', 2), ('security', 2), ('sessions', 1)]`

FN: `[]`

Volatile: `[('sessions', 1)]`

- repeat 1: `['acp', 'acpx', 'security', 'sessions']` exact=False
- repeat 2: `['acp', 'acpx', 'security']` exact=False

### 7. openclaw-openclaw-42408 — stable_wrong

Title: [Bug/Docs]: local+hybrid memory_search quality can appear unstable due to extraPaths path drift + benchmark-file contamination

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'docs', 'memory'], 'count': 2}]`

FP: `[('config', 2), ('docs', 2), ('memory', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'docs', 'memory']` exact=False
- repeat 2: `['config', 'docs', 'memory']` exact=False

### 8. openclaw-openclaw-43416 — stable_wrong

Title: feat(ui): add copy button for assistant messages

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['ui_tui'], 'count': 2}]`

FP: `[('ui_tui', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['ui_tui']` exact=False
- repeat 2: `['ui_tui']` exact=False

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

### 11. openclaw-openclaw-71487 — stable_wrong

Title: Web UI: add a clear TTS toggle and default voice picker in Settings

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'ui_tui'], 'count': 2}]`

FP: `[('config', 2), ('ui_tui', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'ui_tui']` exact=False
- repeat 2: `['config', 'ui_tui']` exact=False

### 12. openclaw-openclaw-71646 — stable_wrong

Title: mcp/channel-bridge: pendingClaudePermissions / pendingApprovals leak — no TTL, no close-clear, no cap

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['approvals', 'reliability'], 'count': 2}]`

FP: `[('approvals', 2), ('reliability', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['approvals', 'reliability']` exact=False
- repeat 2: `['approvals', 'reliability']` exact=False

### 13. openclaw-openclaw-71976 — stable_wrong

Title: Memory Dreaming: Light sleep sort prioritizes recency over recallCount, hiding real recall data

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['memory'], 'count': 2}]`

FP: `[('memory', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['memory']` exact=False
- repeat 2: `['memory']` exact=False

### 14. openclaw-openclaw-72138 — stable_wrong

Title: fix(feishu): emit sent hooks for normal replies

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'hooks'], 'count': 2}]`

FP: `[('chat_integrations', 2), ('hooks', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'hooks']` exact=False
- repeat 2: `['chat_integrations', 'hooks']` exact=False

### 15. openclaw-openclaw-76724 — stable_wrong

Title: [Bug]: MCP tools not discovered by Agent despite successful handshake (200 OK)

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['mcp_tooling'], 'count': 2}]`

FP: `[('mcp_tooling', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['mcp_tooling']` exact=False
- repeat 2: `['mcp_tooling']` exact=False

### 16. openclaw-openclaw-78528 — stable_wrong

Title: Security: skill SecretRef API keys still leak into exec child environments

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['exec_tools', 'security', 'skills_plugins'], 'count': 2}]`

FP: `[('exec_tools', 2), ('security', 2), ('skills_plugins', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['exec_tools', 'security', 'skills_plugins']` exact=False
- repeat 2: `['exec_tools', 'security', 'skills_plugins']` exact=False

### 17. openclaw-openclaw-81488 — stable_wrong

Title: Harden node exec approval precheck env [AI]

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['approvals', 'exec_tools', 'security'], 'count': 2}]`

FP: `[('approvals', 2), ('exec_tools', 2), ('security', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['approvals', 'exec_tools', 'security']` exact=False
- repeat 2: `['approvals', 'exec_tools', 'security']` exact=False

### 18. openclaw-openclaw-82642 — stable_wrong

Title: Fix iMessage slash command acknowledgements

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'notifications'], 'count': 2}]`

FP: `[('chat_integrations', 2), ('notifications', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'notifications']` exact=False
- repeat 2: `['chat_integrations', 'notifications']` exact=False

### 19. openclaw-openclaw-84385 — stable_wrong

Title: [codex] Fix macOS app copyright year

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['ui_tui'], 'count': 2}]`

FP: `[('ui_tui', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['ui_tui']` exact=False
- repeat 2: `['ui_tui']` exact=False

### 20. openclaw-openclaw-84761 — stable_wrong

Title: feat(secrets): scan backup files for plaintext provider apiKey values

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['security'], 'count': 2}]`

FP: `[('security', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['security']` exact=False
- repeat 2: `['security']` exact=False

### 21. openclaw-openclaw-88400 — stable_wrong

Title: fix(config): accept overlays for bundled provider aliases

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'inference_api'], 'count': 2}]`

FP: `[('config', 2), ('inference_api', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'inference_api']` exact=False
- repeat 2: `['config', 'inference_api']` exact=False

### 22. openclaw-openclaw-42122 — stable_wrong

Title: Speed up install smoke Docker builds

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['packaging_deployment', 'tests_ci'], 'count': 2}]`

FP: `[('packaging_deployment', 2), ('tests_ci', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['packaging_deployment', 'tests_ci']` exact=False
- repeat 2: `['packaging_deployment', 'tests_ci']` exact=False

### 23. openclaw-openclaw-46552 — stable_wrong

Title: docs(queue): clarify steer behavior with partial streaming and tool boundaries

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['docs', 'queueing'], 'count': 2}]`

FP: `[('docs', 2), ('queueing', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['docs', 'queueing']` exact=False
- repeat 2: `['docs', 'queueing']` exact=False

### 24. openclaw-openclaw-49502 — stable_wrong

Title: feat(gateway): include usage/cost metadata in agent.wait terminal response

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['api_surface', 'gateway', 'telemetry_usage'], 'count': 2}]`

FP: `[('api_surface', 2), ('gateway', 2), ('telemetry_usage', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['api_surface', 'gateway', 'telemetry_usage']` exact=False
- repeat 2: `['api_surface', 'gateway', 'telemetry_usage']` exact=False

### 25. openclaw-openclaw-59208 — stable_wrong

Title: fix(status): honor selected usage auth profile

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['auth_identity', 'telemetry_usage'], 'count': 2}]`

FP: `[('auth_identity', 2), ('telemetry_usage', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['auth_identity', 'telemetry_usage']` exact=False
- repeat 2: `['auth_identity', 'telemetry_usage']` exact=False

### 26. openclaw-openclaw-54471 — stable_wrong

Title: fix(acp): add system_event stream relay to parent session for ACP spawn

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp'], 'count': 2}]`

FP: `[('acp', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp']` exact=False
- repeat 2: `['acp']` exact=False

### 27. openclaw-openclaw-56442 — stable_wrong

Title: feat: Add opt-in ACP parent completion notify for sessions_spawn

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'notifications'], 'count': 2}]`

FP: `[('acp', 2), ('notifications', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'notifications']` exact=False
- repeat 2: `['acp', 'notifications']` exact=False

### 28. openclaw-openclaw-68204 — stable_wrong

Title: Unified run trace schema across agent, ACP, subagent, and task flows

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['telemetry_usage'], 'count': 2}]`

FP: `[('telemetry_usage', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['telemetry_usage']` exact=False
- repeat 2: `['telemetry_usage']` exact=False

### 29. openclaw-openclaw-77694 — stable_wrong

Title: [Bug]: acpx flow run ACP node outputs return empty strings instead of agent replies

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'acpx'], 'count': 2}]`

FP: `[('acp', 2), ('acpx', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'acpx']` exact=False
- repeat 2: `['acp', 'acpx']` exact=False

### 30. openclaw-openclaw-84740 — stable_wrong

Title: Feature Request: Option to hide/suppress certain sessions from the session list

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'sessions', 'ui_tui'], 'count': 2}]`

FP: `[('config', 2), ('sessions', 2), ('ui_tui', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'sessions', 'ui_tui']` exact=False
- repeat 2: `['config', 'sessions', 'ui_tui']` exact=False
