You are an expert optimization assistant. Your task is to analyze evaluation feedback and propose an improved version of a system component.

## Optimization Goal

Improve only the mutable OpenClaw vanilla labeler routing policy.

The fixed AgentCard header, JSON output contract, schema enum, GitHub context renderer,
and allowed-topic taxonomy are not editable.

Primary objective: maximize row-aware GEPA score = 0.50*topic_micro_f1 + 0.20*row_exact_accuracy + 0.30*avg_row_jaccard. Do not optimize for recall-biased F-beta. Use precision, recall, exact match,
row Jaccard, row symdiff, cardinality, topic confusions, row examples, and
prompt-hygiene ASI to understand how to improve reliable row-level reproduction.

Keep the policy vanilla and compact. Prefer short reusable centrality/cardinality rules
over a long topic-by-topic rulebook.

Keep the mutable policy under 12,000 characters; over-budget policies receive a small
GEPA score penalty, so compress rules instead of accumulating exhaustive topic tables.

Preserve concise JSON-only behavior.

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
concern under the fixed taxonomy and boundary overlay. Prefer owner surfaces
over incidental mechanisms, but add co-labels for explicit cross-surface
deliverables.

# Cardinality Rules

Include every topic whose inclusion rule in the fixed overlay is satisfied; do
not drop a qualifying topic to keep the output short. Use 1-3 topics by
default, 4-5 only when genuinely cross-cutting, never more than 5. Drop labels
that are only symptom locations, mechanisms, paths, examples, or consequences.
For bugs, add `reliability` only when failure handling, persistence, recovery,
cleanup, stuck/timeout/crash, data loss, or durable result loss is itself a
routed concern, not merely because behavior is incorrect.

# Boundary Overlays

- Add `reliability` for central terminal-state correctness, send/dispatch
  failures, dropped durable results, premature cleanup, retries, stuck/timeout/
  crash, data loss, recovery, leaks, caps, or lifecycle cleanup; suppress it
  for ranking/display preferences, wrong content/field mapping, invisible UI/API
  formatting, or ordinary product semantics inside one owner surface.
- If an item is explicitly ACPX-owned, prefer `acpx`; add `acp` when ACP
  protocol/session/binding/delivery, parent/child behavior, or ACP-node result
  semantics are also central. Do not add `reliability` for ACP/ACPX result-shape
  bugs unless recovery/loss/cleanup is the routed deliverable.
- Include `coding_agents` when user-visible spawned/child/subagent work,
  follow-up orchestration, handoff, parent orchestration, result announcement,
  give-up behavior, or lifecycle is central; do not replace it with `gateway` or
  `agent_runtime` unless those own the change.
- For chat surfaces, add `notifications` when outbound reply/send delivery,
  sent-message state, message expiration, completion/announcement delivery,
  delivery gates, payload/path changes, or failure recovery is central; chat
  adapter ingestion alone stays `chat_integrations`.
- Add `hooks` when hook emission/registration/filtering/payload/priority is a
  deliverable, including chat event hooks; do not route that to
  `skills_plugins` unless plugin loading/SDK is central. Sent-message hooks for
  outbound replies usually also involve `notifications`.
- Add `self_hosted_inference` for engine setup, preflight, lifecycle,
  compatibility, crashes/timeouts, retries, or backends even when the engine is
  local; if the issue is only provider API request/response behavior, use
  `inference_api` without it.
- Keep `gateway` for gateway-owned routes/state/startup/protocol/execution; do
  not use it for generic provider proxying, notifications, agent orchestration,
  or app-runtime failures.
- Use `tool_calling` only for model tool-call protocol, deltas, schemas,
  transcript/result routing, or rendering. Streaming prose, queue steering,
  chat send reconciliation, command output, screenshots, or generic boundaries
  are not enough.
- Documentation-only changes should include `docs` plus the documented owner
  surface(s), not every mechanism mentioned for context.
- `config` co-labels are warranted for operator-facing settings, defaults,
  persisted shape, validation, setup, or migration, even when another surface
  consumes the option.
- Add `approvals` for pending approval/permission state, prompts, decisions,
  modes, persistence, expiry, caps, or cleanup, including when surfaced through
  MCP; do not route such pending state to `memory`.
- Use `api_surface` only when an external CLI/HTTP/SDK/API contract changes what
  callers can rely on: shape, fields, status, compatibility, or documented
  command behavior. Provider inference integration details such as prompt hints,
  response parsing, streaming chunks, TTS/vision/embeddings request handling, or
  provider compatibility stay `inference_api` unless a public OpenClaw contract
  changes.

