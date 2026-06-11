# V6 batch consensus review

- Batch: `batch-002`
- Rows: 30
- Accepted consensus: 6
- Deferred/review: 24
- GPT/Opus exact modal matches: 9
- Exact modal matches with 5 labels: 3
- Rows where either teacher hit the 5-label cap: 11
- Mean GPT/Opus modal Jaccard: 0.756

## Review rows

### openclaw-openclaw-10467

- Title: [Feature Request]: Multi-lane concurrency support for sub-agents via sessions_spawn
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['coding_agents', 'config', 'queueing', 'reliability', 'tool_calling']` (2/3)
- GPT label-set votes:
  - `['coding_agents', 'config', 'queueing', 'reliability', 'tool_calling']`: 2
  - `['coding_agents', 'config', 'queueing', 'tool_calling']`: 1
- Opus modal: `['coding_agents', 'config', 'queueing']` (2/2)
- Opus label-set votes:
  - `['coding_agents', 'config', 'queueing']`: 2
- Modal Jaccard: 0.600
- Legacy v5: `['coding_agents', 'sessions', 'queueing', 'config']`

### openclaw-openclaw-39248

- Title: Bug: sandbox.mode: "non-main" silently breaks sessions_spawn subagent initialization
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['coding_agents', 'config', 'reliability', 'sandboxing', 'sessions']` (2/3)
- GPT label-set votes:
  - `['coding_agents', 'reliability', 'sandboxing', 'sessions']`: 1
  - `['coding_agents', 'config', 'reliability', 'sandboxing', 'sessions']`: 2
- Opus modal: `['coding_agents', 'reliability', 'sandboxing', 'sessions']` (2/2)
- Opus label-set votes:
  - `['coding_agents', 'reliability', 'sandboxing', 'sessions']`: 2
- Modal Jaccard: 0.800
- Legacy v5: `['agent_runtime', 'sessions', 'sandboxing', 'reliability']`

### openclaw-openclaw-39714

- Title: Sandbox: fix Dockerized browser bridge and tab creation
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['browser_automation', 'coding_agents', 'config', 'sandboxing']` (3/3)
- GPT label-set votes:
  - `['browser_automation', 'coding_agents', 'config', 'sandboxing']`: 3
- Opus modal: `['browser_automation', 'config', 'sandboxing']` (2/2)
- Opus label-set votes:
  - `['browser_automation', 'config', 'sandboxing']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['sandboxing', 'browser_automation', 'reliability']`

### openclaw-openclaw-40332

- Title: [Feature]: Per-binding and per-agent permissionMode for ACP sessions
- Reasons: opus_unstable
- GPT modal: `['acp', 'acpx', 'approvals', 'config', 'security']` (3/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'approvals', 'config', 'security']`: 3
- Opus modal: `['acp', 'acpx', 'approvals', 'config', 'security']` (1/2)
- Opus label-set votes:
  - `['acp', 'acpx', 'approvals', 'config', 'security']`: 1
  - `['acp', 'acpx', 'approvals', 'config']`: 1
- Modal Jaccard: 1.000
- Legacy v5: `['acp', 'acpx', 'approvals', 'config', 'security']`

### openclaw-openclaw-42606

- Title: Browser: harden noVNC bootstrap headers
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['api_surface', 'browser_automation', 'security']` (3/3)
- GPT label-set votes:
  - `['api_surface', 'browser_automation', 'security']`: 3
- Opus modal: `['browser_automation', 'security']` (2/2)
- Opus label-set votes:
  - `['browser_automation', 'security']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['api_surface', 'browser_automation', 'security']`

### openclaw-openclaw-43564

- Title: [Feature Request] ACP Session Skill Context Injection
- Reasons: gpt_unstable, opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'api_surface', 'coding_agents', 'sessions', 'skills_plugins']` (2/3)
- GPT label-set votes:
  - `['acp', 'api_surface', 'coding_agents', 'sessions', 'skills_plugins']`: 2
  - `['acp', 'api_surface', 'coding_agents', 'security', 'skills_plugins']`: 1
- Opus modal: `['acp', 'coding_agents', 'skills_plugins']` (2/2)
- Opus label-set votes:
  - `['acp', 'coding_agents', 'skills_plugins']`: 2
- Modal Jaccard: 0.600
- Legacy v5: `['acp', 'sessions', 'skills_plugins', 'security']`

### openclaw-openclaw-43765

