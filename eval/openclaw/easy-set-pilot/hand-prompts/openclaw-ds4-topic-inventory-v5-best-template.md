# OpenClaw DS4 Topic Inventory Classifier

Classify this OpenClaw GitHub issue or pull request against Onur's current
topics of interest.

Do not write prose, analysis, markdown, or JSON text in the assistant response.
Submit the answer by calling final_json exactly once.

Use the injected GitHub context first. It was collected before this model run
from GitHub, and may be truncated to keep the prompt small. You may explore
further only if the injected context is insufficient or contradictory.

Required output shape:

```json
{"topics_of_interest":[],"description":"One concise evidence-backed sentence.","caveats":[]}
```

## GitHub Context

{{github_context}}

Use this context as source of truth. If important sections are missing,
unavailable, selected, or truncated, classify from what is available and mention
material limits in `caveats`.

## Allowed Topics

```json
{{allowed_topics_json}}
```

## Generic Classification Rule

- Set `topics_of_interest` to the central matching topics from the allowed
  `topics_of_interest` values.
- Use 1-3 topics by default. Return 4-5 topics only when the item is genuinely
  cross-cutting and each topic is central.
- Never return more than 5 topics. If more than 5 topics seem relevant, keep
  only the 5 most central topics.
- Use an empty `topics_of_interest` array when no listed interest topic applies.
- Keep `description` concise and grounded in the provided context.
- Use `caveats` only for uncertainty, missing context, or limits in the
  classification.

## Topic Inventory Inclusion Policy

These topic inventory rules override any earlier default-output-size guidance in
this prompt. In particular, do not use a 1-3 topic preference when the rules
below identify 4-5 central topics.

Classify for maintainer topic inventory and evaluation, not code search.

Output rules:

- Include every topic whose MUST rule is satisfied.
- Do not omit a MUST topic to keep the output short.
- Do not add topics supported only by changed files, tests, examples,
  incidental helper code, or weak consequences.
- Never output more than 5 topics; if more than 5 MUST rules are satisfied,
  keep the 5 strongest central owner boundaries.

MUST include rules:

- `local_models`: MUST include for llama.cpp, GGUF, LM Studio, Ollama, local
  hardware, local model compatibility, local model fallback, or local model
  context behavior.
- `local_model_providers`: MUST include for model-provider setup, provider
  routing, provider auth, provider discovery, provider allow/deny rules,
  provider references, provider catalogs, or provider compatibility checks.
- `model_serving`: MUST include for endpoint protocol behavior,
  OpenAI-compatible serving, streaming, usage chunks, base URL normalization,
  request routing, vLLM/TGI/LocalAI endpoint behavior, or endpoint lifecycle.
- `self_hosted_inference`: MUST include for self-hosted inference backends,
  local/remote custom inference servers, or self-hosted embeddings/inference
  operations.
- `open_weight_models`: MUST include for named open-weight model families,
  model release metadata, context windows, quantization, or hosted open-weight
  catalogs.
- `acpx`: MUST include when ACPX runtime, worker, harness, configured binding,
  or ACPX-specific compatibility is central.
- `acp`: MUST include when ACP runtime/protocol, ACP session, ACP binding, ACP
  parent/child behavior, or ACP delivery is central.
- `coding_agents`: MUST include when subagents, coding-agent runs, agent harness
  behavior, compaction, tool-use approvals, sandboxing for agents, or agent
  orchestration are central.
- `mcp_tooling`: MUST include for MCP server allow/deny rules, MCP conformance
  checks, MCP handshake/tool behavior, MCP config, or MCP tool routing.
- `codex`: MUST include when Codex runtime, Codex auth, Codex ACP, Codex
  plugin, or Codex harness behavior is central.
- `agent_runtime`: MUST include when agent runtime startup, loop, backend,
  model call orchestration, runtime adapter behavior, or runtime
  ownership/execution architecture is central.
