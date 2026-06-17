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
labels, changed files, and diff only to confirm or disambiguate central
interests. Select every allowed topic that is a central maintainer-owned
concern under the fixed taxonomy and boundary overlay.

# Cardinality Rules

Include every topic whose inclusion rule in the fixed overlay is satisfied; do
not drop a qualifying topic to keep the output short. Use 1-3 topics by
default, 4-5 only when genuinely cross-cutting, never more than 5. Drop labels
that are only symptom locations, mechanisms, paths, examples, or consequences.
For row-exactness, prefer replacing a generic symptom label with the specific
surface label that owns the deliverable.

# Boundary Overlays

- Add `telemetry_usage` whenever the central user-visible or API concern is
  usage/status accounting, token/cost/count freshness, diagnostics, metrics, or
  traces; do not convert these to `reliability` just because values are stale or
  wrong.
- Add `notifications` when the change alters outbound delivery, acknowledgements,
  announcements, completion/result delivery, delivery gates, sent-message
  behavior, or chat reply payload paths; chat-surface delivery changes usually
  co-label `chat_integrations` and `notifications`.
- Add `coding_agents` for external coding-agent or subagent product behavior,
  including managed agent follow-ups, announcements, give-up/result delivery, or
  scheduled agent work. Do not replace it with `agent_runtime` unless the runtime
  loop/backend/orchestration machinery itself is the deliverable.
- For ACP work, include `acp` for protocol/session/binding/parent-child/delivery
  semantics even when `acpx` is also present; include `acpx` when the ACPX
  transport/proxy/worker/binding surface is explicitly central.
- Add `sessions` only when identity, lifecycle, persistence, transcript,
  resume/reset, binding, cleanup, or parent/child state is central; thread-bound
  or parent-orchestrated follow-up behavior can qualify. Mere session context,
  files, or display state does not.
- Add `approvals` for permission decisions, prompts, pending approval state, TTLs,
  caps, clearing, or approval-mode behavior even when surfaced through MCP or
  another adapter.
- Add `hooks` when emitted hook events, hook payloads, hook ordering/filtering, or
  managed hook behavior is changed; do not hide hook work under reliability.
- Add `tests_ci` for smoke tests, CI/build-test speed, fixtures, coverage, mocks,
  or test infrastructure as the maintained surface, even when Docker or install
  machinery is involved.
- Add `security` for credential isolation/bridging, auth-boundary exposure,
  unsupported credential scope, sandbox escape, private access, token leakage, or
  other boundary hardening; do not collapse these into reliability.
- Add `self_hosted_inference` when cron/config/preflight/provider work is about a
  self-hosted engine or local serving backend; keep `local_models` for model
  artifact/hardware behavior rather than engine integration.
- Use `api_surface` only for external contract shape or documented endpoint/CLI/SDK
  behavior. Chat slash-command acknowledgements or platform replies are usually
  `chat_integrations` plus `notifications`, not `api_surface`.
- Use `config` only for operator-facing options, persisted schema/defaults,
  validation/repair, policy settings, or migrations. Do not add it for an
  internal flag, test knob, build option, or implementation detail.
- Use `chat_integrations` only for a named chat platform/channel adapter or chat
  delivery surface, not for generic assistant message UI.
- Use `ui_tui` for user-facing OpenClaw UI controls, status/footer/list views,
  copy buttons, or visible app text; do not add integration labels just because
  the UI contains messages.
- Use `codex` only when Codex runtime/auth/plugin/ACP/command compatibility is
  central; a cosmetic or UI-only change in a Codex-branded app may be just
  `ui_tui`.

# Suppression Rules

- Do not add `reliability` for every bug/fix, incorrect value, missing UI text,
  provider incompatibility, or protocol output mismatch. Require a central
  operational concern such as retry/timeout, crash, leak, cap/TTL, stuck state,
  dropped work, lifecycle cleanup, race, recovery, overload, or data loss.
- Do not add `tool_calling` unless the model tool-call protocol, schemas, deltas,
  transcript/result routing, or function-call rendering is the maintained
  surface. Generic command output, API response content, ACP node output, TTS,
  vision, screenshots, or chat replies are not enough.
- Do not add `memory` for generic remembering, context, pending state, transcript,
  or recall words unless the memory/index/vector/provider surface is central.
- Do not add `gateway` merely because work passes through a daemon or service;
  require gateway-owned routes, protocol, startup, state, health, or execution.
