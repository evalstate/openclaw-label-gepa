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

Read title and main problem/feature first; use body, labels, files, and diff only to confirm central maintainer-owned concerns. Select every allowed topic that is a central routed deliverable, not every mentioned mechanism. Prefer owner surfaces; add co-labels when another surface’s behavior, contract, state, lifecycle, or user-visible delivery is explicitly changed.

# Cardinality Rules

Use 1-3 topics by default, 4-5 only for genuinely cross-cutting work; never more than 5. Do not drop a qualifying central co-label for brevity. Drop topics that are only locations, examples, dependencies, implementation mechanisms, or consequences. For bugs, add `reliability` only when operational failure handling is central: timeout, crash, stuck state, retry, durable loss, cleanup, recovery, leak, overload, race, cap, TTL, or lifecycle failure.

# Boundary Overlays

- Add `coding_agents` when user-visible agent/subagent/child/follow-up orchestration changes: handoff, parent control, running-state gating, result delivery/announcement, give-up behavior, lifecycle, or cleanup while agents are active. Pair with `acp`, `sessions`, `cron_automation`, `queueing`, or `notifications` when those owners are also central; do not use it for runtime internals alone.
- Add `notifications` when outbound reply/send delivery, completion announcements, notify gates/settings, sent-message state, delivery payload/path, expiration, or delivery recovery is central. Chat ingestion alone stays `chat_integrations`. Hooks emitted for sent outbound replies usually co-label `chat_integrations`, `hooks`, and `notifications`.
- Add `hooks` when hook registration, emission, events, priority, filters, payload, or hook security is a deliverable.
- Add `approvals` for permission prompts, decisions, modes, pending approval/permission state, expiry/TTL, caps, persistence, or cleanup, including when surfaced through MCP or motivated by reliability.
- Add `self_hosted_inference` for self-hosted or on-device engine setup, preflight, lifecycle, compatibility, crashes/timeouts, retries, or backends. Provider API request/response/streaming/vision/TTS/embedding handling stays `inference_api`; model-artifact or hardware behavior stays `local_models`.
- Add `telemetry_usage` whenever counts, tokens, costs, usage freshness, metrics, diagnostics, traces, or status reporting data are central, including UI/status/footer display. Pair with `ui_tui` when the user-facing display changes.
- Add `ui_tui` for TUI/UI status, footer, dashboard, lists, message extraction/rendering, or visible interaction changes. Do not replace it with `api_surface` unless an external CLI/HTTP/SDK contract itself changes.
- Use `api_surface` only when the caller-visible external contract changes: endpoint/CLI/SDK shape, fields, statuses, compatibility, webhooks, SSE, or documented command behavior. ACP/ACPX node/result delivery correctness, internal helpers, parsing, UI events, status text, inference integration, and gateway process ownership are not enough.
- Add `tests_ci` when the item is itself about tests, regression coverage, fixtures, mocks, CI, or platform test fixes; do not add it merely because a product change includes tests.
- If ACPX is explicitly owned, include `acpx`; also include `acp` when ACP runtime/protocol, session, binding, parent/child behavior, node/result delivery, or Codex ACP compatibility is central.
- Add `codex` for Codex runtime/auth/ACP/plugin/command compatibility. Add `security` when credential isolation, auth bridging, token scope, private boundaries, permission boundaries, or secret exposure are central.
- Keep `gateway` for gateway-owned routes, daemon startup, protocol, state, health, restart, or gateway-owned execution; not generic provider proxying, notifications, orchestration, or app-runtime failures.
- Add `config` only for operator-facing settings, defaults, persisted shape, env/config loading, validation, repair, setup, policy, allow/deny options, or migration.
- Documentation-only changes include `docs` plus the documented owner surface(s), not every contextual mechanism.

# Suppression Rules

- Do not infer topics from filenames, package names, labels, isolated keywords, examples, or incidental mentions when the main deliverable names another owner.
- Do not add `reliability` for wrong field mapping, empty/wrong content, formatting, visibility, ranking, ordering, wording, or ordinary product semantics unless durable loss, recovery, cleanup, retry, crash, timeout, leak, cap, TTL, or stuck behavior is central.
- Do not add `config` for docs that merely clarify behavior, steering, defaults in prose, examples, or internal constants.
- Do not add `memory` for pending state, context windows, transcripts, sessions, leaks, or generic remembering; require memory indexing/search, embeddings/vector/provider state, active memory, or memory archival/recovery.
- Do not add `self_hosted_inference` just because a self-hosted engine is named in an API-compatibility issue.
- Do not add `skills_plugins` for provider prompt hints, extension packages, review skills, or hook/channel events unless plugin/skill manifest, loading, SDK/runtime API, sync/prelude/wrappers, SecretRefs, doctor/check, or Policy plugin behavior is central.
- Do not add `tool_calling` for generic tools, queues, command output, screenshots, streaming prose, chat sends, or boundaries; require model tool-call protocol, deltas, schemas, transcript/result routing, or rendering.
- Do not add `gateway`, `api_surface`, or `agent_runtime` unless that boundary owns the externally relevant change.
- Return only the required concise JSON object; no prose, explanations, or extra fields.
```

## Evaluation Results

Performance data from evaluating the current component across test cases:

```
# Example 1
## Scores (Higher is Better)
### gepa_score
0.910142567114094

