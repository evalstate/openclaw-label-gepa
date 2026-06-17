# Decision Procedure

Read the title and main problem/feature statement first; use body, comments,
labels, files, and diff only to confirm central ownership. Choose every allowed
topic whose maintainer must review the intended behavior or contract.

Prefer the product surface being changed over symptoms, file locations,
implementation helpers, examples, or failure words. A co-label qualifies only
when that surface's contract, state, lifecycle, policy, delivery path, or user
behavior is independently changed.

# Cardinality Rules

Use 1-3 topics by default; use 4-5 only for genuinely cross-cutting changes;
never more than 5. Include all clearly qualifying central topics, but remove
weak extras before final output.

Final pruning test: drop any label supported only by a generic bug/fix word,
changed path, test/build knob, example platform, config key name, session/context
mention, message/tool wording, or consequence of another surface.

# Boundary Overlays

- Add `reliability` only for operational failure-handling changes: retries,
  timeouts, crashes, leaks, caps/TTL, cleanup, stuck/terminal state, data loss,
  races, overload, or recovery. Do not add it for ordinary bugs, wrong or stale
  values, display/rendering fixes, missing payload text, provider/API
  compatibility, CI-only failures, or failures that merely motivate another
  surface.
- Add `telemetry_usage` when token/usage/cost counts, metrics, traces,
  diagnostics, status, freshness, or reporting are central, including through
  UI, gateway, API, or sessions. Prefer it over `reliability` for stale or
  incorrect counters/status.
- Add `notifications` for outbound delivery, completion/ack behavior,
  announcements, delivery gates, sent-message handling, or reply payloads.
  Chat delivery changes commonly need both `chat_integrations` and
  `notifications`.
- Add `chat_integrations` only for a named chat platform, channel adapter,
  message ingestion, or chat delivery surface. Do not add it for generic
  assistant messages, UI copy/rendering, or non-chat message actions.
- Add `coding_agents` for external or OpenClaw-managed coding-agent
  integrations/flows, including subagent-style integrations with Codex, Claude
  Code, Gemini CLI, Pi, or similar. Do not replace it with `gateway`,
  `sessions`, or `agent_runtime` unless those surfaces independently change.
- For ACP/ACPX work, include `acp` for ACP protocol, node, session, binding,
  parent/child, follow-up, output, or delivery semantics; include `acpx` when
  ACPX transport/proxy/worker/binding/managed backend is central. Wrong or empty
  ACP outputs are `acp`/`acpx`, not `reliability`, unless recovery behavior is
  added.
- Use `sessions` only for session lifecycle, identity, persistence, binding,
  transcript, resume/reset, parent/child state, stores, or cleanup. Do not add
  it for ordinary context, terminal artifacts, notification paths, or files that
  merely mention sessions.
- Use `gateway` only for gateway routing, state, startup, protocol,
  gateway-owned execution, routes, restart, or service health. Suppress it when
  the gateway is merely the host/path for chat config, subagents, notifications,
  provider proxying, or API handlers owned by another surface.
- Use `tool_calling` only for model tool-call protocol, deltas, schemas, tool
  result transcript/routing, or parameter coercion for tool invocation. Do not
  add it for command output, chat replies, TTS, prompt hints, thinking/content
  blocks, screenshots, browser vision, or config-like options.
- Use `approvals` for permission prompts, approval decisions/modes, pending
  approval state, or approval TTL/caps/cleanup. Pending approval leaks are
  `approvals` plus `reliability`, not `memory`, unless the memory system itself
  changes.
- Use `memory` only for memory indexing/search, embeddings/vector stores,
  provider state, archival/recovery, or active memory behavior; not for generic
  remembered state, context, transcripts, or pending queues.
- Use `config` only for operator-facing settings, persisted schema/defaults,
  loading, validation, repair, policy/allow-deny options, environment options,
  or migration. Do not add it for build/test knobs, internal constants, or
  config keys used only to implement another surface.
- Use `tests_ci` when tests, CI, fixtures, mocks, smoke tests, or platform test
  infrastructure are the subject. Pair with `packaging_deployment` for
  build/install/image smoke or speed work; do not add `reliability` or `config`
  unless runtime behavior or operator config also changes.
- For provider/API rendering, streaming, TTS, vision, embeddings, usage chunks,
  catalogs, auth/routing, or compatibility, prefer `inference_api`; add
  `self_hosted_inference` only when engine setup, lifecycle, compatibility,
  crashes/timeouts, or local/self-hosted backend behavior is central.
- Add `codex` only when Codex runtime, auth, ACP, plugin, or command
  compatibility is central; suppress it for cosmetic app/UI changes. Add
  `auth_identity` for auth bridges, account binding, credential propagation,
  profile/scope selection, or token-only auth. Add `security` for credential
  boundaries, isolated homes, token scope, private access, permissions, secret
  exposure, sandbox escape, or access control.
- Add `hooks` when hook emission, registration, ordering, payload, filtering,
  execution, or hook security is central. Add `api_surface` only for external
  API/CLI/HTTP/SDK contracts, request/response shapes, webhooks, SSE, or
  documented command contracts. Add `skills_plugins` only for skill/plugin
  surfaces, manifests, loading, SDK/runtime APIs, SecretRefs, MCP Apps, or
  plugin/skill doctor/check behavior.

# Suppression Rules

- Suppress `reliability` for generic bugs, UI/API corrections, stale metrics,
  provider formatting/rendering mismatches, missing notification payloads,
  test-speed work, or compatibility fixes without recovery mechanics.
- Suppress `tool_calling` unless the model tool-call contract itself changes.
- Suppress `api_surface` for slash commands, chat acknowledgements, UI actions,
  or provider internals unless an external contract changes.
- Suppress `agent_runtime` for ACP orchestration or coding-agent integration
  unless core startup, loop, backend, adapter, or model-call orchestration is
  the deliverable.
- Suppress labels inferred only from paths, tests, examples, package names,
  platform names, or incidental mentions when the title/body identify another
  owner.