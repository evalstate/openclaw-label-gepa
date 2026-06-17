# easy-final-v2 instability mining
Completed stability runs: 8

## Least stable test rows across completed stability reruns

### 1. openclaw-openclaw-83863 — pairwise=0.530, exact=0.000, avgJ=0.490, sym=3.50, unique=8/8
Title: ACP/Codex child tasks can be marked succeeded with progress-only output and no final deliverable

Expected: `['acp', 'agent_runtime', 'codex', 'coding_agents', 'reliability']`

Most common predictions: `[(['acp', 'codex', 'notifications', 'reliability', 'sessions'], 1), (['acp', 'agent_runtime', 'codex', 'reliability', 'sessions'], 1), (['acp', 'agent_runtime', 'codex', 'notifications', 'reliability'], 1)]`

Volatile topics: `[('sessions', 6), ('notifications', 5), ('codex', 4), ('coding_agents', 4), ('agent_runtime', 2), ('queueing', 2), ('ui_tui', 1)]`

FP: `[('sessions', 6), ('notifications', 5), ('queueing', 2), ('ui_tui', 1)]`

FN: `[('agent_runtime', 6), ('coding_agents', 4), ('codex', 4)]`

By model:
- deepseek4: `[['acp', 'coding_agents', 'reliability', 'sessions'], ['acp', 'codex', 'reliability', 'sessions', 'ui_tui']]`
- gpt-5.4-mini: `[['acp', 'codex', 'notifications', 'reliability', 'sessions'], ['acp', 'agent_runtime', 'codex', 'reliability', 'sessions'], ['acp', 'agent_runtime', 'codex', 'notifications', 'reliability']]`
- sonnet: `[['acp', 'coding_agents', 'notifications', 'queueing', 'reliability'], ['acp', 'coding_agents', 'notifications', 'queueing', 'reliability', 'sessions'], ['acp', 'coding_agents', 'notifications', 'reliability', 'sessions']]`

### 2. openclaw-openclaw-70002 — pairwise=0.536, exact=0.500, avgJ=0.688, sym=0.62, unique=3/8
Title: ci: skip docs sync & translate-trigger workflows in forks

Expected: `['tests_ci']`

Most common predictions: `[(['tests_ci'], 4), (['reliability', 'tests_ci'], 3), (['docs'], 1)]`

Volatile topics: `[('tests_ci', 7), ('reliability', 3), ('docs', 1)]`

FP: `[('reliability', 3), ('docs', 1)]`

FN: `[('tests_ci', 1)]`

By model:
- deepseek4: `[['tests_ci'], ['docs']]`
- gpt-5.4-mini: `[['reliability', 'tests_ci'], ['reliability', 'tests_ci'], ['reliability', 'tests_ci']]`
- sonnet: `[['tests_ci'], ['tests_ci'], ['tests_ci']]`

### 3. openclaw-openclaw-84697 — pairwise=0.545, exact=0.250, avgJ=0.677, sym=1.12, unique=5/8
Title: Custom OpenAI-compatible provider with baseUrl without /v1 fails with cryptic 'incomplete terminal response' error

Expected: `['config', 'local_model_providers', 'model_serving']`

Most common predictions: `[(['config', 'local_model_providers', 'model_serving'], 2), (['config', 'local_model_providers'], 2), (['local_model_providers', 'model_serving', 'reliability'], 2)]`

Volatile topics: `[('config', 5), ('model_serving', 5), ('reliability', 3)]`

FP: `[('reliability', 3)]`

FN: `[('model_serving', 3), ('config', 3)]`

By model:
- deepseek4: `[['local_model_providers'], ['config', 'local_model_providers']]`
- gpt-5.4-mini: `[['config', 'local_model_providers', 'model_serving'], ['config', 'local_model_providers'], ['config', 'local_model_providers', 'model_serving']]`
- sonnet: `[['config', 'local_model_providers', 'model_serving', 'reliability'], ['local_model_providers', 'model_serving', 'reliability'], ['local_model_providers', 'model_serving', 'reliability']]`

### 4. openclaw-openclaw-70518 — pairwise=0.569, exact=0.375, avgJ=0.727, sym=1.12, unique=6/8
Title: fix(config): add heartbeat skill allowlist

Expected: `['config', 'cron_automation', 'skills_plugins']`

