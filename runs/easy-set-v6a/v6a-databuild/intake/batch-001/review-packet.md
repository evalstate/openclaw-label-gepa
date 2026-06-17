# V6 batch consensus review

- Batch: `batch-001`
- Rows: 30
- Accepted consensus: 17
- Deferred/review: 13
- GPT/Opus exact modal matches: 22
- Exact modal matches with 5 labels: 0
- Rows where either teacher hit the 5-label cap: 0
- Mean GPT/Opus modal Jaccard: 0.908

## Review rows

### openclaw-openclaw-68204

- Title: Unified run trace schema across agent, ACP, subagent, and task flows
- GitHub: https://github.com/openclaw/openclaw/issues/68204
- Reasons: gpt_unstable, gpt_flagged_human_review, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'agent_runtime', 'queueing', 'telemetry_usage']` (2/3)
- GPT label-set votes:
  - `['acp', 'agent_runtime', 'queueing', 'telemetry_usage']`: 2
  - `['telemetry_usage']`: 1
- Opus modal: `['acp', 'agent_runtime', 'telemetry_usage']` (2/2)
- Opus label-set votes:
  - `['acp', 'agent_runtime', 'telemetry_usage']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['acp', 'agent_runtime', 'sessions', 'telemetry_usage']`

### openclaw-openclaw-68916

- Title: [Bug]: ACP oneshot sessions leave orphaned processes — session reset does not clean up child ACP session keys
- GitHub: https://github.com/openclaw/openclaw/issues/68916
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'reliability', 'sessions']` (2/3)
- GPT label-set votes:
  - `['acp', 'gateway', 'reliability', 'sessions']`: 1
  - `['acp', 'reliability', 'sessions']`: 2
- Opus modal: `['acp', 'gateway', 'reliability', 'sessions']` (1/2)
- Opus label-set votes:
  - `['acp', 'gateway', 'reliability', 'sessions']`: 1
  - `['acp', 'reliability', 'sessions']`: 1
- Modal Jaccard: 0.750
- Legacy v5: `['acp', 'sessions', 'reliability']`

### openclaw-openclaw-71157

- Title: [Feature]: Support WhatsApp disappearing-message expiration for outbound replies
- GitHub: https://github.com/openclaw/openclaw/issues/71157
- Reasons: gpt_unstable
- GPT modal: `['chat_integrations', 'config', 'notifications']` (2/3)
- GPT label-set votes:
  - `['chat_integrations', 'config', 'notifications']`: 2
  - `['chat_integrations', 'config', 'notifications', 'security']`: 1
- Opus modal: `['chat_integrations', 'config', 'notifications']` (2/2)
- Opus label-set votes:
  - `['chat_integrations', 'config', 'notifications']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `['chat_integrations', 'config', 'security']`

### openclaw-openclaw-71487

- Title: Web UI: add a clear TTS toggle and default voice picker in Settings
- GitHub: https://github.com/openclaw/openclaw/issues/71487
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'inference_api', 'ui_tui']` (2/3)
- GPT label-set votes:
  - `['config', 'ui_tui']`: 1
  - `['config', 'inference_api', 'ui_tui']`: 2
- Opus modal: `['config', 'ui_tui']` (1/2)
- Opus label-set votes:
  - `['config', 'ui_tui']`: 1
  - `['config', 'inference_api', 'ui_tui']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `['ui_tui', 'self_hosted_inference', 'config']`

### openclaw-openclaw-72138

- Title: fix(feishu): emit sent hooks for normal replies
- GitHub: https://github.com/openclaw/openclaw/pull/72138
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['chat_integrations', 'hooks']` (2/3)
- GPT label-set votes:
  - `['chat_integrations', 'hooks', 'notifications']`: 1
  - `['chat_integrations', 'hooks']`: 2
- Opus modal: `['chat_integrations', 'hooks', 'notifications']` (2/2)
- Opus label-set votes:
  - `['chat_integrations', 'hooks', 'notifications']`: 2
- Modal Jaccard: 0.667
- Legacy v5: `['chat_integrations', 'hooks', 'notifications']`

### openclaw-openclaw-77694

