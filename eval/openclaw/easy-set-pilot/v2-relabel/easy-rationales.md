# easy-set-pilot rationales

## openclaw-openclaw-10467 — [Feature Request]: Multi-lane concurrency support for sub-agents via sessions_spawn

- labels: `agent_runtime, sessions, queueing, config, acp`
- `agent_runtime`: Feature is about sub-agent spawning, concurrency, and lifecycle/orchestration behavior.
- `sessions`: The requested change is to the sessions_spawn tool and mentions session file locks/state.
- `queueing`: Core problem is a single global subagent queue lane and proposed independent named lanes.
- `config`: Requires per-lane maxConcurrent configuration in openclaw.json/config schema.
- `acp`: sessions_spawn and ACP spawn paths are explicitly involved in forwarding the lane.

## openclaw-openclaw-39714 — Sandbox: fix Dockerized browser bridge and tab creation

- labels: `sandboxing, browser_automation, reliability`
- `sandboxing`: The fix targets Dockerized sandbox agents, container reachability, host-gateway extraHosts, and sandbox browser configuration.
- `browser_automation`: Core changes are to the browser bridge, CDP access, Playwright tab creation, and browser open/status behavior.
- `reliability`: It fixes unreachable 127.0.0.1 bridge URLs and tab-open timeouts for sandboxed browser requests.

## openclaw-openclaw-40332 — [Feature]: Per-binding and per-agent permissionMode for ACP sessions

- labels: `acp, acpx, approvals, config, security`
- `acp`: Feature is explicitly for ACP sessions, per-binding ACP settings, and per-agent ACP runtime overrides.
- `acpx`: Current global setting is in the acpx plugin config and the fallback remains plugins.entries.acpx.config.permissionMode.
- `approvals`: The requested permissionMode values are approval modes such as approve-all and approve-reads.
- `config`: Issue proposes new configuration fields and override precedence across bindings, agent runtime, and global defaults.
- `security`: Motivation is limiting over-privileged agents with different trust levels and reducing global access exposure.

## openclaw-openclaw-41892 — feat(control-ui): add cron calendar timeline view

- labels: `cron_automation, ui_tui`
- `cron_automation`: PR directly adds a timeline view for Cron Jobs, scheduled tasks, run times, high-frequency cron chips, and upcoming jobs.
- `ui_tui`: Feature is explicitly for the Control UI Cron Jobs page, adding visual timeline, hover popups, zoom controls, theme support, and mobile fallback.

## openclaw-openclaw-42027 — fix: resolve exec PATH fallback, layered browser diagnostics, and cron force-run deadlock

- labels: `exec_tools, browser_automation, cron_automation, queueing, reliability`
- `exec_tools`: Exec tool PATH recovery is changed for sandbox-host fallback to local execution.
- `browser_automation`: Browser status diagnostics cover profile attach mode, CDP reachability, and browser HTTP errors.
- `cron_automation`: Detached cron.run --force behavior is fixed for cron execution.
- `queueing`: A new CronManual lane separates manual force-runs from the cron execution lane to prevent blocking.
- `reliability`: The PR fixes fallback behavior, diagnostic failures, and a cron self-deadlock.

## openclaw-openclaw-42122 — Speed up install smoke Docker builds

- labels: `packaging_deployment, tests_ci`
- `packaging_deployment`: Changes Dockerfile build behavior and Docker build args for install smoke images.
- `tests_ci`: Updates the .github install-smoke workflow to speed up CI smoke Docker builds.

## openclaw-openclaw-42408 — [Bug/Docs]: local+hybrid memory_search quality can appear unstable due to extraPaths path drift + benchmark-file contamination

- labels: `memory, config, docs`
- `memory`: Issue centers on memory_search/index quality, hybrid retrieval ranking, indexed corpus contamination, and reindexing behavior.
- `config`: Root cause includes extraPaths path drift and guidance to use aligned absolute paths in the active workspace.
- `docs`: Request explicitly asks for memory index/search documentation on path hygiene and benchmark contamination pitfalls.

## openclaw-openclaw-42425 — fix(hooks): load workspace hooks for non-default agents

- labels: `hooks, gateway, sessions`
- `hooks`: PR directly changes the hooks loader to load workspace-local hooks and scope hook handlers.
- `gateway`: The fix occurs at gateway startup and modifies server-startup behavior for multi-workspace hook loading.
- `sessions`: Workspace hook scope is resolved partly from session context/session keys, with regression tests for session-based scoping.

## openclaw-openclaw-42606 — Browser: harden noVNC bootstrap headers

- labels: `browser_automation, security, api_surface`
- `browser_automation`: Change is in the browser bridge noVNC observer bootstrap route for sandbox browser access.
- `security`: PR explicitly hardens the bootstrap page with CSP nonce, nosniff, frame denial, and token-flow protection.
- `api_surface`: It changes HTTP response headers and behavior for the /sandbox/novnc endpoint contract.

## openclaw-openclaw-43416 — feat(ui): add copy button for assistant messages

- labels: `ui_tui`
- `ui_tui`: Adds a hover-triggered copy button and visual feedback in the OpenClaw chat UI message view.

## openclaw-openclaw-43564 — [Feature Request] ACP Session Skill Context Injection

- labels: `acp, sessions, skills_plugins, security`
- `acp`: Feature explicitly targets ACP agents and `sessions_spawn(runtime="acp")`.
- `sessions`: Request is about injecting context when spawning ACP session contexts.
- `skills_plugins`: Central behavior is rendering and injecting OpenClaw skills/SKILL.md content.
- `security`: Issue calls out maintaining isolation so skills do not grant OpenClaw-only tools and is marked for security review.

## openclaw-openclaw-43765 — Improve runtime recovery for heartbeat, Feishu, and exec sessions

- labels: `chat_integrations, cron_automation, exec_tools, gateway, reliability`
- `chat_integrations`: Feishu websocket/channel runtime state is a central part of the PR.
- `cron_automation`: Heartbeat runs are changed to consume and requeue exec system events correctly.
- `exec_tools`: Exec/process tooling terminal status and non-zero foreground exit handling are central changes.
- `gateway`: The generic gateway channel health monitor is updated to restart stale or disconnected channels.
- `reliability`: The PR focuses on recovery from stale sockets, replayed completed work, and incorrect process completion state.

## openclaw-openclaw-44379 — fix(pi-runner): harden context-overflow recovery with one suppress-hook retry

- labels: `agent_runtime, hooks, memory, reliability`
- `agent_runtime`: Changes the embedded PI runner run loop and attempt flow for context-overflow recovery.
- `hooks`: Adds a suppressPromptHookContext retry that disables prompt-hook context injection as a fallback.
- `memory`: The failure mode is oversized external memory/prompt injections causing repeated context overflow.
- `reliability`: Hardens overflow recovery with a bounded retry and normalization of overflow stop reasons to reduce hard failures.

## openclaw-openclaw-45200 — fix(subagents): notify user on announce give-up instead of silently dropping result

- labels: `agent_runtime, notifications, reliability`
- `agent_runtime`: The change is in subagent run handling, adding behavior in resumeSubagentRun when announce give-up occurs.
- `notifications`: The core fix is to notify the user on announce retry-limit instead of silently dropping the completed result.
- `reliability`: Addresses a retry-budget exhaustion failure mode and adds best-effort recovery/audit behavior for lost subagent results.

## openclaw-openclaw-45393 — fix(errors): friendly message and last-message repair for tool_use/tool_result mismatch (#45385)

- labels: `tool_calling, reliability, sessions, security`
- `tool_calling`: Central fix handles Anthropic tool_use/tool_result mismatches and strips dangling tool_use blocks.
- `reliability`: Repairs timeout/race/last-message edge cases that caused rejected conversations and improves recoverable user-facing errors.
- `sessions`: The mismatch is in session history, with guidance to start a fresh session and repair of last-message state on resume.
- `security`: Bundled read-tool changes wrap inbound media content as untrusted and escape it to mitigate prompt injection.

## openclaw-openclaw-45508 — [Feature]: Self-hosted STT/TTS provider support in webchat (Route webchat TTS through the gateway instead of browser Speech API)

- labels: `self_hosted_inference, chat_integrations, gateway, config`
- `self_hosted_inference`: Issue explicitly requests self-hosted STT/TTS support for Speaches, Whisper, Kokoro, and OpenAI-compatible audio endpoints.
- `chat_integrations`: The affected surface is webchat, including Read aloud and mic voice input behavior.
- `gateway`: Proposed fix routes webchat TTS/STT through the gateway instead of browser Web Speech APIs.
- `config`: Problem centers on honoring openclaw.json messages.tts and proposed STT/audio provider configuration.

## openclaw-openclaw-45841 — [Feature]: Sandboxing + ACP

- labels: `acp, sandboxing, security, sessions`
- `acp`: Feature is explicitly about enabling sandboxed OpenClaw sessions to spawn and control ACP sessions.
- `sandboxing`: Core limitation involves Docker/container sandboxed sessions and possible nested sandbox or bridge modes.
- `security`: Proposal centers on preserving isolation, reducing blast radius, and auditable opt-in host-side privilege crossing.
- `sessions`: The behavior in question is sandboxed sessions spawning ACP sessions via sessions_spawn-like flows.

## openclaw-openclaw-46552 — docs(queue): clarify steer behavior with partial streaming and tool boundaries

- labels: `docs, queueing, tool_calling`
- `docs`: PR only changes docs/concepts/queue.md to add explanatory and troubleshooting documentation.
- `queueing`: Central content is queue steer behavior, queue modes, per-session overrides, and followup fallback.
- `tool_calling`: Docs explicitly clarify that steer is not a hard abort and in-flight tool calls run to completion before taking effect.

## openclaw-openclaw-46740 — ACP: classify silent acpx exits as backend unavailable

- labels: `acp, acpx, reliability`
- `acp`: Changes ACP runtime/control-plane error codes and user-facing ACP error text for failed turns.
- `acpx`: Explicitly handles silent non-zero `acpx` backend exits in `extensions/acpx` runtime code.
- `reliability`: Improves availability/error classification when the backend process exits silently instead of returning a structured error.

## openclaw-openclaw-47083 — fix: respect totalTokensFresh flag to avoid showing stale token counts

- labels: `sessions, telemetry_usage, ui_tui`
- `sessions`: The fix adds and respects totalTokensFresh on session list/session row types and sessionInfo updates.
- `telemetry_usage`: Central bug is stale totalTokens/context-used token counts being displayed incorrectly.
- `ui_tui`: Changes affect TUI footer/session actions and Web UI session list presentation.

