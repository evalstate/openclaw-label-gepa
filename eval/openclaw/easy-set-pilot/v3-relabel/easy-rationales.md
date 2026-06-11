# easy-set-pilot rationales

## openclaw-openclaw-39714 — Sandbox: fix Dockerized browser bridge and tab creation

- labels: `sandboxing, browser_automation, reliability`
- `sandboxing`: PR fixes Docker sandbox container connectivity and host-gateway/extraHosts behavior for sandboxed agents.
- `browser_automation`: Changes browser bridge, CDP access, Playwright tab creation, and browser open/status flows.
- `reliability`: Addresses unreachable 127.0.0.1 bridge URLs and tab-open timeouts in Dockerized sandbox flows.

## openclaw-openclaw-40332 — [Feature]: Per-binding and per-agent permissionMode for ACP sessions

- labels: `acp, acpx, approvals, config, security`
- `acp`: Feature is explicitly about ACP sessions, ACP bindings, and ACP override precedence.
- `acpx`: The current global setting is in the acpx plugin config path plugins.entries.acpx.config.permissionMode.
- `approvals`: permissionMode values like approve-all and approve-reads control approval/permission behavior for access.
- `config`: Request is to add per-binding and per-agent config overrides with fallback precedence.
- `security`: Motivation is scoping permissions by trust level to avoid over-provisioning agents with shell/write access.

## openclaw-openclaw-41892 — feat(control-ui): add cron calendar timeline view

- labels: `cron_automation, ui_tui`
- `cron_automation`: The feature is for the Cron Jobs page and visualizes today's scheduled cron tasks, high-frequency jobs, and run timing.
- `ui_tui`: It adds a Control UI calendar/timeline view with hover popups, zoom controls, theming, mobile fallback, and i18n strings.

## openclaw-openclaw-42027 — fix: resolve exec PATH fallback, layered browser diagnostics, and cron force-run deadlock

- labels: `exec_tools, browser_automation, cron_automation, queueing, reliability`
- `exec_tools`: Exec tool PATH recovery is changed in bash-tools.exec.ts so local fallback can find login-shell-managed binaries.
- `browser_automation`: Browser status diagnostics cover profile attach mode, CDP reachability, browser HTTP errors, and browser CLI status.
- `cron_automation`: The fix targets detached cron.run --force behavior and cron service operations.
- `queueing`: Cron force-runs move to a separate CronManual command lane to avoid blocking work enqueued on the Cron lane.
- `reliability`: The PR fixes fallback failures and a cron self-deadlock/timeout, improving recovery from broken tooling states.

## openclaw-openclaw-42122 — Speed up install smoke Docker builds

- labels: `packaging_deployment, tests_ci`
- `packaging_deployment`: Changes Dockerfile build behavior and Docker image build arguments to skip the UI build for smoke images.
- `tests_ci`: Updates the GitHub install-smoke workflow to speed CI smoke Docker builds.

## openclaw-openclaw-42408 — [Bug/Docs]: local+hybrid memory_search quality can appear unstable due to extraPaths path drift + benchmark-file contamination

- labels: `memory, config, docs`
- `memory`: Issue is about memory_search/index retrieval quality, local memory provider, hybrid search, indexed corpus contamination, and retrieval ranking.
- `config`: Root cause centers on configured extraPaths drifting from the active workspace and requests better diagnostics for path alignment/exclusion settings.
- `docs`: Request explicitly asks for memory index/search documentation covering path hygiene and benchmark contamination pitfalls.

## openclaw-openclaw-42425 — fix(hooks): load workspace hooks for non-default agents

- labels: `hooks, gateway, sessions`
- `hooks`: PR directly changes the hooks loader to load workspace-local hooks for each configured agent workspace and scope hook handlers.
- `gateway`: The fix runs at gateway startup and modifies server-startup behavior for the gateway:startup hook loading path.
- `sessions`: Workspace hook scoping depends on event session keys and session-to-agent/workspace resolution, with regression tests for session-based isolation.

## openclaw-openclaw-42606 — Browser: harden noVNC bootstrap headers

- labels: `browser_automation, security, api_surface`
- `browser_automation`: Changes are in the browser bridge noVNC bootstrap route for the sandbox observer browser flow.
- `security`: PR explicitly hardens CSP, nosniff, frame-deny, nonce handling, and token-gated redirect safety.
- `api_surface`: Modifies HTTP response headers and contract for the `/sandbox/novnc` endpoint.

## openclaw-openclaw-43416 — feat(ui): add copy button for assistant messages

- labels: `ui_tui`
- `ui_tui`: Adds a hover-triggered copy button and visual feedback in the chat message UI.

## openclaw-openclaw-43564 — [Feature Request] ACP Session Skill Context Injection

- labels: `acp, sessions, skills_plugins, security`
- `acp`: Feature explicitly targets ACP runtime sessions via `sessions_spawn(runtime="acp")` and ACP agents.
- `sessions`: Request is about injecting context when spawning ACP session contexts and affects session state.
- `skills_plugins`: Central feature is rendering and injecting OpenClaw skills, SKILL.md, and skill lists into agent prompts.
- `security`: Expected behavior explicitly requires maintaining isolation so skills do not grant OpenClaw-only tools, and the issue is marked for security review.

## openclaw-openclaw-44379 — fix(pi-runner): harden context-overflow recovery with one suppress-hook retry

- labels: `agent_runtime, hooks, memory, reliability`
- `agent_runtime`: The fix is in the embedded PI runner run loop and attempt lifecycle for overflow recovery.
- `hooks`: Central behavior is a final retry with prompt-hook context injection suppressed.
- `memory`: The overflow is attributed to external memory/prompt-hook context injections, including memory-core involvement.
- `reliability`: It hardens recurring context-overflow recovery with a bounded retry to reduce hard failures and stalls.

## openclaw-openclaw-45200 — fix(subagents): notify user on announce give-up instead of silently dropping result

- labels: `agent_runtime, notifications, reliability`
- `agent_runtime`: The fix is in subagent registry/resumeSubagentRun and handles subagent completion announce give-up behavior.
- `notifications`: Adds last-resort notifyAnnounceGiveUp to deliver a user-visible completion/failure notice instead of silently dropping it.
- `reliability`: Addresses retry-limit exhaustion and silent result loss with best-effort recovery and audit logging.

## openclaw-openclaw-45393 — fix(errors): friendly message and last-message repair for tool_use/tool_result mismatch (#45385)

- labels: `tool_calling, reliability, sessions, security`
- `tool_calling`: Core fix handles Anthropic `tool_use`/`tool_result` mismatch and dangling tool-call blocks.
- `reliability`: Repairs timeout/race/last-message edge case that caused rejected conversations and raw errors.
- `sessions`: User-facing error and repair concern session history, fresh sessions, and resume/last-message state.
- `security`: PR also hardens inbound media reads with untrusted-data wrapping to prevent prompt injection.

## openclaw-openclaw-45508 — [Feature]: Self-hosted STT/TTS provider support in webchat (Route webchat TTS through the gateway instead of browser Speech API)

- labels: `self_hosted_inference, chat_integrations, gateway, config`
- `self_hosted_inference`: Feature is explicitly about self-hosted STT/TTS providers such as Speaches, Kokoro, and Whisper-compatible endpoints.
- `chat_integrations`: The affected surface is webchat, including Read aloud and mic voice input behavior.
- `gateway`: Core proposal is to route webchat TTS/STT through OpenClaw gateway endpoints instead of browser speech APIs.
- `config`: Issue centers on honoring existing messages.tts config and proposed or existing STT/audio transcription config paths.

## openclaw-openclaw-45841 — [Feature]: Sandboxing + ACP

- labels: `acp, sandboxing, security, sessions`
- `acp`: Issue is explicitly about allowing sandboxed OpenClaw sessions to spawn and control ACP sessions.
- `sandboxing`: Central problem is Docker/container sandbox compatibility and preserving process isolation.
- `security`: Motivation is reducing blast radius, preserving security boundaries, and using auditable opt-in bridging.
- `sessions`: Feature concerns sandboxed sessions spawning ACP sessions via sessions_spawn and related session execution modes.

## openclaw-openclaw-46552 — docs(queue): clarify steer behavior with partial streaming and tool boundaries

- labels: `docs, queueing, tool_calling`
- `docs`: PR only changes docs/concepts/queue.md to add and expand explanatory documentation.
- `queueing`: Central content documents queue steer behavior, followup fallback, per-session overrides, and queue troubleshooting.
- `tool_calling`: Docs explicitly clarify steer behavior at tool boundaries: in-flight tool calls run to completion before injected messages take effect.

## openclaw-openclaw-46740 — ACP: classify silent acpx exits as backend unavailable

- labels: `acp, acpx, reliability`
- `acp`: Changes ACP runtime/control-plane error codes and user-facing ACP error text for backend failures.
- `acpx`: Explicitly handles silent non-zero exits from the acpx backend in extensions/acpx.
- `reliability`: Reclassifies silent backend exits as unavailable to improve availability/failure handling and fallback guidance.

## openclaw-openclaw-47083 — fix: respect totalTokensFresh flag to avoid showing stale token counts

- labels: `sessions, telemetry_usage, ui_tui`
- `sessions`: The fix concerns session rows/session info and how session token state is represented and displayed.
- `telemetry_usage`: Central behavior is gating displayed total token counts using the totalTokensFresh flag to avoid stale usage data.
- `ui_tui`: Changes affect both TUI and Web UI presentation of session token counts.

## openclaw-openclaw-47187 — fix(ui): reset transient chat overlays and style context notice

- labels: `ui_tui`
- `ui_tui`: PR explicitly fixes Control UI chat styling and transient overlay state in web UI chat files.

