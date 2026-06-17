# v6d GPT-5.5 prompt keyword audit vs v6b baseline

## old

```json
{
  "rows": 20,
  "stable_3of3": 20,
  "same_as_v6b_gpt": 20,
  "same_as_v6b_opus": 20
}
```

### old label counts

v6b GPT modal: `{'config': 4, 'ui_tui': 4, 'docs': 3, 'telemetry_usage': 3, 'chat_integrations': 3, 'security': 3, 'memory': 2, 'inference_api': 2, 'approvals': 2, 'mcp_tooling': 2, 'exec_tools': 2, 'reliability': 1, 'hooks': 1, 'skills_plugins': 1, 'notifications': 1, 'packaging_deployment': 1, 'tests_ci': 1, 'queueing': 1, 'api_surface': 1, 'gateway': 1, 'auth_identity': 1}`

v6d GPT modal: `{'config': 4, 'ui_tui': 4, 'docs': 3, 'telemetry_usage': 3, 'chat_integrations': 3, 'security': 3, 'memory': 2, 'inference_api': 2, 'approvals': 2, 'mcp_tooling': 2, 'exec_tools': 2, 'reliability': 1, 'hooks': 1, 'skills_plugins': 1, 'notifications': 1, 'packaging_deployment': 1, 'tests_ci': 1, 'queueing': 1, 'api_surface': 1, 'gateway': 1, 'auth_identity': 1}`

## confused

```json
{
  "rows": 20,
  "unstable": 8,
  "dropped_sessions_vs_gpt": 4,
  "stable_3of3": 12,
  "same_as_v6b_gpt": 12,
  "same_as_v6b_opus": 2,
  "stabilized_to_prior_modal": 10
}
```

### confused label counts

v6b GPT modal: `{'sessions': 12, 'acp': 7, 'acpx': 6, 'reliability': 6, 'config': 6, 'security': 4, 'agent_runtime': 4, 'coding_agent_integrations': 3, 'tool_calling': 3, 'telemetry_usage': 2, 'ui_tui': 2, 'skills_plugins': 1, 'notifications': 1, 'gateway': 1, 'queueing': 1, 'sandboxing': 1, 'approvals': 1, 'hooks': 1, 'docs': 1, 'codex': 1, 'inference_api': 1, 'chat_integrations': 1, 'exec_tools': 1}`

v6d GPT modal: `{'sessions': 8, 'acp': 6, 'acpx': 6, 'reliability': 6, 'config': 6, 'security': 4, 'agent_runtime': 4, 'coding_agent_integrations': 3, 'tool_calling': 3, 'telemetry_usage': 2, 'ui_tui': 2, 'skills_plugins': 1, 'api_surface': 1, 'notifications': 1, 'queueing': 1, 'sandboxing': 1, 'approvals': 1, 'hooks': 1, 'docs': 1, 'codex': 1, 'inference_api': 1, 'chat_integrations': 1, 'exec_tools': 1}`

## Confused Row Detail

### openclaw-openclaw-43564

- Title: [Feature Request] ACP Session Skill Context Injection
- v6b GPT: `['acp', 'coding_agent_integrations', 'security', 'sessions', 'skills_plugins']`
- v6b Opus: `['acp', 'skills_plugins']`
- v6d GPT modal: `['acp', 'coding_agent_integrations', 'security', 'skills_plugins']` (2/3)
- v6d votes: `[['acp', 'coding_agent_integrations', 'security', 'skills_plugins'], ['acp', 'coding_agent_integrations', 'security', 'skills_plugins'], ['acp', 'api_surface', 'coding_agent_integrations', 'security', 'skills_plugins']]`
- v6b reasons: `['gpt_unstable', 'gpt_flagged_human_review', 'gpt_opus_modal_disagreement']`

### openclaw-openclaw-51654

- Title: Support session-level environment variables for ACP sessions
- v6b GPT: `['acp', 'acpx', 'security', 'sessions', 'tool_calling']`
- v6b Opus: `['acp', 'acpx', 'sessions']`
- v6d GPT modal: `['acpx', 'api_surface', 'security', 'sessions']` (1/3)
- v6d votes: `[['acpx', 'api_surface', 'security', 'sessions'], ['acp', 'acpx', 'security', 'sessions'], ['acp', 'acpx', 'api_surface', 'security', 'sessions']]`
- v6b reasons: `['gpt_unstable', 'gpt_opus_modal_disagreement']`

### openclaw-openclaw-54471

- Title: fix(acp): add system_event stream relay to parent session for ACP spawn
- v6b GPT: `['acp']`
- v6b Opus: `['acp']`
- v6d GPT modal: `['acp']` (3/3)
- v6d votes: `[['acp'], ['acp'], ['acp']]`
- v6b reasons: `['gpt_unstable']`

### openclaw-openclaw-56442

