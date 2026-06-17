# OpenClaw easy-set stability report

Rows: `200`  Repeats: `3`

## Prediction stability

- pairwise exact: `0.675`
- pairwise Jaccard: `0.892`
- pairwise symdiff: `0.393`

## Buckets

- `review`: 57
- `stable_wrong`: 110
- `unstable_boundary`: 33

## Repeat metric summary

- `avg_expected_topics`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `avg_predicted_topics`: mean `3.0317`, pstdev `0.0370`, values `[3.05, 2.98, 3.065]`
- `avg_row_jaccard`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `avg_row_symdiff`: mean `3.0317`, pstdev `0.0370`, values `[3.05, 2.98, 3.065]`
- `exact_match`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `gepa_score`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `row_exact_accuracy`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `row_symdiff_score`: mean `0.2481`, pstdev `0.0023`, values `[0.2469, 0.2513, 0.246]`
- `topic_micro_f1`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `topic_micro_precision`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `topic_micro_recall`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0, 1.0]`
- `valid_json`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0, 1.0]`

## Least stable / review rows

### 1. openclaw-openclaw-83333 — unstable_boundary

Title: [Bug]: Memory provider cutover to Ollama leaves production index in mixed OpenAI/Ollama vector state after live sync/reload

Expected: `[]`

pairwise Jaccard `0.500`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `3`

Most common predictions: `[{'topics': ['memory', 'reliability', 'self_hosted_inference'], 'count': 1}, {'topics': ['memory', 'reliability'], 'count': 1}, {'topics': ['memory'], 'count': 1}]`

FP: `[('memory', 3), ('reliability', 2), ('self_hosted_inference', 1)]`

FN: `[]`

Volatile: `[('reliability', 2), ('self_hosted_inference', 1)]`

- repeat 1: `['memory', 'reliability', 'self_hosted_inference']` exact=False
- repeat 2: `['memory', 'reliability']` exact=False
- repeat 3: `['memory']` exact=False

### 2. openclaw-openclaw-82355 — unstable_boundary

Title: Fix streamed chat completions dropping leading less-than

Expected: `[]`

pairwise Jaccard `0.500`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `3`

Most common predictions: `[{'topics': ['api_surface'], 'count': 1}, {'topics': ['api_surface', 'gateway', 'reliability'], 'count': 1}, {'topics': ['api_surface', 'gateway'], 'count': 1}]`

FP: `[('api_surface', 3), ('gateway', 2), ('reliability', 1)]`

FN: `[]`

Volatile: `[('gateway', 2), ('reliability', 1)]`

- repeat 1: `['api_surface']` exact=False
- repeat 2: `['api_surface', 'gateway', 'reliability']` exact=False
- repeat 3: `['api_surface', 'gateway']` exact=False

### 3. openclaw-openclaw-44049 — unstable_boundary

Title: [AI-assisted] Fix duplicated acp server args in ACP client

Expected: `[]`

pairwise Jaccard `0.556`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.33`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'api_surface', 'exec_tools'], 'count': 2}, {'topics': ['acp'], 'count': 1}]`

FP: `[('acp', 3), ('api_surface', 2), ('exec_tools', 2)]`

FN: `[]`

Volatile: `[('api_surface', 2), ('exec_tools', 2)]`

- repeat 1: `['acp', 'api_surface', 'exec_tools']` exact=False
- repeat 2: `['acp', 'api_surface', 'exec_tools']` exact=False
- repeat 3: `['acp']` exact=False

### 4. openclaw-openclaw-70306 — unstable_boundary

Title: fix(acp+gateway): clean final emit, fallback visibility, legacy unit resolve

Expected: `[]`

pairwise Jaccard `0.587`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `3`

Most common predictions: `[{'topics': ['acp', 'codex', 'coding_agent_integrations', 'gateway', 'telemetry_usage'], 'count': 1}, {'topics': ['acp', 'coding_agent_integrations', 'gateway', 'packaging_deployment', 'telemetry_usage'], 'count': 1}, {'topics': ['acp', 'codex', 'config', 'gateway', 'telemetry_usage'], 'count': 1}]`

FP: `[('acp', 3), ('gateway', 3), ('telemetry_usage', 3), ('codex', 2), ('coding_agent_integrations', 2), ('packaging_deployment', 1), ('config', 1)]`

FN: `[]`