Most common predictions: `[(['config', 'cron_automation', 'skills_plugins'], 3), (['config', 'gateway', 'skills_plugins'], 1), (['config', 'skills_plugins'], 1)]`

Volatile topics: `[('cron_automation', 6), ('skills_plugins', 6), ('docs', 3), ('agent_runtime', 1), ('gateway', 1)]`

FP: `[('docs', 3), ('gateway', 1), ('agent_runtime', 1)]`

FN: `[('cron_automation', 2), ('skills_plugins', 2)]`

By model:
- deepseek4: `[['config', 'cron_automation', 'docs'], ['agent_runtime', 'config', 'cron_automation', 'docs']]`
- gpt-5.4-mini: `[['config', 'gateway', 'skills_plugins'], ['config', 'cron_automation', 'skills_plugins'], ['config', 'skills_plugins']]`
- sonnet: `[['config', 'cron_automation', 'skills_plugins'], ['config', 'cron_automation', 'skills_plugins'], ['config', 'cron_automation', 'docs', 'skills_plugins']]`

### 5. openclaw-openclaw-87277 — pairwise=0.584, exact=0.000, avgJ=0.562, sym=1.62, unique=5/8
Title: [Feature] Add MiMo-V2.5 to Xiaomi catalog + automatic multimodal routing when DeepSeek V4-Pro is primary model

Expected: `['config', 'model_releases', 'model_serving']`

Most common predictions: `[(['config', 'model_serving'], 3), (['config', 'model_serving', 'open_weight_models'], 2), (['config', 'model_serving', 'reliability'], 1)]`

Volatile topics: `[('model_serving', 7), ('open_weight_models', 3), ('agent_runtime', 1), ('model_releases', 1), ('reliability', 1)]`

FP: `[('open_weight_models', 3), ('reliability', 1), ('agent_runtime', 1)]`

FN: `[('model_releases', 7), ('model_serving', 1)]`

By model:
- deepseek4: `[['agent_runtime', 'config'], ['config', 'model_serving']]`
- gpt-5.4-mini: `[['config', 'model_serving'], ['config', 'model_serving', 'reliability'], ['config', 'model_serving']]`
- sonnet: `[['config', 'model_releases', 'model_serving', 'open_weight_models'], ['config', 'model_serving', 'open_weight_models'], ['config', 'model_serving', 'open_weight_models']]`

### 6. openclaw-openclaw-85660 — pairwise=0.611, exact=0.125, avgJ=0.738, sym=1.12, unique=5/8
Title: GitHub Copilot plugin: agents.defaults.imageModel for unknown Copilot model ID falls back to OpenAI provider with confusing 401

Expected: `['config', 'model_serving', 'security', 'skills_plugins']`

Most common predictions: `[(['config', 'security', 'skills_plugins'], 3), (['config', 'model_serving', 'security'], 2), (['auth_identity', 'config', 'security'], 1)]`

Volatile topics: `[('security', 7), ('skills_plugins', 5), ('model_serving', 4), ('auth_identity', 1)]`

FP: `[('auth_identity', 1)]`

FN: `[('model_serving', 4), ('skills_plugins', 3), ('security', 1)]`

By model:
- deepseek4: `[['config', 'model_serving', 'security'], ['config', 'model_serving', 'security', 'skills_plugins']]`
- gpt-5.4-mini: `[['auth_identity', 'config', 'security'], ['config', 'model_serving', 'security'], ['config', 'model_serving', 'skills_plugins']]`
- sonnet: `[['config', 'security', 'skills_plugins'], ['config', 'security', 'skills_plugins'], ['config', 'security', 'skills_plugins']]`

### 7. openclaw-openclaw-74204 — pairwise=0.621, exact=0.000, avgJ=0.738, sym=1.25, unique=5/8
Title: memory.qmd.update.embedTimeoutMs default (120 s) is too low for local GGUF; error message doesn't surface the fix

Expected: `['config', 'local_models', 'memory', 'reliability']`

Most common predictions: `[(['config', 'memory', 'reliability'], 3), (['config', 'local_models', 'memory', 'reliability', 'self_hosted_inference'], 2), (['config', 'local_models', 'memory'], 1)]`

Volatile topics: `[('reliability', 6), ('local_models', 5), ('self_hosted_inference', 3), ('docs', 1), ('open_weight_models', 1)]`