# Suppression Rules

- Do not infer topics from filenames, package names, or isolated keywords when
  the main deliverable names a different owner.
- Do not add reliability for harmless ordering, visibility, wording, sorting,
  formatting, or explanatory-data issues unless there is loss, failure, cleanup,
  recovery, leak/cap, or stuck behavior.
- Do not add `memory` for pending state, context windows, sessions, transcripts,
  leaks, or generic remembering; require memory indexing/search, embeddings,
  active memory, vector/provider state, or memory archival/recovery.
- Do not add `self_hosted_inference` just because a self-hosted engine is named
  in an API-compatibility issue.
- Do not add `tool_calling` for any mention of “tool” unless the model
  tool-call contract itself changes.
- Do not add `acp` beside `acpx` for ACPX-only state/transport/artifact work;
  do add it when generic ACP semantics are explicitly changed.
- Do not add `gateway` unless the gateway is the owning boundary.
- Return only the required concise JSON object; no prose, explanations, or
  extra fields.
```

## Evaluation Results

Performance data from evaluating the current component across test cases:

```
# Example 1
## Scores (Higher is Better)
### gepa_score
0.8681759983221478

### composite_score
0.8741809983221478

### topic_micro_f1
0.9261744966442953

### row_exact_accuracy
0.71875

### avg_row_jaccard
0.8911458333333335

### row_symdiff_score
0.7441860465116279

### policy_length_compliance
0.93995

### policy_hygiene_compliance
1.0

## score_details
### false_positives
3

### false_negatives
8

### row_exact_accuracy
0.71875

### avg_row_jaccard
0.8911458333333335

### avg_row_symdiff
0.34375

### avg_expected_topics
2.40625

### avg_predicted_topics
2.25

### asi_score
0.72

### topic_micro_precision
0.9583333333333334

### topic_micro_recall
0.8961038961038961

### exact_match
0.71875

### row_symdiff_score
0.7441860465116279

### composite_score
0.8741809983221478

### gepa_score
0.8681759983221478

### score_mode
row-aware

### valid_json
1.0

### cardinality_closeness
0.935064935064935

### avg_topic_count_delta
-0.15625

### policy_chars
5201

### policy_char_budget
4000

### policy_length_over_budget
1201

### policy_length_penalty
0.006005

### policy_length_compliance
0.93995

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
ui_tui

#### false_positives

#### false_negatives
##### Item 1
telemetry_usage

#### invalid_topics

#### keywords

#### row_score
0.6666666666666666

### Item 2
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

#### false_positives

#### false_negatives
##### Item 1
notifications

#### invalid_topics

#### keywords

#### row_score
0.8

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
acp

##### Item 2
acpx

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

### Item 4
#### id
openclaw-openclaw-46552

#### title
docs(queue): clarify steer behavior with partial streaming and tool boundaries

#### expected
##### Item 1
docs

##### Item 2
queueing

#### actual
##### Item 1
config

##### Item 2
docs

##### Item 3
queueing

#### false_positives
##### Item 1
config

#### false_negatives

#### invalid_topics

#### keywords

#### row_score
0.8

### Item 5
#### id
openclaw-openclaw-48851

#### title
feat(status): add API call count to session status and usage footer

#### expected
##### Item 1
sessions

##### Item 2
telemetry_usage

##### Item 3
ui_tui

#### actual
##### Item 1
api_surface

##### Item 2
sessions

##### Item 3
telemetry_usage

#### false_positives
##### Item 1
api_surface

#### false_negatives
##### Item 1
ui_tui

#### invalid_topics

#### keywords

#### row_score
0.6666666666666666

### Item 6
#### id
openclaw-openclaw-65187

#### title
test: add regression tests for <final> tag stripping in UI message extraction

#### expected
##### Item 1
tests_ci

##### Item 2
ui_tui

#### actual
##### Item 1
ui_tui

#### false_positives

#### false_negatives
##### Item 1
tests_ci

#### invalid_topics

#### keywords

#### row_score
0.6666666666666666

### Item 7
#### id
openclaw-openclaw-69256

#### title
fix(cron): prevent premature session cleanup when subagents are running

#### expected
##### Item 1
coding_agents

##### Item 2
cron_automation

##### Item 3
reliability

##### Item 4
sessions

#### actual
##### Item 1
cron_automation

##### Item 2
reliability

##### Item 3
sessions

#### false_positives

#### false_negatives
##### Item 1
coding_agents

#### invalid_topics

#### keywords

#### row_score
0.8571428571428571