- Do not add `agent_runtime` for ACP delivery semantics, external coding-agent
  integrations, subagent product behavior, or notification/result handling unless
  core runtime machinery is directly changed.
- Do not add `sessions` for stale counters, UI state, chat threads, or incidental
  session files unless session ownership/lifecycle/state is the deliverable.
- Do not add `config` or `packaging_deployment` from changed files alone; require
  the maintained product surface, not build/test plumbing or examples.
- When a specific surface explains the row, suppress broader symptom labels that
  only describe why the change was needed.
```

## Evaluation Results

Performance data from evaluating the current component across test cases:

```
# Example 1
## Scores (Higher is Better)
### gepa_score
0.6757617868098159

### composite_score
0.683731786809816

### topic_micro_f1
0.7852760736196319

### row_exact_accuracy
0.40625

### avg_row_jaccard
0.6994791666666667

### row_symdiff_score
0.47761194029850745

### policy_length_compliance
0.9203

### policy_hygiene_compliance
1.0

## score_details
### false_positives
22

### false_negatives
13

### row_exact_accuracy
0.40625

### avg_row_jaccard
0.6994791666666667

### avg_row_symdiff
1.09375

### avg_expected_topics
2.40625

### avg_predicted_topics
2.6875

### asi_score
1.0

### topic_micro_precision
0.7441860465116279

### topic_micro_recall
0.8311688311688312

### exact_match
0.40625

### row_symdiff_score
0.47761194029850745

### composite_score
0.683731786809816

### gepa_score
0.6757617868098159

### score_mode
row-aware

### valid_json
1.0

### cardinality_closeness
0.8831168831168831

### avg_topic_count_delta
0.28125

### policy_chars
5594

### policy_char_budget
4000

### policy_length_over_budget
1594

### policy_length_penalty
0.00797

### policy_length_compliance
0.9203

### hygiene_penalty
0.0

### hygiene_findings_count
0

## evaluated
32

## failures
### Item 1
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
sessions

##### Item 3
ui_tui

#### false_positives
##### Item 1
reliability

##### Item 2
sessions

#### false_negatives
##### Item 1
telemetry_usage

#### invalid_topics

#### keywords

#### row_score
0.4

### Item 2
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
reliability

#### false_positives
##### Item 1
reliability

#### false_negatives

#### invalid_topics

#### keywords

#### row_score
0.8

### Item 3
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

### Item 4
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
approvals

##### Item 2
mcp_tooling

##### Item 3
memory

##### Item 4
reliability

#### false_positives
##### Item 1
memory

#### false_negatives

#### invalid_topics

#### keywords

#### row_score
0.8571428571428571

### Item 5
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

### Item 6
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

### Item 7
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

### Item 8
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
notifications

##### Item 3
reliability

#### false_positives
##### Item 1
reliability

#### false_negatives

#### invalid_topics

#### keywords

#### row_score
0.8

### Item 9
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

### Item 10
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

### Item 11
#### id
openclaw-openclaw-88400

#### title
fix(config): accept overlays for bundled provider aliases

#### expected
##### Item 1
config

##### Item 2
inference_api

#### actual
##### Item 1
config

##### Item 2
model_lifecycle

#### false_positives
##### Item 1
model_lifecycle

#### false_negatives
##### Item 1
inference_api

#### invalid_topics

#### keywords

#### row_score
0.5

### Item 12
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

## worst_failures
### Item 1
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
agent_runtime

##### Item 2
gateway

##### Item 3
notifications

#### false_positives
##### Item 1
agent_runtime

##### Item 2
gateway

#### false_negatives
##### Item 1
coding_agents

##### Item 2
reliability

#### invalid_topics

#### keywords

#### row_score
0.3333333333333333

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
sessions

##### Item 3
ui_tui

#### false_positives
##### Item 1
reliability

##### Item 2
sessions

#### false_negatives
##### Item 1
telemetry_usage

#### invalid_topics

#### keywords

#### row_score
0.4

### Item 3
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

### Item 4
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

### Item 5
#### id
openclaw-openclaw-88400

#### title
fix(config): accept overlays for bundled provider aliases

#### expected
##### Item 1
config

##### Item 2
inference_api

#### actual
##### Item 1
config

##### Item 2
model_lifecycle

#### false_positives
##### Item 1
model_lifecycle

