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
For bugs, add `reliability` only when the failure mode itself is a routed
concern, not merely because something is incorrect.

# Boundary Overlays

- Add `reliability` for central terminal-state correctness, send/dispatch
  failures, dropped results, premature cleanup, retries, stuck/timeout/crash,
  data loss, recovery, or lifecycle cleanup; suppress it for ranking/display
  preferences or ordinary product semantics inside one surface.
- If an item is explicitly ACPX-owned, prefer `acpx`; add `acp` only when
  generic ACP protocol/session/delivery behavior is also a central deliverable.
- Include `coding_agents` when user-visible spawned/child/subagent work,
  follow-up orchestration, handoff, result announcement, or lifecycle is central;
  do not replace it with `gateway` or `agent_runtime` unless those own the
  change.
- For chat surfaces, add `notifications` when outbound reply delivery,
  sent-message state, completion/announcement delivery, delivery gates, expiry,
  or failure recovery is central; chat adapter work alone stays
  `chat_integrations`.
- Add `hooks` when hook emission/registration/filtering/payload/priority is a
  deliverable, including chat event hooks; do not route that to
  `skills_plugins` unless plugin loading/SDK is central.
- Add `self_hosted_inference` for engine setup, preflight, lifecycle,
  compatibility, crashes/timeouts, or backends even when the engine is local;
  if the issue is only provider API request/response behavior, use
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

# Suppression Rules

- Do not infer topics from filenames, package names, or isolated keywords when
  the main deliverable names a different owner.
- Do not add reliability for harmless ordering, visibility, wording, sorting, or
  explanatory-data issues unless there is loss, failure, cleanup, recovery, or
  stuck behavior.
- Do not add `self_hosted_inference` just because a self-hosted engine is named
  in an API-compatibility issue.
- Do not add `tool_calling` for any mention of “tool” unless the model
  tool-call contract itself changes.
- Do not add `acp` beside `acpx` for ACPX-specific state/transport/artifact
  work unless non-ACPX ACP behavior is explicitly changed.
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
0.8460161423841059

### composite_score
0.8460161423841059

### topic_micro_f1
0.9139072847682119

### row_exact_accuracy
0.65625

### avg_row_jaccard
0.8593750000000001

### row_symdiff_score
0.7111111111111111

### policy_length_compliance
1.0

### policy_hygiene_compliance
1.0

## score_details
### false_positives
5

### false_negatives
8

### row_exact_accuracy
0.65625

### avg_row_jaccard
0.8593750000000001

### avg_row_symdiff
0.40625

### avg_expected_topics
2.40625

### avg_predicted_topics
2.3125

### asi_score
0.84

### topic_micro_precision
0.9324324324324325

### topic_micro_recall
0.8961038961038961

### exact_match
0.65625

### row_symdiff_score
0.7111111111111111

### composite_score
0.8460161423841059

### gepa_score
0.8460161423841059

### score_mode
row-aware

### valid_json
1.0

### cardinality_closeness
0.961038961038961

### avg_topic_count_delta
-0.09375

### policy_chars
3837

### policy_char_budget
4000

### policy_length_over_budget
0

### policy_length_penalty
0.0

### policy_length_compliance
1.0

### hygiene_penalty
0.0

### hygiene_findings_count
0

## evaluated
32

## failures
### Item 1
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

### Item 2
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

### Item 3
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

### Item 4
#### id
openclaw-openclaw-72138

#### title
fix(feishu): emit sent hooks for normal replies

#### expected
##### Item 1
chat_integrations

##### Item 2
hooks

##### Item 3
notifications

#### actual
##### Item 1
chat_integrations

##### Item 2
hooks

#### false_positives

#### false_negatives
##### Item 1
notifications

#### invalid_topics

#### keywords

#### row_score
0.8

### Item 5
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

### Item 6
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

### Item 7
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
notifications

##### Item 2
reliability

#### false_positives

#### false_negatives
##### Item 1
coding_agents

#### invalid_topics

#### keywords

#### row_score
0.8

### Item 8
#### id
openclaw-openclaw-67539