### Item 8
#### id
openclaw-openclaw-69669

#### title
ACP: keep thread-bound follow-ups parent-orchestrated by default, not raw pass-through

#### expected
##### Item 1
acp

##### Item 2
coding_agents

##### Item 3
sessions

#### actual
##### Item 1
acp

##### Item 2
sessions

#### false_positives

#### false_negatives
##### Item 1
coding_agents

#### invalid_topics

#### keywords

#### row_score
0.8

### Item 9
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
acpx

##### Item 2
auth_identity

##### Item 3
codex

#### false_positives

#### false_negatives
##### Item 1
acp

##### Item 2
security

#### invalid_topics

#### keywords

#### row_score
0.75

## worst_failures
### Item 1
#### id
openclaw-openclaw-48851

#### title
feat(status): add API call count to session status and usage footer

#### expected
##### Item 1
sessions

##### Item 2
telemetry_usage

##### Item 3
ui_tui

#### actual
##### Item 1
api_surface

##### Item 2
sessions

##### Item 3
telemetry_usage

#### false_positives
##### Item 1
api_surface

#### false_negatives
##### Item 1
ui_tui

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
ui_tui

#### false_positives

#### false_negatives
##### Item 1
telemetry_usage

#### invalid_topics

#### keywords

#### row_score
0.6666666666666666

### Item 3
#### id
openclaw-openclaw-65187

#### title
test: add regression tests for <final> tag stripping in UI message extraction

#### expected
##### Item 1
tests_ci

##### Item 2
ui_tui

#### actual
##### Item 1
ui_tui

#### false_positives

#### false_negatives
##### Item 1
tests_ci

#### invalid_topics

#### keywords

#### row_score
0.6666666666666666

### Item 4
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
acpx

##### Item 2
auth_identity

##### Item 3
codex

#### false_positives

#### false_negatives
##### Item 1
acp

##### Item 2
security

#### invalid_topics

#### keywords

#### row_score
0.75

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

#### false_positives

#### false_negatives
##### Item 1
notifications

#### invalid_topics

#### keywords

#### row_score
0.8

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
acp

##### Item 2
acpx

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

### Item 7
#### id
openclaw-openclaw-46552

#### title
docs(queue): clarify steer behavior with partial streaming and tool boundaries

#### expected
##### Item 1
docs

##### Item 2
queueing

#### actual
##### Item 1
config

##### Item 2
docs

##### Item 3
queueing

#### false_positives
##### Item 1
config

#### false_negatives

#### invalid_topics

#### keywords

#### row_score
0.8

### Item 8
#### id
openclaw-openclaw-69669

#### title
ACP: keep thread-bound follow-ups parent-orchestrated by default, not raw pass-through

#### expected
##### Item 1
acp

##### Item 2
coding_agents

##### Item 3
sessions

#### actual
##### Item 1
acp

##### Item 2
sessions

#### false_positives

#### false_negatives
##### Item 1
coding_agents

#### invalid_topics

#### keywords

#### row_score
0.8

## topic_error_patterns
### Item 1
#### topic
coding_agents

#### problem
mixed

#### expected
3

#### actual
1

#### true_positives
1

#### false_positives
0

#### false_negatives
2

#### precision
1.0

#### recall
0.333

#### f1
0.5

#### action
`coding_agents` mixed: expected in 3 rows, predicted in 1, TP=1, FP=0, FN=2, precision=1.000, recall=0.333. Both precision and recall need boundary work. Mixed `coding_agents` errors. internal OpenClaw subagents, `sessions_spawn` plumbing, ACP parent/child behavior, queue lanes, trace producers, tool-use mechanics, approval flows, sandboxing, compaction, or agent runtime machinery unless the item is specifically about a coding-agent integration. Boundary: ACP is an integration protocol and is distinct from coding-agent integrations; route ACP protocol/session/delivery work to `acp`/`acpx`. OpenClaw's internal agent runtime is a core product surface; route startup, loop, backend, model-call orchestration, and adapter machinery to `agent_runtime`. MUST include when central: integrations with external coding agents in general, or with a specific coding agent such as Codex, Claude Code, Gemini CLI, or Pi. Boundary: ACP is an integration protocol and is distinct from coding-agent integrations; route ACP protocol/session/delivery work to `acp`/`acpx`. OpenClaw's internal agent runtime is a core product surface; route startup, loop, backend, model-call orchestration, and adapter machinery to `agent_runtime`.

#### examples
##### Item 1
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
sessions

###### keywords

###### error_type
false_negative

#### true_positive_examples
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
coding_agents

