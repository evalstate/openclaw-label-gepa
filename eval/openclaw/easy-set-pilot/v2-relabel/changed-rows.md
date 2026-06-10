# v2 relabel changed rows

- rows: 178
- changed: 10
- avg_jaccard: 0.980
- avg_symdiff: 0.090

## #10467 openclaw-openclaw-10467 — [Feature Request]: Multi-lane concurrency support for sub-agents via sessions_spawn

- old: `coding_agents, sessions, queueing, config`
- new: `agent_runtime, sessions, queueing, config, acp`
- added: `acp, agent_runtime`
- dropped: `coding_agents`
- jaccard: `0.500`; symdiff: `3`; confidence: `0.94`

## #45200 openclaw-openclaw-45200 — fix(subagents): notify user on announce give-up instead of silently dropping result

- old: `coding_agents, notifications, reliability`
- new: `agent_runtime, notifications, reliability`
- added: `agent_runtime`
- dropped: `coding_agents`
- jaccard: `0.500`; symdiff: `2`; confidence: `0.94`

## #58135 openclaw-openclaw-58135 — [Feature]: expose promptMode parameter in sessions_spawn for deterministic blank sub-agents

- old: `acp, api_surface, coding_agents, sessions`
- new: `acp, api_surface, agent_runtime, sessions`
- added: `agent_runtime`
- dropped: `coding_agents`
- jaccard: `0.600`; symdiff: `2`; confidence: `0.94`

## #80255 openclaw-openclaw-80255 — fix #79026: active-memory recall subagent can deadlock on the main lane inside before_prompt_build

- old: `coding_agents, memory, queueing, reliability`
- new: `memory, agent_runtime, queueing, reliability`
- added: `agent_runtime`
- dropped: `coding_agents`
- jaccard: `0.600`; symdiff: `2`; confidence: `0.94`

## #87277 openclaw-openclaw-87277 — [Feature] Add MiMo-V2.5 to Xiaomi catalog + automatic multimodal routing when DeepSeek V4-Pro is primary model

- old: `model_releases, model_serving, reliability`
- new: `model_releases, config, model_serving`
- added: `config`
- dropped: `reliability`
- jaccard: `0.500`; symdiff: `2`; confidence: `0.93`

## #79447 openclaw-openclaw-79447 — fix(model-auth): resolve per-entry apiKey profile ID references

- old: `auth_identity, config, local_model_providers`
- new: `auth_identity, config`
- added: ``
- dropped: `local_model_providers`
- jaccard: `0.667`; symdiff: `1`; confidence: `0.94`

## #84316 openclaw-openclaw-84316 — [Bug]: Telegram group TTS for sub-agent reports success in /tts status but voice never delivered (2026.5.12)

- old: `chat_integrations, coding_agents, notifications, reliability`
- new: `chat_integrations, notifications, reliability`
- added: ``
- dropped: `coding_agents`
- jaccard: `0.750`; symdiff: `1`; confidence: `0.94`

## #84706 openclaw-openclaw-84706 — [Bug]: subagent spawn validation rejects every non-off thinking level on all canonical openai/* models — error cites canonical alias even when openai-codex/* is requested

- old: `api_surface, codex, coding_agents, sessions`
- new: `api_surface, codex, coding_agents, config, sessions`
- added: `config`
- dropped: ``
- jaccard: `0.800`; symdiff: `1`; confidence: `0.91`

## #85660 openclaw-openclaw-85660 — GitHub Copilot plugin: agents.defaults.imageModel for unknown Copilot model ID falls back to OpenAI provider with confusing 401

- old: `config, security, skills_plugins`
- new: `config, skills_plugins, model_serving, security`
- added: `model_serving`
- dropped: ``
- jaccard: `0.750`; symdiff: `1`; confidence: `0.91`

## #90146 openclaw-openclaw-90146 — google-vertex: Missing gemini-3.1-flash-lite in provider catalog causes silent failure instead of error

- old: `agent_runtime, model_releases, reliability`
- new: `config, reliability, agent_runtime, model_releases`
- added: `config`
- dropped: ``
- jaccard: `0.750`; symdiff: `1`; confidence: `0.86`
