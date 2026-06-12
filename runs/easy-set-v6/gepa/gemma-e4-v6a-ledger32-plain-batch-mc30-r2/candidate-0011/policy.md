# Decision Procedure

Read the title and main request first; use body, labels, files, and diff only to confirm central ownership. Choose topics whose maintainers must review the intended behavior, contract, state, lifecycle, policy, or delivery path.

Route by changed product surface, not by keyword, path, helper, symptom, test fixture, or consequence. A co-label qualifies only when that surface independently changes; if evidence is weak, choose the smaller set.

# Cardinality Rules

Default to 1-3 topics; use 4-5 only when each label has its own review owner; never more than 5. Start with the central surface, then add only explicit co-labels for operator config, external/API contract, delivery/notification, auth/security boundary, persistent state/lifecycle, queue/dispatch, or recovery mechanics.

Final prune: drop labels supported only by generic bug/fix/failure words, filenames, tests, examples, platform/package names, internal constants, incidental config keys, session/context mentions, message/tool wording, or side effects of another selected surface.

# Boundary Overlays

- Add `reliability` only when the fix itself changes operational failure handling or lifecycle safeguards: retries/backoff, timeouts, crash/leak cleanup, TTL/caps/close-clear, terminal/stuck state recovery, dropped work/data recovery, races, overload, or durable cleanup. Do not add it for stale counts/status, wrong rendering/output, empty content/replies, compatibility/config acceptance, UI/API/chat option corrections, memory ranking, test/build speed, or a bug whose remedy is wholly another surface.
- `telemetry_usage` owns token/usage/cost counts, metrics, traces, diagnostics, freshness, and status reporting; pair with `ui_tui` when the reporting is displayed. Prefer it over `reliability` for stale or incorrect counters/status.
- Add `notifications` for outbound delivery, replies, acknowledgements, completion payload/path, announcements, notify settings, delivery gates, and sent-message handling. Chat send/reply/ack changes usually need both `chat_integrations` and `notifications`; add `reliability` only for failed/dropped delivery recovery or reconciliation.
- Add `chat_integrations` only for named chat platforms, channel adapters, chat ingestion, or chat delivery surfaces. Suppress it for generic assistant messages, UI copy/rendering, or message wording outside a chat integration.
- Add `coding_agents` for subagent or external coding-agent product flows/integrations when handoff, scheduling, notification, session use, or integration behavior changes. Do not substitute `agent_runtime` or `gateway`; use those only when their own core surface changes. Pure Codex auth/ACP/command compatibility can be `codex`/`acp`/`acpx` without `coding_agents`.
- For ACP/ACPX: include `acp` for ACP protocol, session, node, binding, parent-child, output, or delivery semantics; include `acpx` for ACPX transport, proxy, worker, backend, or binding. Wrong/empty ACP output is `acp`/`acpx`, not `reliability`, unless recovery mechanics change.
- Use `sessions` only for session identity, lifecycle, persistence, binding, transcript, resume/reset, cleanup, stores, or parent/child state; not for context mentions, terminal artifacts, notification paths, or subagent mentions alone.
- Use `gateway` only for gateway routes, protocol, state, startup/restart, health, or gateway-owned execution. Suppress it when gateway code merely hosts another surface.
- Use `tool_calling` only for the model tool-call protocol: schemas, deltas, function/tool-call transcript, result routing, or invocation parameter coercion. Exclude command output, ACP/chat replies, TTS, thinking/content blocks, screenshots/vision, provider rendering, and config-like options.
- Use `approvals` for permission prompts, approval decisions/modes, and pending approval state. Bounding, expiring, persisting, or clearing pending approvals is `approvals` plus `reliability`, not `memory`.
- Use `memory` only for memory indexing/search, embeddings/vector stores, provider state, archival/recovery, or active memory behavior; not generic remembered state, context, transcripts, pending queues, or approvals.
- Use `config` only for operator-facing settings, persisted schemas/defaults, loading/validation/repair, environment/policy/allow-deny options, or migration. Suppress it for build/test knobs, examples, internal constants, or implementation keys.
- Use `tests_ci` when tests, CI, fixtures, smoke tests, mocks, or platform test infrastructure are the subject. For install/build/image/release smoke or speed work, pair `tests_ci` with `packaging_deployment`; do not add `config` or `reliability` unless runtime/operator behavior changes.
- Provider API/rendering, streaming, TTS, vision, embeddings, usage chunks, catalogs, auth/routing, or compatibility belongs to `inference_api`; add `self_hosted_inference` for local/self-hosted engine setup, lifecycle, preflight, backend compatibility, crash, or timeout behavior, even when triggered by automation.
- Add `codex` for Codex runtime, auth, ACP, plugin, or command compatibility; cosmetic app/UI changes stay `ui_tui`. Add `auth_identity` for auth bridges, account binding, credential propagation, profile/scope selection, or token-only auth. Add `security` for isolated homes, credential boundaries, token scope, private access, permissions, secret exposure, sandbox escape, or access control.
- Add `hooks`, `api_surface`, or `skills_plugins` only when their event, external contract, or plugin/skill surface directly changes. Slash commands, chat acknowledgements, and provider internals are not `api_surface` unless a documented external API/CLI/SDK/HTTP contract changes.
- Add `queueing` for lanes, task state, dispatch ordering, locks, backpressure, stuck jobs, or follow-up queues when those mechanics independently change.

# Suppression Rules

- Suppress `reliability` unless a reliability/on-call owner must review new recovery, lifecycle, or safeguard behavior.
- Suppress `tool_calling`, `agent_runtime`, `gateway`, `chat_integrations`, `config`, `memory`, and `api_surface` when triggered only by words, paths, helpers, or implementation details rather than central changed behavior.
- When a row has both a symptom and a concrete surface fix, label the surface fix; add symptom topics only if their contract changes too.
- Prefer exact smaller sets; remove any label you cannot justify as an independent maintainer-routing owner.