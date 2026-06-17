# OpenClaw easy-set stability report

Rows: `20`  Repeats: `3`

## Prediction stability

- pairwise exact: `0.650`
- pairwise Jaccard: `0.896`
- pairwise symdiff: `0.467`

## Buckets

- `review`: 5
- `stable_wrong`: 11
- `unstable_boundary`: 4

## Repeat metric summary

- `avg_expected_topics`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `avg_predicted_topics`: mean `3.2500`, pstdev `0.0707`, values `[3.2, 3.35, 3.2]`
- `avg_row_jaccard`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `avg_row_symdiff`: mean `3.2500`, pstdev `0.0707`, values `[3.2, 3.35, 3.2]`
- `exact_match`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `gepa_score`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `row_exact_accuracy`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `row_symdiff_score`: mean `0.2354`, pstdev `0.0039`, values `[0.2381, 0.2299, 0.2381]`
- `topic_micro_f1`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `topic_micro_precision`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `topic_micro_recall`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0, 1.0]`
- `valid_json`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0, 1.0]`

## Least stable / review rows

### 1. openclaw-openclaw-51654 — unstable_boundary

Title: Support session-level environment variables for ACP sessions

Expected: `[]`

pairwise Jaccard `0.656`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.67`, unique sets `3`

Most common predictions: `[{'topics': ['acp', 'acpx', 'config', 'security', 'sessions'], 'count': 1}, {'topics': ['acp', 'acpx', 'api_surface', 'security', 'sessions'], 'count': 1}, {'topics': ['acp', 'acpx', 'config', 'security'], 'count': 1}]`

FP: `[('acp', 3), ('acpx', 3), ('security', 3), ('config', 2), ('sessions', 2), ('api_surface', 1)]`

FN: `[]`

Volatile: `[('config', 2), ('sessions', 2), ('api_surface', 1)]`

- repeat 1: `['acp', 'acpx', 'config', 'security', 'sessions']` exact=False
- repeat 2: `['acp', 'acpx', 'api_surface', 'security', 'sessions']` exact=False
- repeat 3: `['acp', 'acpx', 'config', 'security']` exact=False

### 2. openclaw-openclaw-56442 — unstable_boundary

Title: feat: Add opt-in ACP parent completion notify for sessions_spawn

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'api_surface', 'notifications'], 'count': 2}, {'topics': ['acp', 'notifications', 'tool_calling'], 'count': 1}]`

FP: `[('acp', 3), ('notifications', 3), ('api_surface', 2), ('tool_calling', 1)]`

FN: `[]`

Volatile: `[('api_surface', 2), ('tool_calling', 1)]`

- repeat 1: `['acp', 'notifications', 'tool_calling']` exact=False
- repeat 2: `['acp', 'api_surface', 'notifications']` exact=False
- repeat 3: `['acp', 'api_surface', 'notifications']` exact=False

### 3. openclaw-openclaw-48406 — unstable_boundary

Title: Docs: add saturated session recovery guide

Expected: `[]`

pairwise Jaccard `0.700`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.67`, unique sets `3`

Most common predictions: `[{'topics': ['agent_runtime', 'config', 'docs', 'reliability'], 'count': 1}, {'topics': ['config', 'docs', 'reliability', 'sessions'], 'count': 1}, {'topics': ['config', 'docs', 'reliability'], 'count': 1}]`

FP: `[('config', 3), ('docs', 3), ('reliability', 3), ('agent_runtime', 1), ('sessions', 1)]`

FN: `[]`

Volatile: `[('agent_runtime', 1), ('sessions', 1)]`

- repeat 1: `['agent_runtime', 'config', 'docs', 'reliability']` exact=False
- repeat 2: `['config', 'docs', 'reliability', 'sessions']` exact=False
- repeat 3: `['config', 'docs', 'reliability']` exact=False

### 4. openclaw-openclaw-43564 — unstable_boundary

Title: [Feature Request] ACP Session Skill Context Injection

Expected: `[]`

pairwise Jaccard `0.756`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.67`, unique sets `3`

Most common predictions: `[{'topics': ['acp', 'coding_agent_integrations', 'security', 'skills_plugins'], 'count': 1}, {'topics': ['acp', 'api_surface', 'coding_agent_integrations', 'security', 'skills_plugins'], 'count': 1}, {'topics': ['acp', 'coding_agent_integrations', 'security', 'sessions', 'skills_plugins'], 'count': 1}]`

FP: `[('acp', 3), ('coding_agent_integrations', 3), ('security', 3), ('skills_plugins', 3), ('api_surface', 1), ('sessions', 1)]`

FN: `[]`

