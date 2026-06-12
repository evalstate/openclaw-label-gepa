# v6d GPT+Opus vs v6b baseline

## all

```json
{
  "rows": 40,
  "v6b_accepted": 20,
  "v6d_accepted": 20,
  "v6d_gpt_opus_modal_match": 23,
  "v6d_gpt_stable": 32,
  "v6d_opus_stable": 37,
  "v6d_gpt_same_as_v6b_gpt": 32,
  "v6d_opus_same_as_v6b_opus": 32,
  "v6d_consensus_same_as_v6b_gpt": 22,
  "v6d_consensus_same_as_v6b_opus": 21,
  "v6d_deferred": 20,
  "v6b_deferred": 20,
  "gpt_dropped_sessions_vs_v6b_gpt": 4,
  "opus_dropped_sessions_vs_v6b_opus": 3
}
```

## old

```json
{
  "rows": 20,
  "v6b_accepted": 20,
  "v6d_accepted": 18,
  "v6d_gpt_opus_modal_match": 19,
  "v6d_gpt_stable": 20,
  "v6d_opus_stable": 19,
  "v6d_gpt_same_as_v6b_gpt": 20,
  "v6d_opus_same_as_v6b_opus": 19,
  "v6d_consensus_same_as_v6b_gpt": 19,
  "v6d_consensus_same_as_v6b_opus": 19,
  "v6d_deferred": 2
}
```

## confused

```json
{
  "rows": 20,
  "v6b_deferred": 20,
  "v6d_deferred": 18,
  "v6d_opus_stable": 18,
  "gpt_dropped_sessions_vs_v6b_gpt": 4,
  "opus_dropped_sessions_vs_v6b_opus": 3,
  "v6d_accepted": 2,
  "v6d_gpt_opus_modal_match": 4,
  "v6d_gpt_stable": 12,
  "v6d_gpt_same_as_v6b_gpt": 12,
  "v6d_opus_same_as_v6b_opus": 13,
  "v6d_consensus_same_as_v6b_gpt": 3,
  "v6d_consensus_same_as_v6b_opus": 2
}
```

## Confused rows

### openclaw-openclaw-43564

- Title: [Feature Request] ACP Session Skill Context Injection
- v6b GPT / Opus: `['acp', 'coding_agent_integrations', 'security', 'sessions', 'skills_plugins']` / `['acp', 'skills_plugins']`
- v6d GPT / Opus: `['acp', 'coding_agent_integrations', 'security', 'skills_plugins']` / `['acp', 'coding_agent_integrations', 'skills_plugins']`
- v6d status: `deferred`; reasons: `['gpt_unstable', 'opus_flagged_human_review', 'gpt_opus_modal_disagreement']`; jaccard: `0.75`

### openclaw-openclaw-51654

- Title: Support session-level environment variables for ACP sessions
- v6b GPT / Opus: `['acp', 'acpx', 'security', 'sessions', 'tool_calling']` / `['acp', 'acpx', 'sessions']`
- v6d GPT / Opus: `['acpx', 'api_surface', 'security', 'sessions']` / `['acp', 'acpx', 'security']`
- v6d status: `deferred`; reasons: `['gpt_unstable', 'gpt_flagged_human_review', 'opus_flagged_human_review', 'gpt_opus_modal_disagreement']`; jaccard: `0.4`

### openclaw-openclaw-54471

- Title: fix(acp): add system_event stream relay to parent session for ACP spawn
- v6b GPT / Opus: `['acp']` / `['acp']`
- v6d GPT / Opus: `['acp']` / `['acp']`
- v6d status: `accepted_consensus`; reasons: `[]`; jaccard: `1.0`

### openclaw-openclaw-56442

- Title: feat: Add opt-in ACP parent completion notify for sessions_spawn
- v6b GPT / Opus: `['acp', 'notifications', 'sessions']` / `['acp', 'notifications']`
- v6d GPT / Opus: `['acp', 'notifications', 'tool_calling']` / `['acp', 'notifications']`
- v6d status: `deferred`; reasons: `['gpt_opus_modal_disagreement']`; jaccard: `0.6666666666666666`

