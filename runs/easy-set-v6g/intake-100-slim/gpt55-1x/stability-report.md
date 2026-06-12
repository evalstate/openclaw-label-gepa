# OpenClaw easy-set stability report

Rows: `100`  Repeats: `1`

## Prediction stability

- pairwise exact: `1.000`
- pairwise Jaccard: `1.000`
- pairwise symdiff: `0.000`

## Buckets

- `stable_wrong`: 100

## Repeat metric summary

- `avg_expected_topics`: mean `0.0000`, pstdev `0.0000`, values `[0.0]`
- `avg_predicted_topics`: mean `2.4400`, pstdev `0.0000`, values `[2.44]`
- `avg_row_jaccard`: mean `0.0000`, pstdev `0.0000`, values `[0.0]`
- `avg_row_symdiff`: mean `2.4400`, pstdev `0.0000`, values `[2.44]`
- `exact_match`: mean `0.0000`, pstdev `0.0000`, values `[0.0]`
- `gepa_score`: mean `0.0000`, pstdev `0.0000`, values `[0.0]`
- `row_exact_accuracy`: mean `0.0000`, pstdev `0.0000`, values `[0.0]`
- `row_symdiff_score`: mean `0.2907`, pstdev `0.0000`, values `[0.2907]`
- `topic_micro_f1`: mean `0.0000`, pstdev `0.0000`, values `[0.0]`
- `topic_micro_precision`: mean `0.0000`, pstdev `0.0000`, values `[0.0]`
- `topic_micro_recall`: mean `1.0000`, pstdev `0.0000`, values `[1.0]`
- `valid_json`: mean `1.0000`, pstdev `0.0000`, values `[1.0]`

## Least stable / review rows

### 1. openclaw-openclaw-39714 — stable_wrong

