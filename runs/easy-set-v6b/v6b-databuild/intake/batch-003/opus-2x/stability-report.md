# OpenClaw easy-set stability report

Rows: `200`  Repeats: `2`

## Prediction stability

- pairwise exact: `0.755`
- pairwise Jaccard: `0.907`
- pairwise symdiff: `0.300`

## Buckets

- `stable_wrong`: 151
- `unstable_boundary`: 49

## Repeat metric summary

- `avg_expected_topics`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `avg_predicted_topics`: mean `2.4000`, pstdev `0.0050`, values `[2.395, 2.405]`
- `avg_row_jaccard`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `avg_row_symdiff`: mean `2.4000`, pstdev `0.0050`, values `[2.395, 2.405]`
- `exact_match`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `gepa_score`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `row_exact_accuracy`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `row_symdiff_score`: mean `0.2941`, pstdev `0.0004`, values `[0.2946, 0.2937]`
- `topic_micro_f1`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `topic_micro_precision`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `topic_micro_recall`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0]`
- `valid_json`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0]`

## Least stable / review rows

### 1. openclaw-openclaw-51462 — unstable_boundary

Title: fix: emit assistant update for tool-call-only messages from OpenAI-compatible providers [AI-assisted]

Expected: `[]`

pairwise Jaccard `0.333`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `2`

Most common predictions: `[{'topics': ['agent_runtime', 'tool_calling'], 'count': 1}, {'topics': ['reliability', 'tool_calling'], 'count': 1}]`

FP: `[('tool_calling', 2), ('agent_runtime', 1), ('reliability', 1)]`

FN: `[]`

Volatile: `[('agent_runtime', 1), ('reliability', 1)]`

- repeat 1: `['agent_runtime', 'tool_calling']` exact=False
- repeat 2: `['reliability', 'tool_calling']` exact=False

### 2. openclaw-openclaw-81304 — unstable_boundary

