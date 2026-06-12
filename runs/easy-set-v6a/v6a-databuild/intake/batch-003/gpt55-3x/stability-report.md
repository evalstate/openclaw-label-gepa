# OpenClaw easy-set stability report

Rows: `30`  Repeats: `3`

## Prediction stability

- pairwise exact: `0.600`
- pairwise Jaccard: `0.871`
- pairwise symdiff: `0.511`

## Buckets

- `review`: 9
- `stable_wrong`: 14
- `unstable_boundary`: 7

## Repeat metric summary

- `avg_expected_topics`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `avg_predicted_topics`: mean `3.4556`, pstdev `0.0416`, values `[3.4, 3.5, 3.4667]`
- `avg_row_jaccard`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `avg_row_symdiff`: mean `3.4556`, pstdev `0.0416`, values `[3.4, 3.5, 3.4667]`
- `exact_match`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `gepa_score`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `row_exact_accuracy`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `row_symdiff_score`: mean `0.2245`, pstdev `0.0021`, values `[0.2273, 0.2222, 0.2239]`
- `topic_micro_f1`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `topic_micro_precision`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0, 0.0]`
- `topic_micro_recall`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0, 1.0]`
- `valid_json`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0, 1.0]`

## Least stable / review rows

### 1. openclaw-openclaw-62769 — unstable_boundary

Title: [Feature]: Support ACP configured bindings for Telegram DMs (not just groups/topics)

Expected: `[]`

pairwise Jaccard `0.611`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.67`, unique sets `3`

Most common predictions: `[{'topics': ['acp', 'chat_integrations', 'sessions'], 'count': 1}, {'topics': ['acp', 'chat_integrations', 'config'], 'count': 1}, {'topics': ['acp', 'chat_integrations'], 'count': 1}]`

FP: `[('acp', 3), ('chat_integrations', 3), ('sessions', 1), ('config', 1)]`

FN: `[]`

Volatile: `[('config', 1), ('sessions', 1)]`

- repeat 1: `['acp', 'chat_integrations', 'sessions']` exact=False
- repeat 2: `['acp', 'chat_integrations', 'config']` exact=False
- repeat 3: `['acp', 'chat_integrations']` exact=False

### 2. openclaw-openclaw-72016 — unstable_boundary

Title: [Feature]: doctor api/extendability

Expected: `[]`

pairwise Jaccard `0.611`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.67`, unique sets `3`

Most common predictions: `[{'topics': ['api_surface', 'skills_plugins', 'telemetry_usage'], 'count': 1}, {'topics': ['api_surface', 'config', 'skills_plugins'], 'count': 1}, {'topics': ['api_surface', 'skills_plugins'], 'count': 1}]`

FP: `[('api_surface', 3), ('skills_plugins', 3), ('telemetry_usage', 1), ('config', 1)]`

FN: `[]`

Volatile: `[('config', 1), ('telemetry_usage', 1)]`

- repeat 1: `['api_surface', 'skills_plugins', 'telemetry_usage']` exact=False
- repeat 2: `['api_surface', 'config', 'skills_plugins']` exact=False
- repeat 3: `['api_surface', 'skills_plugins']` exact=False

### 3. openclaw-openclaw-77748 — unstable_boundary

Title: fix: Codex startup plugins + WhatsApp history & Docker Codex OAuth

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `3`

Most common predictions: `[{'topics': ['chat_integrations', 'codex', 'packaging_deployment', 'security', 'skills_plugins'], 'count': 1}, {'topics': ['chat_integrations', 'codex', 'gateway', 'packaging_deployment', 'skills_plugins'], 'count': 1}, {'topics': ['chat_integrations', 'codex', 'coding_agent_integrations', 'packaging_deployment', 'skills_plugins'], 'count': 1}]`

FP: `[('chat_integrations', 3), ('codex', 3), ('packaging_deployment', 3), ('skills_plugins', 3), ('security', 1), ('gateway', 1), ('coding_agent_integrations', 1)]`

FN: `[]`

Volatile: `[('coding_agent_integrations', 1), ('gateway', 1), ('security', 1)]`

- repeat 1: `['chat_integrations', 'codex', 'packaging_deployment', 'security', 'skills_plugins']` exact=False
- repeat 2: `['chat_integrations', 'codex', 'gateway', 'packaging_deployment', 'skills_plugins']` exact=False
- repeat 3: `['chat_integrations', 'codex', 'coding_agent_integrations', 'packaging_deployment', 'skills_plugins']` exact=False

### 4. openclaw-openclaw-65187 — unstable_boundary

Title: test: add regression tests for <final> tag stripping in UI message extraction

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.33`, unique sets `2`

