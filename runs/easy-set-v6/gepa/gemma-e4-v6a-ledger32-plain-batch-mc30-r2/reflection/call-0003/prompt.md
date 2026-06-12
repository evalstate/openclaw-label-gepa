You are an expert optimization assistant. Your task is to analyze evaluation feedback and propose an improved version of a system component.

## Optimization Goal

Improve only the mutable OpenClaw vanilla labeler routing policy.

The fixed AgentCard header, plain comma-separated topic-ID output contract, schema enum, GitHub context renderer,
and allowed-topic taxonomy are not editable.

Primary objective: maximize row-aware GEPA score = 0.50*topic_micro_f1 + 0.20*row_exact_accuracy + 0.30*avg_row_jaccard. Do not optimize for recall-biased F-beta. Use precision, recall, exact match,
row Jaccard, row symdiff, cardinality, topic confusions, row examples, and
prompt-hygiene ASI to understand how to improve reliable row-level reproduction.

Keep the policy vanilla and compact. Prefer short reusable centrality/cardinality rules
over a long topic-by-topic rulebook.

Keep the mutable policy under 12,000 characters; over-budget policies receive a small
GEPA score penalty, so compress rules instead of accumulating exhaustive topic tables.

Preserve comma-separated topic-ID-only behavior; do not ask for JSON, prose, bullets, or explanations.

Do not copy, rewrite, reorder, rename, delete, extend, or replace the fixed allowed-topic
list, topic definitions, or cue/keyword list. Reference exact existing topic IDs only
when a concise reusable boundary rule needs them.

Do not include row IDs, issue numbers, exact titles, URLs, or copied examples. Do not add
memorized issue/title/keyword tables.

Do not include data-build notes, version-history commentary, teacher/adjudication
procedure, promotion rules, or confusion-bucket bookkeeping in the task policy.


## Domain Context & Constraints

The task model sees this fixed taxonomy before the mutable policy:

