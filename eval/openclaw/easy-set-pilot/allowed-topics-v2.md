## Allowed Topics

```json
[
  "local_models",
  "local_model_providers",
  "model_serving",
  "self_hosted_inference",
  "open_weight_models",
  "acpx",
  "acp",
  "coding_agents",
  "mcp_tooling",
  "hf_agents",
  "hub_workflows",
  "post_training",
  "model_releases",
  "agent_demos",
  "codex",
  "agent_runtime",
  "sessions",
  "gateway",
  "exec_tools",
  "approvals",
  "sandboxing",
  "hooks",
  "cron_automation",
  "chat_integrations",
  "ui_tui",
  "browser_automation",
  "memory",
  "security",
  "config",
  "packaging_deployment",
  "docs",
  "tests_ci",
  "telemetry_usage",
  "api_surface",
  "queueing",
  "notifications",
  "skills_plugins",
  "auth_identity",
  "reliability",
  "tool_calling"
]
```

## Topic definitions and cue words

- `local_models`: Concrete local/on-device model execution and local inference behavior: local model UX, local-only fallback, local backend crashes/timeouts, and local hardware constraints. Use when a specific local backend/model family is central, not merely because an API is OpenAI-compatible. Cue words: local model, local models, local llm, offline model, on-device model, ollama, lm studio, lmstudio, llama.cpp, gguf, gemma, qwen, mlx, local gpu, vram, cold start, ggml-metal
- `local_model_providers`: Provider configuration, discovery, auth, routing, and compatibility for local, self-hosted, or user-configured OpenAI-compatible model backends. This is the API/provider layer around local or self-hosted models, not ordinary hosted cloud providers. Cue words: local provider config, self-hosted provider setup, openai-compatible provider, custom base url, OPENAI_BASE_URL, provider preflight, local provider auth, model resolver, model discovery, fallback chain, litellm, lm studio provider, ollama provider, vllm provider, tgi provider, localai provider
- `model_serving`: Model endpoint serving protocols and compatibility for hosted or local endpoints: streaming behavior, request/response routing, lifecycle, OpenAI-compatible endpoint semantics, model registration/selection failures, and provider endpoint behavior. Cue words: vllm, tgi, localai, openai-compatible streaming, chat completions, responses api, stream closed, usage chunk, endpoint lifecycle, multi-endpoint, request routing, sampling parameters, frequency_penalty, presence_penalty, seed, sse heartbeat, model provider, model registration
- `self_hosted_inference`: Self-hosted inference systems and locally operated services, including embeddings, speech, and memory providers. Cue words: self-hosted, self hosted, local server, private inference, embeddings, memory provider, ollama embeddings, lancedb, speech-to-text, stt, text-to-speech, tts, gateway routed tts, no_proxy, proxy bypass, ssrf
- `open_weight_models`: Open-weight model families, model packaging, quantization, and local deployability signals. Cue words: open weight, open weights, hugging face model, model weights, gguf, quantized, quantization, safetensors, model card, weights download, checkpoint
- `acpx`: ACPX protocol, transport, proxy, backend process, compatibility, and files or commands explicitly named ACPX. Cue words: acpx, extensions/acpx, acpx proxy, acpx backend, acpx transport, acpx command, acpx exec, silent acpx exit, acpx compatibility, acpx session, acpx auth, acpx hmac
- `acp`: ACP protocol features and session tools that are not necessarily ACPX-specific. Cue words: acp, agent client protocol, acp_send, sessions_spawn, sessions_cancel, acp session, acp block, acp runtime, acp binding, acp server, acp client
- `coding_agents`: External coding-agent integrations and runs such as Codex, Claude Code, Gemini/CLI coding agents, Pi, or coding-agent harnesses/tools/approvals/sandboxes. Do not use for purely internal OpenClaw subagent/runtime orchestration unless an external coding-agent backend is central. Cue words: codex, claude code, gemini coding agent, agent run, external coding agent, coding-agent harness, exec approval, toolsAllow, sandbox, durable exec
- `mcp_tooling`: MCP server or client behavior, tools/list, resources, and tool invocation compatibility. Cue words: mcp, model context protocol, tools/list, tool invocation, mcp server, mcp client, resources/list, prompts/list, hermes agent
- `hf_agents`: Hugging Face agent workflows, Spaces, Hub agent demos, or HF-specific agent integrations. Cue words: hugging face, huggingface, hf agent, smolagents, transformers agents, space, dataset repo, hub workflow
- `hub_workflows`: Hub automation for datasets, models, Spaces, releases, and repository synchronization. Cue words: hub, dataset upload, model upload, space deploy, huggingface hub, hf hub, repo sync, lfs, dataset card, model card
- `post_training`: Fine-tuning, preference optimization, evaluation loops, and data generation after pretraining. Cue words: fine tune, finetune, sft, dpo, rlhf, distillation, eval set, preference data, synthetic data, post training
- `model_releases`: New model release tracking or version-specific model behavior. Cue words: model release, new model, release notes, version bump, model family, benchmark, eval
- `agent_demos`: Demo workflows and visible examples for agents. Cue words: demo, showcase, example agent, agent demo, walkthrough, sample workflow
- `codex`: Items that explicitly involve the Codex runtime or command compatibility. Cue words: codex, codex cli, codex acp, codex command, codex runtime, native vision
- `agent_runtime`: Agent runner, harness, orchestration, subagent execution, heartbeat, and agent lifecycle behavior. Cue words: agent run, runner, harness, subagent, spawn, heartbeat, orchestration, embedded runner, attempt, agent lifecycle, agent wait, child task
- `sessions`: Session identity, persistence, binding, transcript, resume, reset, parent/child session behavior, and session stores. Cue words: session, sessions, session key, session store, transcript, resume, reset, thread-bound, parent session, child session, bound session, session list
- `gateway`: OpenClaw gateway behavior, daemon startup, HTTP gateway routes, gateway restart, gateway state, and service health. Cue words: gateway, daemon, gateway restart, gateway state, gateway api, http gateway, service health, startup, launcher
- `exec_tools`: Shell execution, exec tools, command allowlists, tool invocation, tool schemas, and durable process handling. Cue words: exec, command, tool call, tools, tools/invoke, allowlist, safeBins, durable exec, process, shell, tool_choice
- `approvals`: Approval flows, permission modes, approve/deny commands, policy checks, and pending approval state. Cue words: approval, approve, deny, permissionMode, approval-pending, exec approval, tools.deny, policy
- `sandboxing`: Sandbox isolation, containers, Docker, process limits, filesystem hiding, and execution boundaries. Cue words: sandbox, container, docker, bubblewrap, pidsLimit, isolation, filesystem, workspace, volumes
- `hooks`: Hook lifecycle, hook events, hook payloads, hook filtering, and managed hook behavior. Cue words: hook, hooks, before_agent_start, agent_end, before_tools_resolve, message hooks, hook trigger, hook ingress
- `cron_automation`: Cron jobs, scheduled runs, heartbeat automation, one-shot jobs, and recurring task execution. Cue words: cron, scheduled, schedule, heartbeat, one-shot, job execution, deleteAfterRun, at jobs
- `chat_integrations`: Chat platform integrations and delivery surfaces such as Discord, Telegram, Slack, Feishu, WhatsApp, Zulip, Mattermost, and webchat. Cue words: discord, telegram, slack, feishu, whatsapp, zulip, mattermost, webchat, channel, dm, thread, topic
- `ui_tui`: Control UI, TUI, dashboard, web UI, session list, status views, and user-facing interface changes. Cue words: ui, tui, dashboard, web ui, session list, status footer, preview, display name, chat ui
- `browser_automation`: Browser automation, screenshots, Chrome integration, browser vision, and web interaction tooling. Cue words: browser, chrome, screenshot, vision, web page, google sign-in, profile attach
- `memory`: Memory systems, embeddings, vector stores, active memory, LanceDB, and memory archival or recovery. Cue words: memory, embedding, embeddings, vector, lancedb, active-memory, archive, recall, memory hook
- `security`: Security, SSRF, credentials, secrets, token handling, auth hardening, HMAC, vulnerabilities, and unsafe access prevention. Cue words: security, ssrf, credential, secret, token, api key, hmac, auth, oauth, vulnerability, private/internal, password, redaction
- `config`: Configuration files, config schema, defaults, setup/onboarding, environment variables, overrides, and migration. Cue words: config, configuration, defaults, setup, onboarding, env, environment, override, migration, schema, baseUrl
- `packaging_deployment`: Build, packaging, deployment, service managers, SEA, launchd, systemd, pnpm, and runtime distribution. Cue words: build, package, sea, deployment, launchd, systemd, pnpm, postbuild, single executable, service path
- `docs`: Documentation, guides, README changes, spelling, taxonomy, and explanatory content. Cue words: docs, documentation, readme, guide, clarify, spelling, taxonomy, quick start
- `tests_ci`: Tests, CI, fixtures, coverage, mocks, and platform-specific test fixes. Cue words: test, tests, ci, coverage, mock, mocks, fixture, fixtures, windows ci, test coverage
- `telemetry_usage`: Usage accounting, token counts, cost metadata, traces, diagnostics, status reporting, and observability. Cue words: usage, cost, tokens, trace, diagnostic, telemetry, status, reporting, metrics, signalCount
- `api_surface`: HTTP APIs, gateway APIs, REST endpoints, webhooks, SSE, OpenResponses, chat completions, and request/response contracts. Cue words: api, http, webhook, sse, responses, chat completions, /v1, endpoint, request, response, tools/invoke
- `queueing`: Queues, lanes, task state, follow-up queues, run ordering, locks, stuck jobs, and backpressure. Cue words: queue, lane, task, followup, follow-up, lock, backpressure, stuck, pending, running
- `notifications`: Notification policy, delivery gates, notify settings, outbound messages, announcements, and sent-message handling. Cue words: notify, notification, announce, delivery, message delivery, done_only, silent, completion delivery
- `skills_plugins`: Skills/plugins as product surfaces: SKILL.md, managed skills, plugin manifests/loading/registration, plugin SDK/runtime APIs, MCP Apps, plugin hooks, SecretRefs, skill sync/prelude/wrappers. Do not use merely because a package is an extension or a review skill is mentioned. Cue words: skill, skills, plugin, plugins, plugin manifest, plugin sdk, plugin runtime, managed skills, superpowers, hook pack, mcp apps
- `auth_identity`: Authentication, identity, OAuth, device identity, profile selection, account binding, token-only auth, and credential scope. Cue words: auth, oauth, identity, device identity, profile, account, token-only, credential, api key, login
- `reliability`: Reliability fixes for retries, stale state, crashes, timeouts, recovery, cleanup, race conditions, and wedged processes. Cue words: retry, stale, crash, timeout, recover, cleanup, race, wedged, dead, orphaned, fail fast, restart, liveness
- `tool_calling`: Model tool-calling behavior, tool-call deltas, tool schemas, tool result routing, and tool-use compatibility. Cue words: tool call, tool-call, tool_use, tool schema, tool result, tools array, tool_choice, parallel tool call, function call
