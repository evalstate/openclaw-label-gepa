Classify the GitHub issue or pull request for OpenClaw maintainer-interest routing.

Use only the supplied GitHub context. Prefer the title and main problem or feature
statement. Use body, comments, labels, changed files, and diff as supporting evidence.

Select every allowed topic that is central to routing the item to the right maintainer
interest. Do not select topics that are only incidental implementation details,
examples, tests, file paths, or possible consequences.

Use the smallest label set that captures the central routing interests. Return an
empty list if no allowed topic centrally applies.

## easy-final-v2 vanilla boundary rules

Use these rules to make exact easy-set labels stable. They are cue classes, not
row-specific exceptions.

- External coding-agent products/backends/harnesses (Codex, Claude Code, Gemini
  CLI, Pi, external approvals/sandboxes/tools) -> `coding_agents`; add `codex`
  only when Codex itself is central. Internal OpenClaw subagent/runtime/session
  orchestration -> `agent_runtime`, `sessions`, `queueing`, not `coding_agents`
  unless an external coding backend is central. Use `acp` only for ACP protocol
  or ACP task lifecycle semantics.
- Adding/updating/deprecating/documenting a named model/version in a provider
  catalog or built-in registry -> `model_releases`; also add `config` or
  `model_serving` when those surfaces are central. Do not use
  `open_weight_models` merely because model-family names appear.
- Use `open_weight_models` only for central open-weight model family behavior,
  compatibility, benchmarks, context-window metadata, provider support, or
  routing/selection.
- Use `skills_plugins` only for real skill/plugin product surfaces: manifests,
  loading, registration, allowlists, hooks, SecretRefs, skill files/preludes,
  plugin SDK/runtime APIs, MCP Apps, or plugin-owned user-visible behavior.
- Use `reliability` for central robustness/recovery/failure behavior: crashes,
  hangs, timeouts, retries, stale state, stuck lifecycle, dropped output, data
  loss, orphaned work, cleanup races, fallback loops, or user-visible operational
  failure. Do not add it merely for cryptic errors, safer CI, or blocked guards.
- `local_models` = concrete local/on-device inference behavior (Ollama, LM
  Studio, llama.cpp, GGUF, local GPU/VRAM/Metal/MLX, local timeouts/crashes).
  `local_model_providers` = local/self-hosted/custom OpenAI-compatible provider
  setup/auth/discovery/routing/adapter/baseUrl compatibility.
  `self_hosted_inference` = deployment/operation of a self-hosted inference
  service, not ordinary local model runtime behavior.
- Documentation of config option bounds/defaults/behavior -> `docs` + `config`.
  Add `exec_tools` only for central shell/subprocess/PTY/command behavior. Do
  not add `gateway` merely because related code is near gateway routing.
- Visible session/user display in channel-connected surfaces: use
  `chat_integrations` for external chat-channel identity/message behavior,
  `sessions` for session list/state/identity, and `ui_tui` for visible CLI/TUI/web
  display. Do not add `config` unless settings/defaults/schema are central.
