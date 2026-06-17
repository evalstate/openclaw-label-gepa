# V6 batch consensus review

- Batch: `prompt-keyword-audit-40`
- Rows: 40
- Accepted consensus: 20
- Deferred/review: 20
- GPT/Opus exact modal matches: 23
- Exact modal matches with 5 labels: 1
- Rows where either teacher hit the 5-label cap: 3
- Mean GPT/Opus modal Jaccard: 0.845

## Review rows

### openclaw-openclaw-71487

- Title: Web UI: add a clear TTS toggle and default voice picker in Settings
- GitHub: https://github.com/openclaw/openclaw/issues/71487
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['config', 'inference_api', 'ui_tui']` (3/3)
- GPT label-set votes:
  - `['config', 'inference_api', 'ui_tui']`: 3
- Opus modal: `['config', 'ui_tui']` (2/2)
- Opus label-set votes:
  - `['config', 'ui_tui']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['ui_tui', 'self_hosted_inference', 'config']`

### openclaw-openclaw-71646

- Title: mcp/channel-bridge: pendingClaudePermissions / pendingApprovals leak — no TTL, no close-clear, no cap
- GitHub: https://github.com/openclaw/openclaw/issues/71646
- Reasons: opus_unstable
- GPT modal: `['approvals', 'mcp_tooling', 'reliability']` (3/3)
- GPT label-set votes:
  - `['approvals', 'mcp_tooling', 'reliability']`: 3
- Opus modal: `['approvals', 'mcp_tooling', 'reliability']` (1/2)
- Opus label-set votes:
  - `['approvals', 'mcp_tooling', 'reliability']`: 1
  - `['approvals', 'reliability']`: 1
- Modal Jaccard: 1.000
- Legacy v5: `['mcp_tooling', 'approvals', 'reliability']`

### openclaw-openclaw-43564

- Title: [Feature Request] ACP Session Skill Context Injection
- GitHub: https://github.com/openclaw/openclaw/issues/43564
- Reasons: gpt_unstable, opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'coding_agent_integrations', 'security', 'skills_plugins']` (2/3)
- GPT label-set votes:
  - `['acp', 'coding_agent_integrations', 'security', 'skills_plugins']`: 2
  - `['acp', 'api_surface', 'coding_agent_integrations', 'security', 'skills_plugins']`: 1
- Opus modal: `['acp', 'coding_agent_integrations', 'skills_plugins']` (2/2)
- Opus label-set votes:
  - `['acp', 'coding_agent_integrations', 'skills_plugins']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['acp', 'sessions', 'skills_plugins', 'security']`

### openclaw-openclaw-51654

- Title: Support session-level environment variables for ACP sessions
- GitHub: https://github.com/openclaw/openclaw/issues/51654
- Reasons: gpt_unstable, gpt_flagged_human_review, opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['acpx', 'api_surface', 'security', 'sessions']` (1/3)
- GPT label-set votes:
  - `['acpx', 'api_surface', 'security', 'sessions']`: 1
  - `['acp', 'acpx', 'security', 'sessions']`: 1
  - `['acp', 'acpx', 'api_surface', 'security', 'sessions']`: 1
- Opus modal: `['acp', 'acpx', 'security']` (2/2)
- Opus label-set votes:
  - `['acp', 'acpx', 'security']`: 2
- Modal Jaccard: 0.400
- Legacy v5: `['acp', 'acpx', 'sessions', 'security']`

### openclaw-openclaw-56442

- Title: feat: Add opt-in ACP parent completion notify for sessions_spawn
- GitHub: https://github.com/openclaw/openclaw/pull/56442
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acp', 'notifications', 'tool_calling']` (3/3)
- GPT label-set votes:
  - `['acp', 'notifications', 'tool_calling']`: 3
- Opus modal: `['acp', 'notifications']` (2/2)
- Opus label-set votes:
  - `['acp', 'notifications']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['acp', 'sessions', 'notifications', 'api_surface']`

### openclaw-openclaw-68204

- Title: Unified run trace schema across agent, ACP, subagent, and task flows
- GitHub: https://github.com/openclaw/openclaw/issues/68204
- Reasons: opus_unstable
- GPT modal: `['telemetry_usage']` (3/3)
- GPT label-set votes:
  - `['telemetry_usage']`: 3
- Opus modal: `['telemetry_usage']` (1/2)
- Opus label-set votes:
  - `['telemetry_usage']`: 1
  - `['acp', 'agent_runtime', 'telemetry_usage']`: 1
- Modal Jaccard: 1.000
- Legacy v5: `['acp', 'agent_runtime', 'sessions', 'telemetry_usage']`

### openclaw-openclaw-77694

- Title: [Bug]: acpx flow run ACP node outputs return empty strings instead of agent replies
- GitHub: https://github.com/openclaw/openclaw/issues/77694
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acpx']` (3/3)
- GPT label-set votes:
  - `['acpx']`: 3
- Opus modal: `['acp', 'acpx']` (2/2)
- Opus label-set votes:
  - `['acp', 'acpx']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `['acpx', 'acp', 'agent_runtime', 'reliability']`

### openclaw-openclaw-84740

- Title: Feature Request: Option to hide/suppress certain sessions from the session list
- GitHub: https://github.com/openclaw/openclaw/issues/84740
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['sessions', 'ui_tui']` (3/3)
- GPT label-set votes:
  - `['sessions', 'ui_tui']`: 3
