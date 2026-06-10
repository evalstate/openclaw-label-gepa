# easy-set-pilot rationales

## openclaw-openclaw-58411 — sessions_spawn lacks --bind here equivalent — agent cannot bind ACP session to existing Discord thread

- labels: `acp, sessions, chat_integrations, api_surface`
- `acp`: Issue is about ACP spawn semantics and a programmatic equivalent to `/acp spawn --bind here` via `sessions_spawn`.
- `sessions`: Central problem is binding a spawned ACP session to an existing thread instead of creating a new session/thread binding.
- `chat_integrations`: The requested behavior is specifically for an existing Discord thread and chat-thread UX.
- `api_surface`: Proposes adding a new `bindTo: "current"` option to the `sessions_spawn` request contract.

## openclaw-openclaw-47446 — fix(gateway/discord): respect env proxy vars and prevent ECONNRESET

- labels: `chat_integrations, config, gateway, reliability`
- `chat_integrations`: PR is specifically for the Discord integration, including Discord REST calls, WebSocket gateway connection, and interactions behind a proxy.
- `config`: Core change makes the system honor https_proxy/HTTP_PROXY env vars and falls back when channels.discord.proxy is not explicitly configured.
- `gateway`: Changes bootstrap proxy handling during gateway startup and modify the Discord gateway plugin behavior.
- `reliability`: Fixes timeouts and ECONNRESET from local proxies by disabling keepAlive on proxy agents.

## openclaw-openclaw-87277 — [Feature] Add MiMo-V2.5 to Xiaomi catalog + automatic multimodal routing when DeepSeek V4-Pro is primary model

- labels: `model_releases, model_serving, reliability`
- `model_releases`: Issue asks to add newly released MiMo-V2.5 with version-specific benchmarks and catalog metadata.
- `model_serving`: Core behavior request is automatic routing to a multimodal-capable model before dispatch based on input capabilities.
- `reliability`: Motivation is avoiding current errors or silent stripping of image/video/audio attachments, an explicit message-loss failure mode.

## openclaw-openclaw-72016 — [Feature]: doctor api/extendability

- labels: `api_surface, config, skills_plugins`
- `api_surface`: The request is for a public doctor/plugin SDK API and contribution contract for custom checks and fixes.
- `config`: Doctor checks target environment setup, profile drift, gateway configuration conflicts, and preflight diagnosis of OpenClaw setup.
- `skills_plugins`: Central proposal is a plugin/extensibility architecture so custom doctor checks persist across upgrades.

## openclaw-openclaw-71487 — Web UI: add a clear TTS toggle and default voice picker in Settings

- labels: `ui_tui, self_hosted_inference, config`
- `ui_tui`: Request is explicitly for a Web/Control UI Settings panel with toggles, dropdowns, and test playback controls.
- `self_hosted_inference`: The feature centers on Text-to-Speech provider and voice selection, including generating a sample via TTS.
- `config`: It asks to persist TTS enablement, default provider, and default voice to existing settings/preferences such as tts.json.

## openclaw-openclaw-43564 — [Feature Request] ACP Session Skill Context Injection

- labels: `acp, sessions, skills_plugins, security`
- `acp`: Issue explicitly targets injecting context into ACP agents via sessions_spawn(runtime="acp").
- `sessions`: Feature concerns session context at agent spawn time and initial prompt/session state.
- `skills_plugins`: Central request is rendering OpenClaw skills from ~/clawd/skills/ into spawned agent context.
- `security`: Request calls out maintaining isolation and is tagged for security review due skill-context injection.

## openclaw-openclaw-84385 — [codex] Fix macOS app copyright year

- labels: `ui_tui`
- `ui_tui`: Central change updates the macOS app About settings text, a user-facing UI surface.

## openclaw-openclaw-43495 — feat(tts): add <notts> tag support for visual-only content

- labels: `self_hosted_inference, api_surface`
- `self_hosted_inference`: The main feature changes TTS preprocessing and spoken output behavior for text-to-speech content.
- `api_surface`: The PR defines user-facing TTS tag semantics and updates gateway/TTS payload behavior and RPC documentation around visible versus spoken text.

## openclaw-openclaw-72085 — docs(commands): document bashForegroundMs clamp bounds (0–30 000 ms)

- labels: `docs, config`
- `docs`: PR is explicitly docs-only and changes documentation in configuration-reference.md.
- `config`: Documents the accepted range and clamp behavior for the bashForegroundMs configuration key.

## openclaw-openclaw-84094 — feat(gateway): forward frequency_penalty, presence_penalty, and seed via OpenAI-compatible HTTP gateway

- labels: `gateway, api_surface, model_serving`
- `gateway`: Feature explicitly changes the OpenAI-compatible HTTP gateway to validate and forward new request parameters.
- `api_surface`: Extends the POST /v1/chat/completions request contract with validation and OpenAI-compatible 400 errors.
- `model_serving`: Forwards sampling parameters such as frequency_penalty, presence_penalty, and seed to upstream OpenAI-compatible provider requests.

## openclaw-openclaw-47243 — feat(ui): add timestamp and preview to session list

- labels: `sessions, ui_tui`
- `sessions`: The feature changes session-list data handling, adding lastMessagePreview to GatewaySessionRow and requesting includeLastMessage for sessions.list.
- `ui_tui`: The main user-visible change is rendering timestamps and message previews in the web UI session list.

## openclaw-openclaw-73910 — BUG: OpenClaw-managed Codex ACP uses isolated CODEX_HOME without auth bridge and sends unsupported timeout config

- labels: `acp, acpx, auth_identity, codex, config`
- `acp`: The bug is in OpenClaw-managed Codex ACP sessions and ACP session/set_config_option handling.
- `acpx`: The repro compares direct ACPX to the OpenClaw-managed ACPX path and cites the ACPX plugin schema.
- `auth_identity`: The main failure is isolated CODEX_HOME lacking Codex authentication and needing an auth bridge or setup flow.
- `codex`: The affected agent is explicitly Codex ACP / Codex ACP adapter.
- `config`: Codex rejects an unsupported timeout config option sent by the managed path.

## openclaw-openclaw-44379 — fix(pi-runner): harden context-overflow recovery with one suppress-hook retry

- labels: `agent_runtime, hooks, memory, reliability`
- `agent_runtime`: Changes the embedded PI runner run loop and retry behavior for context-overflow recovery.
- `hooks`: Adds a bounded retry with prompt-hook context injection suppressed.
- `memory`: The overflow is attributed to external memory/prompt-hook context injections, including memory-core involvement.
- `reliability`: Explicitly hardens recovery, reduces hard failures/stalls, and normalizes overflow stop reasons.

## openclaw-openclaw-63229 — Bug: Gateway falsely marks healthy local vLLM endpoints as timed out/overloaded, causing 1–23 min fallback cascades

- labels: `gateway, local_models, model_serving, reliability`
- `gateway`: The bug is in the gateway's fallback/routing subsystem and includes gateway timeouts, draining, and session spawn failures.
- `local_models`: The affected endpoints are local vLLM/GPU-served Gemma and Qwen models responding quickly via direct curl.
- `model_serving`: The issue concerns vLLM model endpoints, request routing, provider failover, timeout classification, and overloaded cooldown behavior.
- `reliability`: Core failure is false timeout/overload detection causing long fallback cascades, latency, and unresponsive gateway symptoms.

## openclaw-openclaw-62428 — test(exec): land exec v2 contract follow-through

- labels: `exec_tools, approvals, security, tests_ci`
- `exec_tools`: PR is explicitly about Exec V2 contracts, allowlists, safeBins, command matching, and exec runtime policy.
- `approvals`: Changes and tests cover exec approvals, allowlist mode, allow-always decisions, and effective approval policy merging.
- `security`: Safe-bin trust, rejected bins, trusted-dir filtering, command-contract hardening, and security audit coverage are central.
- `tests_ci`: Title and body emphasize landing contract tests, with many new and updated exec/security test files.

## openclaw-openclaw-72133 — Feature request: per-message token/cost metadata in mobile app and channel surfaces

- labels: `telemetry_usage, ui_tui, chat_integrations`
- `telemetry_usage`: Central request is exposing per-message token counts, cost/cache, context percentage, and model metadata.
- `ui_tui`: Asks to show the metadata in the Control UI-derived mobile/native chat view as per-message footer/status UI.
- `chat_integrations`: Explicitly requests optional footers in channel surfaces such as Signal, iMessage, Telegram, and BlueBubbles.

## openclaw-openclaw-70518 — fix(config): add heartbeat skill allowlist

- labels: `config, cron_automation, skills_plugins`
- `config`: Adds new heartbeat configuration fields, schema/help/labels/types, and documented config surface.
- `cron_automation`: The behavior is specifically for periodic heartbeat runs and the heartbeat runner.
- `skills_plugins`: Introduces a heartbeat-specific allowSkills allowlist that restricts loaded skills for those runs.

## openclaw-openclaw-10467 — [Feature Request]: Multi-lane concurrency support for sub-agents via sessions_spawn

- labels: `coding_agents, sessions, queueing, config`
- `coding_agents`: Feature targets sub-agent orchestration and multi-agent workflows spawned by agents.
- `sessions`: The requested change is an optional lane parameter on the sessions_spawn tool and mentions session file locks.
- `queueing`: Core problem is a single subagent queue lane, lane exhaustion, concurrency limits, and independent queue lanes.
- `config`: Proposal requires per-lane maxConcurrent settings in openclaw.json and schema/default compatibility.

## openclaw-openclaw-83333 — [Bug]: Memory provider cutover to Ollama leaves production index in mixed OpenAI/Ollama vector state after live sync/reload

- labels: `memory, self_hosted_inference, reliability`
- `memory`: The issue is about the production memory index, memorySearch, embedding vectors, status, and failed canary search.
- `self_hosted_inference`: It specifically concerns switching embeddings to an Ollama-backed local/container provider for memory search.
- `reliability`: The bug is an inconsistent mixed vector state after live sync/reload, requiring rollback and indicating stale or failed reindex behavior.

## openclaw-openclaw-80475 — test(acpx): accept built-dist MCP server resolution when dist exists

- labels: `acpx, mcp_tooling, tests_ci`
- `acpx`: The change is explicitly in extensions/acpx and updates ACPx config test behavior.
- `mcp_tooling`: It concerns built-in MCP server argument/path resolution for plugin-tools and openclaw-tools servers.
- `tests_ci`: The PR only updates a Vitest helper in config.test.ts and provides test-run evidence.

## openclaw-openclaw-84668 — docs(agent-runtimes): clarify model name vs runtime routing for Codex (#84637)

- labels: `docs, agent_runtime, codex`
- `docs`: Documentation-only PR modifying docs/concepts/agent-runtimes.md with a warning and audit guidance.
- `agent_runtime`: Clarifies runtime routing via agentRuntime.id and distinguishes runtime selection from model fallbacks.
- `codex`: Explicitly addresses Codex runtime/harness confusion with gpt-*-codex model IDs and Codex-named surfaces.

## openclaw-openclaw-69260 — Harden Gemini ACP integration against ambient API-key fallback and add generic auth-contract hooks for ACP agents

- labels: `acp, auth_identity, hooks, security`
- `acp`: Issue is about Gemini ACP integration and auth contracts for ACP-backed agents/routes.
- `auth_identity`: Central concern is preventing drift between OAuth-personal and API-key auth modes and declaring expected auth contracts.
- `hooks`: Requests generic auth-contract and integration-level env-scrubbing hooks for ACP launches.
- `security`: Framed as hardening against ambient API-key fallback, credential env inheritance, and fail-closed behavior.

## openclaw-openclaw-68725 — feat(amazon-bedrock-mantle): add known context windows for open-weight Mantle models

- labels: `local_model_providers, open_weight_models`
- `local_model_providers`: Changes provider discovery metadata for an OpenAI-compatible Mantle backend, including model context-window resolution.
- `open_weight_models`: The lookup is explicitly for open-weight model families such as Qwen, DeepSeek, GLM, Nemotron, and MiniMax.

## openclaw-openclaw-49502 — feat(gateway): include usage/cost metadata in agent.wait terminal response

- labels: `gateway, api_surface, telemetry_usage`
- `gateway`: Feature is explicitly scoped to gateway handlers and modifies src/gateway server methods for agent.wait.
- `api_surface`: Adds an optional meta field to the agent.wait WebSocket terminal response contract.
- `telemetry_usage`: Surfaces token usage, last-call usage, estimated cost, provider, and model metadata.

## openclaw-openclaw-63826 — security: fix HIGH/CRITICAL vulns in skill scanner, SSRF, hook priority, and token verification