#### title
[Feature]: Add provider-specific TTS prompt hints

#### expected
##### Item 1
inference_api

#### actual
##### Item 1
api_surface

##### Item 2
inference_api

#### false_positives
##### Item 1
api_surface

#### false_negatives

#### invalid_topics

#### keywords

#### row_score
0.6666666666666666

### Item 9
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

### Item 10
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

### Item 11
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

#### false_positives
##### Item 1
reliability

#### false_negatives

#### invalid_topics

#### keywords

#### row_score
0.6666666666666666

## worst_failures
### Item 1
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

### Item 2
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

### Item 3
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
api_surface

##### Item 2
inference_api

#### false_positives
##### Item 1
api_surface

#### false_negatives

#### invalid_topics

#### keywords

#### row_score
0.6666666666666666

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

### Item 7
#### id
openclaw-openclaw-72138

#### title
fix(feishu): emit sent hooks for normal replies

#### expected
##### Item 1
chat_integrations

##### Item 2
hooks

##### Item 3
notifications

#### actual
##### Item 1
chat_integrations

##### Item 2
hooks

#### false_positives

#### false_negatives
##### Item 1
notifications

#### invalid_topics

#### keywords

#### row_score
0.8

### Item 8
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
notifications

##### Item 2
reliability

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
reliability

#### problem
over_predicted

#### expected
10

#### actual
13

#### true_positives
10

#### false_positives
3

#### false_negatives
0

#### precision
0.769

#### recall
1.0

#### f1
0.87

#### action
`reliability` over_predicted: expected in 10 rows, predicted in 13, TP=10, FP=3, FN=0, precision=0.769, recall=1.000. Precision is the bottleneck. a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface.

#### examples
##### Item 1
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

##### Item 2
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

##### Item 3
###### expected
###### Item 1
inference_api

###### actual
###### Item 1
inference_api

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
memory

###### actual
###### Item 1
memory

###### Item 2
reliability

###### keywords

###### row_score
0.667

##### Item 2
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

##### Item 3
###### expected
###### Item 1
inference_api

###### actual
###### Item 1
inference_api

###### Item 2
reliability

###### keywords

###### row_score
0.667

#### false_negative_examples

### Item 2
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
notifications

###### Item 2
reliability

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
notifications

###### Item 2
reliability

###### keywords

###### row_score
0.8

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
sessions

###### keywords

###### row_score
0.8

### Item 3
#### topic
notifications

#### problem
mixed

#### expected
5

#### actual
3

#### true_positives
3

#### false_positives
0

#### false_negatives
2

#### precision
1.0

#### recall
0.6

#### f1
0.75

#### action
`notifications` mixed: expected in 5 rows, predicted in 3, TP=3, FP=0, FN=2, precision=1.000, recall=0.600. Both precision and recall need boundary work. Mixed `notifications` errors. chat-platform-specific behavior alone (`chat_integrations`) or reliability-only recovery. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label. MUST include when central: generic outbound notifications, completion delivery, message delivery gates, announcements, or notify behavior is central. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label.

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

###### keywords

###### error_type
false_negative

#### true_positive_examples
##### Item 1
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

##### Item 2
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

##### Item 3
###### expected
###### Item 1
coding_agents

###### Item 2
notifications

###### Item 3
reliability

###### actual
###### Item 1
notifications

###### Item 2
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

###### keywords

###### row_score
0.8

### Item 4
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
queueing

###### Item 4
reliability

###### keywords

###### row_score
1.0

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

### Item 5
#### topic
memory

#### problem
mixed

#### expected
1

#### actual
2

#### true_positives
1

#### false_positives
1

#### false_negatives
0

#### precision
0.5

#### recall
1.0

#### f1
0.667

#### action
`memory` mixed: expected in 1 rows, predicted in 2, TP=1, FP=1, FN=0, precision=0.500, recall=1.000. Both precision and recall need boundary work. Mixed `memory` errors. context window, session state, transcript, or generic remembering. MUST include when central: memory indexing, memory search, embeddings, active memory, or memory provider state is central.

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