#### false_negatives
##### Item 1
inference_api

#### invalid_topics

#### keywords

#### row_score
0.5

### Item 6
#### id
openclaw-openclaw-67539

#### title
[Feature]: Add provider-specific TTS prompt hints

#### expected
##### Item 1
inference_api

#### actual
##### Item 1
inference_api

##### Item 2
skills_plugins

##### Item 3
tool_calling

#### false_positives
##### Item 1
skills_plugins

##### Item 2
tool_calling

#### false_negatives

#### invalid_topics

#### keywords

#### row_score
0.5

### Item 7
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

### Item 8
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

## topic_error_patterns
### Item 1
#### topic
reliability

#### problem
over_predicted

#### expected
10

#### actual
17

#### true_positives
9

#### false_positives
8

#### false_negatives
1

#### precision
0.529

#### recall
0.9

#### f1
0.667

#### action
`reliability` over_predicted: expected in 10 rows, predicted in 17, TP=9, FP=8, FN=1, precision=0.529, recall=0.900. Precision is the bottleneck. a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface.

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
sessions

###### Item 3
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
approvals

###### Item 2
mcp_tooling

###### Item 3
memory

###### Item 4
reliability

###### keywords

###### row_score
0.857

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
sessions

###### Item 3
ui_tui

###### keywords

###### row_score
0.4

##### Item 2
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
reliability

###### keywords

###### row_score
0.8

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
agent_runtime

###### Item 2
gateway

###### Item 3
notifications

###### keywords

###### row_score
0.333

### Item 2
#### topic
sessions

#### problem
over_predicted

#### expected
6

#### actual
9

#### true_positives
6

#### false_positives
3

#### false_negatives
0

#### precision
0.667

#### recall
1.0

#### f1
0.8

#### action
`sessions` over_predicted: expected in 6 rows, predicted in 9, TP=6, FP=3, FN=0, precision=0.667, recall=1.000. Precision is the bottleneck. every mention of session context or session files.

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
sessions

###### Item 3
ui_tui

###### keywords

###### error_type
false_positive

##### Item 2
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

##### Item 3
###### expected
###### Item 1
acp

###### Item 2
config

###### Item 3
queueing

###### Item 4
reliability

###### actual
###### Item 1
acp

###### Item 2
config

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
telemetry_usage

###### Item 2
ui_tui

###### actual
###### Item 1
reliability

###### Item 2
sessions

###### Item 3
ui_tui

###### keywords

###### row_score
0.4

##### Item 2
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

##### Item 3
###### expected
###### Item 1
acp

###### Item 2
config

###### Item 3
queueing

###### Item 4
reliability

###### actual
###### Item 1
acp

###### Item 2
config

###### Item 3
reliability

###### Item 4
sessions

###### keywords

###### row_score
0.75

#### false_negative_examples

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
skills_plugins

###### Item 3
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
skills_plugins

###### Item 3
tool_calling

###### keywords

###### row_score
0.5

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
agent_runtime

###### Item 2
gateway

###### Item 3
notifications

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
agent_runtime

###### Item 2
gateway

###### Item 3
notifications

###### keywords

###### row_score
0.333

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
agent_runtime

#### problem
mixed

#### expected
0

#### actual
2

#### true_positives
0

#### false_positives
2

#### false_negatives
0

#### precision
0.0

#### recall
0.0

#### f1
0.0

#### action
`agent_runtime` mixed: expected in 0 rows, predicted in 2, TP=0, FP=2, FN=0, precision=0.000, recall=0.000. Both precision and recall need boundary work. Mixed `agent_runtime` errors. ACPX worker internals alone (`acpx`) or any agent-adjacent provider/UI/config change. Do not route internal runtime work to `coding_agents` unless the item is specifically about an external coding-agent integration. MUST include when central: agent runtime startup, loop, backend, model call orchestration, runtime adapter behavior, or runtime ownership/execution architecture is central.

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
agent_runtime

###### Item 2
gateway

###### Item 3
notifications

###### keywords

###### error_type
false_positive

##### Item 2
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
false_positive

#### true_positive_examples

#### false_positive_examples
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
agent_runtime

###### Item 2
gateway

###### Item 3
notifications

###### keywords

###### row_score
0.333

##### Item 2
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

#### false_negative_examples

### Item 6
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
reliability

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
notifications

###### keywords

###### row_score
1.0

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

