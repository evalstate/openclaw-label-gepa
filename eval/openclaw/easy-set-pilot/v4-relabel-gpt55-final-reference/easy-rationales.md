# easy-set-pilot rationales

## openclaw-openclaw-40332 — [Feature]: Per-binding and per-agent permissionMode for ACP sessions

- labels: `acp, acpx, approvals, config, security`
- `acp`: Feature is explicitly about permissionMode overrides for ACP sessions and ACP binding/runtime settings.
- `acpx`: The current global setting is named under the acpx plugin config and the issue targets ACPX permission configuration behavior.
- `approvals`: permissionMode values such as approve-all and approve-reads define approval/permission behavior for reads, writes, and shell access.
- `config`: Requested change is new configuration override locations and precedence for bindings, agent runtime, and global fallback.
- `security`: The core problem is over-permissive global access across agents with different trust levels and requests security review.

## openclaw-openclaw-41892 — feat(control-ui): add cron calendar timeline view

- labels: `cron_automation, ui_tui`
- `cron_automation`: The feature is specifically a timeline/calendar view for cron jobs and today's scheduled tasks.
- `ui_tui`: The change adds visible Control UI elements, styling, hover popups, zoom controls, and mobile fallback for the Cron Jobs page.

## openclaw-openclaw-42027 — fix: resolve exec PATH fallback, layered browser diagnostics, and cron force-run deadlock

- labels: `exec_tools, browser_automation, cron_automation, queueing, reliability`
- `exec_tools`: Exec tool PATH recovery is changed so local fallback can find login-shell-managed binaries.
- `browser_automation`: Browser status and CDP/profile reachability diagnostics are a central part of the PR.
- `cron_automation`: The PR fixes detached cron.run --force behavior for cron jobs.
- `queueing`: The cron fix introduces a separate manual lane to prevent self-deadlock on the cron execution lane.
- `reliability`: The changes target fallback failures, hard-to-triage browser errors, and a cron deadlock.

## openclaw-openclaw-42122 — Speed up install smoke Docker builds

- labels: `packaging_deployment, tests_ci`
- `packaging_deployment`: Changes the Dockerfile build path and Docker build args for smoke images, directly affecting container build/deployment packaging.
- `tests_ci`: Updates the install-smoke GitHub Actions workflow to speed up CI smoke Docker builds.

## openclaw-openclaw-42408 — [Bug/Docs]: local+hybrid memory_search quality can appear unstable due to extraPaths path drift + benchmark-file contamination

- labels: `memory, config, docs`
- `memory`: The issue is centered on memory_search/index quality, retrieval ranking, indexed corpus contamination, and local memory provider behavior.
- `config`: extraPaths path drift, path selection, and proposed exclude patterns are configuration/setup concerns affecting indexing.
- `docs`: The request explicitly asks for memory index/search documentation on path hygiene and evaluation contamination pitfalls.

## openclaw-openclaw-42425 — fix(hooks): load workspace hooks for non-default agents

- labels: `hooks, gateway, sessions`
- `hooks`: PR directly changes the internal hook loader to load and scope workspace-local hooks across workspaces.
- `gateway`: The fix runs at gateway startup and updates server-startup behavior to enumerate agent workspaces.
- `sessions`: Hook scope isolation depends on session context/session keys to resolve the correct agent workspace.

## openclaw-openclaw-42606 — Browser: harden noVNC bootstrap headers

- labels: `browser_automation, security, api_surface`
- `browser_automation`: Change is in the browser bridge/noVNC observer bootstrap route used for browser sandbox viewing.
- `security`: Central change adds CSP nonce, nosniff, and frame-deny hardening for a token-gated bootstrap page.
- `api_surface`: It changes HTTP response headers and contract for the `/sandbox/novnc` route.

## openclaw-openclaw-43416 — feat(ui): add copy button for assistant messages

- labels: `ui_tui`
- `ui_tui`: Adds a user-facing copy button, hover state, clipboard action, and visual feedback in the chat message UI.

## openclaw-openclaw-44379 — fix(pi-runner): harden context-overflow recovery with one suppress-hook retry

- labels: `agent_runtime, hooks, memory, reliability`
- `agent_runtime`: Changes the embedded PI agent runner loop and attempt parameters for context-overflow recovery.
- `hooks`: Adds a bounded retry that suppresses prompt-hook context injection as the explicit fallback behavior.
- `memory`: The overflow is attributed to external memory/prompt-hook injections, with memory-context suppression central to the fix.
- `reliability`: Hardens recovery from recurring context-overflow failures with normalized handling and one safe retry.

## openclaw-openclaw-45200 — fix(subagents): notify user on announce give-up instead of silently dropping result

- labels: `agent_runtime, notifications, reliability`
- `agent_runtime`: The change is in subagent run handling, specifically the announce give-up path in resumeSubagentRun.
- `notifications`: The fix adds a last-resort user notification when a completed subagent result cannot be announced normally.
- `reliability`: It addresses a retry-limit failure mode where completed results were silently dropped and adds recoverable/auditable behavior.

## openclaw-openclaw-45393 — fix(errors): friendly message and last-message repair for tool_use/tool_result mismatch (#45385)

- labels: `tool_calling, reliability, sessions, security`
- `tool_calling`: Core fix handles Anthropic tool_use/tool_result mismatches and strips dangling tool_use blocks from message history.
- `reliability`: Repairs a timeout/race/last-message failure mode that caused subsequent API requests to be rejected.
- `sessions`: The repair targets session history/message transcript state and gives users recovery guidance for stale sessions.
- `security`: Bundled read-tool change wraps inbound media content as untrusted to prevent prompt injection.

## openclaw-openclaw-45508 — [Feature]: Self-hosted STT/TTS provider support in webchat (Route webchat TTS through the gateway instead of browser Speech API)

- labels: `self_hosted_inference, chat_integrations, gateway, config`
- `self_hosted_inference`: The feature is explicitly about using self-hosted STT/TTS providers such as Whisper, Speaches, and Kokoro.
- `chat_integrations`: The affected surface is webchat voice input and read-aloud behavior.
- `gateway`: The request is to route webchat audio through the OpenClaw gateway instead of browser speech APIs.
- `config`: The issue centers on honoring existing messages.tts configuration and proposes/configures STT settings.

## openclaw-openclaw-45841 — [Feature]: Sandboxing + ACP

- labels: `acp, sandboxing, security, sessions`
- `acp`: The feature request is explicitly about enabling ACP sessions from sandboxed OpenClaw sessions.
- `sandboxing`: Docker/container sandbox boundaries and sandbox compatibility are the core blocker and proposed design area.
- `security`: The proposal centers on preserving isolation, controlled bridge/proxy access, auditability, allowlisting, and privilege-boundary tradeoffs.
- `sessions`: The issue concerns sandboxed sessions spawning ACP sessions and session_spawn bridge behavior.

## openclaw-openclaw-46552 — docs(queue): clarify steer behavior with partial streaming and tool boundaries

- labels: `docs, queueing, tool_calling`
- `docs`: PR only changes docs/concepts/queue.md to add explanatory and troubleshooting documentation.
- `queueing`: The documented behavior is queue steer mode, per-session queue overrides, and followup/steer behavior.
- `tool_calling`: It explicitly clarifies tool-boundary semantics: in-flight tool calls complete before steer takes effect.

## openclaw-openclaw-46740 — ACP: classify silent acpx exits as backend unavailable

- labels: `acp, acpx, reliability`
- `acp`: Changes ACP runtime/control-plane error classification from generic turn failure to backend-unavailable codes.
- `acpx`: The failure being handled is an explicit silent non-zero exit of the acpx backend process.
- `reliability`: Central concern is clearer handling of backend disappearance/non-zero exits and availability-oriented fallback guidance.

## openclaw-openclaw-47187 — fix(ui): reset transient chat overlays and style context notice

- labels: `ui_tui`
- `ui_tui`: PR directly fixes Control UI chat styling and transient overlay state in UI files.

