# V6 batch consensus review

- Batch: `batch-002`
- Rows: 30
- Accepted consensus: 5
- Deferred/review: 25
- GPT/Opus exact modal matches: 8
- Exact modal matches with 5 labels: 1
- Rows where either teacher hit the 5-label cap: 7
- Mean GPT/Opus modal Jaccard: 0.739

## Review rows

### openclaw-openclaw-10467

- Title: [Feature Request]: Multi-lane concurrency support for sub-agents via sessions_spawn
- GitHub: https://github.com/openclaw/openclaw/issues/10467
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['agent_runtime', 'config', 'queueing', 'tool_calling']` (3/3)
- GPT label-set votes:
  - `['agent_runtime', 'config', 'queueing', 'tool_calling']`: 3
- Opus modal: `['agent_runtime', 'config', 'queueing']` (2/2)
- Opus label-set votes:
  - `['agent_runtime', 'config', 'queueing']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['coding_agents', 'sessions', 'queueing', 'config']`

### openclaw-openclaw-39248

- Title: Bug: sandbox.mode: "non-main" silently breaks sessions_spawn subagent initialization
- GitHub: https://github.com/openclaw/openclaw/issues/39248
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['agent_runtime', 'reliability', 'sandboxing', 'sessions']` (3/3)
- GPT label-set votes:
  - `['agent_runtime', 'reliability', 'sandboxing', 'sessions']`: 3
- Opus modal: `['agent_runtime', 'reliability', 'sandboxing']` (2/2)
- Opus label-set votes:
  - `['agent_runtime', 'reliability', 'sandboxing']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['agent_runtime', 'sessions', 'sandboxing', 'reliability']`

### openclaw-openclaw-39714

- Title: Sandbox: fix Dockerized browser bridge and tab creation
- GitHub: https://github.com/openclaw/openclaw/pull/39714
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['browser_automation', 'config', 'sandboxing', 'security']` (1/3)
- GPT label-set votes:
  - `['browser_automation', 'config', 'sandboxing', 'security']`: 1
  - `['browser_automation', 'config', 'reliability', 'sandboxing', 'security']`: 1
  - `['browser_automation', 'config', 'sandboxing']`: 1
- Opus modal: `['browser_automation', 'config', 'sandboxing']` (2/2)
- Opus label-set votes:
  - `['browser_automation', 'config', 'sandboxing']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['sandboxing', 'browser_automation', 'reliability']`

### openclaw-openclaw-40332

- Title: [Feature]: Per-binding and per-agent permissionMode for ACP sessions
- GitHub: https://github.com/openclaw/openclaw/issues/40332
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acp', 'acpx', 'approvals', 'config', 'security']` (3/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'approvals', 'config', 'security']`: 3
- Opus modal: `['acp', 'acpx', 'approvals', 'config']` (2/2)
- Opus label-set votes:
  - `['acp', 'acpx', 'approvals', 'config']`: 2
- Modal Jaccard: 0.800
- Legacy v5: `['acp', 'acpx', 'approvals', 'config', 'security']`

### openclaw-openclaw-42606

- Title: Browser: harden noVNC bootstrap headers
- GitHub: https://github.com/openclaw/openclaw/pull/42606
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['api_surface', 'browser_automation', 'security']` (2/3)
- GPT label-set votes:
  - `['api_surface', 'browser_automation', 'security']`: 2
  - `['browser_automation', 'security']`: 1
- Opus modal: `['browser_automation', 'security']` (2/2)
- Opus label-set votes:
  - `['browser_automation', 'security']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['api_surface', 'browser_automation', 'security']`

### openclaw-openclaw-43564

- Title: [Feature Request] ACP Session Skill Context Injection
- GitHub: https://github.com/openclaw/openclaw/issues/43564
- Reasons: gpt_unstable, gpt_flagged_human_review, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'coding_agent_integrations', 'security', 'skills_plugins']` (2/3)
- GPT label-set votes:
  - `['acp', 'coding_agent_integrations', 'security', 'skills_plugins']`: 2
  - `['acp', 'security', 'sessions', 'skills_plugins']`: 1
- Opus modal: `['acp', 'skills_plugins']` (1/2)
- Opus label-set votes:
  - `['acp', 'skills_plugins']`: 1
  - `['acp', 'coding_agent_integrations', 'skills_plugins']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `['acp', 'sessions', 'skills_plugins', 'security']`