## openclaw-openclaw-47187 — fix(ui): reset transient chat overlays and style context notice

- labels: `ui_tui`
- `ui_tui`: PR explicitly fixes Control UI chat styling and transient overlay/search state in UI CSS and chat view files.

## openclaw-openclaw-47243 — feat(ui): add timestamp and preview to session list

- labels: `sessions, ui_tui`
- `sessions`: The feature changes the session list data and display, adding last-message preview and timestamp for session rows.
- `ui_tui`: The PR is explicitly a UI change rendering timestamp and preview text in the web session list view.

## openclaw-openclaw-47446 — fix(gateway/discord): respect env proxy vars and prevent ECONNRESET

- labels: `chat_integrations, config, gateway, reliability`
- `chat_integrations`: PR is explicitly for Discord integration behavior: REST calls, WebSocket gateway, bot identity, and interactions.
- `config`: Central change makes proxy behavior respect environment variables and explicit channels.discord.proxy configuration.
- `gateway`: Changes gateway startup and the Discord gateway plugin, including global undici dispatcher bootstrap.
- `reliability`: Fixes proxy-related timeouts and ECONNRESET by disabling keepAlive for local proxy tunnels.

## openclaw-openclaw-48260 — feat(ui): add active time summary to usage overview

- labels: `telemetry_usage, ui_tui`
- `telemetry_usage`: Adds active-time and average-session-duration metrics to the Usage Overview using existing usage session statistics.
- `ui_tui`: User-visible web UI change adding an Active Time card on the Dashboard Usage page.

## openclaw-openclaw-48406 — Docs: add saturated session recovery guide

- labels: `docs, memory, sessions`
- `docs`: Title and body explicitly describe adding operator-facing documentation and reference guides.
- `memory`: Compaction docs/config mention memoryFlush and storing durable memories as part of saturated-session recovery guidance.
- `sessions`: Dedicated saturated-session recovery and session-management compaction docs make session state and recovery central.

## openclaw-openclaw-48580 — Bug: acpx codex sessions 创建的会话立即退出 - stdin is not a terminal

- labels: `acpx, codex, sessions, reliability`
- `acpx`: Issue is about `acpx codex sessions new` and ACPX spawning/handling the agent process.
- `codex`: The failing backend is Codex CLI via `@zed-industries/codex-acp`, with a TTY requirement.
- `sessions`: Core bug is incorrect Codex session state: JSON shows `closed:false` and a PID after the process exited.
- `reliability`: Reports stale/zombie session state and missing liveness cleanup after immediate process exit.

## openclaw-openclaw-48606 — fix: macOS default browser detection fallback to known paths

- labels: `browser_automation, reliability`
- `browser_automation`: Changes browser Chrome executable detection for macOS default Chromium browsers in the browser extension.
- `reliability`: Adds fallback known paths when osascript/defaults resolution fails, preventing missed browser detection.

## openclaw-openclaw-48851 — feat(status): add API call count to session status and usage footer

- labels: `sessions, telemetry_usage, ui_tui`
- `sessions`: The PR persists per-run callCount on session entries and updates session usage state.
- `telemetry_usage`: Adds API call count as usage accounting alongside tokens and cost reporting.
- `ui_tui`: Displays the call count in /status output and the response usage footer.

## openclaw-openclaw-48877 — feat(telegram): add multi-level menu support to customCommands

- labels: `chat_integrations, config`
- `chat_integrations`: PR explicitly changes Telegram bot command and callback handling for inline keyboard menus.
- `config`: Adds declarative customCommands menus/routes fields plus Telegram config types and Zod schema changes.

## openclaw-openclaw-48940 — ACP: add gateway-owned node-backed runtime

- labels: `acp, gateway, agent_runtime, sessions, reliability`
- `acp`: Title and body explicitly add a node-backed ACP runtime with ACP worker events and protocol docs.
- `gateway`: Gateway owns durable ACP state, ingests worker events, and remains authoritative for terminal run state.
- `agent_runtime`: The PR implements a node-backed execution worker bridge, run control, lifecycle handling, and runtime recovery.
- `sessions`: The durable ACP store persists sessions and run state, with restart/replay behavior tied to gateway session state.
- `reliability`: Core changes target restart, replay, reconnect, cancel/close races, lease fencing, and crash recovery.

## openclaw-openclaw-49310 — fix: keep tui busy during follow-up waits

- labels: `sessions, ui_tui`
- `sessions`: Core behavior depends on detecting the sessions_yield marker and preserving/restoring follow-up state from session history.
- `ui_tui`: Change is in TUI files and adds an `awaiting follow-up` busy activity/status state for visible UI behavior.

## openclaw-openclaw-49502 — feat(gateway): include usage/cost metadata in agent.wait terminal response

- labels: `gateway, api_surface, telemetry_usage`
- `gateway`: Changes are in gateway server methods and add metadata to the gateway agent.wait response paths.
- `api_surface`: Extends the agent.wait WebSocket response contract with an optional meta field while preserving compatibility.
- `telemetry_usage`: The new meta field carries token usage, last-call usage, estimated cost, provider, and model data.

## openclaw-openclaw-50054 — fix(acp): add distributed session locking with fail-closed redis fallback

- labels: `acp, sessions, reliability`
- `acp`: PR explicitly wires locking into ACP dispatch and skips ACP execution when locked.
- `sessions`: Core change is distributed locking keyed to ACP sessions via SessionLockManager.
- `reliability`: Adds fail-closed Redis behavior, owner-checked release/renew, and contention handling to avoid unsafe concurrent runs.

## openclaw-openclaw-51667 — Feature: Native Audio Input for Omni-Modal Models (skip STT transcription)

- labels: `chat_integrations, config, model_serving, sessions`
- `chat_integrations`: The feature is driven by WhatsApp/Telegram voice notes arriving through chat channels.
- `config`: The request proposes explicit configuration flags such as tools.media.audio.native and fallbackToTranscription.
- `model_serving`: Central behavior is sending audio as a native media part to omni-modal model providers instead of STT.
- `sessions`: Comments highlight transcript durability, snapshot/restore, and session continuity impacts when bypassing transcription.

## openclaw-openclaw-51849 — Docs: add freeCodeCamp OpenClaw full tutorial to showcase

- labels: `docs, agent_demos`
- `docs`: PR only changes docs/start/showcase.md to add a tutorial entry to documentation.
- `agent_demos`: Adds a showcase/tutorial video under “OpenClaw in Action,” matching demo/showcase/walkthrough cues.

## openclaw-openclaw-52249 — ACP parent session stuck until refresh when yielded waiting for child completion

- labels: `acp, sessions, queueing, reliability`
- `acp`: Issue is explicitly about ACP parent-stream relay, ACP child sessions, and ACP yield/resume behavior.
- `sessions`: Core failure involves parent/child session state, sessions_spawn, sessions_yield, and automatic session resume.
- `queueing`: Fix routes child-completion follow-ups through enqueueSystemEvent and heartbeat wake scheduling instead of direct resume.
- `reliability`: Parent session becomes stuck/wedged until refresh due to state inconsistency and an ad-hoc resume path.

## openclaw-openclaw-53319 — [Bug]: ACP concurrent session spawns — first agent fails to launch CC process

- labels: `acp, acpx, sessions, reliability`
- `acp`: Issue explicitly involves ACP session spawning via `sessions_spawn runtime:"acp"` and ACP backend behavior.
- `acpx`: Environment and analysis identify the ACP backend as `acpx` and suspect the acpx CLI launch path.
- `sessions`: The failure occurs during concurrent child session creation, with child session keys and session state accepted but not progressing.
- `reliability`: Reported as a race/concurrency failure with stalls, silent non-start, possible crash, and missing output.

## openclaw-openclaw-53997 — acpx: add terminal-truth artifacts and strict terminal states

- labels: `acpx, acp, reliability`
- `acpx`: All changed files are under extensions/acpx and the PR explicitly changes the AcpX runtime and artifacts.
- `acp`: The feature concerns ACP runtime-wrapped execution, ACP artifacts, parsed ACP errors, and AcpRuntime behavior.
- `reliability`: Adds durable terminal truth, strict terminal states, abort-before-spawn race handling, and safer retry/error behavior.

## openclaw-openclaw-55790 — sessions_spawn(runtime="subagent") ignores inherited/per-agent subagent thinking defaults and initializes children at low

- labels: `agent_runtime, config, sessions`
- `agent_runtime`: The bug is in spawning a child with runtime="subagent" and resolving subagent runtime defaults.
- `config`: The failure concerns configured thinking defaults such as agents.list[].subagents.thinking and thinkingDefault inheritance.
- `sessions`: sessions_spawn creates child sessions with incorrect session state, shown in parent/child session transcripts.

## openclaw-openclaw-56442 — feat: Add opt-in ACP parent completion notify for sessions_spawn

- labels: `acp, sessions, notifications, api_surface`
- `acp`: Feature is explicitly for ACP `sessions_spawn` with ACP `mode:"run"` completion behavior.
- `sessions`: Change routes child ACP spawn completions back to the parent requester session and depends on session context.
- `notifications`: Adds opt-in `parentUpdates:"notify"` completion announce/notification routing with fallback behavior.
- `api_surface`: Introduces a new `parentUpdates` parameter in the `sessions_spawn` contract and gateway protocol schema.

## openclaw-openclaw-56532 — memory-lancedb: add configurable timeout/retry for embedding calls

- labels: `memory, config, reliability`
- `memory`: PR changes the memory-lancedb extension's embedding path and LanceDB memory provider behavior.
- `config`: Adds and validates configurable embedding.timeoutMs and embedding.maxRetries fields in config and plugin manifest.
- `reliability`: Timeout/retry bounds prevent hung or 5xx-storming embedding backends from stalling agent turns and reduce failure cascades.

## openclaw-openclaw-56613 — [Feature]: Talk/Voice tab — agent/session switching + per-agent TTS voice

- labels: `sessions, ui_tui, config`
- `sessions`: Voice/Talk mode is hardcoded to the main session and needs to respect selected agent/session routing.
- `ui_tui`: Request is for Talk/Voice tab UI behavior, adding an agent/session picker similar to the Chat tab.
- `config`: Per-agent TTS voice is specified through agent-level configuration such as agents.list[].tts overriding global TTS settings.

## openclaw-openclaw-56866 — feat(whatsapp): ACP session binding with media threading and prompt fixes

