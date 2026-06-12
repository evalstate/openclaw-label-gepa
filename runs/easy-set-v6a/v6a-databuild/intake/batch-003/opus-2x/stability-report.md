# OpenClaw easy-set stability report

Rows: `30`  Repeats: `2`

## Prediction stability

- pairwise exact: `0.833`
- pairwise Jaccard: `0.944`
- pairwise symdiff: `0.167`

## Buckets

- `stable_wrong`: 25
- `unstable_boundary`: 5

## Repeat metric summary

- `avg_expected_topics`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `avg_predicted_topics`: mean `2.7833`, pstdev `0.0167`, values `[2.8, 2.7667]`
- `avg_row_jaccard`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `avg_row_symdiff`: mean `2.7833`, pstdev `0.0167`, values `[2.8, 2.7667]`
- `exact_match`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `gepa_score`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `row_exact_accuracy`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `row_symdiff_score`: mean `0.2643`, pstdev `0.0012`, values `[0.2632, 0.2655]`
- `topic_micro_f1`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `topic_micro_precision`: mean `0.0000`, pstdev `0.0000`, values `[0.0, 0.0]`
- `topic_micro_recall`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0]`
- `valid_json`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0]`

## Least stable / review rows

### 1. openclaw-openclaw-68725 — unstable_boundary

Title: feat(amazon-bedrock-mantle): add known context windows for open-weight Mantle models

Expected: `[]`

pairwise Jaccard `0.500`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.50`, unique sets `2`

Most common predictions: `[{'topics': ['inference_api', 'model_lifecycle'], 'count': 1}, {'topics': ['model_lifecycle'], 'count': 1}]`

FP: `[('model_lifecycle', 2), ('inference_api', 1)]`

FN: `[]`

Volatile: `[('inference_api', 1)]`

- repeat 1: `['inference_api', 'model_lifecycle']` exact=False
- repeat 2: `['model_lifecycle']` exact=False

### 2. openclaw-openclaw-69328 — unstable_boundary

Title: fix(acp): avoid false zero-diff failures and append session messages

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'ui_tui'], 'count': 1}, {'topics': ['acp', 'reliability', 'ui_tui'], 'count': 1}]`

FP: `[('acp', 2), ('ui_tui', 2), ('reliability', 1)]`

FN: `[]`

Volatile: `[('reliability', 1)]`

- repeat 1: `['acp', 'ui_tui']` exact=False
- repeat 2: `['acp', 'reliability', 'ui_tui']` exact=False

### 3. openclaw-openclaw-69669 — unstable_boundary

Title: ACP: keep thread-bound follow-ups parent-orchestrated by default, not raw pass-through

Expected: `[]`

pairwise Jaccard `0.667`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.50`, unique sets `2`

Most common predictions: `[{'topics': ['acp', 'sessions'], 'count': 1}, {'topics': ['acp', 'agent_runtime', 'sessions'], 'count': 1}]`

FP: `[('acp', 2), ('sessions', 2), ('agent_runtime', 1)]`

FN: `[]`

Volatile: `[('agent_runtime', 1)]`

- repeat 1: `['acp', 'sessions']` exact=False
- repeat 2: `['acp', 'agent_runtime', 'sessions']` exact=False

### 4. openclaw-openclaw-74204 — unstable_boundary

Title: memory.qmd.update.embedTimeoutMs default (120 s) is too low for local GGUF; error message doesn't surface the fix

Expected: `[]`

pairwise Jaccard `0.750`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.50`, unique sets `2`

Most common predictions: `[{'topics': ['config', 'local_models', 'memory', 'reliability'], 'count': 1}, {'topics': ['config', 'local_models', 'memory'], 'count': 1}]`

FP: `[('config', 2), ('local_models', 2), ('memory', 2), ('reliability', 1)]`

FN: `[]`

Volatile: `[('reliability', 1)]`