Volatile: `[('codex', 2), ('coding_agent_integrations', 2), ('config', 1), ('packaging_deployment', 1)]`

- repeat 1: `['acp', 'codex', 'coding_agent_integrations', 'gateway', 'telemetry_usage']` exact=False
- repeat 2: `['acp', 'coding_agent_integrations', 'gateway', 'packaging_deployment', 'telemetry_usage']` exact=False
- repeat 3: `['acp', 'codex', 'config', 'gateway', 'telemetry_usage']` exact=False

### 5. openclaw-openclaw-84778 — unstable_boundary

Title: /steer command doesn't actually inject into active run — queues for next turn instead

Expected: `[]`

pairwise Jaccard `0.611`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.67`, unique sets `3`

Most common predictions: `[{'topics': ['agent_runtime', 'codex', 'queueing'], 'count': 1}, {'topics': ['agent_runtime', 'queueing', 'ui_tui'], 'count': 1}, {'topics': ['agent_runtime', 'queueing'], 'count': 1}]`

FP: `[('agent_runtime', 3), ('queueing', 3), ('codex', 1), ('ui_tui', 1)]`

FN: `[]`

Volatile: `[('codex', 1), ('ui_tui', 1)]`

- repeat 1: `['agent_runtime', 'codex', 'queueing']` exact=False
- repeat 2: `['agent_runtime', 'queueing', 'ui_tui']` exact=False
- repeat 3: `['agent_runtime', 'queueing']` exact=False

### 6. openclaw-openclaw-84699 — unstable_boundary

Title: fix(doctor): warn when sandbox hides MCP tools

Expected: `[]`

pairwise Jaccard `0.633`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.33`, unique sets `3`

Most common predictions: `[{'topics': ['config', 'docs', 'mcp_tooling', 'sandboxing', 'telemetry_usage'], 'count': 1}, {'topics': ['config', 'mcp_tooling', 'sandboxing', 'skills_plugins'], 'count': 1}, {'topics': ['config', 'docs', 'mcp_tooling', 'sandboxing'], 'count': 1}]`

FP: `[('config', 3), ('mcp_tooling', 3), ('sandboxing', 3), ('docs', 2), ('telemetry_usage', 1), ('skills_plugins', 1)]`

FN: `[]`

Volatile: `[('docs', 2), ('skills_plugins', 1), ('telemetry_usage', 1)]`

- repeat 1: `['config', 'docs', 'mcp_tooling', 'sandboxing', 'telemetry_usage']` exact=False
- repeat 2: `['config', 'mcp_tooling', 'sandboxing', 'skills_plugins']` exact=False
- repeat 3: `['config', 'docs', 'mcp_tooling', 'sandboxing']` exact=False

### 7. openclaw-openclaw-45739 — unstable_boundary

Title: ACP: recover parent relay output from gateway state

Expected: `[]`

pairwise Jaccard `0.639`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `3`

Most common predictions: `[{'topics': ['acp', 'gateway', 'reliability', 'sessions'], 'count': 1}, {'topics': ['acp', 'reliability'], 'count': 1}, {'topics': ['acp', 'reliability', 'sessions'], 'count': 1}]`

FP: `[('acp', 3), ('reliability', 3), ('sessions', 2), ('gateway', 1)]`

FN: `[]`

Volatile: `[('sessions', 2), ('gateway', 1)]`

- repeat 1: `['acp', 'gateway', 'reliability', 'sessions']` exact=False
- repeat 2: `['acp', 'reliability']` exact=False
- repeat 3: `['acp', 'reliability', 'sessions']` exact=False

### 8. openclaw-openclaw-52075 — unstable_boundary

Title: docs: clarify custom mobile client usage for chat completions

Expected: `[]`

pairwise Jaccard `0.639`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `3`

Most common predictions: `[{'topics': ['api_surface', 'docs', 'sessions'], 'count': 1}, {'topics': ['api_surface', 'docs'], 'count': 1}, {'topics': ['api_surface', 'docs', 'gateway', 'sessions'], 'count': 1}]`

FP: `[('api_surface', 3), ('docs', 3), ('sessions', 2), ('gateway', 1)]`

FN: `[]`

Volatile: `[('sessions', 2), ('gateway', 1)]`

- repeat 1: `['api_surface', 'docs', 'sessions']` exact=False
- repeat 2: `['api_surface', 'docs']` exact=False
- repeat 3: `['api_surface', 'docs', 'gateway', 'sessions']` exact=False

