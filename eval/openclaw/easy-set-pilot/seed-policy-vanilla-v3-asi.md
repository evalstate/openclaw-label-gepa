Classify the GitHub issue or pull request for OpenClaw maintainer-interest routing.

Use only the supplied GitHub context. Prefer the title and main problem or feature
statement. Use body, comments, labels, changed files, and diff as supporting evidence.

Select every allowed topic that is central to routing the item to the right maintainer
interest. Do not select topics that are only incidental implementation details,
examples, tests, file paths, or possible consequences.

Use the smallest label set that captures the central routing interests. Return an
empty list if no allowed topic centrally applies.

## Easy-set v3 ASI boundary rules

These are generalized cue classes mined from easy-final-v2 relabel and stability
runs. Do not memorize issue IDs, titles, URLs, or exact scenario bundles.

- External coding-agent products/backends/harnesses (Codex, Claude Code, Gemini
  CLI, Pi, external approval/sandbox/tool harnesses) -> `coding_agents`; add
  `codex` only when Codex itself is central. Internal OpenClaw subagent/runtime/
  session orchestration -> `agent_runtime`, `sessions`, `queueing`, and/or `acp`,
  not `coding_agents`, unless an external coding backend is central.
- Use `acp` for ACP protocol, ACP task lifecycle semantics, ACP sessions/tools,
  or ACP binding behavior. Use `acpx` only when ACPX transport/proxy/backend,
  ACPX config/env/auth, or extension/acpx files are central.
- Use `agent_runtime` for OpenClaw internal execution machinery: subagent
  lifecycle, runtime state machine, child task outcome, turn execution,
  abort/final outcome, run supervision, task ledger, and embedded attempt state.
- Named model/version additions, removals, catalog updates, or provider registry
  entries -> `model_releases`; also add `config` for defaults/schema/catalog
  settings and `model_serving` for endpoint/routing/serving compatibility.
  Do not add `reliability` merely because a missing catalog entry causes a
  confusing error unless crashes, hangs, retries, stale state, data loss, or
  operational failure are central.
- Use `open_weight_models` only for central open-weight model family behavior,
  packaging, quantization, context metadata, compatibility, benchmarks, or
  routing/selection. Do not use it merely because model-family names such as
  DeepSeek, Qwen, GLM, GGUF, MiMo, or Llama appear.
- `local_models` = concrete local/on-device inference behavior: Ollama, LM
  Studio, llama.cpp, GGUF, local GPU/VRAM/Metal/MLX, local backend timeouts or
  crashes, local embeddings, or specific local model behavior.
  `local_model_providers` = local/self-hosted/custom OpenAI-compatible provider
  setup, auth, discovery, routing, adapter compatibility, or baseUrl
  normalization. `self_hosted_inference` = deployment/operation of a
  self-hosted inference service, including TTS/STT/embedding services; do not
  use it merely because a local model or GGUF is mentioned.
- Use `skills_plugins` only when a real skill/plugin product surface is central:
  manifests, loading, registration, allowlists, hooks, SecretRefs, skill files,
  preludes/wrappers, plugin SDK/runtime APIs, MCP Apps, or plugin-owned
  user-visible behavior. Do not add it merely because code is in an extension
  package or an implementation file is plugin-adjacent.
- Use `reliability` for central robustness/recovery/failure behavior: crashes,
  hangs, timeouts, retries, stale state, stuck lifecycle, dropped output, data
  loss, orphaned work, cleanup races, fallback loops, leaks, or user-visible
  operational failure. Do not add it merely for cryptic validation errors,
  safer CI guards, or blocked workflows.
- Workflow/test/CI changes -> `tests_ci` when tests, CI workflows, lint/typecheck,
  fixture behavior, coverage, or validation tooling are central. Do not add
  `docs` for docs-sync workflow files unless documentation content itself
  changes. Do not add `reliability` for fork-only CI guardrails unless runtime
  robustness is central.
- Documentation of config option bounds, defaults, examples, or behavior ->
  `docs` + `config`. Add `exec_tools` only when shell/subprocess/PTY/command
  behavior itself is central. Do not add `gateway` merely because related code is
  near gateway routing or consumed by the gateway.
- Visible session/user display in channel-connected surfaces: use
  `chat_integrations` for external chat-channel identity/message behavior,
  `sessions` for session list/state/identity/storage/transcript/resume, and
  `ui_tui` for visible CLI/TUI/web display. Do not add `config` unless
  settings/defaults/schema are central. Do not add `acp` merely because a
  session exists.
- Generic notification policy, delivery gates, completion announcements, or
  notify settings -> `notifications`. Named Discord/Telegram/Slack/webchat
  message behavior -> `chat_integrations`; delivery loss/retry/fallback can add
  `reliability` when operationally central.
- Security labels require a central security boundary: credentials, secrets,
  tokens, auth hardening, SSRF, HMAC, vulnerabilities, unsafe data access, or
  leakage prevention. Do not add `security` merely for a 401/error mention unless
  auth/credential or leak behavior is central.
- API labels require a public/API contract, HTTP or tool/request/response shape,
  schema, endpoint, webhook/SSE/OpenResponses/Chat Completions compatibility, or
  user-facing contract. Do not use `api_surface` for incidental helper changes.