- labels: `acp, chat_integrations, hooks, sessions`
- `acp`: PR explicitly adds WhatsApp ACP binding support, ACP dispatch changes, and ACP prompt/media handling.
- `chat_integrations`: WhatsApp channel message handling and delivery are the integration surface being changed.
- `hooks`: Adds before_prompt_build and plugin lifecycle hook dispatch in the ACP flow.
- `sessions`: Core feature is configured ACP session binding, routing, long-lived session behavior, and media threading into sessions.

## openclaw-openclaw-58135 — [Feature]: expose promptMode parameter in sessions_spawn for deterministic blank sub-agents

- labels: `acp, api_surface, agent_runtime, sessions`
- `acp`: The feature targets the ACP session tool `sessions_spawn` and its parameters.
- `api_surface`: It asks to add an optional `promptMode` field to the spawn handler parameter schema/request contract.
- `agent_runtime`: The change controls child sub-agent run configuration and system prompt construction.
- `sessions`: It concerns spawning child sessions/sub-agents and their inherited session prompt state.

## openclaw-openclaw-58411 — sessions_spawn lacks --bind here equivalent — agent cannot bind ACP session to existing Discord thread

- labels: `acp, sessions, chat_integrations, api_surface`
- `acp`: Issue is about ACP session spawning and matching `/acp spawn --bind here` semantics.
- `sessions`: Central request is binding a spawned session to an existing thread instead of creating a new one.
- `chat_integrations`: The affected UX is an existing Discord thread where the agent should continue in place.
- `api_surface`: Proposes adding a `bindTo: "current"` option to the programmatic `sessions_spawn` request contract.

## openclaw-openclaw-59208 — fix(status): honor selected usage auth profile

- labels: `auth_identity, telemetry_usage, ui_tui`
- `auth_identity`: Core fix is selecting the correct OAuth auth profile via session authProfileOverride for credential resolution.
- `telemetry_usage`: The bug affected provider usage/quota resolution and the /status usage line.
- `ui_tui`: The visible issue was an inconsistent /status status card/status surface.

## openclaw-openclaw-59878 — Session lane stuck in 'running' after run dies — sessions.abort + gateway restart fail to clear stale state

- labels: `sessions, gateway, queueing, reliability`
- `sessions`: The bug is about session lanes stuck in persisted `running` state and `sessions.abort`/`sessions.send` behavior.
- `gateway`: Gateway restart and gateway RPC calls are central to the stale-state recovery failure.
- `queueing`: New messages queue indefinitely behind a dead session lane lock, with lane wait warnings and queueAhead evidence.
- `reliability`: Core failure is stale state after a dead run, missing cleanup/reconciliation, and need for timeout auto-recovery.

## openclaw-openclaw-60737 — [Feature]: Per-DM/per-chat default ACP binding for auto-spawning ACP sessions on new topics

- labels: `acp, chat_integrations, config, sessions`
- `acp`: Feature is explicitly about default ACP bindings and auto-spawning ACP sessions.
- `chat_integrations`: Behavior is scoped to Telegram DM and group forum topics/chats.
- `config`: Proposes new defaultAcp options in TelegramDirectConfig/TelegramGroupConfig.
- `sessions`: Focuses on creating, binding, and routing topic/thread conversations to ACP sessions.

## openclaw-openclaw-60979 — feature: sessions_spawn ACP delivery to channel (stream output to Zulip/Discord topic)

- labels: `acp, sessions, chat_integrations, notifications`
- `acp`: Feature is explicitly for `sessions_spawn` with `runtime="acp"` and ACP session output delivery.
- `sessions`: The requested behavior concerns spawned session output binding and `SessionBindingAdapter` infrastructure.
- `chat_integrations`: Output should be streamed to Zulip/Discord channel conversations or topics.
- `notifications`: Proposes a `delivery.mode: "announce"` option to route session output to a channel.

## openclaw-openclaw-61775 — enhance Makefile with standard build, test, and quality targets

- labels: `packaging_deployment, tests_ci`
- `packaging_deployment`: Makefile adds standard build/developer workflow targets delegating to pnpm, including build, rebuild, clean-dist, deps, and dev.
- `tests_ci`: Makefile adds test and quality-gate targets such as check, lint, typecheck, test, test-coverage, and landing-gate.

## openclaw-openclaw-62428 — test(exec): land exec v2 contract follow-through

- labels: `exec_tools, approvals, security, tests_ci`
- `exec_tools`: Exec V2 contracts, allowlists, safeBins, command matching, and interpreter/script command handling are central.
- `approvals`: Files and tests focus on exec approvals, allow-always decisions, allowlist mode, and effective approval/security policy merging.
- `security`: Safe-bin trust rules, rejected bins, mutable trusted-dir filtering, command-contract hardening, and security audit changes are central.
- `tests_ci`: The PR is explicitly test(exec) and adds extensive contract tests for allowlists, safeBins, policies, and Linux behavior.

## openclaw-openclaw-62769 — [Feature]: Support ACP configured bindings for Telegram DMs (not just groups/topics)

- labels: `acp, chat_integrations, sessions`
- `acp`: Issue is explicitly about Telegram bindings with type "acp" routing messages to an ACP harness/session.
- `chat_integrations`: The failing surface is Telegram DM conversations versus Telegram groups/topics.
- `sessions`: Expected behavior is creating/resuming persistent ACP sessions, with session metadata loss noted.

## openclaw-openclaw-63007 — Pass outbound session identity into message_sending and surface guarded gateway send denial

- labels: `gateway, hooks, notifications, sessions`
- `gateway`: PR explicitly fixes the `gateway call send` path and changes gateway server send handling/tests.
- `hooks`: Central change passes identity into the `message_sending` hook context and updates hook mappers/types.
- `notifications`: Changes the outbound message delivery path and surfaces guarded delivery cancellation instead of a generic no-result error.
- `sessions`: Adds and propagates outbound `agentId`/`sessionKey` session identity through delivery and hook context.

## openclaw-openclaw-63229 — Bug: Gateway falsely marks healthy local vLLM endpoints as timed out/overloaded, causing 1–23 min fallback cascades

- labels: `gateway, local_models, model_serving, reliability`
- `gateway`: The bug is in the gateway's model-fallback/routing subsystem and includes gateway timeouts and restart/draining messages.
- `local_models`: Healthy local vLLM endpoints running Gemma and Qwen on dedicated local GPUs are central to the report.
- `model_serving`: The issue concerns vLLM endpoint health classification, request routing, provider fallback, and timeout/overload serving semantics.
- `reliability`: The core failure is false timeouts/overload states causing long fallback cascades and unresponsive gateway behavior.

## openclaw-openclaw-63826 — security: fix HIGH/CRITICAL vulns in skill scanner, SSRF, hook priority, and token verification

- labels: `security, skills_plugins, hooks, auth_identity, local_model_providers`
- `security`: PR explicitly fixes HIGH/CRITICAL vulnerabilities including SSRF, scanner bypasses, hook bypass, and token revocation TOCTOU.
- `skills_plugins`: Core changes affect the skill scanner and plugin registry protections for external plugins.
- `hooks`: Hook priority clamping is a central fix to prevent malicious hooks from bypassing security-critical hooks.
- `auth_identity`: Device token verification and revocation behavior is explicitly modified for authentication safety.
- `local_model_providers`: SSRF fix is in self-hosted OpenAI-compatible local model provider discovery using user-provided baseUrl.

## openclaw-openclaw-64181 — fix(hooks): reject error responses from slug generator and strip post-truncation dashes

- labels: `hooks, memory, reliability`
- `hooks`: The fix is explicitly in the hooks slug generator files and title, adjusting hook-side LLM slug response handling.
- `memory`: The bug caused invalid session memory filenames and fragmented canonical daily memory paths.
- `reliability`: Rejects failure-mode/error payloads and fixes truncation cleanup to prevent malformed slugs from regressions.

## openclaw-openclaw-64199 — [Bug]: ACP configured binding uses parent channel ID for session key — all threads under same channel share one persistent Claude Code process

- labels: `acp, acpx, sessions, chat_integrations, security`
- `acp`: Issue explicitly concerns runtime.type "acp" configured bindings and buildConfiguredAcpSessionKey behavior.
- `acpx`: The wrong key maps to the same acpxRecordId and shared acpx state records/persistent client.
- `sessions`: Core bug is incorrect session-key granularity causing multiple Discord threads to share one persistent session/process.
- `chat_integrations`: Discord channel bindings and Discord thread IDs are central to the reproduction and impact.
- `security`: Cross-thread context contamination exposes one thread's conversation history to another.

## openclaw-openclaw-64718 — fix(security): default exec to deny for non-owner auto-reply senders

- labels: `security, exec_tools, approvals, auth_identity`
- `security`: PR explicitly hardens a security boundary against unauthenticated prompt-injection causing arbitrary command execution.
- `exec_tools`: Change centers on exec tool override resolution and defaulting exec security to deny for non-owners.
- `approvals`: The fix changes ask behavior from no approval gate to ask="always" for non-owner auto-reply senders.
- `auth_identity`: Behavior is gated on senderIsOwner, distinguishing owner sessions from unauthenticated/non-owner senders.

## openclaw-openclaw-65187 — test: add regression tests for <final> tag stripping in UI message extraction

- labels: `tests_ci, ui_tui`
- `tests_ci`: PR adds regression tests and Vitest assertions only, with no production code changes.
- `ui_tui`: Tests cover Control UI chat message extraction and stripping of tags from displayed assistant text.

## openclaw-openclaw-65242 — fix: CompletionDeliveryGate to prevent duplicate ACP completion delivery

- labels: `acp, coding_agents, notifications, reliability, sessions`
- `acp`: The PR is explicitly about duplicate ACP child-session completion delivery and adds ACP-specific silent-wake handling.
- `coding_agents`: ACP spawned child runs are the coding-agent completion path involved, with acp-spawn files and Codex ACP child-session test keys.
- `notifications`: The new CompletionDeliveryGate coordinates user-visible completion banners, announces, and farewell delivery to prevent duplicate messages.
- `reliability`: The fix addresses racing delivery paths, stale completion replays, and duplicate outputs using first-writer-wins coordination.
- `sessions`: The logic keys delivery by owner/requester/child session identity and changes ACP parent-child session wake behavior.

## openclaw-openclaw-65364 — feat(plugins): add registerProviderRuntimeAuthOverride API