### Item 7
#### topic
acp

#### problem
mixed

#### expected
6

#### actual
5

#### true_positives
5

#### false_positives
0

#### false_negatives
1

#### precision
1.0

#### recall
0.833

#### f1
0.909

#### action
`acp` mixed: expected in 6 rows, predicted in 5, TP=5, FP=0, FN=1, precision=1.000, recall=0.833. Both precision and recall need boundary work. Mixed `acp` errors. merely because an item mentions an agent session or internal runtime behavior. MUST include when central: ACP runtime/protocol, ACP session, ACP binding, ACP parent/child behavior, or ACP delivery is central.

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

###### error_type
false_negative

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
acp

###### Item 2
config

###### Item 3
queueing

###### Item 4
reliability

###### actual
###### Item 1
acp

###### Item 2
config

###### Item 3
reliability

###### Item 4
sessions

###### keywords

###### row_score
0.75

##### Item 3
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

#### false_positive_examples

#### false_negative_examples
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

### Item 8
#### topic
notifications

#### problem
mixed

#### expected
5

#### actual
4

#### true_positives
4

#### false_positives
0

#### false_negatives
1

#### precision
1.0

#### recall
0.8

#### f1
0.889

#### action
`notifications` mixed: expected in 5 rows, predicted in 4, TP=4, FP=0, FN=1, precision=1.000, recall=0.800. Both precision and recall need boundary work. Mixed `notifications` errors. chat-platform-specific behavior alone (`chat_integrations`) or reliability-only recovery. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label. MUST include when central: generic outbound notifications, completion delivery, message delivery gates, announcements, or notify behavior is central. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label.

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
false_negative

#### true_positive_examples
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
notifications

###### keywords

###### row_score
1.0

##### Item 2
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

##### Item 3
###### expected
###### Item 1
chat_integrations

###### Item 2
notifications

###### actual
###### Item 1
chat_integrations

###### Item 2
notifications

###### Item 3
reliability

###### keywords

###### row_score
0.8

#### false_positive_examples

#### false_negative_examples
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

## confusions
### Item 1
#### expected
coding_agents

#### predicted
agent_runtime

#### count
2

#### action
Clarify `coding_agents` vs `agent_runtime`. For missed `coding_agents`: MUST include when central: integrations with external coding agents in general, or with a specific coding agent such as Codex, Claude Code, Gemini CLI, or Pi. Boundary: ACP is an integration protocol and is distinct from coding-agent integrations; route ACP protocol/session/delivery work to `acp`/`acpx`. OpenClaw's internal agent runtime is a core product surface; route startup, loop, backend, model-call orchestration, and adapter machinery to `agent_runtime`. For extra `agent_runtime`: ACPX worker internals alone (`acpx`) or any agent-adjacent provider/UI/config change. Do not route internal runtime work to `coding_agents` unless the item is specifically about an external coding-agent integration.

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
agent_runtime

###### Item 2
gateway

###### Item 3
notifications

###### keywords

###### row_score
0.333

##### Item 2
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

### Item 2
#### expected
telemetry_usage

#### predicted
sessions

#### count
1

#### action
Clarify `telemetry_usage` vs `sessions`. For missed `telemetry_usage`: MUST include when central: token counts, usage counts, costs, metrics, diagnostics, traces, or status reporting are central. For extra `sessions`: every mention of session context or session files.

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
sessions

###### Item 3
ui_tui

###### keywords

###### row_score
0.4

### Item 3
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
sessions

###### Item 3
ui_tui

###### keywords

###### row_score
0.4

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
inference_api

#### predicted
model_lifecycle

#### count
1

#### action
Clarify `inference_api` vs `model_lifecycle`. For missed `inference_api`: MUST include when central: the integration layer between OpenClaw and model serving/providers — usage of Responses, Chat Completions, Anthropic Messages, or similar inference APIs and integrations (including TTS, vision, and embeddings APIs); streaming/SSE and usage chunks; base URL normalization; inference request/response handling; or adding/configuring inference providers (setup, auth, routing, references, catalogs, allow/deny rules, compatibility checks). For extra `model_lifecycle`: merely because a model name appears, or inference API-integration changes (`inference_api`).

#### examples
##### Item 1
###### expected
###### Item 1
config

###### Item 2
inference_api

###### actual
###### Item 1
config

###### Item 2
model_lifecycle

