# OpenClaw easy-set stability report

Rows: `30`  Repeats: `3`

## Prediction stability

- pairwise exact: `0.722`
- pairwise Jaccard: `0.907`
- pairwise symdiff: `0.422`

## Buckets

- `review`: 9
- `stable_wrong`: 18
- `unstable_boundary`: 3

## Repeat metric summary

- `avg_expected_topics`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `avg_predicted_topics`: mean `3.8000`, pstdev `0.0272`, values `[3.8333, 3.8, 3.7667]`
- `avg_row_jaccard`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `avg_row_symdiff`: mean `3.8000`, pstdev `0.0272`, values `[3.8333, 3.8, 3.7667]`
- `exact_match`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `gepa_score`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `row_exact_accuracy`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `row_symdiff_score`: mean `0.2083`, pstdev `0.0012`, values `[0.2069, 0.2083, 0.2098]`
- `topic_micro_f1`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `topic_micro_precision`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `topic_micro_recall`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0, 1.0]`
- `valid_json`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0, 1.0]`

## Least stable / review rows

### 1. openclaw-openclaw-45393 — unstable_boundary

Title: fix(errors): friendly message and last-message repair for tool_use/tool_result mismatch (#45385)

Expected: `[]`

pairwise Jaccard `0.600`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `3`

Most common predictions: `[{'topics': ['inference_api', 'security', 'sessions', 'tool_calling'], 'count': 1}, {'topics': ['inference_api', 'reliability', 'security', 'tool_calling'], 'count': 1}, {'topics': ['coding_agents', 'inference_api', 'security', 'tool_calling'], 'count': 1}]`

FP: `[('inference_api', 3), ('security', 3), ('tool_calling', 3), ('sessions', 1), ('reliability', 1), ('coding_agents', 1)]`

FN: `[]`

Volatile: `[('coding_agents', 1), ('reliability', 1), ('sessions', 1)]`

- repeat 1: `['inference_api', 'security', 'sessions', 'tool_calling']` exact=False
- repeat 2: `['inference_api', 'reliability', 'security', 'tool_calling']` exact=False
- repeat 3: `['coding_agents', 'inference_api', 'security', 'tool_calling']` exact=False

### 2. openclaw-openclaw-58135 — unstable_boundary

Title: [Feature]: expose promptMode parameter in sessions_spawn for deterministic blank sub-agents

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `2`

Most common predictions: `[{'topics': ['api_surface', 'coding_agents', 'sessions'], 'count': 2}, {'topics': ['coding_agents', 'sessions', 'tool_calling'], 'count': 1}]`

FP: `[('coding_agents', 3), ('sessions', 3), ('api_surface', 2), ('tool_calling', 1)]`

FN: `[]`

Volatile: `[('api_surface', 2), ('tool_calling', 1)]`

- repeat 1: `['api_surface', 'coding_agents', 'sessions']` exact=False
- repeat 2: `['api_surface', 'coding_agents', 'sessions']` exact=False
- repeat 3: `['coding_agents', 'sessions', 'tool_calling']` exact=False

### 3. openclaw-openclaw-59208 — unstable_boundary

Title: fix(status): honor selected usage auth profile

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `2`

Most common predictions: `[{'topics': ['auth_identity', 'telemetry_usage', 'ui_tui'], 'count': 2}, {'topics': ['auth_identity', 'security', 'telemetry_usage'], 'count': 1}]`

FP: `[('auth_identity', 3), ('telemetry_usage', 3), ('ui_tui', 2), ('security', 1)]`

FN: `[]`

Volatile: `[('ui_tui', 2), ('security', 1)]`

- repeat 1: `['auth_identity', 'telemetry_usage', 'ui_tui']` exact=False
- repeat 2: `['auth_identity', 'security', 'telemetry_usage']` exact=False
- repeat 3: `['auth_identity', 'telemetry_usage', 'ui_tui']` exact=False

### 4. openclaw-openclaw-43564 — review

Title: [Feature Request] ACP Session Skill Context Injection

Expected: `[]`

pairwise Jaccard `0.778`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'api_surface', 'coding_agents', 'sessions', 'skills_plugins'], 'count': 2}, {'topics': ['acp', 'api_surface', 'coding_agents', 'security', 'skills_plugins'], 'count': 1}]`

FP: `[('acp', 3), ('api_surface', 3), ('coding_agents', 3), ('skills_plugins', 3), ('sessions', 2), ('security', 1)]`

FN: `[]`

Volatile: `[('sessions', 2), ('security', 1)]`

- repeat 1: `['acp', 'api_surface', 'coding_agents', 'sessions', 'skills_plugins']` exact=False
- repeat 2: `['acp', 'api_surface', 'coding_agents', 'security', 'skills_plugins']` exact=False
- repeat 3: `['acp', 'api_surface', 'coding_agents', 'sessions', 'skills_plugins']` exact=False

### 5. openclaw-openclaw-51654 — review

Title: Support session-level environment variables for ACP sessions

Expected: `[]`

pairwise Jaccard `0.778`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'acpx', 'auth_identity', 'security', 'sessions'], 'count': 2}, {'topics': ['acp', 'acpx', 'api_surface', 'security', 'sessions'], 'count': 1}]`