## openclaw-openclaw-47243 — feat(ui): add timestamp and preview to session list

- labels: `sessions, ui_tui`
- `sessions`: Feature changes the session list data shown for each session, adding timestamp and last-message preview to session rows.
- `ui_tui`: Primary change is a user-facing web UI enhancement to the session list view.

## openclaw-openclaw-47446 — fix(gateway/discord): respect env proxy vars and prevent ECONNRESET

- labels: `chat_integrations, config, gateway, reliability`
- `chat_integrations`: The fix is explicitly for the Discord integration, including Discord REST calls and WebSocket gateway connections.
- `config`: Central behavior is honoring https_proxy/HTTP_PROXY env vars and falling back when channels.discord.proxy is not configured.
- `gateway`: Gateway startup bootstraps the global proxy dispatcher and Discord gateway plugin behavior is changed.
- `reliability`: The PR prevents timeouts and ECONNRESET failures from local proxies by disabling keepAlive and using proxy dispatchers correctly.

## openclaw-openclaw-48260 — feat(ui): add active time summary to usage overview

- labels: `telemetry_usage, ui_tui`
- `telemetry_usage`: Adds active-time and average-session-duration summaries to the Usage overview, a usage/diagnostics reporting surface.
- `ui_tui`: User-visible web UI change on the Dashboard Usage page adding an Active Time card.

## openclaw-openclaw-48580 — Bug: acpx codex sessions 创建的会话立即退出 - stdin is not a terminal

- labels: `acpx, codex, sessions, reliability`
- `acpx`: The failing command and logs are explicitly ACPX-based: `acpx codex sessions new` and ACPX spawning the agent.
- `codex`: The issue centers on Codex CLI/ACP integration requiring a TTY and exiting immediately.
- `sessions`: The main symptom is incorrect session state: a newly created session remains `closed: false` with a stale PID.
- `reliability`: The bug is a process-exit/state-drift failure where ACPX does not detect or clean up a dead spawned process.

## openclaw-openclaw-48606 — fix: macOS default browser detection fallback to known paths

- labels: `browser_automation, reliability`
- `browser_automation`: Changes browser extension code that detects the macOS default Chromium executable for browser automation.
- `reliability`: Adds fallback path resolution when osascript/defaults browser detection fails due to bundle ID mismatches.

## openclaw-openclaw-48851 — feat(status): add API call count to session status and usage footer

- labels: `sessions, telemetry_usage, ui_tui`
- `sessions`: Persists per-run callCount on session entries and session usage state for current-turn status.
- `telemetry_usage`: Adds API call count as usage accounting alongside tokens and cost, including usage footer reporting.
- `ui_tui`: Displays the call count in user-facing /status output and the response usage footer.

## openclaw-openclaw-48877 — feat(telegram): add multi-level menu support to customCommands

- labels: `chat_integrations, config`
- `chat_integrations`: Feature is explicitly for Telegram bot custom commands and inline keyboard menu/callback handling.
- `config`: Adds user-facing customCommands configuration fields, types, schema, and resolution for menus/routes.

## openclaw-openclaw-48940 — ACP: add gateway-owned node-backed runtime

- labels: `acp, gateway, agent_runtime, sessions, reliability`
- `acp`: PR explicitly adds a node-backed ACP runtime, ACP store, ACP worker events, and ACP reply replay paths.
- `gateway`: Gateway is made authoritative for durable ACP state, ingestion, terminal resolution, replay, and node control.
- `agent_runtime`: Adds a real node-host worker bridge and execution path where paired nodes run ACP worker roles under gateway control.
- `sessions`: Durable store persists ACP sessions and runs, replay targets, checkpoints, and recovery state across restart/reconnect.
- `reliability`: Central focus includes restart recovery, replay, reconnect/cancel/close race hardening, leases, and terminal-state recovery.

## openclaw-openclaw-49310 — fix: keep tui busy during follow-up waits

- labels: `sessions, ui_tui`
- `sessions`: The fix keys off the sessions_yield follow-up marker and restores/clears this state from session history.
- `ui_tui`: The main user-facing change is a new TUI busy activity state, shown while awaiting follow-up.

## openclaw-openclaw-49502 — feat(gateway): include usage/cost metadata in agent.wait terminal response

- labels: `gateway, api_surface, telemetry_usage`
- `gateway`: Change is in gateway server methods and modifies the agent.wait gateway response paths.
- `api_surface`: Adds an optional meta field to the agent.wait WebSocket response contract.
- `telemetry_usage`: Surfaces token usage, provider/model, and estimated cost metadata for completed runs.

## openclaw-openclaw-50054 — fix(acp): add distributed session locking with fail-closed redis fallback

- labels: `acp, sessions, reliability`
- `acp`: The change explicitly wires locking into ACP reply dispatch and reports acp_execution_locked skips.
- `sessions`: The core feature is distributed locking around ACP session execution keyed by session state.
- `reliability`: Fail-closed Redis behavior, owner-checked release/renewal, and contention handling prevent races and unsafe concurrent runs.

## openclaw-openclaw-53319 — [Bug]: ACP concurrent session spawns — first agent fails to launch CC process

- labels: `acp, acpx, sessions, reliability`
- `acp`: The failure occurs when using `sessions_spawn runtime:"acp"` and concerns ACP session behavior.
- `acpx`: The reported backend is explicitly `acpx`, with analysis pointing to the acpx CLI launch path.
- `sessions`: The bug is about concurrent child session spawns, accepted childSessionKeys, and session stream logs.
- `reliability`: A race or crash during concurrent initialization leaves one agent stalled with no output or process.

## openclaw-openclaw-54471 — fix(acp): add system_event stream relay to parent session for ACP spawn

- labels: `acp, sessions, notifications`
- `acp`: The fix is explicitly for ACP spawn stream handling and relaying ACP system_event events.
- `sessions`: The behavior concerns sessions_spawn with streamTo parent and relaying child ACP session events to the parent session.
- `notifications`: The bug prevents clarifying questions and progress system events from being delivered to users as notifications/messages.

## openclaw-openclaw-55790 — sessions_spawn(runtime="subagent") ignores inherited/per-agent subagent thinking defaults and initializes children at low

- labels: `agent_runtime, config, sessions`
- `agent_runtime`: The bug is in spawning a subagent runtime and initializing subagent execution state.
- `config`: The failure concerns resolving documented per-agent and default thinking configuration values.
- `sessions`: The affected operation is sessions_spawn and the incorrect state is on spawned child sessions.

## openclaw-openclaw-56532 — memory-lancedb: add configurable timeout/retry for embedding calls

- labels: `memory, config, reliability`
- `memory`: The change is in the memory-lancedb extension and its OpenAI-compatible embedding calls for memory recall.
- `config`: Adds operator-configurable embedding.timeoutMs and embedding.maxRetries with schema, manifest, and docs updates.
- `reliability`: Bounds hung or rate-limited embedding requests to avoid stalled agent turns and cascading connection failures.

## openclaw-openclaw-56613 — [Feature]: Talk/Voice tab — agent/session switching + per-agent TTS voice

- labels: `config, sessions, ui_tui`
- `config`: The issue requests per-agent TTS voice settings via agent-level configuration such as agents.list[].tts.
- `sessions`: The remaining core request is selecting which agent/session the Voice tab sends messages to instead of hardcoded main.
- `ui_tui`: The feature is specifically about the Talk/Voice tab UI adding an agent/session picker like the Chat tab.

## openclaw-openclaw-57597 — fix(acp): persist spawn labels in target session store

- labels: `acp, sessions, reliability`
- `acp`: The fix is in `/acp spawn --label` behavior and ACP command lifecycle handling.
- `sessions`: The core change writes spawned session labels to the correct target session store for later label-based resolution.
- `reliability`: This fixes a silent state-persistence bug that made follow-up ACP session commands fail in cross-agent flows.