### 9. openclaw-openclaw-71889 — unstable_boundary

Title: [Bug]: agents add wizard pre-fills nested workspace path (workspace/<id>) instead of documented peer-level (workspace-<id>)

Expected: `[]`

pairwise Jaccard `0.639`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `3`

Most common predictions: `[{'topics': ['config', 'reliability', 'security'], 'count': 1}, {'topics': ['config', 'security'], 'count': 1}, {'topics': ['config', 'reliability', 'sandboxing', 'security'], 'count': 1}]`

FP: `[('config', 3), ('security', 3), ('reliability', 2), ('sandboxing', 1)]`

FN: `[]`

Volatile: `[('reliability', 2), ('sandboxing', 1)]`

- repeat 1: `['config', 'reliability', 'security']` exact=False
- repeat 2: `['config', 'security']` exact=False
- repeat 3: `['config', 'reliability', 'sandboxing', 'security']` exact=False

### 10. openclaw-openclaw-48637 — unstable_boundary

Title: docs: explain Paperclip gateway pairing approval

Expected: `[]`

pairwise Jaccard `0.656`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.67`, unique sets `3`

Most common predictions: `[{'topics': ['api_surface', 'auth_identity', 'coding_agent_integrations', 'config', 'docs'], 'count': 1}, {'topics': ['approvals', 'auth_identity', 'coding_agent_integrations', 'config', 'docs'], 'count': 1}, {'topics': ['approvals', 'auth_identity', 'coding_agent_integrations', 'docs'], 'count': 1}]`

FP: `[('auth_identity', 3), ('coding_agent_integrations', 3), ('docs', 3), ('config', 2), ('approvals', 2), ('api_surface', 1)]`

FN: `[]`

Volatile: `[('approvals', 2), ('config', 2), ('api_surface', 1)]`

- repeat 1: `['api_surface', 'auth_identity', 'coding_agent_integrations', 'config', 'docs']` exact=False
- repeat 2: `['approvals', 'auth_identity', 'coding_agent_integrations', 'config', 'docs']` exact=False
- repeat 3: `['approvals', 'auth_identity', 'coding_agent_integrations', 'docs']` exact=False

### 11. openclaw-openclaw-83863 — unstable_boundary

Title: ACP/Codex child tasks can be marked succeeded with progress-only output and no final deliverable

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `3`

Most common predictions: `[{'topics': ['acp', 'agent_runtime', 'codex', 'queueing', 'reliability'], 'count': 1}, {'topics': ['acp', 'agent_runtime', 'codex', 'coding_agent_integrations', 'queueing'], 'count': 1}, {'topics': ['acp', 'agent_runtime', 'codex', 'notifications', 'queueing'], 'count': 1}]`

FP: `[('acp', 3), ('agent_runtime', 3), ('codex', 3), ('queueing', 3), ('reliability', 1), ('coding_agent_integrations', 1), ('notifications', 1)]`

FN: `[]`

Volatile: `[('coding_agent_integrations', 1), ('notifications', 1), ('reliability', 1)]`

- repeat 1: `['acp', 'agent_runtime', 'codex', 'queueing', 'reliability']` exact=False
- repeat 2: `['acp', 'agent_runtime', 'codex', 'coding_agent_integrations', 'queueing']` exact=False
- repeat 3: `['acp', 'agent_runtime', 'codex', 'notifications', 'queueing']` exact=False

### 12. openclaw-openclaw-44375 — unstable_boundary

Title: Adding ACP agent to agents.list silently hijacks all routing from implicit main agent

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.33`, unique sets `3`

Most common predictions: `[{'topics': ['agent_runtime', 'config', 'security'], 'count': 1}, {'topics': ['config', 'security', 'sessions'], 'count': 1}, {'topics': ['agent_runtime', 'config', 'security', 'sessions'], 'count': 1}]`

FP: `[('config', 3), ('security', 3), ('agent_runtime', 2), ('sessions', 2)]`

FN: `[]`

Volatile: `[('agent_runtime', 2), ('sessions', 2)]`

- repeat 1: `['agent_runtime', 'config', 'security']` exact=False
- repeat 2: `['config', 'security', 'sessions']` exact=False
- repeat 3: `['agent_runtime', 'config', 'security', 'sessions']` exact=False

