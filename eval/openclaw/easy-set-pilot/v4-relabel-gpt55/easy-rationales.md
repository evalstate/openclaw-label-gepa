# easy-set-pilot rationales

## openclaw-openclaw-40332 — [Feature]: Per-binding and per-agent permissionMode for ACP sessions

- labels: `acp, acpx, approvals, config, security`
- `acp`: Feature scopes permissionMode for ACP sessions, bindings, and per-agent ACP runtime overrides.
- `acpx`: The current global setting is explicitly under the acpx plugin config and remains the fallback.
- `approvals`: permissionMode values such as approve-all and approve-reads directly control approval/permission behavior.
- `config`: Request is for new config locations and precedence across binding, agent runtime, and global fallback.
- `security`: Core motivation is least-privilege scoping across agents with different trust levels to avoid over-provisioning access.

## openclaw-openclaw-41892 — feat(control-ui): add cron calendar timeline view

- labels: `cron_automation, ui_tui`
- `cron_automation`: Adds a timeline view for cron jobs showing scheduled tasks, high-frequency jobs, and run-history navigation.
- `ui_tui`: Implements a new Control UI Cron Jobs page visual timeline with hover popups, zoom controls, styling, and i18n strings.

## openclaw-openclaw-42027 — fix: resolve exec PATH fallback, layered browser diagnostics, and cron force-run deadlock

- labels: `exec_tools, browser_automation, cron_automation, queueing, reliability`
- `exec_tools`: Exec tool PATH recovery is changed for local fallback, affecting shell command execution behavior.
- `browser_automation`: Browser status diagnostics cover profile attach mode, CDP reachability, and browser HTTP error reporting.
- `cron_automation`: The fix targets detached cron force-runs and cron execution behavior.
- `queueing`: Cron force-runs move to a separate manual command lane to avoid blocking reuse of the cron lane.
- `reliability`: The PR fixes operational failures: missing PATH fallback diagnostics and a cron self-deadlock timeout.

## openclaw-openclaw-42122 — Speed up install smoke Docker builds

- labels: `packaging_deployment, tests_ci`
- `packaging_deployment`: Changes Dockerfile build behavior and Docker build args for smoke images.
- `tests_ci`: Updates the GitHub install-smoke workflow to speed CI smoke Docker builds.

## openclaw-openclaw-42408 — [Bug/Docs]: local+hybrid memory_search quality can appear unstable due to extraPaths path drift + benchmark-file contamination

- labels: `memory, config, docs`
- `memory`: Issue centers on memory_search/index retrieval quality, hybrid search ranking, indexed corpus contamination, and local memory store behavior.
- `config`: Root cause and mitigations involve extraPaths configuration, path alignment, exclusions, and workspace-specific setup.
- `docs`: Request explicitly asks for memory index/search documentation on path hygiene and benchmark contamination pitfalls.

## openclaw-openclaw-42425 — fix(hooks): load workspace hooks for non-default agents

- labels: `hooks, gateway, sessions`
- `hooks`: PR directly changes the internal hook loader to load workspace-local hooks and apply hook scope guards.
- `gateway`: The loading happens at gateway startup and modifies server-startup behavior for multi-agent workspaces.
- `sessions`: Hook scoping resolves event workspace using session context, including legacy session-key handling.

## openclaw-openclaw-42606 — Browser: harden noVNC bootstrap headers

- labels: `browser_automation, security, api_surface`
- `browser_automation`: Change is in the browser bridge noVNC bootstrap route for the sandbox observer.
- `security`: PR explicitly hardens the page with CSP nonce, nosniff, and frame-deny headers.
- `api_surface`: It changes HTTP response headers/contract for the /sandbox/novnc route.

## openclaw-openclaw-43416 — feat(ui): add copy button for assistant messages

- labels: `ui_tui`
- `ui_tui`: Adds a user-facing hover copy button and feedback state in the chat message UI.

## openclaw-openclaw-44379 — fix(pi-runner): harden context-overflow recovery with one suppress-hook retry

- labels: `agent_runtime, hooks, memory, reliability`
- `agent_runtime`: The fix is in the embedded PI runner run loop and retry/attempt lifecycle for context-overflow recovery.
- `hooks`: The new fallback explicitly suppresses prompt-hook context injection for one bounded retry.
- `memory`: The overflow scenario is caused by external memory/prompt context injections, with memory-core extension files involved.
- `reliability`: The PR hardens recurring context-overflow recovery to avoid hard failures and stalls.

## openclaw-openclaw-45200 — fix(subagents): notify user on announce give-up instead of silently dropping result

- labels: `agent_runtime, notifications, reliability`
- `agent_runtime`: The change is in subagent run handling, specifically the announce retry-limit branch in resumeSubagentRun.
- `notifications`: It adds a last-resort user-facing notification when a subagent result cannot be announced normally.
- `reliability`: It fixes a production failure mode where completed subagent results were silently discarded after retries were exhausted.

## openclaw-openclaw-45393 — fix(errors): friendly message and last-message repair for tool_use/tool_result mismatch (#45385)

- labels: `tool_calling, reliability, sessions, security`
- `tool_calling`: Primary fix handles Anthropic tool_use/tool_result mismatches and strips dangling tool_use blocks.
- `reliability`: Addresses timeout/race/last-message edge cases that caused rejected conversations and user-visible failures.
- `sessions`: Repairs invalid session history/transcript state and advises starting a fresh session if needed.
- `security`: Adds inbound media read wrapping, escaping, and path normalization to prevent prompt injection from untrusted files.

## openclaw-openclaw-45508 — [Feature]: Self-hosted STT/TTS provider support in webchat (Route webchat TTS through the gateway instead of browser Speech API)

- labels: `self_hosted_inference, chat_integrations, gateway, config`
- `self_hosted_inference`: The feature is explicitly about self-hosted STT/TTS speech providers such as Speaches, Whisper, and Kokoro.
- `chat_integrations`: The affected surface is webchat, including the Read aloud and mic voice controls.
- `gateway`: The requested change is to route webchat TTS/STT through the OpenClaw gateway instead of browser speech APIs.
- `config`: The issue centers on honoring openclaw.json voice configuration and discusses messages.tts and proposed STT config.

## openclaw-openclaw-45841 — [Feature]: Sandboxing + ACP

- labels: `acp, sandboxing, security, sessions`
- `acp`: The feature request is specifically about enabling ACP sessions from sandboxed OpenClaw sessions.
- `sandboxing`: The core limitation involves Docker/container sandbox boundaries blocking ACP spawning.
- `security`: The proposal centers on preserving isolation, reducing blast radius, and using audited opt-in bridge access.
- `sessions`: The requested behavior concerns sandboxed sessions spawning, steering, and canceling ACP sessions.

## openclaw-openclaw-46552 — docs(queue): clarify steer behavior with partial streaming and tool boundaries

- labels: `docs, queueing, tool_calling`
- `docs`: PR only changes docs/concepts/queue.md to add explanatory and troubleshooting documentation.
- `queueing`: The documented behavior is queue steer mode, per-session queue overrides, followup fallback, and queue troubleshooting.
- `tool_calling`: A central clarification is that steer is not a hard abort and in-flight tool calls complete before the injected message takes effect.

## openclaw-openclaw-46740 — ACP: classify silent acpx exits as backend unavailable

- labels: `acp, acpx, reliability`
- `acp`: Changes ACP runtime/control-plane error classification from generic turn failure to backend unavailable.
- `acpx`: The failure being handled is explicitly silent non-zero exits from the acpx backend process.
- `reliability`: Central concern is handling backend process disappearance/availability failures with actionable error classification.

