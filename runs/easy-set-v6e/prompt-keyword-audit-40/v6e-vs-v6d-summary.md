# v6e vs v6d prompt-keyword-audit-40

## Aggregate

| Metric | v6d | v6e |
|---|---:|---:|
| `accepted_consensus` | 20 | 18 |
| `deferred` | 20 | 22 |
| `gpt_exact_stable_rows` | 32 | 32 |
| `opus_exact_stable_rows` | 37 | 34 |
| `gpt_opus_exact_modal_matches` | 23 | 23 |
| `mean_gpt_opus_modal_jaccard` | 0.845 | 0.8491666666666667 |
| `exact_modal_matches_with_5_labels` | 1 | 1 |
| `rows_with_any_5_label_teacher_modal` | 3 | 5 |

## Review Reasons

- v6d: `{'gpt_opus_modal_disagreement': 17, 'opus_unstable': 3, 'gpt_unstable': 8, 'opus_flagged_human_review': 3, 'gpt_flagged_human_review': 2}`
- v6e: `{'gpt_unstable': 8, 'opus_unstable': 6, 'gpt_opus_modal_disagreement': 17, 'gpt_flagged_human_review': 10, 'opus_flagged_human_review': 6}`

## Accepted Set Changes

- Lost accepted rows: `['openclaw-openclaw-47083', 'openclaw-openclaw-48580', 'openclaw-openclaw-59208']`
- Gained accepted rows: `['openclaw-openclaw-60737']`

## Changed Rows

### openclaw-openclaw-40332

- Title: [Feature]: Per-binding and per-agent permissionMode for ACP sessions
- Status: `deferred` -> `deferred`
- Accepted labels: `[]` -> `[]`
- GPT modal: `['acp', 'acpx', 'approvals', 'config', 'security']` -> `['acp', 'acpx', 'approvals', 'config', 'security']`
- Opus modal: `['acp', 'acpx', 'approvals', 'config']` -> `['acp', 'acpx', 'approvals', 'config', 'security']`
- Reasons: `['gpt_opus_modal_disagreement']` -> `['opus_unstable']`
- Jaccard: `0.8` -> `1.0`

### openclaw-openclaw-43564

- Title: [Feature Request] ACP Session Skill Context Injection
- Status: `deferred` -> `deferred`
- Accepted labels: `[]` -> `[]`
- GPT modal: `['acp', 'coding_agent_integrations', 'security', 'skills_plugins']` -> `['acp', 'api_surface', 'coding_agent_integrations', 'security', 'skills_plugins']`
- Opus modal: `['acp', 'coding_agent_integrations', 'skills_plugins']` -> `['acp', 'coding_agent_integrations', 'skills_plugins']`
- Reasons: `['gpt_unstable', 'opus_flagged_human_review', 'gpt_opus_modal_disagreement']` -> `['gpt_unstable', 'gpt_flagged_human_review', 'opus_unstable', 'opus_flagged_human_review', 'gpt_opus_modal_disagreement']`
- Jaccard: `0.75` -> `0.6`

### openclaw-openclaw-44379

- Title: fix(pi-runner): harden context-overflow recovery with one suppress-hook retry
- Status: `deferred` -> `deferred`
- Accepted labels: `[]` -> `[]`
- GPT modal: `['coding_agent_integrations', 'hooks', 'reliability']` -> `['agent_runtime', 'hooks', 'reliability']`
- Opus modal: `['agent_runtime', 'reliability']` -> `['agent_runtime', 'reliability']`
- Reasons: `['gpt_opus_modal_disagreement']` -> `['gpt_unstable', 'gpt_flagged_human_review', 'gpt_opus_modal_disagreement']`
- Jaccard: `0.25` -> `0.6666666666666666`

### openclaw-openclaw-47083