Most common predictions: `[{'topics': ['tests_ci'], 'count': 2}, {'topics': ['tests_ci', 'ui_tui'], 'count': 1}]`

FP: `[('tests_ci', 3), ('ui_tui', 1)]`

FN: `[]`

Volatile: `[('ui_tui', 1)]`

- repeat 1: `['tests_ci']` exact=False
- repeat 2: `['tests_ci']` exact=False
- repeat 3: `['tests_ci', 'ui_tui']` exact=False

### 5. openclaw-openclaw-66125 — unstable_boundary

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

### 6. openclaw-openclaw-77827 — unstable_boundary

Title: fix: LM Studio thinking blocks invisible with Responses API

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.33`, unique sets `2`

Most common predictions: `[{'topics': ['inference_api'], 'count': 2}, {'topics': ['inference_api', 'self_hosted_inference'], 'count': 1}]`

FP: `[('inference_api', 3), ('self_hosted_inference', 1)]`

FN: `[]`

Volatile: `[('self_hosted_inference', 1)]`

- repeat 1: `['inference_api']` exact=False
- repeat 2: `['inference_api']` exact=False
- repeat 3: `['inference_api', 'self_hosted_inference']` exact=False

### 7. openclaw-openclaw-62552 — unstable_boundary

Title: fix(acp): stabilize bridge session keys

Expected: `[]`

pairwise Jaccard `0.717`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `3`

Most common predictions: `[{'topics': ['acp', 'queueing', 'sessions'], 'count': 1}, {'topics': ['acp', 'gateway', 'queueing', 'reliability', 'sessions'], 'count': 1}, {'topics': ['acp', 'queueing', 'reliability', 'sessions'], 'count': 1}]`

FP: `[('acp', 3), ('queueing', 3), ('sessions', 3), ('reliability', 2), ('gateway', 1)]`

FN: `[]`

Volatile: `[('reliability', 2), ('gateway', 1)]`

- repeat 1: `['acp', 'queueing', 'sessions']` exact=False
- repeat 2: `['acp', 'gateway', 'queueing', 'reliability', 'sessions']` exact=False
- repeat 3: `['acp', 'queueing', 'reliability', 'sessions']` exact=False

### 8. openclaw-openclaw-63007 — review

Title: Pass outbound session identity into message_sending and surface guarded gateway send denial

Expected: `[]`

pairwise Jaccard `0.778`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `2`

Most common predictions: `[{'topics': ['gateway', 'hooks', 'notifications', 'security', 'sessions'], 'count': 2}, {'topics': ['gateway', 'hooks', 'notifications', 'sessions', 'skills_plugins'], 'count': 1}]`

FP: `[('gateway', 3), ('hooks', 3), ('notifications', 3), ('sessions', 3), ('security', 2), ('skills_plugins', 1)]`

FN: `[]`

Volatile: `[('security', 2), ('skills_plugins', 1)]`

- repeat 1: `['gateway', 'hooks', 'notifications', 'security', 'sessions']` exact=False
- repeat 2: `['gateway', 'hooks', 'notifications', 'security', 'sessions']` exact=False
- repeat 3: `['gateway', 'hooks', 'notifications', 'sessions', 'skills_plugins']` exact=False

### 9. openclaw-openclaw-69260 — review

Title: Harden Gemini ACP integration against ambient API-key fallback and add generic auth-contract hooks for ACP agents

Expected: `[]`

pairwise Jaccard `0.778`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'acpx', 'coding_agent_integrations', 'config', 'security'], 'count': 2}, {'topics': ['acp', 'acpx', 'auth_identity', 'coding_agent_integrations', 'security'], 'count': 1}]`

