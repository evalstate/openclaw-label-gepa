# V6 batch consensus review

- Batch: `batch-001`
- Rows: 30
- Accepted consensus: 18
- Deferred/review: 12
- GPT/Opus exact modal matches: 22
- Exact modal matches with 5 labels: 0
- Rows where either teacher hit the 5-label cap: 0
- Mean GPT/Opus modal Jaccard: 0.922

## Review rows

### openclaw-openclaw-42408

- Title: [Bug/Docs]: local+hybrid memory_search quality can appear unstable due to extraPaths path drift + benchmark-file contamination
- Reasons: gpt_unstable
- GPT modal: `['config', 'docs', 'memory']` (2/3)
- GPT label-set votes:
  - `['config', 'docs', 'memory']`: 2
  - `['config', 'docs', 'memory', 'telemetry_usage']`: 1
- Opus modal: `['config', 'docs', 'memory']` (2/2)
- Opus label-set votes:
  - `['config', 'docs', 'memory']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `['config', 'docs', 'memory']`

### openclaw-openclaw-68204

- Title: Unified run trace schema across agent, ACP, subagent, and task flows
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'coding_agents', 'telemetry_usage']` (2/3)
- GPT label-set votes:
  - `['acp', 'coding_agents', 'telemetry_usage']`: 2
  - `['acp', 'coding_agents', 'queueing', 'telemetry_usage']`: 1
- Opus modal: `['acp', 'agent_runtime', 'coding_agents', 'telemetry_usage']` (1/2)
- Opus label-set votes:
  - `['acp', 'agent_runtime', 'coding_agents', 'telemetry_usage']`: 1
  - `['acp', 'coding_agents', 'telemetry_usage']`: 1
- Modal Jaccard: 0.750
- Legacy v5: `['acp', 'agent_runtime', 'sessions', 'telemetry_usage']`

### openclaw-openclaw-68916

- Title: [Bug]: ACP oneshot sessions leave orphaned processes — session reset does not clean up child ACP session keys
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['acp', 'reliability', 'sessions']` (3/3)
- GPT label-set votes:
  - `['acp', 'reliability', 'sessions']`: 3
- Opus modal: `['acp', 'gateway', 'reliability', 'sessions']` (1/2)
- Opus label-set votes:
  - `['acp', 'gateway', 'reliability', 'sessions']`: 1
  - `['acp', 'reliability', 'sessions']`: 1
- Modal Jaccard: 0.750
- Legacy v5: `['acp', 'sessions', 'reliability']`

### openclaw-openclaw-71487

- Title: Web UI: add a clear TTS toggle and default voice picker in Settings
- Reasons: opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['config', 'inference_api', 'ui_tui']` (3/3)
- GPT label-set votes:
  - `['config', 'inference_api', 'ui_tui']`: 3
- Opus modal: `['inference_api', 'ui_tui']` (1/2)
- Opus label-set votes:
  - `['inference_api', 'ui_tui']`: 1
  - `['ui_tui']`: 1
- Modal Jaccard: 0.667
- Legacy v5: `['ui_tui', 'self_hosted_inference', 'config']`

### openclaw-openclaw-76724

- Title: [Bug]: MCP tools not discovered by Agent despite successful handshake (200 OK)
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['mcp_tooling', 'ui_tui']` (3/3)
- GPT label-set votes:
  - `['mcp_tooling', 'ui_tui']`: 3
- Opus modal: `['mcp_tooling']` (2/2)
- Opus label-set votes:
  - `['mcp_tooling']`: 2
- Modal Jaccard: 0.500
- Legacy v5: `['mcp_tooling', 'ui_tui']`

### openclaw-openclaw-78528

- Title: Security: skill SecretRef API keys still leak into exec child environments
- Reasons: gpt_opus_modal_disagreement
- GPT modal: `['auth_identity', 'exec_tools', 'security', 'skills_plugins']` (3/3)
- GPT label-set votes:
  - `['auth_identity', 'exec_tools', 'security', 'skills_plugins']`: 3
- Opus modal: `['exec_tools', 'security', 'skills_plugins']` (2/2)
- Opus label-set votes:
  - `['exec_tools', 'security', 'skills_plugins']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['security', 'exec_tools', 'skills_plugins', 'auth_identity']`

### openclaw-openclaw-81488

- Title: Harden node exec approval precheck env [AI]
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['approvals', 'coding_agents', 'exec_tools', 'security']` (2/3)
- GPT label-set votes:
  - `['approvals', 'exec_tools', 'security']`: 1
  - `['approvals', 'coding_agents', 'exec_tools', 'security']`: 2