Title: Sandbox: fix Dockerized browser bridge and tab creation

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['browser_automation', 'config', 'sandboxing'], 'count': 1}]`

FP: `[('browser_automation', 1), ('config', 1), ('sandboxing', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['browser_automation', 'config', 'sandboxing']` exact=False

### 2. openclaw-openclaw-42425 — stable_wrong

Title: fix(hooks): load workspace hooks for non-default agents

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['hooks'], 'count': 1}]`

FP: `[('hooks', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['hooks']` exact=False

### 3. openclaw-openclaw-42606 — stable_wrong

Title: Browser: harden noVNC bootstrap headers

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['browser_automation', 'security'], 'count': 1}]`

FP: `[('browser_automation', 1), ('security', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['browser_automation', 'security']` exact=False

### 4. openclaw-openclaw-43246 — stable_wrong

Title: fix(message): deny same-provider cross-context sends by default [AI-assisted]

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'notifications', 'security'], 'count': 1}]`

FP: `[('config', 1), ('notifications', 1), ('security', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'notifications', 'security']` exact=False

### 5. openclaw-openclaw-43495 — stable_wrong

Title: feat(tts): add <notts> tag support for visual-only content

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['gateway', 'inference_api', 'security'], 'count': 1}]`

FP: `[('gateway', 1), ('inference_api', 1), ('security', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['gateway', 'inference_api', 'security']` exact=False

### 6. openclaw-openclaw-43765 — stable_wrong

Title: Improve runtime recovery for heartbeat, Feishu, and exec sessions

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'cron_automation', 'exec_tools'], 'count': 1}]`

FP: `[('chat_integrations', 1), ('cron_automation', 1), ('exec_tools', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'cron_automation', 'exec_tools']` exact=False

### 7. openclaw-openclaw-44202 — stable_wrong

Title: [Bug]: local memory embeddings on Apple Silicon can crash gateway in ggml-metal / node-llama-cpp; need official Metal/GPU guidance

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['memory', 'reliability', 'self_hosted_inference'], 'count': 1}]`

FP: `[('memory', 1), ('reliability', 1), ('self_hosted_inference', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['memory', 'reliability', 'self_hosted_inference']` exact=False

### 8. openclaw-openclaw-45508 — stable_wrong

Title: [Feature]: Self-hosted STT/TTS provider support in webchat (Route webchat TTS through the gateway instead of browser Speech API)

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'config', 'self_hosted_inference'], 'count': 1}]`

FP: `[('chat_integrations', 1), ('config', 1), ('self_hosted_inference', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'config', 'self_hosted_inference']` exact=False

### 9. openclaw-openclaw-47187 — stable_wrong

Title: fix(ui): reset transient chat overlays and style context notice

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['ui_tui'], 'count': 1}]`

FP: `[('ui_tui', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['ui_tui']` exact=False

### 10. openclaw-openclaw-47285 — stable_wrong

Title: feat(memory-lancedb): native Azure OpenAI support

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['inference_api', 'memory'], 'count': 1}]`

FP: `[('inference_api', 1), ('memory', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['inference_api', 'memory']` exact=False

### 11. openclaw-openclaw-47446 — stable_wrong

Title: fix(gateway/discord): respect env proxy vars and prevent ECONNRESET

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'gateway', 'reliability'], 'count': 1}]`

FP: `[('chat_integrations', 1), ('gateway', 1), ('reliability', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'gateway', 'reliability']` exact=False

### 12. openclaw-openclaw-48260 — stable_wrong

Title: feat(ui): add active time summary to usage overview

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['telemetry_usage', 'ui_tui'], 'count': 1}]`

FP: `[('telemetry_usage', 1), ('ui_tui', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['telemetry_usage', 'ui_tui']` exact=False

### 13. openclaw-openclaw-49310 — stable_wrong

Title: fix: keep tui busy during follow-up waits

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['ui_tui'], 'count': 1}]`

FP: `[('ui_tui', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['ui_tui']` exact=False

### 14. openclaw-openclaw-53319 — stable_wrong

Title: [Bug]: ACP concurrent session spawns — first agent fails to launch CC process

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'acpx', 'reliability'], 'count': 1}]`

FP: `[('acp', 1), ('acpx', 1), ('reliability', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'acpx', 'reliability']` exact=False

### 15. openclaw-openclaw-55790 — stable_wrong

Title: sessions_spawn(runtime="subagent") ignores inherited/per-agent subagent thinking defaults and initializes children at low

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['agent_runtime', 'config'], 'count': 1}]`

FP: `[('agent_runtime', 1), ('config', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['agent_runtime', 'config']` exact=False

### 16. openclaw-openclaw-55888 — stable_wrong

Title: [Feature]: 🚀 [Performance Insight] Unlocking 26.7k Context Window on M4 Pro: Fixing the 8k Compaction Lag (64GB RAM Only)

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'self_hosted_inference', 'sessions'], 'count': 1}]`

FP: `[('config', 1), ('self_hosted_inference', 1), ('sessions', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'self_hosted_inference', 'sessions']` exact=False

### 17. openclaw-openclaw-56532 — stable_wrong

Title: memory-lancedb: add configurable timeout/retry for embedding calls

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'memory', 'reliability'], 'count': 1}]`

FP: `[('config', 1), ('memory', 1), ('reliability', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'memory', 'reliability']` exact=False

### 18. openclaw-openclaw-56613 — stable_wrong

Title: [Feature]: Talk/Voice tab — agent/session switching + per-agent TTS voice

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'inference_api', 'ui_tui'], 'count': 1}]`

FP: `[('config', 1), ('inference_api', 1), ('ui_tui', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['config', 'inference_api', 'ui_tui']` exact=False

### 19. openclaw-openclaw-56866 — stable_wrong

Title: feat(whatsapp): ACP session binding with media threading and prompt fixes

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'chat_integrations', 'hooks'], 'count': 1}]`

FP: `[('acp', 1), ('chat_integrations', 1), ('hooks', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'chat_integrations', 'hooks']` exact=False

### 20. openclaw-openclaw-57597 — stable_wrong

Title: fix(acp): persist spawn labels in target session store

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['sessions'], 'count': 1}]`

FP: `[('sessions', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['sessions']` exact=False

### 21. openclaw-openclaw-58411 — stable_wrong

Title: sessions_spawn lacks --bind here equivalent — agent cannot bind ACP session to existing Discord thread

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'chat_integrations', 'tool_calling'], 'count': 1}]`

FP: `[('acp', 1), ('chat_integrations', 1), ('tool_calling', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'chat_integrations', 'tool_calling']` exact=False

### 22. openclaw-openclaw-59878 — stable_wrong

Title: Session lane stuck in 'running' after run dies — sessions.abort + gateway restart fail to clear stale state

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['queueing', 'reliability', 'sessions'], 'count': 1}]`

FP: `[('queueing', 1), ('reliability', 1), ('sessions', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['queueing', 'reliability', 'sessions']` exact=False

### 23. openclaw-openclaw-61775 — stable_wrong

Title: enhance Makefile with standard build, test, and quality targets

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['packaging_deployment', 'tests_ci'], 'count': 1}]`

FP: `[('packaging_deployment', 1), ('tests_ci', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['packaging_deployment', 'tests_ci']` exact=False

### 24. openclaw-openclaw-62552 — stable_wrong

Title: fix(acp): stabilize bridge session keys

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'queueing', 'sessions'], 'count': 1}]`

FP: `[('acp', 1), ('queueing', 1), ('sessions', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'queueing', 'sessions']` exact=False

### 25. openclaw-openclaw-62769 — stable_wrong

Title: [Feature]: Support ACP configured bindings for Telegram DMs (not just groups/topics)

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'chat_integrations'], 'count': 1}]`

FP: `[('acp', 1), ('chat_integrations', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'chat_integrations']` exact=False

### 26. openclaw-openclaw-63007 — stable_wrong

Title: Pass outbound session identity into message_sending and surface guarded gateway send denial

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['gateway', 'hooks', 'notifications'], 'count': 1}]`

FP: `[('gateway', 1), ('hooks', 1), ('notifications', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['gateway', 'hooks', 'notifications']` exact=False

### 27. openclaw-openclaw-63229 — stable_wrong

Title: Bug: Gateway falsely marks healthy local vLLM endpoints as timed out/overloaded, causing 1–23 min fallback cascades

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['gateway', 'inference_api', 'reliability'], 'count': 1}]`

FP: `[('gateway', 1), ('inference_api', 1), ('reliability', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['gateway', 'inference_api', 'reliability']` exact=False

### 28. openclaw-openclaw-63826 — stable_wrong

Title: security: fix HIGH/CRITICAL vulns in skill scanner, SSRF, hook priority, and token verification

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['hooks', 'security', 'skills_plugins'], 'count': 1}]`

FP: `[('hooks', 1), ('security', 1), ('skills_plugins', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['hooks', 'security', 'skills_plugins']` exact=False

### 29. openclaw-openclaw-64199 — stable_wrong

Title: [Bug]: ACP configured binding uses parent channel ID for session key — all threads under same channel share one persistent Claude Code process

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'acpx', 'security'], 'count': 1}]`

FP: `[('acp', 1), ('acpx', 1), ('security', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'acpx', 'security']` exact=False

### 30. openclaw-openclaw-64317 — stable_wrong

Title: [Bug]: Headed Chromium viewport screenshots time out on Omarchy/Hyprland/Wayland after successful page load

Expected: `[]`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.000`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['browser_automation'], 'count': 1}]`

FP: `[('browser_automation', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['browser_automation']` exact=False
