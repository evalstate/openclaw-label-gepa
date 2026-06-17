# V6 batch consensus review

- Batch: `prompt-keyword-audit-40`
- Rows: 40
- Accepted consensus: 25
- Deferred/review: 15
- GPT/Opus exact modal matches: 30
- Exact modal matches with 5 labels: 0
- Rows where either teacher hit the 5-label cap: 0
- Mean GPT/Opus modal Jaccard: 0.900

## Review rows

### openclaw-openclaw-47083

- Title: fix: respect totalTokensFresh flag to avoid showing stale token counts
- GitHub: https://github.com/openclaw/openclaw/pull/47083
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['ui_tui']` (2/3)
- GPT label-set votes:
  - `['ui_tui']`: 2
  - `['telemetry_usage', 'ui_tui']`: 1
- Opus modal: `['telemetry_usage', 'ui_tui']` (2/2)
- Opus label-set votes:
  - `['telemetry_usage', 'ui_tui']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-82642

- Title: Fix iMessage slash command acknowledgements
- GitHub: https://github.com/openclaw/openclaw/pull/82642
- Reasons: gpt_unstable
- GPT modal: `['chat_integrations', 'notifications']` (2/3)
- GPT label-set votes:
  - `['chat_integrations', 'notifications']`: 2
  - `['chat_integrations']`: 1
- Opus modal: `['chat_integrations', 'notifications']` (2/2)
- Opus label-set votes:
  - `['chat_integrations', 'notifications']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-51654

- Title: Support session-level environment variables for ACP sessions
- GitHub: https://github.com/openclaw/openclaw/issues/51654
- Reasons: gpt_unstable, opus_unstable
- GPT modal: `['acp', 'acpx', 'security']` (2/3)
- GPT label-set votes:
  - `['acp', 'acpx', 'security']`: 2
  - `['acpx', 'security', 'tool_calling']`: 1
- Opus modal: `['acp', 'acpx', 'security']` (1/2)
- Opus label-set votes:
  - `['acp', 'acpx', 'security']`: 1
  - `['acp', 'acpx']`: 1
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-56442

- Title: feat: Add opt-in ACP parent completion notify for sessions_spawn
- GitHub: https://github.com/openclaw/openclaw/pull/56442
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'notifications', 'tool_calling']` (2/3)
- GPT label-set votes:
  - `['acp', 'tool_calling']`: 1
  - `['acp', 'notifications', 'tool_calling']`: 2
- Opus modal: `['acp', 'notifications']` (2/2)
- Opus label-set votes:
  - `['acp', 'notifications']`: 2
- Modal Jaccard: 0.667
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
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['sessions', 'ui_tui']` (3/3)
- GPT label-set votes:
  - `['sessions', 'ui_tui']`: 3
- Opus modal: `['config', 'sessions', 'ui_tui']` (1/2)
- Opus label-set votes:
  - `['config', 'sessions', 'ui_tui']`: 1
  - `['sessions', 'ui_tui']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-10467

- Title: [Feature Request]: Multi-lane concurrency support for sub-agents via sessions_spawn
- GitHub: https://github.com/openclaw/openclaw/issues/10467
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'queueing', 'tool_calling']` (3/3)
- GPT label-set votes:
  - `['config', 'queueing', 'tool_calling']`: 3
- Opus modal: `['config', 'queueing']` (1/2)
- Opus label-set votes:
  - `['config', 'queueing']`: 1
  - `['config', 'queueing', 'tool_calling']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-39248

- Title: Bug: sandbox.mode: "non-main" silently breaks sessions_spawn subagent initialization
- GitHub: https://github.com/openclaw/openclaw/issues/39248
- Reasons: gpt_unstable
- GPT modal: `['agent_runtime', 'reliability', 'sandboxing']` (2/3)
- GPT label-set votes:
  - `['agent_runtime', 'reliability', 'sandboxing']`: 2
  - `['agent_runtime', 'sandboxing', 'sessions']`: 1
- Opus modal: `['agent_runtime', 'reliability', 'sandboxing']` (2/2)
- Opus label-set votes:
  - `['agent_runtime', 'reliability', 'sandboxing']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `[]`

### openclaw-openclaw-40332

- Title: [Feature]: Per-binding and per-agent permissionMode for ACP sessions
- GitHub: https://github.com/openclaw/openclaw/issues/40332
- Reasons: gpt_unstable
- GPT modal: `['acp', 'approvals', 'config']` (2/3)
- GPT label-set votes:
  - `['acp', 'approvals', 'config']`: 2
  - `['approvals', 'config', 'security']`: 1
- Opus modal: `['acp', 'approvals', 'config']` (2/2)
- Opus label-set votes:
  - `['acp', 'approvals', 'config']`: 2
- Modal Jaccard: 1.000
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
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'docs', 'reliability']` (2/3)
- GPT label-set votes:
  - `['config', 'docs', 'reliability']`: 2
  - `['agent_runtime', 'docs', 'reliability']`: 1
- Opus modal: `['docs', 'reliability', 'sessions']` (1/2)
- Opus label-set votes:
  - `['docs', 'reliability', 'sessions']`: 1
  - `['config', 'docs', 'sessions']`: 1
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-48580

- Title: Bug: acpx codex sessions 创建的会话立即退出 - stdin is not a terminal
- GitHub: https://github.com/openclaw/openclaw/issues/48580
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['acpx', 'codex', 'sessions']` (3/3)
- GPT label-set votes:
  - `['acpx', 'codex', 'sessions']`: 3
- Opus modal: `['acpx', 'codex', 'reliability']` (2/2)
- Opus label-set votes:
  - `['acpx', 'codex', 'reliability']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `[]`

### openclaw-openclaw-48851

- Title: feat(status): add API call count to session status and usage footer
- GitHub: https://github.com/openclaw/openclaw/pull/48851
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['sessions', 'telemetry_usage', 'ui_tui']` (3/3)
- GPT label-set votes:
  - `['sessions', 'telemetry_usage', 'ui_tui']`: 3
- Opus modal: `['sessions', 'telemetry_usage']` (1/2)
- Opus label-set votes:
  - `['sessions', 'telemetry_usage']`: 1
  - `['sessions', 'telemetry_usage', 'ui_tui']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-82880

- Title: security: harden ACPX proxy and Firecrawl SSRF protection
- GitHub: https://github.com/openclaw/openclaw/pull/82880
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acpx', 'exec_tools', 'security']` (2/3)
- GPT label-set votes:
  - `['acpx', 'security', 'skills_plugins']`: 1
  - `['acpx', 'exec_tools', 'security']`: 2
- Opus modal: `['acpx', 'security']` (2/2)
- Opus label-set votes:
  - `['acpx', 'security']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `[]`

### openclaw-openclaw-46740

- Title: ACP: classify silent acpx exits as backend unavailable
- GitHub: https://github.com/openclaw/openclaw/pull/46740
- Reasons: gpt_unstable
- GPT modal: `['acp', 'acpx', 'reliability']` (2/3)
- GPT label-set votes:
  - `['acp', 'acpx']`: 1
  - `['acp', 'acpx', 'reliability']`: 2
- Opus modal: `['acp', 'acpx', 'reliability']` (2/2)
- Opus label-set votes:
  - `['acp', 'acpx', 'reliability']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `[]`
