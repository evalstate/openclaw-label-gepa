# OpenClaw easy-set stability report

Rows: `30`  Repeats: `2`

## Prediction stability

- pairwise exact: `0.767`
- pairwise Jaccard: `0.921`
- pairwise symdiff: `0.233`

## Buckets

- `stable_wrong`: 23
- `unstable_boundary`: 7

## Repeat metric summary

- `avg_expected_topics`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `avg_predicted_topics`: mean `2.6167`, pstdev `0.0500`, values `[2.5667, 2.6667]`
- `avg_row_jaccard`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `avg_row_symdiff`: mean `2.6167`, pstdev `0.0500`, values `[2.5667, 2.6667]`
- `exact_match`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `gepa_score`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `row_exact_accuracy`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `row_symdiff_score`: mean `0.2766`, pstdev `0.0038`, values `[0.2804, 0.2727]`
- `topic_micro_f1`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `topic_micro_precision`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `topic_micro_recall`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0]`
- `valid_json`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0]`

## Least stable / review rows

### 1. openclaw-openclaw-48851 — unstable_boundary

Title: feat(status): add API call count to session status and usage footer

Expected: `[]`

pairwise Jaccard `0.500`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.50`, unique sets `2`

Most common predictions: `[{'topics': ['sessions', 'telemetry_usage'], 'count': 1}, {'topics': ['telemetry_usage'], 'count': 1}]`

FP: `[('telemetry_usage', 2), ('sessions', 1)]`

FN: `[]`

Volatile: `[('sessions', 1)]`

- repeat 1: `['sessions', 'telemetry_usage']` exact=False
- repeat 2: `['telemetry_usage']` exact=False

### 2. openclaw-openclaw-58135 — unstable_boundary

Title: [Feature]: expose promptMode parameter in sessions_spawn for deterministic blank sub-agents

Expected: `[]`

pairwise Jaccard `0.500`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.50`, unique sets `2`

Most common predictions: `[{'topics': ['agent_runtime', 'sessions'], 'count': 1}, {'topics': ['agent_runtime'], 'count': 1}]`

FP: `[('agent_runtime', 2), ('sessions', 1)]`

FN: `[]`

Volatile: `[('sessions', 1)]`

- repeat 1: `['agent_runtime', 'sessions']` exact=False
- repeat 2: `['agent_runtime']` exact=False

### 3. openclaw-openclaw-45200 — unstable_boundary

Title: fix(subagents): notify user on announce give-up instead of silently dropping result

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['agent_runtime', 'notifications'], 'count': 1}, {'topics': ['agent_runtime', 'notifications', 'reliability'], 'count': 1}]`

FP: `[('agent_runtime', 2), ('notifications', 2), ('reliability', 1)]`

FN: `[]`

Volatile: `[('reliability', 1)]`

- repeat 1: `['agent_runtime', 'notifications']` exact=False
- repeat 2: `['agent_runtime', 'notifications', 'reliability']` exact=False

### 4. openclaw-openclaw-56442 — unstable_boundary

Title: feat: Add opt-in ACP parent completion notify for sessions_spawn

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'notifications'], 'count': 1}, {'topics': ['acp', 'agent_runtime', 'notifications'], 'count': 1}]`

FP: `[('acp', 2), ('notifications', 2), ('agent_runtime', 1)]`

FN: `[]`

Volatile: `[('agent_runtime', 1)]`

- repeat 1: `['acp', 'notifications']` exact=False
- repeat 2: `['acp', 'agent_runtime', 'notifications']` exact=False

### 5. openclaw-openclaw-45508 — unstable_boundary

Title: [Feature]: Self-hosted STT/TTS provider support in webchat (Route webchat TTS through the gateway instead of browser Speech API)

Expected: `[]`

pairwise Jaccard `0.750`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.50`, unique sets `2`

Most common predictions: `[{'topics': ['chat_integrations', 'config', 'inference_api'], 'count': 1}, {'topics': ['chat_integrations', 'config', 'inference_api', 'self_hosted_inference'], 'count': 1}]`

FP: `[('chat_integrations', 2), ('config', 2), ('inference_api', 2), ('self_hosted_inference', 1)]`

FN: `[]`

Volatile: `[('self_hosted_inference', 1)]`

- repeat 1: `['chat_integrations', 'config', 'inference_api']` exact=False
- repeat 2: `['chat_integrations', 'config', 'inference_api', 'self_hosted_inference']` exact=False

### 6. openclaw-openclaw-56532 — unstable_boundary

Title: memory-lancedb: add configurable timeout/retry for embedding calls

Expected: `[]`

pairwise Jaccard `0.750`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.50`, unique sets `2`

Most common predictions: `[{'topics': ['config', 'memory', 'reliability'], 'count': 1}, {'topics': ['config', 'inference_api', 'memory', 'reliability'], 'count': 1}]`

FP: `[('config', 2), ('memory', 2), ('reliability', 2), ('inference_api', 1)]`

