# Decision Procedure

Read the title and stated user-visible problem/feature first; use body, labels, files, and diff only to confirm central ownership. Choose topics whose maintainers must review the intended behavior or contract.

Route by the deliverable surface, not by keyword, path, helper, symptom, test fixture, package/platform name, or side effect. A co-label qualifies only when that surface's contract, state, lifecycle, policy, delivery path, or user behavior independently changes.

Before finalizing, remove any label that would not change the owning reviewer or release-note surface.

# Cardinality Rules

Default to 1-3 topics. Use 4-5 only when independent central surfaces all change; never more than 5.

Include clear co-labels, then prune weak extras. If a generic failure motivates a concrete surface fix, label the concrete surface; add `reliability` only when failure-handling behavior itself changes.

Final prune: drop labels supported only by bug wording, files, tests, examples, internal constants/flags, incidental config keys, session/context/message/tool mentions, or consequences of another selected surface.

# Boundary Overlays

- Add `reliability` only for operational failure-handling or lifecycle guarantees: retries, timeouts, crashes, leaks, cleanup/TTL/caps of internal state, terminal/stuck state, dropped work/data, races, overload, or recovery. Do not add it for ordinary bugs, wrong/empty/invisible/rendered content, stale counters/status, provider/API compatibility, UI/API corrections, chat options/payloads, CI/build speed, or fixes wholly owned by another surface.
- Use `telemetry_usage` for token/usage/cost counts, metrics, traces, diagnostics, freshness, status, or reporting. Prefer it over `reliability` for stale or incorrect counters/status; add `ui_tui` too only when displayed UI behavior changes.
- Use `notifications` for outbound delivery, replies, completion/ack behavior, announcements, notify settings, delivery gates, sent-message handling, or delivery payload/path. Chat delivery/ack/reply changes usually need both `chat_integrations` and `notifications`; add `reliability` only for central failed/dropped-delivery recovery.
- Use `chat_integrations` only for named chat platforms, channel adapters, chat ingestion, or chat delivery surfaces. Suppress it for generic assistant messages, copy/rendering UI, non-chat actions, or message wording outside a chat integration.
- Use `coding_agents` for external or OpenClaw-managed coding-agent flows, including subagents and specific coding-agent integrations. Do not substitute `agent_runtime` or `gateway` merely because they host the flow. Use `agent_runtime` only for core runtime startup, loop, backend/adapter, model-call orchestration, or ownership architecture; use `gateway` only for gateway routes, daemon/protocol/state/health, startup/restart, or gateway-owned execution.
- For ACP/ACPX: include `acp` for ACP protocol/session/node/binding/parent-child/output/delivery semantics; include `acpx` for ACPX transport/proxy/worker/backend/binding or explicitly ACPX-owned behavior. Wrong, empty, unsupported, or misdelivered ACP output/config is `acp`/`acpx`, not `reliability`, unless recovery/lifecycle handling is added.
- Use `sessions` only for session identity, lifecycle, persistence, binding, transcript, resume/reset, parent/child state, stores, or cleanup. Do not add it for context mentions, terminal artifacts, notification paths, subagent flows, or files that merely mention sessions.
- Use `approvals` for approval prompts, permission decisions/modes, pending approval state, or approval TTL/caps/cleanup. Pending approval leaks are `approvals` plus `reliability`, not `memory`, unless memory indexing/storage changes.
- Use `memory` only for memory indexing/search, embeddings/vector stores, provider state, archival/recovery, or active memory behavior; not generic remembered state, context, transcripts, pending queues, or approval state.
- Use `config` only for operator-facing settings, persisted schema/defaults, loading/validation/repair, policy/allow-deny options, environment options, or migration. Suppress it for build/test knobs, examples, internal constants, or keys used only to implement another surface.
- Use `tests_ci` when tests, CI, fixtures, smoke tests, mocks, or platform test infrastructure are the subject. Pair with `packaging_deployment` for build/install/image smoke or speed work; do not add `config` or `reliability` unless runtime/operator behavior changes.
- For provider/API rendering, streaming, TTS, vision, embeddings, usage chunks, catalogs, auth/routing, or compatibility, prefer `inference_api`. Add `self_hosted_inference` only when engine/backend setup, lifecycle, compatibility, crash/timeout, preflight, or local/self-hosted backend behavior is central; use `local_models` only for model artifacts, hardware, or model-family behavior.
- Use `tool_calling` only when the model tool-call protocol changes: schemas, deltas, tool-call/result transcript or routing, or invocation parameter coercion. Do not add it for command output, notifications, TTS, browser vision/screenshots, provider content rendering, ACP terminal artifacts, or config-like options.
- Add `codex` only for Codex runtime, auth, ACP, plugin, or command compatibility; suppress it for cosmetic app/UI changes. Add `auth_identity` for auth bridges, account binding, credential propagation, profile/scope selection, or token-only auth. Add `security` for credential boundaries, isolated homes, token scope, private access, permissions, secret exposure, sandbox escape, or access control.
- Add `hooks` for hook emission, registration, ordering, payload, filtering, execution, or hook security. Add `api_surface` only for external API/CLI/HTTP/SDK contracts, request/response shapes, webhooks, SSE, or documented command contracts. Add `skills_plugins` only for skill/plugin product surfaces.

# Suppression Rules

- Suppress `reliability` for generic bugs, display/content/API corrections, stale metrics, provider rendering/format mismatches, notification payload additions, chat message options, test/build speed, or compatibility fixes without recovery mechanics.
- Suppress `tool_calling` unless the model tool-call contract itself changes.
- Suppress `api_surface` for slash commands, chat acknowledgements, UI actions, or provider internals unless an external contract changes.
- Suppress `agent_runtime` for ACP orchestration or coding-agent integration unless core runtime machinery is the deliverable.
- Suppress labels inferred only from paths, tests, examples, package/platform names, or incidental mentions when title/body identify another owner.