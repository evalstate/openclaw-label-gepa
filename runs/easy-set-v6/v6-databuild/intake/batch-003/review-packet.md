# V6 batch consensus review

- Batch: `batch-003`
- Rows: 30
- Accepted consensus: 8
- Deferred/review: 22
- GPT/Opus exact modal matches: 9
- Exact modal matches with 5 labels: 2
- Rows where either teacher hit the 5-label cap: 13
- Mean GPT/Opus modal Jaccard: 0.736

## Review rows

### openclaw-openclaw-62428

- Title: test(exec): land exec v2 contract follow-through
- GitHub: https://github.com/openclaw/openclaw/pull/62428
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['approvals', 'config', 'exec_tools', 'security', 'tests_ci']` (2/3)
- GPT label-set votes:
  - `['approvals', 'config', 'exec_tools', 'security', 'tests_ci']`: 2
  - `['approvals', 'config', 'exec_tools', 'security']`: 1
- Opus modal: `['approvals', 'config', 'exec_tools', 'security']` (2/2)
- Opus label-set votes:
  - `['approvals', 'config', 'exec_tools', 'security']`: 2
- Modal Jaccard: 0.800
- Legacy v5: `['exec_tools', 'approvals', 'security', 'tests_ci']`

### openclaw-openclaw-62552

- Title: fix(acp): stabilize bridge session keys
- GitHub: https://github.com/openclaw/openclaw/pull/62552
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'gateway', 'queueing', 'reliability', 'sessions']` (1/3)
- GPT label-set votes:
  - `['acp', 'gateway', 'queueing', 'reliability', 'sessions']`: 1
  - `['acp', 'queueing', 'reliability', 'sessions']`: 1
  - `['acp', 'queueing', 'sessions']`: 1
- Opus modal: `['acp', 'reliability', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acp', 'reliability', 'sessions']`: 2
- Modal Jaccard: 0.600
- Legacy v5: `['acp', 'sessions', 'queueing', 'reliability']`

### openclaw-openclaw-62769

- Title: [Feature]: Support ACP configured bindings for Telegram DMs (not just groups/topics)
- GitHub: https://github.com/openclaw/openclaw/issues/62769
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acp', 'chat_integrations', 'config']` (3/3)
- GPT label-set votes:
  - `['acp', 'chat_integrations', 'config']`: 3
- Opus modal: `['acp', 'chat_integrations']` (2/2)
- Opus label-set votes:
  - `['acp', 'chat_integrations']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['acp', 'chat_integrations', 'sessions']`

### openclaw-openclaw-63007

- Title: Pass outbound session identity into message_sending and surface guarded gateway send denial
- GitHub: https://github.com/openclaw/openclaw/pull/63007
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['gateway', 'hooks', 'notifications', 'sessions', 'skills_plugins']` (3/3)
- GPT label-set votes:
  - `['gateway', 'hooks', 'notifications', 'sessions', 'skills_plugins']`: 3
- Opus modal: `['gateway', 'hooks', 'notifications']` (2/2)
- Opus label-set votes:
  - `['gateway', 'hooks', 'notifications']`: 2
- Modal Jaccard: 0.600
- Legacy v5: `['gateway', 'hooks', 'notifications', 'sessions']`

### openclaw-openclaw-63229

- Title: Bug: Gateway falsely marks healthy local vLLM endpoints as timed out/overloaded, causing 1–23 min fallback cascades
- GitHub: https://github.com/openclaw/openclaw/issues/63229
- Reasons: gpt_unstable, gpt_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['gateway', 'inference_api', 'reliability', 'self_hosted_inference']` (2/3)
- GPT label-set votes:
  - `['gateway', 'inference_api', 'reliability', 'self_hosted_inference']`: 2
  - `['gateway', 'inference_api', 'reliability', 'self_hosted_inference', 'sessions']`: 1
- Opus modal: `['gateway', 'inference_api', 'reliability']` (2/2)
- Opus label-set votes:
  - `['gateway', 'inference_api', 'reliability']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['gateway', 'local_models', 'model_serving', 'reliability']`

### openclaw-openclaw-64199

