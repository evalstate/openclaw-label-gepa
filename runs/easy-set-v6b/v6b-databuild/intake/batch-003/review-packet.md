# V6 batch consensus review

- Batch: `batch-003`
- Rows: 200
- Accepted consensus: 46
- Deferred/review: 154
- GPT/Opus exact modal matches: 66
- Exact modal matches with 5 labels: 0
- Rows where either teacher hit the 5-label cap: 24
- Mean GPT/Opus modal Jaccard: 0.734

## Review rows

### openclaw-openclaw-80479

- Title: feat(memory/embeddings): add openai-compatible provider for self-hosted servers (llama.cpp, Ollama, vLLM, TGI, LocalAI)
- GitHub: https://github.com/openclaw/openclaw/pull/80479
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['inference_api', 'memory', 'self_hosted_inference', 'skills_plugins']` (2/3)
- GPT label-set votes:
  - `['inference_api', 'memory', 'self_hosted_inference', 'skills_plugins']`: 2
  - `['inference_api', 'memory', 'self_hosted_inference']`: 1
- Opus modal: `['memory', 'self_hosted_inference', 'skills_plugins']` (1/2)
- Opus label-set votes:
  - `['memory', 'self_hosted_inference', 'skills_plugins']`: 1
  - `['memory', 'self_hosted_inference']`: 1
- Modal Jaccard: 0.750
- Legacy v5: `['local_model_providers', 'memory', 'self_hosted_inference']`

### openclaw-openclaw-63229

- Title: Bug: Gateway falsely marks healthy local vLLM endpoints as timed out/overloaded, causing 1–23 min fallback cascades
- GitHub: https://github.com/openclaw/openclaw/issues/63229
- Reasons: opus_unstable, opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['gateway', 'inference_api', 'reliability', 'self_hosted_inference']` (3/3)
- GPT label-set votes:
  - `['gateway', 'inference_api', 'reliability', 'self_hosted_inference']`: 3
- Opus modal: `['gateway', 'reliability', 'self_hosted_inference']` (1/2)
- Opus label-set votes:
  - `['gateway', 'reliability', 'self_hosted_inference']`: 1
  - `['agent_runtime', 'gateway', 'reliability', 'self_hosted_inference']`: 1
- Modal Jaccard: 0.750
- Legacy v5: `['gateway', 'local_models', 'model_serving', 'reliability']`

### openclaw-openclaw-83333

- Title: [Bug]: Memory provider cutover to Ollama leaves production index in mixed OpenAI/Ollama vector state after live sync/reload
- GitHub: https://github.com/openclaw/openclaw/issues/83333
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['memory', 'reliability', 'self_hosted_inference']` (1/3)
- GPT label-set votes:
  - `['memory', 'reliability', 'self_hosted_inference']`: 1
  - `['memory', 'reliability']`: 1
  - `['memory']`: 1
- Opus modal: `['memory', 'reliability']` (1/2)
- Opus label-set votes:
  - `['memory', 'reliability']`: 1
  - `['memory', 'reliability', 'self_hosted_inference']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `['memory', 'self_hosted_inference', 'reliability']`

### openclaw-openclaw-70790

- Title: fix(agents): strip empty tools/tool_choice from embedded runner payloads
- GitHub: https://github.com/openclaw/openclaw/pull/70790
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['agent_runtime', 'inference_api', 'tool_calling']` (3/3)
- GPT label-set votes:
  - `['agent_runtime', 'inference_api', 'tool_calling']`: 3
- Opus modal: `['inference_api', 'tool_calling']` (2/2)
- Opus label-set votes:
  - `['inference_api', 'tool_calling']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-82880

- Title: security: harden ACPX proxy and Firecrawl SSRF protection
- GitHub: https://github.com/openclaw/openclaw/pull/82880
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acpx', 'config', 'exec_tools', 'security']` (3/3)
- GPT label-set votes:
  - `['acpx', 'config', 'exec_tools', 'security']`: 3
- Opus modal: `['acpx', 'security']` (2/2)
- Opus label-set votes:
  - `['acpx', 'security']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-46740

- Title: ACP: classify silent acpx exits as backend unavailable
- GitHub: https://github.com/openclaw/openclaw/pull/46740
- Reasons: gpt_unstable
- GPT modal: `['acp', 'acpx', 'reliability']` (2/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'reliability']`: 2
  - `['acpx', 'reliability']`: 1
- Opus modal: `['acp', 'acpx', 'reliability']` (2/2)
- Opus label-set votes:
  - `['acp', 'acpx', 'reliability']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `['acp', 'acpx', 'reliability']`

### openclaw-openclaw-74339

- Title: fix(acpx): prevent duplicate -c config overrides for Codex ACP command
- GitHub: https://github.com/openclaw/openclaw/pull/74339
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acpx', 'codex', 'coding_agent_integrations']` (3/3)
- GPT label-set votes:
  - `['acpx', 'codex', 'coding_agent_integrations']`: 3
- Opus modal: `['acpx', 'codex']` (2/2)
- Opus label-set votes:
  - `['acpx', 'codex']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-78936

- Title: fix #78919: [Bug] ACP sessions_spawn doesn't route images to Codex's native vision like acpx codex exec does
- GitHub: https://github.com/openclaw/openclaw/pull/78936
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'codex', 'coding_agent_integrations', 'security']` (2/3)
- GPT label-set votes:
  - `['acp', 'codex', 'coding_agent_integrations', 'security']`: 2
  - `['acp', 'agent_runtime', 'codex', 'coding_agent_integrations', 'security']`: 1
- Opus modal: `['acp', 'codex', 'coding_agent_integrations']` (1/2)
- Opus label-set votes:
  - `['acp', 'codex', 'coding_agent_integrations']`: 1
  - `['acp', 'codex']`: 1
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-43348

- Title: feat(acp): add acp_send tool and sessions_cancel tool
- GitHub: https://github.com/openclaw/openclaw/pull/43348
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acp', 'gateway', 'security', 'sessions', 'tool_calling']` (3/3)
- GPT label-set votes:
  - `['acp', 'gateway', 'security', 'sessions', 'tool_calling']`: 3
- Opus modal: `['acp', 'gateway', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acp', 'gateway', 'sessions']`: 2
- Modal Jaccard: 0.600
- Legacy v5: `[]`

### openclaw-openclaw-84443

- Title: [Feature]: Add ACP support for Antigravity CLI (agy)
- GitHub: https://github.com/openclaw/openclaw/issues/84443
- Reasons: gpt_unstable
- GPT modal: `['acp', 'coding_agent_integrations']` (2/3)
- GPT label-set votes:
  - `['acp', 'coding_agent_integrations', 'sessions']`: 1
  - `['acp', 'coding_agent_integrations']`: 2
- Opus modal: `['acp', 'coding_agent_integrations']` (2/2)
- Opus label-set votes:
  - `['acp', 'coding_agent_integrations']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-84381

- Title: fix(agent): abort accepted gateway runs on signal
- GitHub: https://github.com/openclaw/openclaw/pull/84381
- Reasons: gpt_unstable
- GPT modal: `['gateway', 'reliability', 'security']` (2/3)
- GPT label-set votes:
  - `['api_surface', 'gateway', 'reliability', 'security']`: 1
  - `['gateway', 'reliability', 'security']`: 2
- Opus modal: `['gateway', 'reliability', 'security']` (2/2)
- Opus label-set votes:
  - `['gateway', 'reliability', 'security']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-48433

- Title: feat(exec): per-host allowlists via tools.exec.allowedHosts
- GitHub: https://github.com/openclaw/openclaw/pull/48433
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'exec_tools', 'sandboxing', 'security']` (3/3)
- GPT label-set votes:
  - `['config', 'exec_tools', 'sandboxing', 'security']`: 3
- Opus modal: `['approvals', 'config', 'exec_tools', 'security']` (1/2)
- Opus label-set votes:
  - `['approvals', 'config', 'exec_tools', 'security']`: 1
  - `['config', 'exec_tools', 'security']`: 1
- Modal Jaccard: 0.600
- Legacy v5: `[]`

### openclaw-openclaw-84570

- Title: Remove skill prelude exec allowlist
- GitHub: https://github.com/openclaw/openclaw/pull/84570
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['approvals', 'exec_tools', 'security', 'skills_plugins']` (2/3)
- GPT label-set votes:
  - `['approvals', 'exec_tools', 'security', 'skills_plugins']`: 2
  - `['approvals', 'config', 'exec_tools', 'security', 'skills_plugins']`: 1
- Opus modal: `['approvals', 'exec_tools', 'skills_plugins']` (2/2)
- Opus label-set votes:
  - `['approvals', 'exec_tools', 'skills_plugins']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['approvals', 'exec_tools', 'skills_plugins']`

### openclaw-openclaw-71856

- Title: feat(tui): fetch startup conversation summary dynamically from Gateway API
- GitHub: https://github.com/openclaw/openclaw/pull/71856
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['ui_tui']` (2/3)
- GPT label-set votes:
  - `['ui_tui']`: 2
  - `['sessions', 'ui_tui']`: 1
- Opus modal: `['sessions', 'ui_tui']` (2/2)
- Opus label-set votes:
  - `['sessions', 'ui_tui']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-83552

- Title: fix(harness): route CLI runtime aliases (claude-cli, google-gemini-cli) through PI harness
- GitHub: https://github.com/openclaw/openclaw/pull/83552
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['coding_agent_integrations', 'reliability']` (2/3)
- GPT label-set votes:
  - `['coding_agent_integrations', 'reliability']`: 2
  - `['agent_runtime', 'coding_agent_integrations', 'reliability']`: 1
- Opus modal: `['agent_runtime', 'coding_agent_integrations', 'reliability']` (2/2)
- Opus label-set votes:
  - `['agent_runtime', 'coding_agent_integrations', 'reliability']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-55888

- Title: [Feature]: 🚀 [Performance Insight] Unlocking 26.7k Context Window on M4 Pro: Fixing the 8k Compaction Lag (64GB RAM Only)
- GitHub: https://github.com/openclaw/openclaw/issues/55888
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['config', 'docs', 'self_hosted_inference', 'sessions']` (3/3)
- GPT label-set votes:
  - `['config', 'docs', 'self_hosted_inference', 'sessions']`: 3
- Opus modal: `['config', 'self_hosted_inference']` (2/2)
- Opus label-set votes:
  - `['config', 'self_hosted_inference']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `['config', 'local_models', 'memory']`

### openclaw-openclaw-52029

- Title: Feature Request: heartbeat.tools option to disable tools during heartbeat
- GitHub: https://github.com/openclaw/openclaw/issues/52029
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'cron_automation', 'security', 'tool_calling']` (2/3)
- GPT label-set votes:
  - `['config', 'cron_automation', 'security', 'tool_calling']`: 2
  - `['config', 'cron_automation', 'reliability', 'security', 'tool_calling']`: 1
- Opus modal: `['config', 'cron_automation', 'security']` (2/2)
- Opus label-set votes:
  - `['config', 'cron_automation', 'security']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-65180

- Title: fix(cli,sessions): make local model run stateless by default and keep transcript fallback profile-scoped
- GitHub: https://github.com/openclaw/openclaw/pull/65180
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['api_surface', 'self_hosted_inference', 'sessions']` (2/3)
- GPT label-set votes:
  - `['api_surface', 'self_hosted_inference', 'sessions']`: 2
  - `['api_surface', 'docs', 'self_hosted_inference', 'sessions']`: 1
- Opus modal: `['self_hosted_inference', 'sessions']` (2/2)
- Opus label-set votes:
  - `['self_hosted_inference', 'sessions']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-41737