###### Item 2
notifications

###### Item 3
reliability

###### keywords

###### row_score
1.0

#### false_positive_examples

#### false_negative_examples
##### Item 1
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
sessions

###### keywords

###### row_score
0.8

### Item 2
#### topic
reliability

#### problem
mixed

#### expected
10

#### actual
11

#### true_positives
10

#### false_positives
1

#### false_negatives
0

#### precision
0.909

#### recall
1.0

#### f1
0.952

#### action
`reliability` mixed: expected in 10 rows, predicted in 11, TP=10, FP=1, FN=0, precision=0.909, recall=1.000. Both precision and recall need boundary work. Mixed `reliability` errors. a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface. MUST include when central: timeout, crash, leak, stuck state, retry, data loss, lifecycle cleanup, recovery, overload, or operational failure mode.

#### examples
##### Item 1
###### expected
###### Item 1
acp

###### Item 2
acpx

###### actual
###### Item 1
acp

###### Item 2
acpx

###### Item 3
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

###### keywords

###### row_score
1.0

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
reliability

###### keywords

###### row_score
1.0

#### false_positive_examples
##### Item 1
###### expected
###### Item 1
acp

###### Item 2
acpx

###### actual
###### Item 1
acp

###### Item 2
acpx

###### Item 3
reliability

###### keywords

###### row_score
0.8

#### false_negative_examples

### Item 3
#### topic
ui_tui

#### problem
mixed

#### expected
7

#### actual
6

#### true_positives
6

#### false_positives
0

#### false_negatives
1

#### precision
1.0

#### recall
0.857

#### f1
0.923

#### action
`ui_tui` mixed: expected in 7 rows, predicted in 6, TP=6, FP=0, FN=1, precision=1.000, recall=0.857. Both precision and recall need boundary work. Mixed `ui_tui` errors. command internals, telemetry fields, or API behavior not shown to users. MUST include when central: UI/TUI display, status, footer, mobile UI, or visual interaction is central.

#### examples
##### Item 1
###### expected
###### Item 1
sessions

###### Item 2
telemetry_usage

###### Item 3
ui_tui

###### actual
###### Item 1
api_surface

###### Item 2
sessions

###### Item 3
telemetry_usage

###### keywords

###### error_type
false_negative

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
ui_tui

###### keywords

###### row_score
1.0

##### Item 3
###### expected
###### Item 1
telemetry_usage

###### Item 2
ui_tui

###### actual
###### Item 1
ui_tui

###### keywords

###### row_score
0.667

#### false_positive_examples

#### false_negative_examples
##### Item 1
###### expected
###### Item 1
sessions

###### Item 2
telemetry_usage

###### Item 3
ui_tui

###### actual
###### Item 1
api_surface

###### Item 2
sessions

###### Item 3
telemetry_usage

###### keywords

###### row_score
0.667

### Item 4
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
docs

###### Item 2
queueing

###### actual
###### Item 1
config

###### Item 2
docs

###### Item 3
queueing

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

###### keywords

###### row_score
1.0

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

###### keywords

###### row_score
0.8

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

###### Item 4
self_hosted_inference

###### keywords

###### row_score
1.0

#### false_positive_examples
##### Item 1
###### expected
###### Item 1
docs

###### Item 2
queueing

###### actual
###### Item 1
config

###### Item 2
docs

###### Item 3
queueing

###### keywords

###### row_score
0.8

#### false_negative_examples

### Item 5
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

###### Item 3
auth_identity

###### Item 4
codex

###### Item 5
security

###### actual
###### Item 1
acpx

###### Item 2
auth_identity

###### Item 3
codex

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
acpx

###### actual
###### Item 1
acp

###### Item 2
acpx

###### Item 3
reliability

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
queueing

###### Item 4
reliability

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

###### Item 3
auth_identity

###### Item 4
codex

###### Item 5
security

###### actual
###### Item 1
acpx

###### Item 2
auth_identity

###### Item 3
codex

###### keywords

###### row_score
0.75

### Item 6
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
config

###### Item 3
notifications

###### actual
###### Item 1
chat_integrations

###### Item 2
config

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
chat_integrations

###### Item 2
notifications

###### actual
###### Item 1
chat_integrations

###### Item 2
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

###### Item 3
reliability

###### actual
###### Item 1
chat_integrations

###### Item 2
notifications

###### Item 3
reliability

###### keywords

###### row_score
1.0

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

###### keywords

###### row_score
0.8

### Item 7
#### topic
telemetry_usage

#### problem
mixed

#### expected
3

#### actual
2