- repeat 1: `['config', 'local_models', 'memory', 'reliability']` exact=False
- repeat 2: `['config', 'local_models', 'memory']` exact=False

### 5. openclaw-openclaw-75657 — unstable_boundary

Title: fix: local GGUF embedding model warmup blocks Node.js event loop for minutes on startup (ARM64/Pi)

Expected: `[]`

pairwise Jaccard `0.750`, pairwise exact `0.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.50`, unique sets `2`

Most common predictions: `[{'topics': ['local_models', 'memory', 'reliability', 'self_hosted_inference'], 'count': 1}, {'topics': ['memory', 'reliability', 'self_hosted_inference'], 'count': 1}]`

FP: `[('memory', 2), ('reliability', 2), ('self_hosted_inference', 2), ('local_models', 1)]`

FN: `[]`

Volatile: `[('local_models', 1)]`

- repeat 1: `['local_models', 'memory', 'reliability', 'self_hosted_inference']` exact=False
- repeat 2: `['memory', 'reliability', 'self_hosted_inference']` exact=False

### 6. openclaw-openclaw-62428 — stable_wrong

Title: test(exec): land exec v2 contract follow-through

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `1`

Most common predictions: `[{'topics': ['approvals', 'config', 'exec_tools', 'security'], 'count': 2}]`

FP: `[('approvals', 2), ('config', 2), ('exec_tools', 2), ('security', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['approvals', 'config', 'exec_tools', 'security']` exact=False
- repeat 2: `['approvals', 'config', 'exec_tools', 'security']` exact=False

### 7. openclaw-openclaw-62552 — stable_wrong