Title: fix(setup): preserve existing primary model when applying provider auth (#64129)

Expected: `[]`

pairwise Jaccard `0.333`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `2`

Most common predictions: `[{'topics': ['config', 'model_lifecycle'], 'count': 1}, {'topics': ['inference_api', 'model_lifecycle'], 'count': 1}]`

FP: `[('model_lifecycle', 2), ('config', 1), ('inference_api', 1)]`

FN: `[]`

Volatile: `[('config', 1), ('inference_api', 1)]`

- repeat 1: `['config', 'model_lifecycle']` exact=False
- repeat 2: `['inference_api', 'model_lifecycle']` exact=False

### 3. openclaw-openclaw-84805 — unstable_boundary

Title: fix(cron): only apply Google preview model normalization for Google providers

Expected: `[]`

pairwise Jaccard `0.333`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `2`

Most common predictions: `[{'topics': ['config', 'model_lifecycle'], 'count': 1}, {'topics': ['inference_api', 'model_lifecycle'], 'count': 1}]`

FP: `[('model_lifecycle', 2), ('config', 1), ('inference_api', 1)]`

FN: `[]`

Volatile: `[('config', 1), ('inference_api', 1)]`

- repeat 1: `['config', 'model_lifecycle']` exact=False
- repeat 2: `['inference_api', 'model_lifecycle']` exact=False

### 4. openclaw-openclaw-84803 — unstable_boundary

Title: WhatsApp group history drops media from unmentioned messages before later mention

Expected: `[]`

pairwise Jaccard `0.333`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `2`

Most common predictions: `[{'topics': ['chat_integrations', 'security'], 'count': 1}, {'topics': ['chat_integrations', 'reliability'], 'count': 1}]`

FP: `[('chat_integrations', 2), ('security', 1), ('reliability', 1)]`

FN: `[]`

Volatile: `[('reliability', 1), ('security', 1)]`

- repeat 1: `['chat_integrations', 'security']` exact=False
- repeat 2: `['chat_integrations', 'reliability']` exact=False

### 5. openclaw-openclaw-80495 — unstable_boundary

Title: [Bug]: LM Studio Provider Fails: Environment Variable Expansion + API Endpoint Mismatch

Expected: `[]`

pairwise Jaccard `0.500`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.50`, unique sets `2`

Most common predictions: `[{'topics': ['self_hosted_inference'], 'count': 1}, {'topics': ['inference_api', 'self_hosted_inference'], 'count': 1}]`

FP: `[('self_hosted_inference', 2), ('inference_api', 1)]`

FN: `[]`

Volatile: `[('inference_api', 1)]`

- repeat 1: `['self_hosted_inference']` exact=False
- repeat 2: `['inference_api', 'self_hosted_inference']` exact=False

### 6. openclaw-openclaw-44086 — unstable_boundary

Title: fix(agents): assistant message content null instead of empty string breaks OpenAI-compatible providers

Expected: `[]`

pairwise Jaccard `0.500`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.50`, unique sets `2`

Most common predictions: `[{'topics': ['inference_api'], 'count': 1}, {'topics': ['inference_api', 'tool_calling'], 'count': 1}]`

FP: `[('inference_api', 2), ('tool_calling', 1)]`

FN: `[]`

Volatile: `[('tool_calling', 1)]`

- repeat 1: `['inference_api']` exact=False
- repeat 2: `['inference_api', 'tool_calling']` exact=False

### 7. openclaw-openclaw-84509 — unstable_boundary

Title: fix(acp): preserve pre-tool text in final_only delivery mode

Expected: `[]`

pairwise Jaccard `0.500`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.50`, unique sets `2`

Most common predictions: `[{'topics': ['acp'], 'count': 1}, {'topics': ['acp', 'notifications'], 'count': 1}]`

FP: `[('acp', 2), ('notifications', 1)]`

FN: `[]`

Volatile: `[('notifications', 1)]`

- repeat 1: `['acp']` exact=False
- repeat 2: `['acp', 'notifications']` exact=False

### 8. openclaw-openclaw-69260 — unstable_boundary

Title: Harden Gemini ACP integration against ambient API-key fallback and add generic auth-contract hooks for ACP agents

Expected: `[]`

pairwise Jaccard `0.500`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.50`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'acpx', 'auth_identity', 'coding_agent_integrations', 'security'], 'count': 1}, {'topics': ['acpx', 'coding_agent_integrations', 'config', 'security'], 'count': 1}]`

FP: `[('acpx', 2), ('coding_agent_integrations', 2), ('security', 2), ('acp', 1), ('auth_identity', 1), ('config', 1)]`

FN: `[]`

Volatile: `[('acp', 1), ('auth_identity', 1), ('config', 1)]`

- repeat 1: `['acp', 'acpx', 'auth_identity', 'coding_agent_integrations', 'security']` exact=False
- repeat 2: `['acpx', 'coding_agent_integrations', 'config', 'security']` exact=False

### 9. openclaw-openclaw-55723 — unstable_boundary

Title: fix(agents): preserve ACP requester agent overrides

Expected: `[]`

pairwise Jaccard `0.500`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.50`, unique sets `2`

Most common predictions: `[{'topics': ['acp'], 'count': 1}, {'topics': ['acp', 'agent_runtime'], 'count': 1}]`

FP: `[('acp', 2), ('agent_runtime', 1)]`

FN: `[]`

Volatile: `[('agent_runtime', 1)]`

- repeat 1: `['acp']` exact=False
- repeat 2: `['acp', 'agent_runtime']` exact=False

### 10. openclaw-openclaw-69669 — unstable_boundary

Title: ACP: keep thread-bound follow-ups parent-orchestrated by default, not raw pass-through

Expected: `[]`

pairwise Jaccard `0.500`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.50`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'sessions'], 'count': 1}, {'topics': ['acp'], 'count': 1}]`

FP: `[('acp', 2), ('sessions', 1)]`

FN: `[]`

Volatile: `[('sessions', 1)]`

- repeat 1: `['acp', 'sessions']` exact=False
- repeat 2: `['acp']` exact=False

### 11. openclaw-openclaw-67244 — unstable_boundary

Title: Explicit ACP agent runs: embedded backend visibility failure and stale final JSON state after sessions_yield

Expected: `[]`

pairwise Jaccard `0.500`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.50`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'acpx', 'gateway', 'reliability'], 'count': 1}, {'topics': ['acp', 'acpx', 'api_surface', 'gateway', 'sessions'], 'count': 1}]`