#### true_positives
2

#### false_positives
0

#### false_negatives
1

#### precision
1.0

#### recall
0.667

#### f1
0.8

#### action
`telemetry_usage` mixed: expected in 3 rows, predicted in 2, TP=2, FP=0, FN=1, precision=1.000, recall=0.667. Both precision and recall need boundary work. Mixed `telemetry_usage` errors. generic reliability or UI text without measurement/status data. MUST include when central: token counts, usage counts, costs, metrics, diagnostics, traces, or status reporting are central.

#### examples
##### Item 1
###### expected
###### Item 1
telemetry_usage

###### Item 2
ui_tui

###### actual
###### Item 1
ui_tui

###### keywords

###### error_type
false_negative

#### true_positive_examples
##### Item 1
###### expected
###### Item 1
sessions

###### Item 2
telemetry_usage

###### Item 3
ui_tui

###### actual
###### Item 1
api_surface

###### Item 2
sessions

###### Item 3
telemetry_usage

###### keywords

###### row_score
0.667

##### Item 2
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
telemetry_usage

###### keywords

###### row_score
1.0

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
ui_tui

###### keywords

###### row_score
0.667

### Item 8
#### topic
tests_ci

#### problem
mixed

#### expected
2

#### actual
1

#### true_positives
1

#### false_positives
0

#### false_negatives
1

#### precision
1.0

#### recall
0.5

#### f1
0.667

#### action
`tests_ci` mixed: expected in 2 rows, predicted in 1, TP=1, FP=0, FN=1, precision=1.000, recall=0.500. Both precision and recall need boundary work. Mixed `tests_ci` errors. a PR merely including tests alongside a change. MUST include when central: only when tests, CI, or test infrastructure itself is the subject.

#### examples
##### Item 1
###### expected
###### Item 1
tests_ci

###### Item 2
ui_tui

###### actual
###### Item 1
ui_tui

###### keywords

###### error_type
false_negative

#### true_positive_examples
##### Item 1
###### expected
###### Item 1
packaging_deployment

###### Item 2
tests_ci

###### actual
###### Item 1
packaging_deployment

###### Item 2
tests_ci

###### keywords

###### row_score
1.0

#### false_positive_examples

#### false_negative_examples
##### Item 1
###### expected
###### Item 1
tests_ci

###### Item 2
ui_tui

###### actual
###### Item 1
ui_tui

###### keywords

###### row_score
0.667

## confusions
### Item 1
#### expected
ui_tui

#### predicted
api_surface

#### count
1

#### action
Clarify `ui_tui` vs `api_surface`. For missed `ui_tui`: MUST include when central: UI/TUI display, status, footer, mobile UI, or visual interaction is central. For extra `api_surface`: internal helpers, payload parsing, status text, UI events, ordinary commands, inference-integration behavior (`inference_api`), or gateway process ownership (`gateway`). Decision rule: if the item changes WHAT an external contract promises (shape, fields, status, compatibility), api_surface applies even when the implementation lives in the gateway or a serving endpoint; `docs` only when the contract text itself is the subject.

#### examples
##### Item 1
###### expected
###### Item 1
sessions

###### Item 2
telemetry_usage

###### Item 3
ui_tui

###### actual
###### Item 1
api_surface

###### Item 2
sessions

###### Item 3
telemetry_usage

###### keywords

###### row_score
0.667

## invalid_topics

## actionable_feedback
### Item 1
Pure-F1 objective: optimize exact topic membership, not recall-biased F-beta. Current precision=0.958, recall=0.896, F1=0.926.

### Item 2
Cardinality diagnosis: under_labeling; avg predicted 2.25 vs expected 2.41. Add central co-labels when multiple maintainer interests are explicit; avoid single-label collapse.

### Item 3
Policy length penalty: policy is 1201 chars over the 4000 char budget; GEPA score was reduced by 0.0060.

### Item 4
Topic cardinality is close: avg predicted topics 2.25 vs expected 2.41. Focus on boundary-specific errors.

