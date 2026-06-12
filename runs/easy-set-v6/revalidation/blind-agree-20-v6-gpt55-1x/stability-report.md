# OpenClaw easy-set stability report

Rows: `20`  Repeats: `1`

## Prediction stability

- pairwise exact: `1.000`
- pairwise Jaccard: `1.000`
- pairwise symdiff: `0.000`

## Buckets

- `stable_correct`: 5
- `stable_wrong`: 15

## Repeat metric summary

- `avg_expected_topics`: mean `3.0000`, pstdev `0.0000`, values `[3.0]`
- `avg_predicted_topics`: mean `2.8000`, pstdev `0.0000`, values `[2.8]`
- `avg_row_jaccard`: mean `0.6842`, pstdev `0.0000`, values `[0.6842]`
- `avg_row_symdiff`: mean `1.1000`, pstdev `0.0000`, values `[1.1]`
- `exact_match`: mean `0.2500`, pstdev `0.0000`, values `[0.25]`
- `gepa_score`: mean `0.6604`, pstdev `0.0000`, values `[0.6604]`
- `row_exact_accuracy`: mean `0.2500`, pstdev `0.0000`, values `[0.25]`
- `row_symdiff_score`: mean `0.4762`, pstdev `0.0000`, values `[0.4762]`
- `topic_micro_f1`: mean `0.8103`, pstdev `0.0000`, values `[0.8103]`
- `topic_micro_precision`: mean `0.8393`, pstdev `0.0000`, values `[0.8393]`
- `topic_micro_recall`: mean `0.7833`, pstdev `0.0000`, values `[0.7833]`
- `valid_json`: mean `1.0000`, pstdev `0.0000`, values `[1.0]`

## Least stable / review rows

### 1. openclaw-openclaw-47083 — stable_wrong

Title: fix: respect totalTokensFresh flag to avoid showing stale token counts

Expected: `['sessions', 'telemetry_usage', 'ui_tui']`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.667`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['telemetry_usage', 'ui_tui'], 'count': 1}]`

FP: `[]`

FN: `[('sessions', 1)]`

Volatile: `[]`

- repeat 1: `['telemetry_usage', 'ui_tui']` exact=False

### 2. openclaw-openclaw-51849 — stable_wrong

Title: Docs: add freeCodeCamp OpenClaw full tutorial to showcase

Expected: `['agent_demos', 'docs']`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.500`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['docs'], 'count': 1}]`

FP: `[]`

FN: `[('agent_demos', 1)]`

Volatile: `[]`

- repeat 1: `['docs']` exact=False

### 3. openclaw-openclaw-53997 — stable_wrong

Title: acpx: add terminal-truth artifacts and strict terminal states

Expected: `['acp', 'acpx', 'reliability']`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.400`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acpx', 'agent_runtime', 'exec_tools', 'reliability'], 'count': 1}]`

FP: `[('agent_runtime', 1), ('exec_tools', 1)]`

FN: `[('acp', 1)]`

Volatile: `[]`

- repeat 1: `['acpx', 'agent_runtime', 'exec_tools', 'reliability']` exact=False

### 4. openclaw-openclaw-68916 — stable_wrong

Title: [Bug]: ACP oneshot sessions leave orphaned processes — session reset does not clean up child ACP session keys

Expected: `['acp', 'reliability', 'sessions']`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.750`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'gateway', 'reliability', 'sessions'], 'count': 1}]`

FP: `[('gateway', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['acp', 'gateway', 'reliability', 'sessions']` exact=False

### 5. openclaw-openclaw-71157 — stable_wrong

Title: [Feature]: Support WhatsApp disappearing-message expiration for outbound replies

Expected: `['chat_integrations', 'config', 'security']`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.500`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'config', 'notifications'], 'count': 1}]`

FP: `[('notifications', 1)]`

FN: `[('security', 1)]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'config', 'notifications']` exact=False

### 6. openclaw-openclaw-71487 — stable_wrong

Title: Web UI: add a clear TTS toggle and default voice picker in Settings

Expected: `['config', 'self_hosted_inference', 'ui_tui']`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.667`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['config', 'ui_tui'], 'count': 1}]`

FP: `[]`

FN: `[('self_hosted_inference', 1)]`

Volatile: `[]`

- repeat 1: `['config', 'ui_tui']` exact=False

