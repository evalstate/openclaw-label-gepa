# Reviewed-row relabel stability

## Summary

- rows: 29
- valid_r1: 29
- valid_r2: 29
- r1_r2_exact_rows: 21
- r1_r2_exact_rate: 0.7241379310344828
- r1_r2_avg_jaccard: 0.9091954022988505
- r1_vs_reviewed_exact: 15
- r2_vs_reviewed_exact: 14
- r1_vs_reviewed_exact_rate: 0.5172413793103449
- r2_vs_reviewed_exact_rate: 0.4827586206896552
- r1_vs_reviewed_avg_jaccard: 0.778735632183908
- r2_vs_reviewed_avg_jaccard: 0.8011494252873563
- r1_avg_symdiff_vs_reviewed: 0.896551724137931
- r2_avg_symdiff_vs_reviewed: 0.7586206896551724
- stable_and_matches_reviewed: 13

## Rows with r1/r2 instability

### 39248 openclaw-openclaw-39248 — Bug: sandbox.mode: "non-main" silently breaks sessions_spawn subagent initialization

- reviewed: `agent_runtime, reliability, sandboxing, sessions`
- r1: `agent_runtime, reliability, sandboxing, sessions`
- r2: `acp, agent_runtime, reliability, sandboxing, sessions`
- notes: it is not coding_agents as this applies to openclaw internal subagents rather than external tools.

### 44202 openclaw-openclaw-44202 — [Bug]: local memory embeddings on Apple Silicon can crash gateway in ggml-metal / node-llama-cpp; need official Metal/GPU guidance

- reviewed: `local_models, memory, reliability, self_hosted_inference`
- r1: `gateway, local_models, memory, reliability`
- r2: `gateway, local_models, memory, reliability, self_hosted_inference`
- notes: this issue mentions the gateway as a diagnostic point not a root cause so was removed.

### 47285 openclaw-openclaw-47285 — feat(memory-lancedb): native Azure OpenAI support

- reviewed: `api_surface, memory`
- r1: `auth_identity, memory, model_serving`
- r2: `auth_identity, config, memory`
- notes: it is not local_model_providers as azure is a hosted model provider. this is an update to the memory model.

### 51654 openclaw-openclaw-51654 — Support session-level environment variables for ACP sessions

- reviewed: `acp, acpx, security, sessions`
- r1: `acp, acpx, auth_identity, sessions`
- r2: `acp, acpx, auth_identity, security, sessions`
- notes: auth_identity is intended to be used for direct auth issues or identity issues with openclaw, rather than a general term.

### 52747 openclaw-openclaw-52747 — fix(acp): time out stuck session lane tasks

- reviewed: `acp, config, queueing, reliability, sessions`
- r1: `acp, queueing, reliability, sessions`
- r2: `acp, config, queueing, reliability, sessions`
- notes: this is correct, config is debatable

### 84039 openclaw-openclaw-84039 — fix(cli): honor --no-prefix-cwd in acp

- reviewed: `acp`
- r1: `acp`
- r2: `acp, tests_ci`
- notes: User reviewed and said this row is correct.

### 84549 openclaw-openclaw-84549 — fix(deepinfra): load all DeepInfra models when user wants to browse t…

- reviewed: `config, model_serving`
- r1: `model_serving, skills_plugins`
- r2: `config, model_serving, skills_plugins`
- notes: Only apply the `skills_plugin` if there is a specific change to that area (a mention of a review skill is not alone enough). config label applies as this PR addresses a configuration failure/bypass

### 84997 openclaw-openclaw-84997 — [AI-assisted] Add NEAR AI Cloud provider

- reviewed: `auth_identity, model_serving`
- r1: `api_surface, auth_identity, config`
- r2: `auth_identity, config, model_serving`
- notes: NearAI is a cloud hosted (not local) model provider so local_model_providers does not apply.


## Rows not matching reviewed labels in both runs

### 39248 openclaw-openclaw-39248 — Bug: sandbox.mode: "non-main" silently breaks sessions_spawn subagent initialization

- reviewed: `agent_runtime, reliability, sandboxing, sessions`
- r1: `agent_runtime, reliability, sandboxing, sessions` exact=True j=1.00
- r2: `acp, agent_runtime, reliability, sandboxing, sessions` exact=False j=0.80
- decision: fix_labels
- notes: it is not coding_agents as this applies to openclaw internal subagents rather than external tools.

### 43246 openclaw-openclaw-43246 — fix(message): deny same-provider cross-context sends by default [AI-assisted]

- reviewed: `chat_integrations, config, security, tool_calling`
- r1: `chat_integrations, config, notifications, security` exact=False j=0.60
- r2: `chat_integrations, config, notifications, security` exact=False j=0.60
- decision: fix_labels
- notes: tool_calling applies as this relates to how tools are used. security as this relates to potential leakage. 

### 44202 openclaw-openclaw-44202 — [Bug]: local memory embeddings on Apple Silicon can crash gateway in ggml-metal / node-llama-cpp; need official Metal/GPU guidance

- reviewed: `local_models, memory, reliability, self_hosted_inference`
- r1: `gateway, local_models, memory, reliability` exact=False j=0.60
- r2: `gateway, local_models, memory, reliability, self_hosted_inference` exact=False j=0.80
- decision: fix_labels
- notes: this issue mentions the gateway as a diagnostic point not a root cause so was removed.

### 47285 openclaw-openclaw-47285 — feat(memory-lancedb): native Azure OpenAI support