## openclaw-openclaw-47187 — fix(ui): reset transient chat overlays and style context notice

- labels: `ui_tui`
- `ui_tui`: PR only changes Control UI chat styling and transient overlay state to fix visible chat surface artifacts.

## openclaw-openclaw-47243 — feat(ui): add timestamp and preview to session list

- labels: `sessions, ui_tui`
- `sessions`: The feature changes session list rows to request and display session metadata including updated timestamp and last-message preview.
- `ui_tui`: The main user-visible change is rendering timestamp and preview text in the session list UI.

## openclaw-openclaw-47446 — fix(gateway/discord): respect env proxy vars and prevent ECONNRESET

- labels: `chat_integrations, config, gateway, reliability`
- `chat_integrations`: The fix is specifically for Discord gateway REST/WebSocket behavior behind proxies.
- `config`: It makes gateway/Discord networking honor env proxy vars and fall back when explicit channels.discord.proxy is absent.
- `gateway`: Gateway startup bootstraps the global undici proxy dispatcher and Discord gateway plugin behavior is changed.
- `reliability`: The PR addresses timeouts and ECONNRESET from local proxies by disabling keepAlive.

## openclaw-openclaw-48260 — feat(ui): add active time summary to usage overview

- labels: `telemetry_usage, ui_tui`
- `telemetry_usage`: Adds and displays active-time and average-session-duration usage metrics in the Usage Overview.
- `ui_tui`: User-visible web UI change adding an Active Time card to the dashboard Usage page.

## openclaw-openclaw-48606 — fix: macOS default browser detection fallback to known paths

- labels: `browser_automation, reliability`
- `browser_automation`: Changes browser extension executable detection for macOS Chromium browsers used by browser automation.
- `reliability`: Adds fallback paths when default browser resolution fails, improving recovery from detection failures.

## openclaw-openclaw-48851 — feat(status): add API call count to session status and usage footer

- labels: `sessions, telemetry_usage, ui_tui`
- `sessions`: The PR persists per-run callCount on session entries and updates session usage state/types.
- `telemetry_usage`: The feature adds API call counts as usage/accounting metadata alongside tokens and cost.
- `ui_tui`: The call count is displayed in user-facing /status output and the response usage footer.

## openclaw-openclaw-48877 — feat(telegram): add multi-level menu support to customCommands

- labels: `chat_integrations, config`
- `chat_integrations`: The PR explicitly changes Telegram bot command and callback handling for inline keyboard menus.
- `config`: It extends Telegram customCommands configuration schema/types with menus and routes fields.

## openclaw-openclaw-49310 — fix: keep tui busy during follow-up waits

- labels: `sessions, ui_tui`
- `sessions`: The change detects and restores state from the sessions_yield follow-up marker in final assistant output and session history.
- `ui_tui`: The user-facing TUI busy/activity state is updated to show awaiting follow-up instead of idle.

## openclaw-openclaw-49502 — feat(gateway): include usage/cost metadata in agent.wait terminal response

- labels: `gateway, api_surface, telemetry_usage`
- `gateway`: Change is implemented in gateway server methods and modifies agent.wait gateway response behavior.
- `api_surface`: Adds an optional meta field to the user-facing agent.wait WebSocket response contract.
- `telemetry_usage`: Surfaces token usage, last-call usage, estimated cost, provider, and model metadata for runs.

## openclaw-openclaw-50054 — fix(acp): add distributed session locking with fail-closed redis fallback

- labels: `acp, sessions, reliability`
- `acp`: The change is explicitly in ACP dispatch and adds ACP execution locking around tryDispatchAcpReply.
- `sessions`: The lock is keyed to ACP sessions and controls concurrent execution for a session.
- `reliability`: Distributed locking, owner-checked release/renew, and fail-closed Redis behavior address concurrency and failure-mode reliability.

## openclaw-openclaw-53319 — [Bug]: ACP concurrent session spawns — first agent fails to launch CC process

- labels: `acp, acpx, sessions, reliability`
- `acp`: The bug is triggered through ACP session spawning with `sessions_spawn runtime:"acp"`.
- `acpx`: The configured ACP backend is explicitly `acpx`, and the analysis points to an acpx concurrent initialization race.
- `sessions`: The failure concerns rapid concurrent child session spawns, accepted child session keys, and session launch state.
- `reliability`: The reported behavior is a race/stall/silent launch failure where one process never starts under concurrency.

## openclaw-openclaw-54471 — fix(acp): add system_event stream relay to parent session for ACP spawn

- labels: `acp, sessions, notifications`
- `acp`: The fix is explicitly for ACP spawn stream handling and relays ACP system_event streams.
- `sessions`: The bug concerns events from a spawned ACP child session being relayed to the parent session via streamTo: "parent".
- `notifications`: The missing system_event relay prevents user-visible clarifying questions and progress updates from being delivered.

## openclaw-openclaw-55790 — sessions_spawn(runtime="subagent") ignores inherited/per-agent subagent thinking defaults and initializes children at low

- labels: `agent_runtime, config, sessions`
- `agent_runtime`: Bug is in subagent spawning/runtime behavior for runtime="subagent" and child agent initialization.
- `config`: Central failure is resolving configured per-agent and default subagent thinking settings.
- `sessions`: Issue concerns parent-to-child session spawning and inherited session thinking state.

## openclaw-openclaw-56532 — memory-lancedb: add configurable timeout/retry for embedding calls

- labels: `memory, config, reliability`
- `memory`: The change is in the memory-lancedb extension and affects embedding calls used by memory auto-recall.
- `config`: It adds configurable embedding.timeoutMs and embedding.maxRetries fields with validation and manifest/docs updates.
- `reliability`: The goal is to bound hung or rate-limited embedding backends to avoid stalled agent turns and cascading failures.

## openclaw-openclaw-56613 — [Feature]: Talk/Voice tab — agent/session switching + per-agent TTS voice

- labels: `config, sessions, ui_tui`
- `config`: Requests per-agent TTS voice settings via agent/workspace configuration instead of a single global voice.
- `sessions`: Core remaining request is selecting which agent/session the Talk/Voice tab routes messages to.
- `ui_tui`: Feature is explicitly for the mobile/macOS Talk/Voice tab UI adding an agent/session picker.

## openclaw-openclaw-57597 — fix(acp): persist spawn labels in target session store

- labels: `acp, sessions, reliability`
- `acp`: The fix is specifically for `/acp spawn --label` behavior and ACP follow-up commands.
- `sessions`: The core change persists spawned session labels in the correct target session store.
- `reliability`: It fixes a bug where cross-agent spawned session labels were lost, breaking later label-based resolution.

## openclaw-openclaw-58411 — sessions_spawn lacks --bind here equivalent — agent cannot bind ACP session to existing Discord thread

- labels: `acp, sessions, chat_integrations, api_surface`
- `acp`: Issue is about ACP spawn semantics and adding a programmatic equivalent to `/acp spawn --bind here`.
- `sessions`: Central behavior is binding a spawned session to an existing thread instead of creating a new session thread.
- `chat_integrations`: The affected UX is specifically binding an ACP session within an existing Discord thread.
- `api_surface`: Proposes a new `bindTo: "current"` option in the `sessions_spawn` request contract.

## openclaw-openclaw-59208 — fix(status): honor selected usage auth profile

- labels: `auth_identity, telemetry_usage, ui_tui`
- `auth_identity`: Fix centers on selecting the correct OAuth auth profile and honoring session authProfileOverride for credential resolution.
- `telemetry_usage`: The bug affects provider usage/quota resolution and the Usage line shown in status.
- `ui_tui`: The user-visible /status status card/text was internally inconsistent and is the surface being fixed.