- Title: vLLM: add endpoint lifecycle management, multi-endpoint selection, and stale default cleanup
- GitHub: https://github.com/openclaw/openclaw/pull/41737
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'model_lifecycle', 'self_hosted_inference']` (2/3)
- GPT label-set votes:
  - `['config', 'inference_api', 'model_lifecycle', 'self_hosted_inference']`: 1
  - `['config', 'model_lifecycle', 'self_hosted_inference']`: 2
- Opus modal: `['auth_identity', 'config', 'self_hosted_inference']` (1/2)
- Opus label-set votes:
  - `['auth_identity', 'config', 'self_hosted_inference']`: 1
  - `['auth_identity', 'config', 'model_lifecycle', 'self_hosted_inference']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-84301

- Title: [Bug]: Make Dream Diary narrative timeout configurable for slow/serial local model backends
- GitHub: https://github.com/openclaw/openclaw/issues/84301
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['config', 'memory', 'queueing', 'reliability', 'self_hosted_inference']` (3/3)
- GPT label-set votes:
  - `['config', 'memory', 'queueing', 'reliability', 'self_hosted_inference']`: 3
- Opus modal: `['config', 'memory', 'reliability']` (2/2)
- Opus label-set votes:
  - `['config', 'memory', 'reliability']`: 2
- Modal Jaccard: 0.600
- Legacy v5: `['config', 'local_models', 'queueing', 'reliability']`

### openclaw-openclaw-80495

- Title: [Bug]: LM Studio Provider Fails: Environment Variable Expansion + API Endpoint Mismatch
- GitHub: https://github.com/openclaw/openclaw/issues/80495
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'inference_api', 'self_hosted_inference']` (3/3)
- GPT label-set votes:
  - `['config', 'inference_api', 'self_hosted_inference']`: 3
- Opus modal: `['self_hosted_inference']` (1/2)
- Opus label-set votes:
  - `['self_hosted_inference']`: 1
  - `['inference_api', 'self_hosted_inference']`: 1
- Modal Jaccard: 0.333
- Legacy v5: `[]`

### openclaw-openclaw-77992

- Title: [Bug] Context display shows ?/131k with llama.cpp after upgrading to 2026.5.4 — field name mismatch not resolved
- GitHub: https://github.com/openclaw/openclaw/issues/77992
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['inference_api', 'self_hosted_inference', 'telemetry_usage']` (3/3)
- GPT label-set votes:
  - `['inference_api', 'self_hosted_inference', 'telemetry_usage']`: 3
- Opus modal: `['inference_api', 'telemetry_usage']` (1/2)
- Opus label-set votes:
  - `['inference_api', 'telemetry_usage']`: 1
  - `['inference_api', 'self_hosted_inference', 'telemetry_usage']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `['local_models', 'local_model_providers', 'model_serving', 'telemetry_usage']`

### openclaw-openclaw-78085

- Title: fix(agents): parse prompt_tokens/completion_tokens in CLI usage for llama.cpp compatibility (#77992)
- GitHub: https://github.com/openclaw/openclaw/pull/78085
- Reasons: gpt_unstable
- GPT modal: `['self_hosted_inference', 'telemetry_usage']` (2/3)
- GPT label-set votes:
  - `['self_hosted_inference', 'telemetry_usage']`: 2
  - `['inference_api', 'self_hosted_inference', 'telemetry_usage']`: 1
- Opus modal: `['self_hosted_inference', 'telemetry_usage']` (2/2)
- Opus label-set votes:
  - `['self_hosted_inference', 'telemetry_usage']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-77827

- Title: fix: LM Studio thinking blocks invisible with Responses API
- GitHub: https://github.com/openclaw/openclaw/pull/77827
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['inference_api']` (2/3)
- GPT label-set votes:
  - `['inference_api', 'self_hosted_inference']`: 1
  - `['inference_api']`: 2
- Opus modal: `['inference_api', 'self_hosted_inference']` (2/2)
- Opus label-set votes:
  - `['inference_api', 'self_hosted_inference']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `['model_serving', 'api_surface', 'local_model_providers']`

### openclaw-openclaw-75274

- Title: fix(ollama): per-request URL routing for multi-provider setups
- GitHub: https://github.com/openclaw/openclaw/pull/75274
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['inference_api', 'security', 'self_hosted_inference']` (2/3)
- GPT label-set votes:
  - `['security', 'self_hosted_inference']`: 1
  - `['inference_api', 'security', 'self_hosted_inference']`: 2
- Opus modal: `['security', 'self_hosted_inference']` (2/2)
- Opus label-set votes:
  - `['security', 'self_hosted_inference']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-80476

- Title: [Feature]: bundled openai-compatible embedding provider for self-hosted servers (llama.cpp, Ollama, vLLM, TGI, LocalAI)
- GitHub: https://github.com/openclaw/openclaw/issues/80476
- Reasons: gpt_unstable, gpt_flagged_human_review, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'inference_api', 'memory', 'security', 'self_hosted_inference']` (2/3)
- GPT label-set votes:
  - `['config', 'inference_api', 'memory', 'self_hosted_inference']`: 1
  - `['config', 'inference_api', 'memory', 'security', 'self_hosted_inference']`: 2
- Opus modal: `['config', 'memory', 'self_hosted_inference', 'skills_plugins']` (1/2)
- Opus label-set votes:
  - `['config', 'memory', 'self_hosted_inference', 'skills_plugins']`: 1
  - `['memory', 'self_hosted_inference', 'skills_plugins']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-44086

- Title: fix(agents): assistant message content null instead of empty string breaks OpenAI-compatible providers
- GitHub: https://github.com/openclaw/openclaw/pull/44086
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['inference_api', 'tool_calling']` (2/3)
- GPT label-set votes:
  - `['coding_agent_integrations', 'inference_api', 'tool_calling']`: 1
  - `['inference_api', 'tool_calling']`: 2
- Opus modal: `['inference_api']` (1/2)
- Opus label-set votes:
  - `['inference_api']`: 1
  - `['inference_api', 'tool_calling']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-84587

- Title: [Feature]: GPT4Free (g4f) OpenAI-Compatible Backend + Fallback & Proxy Support
- GitHub: https://github.com/openclaw/openclaw/issues/84587
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['config', 'inference_api', 'reliability']` (3/3)
- GPT label-set votes:
  - `['config', 'inference_api', 'reliability']`: 3
- Opus modal: `['inference_api', 'reliability']` (2/2)
- Opus label-set votes:
  - `['inference_api', 'reliability']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-51462

- Title: fix: emit assistant update for tool-call-only messages from OpenAI-compatible providers [AI-assisted]
- GitHub: https://github.com/openclaw/openclaw/pull/51462
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['inference_api', 'notifications', 'tool_calling']` (2/3)
- GPT label-set votes:
  - `['inference_api', 'notifications', 'tool_calling']`: 2
  - `['inference_api', 'reliability', 'tool_calling']`: 1
- Opus modal: `['agent_runtime', 'tool_calling']` (1/2)
- Opus label-set votes:
  - `['agent_runtime', 'tool_calling']`: 1
  - `['reliability', 'tool_calling']`: 1
- Modal Jaccard: 0.250
- Legacy v5: `[]`

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

### openclaw-openclaw-61716

- Title: [Feature]: Add model parameter prompts (context window, max_tokens, modalities) during OpenAI-compatible provider onboarding CLI flow
- GitHub: https://github.com/openclaw/openclaw/issues/61716
- Reasons: gpt_unstable
- GPT modal: `['config', 'inference_api', 'model_lifecycle']` (2/3)
- GPT label-set votes:
  - `['config', 'inference_api', 'model_lifecycle']`: 2
  - `['api_surface', 'config', 'inference_api', 'model_lifecycle']`: 1
- Opus modal: `['config', 'inference_api', 'model_lifecycle']` (2/2)
- Opus label-set votes:
  - `['config', 'inference_api', 'model_lifecycle']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-32496

- Title: [Feature]:  Support frequency_penalty and presence_penalty Parameters for OpenAI-Compatible Providers
- GitHub: https://github.com/openclaw/openclaw/issues/32496
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['api_surface', 'inference_api']` (3/3)
- GPT label-set votes:
  - `['api_surface', 'inference_api']`: 3
- Opus modal: `['inference_api']` (2/2)
- Opus label-set votes:
  - `['inference_api']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-84763

- Title: fix(acpx): scrub provider credential env from ACP harness spawns
- GitHub: https://github.com/openclaw/openclaw/pull/84763
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acpx', 'coding_agent_integrations', 'config', 'security']` (2/3)
- GPT label-set votes:
  - `['acpx', 'codex', 'coding_agent_integrations', 'config', 'security']`: 1
  - `['acpx', 'coding_agent_integrations', 'config', 'security']`: 2
- Opus modal: `['acpx', 'config', 'security']` (2/2)
- Opus label-set votes:
  - `['acpx', 'config', 'security']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['acpx', 'acp', 'auth_identity', 'security', 'config']`

### openclaw-openclaw-66465

- Title: [Feature]: persist ACPX subprocess stderr to disk for post-mortem debugging
- GitHub: https://github.com/openclaw/openclaw/issues/66465
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acpx', 'config', 'security', 'telemetry_usage']` (3/3)
- GPT label-set votes:
  - `['acpx', 'config', 'security', 'telemetry_usage']`: 3
- Opus modal: `['acpx', 'config', 'security']` (2/2)
- Opus label-set votes:
  - `['acpx', 'config', 'security']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-59532

- Title: Feature Request: Per-agent default model and reasoning_effort in ACPX plugin config
- GitHub: https://github.com/openclaw/openclaw/issues/59532
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'acpx', 'config', 'skills_plugins']` (1/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'config', 'skills_plugins']`: 1
  - `['acp', 'acpx', 'coding_agent_integrations', 'config']`: 1
  - `['acp', 'acpx', 'config']`: 1
- Opus modal: `['acpx', 'config', 'skills_plugins']` (1/2)
- Opus label-set votes:
  - `['acpx', 'config', 'skills_plugins']`: 1
  - `['acpx', 'config']`: 1
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-82507

- Title: [Feature]: ACPX Codex sandbox should inherit user-installed plugins (e.g. Superpowers)
- GitHub: https://github.com/openclaw/openclaw/issues/82507
- Reasons: gpt_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['acpx', 'codex', 'sandboxing', 'security', 'skills_plugins']` (3/3)
- GPT label-set votes:
  - `['acpx', 'codex', 'sandboxing', 'security', 'skills_plugins']`: 3
- Opus modal: `['acpx', 'codex', 'config', 'security', 'skills_plugins']` (2/2)
- Opus label-set votes:
  - `['acpx', 'codex', 'config', 'security', 'skills_plugins']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['acpx', 'codex', 'sandboxing', 'skills_plugins']`

### openclaw-openclaw-81200

- Title: fix(acpx): strip provider API keys from child harness env
- GitHub: https://github.com/openclaw/openclaw/pull/81200
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acpx', 'coding_agent_integrations', 'config', 'security']` (3/3)
- GPT label-set votes:
  - `['acpx', 'coding_agent_integrations', 'config', 'security']`: 3
- Opus modal: `['acpx', 'security']` (2/2)
- Opus label-set votes:
  - `['acpx', 'security']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `['acpx', 'acp', 'security', 'auth_identity']`

### openclaw-openclaw-79625

- Title: [Bug]: Decouple sidecar startup from ACPX — Discord/heartbeat/cron should start in parallel, not after ACPX ready
- GitHub: https://github.com/openclaw/openclaw/issues/79625
- Reasons: gpt_unstable
- GPT modal: `['acpx', 'chat_integrations', 'cron_automation', 'gateway']` (2/3)
- GPT label-set votes:
  - `['acpx', 'chat_integrations', 'cron_automation', 'gateway']`: 2
  - `['acpx', 'chat_integrations', 'cron_automation', 'gateway', 'skills_plugins']`: 1
- Opus modal: `['acpx', 'chat_integrations', 'cron_automation', 'gateway']` (2/2)
- Opus label-set votes:
  - `['acpx', 'chat_integrations', 'cron_automation', 'gateway']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-82432

- Title: test(acpx): cover built MCP server config
- GitHub: https://github.com/openclaw/openclaw/pull/82432
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acpx', 'mcp_tooling', 'tests_ci']` (3/3)
- GPT label-set votes:
  - `['acpx', 'mcp_tooling', 'tests_ci']`: 3
- Opus modal: `['acpx', 'tests_ci']` (2/2)
- Opus label-set votes:
  - `['acpx', 'tests_ci']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-77006

- Title: fix(acpx): allow explicit Codex home override
- GitHub: https://github.com/openclaw/openclaw/pull/77006
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acpx', 'codex', 'coding_agent_integrations', 'config', 'skills_plugins']` (3/3)
- GPT label-set votes:
  - `['acpx', 'codex', 'coding_agent_integrations', 'config', 'skills_plugins']`: 3
- Opus modal: `['acpx', 'codex', 'config']` (2/2)
- Opus label-set votes:
  - `['acpx', 'codex', 'config']`: 2
- Modal Jaccard: 0.600
- Legacy v5: `[]`

### openclaw-openclaw-74305

- Title: [Bug]: ACPX Codex worker fails when model/thinking overrides are configured
- GitHub: https://github.com/openclaw/openclaw/issues/74305
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'acpx', 'codex', 'coding_agent_integrations']` (3/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'codex', 'coding_agent_integrations']`: 3
- Opus modal: `['acpx', 'codex']` (1/2)
- Opus label-set votes:
  - `['acpx', 'codex']`: 1
  - `['acp', 'acpx', 'codex']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `['acpx', 'acp', 'codex', 'reliability']`

### openclaw-openclaw-81482

- Title: fix(acpx): keep oneshot client alive for initial turn
- GitHub: https://github.com/openclaw/openclaw/pull/81482
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'acpx']` (3/3)
- GPT label-set votes:
  - `['acp', 'acpx']`: 3
