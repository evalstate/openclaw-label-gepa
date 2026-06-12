# OpenClaw easy-set stability report

Rows: `40`  Repeats: `3`

## Prediction stability

- pairwise exact: `0.983`
- pairwise Jaccard: `0.997`
- pairwise symdiff: `0.017`

## Buckets

- `stable_correct`: 39
- `unstable_near`: 1

## Repeat metric summary

- `avg_expected_topics`: mean `3.3000`, pstdev `0.0000`, values `[3.3, 3.3, 3.3]`
- `avg_predicted_topics`: mean `3.3083`, pstdev `0.0118`, values `[3.3, 3.3, 3.325]`
- `avg_row_jaccard`: mean `0.9983`, pstdev `0.0024`, values `[1.0, 1.0, 0.995]`
- `avg_row_symdiff`: mean `0.0083`, pstdev `0.0118`, values `[0.0, 0.0, 0.025]`
- `exact_match`: mean `0.9917`, pstdev `0.0118`, values `[1.0, 1.0, 0.975]`
- `gepa_score`: mean `0.9973`, pstdev `0.0038`, values `[1.0, 1.0, 0.9919]`
- `row_exact_accuracy`: mean `0.9917`, pstdev `0.0118`, values `[1.0, 1.0, 0.975]`
- `row_symdiff_score`: mean `0.9919`, pstdev `0.0115`, values `[1.0, 1.0, 0.9756]`
- `topic_micro_f1`: mean `0.9987`, pstdev `0.0018`, values `[1.0, 1.0, 0.9962]`
- `topic_micro_precision`: mean `0.9975`, pstdev `0.0035`, values `[1.0, 1.0, 0.9925]`
- `topic_micro_recall`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0, 1.0]`
- `valid_json`: mean `1.0000`, pstdev `0.0000`, values `[1.0, 1.0, 1.0]`

## Least stable / review rows

### 1. openclaw-openclaw-75784 — unstable_near

Title: Phantom user messages appear in webchat after heartbeat wakes / gateway restart / session repair

Expected: `['chat_integrations', 'gateway', 'reliability', 'sessions']`

pairwise Jaccard `0.867`, pairwise exact `0.333`, exact vs expected `0.667`, avg Jaccard vs expected `0.933`, avg symdiff `0.33`, unique sets `2`

Most common predictions: `[{'topics': ['chat_integrations', 'gateway', 'reliability', 'sessions'], 'count': 2}, {'topics': ['agent_runtime', 'chat_integrations', 'gateway', 'reliability', 'sessions'], 'count': 1}]`

FP: `[('agent_runtime', 1)]`

FN: `[]`

Volatile: `[('agent_runtime', 1)]`

- repeat 1: `['chat_integrations', 'gateway', 'reliability', 'sessions']` exact=True
- repeat 2: `['chat_integrations', 'gateway', 'reliability', 'sessions']` exact=True
- repeat 3: `['agent_runtime', 'chat_integrations', 'gateway', 'reliability', 'sessions']` exact=False