- Title: Improve runtime recovery for heartbeat, Feishu, and exec sessions
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
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['gateway', 'memory', 'reliability', 'self_hosted_inference']` (3/3)
- GPT label-set votes:
  - `['gateway', 'memory', 'reliability', 'self_hosted_inference']`: 3
- Opus modal: `['memory', 'reliability', 'self_hosted_inference']` (1/2)
- Opus label-set votes:
  - `['memory', 'reliability', 'self_hosted_inference']`: 1
  - `['local_models', 'memory', 'reliability', 'self_hosted_inference']`: 1
- Modal Jaccard: 0.750
- Legacy v5: `['local_models', 'self_hosted_inference', 'memory', 'reliability']`

### openclaw-openclaw-44379

- Title: fix(pi-runner): harden context-overflow recovery with one suppress-hook retry
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['coding_agents', 'hooks', 'reliability']` (2/3)
- GPT label-set votes:
  - `['agent_runtime', 'coding_agents', 'hooks', 'reliability']`: 1
  - `['coding_agents', 'hooks', 'reliability']`: 2
- Opus modal: `['agent_runtime', 'coding_agents', 'reliability']` (2/2)
- Opus label-set votes:
  - `['agent_runtime', 'coding_agents', 'reliability']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `['agent_runtime', 'hooks', 'memory', 'reliability']`

### openclaw-openclaw-45393

- Title: fix(errors): friendly message and last-message repair for tool_use/tool_result mismatch (#45385)
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['inference_api', 'security', 'sessions', 'tool_calling']` (1/3)
- GPT label-set votes:
  - `['inference_api', 'security', 'sessions', 'tool_calling']`: 1
  - `['inference_api', 'reliability', 'security', 'tool_calling']`: 1
  - `['coding_agents', 'inference_api', 'security', 'tool_calling']`: 1
- Opus modal: `['security', 'tool_calling']` (1/2)
- Opus label-set votes:
  - `['security', 'tool_calling']`: 1
  - `['reliability', 'security', 'tool_calling']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `['tool_calling', 'reliability', 'sessions', 'security']`

### openclaw-openclaw-45508

- Title: [Feature]: Self-hosted STT/TTS provider support in webchat (Route webchat TTS through the gateway instead of browser Speech API)
- Reasons: opus_unstable, opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['chat_integrations', 'config', 'gateway', 'inference_api', 'self_hosted_inference']` (3/3)
- GPT label-set votes:
  - `['chat_integrations', 'config', 'gateway', 'inference_api', 'self_hosted_inference']`: 3
- Opus modal: `['config', 'inference_api', 'self_hosted_inference', 'ui_tui']` (1/2)
- Opus label-set votes:
  - `['config', 'inference_api', 'self_hosted_inference', 'ui_tui']`: 1
  - `['chat_integrations', 'config', 'gateway', 'inference_api', 'self_hosted_inference']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `['self_hosted_inference', 'chat_integrations', 'gateway', 'config']`

### openclaw-openclaw-47446

- Title: fix(gateway/discord): respect env proxy vars and prevent ECONNRESET
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
- Reasons: opus_unstable, opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['coding_agents', 'config', 'docs', 'reliability', 'sessions']` (3/3)
- GPT label-set votes:
  - `['coding_agents', 'config', 'docs', 'reliability', 'sessions']`: 3
- Opus modal: `['coding_agents', 'docs', 'reliability', 'sessions']` (1/2)
- Opus label-set votes:
  - `['coding_agents', 'docs', 'reliability', 'sessions']`: 1
  - `['coding_agents', 'config', 'docs', 'reliability', 'sessions']`: 1
- Modal Jaccard: 0.800
- Legacy v5: `['docs', 'memory', 'sessions']`

### openclaw-openclaw-48580

- Title: Bug: acpx codex sessions 创建的会话立即退出 - stdin is not a terminal
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acpx', 'codex', 'coding_agents', 'reliability', 'sessions']` (3/3)
- GPT label-set votes:
  - `['acpx', 'codex', 'coding_agents', 'reliability', 'sessions']`: 3
- Opus modal: `['acpx', 'codex', 'reliability', 'sessions']` (2/2)
- Opus label-set votes:
  - `['acpx', 'codex', 'reliability', 'sessions']`: 2
- Modal Jaccard: 0.800
- Legacy v5: `['acpx', 'codex', 'sessions', 'reliability']`

### openclaw-openclaw-51654

- Title: Support session-level environment variables for ACP sessions
- Reasons: gpt_unstable, opus_unstable
- GPT modal: `['acp', 'acpx', 'auth_identity', 'security', 'sessions']` (2/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'auth_identity', 'security', 'sessions']`: 2
  - `['acp', 'acpx', 'api_surface', 'security', 'sessions']`: 1
- Opus modal: `['acp', 'acpx', 'auth_identity', 'security', 'sessions']` (1/2)
- Opus label-set votes:
  - `['acp', 'acpx', 'auth_identity', 'security', 'sessions']`: 1
  - `['acp', 'acpx', 'security', 'sessions']`: 1
- Modal Jaccard: 1.000
- Legacy v5: `['acp', 'acpx', 'sessions', 'security']`

### openclaw-openclaw-51667

- Title: Feature: Native Audio Input for Omni-Modal Models (skip STT transcription)
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['chat_integrations', 'config', 'inference_api', 'sessions']` (2/3)
- GPT label-set votes:
  - `['chat_integrations', 'config', 'inference_api', 'sessions']`: 2
  - `['config', 'inference_api', 'sessions']`: 1