## openclaw-openclaw-47243 — feat(ui): add timestamp and preview to session list

- labels: `sessions, ui_tui`
- `sessions`: Feature changes the session list rows, adding last-message preview and timestamp data for sessions.
- `ui_tui`: Primary change is web UI rendering of session timestamps and previews in the session list.

## openclaw-openclaw-47446 — fix(gateway/discord): respect env proxy vars and prevent ECONNRESET

- labels: `chat_integrations, config, gateway, reliability`
- `chat_integrations`: PR specifically fixes Discord gateway REST and WebSocket behavior in the Discord extension.
- `config`: Core change makes Discord proxy handling respect env proxy variables and fallback when no explicit channels.discord.proxy is configured.
- `gateway`: Gateway startup bootstraps the global Undici proxy dispatcher and the PR is scoped to gateway/Discord runtime behavior.
- `reliability`: Fixes timeouts and ECONNRESET failures from local proxies by disabling keepAlive and honoring proxy settings.

## openclaw-openclaw-48260 — feat(ui): add active time summary to usage overview

- labels: `telemetry_usage, ui_tui`
- `telemetry_usage`: Adds usage overview metrics for total active time and average session duration, using usage/session duration data.
- `ui_tui`: Feature is explicitly a web UI Usage page/Usage Overview card display change.

## openclaw-openclaw-48406 — Docs: add saturated session recovery guide

- labels: `docs, memory, sessions`
- `docs`: PR is explicitly a docs change adding a saturated-session recovery guide and updating reference docs.
- `sessions`: Central subject is saturated session recovery, compaction, recommend-reset, transcripts, and session reset handling.
- `memory`: The recovery/compaction documentation covers memory flush and durable memory behavior around saturated sessions.

## openclaw-openclaw-48580 — Bug: acpx codex sessions 创建的会话立即退出 - stdin is not a terminal

- labels: `acpx, codex, sessions, reliability`
- `acpx`: Issue is triggered by `acpx codex sessions new` and describes ACPX spawning/handling of the Codex agent.
- `codex`: The failing backend is Codex CLI, with a TTY requirement causing immediate exit.
- `sessions`: Central symptom is incorrect session state: `closed: false` and a PID recorded after the process has exited.
- `reliability`: Bug concerns stale state, process liveness detection, and cleanup/auto-closing after an immediate exit.

## openclaw-openclaw-48606 — fix: macOS default browser detection fallback to known paths

- labels: `browser_automation, reliability`
- `browser_automation`: Changes browser extension code for detecting default Chromium browser executables on macOS.
- `reliability`: Adds fallback path resolution when osascript/defaults browser detection fails, improving recovery from detection failures.

## openclaw-openclaw-48851 — feat(status): add API call count to session status and usage footer

- labels: `sessions, telemetry_usage, ui_tui`
- `sessions`: PR persists per-run callCount on session entries and reads it for current-turn session status.
- `telemetry_usage`: Adds usage reporting for API call counts alongside tokens/cost in status and response usage footer.
- `ui_tui`: User-visible /status output and response usage footer display the new call count.

## openclaw-openclaw-48877 — feat(telegram): add multi-level menu support to customCommands

- labels: `chat_integrations, config`
- `chat_integrations`: The PR is explicitly for the Telegram extension, adding inline keyboard menu handling for Telegram custom commands.
- `config`: It extends Telegram customCommands schema/types with new declarative menus and routes configuration fields.

## openclaw-openclaw-48940 — ACP: add gateway-owned node-backed runtime

- labels: `acp, gateway, agent_runtime, sessions, reliability`
- `acp`: The PR explicitly adds a node-backed ACP runtime, ACP store, ACP worker events, and ACP protocol/runtime docs.
- `gateway`: Gateway is the owner of durable state, ingests worker events, controls node work, and performs replay/recovery.
- `agent_runtime`: Adds a node-backed execution worker path, node-host bridge, run lifecycle handling, and runtime orchestration.
- `sessions`: The new ACP store persists sessions and runs, with replay/resume state and terminal session state handling.
- `reliability`: Central changes harden restart, replay, reconnect, cancel, close races, startup recovery, leases, and crash recovery.

## openclaw-openclaw-49310 — fix: keep tui busy during follow-up waits

- labels: `sessions, ui_tui`
- `sessions`: The fix detects and restores state from a sessions_yield follow-up marker in final messages and session history.
- `ui_tui`: The central behavior is keeping the TUI visibly busy with an awaiting follow-up activity state.

## openclaw-openclaw-49502 — feat(gateway): include usage/cost metadata in agent.wait terminal response

- labels: `gateway, api_surface, telemetry_usage`
- `gateway`: Change is in gateway server methods and targets the `agent.wait` gateway response paths.
- `api_surface`: Adds an optional `meta` field to the `agent.wait` WebSocket terminal response contract.
- `telemetry_usage`: Metadata contains token usage, last-call usage, estimated USD cost, provider, and model for reporting.

## openclaw-openclaw-50054 — fix(acp): add distributed session locking with fail-closed redis fallback

- labels: `acp, sessions, reliability`
- `acp`: PR explicitly modifies ACP dispatch flow and ACP execution locking.
- `sessions`: Core change is distributed locking keyed to ACP sessions/session keys.
- `reliability`: Adds fail-closed Redis behavior plus acquire/release/renew safeguards to prevent concurrent or unsafe execution.

## openclaw-openclaw-51849 — Docs: add freeCodeCamp OpenClaw full tutorial to showcase

- labels: `docs, agent_demos`
- `docs`: Single-file documentation change in docs/start/showcase.md adding a tutorial entry.
- `agent_demos`: Adds a freeCodeCamp tutorial/showcase video to the OpenClaw in Action showcase section.

## openclaw-openclaw-52249 — ACP parent session stuck until refresh when yielded waiting for child completion

- labels: `acp, sessions, queueing, reliability`
- `acp`: Issue is explicitly about ACP parent/child session behavior, ACP relay code, and ACP yield/resume handling.
- `sessions`: Core failure is parent session state and resume behavior after a child session completes.
- `queueing`: Fix routes child-completion follow-ups through enqueueSystemEvent and the heartbeat wake scheduler.
- `reliability`: Addresses a wedged/stuck non-responsive parent session that only recovers after manual refresh.

## openclaw-openclaw-53319 — [Bug]: ACP concurrent session spawns — first agent fails to launch CC process

- labels: `acp, acpx, sessions, reliability`
- `acp`: Issue explicitly uses ACP session spawning via `sessions_spawn runtime:"acp"`.
- `acpx`: Environment and analysis identify the ACP backend as `acpx` and suspect the acpx CLI launch path.
- `sessions`: Bug concerns concurrent child session spawns, accepted session keys, and session initialization state.
- `reliability`: Reports a race/stall where the first agent silently fails to launch or crashes during concurrent initialization.

## openclaw-openclaw-54471 — fix(acp): add system_event stream relay to parent session for ACP spawn

- labels: `acp, sessions, notifications`
- `acp`: The fix is explicitly for ACP spawn and ACP session stream handling.
- `sessions`: It relays spawned ACP session system events to the parent session when using sessions_spawn with streamTo parent.
- `notifications`: The bug caused clarifying questions and progress updates to not be delivered or shown to users.

## openclaw-openclaw-55790 — sessions_spawn(runtime="subagent") ignores inherited/per-agent subagent thinking defaults and initializes children at low

- labels: `agent_runtime, config, sessions`
- `agent_runtime`: Bug is in spawning subagents with runtime="subagent" and resolving child agent runtime behavior.
- `config`: Core failure is inheritance/default resolution from agents.list[].subagents.thinking and thinkingDefault config fields.
- `sessions`: Issue centers on sessions_spawn, parent/child sessions, and child session state initializing with the wrong thinking level.

## openclaw-openclaw-56442 — feat: Add opt-in ACP parent completion notify for sessions_spawn

- labels: `acp, sessions, notifications, api_surface`
- `acp`: PR explicitly changes ACP `sessions_spawn` behavior for ACP `mode:"run"` spawns.
- `sessions`: Core behavior concerns parent/requester and child session completion reporting via `sessions_spawn`.
- `notifications`: Adds opt-in `parentUpdates:"notify"` to route terminal completion through announce/completion delivery.
- `api_surface`: Introduces a new request/schema parameter and documents its contract for `sessions_spawn`.

## openclaw-openclaw-56532 — memory-lancedb: add configurable timeout/retry for embedding calls

- labels: `memory, config, reliability`
- `memory`: The change is in the memory-lancedb extension and affects embedding calls used for memory auto-recall.
- `config`: Adds configurable embedding.timeoutMs and embedding.maxRetries fields with schema and manifest validation.
- `reliability`: Bounds hung or storming embedding backends with timeout/retry behavior to avoid stalled agent turns and cascading failures.

## openclaw-openclaw-56613 — [Feature]: Talk/Voice tab — agent/session switching + per-agent TTS voice

- labels: `config, sessions, ui_tui`
- `config`: Requests per-agent TTS voice settings via agents.list[].tts overriding global TTS configuration.
- `sessions`: Voice/Talk tab is hardcoded to the main session and should route to the selected agent/session.
- `ui_tui`: Feature is about the mobile/macOS Talk/Voice tab adding an agent/session picker similar to Chat.

## openclaw-openclaw-57597 — fix(acp): persist spawn labels in target session store

- labels: `acp, sessions, reliability`
- `acp`: The fix is for `/acp spawn ... --label` behavior and ACP session follow-up commands.
- `sessions`: The bug concerns writing spawned session labels to the correct target session store using the spawned `sessionKey`.
- `reliability`: It fixes a state-persistence bug where cross-agent spawns silently lost labels and broke later resolution.

## openclaw-openclaw-58411 — sessions_spawn lacks --bind here equivalent — agent cannot bind ACP session to existing Discord thread