### 7. openclaw-openclaw-71976 — stable_wrong

Title: Memory Dreaming: Light sleep sort prioritizes recency over recallCount, hiding real recall data

Expected: `['memory', 'reliability']`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.500`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['memory'], 'count': 1}]`

FP: `[]`

FN: `[('reliability', 1)]`

Volatile: `[]`

- repeat 1: `['memory']` exact=False

### 8. openclaw-openclaw-72138 — stable_wrong

Title: fix(feishu): emit sent hooks for normal replies

Expected: `['chat_integrations', 'hooks', 'notifications']`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.750`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'hooks', 'notifications', 'skills_plugins'], 'count': 1}]`

FP: `[('skills_plugins', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'hooks', 'notifications', 'skills_plugins']` exact=False

### 9. openclaw-openclaw-77694 — stable_wrong

Title: [Bug]: acpx flow run ACP node outputs return empty strings instead of agent replies

Expected: `['acp', 'acpx', 'agent_runtime', 'reliability']`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.400`, avg symdiff `3.00`, unique sets `1`

Most common predictions: `[{'topics': ['acp', 'acpx', 'coding_agents'], 'count': 1}]`

FP: `[('coding_agents', 1)]`

FN: `[('agent_runtime', 1), ('reliability', 1)]`

Volatile: `[]`

- repeat 1: `['acp', 'acpx', 'coding_agents']` exact=False

### 10. openclaw-openclaw-78528 — stable_wrong

Title: Security: skill SecretRef API keys still leak into exec child environments

Expected: `['auth_identity', 'exec_tools', 'security', 'skills_plugins']`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.750`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['exec_tools', 'security', 'skills_plugins'], 'count': 1}]`

FP: `[]`

FN: `[('auth_identity', 1)]`

Volatile: `[]`

- repeat 1: `['exec_tools', 'security', 'skills_plugins']` exact=False

### 11. openclaw-openclaw-82642 — stable_wrong

Title: Fix iMessage slash command acknowledgements

Expected: `['chat_integrations', 'notifications', 'reliability']`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.667`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['chat_integrations', 'notifications'], 'count': 1}]`

FP: `[]`

FN: `[('reliability', 1)]`

Volatile: `[]`

- repeat 1: `['chat_integrations', 'notifications']` exact=False

### 12. openclaw-openclaw-84761 — stable_wrong

Title: feat(secrets): scan backup files for plaintext provider apiKey values

Expected: `['auth_identity', 'config', 'security']`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.333`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['security'], 'count': 1}]`

FP: `[]`

FN: `[('auth_identity', 1), ('config', 1)]`

Volatile: `[]`

- repeat 1: `['security']` exact=False

### 13. openclaw-openclaw-84771 — stable_wrong

Title: Event loop saturation during startup: synchronous model-prewarm and session-locks block event loop for 28-64 seconds

Expected: `['gateway', 'model_serving', 'reliability', 'sessions']`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.800`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['gateway', 'model_serving', 'queueing', 'reliability', 'sessions'], 'count': 1}]`

FP: `[('queueing', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['gateway', 'model_serving', 'queueing', 'reliability', 'sessions']` exact=False

### 14. openclaw-openclaw-84997 — stable_wrong

Title: [AI-assisted] Add NEAR AI Cloud provider

Expected: `['auth_identity', 'model_serving']`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.500`, avg symdiff `2.00`, unique sets `1`

Most common predictions: `[{'topics': ['api_surface', 'auth_identity', 'model_releases', 'model_serving'], 'count': 1}]`

FP: `[('api_surface', 1), ('model_releases', 1)]`

FN: `[]`

Volatile: `[]`

- repeat 1: `['api_surface', 'auth_identity', 'model_releases', 'model_serving']` exact=False

### 15. openclaw-openclaw-88400 — stable_wrong

Title: fix(config): accept overlays for bundled provider aliases

Expected: `['config', 'model_serving']`

pairwise Jaccard `1.000`, pairwise exact `1.000`, exact vs expected `0.000`, avg Jaccard vs expected `0.500`, avg symdiff `1.00`, unique sets `1`

Most common predictions: `[{'topics': ['config'], 'count': 1}]`

FP: `[]`

FN: `[('model_serving', 1)]`

Volatile: `[]`

- repeat 1: `['config']` exact=False
