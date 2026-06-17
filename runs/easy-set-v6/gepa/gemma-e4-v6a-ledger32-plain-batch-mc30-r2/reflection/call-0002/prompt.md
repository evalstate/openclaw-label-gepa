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

Prefer the product surface being changed over the symptom, file location,
implementation helper, or bug mechanism. A topic qualifies only when its owner
would need to review the intended behavior or contract.

# Cardinality Rules

Include every topic whose inclusion rule in the fixed overlay is satisfied; do
not drop a qualifying topic to keep the output short. Use 1-3 topics by
default, 4-5 only when genuinely cross-cutting, never more than 5. Drop labels
that are only symptom locations, mechanisms, paths, examples, or consequences.

Before final output, remove weak extras: if a label is supported only by a bug
word, test/build file, example platform, config key name, session mention, or
tool/message wording, do not emit it.

# Boundary Overlays

- Add `reliability` only when the fix itself changes operational failure
  handling: retries, timeouts, crashes, leaks, caps/TTL, cleanup, stuck state,
  data loss, races, overload, terminal states, or recovery. Do not use it for a
  generic bug, wrong display/value, missing payload, compatibility mismatch, or
  failure that merely motivates another surface.
- Add `telemetry_usage` when counts, token/usage/cost accounting, metrics,
  traces, diagnostics, or status reporting are central, including when surfaced
  through UI, gateway, API, or sessions; do not substitute `reliability`.
- Add `notifications` when outbound delivery, completion/ack behavior,
  announcements, delivery gates, sent-message handling, or chat reply payloads
  are central. Chat delivery changes often need both `chat_integrations` and
  `notifications`.
- Add `coding_agents` for external agent integrations or managed external
  agent flows, including subagent-style integrations. Do not replace it with
  `gateway`, `agent_runtime`, or `sessions` unless those surfaces are
  independently changed.
- For ACP/ACPX items, include `acp` for ACP protocol/session/binding,
  parent-child, node, follow-up, or delivery semantics; include `acpx` when the
  ACPX transport/proxy/worker/binding is also central.
- Use `sessions` only for lifecycle, identity, persistence, binding, resume,
  reset, transcript, parent/child state, or cleanup. Do not add it for ordinary
  context, thread, UI state, or files that merely mention sessions.
- Use `tool_calling` only for model tool-call protocol, deltas, schemas, tool
  result transcript/routing, or parameter coercion for tool invocation. Do not
  add it for ordinary command output, inference text blocks, chat messages,
  terminal states, TTS, screenshots, or config options.
- Use `config` only for operator-facing settings, persisted schema/defaults,
  loading, validation, repair, policy/allow-deny options, or migration. Do not
  add it for build/test knobs or internal constants used to implement another
  surface.
- Use `tests_ci` with `packaging_deployment` when the central change is smoke,
  CI, fixtures, or platform test infrastructure for builds/installers/images;
  do not label such rows `reliability` or `config` unless runtime behavior is
  also changed.
- Use `chat_integrations` only for a named chat platform, channel adapter,
  message ingestion, or chat delivery surface. Do not add it for generic UI
  message actions or non-chat copy/rendering features.
- A mere mention of Codex does not require `codex`; include it only when Codex
  runtime/auth/ACP/plugin/command compatibility is a central subject.
- For provider/API rendering or compatibility issues, prefer
  `inference_api`; add `self_hosted_inference` only when engine setup,
  lifecycle, compatibility, or self-hosted backend behavior is itself central.
- Add `hooks` when hook emission, registration, ordering, payload, filtering,
  execution, or hook security is central, even if the hook is sent from a chat
  or notification path.
- Add `approvals` for permission prompts, approval decisions/modes, pending
  approval state, or approval TTL/caps/cleanup; do not call pending approvals
  `memory`.
- Add `security` when credential/auth boundaries, isolated homes, token scope,
  private access, permission boundaries, secret exposure, or sandbox escape are
  central, even if the visible symptom is compatibility.