- labels: `acp, sessions, chat_integrations, api_surface`
- `acp`: Issue is about ACP session spawning and `/acp spawn --bind here` semantics.
- `sessions`: Central request is binding a spawned session to an existing current thread rather than creating a new session thread.
- `chat_integrations`: The affected UX is explicitly in an existing Discord thread.
- `api_surface`: Proposes adding a `bindTo: "current"` option to the programmatic `sessions_spawn` request contract.

## openclaw-openclaw-59208 — fix(status): honor selected usage auth profile

- labels: `auth_identity, telemetry_usage, ui_tui`
- `auth_identity`: Fix centers on OAuth profile selection and honoring a session authProfileOverride for credential resolution.
- `telemetry_usage`: The bug affects provider usage/quota resolution and the usage line shown by /status.
- `ui_tui`: The visible affected surface is the /status status card/text, where auth and usage lines were inconsistent.

## openclaw-openclaw-59878 — Session lane stuck in 'running' after run dies — sessions.abort + gateway restart fail to clear stale state

- labels: `sessions, gateway, queueing, reliability`
- `sessions`: Issue centers on session lanes, session status stuck as running, sessions.abort, and sessions.send recovery.
- `gateway`: Gateway restart and gateway logs/calls are central to the stale-state failure and expected reconciliation.
- `queueing`: New messages queue indefinitely behind a dead session-lane lock, with lane wait and queueAhead evidence.
- `reliability`: Stale running state after dead runs, missing cleanup, restart persistence, timeout, and auto-recovery are reliability failures.

## openclaw-openclaw-60381 — browser tool: add force parameter for click and expose evaluate action

- labels: `browser_automation, api_surface, security`
- `browser_automation`: Issue is explicitly about the Playwright-based browser tool click behavior and adding page evaluation.
- `api_surface`: Proposes adding a new click parameter and exposing an evaluate action, changing the browser tool action contract/routing.
- `security`: Discusses blocked javascript: navigation as an unsafe vector and gated arbitrary page.evaluate execution.

## openclaw-openclaw-60737 — [Feature]: Per-DM/per-chat default ACP binding for auto-spawning ACP sessions on new topics

- labels: `acp, chat_integrations, config, sessions`
- `acp`: Feature is explicitly about default ACP bindings and auto-spawning ACP sessions via /acp behavior.
- `chat_integrations`: Scope is Telegram DM/group chat forum topics and routing messages within those chats.
- `config`: Proposes new defaultAcp options in TelegramDirectConfig/TelegramGroupConfig with override behavior.
- `sessions`: Core behavior creates and binds ACP sessions to new topics/threads for later message routing.

## openclaw-openclaw-60979 — feature: sessions_spawn ACP delivery to channel (stream output to Zulip/Discord topic)

- labels: `acp, sessions, chat_integrations, notifications`
- `acp`: Issue explicitly targets `sessions_spawn` for `runtime="acp"` and ACP session output behavior.
- `sessions`: Core feature is spawning a session and binding its output to a conversation/topic.
- `chat_integrations`: Requested delivery target is a Zulip/Discord channel conversation or topic via channel plugins.
- `notifications`: Proposes a `delivery.mode: "announce"` option to route outbound session output to chat.

## openclaw-openclaw-61775 — enhance Makefile with standard build, test, and quality targets

- labels: `packaging_deployment, tests_ci`
- `packaging_deployment`: Makefile adds build, rebuild, clean-dist, deps, pnpm install, UI build, and developer workflow targets.
- `tests_ci`: Makefile adds test, test-fast, test-coverage, scoped test targets, and quality gates like check, lint, format, and typecheck.

## openclaw-openclaw-62428 — test(exec): land exec v2 contract follow-through

- labels: `exec_tools, approvals, security, tests_ci`
- `exec_tools`: Exec V2, command contracts, allowlist matching, safeBins, and script/interpreter command handling are central.
- `approvals`: Exec approval allowlist/effective policy and allow-always behavior are explicitly tested and documented.
- `security`: Safe bin trust, rejected bins, mutable trusted-dir filtering, audits, and command-contract hardening are security-boundary changes.
- `tests_ci`: The PR is explicitly a test-focused contract follow-through with many new exec/security test files.

## openclaw-openclaw-62552 — fix(acp): stabilize bridge session keys

- labels: `acp, sessions, queueing, reliability`
- `acp`: PR is explicitly a fix(acp) and changes ACP translator behavior for bridge fallback sessions and pending ACP prompts.
- `sessions`: Central change stabilizes session keys, raw/canonical session-key matching, and terminal child session handling.
- `queueing`: Task registry maintenance updates task state by marking active cron/cli/subagent tasks lost when backing child sessions are terminal.
- `reliability`: Fix prevents hangs/failures and stale live tasks caused by session-key collisions and terminal child sessions.

## openclaw-openclaw-62769 — [Feature]: Support ACP configured bindings for Telegram DMs (not just groups/topics)

- labels: `acp, chat_integrations, sessions`
- `acp`: Issue is explicitly about Telegram bindings with type "acp" routing to ACP harness sessions.
- `chat_integrations`: The affected surface is Telegram DM versus group/topic message routing.
- `sessions`: Feature requires persistent ACP sessions to be created or resumed for Telegram DM conversations.

## openclaw-openclaw-63007 — Pass outbound session identity into message_sending and surface guarded gateway send denial

- labels: `gateway, hooks, notifications, sessions`
- `gateway`: PR explicitly fixes the `gateway call send` path and surfaces guarded send denial from the gateway handler.
- `hooks`: Core change passes identity into the `message_sending` hook context and updates hook mappers/types.
- `notifications`: Changes the outbound message delivery path, including delivery cancellation and delivery result reporting.
- `sessions`: Adds outbound session identity fields such as `agentId` and `sessionKey` through delivery and hook contexts.

## openclaw-openclaw-63229 — Bug: Gateway falsely marks healthy local vLLM endpoints as timed out/overloaded, causing 1–23 min fallback cascades

- labels: `gateway, local_models, model_serving, reliability`
- `gateway`: Issue centers on gateway fallback/routing and gateway timeouts, including sessions_spawn via the gateway.
- `local_models`: Healthy local vLLM endpoints running Gemma/Qwen on dedicated GPUs are falsely treated as unavailable.
- `model_serving`: vLLM endpoint health, request routing, failover, and overload/timeout classification are central.
- `reliability`: Bug involves false timeouts, unresponsive gateway symptoms, long fallback cascades, and retry/failover misclassification.

## openclaw-openclaw-64181 — fix(hooks): reject error responses from slug generator and strip post-truncation dashes

- labels: `hooks, memory, reliability`
- `hooks`: Title and changed files are in src/hooks/llm-slug-generator, fixing hook slug-generation behavior.
- `memory`: Bug produced malformed memory filenames and fragmented session memory paths.
- `reliability`: Rejects failure/error payloads and fixes truncation cleanup to prevent bad slug output from runtime failures.

## openclaw-openclaw-64199 — [Bug]: ACP configured binding uses parent channel ID for session key — all threads under same channel share one persistent Claude Code process

- labels: `acp, acpx, sessions, chat_integrations, security`
- `acp`: Bug is explicitly limited to runtime.type "acp" configured bindings and ACP session-key construction.
- `acpx`: The faulty key maps to the same acpxRecordId and acpx state record/directory.
- `sessions`: Core failure is session-key granularity causing Discord threads to share one persistent session/process.
- `chat_integrations`: The affected binding is for Discord channels and threads.
- `security`: Cross-thread context contamination exposes one thread's conversation history to another.

## openclaw-openclaw-64718 — fix(security): default exec to deny for non-owner auto-reply senders

- labels: `security, exec_tools, approvals, auth_identity`
- `security`: PR explicitly hardens a security boundary against prompt-injection-triggered arbitrary command execution.
- `exec_tools`: Change is centered on exec tool overrides/defaults such as exec security, host, ask, and node.
- `approvals`: The bug involved ask="off" removing the approval gate; the fix defaults non-owners to ask="always".
- `auth_identity`: Behavior now depends on senderIsOwner, distinguishing owner from non-owner or unauthenticated channel senders.

## openclaw-openclaw-65187 — test: add regression tests for <final> tag stripping in UI message extraction

- labels: `tests_ci, ui_tui`
- `tests_ci`: PR is explicitly test-only, adding regression cases in a .test.ts file and reporting UI tests pass.
- `ui_tui`: Tests target Control UI chat message extraction and stripping tags from the UI chat surface.

## openclaw-openclaw-65242 — fix: CompletionDeliveryGate to prevent duplicate ACP completion delivery

- labels: `acp, agent_runtime, sessions, notifications, reliability`
- `acp`: The PR explicitly targets duplicate ACP completion delivery and ACP child-session silent wakes.
- `agent_runtime`: It coordinates subagent/ACP completion lifecycle paths across task registry, announce flow, farewell hook, and heartbeat wake.
- `sessions`: The gate keys and behavior depend on owner/requester/child session keys and parent-child session completion handling.
- `notifications`: The core fix prevents multiple user-visible completion banners, announces, and farewell deliveries.
- `reliability`: First-writer-wins gating addresses duplicate delivery, stale replays, and race conditions between competing paths.

## openclaw-openclaw-65364 — feat(plugins): add registerProviderRuntimeAuthOverride API

- labels: `api_surface, auth_identity, security, skills_plugins`
- `api_surface`: Adds a new public SDK API, registerProviderRuntimeAuthOverride, with documented request/result types and semantics.
- `auth_identity`: Feature lets plugins supply runtime provider credentials, API keys, OAuth/token modes, and auth availability signals.
- `security`: Change crosses an auth-provider security boundary with credential handling, validation, reentrancy guard, and error logging concerns.
- `skills_plugins`: The API is exposed through the plugin SDK/registry for external plugins to register provider auth overrides.