###### keywords

###### row_score
0.5

## invalid_topics

## actionable_feedback
### Item 1
Pure-F1 objective: optimize exact topic membership, not recall-biased F-beta. Current precision=0.744, recall=0.831, F1=0.785.

### Item 2
Cardinality diagnosis: over_labeling; avg predicted 2.69 vs expected 2.41. Tighten incidental-evidence gates and remove labels supported only by files, tests, examples, or side effects.

### Item 3
Policy length penalty: policy is 1594 chars over the 4000 char budget; GEPA score was reduced by 0.0080.

### Item 4
Candidate is over-labeling: avg predicted topics 2.69 vs expected 2.41. Strengthen title-first centrality and second-topic gates.

### Item 5
`reliability` over_predicted: expected in 10 rows, predicted in 17, TP=9, FP=8, FN=1, precision=0.529, recall=0.900. Precision is the bottleneck. a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface.

### Item 6
`sessions` over_predicted: expected in 6 rows, predicted in 9, TP=6, FP=3, FN=0, precision=0.667, recall=1.000. Precision is the bottleneck. every mention of session context or session files.

### Item 7
`tool_calling` over_predicted: expected in 0 rows, predicted in 3, TP=0, FP=3, FN=0, precision=0.000, recall=0.000. Precision is the bottleneck. generic command output, TTS, browser screenshot/vision, or config-like options. Co-label: parameter coercion/normalization for tool invocation is tool_calling, even inside an MCP bundle or adapter.

### Item 8
`coding_agents` under_predicted: expected in 3 rows, predicted in 0, TP=0, FP=0, FN=3, precision=0.000, recall=0.000. Recall is the bottleneck. MUST include when central: integrations with external coding agents in general, or with a specific coding agent such as Codex, Claude Code, Gemini CLI, or Pi. Boundary: ACP is an integration protocol and is distinct from coding-agent integrations; route ACP protocol/session/delivery work to `acp`/`acpx`. OpenClaw's internal agent runtime is a core product surface; route startup, loop, backend, model-call orchestration, and adapter machinery to `agent_runtime`.

### Item 9
`agent_runtime` mixed: expected in 0 rows, predicted in 2, TP=0, FP=2, FN=0, precision=0.000, recall=0.000. Both precision and recall need boundary work. Mixed `agent_runtime` errors. ACPX worker internals alone (`acpx`) or any agent-adjacent provider/UI/config change. Do not route internal runtime work to `coding_agents` unless the item is specifically about an external coding-agent integration. MUST include when central: agent runtime startup, loop, backend, model call orchestration, runtime adapter behavior, or runtime ownership/execution architecture is central.

### Item 10
`config` mixed: expected in 5 rows, predicted in 6, TP=5, FP=1, FN=0, precision=0.833, recall=1.000. Both precision and recall need boundary work. Mixed `config` errors. a config key that is merely the internal mechanism, example, or implementation detail of another surface's change. Boundary: operator-facing config options qualify on their own. MUST include when central: configuration schemas, persisted config shape, config loading, config validation, config repair, environment/config defaults, operator-facing config options, allow/deny configuration, or policy settings. Boundary: operator-facing config options qualify on their own.

## vanilla_f1_asi
### global_diagnosis
#### precision
0.7441860465116279

#### recall
0.8311688311688312

#### f1
0.7852760736196319

#### gepa_score
0.6757617868098159

#### score_mode
row-aware

#### exact_match
0.40625

#### row_exact_accuracy
0.40625

#### avg_row_jaccard
0.6994791666666667

#### avg_row_symdiff
1.09375

#### row_symdiff_score
0.47761194029850745

#### composite_score
0.683731786809816

#### valid_json
1.0

#### cardinality_closeness
0.8831168831168831

#### avg_expected_topics
2.40625

#### avg_predicted_topics
2.6875

#### false_positives
22

#### false_negatives
13

#### policy_chars
5594

#### policy_char_budget
4000

#### policy_length_over_budget
1594

#### policy_length_penalty
0.00797

#### policy_length_compliance
0.9203

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
1

##### precision
0.529

##### recall
0.9

##### action
`reliability` over_predicted: expected in 10 rows, predicted in 17, TP=9, FP=8, FN=1, precision=0.529, recall=0.900. Precision is the bottleneck. a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface.

#### Item 2
##### topic
sessions

##### problem
over_predicted