- labels: `api_surface, auth_identity, security, skills_plugins`
- `api_surface`: Introduces a new public registration API with explicit input/result types and runtime contract.
- `auth_identity`: The API supplies runtime provider credentials and auth modes such as api-key, oauth, token, and aws-sdk.
- `security`: Handles brokered/vault-backed credentials, provider headers, validation, and security-boundary concerns around auth overrides.
- `skills_plugins`: The feature is a plugin SDK/runtime API, registerProviderRuntimeAuthOverride, for external plugins.

## openclaw-openclaw-65640 — fix(acp): persistent session recovery for --bind here sessions

- labels: `acp, acpx, sessions, reliability`
- `acp`: PR explicitly fixes ACP persistent session behavior for /acp spawn and /acp model paths.
- `acpx`: Failure mode centers on an acpx backend losing ACP session state and needing fresh handles.
- `sessions`: Core issue is persistent session resume, --bind here session keys, stale bindings, and session cleanup.
- `reliability`: Adds retry and recovery handling for stale/missing backend sessions after restart or eviction.

## openclaw-openclaw-66000 — fix(cli): clear conflicting OPENCLAW_LAUNCHD_LABEL when --profile is provided

- labels: `config, gateway, packaging_deployment`
- `config`: Fix centers on CLI profile handling and the OPENCLAW_LAUNCHD_LABEL environment variable override behavior.
- `gateway`: Bug occurs when running gateway status from within a gateway process and resolving the correct profiled gateway plist.
- `packaging_deployment`: Launchd labels and LaunchAgents plist resolution are service-manager/deployment concerns.

## openclaw-openclaw-66125 — [Bug]: openai-completions fallback candidate is selected, but fallback does not complete successfully through an OpenAI-compatible proxy

- labels: `local_model_providers, model_serving, reliability`
- `local_model_providers`: Central issue is a local OpenAI-compatible provider/proxy with baseUrl, api mode, model discovery, and fallback-chain selection.
- `model_serving`: Failure concerns OpenAI-compatible /v1/models and /v1/chat/completions endpoint semantics, request-shape compatibility, and streaming/usage chunk handling.
- `reliability`: It is a regression where the selected fallback provider fails to complete and falls through without clear diagnostics.

## openclaw-openclaw-66327 — feat(msteams): implement sendPayload for interactive approval cards

- labels: `chat_integrations, approvals, notifications`
- `chat_integrations`: Implements MS Teams channel outbound behavior for rendering interactive cards in the Teams integration.
- `approvals`: Feature specifically changes approval prompts to show Approve/Deny Adaptive Card buttons and send /approve commands.
- `notifications`: Changes outbound payload/message delivery so interactive approval prompts are delivered as cards instead of plain text.

## openclaw-openclaw-67244 — Explicit ACP agent runs: embedded backend visibility failure and stale final JSON state after sessions_yield

- labels: `acp, acpx, agent_runtime, sessions, reliability`
- `acp`: Issue is explicitly about ACP agent runs and descendant work after sessions_yield.
- `acpx`: Failure cites the embedded ACPX runtime backend and ACPX backend registration visibility.
- `agent_runtime`: Bugs occur in the explicit embedded agent --json run path and backend lookup for runs.
- `sessions`: Uses a session-id and describes stale final session state after sessions_yield reconciliation.
- `reliability`: Reports stale liveness metadata and backend visibility failures despite completed work.

## openclaw-openclaw-67539 — [Feature]: Add provider-specific TTS prompt hints

- labels: `self_hosted_inference, api_surface`
- `self_hosted_inference`: The feature is centered on TTS/speech providers and model-aware speech prompt hints.
- `api_surface`: It proposes extending the speech provider contract with a buildPromptHint API and tests for that contract.

## openclaw-openclaw-68187 — SSE-backed MCP sessions can stay stale after server restart and fail with 'Session not found'

- labels: `mcp_tooling, sessions, gateway, reliability`
- `mcp_tooling`: The issue centers on an SSE-backed MCP server/integration and MCP tool calls failing after restart.
- `sessions`: Stale OpenClaw client/proxy session state and 'Session not found' are the core failure mode.
- `gateway`: The failure is attributed to the OpenClaw gateway/proxy layer and the workaround is restarting the gateway.
- `reliability`: Expected behavior is restart detection, reconnection, invalidation, and recovery from stale/dead sessions.

## openclaw-openclaw-68204 — Unified run trace schema across agent, ACP, subagent, and task flows

- labels: `acp, agent_runtime, sessions, telemetry_usage`
- `acp`: Issue explicitly requires the trace schema to cover ACP sessions and update ACP parent-child relay paths.
- `agent_runtime`: Core scope is tracing main agent runs, subagents, task flows, and run lifecycle relationships.
- `sessions`: Schema includes sessionKey and parent-child linkage for ACP sessions and related run/session state.
- `telemetry_usage`: Primary request is an observability/tracing schema to reconstruct run timelines and diagnostics.

## openclaw-openclaw-68725 — feat(amazon-bedrock-mantle): add known context windows for open-weight Mantle models

- labels: `config, open_weight_models`
- `config`: PR changes a hosted provider discovery default/lookup table for model contextWindow metadata.
- `open_weight_models`: The context-window table is explicitly for named open-weight model families on Mantle.

## openclaw-openclaw-68843 — fix(acp): treat missing cwd as stale bound session

- labels: `acp, sessions, reliability`
- `acp`: Title and files explicitly target ACP behavior, including ACP_SESSION_INIT_FAILED and dispatch-acp/reset handling.
- `sessions`: Core fix is clearing stale bound ACP sessions and persistent session bindings when the runtime cwd is missing.
- `reliability`: Bug fix prevents wedged retries/dead sessions and enables automatic recovery instead of manual cleanup.

## openclaw-openclaw-68916 — [Bug]: ACP oneshot sessions leave orphaned processes — session reset does not clean up child ACP session keys

- labels: `acp, sessions, reliability`
- `acp`: Issue explicitly concerns ACP oneshot sessions, ACP runtimes, and closeAcpRuntimeForSession cleanup behavior.
- `sessions`: Core bug is parent session reset failing to enumerate and clean up child ACP session keys and lineage metadata.
- `reliability`: Describes orphaned processes, swallowed close failures, memory exhaustion, and missing fallback cleanup.

## openclaw-openclaw-69260 — Harden Gemini ACP integration against ambient API-key fallback and add generic auth-contract hooks for ACP agents

- labels: `acp, auth_identity, hooks, security`
- `acp`: The issue is explicitly about Gemini ACP integration and generic auth contracts for ACP-backed agents.
- `auth_identity`: Central behavior concerns OAuth vs API-key auth lanes, auth-mode pinning, and credential fallback.
- `hooks`: The requested product direction includes generic auth-contract and env-scrubbing hooks for ACP launches.
- `security`: It is framed as hardening/defense-in-depth against ambient API-key credential drift and fail-closed behavior.

## openclaw-openclaw-69328 — fix(acp): avoid false zero-diff failures and append session messages

- labels: `acp, reliability, sessions, ui_tui`
- `acp`: Title and changed files explicitly target ACP control-plane/session manager and ACP verification-gate behavior.
- `reliability`: Fixes false zero-diff hard failures and handles oneshot/persistent completion states more gracefully.
- `sessions`: Persistent session handling and active-run session.message transcript appending are central to the PR.
- `ui_tui`: Control UI chat transcript behavior is changed to append session messages with dedupe and optimistic echo replacement.

## openclaw-openclaw-69669 — ACP: keep thread-bound follow-ups parent-orchestrated by default, not raw pass-through

- labels: `acp, sessions, coding_agents`
- `acp`: Title and body explicitly concern ACP follow-ups, ACP child harness behavior, and sessions_spawn(runtime="acp").
- `sessions`: Core issue is thread-bound parent/child session continuity, reactivation, and follow-up routing after sessions.send.
- `coding_agents`: The behavior is described in ACP thread-bound coding workflows where a parent orchestrator prompts a child coding harness to execute tasks.

## openclaw-openclaw-70002 — ci: skip docs sync & translate-trigger workflows in forks

- labels: `tests_ci`
- `tests_ci`: Changes only GitHub Actions workflow files to add fork guards and prevent CI failures in forks.

## openclaw-openclaw-70518 — fix(config): add heartbeat skill allowlist

- labels: `config, cron_automation, skills_plugins`
- `config`: Adds new heartbeat configuration fields, schema/types/help/labels, and config honor tests for allowSkills.
- `cron_automation`: The changed behavior is specific to periodic heartbeat runs and the heartbeat runner.
- `skills_plugins`: Introduces a heartbeat-specific skill allowlist that controls which skills are loaded for those runs.

## openclaw-openclaw-70529 — [Bug]: Desktop cannot use existing Chrome sessions: EasyClaw Google sign-in fails, and user profile attach fails with spawn npx ENOENT

- labels: `auth_identity, browser_automation, exec_tools, packaging_deployment`
- `auth_identity`: One failure path is Google OAuth/sign-in for the EasyClaw Browser Relay extension after callback.
- `browser_automation`: Core bug blocks attaching to existing Chrome sessions/profiles for browser tool control and tab exposure.
- `exec_tools`: The profile attach path fails when Desktop tries to spawn the `npx` command and gets ENOENT.
- `packaging_deployment`: Desktop packaged app bundles `node` but not `npm`/`npx`, causing a packaged-runtime failure.

## openclaw-openclaw-70882 — fix(bundle-mcp): coerce stringified object/array params before MCP tool calls

- labels: `mcp_tooling, tool_calling, security`
- `mcp_tooling`: The fix is in the bundle MCP materialization layer and targets strict MCP servers rejecting malformed params.
- `tool_calling`: It coerces LLM-produced tool call arguments based on the tool inputSchema before invoking the MCP tool.
- `security`: The final patch adds prototype-pollution and oversized-payload guards around parsing user-controlled tool arguments.

## openclaw-openclaw-71157 — [Feature]: Support WhatsApp disappearing-message expiration for outbound replies

- labels: `chat_integrations, config, security`
- `chat_integrations`: Feature is specifically for WhatsApp outbound replies and Baileys send behavior.
- `config`: Proposes channel/account config keys for disappearing-message expiration and override behavior.
- `security`: Motivation is privacy-sensitive disappearing-message policy mismatch and unexpectedly persistent replies.

## openclaw-openclaw-71216 — Config schema: add `sandbox`, `routing.rules`, `instances`, and `gateway.nodes.denyPaths`