FP: `[('acp', 3), ('acpx', 3), ('security', 3), ('sessions', 3), ('auth_identity', 2), ('api_surface', 1)]`

FN: `[]`

Volatile: `[('auth_identity', 2), ('api_surface', 1)]`

- repeat 1: `['acp', 'acpx', 'auth_identity', 'security', 'sessions']` exact=False
- repeat 2: `['acp', 'acpx', 'auth_identity', 'security', 'sessions']` exact=False
- repeat 3: `['acp', 'acpx', 'api_surface', 'security', 'sessions']` exact=False

### 6. openclaw-openclaw-54471 — review

Title: fix(acp): add system_event stream relay to parent session for ACP spawn

Expected: `[]`

pairwise Jaccard `0.778`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.33`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'sessions'], 'count': 2}, {'topics': ['acp', 'coding_agents', 'sessions'], 'count': 1}]`

FP: `[('acp', 3), ('sessions', 3), ('coding_agents', 1)]`

FN: `[]`

Volatile: `[('coding_agents', 1)]`

- repeat 1: `['acp', 'sessions']` exact=False
- repeat 2: `['acp', 'coding_agents', 'sessions']` exact=False
- repeat 3: `['acp', 'sessions']` exact=False

### 7. openclaw-openclaw-56442 — review

Title: feat: Add opt-in ACP parent completion notify for sessions_spawn

Expected: `[]`

pairwise Jaccard `0.778`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'api_surface', 'coding_agents', 'notifications', 'sessions'], 'count': 2}, {'topics': ['acp', 'coding_agents', 'notifications', 'sessions', 'tool_calling'], 'count': 1}]`

FP: `[('acp', 3), ('coding_agents', 3), ('notifications', 3), ('sessions', 3), ('api_surface', 2), ('tool_calling', 1)]`

FN: `[]`

Volatile: `[('api_surface', 2), ('tool_calling', 1)]`

- repeat 1: `['acp', 'api_surface', 'coding_agents', 'notifications', 'sessions']` exact=False
- repeat 2: `['acp', 'coding_agents', 'notifications', 'sessions', 'tool_calling']` exact=False
- repeat 3: `['acp', 'api_surface', 'coding_agents', 'notifications', 'sessions']` exact=False

### 8. openclaw-openclaw-60381 — review

Title: browser tool: add force parameter for click and expose evaluate action

Expected: `[]`

pairwise Jaccard `0.778`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.33`, unique sets `2`

Most common predictions: `[{'topics': ['browser_automation', 'tool_calling'], 'count': 2}, {'topics': ['browser_automation', 'security', 'tool_calling'], 'count': 1}]`

FP: `[('browser_automation', 3), ('tool_calling', 3), ('security', 1)]`

FN: `[]`

Volatile: `[('security', 1)]`

- repeat 1: `['browser_automation', 'security', 'tool_calling']` exact=False
- repeat 2: `['browser_automation', 'tool_calling']` exact=False
- repeat 3: `['browser_automation', 'tool_calling']` exact=False

