# V6 batch consensus review

- Batch: `prompt-keyword-audit-40`
- Rows: 40
- Accepted consensus: 22
- Deferred/review: 18
- GPT/Opus exact modal matches: 27
- Exact modal matches with 5 labels: 0
- Rows where either teacher hit the 5-label cap: 2
- Mean GPT/Opus modal Jaccard: 0.870

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
- Legacy v5: `[]`

### openclaw-openclaw-82642

- Title: Fix iMessage slash command acknowledgements
- GitHub: https://github.com/openclaw/openclaw/pull/82642
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['chat_integrations']` (2/3)
- GPT label-set votes:
  - `['chat_integrations']`: 2
  - `['chat_integrations', 'notifications']`: 1
- Opus modal: `['chat_integrations', 'notifications']` (2/2)
- Opus label-set votes:
  - `['chat_integrations', 'notifications']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-43564

- Title: [Feature Request] ACP Session Skill Context Injection
- GitHub: https://github.com/openclaw/openclaw/issues/43564
- Reasons: gpt_unstable, gpt_flagged_human_review, opus_unstable
- GPT modal: `['acp', 'coding_agent_integrations', 'skills_plugins']` (2/3)
- GPT label-set votes:
  - `['acp', 'coding_agent_integrations', 'skills_plugins']`: 2
  - `['acp', 'coding_agent_integrations', 'skills_plugins', 'tool_calling']`: 1
- Opus modal: `['acp', 'coding_agent_integrations', 'skills_plugins']` (1/2)
- Opus label-set votes:
  - `['acp', 'coding_agent_integrations', 'skills_plugins']`: 1
  - `['acp', 'config', 'skills_plugins']`: 1
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-54471

- Title: fix(acp): add system_event stream relay to parent session for ACP spawn
- GitHub: https://github.com/openclaw/openclaw/pull/54471
- Reasons: gpt_unstable
- GPT modal: `['acp']` (2/3)
- GPT label-set votes:
  - `['acp', 'codex']`: 1
  - `['acp']`: 2
- Opus modal: `['acp']` (2/2)
- Opus label-set votes:
  - `['acp']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-56442

- Title: feat: Add opt-in ACP parent completion notify for sessions_spawn
- GitHub: https://github.com/openclaw/openclaw/pull/56442
- Reasons: opus_unstable
- GPT modal: `['acp', 'notifications', 'tool_calling']` (3/3)
- GPT label-set votes:
  - `['acp', 'notifications', 'tool_calling']`: 3
- Opus modal: `['acp', 'notifications', 'tool_calling']` (1/2)
- Opus label-set votes:
  - `['acp', 'notifications', 'tool_calling']`: 1
  - `['acp', 'notifications']`: 1
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-68204

- Title: Unified run trace schema across agent, ACP, subagent, and task flows
- GitHub: https://github.com/openclaw/openclaw/issues/68204
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['telemetry_usage']` (3/3)
- GPT label-set votes:
  - `['telemetry_usage']`: 3
- Opus modal: `['acp', 'agent_runtime', 'telemetry_usage']` (2/2)
- Opus label-set votes:
  - `['acp', 'agent_runtime', 'telemetry_usage']`: 2
- Modal Jaccard: 0.333
- Legacy v5: `[]`

### openclaw-openclaw-77694

- Title: [Bug]: acpx flow run ACP node outputs return empty strings instead of agent replies
- GitHub: https://github.com/openclaw/openclaw/issues/77694
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acpx']` (3/3)
- GPT label-set votes:
  - `['acpx']`: 3
- Opus modal: `['acp', 'acpx']` (1/2)
- Opus label-set votes:
  - `['acp', 'acpx']`: 1
  - `['acpx']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `[]`

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
- Legacy v5: `[]`

### openclaw-openclaw-84771

- Title: Event loop saturation during startup: synchronous model-prewarm and session-locks block event loop for 28-64 seconds
- GitHub: https://github.com/openclaw/openclaw/issues/84771
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['agent_runtime', 'reliability', 'sessions']` (2/3)
- GPT label-set votes:
  - `['agent_runtime', 'reliability', 'sessions']`: 2
  - `['agent_runtime', 'gateway', 'reliability', 'sessions']`: 1
- Opus modal: `['agent_runtime', 'gateway', 'reliability', 'sessions']` (2/2)
- Opus label-set votes:
  - `['agent_runtime', 'gateway', 'reliability', 'sessions']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-10467

- Title: [Feature Request]: Multi-lane concurrency support for sub-agents via sessions_spawn
- GitHub: https://github.com/openclaw/openclaw/issues/10467
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['agent_runtime', 'config', 'queueing', 'tool_calling']` (2/3)
- GPT label-set votes:
  - `['config', 'queueing', 'tool_calling']`: 1
  - `['agent_runtime', 'config', 'queueing', 'tool_calling']`: 2
