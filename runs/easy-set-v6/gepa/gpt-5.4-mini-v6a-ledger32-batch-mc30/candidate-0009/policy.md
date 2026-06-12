# Decision Procedure

Read title and main problem/feature first; use body, labels, files, and diff only to confirm central maintainer-owned concerns. Select every allowed topic that is a central routed deliverable, not every mentioned mechanism. Prefer owner surfaces; add co-labels when another surface’s behavior, contract, state, lifecycle, or user-visible delivery is explicitly changed.

# Cardinality Rules

Use 1-3 topics by default, 4-5 only for genuinely cross-cutting work; never more than 5. Do not drop a qualifying central co-label for brevity. Drop topics that are only locations, examples, dependencies, implementation mechanisms, or consequences. For bugs, add `reliability` only when operational failure handling is central: timeout, crash, stuck state, retry, durable loss/drop, cleanup, recovery, leak, overload, race, cap, TTL/expiry, or lifecycle failure.

# Boundary Overlays

- Add `coding_agents` when user-visible agent/subagent/child/follow-up orchestration changes: handoff, parent control, pass-through vs orchestration, running-state gating, result delivery/announcement, give-up behavior, lifecycle, or cleanup while agents are active. Pair with `acp`, `sessions`, `cron_automation`, `queueing`, `notifications`, or `reliability` when those owners are also central; do not use it for runtime internals alone.
- Add `notifications` when outbound reply/send delivery, completion announcements, notify gates/settings, sent-message state, delivery payload/path, expiration/disappearing/TTL behavior, or delivery recovery is central. Chat ingestion alone stays `chat_integrations`; chat-surface changes that alter outbound delivery semantics co-label `notifications`.
- Add `reliability` for explicit retry/preflight recovery, silent result loss/drop prevention, premature cleanup, stuck/running-state failures, timeout/crash/leak/overload/race handling, lifecycle cleanup, caps, TTL/expiry, or recovery from operational failure. Do not add it for ordinary wrong content, wording, display, mapping, or generic bug fixes.
- Add `hooks` when hook registration, emission, events, priority, filters, payload, or hook security is a deliverable.
- Add `approvals` for permission prompts, decisions, modes, pending approval/permission state, expiry/TTL, caps, persistence, or cleanup, including when surfaced through MCP or motivated by reliability.
- Add `self_hosted_inference` for self-hosted or on-device engine setup, preflight, lifecycle, compatibility, crashes/timeouts, retries, or backends. Provider API request/response/streaming/vision/TTS/embedding handling stays `inference_api`; model-artifact or hardware behavior stays `local_models`.
- Add `telemetry_usage` whenever counts, tokens, costs, usage freshness, metrics, diagnostics, traces, or status reporting data are central, including UI/status/footer display. Pair with `ui_tui` when the user-facing display changes.
- Add `ui_tui` for TUI/UI status, footer, dashboard, lists, message extraction/rendering, or visible interaction changes. Do not replace it with `api_surface` unless an external CLI/HTTP/SDK contract itself changes.
- Use `api_surface` only when the caller-visible external contract changes: endpoint/CLI/SDK shape, fields, statuses, compatibility, webhooks, SSE, or documented command behavior. ACP/ACPX node/result delivery correctness, internal helpers, parsing, UI events, status text, inference integration, and gateway process ownership are not enough.
- Add `tests_ci` when the item is itself about tests, regression coverage, fixtures, mocks, CI, or platform test fixes; do not add it merely because a product change includes tests.
- If ACPX is explicitly owned, include `acpx`; also include `acp` when ACP runtime/protocol, session, binding, parent/child behavior, node/result delivery, follow-ups, or Codex ACP compatibility is central.
- Add `codex` for Codex runtime/auth/ACP/plugin/command compatibility. Add `security` when credential isolation, auth bridging, token scope, private boundaries, permission boundaries, or secret exposure are central.
- Keep `gateway` for gateway-owned routes, daemon startup, protocol, state, health, restart, or gateway-owned execution; not generic provider proxying, notifications, orchestration, or app-runtime failures.
- Add `config` only for operator-facing settings, defaults, persisted shape, env/config loading, validation, repair, setup, policy, allow/deny options, or migration.
- Documentation-only changes include `docs` plus the documented owner surface(s), not every contextual mechanism.

# Suppression Rules

- Do not infer topics from filenames, package names, labels, isolated keywords, examples, or incidental mentions when the main deliverable names another owner.
- Do not add `config` for docs that merely clarify behavior, steering, defaults in prose, examples, or internal constants.
- Do not add `memory` for pending state, context windows, transcripts, sessions, leaks, or generic remembering; require memory indexing/search, embeddings/vector/provider state, active memory, or memory archival/recovery.
- Do not add `self_hosted_inference` just because a self-hosted engine is named in an API-compatibility issue.
- Do not add `skills_plugins` for provider prompt hints, extension packages, review skills, or hook/channel events unless plugin/skill manifest, loading, SDK/runtime API, sync/prelude/wrappers, SecretRefs, doctor/check, or Policy plugin behavior is central.
- Do not add `tool_calling` for generic tools, queues, command output, screenshots, streaming prose, chat sends, docs about tool boundaries, or boundaries; require model tool-call protocol, deltas, schemas, transcript/result routing, or rendering.
- Do not add `gateway`, `api_surface`, or `agent_runtime` unless that boundary owns the externally relevant change.
- Return only the required concise JSON object; no prose, explanations, or extra fields.