# Suppression Rules

- Suppress `reliability` when the row is only a feature request, UI/API
  correction, missing notification, stale metric display, provider formatting
  mismatch, test speedup, or generic bug fix without operational recovery
  behavior.
- Suppress `tool_calling` unless the model tool-call contract itself changes.
- Suppress `api_surface` for slash commands, chat acknowledgements, UI actions,
  or provider internals unless an external API/CLI/HTTP/SDK contract changes.
- Suppress `memory` for leaks of pending state, context/session references, or
  generic remembered data unless the memory system/index/provider is central.
- Suppress `agent_runtime` for ACP orchestration or external coding-agent
  integration unless core runtime startup/loop/backend/model-call machinery is
  the deliverable.
- Suppress `gateway` when it is only the host/path for subagents,
  notifications, or API routes and gateway behavior is not independently
  changed.
- Suppress labels inferred only from changed file paths, tests, examples,
  package names, or platform names when the title/body point to another owner.
- Suppress cosmetic platform/app mentions unless the platform integration
  behavior itself changes.
```

## Evaluation Results

Performance data from evaluating the current component across test cases:

```
# Example 1
## Scores (Higher is Better)
### gepa_score
0.652838888888889

### composite_score
0.6613888888888889

### topic_micro_f1
0.7777777777777778

### row_exact_accuracy
0.34375

### avg_row_jaccard
0.6791666666666667

### row_symdiff_score
0.47058823529411764

### policy_length_compliance
0.9145

### policy_hygiene_compliance
1.0

## score_details
### false_positives
22

### false_negatives
14

### row_exact_accuracy
0.34375

### avg_row_jaccard
0.6791666666666667

### avg_row_symdiff
1.125

### avg_expected_topics
2.40625

### avg_predicted_topics
2.65625

### asi_score
1.0

### topic_micro_precision
0.7411764705882353

### topic_micro_recall
0.8181818181818182

### exact_match
0.34375

### row_symdiff_score
0.47058823529411764

### composite_score
0.6613888888888889

### gepa_score
0.652838888888889

### score_mode
row-aware

### valid_json
1.0

### cardinality_closeness
0.8961038961038961

### avg_topic_count_delta
0.25

### policy_chars
5710

### policy_char_budget
4000

### policy_length_over_budget
1710

### policy_length_penalty
0.00855

### policy_length_compliance
0.9145

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
gateway

#### false_positives
##### Item 1
gateway

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

### Item 6
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

### Item 7
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

### Item 8
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

### Item 9
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

### Item 10
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

### Item 11
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
codex

##### Item 3
reliability

##### Item 4
security

#### false_positives
##### Item 1
reliability

#### false_negatives
##### Item 1
acpx

##### Item 2
auth_identity

#### invalid_topics

#### keywords

#### row_score
0.6666666666666666

### Item 8
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

## topic_error_patterns
### Item 1
#### topic
reliability

#### problem
over_predicted

#### expected
10

#### actual
19

#### true_positives
10

#### false_positives
9

#### false_negatives
0

#### precision
0.526

#### recall
1.0

#### f1
0.69

#### action
`reliability` over_predicted: expected in 10 rows, predicted in 19, TP=10, FP=9, FN=0, precision=0.526, recall=1.000. Precision is the bottleneck. a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface.

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
memory

###### actual
###### Item 1
memory

###### Item 2
reliability

###### keywords

###### error_type
false_positive

##### Item 3
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
memory

###### actual
###### Item 1
memory

###### Item 2
reliability

###### keywords

###### row_score
0.667

##### Item 3
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

#### false_negative_examples

### Item 2
#### topic
telemetry_usage

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
`telemetry_usage` under_predicted: expected in 3 rows, predicted in 0, TP=0, FP=0, FN=3, precision=0.000, recall=0.000. Recall is the bottleneck. MUST include when central: token counts, usage counts, costs, metrics, diagnostics, traces, or status reporting are central.

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
false_negative

