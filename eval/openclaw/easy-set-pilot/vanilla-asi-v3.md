# OpenClaw easy-set vanilla ASI v3

Current easy-set-local ASI for vanilla OpenClaw maintainer-interest routing.
This replaces the old/global `asi-pack-v4.md` naming for the easy-set pilot.
Keep it local until v3 held-out stability is verified.

## Scope

- Label source under test: `easy-final-v2*.jsonl` until reviewed/promoted.
- Prompt-safe seed: `seed-policy-vanilla-v3-asi.md`.
- Taxonomy/card surface: `allowed-topics-v3.md`, `openclaw-vanilla-labeler-v3.md`.
- Source artifacts: v2 relabel changed rows, v2 instability mining, and the
  instability review packet.

This ASI is generalized guidance, not row-specific memorization. Do not put issue
IDs, issue numbers, titles, or URL-specific exceptions into task prompts.

## Stability-first approved-label policy

- Keep a row in easy exact-match evaluation only when the topic set is defensible
  from central evidence without multiple boundary exceptions.
- If repeated runs disagree because taxonomy boundaries overlap, demote the row
  to medium/boundary ASI material rather than forcing it into exact-match easy.
- Use instability as a review trigger, not automatic relabeling. Stable wrong
  predictions can reveal unclear guidance; unstable predictions can reveal real
  taxonomy overlap.
- Apply approved-label edits to the source file first, then regenerate splits.
  Do not edit train/test/unused split files independently.
- Record provenance for reviewed rows: previous labels, final labels, decision,
  notes, and whether the row stays easy, moves to medium, or becomes ASI only.

## v2 -> v3 relabel lessons

The main approved-label shift is away from overusing `coding_agents` for internal
OpenClaw subagents:

- Internal `sessions_spawn`, subagent lane, task-ledger, announcement, active
  memory recall subagent, and OpenClaw-managed runtime behavior should prefer
  `agent_runtime`, `sessions`, `queueing`, and/or `acp`.
- Use `coding_agents` only when an external coding-agent product/backend/harness
  is central: Codex, Claude Code, Gemini CLI, Pi, or external approval/sandbox/
  tool harness behavior.
- Use `codex` alongside `coding_agents` only when Codex product/runtime/config or
  Codex ACP behavior is central.

Other relabel lessons:

- Hosted provider auth/config fixes are not `local_model_providers` unless the
  row centers local/self-hosted/custom OpenAI-compatible provider setup.
- Named model catalog additions or missing built-in provider catalog entries need
  `model_releases`; add `config` for registry/default/schema/config semantics
  and `model_serving` for endpoint/routing/selection compatibility.
- Do not add `reliability` for a merely confusing error or safer guard. Add it
  for crashes, hangs, retries, stale state, data loss, fallback loops, timeouts,
  cleanup races, or visible operational failure.

## Stability-mined boundary rules

### ACP / ACPX / Codex / coding_agents / agent_runtime / sessions / queueing

- `acp`: ACP protocol/session/tool lifecycle, ACP task status, ACP parent-child
  semantics, ACP bindings, `sessions_spawn` through ACP, or ACP delivery.
- `acpx`: ACPX proxy/transport/backend process, extension/acpx config/env/auth,
  ACPX command compatibility, HMAC, or ACPX subprocess behavior.
- `agent_runtime`: OpenClaw runner/orchestration internals: child task outcomes,
  runtime state machine, embedded attempts, agent lifecycle, turn execution,
  cancellation/abort/finalization, task ledger, or supervision.
- `sessions`: session identity, persistence, transcript, resume/reset, session
  list/state, parent-child session relationship, session store, or session key.
- `queueing`: lanes, queues, locks, follow-up queues, pending/running ordering,
  task backlog, concurrency, or backpressure.
- `coding_agents`: external coding-agent backend/harness. Do not use it for every
  subagent or every ACP row.
- `codex`: Codex runtime/CLI/ACP/config/compatibility specifically.

