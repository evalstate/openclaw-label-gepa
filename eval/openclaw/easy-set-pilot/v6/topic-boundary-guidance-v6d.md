# OpenClaw topic-boundary guidance

Apply these rules as boundary overlays on top of the allowed-topic taxonomy.
They are not extra labels and do not replace the topic definitions.

Classify for maintainer topic inventory and evaluation, not code search. Each
topic names a surface a maintainer owns; a label is correct when that owner
would need to act on or review the item.

## Cardinality law

- Use 1-3 topics by default. Use 4-5 topics only when the item is genuinely
  cross-cutting and each topic is central.
- Include every topic whose MUST rule is satisfied. Do not omit a MUST topic to
  keep the output short.
- Never output more than 5 topics. If more than 5 MUST rules are satisfied,
  keep the 5 strongest central owner boundaries.
- Use an empty label set when no allowed topic applies.

## Incidental-evidence exclusion (global)

Do not add topics supported only by changed files, tests added alongside a
change, examples, incidental helper code, file paths, helper names, or weak
downstream consequences. A MUST rule is satisfied only when its subject is
central to the item, not merely mentioned. Label the surface whose behavior
the item changes, not the surfaces where the change is merely visible.

## Conformance and policy rows (compositional co-label rules)

- If an item introduces or validates allow/deny rules, conformance checks, or
  doctor checks, include the checked domains, and include `config` when those
  rules/settings are operator-visible or persisted.
- If policy/conformance work lives in, extends, documents, or adds checks for
  the Policy plugin, `skills_plugins` MUST be included.
- If the checks include private-network, SSRF, credential, auth, or permission
  posture, `security` MUST be included.
- If the checks include model providers, provider refs, provider catalogs, or
  provider routing/setup, `inference_api` MUST be included.
- If the checks include MCP servers or MCP tools, `mcp_tooling` MUST be
  included.

## Coding-agent boundary

Do not use `coding_agent_integrations` merely because the item mentions agents, subagents,
`sessions_spawn`, agent runs, tool use, approvals, sandboxing, compaction,
traces, or orchestration inside OpenClaw. Route those internal OpenClaw
concerns to the concrete owning surface instead: `agent_runtime`, `acp`,
`acpx`, `sessions`, `queueing`, `tool_calling`, `approvals`, `sandboxing`, or
`telemetry_usage`.

ACP is an integration protocol. It may be used by coding agents, but ACP work
is not `coding_agent_integrations` unless the issue or PR is specifically about a
coding-agent integration through ACP.

## Inference family disambiguation

Pick within the inference topics by the owning layer:

- `inference_api` = the API/INTEGRATION layer between OpenClaw and model
  serving/providers: Responses, Chat Completions, Anthropic Messages and
  similar inference APIs (including TTS/vision/embeddings), streaming/usage
  chunks, base URL normalization, and adding/configuring inference providers.
- `self_hosted_inference` = the ENGINE layer: integration with vLLM,
  llama.cpp, Ollama, LM Studio, TGI, LocalAI — on device or self-hosted
  elsewhere — engine setup, lifecycle, compatibility, crashes/timeouts, and
  self-hosted embeddings/speech/memory backends. This topic also owns the
  former local model-artifact/hardware layer: GGUF and quantization behavior,
  VRAM/hardware constraints, model-family quirks, local model UX/fallback, and
  local model context behavior.
- `model_lifecycle` = catalog/config lifecycle: introducing, decommissioning,
  or adjusting model configurations and metadata.

Layer test: which would the maintainer change to fix it — the API client
(`inference_api`), the engine hookup (`self_hosted_inference`), expectations
about local model operation (`self_hosted_inference`), or the model catalog/config
(`model_lifecycle`)? Co-label when the item genuinely changes more than one
layer. Never substitute `config` or `docs` for this family when a
provider/engine/model integration is the central subject.

## `inference_api`

- MUST include: the integration layer between OpenClaw and model
  serving/providers — usage of Responses, Chat Completions, Anthropic
  Messages, or similar inference APIs and integrations (including TTS, vision,
  and embeddings APIs); streaming/SSE and usage chunks; base URL
  normalization; inference request/response handling; or adding/configuring
  inference providers (setup, auth, routing, references, catalogs, allow/deny
  rules, compatibility checks).