## openclaw-openclaw-59878 — Session lane stuck in 'running' after run dies — sessions.abort + gateway restart fail to clear stale state

- labels: `sessions, gateway, queueing, reliability`
- `sessions`: The bug is stale session lane status, sessions.abort behavior, and session reset/recovery via sessions.send.
- `gateway`: Gateway restart is expected to reconcile state, and gateway logs/RPC calls are central evidence.
- `queueing`: New messages queue indefinitely behind the dead session lane lock with lane wait warnings.
- `reliability`: This is a stale-state recovery failure after runs die, requiring cleanup, timeout, or watchdog recovery.

## openclaw-openclaw-60737 — [Feature]: Per-DM/per-chat default ACP binding for auto-spawning ACP sessions on new topics

- labels: `acp, chat_integrations, config, sessions`
- `acp`: Feature is explicitly about default ACP bindings and auto-spawning ACP sessions.
- `chat_integrations`: Behavior is scoped to Telegram DMs, group chats, forum topics, and chat-thread routing.
- `config`: Proposes new Telegram config fields such as defaultAcp and override behavior.
- `sessions`: New topics are bound to newly spawned ACP sessions and subsequent messages route by that binding.

## openclaw-openclaw-60979 — feature: sessions_spawn ACP delivery to channel (stream output to Zulip/Discord topic)

- labels: `acp, sessions, chat_integrations, notifications`
- `acp`: The requested feature is specifically for `sessions_spawn` with `runtime="acp"` and ACP session output delivery.
- `sessions`: The issue centers on spawning sessions and binding spawned session output to a target instead of only the parent session.
- `chat_integrations`: The desired target is a chat channel conversation/topic such as Zulip or Discord.
- `notifications`: The proposed `delivery.mode: "announce"` routes outbound session output/announcements to a channel.

## openclaw-openclaw-61775 — enhance Makefile with standard build, test, and quality targets

- labels: `packaging_deployment, tests_ci`
- `packaging_deployment`: Makefile adds contributor build/dependency/clean/dev workflow targets delegating to pnpm scripts.
- `tests_ci`: Makefile adds test, coverage, lint, typecheck, check, and landing-gate quality targets.

## openclaw-openclaw-62428 — test(exec): land exec v2 contract follow-through

- labels: `exec_tools, approvals, security, tests_ci`
- `exec_tools`: PR centers on Exec V2 contracts, safeBins, allowlist matching, and command execution behavior.
- `approvals`: Adds and updates exec approvals allowlist/effective-policy contract tests and docs.
- `security`: Hardens command-contract and trusted-dir/safe-bin policy to enforce security boundaries.
- `tests_ci`: Title and body emphasize landing test coverage, with many new or updated exec/security test files.

## openclaw-openclaw-62552 — fix(acp): stabilize bridge session keys

- labels: `acp, sessions, queueing, reliability`
- `acp`: The main fix is in the ACP translator and ACP bridge fallback/pending prompt handling.
- `sessions`: The PR stabilizes bridge session keys and matches raw versus Gateway-canonical session identifiers.
- `queueing`: Task registry maintenance now marks active cron/cli/subagent tasks lost when their child backing session is terminal.
- `reliability`: The changes address hangs/failures and stale live tasks caused by session key collisions and terminal child sessions.

## openclaw-openclaw-62769 — [Feature]: Support ACP configured bindings for Telegram DMs (not just groups/topics)

- labels: `acp, chat_integrations, sessions`
- `acp`: The feature is specifically about routing Telegram messages through configured ACP bindings and creating/resuming an ACP harness session.
- `chat_integrations`: Telegram DM behavior is the user-facing integration surface being fixed.
- `sessions`: The requested behavior depends on persistent conversation-to-ACP session binding and resume semantics.

## openclaw-openclaw-63007 — Pass outbound session identity into message_sending and surface guarded gateway send denial

- labels: `gateway, hooks, notifications, sessions`
- `gateway`: PR explicitly fixes the `gateway call send` path and gateway send denial handling.
- `hooks`: Adds outbound identity to the `message_sending` hook context and tests hook mapper behavior.
- `notifications`: Changes outbound message delivery handling, including guarded delivery cancellation and delivery results.
- `sessions`: Central change is passing outbound `agentId` and `sessionKey` session identity through delivery and hooks.

## openclaw-openclaw-63229 — Bug: Gateway falsely marks healthy local vLLM endpoints as timed out/overloaded, causing 1–23 min fallback cascades

- labels: `gateway, local_models, model_serving, reliability`
- `gateway`: The reported failures are in the gateway's fallback/routing subsystem and include gateway timeouts/unresponsiveness.
- `local_models`: Healthy local vLLM/Gemma/Qwen GPU endpoints are central and are being falsely treated as timed out or overloaded.
- `model_serving`: The issue concerns endpoint request routing, fallback chains, timeout/overload classification, and provider availability semantics.
- `reliability`: False timeouts, long fallback cascades, and unresponsive gateway behavior are central operational reliability failures.

## openclaw-openclaw-64181 — fix(hooks): reject error responses from slug generator and strip post-truncation dashes

- labels: `hooks, memory, reliability`
- `hooks`: Fix is contained in src/hooks/llm-slug-generator.ts and changes hook-side LLM slug response handling.
- `memory`: Bug produced incorrect memory filenames and fragmented the canonical session memory file path.
- `reliability`: Rejects failure-mode error payloads and fixes malformed trailing-dash slugs to prevent bad state from provider failures.

## openclaw-openclaw-64199 — [Bug]: ACP configured binding uses parent channel ID for session key — all threads under same channel share one persistent Claude Code process

- labels: `acp, acpx, sessions, chat_integrations, security`
- `acp`: The bug is specific to `runtime.type: "acp"` configured bindings and ACP session key construction.
- `acpx`: The shared state is traced through `acpxRecordId`, the ACPX state directory, and persistent ACPX client records.
- `sessions`: The core defect is incorrect session-key granularity causing multiple threads to share one persistent session/process.
- `chat_integrations`: The affected binding surface is Discord channels and spawned Discord threads.
- `security`: The issue causes cross-thread context contamination where one thread can see another thread's conversation history.

## openclaw-openclaw-64718 — fix(security): default exec to deny for non-owner auto-reply senders

- labels: `security, exec_tools, approvals, auth_identity`
- `security`: Fix hardens a prompt-injection path that could let unauthenticated senders trigger arbitrary command execution.
- `exec_tools`: The changed logic resolves exec tool security/ask overrides and defaults non-owner senders to deny.
- `approvals`: The bug involved ask=off removing the approval gate, and the fix sets ask=always for non-owner auto-replies.
- `auth_identity`: Behavior now depends on sender ownership identity via senderIsOwner to distinguish trusted owners from non-owner channel senders.

## openclaw-openclaw-65187 — test: add regression tests for <final> tag stripping in UI message extraction

- labels: `tests_ci, ui_tui`
- `tests_ci`: PR only adds regression tests in a UI test file and reports UI test execution.
- `ui_tui`: Tests target Control UI chat message extraction and displayed stripping of internal tags.

## openclaw-openclaw-65242 — fix: CompletionDeliveryGate to prevent duplicate ACP completion delivery

- labels: `acp, agent_runtime, sessions, notifications, reliability`
- `acp`: The fix is specifically for ACP child-session completion delivery paths and ACP silent wake behavior.
- `agent_runtime`: It coordinates subagent/ACP completion lifecycle paths including task registry, announce flow, and completion handling.
- `sessions`: Completion keys and behavior are tied to child, parent, requester, and owner session identity and wake/resume semantics.
- `notifications`: The main user-visible problem is duplicate or incorrect completion messages being delivered to users.
- `reliability`: The gate fixes a race/duplicate-delivery failure mode with first-writer-wins coordination and stale replay prevention.