### openclaw-openclaw-43765

- Title: Improve runtime recovery for heartbeat, Feishu, and exec sessions
- GitHub: https://github.com/openclaw/openclaw/pull/43765
- Reasons: opus_flagged_human_review
- GPT modal: `['chat_integrations', 'cron_automation', 'exec_tools', 'gateway', 'reliability']` (3/3)
- GPT label-set votes:
  - `['chat_integrations', 'cron_automation', 'exec_tools', 'gateway', 'reliability']`: 3
- Opus modal: `['chat_integrations', 'cron_automation', 'exec_tools', 'gateway', 'reliability']` (2/2)
- Opus label-set votes:
  - `['chat_integrations', 'cron_automation', 'exec_tools', 'gateway', 'reliability']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `['chat_integrations', 'cron_automation', 'exec_tools', 'gateway', 'reliability']`

### openclaw-openclaw-44202

- Title: [Bug]: local memory embeddings on Apple Silicon can crash gateway in ggml-metal / node-llama-cpp; need official Metal/GPU guidance
- GitHub: https://github.com/openclaw/openclaw/issues/44202
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['gateway', 'local_models', 'memory', 'reliability', 'self_hosted_inference']` (2/3)
- GPT label-set votes:
  - `['gateway', 'local_models', 'memory', 'reliability', 'self_hosted_inference']`: 2
  - `['gateway', 'memory', 'reliability', 'self_hosted_inference']`: 1
- Opus modal: `['memory', 'reliability', 'self_hosted_inference']` (1/2)
- Opus label-set votes:
  - `['memory', 'reliability', 'self_hosted_inference']`: 1
  - `['local_models', 'memory', 'reliability', 'self_hosted_inference']`: 1
- Modal Jaccard: 0.600
- Legacy v5: `['local_models', 'self_hosted_inference', 'memory', 'reliability']`

### openclaw-openclaw-44379

- Title: fix(pi-runner): harden context-overflow recovery with one suppress-hook retry
- GitHub: https://github.com/openclaw/openclaw/pull/44379
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['coding_agent_integrations', 'hooks', 'reliability']` (3/3)
- GPT label-set votes:
  - `['coding_agent_integrations', 'hooks', 'reliability']`: 3
- Opus modal: `['agent_runtime', 'reliability']` (2/2)
- Opus label-set votes:
  - `['agent_runtime', 'reliability']`: 2
- Modal Jaccard: 0.250
- Legacy v5: `['agent_runtime', 'hooks', 'memory', 'reliability']`

### openclaw-openclaw-45393

- Title: fix(errors): friendly message and last-message repair for tool_use/tool_result mismatch (#45385)
- GitHub: https://github.com/openclaw/openclaw/pull/45393
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['inference_api', 'security', 'tool_calling']` (1/3)
- GPT label-set votes:
  - `['inference_api', 'security', 'tool_calling']`: 1
  - `['security', 'tool_calling']`: 1
  - `['inference_api', 'security', 'sessions', 'tool_calling']`: 1
- Opus modal: `['security', 'tool_calling']` (2/2)
- Opus label-set votes:
  - `['security', 'tool_calling']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['tool_calling', 'reliability', 'sessions', 'security']`

### openclaw-openclaw-45508

- Title: [Feature]: Self-hosted STT/TTS provider support in webchat (Route webchat TTS through the gateway instead of browser Speech API)
- GitHub: https://github.com/openclaw/openclaw/issues/45508
- Reasons: gpt_unstable, opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['chat_integrations', 'config', 'gateway', 'inference_api', 'self_hosted_inference']` (2/3)
- GPT label-set votes:
  - `['chat_integrations', 'config', 'inference_api']`: 1
  - `['chat_integrations', 'config', 'gateway', 'inference_api', 'self_hosted_inference']`: 2
- Opus modal: `['chat_integrations', 'config', 'gateway', 'inference_api']` (2/2)
- Opus label-set votes:
  - `['chat_integrations', 'config', 'gateway', 'inference_api']`: 2
- Modal Jaccard: 0.800
- Legacy v5: `['self_hosted_inference', 'chat_integrations', 'gateway', 'config']`

### openclaw-openclaw-47446

- Title: fix(gateway/discord): respect env proxy vars and prevent ECONNRESET
- GitHub: https://github.com/openclaw/openclaw/pull/47446
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['chat_integrations', 'config', 'gateway', 'reliability']` (3/3)
- GPT label-set votes:
  - `['chat_integrations', 'config', 'gateway', 'reliability']`: 3