FN: `[]`

Volatile: `[('inference_api', 1)]`

- repeat 1: `['config', 'memory', 'reliability']` exact=False
- repeat 2: `['config', 'inference_api', 'memory', 'reliability']` exact=False

### 7. openclaw-openclaw-40332 — unstable_boundary

Title: [Feature]: Per-binding and per-agent permissionMode for ACP sessions

Expected: `[]`

pairwise Jaccard `0.800`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.50`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'acpx', 'approvals', 'config'], 'count': 1}, {'topics': ['acp', 'acpx', 'approvals', 'config', 'security'], 'count': 1}]`

FP: `[('acp', 2), ('acpx', 2), ('approvals', 2), ('config', 2), ('security', 1)]`

FN: `[]`

Volatile: `[('security', 1)]`

- repeat 1: `['acp', 'acpx', 'approvals', 'config']` exact=False
- repeat 2: `['acp', 'acpx', 'approvals', 'config', 'security']` exact=False

### 8. openclaw-openclaw-10467 — stable_wrong

Title: [Feature Request]: Multi-lane concurrency support for sub-agents via sessions_spawn

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['agent_runtime', 'config', 'queueing'], 'count': 2}]`

FP: `[('agent_runtime', 2), ('config', 2), ('queueing', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['agent_runtime', 'config', 'queueing']` exact=False
- repeat 2: `['agent_runtime', 'config', 'queueing']` exact=False

### 9. openclaw-openclaw-39248 — stable_wrong

Title: Bug: sandbox.mode: "non-main" silently breaks sessions_spawn subagent initialization

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['agent_runtime', 'reliability', 'sandboxing'], 'count': 2}]`

FP: `[('agent_runtime', 2), ('reliability', 2), ('sandboxing', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['agent_runtime', 'reliability', 'sandboxing']` exact=False
- repeat 2: `['agent_runtime', 'reliability', 'sandboxing']` exact=False

### 10. openclaw-openclaw-39714 — stable_wrong

Title: Sandbox: fix Dockerized browser bridge and tab creation

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['browser_automation', 'config', 'sandboxing'], 'count': 2}]`

FP: `[('browser_automation', 2), ('config', 2), ('sandboxing', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['browser_automation', 'config', 'sandboxing']` exact=False
- repeat 2: `['browser_automation', 'config', 'sandboxing']` exact=False

### 11. openclaw-openclaw-42122 — stable_wrong

Title: Speed up install smoke Docker builds

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['packaging_deployment', 'tests_ci'], 'count': 2}]`

FP: `[('packaging_deployment', 2), ('tests_ci', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['packaging_deployment', 'tests_ci']` exact=False
- repeat 2: `['packaging_deployment', 'tests_ci']` exact=False

### 12. openclaw-openclaw-42606 — stable_wrong

Title: Browser: harden noVNC bootstrap headers

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['browser_automation', 'security'], 'count': 2}]`

FP: `[('browser_automation', 2), ('security', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['browser_automation', 'security']` exact=False
- repeat 2: `['browser_automation', 'security']` exact=False

### 13. openclaw-openclaw-43564 — stable_wrong

Title: [Feature Request] ACP Session Skill Context Injection

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'skills_plugins'], 'count': 2}]`

FP: `[('acp', 2), ('skills_plugins', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'skills_plugins']` exact=False
- repeat 2: `['acp', 'skills_plugins']` exact=False

### 14. openclaw-openclaw-43765 — stable_wrong

Title: Improve runtime recovery for heartbeat, Feishu, and exec sessions

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'cron_automation', 'exec_tools', 'gateway', 'reliability'], 'count': 2}]`

FP: `[('chat_integrations', 2), ('cron_automation', 2), ('exec_tools', 2), ('gateway', 2), ('reliability', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'cron_automation', 'exec_tools', 'gateway', 'reliability']` exact=False
- repeat 2: `['chat_integrations', 'cron_automation', 'exec_tools', 'gateway', 'reliability']` exact=False

### 15. openclaw-openclaw-44202 — stable_wrong

Title: [Bug]: local memory embeddings on Apple Silicon can crash gateway in ggml-metal / node-llama-cpp; need official Metal/GPU guidance

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['memory', 'reliability', 'self_hosted_inference'], 'count': 2}]`

FP: `[('memory', 2), ('reliability', 2), ('self_hosted_inference', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['memory', 'reliability', 'self_hosted_inference']` exact=False
- repeat 2: `['memory', 'reliability', 'self_hosted_inference']` exact=False

### 16. openclaw-openclaw-44379 — stable_wrong

Title: fix(pi-runner): harden context-overflow recovery with one suppress-hook retry

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['agent_runtime', 'reliability'], 'count': 2}]`

FP: `[('agent_runtime', 2), ('reliability', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['agent_runtime', 'reliability']` exact=False
- repeat 2: `['agent_runtime', 'reliability']` exact=False

### 17. openclaw-openclaw-45393 — stable_wrong

Title: fix(errors): friendly message and last-message repair for tool_use/tool_result mismatch (#45385)

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['security', 'tool_calling'], 'count': 2}]`

FP: `[('security', 2), ('tool_calling', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['security', 'tool_calling']` exact=False
- repeat 2: `['security', 'tool_calling']` exact=False

### 18. openclaw-openclaw-46552 — stable_wrong

Title: docs(queue): clarify steer behavior with partial streaming and tool boundaries

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['docs', 'queueing'], 'count': 2}]`

FP: `[('docs', 2), ('queueing', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['docs', 'queueing']` exact=False
- repeat 2: `['docs', 'queueing']` exact=False

### 19. openclaw-openclaw-47446 — stable_wrong

Title: fix(gateway/discord): respect env proxy vars and prevent ECONNRESET

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'gateway', 'reliability'], 'count': 2}]`

FP: `[('chat_integrations', 2), ('gateway', 2), ('reliability', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'gateway', 'reliability']` exact=False
- repeat 2: `['chat_integrations', 'gateway', 'reliability']` exact=False

### 20. openclaw-openclaw-48406 — stable_wrong

Title: Docs: add saturated session recovery guide

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['docs', 'reliability', 'sessions'], 'count': 2}]`

FP: `[('docs', 2), ('reliability', 2), ('sessions', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['docs', 'reliability', 'sessions']` exact=False
- repeat 2: `['docs', 'reliability', 'sessions']` exact=False

### 21. openclaw-openclaw-48580 — stable_wrong

Title: Bug: acpx codex sessions 创建的会话立即退出 - stdin is not a terminal

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `1`

Most common predictions: `[{'topics': ['acpx', 'codex', 'reliability', 'sessions'], 'count': 2}]`

FP: `[('acpx', 2), ('codex', 2), ('reliability', 2), ('sessions', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acpx', 'codex', 'reliability', 'sessions']` exact=False
- repeat 2: `['acpx', 'codex', 'reliability', 'sessions']` exact=False

### 22. openclaw-openclaw-49502 — stable_wrong

Title: feat(gateway): include usage/cost metadata in agent.wait terminal response

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['api_surface', 'gateway', 'telemetry_usage'], 'count': 2}]`

FP: `[('api_surface', 2), ('gateway', 2), ('telemetry_usage', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['api_surface', 'gateway', 'telemetry_usage']` exact=False
- repeat 2: `['api_surface', 'gateway', 'telemetry_usage']` exact=False

### 23. openclaw-openclaw-51654 — stable_wrong

Title: Support session-level environment variables for ACP sessions

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'acpx', 'sessions'], 'count': 2}]`

FP: `[('acp', 2), ('acpx', 2), ('sessions', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'acpx', 'sessions']` exact=False
- repeat 2: `['acp', 'acpx', 'sessions']` exact=False

### 24. openclaw-openclaw-51667 — stable_wrong

Title: Feature: Native Audio Input for Omni-Modal Models (skip STT transcription)

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'inference_api'], 'count': 2}]`

FP: `[('config', 2), ('inference_api', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'inference_api']` exact=False
- repeat 2: `['config', 'inference_api']` exact=False

### 25. openclaw-openclaw-52747 — stable_wrong

Title: fix(acp): time out stuck session lane tasks

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'config', 'queueing', 'reliability'], 'count': 2}]`

FP: `[('acp', 2), ('config', 2), ('queueing', 2), ('reliability', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'config', 'queueing', 'reliability']` exact=False
- repeat 2: `['acp', 'config', 'queueing', 'reliability']` exact=False

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

### 27. openclaw-openclaw-59208 — stable_wrong

Title: fix(status): honor selected usage auth profile

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['auth_identity', 'telemetry_usage'], 'count': 2}]`

FP: `[('auth_identity', 2), ('telemetry_usage', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['auth_identity', 'telemetry_usage']` exact=False
- repeat 2: `['auth_identity', 'telemetry_usage']` exact=False

### 28. openclaw-openclaw-60381 — stable_wrong

Title: browser tool: add force parameter for click and expose evaluate action

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['browser_automation'], 'count': 2}]`

FP: `[('browser_automation', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['browser_automation']` exact=False
- repeat 2: `['browser_automation']` exact=False

### 29. openclaw-openclaw-60737 — stable_wrong

Title: [Feature]: Per-DM/per-chat default ACP binding for auto-spawning ACP sessions on new topics

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'chat_integrations', 'config'], 'count': 2}]`

FP: `[('acp', 2), ('chat_integrations', 2), ('config', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'chat_integrations', 'config']` exact=False
- repeat 2: `['acp', 'chat_integrations', 'config']` exact=False

### 30. openclaw-openclaw-61775 — stable_wrong

Title: enhance Makefile with standard build, test, and quality targets

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['packaging_deployment'], 'count': 2}]`

FP: `[('packaging_deployment', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['packaging_deployment']` exact=False
- repeat 2: `['packaging_deployment']` exact=False