FP: `[('self_hosted_inference', 3), ('docs', 1), ('open_weight_models', 1)]`

FN: `[('local_models', 3), ('reliability', 2)]`

By model:
- deepseek4: `[['config', 'docs', 'local_models', 'memory', 'reliability'], ['config', 'local_models', 'memory', 'open_weight_models', 'self_hosted_inference']]`
- gpt-5.4-mini: `[['config', 'memory', 'reliability'], ['config', 'memory', 'reliability'], ['config', 'memory', 'reliability']]`
- sonnet: `[['config', 'local_models', 'memory'], ['config', 'local_models', 'memory', 'reliability', 'self_hosted_inference'], ['config', 'local_models', 'memory', 'reliability', 'self_hosted_inference']]`

### 8. openclaw-openclaw-72085 — pairwise=0.637, exact=0.375, avgJ=0.771, sym=0.62, unique=4/8
Title: docs(commands): document bashForegroundMs clamp bounds (0–30 000 ms)

Expected: `['config', 'docs']`

Most common predictions: `[(['config', 'docs'], 3), (['config', 'docs', 'gateway'], 2), (['config', 'docs', 'exec_tools'], 2)]`

Volatile topics: `[('config', 7), ('exec_tools', 2), ('gateway', 2)]`

FP: `[('gateway', 2), ('exec_tools', 2)]`

FN: `[('config', 1)]`

By model:
- deepseek4: `[['docs'], ['config', 'docs', 'exec_tools']]`
- gpt-5.4-mini: `[['config', 'docs', 'gateway'], ['config', 'docs', 'gateway'], ['config', 'docs']]`
- sonnet: `[['config', 'docs'], ['config', 'docs'], ['config', 'docs', 'exec_tools']]`

### 9. openclaw-openclaw-84753 — pairwise=0.651, exact=0.000, avgJ=0.569, sym=2.00, unique=4/8
Title: [Feature]: Show display name instead of user ID in session list

Expected: `['chat_integrations', 'sessions', 'ui_tui']`

Most common predictions: `[(['acp', 'config', 'sessions', 'ui_tui'], 3), (['chat_integrations', 'config', 'sessions', 'ui_tui'], 3), (['acp', 'chat_integrations', 'config', 'sessions', 'ui_tui'], 1)]`

Volatile topics: `[('config', 7), ('sessions', 7), ('chat_integrations', 5), ('acp', 4), ('api_surface', 1)]`

FP: `[('config', 7), ('acp', 4), ('api_surface', 1)]`

FN: `[('chat_integrations', 3), ('sessions', 1)]`

By model:
- deepseek4: `[['acp', 'chat_integrations', 'config', 'sessions', 'ui_tui'], ['api_surface', 'chat_integrations', 'ui_tui']]`
- gpt-5.4-mini: `[['acp', 'config', 'sessions', 'ui_tui'], ['acp', 'config', 'sessions', 'ui_tui'], ['acp', 'config', 'sessions', 'ui_tui']]`
- sonnet: `[['chat_integrations', 'config', 'sessions', 'ui_tui'], ['chat_integrations', 'config', 'sessions', 'ui_tui'], ['chat_integrations', 'config', 'sessions', 'ui_tui']]`

### 10. openclaw-openclaw-75784 — pairwise=0.663, exact=0.375, avgJ=0.750, sym=1.38, unique=5/8
Title: Phantom user messages appear in webchat after heartbeat wakes / gateway restart / session repair

Expected: `['chat_integrations', 'gateway', 'reliability', 'sessions']`

Most common predictions: `[(['chat_integrations', 'gateway', 'reliability', 'sessions'], 3), (['agent_runtime', 'gateway', 'reliability', 'sessions', 'ui_tui'], 2), (['gateway', 'reliability', 'sessions', 'ui_tui'], 1)]`

Volatile topics: `[('gateway', 7), ('chat_integrations', 5), ('agent_runtime', 4), ('ui_tui', 3)]`

FP: `[('agent_runtime', 4), ('ui_tui', 3)]`

FN: `[('chat_integrations', 3), ('gateway', 1)]`

