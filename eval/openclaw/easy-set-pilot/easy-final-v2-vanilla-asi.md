# easy-final-v2 vanilla ASI

Forward-path ASI for the easy-set-pilot vanilla labeler. These rules are for
approved-label review and small-model vanilla/GEPA runs. They are generalized
boundary rules, not row-specific overrides.

## Stability-first approved-label policy

- Keep a row in the easy exact-match set only when the topic set is defensible
  without multiple boundary exceptions.
- If repeated runs disagree because taxonomy boundaries overlap, keep the row as
  medium/ASI material rather than forcing it into easy exact-match evaluation.
- Do not encode issue IDs, titles, or exact scenario bundles in prompts. Convert
  every failure into reusable cue -> label guidance.

## coding_agents / codex / agent_runtime / acp

- Use `coding_agents` only when an external coding-agent product, backend, or
  harness is central: Codex, Claude Code, Gemini CLI, Pi, external approval,
  sandbox, or tool harnesses.
- Use `codex` when the Codex product, provider/config, ACP integration, or Codex
  runtime behavior is central.
- Use `agent_runtime` for OpenClaw internal execution machinery: subagent
  lifecycle, runtime state machine, child task outcome, turn execution,
  abort/final outcome, run supervision, and task-ledger state.
- Use `acp` only when Agent Client Protocol transport, protocol surface, or ACP
  task lifecycle semantics are central.
- Do not use `coding_agents` merely for internal OpenClaw subagents unless an
  external coding-agent backend is part of the row.

## model_releases / open_weight_models

- Use `model_releases` when a row asks to add, update, deprecate, rename, or
  document a named model/version in a provider catalog or built-in model
  registry. This can co-occur with `config` and `model_serving`.
- Do not replace `model_releases` with `open_weight_models` just because a model
  family name appears.
- Use `open_weight_models` only when the row is centrally about open-weight model
  family behavior, compatibility, benchmarks, context-window metadata, provider
  support, or routing/selection for those open-weight families.
- Do not add `open_weight_models` merely because the row mentions DeepSeek, Qwen,
  GLM, GGUF, MiMo, Llama, or similar model-family names.

## skills_plugins

- Use `skills_plugins` only when a real skill/plugin product surface is central:
  plugin manifests, loading, registration, allowlists, hooks, SecretRefs, skill
  files/prelude/wrappers, plugin SDK/runtime APIs, MCP Apps, or plugin-owned
  user-visible behavior.
- Do not add `skills_plugins` merely because code lives in an extension package,
  a bot/review skill is mentioned, or implementation files are plugin-adjacent.

## reliability

- Use `reliability` when runtime robustness, recovery, or failure behavior is
  central: crashes, hangs, timeouts, retries, stale state, stuck lifecycle,
  dropped output, data loss, orphaned work, cleanup races, fallback loops, or
  user-visible operational failure.
- Do not add `reliability` merely because an error is confusing, a validation
  message is cryptic, a CI workflow is safer, or a guard blocks something.

## local_models / local_model_providers / self_hosted_inference

- Use `local_models` for concrete local/on-device inference behavior: Ollama, LM
  Studio, llama.cpp, GGUF, local GPU/VRAM/Metal/MLX, local backend
  timeouts/crashes, local embedding behavior, or specific local model behavior.
- Use `local_model_providers` for local/self-hosted/custom OpenAI-compatible
  provider setup, auth, discovery, routing, adapter compatibility, or base URL
  normalization.
- Use `self_hosted_inference` only when the central issue is deployment or
  operation of a self-hosted inference service, not ordinary local model runtime
  behavior.
- Do not use `self_hosted_inference` merely because a local model or GGUF is
  mentioned.

## docs / config / exec_tools / gateway

- If the row documents config option bounds, defaults, or behavior, use `docs` +
  `config`.
- Add `exec_tools` only when shell, subprocess, PTY, command launch, command
  output, exit status, or durable exec behavior is itself central.
- Do not add `exec_tools` merely because a documented config key affects command
  execution timing.
- Do not add `gateway` merely because a documented option is consumed near
  gateway or command-routing code.

## chat_integrations / sessions / ui_tui / config

- Use `chat_integrations` when external chat-channel identity, user metadata,
  message state, or channel-specific behavior is central.
- Use `sessions` when session list/state/identity/storage/transcript/resume or
  session-key behavior is central.
- Use `ui_tui` when the visible CLI/TUI/web display is central.
- Do not add `config` merely because display-name mapping or identity resolution
  could require stored settings. Add `config` only when settings/defaults/schema
  are central.