##### Item 2
###### expected
###### Item 1
sessions

###### Item 2
telemetry_usage

###### Item 3
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
false_negative

##### Item 3
###### expected
###### Item 1
api_surface

###### Item 2
gateway

###### Item 3
telemetry_usage

###### actual
###### Item 1
api_surface

###### Item 2
gateway

###### Item 3
reliability

###### keywords

###### error_type
false_negative

#### true_positive_examples

#### false_positive_examples

#### false_negative_examples
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
sessions

###### Item 2
telemetry_usage

###### Item 3
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
0.667

##### Item 3
###### expected
###### Item 1
api_surface

###### Item 2
gateway

###### Item 3
telemetry_usage

###### actual
###### Item 1
api_surface

###### Item 2
gateway

###### Item 3
reliability

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
reliability

###### Item 2
sessions

###### Item 3
ui_tui

###### keywords

###### row_score
0.667

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
gateway

#### problem
mixed

#### expected
1

#### actual
3

#### true_positives
1

#### false_positives
2

#### false_negatives
0

#### precision
0.333

#### recall
1.0

#### f1
0.5

#### action
`gateway` mixed: expected in 1 rows, predicted in 3, TP=1, FP=2, FN=0, precision=0.333, recall=1.000. Both precision and recall need boundary work. Mixed `gateway` errors. ordinary provider proxy, HTTP compatibility, or app-runtime bugs unless the gateway is the owning boundary. MUST include when central: gateway routing, gateway state, gateway startup, gateway protocol, or gateway-owned execution is central.

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
gateway

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
api_surface

###### Item 2
gateway

###### Item 3
telemetry_usage

###### actual
###### Item 1
api_surface

###### Item 2
gateway

###### Item 3
reliability

###### keywords

###### row_score
0.667

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
gateway

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
gateway

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
gateway

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

## confusions
### Item 1
#### expected
telemetry_usage

#### predicted
reliability

#### count
3

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

##### Item 2
###### expected
###### Item 1
sessions

###### Item 2
telemetry_usage

###### Item 3
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
0.667

### Item 2
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

### Item 3
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

### Item 4
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

### Item 5
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

### Item 6
#### expected
tests_ci

#### predicted
config

#### count
1

#### action
Clarify `tests_ci` vs `config`. For missed `tests_ci`: MUST include when central: only when tests, CI, or test infrastructure itself is the subject. For extra `config`: a config key that is merely the internal mechanism, example, or implementation detail of another surface's change. Boundary: operator-facing config options qualify on their own.

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
Pure-F1 objective: optimize exact topic membership, not recall-biased F-beta. Current precision=0.741, recall=0.818, F1=0.778.

### Item 2
Cardinality diagnosis: over_labeling; avg predicted 2.66 vs expected 2.41. Tighten incidental-evidence gates and remove labels supported only by files, tests, examples, or side effects.

### Item 3
Policy length penalty: policy is 1710 chars over the 4000 char budget; GEPA score was reduced by 0.0086.

### Item 4
Topic cardinality is close: avg predicted topics 2.66 vs expected 2.41. Focus on boundary-specific errors.

### Item 5
`reliability` over_predicted: expected in 10 rows, predicted in 19, TP=10, FP=9, FN=0, precision=0.526, recall=1.000. Precision is the bottleneck. a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface.

### Item 6
`telemetry_usage` under_predicted: expected in 3 rows, predicted in 0, TP=0, FP=0, FN=3, precision=0.000, recall=0.000. Recall is the bottleneck. MUST include when central: token counts, usage counts, costs, metrics, diagnostics, traces, or status reporting are central.