###### error_type
false_positive

#### true_positive_examples
##### Item 1
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

#### false_positive_examples
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

#### false_negative_examples

### Item 6
#### topic
api_surface

#### problem
mixed

#### expected
1

#### actual
2

#### true_positives
1

#### false_positives
1

#### false_negatives
0

#### precision
0.5

#### recall
1.0

#### f1
0.667

#### action
`api_surface` mixed: expected in 1 rows, predicted in 2, TP=1, FP=1, FN=0, precision=0.500, recall=1.000. Both precision and recall need boundary work. Mixed `api_surface` errors. internal helpers, payload parsing, status text, UI events, ordinary commands, inference-integration behavior (`inference_api`), or gateway process ownership (`gateway`). Decision rule: if the item changes WHAT an external contract promises (shape, fields, status, compatibility), api_surface applies even when the implementation lives in the gateway or a serving endpoint; `docs` only when the contract text itself is the subject. MUST include when central: external API, CLI, HTTP, SDK, or documented command contracts. Decision rule: if the item changes WHAT an external contract promises (shape, fields, status, compatibility), api_surface applies even when the implementation lives in the gateway or a serving endpoint; `docs` only when the contract text itself is the subject.

#### examples
##### Item 1
###### expected
###### Item 1
inference_api

###### actual
###### Item 1
api_surface

###### Item 2
inference_api

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
telemetry_usage

###### keywords

###### row_score
1.0

#### false_positive_examples
##### Item 1
###### expected
###### Item 1
inference_api

###### actual
###### Item 1
api_surface

###### Item 2
inference_api

###### keywords

###### row_score
0.667

#### false_negative_examples

### Item 7
#### topic
approvals

#### problem
mixed

#### expected
1

#### actual
0

#### true_positives
0

#### false_positives
0

#### false_negatives
1

#### precision
0.0

#### recall
0.0

#### f1
0.0

#### action
`approvals` mixed: expected in 1 rows, predicted in 0, TP=0, FP=0, FN=1, precision=0.000, recall=0.000. Both precision and recall need boundary work. Mixed `approvals` errors. merely because a command or tool might require permission. Co-label: bounding/expiring/persisting pending-approval state is approvals surface even when motivated by a memory/reliability fix. MUST include when central: approval prompts, permission decisions, or approval mode behavior is central. Co-label: bounding/expiring/persisting pending-approval state is approvals surface even when motivated by a memory/reliability fix.

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

###### error_type
false_negative

#### true_positive_examples

#### false_positive_examples

#### false_negative_examples
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

### Item 8
#### topic
self_hosted_inference

#### problem
mixed

#### expected
1

#### actual
0

#### true_positives
0

#### false_positives
0

#### false_negatives
1

#### precision
0.0

#### recall
0.0

#### f1
0.0

#### action
`self_hosted_inference` mixed: expected in 1 rows, predicted in 0, TP=0, FP=0, FN=1, precision=0.000, recall=0.000. Both precision and recall need boundary work. Mixed `self_hosted_inference` errors. generic hosted inference API usage (`inference_api`), or model-artifact/hardware behavior (`local_models`). Boundary: "self-hosted" includes on-device engines; the boundary with `local_models` is engine integration vs model/hardware behavior. MUST include when central: integration with inference engines such as vLLM, llama.cpp, Ollama, LM Studio, TGI, or LocalAI — on device or self-hosted elsewhere — including engine setup, lifecycle, compatibility, engine crashes/timeouts, and self-hosted embeddings/speech/memory backends. Boundary: "self-hosted" includes on-device engines; the boundary with `local_models` is engine integration vs model/hardware behavior.

#### examples
##### Item 1
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

###### error_type
false_negative

#### true_positive_examples

#### false_positive_examples

#### false_negative_examples
##### Item 1
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

## confusions
### Item 1
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

### Item 2
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

## invalid_topics

## actionable_feedback
### Item 1
Pure-F1 objective: optimize exact topic membership, not recall-biased F-beta. Current precision=0.932, recall=0.896, F1=0.914.

