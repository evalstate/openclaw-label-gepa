# v4-relabel-gpt55 sanity check

- input: `easy-final-v4.jsonl`
- model: `codexresponses.gpt-5.5?reasoning=high`
- teacher card: `teacher-card-v4.md`
- topic surface: `allowed-topics-v4.md`

## Summary

- rows relabeled: 125
- raw failures: 0
- teacher bucket counts: `{'easy': 125}`
- strict easy rows: 119
- exact label agreement with current v4: 124 / 125
- changed rows: 1
- non-strict rows: 6

## Changed rows

### openclaw-openclaw-90146 / #90146 — google-vertex: Missing gemini-3.1-flash-lite in provider catalog causes silent failure instead of error

- current: `config, reliability, agent_runtime, model_releases`
- teacher: `model_serving, model_releases, agent_runtime, reliability, config`
- additions: `model_serving`
- removals: ``
- bucket: `easy` confidence: `0.93` strict_easy: `True`
- boundary families: `acp_session_runtime, provider_model, reliability, docs_tests_config`
- known bucket hits: `none`

## Non-strict rows

- `openclaw-openclaw-48580` / #48580 — confidence `0.95`, labels `acpx, codex, sessions, reliability` — Bug: acpx codex sessions 创建的会话立即退出 - stdin is not a terminal
- `openclaw-openclaw-48940` / #48940 — confidence `0.95`, labels `acp, gateway, agent_runtime, sessions, reliability` — ACP: add gateway-owned node-backed runtime
- `openclaw-openclaw-70002` / #70002 — confidence `0.97`, labels `tests_ci` — ci: skip docs sync & translate-trigger workflows in forks
- `openclaw-openclaw-71803` / #71803 — confidence `0.95`, labels `agent_runtime, exec_tools, reliability, sessions` — CLI watchdog kills sessions that are correctly idle while waiting on a Monitor task
- `openclaw-openclaw-74484` / #74484 — confidence `0.94`, labels `auth_identity, gateway, reliability` — Gateway pairing scope deadlock: CLI cannot approve/reject auto-reissued over-scoped repair requests
- `openclaw-openclaw-82145` / #82145 — confidence `0.94`, labels `cron_automation, local_model_providers, config, reliability` — cron: allow retries for local model preflight

## Concentration assessment

- Changed row boundary families: `acp_session_runtime, docs_tests_config, provider_model, reliability`
- Changed rows in `v4_confusion_bucket`: 0 (`none`)
- Changed rows in `v3_opus_disagreements`: 0 (`none`)
- Changed rows in `v2_instability_boundary`: 0 (`none`)
- Changed rows in `v3_not_easy_review`: 0 (`none`)

Interpretation: a single changed row out of 125 means the concise v4 teacher setup is highly consistent with the current labels. Review the one changed row manually; otherwise the sanity check supports that v4 did not broadly destabilize the easy labels.