### openclaw-openclaw-68204

- Title: Unified run trace schema across agent, ACP, subagent, and task flows
- v6b GPT / Opus: `['telemetry_usage']` / `['acp', 'agent_runtime', 'telemetry_usage']`
- v6d GPT / Opus: `['telemetry_usage']` / `['telemetry_usage']`
- v6d status: `deferred`; reasons: `['opus_unstable']`; jaccard: `1.0`

### openclaw-openclaw-77694

- Title: [Bug]: acpx flow run ACP node outputs return empty strings instead of agent replies
- v6b GPT / Opus: `['acpx']` / `['acp', 'acpx']`
- v6d GPT / Opus: `['acpx']` / `['acp', 'acpx']`
- v6d status: `deferred`; reasons: `['gpt_opus_modal_disagreement']`; jaccard: `0.5`

### openclaw-openclaw-84740

- Title: Feature Request: Option to hide/suppress certain sessions from the session list
- v6b GPT / Opus: `['sessions', 'ui_tui']` / `['config', 'sessions', 'ui_tui']`
- v6d GPT / Opus: `['sessions', 'ui_tui']` / `['config', 'sessions', 'ui_tui']`
- v6d status: `deferred`; reasons: `['gpt_opus_modal_disagreement']`; jaccard: `0.6666666666666666`

### openclaw-openclaw-84771

- Title: Event loop saturation during startup: synchronous model-prewarm and session-locks block event loop for 28-64 seconds
- v6b GPT / Opus: `['agent_runtime', 'gateway', 'reliability', 'sessions']` / `['agent_runtime', 'gateway', 'reliability', 'sessions']`
- v6d GPT / Opus: `['agent_runtime', 'reliability', 'sessions']` / `['agent_runtime', 'gateway', 'reliability', 'sessions']`
- v6d status: `deferred`; reasons: `['gpt_unstable', 'gpt_opus_modal_disagreement']`; jaccard: `0.75`

### openclaw-openclaw-10467

- Title: [Feature Request]: Multi-lane concurrency support for sub-agents via sessions_spawn
- v6b GPT / Opus: `['agent_runtime', 'config', 'queueing', 'tool_calling']` / `['agent_runtime', 'config', 'queueing']`
- v6d GPT / Opus: `['acp', 'agent_runtime', 'config', 'queueing', 'tool_calling']` / `['agent_runtime', 'config', 'queueing']`
- v6d status: `deferred`; reasons: `['gpt_unstable', 'gpt_opus_modal_disagreement']`; jaccard: `0.6`

### openclaw-openclaw-39248

- Title: Bug: sandbox.mode: "non-main" silently breaks sessions_spawn subagent initialization
- v6b GPT / Opus: `['agent_runtime', 'reliability', 'sandboxing', 'sessions']` / `['agent_runtime', 'reliability', 'sandboxing']`
- v6d GPT / Opus: `['agent_runtime', 'reliability', 'sandboxing', 'sessions']` / `['agent_runtime', 'reliability', 'sandboxing']`
- v6d status: `deferred`; reasons: `['gpt_opus_modal_disagreement']`; jaccard: `0.75`

### openclaw-openclaw-40332

- Title: [Feature]: Per-binding and per-agent permissionMode for ACP sessions
- v6b GPT / Opus: `['acp', 'acpx', 'approvals', 'config', 'security']` / `['acp', 'acpx', 'approvals', 'config']`
- v6d GPT / Opus: `['acp', 'acpx', 'approvals', 'config', 'security']` / `['acp', 'acpx', 'approvals', 'config']`
- v6d status: `deferred`; reasons: `['gpt_opus_modal_disagreement']`; jaccard: `0.8`

### openclaw-openclaw-44379

- Title: fix(pi-runner): harden context-overflow recovery with one suppress-hook retry
- v6b GPT / Opus: `['coding_agent_integrations', 'hooks', 'reliability']` / `['agent_runtime', 'reliability']`
- v6d GPT / Opus: `['coding_agent_integrations', 'hooks', 'reliability']` / `['agent_runtime', 'reliability']`
- v6d status: `deferred`; reasons: `['gpt_opus_modal_disagreement']`; jaccard: `0.25`