### Item 2
Cardinality diagnosis: under_labeling; avg predicted 2.31 vs expected 2.41. Add central co-labels when multiple maintainer interests are explicit; avoid single-label collapse.

### Item 3
Topic cardinality is close: avg predicted topics 2.31 vs expected 2.41. Focus on boundary-specific errors.

### Item 4
`reliability` over_predicted: expected in 10 rows, predicted in 13, TP=10, FP=3, FN=0, precision=0.769, recall=1.000. Precision is the bottleneck. a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface.

### Item 5
`coding_agents` under_predicted: expected in 3 rows, predicted in 0, TP=0, FP=0, FN=3, precision=0.000, recall=0.000. Recall is the bottleneck. MUST include when central: integrations with external coding agents in general, or with a specific coding agent such as Codex, Claude Code, Gemini CLI, or Pi. Boundary: ACP is an integration protocol and is distinct from coding-agent integrations; route ACP protocol/session/delivery work to `acp`/`acpx`. OpenClaw's internal agent runtime is a core product surface; route startup, loop, backend, model-call orchestration, and adapter machinery to `agent_runtime`.

### Item 6
`notifications` mixed: expected in 5 rows, predicted in 3, TP=3, FP=0, FN=2, precision=1.000, recall=0.600. Both precision and recall need boundary work. Mixed `notifications` errors. chat-platform-specific behavior alone (`chat_integrations`) or reliability-only recovery. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label. MUST include when central: generic outbound notifications, completion delivery, message delivery gates, announcements, or notify behavior is central. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label.

### Item 7
`acp` mixed: expected in 6 rows, predicted in 5, TP=5, FP=0, FN=1, precision=1.000, recall=0.833. Both precision and recall need boundary work. Mixed `acp` errors. merely because an item mentions an agent session or internal runtime behavior. MUST include when central: ACP runtime/protocol, ACP session, ACP binding, ACP parent/child behavior, or ACP delivery is central.

### Item 8
`memory` mixed: expected in 1 rows, predicted in 2, TP=1, FP=1, FN=0, precision=0.500, recall=1.000. Both precision and recall need boundary work. Mixed `memory` errors. context window, session state, transcript, or generic remembering. MUST include when central: memory indexing, memory search, embeddings, active memory, or memory provider state is central.

### Item 9
`api_surface` mixed: expected in 1 rows, predicted in 2, TP=1, FP=1, FN=0, precision=0.500, recall=1.000. Both precision and recall need boundary work. Mixed `api_surface` errors. internal helpers, payload parsing, status text, UI events, ordinary commands, inference-integration behavior (`inference_api`), or gateway process ownership (`gateway`). Decision rule: if the item changes WHAT an external contract promises (shape, fields, status, compatibility), api_surface applies even when the implementation lives in the gateway or a serving endpoint; `docs` only when the contract text itself is the subject. MUST include when central: external API, CLI, HTTP, SDK, or documented command contracts. Decision rule: if the item changes WHAT an external contract promises (shape, fields, status, compatibility), api_surface applies even when the implementation lives in the gateway or a serving endpoint; `docs` only when the contract text itself is the subject.

## vanilla_f1_asi
### global_diagnosis
#### precision
0.9324324324324325

#### recall
0.8961038961038961

#### f1
0.9139072847682119

#### gepa_score
0.8460161423841059

#### score_mode
row-aware

#### exact_match
0.65625

#### row_exact_accuracy
0.65625

#### avg_row_jaccard
0.8593750000000001

#### avg_row_symdiff
0.40625

#### row_symdiff_score
0.7111111111111111

#### composite_score
0.8460161423841059

#### valid_json
1.0

#### cardinality_closeness
0.961038961038961

#### avg_expected_topics
2.40625

#### avg_predicted_topics
2.3125

#### false_positives
5

#### false_negatives
8

#### policy_chars
3837

#### policy_char_budget
4000

#### policy_length_over_budget
0

#### policy_length_penalty
0.0

#### policy_length_compliance
1.0

#### diagnosis
under_labeling