### 13. openclaw-openclaw-71856 — unstable_boundary

Title: feat(tui): fetch startup conversation summary dynamically from Gateway API

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.33`, unique sets `2`

Most common predictions: `[{'topics': ['ui_tui'], 'count': 2}, {'topics': ['sessions', 'ui_tui'], 'count': 1}]`

FP: `[('ui_tui', 3), ('sessions', 1)]`

FN: `[]`

Volatile: `[('sessions', 1)]`

- repeat 1: `['ui_tui']` exact=False
- repeat 2: `['ui_tui']` exact=False
- repeat 3: `['sessions', 'ui_tui']` exact=False

### 14. openclaw-openclaw-77827 — unstable_boundary

Title: fix: LM Studio thinking blocks invisible with Responses API

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.33`, unique sets `2`

Most common predictions: `[{'topics': ['inference_api'], 'count': 2}, {'topics': ['inference_api', 'self_hosted_inference'], 'count': 1}]`

FP: `[('inference_api', 3), ('self_hosted_inference', 1)]`

FN: `[]`

Volatile: `[('self_hosted_inference', 1)]`

- repeat 1: `['inference_api', 'self_hosted_inference']` exact=False
- repeat 2: `['inference_api']` exact=False
- repeat 3: `['inference_api']` exact=False

### 15. openclaw-openclaw-51462 — unstable_boundary

Title: fix: emit assistant update for tool-call-only messages from OpenAI-compatible providers [AI-assisted]

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `2`

Most common predictions: `[{'topics': ['inference_api', 'notifications', 'tool_calling'], 'count': 2}, {'topics': ['inference_api', 'reliability', 'tool_calling'], 'count': 1}]`

FP: `[('inference_api', 3), ('tool_calling', 3), ('notifications', 2), ('reliability', 1)]`

FN: `[]`

Volatile: `[('notifications', 2), ('reliability', 1)]`

- repeat 1: `['inference_api', 'notifications', 'tool_calling']` exact=False
- repeat 2: `['inference_api', 'reliability', 'tool_calling']` exact=False
- repeat 3: `['inference_api', 'notifications', 'tool_calling']` exact=False

### 16. openclaw-openclaw-66125 — unstable_boundary

Title: [Bug]: openai-completions fallback candidate is selected, but fallback does not complete successfully through an OpenAI-compatible proxy

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.33`, unique sets `2`

Most common predictions: `[{'topics': ['inference_api'], 'count': 2}, {'topics': ['inference_api', 'telemetry_usage'], 'count': 1}]`

FP: `[('inference_api', 3), ('telemetry_usage', 1)]`

FN: `[]`

Volatile: `[('telemetry_usage', 1)]`

- repeat 1: `['inference_api', 'telemetry_usage']` exact=False
- repeat 2: `['inference_api']` exact=False
- repeat 3: `['inference_api']` exact=False

### 17. openclaw-openclaw-84509 — unstable_boundary

Title: fix(acp): preserve pre-tool text in final_only delivery mode

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.67`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'notifications'], 'count': 2}, {'topics': ['acp'], 'count': 1}]`

FP: `[('acp', 3), ('notifications', 2)]`

FN: `[]`

Volatile: `[('notifications', 2)]`

- repeat 1: `['acp', 'notifications']` exact=False
- repeat 2: `['acp']` exact=False
- repeat 3: `['acp', 'notifications']` exact=False

### 18. openclaw-openclaw-56102 — unstable_boundary

Title: [Bug]: ACP server rejects MCP protocolVersion: 2025-11-25 from VS Code 1.113 / Cursor

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.67`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'mcp_tooling'], 'count': 2}, {'topics': ['acp'], 'count': 1}]`

FP: `[('acp', 3), ('mcp_tooling', 2)]`

FN: `[]`

Volatile: `[('mcp_tooling', 2)]`

- repeat 1: `['acp', 'mcp_tooling']` exact=False
- repeat 2: `['acp', 'mcp_tooling']` exact=False
- repeat 3: `['acp']` exact=False

### 19. openclaw-openclaw-44011 — unstable_boundary

Title: fix(hooks): expose session context in typed message hooks

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `2`

Most common predictions: `[{'topics': ['hooks', 'sessions', 'skills_plugins'], 'count': 2}, {'topics': ['api_surface', 'hooks', 'skills_plugins'], 'count': 1}]`

FP: `[('hooks', 3), ('skills_plugins', 3), ('sessions', 2), ('api_surface', 1)]`

FN: `[]`

Volatile: `[('sessions', 2), ('api_surface', 1)]`

- repeat 1: `['hooks', 'sessions', 'skills_plugins']` exact=False
- repeat 2: `['api_surface', 'hooks', 'skills_plugins']` exact=False
- repeat 3: `['hooks', 'sessions', 'skills_plugins']` exact=False

### 20. openclaw-openclaw-44523 — unstable_boundary

Title: fix(session): preserve model override across daily freshness resets

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.67`, unique sets `2`

