# OpenClaw easy-set stability report

Rows: `20`  Repeats: `2`

## Prediction stability

- pairwise exact: `0.800`
- pairwise Jaccard: `0.910`
- pairwise symdiff: `0.350`

## Buckets

- `stable_wrong`: 16
- `unstable_boundary`: 4

## Repeat metric summary

- `avg_expected_topics`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `avg_predicted_topics`: mean `2.6750`, pstdev `0.0250`, values `[2.65, 2.7]`
- `avg_row_jaccard`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `avg_row_symdiff`: mean `2.6750`, pstdev `0.0250`, values `[2.65, 2.7]`
- `exact_match`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `gepa_score`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `row_exact_accuracy`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `row_symdiff_score`: mean `0.2721`, pstdev `0.0019`, values `[0.274, 0.2703]`
- `topic_micro_f1`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `topic_micro_precision`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `topic_micro_recall`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0]`
- `valid_json`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0]`

## Least stable / review rows

### 1. openclaw-openclaw-68204 — unstable_boundary

Title: Unified run trace schema across agent, ACP, subagent, and task flows

Expected: `[]`

pairwise Jaccard `0.333`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `2`

Most common predictions: `[{'topics': ['telemetry_usage'], 'count': 1}, {'topics': ['acp', 'agent_runtime', 'telemetry_usage'], 'count': 1}]`

FP: `[('telemetry_usage', 2), ('acp', 1), ('agent_runtime', 1)]`

FN: `[]`

Volatile: `[('acp', 1), ('agent_runtime', 1)]`

- repeat 1: `['telemetry_usage']` exact=False
- repeat 2: `['acp', 'agent_runtime', 'telemetry_usage']` exact=False

### 2. openclaw-openclaw-48406 — unstable_boundary

Title: Docs: add saturated session recovery guide

Expected: `[]`

pairwise Jaccard `0.400`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.50`, unique sets `2`

Most common predictions: `[{'topics': ['agent_runtime', 'config', 'docs', 'reliability'], 'count': 1}, {'topics': ['docs', 'reliability', 'sessions'], 'count': 1}]`

FP: `[('docs', 2), ('reliability', 2), ('agent_runtime', 1), ('config', 1), ('sessions', 1)]`

FN: `[]`

Volatile: `[('agent_runtime', 1), ('config', 1), ('sessions', 1)]`

- repeat 1: `['agent_runtime', 'config', 'docs', 'reliability']` exact=False
- repeat 2: `['docs', 'reliability', 'sessions']` exact=False

### 3. openclaw-openclaw-48851 — unstable_boundary

Title: feat(status): add API call count to session status and usage footer

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['sessions', 'telemetry_usage'], 'count': 1}, {'topics': ['sessions', 'telemetry_usage', 'ui_tui'], 'count': 1}]`

FP: `[('sessions', 2), ('telemetry_usage', 2), ('ui_tui', 1)]`

FN: `[]`

Volatile: `[('ui_tui', 1)]`

- repeat 1: `['sessions', 'telemetry_usage']` exact=False
- repeat 2: `['sessions', 'telemetry_usage', 'ui_tui']` exact=False

### 4. openclaw-openclaw-48580 — unstable_boundary

Title: Bug: acpx codex sessions 创建的会话立即退出 - stdin is not a terminal

Expected: `[]`

pairwise Jaccard `0.800`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.50`, unique sets `2`

Most common predictions: `[{'topics': ['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions'], 'count': 1}, {'topics': ['acpx', 'codex', 'reliability', 'sessions'], 'count': 1}]`

FP: `[('acpx', 2), ('codex', 2), ('reliability', 2), ('sessions', 2), ('coding_agent_integrations', 1)]`

FN: `[]`

Volatile: `[('coding_agent_integrations', 1)]`

- repeat 1: `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']` exact=False
- repeat 2: `['acpx', 'codex', 'reliability', 'sessions']` exact=False

### 5. openclaw-openclaw-43564 — stable_wrong