- Opus modal: `['acp', 'acpx', 'sessions']` (1/2)
- Opus label-set votes:
  - `['acp', 'acpx', 'sessions']`: 1
  - `['acp', 'acpx']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-44049

- Title: [AI-assisted] Fix duplicated acp server args in ACP client
- GitHub: https://github.com/openclaw/openclaw/pull/44049
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'api_surface', 'exec_tools']` (2/3)
- GPT label-set votes:
  - `['acp', 'api_surface', 'exec_tools']`: 2
  - `['acp']`: 1
- Opus modal: `['acp']` (2/2)
- Opus label-set votes:
  - `['acp']`: 2
- Modal Jaccard: 0.333
- Legacy v5: `[]`

### openclaw-openclaw-46949

- Title: fix(acp): release dormant oneshot runtimes under pressure
- GitHub: https://github.com/openclaw/openclaw/pull/46949
- Reasons: opus_unstable
- GPT modal: `['acp', 'reliability', 'sessions']` (3/3)
- GPT label-set votes:
  - `['acp', 'reliability', 'sessions']`: 3
- Opus modal: `['acp', 'reliability', 'sessions']` (1/2)
- Opus label-set votes:
  - `['acp', 'reliability', 'sessions']`: 1
  - `['acp', 'reliability']`: 1
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-48940

- Title: ACP: add gateway-owned node-backed runtime
- GitHub: https://github.com/openclaw/openclaw/pull/48940
- Reasons: opus_unstable, opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'gateway', 'notifications', 'reliability', 'security']` (3/3)
- GPT label-set votes:
  - `['acp', 'gateway', 'notifications', 'reliability', 'security']`: 3
- Opus modal: `['acp', 'gateway', 'reliability', 'security', 'sessions']` (1/2)
- Opus label-set votes:
  - `['acp', 'gateway', 'reliability', 'security', 'sessions']`: 1
  - `['acp', 'gateway', 'reliability', 'sessions']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `['acp', 'gateway', 'agent_runtime', 'sessions', 'reliability']`

### openclaw-openclaw-84509

- Title: fix(acp): preserve pre-tool text in final_only delivery mode
- GitHub: https://github.com/openclaw/openclaw/pull/84509
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'notifications']` (2/3)
- GPT label-set votes:
  - `['acp', 'notifications']`: 2
  - `['acp']`: 1
- Opus modal: `['acp']` (1/2)
- Opus label-set votes:
  - `['acp']`: 1
  - `['acp', 'notifications']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-64616

- Title: Tasks: mark stale ACP zombie sessions lost during maintenance
- GitHub: https://github.com/openclaw/openclaw/pull/64616
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acp', 'queueing', 'reliability', 'sessions']` (3/3)
- GPT label-set votes:
  - `['acp', 'queueing', 'reliability', 'sessions']`: 3
- Opus modal: `['acp', 'reliability', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acp', 'reliability', 'sessions']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-63793

- Title: fix(acp): fail fast on dead spawns and recover stale disconnects
- GitHub: https://github.com/openclaw/openclaw/pull/63793
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'reliability', 'sessions']` (2/3)
- GPT label-set votes:
  - `['acp', 'reliability']`: 1
  - `['acp', 'reliability', 'sessions']`: 2
- Opus modal: `['acp', 'reliability']` (2/2)
- Opus label-set votes:
  - `['acp', 'reliability']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-64416

- Title: fix(acp): normalize completion delivery guidance
- GitHub: https://github.com/openclaw/openclaw/pull/64416
- Reasons: gpt_unstable, gpt_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'agent_runtime', 'notifications', 'security']` (2/3)
- GPT label-set votes:
  - `['acp', 'notifications', 'security']`: 1
  - `['acp', 'agent_runtime', 'notifications', 'security']`: 2
- Opus modal: `['acp', 'agent_runtime', 'notifications']` (2/2)
- Opus label-set votes:
  - `['acp', 'agent_runtime', 'notifications']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-64322

- Title: fix(acp): assign distinct session keys to Discord threads under the same parent channel
- GitHub: https://github.com/openclaw/openclaw/pull/64322
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'chat_integrations', 'sessions']` (3/3)
- GPT label-set votes:
  - `['acp', 'chat_integrations', 'sessions']`: 3
- Opus modal: `['acp', 'chat_integrations']` (1/2)
- Opus label-set votes:
  - `['acp', 'chat_integrations']`: 1
  - `['acp', 'chat_integrations', 'sessions']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-62552

- Title: fix(acp): stabilize bridge session keys
- GitHub: https://github.com/openclaw/openclaw/pull/62552
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'queueing', 'reliability', 'sessions']` (2/3)
- GPT label-set votes:
  - `['acp', 'queueing', 'reliability', 'sessions']`: 2
  - `['acp', 'queueing', 'sessions']`: 1
- Opus modal: `['acp', 'queueing', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acp', 'queueing', 'sessions']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['acp', 'sessions', 'queueing', 'reliability']`

### openclaw-openclaw-45739

- Title: ACP: recover parent relay output from gateway state
- GitHub: https://github.com/openclaw/openclaw/pull/45739
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'gateway', 'reliability', 'sessions']` (1/3)
- GPT label-set votes:
  - `['acp', 'gateway', 'reliability', 'sessions']`: 1
  - `['acp', 'reliability']`: 1
  - `['acp', 'reliability', 'sessions']`: 1
- Opus modal: `['acp', 'reliability']` (2/2)
- Opus label-set votes:
  - `['acp', 'reliability']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-69260

- Title: Harden Gemini ACP integration against ambient API-key fallback and add generic auth-contract hooks for ACP agents
- GitHub: https://github.com/openclaw/openclaw/issues/69260
- Reasons: gpt_unstable, gpt_flagged_human_review, opus_unstable, opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['acpx', 'coding_agent_integrations', 'config', 'security']` (2/3)
- GPT label-set votes:
  - `['acpx', 'coding_agent_integrations', 'config', 'security']`: 2
  - `['acpx', 'coding_agent_integrations', 'config', 'hooks', 'security']`: 1
- Opus modal: `['acp', 'acpx', 'auth_identity', 'coding_agent_integrations', 'security']` (1/2)
- Opus label-set votes:
  - `['acp', 'acpx', 'auth_identity', 'coding_agent_integrations', 'security']`: 1
  - `['acpx', 'coding_agent_integrations', 'config', 'security']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `['acp', 'auth_identity', 'hooks', 'security']`

### openclaw-openclaw-70306

- Title: fix(acp+gateway): clean final emit, fallback visibility, legacy unit resolve
- GitHub: https://github.com/openclaw/openclaw/pull/70306
- Reasons: gpt_unstable, opus_unstable, opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'codex', 'coding_agent_integrations', 'gateway', 'telemetry_usage']` (1/3)
- GPT label-set votes:
  - `['acp', 'codex', 'coding_agent_integrations', 'gateway', 'telemetry_usage']`: 1
  - `['acp', 'coding_agent_integrations', 'gateway', 'packaging_deployment', 'telemetry_usage']`: 1
  - `['acp', 'codex', 'config', 'gateway', 'telemetry_usage']`: 1
- Opus modal: `['acp', 'agent_runtime', 'gateway', 'telemetry_usage']` (1/2)
- Opus label-set votes:
  - `['acp', 'agent_runtime', 'gateway', 'telemetry_usage']`: 1
  - `['acp', 'gateway', 'telemetry_usage']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-57824

- Title: Fix ACP image forwarding and Synology invalid-token throttling
- GitHub: https://github.com/openclaw/openclaw/pull/57824
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'api_surface', 'chat_integrations', 'security']` (2/3)
- GPT label-set votes:
  - `['acp', 'api_surface', 'chat_integrations', 'security']`: 2
  - `['acp', 'chat_integrations', 'security']`: 1
- Opus modal: `['acp', 'chat_integrations', 'security']` (2/2)
- Opus label-set votes:
  - `['acp', 'chat_integrations', 'security']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-57597

- Title: fix(acp): persist spawn labels in target session store
- GitHub: https://github.com/openclaw/openclaw/pull/57597
- Reasons: gpt_unstable
- GPT modal: `['acp', 'sessions']` (2/3)
- GPT label-set votes:
  - `['acp', 'reliability', 'sessions']`: 1
  - `['acp', 'sessions']`: 2
- Opus modal: `['acp', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acp', 'sessions']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `['acp', 'sessions', 'reliability']`

### openclaw-openclaw-56176

- Title: fix: accept MCP protocolVersion 2025-11-25 in ACP server (#56102)
- GitHub: https://github.com/openclaw/openclaw/pull/56176
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acp', 'mcp_tooling']` (3/3)
- GPT label-set votes:
  - `['acp', 'mcp_tooling']`: 3