#### action
Add central co-labels when multiple maintainer interests are explicit; avoid single-label collapse.

### topic_priorities
#### Item 1
##### topic
reliability

##### problem
over_predicted

##### false_positives
3

##### false_negatives
0

##### precision
0.769

##### recall
1.0

##### action
`reliability` over_predicted: expected in 10 rows, predicted in 13, TP=10, FP=3, FN=0, precision=0.769, recall=1.000. Precision is the bottleneck. a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface.

#### Item 2
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

#### Item 3
##### topic
notifications

##### problem
mixed

##### false_positives
0

##### false_negatives
2

##### precision
1.0

##### recall
0.6

##### action
`notifications` mixed: expected in 5 rows, predicted in 3, TP=3, FP=0, FN=2, precision=1.000, recall=0.600. Both precision and recall need boundary work. Mixed `notifications` errors. chat-platform-specific behavior alone (`chat_integrations`) or reliability-only recovery. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label. MUST include when central: generic outbound notifications, completion delivery, message delivery gates, announcements, or notify behavior is central. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label.

#### Item 4
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

#### Item 5
##### topic
memory

##### problem
mixed

##### false_positives
1

##### false_negatives
0

##### precision
0.5

##### recall
1.0

##### action
`memory` mixed: expected in 1 rows, predicted in 2, TP=1, FP=1, FN=0, precision=0.500, recall=1.000. Both precision and recall need boundary work. Mixed `memory` errors. context window, session state, transcript, or generic remembering. MUST include when central: memory indexing, memory search, embeddings, active memory, or memory provider state is central.

#### Item 6
##### topic
api_surface

##### problem
mixed

##### false_positives
1

##### false_negatives
0

##### precision
0.5

##### recall
1.0

##### action
`api_surface` mixed: expected in 1 rows, predicted in 2, TP=1, FP=1, FN=0, precision=0.500, recall=1.000. Both precision and recall need boundary work. Mixed `api_surface` errors. internal helpers, payload parsing, status text, UI events, ordinary commands, inference-integration behavior (`inference_api`), or gateway process ownership (`gateway`). Decision rule: if the item changes WHAT an external contract promises (shape, fields, status, compatibility), api_surface applies even when the implementation lives in the gateway or a serving endpoint; `docs` only when the contract text itself is the subject. MUST include when central: external API, CLI, HTTP, SDK, or documented command contracts. Decision rule: if the item changes WHAT an external contract promises (shape, fields, status, compatibility), api_surface applies even when the implementation lives in the gateway or a serving endpoint; `docs` only when the contract text itself is the subject.

#### Item 7
##### topic
approvals

##### problem
mixed

##### false_positives
0

##### false_negatives
1

##### precision
0.0

##### recall
0.0

##### action
`approvals` mixed: expected in 1 rows, predicted in 0, TP=0, FP=0, FN=1, precision=0.000, recall=0.000. Both precision and recall need boundary work. Mixed `approvals` errors. merely because a command or tool might require permission. Co-label: bounding/expiring/persisting pending-approval state is approvals surface even when motivated by a memory/reliability fix. MUST include when central: approval prompts, permission decisions, or approval mode behavior is central. Co-label: bounding/expiring/persisting pending-approval state is approvals surface even when motivated by a memory/reliability fix.

#### Item 8
##### topic
self_hosted_inference

##### problem
mixed

##### false_positives
0

##### false_negatives
1

##### precision
0.0

##### recall
0.0

##### action
`self_hosted_inference` mixed: expected in 1 rows, predicted in 0, TP=0, FP=0, FN=1, precision=0.000, recall=0.000. Both precision and recall need boundary work. Mixed `self_hosted_inference` errors. generic hosted inference API usage (`inference_api`), or model-artifact/hardware behavior (`local_models`). Boundary: "self-hosted" includes on-device engines; the boundary with `local_models` is engine integration vs model/hardware behavior. MUST include when central: integration with inference engines such as vLLM, llama.cpp, Ollama, LM Studio, TGI, or LocalAI — on device or self-hosted elsewhere — including engine setup, lifecycle, compatibility, engine crashes/timeouts, and self-hosted embeddings/speech/memory backends. Boundary: "self-hosted" includes on-device engines; the boundary with `local_models` is engine integration vs model/hardware behavior.