- labels: `security, skills_plugins, hooks, auth_identity, local_model_providers`
- `security`: PR explicitly fixes HIGH/CRITICAL vulnerabilities including scanner bypass, SSRF, hook bypass, and token revocation TOCTOU.
- `skills_plugins`: Central fixes affect the skill scanner and plugin registry behavior for potentially malicious external plugins.
- `hooks`: One vulnerability and fix directly caps hook priority to prevent security-critical hook bypass.
- `auth_identity`: Device token revocation and verifyDeviceToken behavior are authentication/identity token handling issues.
- `local_model_providers`: SSRF fix is in OpenAI-compatible local provider discovery using user-provided baseUrl/provider setup.

## openclaw-openclaw-84719 — fix: preserve active webhook request counters

- labels: `api_surface, reliability, skills_plugins`
- `api_surface`: Changes webhook request-guard behavior, part of the webhook request handling/API contract.
- `reliability`: Fix preserves active in-flight counters and rejects new keys at capacity, preventing stale/incorrect limiter state.
- `skills_plugins`: The implementation is in src/plugin-sdk webhook request guards, affecting plugin SDK webhook handling.

## openclaw-openclaw-80431 — ACPx plugin-tools MCP config test expects source path but resolver returns dist path

- labels: `acpx, mcp_tooling, tests_ci`
- `acpx`: The failing test is in extensions/acpx/src/config.test.ts and concerns embedded ACPx plugin config.
- `mcp_tooling`: The mismatch is for injecting the built-in plugin-tools MCP server and its resolved MCP server entrypoint.
- `tests_ci`: The issue is a pnpm test failure caused by expected versus received resolver paths in a config test.

## openclaw-openclaw-42027 — fix: resolve exec PATH fallback, layered browser diagnostics, and cron force-run deadlock

- labels: `exec_tools, browser_automation, cron_automation, queueing, reliability`
- `exec_tools`: Exec tool PATH recovery is changed in bash-tools.exec.ts for local fallback execution.
- `browser_automation`: Browser status diagnostics cover profile attach mode, CDP reachability, and browser HTTP errors.
- `cron_automation`: Fixes detached cron.run --force behavior for cron jobs.
- `queueing`: Introduces/separates a CronManual lane so manual force-runs do not block the cron lane.
- `reliability`: Addresses fallback misbehavior and a cron self-deadlock that caused timeouts and broken-tool symptoms.

## openclaw-openclaw-39248 — Bug: sandbox.mode: "non-main" silently breaks sessions_spawn subagent initialization

- labels: `coding_agents, agent_runtime, sessions, sandboxing, reliability`
- `coding_agents`: Issue affects subagent orchestration in the coding-agent workflow via sessions_spawn.
- `agent_runtime`: Subagents are accepted but never initialize or execute, a core agent lifecycle/runtime failure.
- `sessions`: The failure centers on sessions_spawn, childSessionKey, sessions_history, transcripts, and session state.
- `sandboxing`: The bug is triggered by agents.defaults.sandbox.mode="non-main" and Docker sandbox initialization.
- `reliability`: Symptoms include silent stalls, missing logs, no progress, and eventual timeout.

## openclaw-openclaw-84660 — [Bug] Voice STT: empty moonshine transcripts passed as raw JSON to LLM, clogging serialized processing queue

- labels: `chat_integrations, self_hosted_inference, queueing, reliability`
- `chat_integrations`: Bug occurs in Discord voice STT, affecting the bot's responsiveness in a voice channel.
- `self_hosted_inference`: Central issue is handling STT output from moonshine/sherpa-onnx speech transcription.
- `queueing`: Empty transcripts clog the serialized processingQueue and block later voice segments.
- `reliability`: Empty/noisy transcript handling makes the pipeline appear stopped and causes message loss/unresponsiveness.

## openclaw-openclaw-46552 — docs(queue): clarify steer behavior with partial streaming and tool boundaries

- labels: `docs, queueing, tool_calling`
- `docs`: PR only changes docs/concepts/queue.md and adds/clarifies documentation sections.
- `queueing`: The documented behavior is queue steer mode, per-session queue overrides, and followup fallback.
- `tool_calling`: It explicitly clarifies tool-boundary semantics: in-flight tool calls complete before steer takes effect.

## openclaw-openclaw-44202 — [Bug]: local memory embeddings on Apple Silicon can crash gateway in ggml-metal / node-llama-cpp; need official Metal/GPU guidance

- labels: `gateway, local_models, self_hosted_inference, memory, reliability`
- `gateway`: The reported failure repeatedly crashes the OpenClaw gateway during restart/shutdown.
- `local_models`: The crash is in local GGUF/node-llama-cpp/ggml-metal execution on Apple Silicon GPU/Metal.
- `self_hosted_inference`: The issue centers on locally operated embedding inference via a local memory provider.
- `memory`: Local memory embeddings, memory search, indexing, chunks, and vector readiness are central to the report.
- `reliability`: It describes crash loops, native assertions, recovery steps, and mitigations for a restart/shutdown failure.

## openclaw-openclaw-75657 — fix: local GGUF embedding model warmup blocks Node.js event loop for minutes on startup (ARM64/Pi)

- labels: `gateway, local_models, memory, reliability`
- `gateway`: The bug occurs during Gateway startup and makes the Gateway/WebSocket service unreachable until ready.
- `local_models`: The issue centers on local GGUF model loading via node-llama-cpp on ARM64/Pi hardware.
- `memory`: The local model is used for memorySearch/local embedding provider behavior.
- `reliability`: Startup event-loop blocking causes timeouts, liveness warnings, and an unreachable service for minutes.

## openclaw-openclaw-84570 — Remove skill prelude exec allowlist

- labels: `approvals, exec_tools, skills_plugins`
- `approvals`: PR removes an exec-approval allowlist exception and makes legacy skill prelude chains go through the normal approval flow.
- `exec_tools`: Change centers on shell/exec allowlist evaluation for command chains such as cat/printf plus a skill wrapper.
- `skills_plugins`: Behavior is specifically about trusted skill wrapper execution, SKILL.md preludes, and autoAllowSkills.

## openclaw-openclaw-84413 — [Bug]: 2026.5.18 Codex Chrome DevTools MCP sidecars accumulate under gateway and drive cgroup memory growth

- labels: `codex, gateway, mcp_tooling, reliability`
- `codex`: Issue explicitly concerns embedded Codex runs and the Codex app-server spawning sidecars.
- `gateway`: Unreaped child processes accumulate under the OpenClaw gateway service cgroup and clear on gateway restart.
- `mcp_tooling`: The leaking sidecars are repeated chrome-devtools-mcp server trees managed as MCP tooling.
- `reliability`: Bug is a lifecycle cleanup/resource leak causing memory growth and potential crash-loop behavior.

## openclaw-openclaw-82507 — [Feature]: ACPX Codex sandbox should inherit user-installed plugins (e.g. Superpowers)

- labels: `acpx, codex, sandboxing, skills_plugins`
- `acpx`: Issue is specifically about ACPX background tasks and the ACPX Codex home path.
- `codex`: The affected adapter and home directory are Codex-specific, including CODEX_HOME and Codex ACP.
- `sandboxing`: Core problem is the isolated Codex sandbox home not inheriting user state.
- `skills_plugins`: Requested behavior is to inherit or allow Codex plugins/skills such as Superpowers and marketplaces.

## openclaw-openclaw-82596 — Feature/exec denylist

- labels: `approvals, exec_tools, security`
- `approvals`: Adds a new exec approval/security mode and updates approval evaluators, prompts, stores, and docs.
- `exec_tools`: Core behavior is denying model-initiated shell exec commands such as curl/wget via exec tool policy.
- `security`: Denylist is explicitly a security boundary to prevent unsafe network-fetch bypasses and fail closed on malformed rules.

## openclaw-openclaw-64718 — fix(security): default exec to deny for non-owner auto-reply senders

- labels: `security, exec_tools, approvals, auth_identity`
- `security`: PR is explicitly a security hardening fix preventing unauthenticated non-owner senders from triggering arbitrary exec via prompt injection.
- `exec_tools`: Core behavior changes resolveReplyExecOverrides and defaults exec tool security to deny for non-owner auto-replies.
- `approvals`: The fix changes approval behavior from ask=off to ask=always where no approval UI/gate existed for non-owner senders.
- `auth_identity`: Policy depends on senderIsOwner and distinguishes owner sessions from unauthenticated/non-owner channel senders.

## openclaw-openclaw-81488 — Harden node exec approval precheck env [AI]

- labels: `approvals, exec_tools, security`
- `approvals`: PR directly changes node exec approval precheck analysis so commands do not incorrectly skip approval.
- `exec_tools`: The affected path is node-host command execution via system.run, command allowlist matching, and PATH resolution for exec tools.
- `security`: Marked as security hardening and prevents gateway-local PATH from satisfying node command approval checks.

## openclaw-openclaw-40332 — [Feature]: Per-binding and per-agent permissionMode for ACP sessions

- labels: `acp, acpx, approvals, config, security`
- `acp`: Feature is explicitly for ACP sessions, bindings, and agent runtime ACP override precedence.
- `acpx`: Current global setting is under the acpx plugin config and fallback remains plugins.entries.acpx.config.permissionMode.
- `approvals`: Core setting is permissionMode with approve-all and approve-reads behaviors controlling allowed actions.
- `config`: Request is to add per-binding and per-agent configuration overrides plus fallback precedence.
- `security`: Motivation is least-privilege scoping across agents with different trust levels, avoiding global over-provisioning.

## openclaw-openclaw-78528 — Security: skill SecretRef API keys still leak into exec child environments

- labels: `security, exec_tools, skills_plugins, auth_identity`
- `security`: Issue is explicitly a security regression where SecretRef API keys leak into child process environments.
- `exec_tools`: Leak occurs through commands spawned by the generic exec tool inheriting process.env.
- `skills_plugins`: The affected secrets are skill entry SecretRefs under skills.entries.<skill>.apiKey.
- `auth_identity`: The bug concerns API key/credential scope: skill-scoped credentials become process-wide.

## openclaw-openclaw-82145 — cron: allow retries for local model preflight

- labels: `cron_automation, local_model_providers, config, reliability`
- `cron_automation`: Change targets isolated cron jobs and how scheduled runs preflight before starting agent turns.
- `local_model_providers`: Preflight probes local/private providers such as Ollama, vLLM, SGLang, and LM Studio via provider endpoints.
- `config`: Adds configurable cron.modelPreflight timeoutMs, maxAttempts, and retryDelayMs schema/help/docs.
- `reliability`: Retries and timeout controls address sleeping or cold-starting providers being incorrectly marked skipped.

## openclaw-openclaw-74204 — memory.qmd.update.embedTimeoutMs default (120 s) is too low for local GGUF; error message doesn't surface the fix

- labels: `config, local_models, memory, reliability`
- `config`: Issue centers on the `memory.qmd.update.embedTimeoutMs` config default and making the override discoverable.
- `local_models`: Failure is specific to a local GGUF embedding model on CPU commodity hardware needing longer timeout.
- `memory`: QMD memory embedding and hybrid/vector memory search are the affected subsystem.
- `reliability`: The default timeout repeatedly kills embedding runs, causing backoff loops and disabled vector search.

## openclaw-openclaw-84709 — fix(cron): fail closed when required tools are unavailable

- labels: `codex, cron_automation, exec_tools, reliability`
- `codex`: PR modifies extensions/codex app-server runtime and explicitly fixes Codex native/dynamic tool surface behavior.
- `cron_automation`: Central behavior is cron isolated-agent jobs and cron allowlists failing before model dispatch.
- `exec_tools`: Fix concerns required runtime tools such as exec/read, tool allowlists, and dynamic tool surface availability.
- `reliability`: Adds fail-closed TOOL_SURFACE_UNAVAILABLE handling and prevents false healthy summaries when required tools are missing.

## openclaw-openclaw-81249 — [Feature/Bug]: Local Ollama embeddings fail when proxy is enabled (SSRF defenses ignore NO_PROXY)

- labels: `config, local_models, security, self_hosted_inference`
- `config`: Requests a new openclaw.json proxy bypass setting and notes schema validation rejects an attempted bypass key.
- `local_models`: Issue centers on local Ollama on loopback and local LLM traffic being incorrectly routed through a proxy.
- `security`: The requested change affects SSRF defenses, NO_PROXY stripping, and secure loopback whitelist behavior.
- `self_hosted_inference`: Local Ollama embeddings on a self-hosted/headless deployment fail due to proxy routing and NO_PROXY handling.

## openclaw-openclaw-55888 — [Feature]: 🚀 [Performance Insight] Unlocking 26.7k Context Window on M4 Pro: Fixing the 8k Compaction Lag (64GB RAM Only)