FP: `[('acp', 2), ('acpx', 2), ('gateway', 2), ('reliability', 1), ('api_surface', 1), ('sessions', 1)]`

FN: `[]`

Volatile: `[('api_surface', 1), ('reliability', 1), ('sessions', 1)]`

- repeat 1: `['acp', 'acpx', 'gateway', 'reliability']` exact=False
- repeat 2: `['acp', 'acpx', 'api_surface', 'gateway', 'sessions']` exact=False

### 12. openclaw-openclaw-80909 — unstable_boundary

Title: MCP server tools never reach outbound `tools[]` across 4.26 → 5.7 (cluster previously closed + locked as 'resolved')

Expected: `[]`

pairwise Jaccard `0.500`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `2`

Most common predictions: `[{'topics': ['agent_runtime', 'mcp_tooling', 'tool_calling'], 'count': 1}, {'topics': ['inference_api', 'mcp_tooling', 'tool_calling'], 'count': 1}]`

FP: `[('mcp_tooling', 2), ('tool_calling', 2), ('agent_runtime', 1), ('inference_api', 1)]`

FN: `[]`

Volatile: `[('agent_runtime', 1), ('inference_api', 1)]`

- repeat 1: `['agent_runtime', 'mcp_tooling', 'tool_calling']` exact=False
- repeat 2: `['inference_api', 'mcp_tooling', 'tool_calling']` exact=False

### 13. openclaw-openclaw-84795 — unstable_boundary

Title: Windows native: shell env fallback failed with spawnSync /bin/sh ENOENT

Expected: `[]`

pairwise Jaccard `0.500`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.50`, unique sets `2`

Most common predictions: `[{'topics': ['exec_tools', 'reliability'], 'count': 1}, {'topics': ['exec_tools'], 'count': 1}]`

FP: `[('exec_tools', 2), ('reliability', 1)]`

FN: `[]`

Volatile: `[('reliability', 1)]`

- repeat 1: `['exec_tools', 'reliability']` exact=False
- repeat 2: `['exec_tools']` exact=False

### 14. openclaw-openclaw-66685 — unstable_boundary

Title: Suppress expired exec approval followup warnings

Expected: `[]`

pairwise Jaccard `0.500`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.50`, unique sets `2`

Most common predictions: `[{'topics': ['approvals'], 'count': 1}, {'topics': ['approvals', 'exec_tools'], 'count': 1}]`

FP: `[('approvals', 2), ('exec_tools', 1)]`

FN: `[]`

Volatile: `[('exec_tools', 1)]`

- repeat 1: `['approvals']` exact=False
- repeat 2: `['approvals', 'exec_tools']` exact=False

### 15. openclaw-openclaw-60551 — unstable_boundary

Title: Strip leaked reasoning preambles before outbound send

Expected: `[]`

pairwise Jaccard `0.500`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.50`, unique sets `2`

Most common predictions: `[{'topics': ['agent_runtime'], 'count': 1}, {'topics': ['agent_runtime', 'notifications'], 'count': 1}]`

FP: `[('agent_runtime', 2), ('notifications', 1)]`

FN: `[]`

Volatile: `[('notifications', 1)]`

- repeat 1: `['agent_runtime']` exact=False
- repeat 2: `['agent_runtime', 'notifications']` exact=False

### 16. openclaw-openclaw-73910 — unstable_boundary

Title: BUG: OpenClaw-managed Codex ACP uses isolated CODEX_HOME without auth bridge and sends unsupported timeout config

Expected: `[]`

pairwise Jaccard `0.600`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `2`

Most common predictions: `[{'topics': ['acpx', 'auth_identity', 'codex', 'security'], 'count': 1}, {'topics': ['acp', 'acpx', 'codex', 'security'], 'count': 1}]`

FP: `[('acpx', 2), ('codex', 2), ('security', 2), ('auth_identity', 1), ('acp', 1)]`

FN: `[]`

Volatile: `[('acp', 1), ('auth_identity', 1)]`

- repeat 1: `['acpx', 'auth_identity', 'codex', 'security']` exact=False
- repeat 2: `['acp', 'acpx', 'codex', 'security']` exact=False

### 17. openclaw-openclaw-80479 — unstable_boundary

Title: feat(memory/embeddings): add openai-compatible provider for self-hosted servers (llama.cpp, Ollama, vLLM, TGI, LocalAI)

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['memory', 'self_hosted_inference', 'skills_plugins'], 'count': 1}, {'topics': ['memory', 'self_hosted_inference'], 'count': 1}]`