- Title: [Bug]: ACP configured binding uses parent channel ID for session key — all threads under same channel share one persistent Claude Code process
- GitHub: https://github.com/openclaw/openclaw/issues/64199
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acp', 'acpx', 'chat_integrations', 'security', 'sessions']` (3/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'chat_integrations', 'security', 'sessions']`: 3
- Opus modal: `['acp', 'acpx', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acp', 'acpx', 'sessions']`: 2
- Modal Jaccard: 0.600
- Legacy v5: `['acp', 'acpx', 'sessions', 'chat_integrations', 'security']`

### openclaw-openclaw-65364

- Title: feat(plugins): add registerProviderRuntimeAuthOverride API
- GitHub: https://github.com/openclaw/openclaw/pull/65364
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['api_surface', 'auth_identity', 'inference_api', 'security', 'skills_plugins']` (3/3)
- GPT label-set votes:
  - `['api_surface', 'auth_identity', 'inference_api', 'security', 'skills_plugins']`: 3
- Opus modal: `['auth_identity', 'inference_api', 'security', 'skills_plugins']` (1/2)
- Opus label-set votes:
  - `['auth_identity', 'inference_api', 'security', 'skills_plugins']`: 1
  - `['auth_identity', 'security', 'skills_plugins']`: 1
- Modal Jaccard: 0.800
- Legacy v5: `['api_surface', 'auth_identity', 'security', 'skills_plugins']`

### openclaw-openclaw-66125

- Title: [Bug]: openai-completions fallback candidate is selected, but fallback does not complete successfully through an OpenAI-compatible proxy
- GitHub: https://github.com/openclaw/openclaw/issues/66125
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['inference_api']` (2/3)
- GPT label-set votes:
  - `['inference_api', 'telemetry_usage']`: 1
  - `['inference_api']`: 2
- Opus modal: `['inference_api', 'reliability']` (1/2)
- Opus label-set votes:
  - `['inference_api', 'reliability']`: 1
  - `['inference_api']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `['local_model_providers', 'model_serving', 'reliability']`

### openclaw-openclaw-67244

- Title: Explicit ACP agent runs: embedded backend visibility failure and stale final JSON state after sessions_yield
- GitHub: https://github.com/openclaw/openclaw/issues/67244
- Reasons: gpt_unstable, gpt_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'acpx', 'api_surface', 'coding_agents', 'sessions']` (2/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'agent_runtime', 'coding_agents', 'sessions']`: 1
  - `['acp', 'acpx', 'api_surface', 'coding_agents', 'sessions']`: 2
- Opus modal: `['acp', 'acpx', 'reliability', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acp', 'acpx', 'reliability', 'sessions']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `['acp', 'acpx', 'agent_runtime', 'sessions', 'reliability']`

### openclaw-openclaw-68725

- Title: feat(amazon-bedrock-mantle): add known context windows for open-weight Mantle models
- GitHub: https://github.com/openclaw/openclaw/pull/68725
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['inference_api', 'model_lifecycle']` (3/3)
- GPT label-set votes:
  - `['inference_api', 'model_lifecycle']`: 3
- Opus modal: `['model_lifecycle']` (1/2)
- Opus label-set votes:
  - `['model_lifecycle']`: 1
  - `['inference_api', 'model_lifecycle']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `['open_weight_models', 'config']`

### openclaw-openclaw-69260

- Title: Harden Gemini ACP integration against ambient API-key fallback and add generic auth-contract hooks for ACP agents
- GitHub: https://github.com/openclaw/openclaw/issues/69260
- Reasons: gpt_unstable, opus_unstable, opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'acpx', 'auth_identity', 'coding_agents', 'security']` (1/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'auth_identity', 'coding_agents', 'security']`: 1
  - `['acp', 'auth_identity', 'config', 'hooks', 'security']`: 1
  - `['acp', 'auth_identity', 'coding_agents', 'config', 'security']`: 1
- Opus modal: `['acp', 'auth_identity', 'config', 'security']` (1/2)
- Opus label-set votes:
  - `['acp', 'auth_identity', 'config', 'security']`: 1
  - `['acp', 'auth_identity', 'coding_agents', 'config', 'security']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `['acp', 'auth_identity', 'hooks', 'security']`

### openclaw-openclaw-69328

- Title: fix(acp): avoid false zero-diff failures and append session messages
- GitHub: https://github.com/openclaw/openclaw/pull/69328
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'coding_agents', 'sessions', 'ui_tui']` (3/3)
- GPT label-set votes:
  - `['acp', 'coding_agents', 'sessions', 'ui_tui']`: 3