By model:
- deepseek4: `[['agent_runtime', 'chat_integrations', 'gateway', 'reliability', 'sessions'], ['agent_runtime', 'chat_integrations', 'reliability', 'sessions']]`
- gpt-5.4-mini: `[['chat_integrations', 'gateway', 'reliability', 'sessions'], ['chat_integrations', 'gateway', 'reliability', 'sessions'], ['chat_integrations', 'gateway', 'reliability', 'sessions']]`
- sonnet: `[['agent_runtime', 'gateway', 'reliability', 'sessions', 'ui_tui'], ['gateway', 'reliability', 'sessions', 'ui_tui'], ['agent_runtime', 'gateway', 'reliability', 'sessions', 'ui_tui']]`

### 11. openclaw-openclaw-67539 — pairwise=0.679, exact=0.625, avgJ=0.812, sym=0.50, unique=4/8
Title: [Feature]: Add provider-specific TTS prompt hints

Expected: `['api_surface', 'self_hosted_inference']`

Most common predictions: `[(['api_surface', 'self_hosted_inference'], 5), (['api_surface', 'self_hosted_inference', 'skills_plugins'], 1), (['self_hosted_inference'], 1)]`

Volatile topics: `[('api_surface', 6), ('skills_plugins', 2)]`

FP: `[('skills_plugins', 2)]`

FN: `[('api_surface', 2)]`

By model:
- deepseek4: `[['self_hosted_inference'], ['self_hosted_inference', 'skills_plugins']]`
- gpt-5.4-mini: `[['api_surface', 'self_hosted_inference'], ['api_surface', 'self_hosted_inference'], ['api_surface', 'self_hosted_inference']]`
- sonnet: `[['api_surface', 'self_hosted_inference'], ['api_surface', 'self_hosted_inference'], ['api_surface', 'self_hosted_inference', 'skills_plugins']]`

### 12. openclaw-openclaw-75043 — pairwise=0.690, exact=0.250, avgJ=0.729, sym=1.00, unique=4/8
Title: Add provider-aware automatic TTS emotion mapping

Expected: `['api_surface', 'config', 'self_hosted_inference']`

Most common predictions: `[(['config', 'self_hosted_inference'], 2), (['config', 'docs', 'self_hosted_inference'], 2), (['api_surface', 'config', 'self_hosted_inference'], 2)]`

Volatile topics: `[('api_surface', 4), ('docs', 4)]`

FP: `[('docs', 4)]`

FN: `[('api_surface', 4)]`

By model:
- deepseek4: `[['config', 'docs', 'self_hosted_inference'], ['api_surface', 'config', 'self_hosted_inference']]`
- gpt-5.4-mini: `[['config', 'self_hosted_inference'], ['config', 'docs', 'self_hosted_inference'], ['config', 'self_hosted_inference']]`
- sonnet: `[['api_surface', 'config', 'self_hosted_inference'], ['api_surface', 'config', 'docs', 'self_hosted_inference'], ['api_surface', 'config', 'docs', 'self_hosted_inference']]`