```md
## Allowed Topics

Use only the topic IDs listed below. Choose labels by central
maintainer-routing concern, not by keyword match.

```json
[
  "local_models",
  "inference_api",
  "self_hosted_inference",
  "acpx",
  "acp",
  "coding_agents",
  "mcp_tooling",
  "model_lifecycle",
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

## Topic definitions

- `local_models`: Model-artifact and local-hardware behavior on device: GGUF/quantization behavior, VRAM and hardware constraints, model-family quirks, local model UX/fallback, and local model context behavior. Engine integration itself belongs to `self_hosted_inference`.
- `inference_api`: The integration layer between OpenClaw and model serving/providers: usage of Responses, Chat Completions, Anthropic Messages, and similar inference APIs; streaming/SSE and usage chunks; base URL normalization; request/response handling for inference, including TTS, vision, and embeddings API integrations; and adding or configuring inference providers (setup, auth, routing, catalogs, compatibility).
- `self_hosted_inference`: Integration with inference engines such as vLLM, llama.cpp, Ollama, LM Studio, TGI, or LocalAI — whether on device or self-hosted elsewhere: engine setup, lifecycle, compatibility, engine crashes/timeouts, and self-hosted embeddings/speech/memory backends.
- `acpx`: ACPX protocol, transport, proxy, worker/backend process, configured binding, compatibility, and files or commands explicitly named ACPX.
- `acp`: ACP protocol features, ACP sessions, binding, parent/child behavior, and delivery semantics that are not necessarily ACPX-specific.
- `coding_agents`: Integrations with external coding agents in general, or with a specific coding agent such as Codex, Claude Code, Gemini CLI, or Pi. Internal OpenClaw subagents, `sessions_spawn` plumbing, ACP parent/child behavior, queue lanes, trace producers, tool-use mechanics, approval flows, sandboxing, compaction, and agent runtime machinery do not qualify unless the item is specifically about a coding-agent integration.
- `mcp_tooling`: MCP server or client behavior, MCP allow/deny rules, conformance checks, handshake/tool behavior, MCP config, tools/list and resources, and tool invocation compatibility.
- `model_lifecycle`: Introduction, decommissioning, or adjustment of model configurations: adding/removing/renaming model IDs, catalog and default updates, deprecations, version-specific model support, and model metadata (context windows, quantization variants) changes.
- `codex`: Items that explicitly involve the Codex runtime, Codex auth, Codex ACP, Codex plugin, or Codex command compatibility.
- `agent_runtime`: Agent runtime machinery: runtime startup, loop, backends, model call orchestration, runtime adapter behavior, and runtime ownership/execution architecture. External coding-agent integrations belong to `coding_agents`; ACP protocol/session/delivery work belongs to `acp`/`acpx`.
- `sessions`: Session identity, lifecycle, persistence, binding, transcript, resume, reset, cleanup, parent/child session behavior, and session stores.
- `gateway`: OpenClaw gateway behavior, daemon startup, HTTP gateway routes, gateway protocol, gateway restart, gateway state, gateway-owned execution, and service health.
- `exec_tools`: Shell execution, command invocation, PATH handling, exec tools, command allowlists, tool execution policy, execution output control, and durable process handling.
- `approvals`: Approval flows, permission decisions, approval prompts, approve/deny commands, approval mode behavior, policy checks, and pending approval state.
- `sandboxing`: Sandbox policy, sandbox inheritance, sandbox escape, path isolation, containers, Docker, process limits, filesystem hiding, and execution boundaries.
- `hooks`: Hook registration, hook lifecycle, hook events, hook priority, hook payloads, hook filtering, hook security, and managed hook behavior.
- `cron_automation`: Cron jobs, scheduled runs, heartbeat automation, one-shot jobs, force-run behavior, and recurring task execution.
- `chat_integrations`: Chat platform integrations, channel adapters, message ingestion, and delivery surfaces such as Discord, Telegram, Slack, Feishu, WhatsApp, Zulip, Mattermost, and webchat.
- `ui_tui`: Control UI, TUI, dashboard, web UI, mobile UI, footer/status views, session list, and user-facing interface changes.
- `browser_automation`: Browser automation, CDP/Chrome integration, browser session attach, auth browser flows, screenshots, browser vision, and web interaction tooling.
- `memory`: Memory systems, memory indexing/search, embeddings, vector stores, active memory, LanceDB, memory provider state, and memory archival or recovery.
- `security`: Security posture and boundaries: SSRF, private-network access, credential/auth boundaries, permissions, secret leakage, token handling, HMAC, sandbox escape, vulnerabilities, supply-chain hardening, and access control.
- `config`: Configuration schemas, persisted config shape, config loading/validation/repair, defaults, setup/onboarding, environment variables, operator-facing config options, allow/deny configuration, policy settings, overrides, and migration.
- `packaging_deployment`: Build, packaging, installers, Docker images, release artifacts, deployment, service managers, SEA, launchd, systemd, pnpm, and runtime distribution.
- `docs`: Documentation, guides, README changes, spelling, taxonomy, and explanatory content — when the documentation itself is the subject.
- `tests_ci`: Tests, CI, fixtures, coverage, mocks, and platform-specific test fixes — when test infrastructure itself is the subject.
- `telemetry_usage`: Usage accounting, token counts, cost metadata, metrics, traces, diagnostics, status reporting, and observability.
- `api_surface`: External API, CLI, HTTP, and SDK contracts: REST endpoints, webhooks, SSE, OpenResponses, chat completions, documented command contracts, and request/response shapes.
- `queueing`: Queues, lanes, task state, follow-up queues, scheduling, run ordering, work dispatch, locks gating dispatch, stuck jobs, and backpressure.
- `notifications`: Notification policy, completion delivery, delivery gates, notify settings, outbound messages, announcements, and sent-message handling.
- `skills_plugins`: Skills/plugins as product surfaces: SKILL.md, managed skills, plugin manifests/loading/registration, plugin SDK/runtime APIs, MCP Apps, plugin hooks, SecretRefs, skill sync/prelude/wrappers, and doctor/check behavior for plugin or skill surfaces (the bundled Policy plugin is a plugin surface).
- `auth_identity`: Authentication, identity, OAuth, credential propagation, identity overlay, device identity, auth profile selection, account binding, token-only auth, and credential scope.
- `reliability`: Reliability behavior: timeouts, crashes, leaks, stuck state, retries, data loss, lifecycle cleanup, recovery, overload, races, and operational failure modes.
- `tool_calling`: Model tool-calling behavior: tool-call protocol, tool-call deltas, function/tool schemas, tool result transcript handling, tool result routing, and tool-call rendering.
```

Static reflection/evaluator guidance follows. The task model does not see this
file unless GEPA distills a small piece of it into the mutable policy.

```md
# OpenClaw reflection ASI

Use this as GEPA/reflection side information. Do not insert it verbatim into the
task AgentCard.

## Optimization target

Optimize exact topic membership for maintainer-interest routing. The task model
already sees the full fixed taxonomy and a fixed boundary overlay. The mutable
candidate is an OVERLAY on top of those fixed inputs.

Hard constraints on the candidate policy:

- Do NOT restate topic definitions, the allowed-topic enum, or cue-word lists.
  The fixed prompt already contains them; restating them wastes budget, invites
  keyword matching, and goes stale.
- Add only compact decision rules that change behavior beyond the fixed inputs:
  centrality tests, co-label cardinality rules, targeted boundary tie-breakers,
  suppression rules, and corrections for this model's observed failure patterns.
- Keep the section structure of the seed policy (Decision Procedure /
  Cardinality Rules / Boundary Overlays / Suppression Rules) and respect the
  stated bullet budgets.
- Prefer editing or replacing an existing rule over appending a new one.
- Respect the fixed cardinality law: inclusion rules are recall-oriented
  (include every qualifying topic, cap 5); do not write rules that trade
  qualifying co-labels away for precision.

Detailed per-row failures (false positives, false negatives, and the rows they
occurred on) arrive dynamically in the evaluation side information; write rules
that generalize those failures rather than memorizing rows.
```

## Current Component

The component being optimized:

```
# Decision Procedure

Read the title and main problem/feature statement first; use body, comments,
labels, files, and diff only to confirm central ownership. Choose every allowed
topic whose maintainer must review the intended behavior or contract.

Prefer the product surface being changed over symptoms, file locations,
implementation helpers, examples, or failure words. A co-label qualifies only
when that surface's contract, state, lifecycle, policy, delivery path, or user
behavior is independently changed.

# Cardinality Rules

Use 1-3 topics by default; use 4-5 only for genuinely cross-cutting changes;
never more than 5. Include all clearly qualifying central topics, but remove
weak extras before final output.

Final pruning test: drop any label supported only by a generic bug/fix word,
changed path, test/build knob, example platform, config key name, session/context
mention, message/tool wording, or consequence of another surface.

# Boundary Overlays

- Add `reliability` only for operational failure-handling changes: retries,
  timeouts, crashes, leaks, caps/TTL, cleanup, stuck/terminal state, data loss,
  races, overload, or recovery. Do not add it for ordinary bugs, wrong or stale
  values, display/rendering fixes, missing payload text, provider/API
  compatibility, CI-only failures, or failures that merely motivate another
  surface.
- Add `telemetry_usage` when token/usage/cost counts, metrics, traces,
  diagnostics, status, freshness, or reporting are central, including through
  UI, gateway, API, or sessions. Prefer it over `reliability` for stale or
  incorrect counters/status.
- Add `notifications` for outbound delivery, completion/ack behavior,
  announcements, delivery gates, sent-message handling, or reply payloads.
  Chat delivery changes commonly need both `chat_integrations` and
  `notifications`.
- Add `chat_integrations` only for a named chat platform, channel adapter,
  message ingestion, or chat delivery surface. Do not add it for generic
  assistant messages, UI copy/rendering, or non-chat message actions.
- Add `coding_agents` for external or OpenClaw-managed coding-agent
  integrations/flows, including subagent-style integrations with Codex, Claude
  Code, Gemini CLI, Pi, or similar. Do not replace it with `gateway`,
  `sessions`, or `agent_runtime` unless those surfaces independently change.
- For ACP/ACPX work, include `acp` for ACP protocol, node, session, binding,
  parent/child, follow-up, output, or delivery semantics; include `acpx` when
  ACPX transport/proxy/worker/binding/managed backend is central. Wrong or empty
  ACP outputs are `acp`/`acpx`, not `reliability`, unless recovery behavior is
  added.
- Use `sessions` only for session lifecycle, identity, persistence, binding,
  transcript, resume/reset, parent/child state, stores, or cleanup. Do not add
  it for ordinary context, terminal artifacts, notification paths, or files that
  merely mention sessions.
- Use `gateway` only for gateway routing, state, startup, protocol,
  gateway-owned execution, routes, restart, or service health. Suppress it when
  the gateway is merely the host/path for chat config, subagents, notifications,
  provider proxying, or API handlers owned by another surface.
- Use `tool_calling` only for model tool-call protocol, deltas, schemas, tool
  result transcript/routing, or parameter coercion for tool invocation. Do not
  add it for command output, chat replies, TTS, prompt hints, thinking/content
  blocks, screenshots, browser vision, or config-like options.
- Use `approvals` for permission prompts, approval decisions/modes, pending
  approval state, or approval TTL/caps/cleanup. Pending approval leaks are
  `approvals` plus `reliability`, not `memory`, unless the memory system itself
  changes.
- Use `memory` only for memory indexing/search, embeddings/vector stores,
  provider state, archival/recovery, or active memory behavior; not for generic
  remembered state, context, transcripts, or pending queues.
- Use `config` only for operator-facing settings, persisted schema/defaults,
  loading, validation, repair, policy/allow-deny options, environment options,
  or migration. Do not add it for build/test knobs, internal constants, or
  config keys used only to implement another surface.
- Use `tests_ci` when tests, CI, fixtures, mocks, smoke tests, or platform test
  infrastructure are the subject. Pair with `packaging_deployment` for
  build/install/image smoke or speed work; do not add `reliability` or `config`
  unless runtime behavior or operator config also changes.
- For provider/API rendering, streaming, TTS, vision, embeddings, usage chunks,
  catalogs, auth/routing, or compatibility, prefer `inference_api`; add
  `self_hosted_inference` only when engine setup, lifecycle, compatibility,
  crashes/timeouts, or local/self-hosted backend behavior is central.
- Add `codex` only when Codex runtime, auth, ACP, plugin, or command
  compatibility is central; suppress it for cosmetic app/UI changes. Add
  `auth_identity` for auth bridges, account binding, credential propagation,
  profile/scope selection, or token-only auth. Add `security` for credential
  boundaries, isolated homes, token scope, private access, permissions, secret
  exposure, sandbox escape, or access control.
- Add `hooks` when hook emission, registration, ordering, payload, filtering,
  execution, or hook security is central. Add `api_surface` only for external
  API/CLI/HTTP/SDK contracts, request/response shapes, webhooks, SSE, or
  documented command contracts. Add `skills_plugins` only for skill/plugin
  surfaces, manifests, loading, SDK/runtime APIs, SecretRefs, MCP Apps, or
  plugin/skill doctor/check behavior.

# Suppression Rules

- Suppress `reliability` for generic bugs, UI/API corrections, stale metrics,
  provider formatting/rendering mismatches, missing notification payloads,
  test-speed work, or compatibility fixes without recovery mechanics.
- Suppress `tool_calling` unless the model tool-call contract itself changes.
- Suppress `api_surface` for slash commands, chat acknowledgements, UI actions,
  or provider internals unless an external contract changes.
- Suppress `agent_runtime` for ACP orchestration or coding-agent integration
  unless core startup, loop, backend, adapter, or model-call orchestration is
  the deliverable.
- Suppress labels inferred only from paths, tests, examples, package names,
  platform names, or incidental mentions when the title/body identify another
  owner.
```

## Evaluation Results

Performance data from evaluating the current component across test cases:

```
# Example 1
## Scores (Higher is Better)
### gepa_score
0.663085

### composite_score
0.675625

### topic_micro_f1
0.7875

### row_exact_accuracy
0.375

### avg_row_jaccard
0.6895833333333333

### row_symdiff_score
0.48484848484848486

### policy_length_compliance
0.8746

### policy_hygiene_compliance
1.0

## score_details
### false_positives
20

### false_negatives
14

### row_exact_accuracy
0.375

### avg_row_jaccard
0.6895833333333333

### avg_row_symdiff
1.0625

### avg_expected_topics
2.40625

### avg_predicted_topics
2.59375

### asi_score
1.0

### topic_micro_precision
0.7590361445783133

### topic_micro_recall
0.8181818181818182

### exact_match
0.375

### row_symdiff_score
0.48484848484848486

### composite_score
0.675625

### gepa_score
0.663085

### score_mode
row-aware

### valid_json
1.0

### cardinality_closeness
0.922077922077922

### avg_topic_count_delta
0.1875

### policy_chars
6508

### policy_char_budget
4000

### policy_length_over_budget
2508

### policy_length_penalty
0.012540000000000003

### policy_length_compliance
0.8746

### hygiene_penalty
0.0

### hygiene_findings_count
0

## evaluated
32

## failures
### Item 1
#### id
openclaw-openclaw-43416

#### title
feat(ui): add copy button for assistant messages

#### expected
##### Item 1
ui_tui

#### actual
##### Item 1
chat_integrations

##### Item 2
ui_tui

#### false_positives
##### Item 1
chat_integrations

#### false_negatives

#### invalid_topics

#### keywords

#### row_score
0.6666666666666666

### Item 2
#### id
openclaw-openclaw-47083

#### title
fix: respect totalTokensFresh flag to avoid showing stale token counts

#### expected
##### Item 1
telemetry_usage

##### Item 2
ui_tui

#### actual
##### Item 1
reliability

##### Item 2
ui_tui

#### false_positives
##### Item 1
reliability

#### false_negatives
##### Item 1
telemetry_usage

#### invalid_topics

#### keywords

#### row_score
0.5

### Item 3
#### id
openclaw-openclaw-48877

#### title
feat(telegram): add multi-level menu support to customCommands

#### expected
##### Item 1
chat_integrations

##### Item 2
config

#### actual
##### Item 1
chat_integrations

##### Item 2
config

##### Item 3
ui_tui

#### false_positives
##### Item 1
ui_tui

#### false_negatives

#### invalid_topics

#### keywords

#### row_score
0.8

### Item 4
#### id
openclaw-openclaw-53997

#### title
acpx: add terminal-truth artifacts and strict terminal states

#### expected
##### Item 1
acpx

##### Item 2
reliability

#### actual
##### Item 1
acpx

##### Item 2
reliability

##### Item 3
sessions

#### false_positives
##### Item 1
sessions

#### false_negatives

#### invalid_topics

#### keywords

#### row_score
0.8

### Item 5
#### id
openclaw-openclaw-71157

#### title
[Feature]: Support WhatsApp disappearing-message expiration for outbound replies

#### expected
##### Item 1
chat_integrations

##### Item 2
config

##### Item 3
notifications

#### actual
##### Item 1
chat_integrations

##### Item 2
config

##### Item 3
reliability

#### false_positives
##### Item 1
reliability

#### false_negatives
##### Item 1
notifications

#### invalid_topics

#### keywords

#### row_score
0.6666666666666666

### Item 6
#### id
openclaw-openclaw-71646

#### title
mcp/channel-bridge: pendingClaudePermissions / pendingApprovals leak — no TTL, no close-clear, no cap

#### expected
##### Item 1
approvals

##### Item 2
mcp_tooling

##### Item 3
reliability

#### actual
##### Item 1
mcp_tooling

##### Item 2
memory

##### Item 3
reliability

#### false_positives
##### Item 1
memory

#### false_negatives
##### Item 1
approvals

#### invalid_topics

#### keywords

#### row_score
0.6666666666666666

### Item 7
#### id
openclaw-openclaw-71976

#### title
Memory Dreaming: Light sleep sort prioritizes recency over recallCount, hiding real recall data

#### expected
##### Item 1
memory

#### actual
##### Item 1
memory

##### Item 2
reliability

#### false_positives
##### Item 1
reliability

#### false_negatives

#### invalid_topics

#### keywords

#### row_score
0.6666666666666666

### Item 8
#### id
openclaw-openclaw-77694

#### title
[Bug]: acpx flow run ACP node outputs return empty strings instead of agent replies

#### expected
##### Item 1
acp

##### Item 2
acpx

#### actual
##### Item 1
acpx

##### Item 2
reliability

#### false_positives
##### Item 1
reliability

#### false_negatives
##### Item 1
acp

#### invalid_topics

#### keywords

#### row_score
0.5

### Item 9
#### id
openclaw-openclaw-82145

#### title
cron: allow retries for local model preflight

#### expected
##### Item 1
config

##### Item 2
cron_automation

##### Item 3
reliability

##### Item 4
self_hosted_inference

#### actual
##### Item 1
config

##### Item 2
cron_automation

##### Item 3
reliability

#### false_positives

#### false_negatives
##### Item 1
self_hosted_inference

#### invalid_topics

#### keywords

#### row_score
0.8571428571428571

### Item 10
#### id
openclaw-openclaw-82642

#### title
Fix iMessage slash command acknowledgements

#### expected
##### Item 1
chat_integrations

##### Item 2
notifications

#### actual
##### Item 1
chat_integrations

##### Item 2
reliability

#### false_positives
##### Item 1
reliability

#### false_negatives
##### Item 1
notifications

#### invalid_topics

#### keywords

#### row_score
0.5

### Item 11
#### id
openclaw-openclaw-84385

#### title
[codex] Fix macOS app copyright year

#### expected
##### Item 1
ui_tui

#### actual
##### Item 1
codex

##### Item 2
ui_tui

#### false_positives
##### Item 1
codex

#### false_negatives

#### invalid_topics

#### keywords

#### row_score
0.6666666666666666

### Item 12
#### id
openclaw-openclaw-84732

#### title
Slack channel sends fail: `reconcileUnknownSend` required but no channel adapter implements it

#### expected
##### Item 1
chat_integrations

##### Item 2
notifications

##### Item 3
reliability

#### actual
##### Item 1
chat_integrations

##### Item 2
reliability

##### Item 3
tool_calling

#### false_positives
##### Item 1
tool_calling

#### false_negatives
##### Item 1
notifications

#### invalid_topics

#### keywords

#### row_score
0.6666666666666666

## worst_failures
### Item 1
#### id
openclaw-openclaw-42122

#### title
Speed up install smoke Docker builds

#### expected
##### Item 1
packaging_deployment

##### Item 2
tests_ci

#### actual
##### Item 1
config

##### Item 2
packaging_deployment

##### Item 3
reliability

#### false_positives
##### Item 1
config

##### Item 2
reliability

#### false_negatives
##### Item 1
tests_ci

#### invalid_topics

#### keywords

#### row_score
0.4

### Item 2
#### id
openclaw-openclaw-47083

#### title
fix: respect totalTokensFresh flag to avoid showing stale token counts

#### expected
##### Item 1
telemetry_usage

##### Item 2
ui_tui

#### actual
##### Item 1
reliability

##### Item 2
ui_tui

#### false_positives
##### Item 1
reliability

#### false_negatives
##### Item 1
telemetry_usage

#### invalid_topics

#### keywords

#### row_score
0.5

### Item 3
#### id
openclaw-openclaw-77694

#### title
[Bug]: acpx flow run ACP node outputs return empty strings instead of agent replies

#### expected
##### Item 1
acp

##### Item 2
acpx

#### actual
##### Item 1
acpx

##### Item 2
reliability

#### false_positives
##### Item 1
reliability

#### false_negatives
##### Item 1
acp

#### invalid_topics

#### keywords

#### row_score
0.5

### Item 4
#### id
openclaw-openclaw-82642

#### title
Fix iMessage slash command acknowledgements

#### expected
##### Item 1
chat_integrations

##### Item 2
notifications

#### actual
##### Item 1
chat_integrations

##### Item 2
reliability

#### false_positives
##### Item 1
reliability

#### false_negatives
##### Item 1
notifications

#### invalid_topics

#### keywords

#### row_score
0.5

### Item 5
#### id
openclaw-openclaw-77827

#### title
fix: LM Studio thinking blocks invisible with Responses API

#### expected
##### Item 1
inference_api

#### actual
##### Item 1
inference_api

##### Item 2
reliability

##### Item 3
tool_calling

#### false_positives
##### Item 1
reliability

##### Item 2
tool_calling

#### false_negatives

#### invalid_topics

#### keywords

#### row_score
0.5

### Item 6
#### id
openclaw-openclaw-45200

#### title
fix(subagents): notify user on announce give-up instead of silently dropping result

#### expected
##### Item 1
coding_agents

##### Item 2
notifications

##### Item 3
reliability

#### actual
##### Item 1
gateway

##### Item 2
notifications

##### Item 3
reliability

##### Item 4
sessions

#### false_positives
##### Item 1
gateway

##### Item 2
sessions

#### false_negatives
##### Item 1
coding_agents

#### invalid_topics

#### keywords

#### row_score
0.5714285714285714

### Item 7
#### id
openclaw-openclaw-73910

#### title
BUG: OpenClaw-managed Codex ACP uses isolated CODEX_HOME without auth bridge and sends unsupported timeout config

#### expected
##### Item 1
acp

##### Item 2
acpx

##### Item 3
auth_identity

##### Item 4
codex

##### Item 5
security

#### actual
##### Item 1
acp

##### Item 2
auth_identity

##### Item 3
codex

##### Item 4
reliability

#### false_positives
##### Item 1
reliability

#### false_negatives
##### Item 1
acpx

##### Item 2
security

#### invalid_topics

#### keywords

#### row_score
0.6666666666666666

### Item 8
#### id
openclaw-openclaw-71157

#### title
[Feature]: Support WhatsApp disappearing-message expiration for outbound replies

#### expected
##### Item 1
chat_integrations

##### Item 2
config

##### Item 3
notifications

#### actual
##### Item 1
chat_integrations

##### Item 2
config

##### Item 3
reliability

#### false_positives
##### Item 1
reliability

#### false_negatives
##### Item 1
notifications

#### invalid_topics

#### keywords

#### row_score
0.6666666666666666

## topic_error_patterns
### Item 1
#### topic
reliability

#### problem
over_predicted

#### expected
10

#### actual
18

#### true_positives
10

#### false_positives
8

#### false_negatives
0

#### precision
0.556

#### recall
1.0

#### f1
0.714

#### action
`reliability` over_predicted: expected in 10 rows, predicted in 18, TP=10, FP=8, FN=0, precision=0.556, recall=1.000. Precision is the bottleneck. a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface.

#### examples
##### Item 1
###### expected
###### Item 1
telemetry_usage

###### Item 2
ui_tui

###### actual
###### Item 1
reliability

###### Item 2
ui_tui

###### keywords

###### error_type
false_positive

##### Item 2
###### expected
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
notifications

###### actual
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
reliability

###### keywords

###### error_type
false_positive

##### Item 3
###### expected
###### Item 1
memory

###### actual
###### Item 1
memory

###### Item 2
reliability

###### keywords

###### error_type
false_positive

#### true_positive_examples
##### Item 1
###### expected
###### Item 1
acpx

###### Item 2
reliability

###### actual
###### Item 1
acpx

###### Item 2
reliability

###### Item 3
sessions

###### keywords

###### row_score
0.8

##### Item 2
###### expected
###### Item 1
acp

###### Item 2
reliability

###### Item 3
sessions

###### actual
###### Item 1
acp

###### Item 2
reliability

###### Item 3
sessions

###### keywords

###### row_score
1.0

##### Item 3
###### expected
###### Item 1
approvals

###### Item 2
mcp_tooling

###### Item 3
reliability

###### actual
###### Item 1
mcp_tooling

###### Item 2
memory

###### Item 3
reliability

###### keywords

###### row_score
0.667

#### false_positive_examples
##### Item 1
###### expected
###### Item 1
telemetry_usage

###### Item 2
ui_tui

###### actual
###### Item 1
reliability

###### Item 2
ui_tui

###### keywords

###### row_score
0.5

##### Item 2
###### expected
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
notifications

###### actual
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
reliability

###### keywords

###### row_score
0.667

##### Item 3
###### expected
###### Item 1
memory

###### actual
###### Item 1
memory

###### Item 2
reliability

###### keywords

###### row_score
0.667

#### false_negative_examples

### Item 2
#### topic
notifications

#### problem
under_predicted

#### expected
5

#### actual
2

#### true_positives
2

#### false_positives
0

#### false_negatives
3

#### precision
1.0

#### recall
0.4

#### f1
0.571

#### action
`notifications` under_predicted: expected in 5 rows, predicted in 2, TP=2, FP=0, FN=3, precision=1.000, recall=0.400. Recall is the bottleneck. MUST include when central: generic outbound notifications, completion delivery, message delivery gates, announcements, or notify behavior is central. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label.

#### examples
##### Item 1
###### expected
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
notifications

###### actual
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
reliability

###### keywords

###### error_type
false_negative

##### Item 2
###### expected
###### Item 1
chat_integrations

###### Item 2
notifications

###### actual
###### Item 1
chat_integrations

###### Item 2
reliability

###### keywords

###### error_type
false_negative

##### Item 3
###### expected
###### Item 1
chat_integrations

###### Item 2
notifications

###### Item 3
reliability

###### actual
###### Item 1
chat_integrations

###### Item 2
reliability

###### Item 3
tool_calling

###### keywords

###### error_type
false_negative

#### true_positive_examples
##### Item 1
###### expected
###### Item 1
chat_integrations

###### Item 2
hooks

###### Item 3
notifications

###### actual
###### Item 1
chat_integrations

###### Item 2
hooks

###### Item 3
notifications

###### keywords

###### row_score
1.0

##### Item 2
###### expected
###### Item 1
coding_agents

###### Item 2
notifications

###### Item 3
reliability

###### actual
###### Item 1
gateway

###### Item 2
notifications

###### Item 3
reliability

###### Item 4
sessions

###### keywords

###### row_score
0.571

#### false_positive_examples

#### false_negative_examples
##### Item 1
###### expected
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
notifications

###### actual
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
reliability

###### keywords

###### row_score
0.667

##### Item 2
###### expected
###### Item 1
chat_integrations

###### Item 2
notifications

###### actual
###### Item 1
chat_integrations

###### Item 2
reliability

###### keywords

###### row_score
0.5

##### Item 3
###### expected
###### Item 1
chat_integrations

###### Item 2
notifications

###### Item 3
reliability

###### actual
###### Item 1
chat_integrations

###### Item 2
reliability

###### Item 3
tool_calling

###### keywords

###### row_score
0.667

### Item 3
#### topic
tool_calling

#### problem
over_predicted

#### expected
0

#### actual
3

#### true_positives
0

#### false_positives
3

#### false_negatives
0

#### precision
0.0

#### recall
0.0

#### f1
0.0

#### action
`tool_calling` over_predicted: expected in 0 rows, predicted in 3, TP=0, FP=3, FN=0, precision=0.000, recall=0.000. Precision is the bottleneck. generic command output, TTS, browser screenshot/vision, or config-like options. Co-label: parameter coercion/normalization for tool invocation is tool_calling, even inside an MCP bundle or adapter.

#### examples
##### Item 1
###### expected
###### Item 1
chat_integrations

###### Item 2
notifications

###### Item 3
reliability

###### actual
###### Item 1
chat_integrations

###### Item 2
reliability

###### Item 3
tool_calling

###### keywords

###### error_type
false_positive

##### Item 2
###### expected
###### Item 1
inference_api

###### actual
###### Item 1
inference_api

###### Item 2
tool_calling

###### keywords

###### error_type
false_positive

##### Item 3
###### expected
###### Item 1
inference_api

###### actual
###### Item 1
inference_api

###### Item 2
reliability

###### Item 3
tool_calling

###### keywords

###### error_type
false_positive

#### true_positive_examples

#### false_positive_examples
##### Item 1
###### expected
###### Item 1
chat_integrations

###### Item 2
notifications

###### Item 3
reliability

###### actual
###### Item 1
chat_integrations

###### Item 2
reliability

###### Item 3
tool_calling

###### keywords

###### row_score
0.667

##### Item 2
###### expected
###### Item 1
inference_api

###### actual
###### Item 1
inference_api

###### Item 2
tool_calling

###### keywords

###### row_score
0.667

##### Item 3
###### expected
###### Item 1
inference_api

###### actual
###### Item 1
inference_api

###### Item 2
reliability

###### Item 3
tool_calling

###### keywords

###### row_score
0.5

#### false_negative_examples

### Item 4
#### topic
coding_agents

#### problem
under_predicted

#### expected
3

#### actual
0

#### true_positives
0

#### false_positives
0

#### false_negatives
3

#### precision
0.0

#### recall
0.0

#### f1
0.0

#### action
`coding_agents` under_predicted: expected in 3 rows, predicted in 0, TP=0, FP=0, FN=3, precision=0.000, recall=0.000. Recall is the bottleneck. MUST include when central: integrations with external coding agents in general, or with a specific coding agent such as Codex, Claude Code, Gemini CLI, or Pi. Boundary: ACP is an integration protocol and is distinct from coding-agent integrations; route ACP protocol/session/delivery work to `acp`/`acpx`. OpenClaw's internal agent runtime is a core product surface; route startup, loop, backend, model-call orchestration, and adapter machinery to `agent_runtime`.

#### examples
##### Item 1
###### expected
###### Item 1
coding_agents

###### Item 2
notifications

###### Item 3
reliability

###### actual
###### Item 1
gateway

###### Item 2
notifications

###### Item 3
reliability

###### Item 4
sessions

###### keywords

###### error_type
false_negative

##### Item 2
###### expected
###### Item 1
coding_agents

###### Item 2
cron_automation

###### Item 3
reliability

###### Item 4
sessions

###### actual
###### Item 1
cron_automation

###### Item 2
reliability

###### Item 3
sessions

###### keywords

###### error_type
false_negative

##### Item 3
###### expected
###### Item 1
acp

###### Item 2
coding_agents

###### Item 3
sessions

###### actual
###### Item 1
acp

###### Item 2
agent_runtime

###### Item 3
sessions

###### keywords

###### error_type
false_negative

#### true_positive_examples

#### false_positive_examples

#### false_negative_examples
##### Item 1
###### expected
###### Item 1
coding_agents

###### Item 2
notifications

###### Item 3
reliability

###### actual
###### Item 1
gateway

###### Item 2
notifications

###### Item 3
reliability

###### Item 4
sessions

###### keywords

###### row_score
0.571

##### Item 2
###### expected
###### Item 1
coding_agents

###### Item 2
cron_automation

###### Item 3
reliability

###### Item 4
sessions

###### actual
###### Item 1
cron_automation

###### Item 2
reliability

###### Item 3
sessions

###### keywords

###### row_score
0.857

##### Item 3
###### expected
###### Item 1
acp

###### Item 2
coding_agents

###### Item 3
sessions

###### actual
###### Item 1
acp

###### Item 2
agent_runtime

###### Item 3
sessions

###### keywords

###### row_score
0.667

### Item 5
#### topic
sessions

#### problem
mixed

#### expected
6

#### actual
8

#### true_positives
6

#### false_positives
2

#### false_negatives
0

#### precision
0.75

#### recall
1.0

#### f1
0.857

#### action
`sessions` mixed: expected in 6 rows, predicted in 8, TP=6, FP=2, FN=0, precision=0.750, recall=1.000. Both precision and recall need boundary work. Mixed `sessions` errors. every mention of session context or session files. MUST include when central: session lifecycle, state, storage, identity, binding, or cleanup is central.

#### examples
##### Item 1
###### expected
###### Item 1
acpx

###### Item 2
reliability

###### actual
###### Item 1
acpx

###### Item 2
reliability

###### Item 3
sessions

###### keywords

###### error_type
false_positive

##### Item 2
###### expected
###### Item 1
coding_agents

###### Item 2
notifications

###### Item 3
reliability

###### actual
###### Item 1
gateway

###### Item 2
notifications

###### Item 3
reliability

###### Item 4
sessions

###### keywords

###### error_type
false_positive

#### true_positive_examples
##### Item 1
###### expected
###### Item 1
acp

###### Item 2
reliability

###### Item 3
sessions

###### actual
###### Item 1
acp

###### Item 2
reliability

###### Item 3
sessions

###### keywords

###### row_score
1.0

##### Item 2
###### expected
###### Item 1
sessions

###### Item 2
ui_tui

###### actual
###### Item 1
sessions

###### Item 2
ui_tui

###### keywords

###### row_score
1.0

##### Item 3
###### expected
###### Item 1
sessions

###### Item 2
telemetry_usage

###### Item 3
ui_tui

###### actual
###### Item 1
sessions

###### Item 2
telemetry_usage

###### Item 3
ui_tui

###### keywords

###### row_score
1.0

#### false_positive_examples
##### Item 1
###### expected
###### Item 1
acpx

###### Item 2
reliability

###### actual
###### Item 1
acpx

###### Item 2
reliability

###### Item 3
sessions

###### keywords

###### row_score
0.8

##### Item 2
###### expected
###### Item 1
coding_agents

###### Item 2
notifications

###### Item 3
reliability

###### actual
###### Item 1
gateway

###### Item 2
notifications

###### Item 3
reliability

###### Item 4
sessions

###### keywords

###### row_score
0.571

#### false_negative_examples

### Item 6
#### topic
ui_tui

#### problem
mixed

#### expected
7

#### actual
8

#### true_positives
7

#### false_positives
1

#### false_negatives
0

#### precision
0.875

#### recall
1.0

#### f1
0.933

#### action
`ui_tui` mixed: expected in 7 rows, predicted in 8, TP=7, FP=1, FN=0, precision=0.875, recall=1.000. Both precision and recall need boundary work. Mixed `ui_tui` errors. command internals, telemetry fields, or API behavior not shown to users. MUST include when central: UI/TUI display, status, footer, mobile UI, or visual interaction is central.

#### examples
##### Item 1
###### expected
###### Item 1
chat_integrations

###### Item 2
config

###### actual
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
ui_tui

###### keywords

###### error_type
false_positive

#### true_positive_examples
##### Item 1
###### expected
###### Item 1
cron_automation

###### Item 2
ui_tui

###### actual
###### Item 1
cron_automation

###### Item 2
ui_tui

###### keywords

###### row_score
1.0

##### Item 2
###### expected
###### Item 1
ui_tui

###### actual
###### Item 1
chat_integrations

###### Item 2
ui_tui

###### keywords

###### row_score
0.667

##### Item 3
###### expected
###### Item 1
telemetry_usage

###### Item 2
ui_tui

###### actual
###### Item 1
reliability

###### Item 2
ui_tui

###### keywords

###### row_score
0.5

#### false_positive_examples
##### Item 1
###### expected
###### Item 1
chat_integrations

###### Item 2
config

###### actual
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
ui_tui

###### keywords

###### row_score
0.8

#### false_negative_examples

### Item 7
#### topic
chat_integrations

#### problem
mixed

#### expected
5

#### actual
6

#### true_positives
5

#### false_positives
1

#### false_negatives
0

#### precision
0.833

#### recall
1.0

#### f1
0.909

#### action
`chat_integrations` mixed: expected in 5 rows, predicted in 6, TP=5, FP=1, FN=0, precision=0.833, recall=1.000. Both precision and recall need boundary work. Mixed `chat_integrations` errors. generic message delivery/recovery without a named chat surface. MUST include when central: a named chat platform, channel adapter, message ingestion, or chat delivery surface is central.

#### examples
##### Item 1
###### expected
###### Item 1
ui_tui

###### actual
###### Item 1
chat_integrations

###### Item 2
ui_tui

###### keywords

###### error_type
false_positive

#### true_positive_examples
##### Item 1
###### expected
###### Item 1
chat_integrations

###### Item 2
config

###### actual
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
ui_tui

###### keywords

###### row_score
0.8

##### Item 2
###### expected
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
notifications

###### actual
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
reliability

###### keywords

###### row_score
0.667

##### Item 3
###### expected
###### Item 1
chat_integrations

###### Item 2
hooks

###### Item 3
notifications

###### actual
###### Item 1
chat_integrations

###### Item 2
hooks

###### Item 3
notifications

###### keywords

###### row_score
1.0

#### false_positive_examples
##### Item 1
###### expected
###### Item 1
ui_tui

###### actual
###### Item 1
chat_integrations

###### Item 2
ui_tui

###### keywords

###### row_score
0.667

#### false_negative_examples

### Item 8
#### topic
config

#### problem
mixed

#### expected
5

#### actual
6

#### true_positives
5

#### false_positives
1

#### false_negatives
0

#### precision
0.833

#### recall
1.0

#### f1
0.909

#### action
`config` mixed: expected in 5 rows, predicted in 6, TP=5, FP=1, FN=0, precision=0.833, recall=1.000. Both precision and recall need boundary work. Mixed `config` errors. a config key that is merely the internal mechanism, example, or implementation detail of another surface's change. Boundary: operator-facing config options qualify on their own. MUST include when central: configuration schemas, persisted config shape, config loading, config validation, config repair, environment/config defaults, operator-facing config options, allow/deny configuration, or policy settings. Boundary: operator-facing config options qualify on their own.

#### examples
##### Item 1
###### expected
###### Item 1
packaging_deployment

###### Item 2
tests_ci

###### actual
###### Item 1
config

###### Item 2
packaging_deployment

###### Item 3
reliability

###### keywords

###### error_type
false_positive

#### true_positive_examples
##### Item 1
###### expected
###### Item 1
chat_integrations

###### Item 2
config

###### actual
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
ui_tui

###### keywords

###### row_score
0.8

##### Item 2
###### expected
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
notifications

###### actual
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
reliability

###### keywords

###### row_score
0.667

##### Item 3
###### expected
###### Item 1
config

###### Item 2
cron_automation

###### Item 3
reliability

###### Item 4
self_hosted_inference

###### actual
###### Item 1
config

###### Item 2
cron_automation

###### Item 3
reliability

###### keywords

###### row_score
0.857

#### false_positive_examples
##### Item 1
###### expected
###### Item 1
packaging_deployment

###### Item 2
tests_ci

###### actual
###### Item 1
config

###### Item 2
packaging_deployment

###### Item 3
reliability

###### keywords

###### row_score
0.4

#### false_negative_examples

## confusions
### Item 1
#### expected
notifications

#### predicted
reliability

#### count
2

#### action
Clarify `notifications` vs `reliability`. For missed `notifications`: MUST include when central: generic outbound notifications, completion delivery, message delivery gates, announcements, or notify behavior is central. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label. For extra `reliability`: a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface.

#### examples
##### Item 1
###### expected
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
notifications

###### actual
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
reliability

###### keywords

###### row_score
0.667

##### Item 2
###### expected
###### Item 1
chat_integrations

###### Item 2
notifications

###### actual
###### Item 1
chat_integrations

###### Item 2
reliability

###### keywords

###### row_score
0.5

### Item 2
#### expected
telemetry_usage

#### predicted
reliability

#### count
1

#### action
Clarify `telemetry_usage` vs `reliability`. For missed `telemetry_usage`: MUST include when central: token counts, usage counts, costs, metrics, diagnostics, traces, or status reporting are central. For extra `reliability`: a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface.

#### examples
##### Item 1
###### expected
###### Item 1
telemetry_usage

###### Item 2
ui_tui

###### actual
###### Item 1
reliability

###### Item 2
ui_tui

###### keywords

###### row_score
0.5

### Item 3
#### expected
approvals

#### predicted
memory

#### count
1

#### action
Clarify `approvals` vs `memory`. For missed `approvals`: MUST include when central: approval prompts, permission decisions, or approval mode behavior is central. Co-label: bounding/expiring/persisting pending-approval state is approvals surface even when motivated by a memory/reliability fix. For extra `memory`: context window, session state, transcript, or generic remembering.

#### examples
##### Item 1
###### expected
###### Item 1
approvals

###### Item 2
mcp_tooling

###### Item 3
reliability

###### actual
###### Item 1
mcp_tooling

###### Item 2
memory

###### Item 3
reliability

###### keywords

###### row_score
0.667

### Item 4
#### expected
acp

#### predicted
reliability

#### count
1

#### action
Clarify `acp` vs `reliability`. For missed `acp`: MUST include when central: ACP runtime/protocol, ACP session, ACP binding, ACP parent/child behavior, or ACP delivery is central. For extra `reliability`: a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface.

#### examples
##### Item 1
###### expected
###### Item 1
acp

###### Item 2
acpx

###### actual
###### Item 1
acpx

###### Item 2
reliability

###### keywords

###### row_score
0.5

### Item 5
#### expected
notifications

#### predicted
tool_calling

#### count
1

#### action
Clarify `notifications` vs `tool_calling`. For missed `notifications`: MUST include when central: generic outbound notifications, completion delivery, message delivery gates, announcements, or notify behavior is central. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label. For extra `tool_calling`: generic command output, TTS, browser screenshot/vision, or config-like options. Co-label: parameter coercion/normalization for tool invocation is tool_calling, even inside an MCP bundle or adapter.

#### examples
##### Item 1
###### expected
###### Item 1
chat_integrations

###### Item 2
notifications

###### Item 3
reliability

###### actual
###### Item 1
chat_integrations

###### Item 2
reliability

###### Item 3
tool_calling

###### keywords

###### row_score
0.667

### Item 6
#### expected
tests_ci

#### predicted
reliability

#### count
1

#### action
Clarify `tests_ci` vs `reliability`. For missed `tests_ci`: MUST include when central: only when tests, CI, or test infrastructure itself is the subject. For extra `reliability`: a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface.

#### examples
##### Item 1
###### expected
###### Item 1
packaging_deployment

###### Item 2
tests_ci

###### actual
###### Item 1
config

###### Item 2
packaging_deployment

###### Item 3
reliability

###### keywords

###### row_score
0.4

## invalid_topics

## actionable_feedback
### Item 1
Pure-F1 objective: optimize exact topic membership, not recall-biased F-beta. Current precision=0.759, recall=0.818, F1=0.787.

### Item 2
Cardinality diagnosis: over_labeling; avg predicted 2.59 vs expected 2.41. Tighten incidental-evidence gates and remove labels supported only by files, tests, examples, or side effects.

### Item 3
Policy length penalty: policy is 2508 chars over the 4000 char budget; GEPA score was reduced by 0.0125.

### Item 4
Topic cardinality is close: avg predicted topics 2.59 vs expected 2.41. Focus on boundary-specific errors.

### Item 5
`reliability` over_predicted: expected in 10 rows, predicted in 18, TP=10, FP=8, FN=0, precision=0.556, recall=1.000. Precision is the bottleneck. a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface.

### Item 6
`notifications` under_predicted: expected in 5 rows, predicted in 2, TP=2, FP=0, FN=3, precision=1.000, recall=0.400. Recall is the bottleneck. MUST include when central: generic outbound notifications, completion delivery, message delivery gates, announcements, or notify behavior is central. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label.

### Item 7
`tool_calling` over_predicted: expected in 0 rows, predicted in 3, TP=0, FP=3, FN=0, precision=0.000, recall=0.000. Precision is the bottleneck. generic command output, TTS, browser screenshot/vision, or config-like options. Co-label: parameter coercion/normalization for tool invocation is tool_calling, even inside an MCP bundle or adapter.

### Item 8
`coding_agents` under_predicted: expected in 3 rows, predicted in 0, TP=0, FP=0, FN=3, precision=0.000, recall=0.000. Recall is the bottleneck. MUST include when central: integrations with external coding agents in general, or with a specific coding agent such as Codex, Claude Code, Gemini CLI, or Pi. Boundary: ACP is an integration protocol and is distinct from coding-agent integrations; route ACP protocol/session/delivery work to `acp`/`acpx`. OpenClaw's internal agent runtime is a core product surface; route startup, loop, backend, model-call orchestration, and adapter machinery to `agent_runtime`.

### Item 9
`sessions` mixed: expected in 6 rows, predicted in 8, TP=6, FP=2, FN=0, precision=0.750, recall=1.000. Both precision and recall need boundary work. Mixed `sessions` errors. every mention of session context or session files. MUST include when central: session lifecycle, state, storage, identity, binding, or cleanup is central.

### Item 10
`ui_tui` mixed: expected in 7 rows, predicted in 8, TP=7, FP=1, FN=0, precision=0.875, recall=1.000. Both precision and recall need boundary work. Mixed `ui_tui` errors. command internals, telemetry fields, or API behavior not shown to users. MUST include when central: UI/TUI display, status, footer, mobile UI, or visual interaction is central.

## vanilla_f1_asi
### global_diagnosis
#### precision
0.7590361445783133

#### recall
0.8181818181818182

#### f1
0.7875

#### gepa_score
0.663085

#### score_mode
row-aware

#### exact_match
0.375

#### row_exact_accuracy
0.375

#### avg_row_jaccard
0.6895833333333333

#### avg_row_symdiff
1.0625

#### row_symdiff_score
0.48484848484848486

#### composite_score
0.675625

#### valid_json
1.0

#### cardinality_closeness
0.922077922077922

#### avg_expected_topics
2.40625

#### avg_predicted_topics
2.59375

#### false_positives
20

#### false_negatives
14

#### policy_chars
6508

#### policy_char_budget
4000

#### policy_length_over_budget
2508

#### policy_length_penalty
0.012540000000000003

#### policy_length_compliance
0.8746

#### diagnosis
over_labeling

#### action
Tighten incidental-evidence gates and remove labels supported only by files, tests, examples, or side effects.

### topic_priorities
#### Item 1
##### topic
reliability

##### problem
over_predicted

##### false_positives
8

##### false_negatives
0

##### precision
0.556

##### recall
1.0

##### action
`reliability` over_predicted: expected in 10 rows, predicted in 18, TP=10, FP=8, FN=0, precision=0.556, recall=1.000. Precision is the bottleneck. a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface.

#### Item 2
##### topic
notifications

##### problem
under_predicted

##### false_positives
0

##### false_negatives
3

##### precision
1.0

##### recall
0.4

##### action
`notifications` under_predicted: expected in 5 rows, predicted in 2, TP=2, FP=0, FN=3, precision=1.000, recall=0.400. Recall is the bottleneck. MUST include when central: generic outbound notifications, completion delivery, message delivery gates, announcements, or notify behavior is central. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label.

#### Item 3
##### topic
tool_calling

##### problem
over_predicted

##### false_positives
3

##### false_negatives
0

##### precision
0.0

##### recall
0.0

##### action
`tool_calling` over_predicted: expected in 0 rows, predicted in 3, TP=0, FP=3, FN=0, precision=0.000, recall=0.000. Precision is the bottleneck. generic command output, TTS, browser screenshot/vision, or config-like options. Co-label: parameter coercion/normalization for tool invocation is tool_calling, even inside an MCP bundle or adapter.

#### Item 4
##### topic
coding_agents

##### problem
under_predicted

##### false_positives
0

##### false_negatives
3

##### precision
0.0

##### recall
0.0

##### action
`coding_agents` under_predicted: expected in 3 rows, predicted in 0, TP=0, FP=0, FN=3, precision=0.000, recall=0.000. Recall is the bottleneck. MUST include when central: integrations with external coding agents in general, or with a specific coding agent such as Codex, Claude Code, Gemini CLI, or Pi. Boundary: ACP is an integration protocol and is distinct from coding-agent integrations; route ACP protocol/session/delivery work to `acp`/`acpx`. OpenClaw's internal agent runtime is a core product surface; route startup, loop, backend, model-call orchestration, and adapter machinery to `agent_runtime`.

#### Item 5
##### topic
sessions

##### problem
mixed

##### false_positives
2

##### false_negatives
0

##### precision
0.75

##### recall
1.0

##### action
`sessions` mixed: expected in 6 rows, predicted in 8, TP=6, FP=2, FN=0, precision=0.750, recall=1.000. Both precision and recall need boundary work. Mixed `sessions` errors. every mention of session context or session files. MUST include when central: session lifecycle, state, storage, identity, binding, or cleanup is central.

#### Item 6
##### topic
ui_tui

##### problem
mixed

##### false_positives
1

##### false_negatives
0

##### precision
0.875

##### recall
1.0

##### action
`ui_tui` mixed: expected in 7 rows, predicted in 8, TP=7, FP=1, FN=0, precision=0.875, recall=1.000. Both precision and recall need boundary work. Mixed `ui_tui` errors. command internals, telemetry fields, or API behavior not shown to users. MUST include when central: UI/TUI display, status, footer, mobile UI, or visual interaction is central.

#### Item 7
##### topic
chat_integrations

##### problem
mixed

##### false_positives
1

##### false_negatives
0

##### precision
0.833

##### recall
1.0

##### action
`chat_integrations` mixed: expected in 5 rows, predicted in 6, TP=5, FP=1, FN=0, precision=0.833, recall=1.000. Both precision and recall need boundary work. Mixed `chat_integrations` errors. generic message delivery/recovery without a named chat surface. MUST include when central: a named chat platform, channel adapter, message ingestion, or chat delivery surface is central.

#### Item 8
##### topic
config

##### problem
mixed

##### false_positives
1

##### false_negatives
0

##### precision
0.833

##### recall
1.0

##### action
`config` mixed: expected in 5 rows, predicted in 6, TP=5, FP=1, FN=0, precision=0.833, recall=1.000. Both precision and recall need boundary work. Mixed `config` errors. a config key that is merely the internal mechanism, example, or implementation detail of another surface's change. Boundary: operator-facing config options qualify on their own. MUST include when central: configuration schemas, persisted config shape, config loading, config validation, config repair, environment/config defaults, operator-facing config options, allow/deny configuration, or policy settings. Boundary: operator-facing config options qualify on their own.

### confusions
#### Item 1
##### expected
notifications

##### predicted
reliability

##### count
2

##### action
Clarify `notifications` vs `reliability`. For missed `notifications`: MUST include when central: generic outbound notifications, completion delivery, message delivery gates, announcements, or notify behavior is central. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label. For extra `reliability`: a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface.

##### examples
###### Item 1
###### expected
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
notifications

###### actual
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
reliability

###### keywords

###### row_score
0.667

###### Item 2
###### expected
###### Item 1
chat_integrations

###### Item 2
notifications

###### actual
###### Item 1
chat_integrations

###### Item 2
reliability

###### keywords

###### row_score
0.5

#### Item 2
##### expected
telemetry_usage

##### predicted
reliability

##### count
1

##### action
Clarify `telemetry_usage` vs `reliability`. For missed `telemetry_usage`: MUST include when central: token counts, usage counts, costs, metrics, diagnostics, traces, or status reporting are central. For extra `reliability`: a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface.

##### examples
###### Item 1
###### expected
###### Item 1
telemetry_usage

###### Item 2
ui_tui

###### actual
###### Item 1
reliability

###### Item 2
ui_tui

###### keywords

###### row_score
0.5

#### Item 3
##### expected
approvals

##### predicted
memory

##### count
1

##### action
Clarify `approvals` vs `memory`. For missed `approvals`: MUST include when central: approval prompts, permission decisions, or approval mode behavior is central. Co-label: bounding/expiring/persisting pending-approval state is approvals surface even when motivated by a memory/reliability fix. For extra `memory`: context window, session state, transcript, or generic remembering.

##### examples
###### Item 1
###### expected
###### Item 1
approvals

###### Item 2
mcp_tooling

###### Item 3
reliability

###### actual
###### Item 1
mcp_tooling

###### Item 2
memory

###### Item 3
reliability

###### keywords

###### row_score
0.667

#### Item 4
##### expected
acp

##### predicted
reliability

##### count
1

##### action
Clarify `acp` vs `reliability`. For missed `acp`: MUST include when central: ACP runtime/protocol, ACP session, ACP binding, ACP parent/child behavior, or ACP delivery is central. For extra `reliability`: a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface.

##### examples
###### Item 1
###### expected
###### Item 1
acp

###### Item 2
acpx

###### actual
###### Item 1
acpx

###### Item 2
reliability

###### keywords

###### row_score
0.5

#### Item 5
##### expected
notifications

##### predicted
tool_calling

##### count
1

##### action
Clarify `notifications` vs `tool_calling`. For missed `notifications`: MUST include when central: generic outbound notifications, completion delivery, message delivery gates, announcements, or notify behavior is central. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label. For extra `tool_calling`: generic command output, TTS, browser screenshot/vision, or config-like options. Co-label: parameter coercion/normalization for tool invocation is tool_calling, even inside an MCP bundle or adapter.

##### examples
###### Item 1
###### expected
###### Item 1
chat_integrations

###### Item 2
notifications

###### Item 3
reliability

###### actual
###### Item 1
chat_integrations

###### Item 2
reliability

###### Item 3
tool_calling

###### keywords

###### row_score
0.667

#### Item 6
##### expected
tests_ci

##### predicted
reliability

##### count
1

##### action
Clarify `tests_ci` vs `reliability`. For missed `tests_ci`: MUST include when central: only when tests, CI, or test infrastructure itself is the subject. For extra `reliability`: a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface.

##### examples
###### Item 1
###### expected
###### Item 1
packaging_deployment

###### Item 2
tests_ci

###### actual
###### Item 1
config

###### Item 2
packaging_deployment

###### Item 3
reliability

###### keywords

###### row_score
0.4

### row_examples
#### Item 1
##### id
openclaw-openclaw-42122

##### title
Speed up install smoke Docker builds

##### expected
###### Item 1
packaging_deployment

###### Item 2
tests_ci

##### actual
###### Item 1
config

###### Item 2
packaging_deployment

###### Item 3
reliability

##### false_positives
###### Item 1
config

###### Item 2
reliability

##### false_negatives
###### Item 1
tests_ci

##### row_score
0.4

#### Item 2
##### id
openclaw-openclaw-47083

##### title
fix: respect totalTokensFresh flag to avoid showing stale token counts

##### expected
###### Item 1
telemetry_usage

###### Item 2
ui_tui

##### actual
###### Item 1
reliability

###### Item 2
ui_tui

##### false_positives
###### Item 1
reliability

##### false_negatives
###### Item 1
telemetry_usage

##### row_score
0.5

#### Item 3
##### id
openclaw-openclaw-77694

##### title
[Bug]: acpx flow run ACP node outputs return empty strings instead of agent replies

##### expected
###### Item 1
acp

###### Item 2
acpx

##### actual
###### Item 1
acpx

###### Item 2
reliability

##### false_positives
###### Item 1
reliability

##### false_negatives
###### Item 1
acp

##### row_score
0.5

#### Item 4
##### id
openclaw-openclaw-82642

##### title
Fix iMessage slash command acknowledgements

##### expected
###### Item 1
chat_integrations

###### Item 2
notifications

##### actual
###### Item 1
chat_integrations

###### Item 2
reliability

##### false_positives
###### Item 1
reliability

##### false_negatives
###### Item 1
notifications

##### row_score
0.5

#### Item 5
##### id
openclaw-openclaw-77827

##### title
fix: LM Studio thinking blocks invisible with Responses API

##### expected
###### Item 1
inference_api

##### actual
###### Item 1
inference_api

###### Item 2
reliability

###### Item 3
tool_calling

##### false_positives
###### Item 1
reliability

###### Item 2
tool_calling

##### false_negatives

##### row_score
0.5

#### Item 6
##### id
openclaw-openclaw-45200

##### title
fix(subagents): notify user on announce give-up instead of silently dropping result

##### expected
###### Item 1
coding_agents

###### Item 2
notifications

###### Item 3
reliability

##### actual
###### Item 1
gateway

###### Item 2
notifications

###### Item 3
reliability

###### Item 4
sessions

##### false_positives
###### Item 1
gateway

###### Item 2
sessions

##### false_negatives
###### Item 1
coding_agents

##### row_score
0.5714285714285714

#### Item 7
##### id
openclaw-openclaw-73910

##### title
BUG: OpenClaw-managed Codex ACP uses isolated CODEX_HOME without auth bridge and sends unsupported timeout config

##### expected
###### Item 1
acp

###### Item 2
acpx

###### Item 3
auth_identity

###### Item 4
codex

###### Item 5
security

##### actual
###### Item 1
acp

###### Item 2
auth_identity

###### Item 3
codex

###### Item 4
reliability

##### false_positives
###### Item 1
reliability

##### false_negatives
###### Item 1
acpx

###### Item 2
security

##### row_score
0.6666666666666666

#### Item 8
##### id
openclaw-openclaw-71157

##### title
[Feature]: Support WhatsApp disappearing-message expiration for outbound replies

##### expected
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
notifications

##### actual
###### Item 1
chat_integrations

###### Item 2
config

###### Item 3
reliability

##### false_positives
###### Item 1
reliability

##### false_negatives
###### Item 1
notifications

##### row_score
0.6666666666666666

### prompt_hygiene
#### ok
True

#### findings

#### policy_chars
6508

### reflection_hint
Make concise reusable routing rules. Do not copy the fixed allowed-topic taxonomy, do not add row-specific examples, and do not optimize for recall at the expense of F1.

## static_asi_path
eval/openclaw/easy-set-pilot/v6/vanilla-asi-v6-slim.md

## candidate_idx
3

## batch_summary
### model
gemma-e4

### input
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/input.jsonl

### output
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/candidate-0003/results.jsonl

### schema
None

### schema_model
None

### instruction
None

### agent_card
eval/openclaw/easy-set-pilot/v6/openclaw-vanilla-labeler-plain-v6a.md

### agent
openclaw_vanilla_labeler_plain

### template
/home/ssmith/temp/gepa-batch-openclaw/eval/openclaw/task-template.md

### shell_runtime
False

### output_mode
text

### export_traces
None

### hf_dataset
None

### hf_dataset_path
None

### parallel
4

### work_dir
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/candidate-0003/.results.jsonl.batch/20260611T211826Z-af368b82

### started_at
2026-06-11T21:18:26Z

### completed_at
2026-06-11T21:19:01Z

### input_rows
32

### selected_rows
32

### processed_rows
32

### skipped_rows
0

### failed_rows
0

### duration_ms
33262.13

### timing_ms
#### duration
##### count
32

##### min
1489.23

##### mean
3965.59

##### median_approx
3942.90125

##### max
5314.73

#### ttft
##### count
32

##### min
691.34

##### mean
2717.1978125

##### median_approx
2823.33875

##### max
4822.81

#### time_to_response
##### count
32

##### min
691.34

##### mean
2717.1978125

##### median_approx
2823.33875

##### max
4822.81

### usage
#### input_tokens
215008

#### output_tokens
258

#### total_tokens
215266

#### billing_tokens
215266

#### reasoning_tokens
0

#### tool_use_tokens
0

#### tool_calls
0

#### rows_with_usage
32

#### usage_coverage_percent
100.0

### cache
#### read_tokens
0

#### write_tokens
0

#### hit_tokens
148992

#### served_tokens
148992

#### activity_tokens
148992

#### effective_input_tokens
66016

#### hit_rate_percent
69.29602619437416

#### write_rate_percent
0.0

#### activity_rate_percent
69.29602619437416

#### rows_with_cache_activity
32

#### row_cache_activity_percent
100.0

#### non_cached_input_tokens
66016

#### served_to_effective_input_ratio
2.256907416383907

### shards
#### Item 1
##### index
0

##### offset
0

##### limit
8

##### output
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/candidate-0003/.results.jsonl.batch/20260611T211826Z-af368b82/part-000.jsonl

#### Item 2
##### index
1

##### offset
8

##### limit
8

##### output
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/candidate-0003/.results.jsonl.batch/20260611T211826Z-af368b82/part-001.jsonl

#### Item 3
##### index
2

##### offset
16

##### limit
8

##### output
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/candidate-0003/.results.jsonl.batch/20260611T211826Z-af368b82/part-002.jsonl

#### Item 4
##### index
3

##### offset
24

##### limit
8

##### output
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/candidate-0003/.results.jsonl.batch/20260611T211826Z-af368b82/part-003.jsonl

## lineage
### policy_sha256
99fbb376dd1822db9604a736ed67cc1c2f2cfd077e7a3d3983ebaef3ed8e5a2d

### parent_candidate_idx
2

### reflection_call
call-0002


```

## Your Task

Analyze the evaluation results systematically:

- **Goal alignment**: How well does the current component achieve the stated optimization goal?
- **Failure patterns**: What specific errors, edge cases, or failure modes appear in the evaluation data?
- **Success patterns**: What behaviors or approaches worked well and should be preserved?
- **Root causes**: What underlying issues explain the observed failures?
- **Constraint compliance**: Does the component satisfy all requirements from the domain context?

Based on your analysis, propose an improved version that:
1. Addresses the identified failure patterns and root causes
2. Preserves successful behaviors from the current version
3. Makes meaningful improvements rather than superficial changes
4. Adheres to all constraints and requirements from the domain context

## Output Format

Provide ONLY the improved version within ``` blocks. The output must be a complete, 
drop-in replacement for the current component (whether it's a prompt, configuration, 
code, or any other parameter type).
Do not include explanations, commentary, or markdown outside the ``` blocks.