- Opus modal: `['acp']` (2/2)
- Opus label-set votes:
  - `['acp']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-55723

- Title: fix(agents): preserve ACP requester agent overrides
- GitHub: https://github.com/openclaw/openclaw/pull/55723
- Reasons: opus_unstable
- GPT modal: `['acp']` (3/3)
- GPT label-set votes:
  - `['acp']`: 3
- Opus modal: `['acp']` (1/2)
- Opus label-set votes:
  - `['acp']`: 1
  - `['acp', 'agent_runtime']`: 1
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-40654

- Title: feat(discord): archive ACP-created threads on /acp close
- GitHub: https://github.com/openclaw/openclaw/pull/40654
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acp', 'chat_integrations', 'notifications', 'sessions']` (3/3)
- GPT label-set votes:
  - `['acp', 'chat_integrations', 'notifications', 'sessions']`: 3
- Opus modal: `['acp', 'chat_integrations', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acp', 'chat_integrations', 'sessions']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-69669

- Title: ACP: keep thread-bound follow-ups parent-orchestrated by default, not raw pass-through
- GitHub: https://github.com/openclaw/openclaw/issues/69669
- Reasons: opus_unstable
- GPT modal: `['acp', 'sessions']` (3/3)
- GPT label-set votes:
  - `['acp', 'sessions']`: 3
- Opus modal: `['acp', 'sessions']` (1/2)
- Opus label-set votes:
  - `['acp', 'sessions']`: 1
  - `['acp']`: 1
- Modal Jaccard: 1.000
- Legacy v5: `['acp', 'coding_agents', 'sessions']`

### openclaw-openclaw-51268

- Title: feat(acp): add --no-device-identity flag for token-only auth
- GitHub: https://github.com/openclaw/openclaw/pull/51268
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acp', 'api_surface', 'auth_identity', 'security']` (3/3)
- GPT label-set votes:
  - `['acp', 'api_surface', 'auth_identity', 'security']`: 3
- Opus modal: `['acp', 'auth_identity', 'security']` (2/2)
- Opus label-set votes:
  - `['acp', 'auth_identity', 'security']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-73910

- Title: BUG: OpenClaw-managed Codex ACP uses isolated CODEX_HOME without auth bridge and sends unsupported timeout config
- GitHub: https://github.com/openclaw/openclaw/issues/73910
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'acpx', 'codex', 'coding_agent_integrations', 'security']` (3/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'codex', 'coding_agent_integrations', 'security']`: 3
- Opus modal: `['acpx', 'auth_identity', 'codex', 'security']` (1/2)
- Opus label-set votes:
  - `['acpx', 'auth_identity', 'codex', 'security']`: 1
  - `['acp', 'acpx', 'codex', 'security']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `['acp', 'acpx', 'auth_identity', 'codex', 'config']`

### openclaw-openclaw-67244

- Title: Explicit ACP agent runs: embedded backend visibility failure and stale final JSON state after sessions_yield
- GitHub: https://github.com/openclaw/openclaw/issues/67244
- Reasons: gpt_unstable, gpt_flagged_human_review, opus_unstable, opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'acpx', 'api_surface', 'reliability', 'sessions']` (1/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'api_surface', 'reliability', 'sessions']`: 1
  - `['acp', 'acpx', 'agent_runtime', 'api_surface', 'sessions']`: 1
  - `['acp', 'acpx', 'api_surface', 'sessions']`: 1
- Opus modal: `['acp', 'acpx', 'gateway', 'reliability']` (1/2)
- Opus label-set votes:
  - `['acp', 'acpx', 'gateway', 'reliability']`: 1
  - `['acp', 'acpx', 'api_surface', 'gateway', 'sessions']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `['acp', 'acpx', 'agent_runtime', 'sessions', 'reliability']`

### openclaw-openclaw-50054

- Title: fix(acp): add distributed session locking with fail-closed redis fallback
- GitHub: https://github.com/openclaw/openclaw/pull/50054
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'config', 'queueing', 'reliability', 'sessions']` (3/3)
- GPT label-set votes:
  - `['acp', 'config', 'queueing', 'reliability', 'sessions']`: 3
- Opus modal: `['acp', 'config', 'queueing', 'reliability']` (1/2)
- Opus label-set votes:
  - `['acp', 'config', 'queueing', 'reliability']`: 1
  - `['acp', 'queueing', 'reliability']`: 1
- Modal Jaccard: 0.800
- Legacy v5: `['acp', 'sessions', 'reliability']`

### openclaw-openclaw-84039

- Title: fix(cli): honor --no-prefix-cwd in acp
- GitHub: https://github.com/openclaw/openclaw/pull/84039
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acp', 'api_surface']` (3/3)
- GPT label-set votes:
  - `['acp', 'api_surface']`: 3
- Opus modal: `['acp']` (2/2)
- Opus label-set votes:
  - `['acp']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `['acp']`

### openclaw-openclaw-64199

- Title: [Bug]: ACP configured binding uses parent channel ID for session key — all threads under same channel share one persistent Claude Code process
- GitHub: https://github.com/openclaw/openclaw/issues/64199
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acp', 'acpx', 'chat_integrations', 'security', 'sessions']` (3/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'chat_integrations', 'security', 'sessions']`: 3
- Opus modal: `['acp', 'chat_integrations', 'security', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acp', 'chat_integrations', 'security', 'sessions']`: 2
- Modal Jaccard: 0.800
- Legacy v5: `['acp', 'acpx', 'sessions', 'chat_integrations', 'security']`

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

### openclaw-openclaw-60979

- Title: feature: sessions_spawn ACP delivery to channel (stream output to Zulip/Discord topic)
- GitHub: https://github.com/openclaw/openclaw/issues/60979
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'chat_integrations', 'notifications', 'sessions']` (2/3)
- GPT label-set votes:
  - `['acp', 'chat_integrations', 'notifications', 'sessions']`: 2
  - `['acp', 'chat_integrations', 'notifications', 'sessions', 'tool_calling']`: 1
- Opus modal: `['acp', 'chat_integrations', 'notifications']` (2/2)
- Opus label-set votes:
  - `['acp', 'chat_integrations', 'notifications']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['acp', 'sessions', 'chat_integrations', 'notifications']`

### openclaw-openclaw-83863

- Title: ACP/Codex child tasks can be marked succeeded with progress-only output and no final deliverable
- GitHub: https://github.com/openclaw/openclaw/issues/83863
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'agent_runtime', 'codex', 'queueing', 'reliability']` (1/3)
- GPT label-set votes:
  - `['acp', 'agent_runtime', 'codex', 'queueing', 'reliability']`: 1
  - `['acp', 'agent_runtime', 'codex', 'coding_agent_integrations', 'queueing']`: 1
  - `['acp', 'agent_runtime', 'codex', 'notifications', 'queueing']`: 1
- Opus modal: `['acp', 'agent_runtime', 'reliability']` (1/2)
- Opus label-set votes:
  - `['acp', 'agent_runtime', 'reliability']`: 1
  - `['acp', 'agent_runtime', 'codex', 'reliability']`: 1
- Modal Jaccard: 0.600
- Legacy v5: `['acp', 'codex', 'coding_agents', 'agent_runtime', 'reliability']`

### openclaw-openclaw-58411

- Title: sessions_spawn lacks --bind here equivalent — agent cannot bind ACP session to existing Discord thread
- GitHub: https://github.com/openclaw/openclaw/issues/58411
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acp', 'chat_integrations', 'sessions', 'tool_calling']` (3/3)
- GPT label-set votes:
  - `['acp', 'chat_integrations', 'sessions', 'tool_calling']`: 3
- Opus modal: `['acp', 'chat_integrations', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acp', 'chat_integrations', 'sessions']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['acp', 'sessions', 'chat_integrations', 'api_surface']`

### openclaw-openclaw-56102

- Title: [Bug]: ACP server rejects MCP protocolVersion: 2025-11-25 from VS Code 1.113 / Cursor
- GitHub: https://github.com/openclaw/openclaw/issues/56102
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'mcp_tooling']` (2/3)
- GPT label-set votes:
  - `['acp', 'mcp_tooling']`: 2
  - `['acp']`: 1
- Opus modal: `['acp']` (2/2)
- Opus label-set votes:
  - `['acp']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-55484

- Title: ACP: support non-thread persistent affinity for cron and orchestrator sessions
- GitHub: https://github.com/openclaw/openclaw/issues/55484
- Reasons: gpt_unstable, gpt_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'cron_automation', 'security', 'sessions']` (2/3)
- GPT label-set votes:
  - `['acp', 'security', 'sessions', 'tool_calling']`: 1
  - `['acp', 'cron_automation', 'security', 'sessions']`: 2
- Opus modal: `['acp', 'security', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acp', 'security', 'sessions']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-54895

- Title: Feature: Inter-session progress streaming for sessions_send (ACP/long-running session support)
- GitHub: https://github.com/openclaw/openclaw/issues/54895
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['gateway', 'reliability', 'security', 'sessions']` (2/3)
- GPT label-set votes:
  - `['gateway', 'reliability', 'security', 'sessions']`: 2
  - `['api_surface', 'gateway', 'reliability', 'security', 'sessions']`: 1
- Opus modal: `['gateway', 'sessions']` (2/2)
- Opus label-set votes:
  - `['gateway', 'sessions']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-53406

- Title: feat: Let users steer running ACP/sub-agent sessions from Discord (and other chat surfaces)
- GitHub: https://github.com/openclaw/openclaw/issues/53406
- Reasons: gpt_flagged_human_review
- GPT modal: `['acp', 'agent_runtime', 'chat_integrations']` (3/3)
- GPT label-set votes:
  - `['acp', 'agent_runtime', 'chat_integrations']`: 3
- Opus modal: `['acp', 'agent_runtime', 'chat_integrations']` (2/2)
- Opus label-set votes:
  - `['acp', 'agent_runtime', 'chat_integrations']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-52249

- Title: ACP parent session stuck until refresh when yielded waiting for child completion
- GitHub: https://github.com/openclaw/openclaw/issues/52249
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'cron_automation', 'reliability', 'sessions']` (2/3)
- GPT label-set votes:
  - `['acp', 'cron_automation', 'reliability', 'sessions']`: 2
  - `['acp', 'reliability', 'sessions']`: 1
- Opus modal: `['acp', 'reliability', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acp', 'reliability', 'sessions']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['acp', 'sessions', 'queueing', 'reliability']`

### openclaw-openclaw-53319

- Title: [Bug]: ACP concurrent session spawns — first agent fails to launch CC process
- GitHub: https://github.com/openclaw/openclaw/issues/53319
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acp', 'acpx', 'coding_agent_integrations', 'reliability', 'sessions']` (3/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'coding_agent_integrations', 'reliability', 'sessions']`: 3
- Opus modal: `['acp', 'acpx', 'reliability']` (2/2)
- Opus label-set votes:
  - `['acp', 'acpx', 'reliability']`: 2
- Modal Jaccard: 0.600
- Legacy v5: `['acp', 'acpx', 'sessions', 'reliability']`

### openclaw-openclaw-50798

- Title: [Feature]: Visible agent-to-agent messaging for ACP thread-bound sessions (proxy-only delivery without main session creation)
- GitHub: https://github.com/openclaw/openclaw/issues/50798
- Reasons: gpt_flagged_human_review, opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'api_surface', 'chat_integrations', 'sessions']` (3/3)
- GPT label-set votes:
  - `['acp', 'api_surface', 'chat_integrations', 'sessions']`: 3
- Opus modal: `['acp', 'chat_integrations', 'notifications', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acp', 'chat_integrations', 'notifications', 'sessions']`: 2
- Modal Jaccard: 0.600
- Legacy v5: `[]`

### openclaw-openclaw-49567

- Title: [Feature] Allow per-binding tool restrictions (tools.deny) in route/ACP bindings
- GitHub: https://github.com/openclaw/openclaw/issues/49567
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acp', 'config', 'exec_tools', 'gateway', 'security']` (3/3)
- GPT label-set votes:
  - `['acp', 'config', 'exec_tools', 'gateway', 'security']`: 3
- Opus modal: `['acp', 'config', 'exec_tools', 'security']` (2/2)
- Opus label-set votes:
  - `['acp', 'config', 'exec_tools', 'security']`: 2
- Modal Jaccard: 0.800
- Legacy v5: `[]`

### openclaw-openclaw-45841

- Title: [Feature]: Sandboxing + ACP
- GitHub: https://github.com/openclaw/openclaw/issues/45841
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'config', 'sandboxing', 'security']` (2/3)
- GPT label-set votes:
  - `['acp', 'config', 'sandboxing', 'security']`: 2
  - `['acp', 'sandboxing', 'security']`: 1
- Opus modal: `['acp', 'sandboxing', 'security']` (2/2)
- Opus label-set votes:
  - `['acp', 'sandboxing', 'security']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['acp', 'sandboxing', 'security', 'sessions']`

### openclaw-openclaw-44375

- Title: Adding ACP agent to agents.list silently hijacks all routing from implicit main agent
- GitHub: https://github.com/openclaw/openclaw/issues/44375
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['agent_runtime', 'config', 'security']` (1/3)
- GPT label-set votes:
  - `['agent_runtime', 'config', 'security']`: 1
  - `['config', 'security', 'sessions']`: 1
  - `['agent_runtime', 'config', 'security', 'sessions']`: 1