- Do not include: OpenClaw's own external API/CLI/SDK contracts
  (`api_surface`), engine-specific hookup or lifecycle
  (`self_hosted_inference`), model catalog/config lifecycle
  (`model_lifecycle`), or pure config metadata with no inference-integration
  behavior.

## `self_hosted_inference`

- MUST include: integration with inference engines such as vLLM, llama.cpp,
  Ollama, LM Studio, TGI, or LocalAI — on device or self-hosted elsewhere —
  including engine setup, lifecycle, compatibility, engine crashes/timeouts,
  self-hosted embeddings/speech/memory backends, GGUF or quantization behavior,
  local hardware/VRAM constraints, model-family quirks, local model
  UX/fallback, or local model context behavior.
- Do not include: generic hosted inference API usage (`inference_api`) or
  catalog/default/model-ID lifecycle work (`model_lifecycle`).
- Boundary: "self-hosted" includes on-device engines and local model
  artifact/hardware behavior.

## `model_lifecycle`

- MUST include: introduction, decommissioning, or adjustment of model
  configurations — adding/removing/renaming model IDs, catalog or default
  updates, deprecations, version-specific model support, or model metadata
  (context windows, quantization variants) changes.
- Do not include: merely because a model name appears, or inference
  API-integration changes (`inference_api`).

## `acpx`

- MUST include: ACPX runtime, worker, harness, configured binding, or
  ACPX-specific compatibility is central.
- Do not include: generic ACP issues without ACPX-specific surfaces.
- Co-label test: add `acp` alongside `acpx` only when the item names ACP
  binding, override, parent/child session, or delivery semantics as behavior
  being implemented, fixed, or preserved. Pure ACPX transport, worker,
  harness, proxy, command, auth, or compatibility work does not imply `acp`.

## `acp`

- MUST include: ACP protocol semantics — binding and override, spawn/cancel,
  parent/child message relay and delivery (event streams, completion notify),
  message blocks, or ACP client/server compatibility.
- Do not include: the session objects themselves — lifecycle, state,
  persistence, storage, cleanup (`sessions`) — or items that merely run inside
  an ACP session. ACP work is not `coding_agent_integrations` unless the item
  is specifically about a coding-agent integration through ACP.
- Layer test: `acp` owns what messages between parent and child sessions mean
  and how they are delivered; `sessions` owns the session records. Co-label
  only when the item changes both the protocol behavior and the session
  object's lifecycle or state.

## `coding_agent_integrations`

- MUST include: integrations with external coding agents in general, or with a
  specific coding agent such as Codex, Claude Code, Gemini CLI, or Pi — their
  backends, runs, auth, harness compatibility, or integration behavior.
- Do not include: internal OpenClaw subagents, `sessions_spawn` plumbing, agent
  runs, tool use, approvals, sandboxing, compaction, traces, or orchestration
  inside OpenClaw. Those belong to their owning surfaces: `agent_runtime`,
  `acp`, `acpx`, `sessions`, `queueing`, `tool_calling`, `approvals`,
  `sandboxing`, or `telemetry_usage`. The owner of this topic maintains the
  external coding-agent integrations, not OpenClaw's internal agent machinery.

## `mcp_tooling`

- MUST include: MCP server allow/deny rules, MCP conformance checks, MCP
  handshake/tool behavior, MCP config, MCP tool discovery/materialization
  (tools/list), or MCP tool routing.
- Do not include: MCP appearing only in examples or incidental config.

## `codex`

- MUST include: Codex runtime, Codex auth, Codex ACP, Codex plugin, or Codex
  harness behavior is central.
- Do not include: generic coding-agent workflows without Codex specifics.

## `agent_runtime`

- MUST include: OpenClaw's internal agent machinery — runtime startup, loop,
  backends, model call orchestration, runtime adapter behavior, subagent
  execution and orchestration, or runtime ownership/execution architecture.
- Do not include: external coding-agent integrations (`coding_agent_integrations`), ACP
  protocol/session/delivery work (`acp`/`acpx`), or any agent-adjacent
  provider/UI/config change.

## `sessions`