- Opus modal: `['chat_integrations', 'gateway', 'reliability']` (2/2)
- Opus label-set votes:
  - `['chat_integrations', 'gateway', 'reliability']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['chat_integrations', 'config', 'gateway', 'reliability']`

### openclaw-openclaw-48406

- Title: Docs: add saturated session recovery guide
- GitHub: https://github.com/openclaw/openclaw/pull/48406
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'docs', 'reliability', 'sessions']` (3/3)
- GPT label-set votes:
  - `['config', 'docs', 'reliability', 'sessions']`: 3
- Opus modal: `['docs', 'reliability', 'sessions']` (1/2)
- Opus label-set votes:
  - `['docs', 'reliability', 'sessions']`: 1
  - `['agent_runtime', 'docs', 'reliability']`: 1
- Modal Jaccard: 0.750
- Legacy v5: `['docs', 'memory', 'sessions']`

### openclaw-openclaw-48580

- Title: Bug: acpx codex sessions 创建的会话立即退出 - stdin is not a terminal
- GitHub: https://github.com/openclaw/openclaw/issues/48580
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']` (3/3)
- GPT label-set votes:
  - `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']`: 3
- Opus modal: `['acpx', 'codex', 'reliability', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acpx', 'codex', 'reliability', 'sessions']`: 2
- Modal Jaccard: 0.800
- Legacy v5: `['acpx', 'codex', 'sessions', 'reliability']`

### openclaw-openclaw-48851

- Title: feat(status): add API call count to session status and usage footer
- GitHub: https://github.com/openclaw/openclaw/pull/48851
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['sessions', 'telemetry_usage', 'ui_tui']` (3/3)
- GPT label-set votes:
  - `['sessions', 'telemetry_usage', 'ui_tui']`: 3
- Opus modal: `['telemetry_usage', 'ui_tui']` (1/2)
- Opus label-set votes:
  - `['telemetry_usage', 'ui_tui']`: 1
  - `['sessions', 'telemetry_usage']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `['sessions', 'telemetry_usage', 'ui_tui']`

### openclaw-openclaw-51654

- Title: Support session-level environment variables for ACP sessions
- GitHub: https://github.com/openclaw/openclaw/issues/51654
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'acpx', 'api_surface', 'security', 'sessions']` (1/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'api_surface', 'security', 'sessions']`: 1
  - `['acp', 'acpx', 'security', 'sessions', 'tool_calling']`: 1
  - `['acp', 'acpx', 'config', 'security', 'sessions']`: 1
- Opus modal: `['acp', 'acpx', 'security', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acp', 'acpx', 'security', 'sessions']`: 2
- Modal Jaccard: 0.800
- Legacy v5: `['acp', 'acpx', 'sessions', 'security']`

### openclaw-openclaw-51667

- Title: Feature: Native Audio Input for Omni-Modal Models (skip STT transcription)
- GitHub: https://github.com/openclaw/openclaw/issues/51667
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['config', 'inference_api', 'sessions']` (3/3)
- GPT label-set votes:
  - `['config', 'inference_api', 'sessions']`: 3
- Opus modal: `['config', 'inference_api']` (2/2)
- Opus label-set votes:
  - `['config', 'inference_api']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['chat_integrations', 'config', 'model_serving', 'sessions']`

### openclaw-openclaw-54471

- Title: fix(acp): add system_event stream relay to parent session for ACP spawn
- GitHub: https://github.com/openclaw/openclaw/pull/54471
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'sessions']` (2/3)
- GPT label-set votes:
  - `['acp', 'sessions']`: 2
  - `['acp']`: 1
- Opus modal: `['acp', 'notifications']` (2/2)
- Opus label-set votes:
  - `['acp', 'notifications']`: 2
- Modal Jaccard: 0.333
- Legacy v5: `['acp', 'sessions', 'notifications']`

### openclaw-openclaw-56442