- Title: feat: Add opt-in ACP parent completion notify for sessions_spawn
- v6b GPT: `['acp', 'notifications', 'sessions']`
- v6b Opus: `['acp', 'notifications']`
- v6d GPT modal: `['acp', 'notifications', 'tool_calling']` (3/3)
- v6d votes: `[['acp', 'notifications', 'tool_calling'], ['acp', 'notifications', 'tool_calling'], ['acp', 'notifications', 'tool_calling']]`
- v6b reasons: `['gpt_unstable', 'opus_unstable', 'gpt_opus_modal_disagreement']`

### openclaw-openclaw-68204

- Title: Unified run trace schema across agent, ACP, subagent, and task flows
- v6b GPT: `['telemetry_usage']`
- v6b Opus: `['acp', 'agent_runtime', 'telemetry_usage']`
- v6d GPT modal: `['telemetry_usage']` (3/3)
- v6d votes: `[['telemetry_usage'], ['telemetry_usage'], ['telemetry_usage']]`
- v6b reasons: `['gpt_unstable', 'gpt_opus_modal_disagreement']`

### openclaw-openclaw-77694

- Title: [Bug]: acpx flow run ACP node outputs return empty strings instead of agent replies
- v6b GPT: `['acpx']`
- v6b Opus: `['acp', 'acpx']`
- v6d GPT modal: `['acpx']` (3/3)
- v6d votes: `[['acpx'], ['acpx'], ['acpx']]`
- v6b reasons: `['gpt_opus_modal_disagreement']`

### openclaw-openclaw-84740

- Title: Feature Request: Option to hide/suppress certain sessions from the session list
- v6b GPT: `['sessions', 'ui_tui']`
- v6b Opus: `['config', 'sessions', 'ui_tui']`
- v6d GPT modal: `['sessions', 'ui_tui']` (3/3)
- v6d votes: `[['sessions', 'ui_tui'], ['sessions', 'ui_tui'], ['sessions', 'ui_tui']]`
- v6b reasons: `['gpt_opus_modal_disagreement']`

### openclaw-openclaw-84771

- Title: Event loop saturation during startup: synchronous model-prewarm and session-locks block event loop for 28-64 seconds
- v6b GPT: `['agent_runtime', 'gateway', 'reliability', 'sessions']`
- v6b Opus: `['agent_runtime', 'gateway', 'reliability', 'sessions']`
- v6d GPT modal: `['agent_runtime', 'reliability', 'sessions']` (1/3)
- v6d votes: `[['agent_runtime', 'reliability', 'sessions'], ['agent_runtime', 'gateway', 'reliability', 'sessions'], ['gateway', 'reliability', 'sessions']]`
- v6b reasons: `['gpt_unstable']`

### openclaw-openclaw-10467

- Title: [Feature Request]: Multi-lane concurrency support for sub-agents via sessions_spawn
- v6b GPT: `['agent_runtime', 'config', 'queueing', 'tool_calling']`
- v6b Opus: `['agent_runtime', 'config', 'queueing']`
- v6d GPT modal: `['acp', 'agent_runtime', 'config', 'queueing', 'tool_calling']` (2/3)
- v6d votes: `[['acp', 'agent_runtime', 'config', 'queueing', 'tool_calling'], ['agent_runtime', 'config', 'queueing', 'tool_calling'], ['acp', 'agent_runtime', 'config', 'queueing', 'tool_calling']]`
- v6b reasons: `['gpt_unstable', 'gpt_opus_modal_disagreement']`

### openclaw-openclaw-39248

- Title: Bug: sandbox.mode: "non-main" silently breaks sessions_spawn subagent initialization
- v6b GPT: `['agent_runtime', 'reliability', 'sandboxing', 'sessions']`
- v6b Opus: `['agent_runtime', 'reliability', 'sandboxing']`
- v6d GPT modal: `['agent_runtime', 'reliability', 'sandboxing', 'sessions']` (3/3)
- v6d votes: `[['agent_runtime', 'reliability', 'sandboxing', 'sessions'], ['agent_runtime', 'reliability', 'sandboxing', 'sessions'], ['agent_runtime', 'reliability', 'sandboxing', 'sessions']]`
- v6b reasons: `['gpt_opus_modal_disagreement']`

### openclaw-openclaw-40332

- Title: [Feature]: Per-binding and per-agent permissionMode for ACP sessions
- v6b GPT: `['acp', 'acpx', 'approvals', 'config', 'security']`
- v6b Opus: `['acp', 'acpx', 'approvals', 'config']`
- v6d GPT modal: `['acp', 'acpx', 'approvals', 'config', 'security']` (3/3)
- v6d votes: `[['acp', 'acpx', 'approvals', 'config', 'security'], ['acp', 'acpx', 'approvals', 'config', 'security'], ['acp', 'acpx', 'approvals', 'config', 'security']]`
- v6b reasons: `['opus_unstable', 'gpt_opus_modal_disagreement']`

### openclaw-openclaw-44379