## openclaw-openclaw-65640 — fix(acp): persistent session recovery for --bind here sessions

- labels: `acp, acpx, sessions, reliability`
- `acp`: The PR directly changes ACP control-plane session handling and ACP error detection/retry behavior.
- `acpx`: The recovery scenario is specifically an ACPX backend losing a session, with ACPX backend/session identifiers in the affected flow.
- `sessions`: The core issue is persistent session resume, stale binding cleanup, and `--bind here` session recovery.
- `reliability`: The fix adds retry and stale-state cleanup so sessions recover from missing backend state after restart or eviction.

## openclaw-openclaw-66000 — fix(cli): clear conflicting OPENCLAW_LAUNCHD_LABEL when --profile is provided

- labels: `config, gateway, packaging_deployment`
- `config`: The fix changes CLI profile environment handling for OPENCLAW_LAUNCHD_LABEL when --profile is explicit.
- `gateway`: The stale launchd label caused gateway status to resolve the wrong profiled gateway plist.
- `packaging_deployment`: Launchd label and LaunchAgent plist resolution are central service-manager/deployment concerns.

## openclaw-openclaw-66125 — [Bug]: openai-completions fallback candidate is selected, but fallback does not complete successfully through an OpenAI-compatible proxy

- labels: `local_model_providers, model_serving, reliability`
- `local_model_providers`: Issue centers on a configured local OpenAI-compatible provider/proxy, fallback routing, base URL, and provider selection.
- `model_serving`: Failure involves OpenAI-compatible completions endpoint semantics, request-shape compatibility, model listing, and chat completions behavior.
- `reliability`: Regression where selected fallback provider fails to complete and falls through without actionable diagnostics.

## openclaw-openclaw-66327 — feat(msteams): implement sendPayload for interactive approval cards

- labels: `chat_integrations, approvals, notifications`
- `chat_integrations`: Implements MS Teams channel outbound behavior using Adaptive Cards for interactive messages.
- `approvals`: The feature specifically renders approval prompts with Approve/Deny buttons that submit /approve commands.
- `notifications`: Changes outbound message delivery for interactive payloads, including fallback and card-send behavior.

## openclaw-openclaw-67244 — Explicit ACP agent runs: embedded backend visibility failure and stale final JSON state after sessions_yield

- labels: `acp, acpx, agent_runtime, sessions, reliability`
- `acp`: The issue is explicitly about ACP agent runs and descendant completion after sessions_yield.
- `acpx`: The backend visibility bug specifically involves embedded ACPX runtime backend/plugin registration.
- `agent_runtime`: The failures occur in the explicit agent --json embedded run path and agent lifecycle reconciliation.
- `sessions`: Stale final state is tied to a session-id run, sessions_yield, liveness state, replayInvalid, and completed descendant session work.
- `reliability`: Both reported bugs are operational correctness failures: false backend-unconfigured errors and stale completion metadata after successful work.

## openclaw-openclaw-68187 — SSE-backed MCP sessions can stay stale after server restart and fail with 'Session not found'

- labels: `mcp_tooling, sessions, gateway, reliability`
- `mcp_tooling`: Issue centers on MCP integration behavior for an SSE-backed MCP server and tool calls through that path.
- `sessions`: Stale client/proxy session state and 'Session not found' after restart are the primary failure mode.
- `gateway`: Recovery requires restarting the OpenClaw gateway and the suspected defect is in the gateway/proxy client-session layer.
- `reliability`: Expected behavior is automatic stale-session detection, reconnect, invalidation, and recovery after server restart.

## openclaw-openclaw-68204 — Unified run trace schema across agent, ACP, subagent, and task flows

- labels: `acp, agent_runtime, sessions, telemetry_usage`
- `acp`: Scope explicitly includes ACP sessions and updating ACP parent-child relay paths.
- `agent_runtime`: The schema is for main agent runs, subagents, task flows, and run lifecycle events.
- `sessions`: Trace fields and goals include sessionKey and preserving parent-child run/session linkage.
- `telemetry_usage`: The issue is primarily about observability/tracing with canonical trace events, latency, status, and timeline reconstruction.

## openclaw-openclaw-68843 — fix(acp): treat missing cwd as stale bound session

- labels: `acp, sessions, reliability`
- `acp`: The fix is explicitly in ACP session initialization/reset handling and ACP stale-session detection.
- `sessions`: Central behavior is clearing stale bound session bindings when the runtime cwd is missing.
- `reliability`: Addresses wedged retries and automatic recovery from stale session state instead of requiring manual cleanup.

## openclaw-openclaw-69260 — Harden Gemini ACP integration against ambient API-key fallback and add generic auth-contract hooks for ACP agents

- labels: `acp, auth_identity, hooks, security`
- `acp`: The issue is explicitly about Gemini ACP-backed agent integration and ACP agent definitions/routes.
- `auth_identity`: Central request is to enforce expected auth modes and prevent drift from oauth-personal to API-key auth.
- `hooks`: It asks for generic auth-contract and env-scrubbing hooks for ACP agent launches.
- `security`: The hardening prevents ambient API keys and incompatible credential env from being used unexpectedly.

## openclaw-openclaw-69328 — fix(acp): avoid false zero-diff failures and append session messages

- labels: `acp, reliability, sessions, ui_tui`
- `acp`: PR changes ACP control-plane behavior, including the ACP verification gate and ACP session manager handling.
- `reliability`: Fixes false zero-diff hard failures and makes oneshot/persistent run completion handling more robust.
- `sessions`: Persistent sessions and incoming session.message transcript payload handling are central to the change.
- `ui_tui`: Control UI chat now appends active-run session messages with dedupe and optimistic echo replacement.

## openclaw-openclaw-70882 — fix(bundle-mcp): coerce stringified object/array params before MCP tool calls

- labels: `mcp_tooling, tool_calling, security`
- `mcp_tooling`: The fix is in the bundled MCP materialization layer and targets strict MCP servers rejecting parameter shapes.
- `tool_calling`: It normalizes LLM-produced tool call arguments against tool input schemas before invoking tools.
- `security`: The follow-up patch explicitly adds prototype-pollution and oversized-payload guards for parsed tool arguments.

## openclaw-openclaw-71157 — [Feature]: Support WhatsApp disappearing-message expiration for outbound replies

- labels: `chat_integrations, config`
- `chat_integrations`: The feature is specific to WhatsApp outbound reply behavior and Baileys send metadata for a chat integration.
- `config`: It proposes channel- and account-level configuration keys with override/default behavior for disappearing-message expiration.

## openclaw-openclaw-71216 — Config schema: add `sandbox`, `routing.rules`, `instances`, and `gateway.nodes.denyPaths`

- labels: `config, gateway, local_model_providers, sandboxing, security`
- `config`: Issue explicitly requests new config schema fields for sandbox, routing rules, instances, and denyPaths.
- `gateway`: Several asks are for gateway-enforced behavior, including multi-gateway instances and gateway.nodes.denyPaths.
- `local_model_providers`: routing.rules is provider selection for a mixed cloud/local Ollama setup with host and model routing.
- `sandboxing`: sandbox.mode is a global tool-execution sandbox mode and instance isolation is part of the requested policy surface.
- `security`: denyPaths and sensitivity-based routing are intended to protect credentials, secrets, and sensitive operations.

## openclaw-openclaw-71487 — Web UI: add a clear TTS toggle and default voice picker in Settings

