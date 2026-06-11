# v4-relabel-gpt55 non-strict detail

## openclaw-openclaw-48580 / #48580 — Bug: acpx codex sessions 创建的会话立即退出 - stdin is not a terminal

- labels: `acpx, codex, sessions, reliability`
- strict_easy: `False`
- reasons: `possible_confusions=3`
- confidence: `0.95`
- ambiguity: `{'level': 'low', 'possible_confusions': ['coding_agents', 'agent_runtime', 'auth_identity'], 'why_not_hard': 'The title, command, logs, and expected behavior directly identify ACPX, Codex, session state drift, and startup cleanup/reliability.'}`

## openclaw-openclaw-48940 / #48940 — ACP: add gateway-owned node-backed runtime

- labels: `acp, gateway, agent_runtime, sessions, reliability`
- strict_easy: `False`
- reasons: `possible_confusions=3`
- confidence: `0.95`
- ambiguity: `{'level': 'low', 'possible_confusions': ['docs', 'chat_integrations', 'notifications'], 'why_not_hard': 'The title and summary directly identify ACP, gateway-owned durable state, node runtime execution, session/run persistence, and recovery hardening as the core concerns.'}`

## openclaw-openclaw-70002 / #70002 — ci: skip docs sync & translate-trigger workflows in forks

- labels: `tests_ci`
- strict_easy: `False`
- reasons: `possible_confusions=2`
- confidence: `0.97`
- ambiguity: `{'level': 'low', 'possible_confusions': ['docs', 'auth_identity'], 'why_not_hard': 'The diff is limited to CI workflow guard conditions, making the central routing label straightforward.'}`

## openclaw-openclaw-71803 / #71803 — CLI watchdog kills sessions that are correctly idle while waiting on a Monitor task

- labels: `agent_runtime, exec_tools, reliability, sessions`
- strict_easy: `False`
- reasons: `possible_confusions=2`
- confidence: `0.95`
- ambiguity: `{'level': 'low', 'possible_confusions': ['tool_calling', 'coding_agents'], 'why_not_hard': 'The issue explicitly names the watchdog timeout, Monitor shell task, and session loss, making the routing labels stable.'}`

## openclaw-openclaw-74484 / #74484 — Gateway pairing scope deadlock: CLI cannot approve/reject auto-reissued over-scoped repair requests

- labels: `auth_identity, gateway, reliability`
- strict_easy: `False`
- reasons: `possible_confusions=2`
- confidence: `0.94`
- ambiguity: `{'level': 'low', 'possible_confusions': ['approvals', 'security'], 'why_not_hard': 'The central surfaces are explicitly pairing scopes, gateway authorization, and deadlock recovery; boundary labels are secondary.'}`

## openclaw-openclaw-82145 / #82145 — cron: allow retries for local model preflight

- labels: `cron_automation, local_model_providers, config, reliability`
- strict_easy: `False`
- reasons: `possible_confusions=2`
- confidence: `0.94`
- ambiguity: `{'level': 'low', 'possible_confusions': ['model_serving', 'gateway'], 'why_not_hard': 'The PR explicitly describes configurable retries for isolated cron local-model provider preflight, with clear config and reliability implications.'}`
