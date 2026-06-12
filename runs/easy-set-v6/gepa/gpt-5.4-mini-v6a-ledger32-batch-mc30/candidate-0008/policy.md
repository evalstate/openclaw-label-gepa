# Decision Procedure

Read title/main request first; use body, labels, files, and diff only to confirm central maintainer-owned deliverables. Label every allowed topic whose owner must act on behavior, contract, state, lifecycle, routing, or user-visible delivery. Do not label incidental mechanisms.

# Cardinality Rules

Use 1-3 topics normally; 4-5 only for explicit cross-surface work; never more than 5. Do not drop a qualifying co-label for brevity. Drop topics that are only locations, examples, dependencies, side effects, or implementation details. For bugs, add `reliability` only when operational failure handling is central: timeout, crash, stuck state, retry, durable loss/drop, cleanup, recovery, leak, overload, race, cap, TTL, expiry, or lifecycle failure.

# Boundary Overlays

- Add `coding_agents` when user-visible subagent/child/follow-up/agent orchestration changes: handoff, parent control, running-state gates, result delivery/announcement, give-up behavior, lifecycle, or active-agent cleanup. Pair with `acp`, `sessions`, `cron_automation`, `queueing`, `notifications`, or `reliability` when those owners are also central. Do not use it for runtime internals alone.
- Add `notifications` for outbound reply/send delivery, completion announcements, notify gates/settings, sent-message state, delivery payload/path, expiration/disappearing-message behavior, or delivery recovery. Chat ingestion alone stays `chat_integrations`; chat delivery/lifetime controls co-label `notifications`.
- Add `reliability` for retries, preflight retry policy, silent result drops, lost delivery, premature cleanup, stuck/active-state mistakes, recovery, or lifecycle failure, even when another owner supplies the feature. Do not use it for ordinary wrong fields, wording, formatting, ranking, or visibility.
- Add `hooks` when hook registration, emission, event shape, priority, filters, payload, managed hooks, or hook security is a deliverable.
- Add `approvals` for permission prompts/decisions/modes, pending approval state, expiry/TTL, caps, persistence, cleanup, or approval policy checks.
- Add `self_hosted_inference` for self-hosted/on-device engine setup, preflight, lifecycle, compatibility, crashes/timeouts, retries, or backends. Provider request/response/streaming/vision/TTS/embeddings stay `inference_api`; model artifacts or hardware stay `local_models`.
- Add `telemetry_usage` when counts, tokens, costs, metrics, traces, diagnostics, usage freshness, or status-reporting data are central; pair with `ui_tui` for user-facing display changes.
- Add `ui_tui` for TUI/UI status, footer, dashboard, lists, message extraction/rendering, or visible interaction changes. Do not substitute `api_surface` unless an external CLI/HTTP/SDK contract changes.
- Use `api_surface` only for caller-visible external contracts: endpoints, CLI/SDK shape, fields, statuses, compatibility, webhooks, SSE, or documented command behavior.
- Add `tests_ci` only when tests, fixtures, CI, coverage, mocks, or platform test infrastructure are themselves the subject.
- If ACPX is explicitly owned, include `acpx`; also include `acp` when ACP runtime/protocol, session, binding, parent/child behavior, node/result delivery, or Codex ACP compatibility is central.
- Add `codex` for Codex runtime/auth/ACP/plugin/command compatibility. Add `security` for credential isolation, auth bridging, token scope, private boundaries, permission boundaries, secret exposure, or vulnerability work.
- Keep `gateway` for gateway-owned routes, daemon startup, protocol, state, health, restart, or gateway-owned execution; not generic provider proxying or app-runtime failures.
- Add `config` only for operator-facing settings, defaults, persisted shape, env/config loading, validation, repair, setup, policy, allow/deny options, or migration.
- Documentation-only changes include `docs` plus the documented owner surface(s), not every contextual mechanism.

# Suppression Rules

- Do not infer topics from filenames, package names, labels, isolated keywords, examples, or incidental mentions when the main deliverable names another owner.
- Do not add `config` for docs that merely clarify behavior, steering, defaults in prose, examples, or internal constants.
- Do not add `memory` for pending state, context windows, transcripts, sessions, leaks, or generic remembering; require memory indexing/search, embeddings/vector/provider state, active memory, or memory archival/recovery.
- Do not add `self_hosted_inference` just because a self-hosted engine is named in an API-compatibility issue.
- Do not add `skills_plugins` for provider prompt hints, extension packages, review skills, or hook/channel events unless plugin/skill manifest, loading, SDK/runtime API, sync/prelude/wrappers, SecretRefs, doctor/check, or Policy plugin behavior is central.
- Do not add `tool_calling` for generic tools, queues, command output, screenshots, streaming prose, chat sends, docs mentions of tool boundaries, or boundary wording; require model tool-call protocol, deltas, schemas, transcript/result routing, or rendering as the documented/product subject.
- Do not add `gateway`, `api_surface`, or `agent_runtime` unless that boundary owns the externally relevant change.
- Return only the required concise JSON object; no prose, explanations, or extra fields.