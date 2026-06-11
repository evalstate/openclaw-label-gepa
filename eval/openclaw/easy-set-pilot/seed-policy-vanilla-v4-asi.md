Classify the GitHub issue or pull request for OpenClaw maintainer-interest routing.

Use only the supplied GitHub context. Prefer the title and main problem or feature
statement. Use body, comments, labels, changed files, and diff as supporting evidence.

Select every allowed topic that is central to routing the item to the right maintainer
interest. Do not select topics that are only incidental implementation details,
examples, tests, file paths, helper names, or possible consequences.

Use the smallest label set that captures distinct central routing interests, but do not
collapse explicit central co-labels. If the title/body makes multiple maintainer-owned
surfaces central, include each one.

Return an empty list only if no allowed topic centrally applies.

## Benchmark-aligned boundary overlays

The following overlays match the benchmark dynamic ASI (`openclaw_benchmark.TOPIC_HINTS`).
Use false-positive guards as exclusion gates and false-negative guards as positive central
evidence reminders. These are boundary overlays on top of the allowed-topic taxonomy, not
extra labels and not a replacement for the topic definitions.

# OpenClaw topic-boundary guidance

Generated from `src/openclaw_gepa/openclaw_benchmark.py` `TOPIC_HINTS`.
Keep this file synchronized with the benchmark dynamic ASI; do not hand-edit
topic guidance here without updating/checking the source hints.

Use these as boundary overlays on top of the allowed-topic taxonomy. They are
not extra labels and do not replace the topic definitions.

## `api_surface`

- False-positive guard: Tighten api_surface: require public API, CLI/API contract, HTTP contract, request/response shape, or compatibility contract. Exclude internal helpers, payload parsing, status text, UI events, ordinary commands, and local model compatibility.
- False-negative guard: Add api_surface when a public API, CLI/API contract, HTTP request/response shape, schema, or compatibility contract is central.

## `notifications`

- False-positive guard: Tighten notifications: require notification policy/routing/delivery/maintainer alert mechanics. Exclude chat-specific behavior, reliability-only recovery, or generic message text.
- False-negative guard: Add notifications for generic notification delivery, routing, maintainer alerts, notifier policy, announcements, or delivery gates.

## `coding_agents`

- False-positive guard: Tighten coding_agents: require an external coding-agent backend/run such as Codex, Claude Code, Gemini CLI/coding agents, Pi, or coding-agent harness/tools/approvals. Do not use for internal OpenClaw subagent/session/queue/lock orchestration; prefer agent_runtime/sessions/queueing.
- False-negative guard: Improve coding_agents recall: add when Codex, Claude Code, Gemini CLI/coding agents, Pi, external coding-agent harnesses, coding-agent approvals/sandboxing/tools, or provider behavior breaking an external coding-agent turn is central.

## `local_model_providers`

- False-positive guard: Tighten local_model_providers: require local, self-hosted, or user-configured OpenAI-compatible provider setup/routing/auth/discovery/compatibility. Do not use for ordinary hosted cloud providers such as Vertex/Azure/Bedrock/Anthropic/DeepInfra/OpenRouter, local lifecycle knobs, model serving endpoint behavior, hosted catalogs, or generic local model mentions.
- False-negative guard: Add local_model_providers when local/self-hosted/user-configured OpenAI-compatible provider setup, auth, discovery, routing, model resolution, or adapter compatibility is central.

## `local_models`

- False-positive guard: Tighten local_models: require concrete local/on-device inference, backend, model-family, or hardware behavior (LM Studio/Ollama/llama.cpp/GGUF/local GPU/ggml-metal). Do not use merely for OpenAI-compatible API/protocol issues.
- False-negative guard: Add local_models when local backend execution, local model UX, local hardware/VRAM/cold-start, llama.cpp/Ollama/LM Studio inference behavior, or local model crash/timeout is central.

## `config`

- False-positive guard: Tighten config: do not add merely because an option, payload field, or example exists. Use only for config schema, persisted config, setup options, defaults, validation, or config read/write policy.
- False-negative guard: Add config when setup options, defaults, validation, persisted config, config schema, or config read/write policy are central.