- labels: `ui_tui, self_hosted_inference, config`
- `ui_tui`: The request is for a first-class Text-to-Speech panel in the Control UI/Web UI Settings with toggles and dropdowns.
- `self_hosted_inference`: The feature manages TTS speech inference providers, voices, status, and sample generation via existing TTS inference capabilities.
- `config`: It explicitly concerns persisting TTS enablement, provider, and default voice preferences in the existing settings/config contract.

## openclaw-openclaw-71594 — docs(gateway): clarify IPv4-only BYOH bind path

- labels: `docs, gateway`
- `docs`: PR explicitly updates gateway documentation, TSDoc, and help text to clarify IPv4-only BYOH behavior.
- `gateway`: The clarified behavior concerns Gateway bind modes and custom bind host guidance.

## openclaw-openclaw-71646 — mcp/channel-bridge: pendingClaudePermissions / pendingApprovals leak — no TTL, no close-clear, no cap

- labels: `mcp_tooling, approvals, reliability`
- `mcp_tooling`: Issue is in src/mcp/channel-bridge.ts and affects long-running openclaw mcp serve bridge behavior.
- `approvals`: Central leak involves pendingClaudePermissions and pendingApprovals for permission/approval requests that are not resolved or cleared.
- `reliability`: Reports unbounded pending-map growth due missing TTL, close cleanup, and caps in a long-running process.

## openclaw-openclaw-71648 — fix(mcp): bound pendingClaudePermissions / pendingApprovals via TTL sweeper + close clear

- labels: `mcp_tooling, approvals, reliability`
- `mcp_tooling`: The fix is in the MCP channel bridge/server path for long-running `openclaw mcp serve` behavior.
- `approvals`: The bounded state is explicitly `pendingApprovals` and missed `*.approval.resolved` approval frames.
- `reliability`: Adds TTL sweeping, close cleanup, and post-close guards to prevent leaks and ghost writes in long-running processes.

## openclaw-openclaw-71784 — Bug: memory search live embedding fails ~20–40% with `fetch failed | other side closed` (provider-agnostic; upstream healthy)

- labels: `memory, reliability`
- `memory`: The bug directly affects live memory search and semantic memory recall embedding queries.
- `reliability`: The issue is intermittent 20–40% fetch/socket failures requiring retry or recovery behavior despite healthy upstream providers.

## openclaw-openclaw-71930 — Mattermost plugin drops post_edited events — @mentions added via edit do not trigger agent wake

- labels: `chat_integrations, reliability`
- `chat_integrations`: The issue is specifically about the Mattermost WebSocket integration handling edited chat posts and @mentions.
- `reliability`: A supported chat event is silently dropped, causing message loss and failure to wake the agent.

## openclaw-openclaw-71976 — Memory Dreaming: Light sleep sort prioritizes recency over recallCount, hiding real recall data

- labels: `memory, reliability`
- `memory`: Issue is about Memory Dreaming, short-term recall data, rehydration, and promotion behavior in the memory store.
- `reliability`: Reports deterministic failure modes where valid memory candidates are buried or not promoted due to stale/shifted recall metadata and narrow rehydration search.

## openclaw-openclaw-72001 — fix(hooks): write allowedSessionKeyPrefixes from gmail wizard

- labels: `hooks, gateway, config`
- `hooks`: The fix is in Gmail hook setup/preset handling and hook validator compatibility for templated hook session keys.
- `gateway`: The reported failure is that the gateway refuses to load the generated hooks config on restart, and gateway hook tests validate the fix.
- `config`: The wizard now writes the missing hooks.allowedSessionKeyPrefixes field into openclaw.json while preserving existing values.

## openclaw-openclaw-72015 — Reliability: active-memory blocks replies and QMD boot initialization can overload multi-agent gateways

- labels: `gateway, memory, reliability`
- `gateway`: The issue centers on multi-agent gateway boot/restart overload, health probe timeouts, and degraded gateway responsiveness.
- `memory`: Active-memory and QMD memory startup/update behavior are the core components causing blocking and startup bursts.
- `reliability`: The reported impact is high CPU, long latency, timeouts, crash-loop risk, and requested fail-open/nonblocking defaults.

## openclaw-openclaw-72085 — docs(commands): document bashForegroundMs clamp bounds (0–30 000 ms)

- labels: `docs, config`
- `docs`: Docs-only PR adding a bullet to the configuration reference; no code or behavior changes.
- `config`: The documented item is the `bashForegroundMs` configuration option and its accepted clamp range.

## openclaw-openclaw-72087 — Bug: dist/entry.js main-path breaks Codex OAuth image generation on Linux while direct runCli()/provider path succeeds

- labels: `auth_identity, codex, packaging_deployment`
- `auth_identity`: Failure occurs in an openai-codex OAuth profile flow with no API key, making auth-provider behavior central.
- `codex`: The affected path uses Codex OAuth and the Codex Responses backend for image generation.
- `packaging_deployment`: The report isolates the regression to the packaged dist/entry.js main bootstrap path versus direct runCli/provider invocation.

## openclaw-openclaw-72133 — Feature request: per-message token/cost metadata in mobile app and channel surfaces

- labels: `telemetry_usage, ui_tui, chat_integrations`
- `telemetry_usage`: Request is to expose per-message token, cost, cache, context percentage, and model metadata.
- `ui_tui`: Asks to add the metadata to the iOS/Android native chat view and references existing Control UI behavior.
- `chat_integrations`: Explicitly requests optional footers in messaging channel surfaces such as Signal, iMessage, Telegram, and BlueBubbles.

## openclaw-openclaw-72138 — fix(feishu): emit sent hooks for normal replies

- labels: `chat_integrations, hooks, notifications`
- `chat_integrations`: The fix is specific to Feishu normal conversation reply handling in the Feishu extension.
- `hooks`: The core change emits canonical plugin message_sent and internal message:sent hooks from reply dispatch paths.
- `notifications`: The PR changes outbound sent-message handling so successful or failed normal replies are reflected for message delivery workflows.

## openclaw-openclaw-72262 — docs: add WhatsApp 408 disconnect troubleshooting runbook

- labels: `chat_integrations, docs, reliability`
- `chat_integrations`: The runbook is specifically for the WhatsApp channel/Baileys integration.
- `docs`: The issue explicitly requests additions to WhatsApp and channel troubleshooting documentation.
- `reliability`: The documented scenario is a repeated 408 disconnect/reconnect failure with recovery guidance.

## openclaw-openclaw-73910 — BUG: OpenClaw-managed Codex ACP uses isolated CODEX_HOME without auth bridge and sends unsupported timeout config

- labels: `acp, acpx, auth_identity, codex, config`
- `acp`: The failure is in OpenClaw-managed Codex ACP sessions, including an ACP session/set_config_option rejection.
- `acpx`: The repro compares direct ACPX to the managed path and implicates the ACPX plugin schema/default timeout forwarding.
- `auth_identity`: The isolated CODEX_HOME lacks Codex authentication and the requested fix is auth reuse, bridging, or setup flow.
- `codex`: Codex ACP, CODEX_HOME, and the Codex adapter/runtime are the specific failing integration.
- `config`: Unsupported timeout=120 config handoff and generated Codex config are central reported causes.

## openclaw-openclaw-74305 — [Bug]: ACPX Codex worker fails when model/thinking overrides are configured

- labels: `acpx, acp, codex, reliability`
- `acpx`: The failure is in the ACPX-enabled Codex worker path and ACPX plugin command handling.
- `acp`: The repro uses the ACP runtime, ACP worker flow, ACP stream log, and AcpRuntimeError/ACP_TURN_FAILED.
- `codex`: The issue is specific to codex-acp and Codex CLI model/thinking command overrides.
- `reliability`: Configured overrides cause the worker run to fail with an internal runtime error instead of completing or validating cleanly.

