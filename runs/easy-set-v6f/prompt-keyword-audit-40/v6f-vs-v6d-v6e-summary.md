# v6f full-40 label-only comparison

Input: `runs/easy-set-v6f/prompt-keyword-audit-40/input.jsonl` (same 40 items used by v6d/v6e prompt-keyword audit).

| variant | accepted | deferred | GPT stable | Opus stable | GPT/Opus exact modal | mean Jaccard | 5-label modal rows |
|---|---:|---:|---:|---:|---:|---:|---:|
| v6d_current_edited_prompt | 20 | 20 | 32 | 37 | 23 | 0.845 | 3 |
| v6e_with_eligibility_overlay | 18 | 22 | 32 | 34 | 23 | 0.849 | 5 |
| v6f_current_label_only | 22 | 18 | 32 | 34 | 27 | 0.870 | 2 |

## Review reasons

- `v6d_current_edited_prompt`: `{"gpt_flagged_human_review": 2, "gpt_opus_modal_disagreement": 17, "gpt_unstable": 8, "opus_flagged_human_review": 3, "opus_unstable": 3}`
- `v6e_with_eligibility_overlay`: `{"gpt_flagged_human_review": 10, "gpt_opus_modal_disagreement": 17, "gpt_unstable": 8, "opus_flagged_human_review": 6, "opus_unstable": 6}`
- `v6f_current_label_only`: `{"gpt_flagged_human_review": 2, "gpt_opus_modal_disagreement": 13, "gpt_unstable": 8, "opus_flagged_human_review": 1, "opus_unstable": 6}`

## Status changes versus v6d

### v6e_with_eligibility_overlay
- `openclaw-openclaw-47083` #47083: accepted_consensus `['telemetry_usage', 'ui_tui']` -> deferred `[]`; GPT modal `['telemetry_usage', 'ui_tui']`, Opus modal `['telemetry_usage', 'ui_tui']`, reasons `['gpt_unstable', 'opus_unstable']`
- `openclaw-openclaw-59208` #59208: accepted_consensus `['auth_identity', 'telemetry_usage']` -> deferred `[]`; GPT modal `['auth_identity', 'telemetry_usage']`, Opus modal `['auth_identity', 'telemetry_usage']`, reasons `['gpt_flagged_human_review']`
- `openclaw-openclaw-48580` #48580: accepted_consensus `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']` -> deferred `[]`; GPT modal `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']`, Opus modal `['acpx', 'codex', 'reliability', 'sessions']`, reasons `['gpt_flagged_human_review', 'opus_flagged_human_review', 'gpt_opus_modal_disagreement']`
- `openclaw-openclaw-60737` #60737: deferred `[]` -> accepted_consensus `['acp', 'chat_integrations', 'config']`; GPT modal `['acp', 'chat_integrations', 'config']`, Opus modal `['acp', 'chat_integrations', 'config']`, reasons `[]`

### v6f_current_label_only
- `openclaw-openclaw-71646` #71646: deferred `[]` -> accepted_consensus `['approvals', 'mcp_tooling', 'reliability']`; GPT modal `['approvals', 'mcp_tooling', 'reliability']`, Opus modal `['approvals', 'mcp_tooling', 'reliability']`, reasons `[]`
- `openclaw-openclaw-82642` #82642: accepted_consensus `['chat_integrations', 'notifications']` -> deferred `[]`; GPT modal `['chat_integrations']`, Opus modal `['chat_integrations', 'notifications']`, reasons `['gpt_unstable', 'gpt_opus_modal_disagreement']`
- `openclaw-openclaw-51654` #51654: deferred `[]` -> accepted_consensus `['acp', 'acpx', 'security', 'tool_calling']`; GPT modal `['acp', 'acpx', 'security', 'tool_calling']`, Opus modal `['acp', 'acpx', 'security', 'tool_calling']`, reasons `[]`
- `openclaw-openclaw-54471` #54471: accepted_consensus `['acp']` -> deferred `[]`; GPT modal `['acp']`, Opus modal `['acp']`, reasons `['gpt_unstable']`
- `openclaw-openclaw-48580` #48580: accepted_consensus `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']` -> deferred `[]`; GPT modal `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']`, Opus modal `['acpx', 'codex', 'reliability', 'sessions']`, reasons `['gpt_opus_modal_disagreement']`
- `openclaw-openclaw-48851` #48851: deferred `[]` -> accepted_consensus `['sessions', 'telemetry_usage', 'ui_tui']`; GPT modal `['sessions', 'telemetry_usage', 'ui_tui']`, Opus modal `['sessions', 'telemetry_usage', 'ui_tui']`, reasons `[]`
- `openclaw-openclaw-58135` #58135: deferred `[]` -> accepted_consensus `['agent_runtime', 'tool_calling']`; GPT modal `['agent_runtime', 'tool_calling']`, Opus modal `['agent_runtime', 'tool_calling']`, reasons `[]`
- `openclaw-openclaw-60737` #60737: deferred `[]` -> accepted_consensus `['acp', 'chat_integrations', 'config']`; GPT modal `['acp', 'chat_integrations', 'config']`, Opus modal `['acp', 'chat_integrations', 'config']`, reasons `[]`