## `reliability`

- False-positive guard: Tighten reliability: do not use as a generic bug tag. Require timeout, crash, hang, retry, stuck state, data loss, cleanup, lifecycle recovery, fallback loop, or leak evidence.
- False-negative guard: Add reliability for crashes, hangs, timeouts, data loss, retries, fallback/recovery, stale state, cleanup, stuck lifecycle, or operational failure behavior.

## `sessions`

- False-positive guard: Tighten sessions: require session lifecycle/state/storage/identity boundaries; do not use for every mention of session context or files.
- False-negative guard: Add sessions when session lifecycle, state, persistence, identity, isolation, resume, or storage behavior is central.

## `model_serving`

- False-positive guard: Tighten model_serving only when endpoint/protocol/model-serving behavior is central. Do not use for pure config metadata with no serving behavior, or local provider setup without endpoint compatibility.
- False-negative guard: Add model_serving for hosted or local model endpoint behavior: Responses/Chat Completions, streaming/SSE, model registration/selection, endpoint lifecycle, serving metadata, request routing, or provider endpoint compatibility.

## `skills_plugins`

- False-positive guard: Tighten skills_plugins: require a real skill/plugin surface such as plugin manifests/loading/registration, plugin SDK/runtime APIs, skill files/prelude/sync/wrappers, hooks, SecretRefs, MCP Apps, or plugin-owned user-visible behavior. Do not add just because an extension package or review skill is mentioned.
- False-negative guard: Add skills_plugins for SKILL.md/managed skills, plugin manifests/loading/registration, plugin SDK/runtime APIs, plugin hooks, SecretRefs, skill sync/prelude/wrappers, MCP Apps, or plugin-owned tools/resources/UI.

## `chat_integrations`

- False-positive guard: Tighten chat_integrations: require a named chat surface or user-facing chat integration behavior, not generic message delivery/recovery.
- False-negative guard: Add chat_integrations for named Discord, Telegram, Slack, Zulip, Feishu, Matrix, webchat, or similar integration behavior.

## `tool_calling`

- False-positive guard: Tighten tool_calling: require tool-call semantics/transcript/result handling; exclude generic command output, TTS, browser screenshot/vision, or config-like options.
- False-negative guard: Add tool_calling for structured tool result display, stdout rendering for tool results, pre-tool text preservation, or tool-call transcript/content semantics.

## `gateway`

- False-positive guard: Tighten gateway: require gateway service/process/boundary/startup/routing ownership or gateway-managed sidecars. Exclude ordinary provider proxy, HTTP compatibility, browser command, or app-runtime bugs unless the gateway is the owning boundary.
- False-negative guard: Add gateway when the gateway service, cgroup/process tree, startup, managed sidecars, routing boundary, or gateway-owned lifecycle is central.

## `exec_tools`

- False-positive guard: Tighten exec_tools: require shell/PTY command execution, subprocess lifecycle, command approval/allowlist, browser command launch, TTS/speech execution, or execution output handling. Exclude API/tool schema semantics.
- False-negative guard: Add exec_tools when shell/PTY commands, subprocesses, browser command launch, sidecar execution, command approval/allowlist, or execution output handling is central.

## `agent_runtime`

- False-positive guard: Tighten agent_runtime: require core agent turn/runtime/planning/execution lifecycle behavior, not any agent-adjacent provider, UI, or config change.
- False-negative guard: Add agent_runtime when the core agent turn lifecycle, runtime plan, harness execution path, agent state machine, or embedded runner behavior is central.

## `telemetry_usage`

- False-positive guard: Tighten telemetry_usage: require usage/count/token/cost/metric/log/trace/quota/status diagnostics. Exclude generic reliability or UI text without measurement/status data.
- False-negative guard: Add telemetry_usage for token/usage/cost counters, diagnostics, metrics, traces, usage chunks, quota/status reporting, or run logs.

## `browser_automation`