### 13. openclaw-openclaw-78977 — pairwise=0.699, exact=0.625, avgJ=0.823, sym=0.62, unique=3/8
Title: fix(providers): skip store:false for proxy-like Responses API endpoints (#78897)

Expected: `['local_model_providers', 'model_serving', 'reliability']`

Most common predictions: `[(['local_model_providers', 'model_serving', 'reliability'], 5), (['local_model_providers', 'model_serving'], 2), (['api_surface', 'model_serving'], 1)]`

Volatile topics: `[('local_model_providers', 7), ('reliability', 5), ('api_surface', 1)]`

FP: `[('api_surface', 1)]`

FN: `[('reliability', 3), ('local_model_providers', 1)]`

By model:
- deepseek4: `[['local_model_providers', 'model_serving'], ['local_model_providers', 'model_serving', 'reliability']]`
- gpt-5.4-mini: `[['local_model_providers', 'model_serving'], ['local_model_providers', 'model_serving', 'reliability'], ['api_surface', 'model_serving']]`
- sonnet: `[['local_model_providers', 'model_serving', 'reliability'], ['local_model_providers', 'model_serving', 'reliability'], ['local_model_providers', 'model_serving', 'reliability']]`

### 14. openclaw-openclaw-56613 — pairwise=0.714, exact=0.000, avgJ=0.708, sym=1.00, unique=2/8
Title: [Feature]: Talk/Voice tab — agent/session switching + per-agent TTS voice

Expected: `['config', 'sessions', 'ui_tui']`

Most common predictions: `[(['config', 'self_hosted_inference', 'sessions', 'ui_tui'], 4), (['sessions', 'ui_tui'], 4)]`

Volatile topics: `[('config', 4), ('self_hosted_inference', 4)]`

FP: `[('self_hosted_inference', 4)]`

FN: `[('config', 4)]`

By model:
- deepseek4: `[['sessions', 'ui_tui'], ['sessions', 'ui_tui']]`
- gpt-5.4-mini: `[['config', 'self_hosted_inference', 'sessions', 'ui_tui'], ['sessions', 'ui_tui'], ['sessions', 'ui_tui']]`
- sonnet: `[['config', 'self_hosted_inference', 'sessions', 'ui_tui'], ['config', 'self_hosted_inference', 'sessions', 'ui_tui'], ['config', 'self_hosted_inference', 'sessions', 'ui_tui']]`

### 15. openclaw-openclaw-71157 — pairwise=0.726, exact=0.250, avgJ=0.771, sym=0.75, unique=3/8
Title: [Feature]: Support WhatsApp disappearing-message expiration for outbound replies

Expected: `['chat_integrations', 'config', 'security']`

Most common predictions: `[(['chat_integrations', 'config'], 4), (['chat_integrations', 'config', 'security'], 2), (['chat_integrations', 'config', 'notifications', 'security'], 2)]`

Volatile topics: `[('security', 4), ('notifications', 2)]`

FP: `[('notifications', 2)]`

FN: `[('security', 4)]`

By model:
- deepseek4: `[['chat_integrations', 'config', 'security'], ['chat_integrations', 'config']]`
- gpt-5.4-mini: `[['chat_integrations', 'config'], ['chat_integrations', 'config'], ['chat_integrations', 'config']]`
- sonnet: `[['chat_integrations', 'config', 'security'], ['chat_integrations', 'config', 'notifications', 'security'], ['chat_integrations', 'config', 'notifications', 'security']]`

## Least stable train rows across GEPA candidates

### 1. openclaw-openclaw-43495 — pairwise=0.340, exact=0.056, avgJ=0.346, sym=2.78, unique=29/54
Title: feat(tts): add <notts> tag support for visual-only content

Expected: `['api_surface', 'self_hosted_inference']`

Most common predictions: `[(['api_surface', 'config', 'docs', 'gateway', 'security', 'self_hosted_inference'], 6), (['api_surface', 'config'], 5), (['api_surface', 'config', 'gateway', 'security', 'self_hosted_inference'], 4)]`

FP: `[('config', 33), ('gateway', 29), ('docs', 20), ('security', 18), ('sessions', 5)]`

FN: `[('api_surface', 24), ('self_hosted_inference', 14)]`

### 2. openclaw-openclaw-84706 — pairwise=0.400, exact=0.019, avgJ=0.438, sym=3.56, unique=39/54
Title: [Bug]: subagent spawn validation rejects every non-off thinking level on all canonical openai/* models — error cites canonical alias even when openai-codex/* is requested

Expected: `['api_surface', 'codex', 'coding_agents', 'config', 'sessions']`

Most common predictions: `[(['acp', 'api_surface', 'config', 'sessions'], 3), (['api_surface', 'codex', 'sessions'], 3), (['acp', 'api_surface', 'codex', 'config', 'sessions'], 3)]`

FP: `[('acp', 29), ('agent_runtime', 15), ('model_serving', 10), ('reliability', 6), ('local_model_providers', 1)]`

FN: `[('coding_agents', 48), ('codex', 29), ('api_surface', 27), ('config', 23), ('sessions', 4)]`

### 3. openclaw-openclaw-76724 — pairwise=0.536, exact=0.333, avgJ=0.654, sym=1.00, unique=13/54
Title: [Bug]: MCP tools not discovered by Agent despite successful handshake (200 OK)

Expected: `['mcp_tooling', 'ui_tui']`

Most common predictions: `[(['mcp_tooling', 'ui_tui'], 18), (['mcp_tooling'], 12), (['gateway', 'mcp_tooling'], 5)]`

FP: `[('config', 11), ('gateway', 10), ('reliability', 7), ('api_surface', 2), ('agent_runtime', 1)]`

FN: `[('ui_tui', 23)]`

### 4. openclaw-openclaw-10467 — pairwise=0.581, exact=0.000, avgJ=0.593, sym=2.41, unique=24/54
Title: [Feature Request]: Multi-lane concurrency support for sub-agents via sessions_spawn

Expected: `['acp', 'agent_runtime', 'config', 'queueing', 'sessions']`

Most common predictions: `[(['api_surface', 'config', 'queueing', 'sessions'], 8), (['acp', 'api_surface', 'config', 'queueing', 'sessions'], 6), (['agent_runtime', 'api_surface', 'config', 'queueing'], 3)]`

FP: `[('api_surface', 35), ('reliability', 11)]`

FN: `[('agent_runtime', 36), ('acp', 28), ('sessions', 14), ('config', 6)]`

### 5. openclaw-openclaw-84038 — pairwise=0.592, exact=0.167, avgJ=0.696, sym=1.37, unique=18/54
Title: [Bug]: doctor --fix silently migrates intentional openai-codex/ config to openai/, breaking PI+OAuth runtime and causing 3-4x token inflation

Expected: `['agent_runtime', 'auth_identity', 'codex', 'config']`

Most common predictions: `[(['auth_identity', 'codex', 'config'], 15), (['agent_runtime', 'auth_identity', 'codex', 'config'], 9), (['codex', 'config', 'reliability'], 4)]`

FP: `[('reliability', 11), ('coding_agents', 8)]`

FN: `[('agent_runtime', 30), ('auth_identity', 15), ('codex', 10)]`

### 6. openclaw-openclaw-51667 — pairwise=0.603, exact=0.093, avgJ=0.713, sym=1.30, unique=15/54
Title: Feature: Native Audio Input for Omni-Modal Models (skip STT transcription)

Expected: `['chat_integrations', 'config', 'model_serving', 'sessions']`

Most common predictions: `[(['config', 'model_serving', 'sessions'], 10), (['chat_integrations', 'config', 'model_serving', 'self_hosted_inference', 'sessions'], 10), (['chat_integrations', 'config', 'model_serving'], 8)]`

FP: `[('self_hosted_inference', 17), ('security', 4), ('reliability', 1), ('api_surface', 1)]`

FN: `[('chat_integrations', 20), ('sessions', 20), ('model_serving', 6), ('config', 1)]`

### 7. openclaw-openclaw-84761 — pairwise=0.603, exact=0.204, avgJ=0.627, sym=1.15, unique=6/54
Title: feat(secrets): scan backup files for plaintext provider apiKey values

Expected: `['auth_identity', 'config', 'security']`

Most common predictions: `[(['security'], 18), (['config', 'security'], 15), (['auth_identity', 'config', 'security'], 11)]`

FP: `[('tests_ci', 5)]`

FN: `[('auth_identity', 34), ('config', 23)]`

### 8. openclaw-openclaw-77345 — pairwise=0.604, exact=0.278, avgJ=0.674, sym=1.02, unique=10/54
Title: google-vertex SSRF guard blocks fake-IP DNS (model.baseUrl not set for built-in providers)

Expected: `['model_serving', 'security']`

Most common predictions: `[(['model_serving', 'security'], 15), (['config', 'model_serving', 'security'], 14), (['model_serving', 'reliability', 'security'], 9)]`

FP: `[('config', 25), ('reliability', 14), ('local_model_providers', 2), ('self_hosted_inference', 1)]`

FN: `[('model_serving', 13)]`

### 9. openclaw-openclaw-71537 — pairwise=0.611, exact=0.148, avgJ=0.646, sym=1.72, unique=15/54
Title: Recover archived (.reset) session transcripts in memory hook + session-logs skill

Expected: `['memory', 'sessions', 'skills_plugins']`

Most common predictions: `[(['hooks', 'memory', 'sessions', 'skills_plugins'], 11), (['memory', 'sessions', 'skills_plugins'], 8), (['docs', 'hooks', 'memory', 'sessions', 'skills_plugins', 'tests_ci'], 7)]`

FP: `[('hooks', 32), ('docs', 24), ('reliability', 12), ('tests_ci', 8)]`

FN: `[('skills_plugins', 15), ('sessions', 2)]`

### 10. openclaw-openclaw-55888 — pairwise=0.613, exact=0.352, avgJ=0.719, sym=1.04, unique=11/54
Title: [Feature]: 🚀 [Performance Insight] Unlocking 26.7k Context Window on M4 Pro: Fixing the 8k Compaction Lag (64GB RAM Only)

Expected: `['config', 'local_models', 'memory']`

Most common predictions: `[(['config', 'local_models', 'memory'], 19), (['config', 'local_models'], 12), (['agent_runtime', 'config', 'local_models'], 5)]`

FP: `[('sessions', 10), ('agent_runtime', 6), ('open_weight_models', 5)]`

FN: `[('memory', 27), ('local_models', 8)]`

### 11. openclaw-openclaw-58135 — pairwise=0.614, exact=0.222, avgJ=0.719, sym=1.17, unique=13/54
Title: [Feature]: expose promptMode parameter in sessions_spawn for deterministic blank sub-agents

Expected: `['acp', 'agent_runtime', 'api_surface', 'sessions']`

Most common predictions: `[(['acp', 'agent_runtime', 'api_surface', 'sessions'], 12), (['api_surface', 'sessions'], 10), (['acp', 'api_surface', 'sessions'], 10)]`

FP: `[('config', 6)]`

FN: `[('acp', 24), ('agent_runtime', 22), ('api_surface', 9), ('sessions', 2)]`

### 12. openclaw-openclaw-68725 — pairwise=0.622, exact=0.574, avgJ=0.744, sym=0.76, unique=9/54
Title: feat(amazon-bedrock-mantle): add known context windows for open-weight Mantle models

Expected: `['config', 'open_weight_models']`

Most common predictions: `[(['config', 'open_weight_models'], 31), (['model_serving', 'open_weight_models'], 11), (['open_weight_models'], 4)]`

FP: `[('model_serving', 16), ('local_model_providers', 4), ('reliability', 1)]`

FN: `[('config', 18), ('open_weight_models', 2)]`

### 13. openclaw-openclaw-84715 — pairwise=0.623, exact=0.222, avgJ=0.735, sym=1.19, unique=13/54
Title: [Bug]: @openclaw/codex peer link failure reproduced on 2026.5.19 after update

Expected: `['codex', 'packaging_deployment', 'reliability', 'skills_plugins']`

Most common predictions: `[(['codex', 'packaging_deployment', 'reliability'], 14), (['codex', 'packaging_deployment', 'reliability', 'skills_plugins'], 12), (['codex', 'packaging_deployment', 'skills_plugins'], 5)]`

FP: `[('coding_agents', 17)]`

FN: `[('skills_plugins', 22), ('reliability', 14), ('codex', 6), ('packaging_deployment', 5)]`

### 14. openclaw-openclaw-73910 — pairwise=0.631, exact=0.093, avgJ=0.650, sym=2.31, unique=23/54
Title: BUG: OpenClaw-managed Codex ACP uses isolated CODEX_HOME without auth bridge and sends unsupported timeout config

Expected: `['acp', 'acpx', 'auth_identity', 'codex', 'config']`

Most common predictions: `[(['acp', 'acpx', 'auth_identity', 'coding_agents', 'config', 'security'], 7), (['acp', 'acpx', 'auth_identity', 'codex', 'coding_agents', 'security'], 6), (['acp', 'acpx', 'auth_identity', 'coding_agents', 'security'], 5)]`

FP: `[('security', 37), ('coding_agents', 30), ('api_surface', 3), ('reliability', 1), ('sessions', 1)]`

FN: `[('config', 24), ('codex', 15), ('acp', 10), ('auth_identity', 3), ('acpx', 1)]`

### 15. openclaw-openclaw-71803 — pairwise=0.633, exact=0.278, avgJ=0.715, sym=1.37, unique=14/54
Title: CLI watchdog kills sessions that are correctly idle while waiting on a Monitor task

Expected: `['agent_runtime', 'exec_tools', 'reliability', 'sessions']`

Most common predictions: `[(['agent_runtime', 'exec_tools', 'reliability', 'sessions'], 15), (['agent_runtime', 'coding_agents', 'reliability', 'sessions'], 8), (['agent_runtime', 'coding_agents', 'exec_tools', 'reliability', 'sessions'], 6)]`

FP: `[('coding_agents', 29), ('codex', 1)]`

FN: `[('exec_tools', 19), ('sessions', 14), ('agent_runtime', 11)]`