Title: [Feature Request] ACP Session Skill Context Injection

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'coding_agent_integrations', 'skills_plugins'], 'count': 2}]`

FP: `[('acp', 2), ('coding_agent_integrations', 2), ('skills_plugins', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'coding_agent_integrations', 'skills_plugins']` exact=False
- repeat 2: `['acp', 'coding_agent_integrations', 'skills_plugins']` exact=False

### 6. openclaw-openclaw-51654 — stable_wrong

Title: Support session-level environment variables for ACP sessions

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'acpx', 'security'], 'count': 2}]`

FP: `[('acp', 2), ('acpx', 2), ('security', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'acpx', 'security']` exact=False
- repeat 2: `['acp', 'acpx', 'security']` exact=False

### 7. openclaw-openclaw-54471 — stable_wrong

Title: fix(acp): add system_event stream relay to parent session for ACP spawn

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp'], 'count': 2}]`

FP: `[('acp', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp']` exact=False
- repeat 2: `['acp']` exact=False

### 8. openclaw-openclaw-56442 — stable_wrong

Title: feat: Add opt-in ACP parent completion notify for sessions_spawn

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'notifications'], 'count': 2}]`

FP: `[('acp', 2), ('notifications', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'notifications']` exact=False
- repeat 2: `['acp', 'notifications']` exact=False

### 9. openclaw-openclaw-77694 — stable_wrong

Title: [Bug]: acpx flow run ACP node outputs return empty strings instead of agent replies

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'acpx'], 'count': 2}]`

FP: `[('acp', 2), ('acpx', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'acpx']` exact=False
- repeat 2: `['acp', 'acpx']` exact=False

### 10. openclaw-openclaw-84740 — stable_wrong

Title: Feature Request: Option to hide/suppress certain sessions from the session list

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'sessions', 'ui_tui'], 'count': 2}]`

FP: `[('config', 2), ('sessions', 2), ('ui_tui', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'sessions', 'ui_tui']` exact=False
- repeat 2: `['config', 'sessions', 'ui_tui']` exact=False

### 11. openclaw-openclaw-84771 — stable_wrong

Title: Event loop saturation during startup: synchronous model-prewarm and session-locks block event loop for 28-64 seconds

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['agent_runtime', 'reliability', 'sessions'], 'count': 2}]`

FP: `[('agent_runtime', 2), ('reliability', 2), ('sessions', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['agent_runtime', 'reliability', 'sessions']` exact=False
- repeat 2: `['agent_runtime', 'reliability', 'sessions']` exact=False

### 12. openclaw-openclaw-10467 — stable_wrong

Title: [Feature Request]: Multi-lane concurrency support for sub-agents via sessions_spawn

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['agent_runtime', 'config', 'queueing'], 'count': 2}]`

FP: `[('agent_runtime', 2), ('config', 2), ('queueing', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['agent_runtime', 'config', 'queueing']` exact=False
- repeat 2: `['agent_runtime', 'config', 'queueing']` exact=False

### 13. openclaw-openclaw-39248 — stable_wrong

Title: Bug: sandbox.mode: "non-main" silently breaks sessions_spawn subagent initialization

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['agent_runtime', 'reliability', 'sandboxing'], 'count': 2}]`

FP: `[('agent_runtime', 2), ('reliability', 2), ('sandboxing', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['agent_runtime', 'reliability', 'sandboxing']` exact=False
- repeat 2: `['agent_runtime', 'reliability', 'sandboxing']` exact=False

### 14. openclaw-openclaw-40332 — stable_wrong

Title: [Feature]: Per-binding and per-agent permissionMode for ACP sessions

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'acpx', 'approvals', 'config'], 'count': 2}]`

FP: `[('acp', 2), ('acpx', 2), ('approvals', 2), ('config', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'acpx', 'approvals', 'config']` exact=False
- repeat 2: `['acp', 'acpx', 'approvals', 'config']` exact=False

### 15. openclaw-openclaw-44379 — stable_wrong

Title: fix(pi-runner): harden context-overflow recovery with one suppress-hook retry

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['agent_runtime', 'reliability'], 'count': 2}]`

FP: `[('agent_runtime', 2), ('reliability', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['agent_runtime', 'reliability']` exact=False
- repeat 2: `['agent_runtime', 'reliability']` exact=False

### 16. openclaw-openclaw-51667 — stable_wrong

Title: Feature: Native Audio Input for Omni-Modal Models (skip STT transcription)

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'inference_api'], 'count': 2}]`

FP: `[('config', 2), ('inference_api', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'inference_api']` exact=False
- repeat 2: `['config', 'inference_api']` exact=False

### 17. openclaw-openclaw-58135 — stable_wrong

Title: [Feature]: expose promptMode parameter in sessions_spawn for deterministic blank sub-agents

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['agent_runtime'], 'count': 2}]`

FP: `[('agent_runtime', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['agent_runtime']` exact=False
- repeat 2: `['agent_runtime']` exact=False

### 18. openclaw-openclaw-60737 — stable_wrong

Title: [Feature]: Per-DM/per-chat default ACP binding for auto-spawning ACP sessions on new topics

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'chat_integrations', 'config'], 'count': 2}]`

FP: `[('acp', 2), ('chat_integrations', 2), ('config', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'chat_integrations', 'config']` exact=False
- repeat 2: `['acp', 'chat_integrations', 'config']` exact=False

### 19. openclaw-openclaw-82880 — stable_wrong

Title: security: harden ACPX proxy and Firecrawl SSRF protection

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acpx', 'exec_tools', 'security'], 'count': 2}]`

FP: `[('acpx', 2), ('exec_tools', 2), ('security', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acpx', 'exec_tools', 'security']` exact=False
- repeat 2: `['acpx', 'exec_tools', 'security']` exact=False

### 20. openclaw-openclaw-46740 — stable_wrong

Title: ACP: classify silent acpx exits as backend unavailable

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'acpx', 'reliability'], 'count': 2}]`

FP: `[('acp', 2), ('acpx', 2), ('reliability', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'acpx', 'reliability']` exact=False
- repeat 2: `['acp', 'acpx', 'reliability']` exact=False