- labels: `config, local_models, memory`
- `config`: The proposed fix is an openclaw.json agents.defaults.compaction configuration override and discusses config hierarchy/defaults.
- `local_models`: The report centers on a local Ollama Qwen model running on M4 Pro hardware with RAM/context-window constraints.
- `memory`: It specifically targets memoryFlush, compaction, summarization thresholds, and retained context behavior.

## openclaw-openclaw-84648 — Add SafeOps preflight hook for exec tool

- labels: `exec_tools, hooks, security`
- `exec_tools`: PR modifies the exec tool path before command dispatch and process execution.
- `hooks`: Title and body explicitly add a SafeOps preflight hook before tool execution.
- `security`: SafeOps preflight is a security-boundary check with secret scan and denial behavior tied to adapter token state.

## openclaw-openclaw-54471 — fix(acp): add system_event stream relay to parent session for ACP spawn

- labels: `acp, sessions, notifications`
- `acp`: Title and change explicitly fix ACP spawn handling and ACP system_event stream relay.
- `sessions`: The bug occurs when sessions_spawn creates an ACP session with streamTo parent, affecting parent-session relay.
- `notifications`: The fix restores delivery of clarifying questions and progress updates so users receive the missing notifications.

## openclaw-openclaw-71646 — mcp/channel-bridge: pendingClaudePermissions / pendingApprovals leak — no TTL, no close-clear, no cap

- labels: `mcp_tooling, approvals, reliability`
- `mcp_tooling`: Issue is in src/mcp/channel-bridge.ts and affects long-running `openclaw mcp serve` behavior.
- `approvals`: Central leak involves `pendingApprovals`, `pendingClaudePermissions`, permission requests, and approval resolved events.
- `reliability`: Reports unbounded pending Map growth due to missing TTL, close-clear, and cap in a long-running process.

## openclaw-openclaw-70529 — [Bug]: Desktop cannot use existing Chrome sessions: EasyClaw Google sign-in fails, and user profile attach fails with spawn npx ENOENT

- labels: `auth_identity, browser_automation, exec_tools, packaging_deployment`
- `auth_identity`: Google OAuth sign-in for the EasyClaw browser extension fails after callback.
- `browser_automation`: The bug blocks attaching to existing Chrome sessions and using browser tabs for agent control.
- `exec_tools`: The attach path fails when Desktop tries to spawn the `npx` executable and gets ENOENT.
- `packaging_deployment`: The Desktop app bundle ships `node` but not `npm`/`npx`, causing the packaged runtime failure.

## openclaw-openclaw-84038 — [Bug]: doctor --fix silently migrates intentional openai-codex/ config to openai/, breaking PI+OAuth runtime and causing 3-4x token inflation

- labels: `config, codex, agent_runtime, auth_identity`
- `config`: The bug is about `doctor --fix` silently migrating configured model routes and removing config entries.
- `codex`: The issue explicitly concerns `openai-codex/` routes and the native Codex runtime.
- `agent_runtime`: A configured `agentRuntime: { id: "pi" }` override is removed, switching users to a different runtime.
- `auth_identity`: The regression affects PI+OAuth usage and includes `auth.order` provider/account configuration.

## openclaw-openclaw-71216 — Config schema: add `sandbox`, `routing.rules`, `instances`, and `gateway.nodes.denyPaths`

- labels: `config, gateway, local_model_providers, sandboxing, security`
- `config`: The issue explicitly asks to extend the config schema with sandbox, routing.rules, instances, and gateway.nodes.denyPaths.
- `gateway`: Several requested settings are enforced by the gateway, including multi-gateway instances and gateway.nodes.denyPaths.
- `local_model_providers`: routing.rules is for tag-based provider selection between cloud providers and a local Ollama provider.
- `sandboxing`: sandbox.mode is a requested global mode for tool-execution boundaries and refusal behavior.
- `security`: denyPaths and sensitivity-based routing are framed as preventing access to credentials, SSH keys, secrets, and sensitive data.

## openclaw-openclaw-45200 — fix(subagents): notify user on announce give-up instead of silently dropping result

- labels: `coding_agents, notifications, reliability`
- `coding_agents`: The fix is in subagent-registry and changes subagent announce/give-up handling.
- `notifications`: Adds a last-resort user notification when announce delivery retries are exhausted.
- `reliability`: Addresses silent result loss after retry-limit and adds auditable best-effort recovery behavior.

## openclaw-openclaw-60381 — browser tool: add force parameter for click and expose evaluate action

- labels: `browser_automation, api_surface, security`
- `browser_automation`: Issue is specifically about the Playwright-based browser tool, click behavior, and page.evaluate web interaction support.
- `api_surface`: Proposes adding a new click parameter and exposing an evaluate action, changing the browser tool action contract.
- `security`: Discusses blocked javascript: navigation as an injection vector and arbitrary JavaScript execution via a gated evaluate escape hatch.

## openclaw-openclaw-42122 — Speed up install smoke Docker builds

- labels: `packaging_deployment, tests_ci`
- `packaging_deployment`: Changes the Dockerfile build path and pnpm UI build behavior for Docker image construction.
- `tests_ci`: Modifies the install-smoke GitHub Actions workflow to speed CI smoke Docker builds.

## openclaw-openclaw-83863 — ACP/Codex child tasks can be marked succeeded with progress-only output and no final deliverable

- labels: `acp, codex, coding_agents, agent_runtime, reliability`
- `acp`: The failure is explicitly in ACP child sessions and ACP manager done-event handling.
- `codex`: The issue specifically concerns Codex ACP child tasks returning only progress text.
- `coding_agents`: It affects parent/child agent workflows, subagents, task ledgers, and final-deliverable contracts.
- `agent_runtime`: The core bug is child task lifecycle/status being marked succeeded without a final deliverable.
- `reliability`: Incorrect success state after delivery retry failure creates silent failure and message-loss behavior.

## openclaw-openclaw-48580 — Bug: acpx codex sessions 创建的会话立即退出 - stdin is not a terminal

- labels: `acpx, codex, sessions, reliability`
- `acpx`: The failing command is `acpx codex sessions new`, and logs show ACPX spawning and initializing the agent.
- `codex`: The affected backend is Codex CLI / `codex-acp`, with a Codex-specific TTY requirement.
- `sessions`: The bug is about a newly created session showing `closed: false` with a stale PID after the process exits.
- `reliability`: It describes stale session state and missing liveness/cleanup when the spawned process immediately dies.

## openclaw-openclaw-84637 — [Bug]: Codex runtime/harness is too easy to confuse with gpt-*-codex model fallbacks

- labels: `codex, agent_runtime, config, sessions`
- `codex`: Issue explicitly distinguishes Codex runtime/harness from Codex-named model IDs.
- `agent_runtime`: Central problem is runtime/harness routing via agentRuntime.id and keeping sessions on Pi vs Codex runtime.
- `config`: Repeated churn involves model fallback policy and provider/model agentRuntime configuration.
- `sessions`: Impact and repro focus on normal sessions being routed/persisted with the intended runtime state.

## openclaw-openclaw-43765 — Improve runtime recovery for heartbeat, Feishu, and exec sessions

- labels: `chat_integrations, cron_automation, exec_tools, gateway, reliability`
- `chat_integrations`: Feishu websocket channel state and monitoring are central to the PR.
- `cron_automation`: Heartbeat runs now consume and requeue exec system events to avoid replay loops.
- `exec_tools`: Exec/process tooling terminal status and non-zero foreground exit handling are explicitly changed.
- `gateway`: The generic gateway channel-health monitor restarts stale or disconnected channel sockets.
- `reliability`: The PR focuses on runtime recovery, stale socket restart, replay prevention, and failure handling.

## openclaw-openclaw-83982 — fix(clawhub): preserve base URL path prefix [AI-assisted]

- labels: `api_surface, config, skills_plugins`
- `api_surface`: Fixes ClawHub API request URL construction so endpoints include the configured path prefix.
- `config`: Behavior depends on configured OPENCLAW_CLAWHUB_URL/CLAWHUB_URL baseUrl environment values.
- `skills_plugins`: ClawHub requests are used for skill/plugin discovery such as searchClawHubSkills.

## openclaw-openclaw-48406 — Docs: add saturated session recovery guide

- labels: `docs, memory, sessions`
- `docs`: Title and body explicitly say this is a documentation PR adding an operator-facing saturated-session recovery guide and updating reference docs.
- `sessions`: The core subject is saturated session recovery, session compaction, transcripts, and recommend-reset behavior.
- `memory`: The compaction/recovery docs reference memoryFlush and durable memory preservation during session compaction/recovery.

## openclaw-openclaw-72001 — fix(hooks): write allowedSessionKeyPrefixes from gmail wizard

- labels: `hooks, gateway, config`
- `hooks`: PR fixes Gmail hook setup and hook preset/sessionKey validation behavior.
- `gateway`: Bug is that the gateway refused to load the emitted hooks config on restart.
- `config`: Change writes hooks.allowedSessionKeyPrefixes into openclaw.json setup output.

## openclaw-openclaw-81200 — fix(acpx): strip provider API keys from child harness env

- labels: `acpx, acp, security, auth_identity`
- `acpx`: PR is explicitly in extensions/acpx and changes ACPX wrapper launch behavior.
- `acp`: It modifies built-in Claude and Gemini ACP harness launches and ACP aliases.
- `security`: The fix prevents provider API keys and selector env vars from leaking into child processes.
- `auth_identity`: The core change handles provider authentication environment variables such as ANTHROPIC_API_KEY and GEMINI_API_KEY.

## openclaw-openclaw-84763 — fix(acpx): scrub provider credential env from ACP harness spawns

- labels: `acpx, acp, auth_identity, security, config`
- `acpx`: PR is explicitly under extensions/acpx and changes ACPX runtime/process launch decoration.
- `acp`: Bug occurs in sessions_spawn with runtime:"acp" and ACP harness children such as claude/codex/gemini.
- `auth_identity`: Core fix addresses OAuth/API-key credential scope so spawned harnesses use their own auth instead of gateway credentials.
- `security`: It scrubs provider credential/token environment variables from child processes and is described as security hardening.
- `config`: Adds the acp.scrubProviderEnv configuration knob and updates config schema/help metadata.

## openclaw-openclaw-48940 — ACP: add gateway-owned node-backed runtime

- labels: `acp, gateway, agent_runtime, sessions, reliability`
- `acp`: Title and body explicitly add a node-backed ACP runtime and ACP worker/event paths.
- `gateway`: The gateway owns durable state, ingests worker events, and controls node-backed ACP runs.
- `agent_runtime`: Adds a real node-host execution worker bridge and runtime lifecycle for ACP work.
- `sessions`: Durable ACP store persists sessions, runs, replay targets, terminal state, and checkpoints.
- `reliability`: Focuses on restart, replay, reconnect, cancel, close race hardening, and recovery behavior.

## openclaw-openclaw-80479 — feat(memory/embeddings): add openai-compatible provider for self-hosted servers (llama.cpp, Ollama, vLLM, TGI, LocalAI)

- labels: `local_model_providers, memory, self_hosted_inference`
- `local_model_providers`: Adds an `openai-compatible` provider with baseUrl/model/apiKey behavior for local/OpenAI-compatible backends like Ollama, vLLM, TGI, and LocalAI.
- `memory`: The feature is specifically a memory-lancedb embedding provider and adapter for memory embeddings.
- `self_hosted_inference`: Targets self-hosted/local HTTP embedding servers and private inference deployments rather than cloud OpenAI.

## openclaw-openclaw-56866 — feat(whatsapp): ACP session binding with media threading and prompt fixes

- labels: `acp, chat_integrations, hooks, sessions`
- `acp`: PR explicitly adds WhatsApp support for configured ACP bindings, ACP dispatch, prompts, and sessions.
- `chat_integrations`: The feature is for the WhatsApp channel integration and message flow.
- `hooks`: Adds before_prompt_build and plugin lifecycle hook dispatch in the ACP flow.
- `sessions`: Centers on ACP session binding, session routing, and long-lived session behavior for conversations.

## openclaw-openclaw-80783 — Policy: add model, network, and MCP conformance checks

- labels: `config, local_model_providers, mcp_tooling, security, skills_plugins`
- `config`: PR adds policy.jsonc config-level conformance checks over existing OpenClaw settings and config evidence.
- `local_model_providers`: Adds model-provider evidence plus models.providers allow/deny policy support for configured providers and refs.
- `mcp_tooling`: Adds MCP server evidence and allow/deny checks for OpenClaw-managed MCP servers.
- `security`: Adds private-network SSRF posture checks and URL credential redaction in policy evidence.
- `skills_plugins`: Changes are in the bundled Policy plugin/extension and its doctor health-check registration.

## openclaw-openclaw-84681 — fix(codex): stabilize heartbeat dynamic tool schema

