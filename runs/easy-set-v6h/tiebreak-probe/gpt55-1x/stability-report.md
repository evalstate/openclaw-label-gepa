# OpenClaw easy-set stability report

Rows: `21`  Repeats: `1`

## Prediction stability

- pairwise exact: `1.000`
- pairwise Jaccard: `1.000`
- pairwise symdiff: `0.000`

## Buckets

- `stable_wrong`: 21

## Repeat metric summary

- `avg_expected_topics`: mean `0.0000`, pstdev `0.0000`, values `[0.0]`
- `avg_predicted_topics`: mean `2.3333`, pstdev `0.0000`, values `[2.3333]`
- `avg_row_jaccard`: mean `0.0000`, pstdev `0.0000`, values `[0.0]`
- `avg_row_symdiff`: mean `2.3333`, pstdev `0.0000`, values `[2.3333]`
- `exact_match`: mean `0.0000`, pstdev `0.0000`, values `[0.0]`
- `gepa_score`: mean `0.0000`, pstdev `0.0000`, values `[0.0]`
- `row_exact_accuracy`: mean `0.0000`, pstdev `0.0000`, values `[0.0]`
- `row_symdiff_score`: mean `0.3000`, pstdev `0.0000`, values `[0.3]`
- `topic_micro_f1`: mean `0.0000`, pstdev `0.0000`, values `[0.0]`
- `topic_micro_precision`: mean `0.0000`, pstdev `0.0000`, values `[0.0]`
- `topic_micro_recall`: mean `1.0000`, pstdev `0.0000`, values `[1.0]`
- `valid_json`: mean `1.0000`, pstdev `0.0000`, values `[1.0]`

## Least stable / review rows

### 1. openclaw-openclaw-39248 — stable_wrong

