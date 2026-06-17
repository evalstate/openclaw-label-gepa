# V6 batch consensus review

- Batch: `batch-003`
- Rows: 30
- Accepted consensus: 6
- Deferred/review: 24
- GPT/Opus exact modal matches: 10
- Exact modal matches with 5 labels: 1
- Rows where either teacher hit the 5-label cap: 9
- Mean GPT/Opus modal Jaccard: 0.746

## Review rows

### openclaw-openclaw-62552

- Title: fix(acp): stabilize bridge session keys
- GitHub: https://github.com/openclaw/openclaw/pull/62552
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'queueing', 'sessions']` (1/3)
- GPT label-set votes:
  - `['acp', 'queueing', 'sessions']`: 1
  - `['acp', 'gateway', 'queueing', 'reliability', 'sessions']`: 1
  - `['acp', 'queueing', 'reliability', 'sessions']`: 1
- Opus modal: `['acp', 'reliability', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acp', 'reliability', 'sessions']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `['acp', 'sessions', 'queueing', 'reliability']`

### openclaw-openclaw-62769

- Title: [Feature]: Support ACP configured bindings for Telegram DMs (not just groups/topics)
- GitHub: https://github.com/openclaw/openclaw/issues/62769
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'chat_integrations', 'sessions']` (1/3)
- GPT label-set votes:
  - `['acp', 'chat_integrations', 'sessions']`: 1
  - `['acp', 'chat_integrations', 'config']`: 1
  - `['acp', 'chat_integrations']`: 1
- Opus modal: `['acp', 'chat_integrations']` (2/2)
- Opus label-set votes:
  - `['acp', 'chat_integrations']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['acp', 'chat_integrations', 'sessions']`

### openclaw-openclaw-63007

- Title: Pass outbound session identity into message_sending and surface guarded gateway send denial
- GitHub: https://github.com/openclaw/openclaw/pull/63007
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['gateway', 'hooks', 'notifications', 'security', 'sessions']` (2/3)
- GPT label-set votes:
  - `['gateway', 'hooks', 'notifications', 'security', 'sessions']`: 2
  - `['gateway', 'hooks', 'notifications', 'sessions', 'skills_plugins']`: 1
- Opus modal: `['gateway', 'hooks', 'notifications']` (2/2)
- Opus label-set votes:
  - `['gateway', 'hooks', 'notifications']`: 2
- Modal Jaccard: 0.600
- Legacy v5: `['gateway', 'hooks', 'notifications', 'sessions']`

### openclaw-openclaw-63229

- Title: Bug: Gateway falsely marks healthy local vLLM endpoints as timed out/overloaded, causing 1–23 min fallback cascades
- GitHub: https://github.com/openclaw/openclaw/issues/63229
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['gateway', 'inference_api', 'reliability']` (2/3)
- GPT label-set votes:
  - `['gateway', 'inference_api', 'reliability']`: 2
  - `['gateway', 'inference_api', 'reliability', 'self_hosted_inference']`: 1
- Opus modal: `['agent_runtime', 'gateway', 'reliability']` (2/2)
- Opus label-set votes:
  - `['agent_runtime', 'gateway', 'reliability']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `['gateway', 'local_models', 'model_serving', 'reliability']`

### openclaw-openclaw-64199

- Title: [Bug]: ACP configured binding uses parent channel ID for session key — all threads under same channel share one persistent Claude Code process
- GitHub: https://github.com/openclaw/openclaw/issues/64199
- Reasons: gpt_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'acpx', 'chat_integrations', 'security', 'sessions']` (3/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'chat_integrations', 'security', 'sessions']`: 3
- Opus modal: `['acp', 'acpx', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acp', 'acpx', 'sessions']`: 2
- Modal Jaccard: 0.600
- Legacy v5: `['acp', 'acpx', 'sessions', 'chat_integrations', 'security']`

### openclaw-openclaw-65187

- Title: test: add regression tests for <final> tag stripping in UI message extraction
- GitHub: https://github.com/openclaw/openclaw/pull/65187
- Reasons: gpt_unstable
- GPT modal: `['tests_ci']` (2/3)
- GPT label-set votes:
  - `['tests_ci']`: 2
  - `['tests_ci', 'ui_tui']`: 1
- Opus modal: `['tests_ci']` (2/2)
- Opus label-set votes:
  - `['tests_ci']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `['tests_ci', 'ui_tui']`

### openclaw-openclaw-65364

- Title: feat(plugins): add registerProviderRuntimeAuthOverride API
- GitHub: https://github.com/openclaw/openclaw/pull/65364
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['api_surface', 'inference_api', 'security', 'skills_plugins']` (3/3)
- GPT label-set votes:
  - `['api_surface', 'inference_api', 'security', 'skills_plugins']`: 3
- Opus modal: `['inference_api', 'security', 'skills_plugins']` (2/2)
- Opus label-set votes:
  - `['inference_api', 'security', 'skills_plugins']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['api_surface', 'auth_identity', 'security', 'skills_plugins']`

### openclaw-openclaw-66125