- Opus modal: `['agent_runtime', 'config', 'sessions']` (1/2)
- Opus label-set votes:
  - `['agent_runtime', 'config', 'sessions']`: 1
  - `['agent_runtime', 'config']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-44294

- Title: Preserve structured ACP backend error kinds instead of mapping all errors to `end_turn`
- GitHub: https://github.com/openclaw/openclaw/issues/44294
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acp', 'api_surface']` (3/3)
- GPT label-set votes:
  - `['acp', 'api_surface']`: 3
- Opus modal: `['acp']` (2/2)
- Opus label-set votes:
  - `['acp']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-38907

- Title: ACP bridge sessions fail with acp_session_init_failed (echo + end_turn, no chunks)
- GitHub: https://github.com/openclaw/openclaw/issues/38907
- Reasons: gpt_unstable
- GPT modal: `['acp', 'sessions']` (2/3)
- GPT label-set votes:
  - `['acp', 'reliability', 'sessions']`: 1
  - `['acp', 'sessions']`: 2
- Opus modal: `['acp', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acp', 'sessions']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-84758

- Title: feat(subagents): add execution backend placement contract
- GitHub: https://github.com/openclaw/openclaw/pull/84758
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'agent_runtime', 'config', 'tool_calling']` (2/3)
- GPT label-set votes:
  - `['agent_runtime', 'config', 'tool_calling']`: 1
  - `['acp', 'agent_runtime', 'config', 'tool_calling']`: 2
- Opus modal: `['agent_runtime', 'config']` (2/2)
- Opus label-set votes:
  - `['agent_runtime', 'config']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-84742

- Title: fix(doctor): warn when sandbox hides MCP tools
- GitHub: https://github.com/openclaw/openclaw/pull/84742
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'mcp_tooling', 'sandboxing', 'telemetry_usage']` (2/3)
- GPT label-set votes:
  - `['config', 'mcp_tooling', 'sandboxing', 'telemetry_usage']`: 2
  - `['config', 'mcp_tooling', 'sandboxing', 'skills_plugins']`: 1
- Opus modal: `['config', 'mcp_tooling', 'sandboxing']` (2/2)
- Opus label-set votes:
  - `['config', 'mcp_tooling', 'sandboxing']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-44348

- Title: fix(hooks): expose sessionKey and agentId in agent_end and before_agent_start events
- GitHub: https://github.com/openclaw/openclaw/pull/44348
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['hooks', 'skills_plugins']` (3/3)
- GPT label-set votes:
  - `['hooks', 'skills_plugins']`: 3
- Opus modal: `['hooks']` (2/2)
- Opus label-set votes:
  - `['hooks']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-44011

- Title: fix(hooks): expose session context in typed message hooks
- GitHub: https://github.com/openclaw/openclaw/pull/44011
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['hooks', 'sessions', 'skills_plugins']` (2/3)
- GPT label-set votes:
  - `['hooks', 'sessions', 'skills_plugins']`: 2
  - `['api_surface', 'hooks', 'skills_plugins']`: 1
- Opus modal: `['hooks', 'skills_plugins']` (2/2)
- Opus label-set votes:
  - `['hooks', 'skills_plugins']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-63919

- Title: feat(gateway): wire coding tools into /tools/invoke HTTP surface
- GitHub: https://github.com/openclaw/openclaw/pull/63919
- Reasons: gpt_unstable, gpt_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['api_surface', 'config', 'gateway', 'security']` (2/3)
- GPT label-set votes:
  - `['api_surface', 'config', 'exec_tools', 'gateway', 'security']`: 1
  - `['api_surface', 'config', 'gateway', 'security']`: 2
- Opus modal: `['config', 'exec_tools', 'gateway', 'security']` (2/2)
- Opus label-set votes:
  - `['config', 'exec_tools', 'gateway', 'security']`: 2
- Modal Jaccard: 0.600
- Legacy v5: `[]`

### openclaw-openclaw-45524

- Title: fix(gateway): flag agents.defaults.sandbox.mode=off as dangerous at startup
- GitHub: https://github.com/openclaw/openclaw/pull/45524
- Reasons: gpt_unstable
- GPT modal: `['auth_identity', 'config', 'sandboxing', 'security']` (2/3)
- GPT label-set votes:
  - `['auth_identity', 'config', 'sandboxing', 'security']`: 2
  - `['config', 'sandboxing', 'security']`: 1
- Opus modal: `['auth_identity', 'config', 'sandboxing', 'security']` (2/2)
- Opus label-set votes:
  - `['auth_identity', 'config', 'sandboxing', 'security']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-45465

- Title: cron: add lifecycle hooks for job execution
- GitHub: https://github.com/openclaw/openclaw/pull/45465
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'cron_automation', 'hooks', 'reliability', 'security']` (2/3)
- GPT label-set votes:
  - `['config', 'cron_automation', 'hooks', 'security']`: 1
  - `['config', 'cron_automation', 'hooks', 'reliability', 'security']`: 2
- Opus modal: `['config', 'cron_automation', 'hooks']` (1/2)
- Opus label-set votes:
  - `['config', 'cron_automation', 'hooks']`: 1
  - `['config', 'cron_automation', 'hooks', 'security']`: 1
- Modal Jaccard: 0.600
- Legacy v5: `[]`

### openclaw-openclaw-44972

- Title: fix(gateway): emit response.incomplete for OpenResponses tool-call SSE responses
- GitHub: https://github.com/openclaw/openclaw/pull/44972
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['api_surface', 'gateway']` (2/3)
- GPT label-set votes:
  - `['api_surface', 'gateway']`: 2
  - `['api_surface', 'gateway', 'tool_calling']`: 1
- Opus modal: `['api_surface', 'tool_calling']` (2/2)
- Opus label-set votes:
  - `['api_surface', 'tool_calling']`: 2
- Modal Jaccard: 0.333
- Legacy v5: `[]`

### openclaw-openclaw-44523

- Title: fix(session): preserve model override across daily freshness resets
- GitHub: https://github.com/openclaw/openclaw/pull/44523
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['reliability', 'sessions']` (2/3)
- GPT label-set votes:
  - `['reliability', 'sessions']`: 2
  - `['sessions']`: 1
- Opus modal: `['sessions']` (2/2)
- Opus label-set votes:
  - `['sessions']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-44098

- Title: fix(security): add default pidsLimit for sandbox containers
- GitHub: https://github.com/openclaw/openclaw/pull/44098
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['config', 'sandboxing', 'security']` (3/3)
- GPT label-set votes:
  - `['config', 'sandboxing', 'security']`: 3
- Opus modal: `['sandboxing', 'security']` (2/2)
- Opus label-set votes:
  - `['sandboxing', 'security']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-44015

- Title: gateway: enforce 512 KB max length for chat.send message
- GitHub: https://github.com/openclaw/openclaw/pull/44015
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['api_surface', 'gateway', 'reliability']` (3/3)
- GPT label-set votes:
  - `['api_surface', 'gateway', 'reliability']`: 3
- Opus modal: `['api_surface', 'gateway']` (2/2)
- Opus label-set votes:
  - `['api_surface', 'gateway']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-84693

- Title: fix(sessions): reduce session-store memory retention
- GitHub: https://github.com/openclaw/openclaw/pull/84693
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['api_surface', 'reliability', 'sessions', 'skills_plugins']` (3/3)
- GPT label-set votes:
  - `['api_surface', 'reliability', 'sessions', 'skills_plugins']`: 3
- Opus modal: `['reliability', 'sessions', 'skills_plugins']` (2/2)
- Opus label-set votes:
  - `['reliability', 'sessions', 'skills_plugins']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-49112

- Title: add doctor coverage for stale gateway locks
- GitHub: https://github.com/openclaw/openclaw/pull/49112
- Reasons: gpt_unstable
- GPT modal: `['gateway', 'reliability']` (2/3)
- GPT label-set votes:
  - `['gateway', 'reliability']`: 2
  - `['gateway', 'reliability', 'telemetry_usage']`: 1
- Opus modal: `['gateway', 'reliability']` (2/2)
- Opus label-set votes:
  - `['gateway', 'reliability']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-62733

- Title: Fix local memory embedding VRAM fallback and logging file resolution
- GitHub: https://github.com/openclaw/openclaw/pull/62733
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'memory', 'reliability', 'self_hosted_inference', 'telemetry_usage']` (3/3)
- GPT label-set votes:
  - `['config', 'memory', 'reliability', 'self_hosted_inference', 'telemetry_usage']`: 3
- Opus modal: `['config', 'memory', 'reliability', 'self_hosted_inference']` (1/2)
- Opus label-set votes:
  - `['config', 'memory', 'reliability', 'self_hosted_inference']`: 1
  - `['config', 'reliability', 'self_hosted_inference']`: 1
- Modal Jaccard: 0.800
- Legacy v5: `[]`

### openclaw-openclaw-74204