- labels: `config, gateway, local_model_providers, sandboxing, security`
- `config`: Issue explicitly asks to add new fields to the public config schema.
- `gateway`: Requested fields include multi-gateway instances and gateway-enforced denyPaths/nodes behavior.
- `local_model_providers`: routing.rules is for provider selection in a mixed cloud/local-Ollama setup with host/model configuration.
- `sandboxing`: sandbox.mode is proposed as a global sandbox mode for tool execution.
- `security`: denyPaths, sensitive-operation routing, credentials directories, SSH keys, and secrets are central security concerns.

## openclaw-openclaw-71537 — Recover archived (.reset) session transcripts in memory hook + session-logs skill

- labels: `memory, sessions, skills_plugins`
- `memory`: Fixes the bundled session-memory hook so reset archives are read and summarized into memory instead of being missed.
- `sessions`: Core behavior concerns reset/deleted session transcript files, session IDs, and archived session log recovery.
- `skills_plugins`: Updates the session-logs SKILL.md surface with helpers and examples that include archived transcript forms.

## openclaw-openclaw-71594 — docs(gateway): clarify IPv4-only BYOH bind path

- labels: `docs, gateway`
- `docs`: PR primarily clarifies CLI docs, TSDoc/comments, and help text about IPv4-only BYOH gateway binding.
- `gateway`: The documented behavior is specifically the Gateway bind path, customBindHost, and IPv4 sidecar/proxy workaround.

## openclaw-openclaw-71646 — mcp/channel-bridge: pendingClaudePermissions / pendingApprovals leak — no TTL, no close-clear, no cap

- labels: `mcp_tooling, approvals, reliability`
- `mcp_tooling`: Issue is explicitly about `src/mcp/channel-bridge.ts` and a long-running `openclaw mcp serve` process.
- `approvals`: Central leak involves `pendingApprovals`, `exec.approval.requested`, `plugin.approval.requested`, and pending permission replies.
- `reliability`: Reports unbounded pending Maps due to missing TTL, close cleanup, caps, and dropped WebSocket resolution frames.

## openclaw-openclaw-71648 — fix(mcp): bound pendingClaudePermissions / pendingApprovals via TTL sweeper + close clear

- labels: `mcp_tooling, approvals, reliability`
- `mcp_tooling`: PR explicitly fixes src/mcp channel bridge/server behavior for long-running openclaw mcp serve.
- `approvals`: Central state being bounded is pendingApprovals and Claude permission/approval resolution handling.
- `reliability`: Adds TTL sweeping, close-time clearing, and post-close guards to prevent leaks and ghost writes.

## openclaw-openclaw-71784 — Bug: memory search live embedding fails ~20–40% with `fetch failed | other side closed` (provider-agnostic; upstream healthy)

- labels: `memory, reliability`
- `memory`: The bug affects live memory search/query embeddings and semantic memory recall.
- `reliability`: The reported failure is intermittent TLS/socket fetch errors causing unreliable recall despite healthy upstream providers.

## openclaw-openclaw-71803 — CLI watchdog kills sessions that are correctly idle while waiting on a Monitor task

- labels: `agent_runtime, exec_tools, reliability, sessions`
- `agent_runtime`: The issue centers on the CLI backend watchdog supervising an embedded agent process and killing it while the agent is expected-idle.
- `exec_tools`: The expected idle state occurs during a Monitor tool call waiting on a long-running shell command such as Whisper, ffmpeg, or builds.
- `reliability`: It is a timeout/crash-loop failure where a healthy long-running task causes the CLI process to be terminated incorrectly.
- `sessions`: The watchdog destroys the active agent session mid-flow, leaving session state unrecoverable for the user.

## openclaw-openclaw-71930 — Mattermost plugin drops post_edited events — @mentions added via edit do not trigger agent wake

- labels: `chat_integrations, reliability`
- `chat_integrations`: Issue is specifically about Mattermost WebSocket handling of channel message edit events and @mentions.
- `reliability`: A supported event is silently dropped, causing message-loss and failed agent wake behavior.

## openclaw-openclaw-71976 — Memory Dreaming: Light sleep sort prioritizes recency over recallCount, hiding real recall data

- labels: `memory, reliability`
- `memory`: Issue is about Memory Dreaming, short-term recall data, recallCount, rehydration, and promotion behavior in the memory store.
- `reliability`: Describes concrete bugs where sorting and narrow rehydration spans cause valid memory promotion candidates to be hidden or fail.

## openclaw-openclaw-72001 — fix(hooks): write allowedSessionKeyPrefixes from gmail wizard

- labels: `hooks, gateway, config`
- `hooks`: The fix is in Gmail hook setup and hook config validation for templated mapping sessionKey prefixes.
- `gateway`: The bug is that the gateway refused to load the wizard-emitted hooks config on restart.
- `config`: The PR changes the Gmail setup wizard to write hooks.allowedSessionKeyPrefixes into openclaw.json while preserving existing values.

## openclaw-openclaw-72015 — Reliability: active-memory blocks replies and QMD boot initialization can overload multi-agent gateways

- labels: `gateway, memory, reliability`
- `gateway`: Issue describes multi-agent gateway boot/restart overload, health timeouts, and degraded gateway responsiveness.
- `memory`: Central failures involve active-memory and QMD memory startup/update behavior.
- `reliability`: Reported symptoms are slow replies, timeout cascades, high CPU, crash-loop risk, and need for fail-open cancellation/defaults.

## openclaw-openclaw-72016 — [Feature]: doctor api/extendability

- labels: `skills_plugins, config, api_surface`
- `skills_plugins`: Requests a plugin/extensibility architecture and public plugin SDK API for adding custom doctor checks.
- `config`: Doctor checks are meant to diagnose setup, environment, profile, and gateway configuration conflicts before upgrades or production breakage.
- `api_surface`: The requested feature is a supported doctor extension API/contract, including registration of checks and optional fix results.

## openclaw-openclaw-72087 — Bug: dist/entry.js main-path breaks Codex OAuth image generation on Linux while direct runCli()/provider path succeeds

- labels: `auth_identity, codex, packaging_deployment`
- `auth_identity`: The failure is tied to the openai-codex OAuth profile and image auth selection, with no API key used.
- `codex`: The report explicitly involves Codex OAuth and calls to the chatgpt.com backend Codex Responses path.
- `packaging_deployment`: The suspected regression is specifically in the packaged dist/entry.js main bootstrap path versus direct runCli/provider execution.

## openclaw-openclaw-72133 — Feature request: per-message token/cost metadata in mobile app and channel surfaces

- labels: `telemetry_usage, ui_tui, chat_integrations`
- `telemetry_usage`: Request centers on exposing per-message token counts, cost/cache metadata, context percentage, and model information.
- `ui_tui`: Asks to show the metadata in native iOS/Android chat UI and references the existing Control UI display.
- `chat_integrations`: Explicitly requests optional metadata footers in messaging/channel surfaces such as Signal, iMessage, Telegram, and BlueBubbles.

## openclaw-openclaw-72138 — fix(feishu): emit sent hooks for normal replies

- labels: `chat_integrations, hooks, notifications`
- `chat_integrations`: The fix is specifically for the Feishu chat integration normal conversation reply dispatcher.
- `hooks`: The core change emits canonical plugin `message_sent` and internal `message:sent` hooks for reply paths.
- `notifications`: The PR concerns successful outbound message delivery/sent-message handling for normal bot replies, including failures and message IDs.

## openclaw-openclaw-72262 — docs: add WhatsApp 408 disconnect troubleshooting runbook

- labels: `chat_integrations, docs, reliability`
- `chat_integrations`: The runbook is specifically for the WhatsApp channel integration and Baileys/WhatsApp Web disconnect behavior.
- `docs`: The requested fix is to add troubleshooting documentation to WhatsApp and channel troubleshooting docs.
- `reliability`: The content addresses disconnect/reconnect loops, timeouts, stale auth state, and safe recovery steps.

## openclaw-openclaw-73910 — BUG: OpenClaw-managed Codex ACP uses isolated CODEX_HOME without auth bridge and sends unsupported timeout config

- labels: `acp, acpx, auth_identity, codex, config`
- `acp`: The failure is in managed Codex ACP sessions and ACP session/set_config_option handling.
- `acpx`: Direct ACPX to Codex is compared with the managed path, and the ACPX plugin schema/defaults are implicated.
- `auth_identity`: The core failure involves isolated CODEX_HOME lacking Codex authentication and possible auth.json bridging.
- `codex`: The affected managed agent and adapter are explicitly Codex ACP/Codex runtime.
- `config`: Codex rejects an unsupported timeout configuration option sent by OpenClaw.

## openclaw-openclaw-74204 — memory.qmd.update.embedTimeoutMs default (120 s) is too low for local GGUF; error message doesn't surface the fix

- labels: `config, local_models, memory, reliability`
- `config`: The issue is about the default value and override for `memory.qmd.update.embedTimeoutMs`.
- `local_models`: The timeout failure is specific to a local GGUF embedding model running on commodity CPU hardware.
- `memory`: QMD semantic embedding and vector/hybrid memory search are the affected subsystem.
- `reliability`: Repeated embed timeouts and backoff prevent vector search from completing reliably.

## openclaw-openclaw-74305 — [Bug]: ACPX Codex worker fails when model/thinking overrides are configured

- labels: `acpx, acp, codex, reliability`
- `acpx`: The failure is in the ACPX plugin/worker path and ACPX Codex command handling.
- `acp`: The repro uses ACP runtime sessions_spawn and reports AcpRuntimeError/ACP_TURN_FAILED.
- `codex`: The affected worker is codex-acp/Codex CLI with model and reasoning override flags.
- `reliability`: This is a crash/internal-error failure where the worker run fails and no child transcript is created.

## openclaw-openclaw-74484 — Gateway pairing scope deadlock: CLI cannot approve/reject auto-reissued over-scoped repair requests

- labels: `auth_identity, gateway, reliability`
- `auth_identity`: Issue centers on paired CLI device identity, operator scopes, and device.pair approve/reject authorization.
- `gateway`: Failures occur through the OpenClaw gateway control plane and gateway method-scope checks.
- `reliability`: Describes a scope deadlock/recovery failure with auto-reissued pending repair requests and rotating IDs.

## openclaw-openclaw-75657 — fix: local GGUF embedding model warmup blocks Node.js event loop for minutes on startup (ARM64/Pi)

