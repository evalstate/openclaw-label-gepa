## Boundary overlay (fixed)

Classify for maintainer topic inventory, not code search. Apply these rules on
top of the topic definitions; they are not extra labels.

### Cardinality law

- Use 1-3 topics by default; 4-5 only when the item is genuinely cross-cutting
  and each topic is central. Never more than 5; if more qualify, keep the 5
  strongest central owner boundaries. Return [] when no topic applies.
- Include every topic whose inclusion rule is satisfied — do not drop a
  qualifying topic to keep the output short.
- Do not add topics supported only by changed files, tests added alongside a
  change, examples, incidental helper code, or weak downstream consequences.

### Conformance and policy rows

- Allow/deny rules, conformance checks, or doctor checks: include the checked
  domains, plus `config` when the rules/settings are operator-visible or
  persisted; plus `security` for private-network/SSRF/credential/auth/
  permission posture; plus `inference_api` for provider refs/catalogs/
  routing; plus `mcp_tooling` for MCP servers/tools.
- Work on the bundled Policy plugin (a plugin surface) requires
  `skills_plugins`, even when model/MCP/security/config topics also apply.

### Inference family

`inference_api` = the API/INTEGRATION layer between OpenClaw and model
serving/providers: Responses, Chat Completions, Anthropic Messages and similar
inference APIs (including TTS/vision/embeddings), streaming/usage chunks,
base-URL normalization, and adding/configuring inference providers (setup,
auth, routing, catalogs, compatibility). `self_hosted_inference` = the local or
self-hosted inference layer: integration with vLLM, llama.cpp, Ollama, LM
Studio, TGI, LocalAI; on-device engine setup/lifecycle/compatibility/crashes;
self-hosted embeddings/speech/memory backends; and local model operation such
as GGUF/quantization, VRAM/hardware constraints, model-family quirks, local
model UX/fallback/context. `model_lifecycle` = introducing, decommissioning, or
adjusting model configurations, catalogs, and metadata. Layer test: which
would the maintainer change to fix it — the API client, the local/self-hosted
inference hookup or model operation, or the model catalog/config? Never
substitute `config` or `docs` for this family when a provider/engine/model
integration is the central subject.

### High-traffic boundaries

- `reliability`: timeout, crash, leak, stuck state, retry, data loss, cleanup,
  recovery, overload, or operational failure mode as a deliverable — including
  docs/tests whose subject is that behavior. Not a generic bug tag; CI-only
  failures are `tests_ci`.
- `api_surface`: external API, CLI, HTTP, SDK, or documented command contracts.
  If the item changes WHAT an external contract promises, label api_surface
  even when the implementation lives in the gateway or a serving endpoint.
- `config`: schemas, persisted shape, loading/validation/repair, defaults,
  allow/deny configuration, policy settings, and adding or changing user- or
  operator-facing settings — toggles, pickers, defaults, persisted
  preferences, including when surfaced through a settings UI. A config key as
  mere mechanism of another surface does not qualify.
- `security`: concrete security issues, improvements, or direct security
  features: SSRF, private-network access, credential/secret/token exposure or
  hardening, auth or permission boundary changes, access-control enforcement,
  sandbox escape/isolation hardening, vulnerability mitigation, supply-chain
  hardening, or signature/HMAC/verification behavior. Do not include
  privacy-focused features, disappearing messages, retention/visibility
  preferences, generic privacy UX, or ordinary auth/profile configuration
  unless they change a security control. `auth_identity` rows co-label
  `security` only when they change an access rule, exposure path, permission
  check, credential/secret/token handling, signature/HMAC/verification, or
  auth-boundary hardening; isolation behavior also takes `sandboxing`.
- `auth_identity`: only when OpenClaw's own authentication/identity surface is
  the subject — login, auth profiles, OAuth flows, tokens, account binding,
  credential propagation. Authentication of external services touched
  incidentally by another surface's change does not qualify.
- `ui_tui`: only when the UI display, interaction, navigation, rendering, or
  user-facing control behavior is itself the failing or changed surface. A
  defect merely observed or triggered through a dashboard, button, status
  count, tool list, or footer belongs to the surface that actually fails.
- `telemetry_usage`: only when OpenClaw's own telemetry/usage surface is the
  subject — token/usage/cost accounting, diagnostics, trace production and
  observability coverage, status reporting. Benchmark or measurement
  vocabulary adjacent to another surface's change does not qualify.
- `coding_agent_integrations` vs internal orchestration: include
  `coding_agent_integrations` when OpenClaw changes how it integrates with,
  launches, configures, authenticates, routes to, adapts, or preserves
  compatibility for an external coding-agent runtime or CLI such as Pi, Codex,
  Claude Code, Gemini CLI, or similar. Do not key on internal mechanism names.
  First identify the actor whose behavior changes: external coding-agent
  contract -> `coding_agent_integrations`; internal OpenClaw run/session/
  message/tool/approval/sandbox/trace behavior -> the concrete internal owner
  (`agent_runtime`, `acp`, `acpx`, `sessions`, `queueing`, `tool_calling`,
  `approvals`, `sandboxing`, or `telemetry_usage`).
- `acpx`/`acp`: ACPX worker/transport/binding internals → `acpx`; add `acp`
  only when ACP protocol behavior is changed: binding/override, spawn/cancel
  semantics, parent/child message relay, event streams, completion delivery,
  message blocks, or client/server compatibility. Pure ACPX worker/transport/
  harness/proxy/command/auth/compatibility internals do not imply `acp`,
  `agent_runtime`, or `exec_tools`.
- `acp` vs `sessions`: `acp` owns what parent/child messages mean and how they
  are delivered (relay, event streams, completion notify, binding/override);
  `sessions` owns the session records — identity, lifecycle, state,
  persistence, cleanup, stores. Co-label only when the item changes both the
  protocol behavior and the session object's lifecycle or state.
- `queueing`: queues, lanes, scheduling, ordering, work dispatch; locks that
  gate dispatch/pending-running state count, a mutex implementation detail
  does not. Keep the co-label when lane/lock/state mechanics change inside a
  session or ACP flow.
- `notifications`: include only when an outbound delivery path, sent-message
  handling, completion/notification delivery gate, notify setting, or
  announcement behavior is implemented or changed. Emitting events/hooks about
  sends is `hooks`; reliability-only recovery is `reliability`; named chat
  behavior without a changed outbound delivery path/gate is `chat_integrations`
  only.
- `hooks` vs `skills_plugins`: channel/event hooks are `hooks` (+ the chat
  surface); `skills_plugins` only when plugin SDK/loading/manifest or a skill/
  plugin surface (including the Policy plugin) is changed, validated, or given
  doctor/check behavior.
- `docs`: only when documentation itself is the subject — and a docs-only item
  still carries the product topic whose behavior is centrally documented.
- `tool_calling`: tool-call protocol, function/tool schemas, result transcript
  handling, tool-call rendering; parameter coercion for tool invocation counts,
  even inside an MCP bundle.