- Title: fix: respect totalTokensFresh flag to avoid showing stale token counts
- Status: `accepted_consensus` -> `deferred`
- Accepted labels: `['telemetry_usage', 'ui_tui']` -> `[]`
- GPT modal: `['telemetry_usage', 'ui_tui']` -> `['telemetry_usage', 'ui_tui']`
- Opus modal: `['telemetry_usage', 'ui_tui']` -> `['telemetry_usage', 'ui_tui']`
- Reasons: `[]` -> `['gpt_unstable', 'opus_unstable']`
- Jaccard: `1.0` -> `1.0`

### openclaw-openclaw-48406

- Title: Docs: add saturated session recovery guide
- Status: `deferred` -> `deferred`
- Accepted labels: `[]` -> `[]`
- GPT modal: `['config', 'docs', 'reliability', 'sessions']` -> `['config', 'docs', 'reliability']`
- Opus modal: `['config', 'docs', 'reliability']` -> `['docs', 'reliability', 'sessions']`
- Reasons: `['gpt_unstable', 'opus_flagged_human_review', 'gpt_opus_modal_disagreement']` -> `['gpt_unstable', 'opus_unstable', 'opus_flagged_human_review', 'gpt_opus_modal_disagreement']`
- Jaccard: `0.75` -> `0.5`

### openclaw-openclaw-48580

- Title: Bug: acpx codex sessions 创建的会话立即退出 - stdin is not a terminal
- Status: `accepted_consensus` -> `deferred`
- Accepted labels: `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']` -> `[]`
- GPT modal: `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']` -> `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']`
- Opus modal: `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']` -> `['acpx', 'codex', 'reliability', 'sessions']`
- Reasons: `[]` -> `['gpt_flagged_human_review', 'opus_flagged_human_review', 'gpt_opus_modal_disagreement']`
- Jaccard: `1.0` -> `0.8`

### openclaw-openclaw-51654

- Title: Support session-level environment variables for ACP sessions
- Status: `deferred` -> `deferred`
- Accepted labels: `[]` -> `[]`
- GPT modal: `['acpx', 'api_surface', 'security', 'sessions']` -> `['acp', 'acpx', 'api_surface', 'security', 'sessions']`
- Opus modal: `['acp', 'acpx', 'security']` -> `['acp', 'acpx', 'security', 'sessions']`
- Reasons: `['gpt_unstable', 'gpt_flagged_human_review', 'opus_flagged_human_review', 'gpt_opus_modal_disagreement']` -> `['gpt_flagged_human_review', 'opus_unstable', 'gpt_opus_modal_disagreement']`
- Jaccard: `0.4` -> `0.8`

### openclaw-openclaw-56442

- Title: feat: Add opt-in ACP parent completion notify for sessions_spawn
- Status: `deferred` -> `deferred`
- Accepted labels: `[]` -> `[]`
- GPT modal: `['acp', 'notifications', 'tool_calling']` -> `['acp', 'api_surface', 'notifications']`
- Opus modal: `['acp', 'notifications']` -> `['acp', 'notifications']`
- Reasons: `['gpt_opus_modal_disagreement']` -> `['gpt_opus_modal_disagreement']`
- Jaccard: `0.6666666666666666` -> `0.6666666666666666`

### openclaw-openclaw-58135

- Title: [Feature]: expose promptMode parameter in sessions_spawn for deterministic blank sub-agents
- Status: `deferred` -> `deferred`
- Accepted labels: `[]` -> `[]`
- GPT modal: `['agent_runtime', 'tool_calling']` -> `['agent_runtime', 'api_surface', 'sessions']`
- Opus modal: `['agent_runtime']` -> `['agent_runtime']`
- Reasons: `['gpt_unstable', 'gpt_opus_modal_disagreement']` -> `['gpt_unstable', 'gpt_flagged_human_review', 'opus_flagged_human_review', 'gpt_opus_modal_disagreement']`
- Jaccard: `0.5` -> `0.3333333333333333`

### openclaw-openclaw-59208