- Title: memory.qmd.update.embedTimeoutMs default (120 s) is too low for local GGUF; error message doesn't surface the fix
- GitHub: https://github.com/openclaw/openclaw/issues/74204
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'memory', 'reliability', 'self_hosted_inference', 'telemetry_usage']` (3/3)
- GPT label-set votes:
  - `['config', 'memory', 'reliability', 'self_hosted_inference', 'telemetry_usage']`: 3
- Opus modal: `['config', 'memory', 'self_hosted_inference']` (1/2)
- Opus label-set votes:
  - `['config', 'memory', 'self_hosted_inference']`: 1
  - `['config', 'memory', 'reliability', 'self_hosted_inference']`: 1
- Modal Jaccard: 0.600
- Legacy v5: `['config', 'local_models', 'memory', 'reliability']`

### openclaw-openclaw-75657

- Title: fix: local GGUF embedding model warmup blocks Node.js event loop for minutes on startup (ARM64/Pi)
- GitHub: https://github.com/openclaw/openclaw/issues/75657
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['gateway', 'memory', 'reliability', 'self_hosted_inference']` (3/3)
- GPT label-set votes:
  - `['gateway', 'memory', 'reliability', 'self_hosted_inference']`: 3
- Opus modal: `['memory', 'reliability', 'self_hosted_inference']` (2/2)
- Opus label-set votes:
  - `['memory', 'reliability', 'self_hosted_inference']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['gateway', 'local_models', 'memory', 'reliability']`

### openclaw-openclaw-80379

- Title: [Bug]: Tool result secret redaction mutates session history, breaking KV cache prefix matching for local LLM providers
- GitHub: https://github.com/openclaw/openclaw/issues/80379
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['security', 'self_hosted_inference', 'sessions', 'tool_calling']` (3/3)
- GPT label-set votes:
  - `['security', 'self_hosted_inference', 'sessions', 'tool_calling']`: 3
- Opus modal: `['security', 'self_hosted_inference', 'sessions']` (1/2)
- Opus label-set votes:
  - `['security', 'self_hosted_inference', 'sessions']`: 1
  - `['security', 'self_hosted_inference', 'sessions', 'tool_calling']`: 1
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-43493

- Title: feat: configure metadata (contextWindow, maxTokens, etc.) for custom provider setup
- GitHub: https://github.com/openclaw/openclaw/pull/43493
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'inference_api', 'model_lifecycle', 'ui_tui']` (2/3)
- GPT label-set votes:
  - `['config', 'inference_api', 'model_lifecycle', 'ui_tui']`: 2
  - `['config', 'inference_api', 'model_lifecycle']`: 1
- Opus modal: `['config', 'model_lifecycle']` (2/2)
- Opus label-set votes:
  - `['config', 'model_lifecycle']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-44136

- Title: fix(copilot): respect user-configured baseUrl in token flow
- GitHub: https://github.com/openclaw/openclaw/pull/44136
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['config', 'inference_api']` (3/3)
- GPT label-set votes:
  - `['config', 'inference_api']`: 3
- Opus modal: `['inference_api']` (2/2)
- Opus label-set votes:
  - `['inference_api']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-81304

- Title: fix(setup): preserve existing primary model when applying provider auth (#64129)
- GitHub: https://github.com/openclaw/openclaw/pull/81304
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'inference_api']` (2/3)
- GPT label-set votes:
  - `['config', 'inference_api', 'model_lifecycle']`: 1
  - `['config', 'inference_api']`: 2
- Opus modal: `['config', 'model_lifecycle']` (1/2)
- Opus label-set votes:
  - `['config', 'model_lifecycle']`: 1
  - `['inference_api', 'model_lifecycle']`: 1
- Modal Jaccard: 0.333
- Legacy v5: `[]`

### openclaw-openclaw-54802

- Title: fix: align codex simple completions with responses API
- GitHub: https://github.com/openclaw/openclaw/pull/54802
- Reasons: gpt_unstable
- GPT modal: `['codex', 'inference_api']` (2/3)
- GPT label-set votes:
  - `['codex', 'inference_api']`: 2
  - `['inference_api']`: 1
- Opus modal: `['codex', 'inference_api']` (2/2)
- Opus label-set votes:
  - `['codex', 'inference_api']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-52075

- Title: docs: clarify custom mobile client usage for chat completions
- GitHub: https://github.com/openclaw/openclaw/pull/52075
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['api_surface', 'docs', 'sessions']` (1/3)
- GPT label-set votes:
  - `['api_surface', 'docs', 'sessions']`: 1
  - `['api_surface', 'docs']`: 1
  - `['api_surface', 'docs', 'gateway', 'sessions']`: 1
- Opus modal: `['api_surface', 'docs']` (2/2)
- Opus label-set votes:
  - `['api_surface', 'docs']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-78977

- Title: fix(providers): skip store:false for proxy-like Responses API endpoints (#78897)
- GitHub: https://github.com/openclaw/openclaw/pull/78977
- Reasons: gpt_unstable, gpt_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['inference_api', 'security']` (2/3)
- GPT label-set votes:
  - `['inference_api', 'security']`: 2
  - `['inference_api']`: 1
- Opus modal: `['inference_api']` (2/2)
- Opus label-set votes:
  - `['inference_api']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `['local_model_providers', 'model_serving', 'reliability']`

### openclaw-openclaw-82355

- Title: Fix streamed chat completions dropping leading less-than
- GitHub: https://github.com/openclaw/openclaw/pull/82355
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['api_surface']` (1/3)
- GPT label-set votes:
  - `['api_surface']`: 1
  - `['api_surface', 'gateway', 'reliability']`: 1
  - `['api_surface', 'gateway']`: 1
- Opus modal: `['api_surface', 'gateway', 'reliability']` (1/2)
- Opus label-set votes:
  - `['api_surface', 'gateway', 'reliability']`: 1
  - `['api_surface', 'gateway']`: 1
- Modal Jaccard: 0.333
- Legacy v5: `[]`

### openclaw-openclaw-84791

- Title: Fix Telegram TTS voice-note routing
- GitHub: https://github.com/openclaw/openclaw/pull/84791
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['chat_integrations', 'notifications']` (2/3)
- GPT label-set votes:
  - `['chat_integrations', 'notifications']`: 2
  - `['chat_integrations']`: 1
- Opus modal: `['chat_integrations']` (2/2)
- Opus label-set votes:
  - `['chat_integrations']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-83988

- Title: fix(tts): defer text settlement for final-mode TTS to eliminate churn (#83511)
- GitHub: https://github.com/openclaw/openclaw/pull/83988
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'chat_integrations', 'inference_api', 'notifications']` (2/3)
- GPT label-set votes:
  - `['acp', 'chat_integrations', 'inference_api', 'notifications']`: 2
  - `['chat_integrations', 'inference_api', 'notifications']`: 1
- Opus modal: `['acp', 'chat_integrations', 'notifications']` (2/2)
- Opus label-set votes:
  - `['acp', 'chat_integrations', 'notifications']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-84660

- Title: [Bug] Voice STT: empty moonshine transcripts passed as raw JSON to LLM, clogging serialized processing queue
- GitHub: https://github.com/openclaw/openclaw/issues/84660
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['chat_integrations', 'queueing', 'reliability', 'self_hosted_inference']` (2/3)
- GPT label-set votes:
  - `['chat_integrations', 'queueing', 'reliability', 'self_hosted_inference']`: 2
  - `['chat_integrations', 'queueing', 'self_hosted_inference']`: 1
- Opus modal: `['chat_integrations', 'queueing', 'self_hosted_inference']` (1/2)
- Opus label-set votes:
  - `['chat_integrations', 'queueing', 'self_hosted_inference']`: 1
  - `['chat_integrations', 'self_hosted_inference']`: 1
- Modal Jaccard: 0.750
- Legacy v5: `['chat_integrations', 'self_hosted_inference', 'queueing', 'reliability']`

### openclaw-openclaw-78919

- Title: [Bug] ACP sessions_spawn doesn't route images to Codex's native vision like acpx codex exec does
- GitHub: https://github.com/openclaw/openclaw/issues/78919
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'codex', 'coding_agent_integrations']` (1/3)
- GPT label-set votes:
  - `['acp', 'codex', 'coding_agent_integrations']`: 1
  - `['acp', 'agent_runtime', 'codex', 'coding_agent_integrations']`: 1
  - `['acp', 'codex', 'coding_agent_integrations', 'sessions']`: 1
- Opus modal: `['acp', 'codex']` (2/2)
- Opus label-set votes:
  - `['acp', 'codex']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['acp', 'acpx', 'codex', 'sessions']`

### openclaw-openclaw-81541

- Title: fix(acpx): tolerate adapter config gaps
- GitHub: https://github.com/openclaw/openclaw/pull/81541
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acp', 'acpx', 'codex', 'coding_agent_integrations', 'sessions']` (3/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'codex', 'coding_agent_integrations', 'sessions']`: 3
- Opus modal: `['acp', 'acpx', 'codex', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acp', 'acpx', 'codex', 'sessions']`: 2
- Modal Jaccard: 0.800
- Legacy v5: `[]`

### openclaw-openclaw-79539

- Title: fix(acpx): write per-event JSONL stream to advertised event_log.active_path
- GitHub: https://github.com/openclaw/openclaw/pull/79539
- Reasons: gpt_unstable
- GPT modal: `['acpx', 'telemetry_usage']` (2/3)
- GPT label-set votes:
  - `['acpx', 'telemetry_usage']`: 2
  - `['acp', 'acpx', 'telemetry_usage']`: 1
- Opus modal: `['acpx', 'telemetry_usage']` (2/2)
- Opus label-set votes:
  - `['acpx', 'telemetry_usage']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-80475

- Title: test(acpx): accept built-dist MCP server resolution when dist exists
- GitHub: https://github.com/openclaw/openclaw/pull/80475
- Reasons: gpt_unstable
- GPT modal: `['acpx', 'tests_ci']` (2/3)
- GPT label-set votes:
  - `['acpx', 'mcp_tooling', 'tests_ci']`: 1
  - `['acpx', 'tests_ci']`: 2
- Opus modal: `['acpx', 'tests_ci']` (2/2)
- Opus label-set votes:
  - `['acpx', 'tests_ci']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `['acpx', 'mcp_tooling', 'tests_ci']`

### openclaw-openclaw-84811

- Title: agents_list shows orphaned allowlist entries as spawnable agents; sessions_spawn accepts them without validation
- GitHub: https://github.com/openclaw/openclaw/issues/84811
- Reasons: gpt_unstable, gpt_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['agent_runtime', 'config', 'security', 'sessions']` (2/3)
- GPT label-set votes:
  - `['agent_runtime', 'config', 'security']`: 1
  - `['agent_runtime', 'config', 'security', 'sessions']`: 2
- Opus modal: `['agent_runtime', 'config', 'security']` (2/2)
- Opus label-set votes:
  - `['agent_runtime', 'config', 'security']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-72013

- Title: ACP startup identity reconcile warns on terminal one-shot sessions
- GitHub: https://github.com/openclaw/openclaw/issues/72013
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'gateway', 'sessions']` (2/3)
- GPT label-set votes:
  - `['acp', 'gateway', 'sessions']`: 2
  - `['acp', 'gateway', 'reliability', 'sessions']`: 1
- Opus modal: `['acp', 'sessions']` (1/2)
- Opus label-set votes:
  - `['acp', 'sessions']`: 1
  - `['acp', 'gateway', 'sessions']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `['acp', 'gateway', 'sessions']`

### openclaw-openclaw-48834