- Opus modal: `['acp', 'coding_agents', 'ui_tui']` (1/2)
- Opus label-set votes:
  - `['acp', 'coding_agents', 'ui_tui']`: 1
  - `['acp', 'coding_agents', 'sessions', 'ui_tui']`: 1
- Modal Jaccard: 0.750
- Legacy v5: `['acp', 'reliability', 'sessions', 'ui_tui']`

### openclaw-openclaw-71216

- Title: Config schema: add `sandbox`, `routing.rules`, `instances`, and `gateway.nodes.denyPaths`
- GitHub: https://github.com/openclaw/openclaw/issues/71216
- Reasons: opus_flagged_human_review
- GPT modal: `['config', 'gateway', 'inference_api', 'sandboxing', 'security']` (3/3)
- GPT label-set votes:
  - `['config', 'gateway', 'inference_api', 'sandboxing', 'security']`: 3
- Opus modal: `['config', 'gateway', 'inference_api', 'sandboxing', 'security']` (2/2)
- Opus label-set votes:
  - `['config', 'gateway', 'inference_api', 'sandboxing', 'security']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `['config', 'gateway', 'local_model_providers', 'sandboxing', 'security']`

### openclaw-openclaw-71537

- Title: Recover archived (.reset) session transcripts in memory hook + session-logs skill
- GitHub: https://github.com/openclaw/openclaw/pull/71537
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['docs', 'hooks', 'memory', 'sessions', 'skills_plugins']` (3/3)
- GPT label-set votes:
  - `['docs', 'hooks', 'memory', 'sessions', 'skills_plugins']`: 3
- Opus modal: `['memory', 'sessions', 'skills_plugins']` (2/2)
- Opus label-set votes:
  - `['memory', 'sessions', 'skills_plugins']`: 2
- Modal Jaccard: 0.600
- Legacy v5: `['memory', 'sessions', 'skills_plugins']`

### openclaw-openclaw-71594

- Title: docs(gateway): clarify IPv4-only BYOH bind path
- GitHub: https://github.com/openclaw/openclaw/pull/71594
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'docs', 'gateway']` (2/3)
- GPT label-set votes:
  - `['config', 'docs', 'gateway']`: 2
  - `['docs', 'gateway']`: 1
- Opus modal: `['docs', 'gateway']` (2/2)
- Opus label-set votes:
  - `['docs', 'gateway']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['docs', 'gateway']`

### openclaw-openclaw-72001

- Title: fix(hooks): write allowedSessionKeyPrefixes from gmail wizard
- GitHub: https://github.com/openclaw/openclaw/pull/72001
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'hooks', 'security']` (2/3)
- GPT label-set votes:
  - `['config', 'hooks']`: 1
  - `['config', 'hooks', 'security']`: 2
- Opus modal: `['config', 'hooks']` (2/2)
- Opus label-set votes:
  - `['config', 'hooks']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['hooks', 'gateway', 'config']`

### openclaw-openclaw-72015

- Title: Reliability: active-memory blocks replies and QMD boot initialization can overload multi-agent gateways
- GitHub: https://github.com/openclaw/openclaw/issues/72015
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'gateway', 'memory', 'reliability', 'skills_plugins']` (2/3)
- GPT label-set votes:
  - `['config', 'gateway', 'memory', 'reliability']`: 1
  - `['config', 'gateway', 'memory', 'reliability', 'skills_plugins']`: 2
- Opus modal: `['gateway', 'memory', 'reliability', 'skills_plugins']` (1/2)
- Opus label-set votes:
  - `['gateway', 'memory', 'reliability', 'skills_plugins']`: 1
  - `['gateway', 'memory', 'reliability']`: 1
- Modal Jaccard: 0.800
- Legacy v5: `['gateway', 'memory', 'reliability']`

### openclaw-openclaw-72016

- Title: [Feature]: doctor api/extendability
- GitHub: https://github.com/openclaw/openclaw/issues/72016
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['api_surface', 'skills_plugins']` (2/3)
- GPT label-set votes:
  - `['api_surface', 'config', 'skills_plugins']`: 1
  - `['api_surface', 'skills_plugins']`: 2