##### false_positives
3

##### false_negatives
0

##### precision
0.667

##### recall
1.0

##### action
`sessions` over_predicted: expected in 6 rows, predicted in 9, TP=6, FP=3, FN=0, precision=0.667, recall=1.000. Precision is the bottleneck. every mention of session context or session files.

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
agent_runtime

##### problem
mixed

##### false_positives
2

##### false_negatives
0

##### precision
0.0

##### recall
0.0

##### action
`agent_runtime` mixed: expected in 0 rows, predicted in 2, TP=0, FP=2, FN=0, precision=0.000, recall=0.000. Both precision and recall need boundary work. Mixed `agent_runtime` errors. ACPX worker internals alone (`acpx`) or any agent-adjacent provider/UI/config change. Do not route internal runtime work to `coding_agents` unless the item is specifically about an external coding-agent integration. MUST include when central: agent runtime startup, loop, backend, model call orchestration, runtime adapter behavior, or runtime ownership/execution architecture is central.

#### Item 6
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

#### Item 7
##### topic
acp

##### problem
mixed

##### false_positives
0

##### false_negatives
1

##### precision
1.0

##### recall
0.833

##### action
`acp` mixed: expected in 6 rows, predicted in 5, TP=5, FP=0, FN=1, precision=1.000, recall=0.833. Both precision and recall need boundary work. Mixed `acp` errors. merely because an item mentions an agent session or internal runtime behavior. MUST include when central: ACP runtime/protocol, ACP session, ACP binding, ACP parent/child behavior, or ACP delivery is central.

#### Item 8
##### topic
notifications

##### problem
mixed

##### false_positives
0

##### false_negatives
1

##### precision
1.0

##### recall
0.8

##### action
`notifications` mixed: expected in 5 rows, predicted in 4, TP=4, FP=0, FN=1, precision=1.000, recall=0.800. Both precision and recall need boundary work. Mixed `notifications` errors. chat-platform-specific behavior alone (`chat_integrations`) or reliability-only recovery. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label. MUST include when central: generic outbound notifications, completion delivery, message delivery gates, announcements, or notify behavior is central. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label.

### confusions
#### Item 1
##### expected
coding_agents

##### predicted
agent_runtime

##### count
2

##### action
Clarify `coding_agents` vs `agent_runtime`. For missed `coding_agents`: MUST include when central: integrations with external coding agents in general, or with a specific coding agent such as Codex, Claude Code, Gemini CLI, or Pi. Boundary: ACP is an integration protocol and is distinct from coding-agent integrations; route ACP protocol/session/delivery work to `acp`/`acpx`. OpenClaw's internal agent runtime is a core product surface; route startup, loop, backend, model-call orchestration, and adapter machinery to `agent_runtime`. For extra `agent_runtime`: ACPX worker internals alone (`acpx`) or any agent-adjacent provider/UI/config change. Do not route internal runtime work to `coding_agents` unless the item is specifically about an external coding-agent integration.

##### examples
###### Item 1
###### expected
###### Item 1
coding_agents

###### Item 2
notifications

###### Item 3
reliability

###### actual
###### Item 1
agent_runtime

###### Item 2
gateway

###### Item 3
notifications

###### keywords

###### row_score
0.333

###### Item 2
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

#### Item 2
##### expected
telemetry_usage

##### predicted
sessions

##### count
1

##### action
Clarify `telemetry_usage` vs `sessions`. For missed `telemetry_usage`: MUST include when central: token counts, usage counts, costs, metrics, diagnostics, traces, or status reporting are central. For extra `sessions`: every mention of session context or session files.

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
sessions

###### Item 3
ui_tui

###### keywords

###### row_score
0.4

#### Item 3
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
sessions

###### Item 3
ui_tui

###### keywords

###### row_score
0.4

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
inference_api

##### predicted
model_lifecycle

##### count
1

##### action
Clarify `inference_api` vs `model_lifecycle`. For missed `inference_api`: MUST include when central: the integration layer between OpenClaw and model serving/providers — usage of Responses, Chat Completions, Anthropic Messages, or similar inference APIs and integrations (including TTS, vision, and embeddings APIs); streaming/SSE and usage chunks; base URL normalization; inference request/response handling; or adding/configuring inference providers (setup, auth, routing, references, catalogs, allow/deny rules, compatibility checks). For extra `model_lifecycle`: merely because a model name appears, or inference API-integration changes (`inference_api`).