## openclaw-openclaw-58411 — sessions_spawn lacks --bind here equivalent — agent cannot bind ACP session to existing Discord thread

- labels: `acp, sessions, chat_integrations, api_surface`
- `acp`: The requested behavior maps programmatic session spawning to `/acp spawn --bind here` ACP semantics.
- `sessions`: The core issue is binding a spawned ACP session to an existing thread instead of creating a new session thread.
- `chat_integrations`: The user-facing failure occurs in Discord threads, with a related Telegram asymmetry noted.
- `api_surface`: The proposal adds a `bindTo: "current"` option to the `sessions_spawn` programmatic contract.

## openclaw-openclaw-59208 — fix(status): honor selected usage auth profile

- labels: `auth_identity, telemetry_usage, ui_tui`
- `auth_identity`: Fixes OAuth/profile selection by honoring the session-selected authProfileOverride for usage credential resolution.
- `telemetry_usage`: Central behavior is the /status usage/quota line resolving provider usage through the correct profile.
- `ui_tui`: The user-visible /status status card/text is made internally consistent between auth label and usage line.

## openclaw-openclaw-59878 — Session lane stuck in 'running' after run dies — sessions.abort + gateway restart fail to clear stale state

- labels: `sessions, gateway, queueing, reliability`
- `sessions`: Issue centers on persisted session lane status stuck as running and sessions.abort/new behavior.
- `gateway`: Gateway restart is expected to reconcile stale state but fails, and gateway logs show lane waits.
- `queueing`: New messages queue indefinitely behind the stale session lane lock.
- `reliability`: Dead runs leave stale state with no cleanup, recovery, or timeout, causing persistent wedged sessions.

## openclaw-openclaw-60737 — [Feature]: Per-DM/per-chat default ACP binding for auto-spawning ACP sessions on new topics

- labels: `acp, chat_integrations, config, sessions`
- `acp`: Feature is explicitly about default ACP bindings and auto-spawning ACP sessions.
- `chat_integrations`: The requested behavior is for Telegram DM and group forum topics/chats.
- `config`: It proposes new TelegramDirectConfig/TelegramGroupConfig defaultAcp configuration and override behavior.
- `sessions`: Core behavior binds new topics/threads to newly created ACP sessions and reuses that binding for subsequent messages.

## openclaw-openclaw-60979 — feature: sessions_spawn ACP delivery to channel (stream output to Zulip/Discord topic)

- labels: `acp, sessions, chat_integrations, notifications`
- `acp`: The requested feature is explicitly for `sessions_spawn` with `runtime="acp"` and ACP session output.
- `sessions`: It concerns spawned session output binding and parent/child session delivery behavior.
- `chat_integrations`: The target delivery surface is a Zulip/Discord channel conversation or topic.
- `notifications`: The proposal adds an announce-style delivery option for streaming outbound session messages to a channel.

## openclaw-openclaw-61775 — enhance Makefile with standard build, test, and quality targets

- labels: `packaging_deployment, tests_ci`
- `packaging_deployment`: Makefile adds standard dependency, build, clean, dev, and pnpm-based workflow targets for repository build/developer operations.
- `tests_ci`: Makefile adds test, coverage, scoped test, lint, format, typecheck, check, and landing-gate quality targets.

## openclaw-openclaw-62428 — test(exec): land exec v2 contract follow-through

- labels: `exec_tools, approvals, security, tests_ci`
- `exec_tools`: Exec V2 command contracts, allowlist matching, safeBins behavior, and script/interpreter command handling are central.
- `approvals`: Exec approval allowlist behavior and effective approval/security policy merge tests are explicit core changes.
- `security`: Safe bin rejection, trusted-dir filtering, audit warnings, and command-contract hardening are security-boundary concerns.
- `tests_ci`: The PR is primarily landing contract test coverage across exec approvals, allowlists, safeBins, and security audit behavior.

## openclaw-openclaw-62552 — fix(acp): stabilize bridge session keys

- labels: `acp, sessions, queueing, reliability`
- `acp`: PR is explicitly in the ACP translator and changes ACP bridge fallback key and pending prompt matching behavior.
- `sessions`: Core fix stabilizes session keys, raw/canonical session-key equivalence, and terminal child-session handling.
- `queueing`: Task registry maintenance changes task state by marking active cron/cli/subagent tasks lost when their backing child session is terminal.
- `reliability`: Fix addresses hangs/failures and stale live tasks caused by session-key collisions and terminal-session records.

## openclaw-openclaw-62769 — [Feature]: Support ACP configured bindings for Telegram DMs (not just groups/topics)

- labels: `acp, chat_integrations, sessions`
- `acp`: Issue is specifically about Telegram bindings with type "acp" routing messages to an ACP harness.
- `chat_integrations`: The requested support is for Telegram direct-message conversations versus groups/topics.
- `sessions`: Expected behavior is to create or resume persistent ACP sessions from configured DM bindings.

## openclaw-openclaw-63007 — Pass outbound session identity into message_sending and surface guarded gateway send denial

- labels: `gateway, hooks, notifications, sessions`
- `gateway`: The PR explicitly fixes the narrow `gateway call send` path and changes gateway send denial surfacing.
- `hooks`: It passes outbound identity into the `message_sending` hook context and updates hook mappers/tests.
- `notifications`: The change is in the outbound message delivery path, including guarded cancellation and delivery-result handling.
- `sessions`: The central data being propagated is outbound session identity via `agentId` and `sessionKey`.

## openclaw-openclaw-63229 — Bug: Gateway falsely marks healthy local vLLM endpoints as timed out/overloaded, causing 1–23 min fallback cascades

- labels: `gateway, local_models, model_serving, reliability`
- `gateway`: The reported failure is in the gateway's fallback/routing subsystem and includes gateway timeouts for sessions_spawn.
- `local_models`: Specific local vLLM/GPU endpoints are central and are falsely treated as timed out despite direct sub-second local responses.
- `model_serving`: The bug concerns endpoint health classification, provider fallback routing, and timeout/overload semantics for model endpoints.
- `reliability`: False timeouts and overload states cause long fallback cascades and unresponsive-gateway symptoms.

## openclaw-openclaw-64181 — fix(hooks): reject error responses from slug generator and strip post-truncation dashes