Most common predictions: `[{'topics': ['reliability', 'sessions'], 'count': 2}, {'topics': ['sessions'], 'count': 1}]`

FP: `[('sessions', 3), ('reliability', 2)]`

FN: `[]`

Volatile: `[('reliability', 2)]`

- repeat 1: `['reliability', 'sessions']` exact=False
- repeat 2: `['sessions']` exact=False
- repeat 3: `['reliability', 'sessions']` exact=False

### 21. openclaw-openclaw-54802 — unstable_boundary

Title: fix: align codex simple completions with responses API

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.67`, unique sets `2`

Most common predictions: `[{'topics': ['codex', 'inference_api'], 'count': 2}, {'topics': ['inference_api'], 'count': 1}]`

FP: `[('inference_api', 3), ('codex', 2)]`

FN: `[]`

Volatile: `[('codex', 2)]`

- repeat 1: `['codex', 'inference_api']` exact=False
- repeat 2: `['inference_api']` exact=False
- repeat 3: `['codex', 'inference_api']` exact=False

### 22. openclaw-openclaw-78977 — unstable_boundary

Title: fix(providers): skip store:false for proxy-like Responses API endpoints (#78897)

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.67`, unique sets `2`

Most common predictions: `[{'topics': ['inference_api', 'security'], 'count': 2}, {'topics': ['inference_api'], 'count': 1}]`

FP: `[('inference_api', 3), ('security', 2)]`

FN: `[]`

Volatile: `[('security', 2)]`

- repeat 1: `['inference_api', 'security']` exact=False
- repeat 2: `['inference_api', 'security']` exact=False
- repeat 3: `['inference_api']` exact=False

### 23. openclaw-openclaw-84791 — unstable_boundary

Title: Fix Telegram TTS voice-note routing

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.67`, unique sets `2`

Most common predictions: `[{'topics': ['chat_integrations', 'notifications'], 'count': 2}, {'topics': ['chat_integrations'], 'count': 1}]`

FP: `[('chat_integrations', 3), ('notifications', 2)]`

FN: `[]`

Volatile: `[('notifications', 2)]`

- repeat 1: `['chat_integrations', 'notifications']` exact=False
- repeat 2: `['chat_integrations']` exact=False
- repeat 3: `['chat_integrations', 'notifications']` exact=False

### 24. openclaw-openclaw-83921 — unstable_boundary

Title: Benchmark spawner scripts use bare "node" instead of process.execPath, risking version mismatch

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.67`, unique sets `2`

Most common predictions: `[{'topics': ['exec_tools', 'tests_ci'], 'count': 2}, {'topics': ['tests_ci'], 'count': 1}]`

FP: `[('tests_ci', 3), ('exec_tools', 2)]`

FN: `[]`

Volatile: `[('exec_tools', 2)]`

- repeat 1: `['tests_ci']` exact=False
- repeat 2: `['exec_tools', 'tests_ci']` exact=False
- repeat 3: `['exec_tools', 'tests_ci']` exact=False

### 25. openclaw-openclaw-84795 — unstable_boundary

