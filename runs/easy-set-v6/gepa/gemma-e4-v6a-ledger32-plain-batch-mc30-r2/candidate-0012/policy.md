# Decision Procedure

Read the title and main problem/feature statement first; use body, comments,
labels, changed files, and diff only to confirm or disambiguate central
interests. Select every allowed topic that is a central maintainer-owned
concern under the fixed taxonomy and boundary overlay.

# Cardinality Rules

Include every topic whose inclusion rule in the fixed overlay is satisfied; do
not drop a qualifying topic to keep the output short. Use 1-3 topics by
default, 4-5 only when genuinely cross-cutting, never more than 5. Drop labels
that are only symptom locations, mechanisms, paths, examples, or consequences.
For row-exactness, prefer replacing a generic symptom label with the specific
surface label that owns the deliverable.

# Boundary Overlays

- Add `telemetry_usage` whenever the central user-visible or API concern is
  usage/status accounting, token/cost/count freshness, diagnostics, metrics, or
  traces; do not convert these to `reliability` just because values are stale or
  wrong.
- Add `notifications` when the change alters outbound delivery, acknowledgements,
  announcements, completion/result delivery, delivery gates, sent-message
  behavior, or chat reply payload paths; chat-surface delivery changes usually
  co-label `chat_integrations` and `notifications`.
- Add `coding_agents` for external coding-agent or subagent product behavior,
  including managed agent follow-ups, announcements, give-up/result delivery, or
  scheduled agent work. Do not replace it with `agent_runtime` unless the runtime
  loop/backend/orchestration machinery itself is the deliverable.
- For ACP work, include `acp` for protocol/session/binding/parent-child/delivery
  semantics even when `acpx` is also present; include `acpx` when the ACPX
  transport/proxy/worker/binding surface is explicitly central.
- Add `sessions` only when identity, lifecycle, persistence, transcript,
  resume/reset, binding, cleanup, or parent/child state is central; thread-bound
  or parent-orchestrated follow-up behavior can qualify. Mere session context,
  files, or display state does not.
- Add `approvals` for permission decisions, prompts, pending approval state, TTLs,
  caps, clearing, or approval-mode behavior even when surfaced through MCP or
  another adapter.
- Add `hooks` when emitted hook events, hook payloads, hook ordering/filtering, or
  managed hook behavior is changed; do not hide hook work under reliability.
- Add `tests_ci` for smoke tests, CI/build-test speed, fixtures, coverage, mocks,
  or test infrastructure as the maintained surface, even when Docker or install
  machinery is involved.
- Add `security` for credential isolation/bridging, auth-boundary exposure,
  unsupported credential scope, sandbox escape, private access, token leakage, or
  other boundary hardening; do not collapse these into reliability.
- Add `self_hosted_inference` when cron/config/preflight/provider work is about a
  self-hosted engine or local serving backend; keep `local_models` for model
  artifact/hardware behavior rather than engine integration.
- Use `api_surface` only for external contract shape or documented endpoint/CLI/SDK
  behavior. Chat slash-command acknowledgements or platform replies are usually
  `chat_integrations` plus `notifications`, not `api_surface`.
- Use `config` only for operator-facing options, persisted schema/defaults,
  validation/repair, policy settings, or migrations. Do not add it for an
  internal flag, test knob, build option, or implementation detail.
- Use `chat_integrations` only for a named chat platform/channel adapter or chat
  delivery surface, not for generic assistant message UI.
- Use `ui_tui` for user-facing OpenClaw UI controls, status/footer/list views,
  copy buttons, or visible app text; do not add integration labels just because
  the UI contains messages.
- Use `codex` only when Codex runtime/auth/plugin/ACP/command compatibility is
  central; a cosmetic or UI-only change in a Codex-branded app may be just
  `ui_tui`.

# Suppression Rules

- Do not add `reliability` for every bug/fix, incorrect value, missing UI text,
  provider incompatibility, or protocol output mismatch. Require a central
  operational concern such as retry/timeout, crash, leak, cap/TTL, stuck state,
  dropped work, lifecycle cleanup, race, recovery, overload, or data loss.
- Do not add `tool_calling` unless the model tool-call protocol, schemas, deltas,
  transcript/result routing, or function-call rendering is the maintained
  surface. Generic command output, API response content, ACP node output, TTS,
  vision, screenshots, or chat replies are not enough.
- Do not add `memory` for generic remembering, context, pending state, transcript,
  or recall words unless the memory/index/vector/provider surface is central.
- Do not add `gateway` merely because work passes through a daemon or service;
  require gateway-owned routes, protocol, startup, state, health, or execution.
- Do not add `agent_runtime` for ACP delivery semantics, external coding-agent
  integrations, subagent product behavior, or notification/result handling unless
  core runtime machinery is directly changed.
- Do not add `sessions` for stale counters, UI state, chat threads, or incidental
  session files unless session ownership/lifecycle/state is the deliverable.
- Do not add `config` or `packaging_deployment` from changed files alone; require
  the maintained product surface, not build/test plumbing or examples.
- When a specific surface explains the row, suppress broader symptom labels that
  only describe why the change was needed.