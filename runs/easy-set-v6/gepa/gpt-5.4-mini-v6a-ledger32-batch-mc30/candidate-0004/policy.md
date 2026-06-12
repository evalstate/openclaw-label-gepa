# Decision Procedure

Read title and main problem/feature first; use body, labels, files, and diff only to confirm central maintainer-owned concerns. Select every allowed topic that is a central routed deliverable, not every mentioned mechanism. Prefer owner surfaces, and add co-labels when another surface’s behavior, contract, state, or user-visible delivery is explicitly changed.

# Cardinality Rules

Use 1-3 topics by default, 4-5 only for genuinely cross-cutting work; never more than 5. Do not drop a qualifying central co-label for brevity. Drop topics that are only locations, examples, dependencies, implementation mechanisms, or consequences. For bugs, add `reliability` only when operational failure handling is central: timeout, crash, stuck state, retry, durable loss, cleanup, recovery, leak, overload, race, cap, or lifecycle failure.

# Boundary Overlays

- Add `telemetry_usage` whenever counts, tokens, costs, usage freshness, metrics, diagnostics, traces, or status reporting data are central, including when displayed in UI/status/footer. Pair with `ui_tui` when the user-facing display is changed.
- Add `ui_tui` for TUI/UI status, footer, dashboard, lists, message extraction/rendering, or visible interaction changes. Do not replace it with `api_surface` unless an external CLI/HTTP/SDK contract itself changes.
- Use `api_surface` only for caller-visible external contracts: endpoint/CLI/SDK shape, fields, statuses, compatibility, webhooks, SSE, or documented command behavior. Internal status text, UI events, helpers, parsing, and display-only usage data are not enough.
- Add `tests_ci` when the item is itself about tests, regression coverage, fixtures, mocks, CI, or platform test fixes; do not add it merely because a product change includes tests.
- Add `notifications` when outbound reply/send delivery, completion announcements, notify gates/settings, sent-message state, delivery payload/path, expiration, or delivery recovery is central. Chat ingestion alone stays `chat_integrations`.
- Add `hooks` when hook registration, emission, events, priority, filters, payload, or hook security is a deliverable. Chat reply hooks usually co-label `chat_integrations` and `notifications`.
- Add `coding_agents` for user-visible agent/subagent/child/follow-up orchestration, handoff, parent orchestration, result announcement, give-up behavior, or lifecycle, including when driven by ACP, sessions, cron, or queues. Do not use it for runtime internals alone.
- If ACPX is explicitly owned, include `acpx`; also include `acp` when ACP runtime/protocol, session, binding, parent/child behavior, node/result delivery, or Codex ACP compatibility is central.
- Add `codex` for Codex runtime/auth/ACP/plugin/command compatibility. Add `security` when credential isolation, auth bridging, token scope, private boundaries, permission boundaries, or secret exposure are central.
- Add `self_hosted_inference` for engine setup, preflight, lifecycle, compatibility, crashes/timeouts, retries, or backends; provider API request/response/streaming/vision/TTS/embedding handling stays `inference_api`.
- Keep `gateway` for gateway-owned routes, daemon startup, protocol, state, health, restart, or gateway-owned execution; not generic provider proxying, notifications, orchestration, or app-runtime failures.
- Add `config` only for operator-facing settings, defaults, persisted shape, env/config loading, validation, repair, setup, policy, allow/deny options, or migration. A setting named only as an implementation detail or documentation example is not enough.
- Add `approvals` for permission prompts, decisions, modes, pending approval state, expiry, caps, persistence, or cleanup, including when surfaced through MCP.
- Documentation-only changes include `docs` plus the documented owner surface(s), not every contextual mechanism.

# Suppression Rules

- Do not infer topics from filenames, package names, labels, or isolated keywords when the main deliverable names another owner.
- Do not add `reliability` for wrong field mapping, empty/wrong content, formatting, visibility, ranking, ordering, wording, or ordinary product semantics unless durable loss, recovery, cleanup, retry, crash, timeout, leak, cap, or stuck behavior is central.
- Do not add `config` for docs that merely clarify behavior, steering, defaults in prose, examples, or internal constants.
- Do not add `memory` for pending state, context windows, transcripts, sessions, leaks, or generic remembering; require memory indexing/search, embeddings/vector/provider state, active memory, or memory archival/recovery.
- Do not add `self_hosted_inference` just because a self-hosted engine is named in an API-compatibility issue.
- Do not add `tool_calling` for generic tools, queues, command output, screenshots, streaming prose, chat sends, or boundaries; require model tool-call protocol, deltas, schemas, transcript/result routing, or rendering.
- Do not add `gateway`, `api_surface`, or `agent_runtime` unless that boundary owns the externally relevant change.
- Return only the required concise JSON object; no prose, explanations, or extra fields.