- labels: `gateway, local_models, memory, reliability`
- `gateway`: The bug occurs during Gateway startup and makes the gateway/WebSocket port unreachable until warmup completes.
- `local_models`: A local GGUF embedding model loaded via node-llama-cpp on ARM64/Pi is the central failing backend.
- `memory`: The failing path is memorySearch.provider="local" and local memory embeddings/model initialization.
- `reliability`: The issue is a startup liveness failure caused by event-loop blocking, timeout ineffectiveness, and unreachable services.

## openclaw-openclaw-75784 — Phantom user messages appear in webchat after heartbeat wakes / gateway restart / session repair

- labels: `chat_integrations, gateway, reliability, sessions`
- `chat_integrations`: Issue is visible in the webchat channel, where phantom user messages are displayed to users.
- `gateway`: Gateway restart, Gateway logs, and the Gateway agent method are central to how the synthetic message is submitted.
- `reliability`: Bug involves recovery paths, stuck diagnostics, restart behavior, and phantom messages after repair/wake events.
- `sessions`: Session repair, orphaned session resume, and persistence/history projection are core to the failure.

## openclaw-openclaw-76724 — [Bug]: MCP tools not discovered by Agent despite successful handshake (200 OK)

- labels: `mcp_tooling, ui_tui`
- `mcp_tooling`: Issue is explicitly about an MCP server handshake succeeding but tools/list not being requested and MCP tools not being discovered.
- `ui_tui`: The failure is observed in the Agent Tools dashboard, including the 33/33 enabled count and Reload Config UI path not updating the tool list.

## openclaw-openclaw-77345 — google-vertex SSRF guard blocks fake-IP DNS (model.baseUrl not set for built-in providers)

- labels: `model_serving, security`
- `model_serving`: Bug is in provider transport/endpoint handling for built-in Google Vertex, where the request host is resolved dynamically and model.baseUrl is missing.
- `security`: Central failure is the SSRF guard blocking fake-IP DNS ranges and any fix must preserve scoped SSRF protections.

## openclaw-openclaw-77694 — [Bug]: acpx flow run ACP node outputs return empty strings instead of agent replies

- labels: `acpx, acp, agent_runtime, reliability`
- `acpx`: The bug is explicitly in `acpx flow run` behavior and ACPX flow output capture.
- `acp`: The failing flow nodes are ACP nodes created with `acp(...)`, and their ACP outputs are empty.
- `agent_runtime`: The issue concerns flow-run orchestration of agent execution and capturing agent replies across single- and multi-step runs.
- `reliability`: Runs report `status: completed` while silently returning empty outputs, a concrete failure mode in reply capture.

## openclaw-openclaw-77748 — fix: Codex startup plugins + WhatsApp history & Docker Codex OAuth

- labels: `auth_identity, chat_integrations, codex, packaging_deployment, skills_plugins`
- `auth_identity`: Adds Codex OAuth callback wiring and an openai-codex auth helper for login flows.
- `chat_integrations`: Extends the WhatsApp channel with recent history support for follow-up message actions.
- `codex`: Explicitly fixes Codex harness startup registration and Docker Codex OAuth behavior.
- `packaging_deployment`: Updates docker-compose port/env wiring and adds a Docker auth script.
- `skills_plugins`: Changes startup plugin resolution so the plugin owning the configured primary model is loaded.

## openclaw-openclaw-78528 — Security: skill SecretRef API keys still leak into exec child environments

- labels: `security, exec_tools, skills_plugins, auth_identity`
- `security`: The issue is explicitly a security leak of SecretRef-managed secrets/API keys into child environments.
- `exec_tools`: The leak occurs through commands spawned by the generic exec tool inheriting process.env.
- `skills_plugins`: The affected secrets are skill entry SecretRefs under skills.entries.<skill>.apiKey.
- `auth_identity`: The bug concerns API key credentials and their intended skill-scoped access boundary.

## openclaw-openclaw-78919 — [Bug] ACP sessions_spawn doesn't route images to Codex's native vision like acpx codex exec does

- labels: `acp, acpx, codex, sessions`
- `acp`: Bug centers on ACP runtime behavior and the ACP sessions_spawn path rejecting/not forwarding image attachments.
- `acpx`: The issue explicitly compares ACP behavior against the working acpx codex exec path.
- `codex`: Codex is the target agent/runtime, and the failure is routing images to Codex native vision.
- `sessions`: sessions_spawn and session tracking/delegation are the affected surface.

## openclaw-openclaw-78977 — fix(providers): skip store:false for proxy-like Responses API endpoints (#78897)

- labels: `local_model_providers, model_serving, reliability`
- `local_model_providers`: Central fix targets proxy-like/user-configured OpenAI-compatible providers such as LiteLLM with custom baseUrl/non-OpenAI routes.
- `model_serving`: Adjusts Responses API payload compatibility for model endpoints, specifically whether to send the store field.
- `reliability`: Fix prevents multi-turn continuation failures caused by replayed rs_* items being rejected by proxy backends.

## openclaw-openclaw-79447 — fix(model-auth): resolve per-entry apiKey profile ID references

- labels: `auth_identity, config`
- `auth_identity`: Central fix is resolving stored auth profile ID references to actual API credentials and enforcing bearer-compatible credential classes.
- `config`: Bug occurs in configured models.providers.<id>.apiKey per-entry provider settings and their interpretation.

## openclaw-openclaw-79897 — OpenAI-compatible streaming with llama.cpp saves zero usage (stream closed before final usage chunk)

- labels: `local_models, model_serving, telemetry_usage`
- `local_models`: llama.cpp local backend behavior is central to the reproduction and failure mode.
- `model_serving`: Issue is about OpenAI-compatible SSE streaming semantics and missing a final usage-only chunk.
- `telemetry_usage`: Saved token usage is 0/0/0, breaking status context display and compaction accounting.

## openclaw-openclaw-80008 — feat(plugins): expose ACP spawn and prompt in plugin runtime

- labels: `acp, api_surface, config, notifications, skills_plugins`
- `acp`: Adds api.runtime.acp.spawn() and acp.prompt() for ACP-backed agent sessions.
- `api_surface`: Exposes new plugin runtime API methods and request parameters for spawn/prompt.
- `config`: Adds allowSpawn/allowAcpSpawn configuration gates with schema, types, and defaults.
- `notifications`: Core motivation is channel-delivered ACP output via gateway deliver:true.
- `skills_plugins`: Feature is implemented in the plugin SDK/runtime namespace with plugin mocks, registry, status, and docs.

## openclaw-openclaw-80431 — ACPx plugin-tools MCP config test expects source path but resolver returns dist path

- labels: `acpx, mcp_tooling, tests_ci`
- `acpx`: Failure is in extensions/acpx/src/config.test.ts and concerns ACPx embedded plugin config behavior.
- `mcp_tooling`: The mismatch is for injecting the built-in plugin-tools MCP server and its resolved server entry path.
- `tests_ci`: The issue is a pnpm test failure with expected updates to the test/helper and validation via pnpm test.

## openclaw-openclaw-80475 — test(acpx): accept built-dist MCP server resolution when dist exists

- labels: `acpx, mcp_tooling, tests_ci`
- `acpx`: PR is explicitly under extensions/acpx and updates ACPx config test expectations.
- `mcp_tooling`: The behavior concerns built-in MCP server resolution and server args for plugin-tools/openclaw-tools MCP servers.
- `tests_ci`: Only config.test.ts is changed, with Vitest proof for corrected test helper expectations.

## openclaw-openclaw-81200 — fix(acpx): strip provider API keys from child harness env

- labels: `acpx, acp, security, auth_identity`
- `acpx`: Title and changed files are explicitly in extensions/acpx and modify ACPX wrapper/runtime behavior.
- `acp`: The fix targets built-in Claude and Gemini ACP child harness launches and generated ACP wrapper commands.
- `security`: The change prevents provider API keys from being inherited by spawned child harness environments.
- `auth_identity`: It handles provider auth credentials such as ANTHROPIC_API_KEY, GEMINI_API_KEY, and GOOGLE_API_KEY and their scope.

## openclaw-openclaw-81249 — [Feature/Bug]: Local Ollama embeddings fail when proxy is enabled (SSRF defenses ignore NO_PROXY)

- labels: `config, local_models, security, self_hosted_inference`
- `config`: The issue requests an openclaw.json proxy bypass setting and cites schema rejection of a bypass key.
- `local_models`: Ollama on loopback/local LLM traffic is central to the failure scenario.
- `security`: The requested change alters SSRF protections and NO_PROXY stripping behavior.
- `self_hosted_inference`: Local Ollama embeddings and private/self-hosted inference routing through a proxy are the core problem.

## openclaw-openclaw-81488 — Harden node exec approval precheck env [AI]

- labels: `approvals, exec_tools, security`
- `approvals`: Title and body center on exec approval prechecks and preventing skipped approval prompts.
- `exec_tools`: The change affects node-host command execution, system.run, allowlists, PATH resolution, and exec precheck behavior.
- `security`: Described as security hardening so allowlist decisions cannot depend on gateway-local PATH.

## openclaw-openclaw-81957 — ci: harden GitHub Actions supply-chain boundaries

- labels: `security, tests_ci, auth_identity, packaging_deployment`
- `security`: PR explicitly hardens supply-chain boundaries, workflow permissions, trusted refs, cache/artifact boundaries, and token exposure.
- `tests_ci`: Changes are centered on GitHub Actions CI/release workflows and add focused regression coverage.
- `auth_identity`: OIDC trusted publishing, removal of long-lived token fallback, npm auth separation, and credential scope are central.
- `packaging_deployment`: Release and npm/ClawHub publish workflows and plugin package publishing scripts are directly modified.

## openclaw-openclaw-82145 — cron: allow retries for local model preflight

- labels: `cron_automation, local_model_providers, config, reliability`
- `cron_automation`: Change affects isolated cron jobs and scheduled runs, including when cron marks a run skipped.
- `local_model_providers`: Adds preflight retry controls for local configured providers such as Ollama, vLLM, SGLang, and LM Studio using provider endpoints.
- `config`: Introduces configurable cron.modelPreflight timeoutMs, maxAttempts, and retryDelayMs schema/help/docs settings.
- `reliability`: Retries and timeouts address cold-starting or sleeping local provider availability to avoid premature skipped runs.

## openclaw-openclaw-82507 — [Feature]: ACPX Codex sandbox should inherit user-installed plugins (e.g. Superpowers)