### composite_score
0.918697567114094

### topic_micro_f1
0.9530201342281879

### row_exact_accuracy
0.8125

### avg_row_jaccard
0.9322916666666667

### row_symdiff_score
0.8205128205128205

### policy_length_compliance
0.91445

### policy_hygiene_compliance
1.0

## score_details
### false_positives
1

### false_negatives
6

### row_exact_accuracy
0.8125

### avg_row_jaccard
0.9322916666666667

### avg_row_symdiff
0.21875

### avg_expected_topics
2.40625

### avg_predicted_topics
2.25

### asi_score
0.4

### topic_micro_precision
0.9861111111111112

### topic_micro_recall
0.922077922077922

### exact_match
0.8125

### row_symdiff_score
0.8205128205128205

### composite_score
0.918697567114094

### gepa_score
0.910142567114094

### score_mode
row-aware

### valid_json
1.0

### cardinality_closeness
0.935064935064935

### avg_topic_count_delta
-0.15625

### policy_chars
5711

### policy_char_budget
4000

### policy_length_over_budget
1711

### policy_length_penalty
0.008555

### policy_length_compliance
0.91445

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
self_hosted_inference

#### false_positives

#### false_negatives
##### Item 1
reliability

#### invalid_topics

#### keywords

#### row_score
0.8571428571428571

### Item 3
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

#### false_positives

#### false_negatives
##### Item 1
coding_agents

##### Item 2
reliability

#### invalid_topics

#### keywords

#### row_score
0.5

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
docs

##### Item 2
queueing

##### Item 3
tool_calling

#### false_positives
##### Item 1
tool_calling

#### false_negatives

#### invalid_topics

#### keywords

#### row_score
0.8

### Item 5
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

### Item 6
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
notifications

#### false_positives

#### false_negatives
##### Item 1
coding_agents

##### Item 2
reliability

#### invalid_topics

#### keywords

#### row_score
0.5

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
docs

##### Item 2
queueing

##### Item 3
tool_calling

#### false_positives
##### Item 1
tool_calling

#### false_negatives

#### invalid_topics

#### keywords

#### row_score
0.8

### Item 4
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

### Item 5
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
self_hosted_inference

#### false_positives

#### false_negatives
##### Item 1
reliability

#### invalid_topics

#### keywords

#### row_score
0.8571428571428571

### Item 6
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

## topic_error_patterns
### Item 1
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

###### keywords

###### row_score
0.5

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

### Item 2
#### topic
reliability

#### problem
mixed

#### expected
10

#### actual
8

#### true_positives
8

#### false_positives
0

#### false_negatives
2

#### precision
1.0

#### recall
0.8

#### f1
0.889

#### action
`reliability` mixed: expected in 10 rows, predicted in 8, TP=8, FP=0, FN=2, precision=1.000, recall=0.800. Both precision and recall need boundary work. Mixed `reliability` errors. a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface. MUST include when central: timeout, crash, leak, stuck state, retry, data loss, lifecycle cleanup, recovery, overload, or operational failure mode.

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
self_hosted_inference

###### keywords

###### error_type
false_negative

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
notifications

###### keywords

###### error_type
false_negative

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
self_hosted_inference

###### keywords

###### row_score
0.857

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
notifications

###### keywords

###### row_score
0.5

### Item 3
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

### Item 4
#### topic
tool_calling

#### problem
mixed

#### expected
0

#### actual
1

#### true_positives
0

#### false_positives
1

#### false_negatives
0

#### precision
0.0

#### recall
0.0

#### f1
0.0

#### action
`tool_calling` mixed: expected in 0 rows, predicted in 1, TP=0, FP=1, FN=0, precision=0.000, recall=0.000. Both precision and recall need boundary work. Mixed `tool_calling` errors. generic command output, TTS, browser screenshot/vision, or config-like options. Co-label: parameter coercion/normalization for tool invocation is tool_calling, even inside an MCP bundle or adapter. MUST include when central: tool-call protocol, tool result transcript handling, function/tool schema, or tool-call rendering is central. Co-label: parameter coercion/normalization for tool invocation is tool_calling, even inside an MCP bundle or adapter.

#### examples
##### Item 1
###### expected
###### Item 1
docs

###### Item 2
queueing

###### actual
###### Item 1
docs