Title: Windows native: shell env fallback failed with spawnSync /bin/sh ENOENT

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.67`, unique sets `2`

Most common predictions: `[{'topics': ['config', 'exec_tools'], 'count': 2}, {'topics': ['config'], 'count': 1}]`

FP: `[('config', 3), ('exec_tools', 2)]`

FN: `[]`

Volatile: `[('exec_tools', 2)]`

- repeat 1: `['config']` exact=False
- repeat 2: `['config', 'exec_tools']` exact=False
- repeat 3: `['config', 'exec_tools']` exact=False

### 26. openclaw-openclaw-49042 — unstable_boundary

Title: Plugins: expose structured finalLlmOutcome on agent_end

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `2`

Most common predictions: `[{'topics': ['api_surface', 'hooks', 'skills_plugins'], 'count': 2}, {'topics': ['hooks', 'security', 'skills_plugins'], 'count': 1}]`

FP: `[('hooks', 3), ('skills_plugins', 3), ('api_surface', 2), ('security', 1)]`

FN: `[]`

Volatile: `[('api_surface', 2), ('security', 1)]`

- repeat 1: `['api_surface', 'hooks', 'skills_plugins']` exact=False
- repeat 2: `['hooks', 'security', 'skills_plugins']` exact=False
- repeat 3: `['api_surface', 'hooks', 'skills_plugins']` exact=False

### 27. openclaw-openclaw-60551 — unstable_boundary

Title: Strip leaked reasoning preambles before outbound send

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.33`, unique sets `2`

Most common predictions: `[{'topics': ['notifications'], 'count': 2}, {'topics': ['agent_runtime', 'notifications'], 'count': 1}]`

FP: `[('notifications', 3), ('agent_runtime', 1)]`

FN: `[]`

Volatile: `[('agent_runtime', 1)]`

- repeat 1: `['notifications']` exact=False
- repeat 2: `['notifications']` exact=False
- repeat 3: `['agent_runtime', 'notifications']` exact=False

### 28. openclaw-openclaw-59532 — unstable_boundary

Title: Feature Request: Per-agent default model and reasoning_effort in ACPX plugin config

Expected: `[]`

pairwise Jaccard `0.700`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.67`, unique sets `3`

Most common predictions: `[{'topics': ['acp', 'acpx', 'config', 'skills_plugins'], 'count': 1}, {'topics': ['acp', 'acpx', 'coding_agent_integrations', 'config'], 'count': 1}, {'topics': ['acp', 'acpx', 'config'], 'count': 1}]`

FP: `[('acp', 3), ('acpx', 3), ('config', 3), ('skills_plugins', 1), ('coding_agent_integrations', 1)]`

FN: `[]`

Volatile: `[('coding_agent_integrations', 1), ('skills_plugins', 1)]`

- repeat 1: `['acp', 'acpx', 'config', 'skills_plugins']` exact=False
- repeat 2: `['acp', 'acpx', 'coding_agent_integrations', 'config']` exact=False
- repeat 3: `['acp', 'acpx', 'config']` exact=False

### 29. openclaw-openclaw-78919 — unstable_boundary

Title: [Bug] ACP sessions_spawn doesn't route images to Codex's native vision like acpx codex exec does

Expected: `[]`

pairwise Jaccard `0.700`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.67`, unique sets `3`

Most common predictions: `[{'topics': ['acp', 'codex', 'coding_agent_integrations'], 'count': 1}, {'topics': ['acp', 'agent_runtime', 'codex', 'coding_agent_integrations'], 'count': 1}, {'topics': ['acp', 'codex', 'coding_agent_integrations', 'sessions'], 'count': 1}]`

FP: `[('acp', 3), ('codex', 3), ('coding_agent_integrations', 3), ('agent_runtime', 1), ('sessions', 1)]`

FN: `[]`

Volatile: `[('agent_runtime', 1), ('sessions', 1)]`

- repeat 1: `['acp', 'codex', 'coding_agent_integrations']` exact=False
- repeat 2: `['acp', 'agent_runtime', 'codex', 'coding_agent_integrations']` exact=False
- repeat 3: `['acp', 'codex', 'coding_agent_integrations', 'sessions']` exact=False

### 30. openclaw-openclaw-55484 — unstable_boundary

Title: ACP: support non-thread persistent affinity for cron and orchestrator sessions

Expected: `[]`

pairwise Jaccard `0.733`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'cron_automation', 'security', 'sessions'], 'count': 2}, {'topics': ['acp', 'security', 'sessions', 'tool_calling'], 'count': 1}]`

FP: `[('acp', 3), ('security', 3), ('sessions', 3), ('cron_automation', 2), ('tool_calling', 1)]`

FN: `[]`

Volatile: `[('cron_automation', 2), ('tool_calling', 1)]`

- repeat 1: `['acp', 'security', 'sessions', 'tool_calling']` exact=False
- repeat 2: `['acp', 'cron_automation', 'security', 'sessions']` exact=False
- repeat 3: `['acp', 'cron_automation', 'security', 'sessions']` exact=False