### confusions
#### Item 1
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

#### Item 2
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

### row_examples
#### Item 1
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

#### Item 2
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

#### Item 3
##### id
openclaw-openclaw-71976

##### title
Memory Dreaming: Light sleep sort prioritizes recency over recallCount, hiding real recall data

##### expected
###### Item 1
memory

##### actual
###### Item 1
memory

###### Item 2
reliability

##### false_positives
###### Item 1
reliability

##### false_negatives

##### row_score
0.6666666666666666

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
api_surface

###### Item 2
inference_api

##### false_positives
###### Item 1
api_surface

##### false_negatives

##### row_score
0.6666666666666666

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

##### false_positives
###### Item 1
reliability

##### false_negatives

##### row_score
0.6666666666666666

#### Item 6
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

#### Item 7
##### id
openclaw-openclaw-72138

##### title
fix(feishu): emit sent hooks for normal replies

##### expected
###### Item 1
chat_integrations

###### Item 2
hooks

###### Item 3
notifications

##### actual
###### Item 1
chat_integrations

###### Item 2
hooks

##### false_positives

##### false_negatives
###### Item 1
notifications

##### row_score
0.8

#### Item 8
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
notifications

###### Item 2
reliability

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
3837

### reflection_hint
Make concise reusable routing rules. Do not copy the fixed allowed-topic taxonomy, do not add row-specific examples, and do not optimize for recall at the expense of F1.

## static_asi_path
eval/openclaw/easy-set-pilot/v6/vanilla-asi-v6-slim.md

## candidate_idx
2

## batch_summary
### model
codexresponses.gpt-5.4-mini

### input
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/input.jsonl

### output
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/candidate-0002/results.jsonl

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
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/candidate-0002/.results.jsonl.batch/20260611T210638Z-8da116e9

### started_at
2026-06-11T21:06:38Z

### completed_at
2026-06-11T21:08:05Z

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
81298.59

### timing_ms
#### duration
##### count
32

##### min
3191.71

##### mean
6801.9331250000005

##### median_approx
6415.855

##### max
18590.07

#### ttft
##### count
32

##### min
1900.08

##### mean
4889.7315625

##### median_approx
4845.275000000001

##### max
11158.16

#### time_to_response
##### count
32

##### min
2470.89

##### mean
6292.230625

##### median_approx
5785.44625

##### max
18457.09

### usage
#### input_tokens
184642

#### output_tokens
13163

#### total_tokens
197805

#### billing_tokens
197805

#### reasoning_tokens
10645

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
103680

#### served_tokens
103680

#### activity_tokens
103680

#### effective_input_tokens
80962

#### hit_rate_percent
56.151904767062746

#### write_rate_percent
0.0

#### activity_rate_percent
56.151904767062746

#### rows_with_cache_activity
27

#### row_cache_activity_percent
84.375

#### non_cached_input_tokens
80962

#### served_to_effective_input_ratio
1.2806007756725377

### shards
#### Item 1
##### index
0

##### offset
0

##### limit
8

##### output
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/candidate-0002/.results.jsonl.batch/20260611T210638Z-8da116e9/part-000.jsonl

#### Item 2
##### index
1

##### offset
8

##### limit
8

##### output
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/candidate-0002/.results.jsonl.batch/20260611T210638Z-8da116e9/part-001.jsonl

#### Item 3
##### index
2

##### offset
16

##### limit
8

##### output
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/candidate-0002/.results.jsonl.batch/20260611T210638Z-8da116e9/part-002.jsonl

#### Item 4
##### index
3

##### offset
24

##### limit
8

##### output
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/candidate-0002/.results.jsonl.batch/20260611T210638Z-8da116e9/part-003.jsonl

## lineage
### policy_sha256
1fbf207b6f9abc6c7f26c45bec3bc5ae8eeeea66539399b56b797a98a189d673

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