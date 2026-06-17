# OpenClaw topic-boundary guidance

Apply these rules as boundary overlays on top of the allowed-topic taxonomy.
They are not extra labels and do not replace the topic definitions.

Classify for maintainer topic inventory and evaluation, not code search.

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
central to the item, not merely mentioned.

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

## Inference family disambiguation

Pick within the inference topics by the owning layer:

- `inference_api` = the API/INTEGRATION layer between OpenClaw and model
  serving/providers: Responses, Chat Completions, Anthropic Messages and
  similar inference APIs (including TTS/vision/embeddings), streaming/usage
  chunks, base URL normalization, and adding/configuring inference providers.
- `self_hosted_inference` = the ENGINE layer: integration with vLLM,
  llama.cpp, Ollama, LM Studio, TGI, LocalAI — on device or self-hosted
  elsewhere — engine setup, lifecycle, compatibility, crashes/timeouts, and
  self-hosted embeddings/speech/memory backends.
- `local_models` = the MODEL-ARTIFACT/HARDWARE layer on device: GGUF and
  quantization behavior, VRAM/hardware constraints, model-family quirks, local
  model UX/fallback/context behavior.
- `model_lifecycle` = catalog/config lifecycle: introducing, decommissioning,
  or adjusting model configurations and metadata.

Layer test: which would the maintainer change to fix it — the API client
(`inference_api`), the engine hookup (`self_hosted_inference`), expectations
about the model/hardware (`local_models`), or the model catalog/config
(`model_lifecycle`)? Co-label when the item genuinely changes more than one
layer. Never substitute `config` or `docs` for this family when a
provider/engine/model integration is the central subject.

## `local_models`

- MUST include: model-artifact or local-hardware behavior on device — GGUF or
  quantization behavior, VRAM/local hardware constraints, model-family quirks,
  local model UX/fallback, or local model context behavior.
- Do not include: engine setup/integration (`self_hosted_inference`), inference
  API/protocol issues (`inference_api`), or a local backend named only as an
  example.

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
  and self-hosted embeddings/speech/memory backends.
- Do not include: generic hosted inference API usage (`inference_api`), or
  model-artifact/hardware behavior (`local_models`).
- Boundary: "self-hosted" includes on-device engines; the boundary with
  `local_models` is engine integration vs model/hardware behavior.

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
- Co-label: add `acp` alongside when protocol-level binding/override/delivery
  semantics are involved, not purely ACPX transport/worker.

## `acp`

- MUST include: ACP runtime/protocol, ACP session, ACP binding, ACP
  parent/child behavior, or ACP delivery is central.
- Do not include: merely because an item mentions an agent session or internal
  runtime behavior.

## `coding_agents`

- MUST include: integrations with external coding agents in general, or with a
  specific coding agent such as Codex, Claude Code, Gemini CLI, or Pi.
- Do not include: internal OpenClaw subagents, `sessions_spawn` plumbing, ACP
  parent/child behavior, queue lanes, trace producers, tool-use mechanics,
  approval flows, sandboxing, compaction, or agent runtime machinery unless the
  item is specifically about a coding-agent integration.
- Boundary: ACP is an integration protocol and is distinct from coding-agent
  integrations; route ACP protocol/session/delivery work to `acp`/`acpx`.
  OpenClaw's internal agent runtime is a core product surface; route startup,
  loop, backend, model-call orchestration, and adapter machinery to
  `agent_runtime`.

## `mcp_tooling`

- MUST include: MCP server allow/deny rules, MCP conformance checks, MCP
  handshake/tool behavior, MCP config, or MCP tool routing.
- Do not include: MCP appearing only in examples or incidental config.

## `codex`

- MUST include: Codex runtime, Codex auth, Codex ACP, Codex plugin, or Codex
  harness behavior is central.
- Do not include: generic coding-agent workflows without Codex specifics.

## `agent_runtime`

- MUST include: agent runtime startup, loop, backend, model call orchestration,
  runtime adapter behavior, or runtime ownership/execution architecture is
  central.
- Do not include: ACPX worker internals alone (`acpx`) or any agent-adjacent
  provider/UI/config change. Do not route internal runtime work to
  `coding_agents` unless the item is specifically about an external coding-agent
  integration.

## `sessions`

- MUST include: session lifecycle, state, storage, identity, binding, or
  cleanup is central.
- Do not include: every mention of session context or session files.

## `gateway`

- MUST include: gateway routing, gateway state, gateway startup, gateway
  protocol, or gateway-owned execution is central.
- Do not include: ordinary provider proxy, HTTP compatibility, or app-runtime
  bugs unless the gateway is the owning boundary.

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

- MUST include: UI/TUI display, status, footer, mobile UI, or visual
  interaction is central.
- Do not include: command internals, telemetry fields, or API behavior not
  shown to users.

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

- MUST include: SSRF, private-network access, credential/auth boundaries,
  permissions, sandbox escape, secret leakage, supply-chain hardening, or
  access-control evidence.
- Do not include: generic privacy preference wording with no boundary,
  exposure, or access-control substance.
- Boundary: credential/auth boundary and permission-posture rows satisfy
  security, normally co-labeled with `auth_identity` (mechanics) and/or
  `sandboxing` (isolation).

## `config`

- MUST include: configuration schemas, persisted config shape, config loading,
  config validation, config repair, environment/config defaults,
  operator-facing config options, allow/deny configuration, or policy settings.
- Do not include: a config key that is merely the internal mechanism, example,
  or implementation detail of another surface's change.
- Boundary: operator-facing config options qualify on their own.

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

- MUST include: token counts, usage counts, costs, metrics, diagnostics,
  traces, or status reporting are central.
- Do not include: generic reliability or UI text without measurement/status data.

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
- Do not include: chat-platform-specific behavior alone (`chat_integrations`)
  or reliability-only recovery.
- Co-label: when a chat-surface change implements or alters a delivery
  payload/path or delivery gates, add notifications alongside the chat label.

## `skills_plugins`

- MUST include: the item changes, extends, validates, documents, or adds
  doctor/check behavior for a plugin or skill surface. The bundled Policy
  plugin is a plugin surface: if Policy plugin behavior is central, include
  skills_plugins even when model, MCP, security, or config topics are also
  central.
- Do not include: an extension package or review skill merely mentioned, or
  channel/event hooks that do not touch plugin SDK/loading/manifest surfaces.

## `auth_identity`

- MUST include: authentication, OAuth, credential propagation, identity
  overlay, auth profile selection, or account/user identity is central.
- Do not include: generic provider config without identity/auth mechanics.
- Co-label: add `security` when credential/auth boundaries or permission
  posture are involved (see security).

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
- Co-label: parameter coercion/normalization for tool invocation is
  tool_calling, even inside an MCP bundle or adapter.