##### examples
###### Item 1
###### expected
###### Item 1
config

###### Item 2
inference_api

###### actual
###### Item 1
config

###### Item 2
model_lifecycle

###### keywords

###### row_score
0.5

### row_examples
#### Item 1
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
agent_runtime

###### Item 2
gateway

###### Item 3
notifications

##### false_positives
###### Item 1
agent_runtime

###### Item 2
gateway

##### false_negatives
###### Item 1
coding_agents

###### Item 2
reliability

##### row_score
0.3333333333333333

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
sessions

###### Item 3
ui_tui

##### false_positives
###### Item 1
reliability

###### Item 2
sessions

##### false_negatives
###### Item 1
telemetry_usage

##### row_score
0.4

#### Item 3
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

#### Item 4
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

#### Item 5
##### id
openclaw-openclaw-88400

##### title
fix(config): accept overlays for bundled provider aliases

##### expected
###### Item 1
config

###### Item 2
inference_api

##### actual
###### Item 1
config

###### Item 2
model_lifecycle

##### false_positives
###### Item 1
model_lifecycle

##### false_negatives
###### Item 1
inference_api

##### row_score
0.5

#### Item 6
##### id
openclaw-openclaw-67539

##### title
[Feature]: Add provider-specific TTS prompt hints

##### expected
###### Item 1
inference_api

##### actual
###### Item 1
inference_api

###### Item 2
skills_plugins

###### Item 3
tool_calling

##### false_positives
###### Item 1
skills_plugins

###### Item 2
tool_calling

##### false_negatives

##### row_score
0.5

#### Item 7
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

#### Item 8
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

### prompt_hygiene
#### ok
True

#### findings

#### policy_chars
5594

### reflection_hint
Make concise reusable routing rules. Do not copy the fixed allowed-topic taxonomy, do not add row-specific examples, and do not optimize for recall at the expense of F1.

## static_asi_path
eval/openclaw/easy-set-pilot/v6/vanilla-asi-v6-slim.md

## candidate_idx
12

## batch_summary
### model
gemma-e4

### input
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/input.jsonl

### output
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/candidate-0012/results.jsonl

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
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/candidate-0012/.results.jsonl.batch/20260611T213319Z-da4151dd

### started_at
2026-06-11T21:33:19Z

### completed_at
2026-06-11T21:33:55Z

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
33630.74

### timing_ms
#### duration
##### count
32

##### min
3444.19

##### mean
4092.7418749999997

##### median_approx
4183.9887499999995

##### max
4958.56

#### ttft
##### count
32

##### min
1055.3

##### mean
2919.723125

##### median_approx
2970.55625

##### max
4875.22

#### time_to_response
##### count
32

##### min
1055.3

##### mean
2919.723125

##### median_approx
2970.55625

##### max
4875.22

### usage
#### input_tokens
207616

#### output_tokens
263

#### total_tokens
207879

#### billing_tokens
207879

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
142144

#### served_tokens
142144

#### activity_tokens
142144

#### effective_input_tokens
65472

#### hit_rate_percent
68.4648581997534

#### write_rate_percent
0.0

#### activity_rate_percent
68.4648581997534

#### rows_with_cache_activity
32

#### row_cache_activity_percent
100.0

#### non_cached_input_tokens
65472

#### served_to_effective_input_ratio
2.1710654936461387

### shards
#### Item 1
##### index
0

##### offset
0

##### limit
8

##### output
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/candidate-0012/.results.jsonl.batch/20260611T213319Z-da4151dd/part-000.jsonl

#### Item 2
##### index
1

##### offset
8

##### limit
8

##### output
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/candidate-0012/.results.jsonl.batch/20260611T213319Z-da4151dd/part-001.jsonl

#### Item 3
##### index
2

##### offset
16

##### limit
8

##### output
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/candidate-0012/.results.jsonl.batch/20260611T213319Z-da4151dd/part-002.jsonl

#### Item 4
##### index
3

##### offset
24

##### limit
8

##### output
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/candidate-0012/.results.jsonl.batch/20260611T213319Z-da4151dd/part-003.jsonl

## lineage
### policy_sha256
c48334f70f98a7b5ab798cad8dfdecf9e2f5b45af2ce080006b1244c240e8f35

### parent_candidate_idx
1

### reflection_call
call-0011


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