- labels: `hooks, memory, reliability`
- `hooks`: The fix is contained in the hooks LLM slug generator implementation and tests.
- `memory`: The bug produced incorrect memory/*.md filenames and fragmented the canonical session memory path.
- `reliability`: It hardens slug generation against failure-mode LLM/provider error payloads and malformed truncation output.

## openclaw-openclaw-64199 — [Bug]: ACP configured binding uses parent channel ID for session key — all threads under same channel share one persistent Claude Code process

- labels: `acp, acpx, sessions, chat_integrations, security`
- `acp`: Bug is specific to runtime.type "acp" configured bindings and ACP session-key behavior.
- `acpx`: The faulty key maps to the same acpxRecordId and ACPX state record/process.
- `sessions`: Core failure is wrong session key granularity causing multiple threads to share one persistent session/process.
- `chat_integrations`: The affected binding surface is Discord parent channels and Discord threads.
- `security`: Cross-thread context contamination exposes one thread's conversation history to another.

## openclaw-openclaw-64718 — fix(security): default exec to deny for non-owner auto-reply senders

- labels: `security, exec_tools, approvals, auth_identity`
- `security`: PR hardens a security boundary against unauthenticated prompt-injection-triggered arbitrary command execution.
- `exec_tools`: Change directly alters default exec tool override behavior to deny command execution for non-owner auto-reply senders.
- `approvals`: The fix changes the approval posture from no ask gate to ask="always" for non-owner exec attempts.
- `auth_identity`: Behavior depends on senderIsOwner and distinguishes owner from unauthenticated/non-owner channel senders.

## openclaw-openclaw-65187 — test: add regression tests for <final> tag stripping in UI message extraction

- labels: `tests_ci, ui_tui`
- `tests_ci`: PR only adds regression tests and cached-path assertions in a UI test file.
- `ui_tui`: Tests cover Control UI chat message text extraction and stripping of leaked assistant tags from the UI surface.

## openclaw-openclaw-65242 — fix: CompletionDeliveryGate to prevent duplicate ACP completion delivery

- labels: `acp, agent_runtime, sessions, notifications, reliability`
- `acp`: The fix is explicitly for duplicate ACP child-session completion delivery and ACP runtime wake behavior.
- `agent_runtime`: It coordinates subagent/task completion paths, announce flow, and heartbeat wake behavior in the agent lifecycle.
- `sessions`: The gate keys and behavior depend on ACP child sessions, parent/requester sessions, and owner session keys.
- `notifications`: The central user-facing issue is preventing duplicate completion messages and suppressing incorrect visible delivery paths.
- `reliability`: The PR fixes a race between multiple completion delivery paths using a first-writer-wins gate to avoid duplicates and stale replays.

## openclaw-openclaw-65640 — fix(acp): persistent session recovery for --bind here sessions

- labels: `acp, acpx, sessions, reliability`
- `acp`: PR changes ACP control-plane session handling and ACP error detection for /acp spawn and /acp model flows.
- `acpx`: The failure mode is explicitly an acpx backend losing a persistent session, with recovery around acpx-backed session handles.
- `sessions`: Central issue is persistent session binding, resume state, stale bindings, and recovery for --bind here sessions.
- `reliability`: Adds retry and stale-state cleanup paths to recover from missing backend sessions after restart or eviction.

## openclaw-openclaw-66000 — fix(cli): clear conflicting OPENCLAW_LAUNCHD_LABEL when --profile is provided

- labels: `config, gateway, packaging_deployment`
- `config`: Changes CLI profile environment handling for --profile and OPENCLAW_LAUNCHD_LABEL conflicts.
- `gateway`: Fixes gateway status/profile behavior resolving the wrong gateway launch-agent plist from an inherited label.
- `packaging_deployment`: Launchd labels and plist resolution are central service-manager/deployment concerns.

## openclaw-openclaw-66327 — feat(msteams): implement sendPayload for interactive approval cards

- labels: `chat_integrations, approvals, notifications`
- `chat_integrations`: Implements MS Teams channel outbound behavior for rendering interactive cards in a chat platform.
- `approvals`: Approval prompts are converted from raw /approve text into Approve/Deny interactive buttons.
- `notifications`: Changes outbound payload delivery and fallback behavior for channel messages.

## openclaw-openclaw-67244 — Explicit ACP agent runs: embedded backend visibility failure and stale final JSON state after sessions_yield

- labels: `acp, acpx, agent_runtime, sessions, reliability`
- `acp`: The issue is explicitly about ACP agent runs and completion after sessions_yield.
- `acpx`: The backend visibility bug centers on embedded ACPX runtime backend/plugin registration.
- `agent_runtime`: The failing path is the explicit embedded agent --json run process and descendant run lifecycle.
- `sessions`: The stale final state involves a specific session id, sessions_yield, replayInvalid, and livenessState.
- `reliability`: Both reported bugs are operational correctness failures: false backend-not-configured errors and stale final state after successful work.

## openclaw-openclaw-68187 — SSE-backed MCP sessions can stay stale after server restart and fail with 'Session not found'

- labels: `mcp_tooling, sessions, gateway, reliability`
- `mcp_tooling`: Issue is about an SSE-backed MCP server/integration and MCP tool calls failing after restart.
- `sessions`: Core failure is stale client/proxy session state and 'Session not found' after downstream restart.
- `gateway`: Recovery requires restarting the OpenClaw gateway and the defect is attributed to the gateway/proxy layer.
- `reliability`: Expected behavior is automatic stale-session detection, reconnect, invalidation, and recovery after server restart.

## openclaw-openclaw-68204 — Unified run trace schema across agent, ACP, subagent, and task flows

- labels: `acp, agent_runtime, sessions, telemetry_usage`
- `acp`: Issue explicitly requires the canonical trace schema to cover ACP sessions and ACP parent-child relay paths.
- `agent_runtime`: Schema is for main agent runs, subagents, run lifecycle steps, delegation, and task execution progress.
- `sessions`: Run traces include sessionKey and parent/child run linkage across ACP sessions and related flows.
- `telemetry_usage`: Core request is observability/tracing with latency, status, events, and timeline reconstruction.

## openclaw-openclaw-68843 — fix(acp): treat missing cwd as stale bound session

- labels: `acp, sessions, reliability`
- `acp`: The fix is explicitly in ACP handling for ACP_SESSION_INIT_FAILED and ACP dispatch/reset cleanup paths.
- `sessions`: The core behavior is detecting and unbinding stale bound ACP sessions when the runtime cwd is missing.
- `reliability`: It recovers wedged conversations automatically instead of leaving retries stuck on a dead session.

## openclaw-openclaw-69260 — Harden Gemini ACP integration against ambient API-key fallback and add generic auth-contract hooks for ACP agents

- labels: `acp, auth_identity, hooks, security`
- `acp`: The requested product change is for ACP-backed agent definitions, routes, and launch/runtime behavior.
- `auth_identity`: The issue centers on explicit auth modes, OAuth-personal selection, API-key fallback, and credential lane enforcement.
- `hooks`: It asks for generic auth-contract and env-scrubbing hooks around ACP agent launches.
- `security`: The goal is defense-in-depth hardening against unsafe ambient credential inheritance and fail-closed auth behavior.

## openclaw-openclaw-69328 — fix(acp): avoid false zero-diff failures and append session messages

- labels: `acp, reliability, sessions, ui_tui`
- `acp`: PR changes ACP control-plane manager behavior, ACP verification gating, and ACP session handling.
- `reliability`: Fixes false zero-diff hard failures and downgrades some runs to blocked follow-up instead of incorrect failure.
- `sessions`: Persistent versus oneshot session semantics and direct appending of session.message payloads are central.
- `ui_tui`: Control UI chat transcript now appends active-run session messages with dedupe and optimistic echo replacement.

## openclaw-openclaw-70002 — ci: skip docs sync & translate-trigger workflows in forks

- labels: `tests_ci`
- `tests_ci`: Changes only GitHub Actions workflow files to guard CI/docs automation jobs in forks and avoid failing Actions runs.

## openclaw-openclaw-70882 — fix(bundle-mcp): coerce stringified object/array params before MCP tool calls

- labels: `mcp_tooling, tool_calling, security`
- `mcp_tooling`: Fix is in the bundle MCP materialization layer before invoking stdio MCP servers and targets MCP inputSchema compatibility.
- `tool_calling`: Core behavior coerces LLM-produced tool call arguments so object/array parameters are delivered in the schema-expected form.
- `security`: Follow-up patch adds prototype-pollution and oversized-payload guards around parsing/copying tool arguments.

## openclaw-openclaw-71157 — [Feature]: Support WhatsApp disappearing-message expiration for outbound replies

- labels: `chat_integrations, config`
- `chat_integrations`: The feature is specifically for WhatsApp outbound reply behavior and Baileys send metadata across WhatsApp message paths.
- `config`: It proposes new channel-level and account-level WhatsApp configuration keys with override/default behavior.

## openclaw-openclaw-71216 — Config schema: add `sandbox`, `routing.rules`, `instances`, and `gateway.nodes.denyPaths`

- labels: `config, gateway, local_model_providers, sandboxing, security`
- `config`: The issue explicitly requests new config schema fields for sandbox, routing, instances, and denyPaths.
- `gateway`: Several asks are gateway-enforced, including multi-instance gateway declarations and gateway node denyPaths.
- `local_model_providers`: `routing.rules` is provider-selection configuration for mixed cloud/local Ollama routing by tags, host, and model.
- `sandboxing`: `sandbox.mode` is proposed as a global mode controlling tool execution boundaries.
- `security`: `gateway.nodes.denyPaths` is intended to block access to credential directories, SSH keys, and secrets regardless of tool.

## openclaw-openclaw-71487 — Web UI: add a clear TTS toggle and default voice picker in Settings

- labels: `ui_tui, self_hosted_inference, config`
- `ui_tui`: The request is for a first-class Control UI Settings/Web UI TTS panel with toggle, dropdowns, and test button.
- `self_hosted_inference`: The feature centers on TTS speech inference provider and voice selection, including provider-backed sample generation.
- `config`: The UI must read and persist TTS preferences such as enabled state, provider, and default voice to the existing settings contract.

## openclaw-openclaw-71594 — docs(gateway): clarify IPv4-only BYOH bind path

- labels: `docs, gateway`
- `docs`: PR primarily updates CLI docs, TSDoc/comments, and help text to clarify IPv4-only BYOH guidance.
- `gateway`: The documented behavior is specifically about Gateway bind modes and custom bind host support.

## openclaw-openclaw-71646 — mcp/channel-bridge: pendingClaudePermissions / pendingApprovals leak — no TTL, no close-clear, no cap

- labels: `mcp_tooling, approvals, reliability`
- `mcp_tooling`: Issue is specifically in `src/mcp/channel-bridge.ts` for a long-running `openclaw mcp serve` bridge process.
- `approvals`: Central leak involves `pendingApprovals`, approval requested/resolved events, and missing cleanup for pending approval state.
- `reliability`: Reports unbounded pending-map growth due to missing TTL, close cleanup, and caps causing long-running process reliability degradation.

## openclaw-openclaw-71648 — fix(mcp): bound pendingClaudePermissions / pendingApprovals via TTL sweeper + close clear

- labels: `mcp_tooling, approvals, reliability`
- `mcp_tooling`: The fix is in the MCP channel bridge/server path for long-running `openclaw mcp serve` behavior.
- `approvals`: It directly bounds and clears `pendingApprovals` and Claude permission/approval state.
- `reliability`: The change prevents leaked pending entries, stale post-close writes, and lingering sweeper state in long-running processes.

## openclaw-openclaw-71784 — Bug: memory search live embedding fails ~20–40% with `fetch failed | other side closed` (provider-agnostic; upstream healthy)

- labels: `memory, reliability`
- `memory`: The bug is in live memory search embeddings and semantic memory recall with the builtin memory backend.
- `reliability`: The central failure is intermittent TLS/socket fetch errors causing 20–40% of memory search calls to fail despite healthy providers.

## openclaw-openclaw-71803 — CLI watchdog kills sessions that are correctly idle while waiting on a Monitor task

- labels: `agent_runtime, exec_tools, reliability, sessions`
- `agent_runtime`: The issue is about the agent CLI backend watchdog terminating the agent process during expected idle time.
- `exec_tools`: The failure occurs while a Monitor tool is waiting on a long-running shell command such as Whisper, ffmpeg, or builds.
- `reliability`: A healthy workflow is incorrectly killed by a no-output timeout, causing crashes and lost progress.
- `sessions`: The watchdog termination destroys the in-flight agent session and prevents it from resuming the Monitor result.

## openclaw-openclaw-71930 — Mattermost plugin drops post_edited events — @mentions added via edit do not trigger agent wake

- labels: `chat_integrations, reliability`
- `chat_integrations`: Mattermost WebSocket integration drops edited-message events, preventing @mention handling in that chat platform.
- `reliability`: A silent message-loss bug prevents expected agent wake behavior when mentions are added by edit.

## openclaw-openclaw-71976 — Memory Dreaming: Light sleep sort prioritizes recency over recallCount, hiding real recall data

- labels: `memory, reliability`
- `memory`: Issue is about Memory Dreaming, short-term recall data, recall counts, rehydration, and promotion behavior in the memory store.
- `reliability`: The reported bugs cause valid memory candidates to be buried or fail rehydration, resulting in zero promoted results despite existing eligible data.

## openclaw-openclaw-72001 — fix(hooks): write allowedSessionKeyPrefixes from gmail wizard

- labels: `hooks, gateway, config`
- `hooks`: The fix is in the Gmail webhooks setup and hook config, adding the required allowed session key prefix for the Gmail hook preset.
- `gateway`: The reported failure is the gateway refusing to load/restart because its hooks validator rejects the wizard-emitted config.
- `config`: The PR changes setup behavior to write hooks.allowedSessionKeyPrefixes into openclaw.json while preserving existing configured values.

## openclaw-openclaw-72015 — Reliability: active-memory blocks replies and QMD boot initialization can overload multi-agent gateways

- labels: `gateway, memory, reliability`
- `gateway`: Issue centers on multi-agent gateway boot/restart overload, health timeouts, and gateway responsiveness under load.
- `memory`: Active-memory and QMD memory startup/update behavior are the core subsystems causing latency and CPU spikes.
- `reliability`: Primary concern is blocking replies, timeout cascades, high CPU, crash-loop/unreliable operation, and fail-open defaults.

## openclaw-openclaw-72085 — docs(commands): document bashForegroundMs clamp bounds (0–30 000 ms)

- labels: `docs, config`
- `docs`: PR is explicitly docs-only and changes the configuration reference markdown.
- `config`: Documents the accepted range and clamp behavior for the `bashForegroundMs` configuration key.

## openclaw-openclaw-72087 — Bug: dist/entry.js main-path breaks Codex OAuth image generation on Linux while direct runCli()/provider path succeeds

- labels: `auth_identity, codex, packaging_deployment`
- `auth_identity`: Failure is tied to the openai-codex OAuth profile/auth-provider path with no API key.
- `codex`: The affected flow explicitly uses Codex OAuth and the Codex Responses backend.
- `packaging_deployment`: Report isolates the regression to the packaged dist/entry.js main/bootstrap path versus direct runCli/provider execution.

## openclaw-openclaw-72133 — Feature request: per-message token/cost metadata in mobile app and channel surfaces

- labels: `telemetry_usage, ui_tui, chat_integrations`
- `telemetry_usage`: The request centers on exposing per-message token, cost, cache, model, and context-window usage metadata.
- `ui_tui`: It asks to show the metadata in native iOS/Android chat views, a user-facing interface surface.
- `chat_integrations`: It explicitly requests optional metadata footers in messaging channel surfaces such as Signal, iMessage, Telegram, and BlueBubbles.

## openclaw-openclaw-72138 — fix(feishu): emit sent hooks for normal replies

- labels: `chat_integrations, hooks, notifications`
- `chat_integrations`: The fix is specific to the Feishu chat integration normal-reply dispatcher and conversation reply paths.
- `hooks`: The PR centrally adds canonical plugin message_sent and internal message:sent hook emission for Feishu replies.
- `notifications`: The behavior concerns successful outbound reply/sent-message handling so workflows see delivered normal bot responses.

## openclaw-openclaw-72262 — docs: add WhatsApp 408 disconnect troubleshooting runbook

- labels: `chat_integrations, docs, reliability`
- `chat_integrations`: The requested runbook is specifically for the WhatsApp channel integration and Baileys/WhatsApp Web disconnects.
- `docs`: The issue explicitly asks to add troubleshooting documentation in WhatsApp/channel docs.
- `reliability`: The documented failure mode is repeated 408 disconnect/reconnect loops with operator recovery guidance.

## openclaw-openclaw-73910 — BUG: OpenClaw-managed Codex ACP uses isolated CODEX_HOME without auth bridge and sends unsupported timeout config

- labels: `acp, acpx, auth_identity, codex, config`
- `acp`: Failure is in ACP session handling, specifically rejected session/set_config_option during a managed ACP session.
- `acpx`: The issue compares direct ACPX to the OpenClaw-managed ACPX path and cites ACPX adapter/schema behavior.
- `auth_identity`: Central bug is isolated CODEX_HOME lacking Codex authentication and needing a safe auth bridge or setup flow.
- `codex`: The affected agent/runtime is explicitly Codex ACP, with Codex home and auth behavior central to the bug.
- `config`: A second central failure is forwarding an unsupported timeout configuration option/default to Codex ACP.

## openclaw-openclaw-74305 — [Bug]: ACPX Codex worker fails when model/thinking overrides are configured

- labels: `acpx, acp, codex, reliability`
- `acpx`: The failure is in an ACPX-enabled Codex worker path, and the follow-up identifies an ACPX-local command/config normalization fix.
- `acp`: The repro uses runtime "acp" and the observed failure is an AcpRuntimeError/ACP_TURN_FAILED from the ACP worker stream.
- `codex`: The broken command path is codex-acp invoking the Codex CLI with Codex model/thinking overrides.
- `reliability`: The reported bug is a worker run crash/internal error where the spawned task fails instead of completing or returning a validation error.

## openclaw-openclaw-74484 — Gateway pairing scope deadlock: CLI cannot approve/reject auto-reissued over-scoped repair requests

- labels: `auth_identity, gateway, reliability`
- `auth_identity`: The issue centers on paired device identity, operator scopes, and inability to approve/reject pairing repair requests with insufficient credentials.
- `gateway`: Failures occur through gateway control-plane method-scope enforcement and pairing-required gateway responses.
- `reliability`: The auto-reissued pending repair request creates a deadlock with no recovery/bootstrap path for the CLI.

## openclaw-openclaw-75657 — fix: local GGUF embedding model warmup blocks Node.js event loop for minutes on startup (ARM64/Pi)

- labels: `gateway, local_models, memory, reliability`
- `gateway`: The bug occurs during Gateway startup and leaves the Gateway/WebSocket port unreachable until ready.
- `local_models`: A local GGUF embedding model loaded via node-llama-cpp on ARM64/Pi is the concrete blocking component.
- `memory`: The trigger is the local `memorySearch.provider` embedding model used for memory search/indexing.
- `reliability`: The central failure is minutes-long event-loop blocking, startup timeout ineffectiveness, and unreachable service behavior.

## openclaw-openclaw-78528 — Security: skill SecretRef API keys still leak into exec child environments

- labels: `security, exec_tools, skills_plugins, auth_identity`
- `security`: Issue reports SecretRef-managed API keys leaking into process and child environments, a direct secret-exposure vulnerability.
- `exec_tools`: The leak is observed through child processes spawned by the exec tool inheriting environment variables.
- `skills_plugins`: The affected secrets are skill entry SecretRefs under skills.entries.<skill>.apiKey.
- `auth_identity`: The bug concerns API key credential scoping: skill-scoped credentials become process-wide.

## openclaw-openclaw-78919 — [Bug] ACP sessions_spawn doesn't route images to Codex's native vision like acpx codex exec does

- labels: `acp, acpx, codex, sessions`
- `acp`: The failing path is explicitly `runtime:acp` and ACP `sessions_spawn` attachment dispatch.
- `acpx`: The issue compares behavior against the explicitly named `acpx codex exec` path that handles images correctly.
- `codex`: The routed agent is Codex, and the bug is about Codex native vision/image handling.
- `sessions`: The failure occurs in `sessions_spawn` and affects session tracking/delegation behavior.

## openclaw-openclaw-79447 — fix(model-auth): resolve per-entry apiKey profile ID references

- labels: `auth_identity, config`
- `auth_identity`: PR fixes auth-profile ID dereferencing and credential-class checks when resolving model provider API keys.
- `config`: The bug concerns configured models.providers.<id>.apiKey values and their semantics as profile references versus literal bearer tokens.

## openclaw-openclaw-79897 — OpenAI-compatible streaming with llama.cpp saves zero usage (stream closed before final usage chunk)

- labels: `local_models, model_serving, telemetry_usage`
- `local_models`: A specific local llama.cpp backend is central to the reported behavior and reproduction.
- `model_serving`: The bug is in OpenAI-compatible SSE streaming semantics, where a final usage chunk after stop/[DONE] is not consumed.
- `telemetry_usage`: The visible failure is token usage being persisted as 0/0/0, breaking status and context accounting.

## openclaw-openclaw-80255 — fix #79026: active-memory recall subagent can deadlock on the main lane inside before_prompt_build

- labels: `memory, agent_runtime, queueing, reliability`
- `memory`: The fix is in the Active Memory extension and affects active-memory recall behavior.
- `agent_runtime`: The issue concerns the embedded recall subagent and how it is run during prompt building.
- `queueing`: The core change isolates the recall subagent onto a dedicated active-memory lane instead of re-entering the main lane.
- `reliability`: The patch fixes a deadlock, a central operational failure mode.

## openclaw-openclaw-80431 — ACPx plugin-tools MCP config test expects source path but resolver returns dist path

- labels: `acpx, mcp_tooling, tests_ci`
- `acpx`: The failing test is in extensions/acpx and concerns embedded ACPX plugin config behavior.
- `mcp_tooling`: The mismatch is specifically about resolving and injecting the built-in plugin-tools MCP server.
- `tests_ci`: The issue is a pnpm test failure caused by an assertion expecting a source path instead of the resolved dist path.

## openclaw-openclaw-80475 — test(acpx): accept built-dist MCP server resolution when dist exists

- labels: `acpx, mcp_tooling, tests_ci`
- `acpx`: The changed test is under extensions/acpx and mirrors ACPx resolver behavior for built-in server paths.
- `mcp_tooling`: The behavior under test is MCP server resolution and expected command arguments for built-in MCP servers.
- `tests_ci`: The PR only updates a Vitest helper and test expectations in config.test.ts, with no runtime code changes.

## openclaw-openclaw-80479 — feat(memory/embeddings): add openai-compatible provider for self-hosted servers (llama.cpp, Ollama, vLLM, TGI, LocalAI)

- labels: `local_model_providers, memory, self_hosted_inference`
- `local_model_providers`: Adds a user-configured OpenAI-compatible provider with baseUrl/model/apiKey handling for local or self-hosted backends.
- `memory`: The feature is specifically a memory embedding provider for memory-lancedb embeddings.
- `self_hosted_inference`: Targets operators running self-hosted embedding/inference servers such as llama.cpp, Ollama, vLLM, TGI, and LocalAI.

## openclaw-openclaw-81200 — fix(acpx): strip provider API keys from child harness env

- labels: `acpx, acp, security, auth_identity`
- `acpx`: Title, files, and body explicitly modify ACPX-generated child wrappers and runtime behavior.
- `acp`: The fix targets built-in ACP harness aliases/commands such as claude-agent-acp and gemini --acp.
- `security`: The change prevents provider API keys and selector env vars from leaking into spawned child harness environments.
- `auth_identity`: It changes credential scope for provider auth env vars while preserving the parent process env.

## openclaw-openclaw-81488 — Harden node exec approval precheck env [AI]

- labels: `approvals, exec_tools, security`
- `approvals`: The PR changes exec approval precheck analysis so node-host commands do not skip required approval based on gateway PATH.
- `exec_tools`: The affected behavior is node-host shell/system.run command execution, allowlist matching, and forwarded exec environment handling.
- `security`: This is explicit security hardening against incorrect allowlist decisions caused by gateway-local PATH resolution.

## openclaw-openclaw-82145 — cron: allow retries for local model preflight

- labels: `cron_automation, local_model_providers, config, reliability`
- `cron_automation`: Changes isolated cron job preflight behavior before scheduled agent turns and skipped-run handling.
- `local_model_providers`: The preflight targets local/private configured providers such as Ollama, vLLM, SGLang, and LM Studio.
- `config`: Adds and documents cron.modelPreflight timeout, maxAttempts, and retryDelayMs configuration schema/settings.
- `reliability`: Adds bounded retries and delays so sleeping or cold-starting local providers do not cause premature skipped runs.

## openclaw-openclaw-82507 — [Feature]: ACPX Codex sandbox should inherit user-installed plugins (e.g. Superpowers)

- labels: `acpx, codex, sandboxing, skills_plugins`
- `acpx`: Issue is explicitly about ACPX/Codex ACP background tasks and the ACPX codex-home wrapper behavior.
- `codex`: The affected runtime is Codex, with CODEX_HOME and Codex App plugin visibility central to the request.
- `sandboxing`: The problem is caused by an isolated sandbox home not inheriting user-installed plugin state.
- `skills_plugins`: Core feature request is for user-installed Codex plugins/skills such as Superpowers to be visible to ACP tasks.

## openclaw-openclaw-82596 — Feature/exec denylist

- labels: `exec_tools, approvals, security`
- `exec_tools`: The PR adds a denylist mode that evaluates and blocks model-initiated shell exec commands such as curl/wget.
- `approvals`: The change is implemented through exec approval/security modes, approval evaluation, prompting, and ask-fallback behavior.
- `security`: The denylist is explicitly a security boundary to prevent unsafe command bypasses and fail closed on malformed rules.

## openclaw-openclaw-82642 — Fix iMessage slash command acknowledgements

- labels: `chat_integrations, notifications, reliability`
- `chat_integrations`: The fix is in the iMessage extension inbound processing for direct iMessage slash commands.
- `notifications`: The bug is dropped slash-command acknowledgements/replies due to reply delivery policy source marking.
- `reliability`: This restores reliable acknowledgement delivery for authorized iMessage slash commands that completed but lost replies.

## openclaw-openclaw-83333 — [Bug]: Memory provider cutover to Ollama leaves production index in mixed OpenAI/Ollama vector state after live sync/reload

- labels: `memory, self_hosted_inference, reliability`
- `memory`: The bug is about the memory search index, embeddings, vector dimensions, and failed canary memory search.
- `self_hosted_inference`: The cutover is specifically to a locally operated Ollama embeddings provider for memory search.
- `reliability`: The live sync/reload path leaves production in an inconsistent mixed-vector state with broken search and rollback required.

## openclaw-openclaw-84094 — feat(gateway): forward frequency_penalty, presence_penalty, and seed via OpenAI-compatible HTTP gateway

- labels: `gateway, api_surface, model_serving`
- `gateway`: PR explicitly changes the OpenAI-compatible HTTP gateway handling and validation for inbound chat completion requests.
- `api_surface`: Adds user-facing POST /v1/chat/completions parameters and deterministic OpenAI-compatible 400 validation behavior.
- `model_serving`: Forwards sampling parameters through transport to upstream OpenAI-compatible provider request payloads.

## openclaw-openclaw-84297 — [Bug]: Per-agent identity overlay dropped on cron --announce and heartbeat target-channel Slack pushes (announce path; reply path was fixed in #38235)

- labels: `auth_identity, chat_integrations, cron_automation, notifications`
- `auth_identity`: The bug centers on a per-agent identity overlay not being applied to outbound messages.
- `chat_integrations`: The affected delivery path is Slack, specifically chat.postMessage username/icon customization.
- `cron_automation`: The broken paths are cron --announce and heartbeat-triggered Slack pushes.
- `notifications`: The issue concerns outbound announcement/heartbeat message delivery and sent-message identity handling.

## openclaw-openclaw-84316 — [Bug]: Telegram group TTS for sub-agent reports success in /tts status but voice never delivered (2026.5.12)

- labels: `chat_integrations, notifications, reliability`
- `chat_integrations`: The failure is specific to Telegram group chat delivery while Telegram DM works.
- `notifications`: The core symptom is an outbound voice/TTS message reported successful but not delivered.
- `reliability`: It is a message-loss/state-consistency bug where status records success despite missing delivery.

## openclaw-openclaw-84337 — [Bug]: Hook ingress token unlocks password-mode gateway auth

- labels: `security, auth_identity, gateway, hooks`
- `security`: Reported as a concrete high-severity auth bypass where a hook token grants full operator access.
- `auth_identity`: Core bug is password-mode gateway authentication accepting the hook bearer token as the gateway password.
- `gateway`: The affected protected surfaces are Gateway HTTP auth paths and startup/auth utilities.
- `hooks`: The bypass originates from hook ingress token handling and hook routing controls.

## openclaw-openclaw-84385 — [codex] Fix macOS app copyright year

- labels: `ui_tui`
- `ui_tui`: Central change fixes the macOS app About settings display text for the copyright year.

## openclaw-openclaw-84418 — test(cron): document and test owner-only tool security boundary for isolated cron

- labels: `cron_automation, security, tests_ci`
- `cron_automation`: The change is in isolated cron run execution and owner-only tool grants for unattended cron runs.
- `security`: It defines and tests a security boundary so only safe owner-only tools are auto-granted while gateway/nodes are filtered.
- `tests_ci`: The PR adds focused unit tests covering the cron owner-only allowlist behavior.

## openclaw-openclaw-84419 — fix(session): prefer real tool result over synthetic error in transcript repair

- labels: `sessions, tool_calling, reliability`
- `sessions`: The fix is explicitly in session transcript repair and changes persisted session history repair behavior on load.
- `tool_calling`: The repaired transcript logic deduplicates and pairs tool-use results, preferring a real tool result over a synthetic missing-result error.
- `reliability`: It mitigates a race-induced stale/synthetic error state so successful tool results recover correctly instead of showing a false failure.

## openclaw-openclaw-84567 — [Bug]: Codex bundled harness initialize still hangs in 2026.5.18 isolated cron — surfaces via #64744 timeout-wrapping as 'isolated agent setup timed out before runner start'

- labels: `codex, cron_automation, agent_runtime, reliability`
- `codex`: The bug explicitly targets the openai-codex plugin and bundled Codex harness initialization.
- `cron_automation`: The failure occurs in recurring and manually triggered cron jobs with cron diagnostics.
- `agent_runtime`: The timeout happens during isolated agent setup before the runner starts for an agentTurn payload.
- `reliability`: This is a regression hang/timeout causing deterministic setup failure and repeated errors.

## openclaw-openclaw-84570 — Remove skill prelude exec allowlist

- labels: `approvals, exec_tools, skills_plugins`
- `approvals`: The PR changes exec approval allowlist behavior so legacy skill prelude chains go through normal approval flow.
- `exec_tools`: It modifies shell command allowlist analysis/evaluation for exec tools and command chains.
- `skills_plugins`: The behavior is specifically about SKILL.md preludes, trusted skill wrappers, and autoAllowSkills skill execution contracts.

## openclaw-openclaw-84583 — cron announce delivery triggers EmbeddedAttemptSessionTakeoverError when user is actively chatting

- labels: `cron_automation, notifications, chat_integrations, sessions, reliability`
- `cron_automation`: The failure is triggered when an isolated cron job finishes and performs delivery.
- `notifications`: The problematic path is announce delivery of the cron result to a user.
- `chat_integrations`: The delivery target is explicitly the Telegram channel/user.
- `sessions`: The core error is a session file conflict/takeover while an active user session is processing.
- `reliability`: This is a race/conflict causing an EmbeddedAttemptSessionTakeoverError and possible message loss.

## openclaw-openclaw-84645 — Materialize node-host inline interpreter eval before exec approval

- labels: `exec_tools, approvals, security`
- `exec_tools`: PR changes node-host system.run command handling for Python/Node inline eval argv by materializing snippets into script files.
- `approvals`: Core behavior is approval planning: rewriting argv so existing approval hash binding can apply to a real script artifact.
- `security`: Security model is central: fail-closed unsupported carriers, private temp files, deterministic hashes, and 0600 permissions.

## openclaw-openclaw-84648 — Add SafeOps preflight hook for exec tool

- labels: `exec_tools, hooks, security`
- `exec_tools`: PR modifies the exec tool path to run a preflight check before command dispatch.
- `hooks`: Adds a SafeOps preflight/before-tool-execute hook in the exec execution flow.
- `security`: SafeOps is a policy/security preflight gate with explicit security-boundary and secret-scan concerns.

## openclaw-openclaw-84660 — [Bug] Voice STT: empty moonshine transcripts passed as raw JSON to LLM, clogging serialized processing queue

- labels: `chat_integrations, self_hosted_inference, queueing, reliability`
- `chat_integrations`: The bug occurs in Discord voice STT/TTS bot behavior and affects responsiveness in a voice channel.
- `self_hosted_inference`: The central failure is handling output from a speech STT model/provider, moonshine-tiny-en via sherpa-onnx.
- `queueing`: Empty transcript LLM calls clog the serialized processing queue and suggested fixes include queue depth or stale-segment discard.
- `reliability`: The issue is a pipeline reliability bug causing wasted calls, blocking, apparent unresponsiveness, and message loss.

## openclaw-openclaw-84668 — docs(agent-runtimes): clarify model name vs runtime routing for Codex (#84637)

- labels: `docs, agent_runtime, codex`
- `docs`: Documentation-only PR updating docs/concepts/agent-runtimes.md with a warning and audit guidance.
- `agent_runtime`: Central content clarifies runtime routing via agentRuntime.id versus model selection/fallbacks.
- `codex`: Explicitly distinguishes Codex runtime/harness from gpt-*-codex model IDs and other Codex-named surfaces.

## openclaw-openclaw-84681 — fix(codex): stabilize heartbeat dynamic tool schema

- labels: `codex, sessions, tool_calling`
- `codex`: PR is explicitly in the Codex extension/app-server and fixes Codex thread behavior.
- `sessions`: Core behavior is preventing Codex thread rotation so normal and heartbeat turns reuse the same session/thread binding.
- `tool_calling`: Central change separates durable registered tool schemas from current-turn callable tools, especially for heartbeat_respond.

## openclaw-openclaw-84709 — fix(cron): fail closed when required tools are unavailable

- labels: `codex, cron_automation, exec_tools, reliability`
- `codex`: Changes Codex app-server run handling and native/dynamic tool surface behavior.
- `cron_automation`: PR targets cron isolated-agent jobs and cron finalization behavior.
- `exec_tools`: Central issue is required tool allowlists exposing exec/read shell tool surfaces before dispatch.
- `reliability`: Adds fail-closed preflight and failure classification to avoid false-success cron runs when tools are unavailable.

## openclaw-openclaw-84715 — [Bug]: @openclaw/codex peer link failure reproduced on 2026.5.19 after update

- labels: `codex, packaging_deployment, reliability, skills_plugins`
- `codex`: The failure is explicitly in @openclaw/codex and the Codex harness/shared-client import path.
- `packaging_deployment`: The repro centers on update/install state, Homebrew global install, npm node_modules peer links, and repair flow.
- `reliability`: A missing peer link causes Codex turns to fail before any assistant reply, with repair/health-state expectations.
- `skills_plugins`: The broken dependency is in the managed plugin npm tree and per-plugin peer-link repair is central.

## openclaw-openclaw-84729 — [codex] Fix macOS app copyright year

- labels: `tests_ci, ui_tui`
- `tests_ci`: Updates changed-check planning for app lint skipping and adds matching changed-lanes test coverage.
- `ui_tui`: Changes the macOS app About settings copyright text, a user-facing app UI surface.

## openclaw-openclaw-84732 — Slack channel sends fail: `reconcileUnknownSend` required but no channel adapter implements it

- labels: `chat_integrations, notifications, reliability`
- `chat_integrations`: The failure is specific to Slack channel delivery through the Slack channel adapter.
- `notifications`: The core problem is outbound channel message sending and durable sent-message handling.
- `reliability`: Messages fail or can be lost because required durable delivery reconciliation is unsupported.

## openclaw-openclaw-84740 — Feature Request: Option to hide/suppress certain sessions from the session list

- labels: `sessions, ui_tui`
- `sessions`: Request is to hide/archive or auto-suppress specific sessions, affecting session visibility and persisted archive state.
- `ui_tui`: The change is explicitly about the session list view, row actions, filters, and reducing UI clutter.

## openclaw-openclaw-84752 — fix: self-heal lane wedges + restore openai-codex OAuth on embedded path

- labels: `auth_identity, chat_integrations, codex, queueing, reliability`
- `auth_identity`: Restores OAuth profile/sidecar resolution for embedded auth store loads and the openai-codex provider.
- `chat_integrations`: Fixes Telegram polling-session recovery so Telegram channel ingress does not stay offline.
- `codex`: The auth regression and fix explicitly target the openai-codex provider path.
- `queueing`: Repairs per-lane command queue behavior when lanes return idle with queued work and terminal active work stalls.
- `reliability`: Central theme is self-healing wedged lanes and polling sessions after transient failures without manual restarts.

## openclaw-openclaw-84757 — [Bug]: Telegram session can get stuck after compaction when encrypted reasoning content fails verification

- labels: `chat_integrations, sessions, reliability`
- `chat_integrations`: The bug is specifically in a Telegram direct-chat session and Telegram fallback behavior is user-visible.
- `sessions`: The failure is caused by compacted/restored session history replay and persists until a fresh session is started.
- `reliability`: The session becomes stuck across retries and needs automatic recovery or sanitization to avoid repeated failures.

## openclaw-openclaw-84763 — fix(acpx): scrub provider credential env from ACP harness spawns

- labels: `acpx, acp, auth_identity, security, config`
- `acpx`: The fix is explicitly in the ACPX extension and changes ACPX command decoration/process-spawn behavior.
- `acp`: The failing path is sessions_spawn with runtime:"acp" and ACP harness launch behavior.
- `auth_identity`: The bug centers on inherited provider API keys/OAuth tokens interfering with each harness's own authentication.
- `security`: The change scrubs credential environment variables from child process launches to avoid unsafe token propagation.
- `config`: It adds the acp.scrubProviderEnv configuration knob and updates config schema/help metadata.

## openclaw-openclaw-84789 — Active memory crashes on Telegram forum topic sessions (dirName validation)

- labels: `chat_integrations, memory, sessions, reliability`
- `chat_integrations`: The failure occurs specifically in Telegram forum/topic-based group chat sessions.
- `memory`: Active memory starts for the message but crashes, blocking the active memory feature.
- `sessions`: The root cause is a Telegram-derived session key with colons being reused as a directory name.
- `reliability`: The issue is an immediate crash/lane task error affecting all Telegram forum topic messages.

## openclaw-openclaw-84794 — Clean up isolated cron sessions after runs

- labels: `cron_automation, sessions, reliability`
- `cron_automation`: The change is specifically for isolated cron jobs/runs and their delete-after-run behavior.
- `sessions`: Core behavior is deleting run-scoped cron sessions via cleanup after the run completes.
- `reliability`: Moves cleanup into a finally path so sessions are cleaned up across delivery-none, errors, and other terminal paths.

## openclaw-openclaw-84802 — fix(memory-core): allow bounded dreaming session cleanup

- labels: `memory, sessions, reliability`
- `memory`: Change is in memory-core dreaming narrative behavior and changelog explicitly describes Memory-core/dreaming cleanup.
- `sessions`: Core fix changes stable dreaming narrative session keys and deleteSession cleanup behavior for stale sessions.
- `reliability`: Fix bounds cleanup so stale dreaming-narrative sessions do not accumulate and handles cleanup failures in tests.

## openclaw-openclaw-90146 — google-vertex: Missing gemini-3.1-flash-lite in provider catalog causes silent failure instead of error

- labels: `agent_runtime, model_releases, model_serving, reliability`
- `agent_runtime`: The failure occurs in the embedded agent runner and model fallback loop, causing the agent run to produce no reply.
- `model_releases`: The issue centers on adding/supporting a specific newly available Gemini model ID, gemini-3.1-flash-lite.
- `model_serving`: The Google Vertex provider catalog/model selection layer is missing the model and raises model_not_found.
- `reliability`: A known failover/model_not_found error is swallowed, resulting in silent failure instead of fallback or a user-facing error.