- MUST include: the session objects themselves — session identity, lifecycle,
  state, persistence, transcript, resume, reset, cleanup, or session stores —
  including parent/child sessions when their lifecycle or state changes.
- Do not include: ACP parent/child message semantics, binding, relay, or
  delivery (`acp`), or every mention of session context or session files.

## `gateway`

- MUST include: gateway routing, gateway state, gateway startup, gateway
  protocol, gateway restart/health, or gateway-owned execution/lifecycle is
  central.
- Do not include: ordinary provider proxy, HTTP compatibility, app-runtime
  bugs, or code that merely runs in/through the gateway unless the item changes
  gateway-owned routing, state, startup, protocol, execution, or lifecycle.

## `exec_tools`

- MUST include: shell execution, command invocation, PATH, tool execution
  policy, or execution output control is central.
- Do not include: API/tool schema semantics (`tool_calling`), or ACPX/agent
  runtime internals that do not change command execution behavior.

## `approvals`

- MUST include: approval prompts, permission decisions, or approval mode
  behavior is central.
- Do not include: merely because a command or tool might require permission.
- Co-label: bounding/expiring/persisting pending-approval state is approvals
  surface even when motivated by a memory/reliability fix.

## `sandboxing`

- MUST include: sandbox policy, sandbox inheritance, sandbox escape, path
  isolation, or sandbox runtime behavior is central.
- Do not include: merely because command execution or security is mentioned.

## `hooks`

- MUST include: hook registration, hook priority, hook execution, or hook
  security is central.
- Do not include: generic plugin behavior unless hook mechanics are the owner
  surface. Channel/event hooks for a chat surface are `hooks` +
  `chat_integrations`, not `skills_plugins`, unless plugin SDK/loading is
  central.

## `cron_automation`

- MUST include: cron jobs, heartbeat runs, scheduled automation, or force-run
  behavior is central.
- Do not include: merely because an agent/runtime heartbeat is mentioned.

## `chat_integrations`

- MUST include: a named chat platform, channel adapter, message ingestion, or
  chat delivery surface is central.
- Do not include: generic message delivery/recovery without a named chat
  surface.

## `ui_tui`

- MUST include: UI/TUI display, interaction, navigation, rendering, or
  user-facing control behavior is itself the failing or changed surface —
  including status views, footer, mobile UI, and settings screens.
- Do not include: a defect merely observed or triggered through a dashboard,
  button, status count, tool list, footer, or other visible UI surface when
  the failing behavior belongs to another owner. The UI being where the user
  sees the problem does not make the UI the problem.

## `browser_automation`

- MUST include: browser/CDP/Chrome automation, browser session attach, or auth
  browser flow is central.
- Do not include: generic UI or web API behavior.

## `memory`

- MUST include: memory indexing, memory search, embeddings, active memory, or
  memory provider state is central.
- Do not include: context window, session state, transcript, or generic
  remembering.

## `security`

- MUST include: concrete security issues, security improvements, or direct
  security features: SSRF, private-network access, credential/secret/token
  exposure or hardening, auth or permission boundary changes, access-control
  enforcement, sandbox escape/isolation hardening, vulnerability mitigation,
  supply-chain hardening, or signature/HMAC/verification behavior.
- Do not include: privacy-focused product features, disappearing messages,
  retention or visibility preferences, generic privacy UX, or ordinary auth/
  profile configuration unless the item changes an access rule, exposure path,
  permission check, credential/secret/token handling, or other security
  control.
- Boundary: `auth_identity` rows co-label `security` only when they change a
  security control: access rule, exposure path, permission check, credential/
  secret/token handling, signature/HMAC/verification, or auth-boundary
  hardening. Privacy-flavored user preference or identity UX alone does not
  qualify.

## `config`

- MUST include: configuration schemas, persisted config shape, config loading,
  config validation, config repair, environment/config defaults, allow/deny
  configuration, policy settings, or adding/changing user- or operator-facing
  settings — new toggles, pickers, defaults, and persisted preferences qualify,
  including when they are surfaced through a settings UI.
- Do not include: a config key that is merely the internal mechanism, example,
  or implementation detail of another surface's change.

## `packaging_deployment`