###### Item 2
queueing

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
docs

###### Item 2
queueing

###### actual
###### Item 1
docs

###### Item 2
queueing

###### Item 3
tool_calling

###### keywords

###### row_score
0.8

#### false_negative_examples

## confusions

## invalid_topics

## actionable_feedback
### Item 1
Pure-F1 objective: optimize exact topic membership, not recall-biased F-beta. Current precision=0.986, recall=0.922, F1=0.953.

### Item 2
Cardinality diagnosis: under_labeling; avg predicted 2.25 vs expected 2.41. Add central co-labels when multiple maintainer interests are explicit; avoid single-label collapse.

### Item 3
Policy length penalty: policy is 1711 chars over the 4000 char budget; GEPA score was reduced by 0.0086.

### Item 4
Topic cardinality is close: avg predicted topics 2.25 vs expected 2.41. Focus on boundary-specific errors.

### Item 5
`coding_agents` under_predicted: expected in 3 rows, predicted in 0, TP=0, FP=0, FN=3, precision=0.000, recall=0.000. Recall is the bottleneck. MUST include when central: integrations with external coding agents in general, or with a specific coding agent such as Codex, Claude Code, Gemini CLI, or Pi. Boundary: ACP is an integration protocol and is distinct from coding-agent integrations; route ACP protocol/session/delivery work to `acp`/`acpx`. OpenClaw's internal agent runtime is a core product surface; route startup, loop, backend, model-call orchestration, and adapter machinery to `agent_runtime`.

### Item 6
`reliability` mixed: expected in 10 rows, predicted in 8, TP=8, FP=0, FN=2, precision=1.000, recall=0.800. Both precision and recall need boundary work. Mixed `reliability` errors. a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface. MUST include when central: timeout, crash, leak, stuck state, retry, data loss, lifecycle cleanup, recovery, overload, or operational failure mode.

### Item 7
`notifications` mixed: expected in 5 rows, predicted in 4, TP=4, FP=0, FN=1, precision=1.000, recall=0.800. Both precision and recall need boundary work. Mixed `notifications` errors. chat-platform-specific behavior alone (`chat_integrations`) or reliability-only recovery. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label. MUST include when central: generic outbound notifications, completion delivery, message delivery gates, announcements, or notify behavior is central. Co-label: when a chat-surface change implements or alters a delivery payload/path or delivery gates, add notifications alongside the chat label.

### Item 8
`tool_calling` mixed: expected in 0 rows, predicted in 1, TP=0, FP=1, FN=0, precision=0.000, recall=0.000. Both precision and recall need boundary work. Mixed `tool_calling` errors. generic command output, TTS, browser screenshot/vision, or config-like options. Co-label: parameter coercion/normalization for tool invocation is tool_calling, even inside an MCP bundle or adapter. MUST include when central: tool-call protocol, tool result transcript handling, function/tool schema, or tool-call rendering is central. Co-label: parameter coercion/normalization for tool invocation is tool_calling, even inside an MCP bundle or adapter.

## vanilla_f1_asi
### global_diagnosis
#### precision
0.9861111111111112

#### recall
0.922077922077922

#### f1
0.9530201342281879

#### gepa_score
0.910142567114094

#### score_mode
row-aware

#### exact_match
0.8125

#### row_exact_accuracy
0.8125

#### avg_row_jaccard
0.9322916666666667

#### avg_row_symdiff
0.21875

#### row_symdiff_score
0.8205128205128205

#### composite_score
0.918697567114094

#### valid_json
1.0

#### cardinality_closeness
0.935064935064935

#### avg_expected_topics
2.40625

#### avg_predicted_topics
2.25

#### false_positives
1

#### false_negatives
6

#### policy_chars
5711

#### policy_char_budget
4000

#### policy_length_over_budget
1711

#### policy_length_penalty
0.008555

#### policy_length_compliance
0.91445

#### diagnosis
under_labeling

#### action
Add central co-labels when multiple maintainer interests are explicit; avoid single-label collapse.

### topic_priorities
#### Item 1
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

#### Item 2
##### topic
reliability

##### problem
mixed

##### false_positives
0

##### false_negatives
2

##### precision
1.0

##### recall
0.8

##### action
`reliability` mixed: expected in 10 rows, predicted in 8, TP=8, FP=0, FN=2, precision=1.000, recall=0.800. Both precision and recall need boundary work. Mixed `reliability` errors. a generic bug tag, CI-only or test-environment failures (`tests_ci`), or a failure that merely motivates a change whose deliverable belongs entirely to another surface. MUST include when central: timeout, crash, leak, stuck state, retry, data loss, lifecycle cleanup, recovery, overload, or operational failure mode.

#### Item 3
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

#### Item 4
##### topic
tool_calling

##### problem
mixed

##### false_positives
1

##### false_negatives
0

##### precision
0.0