## v6f accepted rows

- `openclaw-openclaw-42408` #42408: `['config', 'docs', 'memory']` [Bug/Docs]: local+hybrid memory_search quality can appear unstable due to extraPaths path drift + benchmark-file contamination
- `openclaw-openclaw-43416` #43416: `['ui_tui']` feat(ui): add copy button for assistant messages
- `openclaw-openclaw-47083` #47083: `['telemetry_usage', 'ui_tui']` fix: respect totalTokensFresh flag to avoid showing stale token counts
- `openclaw-openclaw-48877` #48877: `['chat_integrations', 'config']` feat(telegram): add multi-level menu support to customCommands
- `openclaw-openclaw-51849` #51849: `['docs']` Docs: add freeCodeCamp OpenClaw full tutorial to showcase
- `openclaw-openclaw-71646` #71646: `['approvals', 'mcp_tooling', 'reliability']` mcp/channel-bridge: pendingClaudePermissions / pendingApprovals leak — no TTL, no close-clear, no cap
- `openclaw-openclaw-71976` #71976: `['memory']` Memory Dreaming: Light sleep sort prioritizes recency over recallCount, hiding real recall data
- `openclaw-openclaw-72138` #72138: `['chat_integrations', 'hooks']` fix(feishu): emit sent hooks for normal replies
- `openclaw-openclaw-76724` #76724: `['mcp_tooling']` [Bug]: MCP tools not discovered by Agent despite successful handshake (200 OK)
- `openclaw-openclaw-78528` #78528: `['exec_tools', 'security', 'skills_plugins']` Security: skill SecretRef API keys still leak into exec child environments
- `openclaw-openclaw-81488` #81488: `['approvals', 'exec_tools', 'security']` Harden node exec approval precheck env [AI]
- `openclaw-openclaw-84385` #84385: `['ui_tui']` [codex] Fix macOS app copyright year
- `openclaw-openclaw-84761` #84761: `['security']` feat(secrets): scan backup files for plaintext provider apiKey values
- `openclaw-openclaw-88400` #88400: `['config', 'inference_api']` fix(config): accept overlays for bundled provider aliases
- `openclaw-openclaw-42122` #42122: `['packaging_deployment', 'tests_ci']` Speed up install smoke Docker builds
- `openclaw-openclaw-46552` #46552: `['docs', 'queueing']` docs(queue): clarify steer behavior with partial streaming and tool boundaries
- `openclaw-openclaw-49502` #49502: `['api_surface', 'gateway', 'telemetry_usage']` feat(gateway): include usage/cost metadata in agent.wait terminal response
- `openclaw-openclaw-59208` #59208: `['auth_identity', 'telemetry_usage']` fix(status): honor selected usage auth profile
- `openclaw-openclaw-51654` #51654: `['acp', 'acpx', 'security', 'tool_calling']` Support session-level environment variables for ACP sessions
- `openclaw-openclaw-48851` #48851: `['sessions', 'telemetry_usage', 'ui_tui']` feat(status): add API call count to session status and usage footer
- `openclaw-openclaw-58135` #58135: `['agent_runtime', 'tool_calling']` [Feature]: expose promptMode parameter in sessions_spawn for deterministic blank sub-agents
- `openclaw-openclaw-60737` #60737: `['acp', 'chat_integrations', 'config']` [Feature]: Per-DM/per-chat default ACP binding for auto-spawning ACP sessions on new topics