- `sessions`: MUST include when session lifecycle, state, storage, identity,
  binding, or cleanup is central.
- `gateway`: MUST include when gateway routing, gateway state, gateway startup,
  gateway protocol, or gateway-owned execution is central.
- `exec_tools`: MUST include when shell execution, command invocation, PATH,
  tool execution policy, or execution output control is central.
- `approvals`: MUST include when approval prompts, permission decisions, or
  approval mode behavior is central.
- `sandboxing`: MUST include when sandbox policy, sandbox inheritance, sandbox
  escape, path isolation, or sandbox runtime behavior is central.
- `hooks`: MUST include when hook registration, hook priority, hook execution,
  or hook security is central.
- `cron_automation`: MUST include when cron jobs, heartbeat runs, scheduled
  automation, or force-run behavior is central.
- `chat_integrations`: MUST include when a named chat platform, channel adapter,
  message ingestion, or chat delivery surface is central.
- `ui_tui`: MUST include when UI/TUI display, status, footer, mobile UI, or
  visual interaction is central.
- `browser_automation`: MUST include when browser/CDP/Chrome automation,
  browser session attach, or auth browser flow is central.
- `memory`: MUST include when memory indexing, memory search, embeddings,
  active memory, or memory provider state is central.
- `security`: MUST include for SSRF, private-network access, credential/auth
  boundaries, permissions, sandbox escape, secret leakage, supply-chain
  hardening, or access-control evidence.
- `config`: MUST include for configuration schemas, persisted config shape,
  config loading, config validation, config repair, environment/config
  defaults, operator-facing config options, allow/deny configuration, or policy
  settings.
- `packaging_deployment`: MUST include when packaging, installer, Docker image,
  release artifact, dependency packaging, or deployment is central.
- `docs`: MUST include only when documentation itself is the subject.
- `tests_ci`: MUST include only when tests, CI, or test infrastructure itself is
  the subject.
- `telemetry_usage`: MUST include when token counts, usage counts, costs,
  metrics, diagnostics, traces, or status reporting are central.
- `api_surface`: MUST include for external API, CLI, HTTP, SDK, or documented
  command contracts.
- `queueing`: MUST include when queues, lanes, scheduling, task ordering, or
  work dispatch are central.
- `notifications`: MUST include when generic outbound notifications, completion
  delivery, message delivery gates, announcements, or notify behavior is
  central.
- `skills_plugins`: MUST include when the item changes, extends, validates,
  documents, or adds doctor/check behavior for a plugin or skill surface. The
  bundled Policy plugin is a plugin surface. If Policy plugin behavior is
  central, include `skills_plugins` even when model, MCP, security, or config
  topics are also central.
- `auth_identity`: MUST include when authentication, OAuth, credential
  propagation, identity overlay, auth profile selection, or account/user
  identity is central.
- `reliability`: MUST include for timeout, crash, leak, stuck state, retry, data
  loss, lifecycle cleanup, recovery, overload, or operational failure mode.
- `tool_calling`: MUST include when tool-call protocol, tool result transcript
  handling, function/tool schema, or tool-call rendering is central.

Policy/conformance rows:

- If an item introduces or validates allow/deny rules, conformance checks, or
  doctor checks, include the checked domains and include `config` when those
  rules/settings are operator-visible or persisted.
- If policy/conformance work lives in, extends, documents, or adds checks for
  the Policy plugin, `skills_plugins` MUST be included.
- If the checks include private-network, SSRF, credential, auth, or permission
  posture, `security` MUST be included.
- If the checks include model providers, provider refs, provider catalogs, or
  provider routing/setup, `local_model_providers` MUST be included.
- If the checks include MCP servers or MCP tools, `mcp_tooling` MUST be
  included.

Description and caveats:

- Keep `description` concise and grounded in the provided context.
- Use `caveats` only for uncertainty, missing context, or limits in the
  classification.

Return the final answer only by calling final_json.
