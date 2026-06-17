# Decision Procedure

Read title/problem first; use body/comments/files/diff only to confirm central ownership. Choose every allowed topic whose maintainer must review the changed behavior, contract, state, lifecycle, policy, delivery path, or user surface.

Prefer the product surface being changed over symptoms, hosts, paths, helpers, examples, platform/package names, or failure words. A co-label qualifies only when that surface is independently changed.

# Cardinality Rules

Use 1-3 topics normally; 4-5 only for genuinely cross-cutting changes; never more than 5. Include all clear owners, then prune weak extras.

Final pass: drop labels supported only by bug/fix/fail wording, files/tests/examples, internal constants, config key names, generic session/context/message/tool terms, or consequences of another owner.

# Boundary Overlays

- Add `reliability` only for concrete runtime resilience semantics: retry/timeout/backoff, crash/leak/race/overload recovery, cleanup of stuck/terminal state, caps/TTL, durable failure handling, data-loss recovery, or lifecycle invariants. Suppress for ordinary correctness, stale/hidden values, bad rendering, missing text/payloads, provider/API format compatibility, unsupported option removal, and tests/build speed.
- Add `notifications` for outbound user delivery: notify/announce/ack/completion behavior, delivery gates, reply payloads, sent-message reconciliation, dropped delivery, or chat reply expiration. Chat delivery/path/payload changes usually need `chat_integrations` plus `notifications`; add `reliability` only when failure/recovery mechanics also change.
- Add `telemetry_usage` for counts, costs, metrics, traces, diagnostics, or status reporting, including freshness/correctness and user-visible display. Prefer it over `reliability` for stale or incorrect counters/status.
- Add `tool_calling` only for the model tool-call protocol: function/tool schemas, deltas, tool-result transcript/routing, or invocation parameter coercion. Suppress for shell/command output, chat replies, provider content blocks, TTS/vision/screenshots, UI text, and config-like options.
- Add `coding_agents` when a coding-agent or subagent product flow/integration is the changed surface, including managed flows around Codex, Claude Code, Gemini CLI, Pi, or similar agents. Do not replace it with `gateway`, `sessions`, or `agent_runtime` just because those host the flow.
- ACP routing: include `acp` for protocol, session, node, binding, parent/child, follow-up, output, or delivery semantics; include `acpx` for ACPX transport, proxy, worker/backend, binding, or managed process. Wrong or empty ACP outputs are ACP/ACPX, not `reliability`, unless recovery is added.
- Use `sessions` only for session identity, lifecycle, persistence, binding, transcript, resume/reset, store/cleanup, or parent-child session state. Suppress for generic context, terminal artifacts, notifications, coding-agent hosts, or files merely mentioning sessions.
- Use `gateway` only for gateway routes, protocol, state, startup/restart, health, or gateway-owned execution. Suppress when it merely hosts chat config, notifications, subagents, provider proxying, or API handlers owned elsewhere.
- Add `ui_tui` for OpenClaw UI/TUI/dashboard/mobile/status/visual interactions. Suppress for chat-platform menus/messages, CLI/API internals, non-visible telemetry fields, or message wording outside an OpenClaw UI surface.
- Add `chat_integrations` only for named chat platforms, channel adapters, chat ingestion, or chat delivery surfaces. Suppress for generic assistant messages, OpenClaw UI controls, or non-chat delivery.
- Add `config` only for operator/user-facing config, persisted schema/defaults/loading/validation/repair, environment/options, policy/allow-deny, or migration. Suppress for internal constants, unsupported options, build/test knobs, or config keys used only to implement another owner.
- Add `tests_ci` when tests, CI, fixtures, mocks, smoke tests, or test/build infrastructure are the subject. Pair with `packaging_deployment` for installer/image/build smoke or speed work; do not add `config` or `reliability` unless runtime behavior also changes.
- Add `approvals` for approval prompts, decisions, modes, or pending approval state. Pending permission/approval TTL, caps, close-clear, or leak cleanup is `approvals` plus `reliability`; not `memory` unless memory systems change.
- Use `memory` only for memory search/indexing, embeddings/vector stores, provider state, archival/recovery, or active-memory behavior; not generic remembered state, transcripts, pending queues, approvals, or session state.
- Provider/model boundary: use `inference_api` for provider API rendering, streaming, content blocks, usage chunks, catalogs, auth/routing, or compatibility. Add `self_hosted_inference` for local/self-hosted engine setup, lifecycle, health/preflight, crashes/timeouts, or backend compatibility. Use `local_models` only for artifacts, hardware, model-family quirks, or local context UX.
- Add `codex` only for Codex runtime, auth, ACP, plugin, or command compatibility, not cosmetic app/UI changes. Add `auth_identity` for auth bridges, account/profile selection, or credential propagation. Add `security` for credential boundaries, isolated homes, token scope, private access, permissions, secret exposure, sandbox escape, or access control.
- Add `hooks`, `api_surface`, or `skills_plugins` only when that external/product contract changes; chat acknowledgements alone are notifications/chat, not API surface.

# Suppression Rules

Suppress labels inferred only from paths, packages, tests, examples, platform names, or incidental mentions. Suppress `reliability` without concrete resilience mechanics; `tool_calling` without model tool-call protocol changes; and `sessions`/`gateway`/`agent_runtime` when they merely host ACP, coding-agent, chat, notification, or provider work. Prefer replacing a weak extra with the specific missed owner instead of adding both.