Volatile: `[('api_surface', 1), ('sessions', 1)]`

- repeat 1: `['acp', 'coding_agent_integrations', 'security', 'skills_plugins']` exact=False
- repeat 2: `['acp', 'api_surface', 'coding_agent_integrations', 'security', 'skills_plugins']` exact=False
- repeat 3: `['acp', 'coding_agent_integrations', 'security', 'sessions', 'skills_plugins']` exact=False

### 5. openclaw-openclaw-58135 — review

Title: [Feature]: expose promptMode parameter in sessions_spawn for deterministic blank sub-agents

Expected: `[]`

pairwise Jaccard `0.778`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.33`, unique sets `2`

Most common predictions: `[{'topics': ['agent_runtime', 'tool_calling'], 'count': 2}, {'topics': ['agent_runtime', 'sessions', 'tool_calling'], 'count': 1}]`

FP: `[('agent_runtime', 3), ('tool_calling', 3), ('sessions', 1)]`

FN: `[]`

Volatile: `[('sessions', 1)]`

- repeat 1: `['agent_runtime', 'tool_calling']` exact=False
- repeat 2: `['agent_runtime', 'sessions', 'tool_calling']` exact=False
- repeat 3: `['agent_runtime', 'tool_calling']` exact=False

### 6. openclaw-openclaw-84771 — review

Title: Event loop saturation during startup: synchronous model-prewarm and session-locks block event loop for 28-64 seconds

Expected: `[]`

pairwise Jaccard `0.833`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.67`, unique sets `2`

Most common predictions: `[{'topics': ['agent_runtime', 'gateway', 'reliability', 'sessions'], 'count': 2}, {'topics': ['agent_runtime', 'reliability', 'sessions'], 'count': 1}]`

FP: `[('agent_runtime', 3), ('reliability', 3), ('sessions', 3), ('gateway', 2)]`

FN: `[]`

Volatile: `[('gateway', 2)]`

- repeat 1: `['agent_runtime', 'reliability', 'sessions']` exact=False
- repeat 2: `['agent_runtime', 'gateway', 'reliability', 'sessions']` exact=False
- repeat 3: `['agent_runtime', 'gateway', 'reliability', 'sessions']` exact=False

### 7. openclaw-openclaw-44379 — review

Title: fix(pi-runner): harden context-overflow recovery with one suppress-hook retry

Expected: `[]`

pairwise Jaccard `0.833`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.33`, unique sets `2`

Most common predictions: `[{'topics': ['coding_agent_integrations', 'hooks', 'reliability'], 'count': 2}, {'topics': ['agent_runtime', 'coding_agent_integrations', 'hooks', 'reliability'], 'count': 1}]`

FP: `[('coding_agent_integrations', 3), ('hooks', 3), ('reliability', 3), ('agent_runtime', 1)]`

FN: `[]`

Volatile: `[('agent_runtime', 1)]`

- repeat 1: `['coding_agent_integrations', 'hooks', 'reliability']` exact=False
- repeat 2: `['coding_agent_integrations', 'hooks', 'reliability']` exact=False
- repeat 3: `['agent_runtime', 'coding_agent_integrations', 'hooks', 'reliability']` exact=False

### 8. openclaw-openclaw-60737 — review

Title: [Feature]: Per-DM/per-chat default ACP binding for auto-spawning ACP sessions on new topics

Expected: `[]`

pairwise Jaccard `0.833`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.33`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'chat_integrations', 'config'], 'count': 2}, {'topics': ['acp', 'chat_integrations', 'config', 'sessions'], 'count': 1}]`

FP: `[('acp', 3), ('chat_integrations', 3), ('config', 3), ('sessions', 1)]`

FN: `[]`

Volatile: `[('sessions', 1)]`

- repeat 1: `['acp', 'chat_integrations', 'config', 'sessions']` exact=False
- repeat 2: `['acp', 'chat_integrations', 'config']` exact=False
- repeat 3: `['acp', 'chat_integrations', 'config']` exact=False

### 9. openclaw-openclaw-82880 — review

Title: security: harden ACPX proxy and Firecrawl SSRF protection

Expected: `[]`

pairwise Jaccard `0.867`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.33`, unique sets `2`

Most common predictions: `[{'topics': ['acpx', 'config', 'exec_tools', 'security'], 'count': 2}, {'topics': ['acpx', 'browser_automation', 'config', 'exec_tools', 'security'], 'count': 1}]`

FP: `[('acpx', 3), ('config', 3), ('exec_tools', 3), ('security', 3), ('browser_automation', 1)]`

FN: `[]`

Volatile: `[('browser_automation', 1)]`