Title: fix(acp): stabilize bridge session keys

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'reliability', 'sessions'], 'count': 2}]`

FP: `[('acp', 2), ('reliability', 2), ('sessions', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'reliability', 'sessions']` exact=False
- repeat 2: `['acp', 'reliability', 'sessions']` exact=False

### 8. openclaw-openclaw-62769 — stable_wrong

Title: [Feature]: Support ACP configured bindings for Telegram DMs (not just groups/topics)

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'chat_integrations'], 'count': 2}]`

FP: `[('acp', 2), ('chat_integrations', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'chat_integrations']` exact=False
- repeat 2: `['acp', 'chat_integrations']` exact=False

### 9. openclaw-openclaw-63007 — stable_wrong

Title: Pass outbound session identity into message_sending and surface guarded gateway send denial

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['gateway', 'hooks', 'notifications'], 'count': 2}]`

FP: `[('gateway', 2), ('hooks', 2), ('notifications', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['gateway', 'hooks', 'notifications']` exact=False
- repeat 2: `['gateway', 'hooks', 'notifications']` exact=False

### 10. openclaw-openclaw-63229 — stable_wrong

Title: Bug: Gateway falsely marks healthy local vLLM endpoints as timed out/overloaded, causing 1–23 min fallback cascades

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['agent_runtime', 'gateway', 'reliability'], 'count': 2}]`

FP: `[('agent_runtime', 2), ('gateway', 2), ('reliability', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['agent_runtime', 'gateway', 'reliability']` exact=False
- repeat 2: `['agent_runtime', 'gateway', 'reliability']` exact=False

### 11. openclaw-openclaw-64199 — stable_wrong

Title: [Bug]: ACP configured binding uses parent channel ID for session key — all threads under same channel share one persistent Claude Code process

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'acpx', 'sessions'], 'count': 2}]`

FP: `[('acp', 2), ('acpx', 2), ('sessions', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'acpx', 'sessions']` exact=False
- repeat 2: `['acp', 'acpx', 'sessions']` exact=False

### 12. openclaw-openclaw-64317 — stable_wrong

Title: [Bug]: Headed Chromium viewport screenshots time out on Omarchy/Hyprland/Wayland after successful page load

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['browser_automation', 'reliability'], 'count': 2}]`

FP: `[('browser_automation', 2), ('reliability', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['browser_automation', 'reliability']` exact=False
- repeat 2: `['browser_automation', 'reliability']` exact=False

### 13. openclaw-openclaw-65187 — stable_wrong

Title: test: add regression tests for <final> tag stripping in UI message extraction

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['tests_ci'], 'count': 2}]`

FP: `[('tests_ci', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['tests_ci']` exact=False
- repeat 2: `['tests_ci']` exact=False

### 14. openclaw-openclaw-65364 — stable_wrong

Title: feat(plugins): add registerProviderRuntimeAuthOverride API

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['inference_api', 'security', 'skills_plugins'], 'count': 2}]`

FP: `[('inference_api', 2), ('security', 2), ('skills_plugins', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['inference_api', 'security', 'skills_plugins']` exact=False
- repeat 2: `['inference_api', 'security', 'skills_plugins']` exact=False

### 15. openclaw-openclaw-66125 — stable_wrong

Title: [Bug]: openai-completions fallback candidate is selected, but fallback does not complete successfully through an OpenAI-compatible proxy

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['inference_api'], 'count': 2}]`

FP: `[('inference_api', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['inference_api']` exact=False
- repeat 2: `['inference_api']` exact=False

### 16. openclaw-openclaw-67244 — stable_wrong

Title: Explicit ACP agent runs: embedded backend visibility failure and stale final JSON state after sessions_yield

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'acpx', 'reliability', 'sessions'], 'count': 2}]`

FP: `[('acp', 2), ('acpx', 2), ('reliability', 2), ('sessions', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'acpx', 'reliability', 'sessions']` exact=False
- repeat 2: `['acp', 'acpx', 'reliability', 'sessions']` exact=False

### 17. openclaw-openclaw-67539 — stable_wrong

Title: [Feature]: Add provider-specific TTS prompt hints

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['inference_api'], 'count': 2}]`

FP: `[('inference_api', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['inference_api']` exact=False
- repeat 2: `['inference_api']` exact=False

### 18. openclaw-openclaw-68843 — stable_wrong

Title: fix(acp): treat missing cwd as stale bound session

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'reliability', 'sessions'], 'count': 2}]`

FP: `[('acp', 2), ('reliability', 2), ('sessions', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'reliability', 'sessions']` exact=False
- repeat 2: `['acp', 'reliability', 'sessions']` exact=False

### 19. openclaw-openclaw-69256 — stable_wrong

Title: fix(cron): prevent premature session cleanup when subagents are running

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['cron_automation', 'reliability', 'sessions'], 'count': 2}]`

FP: `[('cron_automation', 2), ('reliability', 2), ('sessions', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['cron_automation', 'reliability', 'sessions']` exact=False
- repeat 2: `['cron_automation', 'reliability', 'sessions']` exact=False

### 20. openclaw-openclaw-69260 — stable_wrong

Title: Harden Gemini ACP integration against ambient API-key fallback and add generic auth-contract hooks for ACP agents

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'auth_identity', 'coding_agent_integrations', 'security'], 'count': 2}]`

FP: `[('acp', 2), ('auth_identity', 2), ('coding_agent_integrations', 2), ('security', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'auth_identity', 'coding_agent_integrations', 'security']` exact=False
- repeat 2: `['acp', 'auth_identity', 'coding_agent_integrations', 'security']` exact=False

### 21. openclaw-openclaw-71216 — stable_wrong

Title: Config schema: add `sandbox`, `routing.rules`, `instances`, and `gateway.nodes.denyPaths`

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'gateway', 'inference_api', 'sandboxing', 'security'], 'count': 2}]`

FP: `[('config', 2), ('gateway', 2), ('inference_api', 2), ('sandboxing', 2), ('security', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'gateway', 'inference_api', 'sandboxing', 'security']` exact=False
- repeat 2: `['config', 'gateway', 'inference_api', 'sandboxing', 'security']` exact=False

### 22. openclaw-openclaw-71537 — stable_wrong

Title: Recover archived (.reset) session transcripts in memory hook + session-logs skill

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['memory', 'sessions', 'skills_plugins'], 'count': 2}]`

FP: `[('memory', 2), ('sessions', 2), ('skills_plugins', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['memory', 'sessions', 'skills_plugins']` exact=False
- repeat 2: `['memory', 'sessions', 'skills_plugins']` exact=False

### 23. openclaw-openclaw-71594 — stable_wrong

Title: docs(gateway): clarify IPv4-only BYOH bind path

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['docs', 'gateway'], 'count': 2}]`

FP: `[('docs', 2), ('gateway', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['docs', 'gateway']` exact=False
- repeat 2: `['docs', 'gateway']` exact=False

### 24. openclaw-openclaw-72001 — stable_wrong

Title: fix(hooks): write allowedSessionKeyPrefixes from gmail wizard

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'hooks'], 'count': 2}]`

FP: `[('config', 2), ('hooks', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'hooks']` exact=False
- repeat 2: `['config', 'hooks']` exact=False

### 25. openclaw-openclaw-72015 — stable_wrong

Title: Reliability: active-memory blocks replies and QMD boot initialization can overload multi-agent gateways

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['gateway', 'memory', 'reliability'], 'count': 2}]`

FP: `[('gateway', 2), ('memory', 2), ('reliability', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['gateway', 'memory', 'reliability']` exact=False
- repeat 2: `['gateway', 'memory', 'reliability']` exact=False

### 26. openclaw-openclaw-72016 — stable_wrong

Title: [Feature]: doctor api/extendability

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['skills_plugins'], 'count': 2}]`

FP: `[('skills_plugins', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['skills_plugins']` exact=False
- repeat 2: `['skills_plugins']` exact=False

### 27. openclaw-openclaw-72087 — stable_wrong

Title: Bug: dist/entry.js main-path breaks Codex OAuth image generation on Linux while direct runCli()/provider path succeeds

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['codex', 'inference_api', 'packaging_deployment'], 'count': 2}]`

FP: `[('codex', 2), ('inference_api', 2), ('packaging_deployment', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['codex', 'inference_api', 'packaging_deployment']` exact=False
- repeat 2: `['codex', 'inference_api', 'packaging_deployment']` exact=False

### 28. openclaw-openclaw-73910 — stable_wrong

Title: BUG: OpenClaw-managed Codex ACP uses isolated CODEX_HOME without auth bridge and sends unsupported timeout config

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `4.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'acpx', 'codex', 'security'], 'count': 2}]`

FP: `[('acp', 2), ('acpx', 2), ('codex', 2), ('security', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'acpx', 'codex', 'security']` exact=False
- repeat 2: `['acp', 'acpx', 'codex', 'security']` exact=False

### 29. openclaw-openclaw-77748 — stable_wrong

Title: fix: Codex startup plugins + WhatsApp history & Docker Codex OAuth

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `5.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'codex', 'gateway', 'packaging_deployment', 'skills_plugins'], 'count': 2}]`

FP: `[('chat_integrations', 2), ('codex', 2), ('gateway', 2), ('packaging_deployment', 2), ('skills_plugins', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'codex', 'gateway', 'packaging_deployment', 'skills_plugins']` exact=False
- repeat 2: `['chat_integrations', 'codex', 'gateway', 'packaging_deployment', 'skills_plugins']` exact=False

### 30. openclaw-openclaw-77827 — stable_wrong

Title: fix: LM Studio thinking blocks invisible with Responses API

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['inference_api', 'self_hosted_inference'], 'count': 2}]`

FP: `[('inference_api', 2), ('self_hosted_inference', 2)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['inference_api', 'self_hosted_inference']` exact=False
- repeat 2: `['inference_api', 'self_hosted_inference']` exact=False