- Title: feat(feishu): enable /focus and /unfocus commands + fix ACP block delivery
- GitHub: https://github.com/openclaw/openclaw/pull/48834
- Reasons: gpt_unstable, opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'chat_integrations', 'config', 'sessions', 'skills_plugins']` (2/3)
- GPT label-set votes:
  - `['acp', 'chat_integrations', 'config', 'sessions', 'skills_plugins']`: 2
  - `['acp', 'chat_integrations', 'config', 'notifications', 'sessions']`: 1
- Opus modal: `['acp', 'chat_integrations', 'config', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acp', 'chat_integrations', 'config', 'sessions']`: 2
- Modal Jaccard: 0.800
- Legacy v5: `[]`

### openclaw-openclaw-65242

- Title: fix: CompletionDeliveryGate to prevent duplicate ACP completion delivery
- GitHub: https://github.com/openclaw/openclaw/pull/65242
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'config', 'notifications', 'reliability']` (2/3)
- GPT label-set votes:
  - `['acp', 'config', 'notifications', 'reliability']`: 2
  - `['acp', 'config', 'hooks', 'notifications', 'reliability']`: 1
- Opus modal: `['acp', 'agent_runtime', 'notifications', 'reliability']` (2/2)
- Opus label-set votes:
  - `['acp', 'agent_runtime', 'notifications', 'reliability']`: 2
- Modal Jaccard: 0.600
- Legacy v5: `['acp', 'coding_agents', 'notifications', 'reliability', 'sessions']`

### openclaw-openclaw-84810

- Title: fix #84789: sanitize colons in dirName for Telegram forum topic sessions
- GitHub: https://github.com/openclaw/openclaw/pull/84810
- Reasons: gpt_unstable, gpt_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['chat_integrations', 'reliability', 'security', 'skills_plugins']` (2/3)
- GPT label-set votes:
  - `['reliability', 'security', 'skills_plugins']`: 1
  - `['chat_integrations', 'reliability', 'security', 'skills_plugins']`: 2
- Opus modal: `['reliability', 'security', 'skills_plugins']` (2/2)
- Opus label-set votes:
  - `['reliability', 'security', 'skills_plugins']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-84699

- Title: fix(doctor): warn when sandbox hides MCP tools
- GitHub: https://github.com/openclaw/openclaw/pull/84699
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'docs', 'mcp_tooling', 'sandboxing', 'telemetry_usage']` (1/3)
- GPT label-set votes:
  - `['config', 'docs', 'mcp_tooling', 'sandboxing', 'telemetry_usage']`: 1
  - `['config', 'mcp_tooling', 'sandboxing', 'skills_plugins']`: 1
  - `['config', 'docs', 'mcp_tooling', 'sandboxing']`: 1
- Opus modal: `['config', 'mcp_tooling', 'sandboxing']` (2/2)
- Opus label-set votes:
  - `['config', 'mcp_tooling', 'sandboxing']`: 2
- Modal Jaccard: 0.600
- Legacy v5: `[]`

### openclaw-openclaw-80909

- Title: MCP server tools never reach outbound `tools[]` across 4.26 → 5.7 (cluster previously closed + locked as 'resolved')
- GitHub: https://github.com/openclaw/openclaw/issues/80909
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['inference_api', 'mcp_tooling', 'tool_calling']` (3/3)
- GPT label-set votes:
  - `['inference_api', 'mcp_tooling', 'tool_calling']`: 3
- Opus modal: `['agent_runtime', 'mcp_tooling', 'tool_calling']` (1/2)
- Opus label-set votes:
  - `['agent_runtime', 'mcp_tooling', 'tool_calling']`: 1
  - `['inference_api', 'mcp_tooling', 'tool_calling']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-83921

- Title: Benchmark spawner scripts use bare "node" instead of process.execPath, risking version mismatch
- GitHub: https://github.com/openclaw/openclaw/issues/83921
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['exec_tools', 'tests_ci']` (2/3)
- GPT label-set votes:
  - `['tests_ci']`: 1
  - `['exec_tools', 'tests_ci']`: 2
- Opus modal: `['tests_ci']` (2/2)
- Opus label-set votes:
  - `['tests_ci']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-83030

- Title: feat(image-generation): Add ReCraft V4.1 model family support (Standard, Utility, Vector) via OpenRouter
- GitHub: https://github.com/openclaw/openclaw/issues/83030
- Reasons: opus_unstable
- GPT modal: `['api_surface', 'inference_api', 'model_lifecycle']` (3/3)
- GPT label-set votes:
  - `['api_surface', 'inference_api', 'model_lifecycle']`: 3
- Opus modal: `['api_surface', 'inference_api', 'model_lifecycle']` (1/2)
- Opus label-set votes:
  - `['api_surface', 'inference_api', 'model_lifecycle']`: 1
  - `['inference_api', 'model_lifecycle']`: 1
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-7403

- Title: Feature: Private Mode for demos and content creation
- GitHub: https://github.com/openclaw/openclaw/issues/7403
- Reasons: gpt_unstable, gpt_flagged_human_review, opus_unstable, opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['gateway', 'memory', 'security', 'sessions', 'ui_tui']` (2/3)
- GPT label-set votes:
  - `['gateway', 'memory', 'security', 'sessions', 'ui_tui']`: 2
  - `['config', 'memory', 'security', 'sessions', 'ui_tui']`: 1
- Opus modal: `['config', 'gateway', 'memory', 'sessions', 'ui_tui']` (1/2)
- Opus label-set votes:
  - `['config', 'gateway', 'memory', 'sessions', 'ui_tui']`: 1
  - `['config', 'gateway', 'memory', 'security', 'sessions']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-84790

- Title: Keep Codex runtime context out of user history
- GitHub: https://github.com/openclaw/openclaw/pull/84790
- Reasons: gpt_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['codex', 'coding_agent_integrations', 'security', 'sessions']` (3/3)
- GPT label-set votes:
  - `['codex', 'coding_agent_integrations', 'security', 'sessions']`: 3
- Opus modal: `['codex', 'security', 'sessions']` (2/2)
- Opus label-set votes:
  - `['codex', 'security', 'sessions']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-84772

- Title: fix(codex): honor tool result cap in app-server transcripts
- GitHub: https://github.com/openclaw/openclaw/pull/84772
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['codex', 'config', 'sessions', 'tool_calling']` (2/3)
- GPT label-set votes:
  - `['codex', 'config', 'sessions', 'tool_calling']`: 2
  - `['codex', 'config', 'tool_calling']`: 1
- Opus modal: `['codex', 'tool_calling']` (2/2)
- Opus label-set votes:
  - `['codex', 'tool_calling']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-84755

- Title: [Bug]: Codex harness sessions stall with active_work_without_progress and stale running/hasActiveRun=false state on 2026.5.19
- GitHub: https://github.com/openclaw/openclaw/issues/84755
- Reasons: gpt_unstable, gpt_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['codex', 'coding_agent_integrations', 'reliability', 'sessions']` (2/3)
- GPT label-set votes:
  - `['codex', 'coding_agent_integrations', 'reliability', 'sessions']`: 2
  - `['codex', 'coding_agent_integrations', 'queueing', 'reliability', 'sessions']`: 1
- Opus modal: `['codex', 'reliability', 'sessions']` (2/2)
- Opus label-set votes:
  - `['codex', 'reliability', 'sessions']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-84795

- Title: Windows native: shell env fallback failed with spawnSync /bin/sh ENOENT
- GitHub: https://github.com/openclaw/openclaw/issues/84795
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'exec_tools']` (2/3)
- GPT label-set votes:
  - `['config']`: 1
  - `['config', 'exec_tools']`: 2
- Opus modal: `['exec_tools', 'reliability']` (1/2)
- Opus label-set votes:
  - `['exec_tools', 'reliability']`: 1
  - `['exec_tools']`: 1
- Modal Jaccard: 0.333
- Legacy v5: `[]`

### openclaw-openclaw-84807

- Title: fix(supervisor): keep workers alive across gateway restarts
- GitHub: https://github.com/openclaw/openclaw/pull/84807
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['exec_tools', 'gateway', 'packaging_deployment', 'reliability']` (2/3)
- GPT label-set votes:
  - `['exec_tools', 'packaging_deployment', 'reliability']`: 1
  - `['exec_tools', 'gateway', 'packaging_deployment', 'reliability']`: 2
- Opus modal: `['packaging_deployment', 'reliability']` (1/2)
- Opus label-set votes:
  - `['packaging_deployment', 'reliability']`: 1
  - `['exec_tools', 'packaging_deployment', 'reliability']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-80056

- Title: Policy: add tool metadata conformance
- GitHub: https://github.com/openclaw/openclaw/pull/80056
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['api_surface', 'config', 'security', 'skills_plugins']` (2/3)
- GPT label-set votes:
  - `['api_surface', 'config', 'skills_plugins']`: 1
  - `['api_surface', 'config', 'security', 'skills_plugins']`: 2
- Opus modal: `['config', 'skills_plugins']` (2/2)
- Opus label-set votes:
  - `['config', 'skills_plugins']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-48637

- Title: docs: explain Paperclip gateway pairing approval
- GitHub: https://github.com/openclaw/openclaw/pull/48637
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['api_surface', 'auth_identity', 'coding_agent_integrations', 'config', 'docs']` (1/3)
- GPT label-set votes:
  - `['api_surface', 'auth_identity', 'coding_agent_integrations', 'config', 'docs']`: 1
  - `['approvals', 'auth_identity', 'coding_agent_integrations', 'config', 'docs']`: 1
  - `['approvals', 'auth_identity', 'coding_agent_integrations', 'docs']`: 1
- Opus modal: `['auth_identity', 'docs', 'gateway']` (1/2)
- Opus label-set votes:
  - `['auth_identity', 'docs', 'gateway']`: 1
  - `['auth_identity', 'docs']`: 1
- Modal Jaccard: 0.333
- Legacy v5: `[]`

### openclaw-openclaw-66685

- Title: Suppress expired exec approval followup warnings
- GitHub: https://github.com/openclaw/openclaw/pull/66685
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['approvals', 'telemetry_usage']` (2/3)
- GPT label-set votes:
  - `['approvals', 'telemetry_usage']`: 2
  - `['approvals', 'exec_tools', 'telemetry_usage']`: 1
- Opus modal: `['approvals']` (1/2)
- Opus label-set votes:
  - `['approvals']`: 1
  - `['approvals', 'exec_tools']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-65398

- Title: fix(feishu): preserve top-level groupPolicy and avoid duplicate registration
- GitHub: https://github.com/openclaw/openclaw/pull/65398
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['chat_integrations', 'config', 'hooks']` (3/3)
- GPT label-set votes:
  - `['chat_integrations', 'config', 'hooks']`: 3
- Opus modal: `['chat_integrations', 'config', 'reliability']` (1/2)
- Opus label-set votes:
  - `['chat_integrations', 'config', 'reliability']`: 1
  - `['chat_integrations', 'config']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-84809

- Title: [Data loss] 2026.5.19 update/backup flow removed ~/.openclaw/workspace and left plugin/npm state inconsistent
- GitHub: https://github.com/openclaw/openclaw/issues/84809
- Reasons: gpt_unstable
- GPT modal: `['packaging_deployment', 'reliability', 'skills_plugins']` (2/3)
- GPT label-set votes:
  - `['config', 'packaging_deployment', 'reliability', 'skills_plugins']`: 1
  - `['packaging_deployment', 'reliability', 'skills_plugins']`: 2