- reviewed: `api_surface, memory`
- r1: `auth_identity, memory, model_serving` exact=False j=0.25
- r2: `auth_identity, config, memory` exact=False j=0.25
- decision: fix_labels
- notes: it is not local_model_providers as azure is a hosted model provider. this is an update to the memory model.

### 51654 openclaw-openclaw-51654 — Support session-level environment variables for ACP sessions

- reviewed: `acp, acpx, security, sessions`
- r1: `acp, acpx, auth_identity, sessions` exact=False j=0.60
- r2: `acp, acpx, auth_identity, security, sessions` exact=False j=0.80
- decision: fix_labels
- notes: auth_identity is intended to be used for direct auth issues or identity issues with openclaw, rather than a general term.

### 52747 openclaw-openclaw-52747 — fix(acp): time out stuck session lane tasks

- reviewed: `acp, config, queueing, reliability, sessions`
- r1: `acp, queueing, reliability, sessions` exact=False j=0.80
- r2: `acp, config, queueing, reliability, sessions` exact=True j=1.00
- decision: keep_easy
- notes: this is correct, config is debatable

### 69256 openclaw-openclaw-69256 — fix(cron): prevent premature session cleanup when subagents are running

- reviewed: `agent_runtime, cron_automation, queueing, reliability, sessions`
- r1: `agent_runtime, cron_automation, reliability, sessions` exact=False j=0.80
- r2: `agent_runtime, cron_automation, reliability, sessions` exact=False j=0.80
- decision: fix_labels
- notes: coding_agents does not apply as it is not directly referring to external tool integrations. queueing applies as it relates to lock/orchestration type activities

### 77827 openclaw-openclaw-77827 — fix: LM Studio thinking blocks invisible with Responses API

- reviewed: `api_surface, local_model_providers, model_serving`
- r1: `api_surface, local_models, model_serving` exact=False j=0.50
- r2: `api_surface, local_models, model_serving` exact=False j=0.50
- decision: fix_labels
- notes: local_models does not apply as it does include a specific model or class of model. local_model_providers applies as this is about serving generally models with LM Studio via the Responses API - which is a local model provider

### 77992 openclaw-openclaw-77992 — [Bug] Context display shows ?/131k with llama.cpp after upgrading to 2026.5.4 — field name mismatch not resolved

- reviewed: `local_model_providers, local_models, model_serving, telemetry_usage`
- r1: `local_models, model_serving, telemetry_usage` exact=False j=0.75
- r2: `local_models, model_serving, telemetry_usage` exact=False j=0.75
- decision: keep_easy
- notes: User reviewed and said this row is correct.

### 80783 openclaw-openclaw-80783 — Policy: add model, network, and MCP conformance checks

- reviewed: `config, local_model_providers, mcp_tooling, security`
- r1: `config, mcp_tooling, security, skills_plugins` exact=False j=0.60
- r2: `config, mcp_tooling, security, skills_plugins` exact=False j=0.60
- decision: fix_labels
- notes: There is no mention of skills / plugins here.

### 84039 openclaw-openclaw-84039 — fix(cli): honor --no-prefix-cwd in acp

- reviewed: `acp`
- r1: `acp` exact=True j=1.00
- r2: `acp, tests_ci` exact=False j=0.50
- decision: keep_easy
- notes: User reviewed and said this row is correct.

### 84549 openclaw-openclaw-84549 — fix(deepinfra): load all DeepInfra models when user wants to browse t…

- reviewed: `config, model_serving`
- r1: `model_serving, skills_plugins` exact=False j=0.33
- r2: `config, model_serving, skills_plugins` exact=False j=0.67
- decision: fix_labels
- notes: Only apply the `skills_plugin` if there is a specific change to that area (a mention of a review skill is not alone enough). config label applies as this PR addresses a configuration failure/bypass

### 84719 openclaw-openclaw-84719 — fix: preserve active webhook request counters

- reviewed: `queueing, reliability`
- r1: `api_surface, reliability, skills_plugins` exact=False j=0.25
- r2: `api_surface, reliability, skills_plugins` exact=False j=0.25
- decision: fix_labels
- notes: this does not directly relate to skills_plugins. queueing label applies as this relates to a backpressure type problem

### 84746 openclaw-openclaw-84746 — [Bug]: Auto-compaction crashes active responses after 5.18 transcript lock scope change (#13744)

- reviewed: `agent_runtime, reliability, sessions`
- r1: `agent_runtime, memory, reliability, sessions` exact=False j=0.75
- r2: `agent_runtime, memory, reliability, sessions` exact=False j=0.75
- decision: fix_labels
- notes: memory does not apply here - memory should be used for the specific memory features, not as a general term

### 84997 openclaw-openclaw-84997 — [AI-assisted] Add NEAR AI Cloud provider

- reviewed: `auth_identity, model_serving`
- r1: `api_surface, auth_identity, config` exact=False j=0.25
- r2: `auth_identity, config, model_serving` exact=False j=0.67
- decision: fix_labels
- notes: NearAI is a cloud hosted (not local) model provider so local_model_providers does not apply.

### 88400 openclaw-openclaw-88400 — fix(config): accept overlays for bundled provider aliases

- reviewed: `config, model_serving`
- r1: `config` exact=False j=0.50
- r2: `config` exact=False j=0.50
- decision: fix_labels
- notes: this is not specific to local models. this is about configuration of model_serving providers.