Title: Bug: sandbox.mode: "non-main" silently breaks sessions_spawn subagent initialization

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['agent_runtime', 'sandboxing'], 'count': 1}]`

FP: `[('agent_runtime', 1), ('sandboxing', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['agent_runtime', 'sandboxing']` exact=False

### 2. openclaw-openclaw-43765 — stable_wrong

Title: Improve runtime recovery for heartbeat, Feishu, and exec sessions

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'exec_tools', 'reliability'], 'count': 1}]`

FP: `[('chat_integrations', 1), ('exec_tools', 1), ('reliability', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'exec_tools', 'reliability']` exact=False

### 3. openclaw-openclaw-45508 — stable_wrong

Title: [Feature]: Self-hosted STT/TTS provider support in webchat (Route webchat TTS through the gateway instead of browser Speech API)

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'config', 'self_hosted_inference'], 'count': 1}]`

FP: `[('chat_integrations', 1), ('config', 1), ('self_hosted_inference', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'config', 'self_hosted_inference']` exact=False

### 4. openclaw-openclaw-46740 — stable_wrong

Title: ACP: classify silent acpx exits as backend unavailable

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['acpx'], 'count': 1}]`

FP: `[('acpx', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acpx']` exact=False

### 5. openclaw-openclaw-51667 — stable_wrong

Title: Feature: Native Audio Input for Omni-Modal Models (skip STT transcription)

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'inference_api'], 'count': 1}]`

FP: `[('config', 1), ('inference_api', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'inference_api']` exact=False

### 6. openclaw-openclaw-56532 — stable_wrong

Title: memory-lancedb: add configurable timeout/retry for embedding calls

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'memory', 'reliability'], 'count': 1}]`

FP: `[('config', 1), ('memory', 1), ('reliability', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'memory', 'reliability']` exact=False

### 7. openclaw-openclaw-56613 — stable_wrong

Title: [Feature]: Talk/Voice tab — agent/session switching + per-agent TTS voice

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'ui_tui'], 'count': 1}]`

FP: `[('config', 1), ('ui_tui', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'ui_tui']` exact=False

### 8. openclaw-openclaw-63229 — stable_wrong

Title: Bug: Gateway falsely marks healthy local vLLM endpoints as timed out/overloaded, causing 1–23 min fallback cascades

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['agent_runtime', 'gateway', 'reliability'], 'count': 1}]`

FP: `[('agent_runtime', 1), ('gateway', 1), ('reliability', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['agent_runtime', 'gateway', 'reliability']` exact=False

### 9. openclaw-openclaw-64317 — stable_wrong

Title: [Bug]: Headed Chromium viewport screenshots time out on Omarchy/Hyprland/Wayland after successful page load

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['browser_automation'], 'count': 1}]`

FP: `[('browser_automation', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['browser_automation']` exact=False

### 10. openclaw-openclaw-65242 — stable_wrong

Title: fix: CompletionDeliveryGate to prevent duplicate ACP completion delivery

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'hooks', 'notifications'], 'count': 1}]`

FP: `[('acp', 1), ('hooks', 1), ('notifications', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'hooks', 'notifications']` exact=False

### 11. openclaw-openclaw-71646 — stable_wrong

Title: mcp/channel-bridge: pendingClaudePermissions / pendingApprovals leak — no TTL, no close-clear, no cap

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['approvals', 'mcp_tooling', 'reliability'], 'count': 1}]`

FP: `[('approvals', 1), ('mcp_tooling', 1), ('reliability', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['approvals', 'mcp_tooling', 'reliability']` exact=False

### 12. openclaw-openclaw-71930 — stable_wrong

Title: Mattermost plugin drops post_edited events — @mentions added via edit do not trigger agent wake

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations'], 'count': 1}]`

FP: `[('chat_integrations', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations']` exact=False

### 13. openclaw-openclaw-75784 — stable_wrong

Title: Phantom user messages appear in webchat after heartbeat wakes / gateway restart / session repair

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'reliability', 'sessions'], 'count': 1}]`

FP: `[('chat_integrations', 1), ('reliability', 1), ('sessions', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'reliability', 'sessions']` exact=False

### 14. openclaw-openclaw-80479 — stable_wrong

Title: feat(memory/embeddings): add openai-compatible provider for self-hosted servers (llama.cpp, Ollama, vLLM, TGI, LocalAI)

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['inference_api', 'memory', 'self_hosted_inference'], 'count': 1}]`

FP: `[('inference_api', 1), ('memory', 1), ('self_hosted_inference', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['inference_api', 'memory', 'self_hosted_inference']` exact=False

### 15. openclaw-openclaw-84316 — stable_wrong

Title: [Bug]: Telegram group TTS for sub-agent reports success in /tts status but voice never delivered (2026.5.12)

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations'], 'count': 1}]`

FP: `[('chat_integrations', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations']` exact=False

### 16. openclaw-openclaw-84583 — stable_wrong

Title: cron announce delivery triggers EmbeddedAttemptSessionTakeoverError when user is actively chatting

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['cron_automation', 'notifications', 'sessions'], 'count': 1}]`

FP: `[('cron_automation', 1), ('notifications', 1), ('sessions', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['cron_automation', 'notifications', 'sessions']` exact=False

### 17. openclaw-openclaw-84706 — stable_wrong

Title: [Bug]: subagent spawn validation rejects every non-off thinking level on all canonical openai/* models — error cites canonical alias even when openai-codex/* is requested

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['agent_runtime', 'model_lifecycle'], 'count': 1}]`

FP: `[('agent_runtime', 1), ('model_lifecycle', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['agent_runtime', 'model_lifecycle']` exact=False

### 18. openclaw-openclaw-84752 — stable_wrong

Title: fix: self-heal lane wedges + restore openai-codex OAuth on embedded path

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['codex', 'queueing', 'reliability'], 'count': 1}]`

FP: `[('codex', 1), ('queueing', 1), ('reliability', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['codex', 'queueing', 'reliability']` exact=False

### 19. openclaw-openclaw-84771 — stable_wrong

Title: Event loop saturation during startup: synchronous model-prewarm and session-locks block event loop for 28-64 seconds

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['agent_runtime', 'reliability', 'sessions'], 'count': 1}]`

FP: `[('agent_runtime', 1), ('reliability', 1), ('sessions', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['agent_runtime', 'reliability', 'sessions']` exact=False

### 20. openclaw-openclaw-87277 — stable_wrong

Title: [Feature] Add MiMo-V2.5 to Xiaomi catalog + automatic multimodal routing when DeepSeek V4-Pro is primary model

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['agent_runtime', 'model_lifecycle'], 'count': 1}]`

FP: `[('agent_runtime', 1), ('model_lifecycle', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['agent_runtime', 'model_lifecycle']` exact=False

### 21. openclaw-openclaw-88400 — stable_wrong

Title: fix(config): accept overlays for bundled provider aliases

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'inference_api'], 'count': 1}]`

FP: `[('config', 1), ('inference_api', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'inference_api']` exact=False