- False-positive guard: Tighten browser_automation: require browser launch/control/CDP/Chrome/Playwright/screenshot/extension/proxy behavior, not generic UI or web API behavior.
- False-negative guard: Add browser_automation for browser command launch, Chrome/DevTools/CDP, Playwright, screenshots, webview automation, browser profile/proxy/extension, or browser sidecars.

## `tests_ci`

- False-positive guard: Tighten tests_ci: require tests, CI workflow, coverage, flake handling, lint/typecheck, or validation tooling as a central subject. Do not add only because a PR includes tests.
- False-negative guard: Add tests_ci when test coverage, CI behavior, flakiness, validation scripts, lint/typecheck, or regression guardrails are central to the item.

## `ui_tui`

- False-positive guard: Tighten ui_tui: require user-facing display/help/status/wizard/TUI/visual state. Exclude ordinary command internals, telemetry fields, or API behavior not shown to users.
- False-negative guard: Add ui_tui for visible CLI/TUI/web UI output, help/status displays, user-facing settings screens, wizards, progress indicators, or presentation changes.

## `auth_identity`

- False-positive guard: Tighten auth_identity: require auth profile, token, credential, identity, permission, or account boundary. Exclude generic provider config or security wording without identity/auth mechanics.
- False-negative guard: Add auth_identity for auth profiles, tokens, credentials, account identity, permission checks, login/session identity, or auth-bound routing.

## `self_hosted_inference`

- False-positive guard: Tighten self_hosted_inference: require self-operated inference services or locally operated inference backends, including embeddings, speech, or memory providers. Exclude ordinary hosted cloud providers, generic local provider config, or endpoint protocol behavior better covered by model_serving.
- False-negative guard: Add self_hosted_inference when self-hosted inference backends, private/local inference servers, self-hosted embeddings/speech/memory providers, proxy bypass for private inference, or operator-run inference services are central.

## `open_weight_models`

- False-positive guard: Tighten open_weight_models: require open-weight model families, weights, quantization, context metadata for open-weight families, packaging/deployability, or hosted catalogs of open-weight models. Do not add merely because a provider serves a named model.
- False-negative guard: Add open_weight_models when named open-weight families, model weights, GGUF/quantization, context windows for open-weight models, model cards/checkpoints, or open-weight catalog metadata are central.

## `model_releases`

- False-positive guard: Tighten model_releases: require new, renamed, deprecated, or version-specific model availability, provider catalog updates, release metadata, or release tracking. Do not add merely because a model name appears.
- False-negative guard: Add model_releases when adding/removing/updating model IDs, provider catalogs, release notes, model-family availability, version-specific model support, or deprecation/rename behavior is central.

## `acp`

- False-positive guard: Tighten acp: require ACP protocol/runtime/session binding/delivery semantics. Do not add merely because an item mentions an agent session or internal runtime behavior.
- False-negative guard: Add acp when ACP protocol, ACP session tools, ACP binding, ACP parent/child delivery, ACP blocks, acp_send, sessions_spawn/cancel, or ACP client/server compatibility is central.

## `acpx`

- False-positive guard: Tighten acpx: require ACPX-specific runtime, proxy, backend, worker, transport, configured binding, command, auth, or compatibility behavior. Do not use for generic ACP issues.
- False-negative guard: Add acpx when files, commands, runtime paths, worker/proxy behavior, transport, configured binding, HMAC/auth, or compatibility are explicitly ACPX-specific.

## `codex`

- False-positive guard: Tighten codex: require the Codex runtime, Codex CLI, Codex ACP, Codex auth, Codex command compatibility, or Codex harness behavior. Do not add merely because a coding-agent-like workflow is discussed.
- False-negative guard: Add codex when Codex-specific runtime behavior, auth, ACP integration, command execution, plugin behavior, or harness compatibility is central.

## `mcp_tooling`

- False-positive guard: Tighten mcp_tooling: require MCP server/client behavior, MCP config, tool/resource/prompt listing, tool invocation, handshake, routing, allow/deny policy, or MCP conformance. Do not add merely because MCP appears in examples or incidental config.
- False-negative guard: Add mcp_tooling for MCP servers/clients, tools/list, resources/list, prompts/list, MCP tool routing, MCP config, MCP allow/deny rules, MCP conformance checks, or MCP invocation compatibility.

