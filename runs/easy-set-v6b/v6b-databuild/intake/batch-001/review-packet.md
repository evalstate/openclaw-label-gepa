# V6 batch consensus review

- Batch: `batch-001`
- Rows: 30
- Accepted consensus: 19
- Deferred/review: 11
- GPT/Opus exact modal matches: 23
- Exact modal matches with 5 labels: 0
- Rows where either teacher hit the 5-label cap: 0
- Mean GPT/Opus modal Jaccard: 0.894

## Review rows

### openclaw-openclaw-41892

- Title: feat(control-ui): add cron calendar timeline view
- GitHub: https://github.com/openclaw/openclaw/pull/41892
- Reasons: opus_unstable
- GPT modal: `['cron_automation', 'ui_tui']` (3/3)
- GPT label-set votes:
  - `['cron_automation', 'ui_tui']`: 3
- Opus modal: `['cron_automation', 'ui_tui']` (1/2)
- Opus label-set votes:
  - `['cron_automation', 'ui_tui']`: 1
  - `['ui_tui']`: 1
- Modal Jaccard: 1.000
- Legacy v5: `['cron_automation', 'ui_tui']`

### openclaw-openclaw-68204

- Title: Unified run trace schema across agent, ACP, subagent, and task flows
- GitHub: https://github.com/openclaw/openclaw/issues/68204
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['telemetry_usage']` (1/3)
- GPT label-set votes:
  - `['telemetry_usage']`: 1
  - `['acp', 'agent_runtime', 'queueing', 'telemetry_usage']`: 1
  - `['acp', 'agent_runtime', 'telemetry_usage']`: 1
- Opus modal: `['acp', 'agent_runtime', 'telemetry_usage']` (2/2)
- Opus label-set votes:
  - `['acp', 'agent_runtime', 'telemetry_usage']`: 2
- Modal Jaccard: 0.333
- Legacy v5: `['acp', 'agent_runtime', 'sessions', 'telemetry_usage']`

### openclaw-openclaw-71157

- Title: [Feature]: Support WhatsApp disappearing-message expiration for outbound replies
- GitHub: https://github.com/openclaw/openclaw/issues/71157
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['chat_integrations', 'config']` (2/3)
- GPT label-set votes:
  - `['chat_integrations', 'config', 'notifications']`: 1
  - `['chat_integrations', 'config']`: 2
- Opus modal: `['chat_integrations', 'config', 'notifications']` (2/2)
- Opus label-set votes:
  - `['chat_integrations', 'config', 'notifications']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['chat_integrations', 'config', 'security']`

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

### openclaw-openclaw-82145

- Title: cron: allow retries for local model preflight
- GitHub: https://github.com/openclaw/openclaw/pull/82145
- Reasons: opus_unstable
- GPT modal: `['config', 'cron_automation', 'reliability', 'self_hosted_inference']` (3/3)
- GPT label-set votes:
  - `['config', 'cron_automation', 'reliability', 'self_hosted_inference']`: 3
- Opus modal: `['config', 'cron_automation', 'reliability', 'self_hosted_inference']` (1/2)
- Opus label-set votes:
  - `['config', 'cron_automation', 'reliability', 'self_hosted_inference']`: 1
  - `['config', 'cron_automation', 'self_hosted_inference']`: 1
- Modal Jaccard: 1.000
- Legacy v5: `['cron_automation', 'local_model_providers', 'config', 'reliability']`

### openclaw-openclaw-84648

- Title: Add SafeOps preflight hook for exec tool
- GitHub: https://github.com/openclaw/openclaw/pull/84648
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['exec_tools', 'hooks', 'security']` (3/3)
- GPT label-set votes:
  - `['exec_tools', 'hooks', 'security']`: 3
- Opus modal: `['exec_tools', 'security']` (2/2)
- Opus label-set votes:
  - `['exec_tools', 'security']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['exec_tools', 'hooks', 'security']`

### openclaw-openclaw-84732

- Title: Slack channel sends fail: `reconcileUnknownSend` required but no channel adapter implements it
- GitHub: https://github.com/openclaw/openclaw/issues/84732
- Reasons: opus_unstable
- GPT modal: `['chat_integrations', 'notifications', 'reliability']` (3/3)
- GPT label-set votes:
  - `['chat_integrations', 'notifications', 'reliability']`: 3
- Opus modal: `['chat_integrations', 'notifications', 'reliability']` (1/2)
- Opus label-set votes:
  - `['chat_integrations', 'notifications', 'reliability']`: 1
  - `['chat_integrations', 'notifications']`: 1
- Modal Jaccard: 1.000
- Legacy v5: `['chat_integrations', 'notifications', 'reliability']`

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
- Reasons: gpt_unstable
- GPT modal: `['agent_runtime', 'gateway', 'reliability', 'sessions']` (2/3)
- GPT label-set votes:
  - `['agent_runtime', 'gateway', 'reliability', 'sessions']`: 2
  - `['agent_runtime', 'reliability', 'sessions']`: 1
- Opus modal: `['agent_runtime', 'gateway', 'reliability', 'sessions']` (2/2)
- Opus label-set votes:
  - `['agent_runtime', 'gateway', 'reliability', 'sessions']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `['gateway', 'model_serving', 'reliability', 'sessions']`

### openclaw-openclaw-84997

- Title: [AI-assisted] Add NEAR AI Cloud provider
- GitHub: https://github.com/openclaw/openclaw/pull/84997
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['inference_api', 'model_lifecycle']` (3/3)
- GPT label-set votes:
  - `['inference_api', 'model_lifecycle']`: 3
- Opus modal: `['inference_api', 'model_lifecycle', 'skills_plugins']` (1/2)
- Opus label-set votes:
  - `['inference_api', 'model_lifecycle', 'skills_plugins']`: 1
  - `['inference_api', 'model_lifecycle']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `['model_serving', 'auth_identity']`

### openclaw-openclaw-87277

- Title: [Feature] Add MiMo-V2.5 to Xiaomi catalog + automatic multimodal routing when DeepSeek V4-Pro is primary model
- GitHub: https://github.com/openclaw/openclaw/issues/87277
- Reasons: opus_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['inference_api', 'model_lifecycle']` (3/3)
- GPT label-set votes:
  - `['inference_api', 'model_lifecycle']`: 3
- Opus modal: `['agent_runtime', 'model_lifecycle']` (2/2)
- Opus label-set votes:
  - `['agent_runtime', 'model_lifecycle']`: 2
- Modal Jaccard: 0.333
- Legacy v5: `['model_releases', 'model_serving', 'reliability']`
