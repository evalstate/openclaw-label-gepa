# easy-set-pilot rationales

## openclaw-openclaw-41892 — feat(control-ui): add cron calendar timeline view

- labels: `ui_tui, cron_automation`
- `ui_tui`: PR adds a Control UI / Cron Jobs page view with a 24h timeline strip, hover popups, theme support, and i18n; changes are in ui/src/ui/views/cron.ts and CSS — a user-facing interface feature.
- `cron_automation`: The view visualizes scheduled cron jobs (24h timeline, NOW indicator, high-frequency chips, run history navigation) and touches src/cron/service; central to cron scheduling display.

## openclaw-openclaw-43416 — feat(ui): add copy button for assistant messages

- labels: `ui_tui`
- `ui_tui`: PR adds a user-facing copy button to assistant chat message bubbles in the macOS/iOS chat UI (ChatMessageViews.swift), a pure UI/UX enhancement.

## openclaw-openclaw-46740 — ACP: classify silent acpx exits as backend unavailable

- labels: `acpx, acp, reliability`
- `acpx`: Changes live in extensions/acpx/src/runtime.ts and classify silent acpx process exits; cue 'silent acpx exit' and acpx backend behavior are central.
- `acp`: Touches src/acp/control-plane/manager.core.ts and ACP runtime error codes (ACP_BACKEND_UNAVAILABLE vs ACP_TURN_FAILED), core ACP protocol error classification.
- `reliability`: Reclassifies backend process crashes/silent non-zero exits to provide accurate recovery guidance (/acp doctor); handling of disappearing/crashed backend is a reliability fix.

## openclaw-openclaw-47187 — fix(ui): reset transient chat overlays and style context notice

- labels: `ui_tui`
- `ui_tui`: PR fixes Control UI chat surface: adds CSS for context-notice and clears transient slash/search overlay state during rerenders; all changes in ui/src styles and chat views.

## openclaw-openclaw-47243 — feat(ui): add timestamp and preview to session list

- labels: `ui_tui, sessions`
- `ui_tui`: PR is feat(ui) adding timestamp and last-message preview rendering in the session list view (ui/src/ui/views/sessions.ts), a user-facing interface change.
- `sessions`: Changes operate on session list rows (GatewaySessionRow), session controller list call, and per-session display to distinguish sessions.

## openclaw-openclaw-48260 — feat(ui): add active time summary to usage overview

- labels: `ui_tui, telemetry_usage`
- `ui_tui`: PR adds an 'Active Time' card to the Usage Overview dashboard, a UI-only display change across ui/src/ui/views and i18n locales.
- `telemetry_usage`: Surfaces usage accounting metrics (total active time, average session duration, durationSumMs) on the usage page.

## openclaw-openclaw-65187 — test: add regression tests for <final> tag stripping in UI message extraction

- labels: `tests_ci, ui_tui`
- `tests_ci`: PR is test-only, adding 4 regression test cases to message-extract.test.ts with no production code changes.
- `ui_tui`: Tests cover Control UI chat message extraction (ui/src/ui/chat), stripping internal tags from the chat surface.

## openclaw-openclaw-72085 — docs(commands): document bashForegroundMs clamp bounds (0–30 000 ms)

- labels: `docs, config`
- `docs`: Pure documentation change adding a bullet to docs/gateway/configuration-reference.md; explicitly scoped 'documentation only, no code touched'.
- `config`: Documents the accepted range and silent-clamp behavior of the configuration key bashForegroundMs in the configuration reference.

## openclaw-openclaw-84668 — docs(agent-runtimes): clarify model name vs runtime routing for Codex (#84637)

- labels: `docs, agent_runtime, codex`
- `docs`: Documentation-only PR (+25/-0) adding a Warning block to docs/concepts/agent-runtimes.md; explicitly labeled docs and bypasses CLI proof gate as docs-only.
- `agent_runtime`: Content clarifies runtime routing via agentRuntime.id (pi, codex, claude-cli) versus model selection, central to agent runtime concepts.
- `codex`: Explicitly distinguishes Codex runtime/harness from gpt-*-codex model IDs and the /codex chat command; Codex routing is the core subject.

## openclaw-openclaw-84740 — Feature Request: Option to hide/suppress certain sessions from the session list

- labels: `sessions, ui_tui`
- `sessions`: Request centers on session list management: hiding/archiving specific sessions, suppressing short-lived/isolated sessions, persisted archive state—core session UX behavior.
- `ui_tui`: Explicitly about cluttered session list view, hide/archive row action, and improving UI/UX for finding active sessions.