- Title: fix(status): honor selected usage auth profile
- Status: `accepted_consensus` -> `deferred`
- Accepted labels: `['auth_identity', 'telemetry_usage']` -> `[]`
- GPT modal: `['auth_identity', 'telemetry_usage']` -> `['auth_identity', 'telemetry_usage']`
- Opus modal: `['auth_identity', 'telemetry_usage']` -> `['auth_identity', 'telemetry_usage']`
- Reasons: `[]` -> `['gpt_flagged_human_review']`
- Jaccard: `1.0` -> `1.0`

### openclaw-openclaw-60737

- Title: [Feature]: Per-DM/per-chat default ACP binding for auto-spawning ACP sessions on new topics
- Status: `deferred` -> `accepted_consensus`
- Accepted labels: `[]` -> `['acp', 'chat_integrations', 'config']`
- GPT modal: `['acp', 'chat_integrations', 'config']` -> `['acp', 'chat_integrations', 'config']`
- Opus modal: `['acp', 'chat_integrations', 'config']` -> `['acp', 'chat_integrations', 'config']`
- Reasons: `['gpt_unstable']` -> `[]`
- Jaccard: `1.0` -> `1.0`

### openclaw-openclaw-71646

- Title: mcp/channel-bridge: pendingClaudePermissions / pendingApprovals leak — no TTL, no close-clear, no cap
- Status: `deferred` -> `deferred`
- Accepted labels: `[]` -> `[]`
- GPT modal: `['approvals', 'mcp_tooling', 'reliability']` -> `['approvals', 'mcp_tooling', 'reliability']`
- Opus modal: `['approvals', 'mcp_tooling', 'reliability']` -> `['approvals', 'reliability']`
- Reasons: `['opus_unstable']` -> `['gpt_opus_modal_disagreement']`
- Jaccard: `1.0` -> `0.6666666666666666`

### openclaw-openclaw-84771

- Title: Event loop saturation during startup: synchronous model-prewarm and session-locks block event loop for 28-64 seconds
- Status: `deferred` -> `deferred`
- Accepted labels: `[]` -> `[]`
- GPT modal: `['agent_runtime', 'reliability', 'sessions']` -> `['agent_runtime', 'gateway', 'reliability', 'sessions']`
- Opus modal: `['agent_runtime', 'gateway', 'reliability', 'sessions']` -> `['agent_runtime', 'gateway', 'reliability', 'sessions']`
- Reasons: `['gpt_unstable', 'gpt_opus_modal_disagreement']` -> `['gpt_unstable', 'gpt_flagged_human_review', 'opus_flagged_human_review']`
- Jaccard: `0.75` -> `1.0`

## Accepted Label Counts v6d

```json
{
  "config": 3,
  "docs": 3,
  "ui_tui": 3,
  "telemetry_usage": 3,
  "chat_integrations": 3,
  "security": 3,
  "memory": 2,
  "exec_tools": 2,
  "hooks": 1,
  "mcp_tooling": 1,
  "skills_plugins": 1,
  "approvals": 1,
  "notifications": 1,
  "inference_api": 1,
  "packaging_deployment": 1,
  "tests_ci": 1,
  "queueing": 1,
  "api_surface": 1,
  "gateway": 1,
  "auth_identity": 1,
  "acp": 1,
  "acpx": 1,
  "codex": 1,
  "coding_agent_integrations": 1,
  "reliability": 1,
  "sessions": 1
}
```

## Accepted Label Counts v6e

```json
{
  "config": 4,
  "chat_integrations": 4,
  "docs": 3,
  "security": 3,
  "memory": 2,
  "ui_tui": 2,
  "exec_tools": 2,
  "acp": 2,
  "hooks": 1,
  "mcp_tooling": 1,
  "skills_plugins": 1,
  "approvals": 1,
  "notifications": 1,
  "inference_api": 1,
  "packaging_deployment": 1,
  "tests_ci": 1,
  "queueing": 1,
  "api_surface": 1,
  "gateway": 1,
  "telemetry_usage": 1
}
```