- Opus modal: `['approvals', 'exec_tools', 'security']` (2/2)
- Opus label-set votes:
  - `['approvals', 'exec_tools', 'security']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['approvals', 'exec_tools', 'security']`

### openclaw-openclaw-84648

- Title: Add SafeOps preflight hook for exec tool
- Reasons: gpt_unstable
- GPT modal: `['exec_tools', 'hooks', 'security']` (2/3)
- GPT label-set votes:
  - `['approvals', 'exec_tools', 'hooks', 'security']`: 1
  - `['exec_tools', 'hooks', 'security']`: 2
- Opus modal: `['exec_tools', 'hooks', 'security']` (2/2)
- Opus label-set votes:
  - `['exec_tools', 'hooks', 'security']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `['exec_tools', 'hooks', 'security']`

### openclaw-openclaw-84761

- Title: feat(secrets): scan backup files for plaintext provider apiKey values
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

### openclaw-openclaw-84771

- Title: Event loop saturation during startup: synchronous model-prewarm and session-locks block event loop for 28-64 seconds
- Reasons: gpt_unstable, gpt_opus_modal_disagreement
- GPT modal: `['agent_runtime', 'gateway', 'reliability', 'sessions']` (2/3)
- GPT label-set votes:
  - `['agent_runtime', 'gateway', 'reliability', 'sessions']`: 2
  - `['gateway', 'reliability', 'sessions']`: 1
- Opus modal: `['gateway', 'reliability', 'sessions']` (2/2)
- Opus label-set votes:
  - `['gateway', 'reliability', 'sessions']`: 2
- Modal Jaccard: 0.750
- Legacy v5: `['gateway', 'model_serving', 'reliability', 'sessions']`

### openclaw-openclaw-84997

- Title: [AI-assisted] Add NEAR AI Cloud provider
- Reasons: gpt_unstable, opus_unstable, gpt_opus_modal_disagreement
- GPT modal: `['auth_identity', 'config', 'inference_api', 'model_lifecycle']` (2/3)
- GPT label-set votes:
  - `['auth_identity', 'config', 'inference_api', 'model_lifecycle']`: 2
  - `['auth_identity', 'inference_api', 'model_lifecycle']`: 1
- Opus modal: `['auth_identity', 'inference_api', 'model_lifecycle']` (1/2)
- Opus label-set votes:
  - `['auth_identity', 'inference_api', 'model_lifecycle']`: 1
  - `['inference_api', 'model_lifecycle']`: 1
- Modal Jaccard: 0.750
- Legacy v5: `['model_serving', 'auth_identity']`

### openclaw-openclaw-87277

- Title: [Feature] Add MiMo-V2.5 to Xiaomi catalog + automatic multimodal routing when DeepSeek V4-Pro is primary model
- Reasons: opus_flagged_human_review
- GPT modal: `['inference_api', 'model_lifecycle']` (3/3)
- GPT label-set votes:
  - `['inference_api', 'model_lifecycle']`: 3
- Opus modal: `['inference_api', 'model_lifecycle']` (2/2)
- Opus label-set votes:
  - `['inference_api', 'model_lifecycle']`: 2
- Modal Jaccard: 1.000
- Legacy v5: `['model_releases', 'model_serving', 'reliability']`