- Opus modal: `['packaging_deployment', 'reliability', 'skills_plugins']` (2/2)
- Opus label-set votes:
  - `['packaging_deployment', 'reliability', 'skills_plugins']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-84799

- Title: fix(config): validate browser sandbox bind sources [AI]
- GitHub: https://github.com/openclaw/openclaw/pull/84799
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['config', 'sandboxing', 'security']` (3/3)
- GPT label-set votes:
  - `['config', 'sandboxing', 'security']`: 3
- Opus modal: `['config', 'sandboxing']` (2/2)
- Opus label-set votes:
  - `['config', 'sandboxing']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-84788

- Title: Fix OpenShell sandbox backend CLI resolution
- GitHub: https://github.com/openclaw/openclaw/pull/84788
- Reasons: gpt_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['exec_tools', 'packaging_deployment', 'sandboxing', 'security']` (3/3)
- GPT label-set votes:
  - `['exec_tools', 'packaging_deployment', 'sandboxing', 'security']`: 3
- Opus modal: `['exec_tools', 'packaging_deployment', 'sandboxing']` (2/2)
- Opus label-set votes:
  - `['exec_tools', 'packaging_deployment', 'sandboxing']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-71889

- Title: [Bug]: agents add wizard pre-fills nested workspace path (workspace/<id>) instead of documented peer-level (workspace-<id>)
- GitHub: https://github.com/openclaw/openclaw/issues/71889
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'reliability', 'security']` (1/3)
- GPT label-set votes:
  - `['config', 'reliability', 'security']`: 1
  - `['config', 'security']`: 1
  - `['config', 'reliability', 'sandboxing', 'security']`: 1
- Opus modal: `['config', 'security']` (2/2)
- Opus label-set votes:
  - `['config', 'security']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-84337

- Title: [Bug]: Hook ingress token unlocks password-mode gateway auth
- GitHub: https://github.com/openclaw/openclaw/issues/84337
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['auth_identity', 'config', 'gateway', 'hooks', 'security']` (1/3)
- GPT label-set votes:
  - `['auth_identity', 'config', 'gateway', 'hooks', 'security']`: 1
  - `['auth_identity', 'config', 'hooks', 'security']`: 1
  - `['auth_identity', 'gateway', 'hooks', 'security']`: 1
- Opus modal: `['gateway', 'hooks', 'security']` (2/2)
- Opus label-set votes:
  - `['gateway', 'hooks', 'security']`: 2
- Modal Jaccard: 0.600
- Legacy v5: `['security', 'auth_identity', 'gateway', 'hooks']`

### openclaw-openclaw-65149

- Title: Add final reply payloads plugin hook
- GitHub: https://github.com/openclaw/openclaw/pull/65149
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['hooks', 'security', 'skills_plugins']` (2/3)
- GPT label-set votes:
  - `['hooks', 'security', 'skills_plugins']`: 2
  - `['api_surface', 'hooks', 'security', 'skills_plugins']`: 1
- Opus modal: `['hooks', 'skills_plugins']` (2/2)
- Opus label-set votes:
  - `['hooks', 'skills_plugins']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-49042

- Title: Plugins: expose structured finalLlmOutcome on agent_end
- GitHub: https://github.com/openclaw/openclaw/pull/49042
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['api_surface', 'hooks', 'skills_plugins']` (2/3)
- GPT label-set votes:
  - `['api_surface', 'hooks', 'skills_plugins']`: 2
  - `['hooks', 'security', 'skills_plugins']`: 1
- Opus modal: `['hooks', 'skills_plugins']` (2/2)
- Opus label-set votes:
  - `['hooks', 'skills_plugins']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-84805

- Title: fix(cron): only apply Google preview model normalization for Google providers
- GitHub: https://github.com/openclaw/openclaw/pull/84805
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'cron_automation', 'inference_api']` (3/3)
- GPT label-set votes:
  - `['config', 'cron_automation', 'inference_api']`: 3
- Opus modal: `['config', 'model_lifecycle']` (1/2)
- Opus label-set votes:
  - `['config', 'model_lifecycle']`: 1
  - `['inference_api', 'model_lifecycle']`: 1
- Modal Jaccard: 0.250
- Legacy v5: `[]`

### openclaw-openclaw-84784

- Title: fix(cron): move persist() outside locked section in prepareManualRun
- GitHub: https://github.com/openclaw/openclaw/pull/84784
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['cron_automation', 'queueing', 'reliability']` (3/3)
- GPT label-set votes:
  - `['cron_automation', 'queueing', 'reliability']`: 3
- Opus modal: `['cron_automation', 'reliability']` (2/2)
- Opus label-set votes:
  - `['cron_automation', 'reliability']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-84803

- Title: WhatsApp group history drops media from unmentioned messages before later mention
- GitHub: https://github.com/openclaw/openclaw/issues/84803
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['chat_integrations', 'reliability', 'security']` (3/3)
- GPT label-set votes:
  - `['chat_integrations', 'reliability', 'security']`: 3
- Opus modal: `['chat_integrations', 'security']` (1/2)
- Opus label-set votes:
  - `['chat_integrations', 'security']`: 1
  - `['chat_integrations', 'reliability']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-84808

- Title: Bug: Control UI '立即更新' (Update Now) button does nothing when clicked
- GitHub: https://github.com/openclaw/openclaw/issues/84808
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['packaging_deployment', 'ui_tui']` (2/3)
- GPT label-set votes:
  - `['gateway', 'packaging_deployment', 'ui_tui']`: 1
  - `['packaging_deployment', 'ui_tui']`: 2
- Opus modal: `['ui_tui']` (2/2)
- Opus label-set votes:
  - `['ui_tui']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-84762

- Title: fix #84745: scope Google preview model normalization to Google providers only
- GitHub: https://github.com/openclaw/openclaw/pull/84762
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'inference_api']` (2/3)
- GPT label-set votes:
  - `['config', 'inference_api']`: 2
  - `['config', 'inference_api', 'model_lifecycle']`: 1
- Opus modal: `['config', 'model_lifecycle']` (2/2)
- Opus label-set votes:
  - `['config', 'model_lifecycle']`: 2
- Modal Jaccard: 0.333
- Legacy v5: `[]`

### openclaw-openclaw-70529

- Title: [Bug]: Desktop cannot use existing Chrome sessions: EasyClaw Google sign-in fails, and user profile attach fails with spawn npx ENOENT
- GitHub: https://github.com/openclaw/openclaw/issues/70529
- Reasons: gpt_flagged_human_review, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['auth_identity', 'browser_automation', 'mcp_tooling', 'packaging_deployment']` (3/3)
- GPT label-set votes:
  - `['auth_identity', 'browser_automation', 'mcp_tooling', 'packaging_deployment']`: 3
- Opus modal: `['browser_automation', 'packaging_deployment']` (1/2)
- Opus label-set votes:
  - `['browser_automation', 'packaging_deployment']`: 1
  - `['browser_automation', 'mcp_tooling', 'packaging_deployment']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `['auth_identity', 'browser_automation', 'exec_tools', 'packaging_deployment']`

### openclaw-openclaw-71469

- Title: fix(google): print Gemini OAuth URL before browser launch
- GitHub: https://github.com/openclaw/openclaw/pull/71469
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['browser_automation', 'inference_api', 'reliability']` (2/3)
- GPT label-set votes:
  - `['browser_automation', 'inference_api', 'reliability']`: 2
  - `['browser_automation', 'inference_api']`: 1
- Opus modal: `['inference_api', 'reliability']` (2/2)
- Opus label-set votes:
  - `['inference_api', 'reliability']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-84781

- Title: fix(simple-completion): sanitize Google thinking payload for unknown Gemini aliases (fixes #84688)
- GitHub: https://github.com/openclaw/openclaw/pull/84781
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['inference_api', 'security']` (3/3)
- GPT label-set votes:
  - `['inference_api', 'security']`: 3
- Opus modal: `['inference_api']` (2/2)
- Opus label-set votes:
  - `['inference_api']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-84722

- Title: Handle concurrent launchd bootstrap restart race
- GitHub: https://github.com/openclaw/openclaw/pull/84722
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['gateway', 'packaging_deployment', 'reliability']` (3/3)
- GPT label-set votes:
  - `['gateway', 'packaging_deployment', 'reliability']`: 3
- Opus modal: `['gateway', 'reliability']` (2/2)
- Opus label-set votes:
  - `['gateway', 'reliability']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-84721

- Title: [Bug]: Gateway restart can fail during concurrent launchd bootstrap even when service starts
- GitHub: https://github.com/openclaw/openclaw/issues/84721
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['gateway', 'packaging_deployment', 'reliability']` (3/3)
- GPT label-set votes:
  - `['gateway', 'packaging_deployment', 'reliability']`: 3
- Opus modal: `['gateway', 'reliability']` (1/2)
- Opus label-set votes:
  - `['gateway', 'reliability']`: 1
  - `['gateway', 'packaging_deployment', 'reliability']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-48942

- Title: test(gateway): consolidate deriveSessionTitle tests into dedicated module
- GitHub: https://github.com/openclaw/openclaw/pull/48942
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['gateway', 'sessions']` (3/3)
- GPT label-set votes:
  - `['gateway', 'sessions']`: 3
- Opus modal: `['sessions']` (2/2)
- Opus label-set votes:
  - `['sessions']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-84418

- Title: test(cron): document and test owner-only tool security boundary for isolated cron
- GitHub: https://github.com/openclaw/openclaw/pull/84418
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['cron_automation', 'security', 'tests_ci']` (2/3)
- GPT label-set votes:
  - `['cron_automation', 'security', 'tests_ci']`: 2
  - `['cron_automation', 'security']`: 1
- Opus modal: `['cron_automation', 'security']` (1/2)
- Opus label-set votes:
  - `['cron_automation', 'security']`: 1
  - `['cron_automation', 'security', 'tests_ci']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `['cron_automation', 'security', 'tests_ci']`

### openclaw-openclaw-84796

- Title: Windows native: Health check fails with ERR_MODULE_NOT_FOUND for task-registry.maintenance
- GitHub: https://github.com/openclaw/openclaw/issues/84796
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['packaging_deployment', 'reliability']` (3/3)
- GPT label-set votes:
  - `['packaging_deployment', 'reliability']`: 3
- Opus modal: `['packaging_deployment']` (2/2)
- Opus label-set votes:
  - `['packaging_deployment']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-84778

- Title: /steer command doesn't actually inject into active run — queues for next turn instead
- GitHub: https://github.com/openclaw/openclaw/issues/84778
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['agent_runtime', 'codex', 'queueing']` (1/3)
- GPT label-set votes:
  - `['agent_runtime', 'codex', 'queueing']`: 1
  - `['agent_runtime', 'queueing', 'ui_tui']`: 1
  - `['agent_runtime', 'queueing']`: 1
- Opus modal: `['agent_runtime', 'queueing']` (2/2)
- Opus label-set votes:
  - `['agent_runtime', 'queueing']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-60551

- Title: Strip leaked reasoning preambles before outbound send
- GitHub: https://github.com/openclaw/openclaw/pull/60551
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['notifications']` (2/3)
- GPT label-set votes:
  - `['notifications']`: 2
  - `['agent_runtime', 'notifications']`: 1
- Opus modal: `['agent_runtime']` (1/2)
- Opus label-set votes:
  - `['agent_runtime']`: 1
  - `['agent_runtime', 'notifications']`: 1
- Modal Jaccard: 0.000
- Legacy v5: `[]`