FP: `[('acp', 3), ('acpx', 3), ('coding_agent_integrations', 3), ('security', 3), ('config', 2), ('auth_identity', 1)]`

FN: `[]`

Volatile: `[('config', 2), ('auth_identity', 1)]`

- repeat 1: `['acp', 'acpx', 'coding_agent_integrations', 'config', 'security']` exact=False
- repeat 2: `['acp', 'acpx', 'coding_agent_integrations', 'config', 'security']` exact=False
- repeat 3: `['acp', 'acpx', 'auth_identity', 'coding_agent_integrations', 'security']` exact=False

### 10. openclaw-openclaw-63229 — review

Title: Bug: Gateway falsely marks healthy local vLLM endpoints as timed out/overloaded, causing 1–23 min fallback cascades

Expected: `[]`

pairwise Jaccard `0.833`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.33`, unique sets `2`

Most common predictions: `[{'topics': ['gateway', 'inference_api', 'reliability'], 'count': 2}, {'topics': ['gateway', 'inference_api', 'reliability', 'self_hosted_inference'], 'count': 1}]`

FP: `[('gateway', 3), ('inference_api', 3), ('reliability', 3), ('self_hosted_inference', 1)]`

FN: `[]`

Volatile: `[('self_hosted_inference', 1)]`

- repeat 1: `['gateway', 'inference_api', 'reliability']` exact=False
- repeat 2: `['gateway', 'inference_api', 'reliability', 'self_hosted_inference']` exact=False
- repeat 3: `['gateway', 'inference_api', 'reliability']` exact=False

### 11. openclaw-openclaw-69256 — review

Title: fix(cron): prevent premature session cleanup when subagents are running

Expected: `[]`

pairwise Jaccard `0.833`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.67`, unique sets `2`

Most common predictions: `[{'topics': ['agent_runtime', 'cron_automation', 'reliability', 'sessions'], 'count': 2}, {'topics': ['cron_automation', 'reliability', 'sessions'], 'count': 1}]`

FP: `[('cron_automation', 3), ('reliability', 3), ('sessions', 3), ('agent_runtime', 2)]`

FN: `[]`

Volatile: `[('agent_runtime', 2)]`

- repeat 1: `['cron_automation', 'reliability', 'sessions']` exact=False
- repeat 2: `['agent_runtime', 'cron_automation', 'reliability', 'sessions']` exact=False
- repeat 3: `['agent_runtime', 'cron_automation', 'reliability', 'sessions']` exact=False

### 12. openclaw-openclaw-69328 — review

Title: fix(acp): avoid false zero-diff failures and append session messages

Expected: `[]`

pairwise Jaccard `0.833`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.33`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'sessions', 'ui_tui'], 'count': 2}, {'topics': ['acp', 'queueing', 'sessions', 'ui_tui'], 'count': 1}]`

FP: `[('acp', 3), ('sessions', 3), ('ui_tui', 3), ('queueing', 1)]`

FN: `[]`

Volatile: `[('queueing', 1)]`

- repeat 1: `['acp', 'sessions', 'ui_tui']` exact=False
- repeat 2: `['acp', 'sessions', 'ui_tui']` exact=False
- repeat 3: `['acp', 'queueing', 'sessions', 'ui_tui']` exact=False

### 13. openclaw-openclaw-67244 — review