## openclaw-openclaw-65640 — fix(acp): persistent session recovery for --bind here sessions

- labels: `acp, acpx, sessions, reliability`
- `acp`: PR explicitly fixes ACP control-plane/session behavior and ACP error handling for `/acp spawn --bind here` and `/acp model`.
- `acpx`: The failure mode is an ACPX backend losing a session, with recovery using ACPX backend session metadata.
- `sessions`: Central change is persistent session resume/recovery, stale binding cleanup, and session key handling for bound sessions.
- `reliability`: Adds retry and stale-state cleanup to recover from backend restart, eviction, and missing-session errors.

## openclaw-openclaw-66000 — fix(cli): clear conflicting OPENCLAW_LAUNCHD_LABEL when --profile is provided

- labels: `config, gateway, packaging_deployment`
- `config`: Central change updates CLI profile environment handling for OPENCLAW_LAUNCHD_LABEL when --profile is explicit.
- `gateway`: Bug affects gateway status resolving the wrong launch agent plist from an inherited gateway process label.
- `packaging_deployment`: Launchd labels and LaunchAgents plist resolution are service-manager/deployment behavior.

## openclaw-openclaw-66125 — [Bug]: openai-completions fallback candidate is selected, but fallback does not complete successfully through an OpenAI-compatible proxy

- labels: `local_model_providers, model_serving, reliability`
- `local_model_providers`: Central issue is a local OpenAI-compatible provider/proxy, base URL, API mode, and fallback provider selection.
- `model_serving`: Failure concerns OpenAI-compatible /v1/models and /v1/chat/completions request-shape/streaming compatibility through the proxy.
- `reliability`: Regression where selected fallback provider fails to complete and falls through without sufficient diagnostics.

## openclaw-openclaw-66327 — feat(msteams): implement sendPayload for interactive approval cards

- labels: `chat_integrations, approvals, notifications`
- `chat_integrations`: Implements MS Teams channel outbound behavior for interactive messages.
- `approvals`: Approval prompts are rendered as Approve/Deny Adaptive Card buttons sending /approve commands.
- `notifications`: Changes outbound message delivery so interactive approval payloads are sent instead of plain text fallbacks.

## openclaw-openclaw-67244 — Explicit ACP agent runs: embedded backend visibility failure and stale final JSON state after sessions_yield

- labels: `acp, acpx, agent_runtime, sessions, reliability`
- `acp`: Issue is explicitly about ACP agent runs, ACP backend lookup, and sessions_yield behavior.
- `acpx`: Failure cites the embedded ACPX runtime backend/plugin being configured in one process but not visible in another.
- `agent_runtime`: Bug is in the explicit `agent --json` embedded run path and descendant run completion reconciliation.
- `sessions`: Uses a session id and centers on stale final session state after `sessions_yield`.
- `reliability`: Reports stale liveness/final JSON state and backend visibility failures despite completed work.

## openclaw-openclaw-68187 — SSE-backed MCP sessions can stay stale after server restart and fail with 'Session not found'

- labels: `mcp_tooling, sessions, gateway, reliability`
- `mcp_tooling`: Issue is explicitly about SSE-backed MCP server/client behavior and MCP-backed tool calls.
- `sessions`: Central failure is stale client/proxy session state causing `Session not found` after restart.
- `gateway`: Observed behind the OpenClaw gateway/proxy layer, with gateway restart as the workaround.
- `reliability`: Expected fix is stale-session detection, reconnect, recovery, or invalidation after server restart.

## openclaw-openclaw-68204 — Unified run trace schema across agent, ACP, subagent, and task flows

- labels: `acp, agent_runtime, sessions, telemetry_usage`
- `acp`: The schema must cover ACP sessions and update ACP parent-child relay paths.
- `agent_runtime`: It targets main agent runs, subagents, task flows, and parent-child run orchestration.
- `sessions`: Session identity and linkage are explicit via ACP sessions, sessionKey, parentRunId, and child runs.
- `telemetry_usage`: The core request is a unified tracing/observability schema for reconstructing run timelines.

## openclaw-openclaw-68843 — fix(acp): treat missing cwd as stale bound session

- labels: `acp, sessions, reliability`
- `acp`: The fix is explicitly in ACP handling for ACP_SESSION_INIT_FAILED and ACP bound-session lifecycle code.
- `sessions`: Central behavior is stale bound ACP sessions remaining attached and needing unbind/reset cleanup.
- `reliability`: Bug fix recovers wedged conversations after missing cwd instead of repeated failures against a dead session.

## openclaw-openclaw-69260 — Harden Gemini ACP integration against ambient API-key fallback and add generic auth-contract hooks for ACP agents

- labels: `acp, auth_identity, hooks, security`
- `acp`: Issue centers on ACP-backed Gemini agent launches and generic auth contracts for ACP agents.
- `auth_identity`: Primary behavior is selecting and enforcing the intended Gemini auth mode versus API-key fallback.
- `hooks`: Requested product direction explicitly includes generic auth-contract and env-scrubbing hooks for integrations.
- `security`: Described as defense-in-depth hardening against ambient API-key credential exposure and auth drift.

## openclaw-openclaw-69328 — fix(acp): avoid false zero-diff failures and append session messages

- labels: `acp, reliability, sessions, ui_tui`
- `acp`: The PR explicitly fixes ACP control-plane behavior and ACP verification-gate handling.
- `reliability`: It prevents false zero-diff failures and changes failure handling to more graceful blocked follow-up behavior.
- `sessions`: Persistent versus oneshot ACP session behavior and appending session.message payloads are central.
- `ui_tui`: The control UI/chat transcript now appends active-run session messages with dedupe and echo replacement.

## openclaw-openclaw-69669 — ACP: keep thread-bound follow-ups parent-orchestrated by default, not raw pass-through

- labels: `acp, sessions, agent_runtime, coding_agents`
- `acp`: Issue is explicitly about ACP thread-bound follow-ups and cites sessions_spawn with runtime="acp" and an ACP child harness.
- `sessions`: Central behavior is thread-bound child session continuity, follow-ups, reactivation, and sessions.send semantics.
- `agent_runtime`: The requested change concerns parent orchestration of child-agent tasks versus raw pass-through to the child harness.
- `coding_agents`: The issue frames the problem in ACP thread-bound coding workflows where the parent expands tasks and the child executes them.

## openclaw-openclaw-70002 — ci: skip docs sync & translate-trigger workflows in forks

- labels: `tests_ci`
- `tests_ci`: Changes only GitHub Actions workflow files to add fork guards and prevent failing CI runs in forks.

## openclaw-openclaw-70529 — [Bug]: Desktop cannot use existing Chrome sessions: EasyClaw Google sign-in fails, and user profile attach fails with spawn npx ENOENT

- labels: `auth_identity, browser_automation, exec_tools, packaging_deployment`
- `auth_identity`: Google sign-in/OAuth callback for the browser relay extension fails.
- `browser_automation`: Core issue blocks attaching to existing Chrome sessions and exposing tabs for browser tool control.
- `exec_tools`: The built-in user profile attach fails while spawning the command `npx` with ENOENT.
- `packaging_deployment`: Desktop app bundle ships `node` but not `npm`/`npx`, causing the packaged-app failure.

## openclaw-openclaw-70882 — fix(bundle-mcp): coerce stringified object/array params before MCP tool calls

- labels: `mcp_tooling, tool_calling, security`
- `mcp_tooling`: The fix is in the bundled MCP materialization layer and targets MCP server validation of tool arguments.
- `tool_calling`: It coerces LLM-produced tool call arguments according to the tool inputSchema before invoking the tool.
- `security`: The final patch includes prototype-pollution and oversized-payload guards for parsed tool arguments.

## openclaw-openclaw-71157 — [Feature]: Support WhatsApp disappearing-message expiration for outbound replies

- labels: `chat_integrations, config`
- `chat_integrations`: Feature is specifically for WhatsApp outbound reply behavior and Baileys send options.
- `config`: Requests channel- and account-level configuration keys with override/default semantics.

## openclaw-openclaw-71216 — Config schema: add `sandbox`, `routing.rules`, `instances`, and `gateway.nodes.denyPaths`

- labels: `config, gateway, local_model_providers, sandboxing, security`
- `config`: The issue explicitly requests new config schema fields: sandbox, routing.rules, instances, and gateway.nodes.denyPaths.
- `gateway`: Requested fields are to be validated and enforced by the OpenClaw gateway, including multi-gateway instances and gateway node deny paths.
- `local_model_providers`: routing.rules is for tag-based provider routing in a mixed cloud/local Ollama setup with host and model selection.
- `sandboxing`: sandbox.mode is a requested global sandbox mode for tool execution and isolation behavior.
- `security`: denyPaths is intended to block reads/writes to credentials, SSH keys, and secrets regardless of tool.

## openclaw-openclaw-71487 — Web UI: add a clear TTS toggle and default voice picker in Settings

- labels: `ui_tui, self_hosted_inference, config`
- `ui_tui`: Issue explicitly requests a first-class TTS panel in the Control UI/Web UI Settings with toggles and dropdowns.
- `self_hosted_inference`: The feature is centered on TTS provider selection, voice listing, and sample playback, which falls under speech/TTS inference provider behavior.
- `config`: It asks the UI to reflect and persist TTS enablement, default provider, and default voice in the existing settings/preferences contract.

## openclaw-openclaw-71594 — docs(gateway): clarify IPv4-only BYOH bind path

- labels: `docs, gateway`
- `docs`: PR primarily updates gateway documentation, comments, and help text to clarify IPv4-only BYOH behavior.
- `gateway`: All clarified behavior concerns Gateway bind modes, customBindHost, and IPv4 sidecar/proxy guidance.