- labels: `codex, sessions, tool_calling`
- `codex`: Title and changed files are explicitly in extensions/codex app-server and concern Codex runtime compatibility.
- `sessions`: Fix prevents Codex thread rotation so normal and heartbeat turns reuse the same thread/session binding.
- `tool_calling`: Central change separates durable dynamic tool schemas from current-turn callable tools and handles heartbeat_respond tool availability.

## openclaw-openclaw-53319 — [Bug]: ACP concurrent session spawns — first agent fails to launch CC process

- labels: `acp, acpx, sessions, reliability`
- `acp`: Issue explicitly uses ACP session spawning via sessions_spawn runtime:"acp" and describes ACP backend behavior.
- `acpx`: The configured ACP backend is acpx, with analysis pointing to the acpx CLI launch path and acpx concurrent handling.
- `sessions`: Bug centers on concurrent child session spawns, childSessionKey handling, and session initialization state.
- `reliability`: Describes a race condition where one agent silently fails to start, stalls, or crashes during concurrent initialization.

## openclaw-openclaw-56442 — feat: Add opt-in ACP parent completion notify for sessions_spawn

- labels: `acp, sessions, notifications, api_surface`
- `acp`: Explicitly adds ACP behavior for sessions_spawn with ACP mode:"run" parent completion handling.
- `sessions`: Change centers on parent/requester and child session completion routing for sessions_spawn.
- `notifications`: Adds opt-in parentUpdates:"notify" completion announce path and fallback delivery behavior.
- `api_surface`: Introduces a new sessions_spawn parameter and updates the gateway protocol schema/request contract.

## openclaw-openclaw-84567 — [Bug]: Codex bundled harness initialize still hangs in 2026.5.18 isolated cron — surfaces via #64744 timeout-wrapping as 'isolated agent setup timed out before runner start'

- labels: `codex, cron_automation, agent_runtime, reliability`
- `codex`: Issue explicitly concerns the bundled Codex harness and openai-codex plugin/model routing.
- `cron_automation`: Failure occurs in recurring/manual cron jobs with payload.kind agentTurn and cron run/get commands.
- `agent_runtime`: The hang is during agent setup before runner start in the bundled harness initialize path.
- `reliability`: Bug is a regression involving deterministic hangs/timeouts and crash-loop style repeated failures.

## openclaw-openclaw-51654 — Support session-level environment variables for ACP sessions

- labels: `acp, acpx, sessions, auth_identity, security`
- `acp`: The feature targets ACP sessions and adds an env parameter to sessions_spawn with runtime "acp".
- `acpx`: The issue says ACP sessions run via the acpx runtime and require injecting env vars into the acpx subprocess.
- `sessions`: The requested behavior is session-specific or per-spawn environment variables and preserved OpenClaw session management.
- `auth_identity`: Primary use cases include different API keys, auth provider endpoints, and temporary scoped credentials per session.
- `security`: The issue explicitly involves multi-tenant environment isolation and credential handling, with security-review labels.

## openclaw-openclaw-84337 — [Bug]: Hook ingress token unlocks password-mode gateway auth

- labels: `security, auth_identity, gateway, hooks`
- `security`: Describes a high-severity auth bypass vulnerability with CVSS impact and security-review labels.
- `auth_identity`: Core bug is credential confusion where a hook bearer token authenticates as gateway password auth.
- `gateway`: Affected behavior is password-mode Gateway HTTP authentication and operator access.
- `hooks`: The bypass originates from hook ingress token handling and hook routing controls.

## openclaw-openclaw-84477 — Discord embedded-run prep wedge before strict-agentic, recovery skips sessionId=unknown lanes

- labels: `agent_runtime, chat_integrations, queueing, reliability, sessions`
- `agent_runtime`: Issue centers on embedded agent-run prep wedging before the strict-agentic execution contract and missing agent lifecycle events.
- `chat_integrations`: The reproduced surface is the Discord channel via @openclaw/discord.
- `queueing`: Known and unknown session lanes get stuck, skipped by recovery, and cleared only by lane suspension or restart.
- `reliability`: Core symptom is a persistent wedge/stall with recovery gaps, abort behavior, and re-wedging after restart.
- `sessions`: Behavior differs by known versus unknown sessionId lanes and involves session-pinned routing and session write locks.

## openclaw-openclaw-39714 — Sandbox: fix Dockerized browser bridge and tab creation

- labels: `sandboxing, browser_automation, reliability`
- `sandboxing`: Fixes Docker sandbox container reachability, host-gateway aliases, and sandbox context/browser bridge URLs.
- `browser_automation`: Central changes affect the browser bridge, CDP tab creation, remote profiles, and browser open/status behavior.
- `reliability`: Addresses unreachable 127.0.0.1 bridge URLs and Playwright newPage timeouts causing browser operations to fail.

## openclaw-openclaw-71803 — CLI watchdog kills sessions that are correctly idle while waiting on a Monitor task

- labels: `agent_runtime, exec_tools, reliability, sessions`
- `agent_runtime`: The issue concerns the agent/cli-backend watchdog terminating the CLI agent process during an embedded agent run.
- `exec_tools`: The failure occurs while waiting on a Monitor tool managing a long-running shell command such as Whisper, ffmpeg, or builds.
- `reliability`: A healthy idle state is misclassified as a timeout, causing premature process termination and crash-loop style failure.
- `sessions`: The watchdog kill destroys the in-flight agent session and prevents later resume of the Monitor result.

## openclaw-openclaw-45393 — fix(errors): friendly message and last-message repair for tool_use/tool_result mismatch (#45385)

- labels: `tool_calling, reliability, sessions, security`
- `tool_calling`: Core fix is for Anthropic `tool_use`/`tool_result` mismatch handling and dangling tool-call blocks.
- `reliability`: Repairs timeout/race/last-message edge cases that caused rejected conversations and raw errors.
- `sessions`: Fixes corrupted session history/last-message state and advises starting a fresh session if needed.
- `security`: Diff adds inbound media read wrapping with untrusted-data markers to prevent prompt injection.

## openclaw-openclaw-68187 — SSE-backed MCP sessions can stay stale after server restart and fail with 'Session not found'

- labels: `mcp_tooling, sessions, gateway, reliability`
- `mcp_tooling`: Issue is about MCP integrations using an SSE-backed MCP server and MCP-backed tools.
- `sessions`: Central failure is stale client/proxy session state and 'Session not found' after restart.
- `gateway`: Observed behind the OpenClaw gateway/proxy layer and workaround is restarting the gateway.
- `reliability`: Expected behavior is automatic recovery/reconnect after downstream server restart instead of stale failure.

## openclaw-openclaw-45508 — [Feature]: Self-hosted STT/TTS provider support in webchat (Route webchat TTS through the gateway instead of browser Speech API)

- labels: `self_hosted_inference, chat_integrations, gateway, config`
- `self_hosted_inference`: Issue explicitly requests self-hosted STT/TTS provider support, including local Whisper-compatible and OpenAI-compatible audio stacks.
- `chat_integrations`: The affected surface is webchat, specifically Read aloud and mic/voice input behavior.
- `gateway`: Core proposal is to route webchat TTS/STT through the gateway instead of browser speech APIs.
- `config`: Behavior depends on openclaw.json audio configuration such as messages.tts and proposed STT config.

## openclaw-openclaw-69328 — fix(acp): avoid false zero-diff failures and append session messages

- labels: `acp, reliability, sessions, ui_tui`
- `acp`: Title and code changes are explicitly in ACP control-plane/session manager and ACP verification-gate behavior.
- `reliability`: Fixes false zero-diff failures and changes hard failures into safer blocked follow-up handling.
- `sessions`: Behavior depends on persistent versus oneshot sessions and appends session.message payloads to transcripts.
- `ui_tui`: Control UI/chat controller now appends active-run session messages with dedupe and optimistic echo replacement.

## openclaw-openclaw-84715 — [Bug]: @openclaw/codex peer link failure reproduced on 2026.5.19 after update

- labels: `codex, packaging_deployment, reliability, skills_plugins`
- `codex`: Issue explicitly concerns @openclaw/codex and the Codex harness failing to import its shared-client bundle.
- `packaging_deployment`: Failure is tied to Homebrew/global install, managed npm tree, peer dependency links, and update/repair flows.
- `reliability`: Bug causes Codex turns to fail before any assistant reply and discusses health checks/repair after update.
- `skills_plugins`: The broken dependency resolution occurs in the managed plugin npm tree for the @openclaw/codex plugin.

## openclaw-openclaw-62552 — fix(acp): stabilize bridge session keys

- labels: `acp, sessions, queueing, reliability`
- `acp`: Explicit ACP bridge fix changes fallback ACP session keys and pending ACP prompt matching.
- `sessions`: Central behavior is session key stability, raw/canonical session-key equivalence, and terminal child session handling.
- `queueing`: Task registry maintenance marks active cron/cli/subagent tasks lost when backing child sessions are terminal, affecting task state cleanup.
- `reliability`: Fix prevents hangs/failures and stale live tasks caused by key collisions and terminal child sessions.

## openclaw-openclaw-74484 — Gateway pairing scope deadlock: CLI cannot approve/reject auto-reissued over-scoped repair requests

- labels: `auth_identity, gateway, reliability`
- `auth_identity`: Core issue is device pairing, token/session scope, and inability to approve or reject scope-upgrade repair requests.
- `gateway`: Failures occur through the OpenClaw gateway control plane and method-scope gate, with gateway pairing-required errors.
- `reliability`: The system enters a recovery deadlock with auto-reissued pending requests and no supported bootstrap path.

## openclaw-openclaw-51667 — Feature: Native Audio Input for Omni-Modal Models (skip STT transcription)

- labels: `chat_integrations, config, model_serving, sessions`
- `chat_integrations`: Feature is triggered by voice notes from WhatsApp/Telegram-style channels.
- `config`: Proposes explicit tools.media.audio.native and fallbackToTranscription configuration options.
- `model_serving`: Requests routing audio as a native media part to omni-modal model endpoints instead of STT.
- `sessions`: Maintainer comment centers on transcript durability, session restore, and snapshot continuity when STT is bypassed.

## openclaw-openclaw-65364 — feat(plugins): add registerProviderRuntimeAuthOverride API

- labels: `api_surface, auth_identity, security, skills_plugins`
- `api_surface`: Adds a public SDK API, registerProviderRuntimeAuthOverride, with new request/result types and semantics.
- `auth_identity`: Feature supplies runtime provider credentials, auth modes, API keys, OAuth/token modes, and provider auth resolution.
- `security`: Touches credential handling and security-boundary concerns, including validation, reentrancy guards, and plugin error logging.
- `skills_plugins`: Core change is a plugin registration API and plugin registry/runtime support for external plugins.

## openclaw-openclaw-56532 — memory-lancedb: add configurable timeout/retry for embedding calls

- labels: `memory, config, reliability`
- `memory`: PR is specifically for the memory-lancedb plugin and OpenAI-compatible embedding calls used for auto-recall.
- `config`: Adds configurable embedding.timeoutMs and embedding.maxRetries fields with schema/manifest validation.
- `reliability`: Bounds hung or 5xx-storming embedding backends with timeout/retry behavior to avoid stalled agent turns and fail faster.

## openclaw-openclaw-78919 — [Bug] ACP sessions_spawn doesn't route images to Codex's native vision like acpx codex exec does

- labels: `acp, acpx, codex, sessions`
- `acp`: Issue centers on ACP `sessions_spawn` with `runtime:acp` failing to route image attachments through the ACP path.
- `acpx`: Compares the failing ACP flow against `acpx codex exec`, which correctly passes images.
- `codex`: The affected agent is Codex, specifically its native vision capability for image analysis.
- `sessions`: The bug is in `sessions_spawn` behavior and affects session-based delegation/tracking.

## openclaw-openclaw-84752 — fix: self-heal lane wedges + restore openai-codex OAuth on embedded path

- labels: `auth_identity, chat_integrations, codex, queueing, reliability`
- `auth_identity`: Restores OAuth profile/sidecar resolution and fixes missing API key errors for embedded auth store loads.
- `chat_integrations`: Directly fixes Telegram polling-session failures that can take the Telegram channel offline.
- `codex`: The auth regression is explicitly for the openai-codex provider and Codex OAuth paths.
- `queueing`: Fixes per-lane command queue wedges, queueDepth handling, lane reset, and queued terminal active work recovery.
- `reliability`: Central theme is self-healing wedged lanes and polling sessions instead of requiring manual gateway restarts.

## openclaw-openclaw-84757 — [Bug]: Telegram session can get stuck after compaction when encrypted reasoning content fails verification

- labels: `chat_integrations, sessions, reliability`
- `chat_integrations`: The failure occurs in a Telegram direct-chat session and results in a Telegram fallback message.
- `sessions`: The bug is caused by persisted session history replay after compaction or restore, leaving the same session unusable until /new.
- `reliability`: The issue is a stuck-session recovery bug where retries keep failing and automatic cleanup/retry behavior is expected.