- repeat 1: `['acpx', 'config', 'exec_tools', 'security']` exact=False
- repeat 2: `['acpx', 'browser_automation', 'config', 'exec_tools', 'security']` exact=False
- repeat 3: `['acpx', 'config', 'exec_tools', 'security']` exact=False

### 10. openclaw-openclaw-54471 — stable_wrong

Title: fix(acp): add system_event stream relay to parent session for ACP spawn

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp'], 'count': 3}]`

FP: `[('acp', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp']` exact=False
- repeat 2: `['acp']` exact=False
- repeat 3: `['acp']` exact=False

### 11. openclaw-openclaw-68204 — stable_wrong

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

### 12. openclaw-openclaw-77694 — stable_wrong

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

### 13. openclaw-openclaw-84740 — stable_wrong

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

### 14. openclaw-openclaw-10467 — stable_wrong

Title: [Feature Request]: Multi-lane concurrency support for sub-agents via sessions_spawn

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'agent_runtime', 'config', 'queueing', 'tool_calling'], 'count': 3}]`

FP: `[('acp', 3), ('agent_runtime', 3), ('config', 3), ('queueing', 3), ('tool_calling', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'agent_runtime', 'config', 'queueing', 'tool_calling']` exact=False
- repeat 2: `['acp', 'agent_runtime', 'config', 'queueing', 'tool_calling']` exact=False
- repeat 3: `['acp', 'agent_runtime', 'config', 'queueing', 'tool_calling']` exact=False

### 15. openclaw-openclaw-39248 — stable_wrong

Title: Bug: sandbox.mode: "non-main" silently breaks sessions_spawn subagent initialization

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `1`

Most common predictions: `[{'topics': ['agent_runtime', 'reliability', 'sandboxing', 'sessions'], 'count': 3}]`

FP: `[('agent_runtime', 3), ('reliability', 3), ('sandboxing', 3), ('sessions', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['agent_runtime', 'reliability', 'sandboxing', 'sessions']` exact=False
- repeat 2: `['agent_runtime', 'reliability', 'sandboxing', 'sessions']` exact=False
- repeat 3: `['agent_runtime', 'reliability', 'sandboxing', 'sessions']` exact=False

### 16. openclaw-openclaw-40332 — stable_wrong

Title: [Feature]: Per-binding and per-agent permissionMode for ACP sessions

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'acpx', 'approvals', 'config', 'security'], 'count': 3}]`

FP: `[('acp', 3), ('acpx', 3), ('approvals', 3), ('config', 3), ('security', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'acpx', 'approvals', 'config', 'security']` exact=False
- repeat 2: `['acp', 'acpx', 'approvals', 'config', 'security']` exact=False
- repeat 3: `['acp', 'acpx', 'approvals', 'config', 'security']` exact=False

### 17. openclaw-openclaw-48580 — stable_wrong

Title: Bug: acpx codex sessions 创建的会话立即退出 - stdin is not a terminal

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `1`

Most common predictions: `[{'topics': ['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions'], 'count': 3}]`

FP: `[('acpx', 3), ('codex', 3), ('coding_agent_integrations', 3), ('reliability', 3), ('sessions', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']` exact=False
- repeat 2: `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']` exact=False
- repeat 3: `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']` exact=False

### 18. openclaw-openclaw-48851 — stable_wrong

Title: feat(status): add API call count to session status and usage footer

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['sessions', 'telemetry_usage', 'ui_tui'], 'count': 3}]`

FP: `[('sessions', 3), ('telemetry_usage', 3), ('ui_tui', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['sessions', 'telemetry_usage', 'ui_tui']` exact=False
- repeat 2: `['sessions', 'telemetry_usage', 'ui_tui']` exact=False
- repeat 3: `['sessions', 'telemetry_usage', 'ui_tui']` exact=False

### 19. openclaw-openclaw-51667 — stable_wrong

Title: Feature: Native Audio Input for Omni-Modal Models (skip STT transcription)

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'inference_api', 'sessions'], 'count': 3}]`

FP: `[('config', 3), ('inference_api', 3), ('sessions', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'inference_api', 'sessions']` exact=False
- repeat 2: `['config', 'inference_api', 'sessions']` exact=False
- repeat 3: `['config', 'inference_api', 'sessions']` exact=False

### 20. openclaw-openclaw-46740 — stable_wrong

Title: ACP: classify silent acpx exits as backend unavailable

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['acpx', 'reliability'], 'count': 3}]`

FP: `[('acpx', 3), ('reliability', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acpx', 'reliability']` exact=False
- repeat 2: `['acpx', 'reliability']` exact=False
- repeat 3: `['acpx', 'reliability']` exact=False