Title: Explicit ACP agent runs: embedded backend visibility failure and stale final JSON state after sessions_yield

Expected: `[]`

pairwise Jaccard `0.867`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.33`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'acpx', 'api_surface', 'sessions'], 'count': 2}, {'topics': ['acp', 'acpx', 'agent_runtime', 'api_surface', 'sessions'], 'count': 1}]`

FP: `[('acp', 3), ('acpx', 3), ('api_surface', 3), ('sessions', 3), ('agent_runtime', 1)]`

FN: `[]`

Volatile: `[('agent_runtime', 1)]`

- repeat 1: `['acp', 'acpx', 'agent_runtime', 'api_surface', 'sessions']` exact=False
- repeat 2: `['acp', 'acpx', 'api_surface', 'sessions']` exact=False
- repeat 3: `['acp', 'acpx', 'api_surface', 'sessions']` exact=False

### 14. openclaw-openclaw-72015 — review

Title: Reliability: active-memory blocks replies and QMD boot initialization can overload multi-agent gateways

Expected: `[]`

pairwise Jaccard `0.867`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.67`, unique sets `2`

Most common predictions: `[{'topics': ['config', 'gateway', 'memory', 'reliability', 'skills_plugins'], 'count': 2}, {'topics': ['gateway', 'memory', 'reliability', 'skills_plugins'], 'count': 1}]`

FP: `[('gateway', 3), ('memory', 3), ('reliability', 3), ('skills_plugins', 3), ('config', 2)]`

FN: `[]`

Volatile: `[('config', 2)]`

- repeat 1: `['gateway', 'memory', 'reliability', 'skills_plugins']` exact=False
- repeat 2: `['config', 'gateway', 'memory', 'reliability', 'skills_plugins']` exact=False
- repeat 3: `['config', 'gateway', 'memory', 'reliability', 'skills_plugins']` exact=False

### 15. openclaw-openclaw-74204 — review

Title: memory.qmd.update.embedTimeoutMs default (120 s) is too low for local GGUF; error message doesn't surface the fix

Expected: `[]`

pairwise Jaccard `0.867`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.67`, unique sets `2`

Most common predictions: `[{'topics': ['config', 'local_models', 'memory', 'reliability', 'telemetry_usage'], 'count': 2}, {'topics': ['config', 'local_models', 'memory', 'reliability'], 'count': 1}]`

FP: `[('config', 3), ('local_models', 3), ('memory', 3), ('reliability', 3), ('telemetry_usage', 2)]`

FN: `[]`

Volatile: `[('telemetry_usage', 2)]`

- repeat 1: `['config', 'local_models', 'memory', 'reliability', 'telemetry_usage']` exact=False
- repeat 2: `['config', 'local_models', 'memory', 'reliability', 'telemetry_usage']` exact=False
- repeat 3: `['config', 'local_models', 'memory', 'reliability']` exact=False

### 16. openclaw-openclaw-75657 — review

Title: fix: local GGUF embedding model warmup blocks Node.js event loop for minutes on startup (ARM64/Pi)

Expected: `[]`