- MUST include: packaging, installer, Docker image, release artifact,
  dependency packaging, or deployment is central.
- Do not include: ordinary runtime config.

## `docs`

- MUST include: only when documentation itself is the subject.
- Co-label: a docs-only item still carries the product topic whose behavior is
  centrally documented (e.g., a failure-recovery runbook is `docs` +
  `reliability`); `docs` alone only when the writing itself is the subject.

## `tests_ci`

- MUST include: only when tests, CI, or test infrastructure itself is the
  subject.
- Do not include: a PR merely including tests alongside a change.

## `telemetry_usage`

- MUST include: OpenClaw's own telemetry and usage surface is the subject —
  token/usage/cost accounting, metrics, diagnostics, trace production and
  observability coverage, or status reporting of the OpenClaw product.
- Do not include: measurement or benchmark vocabulary appearing near another
  surface's change. Being adjacent to benchmarking, evaluation, or numbers is
  not telemetry; the item must change or centrally concern what OpenClaw
  measures, records, or reports about itself.

## `api_surface`

- MUST include: external API, CLI, HTTP, SDK, or documented command contracts.
- Do not include: internal helpers, payload parsing, status text, UI events,
  ordinary commands, inference-integration behavior (`inference_api`), or gateway
  process ownership (`gateway`).
- Decision rule: if the item changes WHAT an external contract promises (shape,
  fields, status, compatibility), api_surface applies even when the
  implementation lives in the gateway or a serving endpoint; `docs` only when
  the contract text itself is the subject.

## `queueing`

- MUST include: queues, lanes, scheduling, task ordering, or work dispatch are
  central.
- Do not include: any async/background task without queue mechanics.
- Boundary: locks that gate dispatch/ordering/pending-running state count as
  queueing mechanics; a lock as a mere mutex implementation detail does not.

## `notifications`

- MUST include: generic outbound notifications, completion delivery, message
  delivery gates, announcements, or notify behavior is central.
- Observable test: include `notifications` only when the item implements or
  changes an outbound delivery path, sent-message handling, a completion/
  notification delivery gate, notify settings, or announcement behavior.
- Do not include: chat-platform-specific behavior alone (`chat_integrations`),
  reliability-only recovery, or emitting events/hooks about sends. Event/hook
  emission about delivery belongs to `hooks` unless the outbound delivery
  path/gate itself is implemented or changed.
- Co-label: add `notifications` alongside `chat_integrations` only when the
  chat-surface change implements or changes an outbound delivery path,
  sent-message handling, completion/notification delivery gate, notify setting,
  or announcement behavior.

## `skills_plugins`

- MUST include: the item changes, extends, validates, documents, or adds
  doctor/check behavior for a plugin or skill surface. The bundled Policy
  plugin is a plugin surface: if Policy plugin behavior is central, include
  skills_plugins even when model, MCP, security, or config topics are also
  central.
- Do not include: an extension package or review skill merely mentioned, or
  channel/event hooks that do not touch plugin SDK/loading/manifest surfaces.

## `auth_identity`

- MUST include: OpenClaw's own authentication and identity surface is the
  subject — login, auth profiles, OAuth flows, tokens, account binding,
  credential propagation, or user/device identity within the product.
- Do not include: authentication of external services touched incidentally by
  another surface's change, or generic provider config without identity/auth
  mechanics. The owner of this topic maintains how users and devices
  authenticate to OpenClaw, not every credential the product handles.
- Co-label: add `security` only when the auth/identity item changes an access
  rule, exposure path, permission check, credential/secret/token handling,
  signature/HMAC/verification, or auth-boundary hardening. Do not add
  `security` for privacy-focused identity/profile preferences without a
  security-control change.

## `reliability`

- MUST include: timeout, crash, leak, stuck state, retry, data loss, lifecycle
  cleanup, recovery, overload, or operational failure mode.
- Do not include: a generic bug tag, CI-only or test-environment failures
  (`tests_ci`), or a failure that merely motivates a change whose deliverable
  belongs entirely to another surface.

## `tool_calling`

- MUST include: tool-call protocol, tool result transcript handling,
  function/tool schema, or tool-call rendering is central.
- Do not include: generic command output, TTS, browser screenshot/vision, or
  config-like options.
