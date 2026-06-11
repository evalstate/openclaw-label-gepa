# v4 GPT-5.5 final-reference relabel sanity

- input: `easy-final-v4.jsonl` after #90146 adjudication
- model: `codexresponses.gpt-5.5?reasoning=high`
- rows: 125
- exact agreement with updated v4: 124 / 125
- changed vs updated v4: 1
- teacher bucket counts: `{'easy': 125}`
- strict easy rows: 123
- non-strict rows: 2
- teacher label changes vs previous GPT-5.5 pass: 1

## Changed vs updated v4

- `openclaw-openclaw-90146` — current `config, reliability, agent_runtime, model_releases` teacher `agent_runtime, model_releases, model_serving, reliability` additions `model_serving` removals `config`

## Teacher changes vs previous GPT-5.5 pass

- `openclaw-openclaw-90146` — pass1 `agent_runtime, config, model_releases, model_serving, reliability` pass2 `agent_runtime, model_releases, model_serving, reliability` — google-vertex: Missing gemini-3.1-flash-lite in provider catalog causes silent failure instead of error