## openclaw-openclaw-75657 — fix: local GGUF embedding model warmup blocks Node.js event loop for minutes on startup (ARM64/Pi)

- labels: `gateway, local_models, memory, reliability`
- `gateway`: The bug occurs during Gateway startup and leaves the Gateway/WebSocket port unreachable until ready.
- `local_models`: A local GGUF embedding model loaded via node-llama-cpp on ARM64/Pi is the direct cause of the blocking behavior.
- `memory`: The failing path is the local `memorySearch.provider` embedding model used for memory search/indexing.
- `reliability`: The issue is an operational startup hang/event-loop block causing timeouts and unreachable services despite a warmup timeout.

## openclaw-openclaw-78528 — Security: skill SecretRef API keys still leak into exec child environments

- labels: `security, exec_tools, skills_plugins, auth_identity`
- `security`: The issue reports SecretRef API keys leaking into child process environments, a concrete secret exposure vulnerability.
- `exec_tools`: The leak occurs through commands spawned by the exec tool inheriting an unsafe environment.
- `skills_plugins`: The affected secrets are configured under skill entries and skill-scoped SecretRefs.
- `auth_identity`: The bug breaks credential scoping for API keys intended only for specific skills/tools.

## openclaw-openclaw-78919 — [Bug] ACP sessions_spawn doesn't route images to Codex's native vision like acpx codex exec does

- labels: `acp, acpx, codex, sessions`
- `acp`: The failing path is explicitly ACP `sessions_spawn` with `runtime:acp`, including ACP attachment handling before dispatch.
- `acpx`: The working comparator is explicitly `acpx codex exec`, and the bug asks for parity with that ACPX code path.
- `codex`: The image routing failure is specific to Codex native vision and Codex command/runtime behavior.
- `sessions`: The affected entry point is `sessions_spawn`, with impact on session tracking and delegated session flow.

## openclaw-openclaw-79447 — fix(model-auth): resolve per-entry apiKey profile ID references

- labels: `auth_identity, config`
- `auth_identity`: Central fix is resolving stored auth-profile ID references to actual provider credentials and enforcing credential-class compatibility.
- `config`: The behavior concerns `models.providers.<id>.apiKey` configuration values and how per-entry provider config is interpreted.

## openclaw-openclaw-79897 — OpenAI-compatible streaming with llama.cpp saves zero usage (stream closed before final usage chunk)

- labels: `local_models, model_serving, telemetry_usage`
- `local_models`: The failing backend is explicitly llama.cpp, a concrete local model server used for agent turns.
- `model_serving`: The core bug is OpenAI-compatible SSE streaming behavior: OpenClaw stops before the final usage-only chunk.
- `telemetry_usage`: The user-visible failure is saved token usage becoming 0/0/0, breaking status context display and compaction accounting.

## openclaw-openclaw-80255 — fix #79026: active-memory recall subagent can deadlock on the main lane inside before_prompt_build

- labels: `memory, agent_runtime, queueing, reliability`
- `memory`: The fix is in the Active Memory extension and specifically affects active-memory recall behavior.
- `agent_runtime`: The recall is performed by an embedded subagent, so subagent execution behavior is central.
- `queueing`: The change isolates recall onto a dedicated active-memory lane instead of re-entering the main lane.
- `reliability`: The PR fixes a deadlock caused by main-lane re-entry during prompt building.

## openclaw-openclaw-80431 — ACPx plugin-tools MCP config test expects source path but resolver returns dist path

- labels: `acpx, mcp_tooling, tests_ci`
- `acpx`: The failing test and resolver behavior are in the ACPX extension config area.
- `mcp_tooling`: The mismatch concerns injection/resolution of the built-in plugin-tools MCP server.
- `tests_ci`: The reported problem is a pnpm test failure and the requested fix is to update the test/helper expectations.

## openclaw-openclaw-80475 — test(acpx): accept built-dist MCP server resolution when dist exists

- labels: `acpx, mcp_tooling, tests_ci`
- `acpx`: The changed test is under extensions/acpx and mirrors ACPx plugin resolver path behavior.
- `mcp_tooling`: The expected arguments are for built-in MCP servers and their dist-vs-source resolution.
- `tests_ci`: The PR only updates a Vitest test helper and test expectations, with no runtime code change.

## openclaw-openclaw-80479 — feat(memory/embeddings): add openai-compatible provider for self-hosted servers (llama.cpp, Ollama, vLLM, TGI, LocalAI)

- labels: `local_model_providers, memory, self_hosted_inference`
- `local_model_providers`: Adds an OpenAI-compatible provider adapter with baseUrl/model/apiKey handling for local or self-hosted backends.
- `memory`: The feature is specifically a memory-lancedb embedding provider and adapter for memory embeddings.
- `self_hosted_inference`: Targets operators running their own embedding servers such as llama.cpp, Ollama, vLLM, TGI, LocalAI, or internal reverse-proxied services.

## openclaw-openclaw-81200 — fix(acpx): strip provider API keys from child harness env

- labels: `acpx, acp, security, auth_identity`
- `acpx`: The fix is in the ACPX extension runtime/auth bridge and generated ACPX child wrappers.
- `acp`: It changes built-in Claude and Gemini ACP harness launch behavior and ACP alias wrapping.
- `security`: The central purpose is preventing provider API-key secrets from leaking into spawned child harness environments.
- `auth_identity`: The change constrains provider authentication credential scope by stripping API-key env vars from child processes while preserving parent auth state.

## openclaw-openclaw-81488 — Harden node exec approval precheck env [AI]

- labels: `approvals, exec_tools, security`
- `approvals`: Central change fixes exec approval precheck analysis so node-host commands do not incorrectly skip required approval.
- `exec_tools`: The affected path is node-host shell/system.run command execution and allowlist evaluation.
- `security`: PR is explicit security hardening for command allowlist decisions by preventing gateway PATH from satisfying node prechecks.

## openclaw-openclaw-82507 — [Feature]: ACPX Codex sandbox should inherit user-installed plugins (e.g. Superpowers)

- labels: `acpx, codex, sandboxing, skills_plugins`
- `acpx`: The issue is explicitly about ACPX background tasks and the ACPX Codex sandbox home.
- `codex`: Codex runtime behavior is central via CODEX_HOME, Codex App plugins, and the Codex ACP wrapper.
- `sandboxing`: The core problem is that an isolated sandboxed Codex home does not inherit user-installed content.
- `skills_plugins`: The requested feature is plugin and skill inheritance/marketplace loading for user-installed Codex plugins such as Superpowers.

## openclaw-openclaw-82596 — Feature/exec denylist

- labels: `exec_tools, approvals, security`
- `exec_tools`: PR adds denylist behavior for model-initiated shell exec commands, including blocking curl/wget and related exec host paths.
- `approvals`: Feature is implemented as a new exec approval/security mode with ask fallback and approval evaluation changes.
- `security`: Denylist sets a security boundary for agent shell execution, with default network-fetch blocks and fail-closed malformed rule handling.

## openclaw-openclaw-82642 — Fix iMessage slash command acknowledgements

- labels: `chat_integrations, notifications, reliability`
- `chat_integrations`: The fix is in the iMessage extension inbound processing for iMessage slash-command handling.
- `notifications`: The central bug is acknowledgement/reply delivery suppression for iMessage command responses.
- `reliability`: It fixes a dropped acknowledgement path so authorized slash commands reliably return replies.