- labels: `acpx, codex, sandboxing, skills_plugins`
- `acpx`: Issue is specifically about ACPX background tasks and ACPX Codex home behavior.
- `codex`: The affected adapter/runtime is Codex, with CODEX_HOME and Codex App plugin inheritance central.
- `sandboxing`: Problem centers on an isolated ACPX Codex sandbox home not inheriting user state.
- `skills_plugins`: Requested feature is inheriting or allowlisting user-installed Codex plugins/skills such as Superpowers.

## openclaw-openclaw-82596 — Feature/exec denylist

- labels: `exec_tools, approvals, security`
- `exec_tools`: Feature directly changes shell exec behavior by adding a denylist for commands such as curl/wget.
- `approvals`: Denylist is implemented as an exec approval/security mode across ExecApprovals evaluators, stores, UI, and docs.
- `security`: Purpose is a security boundary preventing agents from bypassing safer tools and blocking risky network fetches fail-closed.

## openclaw-openclaw-82642 — Fix iMessage slash command acknowledgements

- labels: `chat_integrations, notifications, reliability`
- `chat_integrations`: The fix is specific to the iMessage extension handling inbound DM slash commands.
- `notifications`: The bug concerns acknowledgement/reply delivery policy and suppression for slash command responses.
- `reliability`: It fixes a dropped acknowledgement/reply bug so authorized iMessage commands reliably return responses.

## openclaw-openclaw-83333 — [Bug]: Memory provider cutover to Ollama leaves production index in mixed OpenAI/Ollama vector state after live sync/reload

- labels: `memory, self_hosted_inference, reliability`
- `memory`: Issue centers on memory search indexing, embeddings, vector dimensions, SQLite memory index, and canary recall failures.
- `self_hosted_inference`: Cutover is specifically from OpenAI embeddings to a local/container Ollama embeddings provider for memory search.
- `reliability`: Reports inconsistent mixed provider state after live sync/reload, stale vector dimensions, failed search, and rollback recovery.

## openclaw-openclaw-83863 — ACP/Codex child tasks can be marked succeeded with progress-only output and no final deliverable

- labels: `acp, codex, coding_agents, agent_runtime, reliability`
- `acp`: Issue centers on ACP child sessions and ACP manager terminal done-event handling.
- `codex`: Codex ACP child tasks are explicitly named as the affected runtime path.
- `coding_agents`: The failure concerns external Codex coding-agent child runs and their completion contract.
- `agent_runtime`: Child task/subagent lifecycle state is misclassified as succeeded despite no final deliverable.
- `reliability`: Core bug is an incorrect success state after progress-only output and retry/delivery failure.

## openclaw-openclaw-83982 — fix(clawhub): preserve base URL path prefix [AI-assisted]

- labels: `api_surface, config, skills_plugins`
- `api_surface`: Fixes ClawHub HTTP API request URL construction so paths like /api/v1/search preserve a base path prefix.
- `config`: Behavior depends on configured OPENCLAW_CLAWHUB_URL / CLAWHUB_URL base URLs and their path components.
- `skills_plugins`: The affected ClawHub helper searches and routes ClawHub skills/plugin-related requests.

## openclaw-openclaw-84038 — [Bug]: doctor --fix silently migrates intentional openai-codex/ config to openai/, breaking PI+OAuth runtime and causing 3-4x token inflation

- labels: `config, codex, agent_runtime, auth_identity`
- `config`: The bug is a doctor --fix configuration migration that rewrites model routes and removes configured overrides.
- `codex`: The affected route is explicitly openai-codex/ and the migration re-enables the native Codex runtime.
- `agent_runtime`: The issue centers on preserving or losing agentRuntime: { id: "pi" } versus the native runtime.
- `auth_identity`: The reported breakage involves PI+OAuth setup and auth.order entries for the openai-codex account.

## openclaw-openclaw-84094 — feat(gateway): forward frequency_penalty, presence_penalty, and seed via OpenAI-compatible HTTP gateway

- labels: `gateway, api_surface, model_serving`
- `gateway`: The PR changes the OpenAI-compatible HTTP gateway to validate and forward new request parameters.
- `api_surface`: It updates the POST /v1/chat/completions request contract and OpenAI-compatible 400 validation behavior.
- `model_serving`: It forwards sampling parameters like frequency_penalty, presence_penalty, and seed to the upstream OpenAI-compatible provider endpoint.

## openclaw-openclaw-84301 — [Bug]: Make Dream Diary narrative timeout configurable for slow/serial local model backends

- labels: `config, local_models, queueing, reliability`
- `config`: Issue asks to replace a hardcoded 60s Dream Diary timeout with a user-facing timeout/concurrency config key.
- `local_models`: Failure is specifically tied to slow or serial local model backends such as LM Studio running a local Qwen model.
- `queueing`: The bug involves multiple narrative runs being launched in parallel or queued while the backend processes them serially.
- `reliability`: The hardcoded wait budget causes timeouts and failed narrative runs even though the backend is still working normally.

## openclaw-openclaw-84316 — [Bug]: Telegram group TTS for sub-agent reports success in /tts status but voice never delivered (2026.5.12)

- labels: `chat_integrations, notifications, reliability`
- `chat_integrations`: Bug is specific to Telegram group chat versus Telegram DM delivery behavior.
- `notifications`: Core failure is an outbound TTS voice message reported successful but not delivered to the group.
- `reliability`: Describes message-loss/status-mismatch behavior where success is recorded despite missing delivery.

## openclaw-openclaw-84337 — [Bug]: Hook ingress token unlocks password-mode gateway auth

- labels: `security, auth_identity, gateway, hooks`
- `security`: Describes a high-severity vulnerability where a hook bearer token can bypass intended access controls.
- `auth_identity`: Core bug is authentication credential confusion between hook token and password-mode gateway auth.
- `gateway`: Affected behavior is Gateway HTTP authentication and protected Gateway surfaces.
- `hooks`: The exploit starts from hook ingress token handling for routes such as /hooks/wake.

## openclaw-openclaw-84385 — [codex] Fix macOS app copyright year

- labels: `ui_tui`
- `ui_tui`: Central change fixes the macOS app About settings display text for the copyright year.

## openclaw-openclaw-84413 — [Bug]: 2026.5.18 Codex Chrome DevTools MCP sidecars accumulate under gateway and drive cgroup memory growth

- labels: `codex, gateway, mcp_tooling, reliability`
- `codex`: Issue explicitly concerns embedded openai-codex/gpt-5.5 runs and the Codex app-server spawning sidecars.
- `gateway`: Unreaped children accumulate under the OpenClaw gateway service cgroup and are cleared by gateway restart.
- `mcp_tooling`: The accumulating sidecars are chrome-devtools-mcp process trees/MCP servers.
- `reliability`: Bug is about unreaped long-lived child processes causing memory growth, cleanup failure, and crash-loop risk.

## openclaw-openclaw-84418 — test(cron): document and test owner-only tool security boundary for isolated cron

- labels: `cron_automation, security, tests_ci`
- `cron_automation`: PR is explicitly about isolated cron runs and the cron owner-only tool allowlist.
- `security`: Central change documents and enforces an owner-only tool security boundary, filtering gateway and nodes from unattended runs.
- `tests_ci`: Adds a focused Vitest unit test file with six cases covering the cron allowlist behavior.

## openclaw-openclaw-84419 — fix(session): prefer real tool result over synthetic error in transcript repair

- labels: `sessions, tool_calling, reliability`
- `sessions`: The fix is in session transcript repair and affects persisted session history on session load.
- `tool_calling`: The repaired data is tool-use/tool-result pairing, preferring the real tool result over a synthetic missing-result error.
- `reliability`: Addresses a flush-race failure mode where stale synthetic errors survive despite the real result arriving.

## openclaw-openclaw-84477 — Discord embedded-run prep wedge before strict-agentic, recovery skips sessionId=unknown lanes

- labels: `agent_runtime, chat_integrations, queueing, reliability, sessions`
- `agent_runtime`: The issue centers on embedded agent-run prep stalling before the strict-agentic execution contract and missing agent lifecycle events.
- `chat_integrations`: The failure is reproduced in the Discord channel via @openclaw/discord dispatches.
- `queueing`: It discusses stuck known-session and unknown-session lanes, lane recovery, released lanes, and in-flight lane clearing.
- `reliability`: The core symptom is a wedge/stall with skipped recovery, crash-loop impact, restart mitigation, and re-wedging.
- `sessions`: Session identity and recovery behavior are central, especially sessionId=unknown versus known-session lanes and session.json state.

## openclaw-openclaw-84570 — Remove skill prelude exec allowlist

- labels: `approvals, exec_tools, skills_plugins`
- `approvals`: PR changes exec-approval allowlist behavior so old skill prelude command chains now use the normal approval flow.
- `exec_tools`: Core code updates shell command/exec allowlist analysis for chained commands like cat/printf plus wrapper execution.
- `skills_plugins`: The removed compatibility path is specifically for SKILL.md preludes, trusted skill wrappers, and autoAllowSkills behavior.

## openclaw-openclaw-84583 — cron announce delivery triggers EmbeddedAttemptSessionTakeoverError when user is actively chatting

- labels: `cron_automation, notifications, chat_integrations, sessions, reliability`
- `cron_automation`: Issue centers on a cron job with sessionTarget="isolated" finishing and triggering downstream behavior.
- `notifications`: The failure is caused by announce delivery of the cron result to a user.
- `chat_integrations`: The delivery channel and active user interaction are explicitly Telegram.
- `sessions`: Root cause is concurrent modification of the same Telegram session file and session-state takeover detection.
- `reliability`: Describes a race/conflict causing EmbeddedAttemptSessionTakeoverError and message-loss impact.

## openclaw-openclaw-84637 — [Bug]: Codex runtime/harness is too easy to confuse with gpt-*-codex model fallbacks

- labels: `codex, agent_runtime, config, sessions`
- `codex`: The issue explicitly concerns Codex runtime/harness routing versus Codex-named model IDs.
- `agent_runtime`: Central distinction is `agentRuntime.id = "codex"` or Pi as the runtime/harness routing choice.
- `config`: The bug involves fallback model IDs, default model settings, provider/model runtime config, and policy churn.
- `sessions`: The impact and repro focus on normal sessions being routed or persisted with the intended runtime state.

## openclaw-openclaw-84645 — Materialize node-host inline interpreter eval before exec approval