- Opus modal: `['config', 'inference_api']` (1/2)
- Opus label-set votes:
  - `['config', 'inference_api']`: 1
  - `['chat_integrations', 'config', 'inference_api']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `['chat_integrations', 'config', 'model_serving', 'sessions']`

### openclaw-openclaw-54471

- Title: fix(acp): add system_event stream relay to parent session for ACP spawn
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'sessions']` (2/3)
- GPT label-set votes:
  - `['acp', 'sessions']`: 2
  - `['acp', 'coding_agents', 'sessions']`: 1
- Opus modal: `['acp', 'notifications', 'sessions']` (1/2)
- Opus label-set votes:
  - `['acp', 'notifications', 'sessions']`: 1
  - `['acp', 'notifications']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `['acp', 'sessions', 'notifications']`

### openclaw-openclaw-56442

- Title: feat: Add opt-in ACP parent completion notify for sessions_spawn
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'api_surface', 'coding_agents', 'notifications', 'sessions']` (2/3)
- GPT label-set votes:
  - `['acp', 'api_surface', 'coding_agents', 'notifications', 'sessions']`: 2
  - `['acp', 'coding_agents', 'notifications', 'sessions', 'tool_calling']`: 1
- Opus modal: `['acp', 'coding_agents', 'notifications']` (1/2)
- Opus label-set votes:
  - `['acp', 'coding_agents', 'notifications']`: 1
  - `['acp', 'coding_agents', 'notifications', 'sessions']`: 1
- Modal Jaccard: 0.600
- Legacy v5: `['acp', 'sessions', 'notifications', 'api_surface']`

### openclaw-openclaw-56532

- Title: memory-lancedb: add configurable timeout/retry for embedding calls
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['config', 'inference_api', 'memory', 'reliability', 'skills_plugins']` (3/3)
- GPT label-set votes:
  - `['config', 'inference_api', 'memory', 'reliability', 'skills_plugins']`: 3
- Opus modal: `['config', 'inference_api', 'memory', 'reliability']` (2/2)
- Opus label-set votes:
  - `['config', 'inference_api', 'memory', 'reliability']`: 2
- Modal Jaccard: 0.800
- Legacy v5: `['memory', 'config', 'reliability']`

### openclaw-openclaw-58135

- Title: [Feature]: expose promptMode parameter in sessions_spawn for deterministic blank sub-agents
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['api_surface', 'coding_agents', 'sessions']` (2/3)
- GPT label-set votes:
  - `['api_surface', 'coding_agents', 'sessions']`: 2
  - `['coding_agents', 'sessions', 'tool_calling']`: 1
- Opus modal: `['coding_agents', 'sessions']` (2/2)
- Opus label-set votes:
  - `['coding_agents', 'sessions']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['acp', 'api_surface', 'coding_agents', 'sessions']`

### openclaw-openclaw-59208

- Title: fix(status): honor selected usage auth profile
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['auth_identity', 'telemetry_usage', 'ui_tui']` (2/3)
- GPT label-set votes:
  - `['auth_identity', 'telemetry_usage', 'ui_tui']`: 2
  - `['auth_identity', 'security', 'telemetry_usage']`: 1
- Opus modal: `['auth_identity', 'telemetry_usage']` (2/2)
- Opus label-set votes:
  - `['auth_identity', 'telemetry_usage']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['auth_identity', 'telemetry_usage', 'ui_tui']`

### openclaw-openclaw-60381

- Title: browser tool: add force parameter for click and expose evaluate action
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['browser_automation', 'tool_calling']` (2/3)
- GPT label-set votes:
  - `['browser_automation', 'security', 'tool_calling']`: 1
  - `['browser_automation', 'tool_calling']`: 2
- Opus modal: `['browser_automation']` (2/2)
- Opus label-set votes:
  - `['browser_automation']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `['browser_automation', 'api_surface', 'security']`

### openclaw-openclaw-60737

- Title: [Feature]: Per-DM/per-chat default ACP binding for auto-spawning ACP sessions on new topics
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
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['packaging_deployment', 'tests_ci']` (3/3)
- GPT label-set votes:
  - `['packaging_deployment', 'tests_ci']`: 3
- Opus modal: `['packaging_deployment']` (2/2)
- Opus label-set votes:
  - `['packaging_deployment']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `['packaging_deployment', 'tests_ci']`