- Opus modal: `['skills_plugins']` (2/2)
- Opus label-set votes:
  - `['skills_plugins']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `['api_surface', 'config', 'skills_plugins']`

### openclaw-openclaw-72087

- Title: Bug: dist/entry.js main-path breaks Codex OAuth image generation on Linux while direct runCli()/provider path succeeds
- GitHub: https://github.com/openclaw/openclaw/issues/72087
- Reasons: gpt_unstable, opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['auth_identity', 'codex', 'packaging_deployment']` (1/3)
- GPT label-set votes:
  - `['auth_identity', 'codex', 'packaging_deployment']`: 1
  - `['codex', 'inference_api', 'packaging_deployment']`: 1
  - `['auth_identity', 'codex', 'inference_api', 'packaging_deployment']`: 1
- Opus modal: `['codex', 'inference_api', 'packaging_deployment', 'reliability']` (2/2)
- Opus label-set votes:
  - `['codex', 'inference_api', 'packaging_deployment', 'reliability']`: 2
- Modal Jaccard: 0.400
- Legacy v5: `['auth_identity', 'codex', 'packaging_deployment']`

### openclaw-openclaw-74204

- Title: memory.qmd.update.embedTimeoutMs default (120 s) is too low for local GGUF; error message doesn't surface the fix
- GitHub: https://github.com/openclaw/openclaw/issues/74204
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'local_models', 'memory', 'reliability', 'telemetry_usage']` (3/3)
- GPT label-set votes:
  - `['config', 'local_models', 'memory', 'reliability', 'telemetry_usage']`: 3
- Opus modal: `['config', 'local_models', 'memory']` (1/2)
- Opus label-set votes:
  - `['config', 'local_models', 'memory']`: 1
  - `['config', 'local_models', 'memory', 'reliability']`: 1
- Modal Jaccard: 0.600
- Legacy v5: `['config', 'local_models', 'memory', 'reliability']`

### openclaw-openclaw-75657

- Title: fix: local GGUF embedding model warmup blocks Node.js event loop for minutes on startup (ARM64/Pi)
- GitHub: https://github.com/openclaw/openclaw/issues/75657
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['gateway', 'memory', 'reliability', 'self_hosted_inference']` (2/3)
- GPT label-set votes:
  - `['gateway', 'memory', 'reliability', 'self_hosted_inference']`: 2
  - `['gateway', 'local_models', 'memory', 'reliability', 'self_hosted_inference']`: 1
- Opus modal: `['local_models', 'memory', 'reliability', 'self_hosted_inference']` (1/2)
- Opus label-set votes:
  - `['local_models', 'memory', 'reliability', 'self_hosted_inference']`: 1
  - `['memory', 'reliability', 'self_hosted_inference']`: 1
- Modal Jaccard: 0.600
- Legacy v5: `['gateway', 'local_models', 'memory', 'reliability']`

### openclaw-openclaw-77748

- Title: fix: Codex startup plugins + WhatsApp history & Docker Codex OAuth
- GitHub: https://github.com/openclaw/openclaw/pull/77748
- Reasons: gpt_unstable, gpt_flagged_human_review, opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['auth_identity', 'chat_integrations', 'codex', 'packaging_deployment', 'skills_plugins']` (2/3)
- GPT label-set votes:
  - `['chat_integrations', 'codex', 'gateway', 'packaging_deployment', 'skills_plugins']`: 1
  - `['auth_identity', 'chat_integrations', 'codex', 'packaging_deployment', 'skills_plugins']`: 2
- Opus modal: `['auth_identity', 'chat_integrations', 'codex', 'gateway', 'packaging_deployment']` (2/2)
- Opus label-set votes:
  - `['auth_identity', 'chat_integrations', 'codex', 'gateway', 'packaging_deployment']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['auth_identity', 'chat_integrations', 'codex', 'packaging_deployment', 'skills_plugins']`