### Item 7
`tool_calling` over_predicted: expected in 0 rows, predicted in 3, TP=0, FP=3, FN=0, precision=0.000, recall=0.000. Precision is the bottleneck. generic command output, TTS, browser screenshot/vision, or config-like options. Co-label: parameter coercion/normalization for tool invocation is tool_calling, even inside an MCP bundle or adapter.

### Item 8
`coding_agents` under_predicted: expected in 3 rows, predicted in 0, TP=0, FP=0, FN=3, precision=0.000, recall=0.000. Recall is the bottleneck. MUST include when central: integrations with external coding agents in general, or with a specific coding agent such as Codex, Claude Code, Gemini CLI, or Pi. Boundary: ACP is an integration protocol and is distinct from coding-agent integrations; route ACP protocol/session/delivery work to `acp`/`acpx`. OpenClaw's internal agent runtime is a core product surface; route startup, loop, backend, model-call orchestration, and adapter machinery to `agent_runtime`.

### Item 9
`sessions` mixed: expected in 6 rows, predicted in 8, TP=6, FP=2, FN=0, precision=0.750, recall=1.000. Both precision and recall need boundary work. Mixed `sessions` errors. every mention of session context or session files. MUST include when central: session lifecycle, state, storage, identity, binding, or cleanup is central.

### Item 10
`gateway` mixed: expected in 1 rows, predicted in 3, TP=1, FP=2, FN=0, precision=0.333, recall=1.000. Both precision and recall need boundary work. Mixed `gateway` errors. ordinary provider proxy, HTTP compatibility, or app-runtime bugs unless the gateway is the owning boundary. MUST include when central: gateway routing, gateway state, gateway startup, gateway protocol, or gateway-owned execution is central.

## vanilla_f1_asi
### global_diagnosis
#### precision
0.7411764705882353

#### recall
0.8181818181818182

#### f1
0.7777777777777778

#### gepa_score
0.652838888888889

#### score_mode
row-aware

#### exact_match
0.34375

#### row_exact_accuracy
0.34375

#### avg_row_jaccard
0.6791666666666667

#### avg_row_symdiff
1.125

#### row_symdiff_score
0.47058823529411764

#### composite_score
0.6613888888888889

#### valid_json
1.0

#### cardinality_closeness
0.8961038961038961

#### avg_expected_topics
2.40625

#### avg_predicted_topics
2.65625

#### false_positives
22

#### false_negatives
14

#### policy_chars
5710

#### policy_char_budget
4000

#### policy_length_over_budget
1710

#### policy_length_penalty
0.00855

#### policy_length_compliance
0.9145

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
9

##### false_negatives
0

##### precision
0.526

##### recall
1.0

##### action
`reliability` over_predicted: expected in 10 rows, predicted in 19, TP=10, FP=9, FN=0, precision=0.526, recall=1.000. Precision is the bottleneck. a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface.

#### Item 2
##### topic
telemetry_usage

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
`telemetry_usage` under_predicted: expected in 3 rows, predicted in 0, TP=0, FP=0, FN=3, precision=0.000, recall=0.000. Recall is the bottleneck. MUST include when central: token counts, usage counts, costs, metrics, diagnostics, traces, or status reporting are central.

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
gateway

##### problem
mixed

##### false_positives
2

##### false_negatives
0

##### precision
0.333

##### recall
1.0

##### action
`gateway` mixed: expected in 1 rows, predicted in 3, TP=1, FP=2, FN=0, precision=0.333, recall=1.000. Both precision and recall need boundary work. Mixed `gateway` errors. ordinary provider proxy, HTTP compatibility, or app-runtime bugs unless the gateway is the owning boundary. MUST include when central: gateway routing, gateway state, gateway startup, gateway protocol, or gateway-owned execution is central.

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
telemetry_usage

##### predicted
reliability

##### count
3

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

###### Item 2
###### expected
###### Item 1
sessions

###### Item 2
telemetry_usage

###### Item 3
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
0.667

#### Item 2
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

#### Item 3
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

#### Item 4
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

#### Item 5
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