## openclaw-openclaw-68916 — [Bug]: ACP oneshot sessions leave orphaned processes — session reset does not clean up child ACP session keys

- labels: `acp, sessions, reliability`
- `acp`: Issue explicitly concerns ACP sessions, `sessions_spawn({ runtime: "acp" })`, and `closeAcpRuntimeForSession()` cleanup.
- `sessions`: Core bug is parent session reset failing to enumerate and clean child session keys.
- `reliability`: Orphaned processes, swallowed close failures, memory exhaustion, and missing cleanup are reliability failures.

## openclaw-openclaw-68843 — fix(acp): treat missing cwd as stale bound session

- labels: `acp, sessions, reliability`
- `acp`: PR explicitly fixes ACP session init failure handling and changes ACP runtime stale-session logic.
- `sessions`: Core behavior is bound ACP sessions, stale bindings, unbind cleanup, and reset-in-place recovery.
- `reliability`: Fixes wedged retries against dead sessions by detecting missing cwd and recovering automatically.

## openclaw-openclaw-52747 — fix(acp): time out stuck session lane tasks

- labels: `acp, sessions, queueing, reliability, config`
- `acp`: Title and changed files explicitly fix ACP control-plane session lane behavior.
- `sessions`: The issue is a stuck ACP session/load or initializeSession flow tied to a session lane.
- `queueing`: Problem states the stuck lane blocks subsequent queued tasks; fix releases it and dequeues the next task.
- `reliability`: Adds timeout recovery for hung tasks to prevent wedged lanes and availability loss.
- `config`: Adds acp.sessionLane.taskTimeoutMs with defaulting and schema validation.

## openclaw-openclaw-52249 — ACP parent session stuck until refresh when yielded waiting for child completion

- labels: `acp, sessions, queueing, reliability`
- `acp`: Issue is explicitly about ACP child sessions, ACP parent-stream relay, and ACP yield/resume behavior.
- `sessions`: Core failure is parent/child session state: yielded parent remains stuck after child completion and needs proper yield-wait tracking.
- `queueing`: Fix routes child-completion follow-ups through enqueueSystemEvent and heartbeat wake scheduling instead of direct resume.
- `reliability`: Describes a wedged/non-responsive state and recovery problem where manual refresh is required to unblock the parent.

## openclaw-openclaw-50054 — fix(acp): add distributed session locking with fail-closed redis fallback

- labels: `acp, sessions, reliability`
- `acp`: Title, summary, and diff explicitly wire locking into ACP dispatch and ACP session handling.
- `sessions`: Core change is a SessionLockManager for ACP session keys with acquire, renew, and release semantics.
- `reliability`: Distributed locking and fail-closed Redis behavior prevent concurrent execution races and unsafe fallback when Redis is unavailable.

## openclaw-openclaw-84802 — fix(memory-core): allow bounded dreaming session cleanup

- labels: `memory, sessions, reliability`
- `memory`: PR is explicitly in memory-core/dreaming and changes dreaming narrative behavior.
- `sessions`: Core change reuses stable narrative subagent session keys and deletes bounded session keys.
- `reliability`: Fix prevents stale dreaming-narrative sessions from accumulating and adds cleanup on retries/finalization.

## openclaw-openclaw-84583 — cron announce delivery triggers EmbeddedAttemptSessionTakeoverError when user is actively chatting

- labels: `chat_integrations, cron_automation, notifications, reliability, sessions`
- `chat_integrations`: The failure occurs when announce delivery sends results to the same Telegram user/channel.
- `cron_automation`: The triggering workflow is an isolated cron job completing and delivering its result.
- `notifications`: The problematic path is announce delivery of the cron result to a user.
- `reliability`: A race causes EmbeddedAttemptSessionTakeoverError and message/session-state loss risk.
- `sessions`: The root cause centers on session file locking, session writes, and takeover detection.

## openclaw-openclaw-75784 — Phantom user messages appear in webchat after heartbeat wakes / gateway restart / session repair

- labels: `chat_integrations, gateway, reliability, sessions`
- `chat_integrations`: The reported symptom is phantom user messages appearing in the WebChat channel/history.
- `gateway`: The bug is tied to gateway restart, Gateway journal events, and synthetic messages submitted through the Gateway agent path.
- `reliability`: The issue involves restart recovery, orphan recovery, stuck diagnostics, and session repair producing incorrect state.
- `sessions`: Evidence centers on orphaned subagent sessions, resumeOrphanedSession, session file repair, and session history projection.

## openclaw-openclaw-72015 — Reliability: active-memory blocks replies and QMD boot initialization can overload multi-agent gateways

- labels: `gateway, memory, reliability`
- `gateway`: Issue centers on multi-agent gateway boot/restart overload, health timeouts, and gateway responsiveness.
- `memory`: Active-memory plugin and QMD memory startup/update behavior are the core mechanisms causing latency.
- `reliability`: Explicit reliability concern with high CPU, timeouts, crash-loop impact, and fail-open/cancellation mitigations.

## openclaw-openclaw-69669 — ACP: keep thread-bound follow-ups parent-orchestrated by default, not raw pass-through

- labels: `acp, coding_agents, sessions`
- `acp`: Title and body explicitly discuss ACP thread-bound follow-ups and sessions_spawn(runtime="acp").
- `coding_agents`: Core issue is parent orchestrator rewriting shorthand user follow-ups into explicit child coding-agent tasks instead of raw relay.
- `sessions`: Focuses on thread-bound child session continuity, continuation, reactivation, and parent/child session behavior.

## openclaw-openclaw-69256 — fix(cron): prevent premature session cleanup when subagents are running

- labels: `cron_automation, sessions, agent_runtime, coding_agents, reliability`
- `cron_automation`: The fix is in isolated cron delivery cleanup for jobs using deleteAfterRun.
- `sessions`: Core behavior is deferring sessions.delete so the cron run session is not removed prematurely.
- `agent_runtime`: The guard checks active descendant/subagent runs to preserve parent-worker orchestration lifecycle.
- `coding_agents`: The broken workflow is an orchestrator-worker agent pipeline where subagents must report back to the parent.
- `reliability`: This is a regression bug fix preventing orphaned workers and premature cleanup during active runs.

## openclaw-openclaw-65242 — fix: CompletionDeliveryGate to prevent duplicate ACP completion delivery

- labels: `acp, coding_agents, notifications, reliability, sessions`
- `acp`: The fix explicitly targets duplicate ACP child-session completion delivery and adds ACP silent-wake handling.
- `coding_agents`: It coordinates subagent, task-registry, announce, and completion flows in the agent system.
- `notifications`: The central behavior is preventing duplicate user-visible completion messages and banners.
- `reliability`: The gate uses first-writer-wins coordination to avoid races, stale replays, and duplicate delivery.
- `sessions`: The completion key and behavior depend on owner/requester/child session identity and parent wake semantics.

## openclaw-openclaw-62769 — [Feature]: Support ACP configured bindings for Telegram DMs (not just groups/topics)

- labels: `acp, chat_integrations, sessions`
- `acp`: Issue is explicitly about Telegram bindings with type "acp" routing messages to an ACP harness.
- `chat_integrations`: The affected surface is Telegram direct messages versus groups/topics.
- `sessions`: Expected behavior is to create or resume persistent ACP sessions for Telegram DM conversations.

## openclaw-openclaw-60979 — feature: sessions_spawn ACP delivery to channel (stream output to Zulip/Discord topic)

- labels: `acp, sessions, chat_integrations, notifications`
- `acp`: Request is specifically for `sessions_spawn` with `runtime="acp"` and ACP session output behavior.
- `sessions`: Feature concerns spawned session output binding and delivery for `sessions_spawn`.
- `chat_integrations`: Desired target is a Zulip/Discord channel conversation or topic via channel plugins.
- `notifications`: Core request is a `delivery.mode: "announce"` style channel delivery path for session output.

## openclaw-openclaw-60737 — [Feature]: Per-DM/per-chat default ACP binding for auto-spawning ACP sessions on new topics

- labels: `acp, chat_integrations, config, sessions`
- `acp`: Feature explicitly configures default ACP binding and auto-spawns ACP agents/sessions.
- `chat_integrations`: Scope is Telegram DM and group forum topics routing chat messages.
- `config`: Proposes new defaultAcp options in TelegramDirectConfig/TelegramGroupConfig.
- `sessions`: New topics are bound to spawned ACP sessions and subsequent messages resume that binding.

## openclaw-openclaw-84789 — Active memory crashes on Telegram forum topic sessions (dirName validation)

- labels: `chat_integrations, memory, sessions, reliability`
- `chat_integrations`: The failure is specific to Telegram forum/topic-based group sessions.
- `memory`: The affected feature is the active-memory plugin, which starts and then fails.
- `sessions`: The root cause is a Telegram-derived session key with colons being converted into a directory name.
- `reliability`: This is a crash bug blocking active memory on all Telegram forum topic messages.

## openclaw-openclaw-84771 — Event loop saturation during startup: synchronous model-prewarm and session-locks block event loop for 28-64 seconds

- labels: `gateway, model_serving, reliability, sessions`
- `gateway`: Issue centers on OpenClaw gateway startup, gateway readiness, and restart cascades.
- `model_serving`: Synchronous model-prewarm during startup is a central implicated model lifecycle path.
- `reliability`: Reports event-loop saturation, liveness warnings, memory pressure, crash-loop/restart behavior, and missed heartbeats.
- `sessions`: Session-lock processing and synchronous parsing of many session stores are core causes.

## openclaw-openclaw-84746 — [Bug]: Auto-compaction crashes active responses after 5.18 transcript lock scope change (#13744)

- labels: `agent_runtime, memory, reliability, sessions`
- `agent_runtime`: The bug affects embedded agent runs and kills active model responses when auto-compaction fires.
- `memory`: Auto-compaction of the transcript/session context is the operation that rewrites state and triggers the failure.
- `reliability`: The issue reports crashes, message loss, a race around locks, wedged lanes, and recovery only after restart.
- `sessions`: The root error is a session-file/transcript-lock takeover during in-flight session persistence.

## openclaw-openclaw-84732 — Slack channel sends fail: `reconcileUnknownSend` required but no channel adapter implements it

- labels: `chat_integrations, notifications, reliability`
- `chat_integrations`: The failure is specific to Slack channel sends through the Slack channel adapter/plugin.
- `notifications`: The issue centers on outbound message delivery/durable send handling and message-loss impact.
- `reliability`: A required capability mismatch causes channel message sends to fail despite configured Slack access.

## openclaw-openclaw-84706 — [Bug]: subagent spawn validation rejects every non-off thinking level on all canonical openai/* models — error cites canonical alias even when openai-codex/* is requested