- Title: feat: Add opt-in ACP parent completion notify for sessions_spawn
- GitHub: https://github.com/openclaw/openclaw/pull/56442
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'api_surface', 'notifications', 'sessions']` (2/3)
- GPT label-set votes:
  - `['acp', 'api_surface', 'notifications', 'sessions']`: 2
  - `['acp', 'notifications', 'sessions', 'tool_calling']`: 1
- Opus modal: `['acp', 'notifications']` (2/2)
- Opus label-set votes:
  - `['acp', 'notifications']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `['acp', 'sessions', 'notifications', 'api_surface']`

### openclaw-openclaw-56532

- Title: memory-lancedb: add configurable timeout/retry for embedding calls
- GitHub: https://github.com/openclaw/openclaw/pull/56532
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'inference_api', 'memory', 'reliability', 'skills_plugins']` (3/3)
- GPT label-set votes:
  - `['config', 'inference_api', 'memory', 'reliability', 'skills_plugins']`: 3
- Opus modal: `['config', 'inference_api', 'memory', 'reliability']` (1/2)
- Opus label-set votes:
  - `['config', 'inference_api', 'memory', 'reliability']`: 1
  - `['config', 'memory', 'reliability']`: 1
- Modal Jaccard: 0.800
- Legacy v5: `['memory', 'config', 'reliability']`

### openclaw-openclaw-58135

- Title: [Feature]: expose promptMode parameter in sessions_spawn for deterministic blank sub-agents
- GitHub: https://github.com/openclaw/openclaw/issues/58135
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['agent_runtime', 'sessions', 'tool_calling']` (3/3)
- GPT label-set votes:
  - `['agent_runtime', 'sessions', 'tool_calling']`: 3
- Opus modal: `['agent_runtime']` (2/2)
- Opus label-set votes:
  - `['agent_runtime']`: 2
- Modal Jaccard: 0.333
- Legacy v5: `['acp', 'api_surface', 'coding_agents', 'sessions']`

### openclaw-openclaw-59208

- Title: fix(status): honor selected usage auth profile
- GitHub: https://github.com/openclaw/openclaw/pull/59208
- Reasons: gpt_unstable
- GPT modal: `['auth_identity', 'telemetry_usage']` (2/3)
- GPT label-set votes:
  - `['auth_identity', 'telemetry_usage']`: 2
  - `['auth_identity', 'security', 'telemetry_usage']`: 1
- Opus modal: `['auth_identity', 'telemetry_usage']` (2/2)
- Opus label-set votes:
  - `['auth_identity', 'telemetry_usage']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `['auth_identity', 'telemetry_usage', 'ui_tui']`

### openclaw-openclaw-60381

- Title: browser tool: add force parameter for click and expose evaluate action
- GitHub: https://github.com/openclaw/openclaw/issues/60381
- Reasons: gpt_unstable
- GPT modal: `['browser_automation']` (2/3)
- GPT label-set votes:
  - `['browser_automation']`: 2
  - `['browser_automation', 'tool_calling']`: 1
- Opus modal: `['browser_automation']` (2/2)
- Opus label-set votes:
  - `['browser_automation']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `['browser_automation', 'api_surface', 'security']`

### openclaw-openclaw-60737

- Title: [Feature]: Per-DM/per-chat default ACP binding for auto-spawning ACP sessions on new topics
- GitHub: https://github.com/openclaw/openclaw/issues/60737
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acp', 'chat_integrations', 'config', 'sessions']` (3/3)
- GPT label-set votes:
  - `['acp', 'chat_integrations', 'config', 'sessions']`: 3
- Opus modal: `['acp', 'chat_integrations', 'config']` (2/2)
- Opus label-set votes:
  - `['acp', 'chat_integrations', 'config']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['acp', 'chat_integrations', 'config', 'sessions']`

### openclaw-openclaw-61775

- Title: enhance Makefile with standard build, test, and quality targets
- GitHub: https://github.com/openclaw/openclaw/pull/61775
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['packaging_deployment', 'tests_ci']` (3/3)
- GPT label-set votes:
  - `['packaging_deployment', 'tests_ci']`: 3
- Opus modal: `['packaging_deployment']` (2/2)
- Opus label-set votes:
  - `['packaging_deployment']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `['packaging_deployment', 'tests_ci']`