#### Item 6
##### expected
tests_ci

##### predicted
config

##### count
1

##### action
Clarify `tests_ci` vs `config`. For missed `tests_ci`: MUST include when central: only when tests, CI, or test infrastructure itself is the subject. For extra `config`: a config key that is merely the internal mechanism, example, or implementation detail of another surface's change. Boundary: operator-facing config options qualify on their own.

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
codex

###### Item 3
reliability

###### Item 4
security

##### false_positives
###### Item 1
reliability

##### false_negatives
###### Item 1
acpx

###### Item 2
auth_identity

##### row_score
0.6666666666666666

#### Item 8
##### id
openclaw-openclaw-71646

##### title
mcp/channel-bridge: pendingClaudePermissions / pendingApprovals leak — no TTL, no close-clear, no cap

##### expected
###### Item 1
approvals

###### Item 2
mcp_tooling

###### Item 3
reliability

##### actual
###### Item 1
mcp_tooling

###### Item 2
memory

###### Item 3
reliability

##### false_positives
###### Item 1
memory

##### false_negatives
###### Item 1
approvals

##### row_score
0.6666666666666666

### prompt_hygiene
#### ok
True

#### findings

#### policy_chars
5710

### reflection_hint
Make concise reusable routing rules. Do not copy the fixed allowed-topic taxonomy, do not add row-specific examples, and do not optimize for recall at the expense of F1.

## static_asi_path
eval/openclaw/easy-set-pilot/v6/vanilla-asi-v6-slim.md

## candidate_idx
2

## batch_summary
### model
gemma-e4

### input
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/input.jsonl

### output
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/candidate-0002/results.jsonl

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
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/candidate-0002/.results.jsonl.batch/20260611T211659Z-48d9c065

### started_at
2026-06-11T21:16:59Z

### completed_at
2026-06-11T21:17:35Z

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
33622.78

### timing_ms
#### duration
##### count
32

##### min
896.63

##### mean
4016.7775

##### median_approx
4090.16

##### max
5617.75

#### ttft
##### count
32

##### min
819.19

##### mean
2982.5725

##### median_approx
3089.25375

##### max
4743.86

#### time_to_response
##### count
32

##### min
819.19

##### mean
2982.5725

##### median_approx
3089.25375

##### max
4743.86

### usage
#### input_tokens
207936

#### output_tokens
253

#### total_tokens
208189

#### billing_tokens
208189

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
142080

#### served_tokens
142080

#### activity_tokens
142080

#### effective_input_tokens
65856

#### hit_rate_percent
68.32871652816252

#### write_rate_percent
0.0

#### activity_rate_percent
68.32871652816252

#### rows_with_cache_activity
32

#### row_cache_activity_percent
100.0

#### non_cached_input_tokens
65856

#### served_to_effective_input_ratio
2.1574344023323615

### shards
#### Item 1
##### index
0

##### offset
0

##### limit
8

##### output
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/candidate-0002/.results.jsonl.batch/20260611T211659Z-48d9c065/part-000.jsonl

#### Item 2
##### index
1

##### offset
8

##### limit
8

##### output
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/candidate-0002/.results.jsonl.batch/20260611T211659Z-48d9c065/part-001.jsonl

#### Item 3
##### index
2

##### offset
16

##### limit
8

##### output
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/candidate-0002/.results.jsonl.batch/20260611T211659Z-48d9c065/part-002.jsonl

#### Item 4
##### index
3

##### offset
24

##### limit
8

##### output
runs/easy-set-v6/gepa/gemma-e4-v6a-ledger32-plain-batch-mc30-r2/candidate-0002/.results.jsonl.batch/20260611T211659Z-48d9c065/part-003.jsonl

## lineage
### policy_sha256
36f554afdd34edbf790c0a2fb587ee0576f81fe9b342dd7073e3e04fad3faddc

### parent_candidate_idx
1

### reflection_call
call-0001


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