### Item 5
`coding_agents` mixed: expected in 3 rows, predicted in 1, TP=1, FP=0, FN=2, precision=1.000, recall=0.333. Both precision and recall need boundary work. Mixed `coding_agents` errors. internal OpenClaw subagents, `sessions_spawn` plumbing, ACP parent/child behavior, queue lanes, trace producers, tool-use mechanics, approval flows, sandboxing, compaction, or agent runtime machinery unless the item is specifically about a coding-agent integration. Boundary: ACP is an integration protocol and is distinct from coding-agent integrations; route ACP protocol/session/delivery work to `acp`/`acpx`. OpenClaw's internal agent runtime is a core product surface; route startup, loop, backend, model-call orchestration, and adapter machinery to `agent_runtime`. MUST include when central: integrations with external coding agents in general, or with a specific coding agent such as Codex, Claude Code, Gemini CLI, or Pi. Boundary: ACP is an integration protocol and is distinct from coding-agent integrations; route ACP protocol/session/delivery work to `acp`/`acpx`. OpenClaw's internal agent runtime is a core product surface; route startup, loop, backend, model-call orchestration, and adapter machinery to `agent_runtime`.

### Item 6
`reliability` mixed: expected in 10 rows, predicted in 11, TP=10, FP=1, FN=0, precision=0.909, recall=1.000. Both precision and recall need boundary work. Mixed `reliability` errors. a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface. MUST include when central: timeout, crash, leak, stuck state, retry, data loss, lifecycle cleanup, recovery, overload, or operational failure mode.

### Item 7
`ui_tui` mixed: expected in 7 rows, predicted in 6, TP=6, FP=0, FN=1, precision=1.000, recall=0.857. Both precision and recall need boundary work. Mixed `ui_tui` errors. command internals, telemetry fields, or API behavior not shown to users. MUST include when central: UI/TUI display, status, footer, mobile UI, or visual interaction is central.

### Item 8
`config` mixed: expected in 5 rows, predicted in 6, TP=5, FP=1, FN=0, precision=0.833, recall=1.000. Both precision and recall need boundary work. Mixed `config` errors. a config key that is merely the internal mechanism, example, or implementation detail of another surface's change. Boundary: operator-facing config options qualify on their own. MUST include when central: configuration schemas, persisted config shape, config loading, config validation, config repair, environment/config defaults, operator-facing config options, allow/deny configuration, or policy settings. Boundary: operator-facing config options qualify on their own.

### Item 9
`acp` mixed: expected in 6 rows, predicted in 5, TP=5, FP=0, FN=1, precision=1.000, recall=0.833. Both precision and recall need boundary work. Mixed `acp` errors. merely because an item mentions an agent session or internal runtime behavior. MUST include when central: ACP runtime/protocol, ACP session, ACP binding, ACP parent/child behavior, or ACP delivery is central.

### Item 10
`notifications` mixed: expected in 5 rows, predicted in 4, TP=4, FP=0, FN=1, precision=1.000, recall=0.800. Both precision and recall need boundary work. Mixed `notifications` errors. chat-platform-specific behavior alone (`chat_integrations`) or reliability-only recovery. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label. MUST include when central: generic outbound notifications, completion delivery, message delivery gates, announcements, or notify behavior is central. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label.

## vanilla_f1_asi
### global_diagnosis
#### precision
0.9583333333333334

#### recall
0.8961038961038961

#### f1
0.9261744966442953

#### gepa_score
0.8681759983221478

#### score_mode
row-aware

#### exact_match
0.71875

#### row_exact_accuracy
0.71875

#### avg_row_jaccard
0.8911458333333335

#### avg_row_symdiff
0.34375

#### row_symdiff_score
0.7441860465116279

#### composite_score
0.8741809983221478

#### valid_json
1.0

#### cardinality_closeness
0.935064935064935

#### avg_expected_topics
2.40625

#### avg_predicted_topics
2.25

#### false_positives
3

#### false_negatives
8

#### policy_chars
5201

#### policy_char_budget
4000

#### policy_length_over_budget
1201

#### policy_length_penalty
0.006005

#### policy_length_compliance
0.93995

#### diagnosis
under_labeling

#### action
Add central co-labels when multiple maintainer interests are explicit; avoid single-label collapse.

### topic_priorities
#### Item 1
##### topic
coding_agents

##### problem
mixed

##### false_positives
0

##### false_negatives
2

##### precision
1.0

##### recall
0.333

##### action
`coding_agents` mixed: expected in 3 rows, predicted in 1, TP=1, FP=0, FN=2, precision=1.000, recall=0.333. Both precision and recall need boundary work. Mixed `coding_agents` errors. internal OpenClaw subagents, `sessions_spawn` plumbing, ACP parent/child behavior, queue lanes, trace producers, tool-use mechanics, approval flows, sandboxing, compaction, or agent runtime machinery unless the item is specifically about a coding-agent integration. Boundary: ACP is an integration protocol and is distinct from coding-agent integrations; route ACP protocol/session/delivery work to `acp`/`acpx`. OpenClaw's internal agent runtime is a core product surface; route startup, loop, backend, model-call orchestration, and adapter machinery to `agent_runtime`. MUST include when central: integrations with external coding agents in general, or with a specific coding agent such as Codex, Claude Code, Gemini CLI, or Pi. Boundary: ACP is an integration protocol and is distinct from coding-agent integrations; route ACP protocol/session/delivery work to `acp`/`acpx`. OpenClaw's internal agent runtime is a core product surface; route startup, loop, backend, model-call orchestration, and adapter machinery to `agent_runtime`.