## openclaw-openclaw-71646 — mcp/channel-bridge: pendingClaudePermissions / pendingApprovals leak — no TTL, no close-clear, no cap

- labels: `mcp_tooling, approvals, reliability`
- `mcp_tooling`: Issue is explicitly about src/mcp/channel-bridge.ts and long-running openclaw mcp serve behavior.
- `approvals`: Central leak involves pendingApprovals and Claude permission requests tied to approval/request-resolution lifecycle.
- `reliability`: Reports unbounded pending-map growth due to missing TTL, close cleanup, and caps in a long-running process.

## openclaw-openclaw-71648 — fix(mcp): bound pendingClaudePermissions / pendingApprovals via TTL sweeper + close clear

- labels: `mcp_tooling, approvals, reliability`
- `mcp_tooling`: PR is explicitly under src/mcp and fixes OpenClaw MCP channel bridge/server behavior for openclaw mcp serve.
- `approvals`: Core data structures are pendingApprovals and pendingClaudePermissions, including missed approval.resolved/permission replies.
- `reliability`: Adds TTL sweeping, close cleanup, and post-close guards to prevent leaks and ghost writes in long-running processes.

## openclaw-openclaw-71784 — Bug: memory search live embedding fails ~20–40% with `fetch failed | other side closed` (provider-agnostic; upstream healthy)

- labels: `memory, reliability`
- `memory`: Issue is about live memory search, semantic recall, embeddings, vector status, and per-query embed path failures.
- `reliability`: Core bug is intermittent transient fetch/TLS/socket failures affecting 20–40% of calls despite healthy upstream providers.

## openclaw-openclaw-71803 — CLI watchdog kills sessions that are correctly idle while waiting on a Monitor task

- labels: `agent_runtime, exec_tools, reliability, sessions`
- `agent_runtime`: The issue centers on the CLI backend watchdog killing the agent process during an expected idle period.
- `exec_tools`: The idle period occurs while a Monitor tool waits on a long-running shell command such as Whisper, ffmpeg, or builds.
- `reliability`: A timeout/watchdog incorrectly terminates a healthy process, causing session failure and crash-loop style behavior.
- `sessions`: The failure destroys the in-flight agent session and forces users to reconstruct session state from logs.

## openclaw-openclaw-71930 — Mattermost plugin drops post_edited events — @mentions added via edit do not trigger agent wake

- labels: `chat_integrations, reliability`
- `chat_integrations`: Issue is specifically about the Mattermost WebSocket chat integration handling message edit events and @mentions.
- `reliability`: A supported event is silently dropped, causing message-loss and missed agent wake behavior without logging or recovery.

## openclaw-openclaw-71976 — Memory Dreaming: Light sleep sort prioritizes recency over recallCount, hiding real recall data

- labels: `memory, reliability`
- `memory`: Issue is centered on Memory Dreaming, short-term-recall data, recall counts, rehydration, and promotion behavior in the memory store.
- `reliability`: Describes bugs in sort order and search span that cause valid memory candidates to be buried or promotion to fail despite existing data.

## openclaw-openclaw-72001 — fix(hooks): write allowedSessionKeyPrefixes from gmail wizard

- labels: `hooks, gateway, config`
- `hooks`: The fix is explicitly for Gmail hook setup and hook sessionKey prefix handling.
- `gateway`: The broken emitted hook config caused the gateway hooks validator to refuse startup/restart.
- `config`: The change writes and merges the hooks.allowedSessionKeyPrefixes configuration field.

## openclaw-openclaw-72013 — ACP startup identity reconcile warns on terminal one-shot sessions

- labels: `acp, gateway, sessions`
- `acp`: Issue is explicitly about ACP startup identity reconciliation and ACP one-shot runtime sessions.
- `gateway`: The warning is emitted during gateway startup identity reconciliation.
- `sessions`: Core problem is persisted session identity metadata for terminal one-shot sessions remaining pending.

## openclaw-openclaw-72015 — Reliability: active-memory blocks replies and QMD boot initialization can overload multi-agent gateways

- labels: `gateway, memory, reliability`
- `gateway`: Issue centers on multi-agent gateway boot/restart overload, health timeouts, and degraded gateway responsiveness.
- `memory`: Active-memory and QMD memory startup/update behavior are the core mechanisms causing latency and load.
- `reliability`: Reported high CPU, long latency, timeout cascades, crash-loop impact, and need for fail-open/cancellation defaults are reliability concerns.

## openclaw-openclaw-72085 — docs(commands): document bashForegroundMs clamp bounds (0–30 000 ms)

- labels: `docs, config`
- `docs`: Docs-only PR updating configuration-reference.md with no code or behavior changes.
- `config`: Documents the accepted range and clamp behavior for the bashForegroundMs configuration key.

## openclaw-openclaw-72087 — Bug: dist/entry.js main-path breaks Codex OAuth image generation on Linux while direct runCli()/provider path succeeds

- labels: `auth_identity, codex, packaging_deployment`
- `auth_identity`: Issue centers on an openai-codex OAuth profile and auth-provider-selected image flow without an API key.
- `codex`: Explicitly involves Codex OAuth and Codex Responses backend behavior.
- `packaging_deployment`: Failure is isolated to the packaged dist/entry.js CLI main-entry/bootstrap path, while direct runCli/provider calls succeed.

## openclaw-openclaw-72133 — Feature request: per-message token/cost metadata in mobile app and channel surfaces

- labels: `telemetry_usage, ui_tui, chat_integrations`
- `telemetry_usage`: Request is to expose per-message token, cost, cache, context-window percentage, and model metadata.
- `ui_tui`: Asks to add the metadata to native mobile chat views and references existing Control UI display behavior.
- `chat_integrations`: Explicitly requests optional footers in messaging/channel surfaces such as Signal, iMessage, Telegram, and BlueBubbles.

## openclaw-openclaw-72138 — fix(feishu): emit sent hooks for normal replies

- labels: `chat_integrations, hooks, notifications`
- `chat_integrations`: The change is specifically in the Feishu channel reply dispatcher and bot paths.
- `hooks`: The PR adds canonical plugin message_sent and internal message:sent hook emission for normal replies.
- `notifications`: It fixes sent-message handling for successful and failed outbound Feishu replies.

## openclaw-openclaw-72262 — docs: add WhatsApp 408 disconnect troubleshooting runbook

- labels: `chat_integrations, docs, reliability`
- `chat_integrations`: The runbook is specifically for the WhatsApp channel integration and WhatsApp Web/Baileys disconnect behavior.
- `docs`: The issue explicitly requests documentation updates in WhatsApp and channel troubleshooting docs.
- `reliability`: The documented failure mode is repeated 408 disconnect/reconnect loops with recovery guidance.

## openclaw-openclaw-73910 — BUG: OpenClaw-managed Codex ACP uses isolated CODEX_HOME without auth bridge and sends unsupported timeout config

- labels: `acp, acpx, auth_identity, codex, config`
- `acp`: Failure is in managed Codex ACP sessions and an ACP session/set_config_option rejection.
- `acpx`: The repro compares direct ACPX to Codex with the OpenClaw-managed ACPX path.
- `auth_identity`: Central bug is isolated CODEX_HOME lacking Codex authentication and needing an auth bridge/setup path.
- `codex`: The affected external runtime is explicitly Codex ACP / Codex adapter.
- `config`: Codex rejects an unsupported timeout config option sent by OpenClaw/plugin defaults.

## openclaw-openclaw-74305 — [Bug]: ACPX Codex worker fails when model/thinking overrides are configured

- labels: `acpx, acp, codex, reliability`
- `acpx`: Issue explicitly concerns the ACPX plugin path and ACPX Codex command behavior.
- `acp`: Failure occurs in an ACP worker spawned via sessions_spawn with runtime "acp" and reports an ACP_TURN_FAILED error.
- `codex`: The affected backend is codex-acp/Codex CLI with Codex model and reasoning overrides.
- `reliability`: Bug is a crash/failure path: worker exits with AcpRuntimeError/Internal error and no child transcript is created.

## openclaw-openclaw-74484 — Gateway pairing scope deadlock: CLI cannot approve/reject auto-reissued over-scoped repair requests

- labels: `auth_identity, gateway, reliability`
- `auth_identity`: Core issue is device pairing, token scopes, and inability to approve/reject scope-upgrade repair requests.
- `gateway`: Failures occur through gateway control-plane method-scope checks and gateway pairing enforcement.
- `reliability`: Describes a deadlock/recovery failure with auto-reissued pending requests and no bootstrap path.

## openclaw-openclaw-75657 — fix: local GGUF embedding model warmup blocks Node.js event loop for minutes on startup (ARM64/Pi)

- labels: `gateway, local_models, memory, reliability`
- `gateway`: The bug occurs during Gateway startup and leaves Gateway/WebSocket/status/TUI unreachable until ready.
- `local_models`: A local GGUF embedding model loaded via node-llama-cpp on ARM64/Pi is the central cause.
- `memory`: The failing path is `memorySearch.provider: "local"` and local memory embeddings initialization/search.
- `reliability`: The issue is a startup/event-loop blocking reliability failure causing timeouts and liveness warnings.

## openclaw-openclaw-77694 — [Bug]: acpx flow run ACP node outputs return empty strings instead of agent replies

- labels: `acpx, acp, agent_runtime, reliability`
- `acpx`: Issue is explicitly about `acpx flow run`, `acpx/flows`, and ACPX flow output capture.
- `acp`: The failing node is an ACP node created with `acp(...)`, and ACP node outputs are empty.
- `agent_runtime`: The bug occurs during a flow-run agent execution where agent replies should be captured as node outputs.
- `reliability`: A completed run returns incorrect empty outputs instead of agent replies, indicating an unreliable output-capture failure.

