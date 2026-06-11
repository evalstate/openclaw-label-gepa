## Allowed Topics v4

This is the easy-set-pilot v4 taxonomy surface. Topic IDs are unchanged from v3; v4 keeps the enum stable and uses concise model-facing definitions. Choose labels by central maintainer-routing concern, not by keyword match.

```json
[
  "local_models",
  "local_model_providers",
  "model_serving",
  "self_hosted_inference",
  "open_weight_models",
  "acpx",
  "acp",
  "coding_agents",
  "mcp_tooling",
  "hf_agents",
  "hub_workflows",
  "post_training",
  "model_releases",
  "agent_demos",
  "codex",
  "agent_runtime",
  "sessions",
  "gateway",
  "exec_tools",
  "approvals",
  "sandboxing",
  "hooks",
  "cron_automation",
  "chat_integrations",
  "ui_tui",
  "browser_automation",
  "memory",
  "security",
  "config",
  "packaging_deployment",
  "docs",
  "tests_ci",
  "telemetry_usage",
  "api_surface",
  "queueing",
  "notifications",
  "skills_plugins",
  "auth_identity",
  "reliability",
  "tool_calling"
]
```

## Topic definitions

- `local_models`: Concrete local/on-device model execution and local inference behavior: local model UX, local-only fallback, local backend crashes/timeouts, and local hardware constraints. Use when a specific local backend/model family is central, not merely because an API is OpenAI-compatible.
- `local_model_providers`: Provider configuration, discovery, auth, routing, and compatibility for local, self-hosted, or user-configured OpenAI-compatible model backends. This is the API/provider layer around local or self-hosted models, not ordinary hosted cloud providers.
- `model_serving`: Model endpoint serving protocols and compatibility for hosted or local endpoints: streaming behavior, request/response routing, lifecycle, OpenAI-compatible endpoint semantics, model registration/selection failures, and provider endpoint behavior.
- `self_hosted_inference`: Self-hosted inference systems and locally operated services, including embeddings, speech, and memory providers.
- `open_weight_models`: Open-weight model families, model packaging, quantization, and local deployability signals.
- `acpx`: ACPX protocol, transport, proxy, backend process, compatibility, and files or commands explicitly named ACPX.
- `acp`: ACP protocol features and session tools that are not necessarily ACPX-specific.
- `coding_agents`: External coding-agent integrations and runs such as Codex, Claude Code, Gemini/CLI coding agents, Pi, or coding-agent harnesses/tools/approvals/sandboxes. Do not use for purely internal OpenClaw subagent/runtime orchestration unless an external coding-agent backend is central.
- `mcp_tooling`: MCP server or client behavior, tools/list, resources, and tool invocation compatibility.
- `hf_agents`: Hugging Face agent workflows, Spaces, Hub agent demos, or HF-specific agent integrations.
- `hub_workflows`: Hub automation for datasets, models, Spaces, releases, and repository synchronization.
- `post_training`: Fine-tuning, preference optimization, evaluation loops, and data generation after pretraining.
- `model_releases`: New model release tracking or version-specific model behavior.
- `agent_demos`: Demo workflows and visible examples for agents.
- `codex`: Items that explicitly involve the Codex runtime or command compatibility.
- `agent_runtime`: Agent runner, harness, orchestration, subagent execution, heartbeat, and agent lifecycle behavior.
- `sessions`: Session identity, persistence, binding, transcript, resume, reset, parent/child session behavior, and session stores.
- `gateway`: OpenClaw gateway behavior, daemon startup, HTTP gateway routes, gateway restart, gateway state, and service health.
- `exec_tools`: Shell execution, exec tools, command allowlists, tool invocation, tool schemas, and durable process handling.
- `approvals`: Approval flows, permission modes, approve/deny commands, policy checks, and pending approval state.
- `sandboxing`: Sandbox isolation, containers, Docker, process limits, filesystem hiding, and execution boundaries.
- `hooks`: Hook lifecycle, hook events, hook payloads, hook filtering, and managed hook behavior.
- `cron_automation`: Cron jobs, scheduled runs, heartbeat automation, one-shot jobs, and recurring task execution.
- `chat_integrations`: Chat platform integrations and delivery surfaces such as Discord, Telegram, Slack, Feishu, WhatsApp, Zulip, Mattermost, and webchat.
- `ui_tui`: Control UI, TUI, dashboard, web UI, session list, status views, and user-facing interface changes.
- `browser_automation`: Browser automation, screenshots, Chrome integration, browser vision, and web interaction tooling.
- `memory`: Memory systems, embeddings, vector stores, active memory, LanceDB, and memory archival or recovery.
- `security`: Security, SSRF, credentials, secrets, token handling, auth hardening, HMAC, vulnerabilities, and unsafe access prevention.
- `config`: Configuration files, config schema, defaults, setup/onboarding, environment variables, overrides, and migration.
- `packaging_deployment`: Build, packaging, deployment, service managers, SEA, launchd, systemd, pnpm, and runtime distribution.
- `docs`: Documentation, guides, README changes, spelling, taxonomy, and explanatory content.
- `tests_ci`: Tests, CI, fixtures, coverage, mocks, and platform-specific test fixes.
- `telemetry_usage`: Usage accounting, token counts, cost metadata, traces, diagnostics, status reporting, and observability.
- `api_surface`: HTTP APIs, gateway APIs, REST endpoints, webhooks, SSE, OpenResponses, chat completions, and request/response contracts.
- `queueing`: Queues, lanes, task state, follow-up queues, run ordering, locks, stuck jobs, and backpressure.
- `notifications`: Notification policy, delivery gates, notify settings, outbound messages, announcements, and sent-message handling.
- `skills_plugins`: Skills/plugins as product surfaces: SKILL.md, managed skills, plugin manifests/loading/registration, plugin SDK/runtime APIs, MCP Apps, plugin hooks, SecretRefs, skill sync/prelude/wrappers. Do not use merely because a package is an extension or a review skill is mentioned.
- `auth_identity`: Authentication, identity, OAuth, device identity, profile selection, account binding, token-only auth, and credential scope.
- `reliability`: Reliability fixes for retries, stale state, crashes, timeouts, recovery, cleanup, race conditions, and wedged processes.
- `tool_calling`: Model tool-calling behavior, tool-call deltas, tool schemas, tool result routing, and tool-use compatibility.