- labels: `api_surface, codex, coding_agents, sessions`
- `api_surface`: The bug concerns the sessions_spawn request contract and validation/error response for the subagent API.
- `codex`: The failing route is explicitly openai-codex/* and the environment reports the OpenAI Codex runtime.
- `coding_agents`: The affected behavior is subagent creation/spawn validation inside the agent workflow.
- `sessions`: The concrete failing entry point is sessions_spawn and related subagent session creation paths.

## openclaw-openclaw-84697 — Custom OpenAI-compatible provider with baseUrl without /v1 fails with cryptic 'incomplete terminal response' error

- labels: `config, local_model_providers, model_serving`
- `config`: Issue centers on manual/onboard provider configuration and the required baseUrl path suffix.
- `local_model_providers`: Custom OpenAI-compatible provider setup, baseUrl handling, and provider validation are central.
- `model_serving`: Failure occurs in chat/completions streaming response handling when the endpoint returns HTML instead of JSON/SSE.

## openclaw-openclaw-84419 — fix(session): prefer real tool result over synthetic error in transcript repair

- labels: `sessions, tool_calling, reliability`
- `sessions`: The PR directly fixes session transcript repair and session history deduplication on load.
- `tool_calling`: The core behavior is choosing the correct tool result for a tool-use/result pairing over a synthetic missing-result error.
- `reliability`: It fixes a race-induced stale synthetic error so successful tool results are recovered reliably, backed by regression tests.

## openclaw-openclaw-84316 — [Bug]: Telegram group TTS for sub-agent reports success in /tts status but voice never delivered (2026.5.12)

- labels: `chat_integrations, coding_agents, notifications, reliability`
- `chat_integrations`: The failure is specific to Telegram group chat versus Telegram DM delivery.
- `coding_agents`: The broken path is for a sub-agent with its own bot account and TTS handoff.
- `notifications`: Core symptom is an outbound voice/TTS message reported successful but never delivered.
- `reliability`: This is a behavior bug with message loss and incorrect success state without a crash.

## openclaw-openclaw-84297 — [Bug]: Per-agent identity overlay dropped on cron --announce and heartbeat target-channel Slack pushes (announce path; reply path was fixed in #38235)

- labels: `auth_identity, chat_integrations, cron_automation, notifications`
- `auth_identity`: Central bug is the per-agent identity/persona overlay not being applied to Slack outbound messages.
- `chat_integrations`: The affected delivery surface is Slack channel messaging via chat.postMessage.
- `cron_automation`: The failing paths are cron --announce jobs and heartbeat scheduled pushes.
- `notifications`: Issue concerns outbound announcement/heartbeat message delivery and rendering identity on those pushes.

## openclaw-openclaw-82642 — Fix iMessage slash command acknowledgements

- labels: `chat_integrations, notifications, reliability`
- `chat_integrations`: PR is explicitly about iMessage inbound slash commands and direct DM command handling.
- `notifications`: Fixes acknowledgement/reply delivery policy so command acknowledgements are sent instead of suppressed.
- `reliability`: Addresses a production bug where authorized slash commands completed but their acknowledgements were dropped.

## openclaw-openclaw-80255 — fix #79026: active-memory recall subagent can deadlock on the main lane inside before_prompt_build

- labels: `coding_agents, memory, queueing, reliability`
- `coding_agents`: The fix concerns an Active Memory recall subagent used during agent prompt construction.
- `memory`: The changed files and behavior are in the active-memory extension and its recall path.
- `queueing`: The core change isolates recall onto a dedicated active-memory lane instead of re-entering the main lane.
- `reliability`: The PR fixes a deadlock regression and adds proof that the deadlock path no longer occurs.

## openclaw-openclaw-80008 — feat(plugins): expose ACP spawn and prompt in plugin runtime

- labels: `acp, api_surface, config, notifications, skills_plugins`
- `acp`: Adds ACP-specific spawn and prompt helpers for ACP-backed agent sessions.
- `api_surface`: Introduces new plugin runtime API methods `api.runtime.acp.spawn()` and `api.runtime.acp.prompt()` with typed params.
- `config`: Gates the new helpers behind an opt-in plugin config flag with schema/type updates.
- `notifications`: A core purpose is channel/message delivery of ACP prompt results via `deliver: true`.
- `skills_plugins`: The feature is exposed inside the plugin runtime and updates plugin SDK/runtime mocks and docs.

## openclaw-openclaw-78977 — fix(providers): skip store:false for proxy-like Responses API endpoints (#78897)

- labels: `local_model_providers, model_serving, reliability`
- `local_model_providers`: Fix targets LiteLLM/custom baseUrl proxy-like OpenAI-compatible provider handling.
- `model_serving`: Changes Responses API endpoint payload behavior for the `store` field and continuation handling.
- `reliability`: Prevents multi-turn continuation failures caused by backends rejecting unpersisted `rs_*` items.

## openclaw-openclaw-77992 — [Bug] Context display shows ?/131k with llama.cpp after upgrading to 2026.5.4 — field name mismatch not resolved

- labels: `local_models, local_model_providers, model_serving, telemetry_usage`
- `local_models`: The bug occurs with a local llama.cpp server running a GGUF Qwen model and affects local model users.
- `local_model_providers`: The issue is a provider compatibility mismatch for the configured llamacpp OpenAI-compatible backend.
- `model_serving`: It depends on the llama.cpp server response schema for OpenAI-compatible usage fields.
- `telemetry_usage`: The broken behavior is token usage/context accounting showing '?/131k' instead of parsed token counts.

## openclaw-openclaw-77827 — fix: LM Studio thinking blocks invisible with Responses API

- labels: `model_serving, api_surface, local_models`
- `model_serving`: Fixes OpenAI-compatible Responses streaming parsing for `response.reasoning_text.done` events from LM Studio.
- `api_surface`: Implements handling for an official OpenAI Responses API stream event and its downstream event contract.
- `local_models`: Bug is explicitly reproduced with LM Studio local mode and a local Qwen reasoning model, affecting local model UX.

## openclaw-openclaw-77694 — [Bug]: acpx flow run ACP node outputs return empty strings instead of agent replies

- labels: `acpx, acp, agent_runtime, reliability`
- `acpx`: The bug is explicitly in `acpx flow run` and compares it with direct `acpx <agent> exec` behavior.
- `acp`: The failing flow node is an ACP node created with `acp({ prompt })`, and its output is empty.
- `agent_runtime`: The issue concerns flow-run orchestration completing while failing to capture agent replies from nodes.
- `reliability`: This is a concrete runtime correctness bug where completed runs return empty strings instead of expected replies.

## openclaw-openclaw-76724 — [Bug]: MCP tools not discovered by Agent despite successful handshake (200 OK)

- labels: `mcp_tooling, ui_tui`
- `mcp_tooling`: Issue is explicitly about an MCP server handshake succeeding but tools/list not being sent and MCP tools not being discovered.
- `ui_tui`: User-visible failure is in the Agent Tools/dashboard view showing 33/33 enabled and not listing the new tools after reload.

## openclaw-openclaw-72013 — ACP startup identity reconcile warns on terminal one-shot sessions

- labels: `acp, gateway, sessions`
- `acp`: Issue is specifically about ACP startup identity reconciliation and ACP one-shot runtime sessions.
- `gateway`: The warning occurs during gateway startup and concerns gateway startup reconciliation behavior.
- `sessions`: Core problem involves persisted session records, session identities, terminal one-shot sessions, and session stores.

## openclaw-openclaw-71976 — Memory Dreaming: Light sleep sort prioritizes recency over recallCount, hiding real recall data

- labels: `memory, reliability`
- `memory`: Issue is about Memory Dreaming, short-term-recall.json, recallCount, rehydration, and promotion behavior in the memory subsystem.
- `reliability`: Describes bugs where sorting and narrow search spans cause valid memory candidates to be hidden or fail promotion despite existing data.

## openclaw-openclaw-71930 — Mattermost plugin drops post_edited events — @mentions added via edit do not trigger agent wake

- labels: `chat_integrations, reliability`
- `chat_integrations`: Issue is specifically about Mattermost WebSocket handling and @mention wake behavior in a chat channel.
- `reliability`: A supported event type is silently dropped, causing message-loss/wake failure with no error or log.

## openclaw-openclaw-71784 — Bug: memory search live embedding fails ~20–40% with `fetch failed | other side closed` (provider-agnostic; upstream healthy)

- labels: `memory, reliability`
- `memory`: Issue is specifically about live memory search, semantic recall, embeddings, vector status, and memory indexing.
- `reliability`: Reports intermittent 20–40% transient fetch/TLS/socket failures causing unreliable memory recall.

## openclaw-openclaw-70882 — fix(bundle-mcp): coerce stringified object/array params before MCP tool calls

- labels: `mcp_tooling, tool_calling, security`
- `mcp_tooling`: Fix is in bundle MCP materialization and targets MCP servers rejecting malformed params.
- `tool_calling`: Coerces LLM-produced tool call arguments according to each tool inputSchema before invocation.
- `security`: Patch includes prototype-pollution and oversized JSON.parse payload guards for tool-supplied inputs.

## openclaw-openclaw-68204 — Unified run trace schema across agent, ACP, subagent, and task flows

- labels: `acp, agent_runtime, sessions, telemetry_usage`
- `acp`: Scope explicitly includes ACP sessions, ACP parent-child relay paths, and updating the ACP relay path.
- `agent_runtime`: Canonical trace schema is for main agent runs, subagents, task execution, parent-child runs, and run lifecycle events.
- `sessions`: Schema includes sessionKey and is intended to preserve parent-child linkage across ACP sessions and runs.
- `telemetry_usage`: Issue is centered on observability/tracing and reconstructing run timelines with latency, status, and event metadata.

## openclaw-openclaw-67244 — Explicit ACP agent runs: embedded backend visibility failure and stale final JSON state after sessions_yield

- labels: `acp, acpx, agent_runtime, sessions, reliability`
- `acp`: Issue is explicitly about ACP agent runs and ACP backend lookup/completion behavior.
- `acpx`: Failure names the ACPX runtime plugin and embedded ACPX backend visibility/registration.
- `agent_runtime`: Covers explicit `agent --json` embedded-run path, descendant work, and liveness state handling.
- `sessions`: Stale final state occurs after `sessions_yield` with a specific `--session-id` and descendant session completion reconciliation.
- `reliability`: Reports stale final JSON state and backend visibility failure causing incorrect liveness/status despite completed work.

## openclaw-openclaw-65640 — fix(acp): persistent session recovery for --bind here sessions

- labels: `acp, acpx, sessions, reliability`
- `acp`: PR explicitly fixes ACP session manager/control-plane behavior and /acp commands.
- `acpx`: Problem is recovery when the acpx backend loses a persistent session.
- `sessions`: Core issue is persistent session resume/recovery, --bind here bindings, and stale binding cleanup.
- `reliability`: Adds retry/recovery paths for stale or missing backend sessions after restart or eviction.

## openclaw-openclaw-64199 — [Bug]: ACP configured binding uses parent channel ID for session key — all threads under same channel share one persistent Claude Code process

- labels: `acp, acpx, sessions, chat_integrations, security`
- `acp`: Bug is explicitly limited to runtime.type "acp" configured channel bindings.
- `acpx`: The faulty key maps to the same acpxRecordId and acpx state record/process.
- `sessions`: Core issue is incorrect session-key granularity causing threads to share one persistent session/process.
- `chat_integrations`: The repro and impact are specifically Discord channel/thread bindings.
- `security`: Cross-thread context contamination exposes one thread's conversation history to another.

## openclaw-openclaw-59878 — Session lane stuck in 'running' after run dies — sessions.abort + gateway restart fail to clear stale state

- labels: `gateway, queueing, reliability, sessions`
- `gateway`: Gateway restart fails to clear the stale state, and gateway logs/calls are central to reproduction and workaround.
- `queueing`: Session lane remains in running state, causing new messages to queue indefinitely behind a dead lock.
- `reliability`: Bug is stale/dead run state not being cleaned up or recovered after abort/restart, with proposed timeout recovery.
- `sessions`: Issue centers on session lanes, sessions.abort, sessions.send, session status, and persisted session state.

## openclaw-openclaw-57597 — fix(acp): persist spawn labels in target session store

- labels: `acp, sessions, reliability`
- `acp`: The fix is explicitly for `/acp spawn ... --label` behavior and ACP session label persistence.
- `sessions`: Core change writes spawned session labels to the correct target session store using the spawned `sessionKey`.
- `reliability`: Fixes a bug where cross-agent spawned sessions silently lost labels, breaking follow-up label-based commands.

## openclaw-openclaw-55790 — sessions_spawn(runtime="subagent") ignores inherited/per-agent subagent thinking defaults and initializes children at low

- labels: `coding_agents, agent_runtime, sessions, config`
- `coding_agents`: Bug concerns subagent orchestration via sessions_spawn in an agent workflow.
- `agent_runtime`: The failing path is runtime="subagent" child spawning and initialization behavior.
- `sessions`: Issue centers on spawned parent/child sessions and their recorded thinking_level_change state.
- `config`: Expected behavior depends on resolving configured agent thinkingDefault and subagents.thinking defaults.

## openclaw-openclaw-67539 — [Feature]: Add provider-specific TTS prompt hints

- labels: `self_hosted_inference, api_surface`
- `self_hosted_inference`: The feature is centered on TTS speech providers and provider-specific speech prompt behavior.
- `api_surface`: It proposes changing the speech provider contract with a new optional buildPromptHint hook and context shape.

## openclaw-openclaw-47187 — fix(ui): reset transient chat overlays and style context notice

- labels: `ui_tui`
- `ui_tui`: PR directly changes Control UI chat styles and state handling to fix chat overlay/context notice rendering.

## openclaw-openclaw-48260 — feat(ui): add active time summary to usage overview

- labels: `telemetry_usage, ui_tui`
- `telemetry_usage`: Adds active-time and average session-duration summary metrics to the Usage Overview.
- `ui_tui`: Feature is explicitly a web UI Usage page display change with updated overview rendering and i18n strings.

## openclaw-openclaw-64181 — fix(hooks): reject error responses from slug generator and strip post-truncation dashes

- labels: `hooks, memory, reliability`
- `hooks`: Title and changed files are in hooks, specifically fixing src/hooks/llm-slug-generator.ts behavior.
- `memory`: Bug produced incorrect session memory filenames and fragmented canonical daily memory paths.
- `reliability`: Fix rejects failure/error payloads and corrects slug truncation cleanup to prevent bad state from provider/run failures.

## openclaw-openclaw-56613 — [Feature]: Talk/Voice tab — agent/session switching + per-agent TTS voice

- labels: `config, sessions, ui_tui`
- `config`: Requests per-agent TTS voice settings via agents.list configuration overriding global TTS settings.
- `sessions`: Core remaining request is Voice/Talk tab routing to the selected agent/session instead of hardcoded main session.
- `ui_tui`: Feature is a user-facing Talk/Voice tab session picker similar to the Chat tab session switcher.

## openclaw-openclaw-49310 — fix: keep tui busy during follow-up waits

- labels: `sessions, ui_tui`
- `sessions`: Uses the sessions_yield follow-up marker and restores/clears state when reloading session history.
- `ui_tui`: Changes TUI activity/status handling so the interface stays visibly busy while awaiting follow-up.

## openclaw-openclaw-75043 — Add provider-aware automatic TTS emotion mapping

- labels: `self_hosted_inference, config, api_surface`
- `self_hosted_inference`: The PR is centered on TTS synthesis behavior and speech provider adapters, including OpenAI, ElevenLabs, Volcengine, Xiaomi, and Azure.
- `config`: It adds opt-in `messages.tts.autoEmotion` configuration and updates config help/schema surfaces for the new setting.
- `api_surface`: It maps inferred emotions into provider/request control surfaces and applies the behavior across normal, telephony, and streaming TTS synthesis paths.

## openclaw-openclaw-70002 — ci: skip docs sync & translate-trigger workflows in forks

- labels: `tests_ci`
- `tests_ci`: Direct change to GitHub Actions workflow files to guard CI/CD jobs in forks.

## openclaw-openclaw-47285 — feat(memory-lancedb): native Azure OpenAI support

- labels: `memory, local_model_providers, auth_identity`
- `memory`: The PR targets the memory-lancedb plugin and Azure OpenAI embeddings for LanceDB memory functionality.
- `local_model_providers`: It adds provider compatibility for Azure/OpenAI-compatible embedding endpoints via baseUrl detection and API version handling.
- `auth_identity`: It changes provider authentication by sending Azure's required api-key header instead of a bearer Authorization header.

## openclaw-openclaw-84753 — [Feature]: Show display name instead of user ID in session list

- labels: `chat_integrations, sessions, ui_tui`
- `chat_integrations`: Request concerns Feishu, Discord, Telegram, WhatsApp channel users and resolving channel peer IDs to display names.
- `sessions`: Core behavior is how session lists and session labels display user identity instead of session peer IDs.
- `ui_tui`: Visible surfaces include the Control UI session sidebar and `openclaw status` Sessions table.

## openclaw-openclaw-42408 — [Bug/Docs]: local+hybrid memory_search quality can appear unstable due to extraPaths path drift + benchmark-file contamination

- labels: `config, docs, memory`
- `config`: The root cause and mitigations focus on `extraPaths` path drift, absolute path setup, and exclusion patterns for indexing.
- `docs`: The issue explicitly requests documentation guidance for memory index/search path hygiene and benchmark contamination pitfalls.
- `memory`: The central behavior is `memory_search`, memory indexing, local memory provider, embeddings, and retrieval ranking quality.

## openclaw-openclaw-84794 — Clean up isolated cron sessions after runs

- labels: `cron_automation, sessions, reliability`
- `cron_automation`: PR directly fixes isolated cron job delete-after-run cleanup after cron runs.
- `sessions`: Core behavior deletes run-scoped cron sessions via sessions.delete and session runtime retirement.
- `reliability`: Cleanup is moved into the runner finally block so delivery-none, errors, and terminal paths still clean up.

## openclaw-openclaw-77748 — fix: Codex startup plugins + WhatsApp history & Docker Codex OAuth

- labels: `auth_identity, chat_integrations, codex, packaging_deployment, skills_plugins`
- `auth_identity`: Adds Docker wiring and a helper for Codex OAuth/login callback handling.
- `chat_integrations`: Modifies the WhatsApp channel to provide recent chat history for message actions.
- `codex`: Explicitly fixes Codex harness startup and Codex OAuth operation.
- `packaging_deployment`: Updates docker-compose and adds a Docker helper script for the Codex auth flow.
- `skills_plugins`: Changes startup plugin resolution so provider-owned plugins load when implied by the primary model.

## openclaw-openclaw-72087 — Bug: dist/entry.js main-path breaks Codex OAuth image generation on Linux while direct runCli()/provider path succeeds

- labels: `auth_identity, codex, packaging_deployment`
- `auth_identity`: Failure is tied to the openai-codex OAuth profile and token-based image auth path with no OPENAI_API_KEY.
- `codex`: The report explicitly involves Codex OAuth and the Codex Responses backend for image generation.
- `packaging_deployment`: Suspected regression is in the packaged dist/entry.js CLI bootstrap/main-entry path versus direct runCli/provider execution.

## openclaw-openclaw-84418 — test(cron): document and test owner-only tool security boundary for isolated cron

- labels: `cron_automation, security, tests_ci`
- `cron_automation`: PR is explicitly about isolated cron runs and cron owner-only tool allowlist behavior.
- `security`: Central change documents and enforces the owner-only tool security boundary, filtering gateway/nodes from unattended cron grants.
- `tests_ci`: Adds a focused Vitest test file with six cases for the cron allowlist boundary.

## openclaw-openclaw-53997 — acpx: add terminal-truth artifacts and strict terminal states

- labels: `acpx, acp, reliability`
- `acpx`: Title, paths, and implementation are explicitly under extensions/acpx and change AcpX runtime artifacts/states.
- `acp`: The PR concerns ACP runtime-wrapped execution, ACP turn artifacts, parsed ACP errors, and ACP session/runtime behavior.
- `reliability`: Adds durable terminal truth, strict terminal states, abort-before-spawn race handling, mirror-failure preservation, and safer run-id allocation.

## openclaw-openclaw-58135 — [Feature]: expose promptMode parameter in sessions_spawn for deterministic blank sub-agents

- labels: `acp, api_surface, coding_agents, sessions`
- `acp`: The requested change is to the sessions_spawn ACP-style session tool parameter set.
- `api_surface`: It asks to add an optional promptMode parameter to the spawn handler schema and request contract.
- `coding_agents`: The feature controls how spawned coding sub-agents are initialized and prompted.
- `sessions`: It concerns child session/sub-agent spawning behavior and inherited session prompt state.

## openclaw-openclaw-84039 — fix(cli): honor --no-prefix-cwd in acp

- labels: `acp`
- `acp`: PR explicitly fixes the `openclaw acp` CLI path so `--no-prefix-cwd` is forwarded into the ACP bridge.

## openclaw-openclaw-66000 — fix(cli): clear conflicting OPENCLAW_LAUNCHD_LABEL when --profile is provided

- labels: `config, gateway, packaging_deployment`
- `config`: Fixes environment/profile handling for OPENCLAW_LAUNCHD_LABEL when --profile is explicit.
- `gateway`: The bug affects profiled gateway commands such as gateway status resolving the wrong plist.
- `packaging_deployment`: Behavior centers on launchd labels and LaunchAgent plist resolution for the daemon.

## openclaw-openclaw-84729 — [codex] Fix macOS app copyright year

- labels: `tests_ci, ui_tui`
- `tests_ci`: Changes scripts/check-changed.mjs and changed-lanes tests for validation/CI planning behavior.
- `ui_tui`: Updates macOS AboutSettings SwiftUI app UI text for the copyright year.

## openclaw-openclaw-72262 — docs: add WhatsApp 408 disconnect troubleshooting runbook

- labels: `chat_integrations, docs, reliability`
- `chat_integrations`: Issue is specifically about WhatsApp channel troubleshooting and WhatsApp Web/Baileys disconnects.
- `docs`: Title and body request additions to WhatsApp and channel troubleshooting documentation.
- `reliability`: Runbook covers timeout disconnect loops, reconnect decisions, stale auth recovery, and runtime mismatch diagnosis.

## openclaw-openclaw-48606 — fix: macOS default browser detection fallback to known paths

- labels: `browser_automation, reliability`
- `browser_automation`: Changes browser extension Chrome/Chromium executable detection for macOS default browsers.
- `reliability`: Adds validated fallback paths when osascript/defaults browser resolution fails, preventing missed installed browsers.

## openclaw-openclaw-72138 — fix(feishu): emit sent hooks for normal replies

- labels: `chat_integrations, hooks, notifications`
- `chat_integrations`: PR is explicitly for the Feishu channel normal conversation reply dispatcher.
- `hooks`: Core fix emits canonical plugin message_sent and internal message:sent hooks for reply paths.
- `notifications`: Change concerns sent-message handling and successful/failed outbound delivery signals for replies.

## openclaw-openclaw-71648 — fix(mcp): bound pendingClaudePermissions / pendingApprovals via TTL sweeper + close clear

- labels: `mcp_tooling, approvals, reliability`
- `mcp_tooling`: PR is explicitly under MCP and changes src/mcp channel bridge/server behavior for openclaw mcp serve.
- `approvals`: Core fix bounds pendingApprovals and pendingClaudePermissions, including missed approval resolution handling.
- `reliability`: Adds TTL sweeper, close clearing, self-termination, and post-close guards to prevent leaks and ghost writes in long-running processes.

## openclaw-openclaw-51849 — Docs: add freeCodeCamp OpenClaw full tutorial to showcase

- labels: `docs, agent_demos`
- `docs`: Single-file documentation change in docs/start/showcase.md adding a tutorial entry.
- `agent_demos`: Adds a freeCodeCamp OpenClaw full tutorial video to the showcase/OpenClaw in Action section.

## openclaw-openclaw-61775 — enhance Makefile with standard build, test, and quality targets

- labels: `packaging_deployment, tests_ci`
- `packaging_deployment`: Makefile adds standard build/deps/clean/dev targets delegating to pnpm scripts, a contributor build workflow layer.
- `tests_ci`: Makefile adds test, coverage, scoped test, check, lint, format, typecheck, and landing-gate quality targets.

## openclaw-openclaw-90146 — google-vertex: Missing gemini-3.1-flash-lite in provider catalog causes silent failure instead of error

- labels: `agent_runtime, model_releases, reliability`
- `agent_runtime`: Issue traces failure through embedded-agent-runner and model fallback during an agent run, causing no agent reply.
- `model_releases`: Central fix is adding/mapping the newly available gemini-3.1-flash-lite model in the provider catalog.
- `reliability`: Silent failure/no user-facing error from FailoverError handling is a reliability failure in fallback/error recovery.

## openclaw-openclaw-84301 — [Bug]: Make Dream Diary narrative timeout configurable for slow/serial local model backends

- labels: `config, local_models, queueing, reliability`
- `config`: The requested fix is a user-facing configurable Dream Diary narrative timeout and concurrency setting.
- `local_models`: The failure is tied to slow or serial local model backends such as LM Studio and local Qwen routing.
- `queueing`: The issue describes multiple narrative runs started in parallel/queued form exceeding the wait budget.
- `reliability`: Hardcoded 60s waits cause otherwise normal backend work to time out and fail, reducing completion reliability.

## openclaw-openclaw-71157 — [Feature]: Support WhatsApp disappearing-message expiration for outbound replies

- labels: `chat_integrations, config, security`
- `chat_integrations`: Feature is specifically for WhatsApp outbound replies and Baileys send behavior.
- `config`: Requests channel- and account-level WhatsApp disappearingMessagesSeconds configuration with override behavior.
- `security`: Core motivation is privacy retention mismatch for disappearing-message chats and policy-sensitive message persistence.

## openclaw-openclaw-48877 — feat(telegram): add multi-level menu support to customCommands

- labels: `chat_integrations, config`
- `chat_integrations`: PR explicitly adds Telegram custom command menu/callback behavior and modifies Telegram bot handler files.
- `config`: Adds menus and routes fields to Telegram customCommands config schema and types.

## openclaw-openclaw-66327 — feat(msteams): implement sendPayload for interactive approval cards

- labels: `approvals, chat_integrations, notifications`
- `approvals`: PR specifically renders approval prompts as Teams Adaptive Cards with Approve/Deny buttons and /approve messageBack commands.
- `chat_integrations`: Change is in the MS Teams channel extension outbound adapter for Teams-specific message rendering.
- `notifications`: Implements outbound sendPayload delivery so interactive approval messages are delivered correctly instead of falling back to plain text.

## openclaw-openclaw-84645 — Materialize node-host inline interpreter eval before exec approval

- labels: `exec_tools, approvals, security`
- `exec_tools`: Changes node-host system.run command handling for Python/Node inline eval argv before execution planning.
- `approvals`: Central behavior is approval planning: rewriting inline eval into script paths so approval binding can apply.
- `security`: PR explicitly preserves security model with fail-closed unsupported forms, private temp files, hashing, and 0600 mode.

## openclaw-openclaw-85999 — [Bug]: 2026.5.22 gateway pre-warm (warmCurrentProviderAuthState) blocks event loop ~60s on startup, breaks channel handshakes

- labels: `auth_identity, chat_integrations, gateway, reliability`
- `auth_identity`: The blocking startup work is explicitly `warmCurrentProviderAuthState` and the issue is tagged as auth-provider impact.
- `chat_integrations`: Discord, Feishu, and Telegram channel handshakes time out and inbound chat messages stall.
- `gateway`: The regression occurs during gateway startup/pre-warm and affects gateway readiness after restart.
- `reliability`: This is a startup regression causing event-loop starvation, timeouts, delayed messages, and restart liveness warnings.

## openclaw-openclaw-66125 — [Bug]: openai-completions fallback candidate is selected, but fallback does not complete successfully through an OpenAI-compatible proxy

- labels: `local_model_providers, model_serving, reliability`
- `local_model_providers`: Central issue is a local OpenAI-compatible provider/proxy, base URL, auth, model discovery, and fallback-chain selection.
- `model_serving`: Failure occurs on the OpenAI-compatible completions/chat-completions serving path and possible request-shape or streaming compatibility.
- `reliability`: Regression where a selected fallback provider fails to complete and silently falls through without adequate diagnostics.

## openclaw-openclaw-84549 — fix(deepinfra): load all DeepInfra models when user wants to browse t…

- labels: `local_model_providers, model_serving, skills_plugins`
- `local_model_providers`: DeepInfra provider discovery is fixed to load models from an OpenAI-compatible /v1/openai/models endpoint with API-key gating and fallback catalogs.
- `model_serving`: Changes center on model catalog routing by surface and proxy behavior for DeepInfra/Anthropic model serving, including cache marker handling.
- `skills_plugins`: The work is scoped to the extensions/deepinfra plugin and registers model catalog providers within that extension.

## openclaw-openclaw-79447 — fix(model-auth): resolve per-entry apiKey profile ID references

- labels: `auth_identity, config, local_model_providers`
- `auth_identity`: Fixes resolution of stored auth profile IDs into actual API-key credentials and rejects incompatible credential classes.
- `config`: Behavior depends on configured models.providers.<id>.apiKey values and how profile-reference strings are interpreted.
- `local_model_providers`: Central issue is model provider auth handling for per-entry/custom provider API-key configuration.

## openclaw-openclaw-48851 — feat(status): add API call count to session status and usage footer

- labels: `sessions, telemetry_usage, ui_tui`
- `sessions`: Adds and persists per-run callCount on session entries and uses it in session status.
- `telemetry_usage`: Tracks API call counts as a usage metric alongside tokens and cost reporting.
- `ui_tui`: Displays the call count in /status output and the response usage footer.

## openclaw-openclaw-74305 — [Bug]: ACPX Codex worker fails when model/thinking overrides are configured

- labels: `acpx, acp, codex, reliability`
- `acpx`: The failure is explicitly in the ACPX plugin path and ACPX Codex command handling.
- `acp`: The repro uses the ACP runtime and sessions_spawn to start an ACP worker task.
- `codex`: The affected worker is codex-acp/Codex CLI with Codex model and reasoning overrides.
- `reliability`: It is a crash/internal-error bug where the spawned worker fails and no transcript is created.

## openclaw-openclaw-84740 — Feature Request: Option to hide/suppress certain sessions from the session list

- labels: `sessions, ui_tui`
- `sessions`: The request is about hiding, suppressing, archiving, and filtering specific sessions in the session list.
- `ui_tui`: The central user-facing change is to reduce UI clutter in the session list view with toggles and row actions.

## openclaw-openclaw-79897 — OpenAI-compatible streaming with llama.cpp saves zero usage (stream closed before final usage chunk)

- labels: `local_models, model_serving, telemetry_usage`
- `local_models`: Issue is specific to a local llama.cpp backend used through OpenClaw.
- `model_serving`: Central bug is OpenAI-compatible SSE streaming behavior where a final usage chunk is missed.
- `telemetry_usage`: Impact is saved token usage being 0/0/0, breaking status/context accounting and compaction logic.

## openclaw-openclaw-46740 — ACP: classify silent acpx exits as backend unavailable

- labels: `acp, acpx, reliability`
- `acp`: PR changes ACP runtime/control-plane error codes and user-facing ACP error text for backend exits.
- `acpx`: Title, labels, files, and logic explicitly target silent `acpx` backend exits in `extensions/acpx`.
- `reliability`: Reclassifies silent non-zero backend exits as backend unavailable to improve availability handling and fallback guidance.

## openclaw-openclaw-42606 — Browser: harden noVNC bootstrap headers

- labels: `api_surface, browser_automation, security`
- `api_surface`: Changes HTTP response headers and contract for the `/sandbox/novnc` bootstrap route.
- `browser_automation`: Targets the browser bridge/noVNC sandbox observer bootstrap page.
- `security`: Adds CSP nonce, nosniff, frame-deny headers, and preserves token/password handling for hardening.

## openclaw-openclaw-85660 — GitHub Copilot plugin: agents.defaults.imageModel for unknown Copilot model ID falls back to OpenAI provider with confusing 401

- labels: `config, security, skills_plugins`
- `config`: The repro centers on setting agents.defaults.imageModel to a Copilot model ID and how that config is resolved.
- `security`: A GitHub Copilot token is sent to OpenAI due to wrong provider fallback, creating a credential-scope/security concern.
- `skills_plugins`: The bug is in the GitHub Copilot plugin/extension manifest and model resolver paths.

## openclaw-openclaw-77345 — google-vertex SSRF guard blocks fake-IP DNS (model.baseUrl not set for built-in providers)

- labels: `model_serving, security`
- `model_serving`: Bug is in model transport/endpoint hostname handling for the built-in Google Vertex provider request URL.
- `security`: Core failure is SSRF guard behavior blocking fake-IP private/special-use DNS results and requiring a scoped security fix.

## openclaw-openclaw-84997 — [AI-assisted] Add NEAR AI Cloud provider

- labels: `local_model_providers, auth_identity`
- `local_model_providers`: Adds a bundled OpenAI-compatible `nearai` provider with base URL, model catalog discovery, fallback catalog, and provider compatibility metadata.
- `auth_identity`: Adds API-key onboarding and token configuration for `NEARAI_API_KEY` as part of the provider setup.

## openclaw-openclaw-45841 — [Feature]: Sandboxing + ACP

- labels: `acp, sandboxing, security, sessions`
- `acp`: Issue is explicitly about enabling sandboxed OpenClaw sessions to spawn and control ACP sessions.
- `sandboxing`: Core problem is ACP compatibility when OpenClaw runs inside Docker/container sandboxes.
- `security`: Motivation centers on preserving isolation, limiting host access, and using an auditable opt-in bridge.
- `sessions`: The requested behavior concerns sandboxed sessions using sessions_spawn/spawn-steer-cancel for ACP sessions.

## openclaw-openclaw-65187 — test: add regression tests for <final> tag stripping in UI message extraction

- labels: `tests_ci, ui_tui`
- `tests_ci`: PR only adds regression tests in message-extract.test.ts and reports UI test execution.
- `ui_tui`: Tests target Control UI chat message extraction and stripping leaked assistant tags from the UI surface.

## openclaw-openclaw-71594 — docs(gateway): clarify IPv4-only BYOH bind path

- labels: `docs, gateway`
- `docs`: PR explicitly updates CLI docs, TSDoc/help text, and messaging to clarify IPv4-only BYOH behavior.
- `gateway`: The clarified behavior is specifically about Gateway bind modes and gateway.customBindHost.

## openclaw-openclaw-81957 — ci: harden GitHub Actions supply-chain boundaries

- labels: `security, tests_ci, auth_identity, packaging_deployment`
- `security`: PR explicitly hardens supply-chain boundaries, workflow permissions, token exposure, trusted refs, and action pinning.
- `tests_ci`: Changes are primarily GitHub Actions CI/release workflows and add focused regression coverage.
- `auth_identity`: OIDC trusted publishing, removal of long-lived token fallback, and npm auth scoping are central changes.
- `packaging_deployment`: Release/publish workflows and plugin npm package publishing paths are directly modified.

## openclaw-openclaw-88400 — fix(config): accept overlays for bundled provider aliases

- labels: `config, local_model_providers`
- `config`: PR changes the OpenClaw config schema allowlist so provider overlay aliases validate without baseUrl or models.
- `local_model_providers`: The fix is specifically about model provider aliases and lightweight provider overlay configuration.

## openclaw-openclaw-47083 — fix: respect totalTokensFresh flag to avoid showing stale token counts

- labels: `sessions, telemetry_usage, ui_tui`
- `sessions`: Fix concerns session list/session info rows and a per-session totalTokensFresh state flag.
- `telemetry_usage`: Central behavior is whether token counts/usage totals are displayed when fresh versus stale.
- `ui_tui`: Changes directly affect both TUI and Web UI presentation of session token counts.

## openclaw-openclaw-43416 — feat(ui): add copy button for assistant messages

- labels: `ui_tui`
- `ui_tui`: Adds a hover-triggered copy button and visual feedback in the chat message UI.

## openclaw-openclaw-63007 — Pass outbound session identity into message_sending and surface guarded gateway send denial

- labels: `gateway, hooks, notifications, sessions`
- `gateway`: PR explicitly fixes the `gateway call send` path and changes gateway server send handlers/tests.
- `hooks`: Central change passes `agentId` and `sessionKey` into the `message_sending` plugin hook context.
- `notifications`: It changes guarded outbound message delivery behavior and surfaces delivery cancellation instead of a generic no-result response.
- `sessions`: The main data being propagated is outbound session identity via `agentId` and `sessionKey`.

## openclaw-openclaw-42425 — fix(hooks): load workspace hooks for non-default agents

- labels: `hooks, gateway, sessions`
- `hooks`: PR directly changes hook loading, workspace-local hook registration, handler scoping, and hook loader tests.
- `gateway`: Fix occurs at gateway startup and updates server-startup to load hooks for all agent workspaces.
- `sessions`: Workspace hook scope is resolved from event/session context, including session keys and session-agent resolution tests.

## openclaw-openclaw-88816 — [Bug]: v2026.05.28 breaks Google Vertex Express API Key

- labels: `auth_identity, config, local_model_providers`
- `auth_identity`: Issue is specifically about Google Vertex Express API key auth via auth-profile.json.
- `config`: Failure depends on openclaw.json and auth-profile.json provider/model configuration after upgrade.
- `local_model_providers`: Error is unable to resolve/register the google-vertex model provider and its models[].

## openclaw-openclaw-71537 — Recover archived (.reset) session transcripts in memory hook + session-logs skill

- labels: `memory, sessions, skills_plugins`
- `memory`: Fixes the session-memory hook so reset-archived transcripts are recovered for memory summarization.
- `sessions`: Core behavior concerns session reset archives, session transcript filenames, and finding previous session logs.
- `skills_plugins`: Updates the session-logs skill guidance so it can search active and archived session transcripts.

## openclaw-openclaw-41892 — feat(control-ui): add cron calendar timeline view

- labels: `cron_automation, ui_tui`
- `cron_automation`: PR is centered on cron jobs, scheduled tasks, upcoming runs, high-frequency jobs, and run-history navigation.
- `ui_tui`: Adds a Control UI Cron Jobs page timeline view with hover popups, zoom controls, theme support, and mobile fallback.

## openclaw-openclaw-84761 — feat(secrets): scan backup files for plaintext provider apiKey values

- labels: `security, auth_identity, config`
- `security`: Adds secret scanning for plaintext API keys left in backup files, closing a credential exposure gap.
- `auth_identity`: The scanned secrets are provider apiKey credentials used for authentication.
- `config`: The feature inspects backup config files such as models.json.* and openclaw.json.old in config/agent directories.

## openclaw-openclaw-43246 — fix(message): deny same-provider cross-context sends by default [AI-assisted]

- labels: `chat_integrations, config, notifications, security`
- `chat_integrations`: The fix targets Slack, WhatsApp, iMessage, and similar provider/channel conversation routing.
- `config`: Behavior is controlled by the new default/opt-in setting `tools.message.crossContext.allowWithinProvider=true` and config help/type updates.
- `notifications`: Core change is an outbound message delivery policy that blocks cross-context sends by default.
- `security`: PR explicitly hardens a security boundary to prevent cross-channel/context data leaks.

## openclaw-openclaw-59208 — fix(status): honor selected usage auth profile

- labels: `auth_identity, telemetry_usage, ui_tui`
- `auth_identity`: Fixes OAuth profile selection so the session-selected auth profile is honored for provider usage resolution.
- `telemetry_usage`: Directly affects usage/quota summary loading and the displayed usage line in /status.
- `ui_tui`: The bug is in the user-facing /status status card/text where auth and usage lines were inconsistent.