- Title: fix(pi-runner): harden context-overflow recovery with one suppress-hook retry
- v6b GPT: `['coding_agent_integrations', 'hooks', 'reliability']`
- v6b Opus: `['agent_runtime', 'reliability']`
- v6d GPT modal: `['coding_agent_integrations', 'hooks', 'reliability']` (3/3)
- v6d votes: `[['coding_agent_integrations', 'hooks', 'reliability'], ['coding_agent_integrations', 'hooks', 'reliability'], ['coding_agent_integrations', 'hooks', 'reliability']]`
- v6b reasons: `['gpt_unstable', 'gpt_opus_modal_disagreement']`

### openclaw-openclaw-48406

- Title: Docs: add saturated session recovery guide
- v6b GPT: `['config', 'docs', 'reliability', 'sessions']`
- v6b Opus: `['docs', 'reliability', 'sessions']`
- v6d GPT modal: `['config', 'docs', 'reliability', 'sessions']` (1/3)
- v6d votes: `[['config', 'docs', 'reliability', 'sessions'], ['agent_runtime', 'config', 'docs', 'reliability'], ['config', 'docs', 'reliability']]`
- v6b reasons: `['opus_flagged_human_review', 'gpt_opus_modal_disagreement']`

### openclaw-openclaw-48580

- Title: Bug: acpx codex sessions 创建的会话立即退出 - stdin is not a terminal
- v6b GPT: `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']`
- v6b Opus: `['acpx', 'codex', 'reliability', 'sessions']`
- v6d GPT modal: `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']` (3/3)
- v6d votes: `[['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions'], ['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions'], ['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']]`
- v6b reasons: `['gpt_opus_modal_disagreement']`

### openclaw-openclaw-48851

- Title: feat(status): add API call count to session status and usage footer
- v6b GPT: `['sessions', 'telemetry_usage', 'ui_tui']`
- v6b Opus: `['sessions', 'telemetry_usage']`
- v6d GPT modal: `['sessions', 'telemetry_usage', 'ui_tui']` (3/3)
- v6d votes: `[['sessions', 'telemetry_usage', 'ui_tui'], ['sessions', 'telemetry_usage', 'ui_tui'], ['sessions', 'telemetry_usage', 'ui_tui']]`
- v6b reasons: `['opus_unstable', 'gpt_opus_modal_disagreement']`

### openclaw-openclaw-51667

- Title: Feature: Native Audio Input for Omni-Modal Models (skip STT transcription)
- v6b GPT: `['config', 'inference_api', 'sessions']`
- v6b Opus: `['config', 'inference_api']`
- v6d GPT modal: `['config', 'inference_api', 'sessions']` (3/3)
- v6d votes: `[['config', 'inference_api', 'sessions'], ['config', 'inference_api', 'sessions'], ['config', 'inference_api', 'sessions']]`
- v6b reasons: `['gpt_opus_modal_disagreement']`

### openclaw-openclaw-58135

- Title: [Feature]: expose promptMode parameter in sessions_spawn for deterministic blank sub-agents
- v6b GPT: `['agent_runtime', 'sessions', 'tool_calling']`
- v6b Opus: `['agent_runtime', 'sessions']`
- v6d GPT modal: `['agent_runtime', 'tool_calling']` (2/3)
- v6d votes: `[['agent_runtime', 'tool_calling'], ['agent_runtime', 'sessions', 'tool_calling'], ['agent_runtime', 'tool_calling']]`
- v6b reasons: `['gpt_unstable', 'opus_unstable', 'gpt_opus_modal_disagreement']`

### openclaw-openclaw-60737

- Title: [Feature]: Per-DM/per-chat default ACP binding for auto-spawning ACP sessions on new topics
- v6b GPT: `['acp', 'chat_integrations', 'config', 'sessions']`
- v6b Opus: `['acp', 'chat_integrations', 'config']`
- v6d GPT modal: `['acp', 'chat_integrations', 'config']` (2/3)
- v6d votes: `[['acp', 'chat_integrations', 'config'], ['acp', 'chat_integrations', 'config'], ['acp', 'chat_integrations', 'config', 'sessions']]`
- v6b reasons: `['gpt_opus_modal_disagreement']`

### openclaw-openclaw-82880

- Title: security: harden ACPX proxy and Firecrawl SSRF protection
- v6b GPT: `['acpx', 'config', 'exec_tools', 'security']`
- v6b Opus: `['acpx', 'security']`
- v6d GPT modal: `['acpx', 'config', 'exec_tools', 'security']` (2/3)
- v6d votes: `[['acpx', 'config', 'exec_tools', 'security'], ['acpx', 'config', 'exec_tools', 'mcp_tooling', 'security'], ['acpx', 'config', 'exec_tools', 'security']]`
- v6b reasons: `['gpt_opus_modal_disagreement']`

### openclaw-openclaw-46740

- Title: ACP: classify silent acpx exits as backend unavailable
- v6b GPT: `['acp', 'acpx', 'reliability']`
- v6b Opus: `['acp', 'acpx', 'reliability']`
- v6d GPT modal: `['acpx', 'reliability']` (3/3)
- v6d votes: `[['acpx', 'reliability'], ['acpx', 'reliability'], ['acpx', 'reliability']]`
- v6b reasons: `['gpt_unstable']`