#### Item 2
##### topic
reliability

##### problem
mixed

##### false_positives
1

##### false_negatives
0

##### precision
0.909

##### recall
1.0

##### action
`reliability` mixed: expected in 10 rows, predicted in 11, TP=10, FP=1, FN=0, precision=0.909, recall=1.000. Both precision and recall need boundary work. Mixed `reliability` errors. a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface. MUST include when central: timeout, crash, leak, stuck state, retry, data loss, lifecycle cleanup, recovery, overload, or operational failure mode.

#### Item 3
##### topic
ui_tui

##### problem
mixed

##### false_positives
0

##### false_negatives
1

##### precision
1.0

##### recall
0.857

##### action
`ui_tui` mixed: expected in 7 rows, predicted in 6, TP=6, FP=0, FN=1, precision=1.000, recall=0.857. Both precision and recall need boundary work. Mixed `ui_tui` errors. command internals, telemetry fields, or API behavior not shown to users. MUST include when central: UI/TUI display, status, footer, mobile UI, or visual interaction is central.

#### Item 4
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

#### Item 5
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

#### Item 6
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

#### Item 7
##### topic
telemetry_usage

##### problem
mixed

##### false_positives
0

##### false_negatives
1

##### precision
1.0

##### recall
0.667

##### action
`telemetry_usage` mixed: expected in 3 rows, predicted in 2, TP=2, FP=0, FN=1, precision=1.000, recall=0.667. Both precision and recall need boundary work. Mixed `telemetry_usage` errors. generic reliability or UI text without measurement/status data. MUST include when central: token counts, usage counts, costs, metrics, diagnostics, traces, or status reporting are central.

#### Item 8
##### topic
tests_ci

##### problem
mixed

##### false_positives
0

##### false_negatives
1

##### precision
1.0

##### recall
0.5

##### action
`tests_ci` mixed: expected in 2 rows, predicted in 1, TP=1, FP=0, FN=1, precision=1.000, recall=0.500. Both precision and recall need boundary work. Mixed `tests_ci` errors. a PR merely including tests alongside a change. MUST include when central: only when tests, CI, or test infrastructure itself is the subject.

### confusions
#### Item 1
##### expected
ui_tui

##### predicted
api_surface

##### count
1

##### action
Clarify `ui_tui` vs `api_surface`. For missed `ui_tui`: MUST include when central: UI/TUI display, status, footer, mobile UI, or visual interaction is central. For extra `api_surface`: internal helpers, payload parsing, status text, UI events, ordinary commands, inference-integration behavior (`inference_api`), or gateway process ownership (`gateway`). Decision rule: if the item changes WHAT an external contract promises (shape, fields, status, compatibility), api_surface applies even when the implementation lives in the gateway or a serving endpoint; `docs` only when the contract text itself is the subject.

##### examples
###### Item 1
###### expected
###### Item 1
sessions

###### Item 2
telemetry_usage

###### Item 3
ui_tui

###### actual
###### Item 1
api_surface

###### Item 2
sessions

###### Item 3
telemetry_usage

###### keywords

###### row_score
0.667

### row_examples
#### Item 1
##### id
openclaw-openclaw-48851

##### title
feat(status): add API call count to session status and usage footer

##### expected
###### Item 1
sessions

###### Item 2
telemetry_usage

###### Item 3
ui_tui

##### actual
###### Item 1
api_surface

###### Item 2
sessions

###### Item 3
telemetry_usage

##### false_positives
###### Item 1
api_surface

##### false_negatives
###### Item 1
ui_tui

##### row_score
0.6666666666666666

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
ui_tui

##### false_positives

##### false_negatives
###### Item 1
telemetry_usage

##### row_score
0.6666666666666666

#### Item 3
##### id
openclaw-openclaw-65187

##### title
test: add regression tests for <final> tag stripping in UI message extraction

##### expected
###### Item 1
tests_ci

###### Item 2
ui_tui

##### actual
###### Item 1
ui_tui

##### false_positives

##### false_negatives
###### Item 1
tests_ci

##### row_score
0.6666666666666666