- Title: [Bug]: openai-completions fallback candidate is selected, but fallback does not complete successfully through an OpenAI-compatible proxy
- GitHub: https://github.com/openclaw/openclaw/issues/66125
- Reasons: gpt_unstable
- GPT modal: `['inference_api']` (2/3)
- GPT label-set votes:
  - `['inference_api', 'telemetry_usage']`: 1
  - `['inference_api']`: 2
- Opus modal: `['inference_api']` (2/2)
- Opus label-set votes:
  - `['inference_api']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `['local_model_providers', 'model_serving', 'reliability']`

### openclaw-openclaw-67244

- Title: Explicit ACP agent runs: embedded backend visibility failure and stale final JSON state after sessions_yield
- GitHub: https://github.com/openclaw/openclaw/issues/67244
- Reasons: gpt_unstable, opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'acpx', 'api_surface', 'sessions']` (2/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'agent_runtime', 'api_surface', 'sessions']`: 1
  - `['acp', 'acpx', 'api_surface', 'sessions']`: 2
- Opus modal: `['acp', 'acpx', 'reliability', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acp', 'acpx', 'reliability', 'sessions']`: 2
- Modal Jaccard: 0.600
- Legacy v5: `['acp', 'acpx', 'agent_runtime', 'sessions', 'reliability']`

### openclaw-openclaw-68725

- Title: feat(amazon-bedrock-mantle): add known context windows for open-weight Mantle models
- GitHub: https://github.com/openclaw/openclaw/pull/68725
- Reasons: opus_unstable
- GPT modal: `['inference_api', 'model_lifecycle']` (3/3)
- GPT label-set votes:
  - `['inference_api', 'model_lifecycle']`: 3
- Opus modal: `['inference_api', 'model_lifecycle']` (1/2)
- Opus label-set votes:
  - `['inference_api', 'model_lifecycle']`: 1
  - `['model_lifecycle']`: 1
- Modal Jaccard: 1.000
- Legacy v5: `['open_weight_models', 'config']`

### openclaw-openclaw-69256

- Title: fix(cron): prevent premature session cleanup when subagents are running
- GitHub: https://github.com/openclaw/openclaw/pull/69256
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['agent_runtime', 'cron_automation', 'reliability', 'sessions']` (2/3)
- GPT label-set votes:
  - `['cron_automation', 'reliability', 'sessions']`: 1
  - `['agent_runtime', 'cron_automation', 'reliability', 'sessions']`: 2
- Opus modal: `['cron_automation', 'reliability', 'sessions']` (2/2)
- Opus label-set votes:
  - `['cron_automation', 'reliability', 'sessions']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['cron_automation', 'sessions', 'agent_runtime', 'queueing', 'reliability']`

### openclaw-openclaw-69260

- Title: Harden Gemini ACP integration against ambient API-key fallback and add generic auth-contract hooks for ACP agents
- GitHub: https://github.com/openclaw/openclaw/issues/69260
- Reasons: gpt_unstable, gpt_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'acpx', 'coding_agent_integrations', 'config', 'security']` (2/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'coding_agent_integrations', 'config', 'security']`: 2
  - `['acp', 'acpx', 'auth_identity', 'coding_agent_integrations', 'security']`: 1
- Opus modal: `['acp', 'auth_identity', 'coding_agent_integrations', 'security']` (2/2)
- Opus label-set votes:
  - `['acp', 'auth_identity', 'coding_agent_integrations', 'security']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `['acp', 'auth_identity', 'hooks', 'security']`

### openclaw-openclaw-69328

- Title: fix(acp): avoid false zero-diff failures and append session messages
- GitHub: https://github.com/openclaw/openclaw/pull/69328
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'sessions', 'ui_tui']` (2/3)
- GPT label-set votes:
  - `['acp', 'sessions', 'ui_tui']`: 2
  - `['acp', 'queueing', 'sessions', 'ui_tui']`: 1
- Opus modal: `['acp', 'ui_tui']` (1/2)
- Opus label-set votes:
  - `['acp', 'ui_tui']`: 1
  - `['acp', 'reliability', 'ui_tui']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `['acp', 'reliability', 'sessions', 'ui_tui']`

### openclaw-openclaw-69669

- Title: ACP: keep thread-bound follow-ups parent-orchestrated by default, not raw pass-through
- GitHub: https://github.com/openclaw/openclaw/issues/69669
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'agent_runtime', 'sessions']` (3/3)
- GPT label-set votes:
  - `['acp', 'agent_runtime', 'sessions']`: 3
- Opus modal: `['acp', 'sessions']` (1/2)
- Opus label-set votes:
  - `['acp', 'sessions']`: 1
  - `['acp', 'agent_runtime', 'sessions']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `['acp', 'coding_agents', 'sessions']`

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

### openclaw-openclaw-72001