## openclaw-openclaw-83333 — [Bug]: Memory provider cutover to Ollama leaves production index in mixed OpenAI/Ollama vector state after live sync/reload

- labels: `memory, self_hosted_inference, reliability`
- `memory`: The bug centers on the memory search index, embeddings, vector dimensions, canary search, and reindex/status behavior.
- `self_hosted_inference`: The cutover is specifically from OpenAI embeddings to a locally configured Ollama embedding provider.
- `reliability`: The live sync/reload path leaves a clean-reported but inconsistent mixed-vector state that breaks search and requires rollback.

## openclaw-openclaw-84094 — feat(gateway): forward frequency_penalty, presence_penalty, and seed via OpenAI-compatible HTTP gateway

- labels: `gateway, api_surface, model_serving`
- `gateway`: The PR changes OpenClaw gateway handling for OpenAI-compatible HTTP requests.
- `api_surface`: It extends the public POST /v1/chat/completions request contract and gateway validation for new parameters.
- `model_serving`: It forwards OpenAI-compatible sampling parameters through transport to the upstream provider request payload.

## openclaw-openclaw-84297 — [Bug]: Per-agent identity overlay dropped on cron --announce and heartbeat target-channel Slack pushes (announce path; reply path was fixed in #38235)

- labels: `auth_identity, chat_integrations, cron_automation, notifications`
- `auth_identity`: Bug centers on per-agent identity/persona overlay not being applied to outbound messages.
- `chat_integrations`: The affected delivery surface is Slack, specifically chat.postMessage behavior in Slack channels.
- `cron_automation`: The broken paths are cron --announce jobs and heartbeat target-channel sends.
- `notifications`: Issue concerns outbound announce/heartbeat messages rendering with the wrong sender identity.

## openclaw-openclaw-84316 — [Bug]: Telegram group TTS for sub-agent reports success in /tts status but voice never delivered (2026.5.12)

- labels: `chat_integrations, notifications, reliability`
- `chat_integrations`: The failure is specific to Telegram group chat delivery while Telegram DM works.
- `notifications`: The central bug is an outbound TTS voice message reported successful but not delivered.
- `reliability`: This is a message-loss/state correctness bug where status reports success despite missing delivery.

## openclaw-openclaw-84337 — [Bug]: Hook ingress token unlocks password-mode gateway auth

- labels: `security, auth_identity, gateway, hooks`
- `security`: The issue is an explicit high-severity auth bypass where a hook bearer token grants full operator access.
- `auth_identity`: Central bug is credential scope confusion between hooks.token and gateway.auth.password in password-mode authentication.
- `gateway`: The affected protected surface is the Gateway HTTP auth path and gateway startup/auth utilities.
- `hooks`: The bypass starts from the hook ingress bearer token and hook routing controls.

## openclaw-openclaw-84385 — [codex] Fix macOS app copyright year

- labels: `ui_tui`
- `ui_tui`: The PR fixes visible macOS About settings text by updating the displayed copyright year.

## openclaw-openclaw-84418 — test(cron): document and test owner-only tool security boundary for isolated cron

- labels: `cron_automation, security, tests_ci`
- `cron_automation`: The change targets isolated cron runs and the cron run executor's owner-only tool allowlist.
- `security`: It documents and enforces an owner-only tool security boundary, auto-granting only safe cron tools while filtering gateway/nodes.
- `tests_ci`: The PR adds focused unit tests covering the cron owner-only allowlist behavior.

## openclaw-openclaw-84419 — fix(session): prefer real tool result over synthetic error in transcript repair

- labels: `sessions, tool_calling, reliability`
- `sessions`: The fix is in session transcript repair and affects persisted session history on reload.
- `tool_calling`: The core behavior is deduplicating and pairing tool results, preferring a real tool result over a synthetic missing-result error.
- `reliability`: It mitigates a race-induced stale synthetic error so successful tool calls recover correctly in repaired transcripts.

## openclaw-openclaw-84567 — [Bug]: Codex bundled harness initialize still hangs in 2026.5.18 isolated cron — surfaces via #64744 timeout-wrapping as 'isolated agent setup timed out before runner start'

- labels: `codex, cron_automation, agent_runtime, reliability`
- `codex`: Failure is specific to the bundled Codex harness/openai-codex path; the same cron job works with a Claude CLI model.
- `cron_automation`: The regression occurs in scheduled and manually triggered isolated cron jobs using `openclaw cron run`.
- `agent_runtime`: The hang is during isolated agent setup before the runner starts for an `agentTurn` payload.
- `reliability`: Central bug is a deterministic regression timeout/hang with repeated failures and crash-loop style consecutive errors.

## openclaw-openclaw-84570 — Remove skill prelude exec allowlist

- labels: `approvals, exec_tools, skills_plugins`
- `approvals`: PR changes exec-approval allowlist behavior so legacy skill prelude chains now go through the normal approval flow.
- `exec_tools`: Central change is shell command allowlist analysis/evaluation for exec commands such as cat/printf chains and skill wrappers.
- `skills_plugins`: Behavior specifically concerns skills: SKILL.md prelude handling, trusted skill wrappers, and autoAllowSkills semantics.

## openclaw-openclaw-84583 — cron announce delivery triggers EmbeddedAttemptSessionTakeoverError when user is actively chatting

- labels: `cron_automation, notifications, chat_integrations, sessions, reliability`
- `cron_automation`: The failure is triggered when an isolated cron job finishes and performs announce delivery.
- `notifications`: The central conflict involves announce delivery of cron results to a user.
- `chat_integrations`: The delivery channel is explicitly Telegram and conflicts with an active Telegram chat session.
- `sessions`: The error is caused by concurrent writes to the same session file and embedded prompt lock state.
- `reliability`: This is a race/recovery failure causing takeover errors and possible message loss during active use.

## openclaw-openclaw-84645 — Materialize node-host inline interpreter eval before exec approval

- labels: `exec_tools, approvals, security`
- `exec_tools`: Changes node-host system.run command handling by rewriting inline Python/Node eval invocations into script-file argv forms.
- `approvals`: Core change occurs before approval planning and preserves approval binding through generated script paths and hashes.
- `security`: Explicitly hardens inline eval by fail-closing ambiguous forms, using private temp files, 0600 mode, and stable hash-bound artifacts.

## openclaw-openclaw-84648 — Add SafeOps preflight hook for exec tool

- labels: `exec_tools, hooks, security`
- `exec_tools`: PR inserts SafeOps preflight before exec command dispatch in bash-tools.exec.ts.
- `hooks`: The feature is explicitly a preflight/before-tool-execute hook integrated into tool execution.
- `security`: SafeOps is a policy/security preflight with secret-scan and security-boundary concerns.

## openclaw-openclaw-84660 — [Bug] Voice STT: empty moonshine transcripts passed as raw JSON to LLM, clogging serialized processing queue

- labels: `chat_integrations, self_hosted_inference, queueing, reliability`
- `chat_integrations`: Bug occurs in Discord voice STT bot behavior for voice-channel audio segments.
- `self_hosted_inference`: Central failure is handling output from moonshine/sherpa-onnx speech-to-text inference.
- `queueing`: Empty transcript LLM calls clog the serialized processing queue and proposed fix mentions depth/stale discard.
- `reliability`: Filtering failure makes the voice pipeline appear unresponsive and wastes calls on empty segments.

## openclaw-openclaw-84668 — docs(agent-runtimes): clarify model name vs runtime routing for Codex (#84637)