FP: `[('memory', 2), ('self_hosted_inference', 2), ('skills_plugins', 1)]`

FN: `[]`

Volatile: `[('skills_plugins', 1)]`

- repeat 1: `['memory', 'self_hosted_inference', 'skills_plugins']` exact=False
- repeat 2: `['memory', 'self_hosted_inference']` exact=False

### 18. openclaw-openclaw-83333 — unstable_boundary

Title: [Bug]: Memory provider cutover to Ollama leaves production index in mixed OpenAI/Ollama vector state after live sync/reload

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['memory', 'reliability'], 'count': 1}, {'topics': ['memory', 'reliability', 'self_hosted_inference'], 'count': 1}]`

FP: `[('memory', 2), ('reliability', 2), ('self_hosted_inference', 1)]`

FN: `[]`

Volatile: `[('self_hosted_inference', 1)]`

- repeat 1: `['memory', 'reliability']` exact=False
- repeat 2: `['memory', 'reliability', 'self_hosted_inference']` exact=False

### 19. openclaw-openclaw-78936 — unstable_boundary

Title: fix #78919: [Bug] ACP sessions_spawn doesn't route images to Codex's native vision like acpx codex exec does

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'codex', 'coding_agent_integrations'], 'count': 1}, {'topics': ['acp', 'codex'], 'count': 1}]`

FP: `[('acp', 2), ('codex', 2), ('coding_agent_integrations', 1)]`

FN: `[]`

Volatile: `[('coding_agent_integrations', 1)]`

- repeat 1: `['acp', 'codex', 'coding_agent_integrations']` exact=False
- repeat 2: `['acp', 'codex']` exact=False

### 20. openclaw-openclaw-77992 — unstable_boundary

Title: [Bug] Context display shows ?/131k with llama.cpp after upgrading to 2026.5.4 — field name mismatch not resolved

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['inference_api', 'telemetry_usage'], 'count': 1}, {'topics': ['inference_api', 'self_hosted_inference', 'telemetry_usage'], 'count': 1}]`

FP: `[('inference_api', 2), ('telemetry_usage', 2), ('self_hosted_inference', 1)]`

FN: `[]`

Volatile: `[('self_hosted_inference', 1)]`

- repeat 1: `['inference_api', 'telemetry_usage']` exact=False
- repeat 2: `['inference_api', 'self_hosted_inference', 'telemetry_usage']` exact=False

### 21. openclaw-openclaw-59532 — unstable_boundary

Title: Feature Request: Per-agent default model and reasoning_effort in ACPX plugin config

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['acpx', 'config', 'skills_plugins'], 'count': 1}, {'topics': ['acpx', 'config'], 'count': 1}]`

FP: `[('acpx', 2), ('config', 2), ('skills_plugins', 1)]`

FN: `[]`

Volatile: `[('skills_plugins', 1)]`

- repeat 1: `['acpx', 'config', 'skills_plugins']` exact=False
- repeat 2: `['acpx', 'config']` exact=False

### 22. openclaw-openclaw-74305 — unstable_boundary

Title: [Bug]: ACPX Codex worker fails when model/thinking overrides are configured

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['acpx', 'codex'], 'count': 1}, {'topics': ['acp', 'acpx', 'codex'], 'count': 1}]`

FP: `[('acpx', 2), ('codex', 2), ('acp', 1)]`

FN: `[]`

Volatile: `[('acp', 1)]`

- repeat 1: `['acpx', 'codex']` exact=False
- repeat 2: `['acp', 'acpx', 'codex']` exact=False

### 23. openclaw-openclaw-81482 — unstable_boundary

Title: fix(acpx): keep oneshot client alive for initial turn

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'acpx', 'sessions'], 'count': 1}, {'topics': ['acp', 'acpx'], 'count': 1}]`

FP: `[('acp', 2), ('acpx', 2), ('sessions', 1)]`

FN: `[]`

Volatile: `[('sessions', 1)]`

- repeat 1: `['acp', 'acpx', 'sessions']` exact=False
- repeat 2: `['acp', 'acpx']` exact=False