- Title: [Bug]: acpx flow run ACP node outputs return empty strings instead of agent replies
- GitHub: https://github.com/openclaw/openclaw/issues/77694
- Reasons: gpt_unstable
- GPT modal: `['acp', 'acpx']` (2/3)
- GPT label-set votes:
  - `['acp', 'acpx']`: 2
  - `['acpx']`: 1
- Opus modal: `['acp', 'acpx']` (2/2)
- Opus label-set votes:
  - `['acp', 'acpx']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `['acpx', 'acp', 'agent_runtime', 'reliability']`

### openclaw-openclaw-82145

- Title: cron: allow retries for local model preflight
- GitHub: https://github.com/openclaw/openclaw/pull/82145
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'cron_automation', 'reliability', 'self_hosted_inference']` (3/3)
- GPT label-set votes:
  - `['config', 'cron_automation', 'reliability', 'self_hosted_inference']`: 3
- Opus modal: `['config', 'cron_automation', 'reliability']` (1/2)
- Opus label-set votes:
  - `['config', 'cron_automation', 'reliability']`: 1
  - `['config', 'cron_automation', 'reliability', 'self_hosted_inference']`: 1
- Modal Jaccard: 0.750
- Legacy v5: `['cron_automation', 'local_model_providers', 'config', 'reliability']`

### openclaw-openclaw-84648

- Title: Add SafeOps preflight hook for exec tool
- GitHub: https://github.com/openclaw/openclaw/pull/84648
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['exec_tools', 'hooks', 'security']` (2/3)
- GPT label-set votes:
  - `['exec_tools', 'hooks', 'security']`: 2
  - `['exec_tools', 'security']`: 1
- Opus modal: `['exec_tools', 'security']` (1/2)
- Opus label-set votes:
  - `['exec_tools', 'security']`: 1
  - `['exec_tools', 'hooks', 'security']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `['exec_tools', 'hooks', 'security']`

### openclaw-openclaw-84732

- Title: Slack channel sends fail: `reconcileUnknownSend` required but no channel adapter implements it
- GitHub: https://github.com/openclaw/openclaw/issues/84732
- Reasons: gpt_unstable
- GPT modal: `['chat_integrations', 'notifications', 'reliability']` (2/3)
- GPT label-set votes:
  - `['chat_integrations', 'notifications', 'reliability']`: 2
  - `['chat_integrations', 'notifications']`: 1
- Opus modal: `['chat_integrations', 'notifications', 'reliability']` (2/2)
- Opus label-set votes:
  - `['chat_integrations', 'notifications', 'reliability']`: 2
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

### openclaw-openclaw-84761

- Title: feat(secrets): scan backup files for plaintext provider apiKey values
- GitHub: https://github.com/openclaw/openclaw/pull/84761
- Reasons: gpt_unstable
- GPT modal: `['security']` (2/3)
- GPT label-set votes:
  - `['security']`: 2
  - `['config', 'security']`: 1
- Opus modal: `['security']` (2/2)
- Opus label-set votes:
  - `['security']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `['security', 'auth_identity', 'config']`

### openclaw-openclaw-84997

- Title: [AI-assisted] Add NEAR AI Cloud provider
- GitHub: https://github.com/openclaw/openclaw/pull/84997
- Reasons: gpt_unstable
- GPT modal: `['inference_api', 'model_lifecycle']` (2/3)
- GPT label-set votes:
  - `['inference_api']`: 1
  - `['inference_api', 'model_lifecycle']`: 2
- Opus modal: `['inference_api', 'model_lifecycle']` (2/2)
- Opus label-set votes:
  - `['inference_api', 'model_lifecycle']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `['model_serving', 'auth_identity']`

### openclaw-openclaw-87277

- Title: [Feature] Add MiMo-V2.5 to Xiaomi catalog + automatic multimodal routing when DeepSeek V4-Pro is primary model
- GitHub: https://github.com/openclaw/openclaw/issues/87277
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['inference_api', 'model_lifecycle']` (3/3)
- GPT label-set votes:
  - `['inference_api', 'model_lifecycle']`: 3
- Opus modal: `['agent_runtime', 'model_lifecycle']` (2/2)
- Opus label-set votes:
  - `['agent_runtime', 'model_lifecycle']`: 2
- Modal Jaccard: 0.333
- Legacy v5: `['model_releases', 'model_serving', 'reliability']`