- Title: fix(hooks): write allowedSessionKeyPrefixes from gmail wizard
- GitHub: https://github.com/openclaw/openclaw/pull/72001
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['config', 'hooks', 'security']` (3/3)
- GPT label-set votes:
  - `['config', 'hooks', 'security']`: 3
- Opus modal: `['config', 'hooks']` (2/2)
- Opus label-set votes:
  - `['config', 'hooks']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['hooks', 'gateway', 'config']`

### openclaw-openclaw-72015

- Title: Reliability: active-memory blocks replies and QMD boot initialization can overload multi-agent gateways
- GitHub: https://github.com/openclaw/openclaw/issues/72015
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'gateway', 'memory', 'reliability', 'skills_plugins']` (2/3)
- GPT label-set votes:
  - `['gateway', 'memory', 'reliability', 'skills_plugins']`: 1
  - `['config', 'gateway', 'memory', 'reliability', 'skills_plugins']`: 2
- Opus modal: `['gateway', 'memory', 'reliability']` (2/2)
- Opus label-set votes:
  - `['gateway', 'memory', 'reliability']`: 2
- Modal Jaccard: 0.600
- Legacy v5: `['gateway', 'memory', 'reliability']`

### openclaw-openclaw-72016

- Title: [Feature]: doctor api/extendability
- GitHub: https://github.com/openclaw/openclaw/issues/72016
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['api_surface', 'skills_plugins', 'telemetry_usage']` (1/3)
- GPT label-set votes:
  - `['api_surface', 'skills_plugins', 'telemetry_usage']`: 1
  - `['api_surface', 'config', 'skills_plugins']`: 1
  - `['api_surface', 'skills_plugins']`: 1
- Opus modal: `['skills_plugins']` (2/2)
- Opus label-set votes:
  - `['skills_plugins']`: 2
- Modal Jaccard: 0.333
- Legacy v5: `['api_surface', 'config', 'skills_plugins']`

### openclaw-openclaw-72087

- Title: Bug: dist/entry.js main-path breaks Codex OAuth image generation on Linux while direct runCli()/provider path succeeds
- GitHub: https://github.com/openclaw/openclaw/issues/72087
- Reasons: opus_flagged_human_review
- GPT modal: `['codex', 'inference_api', 'packaging_deployment']` (3/3)
- GPT label-set votes:
  - `['codex', 'inference_api', 'packaging_deployment']`: 3
- Opus modal: `['codex', 'inference_api', 'packaging_deployment']` (2/2)
- Opus label-set votes:
  - `['codex', 'inference_api', 'packaging_deployment']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `['auth_identity', 'codex', 'packaging_deployment']`

### openclaw-openclaw-73910

- Title: BUG: OpenClaw-managed Codex ACP uses isolated CODEX_HOME without auth bridge and sends unsupported timeout config
- GitHub: https://github.com/openclaw/openclaw/issues/73910
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acp', 'acpx', 'codex', 'coding_agent_integrations', 'security']` (3/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'codex', 'coding_agent_integrations', 'security']`: 3
- Opus modal: `['acp', 'acpx', 'codex', 'security']` (2/2)
- Opus label-set votes:
  - `['acp', 'acpx', 'codex', 'security']`: 2
- Modal Jaccard: 0.800
- Legacy v5: `['acp', 'acpx', 'auth_identity', 'codex', 'config']`

### openclaw-openclaw-74204

- Title: memory.qmd.update.embedTimeoutMs default (120 s) is too low for local GGUF; error message doesn't surface the fix
- GitHub: https://github.com/openclaw/openclaw/issues/74204
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'local_models', 'memory', 'reliability', 'telemetry_usage']` (2/3)
- GPT label-set votes:
  - `['config', 'local_models', 'memory', 'reliability', 'telemetry_usage']`: 2
  - `['config', 'local_models', 'memory', 'reliability']`: 1
- Opus modal: `['config', 'local_models', 'memory', 'reliability']` (1/2)
- Opus label-set votes:
  - `['config', 'local_models', 'memory', 'reliability']`: 1
  - `['config', 'local_models', 'memory']`: 1
- Modal Jaccard: 0.800
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
- GPT modal: `['chat_integrations', 'codex', 'packaging_deployment', 'security', 'skills_plugins']` (1/3)
- GPT label-set votes:
  - `['chat_integrations', 'codex', 'packaging_deployment', 'security', 'skills_plugins']`: 1
  - `['chat_integrations', 'codex', 'gateway', 'packaging_deployment', 'skills_plugins']`: 1
  - `['chat_integrations', 'codex', 'coding_agent_integrations', 'packaging_deployment', 'skills_plugins']`: 1
- Opus modal: `['chat_integrations', 'codex', 'gateway', 'packaging_deployment', 'skills_plugins']` (2/2)
- Opus label-set votes:
  - `['chat_integrations', 'codex', 'gateway', 'packaging_deployment', 'skills_plugins']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['auth_identity', 'chat_integrations', 'codex', 'packaging_deployment', 'skills_plugins']`

### openclaw-openclaw-77827

- Title: fix: LM Studio thinking blocks invisible with Responses API
- GitHub: https://github.com/openclaw/openclaw/pull/77827
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['inference_api']` (2/3)
- GPT label-set votes:
  - `['inference_api']`: 2
  - `['inference_api', 'self_hosted_inference']`: 1
- Opus modal: `['inference_api', 'self_hosted_inference']` (2/2)
- Opus label-set votes:
  - `['inference_api', 'self_hosted_inference']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `['model_serving', 'api_surface', 'local_model_providers']`
