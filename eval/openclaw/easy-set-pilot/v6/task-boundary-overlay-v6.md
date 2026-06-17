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
auth, routing, catalogs, compatibility). `self_hosted_inference` = the ENGINE
layer: integration with vLLM, llama.cpp, Ollama, LM Studio, TGI, LocalAI — on
device or self-hosted elsewhere — engine setup, lifecycle, compatibility,
crashes/timeouts, and self-hosted embeddings/speech/memory backends.
`local_models` = the MODEL-ARTIFACT/HARDWARE layer on device: GGUF/quantization
behavior, VRAM/hardware constraints, model-family quirks, local model
UX/fallback/context. `model_lifecycle` = introducing, decommissioning, or
adjusting model configurations, catalogs, and metadata. Layer test: which
would the maintainer change to fix it — the API client, the engine hookup,
expectations about the model/hardware, or the model catalog/config? Never
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
- `security`: SSRF, private-network access, credential/auth boundaries,
  permissions, secret leakage, sandbox escape, supply-chain hardening, access
  control. Credential/auth-boundary rows take `security` AND `auth_identity`
  (mechanics); isolation behavior also takes `sandboxing`.
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
- `coding_agent_integrations` vs `agent_runtime`/`acp`: use `coding_agent_integrations` only for
  integrations with external coding agents in general or with a specific coding
  agent such as Codex, Claude Code, Gemini CLI, or Pi. Internal OpenClaw
  subagents, `sessions_spawn` plumbing, ACP parent/child behavior, queue lanes,
  trace producers, tool-use mechanics, approval flows, sandboxing, compaction,
  and runtime machinery do not imply `coding_agent_integrations`; route those to `acp`,
  `acpx`, `agent_runtime`, `sessions`, `queueing`, `tool_calling`,
  `approvals`, or `sandboxing` as appropriate.
- `acpx`/`acp`: ACPX worker/transport/binding internals → `acpx`; add `acp`
  when protocol-level binding/override/delivery semantics are involved. ACPX
  internals alone do not imply `agent_runtime` or `exec_tools`.
- `queueing`: queues, lanes, scheduling, ordering, work dispatch; locks that
  gate dispatch/pending-running state count, a mutex implementation detail
  does not. Keep the co-label when lane/lock/state mechanics change inside a
  session or ACP flow.
- `notifications`: outbound notifications, completion delivery, delivery
  gates, announcements. A chat-surface change that implements or alters a
  delivery payload/path takes notifications alongside the chat label.
- `hooks` vs `skills_plugins`: channel/event hooks are `hooks` (+ the chat
  surface); `skills_plugins` only when plugin SDK/loading/manifest or a skill/
  plugin surface (including the Policy plugin) is changed, validated, or given
  doctor/check behavior.
- `docs`: only when documentation itself is the subject — and a docs-only item
  still carries the product topic whose behavior is centrally documented.
- `tool_calling`: tool-call protocol, function/tool schemas, result transcript
  handling, tool-call rendering; parameter coercion for tool invocation counts,
  even inside an MCP bundle.