##### recall
0.0

##### action
`tool_calling` mixed: expected in 0 rows, predicted in 1, TP=0, FP=1, FN=0, precision=0.000, recall=0.000. Both precision and recall need boundary work. Mixed `tool_calling` errors. generic command output, TTS, browser screenshot/vision, or config-like options. Co-label: parameter coercion/normalization for tool invocation is tool_calling, even inside an MCP bundle or adapter. MUST include when central: tool-call protocol, tool result transcript handling, function/tool schema, or tool-call rendering is central. Co-label: parameter coercion/normalization for tool invocation is tool_calling, even inside an MCP bundle or adapter.

### confusions

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
notifications

##### false_positives

##### false_negatives
###### Item 1
coding_agents

###### Item 2
reliability

##### row_score
0.5

#### Item 2
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

#### Item 3
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
docs

###### Item 2
queueing

###### Item 3
tool_calling

##### false_positives
###### Item 1
tool_calling

##### false_negatives

##### row_score
0.8

#### Item 4
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

#### Item 5
##### id
openclaw-openclaw-82145

##### title
cron: allow retries for local model preflight

##### expected
###### Item 1
config

###### Item 2
cron_automation

###### Item 3
reliability

###### Item 4
self_hosted_inference

##### actual
###### Item 1
config

###### Item 2
cron_automation

###### Item 3
self_hosted_inference

##### false_positives

##### false_negatives
###### Item 1
reliability

##### row_score
0.8571428571428571

#### Item 6
##### id
openclaw-openclaw-69256

##### title
fix(cron): prevent premature session cleanup when subagents are running

##### expected
###### Item 1
coding_agents

###### Item 2
cron_automation

###### Item 3
reliability

###### Item 4
sessions

##### actual
###### Item 1
cron_automation

###### Item 2
reliability

###### Item 3
sessions

##### false_positives

##### false_negatives
###### Item 1
coding_agents

##### row_score
0.8571428571428571

### prompt_hygiene
#### ok
True

#### findings

#### policy_chars
5711

### reflection_hint
Make concise reusable routing rules. Do not copy the fixed allowed-topic taxonomy, do not add row-specific examples, and do not optimize for recall at the expense of F1.

## static_asi_path
eval/openclaw/easy-set-pilot/v6/vanilla-asi-v6-slim.md

## candidate_idx
5

## batch_summary
### model
codexresponses.gpt-5.4-mini

### input
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/input.jsonl

### output
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/candidate-0005/results.jsonl

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
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/candidate-0005/.results.jsonl.batch/20260611T211218Z-8d6e92a4

### started_at
2026-06-11T21:12:18Z

### completed_at
2026-06-11T21:13:15Z

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
54929.56

### timing_ms
#### duration
##### count
32

##### min
2973.6

##### mean
5790.3471875

##### median_approx
5608.43375

##### max
11952.89

#### ttft
##### count
32

##### min
1899.7

##### mean
4204.538125

##### median_approx
3719.19875

##### max
9215.86

#### time_to_response
##### count
32

##### min
2582.62

##### mean
5539.43625

##### median_approx
5418.26

##### max
11822.24

### usage
#### input_tokens
196098

#### output_tokens
11604

#### total_tokens
207702

#### billing_tokens
207702

#### reasoning_tokens
9043

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
115968

#### served_tokens
115968

#### activity_tokens
115968

#### effective_input_tokens
80130

#### hit_rate_percent
59.13777804975064

#### write_rate_percent
0.0

#### activity_rate_percent
59.13777804975064

#### rows_with_cache_activity
31

#### row_cache_activity_percent
96.875

#### non_cached_input_tokens
80130

#### served_to_effective_input_ratio
1.4472482216398352

### shards
#### Item 1
##### index
0

##### offset
0

##### limit
8

##### output
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/candidate-0005/.results.jsonl.batch/20260611T211218Z-8d6e92a4/part-000.jsonl

#### Item 2
##### index
1

##### offset
8

##### limit
8

##### output
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/candidate-0005/.results.jsonl.batch/20260611T211218Z-8d6e92a4/part-001.jsonl

#### Item 3
##### index
2

##### offset
16

##### limit
8

##### output
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/candidate-0005/.results.jsonl.batch/20260611T211218Z-8d6e92a4/part-002.jsonl

#### Item 4
##### index
3

##### offset
24

##### limit
8

##### output
runs/easy-set-v6/gepa/gpt-5.4-mini-v6a-ledger32-batch-mc30/candidate-0005/.results.jsonl.batch/20260611T211218Z-8d6e92a4/part-003.jsonl

## lineage
### policy_sha256
e9299b88a499f5e11362f06c00f5e2b87bcb6b5ab66dd4d50f7def4631f91cc9

### parent_candidate_idx
4

### reflection_call
call-0004


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