### openclaw-openclaw-48406

- Title: Docs: add saturated session recovery guide
- v6b GPT / Opus: `['config', 'docs', 'reliability', 'sessions']` / `['docs', 'reliability', 'sessions']`
- v6d GPT / Opus: `['config', 'docs', 'reliability', 'sessions']` / `['config', 'docs', 'reliability']`
- v6d status: `deferred`; reasons: `['gpt_unstable', 'opus_flagged_human_review', 'gpt_opus_modal_disagreement']`; jaccard: `0.75`

### openclaw-openclaw-48580

- Title: Bug: acpx codex sessions 创建的会话立即退出 - stdin is not a terminal
- v6b GPT / Opus: `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']` / `['acpx', 'codex', 'reliability', 'sessions']`
- v6d GPT / Opus: `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']` / `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']`
- v6d status: `accepted_consensus`; reasons: `[]`; jaccard: `1.0`

### openclaw-openclaw-48851

- Title: feat(status): add API call count to session status and usage footer
- v6b GPT / Opus: `['sessions', 'telemetry_usage', 'ui_tui']` / `['sessions', 'telemetry_usage']`
- v6d GPT / Opus: `['sessions', 'telemetry_usage', 'ui_tui']` / `['sessions', 'telemetry_usage']`
- v6d status: `deferred`; reasons: `['gpt_opus_modal_disagreement']`; jaccard: `0.6666666666666666`

### openclaw-openclaw-51667

- Title: Feature: Native Audio Input for Omni-Modal Models (skip STT transcription)
- v6b GPT / Opus: `['config', 'inference_api', 'sessions']` / `['config', 'inference_api']`
- v6d GPT / Opus: `['config', 'inference_api', 'sessions']` / `['config', 'inference_api']`
- v6d status: `deferred`; reasons: `['gpt_opus_modal_disagreement']`; jaccard: `0.6666666666666666`

### openclaw-openclaw-58135

- Title: [Feature]: expose promptMode parameter in sessions_spawn for deterministic blank sub-agents
- v6b GPT / Opus: `['agent_runtime', 'sessions', 'tool_calling']` / `['agent_runtime', 'sessions']`
- v6d GPT / Opus: `['agent_runtime', 'tool_calling']` / `['agent_runtime']`
- v6d status: `deferred`; reasons: `['gpt_unstable', 'gpt_opus_modal_disagreement']`; jaccard: `0.5`

### openclaw-openclaw-60737

- Title: [Feature]: Per-DM/per-chat default ACP binding for auto-spawning ACP sessions on new topics
- v6b GPT / Opus: `['acp', 'chat_integrations', 'config', 'sessions']` / `['acp', 'chat_integrations', 'config']`
- v6d GPT / Opus: `['acp', 'chat_integrations', 'config']` / `['acp', 'chat_integrations', 'config']`
- v6d status: `deferred`; reasons: `['gpt_unstable']`; jaccard: `1.0`

### openclaw-openclaw-82880

- Title: security: harden ACPX proxy and Firecrawl SSRF protection
- v6b GPT / Opus: `['acpx', 'config', 'exec_tools', 'security']` / `['acpx', 'security']`
- v6d GPT / Opus: `['acpx', 'config', 'exec_tools', 'security']` / `['acpx', 'exec_tools', 'security']`
- v6d status: `deferred`; reasons: `['gpt_unstable', 'gpt_flagged_human_review', 'opus_unstable', 'gpt_opus_modal_disagreement']`; jaccard: `0.75`

### openclaw-openclaw-46740

- Title: ACP: classify silent acpx exits as backend unavailable
- v6b GPT / Opus: `['acp', 'acpx', 'reliability']` / `['acp', 'acpx', 'reliability']`
- v6d GPT / Opus: `['acpx', 'reliability']` / `['acp', 'acpx', 'reliability']`
- v6d status: `deferred`; reasons: `['gpt_opus_modal_disagreement']`; jaccard: `0.6666666666666666`