## `approvals`

- False-positive guard: Tighten approvals: require approval prompts, approve/deny decisions, permission modes, pending approval state, approval policy checks, or approval UI/commands. Do not add merely because a command or tool might require permission.
- False-negative guard: Add approvals when permission decisions, approval mode behavior, approve/reject flow, approval queues/state, exec approvals, or tool allow/deny decisions are central.

## `sandboxing`

- False-positive guard: Tighten sandboxing: require containment or isolation behavior such as sandbox policy, inherited sandbox state, filesystem/process/container boundaries, sandbox escape, volumes, or runtime isolation. Do not add merely because command execution or security is mentioned.
- False-negative guard: Add sandboxing when sandbox inheritance, sandbox escape/prevention, path isolation, containers, filesystem hiding, process limits, Docker/bubblewrap, or workspace boundary behavior is central.

## `hooks`

- False-positive guard: Tighten hooks: require hook registration, lifecycle, trigger filtering, priority/order, payload shape, hook execution, hook security, or managed hook behavior. Do not add for generic plugin behavior unless hook mechanics are the owner surface.
- False-negative guard: Add hooks when before/after lifecycle events, hook priority, hook ingress, hook payload validation, hook execution policy, managed hooks, or hook security are central.

## `cron_automation`

- False-positive guard: Tighten cron_automation: require scheduled, recurring, or one-shot automation, cron jobs, force-run behavior, or job lifecycle. Do not add merely because an agent/runtime heartbeat is mentioned.
- False-negative guard: Add cron_automation when cron jobs, scheduled runs, recurring task execution, force-run, deleteAfterRun, at-jobs, heartbeat automation jobs, or scheduler behavior is central.

## `memory`

- False-positive guard: Tighten memory: require memory systems such as indexing, recall, active memory, embeddings/vector stores, memory provider state, archival, or recovery. Do not add merely for context window, session state, transcript, or generic remembering.
- False-negative guard: Add memory when memory indexing/search, active-memory recall, embeddings, vector/LanceDB storage, memory provider config/state, archive/recovery, or memory hook behavior is central.

## `security`

- False-positive guard: Tighten security: require concrete security posture such as SSRF/private network access, secrets/credentials/token leakage, auth hardening, permission boundaries, sandbox escape, vulnerability prevention, supply-chain hardening, redaction, or unsafe access control. Do not add for generic privacy preferences or ordinary auth/profile configuration without security risk.
- False-negative guard: Add security when SSRF, private/internal network access, credential/secret/token exposure, HMAC/signature hardening, unsafe permissions, sandbox escape, vulnerability mitigation, redaction, supply-chain hardening, or access-control enforcement is central.

## `queueing`

- False-positive guard: Tighten queueing: require queues, lanes, locks, pending/running state, scheduling, ordering, dispatch, backpressure, or stuck work queues. Do not add for any async/background task unless queue mechanics are the owner boundary.
- False-negative guard: Add queueing when task queues, lanes, follow-up queues, run ordering, work dispatch, locks, pending/running state, backpressure, or stuck queue behavior is central.

## `docs`

- False-positive guard: Tighten docs: require documentation, guides, README/reference text, spelling, taxonomy wording, or explanatory content to be the central subject. Do not add merely because docs are updated alongside implementation.
- False-negative guard: Add docs when the item's main subject is documentation, examples/guides as docs, README/reference changes, explanatory text, taxonomy wording, or doc-only corrections.

## `packaging_deployment`

- False-positive guard: Tighten packaging_deployment: require packaging, installers, release artifacts, Docker images, service managers, build distribution, dependency packaging, or deployment/runtime distribution. Do not add for ordinary runtime config.
- False-negative guard: Add packaging_deployment when build/package/release artifacts, Docker images, SEA/single executable, systemd/launchd service files, installer behavior, dependency packaging, or deployment paths are central.