#### Item 4
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
acpx

###### Item 2
auth_identity

###### Item 3
codex

##### false_positives

##### false_negatives
###### Item 1
acp

###### Item 2
security

##### row_score
0.75

#### Item 5
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

##### false_positives

##### false_negatives
###### Item 1
notifications

##### row_score
0.8

#### Item 6
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
acp

###### Item 2
acpx

###### Item 3
reliability

##### false_positives
###### Item 1
reliability

##### false_negatives

##### row_score
0.8

#### Item 7
##### id
openclaw-openclaw-46552

##### title
docs(queue): clarify steer behavior with partial streaming and tool boundaries

##### expected
###### Item 1
docs

###### Item 2
queueing

##### actual
###### Item 1
config

###### Item 2
docs

###### Item 3
queueing

##### false_positives
###### Item 1
config

##### false_negatives

##### row_score
0.8

#### Item 8
##### id
openclaw-openclaw-69669

##### title
ACP: keep thread-bound follow-ups parent-orchestrated by default, not raw pass-through

##### expected
###### Item 1
acp

###### Item 2
coding_agents

###### Item 3
sessions

##### actual
###### Item 1
acp

###### Item 2
sessions

##### false_positives

##### false_negatives
###### Item 1
coding_agents

##### row_score
0.8

### prompt_hygiene
#### ok
True

#### findings

#### policy_chars
5201

### reflection_hint
Make concise reusable routing rules. Do not copy the fixed allowed-topic taxonomy, do not add row-specific examples, and do not optimize for recall at the expense of F1.

## static_asi_path
eval/openclaw/easy-set-pilot/v6/vanilla-asi-v6-slim.md

## candidate_idx
3

## batch_summary
### model
codexresponses.gpt-5.4-mini

### input
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/input.jsonl

### output
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/candidate-0003/results.jsonl

### schema
/home/ssmith/temp/gepa-batch-openclaw/eval/openclaw/output.schema.json

### schema_model
None

### instruction
None

### agent_card
eval/openclaw/easy-set-pilot/v6/openclaw-vanilla-labeler-v6a.md

### agent
openclaw_vanilla_labeler

### template
/home/ssmith/temp/gepa-batch-openclaw/eval/openclaw/task-template.md

### shell_runtime
False

### output_mode
structured

### export_traces
None

### hf_dataset
None

### hf_dataset_path
None

### parallel
4

### work_dir
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/candidate-0003/.results.jsonl.batch/20260611T210841Z-7cc1cc1a

### started_at
2026-06-11T21:08:41Z

### completed_at
2026-06-11T21:09:47Z

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
61153.62

### timing_ms
#### duration
##### count
32

##### min
3183.17

##### mean
6371.069375

##### median_approx
5585.715

##### max
15225.05

#### ttft
##### count
32

##### min
1922.48

##### mean
3856.535625

##### median_approx
3420.20375

##### max
6539.94

#### time_to_response
##### count
32

##### min
2680.75

##### mean
5999.59

##### median_approx
5351.27125

##### max
15014.12

### usage
#### input_tokens
194114

#### output_tokens
14009

#### total_tokens
208123

#### billing_tokens
208123

#### reasoning_tokens
11450

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
106496

#### served_tokens
106496

#### activity_tokens
106496

#### effective_input_tokens
87618

#### hit_rate_percent
54.86260650957685

#### write_rate_percent
0.0

#### activity_rate_percent
54.86260650957685

#### rows_with_cache_activity
28

#### row_cache_activity_percent
87.5

#### non_cached_input_tokens
87618

#### served_to_effective_input_ratio
1.215458010911

### shards
#### Item 1
##### index
0

##### offset
0

##### limit
8

##### output
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/candidate-0003/.results.jsonl.batch/20260611T210841Z-7cc1cc1a/part-000.jsonl

#### Item 2
##### index
1

##### offset
8

##### limit
8

##### output
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/candidate-0003/.results.jsonl.batch/20260611T210841Z-7cc1cc1a/part-001.jsonl

#### Item 3
##### index
2

##### offset
16

##### limit
8

##### output
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/candidate-0003/.results.jsonl.batch/20260611T210841Z-7cc1cc1a/part-002.jsonl

#### Item 4
##### index
3

##### offset
24

##### limit
8

##### output
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/candidate-0003/.results.jsonl.batch/20260611T210841Z-7cc1cc1a/part-003.jsonl

## lineage
### policy_sha256
dc10e1f1aa61a7e3ef9c34273aee66409acd9b879395c6487b94d13899b98fad

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