- Opus modal: `['config', 'queueing', 'tool_calling']` (2/2)
- Opus label-set votes:
  - `['config', 'queueing', 'tool_calling']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `[]`

### openclaw-openclaw-39248

- Title: Bug: sandbox.mode: "non-main" silently breaks sessions_spawn subagent initialization
- GitHub: https://github.com/openclaw/openclaw/issues/39248
- Reasons: gpt_unstable
- GPT modal: `['agent_runtime', 'reliability', 'sandboxing']` (2/3)
- GPT label-set votes:
  - `['agent_runtime', 'reliability', 'sandboxing', 'sessions']`: 1
  - `['agent_runtime', 'reliability', 'sandboxing']`: 2
- Opus modal: `['agent_runtime', 'reliability', 'sandboxing']` (2/2)
- Opus label-set votes:
  - `['agent_runtime', 'reliability', 'sandboxing']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-40332

- Title: [Feature]: Per-binding and per-agent permissionMode for ACP sessions
- GitHub: https://github.com/openclaw/openclaw/issues/40332
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'acpx', 'approvals', 'config', 'security']` (3/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'approvals', 'config', 'security']`: 3
- Opus modal: `['acp', 'approvals', 'config']` (1/2)
- Opus label-set votes:
  - `['acp', 'approvals', 'config']`: 1
  - `['acp', 'acpx', 'approvals', 'config']`: 1
- Modal Jaccard: 0.600
- Legacy v5: `[]`

### openclaw-openclaw-44379

- Title: fix(pi-runner): harden context-overflow recovery with one suppress-hook retry
- GitHub: https://github.com/openclaw/openclaw/pull/44379
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['agent_runtime', 'hooks', 'reliability']` (3/3)
- GPT label-set votes:
  - `['agent_runtime', 'hooks', 'reliability']`: 3
- Opus modal: `['agent_runtime', 'reliability']` (2/2)
- Opus label-set votes:
  - `['agent_runtime', 'reliability']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-48406

- Title: Docs: add saturated session recovery guide
- GitHub: https://github.com/openclaw/openclaw/pull/48406
- Reasons: gpt_unstable, opus_unstable, opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['agent_runtime', 'config', 'docs', 'reliability']` (2/3)
- GPT label-set votes:
  - `['agent_runtime', 'config', 'docs', 'reliability']`: 2
  - `['config', 'docs', 'reliability', 'sessions']`: 1
- Opus modal: `['docs', 'reliability', 'sessions']` (1/2)
- Opus label-set votes:
  - `['docs', 'reliability', 'sessions']`: 1
  - `['config', 'docs', 'reliability', 'sessions']`: 1
- Modal Jaccard: 0.400
- Legacy v5: `[]`

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
- Legacy v5: `[]`

### openclaw-openclaw-51667

- Title: Feature: Native Audio Input for Omni-Modal Models (skip STT transcription)
- GitHub: https://github.com/openclaw/openclaw/issues/51667
- Reasons: gpt_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['config', 'inference_api', 'sessions']` (3/3)
- GPT label-set votes:
  - `['config', 'inference_api', 'sessions']`: 3
- Opus modal: `['config', 'inference_api']` (2/2)
- Opus label-set votes:
  - `['config', 'inference_api']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-82880

- Title: security: harden ACPX proxy and Firecrawl SSRF protection
- GitHub: https://github.com/openclaw/openclaw/pull/82880
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acpx', 'config', 'exec_tools', 'security']` (3/3)
- GPT label-set votes:
  - `['acpx', 'config', 'exec_tools', 'security']`: 3
- Opus modal: `['acpx', 'security']` (1/2)
- Opus label-set votes:
  - `['acpx', 'security']`: 1
  - `['acpx', 'exec_tools', 'security']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-46740

- Title: ACP: classify silent acpx exits as backend unavailable
- GitHub: https://github.com/openclaw/openclaw/pull/46740
- Reasons: gpt_unstable
- GPT modal: `['acp', 'acpx', 'reliability']` (2/3)
- GPT label-set votes:
  - `['acpx', 'reliability']`: 1
  - `['acp', 'acpx', 'reliability']`: 2
- Opus modal: `['acp', 'acpx', 'reliability']` (2/2)
- Opus label-set votes:
  - `['acp', 'acpx', 'reliability']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `[]`