## openclaw-openclaw-77748 — fix: Codex startup plugins + WhatsApp history & Docker Codex OAuth

- labels: `auth_identity, chat_integrations, codex, packaging_deployment, skills_plugins`
- `auth_identity`: Docker/Codex OAuth callback wiring and openai-codex-auth login helper are central changes.
- `chat_integrations`: WhatsApp channel history and message-action plumbing are a major part of the PR.
- `codex`: PR explicitly fixes Codex harness startup and Codex OAuth/Docker behavior.
- `packaging_deployment`: docker-compose port/env updates and a Docker auth helper script are central deployment changes.
- `skills_plugins`: Gateway startup plugin resolution is changed so the plugin owning the configured primary model is loaded and registered.

## openclaw-openclaw-78528 — Security: skill SecretRef API keys still leak into exec child environments

- labels: `security, exec_tools, skills_plugins, auth_identity`
- `security`: Issue reports secret/API key leakage into child process environments and exfiltration risk.
- `exec_tools`: Leak occurs through commands spawned via the generic exec tool and inherited child envs.
- `skills_plugins`: The affected secrets are skill-scoped SecretRef values under skills.entries.<skill>.apiKey.
- `auth_identity`: Central concern is API key credential scope: skill-only credentials become process-wide.

## openclaw-openclaw-78919 — [Bug] ACP sessions_spawn doesn't route images to Codex's native vision like acpx codex exec does

- labels: `acp, acpx, codex, sessions`
- `acp`: The failing path is ACP `sessions_spawn` with `runtime:acp`, including ACP attachment dispatch behavior.
- `acpx`: The issue explicitly compares the ACP path against `acpx codex exec`, which correctly routes images.
- `codex`: Codex is the target agent/runtime and its native vision capability is the broken compatibility point.
- `sessions`: The bug is specifically in `sessions_spawn` and affects session-tracked delegation flow.

## openclaw-openclaw-78977 — fix(providers): skip store:false for proxy-like Responses API endpoints (#78897)

- labels: `model_serving, reliability`
- `model_serving`: Fixes Responses API payload behavior for proxy-like/OpenAI-compatible endpoints and LiteLLM-style provider compatibility.
- `reliability`: Prevents multi-turn continuation failures caused by rejected replayed response items when store:false was sent.

## openclaw-openclaw-79447 — fix(model-auth): resolve per-entry apiKey profile ID references

- labels: `auth_identity, config`
- `auth_identity`: PR fixes model provider API key auth by dereferencing stored auth profile IDs and validating credential classes.
- `config`: Change centers on models.providers.<id>.apiKey configuration entries and how configured per-provider API key references are resolved.

## openclaw-openclaw-79897 — OpenAI-compatible streaming with llama.cpp saves zero usage (stream closed before final usage chunk)

- labels: `local_models, model_serving, telemetry_usage`
- `local_models`: The issue is specifically about a local llama.cpp backend and its local streaming behavior in OpenClaw.
- `model_serving`: Core bug concerns OpenAI-compatible SSE streaming semantics and missing the final usage-only chunk from the endpoint.
- `telemetry_usage`: Impact is persisted token usage being saved as 0/0/0, breaking status context and compaction accounting.

## openclaw-openclaw-80008 — feat(plugins): expose ACP spawn and prompt in plugin runtime

- labels: `acp, api_surface, config, notifications, skills_plugins`
- `acp`: Adds `api.runtime.acp.spawn()` and `api.runtime.acp.prompt()` for ACP-backed agent session dispatch.
- `api_surface`: Introduces new typed plugin runtime API methods and parameter contracts for spawn and prompt calls.
- `config`: Adds an opt-in `allowAcpSpawn` plugin configuration gate with schema, help, and docs updates.
- `notifications`: Core motivation is channel-delivered ACP output using `deliver: true` with channel/thread/account targeting.
- `skills_plugins`: The feature is exposed through the plugin runtime/SDK namespace with plugin mocks, registry/status, and docs updates.

## openclaw-openclaw-80255 — fix #79026: active-memory recall subagent can deadlock on the main lane inside before_prompt_build

- labels: `memory, agent_runtime, queueing, reliability`
- `memory`: The fix is in the active-memory extension and specifically concerns active-memory recall.
- `agent_runtime`: The issue involves an embedded recall subagent and how it is run.
- `queueing`: The fix isolates the recall subagent onto a dedicated active-memory lane instead of re-entering the main lane.
- `reliability`: It fixes a deadlock caused by main-lane re-entry.

## openclaw-openclaw-80431 — ACPx plugin-tools MCP config test expects source path but resolver returns dist path

- labels: `acpx, mcp_tooling, tests_ci`
- `acpx`: The failing test is in extensions/acpx/src/config.test.ts and concerns embedded ACPx plugin config.
- `mcp_tooling`: The mismatch is specifically for injecting the built-in plugin-tools MCP server path.
- `tests_ci`: The issue is a pnpm test failure caused by expected versus resolved test output.

## openclaw-openclaw-80475 — test(acpx): accept built-dist MCP server resolution when dist exists

- labels: `acpx, mcp_tooling, tests_ci`
- `acpx`: The PR is explicitly scoped to extensions/acpx and ACPx config test behavior.
- `mcp_tooling`: The change concerns resolution/arguments for built-in MCP server entries in mcpServers.
- `tests_ci`: Only a Vitest test helper in config.test.ts is changed to match runtime dist-first behavior.

## openclaw-openclaw-80479 — feat(memory/embeddings): add openai-compatible provider for self-hosted servers (llama.cpp, Ollama, vLLM, TGI, LocalAI)

- labels: `local_model_providers, memory, self_hosted_inference`
- `local_model_providers`: Adds an OpenAI-compatible provider adapter with baseUrl/model/apiKey handling for local or self-hosted backends such as Ollama, vLLM, TGI, LocalAI, and llama.cpp.
- `memory`: The feature is a memory-lancedb embedding provider and updates memory embedding adapter code, tests, and docs.
- `self_hosted_inference`: Targets operators running self-hosted OpenAI-compatible embedding servers as separate HTTP inference processes.

## openclaw-openclaw-81200 — fix(acpx): strip provider API keys from child harness env

- labels: `acpx, acp, security, auth_identity`
- `acpx`: PR is explicitly in extensions/acpx and changes ACPX wrapper/runtime behavior for child harness launches.
- `acp`: The fix targets built-in ACP harness aliases and generated ACP child wrappers for Claude and Gemini.
- `security`: Core change prevents provider API keys from leaking into spawned child process environments.
- `auth_identity`: The stripped variables are provider auth credentials such as ANTHROPIC_API_KEY, GEMINI_API_KEY, and GOOGLE_API_KEY.

## openclaw-openclaw-81249 — [Feature/Bug]: Local Ollama embeddings fail when proxy is enabled (SSRF defenses ignore NO_PROXY)

- labels: `self_hosted_inference, local_models, security, config`
- `self_hosted_inference`: Issue centers on self-hosted/local Ollama embeddings and proxy bypass behavior for local inference services.
- `local_models`: Concrete local Ollama model/embedding endpoint on loopback is failing when routed through the proxy.
- `security`: Requested change affects SSRF protections, NO_PROXY stripping, and safe loopback whitelisting.
- `config`: Proposes openclaw.json proxy bypass settings and notes schema rejection of a bypass key.

## openclaw-openclaw-81488 — Harden node exec approval precheck env [AI]

- labels: `approvals, exec_tools, security`
- `approvals`: PR changes exec approval precheck analysis so node-host commands do not skip required approval based on gateway PATH.
- `exec_tools`: Central code path is node-host command execution/system.run, command allowlist matching, and PATH-based bare command resolution.
- `security`: Explicit security hardening prevents approval suppression from analyzing commands with the wrong environment.

## openclaw-openclaw-81957 — ci: harden GitHub Actions supply-chain boundaries

- labels: `security, tests_ci, auth_identity, packaging_deployment`
- `security`: PR explicitly hardens GitHub Actions supply-chain boundaries, permissions, token exposure, trusted refs, and cache/artifact trust boundaries.
- `tests_ci`: Most changes are in GitHub Actions workflows, with focused regression coverage for CI/publish boundary behavior.
- `auth_identity`: Central changes replace long-lived tokens with OIDC trusted publishing and tighten auth/permission scopes.
- `packaging_deployment`: Release and publish workflows plus npm/plugin publish scripts are core deployment and package publication plumbing.

## openclaw-openclaw-82145 — cron: allow retries for local model preflight

- labels: `cron_automation, local_model_providers, config, reliability`
- `cron_automation`: Change is specifically for isolated cron jobs and scheduled runs marked skipped after preflight.
- `local_model_providers`: Adds retryable preflight probing for local configured providers such as Ollama, vLLM, and LM Studio.
- `config`: Exposes new cron.modelPreflight timeout, maxAttempts, and retryDelayMs configuration schema/help/docs.
- `reliability`: Retries, timeouts, and delay settings address cold-start or sleeping-provider false skips.

## openclaw-openclaw-82507 — [Feature]: ACPX Codex sandbox should inherit user-installed plugins (e.g. Superpowers)

- labels: `acpx, codex, sandboxing, skills_plugins`
- `acpx`: Issue is explicitly about the ACPX Codex sandbox and ACPX background tasks.
- `codex`: Behavior depends on Codex adapter/CODEX_HOME and Codex ACP wrapper compatibility.
- `sandboxing`: Separate isolated CODEX_HOME sandbox does not inherit the user's personal Codex home.
- `skills_plugins`: Feature request centers on installed Codex plugins/skills, Superpowers, marketplaces, and plugin cache visibility.