### 24. openclaw-openclaw-46949 — unstable_boundary

Title: fix(acp): release dormant oneshot runtimes under pressure

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'reliability', 'sessions'], 'count': 1}, {'topics': ['acp', 'reliability'], 'count': 1}]`

FP: `[('acp', 2), ('reliability', 2), ('sessions', 1)]`

FN: `[]`

Volatile: `[('sessions', 1)]`

- repeat 1: `['acp', 'reliability', 'sessions']` exact=False
- repeat 2: `['acp', 'reliability']` exact=False

### 25. openclaw-openclaw-64322 — unstable_boundary

Title: fix(acp): assign distinct session keys to Discord threads under the same parent channel

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'chat_integrations'], 'count': 1}, {'topics': ['acp', 'chat_integrations', 'sessions'], 'count': 1}]`

FP: `[('acp', 2), ('chat_integrations', 2), ('sessions', 1)]`

FN: `[]`

Volatile: `[('sessions', 1)]`

- repeat 1: `['acp', 'chat_integrations']` exact=False
- repeat 2: `['acp', 'chat_integrations', 'sessions']` exact=False

### 26. openclaw-openclaw-44375 — unstable_boundary

Title: Adding ACP agent to agents.list silently hijacks all routing from implicit main agent

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['agent_runtime', 'config', 'sessions'], 'count': 1}, {'topics': ['agent_runtime', 'config'], 'count': 1}]`

FP: `[('agent_runtime', 2), ('config', 2), ('sessions', 1)]`

FN: `[]`

Volatile: `[('sessions', 1)]`

- repeat 1: `['agent_runtime', 'config', 'sessions']` exact=False
- repeat 2: `['agent_runtime', 'config']` exact=False

### 27. openclaw-openclaw-82355 — unstable_boundary

Title: Fix streamed chat completions dropping leading less-than

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['api_surface', 'gateway', 'reliability'], 'count': 1}, {'topics': ['api_surface', 'gateway'], 'count': 1}]`

FP: `[('api_surface', 2), ('gateway', 2), ('reliability', 1)]`

FN: `[]`

Volatile: `[('reliability', 1)]`

- repeat 1: `['api_surface', 'gateway', 'reliability']` exact=False
- repeat 2: `['api_surface', 'gateway']` exact=False

### 28. openclaw-openclaw-84660 — unstable_boundary

Title: [Bug] Voice STT: empty moonshine transcripts passed as raw JSON to LLM, clogging serialized processing queue

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['chat_integrations', 'queueing', 'self_hosted_inference'], 'count': 1}, {'topics': ['chat_integrations', 'self_hosted_inference'], 'count': 1}]`

FP: `[('chat_integrations', 2), ('self_hosted_inference', 2), ('queueing', 1)]`

FN: `[]`

Volatile: `[('queueing', 1)]`

- repeat 1: `['chat_integrations', 'queueing', 'self_hosted_inference']` exact=False
- repeat 2: `['chat_integrations', 'self_hosted_inference']` exact=False

### 29. openclaw-openclaw-72013 — unstable_boundary

Title: ACP startup identity reconcile warns on terminal one-shot sessions

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'sessions'], 'count': 1}, {'topics': ['acp', 'gateway', 'sessions'], 'count': 1}]`

FP: `[('acp', 2), ('sessions', 2), ('gateway', 1)]`

FN: `[]`

Volatile: `[('gateway', 1)]`

- repeat 1: `['acp', 'sessions']` exact=False
- repeat 2: `['acp', 'gateway', 'sessions']` exact=False

### 30. openclaw-openclaw-83030 — unstable_boundary

Title: feat(image-generation): Add ReCraft V4.1 model family support (Standard, Utility, Vector) via OpenRouter

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['api_surface', 'inference_api', 'model_lifecycle'], 'count': 1}, {'topics': ['inference_api', 'model_lifecycle'], 'count': 1}]`

FP: `[('inference_api', 2), ('model_lifecycle', 2), ('api_surface', 1)]`

FN: `[]`

Volatile: `[('api_surface', 1)]`

- repeat 1: `['api_surface', 'inference_api', 'model_lifecycle']` exact=False
- repeat 2: `['inference_api', 'model_lifecycle']` exact=False
