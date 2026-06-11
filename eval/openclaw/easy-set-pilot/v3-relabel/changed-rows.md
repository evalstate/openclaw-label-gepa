# v3 relabel changes vs reviewed easy-final-v2

- rows: 157
- exact agreement: 153
- changed rows: 4
- non-strict/not-easy rows: 8

## Changed rows

### openclaw-openclaw-65242 / #65242 — fix: CompletionDeliveryGate to prevent duplicate ACP completion delivery

- bucket: `easy` confidence: `0.93` strict_easy: `True`
- current: `acp, coding_agents, notifications, reliability, sessions`
- v3_teacher: `acp, agent_runtime, sessions, notifications, reliability`
- fp vs current: `agent_runtime`
- fn vs current: `coding_agents`

### openclaw-openclaw-69669 / #69669 — ACP: keep thread-bound follow-ups parent-orchestrated by default, not raw pass-through

- bucket: `easy` confidence: `0.94` strict_easy: `True`
- current: `acp, sessions, coding_agents`
- v3_teacher: `acp, sessions, agent_runtime, coding_agents`
- fp vs current: `agent_runtime`
- fn vs current: ``

### openclaw-openclaw-72016 / #72016 — [Feature]: doctor api/extendability

- bucket: `medium` confidence: `0.86` strict_easy: `False`
- current: `skills_plugins, config, api_surface`
- v3_teacher: `skills_plugins, config`
- fp vs current: ``
- fn vs current: `api_surface`

### openclaw-openclaw-84697 / #84697 — Custom OpenAI-compatible provider with baseUrl without /v1 fails with cryptic 'incomplete terminal response' error

- bucket: `easy` confidence: `0.93` strict_easy: `True`
- current: `config, model_serving`
- v3_teacher: `config, model_serving, local_model_providers`
- fp vs current: `local_model_providers`
- fn vs current: ``

## Non-strict / not-easy rows

- openclaw-openclaw-43765 / #43765 — bucket `easy`, confidence `0.94`, strict `False`, labels `chat_integrations, cron_automation, exec_tools, gateway, reliability`
- openclaw-openclaw-53997 / #53997 — bucket `easy`, confidence `0.95`, strict `False`, labels `acpx, acp, reliability`
- openclaw-openclaw-56866 / #56866 — bucket `easy`, confidence `0.94`, strict `False`, labels `acp, chat_integrations, hooks, sessions`
- openclaw-openclaw-63826 / #63826 — bucket `easy`, confidence `0.96`, strict `False`, labels `security, skills_plugins, hooks, auth_identity, local_model_providers`
- openclaw-openclaw-68916 / #68916 — bucket `easy`, confidence `0.96`, strict `False`, labels `acp, sessions, reliability`
- openclaw-openclaw-72016 / #72016 — bucket `medium`, confidence `0.86`, strict `False`, labels `skills_plugins, config`
- openclaw-openclaw-84413 / #84413 — bucket `easy`, confidence `0.95`, strict `False`, labels `codex, gateway, mcp_tooling, reliability`
- openclaw-openclaw-84477 / #84477 — bucket `easy`, confidence `0.95`, strict `False`, labels `agent_runtime, chat_integrations, queueing, reliability, sessions`