## openclaw-openclaw-82596 — Feature/exec denylist

- labels: `exec_tools, approvals, security`
- `exec_tools`: Adds denylist behavior for model-initiated shell exec commands such as blocking curl/wget.
- `approvals`: Implements denylist as part of exec approval/security policy evaluation and prompting paths.
- `security`: Feature is a security boundary to prevent unsafe command bypasses and fail closed on malformed rules.

## openclaw-openclaw-82642 — Fix iMessage slash command acknowledgements

- labels: `chat_integrations, notifications, reliability`
- `chat_integrations`: The change is in the iMessage extension inbound processing for direct DM slash commands.
- `notifications`: It fixes delivery of slash-command acknowledgements/replies that were being suppressed by reply delivery policy.
- `reliability`: The PR corrects a real dropped-acknowledgement bug so authorized commands like /status, /new, and /restart reliably receive replies.

## openclaw-openclaw-83333 — [Bug]: Memory provider cutover to Ollama leaves production index in mixed OpenAI/Ollama vector state after live sync/reload

- labels: `memory, self_hosted_inference, reliability`
- `memory`: Issue centers on memorySearch embeddings, SQLite memory index/vector dimensions, and failed canary memory search.
- `self_hosted_inference`: The provider cutover is specifically from OpenAI embeddings to local/container Ollama embeddings for memory search.
- `reliability`: Live sync/reload leaves a mixed, inconsistent index state with stale dimensions and broken search after provider change.

## openclaw-openclaw-83982 — fix(clawhub): preserve base URL path prefix [AI-assisted]

- labels: `api_surface, config, skills_plugins`
- `api_surface`: Fixes construction of ClawHub HTTP API request URLs such as /api/v1/search while preserving a reverse-proxy path prefix.
- `config`: Behavior depends on configured base URL environment variables OPENCLAW_CLAWHUB_URL / CLAWHUB_URL and their pathname handling.
- `skills_plugins`: The affected ClawHub client functions search and interact with ClawHub skills/plugin package APIs.

## openclaw-openclaw-84094 — feat(gateway): forward frequency_penalty, presence_penalty, and seed via OpenAI-compatible HTTP gateway

- labels: `gateway, api_surface, model_serving`
- `gateway`: Title and changes center on the OpenAI-compatible HTTP gateway forwarding and validating request parameters.
- `api_surface`: Updates the POST /v1/chat/completions request contract and OpenAI-compatible 400 validation behavior.
- `model_serving`: Forwards sampling parameters like frequency_penalty, presence_penalty, and seed to upstream OpenAI-compatible provider endpoints.

## openclaw-openclaw-84297 — [Bug]: Per-agent identity overlay dropped on cron --announce and heartbeat target-channel Slack pushes (announce path; reply path was fixed in #38235)

- labels: `auth_identity, chat_integrations, cron_automation, notifications`
- `auth_identity`: The bug centers on per-agent identity/persona overlay not being applied to outbound messages.
- `chat_integrations`: The affected delivery surface is Slack, including channel posts via chat.postMessage.
- `cron_automation`: The failing paths are cron --announce jobs and heartbeat-scheduled Slack targets.
- `notifications`: The issue concerns outbound announce/heartbeat message delivery using the wrong display identity.

## openclaw-openclaw-84301 — [Bug]: Make Dream Diary narrative timeout configurable for slow/serial local model backends

- labels: `config, local_models, queueing, reliability`
- `config`: Issue asks to make a hardcoded Dream Diary narrative timeout user-configurable and proposes a config key.
- `local_models`: Failure is tied to slow/serial local model backends such as LM Studio running qwen locally.
- `queueing`: The timeout is triggered by multiple narrative runs being parallelized/queued while the backend processes them serially.
- `reliability`: Hardcoded 60s wait causes otherwise normal local runs to timeout and fail; requested change is to complete reliably.

## openclaw-openclaw-84316 — [Bug]: Telegram group TTS for sub-agent reports success in /tts status but voice never delivered (2026.5.12)

- labels: `chat_integrations, notifications, reliability`
- `chat_integrations`: Bug is specific to Telegram group chat behavior versus Telegram DM delivery.
- `notifications`: Central failure is outbound voice/TTS message delivery despite status reporting success.
- `reliability`: Reports message loss and incorrect success state for a delivery handoff without a crash.

## openclaw-openclaw-84337 — [Bug]: Hook ingress token unlocks password-mode gateway auth

- labels: `security, auth_identity, gateway, hooks`
- `security`: Issue is a high-severity auth bypass where a hook bearer token can gain full operator access.
- `auth_identity`: Central failure is password-mode Gateway authentication accepting the hook token as a password credential.
- `gateway`: Affected paths are Gateway HTTP auth utilities and Gateway HTTP surfaces such as /tools/invoke.
- `hooks`: The bypass depends on hooks.token and hook ingress bearer handling for /hooks/wake.

## openclaw-openclaw-84385 — [codex] Fix macOS app copyright year

- labels: `ui_tui`
- `ui_tui`: PR fixes the macOS app About settings UI text by updating the displayed copyright year.

## openclaw-openclaw-84418 — test(cron): document and test owner-only tool security boundary for isolated cron

- labels: `cron_automation, security, tests_ci`
- `cron_automation`: The PR is explicitly about isolated cron runs and the cron owner-only tool allowlist.
- `security`: It defines and tests a security boundary so unattended cron only auto-grants safe owner-only tools.
- `tests_ci`: It adds focused unit tests and reports vitest coverage for the owner-only allowlist behavior.

## openclaw-openclaw-84419 — fix(session): prefer real tool result over synthetic error in transcript repair

- labels: `sessions, tool_calling, reliability`
- `sessions`: The fix is in session transcript repair and affects persisted session history on reload.
- `tool_calling`: The repair logic deduplicates and pairs tool results, preferring real tool results over synthetic missing-result errors.
- `reliability`: It mitigates a flush-race/stale repair outcome that caused successful tool calls to appear as errors.

## openclaw-openclaw-84567 — [Bug]: Codex bundled harness initialize still hangs in 2026.5.18 isolated cron — surfaces via #64744 timeout-wrapping as 'isolated agent setup timed out before runner start'

- labels: `codex, cron_automation, agent_runtime, reliability`
- `codex`: The failure is explicitly tied to the bundled openai-codex harness and Codex app-server worker.
- `cron_automation`: The bug occurs in recurring/manual cron jobs with cron run/get diagnostics.
- `agent_runtime`: The reported hang is during agentTurn setup before the runner starts, i.e. agent lifecycle initialization.
- `reliability`: Core symptom is a deterministic hang/timeout regression with an idle worker and repeated failures.

## openclaw-openclaw-84570 — Remove skill prelude exec allowlist

- labels: `approvals, exec_tools, skills_plugins`
- `approvals`: PR changes exec-approval allowlist behavior so legacy skill prelude chains go through normal approval flow.
- `exec_tools`: Central code path evaluates shell command chains, exec allowlists, and trusted wrapper execution.
- `skills_plugins`: Behavior is specifically about SKILL.md, skill wrappers, skillPrelude, and autoAllowSkills.

## openclaw-openclaw-84583 — cron announce delivery triggers EmbeddedAttemptSessionTakeoverError when user is actively chatting

- labels: `cron_automation, notifications, chat_integrations, sessions, reliability`
- `cron_automation`: The failure starts when an isolated cron job finishes and runs its configured delivery.
- `notifications`: The problematic path is announce delivery sending the cron result to a user.
- `chat_integrations`: Delivery is explicitly to a Telegram channel/user while the user is actively chatting.
- `sessions`: The root cause is concurrent modification of the same Telegram session file and sessionTarget behavior.
- `reliability`: The issue is a race/lock conflict causing EmbeddedAttemptSessionTakeoverError and message/session disruption.

## openclaw-openclaw-84637 — [Bug]: Codex runtime/harness is too easy to confuse with gpt-*-codex model fallbacks

- labels: `codex, agent_runtime, config, sessions`
- `codex`: The issue explicitly concerns distinguishing Codex runtime/harness routing from Codex-named model IDs.
- `agent_runtime`: Central bug is incorrect interpretation of agentRuntime.id and runtime/harness routing between Codex and Pi.
- `config`: Observed failures mutate default model, fallback policy, provider, and model runtime configuration.
- `sessions`: The repro and impact focus on normal sessions being routed to Pi versus Codex runtime and persisted session route state.

## openclaw-openclaw-84645 — Materialize node-host inline interpreter eval before exec approval

- labels: `exec_tools, approvals, security`
- `exec_tools`: Changes node-host system.run handling for Python/Node inline eval commands and argv rewriting to script files.
- `approvals`: Core behavior occurs before exec approval planning and preserves approval binding via generated script paths.
- `security`: Focuses on fail-closed handling, stable hash-bound artifacts, private temp files, and 0600 permissions for inline eval.

## openclaw-openclaw-84648 — Add SafeOps preflight hook for exec tool

- labels: `exec_tools, hooks, security`
- `exec_tools`: PR modifies the exec tool path in bash-tools.exec.ts before command dispatch and process execution.
- `hooks`: Title and body explicitly add a SafeOps preflight hook before exec/tool execution.
- `security`: SafeOps preflight is a security-boundary policy integration involving adapter tokens, denial behavior, and secret/security review.

## openclaw-openclaw-84660 — [Bug] Voice STT: empty moonshine transcripts passed as raw JSON to LLM, clogging serialized processing queue

- labels: `chat_integrations, self_hosted_inference, queueing, reliability`
- `chat_integrations`: Bug occurs in Discord voice STT for a bot in a voice channel.
- `self_hosted_inference`: Central failure involves moonshine/sherpa-onnx speech-to-text output handling.
- `queueing`: Empty transcripts clog the serialized entry.processingQueue and block later segments.
- `reliability`: The pipeline becomes unresponsive due to stale/empty segments wasting calls and blocking processing.