### 9. openclaw-openclaw-44379 — review

Title: fix(pi-runner): harden context-overflow recovery with one suppress-hook retry

Expected: `[]`

pairwise Jaccard `0.833`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.33`, unique sets `2`

Most common predictions: `[{'topics': ['coding_agents', 'hooks', 'reliability'], 'count': 2}, {'topics': ['agent_runtime', 'coding_agents', 'hooks', 'reliability'], 'count': 1}]`

FP: `[('coding_agents', 3), ('hooks', 3), ('reliability', 3), ('agent_runtime', 1)]`

FN: `[]`

Volatile: `[('agent_runtime', 1)]`

- repeat 1: `['agent_runtime', 'coding_agents', 'hooks', 'reliability']` exact=False
- repeat 2: `['coding_agents', 'hooks', 'reliability']` exact=False
- repeat 3: `['coding_agents', 'hooks', 'reliability']` exact=False

### 10. openclaw-openclaw-51667 — review

Title: Feature: Native Audio Input for Omni-Modal Models (skip STT transcription)

Expected: `[]`

pairwise Jaccard `0.833`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.67`, unique sets `2`

Most common predictions: `[{'topics': ['chat_integrations', 'config', 'inference_api', 'sessions'], 'count': 2}, {'topics': ['config', 'inference_api', 'sessions'], 'count': 1}]`

FP: `[('config', 3), ('inference_api', 3), ('sessions', 3), ('chat_integrations', 2)]`

FN: `[]`

Volatile: `[('chat_integrations', 2)]`

- repeat 1: `['chat_integrations', 'config', 'inference_api', 'sessions']` exact=False
- repeat 2: `['chat_integrations', 'config', 'inference_api', 'sessions']` exact=False
- repeat 3: `['config', 'inference_api', 'sessions']` exact=False

### 11. openclaw-openclaw-10467 — review

Title: [Feature Request]: Multi-lane concurrency support for sub-agents via sessions_spawn

Expected: `[]`

pairwise Jaccard `0.867`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.67`, unique sets `2`

Most common predictions: `[{'topics': ['coding_agents', 'config', 'queueing', 'reliability', 'tool_calling'], 'count': 2}, {'topics': ['coding_agents', 'config', 'queueing', 'tool_calling'], 'count': 1}]`

FP: `[('coding_agents', 3), ('config', 3), ('queueing', 3), ('tool_calling', 3), ('reliability', 2)]`

FN: `[]`

Volatile: `[('reliability', 2)]`

- repeat 1: `['coding_agents', 'config', 'queueing', 'reliability', 'tool_calling']` exact=False
- repeat 2: `['coding_agents', 'config', 'queueing', 'tool_calling']` exact=False
- repeat 3: `['coding_agents', 'config', 'queueing', 'reliability', 'tool_calling']` exact=False

### 12. openclaw-openclaw-39248 — review

Title: Bug: sandbox.mode: "non-main" silently breaks sessions_spawn subagent initialization

Expected: `[]`

pairwise Jaccard `0.867`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.67`, unique sets `2`

Most common predictions: `[{'topics': ['coding_agents', 'config', 'reliability', 'sandboxing', 'sessions'], 'count': 2}, {'topics': ['coding_agents', 'reliability', 'sandboxing', 'sessions'], 'count': 1}]`

FP: `[('coding_agents', 3), ('reliability', 3), ('sandboxing', 3), ('sessions', 3), ('config', 2)]`

FN: `[]`

Volatile: `[('config', 2)]`

- repeat 1: `['coding_agents', 'reliability', 'sandboxing', 'sessions']` exact=False
- repeat 2: `['coding_agents', 'config', 'reliability', 'sandboxing', 'sessions']` exact=False
- repeat 3: `['coding_agents', 'config', 'reliability', 'sandboxing', 'sessions']` exact=False

### 13. openclaw-openclaw-39714 — stable_wrong

Title: Sandbox: fix Dockerized browser bridge and tab creation

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `1`

