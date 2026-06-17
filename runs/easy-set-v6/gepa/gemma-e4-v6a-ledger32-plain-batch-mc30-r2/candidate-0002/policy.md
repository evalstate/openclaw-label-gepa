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