- labels: `docs, agent_runtime, codex`
- `docs`: PR changes only docs/concepts/agent-runtimes.md and adds explanatory warning text.
- `agent_runtime`: The documentation clarifies runtime routing via agentRuntime.id versus model selection/fallbacks.
- `codex`: The warning specifically distinguishes Codex runtime/harness from Codex-named model IDs.

## openclaw-openclaw-84681 — fix(codex): stabilize heartbeat dynamic tool schema

- labels: `codex, sessions, tool_calling`
- `codex`: PR explicitly changes the Codex extension app-server dynamic tool handling and thread lifecycle behavior.
- `sessions`: The fix keeps normal and heartbeat turns on the same Codex thread/session instead of rotating threads due to schema changes.
- `tool_calling`: Central change separates durable registered tool schemas from currently callable tools, including heartbeat_respond availability and denial.

## openclaw-openclaw-84709 — fix(cron): fail closed when required tools are unavailable

- labels: `codex, cron_automation, exec_tools, reliability`
- `codex`: The PR directly changes Codex app-server handling and Codex native/dynamic tool surface behavior.
- `cron_automation`: The fix targets cron isolated-agent jobs, cron payload tool allowlists, and cron run finalization.
- `exec_tools`: Required exec/shell dynamic tool availability and finite tool allowlists are central to the bug and fix.
- `reliability`: Cron runs now fail closed with TOOL_SURFACE_UNAVAILABLE and avoid false-success summaries when required tools are missing.

## openclaw-openclaw-84715 — [Bug]: @openclaw/codex peer link failure reproduced on 2026.5.19 after update

- labels: `codex, packaging_deployment, reliability, skills_plugins`
- `codex`: The failure is explicitly in @openclaw/codex and the Codex harness/shared-client startup path.
- `packaging_deployment`: The root cause involves Homebrew update/install state and npm peer-link resolution in the deployed package tree.
- `reliability`: The bug causes Codex turns to fail before any assistant reply and is repaired by doctor/repair health recovery.
- `skills_plugins`: The broken dependency is in the managed plugin npm tree and the expected fixes target plugin repair/startup health.

## openclaw-openclaw-84729 — [codex] Fix macOS app copyright year

- labels: `ui_tui, tests_ci`
- `ui_tui`: Updates the macOS About settings copyright text, a visible app UI surface.
- `tests_ci`: Changes the changed-check planning script and matching test coverage for app-lint skip behavior.

## openclaw-openclaw-84732 — Slack channel sends fail: `reconcileUnknownSend` required but no channel adapter implements it

- labels: `chat_integrations, notifications, reliability`
- `chat_integrations`: The failure is specific to sending messages into Slack channels via the Slack channel adapter.
- `notifications`: The issue concerns outbound channel message delivery and durable final send handling for sent messages.
- `reliability`: The missing reconciliation capability causes channel sends to fail, creating message-loss risk.

## openclaw-openclaw-84740 — Feature Request: Option to hide/suppress certain sessions from the session list

- labels: `sessions, ui_tui`
- `sessions`: Request centers on hiding, suppressing, archiving, and filtering specific sessions in the session list.
- `ui_tui`: The requested changes are user-facing session list UX actions and toggles to reduce UI clutter.

## openclaw-openclaw-84752 — fix: self-heal lane wedges + restore openai-codex OAuth on embedded path

- labels: `auth_identity, chat_integrations, codex, queueing, reliability`
- `auth_identity`: Restores OAuth profile/sidecar token resolution in the auth profile store for embedded paths.
- `chat_integrations`: Changes Telegram polling-session recovery to keep the Telegram channel from going offline.
- `codex`: The auth regression is explicitly for the openai-codex provider and its OAuth profile.
- `queueing`: Fixes wedged per-lane command queues by re-pumping/resetting lanes with queued work.
- `reliability`: Central theme is self-healing from stalls, wedges, and transient failures without manual restart.

## openclaw-openclaw-84757 — [Bug]: Telegram session can get stuck after compaction when encrypted reasoning content fails verification

- labels: `chat_integrations, sessions, reliability`
- `chat_integrations`: The failure occurs in a Telegram direct-chat session and surfaces through the Telegram fallback message.
- `sessions`: The bug is caused by persisted session history replay after compaction or restore, leaving the same session unusable.
- `reliability`: The issue is a stuck retry/recovery failure where an invalid replay payload repeatedly prevents assistant output until a new session is started.

## openclaw-openclaw-84763 — fix(acpx): scrub provider credential env from ACP harness spawns

- labels: `acpx, acp, auth_identity, security, config`
- `acpx`: PR explicitly changes the ACPX extension runtime/process launch path and command decoration for harness spawns.
- `acp`: The failing path is sessions_spawn with runtime:"acp" and the new knob is under acp.scrubProviderEnv.
- `auth_identity`: The fix addresses provider auth behavior where spawned harnesses inherit gateway API keys or OAuth tokens instead of using their own auth.
- `security`: Core change scrubs credential environment variables from child process launches to reduce token leakage and unsafe credential scope.
- `config`: Adds and documents a new acp.scrubProviderEnv configuration option with schema/default metadata.

## openclaw-openclaw-84789 — Active memory crashes on Telegram forum topic sessions (dirName validation)

- labels: `chat_integrations, memory, sessions, reliability`
- `chat_integrations`: The failure is specific to Telegram forum/topic group chat sessions.
- `memory`: The crashing component is the active memory plugin/sub-agent.
- `sessions`: The root cause is an unsanitized Telegram topic session key being used as a directory name.
- `reliability`: Active memory crashes immediately and fails for all Telegram forum topic messages.

## openclaw-openclaw-84794 — Clean up isolated cron sessions after runs

- labels: `cron_automation, sessions, reliability`
- `cron_automation`: The PR fixes isolated cron job run cleanup for deleteAfterRun jobs, including delivery.mode none and terminal cron paths.
- `sessions`: The core behavior deletes/cleans up run-scoped cron sessions via sessions.delete and shared session cleanup.
- `reliability`: It moves cleanup into a finally path so sessions are not left behind after no-delivery runs or runner errors.

## openclaw-openclaw-84802 — fix(memory-core): allow bounded dreaming session cleanup

- labels: `memory, sessions, reliability`
- `memory`: Change is in memory-core dreaming narrative behavior and cleanup.
- `sessions`: Central fix changes stable dreaming narrative session keys and deleteSession cleanup behavior.
- `reliability`: Bounded cleanup prevents stale dreaming sessions from accumulating and handles cleanup failure paths.

## openclaw-openclaw-88816 — [Bug]: v2026.05.28 breaks Google Vertex Express API Key

- labels: `auth_identity, config, model_serving`
- `auth_identity`: The regression is specifically tied to Google Vertex Express API key auth in auth-profile.json rather than ADC.
- `config`: The failure involves openclaw.json/auth-profile configuration and provider model registration entries.
- `model_serving`: The core error is a model provider/model registration failure for google-vertex/gemini endpoints.

## openclaw-openclaw-90146 — google-vertex: Missing gemini-3.1-flash-lite in provider catalog causes silent failure instead of error

- labels: `model_serving, model_releases, agent_runtime, reliability, config`
- `model_serving`: The issue centers on a Google Vertex provider catalog/model selection failure for a hosted model endpoint.
- `model_releases`: The missing entry is a specific new/versioned Gemini model, gemini-3.1-flash-lite.
- `agent_runtime`: The failure path is in the embedded agent runner and model fallback loop, preventing the agent from producing a reply.
- `reliability`: A model_not_found FailoverError with no fallback is swallowed, causing a silent failure instead of a recoverable/user-visible error.
- `config`: The requested fix includes correcting the static provider catalog/default model mapping for Google Vertex.