## openclaw-openclaw-84668 — docs(agent-runtimes): clarify model name vs runtime routing for Codex (#84637)

- labels: `docs, agent_runtime, codex`
- `docs`: PR changes only docs/concepts/agent-runtimes.md to add explanatory warning text.
- `agent_runtime`: Clarifies runtime routing via agentRuntime.id and distinguishes runtime selection from model fallback selection.
- `codex`: Explicitly addresses Codex runtime/harness confusion with gpt-*-codex model IDs.

## openclaw-openclaw-84681 — fix(codex): stabilize heartbeat dynamic tool schema

- labels: `codex, sessions, tool_calling`
- `codex`: Title and files are explicitly in the Codex extension/app-server path.
- `sessions`: Fix preserves the same Codex thread/session across normal and heartbeat turns, preventing thread rotation.
- `tool_calling`: Central change stabilizes dynamic tool schemas and controls when heartbeat_respond is callable.

## openclaw-openclaw-84697 — Custom OpenAI-compatible provider with baseUrl without /v1 fails with cryptic 'incomplete terminal response' error

- labels: `config, model_serving, local_model_providers`
- `config`: The bug is triggered by a user-configured provider baseUrl missing the required /v1 path and asks onboarding/config guidance to catch it.
- `model_serving`: It concerns OpenAI-compatible chat completions endpoint construction, streaming parsing, and handling non-JSON/non-SSE responses from the model endpoint.
- `local_model_providers`: A custom OpenAI-compatible provider with a user-supplied baseUrl is central provider-layer setup/compatibility behavior.

## openclaw-openclaw-84709 — fix(cron): fail closed when required tools are unavailable

- labels: `codex, cron_automation, exec_tools, reliability`
- `codex`: Changes are in the Codex extension app-server path and explicitly alter Codex native/dynamic tool surface handling.
- `cron_automation`: The fix targets cron isolated-agent jobs and cron finalization behavior for scheduled runs.
- `exec_tools`: Central issue is required exec/read tool allowlists and ensuring shell/exec tools are available before dispatch.
- `reliability`: Adds fail-closed preflight and failure classification to avoid false healthy cron summaries when required tools are missing.

## openclaw-openclaw-84715 — [Bug]: @openclaw/codex peer link failure reproduced on 2026.5.19 after update

- labels: `codex, packaging_deployment, reliability, skills_plugins`
- `codex`: The failure is explicitly in @openclaw/codex and prevents the Codex harness/shared-client from starting.
- `packaging_deployment`: The bug concerns Homebrew/global install update state, managed npm dependency layout, and peer-link repair.
- `reliability`: A missing peer link causes startup failure before any assistant reply, with repair/health-state expectations to prevent recurrence.
- `skills_plugins`: The root cause is managed plugin npm-tree peer dependency resolution for the @openclaw/codex plugin.

## openclaw-openclaw-84729 — [codex] Fix macOS app copyright year

- labels: `tests_ci, ui_tui`
- `tests_ci`: Updates check-changed planning script and changed-lanes test coverage for SwiftLint/app-lint behavior.
- `ui_tui`: Changes the macOS app About settings UI copyright text.

## openclaw-openclaw-84732 — Slack channel sends fail: `reconcileUnknownSend` required but no channel adapter implements it

- labels: `chat_integrations, notifications, reliability`
- `chat_integrations`: The failure is specific to Slack channel message sends through the Slack channel adapter.
- `notifications`: The issue concerns outbound channel message delivery and durable send handling.
- `reliability`: A required durability capability is missing, causing failed sends and message-loss impact.

## openclaw-openclaw-84740 — Feature Request: Option to hide/suppress certain sessions from the session list

- labels: `sessions, ui_tui`
- `sessions`: The request centers on hiding, archiving, filtering, and auto-suppressing specific sessions in the session list.
- `ui_tui`: The requested change is a user-facing session list UX improvement with hide/archive actions and a toggle/filter.

## openclaw-openclaw-84752 — fix: self-heal lane wedges + restore openai-codex OAuth on embedded path

- labels: `auth_identity, chat_integrations, codex, queueing, reliability`
- `auth_identity`: Restores OAuth profile/sidecar token resolution in the auth profile store.
- `chat_integrations`: Changes Telegram polling-session recovery for a Telegram channel failure mode.
- `codex`: Explicitly fixes OAuth resolution for the openai-codex provider on embedded paths.
- `queueing`: Fixes per-lane command queue wedging via queueDepth checks and lane reset/pump logic.
- `reliability`: Primary theme is self-healing wedged lanes and polling failures without manual restarts.

## openclaw-openclaw-84757 — [Bug]: Telegram session can get stuck after compaction when encrypted reasoning content fails verification

- labels: `chat_integrations, sessions, reliability`
- `chat_integrations`: The bug affects Telegram direct-chat delivery and fallback behavior.
- `sessions`: The failure is tied to persisted session history replay after compaction or restore, leaving the same session unusable.
- `reliability`: It describes a stuck retry/recovery failure requiring sanitization or automatic recovery from invalid replay payloads.

## openclaw-openclaw-84763 — fix(acpx): scrub provider credential env from ACP harness spawns

- labels: `acpx, acp, auth_identity, security, config`
- `acpx`: Changes are in extensions/acpx and alter ACPX command decoration/runtime spawn behavior.
- `acp`: Bug and fix center on sessions_spawn with runtime:"acp" and ACP harness launches.
- `auth_identity`: Fixes inherited provider auth credentials/OAuth tokens causing Claude harness authentication failure.
- `security`: Scrubs provider credential environment variables from child harness processes as security hardening.
- `config`: Adds the acp.scrubProviderEnv config knob and updates config schema/metadata.

## openclaw-openclaw-84771 — Event loop saturation during startup: synchronous model-prewarm and session-locks block event loop for 28-64 seconds

- labels: `gateway, model_serving, reliability, sessions`
- `gateway`: The failure occurs during OpenClaw gateway startup and causes gateway restart cascades and startup liveness problems.
- `model_serving`: A synchronous model-prewarm startup sidecar is one of the central blocking operations, implicating model lifecycle/prewarm behavior.
- `reliability`: The issue is a reliability failure: event loop saturation, liveness warnings, heap pressure, crash loops, delayed heartbeats, and restarts.
- `sessions`: Session-lock processing and synchronous parsing of many session stores are central causes of the startup blockage.

## openclaw-openclaw-84789 — Active memory crashes on Telegram forum topic sessions (dirName validation)

- labels: `chat_integrations, memory, sessions, reliability`
- `chat_integrations`: Bug occurs specifically in Telegram forum/topic-based group chat sessions.
- `memory`: Active memory starts and then fails, blocking the active memory feature.
- `sessions`: Root cause is the Telegram forum session key with colons being reused as a directory name.
- `reliability`: This is a crash/failure mode where active memory immediately fails for all Telegram forum topic messages.

## openclaw-openclaw-84794 — Clean up isolated cron sessions after runs

- labels: `cron_automation, sessions, reliability`
- `cron_automation`: PR is specifically about isolated cron jobs and deleteAfterRun cleanup after cron runs.
- `sessions`: Core behavior deletes run-scoped cron sessions via sessions.delete and session cleanup helper.
- `reliability`: Fixes missed cleanup on delivery-none, runner errors, and other terminal paths using a finally block.

## openclaw-openclaw-84802 — fix(memory-core): allow bounded dreaming session cleanup

- labels: `memory, sessions, reliability`
- `memory`: Change is in extensions/memory-core and fixes dreaming narrative behavior in the memory-core feature.
- `sessions`: Core change reuses stable session keys and adds deleteSession cleanup for dreaming narrative sessions.
- `reliability`: Fix prevents stale session accumulation and makes cleanup bounded/idempotent with retry and failure handling tests.

## openclaw-openclaw-85999 — [Bug]: 2026.5.22 gateway pre-warm (warmCurrentProviderAuthState) blocks event loop ~60s on startup, breaks channel handshakes

- labels: `auth_identity, chat_integrations, gateway, reliability`
- `auth_identity`: The blocking startup path is explicitly `warmCurrentProviderAuthState` / provider auth state pre-warming.
- `chat_integrations`: The regression breaks Discord READY, Feishu bot info, Telegram webhook handling, and inbound chat messages.
- `gateway`: The issue is about gateway startup/restart behavior and readiness during pre-warm.
- `reliability`: Reports event-loop starvation, timeouts, liveness warnings, delayed inbound processing, and startup regression.

## openclaw-openclaw-88816 — [Bug]: v2026.05.28 breaks Google Vertex Express API Key

- labels: `auth_identity, config, model_serving`
- `auth_identity`: Issue centers on Google Vertex Express API key auth via auth-profile.json, explicitly contrasting API key vs ADC.
- `config`: Failure is tied to openclaw.json model defaults and missing models.providers["google-vertex"].models[] registration.
- `model_serving`: Error is an unknown provider model/model registration failure for google-vertex Gemini models before serving requests.

## openclaw-openclaw-90146 — google-vertex: Missing gemini-3.1-flash-lite in provider catalog causes silent failure instead of error

- labels: `config, reliability, agent_runtime, model_releases`
- `config`: Central issue is a missing/misconfigured Google Vertex static provider catalog entry for a model.
- `reliability`: The reported bug is a silent failure/no user-facing error when model_not_found has no fallback.
- `agent_runtime`: The failure path is in embedded-agent-runner and model fallback execution, causing the agent to produce no reply.
- `model_releases`: The catalog gap concerns a specific Gemini 3.1 model/version missing from supported model metadata.