pairwise Jaccard `0.867`, pairwise exact `0.333`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.33`, unique sets `2`

Most common predictions: `[{'topics': ['gateway', 'memory', 'reliability', 'self_hosted_inference'], 'count': 2}, {'topics': ['gateway', 'local_models', 'memory', 'reliability', 'self_hosted_inference'], 'count': 1}]`

FP: `[('gateway', 3), ('memory', 3), ('reliability', 3), ('self_hosted_inference', 3), ('local_models', 1)]`

FN: `[]`

Volatile: `[('local_models', 1)]`

- repeat 1: `['gateway', 'memory', 'reliability', 'self_hosted_inference']` exact=False
- repeat 2: `['gateway', 'memory', 'reliability', 'self_hosted_inference']` exact=False
- repeat 3: `['gateway', 'local_models', 'memory', 'reliability', 'self_hosted_inference']` exact=False

### 17. openclaw-openclaw-62428 — stable_wrong

Title: test(exec): land exec v2 contract follow-through

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `1`

Most common predictions: `[{'topics': ['approvals', 'config', 'exec_tools', 'security'], 'count': 3}]`

FP: `[('approvals', 3), ('config', 3), ('exec_tools', 3), ('security', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['approvals', 'config', 'exec_tools', 'security']` exact=False
- repeat 2: `['approvals', 'config', 'exec_tools', 'security']` exact=False
- repeat 3: `['approvals', 'config', 'exec_tools', 'security']` exact=False

### 18. openclaw-openclaw-64199 — stable_wrong

Title: [Bug]: ACP configured binding uses parent channel ID for session key — all threads under same channel share one persistent Claude Code process

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'acpx', 'chat_integrations', 'security', 'sessions'], 'count': 3}]`

FP: `[('acp', 3), ('acpx', 3), ('chat_integrations', 3), ('security', 3), ('sessions', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'acpx', 'chat_integrations', 'security', 'sessions']` exact=False
- repeat 2: `['acp', 'acpx', 'chat_integrations', 'security', 'sessions']` exact=False
- repeat 3: `['acp', 'acpx', 'chat_integrations', 'security', 'sessions']` exact=False

### 19. openclaw-openclaw-64317 — stable_wrong

Title: [Bug]: Headed Chromium viewport screenshots time out on Omarchy/Hyprland/Wayland after successful page load

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['browser_automation', 'reliability'], 'count': 3}]`

FP: `[('browser_automation', 3), ('reliability', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['browser_automation', 'reliability']` exact=False
- repeat 2: `['browser_automation', 'reliability']` exact=False
- repeat 3: `['browser_automation', 'reliability']` exact=False

### 20. openclaw-openclaw-65364 — stable_wrong

Title: feat(plugins): add registerProviderRuntimeAuthOverride API

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `1`

Most common predictions: `[{'topics': ['api_surface', 'inference_api', 'security', 'skills_plugins'], 'count': 3}]`

FP: `[('api_surface', 3), ('inference_api', 3), ('security', 3), ('skills_plugins', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['api_surface', 'inference_api', 'security', 'skills_plugins']` exact=False
- repeat 2: `['api_surface', 'inference_api', 'security', 'skills_plugins']` exact=False
- repeat 3: `['api_surface', 'inference_api', 'security', 'skills_plugins']` exact=False

### 21. openclaw-openclaw-67539 — stable_wrong

Title: [Feature]: Add provider-specific TTS prompt hints

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['inference_api'], 'count': 3}]`

FP: `[('inference_api', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['inference_api']` exact=False
- repeat 2: `['inference_api']` exact=False
- repeat 3: `['inference_api']` exact=False

### 22. openclaw-openclaw-68725 — stable_wrong

Title: feat(amazon-bedrock-mantle): add known context windows for open-weight Mantle models

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['inference_api', 'model_lifecycle'], 'count': 3}]`

FP: `[('inference_api', 3), ('model_lifecycle', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['inference_api', 'model_lifecycle']` exact=False
- repeat 2: `['inference_api', 'model_lifecycle']` exact=False
- repeat 3: `['inference_api', 'model_lifecycle']` exact=False

### 23. openclaw-openclaw-68843 — stable_wrong

Title: fix(acp): treat missing cwd as stale bound session

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'reliability', 'sessions'], 'count': 3}]`

FP: `[('acp', 3), ('reliability', 3), ('sessions', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'reliability', 'sessions']` exact=False
- repeat 2: `['acp', 'reliability', 'sessions']` exact=False
- repeat 3: `['acp', 'reliability', 'sessions']` exact=False

### 24. openclaw-openclaw-69669 — stable_wrong

Title: ACP: keep thread-bound follow-ups parent-orchestrated by default, not raw pass-through

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'agent_runtime', 'sessions'], 'count': 3}]`

FP: `[('acp', 3), ('agent_runtime', 3), ('sessions', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'agent_runtime', 'sessions']` exact=False
- repeat 2: `['acp', 'agent_runtime', 'sessions']` exact=False
- repeat 3: `['acp', 'agent_runtime', 'sessions']` exact=False

### 25. openclaw-openclaw-71216 — stable_wrong

Title: Config schema: add `sandbox`, `routing.rules`, `instances`, and `gateway.nodes.denyPaths`

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'gateway', 'inference_api', 'sandboxing', 'security'], 'count': 3}]`

FP: `[('config', 3), ('gateway', 3), ('inference_api', 3), ('sandboxing', 3), ('security', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'gateway', 'inference_api', 'sandboxing', 'security']` exact=False
- repeat 2: `['config', 'gateway', 'inference_api', 'sandboxing', 'security']` exact=False
- repeat 3: `['config', 'gateway', 'inference_api', 'sandboxing', 'security']` exact=False

### 26. openclaw-openclaw-71537 — stable_wrong

Title: Recover archived (.reset) session transcripts in memory hook + session-logs skill

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `1`

Most common predictions: `[{'topics': ['docs', 'hooks', 'memory', 'sessions', 'skills_plugins'], 'count': 3}]`

FP: `[('docs', 3), ('hooks', 3), ('memory', 3), ('sessions', 3), ('skills_plugins', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['docs', 'hooks', 'memory', 'sessions', 'skills_plugins']` exact=False
- repeat 2: `['docs', 'hooks', 'memory', 'sessions', 'skills_plugins']` exact=False
- repeat 3: `['docs', 'hooks', 'memory', 'sessions', 'skills_plugins']` exact=False

### 27. openclaw-openclaw-71594 — stable_wrong

Title: docs(gateway): clarify IPv4-only BYOH bind path

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['docs', 'gateway'], 'count': 3}]`

FP: `[('docs', 3), ('gateway', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['docs', 'gateway']` exact=False
- repeat 2: `['docs', 'gateway']` exact=False
- repeat 3: `['docs', 'gateway']` exact=False

### 28. openclaw-openclaw-72001 — stable_wrong

Title: fix(hooks): write allowedSessionKeyPrefixes from gmail wizard

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'hooks', 'security'], 'count': 3}]`

FP: `[('config', 3), ('hooks', 3), ('security', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'hooks', 'security']` exact=False
- repeat 2: `['config', 'hooks', 'security']` exact=False
- repeat 3: `['config', 'hooks', 'security']` exact=False

### 29. openclaw-openclaw-72087 — stable_wrong

Title: Bug: dist/entry.js main-path breaks Codex OAuth image generation on Linux while direct runCli()/provider path succeeds

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['codex', 'inference_api', 'packaging_deployment'], 'count': 3}]`

FP: `[('codex', 3), ('inference_api', 3), ('packaging_deployment', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['codex', 'inference_api', 'packaging_deployment']` exact=False
- repeat 2: `['codex', 'inference_api', 'packaging_deployment']` exact=False
- repeat 3: `['codex', 'inference_api', 'packaging_deployment']` exact=False

### 30. openclaw-openclaw-73910 — stable_wrong

Title: BUG: OpenClaw-managed Codex ACP uses isolated CODEX_HOME without auth bridge and sends unsupported timeout config

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'acpx', 'codex', 'coding_agent_integrations', 'security'], 'count': 3}]`

FP: `[('acp', 3), ('acpx', 3), ('codex', 3), ('coding_agent_integrations', 3), ('security', 3)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'acpx', 'codex', 'coding_agent_integrations', 'security']` exact=False
- repeat 2: `['acp', 'acpx', 'codex', 'coding_agent_integrations', 'security']` exact=False
- repeat 3: `['acp', 'acpx', 'codex', 'coding_agent_integrations', 'security']` exact=False