- Opus modal: `['config', 'sessions', 'ui_tui']` (2/2)
- Opus label-set votes:
  - `['config', 'sessions', 'ui_tui']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['sessions', 'ui_tui']`

### openclaw-openclaw-84771

- Title: Event loop saturation during startup: synchronous model-prewarm and session-locks block event loop for 28-64 seconds
- GitHub: https://github.com/openclaw/openclaw/issues/84771
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['agent_runtime', 'reliability', 'sessions']` (1/3)
- GPT label-set votes:
  - `['agent_runtime', 'reliability', 'sessions']`: 1
  - `['agent_runtime', 'gateway', 'reliability', 'sessions']`: 1
  - `['gateway', 'reliability', 'sessions']`: 1
- Opus modal: `['agent_runtime', 'gateway', 'reliability', 'sessions']` (2/2)
- Opus label-set votes:
  - `['agent_runtime', 'gateway', 'reliability', 'sessions']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['gateway', 'model_serving', 'reliability', 'sessions']`

### openclaw-openclaw-10467

- Title: [Feature Request]: Multi-lane concurrency support for sub-agents via sessions_spawn
- GitHub: https://github.com/openclaw/openclaw/issues/10467
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'agent_runtime', 'config', 'queueing', 'tool_calling']` (2/3)
- GPT label-set votes:
  - `['acp', 'agent_runtime', 'config', 'queueing', 'tool_calling']`: 2
  - `['agent_runtime', 'config', 'queueing', 'tool_calling']`: 1
- Opus modal: `['agent_runtime', 'config', 'queueing']` (2/2)
- Opus label-set votes:
  - `['agent_runtime', 'config', 'queueing']`: 2
- Modal Jaccard: 0.600
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

### openclaw-openclaw-48406

- Title: Docs: add saturated session recovery guide
- GitHub: https://github.com/openclaw/openclaw/pull/48406
- Reasons: gpt_unstable, opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['config', 'docs', 'reliability', 'sessions']` (1/3)
- GPT label-set votes:
  - `['config', 'docs', 'reliability', 'sessions']`: 1
  - `['agent_runtime', 'config', 'docs', 'reliability']`: 1
  - `['config', 'docs', 'reliability']`: 1
- Opus modal: `['config', 'docs', 'reliability']` (2/2)
- Opus label-set votes:
  - `['config', 'docs', 'reliability']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['docs', 'memory', 'sessions']`

### openclaw-openclaw-48851

- Title: feat(status): add API call count to session status and usage footer
- GitHub: https://github.com/openclaw/openclaw/pull/48851
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['sessions', 'telemetry_usage', 'ui_tui']` (3/3)
- GPT label-set votes:
  - `['sessions', 'telemetry_usage', 'ui_tui']`: 3
- Opus modal: `['sessions', 'telemetry_usage']` (2/2)
- Opus label-set votes:
  - `['sessions', 'telemetry_usage']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['sessions', 'telemetry_usage', 'ui_tui']`

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

### openclaw-openclaw-58135

- Title: [Feature]: expose promptMode parameter in sessions_spawn for deterministic blank sub-agents
- GitHub: https://github.com/openclaw/openclaw/issues/58135
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['agent_runtime', 'tool_calling']` (2/3)
- GPT label-set votes:
  - `['agent_runtime', 'tool_calling']`: 2
  - `['agent_runtime', 'sessions', 'tool_calling']`: 1
- Opus modal: `['agent_runtime']` (2/2)
- Opus label-set votes:
  - `['agent_runtime']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `['acp', 'api_surface', 'coding_agents', 'sessions']`

### openclaw-openclaw-60737

- Title: [Feature]: Per-DM/per-chat default ACP binding for auto-spawning ACP sessions on new topics
- GitHub: https://github.com/openclaw/openclaw/issues/60737
- Reasons: gpt_unstable
- GPT modal: `['acp', 'chat_integrations', 'config']` (2/3)
- GPT label-set votes:
  - `['acp', 'chat_integrations', 'config']`: 2
  - `['acp', 'chat_integrations', 'config', 'sessions']`: 1
- Opus modal: `['acp', 'chat_integrations', 'config']` (2/2)
- Opus label-set votes:
  - `['acp', 'chat_integrations', 'config']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `['acp', 'chat_integrations', 'config', 'sessions']`

### openclaw-openclaw-82880

- Title: security: harden ACPX proxy and Firecrawl SSRF protection
- GitHub: https://github.com/openclaw/openclaw/pull/82880
- Reasons: gpt_unstable, gpt_flagged_human_review, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acpx', 'config', 'exec_tools', 'security']` (2/3)
- GPT label-set votes:
  - `['acpx', 'config', 'exec_tools', 'security']`: 2
  - `['acpx', 'config', 'exec_tools', 'mcp_tooling', 'security']`: 1
- Opus modal: `['acpx', 'exec_tools', 'security']` (1/2)
- Opus label-set votes:
  - `['acpx', 'exec_tools', 'security']`: 1
  - `['acpx', 'security']`: 1
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-46740

- Title: ACP: classify silent acpx exits as backend unavailable
- GitHub: https://github.com/openclaw/openclaw/pull/46740
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acpx', 'reliability']` (3/3)
- GPT label-set votes:
  - `['acpx', 'reliability']`: 3
- Opus modal: `['acp', 'acpx', 'reliability']` (2/2)
- Opus label-set votes:
  - `['acp', 'acpx', 'reliability']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['acp', 'acpx', 'reliability']`