- labels: `exec_tools, approvals, security`
- `exec_tools`: Changes node-host system.run command handling for Python/Node inline eval by rewriting argv to generated script files.
- `approvals`: Core behavior is materializing inline eval before approval planning so approval can bind to a stable script artifact.
- `security`: PR explicitly preserves the approval security model with fail-closed unsupported forms, private temp files, sha256 filenames, and 0600 mode.

## openclaw-openclaw-84648 — Add SafeOps preflight hook for exec tool

- labels: `exec_tools, hooks, security`
- `exec_tools`: PR explicitly adds a SafeOps preflight before exec command dispatch in bash-tools.exec.ts.
- `hooks`: Title and body describe a preflight hook before tool execution, with new beforeToolExecute.ts.
- `security`: SafeOps policy check affects command dispatch and was reviewed as a security-boundary change with secret/token considerations.

## openclaw-openclaw-84660 — [Bug] Voice STT: empty moonshine transcripts passed as raw JSON to LLM, clogging serialized processing queue

- labels: `chat_integrations, self_hosted_inference, queueing, reliability`
- `chat_integrations`: Bug occurs in Discord voice STT for the bot in a voice channel.
- `self_hosted_inference`: Central issue involves STT inference using moonshine-tiny-en/sherpa-onnx speech transcription output.
- `queueing`: Empty transcripts clog the serialized processing queue and block later voice segments.
- `reliability`: Filtering failure makes the voice pipeline appear unresponsive and needs stale/depth handling.

## openclaw-openclaw-84668 — docs(agent-runtimes): clarify model name vs runtime routing for Codex (#84637)

- labels: `docs, agent_runtime, codex`
- `docs`: Documentation-only PR adding a warning to docs/concepts/agent-runtimes.md.
- `agent_runtime`: Clarifies runtime routing via agentRuntime.id versus model selection and fallbacks.
- `codex`: Specifically addresses Codex runtime confusion with gpt-*-codex model IDs and Codex-named surfaces.

## openclaw-openclaw-84681 — fix(codex): stabilize heartbeat dynamic tool schema

- labels: `codex, sessions, tool_calling`
- `codex`: The PR is explicitly in extensions/codex and changes Codex app-server dynamic tool handling.
- `sessions`: Core fix prevents Codex thread rotation and keeps normal/heartbeat/normal turns on the same thread/session.
- `tool_calling`: Central change stabilizes dynamic tool schemas and controls whether heartbeat_respond is registered versus callable.

## openclaw-openclaw-84709 — fix(cron): fail closed when required tools are unavailable

- labels: `codex, cron_automation, exec_tools, reliability`
- `codex`: PR changes the Codex app-server path and Codex dynamic/native tool surface handling.
- `cron_automation`: Title and files target cron isolated-agent jobs and cron run diagnostics/finalization.
- `exec_tools`: Core fix concerns required runtime tools such as exec/read, tool allowlists, and missing shell tool availability.
- `reliability`: Adds fail-closed behavior and failure classification when required tools are unavailable before dispatch.

## openclaw-openclaw-84715 — [Bug]: @openclaw/codex peer link failure reproduced on 2026.5.19 after update

- labels: `codex, packaging_deployment, reliability, skills_plugins`
- `codex`: The failure is explicitly in @openclaw/codex, the Codex harness, and its shared-client startup import.
- `packaging_deployment`: The bug involves Homebrew/global installation, managed npm dependency trees, peer links, update, and repair flows.
- `reliability`: Missing peer resolution causes the embedded Codex agent to fail before replying, with repair/health-state expectations.
- `skills_plugins`: The issue centers on a managed plugin npm tree and per-plugin peer dependency link for @openclaw/codex.

## openclaw-openclaw-84729 — [codex] Fix macOS app copyright year

- labels: `tests_ci, ui_tui`
- `tests_ci`: Changes scripts/check-changed.mjs and changed-lanes tests for changed-check planning and SwiftLint skip validation.
- `ui_tui`: Updates the macOS About settings user-facing copyright text.

## openclaw-openclaw-84732 — Slack channel sends fail: `reconcileUnknownSend` required but no channel adapter implements it

- labels: `chat_integrations, notifications, reliability`
- `chat_integrations`: Issue is specifically about Slack channel sends through the Slack channel adapter.
- `notifications`: Core failure is outbound message delivery/durable send handling for channel messages.
- `reliability`: A missing reconciliation capability causes send failures and potential message loss.

## openclaw-openclaw-84740 — Feature Request: Option to hide/suppress certain sessions from the session list

- labels: `sessions, ui_tui`
- `sessions`: Request is about hiding, archiving, suppressing, and filtering specific sessions in the session list.
- `ui_tui`: Feature centers on session-list UX: toggles, row actions, filters, and reducing UI clutter.

## openclaw-openclaw-84752 — fix: self-heal lane wedges + restore openai-codex OAuth on embedded path

- labels: `auth_identity, chat_integrations, codex, queueing, reliability`
- `auth_identity`: Restores OAuth profile and legacy sidecar token resolution in the auth profile store.
- `chat_integrations`: Changes Telegram polling-session recovery to keep the Telegram channel from going offline.
- `codex`: Explicitly fixes OAuth resolution for the openai-codex provider on embedded paths.
- `queueing`: Fixes per-lane command queue wedges, queueDepth handling, and terminal queued work recovery.
- `reliability`: Focuses on self-healing wedged lanes and polling stalls without manual gateway restarts.

## openclaw-openclaw-84753 — [Feature]: Show display name instead of user ID in session list

- labels: `chat_integrations, sessions, ui_tui`
- `chat_integrations`: Feature concerns Feishu, Discord, Telegram, WhatsApp channel users and resolving their display names.
- `sessions`: Core request is changing session labels/session list entries from peer IDs to user display names.
- `ui_tui`: Visible surfaces include the Control UI session sidebar and status Sessions table display.

## openclaw-openclaw-84757 — [Bug]: Telegram session can get stuck after compaction when encrypted reasoning content fails verification

- labels: `chat_integrations, sessions, reliability`
- `chat_integrations`: The bug occurs in a Telegram direct-chat session and surfaces through the Telegram fallback message.
- `sessions`: The core failure is persisted session history replay after compaction/restore making the same session unusable.
- `reliability`: The issue is a stuck retry/recovery failure caused by invalid replayed content, requiring automatic sanitization or clean-session recovery.

## openclaw-openclaw-84761 — feat(secrets): scan backup files for plaintext provider apiKey values

- labels: `security, auth_identity, config`
- `security`: PR explicitly adds secret scanning for plaintext provider API keys in backup files to close a security gap.
- `auth_identity`: The sensitive values are provider apiKey credentials used for authentication.
- `config`: The scan targets legacy backup config files such as models.json.* and openclaw.json.old in config-related directories.

## openclaw-openclaw-84763 — fix(acpx): scrub provider credential env from ACP harness spawns

- labels: `acpx, acp, auth_identity, security, config`
- `acpx`: Change is in extensions/acpx runtime/process files and decorates ACPX harness launch commands.
- `acp`: The failing path is sessions_spawn with runtime:"acp" and ACP harness spawning.
- `auth_identity`: Fix targets provider auth inheritance, OAuth/API-key handling, and per-harness authentication behavior.
- `security`: It scrubs provider credential environment variables from child processes to avoid credential leakage/misuse.
- `config`: Adds acp.scrubProviderEnv config knob and updates config schema/types/help metadata.

## openclaw-openclaw-84771 — Event loop saturation during startup: synchronous model-prewarm and session-locks block event loop for 28-64 seconds

- labels: `gateway, model_serving, reliability, sessions`
- `gateway`: Startup of openclaw-gateway.service and gateway ready/restart behavior are central to the failure.
- `model_serving`: A synchronous model-prewarm startup sidecar is one of the two named blockers causing saturation.
- `reliability`: The issue is about event-loop stalls, liveness warnings, heap pressure, crash/restart cascades, and startup recovery failures.
- `sessions`: Session-locks and synchronous parsing of 168 session stores are a named root cause.

## openclaw-openclaw-84789 — Active memory crashes on Telegram forum topic sessions (dirName validation)

- labels: `chat_integrations, memory, sessions, reliability`
- `chat_integrations`: The failure occurs specifically in Telegram forum/topic-based group sessions.
- `memory`: The issue is about the active-memory plugin/sub-agent crashing and being blocked.
- `sessions`: The root cause is Telegram forum session keys with colons being used in directory names.
- `reliability`: Active memory crashes immediately for all Telegram forum topic messages.

## openclaw-openclaw-84794 — Clean up isolated cron sessions after runs

- labels: `cron_automation, sessions, reliability`
- `cron_automation`: PR fixes isolated cron job deleteAfterRun cleanup after runs, including delivery-none cron executions.
- `sessions`: Core behavior deletes run-scoped cron sessions via sessions.delete and shared session-cleanup helper.
- `reliability`: Cleanup is moved into a finally path so terminal paths, runner errors, and no-delivery runs do not leave stale sessions.

## openclaw-openclaw-84802 — fix(memory-core): allow bounded dreaming session cleanup

- labels: `memory, sessions, reliability`
- `memory`: The PR is in extensions/memory-core and changes dreaming narrative behavior in the memory system.
- `sessions`: It changes stable dreaming-narrative session keys, idempotency keys, and deleteSession cleanup behavior.
- `reliability`: The fix prevents stale dreaming sessions from accumulating and adds bounded cleanup around retries/failures.

## openclaw-openclaw-85999 — [Bug]: 2026.5.22 gateway pre-warm (warmCurrentProviderAuthState) blocks event loop ~60s on startup, breaks channel handshakes

- labels: `auth_identity, chat_integrations, gateway, reliability`
- `auth_identity`: The blocking startup work is explicitly `warmCurrentProviderAuthState` and provider auth-state pre-warming.
- `chat_integrations`: Discord, Feishu, and Telegram channel handshakes time out and inbound chat messages stall.
- `gateway`: The regression occurs during gateway startup/restart and affects gateway readiness and inbound dispatch.
- `reliability`: Central symptoms are event-loop starvation, timeouts, liveness warnings, delayed recovery, and message-loss risk.

## openclaw-openclaw-88816 — [Bug]: v2026.05.28 breaks Google Vertex Express API Key

- labels: `auth_identity, config, model_serving`
- `auth_identity`: Issue centers on Google Vertex Express API-key authentication via auth-profile.json.
- `config`: Failure references OpenClaw model/provider configuration and missing models.providers registration.
- `model_serving`: Error is a hosted provider model registration/selection failure for google-vertex model IDs.