Most common predictions: `[{'topics': ['browser_automation', 'coding_agents', 'config', 'sandboxing'], 'count': 3}]`

FP: `[('browser_automation', 3), ('coding_agents', 3), ('config', 3), ('sandboxing', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['browser_automation', 'coding_agents', 'config', 'sandboxing']` exact=False
- repeat 2: `['browser_automation', 'coding_agents', 'config', 'sandboxing']` exact=False
- repeat 3: `['browser_automation', 'coding_agents', 'config', 'sandboxing']` exact=False

### 14. openclaw-openclaw-40332 — stable_wrong

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

### 15. openclaw-openclaw-42122 — stable_wrong

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

### 16. openclaw-openclaw-42606 — stable_wrong

Title: Browser: harden noVNC bootstrap headers

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['api_surface', 'browser_automation', 'security'], 'count': 3}]`

FP: `[('api_surface', 3), ('browser_automation', 3), ('security', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['api_surface', 'browser_automation', 'security']` exact=False
- repeat 2: `['api_surface', 'browser_automation', 'security']` exact=False
- repeat 3: `['api_surface', 'browser_automation', 'security']` exact=False

### 17. openclaw-openclaw-43765 — stable_wrong

Title: Improve runtime recovery for heartbeat, Feishu, and exec sessions

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'cron_automation', 'exec_tools', 'gateway', 'reliability'], 'count': 3}]`

FP: `[('chat_integrations', 3), ('cron_automation', 3), ('exec_tools', 3), ('gateway', 3), ('reliability', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'cron_automation', 'exec_tools', 'gateway', 'reliability']` exact=False
- repeat 2: `['chat_integrations', 'cron_automation', 'exec_tools', 'gateway', 'reliability']` exact=False
- repeat 3: `['chat_integrations', 'cron_automation', 'exec_tools', 'gateway', 'reliability']` exact=False

### 18. openclaw-openclaw-44202 — stable_wrong

Title: [Bug]: local memory embeddings on Apple Silicon can crash gateway in ggml-metal / node-llama-cpp; need official Metal/GPU guidance

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `1`

Most common predictions: `[{'topics': ['gateway', 'memory', 'reliability', 'self_hosted_inference'], 'count': 3}]`

FP: `[('gateway', 3), ('memory', 3), ('reliability', 3), ('self_hosted_inference', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['gateway', 'memory', 'reliability', 'self_hosted_inference']` exact=False
- repeat 2: `['gateway', 'memory', 'reliability', 'self_hosted_inference']` exact=False
- repeat 3: `['gateway', 'memory', 'reliability', 'self_hosted_inference']` exact=False

### 19. openclaw-openclaw-45200 — stable_wrong

Title: fix(subagents): notify user on announce give-up instead of silently dropping result

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['coding_agents', 'notifications', 'reliability'], 'count': 3}]`

FP: `[('coding_agents', 3), ('notifications', 3), ('reliability', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['coding_agents', 'notifications', 'reliability']` exact=False
- repeat 2: `['coding_agents', 'notifications', 'reliability']` exact=False
- repeat 3: `['coding_agents', 'notifications', 'reliability']` exact=False

### 20. openclaw-openclaw-45508 — stable_wrong

Title: [Feature]: Self-hosted STT/TTS provider support in webchat (Route webchat TTS through the gateway instead of browser Speech API)

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'config', 'gateway', 'inference_api', 'self_hosted_inference'], 'count': 3}]`

FP: `[('chat_integrations', 3), ('config', 3), ('gateway', 3), ('inference_api', 3), ('self_hosted_inference', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'config', 'gateway', 'inference_api', 'self_hosted_inference']` exact=False
- repeat 2: `['chat_integrations', 'config', 'gateway', 'inference_api', 'self_hosted_inference']` exact=False
- repeat 3: `['chat_integrations', 'config', 'gateway', 'inference_api', 'self_hosted_inference']` exact=False

### 21. openclaw-openclaw-46552 — stable_wrong

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

### 22. openclaw-openclaw-47446 — stable_wrong

Title: fix(gateway/discord): respect env proxy vars and prevent ECONNRESET

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'config', 'gateway', 'reliability'], 'count': 3}]`

FP: `[('chat_integrations', 3), ('config', 3), ('gateway', 3), ('reliability', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'config', 'gateway', 'reliability']` exact=False
- repeat 2: `['chat_integrations', 'config', 'gateway', 'reliability']` exact=False
- repeat 3: `['chat_integrations', 'config', 'gateway', 'reliability']` exact=False

### 23. openclaw-openclaw-48406 — stable_wrong

Title: Docs: add saturated session recovery guide

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `1`

Most common predictions: `[{'topics': ['coding_agents', 'config', 'docs', 'reliability', 'sessions'], 'count': 3}]`

FP: `[('coding_agents', 3), ('config', 3), ('docs', 3), ('reliability', 3), ('sessions', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['coding_agents', 'config', 'docs', 'reliability', 'sessions']` exact=False
- repeat 2: `['coding_agents', 'config', 'docs', 'reliability', 'sessions']` exact=False
- repeat 3: `['coding_agents', 'config', 'docs', 'reliability', 'sessions']` exact=False

### 24. openclaw-openclaw-48580 — stable_wrong

Title: Bug: acpx codex sessions 创建的会话立即退出 - stdin is not a terminal

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `1`

Most common predictions: `[{'topics': ['acpx', 'codex', 'coding_agents', 'reliability', 'sessions'], 'count': 3}]`

FP: `[('acpx', 3), ('codex', 3), ('coding_agents', 3), ('reliability', 3), ('sessions', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acpx', 'codex', 'coding_agents', 'reliability', 'sessions']` exact=False
- repeat 2: `['acpx', 'codex', 'coding_agents', 'reliability', 'sessions']` exact=False
- repeat 3: `['acpx', 'codex', 'coding_agents', 'reliability', 'sessions']` exact=False

### 25. openclaw-openclaw-48851 — stable_wrong

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

### 27. openclaw-openclaw-52747 — stable_wrong

Title: fix(acp): time out stuck session lane tasks

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'config', 'queueing', 'reliability'], 'count': 3}]`

FP: `[('acp', 3), ('config', 3), ('queueing', 3), ('reliability', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'config', 'queueing', 'reliability']` exact=False
- repeat 2: `['acp', 'config', 'queueing', 'reliability']` exact=False
- repeat 3: `['acp', 'config', 'queueing', 'reliability']` exact=False

### 28. openclaw-openclaw-56532 — stable_wrong

Title: memory-lancedb: add configurable timeout/retry for embedding calls

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'inference_api', 'memory', 'reliability', 'skills_plugins'], 'count': 3}]`

FP: `[('config', 3), ('inference_api', 3), ('memory', 3), ('reliability', 3), ('skills_plugins', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'inference_api', 'memory', 'reliability', 'skills_plugins']` exact=False
- repeat 2: `['config', 'inference_api', 'memory', 'reliability', 'skills_plugins']` exact=False
- repeat 3: `['config', 'inference_api', 'memory', 'reliability', 'skills_plugins']` exact=False

### 29. openclaw-openclaw-60737 — stable_wrong

Title: [Feature]: Per-DM/per-chat default ACP binding for auto-spawning ACP sessions on new topics

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'chat_integrations', 'config', 'sessions'], 'count': 3}]`

FP: `[('acp', 3), ('chat_integrations', 3), ('config', 3), ('sessions', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'chat_integrations', 'config', 'sessions']` exact=False
- repeat 2: `['acp', 'chat_integrations', 'config', 'sessions']` exact=False
- repeat 3: `['acp', 'chat_integrations', 'config', 'sessions']` exact=False

### 30. openclaw-openclaw-61775 — stable_wrong

Title: enhance Makefile with standard build, test, and quality targets

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['packaging_deployment', 'tests_ci'], 'count': 3}]`

FP: `[('packaging_deployment', 3), ('tests_ci', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['packaging_deployment', 'tests_ci']` exact=False
- repeat 2: `['packaging_deployment', 'tests_ci']` exact=False
- repeat 3: `['packaging_deployment', 'tests_ci']` exact=False