### Models and providers

- `model_releases`: named model/version catalog or built-in registry changes.
- `model_serving`: endpoint protocol/compatibility, Responses/Chat Completions,
  streaming/SSE, model registration/selection, serving metadata, request routing,
  or provider endpoint behavior.
- `local_models`: local/on-device inference and local backend/hardware behavior.
- `local_model_providers`: local/self-hosted/custom OpenAI-compatible provider
  setup/auth/discovery/routing/baseUrl/adapter compatibility.
- `self_hosted_inference`: operating a self-hosted inference service, including
  embeddings/TTS/STT services; not ordinary local model execution.
- `open_weight_models`: open-weight model family/package/quantization/context/
  compatibility behavior, not mere model-family name mentions.

### Plugins, skills, hooks, MCP, approvals

- `skills_plugins`: plugin/skill product surfaces: manifests, loading,
  registration, SDK/runtime APIs, skill files/preludes/wrappers, SecretRefs,
  allowlists, plugin hooks, MCP Apps, plugin-owned user-visible behavior.
- `hooks`: hook lifecycle, payload/filtering, managed hook behavior, priority,
  or hook event semantics. Do not replace a central hook issue with generic
  `skills_plugins` unless plugin surfaces are also central.
- `mcp_tooling`: MCP server/client tools/resources/prompts/list/invocation
  compatibility.
- `approvals`: permission modes, approve/deny flows, pending approvals,
  policy checks, or approval state.

### Docs / config / tests / API / exec

- `config`: settings, defaults, schema, setup/onboarding, env vars, overrides,
  migrations, persisted config, or config validation.
- `docs`: documentation content, guides, README, taxonomy/explanatory content.
  Docs about config bounds/defaults usually require `docs` + `config`.
- `tests_ci`: tests, CI workflows, fixtures, coverage, lint/typecheck, platform
  test fixes, validation scripts, or flake handling. Fork-only workflow guards
  are `tests_ci`, not `reliability` unless runtime robustness is central.
- `api_surface`: public/API contract, HTTP/webhook/SSE/OpenResponses/Chat
  Completions, request/response schema, tool/API contract, or endpoint behavior.
- `exec_tools`: shell/subprocess/PTY/command execution, durable process handling,
  command allowlists/approval, command output/exit status. Do not add it for docs
  that merely mention command-timing config unless command behavior is central.

### Chat, UI, notifications, reliability, security

- `chat_integrations`: named external chat surfaces and channel/message identity
  or delivery behavior: Discord, Telegram, Slack, Feishu, WhatsApp, Zulip,
  Mattermost, webchat, channels/DMs/threads/topics.
- `ui_tui`: visible CLI/TUI/web/dashboard/session-list/status/help display.
- `sessions`: session state/identity/storage/transcript/resume/list behavior.
- `notifications`: generic notification policy, delivery gates, notify settings,
  completion announcements, or notifier mechanics.
- `reliability`: crashes, hangs, timeouts, retry/fallback loops, stale state,
  stuck lifecycle, dropped output, data loss, orphaned work, cleanup races, leaks,
  health/liveness failure, or operational wedging.
- `security`: credentials, secrets, token handling, auth hardening, HMAC, SSRF,
  vulnerabilities, unsafe access prevention, cross-context/data leakage.

## Pending approved-label review from instability mining

The v3 ASI guidance is ready to test, but the approved-label source still needs
manual review before calling the data itself v3:

- Rows marked `drop_to_medium` or `asi_only` in the instability packet should be
  removed from easy exact-match evaluation or manually confirmed.
- Rows marked `keep_easy_with_asi` should stay easy only after confirming the
  labels are defensible with the generalized rules above.
- Rows marked `fix_labels_or_add_asi` or `review_or_drop_to_medium` need human
  adjudication before promotion.

Until that review is applied, use run names like `easy-final-v2-...-v3-asi` to
make clear that the data is v2 and the guidance/ASI is v3.
