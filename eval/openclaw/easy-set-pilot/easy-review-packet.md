# easy-set-pilot review packet

Edit the `decision` block for each row. Suggested values:

- `keep_easy`: labels are clean enough for easy set
- `drop_to_medium`: useful but boundary/ASI material
- `fix_labels`: replace labels in `final_labels`
- `drop`: exclude from pilot

## openclaw-openclaw-47285 / #47285 — feat(memory-lancedb): native Azure OpenAI support

- audit_reasons: `hosted_cloud_provider_not_local_model_provider`
- previous_expected_topics: `auth_identity, local_model_providers, memory`
- gpt55_labels: `memory, local_model_providers, auth_identity`
- possible_confusions: `self_hosted_inference`
- agreement_jaccard: `1.0`

**Rationales**
- `memory`: The PR targets the memory-lancedb plugin and Azure OpenAI embeddings for LanceDB memory functionality.
- `local_model_providers`: It adds provider compatibility for Azure/OpenAI-compatible embedding endpoints via baseUrl detection and API version handling.
- `auth_identity`: It changes provider authentication by sending Azure's required api-key header instead of a bearer Authorization header.

**Excluded rationales**
- `self_hosted_inference`: Azure OpenAI is a hosted provider integration, not a self-hosted or local inference service change.

**Excerpt**

```markdown
This PR adds native Azure OpenAI support to the memory-lancedb plugin.
It automatically detects Azure endpoints (via ) and injects the required  header and  query parameter (defaulting to ).
This allows users to use Azure OpenAI for embeddings without needing an intermediate proxy like LiteLLM or OneAPI, significantly reducing friction for enterprise users.
```

**Decision**

```json
{
  "id": "openclaw-openclaw-47285",
  "decision": "fix_labels",
  "final_labels": [
    "memory",
    "api_surface",
  ],
  "notes": "it is not local_model_providers as azure is a hosted model provider. this is an update to the memory model."
}
```

## openclaw-openclaw-68725 / #68725 — feat(amazon-bedrock-mantle): add known context windows for open-weight Mantle models

- audit_reasons: `teacher_previous_label_disagreement, low_previous_label_jaccard, hosted_cloud_provider_not_local_model_provider`
- previous_expected_topics: `local_model_providers, memory, open_weight_models`
- gpt55_labels: `local_model_providers, open_weight_models`
- possible_confusions: `memory`
- agreement_jaccard: `0.6666666666666666`

**Rationales**
- `local_model_providers`: Changes provider discovery metadata for an OpenAI-compatible Mantle backend, including model context-window resolution.
- `open_weight_models`: The lookup is explicitly for open-weight model families such as Qwen, DeepSeek, GLM, Nemotron, and MiniMax.

**Excluded rationales**
- `memory`: Context-window and compaction-threshold metadata are discussed, but no memory system, embeddings, vector store, or archival behavior is changed.

**Excerpt**

```markdown
# feat(amazon-bedrock-mantle): add known context windows for open-weight Mantle models
## Problem
Mantle's `/v1/models` endpoint returns only model IDs — no token limit metadata. Discovery hardcodes `contextWindow: 32000` for every model, which is wrong for most:
- MiniMax M2/M2.1: **1,000,000** (gets 32K)
- Qwen3 Coder: **256,000** (gets 32K)
- DeepSeek V3.x, GLM 4.x, Nemotron: **128,000** (gets 32K)
This causes the same premature context overflow and wrong compaction thresholds as #65952 (the amazon-bedrock equivalent).
## Fix
Add a `KNOWN_CONTEXT_WINDOWS` lookup table for open-weight models currently available on Mantle. Raise the default fallback from 32K → 128K for unknown models.
```

**Decision**

```json
{
  "id": "openclaw-openclaw-68725",
  "decision": "fix_labels",
  "final_labels": [
    "open_weight_models",
    "config"
  ],
  "notes": "Bedrock/Mantle is hosted; this is configuring known context-window metadata/defaults for open-weight model families, not local provider setup."
}
```

## openclaw-openclaw-77992 / #77992 — [Bug] Context display shows ?/131k with llama.cpp after upgrading to 2026.5.4 — field name mismatch not resolved

- audit_reasons: `teacher_previous_label_disagreement, low_previous_label_jaccard`
- previous_expected_topics: `local_models, model_serving, telemetry_usage`
- gpt55_labels: `local_models, local_model_providers, model_serving, telemetry_usage`
- possible_confusions: `self_hosted_inference`
- agreement_jaccard: `0.75`

**Rationales**
- `local_models`: The bug occurs with a local llama.cpp server running a GGUF Qwen model and affects local model users.
- `local_model_providers`: The issue is a provider compatibility mismatch for the configured llamacpp OpenAI-compatible backend.
- `model_serving`: It depends on the llama.cpp server response schema for OpenAI-compatible usage fields.
- `telemetry_usage`: The broken behavior is token usage/context accounting showing '?/131k' instead of parsed token counts.

**Excluded rationales**
- `self_hosted_inference`: The backend is self-hosted, but the actionable bug is local provider/model-serving usage parsing rather than a broader inference service issue.

**Excerpt**

```markdown
### Bug type
Regression (worked before, now fails)
### Beta release blocker
No
### Summary
After upgrading from OpenClaw 2026.2.26 to 2026.5.4, the context display shows '?/131k' instead of actual token usage when using llama.cpp as the model provider. OpenClaw expects 'input_tokens' and 'output_tokens' fields but llama.cpp returns 'prompt_tokens' and 'completion_tokens'.
### Steps to reproduce
1. Run OpenClaw 2026.5.4 with llama.cpp server as model backend (running locally on port 8080)
2. Send a message through the Telegram channel
3. Check the session status display - context shows '?/131k' instead of actual token count
4. Verify the llama.cpp server returns usage with 'prompt_tokens' and 'completion_tokens' fields (OpenAI-compatible format)
### Expected behavior
In OpenClaw 2026.2.26, the context display showed actual token usage (e.g., '45/131k'). The system should correctly parse llama.cpp's 'prompt_tokens' and 'completion_tokens' fields and display the real-time token usage rate.
### Actual behavior
Context display shows '?/131k' (question mark instead of actual token count). OpenClaw fails to find the expected 'input_tokens' and 'output_tokens' fields because llama.cpp returns 'prompt_tokens' and 'completion_tokens' instead. This is the same issue reported in #53448 but still unfixed in 2026.5.4.
### OpenClaw version
2026.5.4
### Operating system
Linux Mint 22.1 (based on Ubuntu 24.04) - Linux 6.14.0-37-generic (x64)
### Install method
_No response_
### Model
llamacpp/Qwen3.6-35B-A3B-UD-IQ3_XXS.gguf
### Provider / routing chain
openclaw -> llamacpp (local llama-server on http://127.0.0.1:8080)
### Additional provider/model setup details
llama.cpp server running locally on port 8080 with OpenAI-compatible API format. Model: Qwen3.6-35B-A3B-UD-IQ3_XXS.gguf (131k context window). Configured in openclaw.json under models.providers.llamacpp.
### Logs, screenshots, and evidence
```

**Decision**

```json
{
  "id": "openclaw-openclaw-77992",
  "decision": "keep_easy",
  "final_labels": [
    "local_models",
    "local_model_providers",
    "model_serving",
    "telemetry_usage"
  ],
  "notes": "User reviewed and said this row is correct."
}
```

## openclaw-openclaw-80783 / #80783 — Policy: add model, network, and MCP conformance checks

- audit_reasons: `hosted_cloud_provider_not_local_model_provider`
- previous_expected_topics: `config, local_model_providers, mcp_tooling, security, skills_plugins`
- gpt55_labels: `config, local_model_providers, mcp_tooling, security, skills_plugins`
- possible_confusions: `docs`
- agreement_jaccard: `1.0`

**Rationales**
- `config`: PR adds policy.jsonc config-level conformance checks over existing OpenClaw settings and config evidence.
- `local_model_providers`: Adds model-provider evidence plus models.providers allow/deny policy support for configured providers and refs.
- `mcp_tooling`: Adds MCP server evidence and allow/deny checks for OpenClaw-managed MCP servers.
- `security`: Adds private-network SSRF posture checks and URL credential redaction in policy evidence.
- `skills_plugins`: Changes are in the bundled Policy plugin/extension and its doctor health-check registration.

**Excluded rationales**
- `docs`: Docs are updated, but they support the policy plugin feature rather than being the central change.

**Excerpt**

```markdown
# Policy: add model, network, and MCP conformance checks
Branch: `policy-conformance-examples`
GitHub base: `main`
Logical base: `main` after #80056 merged
Status: ready for maintainer review
## Summary
This PR extends the bundled Policy plugin with three additional config-level conformance areas: model providers and model refs, private-network SSRF settings, and OpenClaw-managed MCP servers.
Policy stays a read-only conformance layer over existing OpenClaw config:
- `policy.jsonc` defines authored requirements.
- OpenClaw config remains the source of truth for observed workspace state.
- Policy extracts evidence from existing settings.
- The Policy plugin registers doctor health checks for concrete authored rules.
- `doctor --lint` and `policy check` report drift without mutating config or runtime state.
- `policy check --json` emits the recordable audit tuple: `policyHash + evidenceHash + findingsHash + clean result -> attestationHash`.
This follows the channels and tools policy slices, but keeps the added areas read-only. It proves the shape works across several OpenClaw settings categories without adding runtime enforcement or duplicate registries.
## What Changed
- Added model-provider evidence to `policy check --json`: `modelProviders` and `modelRefs`.
- Added `models.providers.allow` and `models.providers.deny` policy support.
- Added `policy/models-denied-provider` and `policy/models-unapproved-provider`.
- Added network evidence to `policy check --json`.
- Added `network.privateNetwork.allow`.
- Added `policy/network-private-access-enabled`.
- Added MCP server evidence to `policy check --json`.
- Added `mcp.servers.allow` and `mcp.servers.deny` policy support.
- Added `policy/mcp-denied-server` and `policy/mcp-unapproved-server`.
- Updated policy CLI and plugin reference docs.
- Added tests for denied rules, allowlists, evidence extraction, and empty category namespaces.
## Policy Shape
```

**Decision**

```json
{
  "id": "openclaw-openclaw-80783",
  "decision": "fix_labels",
  "final_labels": [
    "config",
    "local_model_providers",
    "mcp_tooling",
    "security",
  ],
  "notes": "There is no mention of skills / plugins here."
}
```

## openclaw-openclaw-84549 / #84549 — fix(deepinfra): load all DeepInfra models when user wants to browse t…

- audit_reasons: `hosted_cloud_provider_not_local_model_provider`
- previous_expected_topics: `local_model_providers, model_serving, skills_plugins`
- gpt55_labels: `local_model_providers, model_serving, skills_plugins`
- possible_confusions: `api_surface`
- agreement_jaccard: `1.0`

**Rationales**
- `local_model_providers`: DeepInfra provider discovery is fixed to load models from an OpenAI-compatible /v1/openai/models endpoint with API-key gating and fallback catalogs.
- `model_serving`: Changes center on model catalog routing by surface and proxy behavior for DeepInfra/Anthropic model serving, including cache marker handling.
- `skills_plugins`: The work is scoped to the extensions/deepinfra plugin and registers model catalog providers within that extension.

**Excluded rationales**
- `api_surface`: Although an OpenAI-style endpoint is consumed, the PR does not primarily change OpenClaw's public HTTP API contract.

**Excerpt**

```markdown
# fix(deepinfra): load all DeepInfra models when user wants to browse t…
# fix(deepinfra): load all DeepInfra models when user wants to browse them during onboarding
## Summary
- **Problem**: DeepInfra plugin pinned the chat catalog to 7 hardcoded manifest entries (a wizard-vs-discovery guard short-circuited discovery once the auth wizard seeded models), had no live discovery seam for image-gen / video-gen, and silently dropped Anthropic `cache_control` markers when proxying `anthropic/*` models — prompt caching was advertised eligible but never fired.
- **Solution**: Wire DeepInfra's `/v1/openai/models?sort_by=openclaw&filter=with_meta` (the agent-tagged projection now shipping in the backend) through a per-surface helper that buckets responses by short-alias tag (`chat`/`vlm`/`embed`/`image-gen`/`video-gen`/`tts`/`stt`). Register live image-gen and video-gen catalogs via `registerModelCatalogProvider` (OpenRouter pattern). Replace the OpenRouter-only Anthropic cache wrapper with a deepinfra-local one gated on the model id.
- **What changed**: new `surface-model-catalogs.ts` (live image-gen + video-gen catalog providers + `resolveModelCapabilities`); new `cache-wrapper.ts` (Anthropic ephemeral cache marker injection for `anthropic/*` on DeepInfra); refactored `provider-models.ts` (per-surface bucketed discovery, API-key gated, 5-min cache, sync static fallback); media-provider builders now accept the per-surface catalog; `index.ts` feeds all media surfaces from one source + registers the new catalog providers; `media-models.ts` `DEFAULT_*` constants demoted to `*_FALLBACK_MODELS`.
- **Scope boundary**: No edits outside `extensions/deepinfra/`. No SDK changes (`src/plugin-sdk/provider-entry.ts` is byte-identical to `main`). TTS/STT/VLM/embed surfaces still use static fallback only — extending `UnifiedModelCatalogKind` to cover them is a separate SDK PR.
## Motivation
DeepInfra ships hundreds of models, but openclaw only surfaced 7 hardcoded chat IDs — every new model needed a code change here. The DeepInfra backend now emits surface-tagged responses on `/v1/openai/models?sort_by=openclaw&filter=with_meta`, so the plugin can map tags → surfaces dynamically. Anthropic prompt caching on DeepInfra was also silently broken: the runner advertised eligibility but the OpenRouter-only stream wrapper short-circuited on `provider !== "openrouter"`, so `cache_control` markers never went out.
## Change Type
- [x] Bug fix
- [x] Feature
- [x] Refactor required for
[body 
```

**Decision**

```json
{
  "id": "openclaw-openclaw-84549",
  "decision": "fix_labels",
  "final_labels": [
    "model_serving",
    "config"
  ],
  "notes": "Only apply the `skills_plugin` if there is a specific change to that area (a mention of a review skill is not alone enough). config label applies as this PR addresses a configuration failure/bypass"
}
```

## openclaw-openclaw-84997 / #84997 — [AI-assisted] Add NEAR AI Cloud provider

- audit_reasons: `hosted_cloud_provider_not_local_model_provider`
- previous_expected_topics: `auth_identity, local_model_providers`
- gpt55_labels: `local_model_providers, auth_identity`
- possible_confusions: `api_surface`
- agreement_jaccard: `1.0`

**Rationales**
- `local_model_providers`: Adds a bundled OpenAI-compatible `nearai` provider with base URL, model catalog discovery, fallback catalog, and provider compatibility metadata.
- `auth_identity`: Adds API-key onboarding and token configuration for `NEARAI_API_KEY` as part of the provider setup.

**Excluded rationales**
- `api_surface`: Although API/contracts are mentioned, the PR explicitly says there are no generic Gateway transport changes; it is provider integration on existing APIs.

**Excerpt**

```markdown
# [AI-assisted] Add NEAR AI Cloud provider
## Summary
- Problem: OpenClaw does not currently expose NEAR AI Cloud as a bundled model provider.
- Solution: Adds a bundled `nearai` provider plugin for NEAR AI Cloud's OpenAI-compatible API at `https://cloud-api.near.ai/v1`.
- What changed: Adds API-key onboarding for `NEARAI_API_KEY`, dynamic public model catalog discovery with a static fallback, OpenAI-compatible replay/compat metadata, provider docs, generated plugin inventory entries, and focused tests.
- What did NOT change (scope boundary): No generic Gateway transport changes and no live provider use unless a user explicitly configures NEAR AI Cloud.
- Review note: AI-assisted.
## Motivation
- Users can configure NEAR AI Cloud TEE-backed inference through the same provider onboarding and model catalog surfaces as other bundled OpenAI-compatible providers.
## Change Type (select all)
- [ ] Bug fix
- [x] Feature
- [ ] Refactor required for the fix
- [x] Docs
- [ ] Security hardening
- [x] Chore/infra
## Scope (select all touched areas)
- [ ] Gateway / orchestration
- [ ] Skills / tool execution
- [x] Auth / tokens
- [ ] Memory / storage
- [x] Integrations
- [x] API / contracts
- [x] UI / DX
- [x] CI/CD / infra
## Linked Issue/PR
- Closes #
- Related #
```

**Decision**

```json
{
  "id": "openclaw-openclaw-84997",
  "decision": "fix_labels",
  "final_labels": [
    "model_serving",
    "auth_identity"
  ],
  "notes": "NearAI is a cloud hosted (not local) model provider so local_model_providers does not apply."
}
```

## openclaw-openclaw-88400 / #88400 — fix(config): accept overlays for bundled provider aliases

- audit_reasons: `hosted_cloud_provider_not_local_model_provider`
- previous_expected_topics: `config, local_model_providers`
- gpt55_labels: `config, local_model_providers`
- possible_confusions: `tests_ci`
- agreement_jaccard: `1.0`

**Rationales**
- `config`: PR changes the OpenClaw config schema allowlist so provider overlay aliases validate without baseUrl or models.
- `local_model_providers`: The fix is specifically about model provider aliases and lightweight provider overlay configuration.

**Excluded rationales**
- `tests_ci`: Regression tests are added, but the central change is provider config schema behavior, not CI or test infrastructure.

**Excerpt**

```markdown
# fix(config): accept overlays for bundled provider aliases
## Summary
- Allow bundled provider aliases to be configured as lightweight provider overlays without `baseUrl` or `models`.
- Add the reviewer-identified bundled overlay aliases to the schema allowlist: `azure-openai-responses`, `moonshotai`, `moonshot-ai`, `z.ai`, and `z-ai`.
- Extend regression coverage for timeout-only overlays using those aliases.
## Real behavior proof (required for external PRs)
- Behavior or issue addressed: bundled provider overlay aliases were rejected as custom providers when present in plugin manifests/catalogs but absent from the schema allowlist.
- Real environment tested: local OpenClaw source checkout on this branch, exercising the production `OpenClawSchema` path.
- Exact steps or command run after this patch:
  ```bash
  node --import tsx --input-type=module --eval 'import { OpenClawSchema } from "./src/config/zod-schema.js"; const aliases = ["azure-openai-responses", "moonshotai", "moonshot-ai", "z.ai", "z-ai"]; const failures = aliases.filter((id) => !OpenClawSchema.safeParse({ models: { providers: { [id]: { timeoutSeconds: 600 } } } }).success); if (failures.length) { console.error(`failed: ${failures.join(", ")}`); process.exit(1); } console.log(`OpenClawSchema safeParse accepted timeout-only overlays: ${aliases.join(", ")}`);'
  ```
- Evidence after fix:
  ```text
  OpenClawSchema safeParse accepted timeout-only overlays: azure-openai-responses, moonshotai, moonshot-ai, z.ai, z-ai
  ```
- Observed result after fix: the production OpenClaw config schema accepts timeout-only overlays for all five reviewer-identified bundled aliases without requiring `baseUrl` or `models`.
- What was not tested: live provider API calls; this proof exercises config schema validation for bundled-provider overlay acceptance.
## Tests and validation
- `node scripts/run-vitest.mjs run src/config/zod-schema.models.test.ts`: passed, 17 tests
- `pnpm exec oxfmt --check src/config/zod-schema.core.ts src/config/zod-schema.models.test.ts`: passed
- model catalog provider/alias parity check: missing from overlay allowlist `(none)`
- `git diff --check`: passed
Labels: size: XS, triage: blank-template, proof: supplied, proof: sufficient, P2, rating: 🐚 platinum hermit, status: 👀 ready for maintainer look
```

**Decision**

```json
{
  "id": "openclaw-openclaw-88400",
  "decision": "fix_labels",
  "final_labels": [
    "config",
    "model_serving"
  ],
  "notes": "this is not specific to local models. this is about configuration of model_serving providers."
}
```

## openclaw-openclaw-88816 / #88816 — [Bug]: v2026.05.28 breaks Google Vertex Express API Key

- audit_reasons: `hosted_cloud_provider_not_local_model_provider`
- previous_expected_topics: `auth_identity, config, local_model_providers`
- gpt55_labels: `auth_identity, config, local_model_providers`
- possible_confusions: `reliability`
- agreement_jaccard: `1.0`

**Rationales**
- `auth_identity`: Issue is specifically about Google Vertex Express API key auth via auth-profile.json.
- `config`: Failure depends on openclaw.json and auth-profile.json provider/model configuration after upgrade.
- `local_model_providers`: Error is unable to resolve/register the google-vertex model provider and its models[].

**Excluded rationales**
- `reliability`: Although a regression, the actionable area is provider/auth configuration rather than generic crash, retry, or recovery behavior.

**Excerpt**

```markdown
# [Bug]: v2026.05.28 breaks Google Vertex Express API Key
### Bug type
Regression (worked before, now fails)
### Beta release blocker
No
### Summary
Updating from v2026.5.20 and v2026.5.28 completely breaks OpenClaw when using Google Vertex when using an API key. If I roll back to v2026.5.20 it works fine again. OpenClaw throws an error about being unable to find a model provider
> All models failed (2): google-vertex/gemini-2.5-pro: Unknown model: google-vertex/gemini-2.5-pro. Found agents.defaults.models["google-vertex/gemini-2.5-pro"], but no matching models.providers["google-vertex"].models[] entry. Add { "id": "gemini-2.5-pro" } to models.providers["google-vertex"].models[] to register this provider model.
The moment I downgrade back to v2026.5.20 it starts working again.
### Steps to reproduce
1. Start OpenClaw v2026.5.20 with the below config using Google Vertex AI Express API key (not ADC)
2. Everything should work
3.  Update to v2026.5.28 and OpenClaw won't respond to any requests and will throw an error
4. 4. Downgrade back to 2026.5.20 and it starts working again
This is my the starting of `openclaw.json`:
```

**Decision**

```json
{
  "id": "openclaw-openclaw-88816",
  "decision": "fix_labels",
  "final_labels": [
    "auth_identity",
    "config",
    "model_serving"
  ],
  "notes": "Google Vertex Express is not a local_model_provider, it is a hosted service so model_serving applies"
}
```

## openclaw-openclaw-39248 / #39248 — Bug: sandbox.mode: "non-main" silently breaks sessions_spawn subagent initialization

- audit_reasons: `teacher_previous_label_disagreement`
- previous_expected_topics: `coding_agents, reliability, sandboxing, sessions`
- gpt55_labels: `coding_agents, agent_runtime, sessions, sandboxing, reliability`
- possible_confusions: `gateway`
- agreement_jaccard: `0.8`

**Rationales**
- `coding_agents`: Issue affects subagent orchestration in the coding-agent workflow via sessions_spawn.
- `agent_runtime`: Subagents are accepted but never initialize or execute, a core agent lifecycle/runtime failure.
- `sessions`: The failure centers on sessions_spawn, childSessionKey, sessions_history, transcripts, and session state.
- `sandboxing`: The bug is triggered by agents.defaults.sandbox.mode="non-main" and Docker sandbox initialization.
- `reliability`: Symptoms include silent stalls, missing logs, no progress, and eventual timeout.

**Excluded rationales**
- `gateway`: Gateway restart and logs are mentioned, but the failing behavior is subagent sandbox/session initialization, not gateway API or daemon health.

**Excerpt**

```markdown
## Summary
When `agents.defaults.sandbox.mode` is set to `"non-main"`, sub-agents spawned via `sessions_spawn` fail to initialize. Sessions are accepted (return valid `childSessionKey` and `runId`) but never start executing — zero tokens, zero messages, no transcript files created. **No errors appear in gateway logs.**
## Environment
- OpenClaw Version: 2026.3.2 (85377a2)
- OS: macOS 15.3.0 (Apple Silicon, arm64)
- Node: v25.8.0
- Docker Desktop: running (coding agent sandbox works fine)
## Steps to Reproduce
1. Set `agents.defaults.sandbox.mode: "non-main"` in config
2. Restart gateway
3. From main agent, spawn a sub-agent:
   ```
   sessions_spawn(task="Reply with: test", model="sonnet")
   ```
4. Check `sessions_history` or `subagents list` after 30+ seconds
## Expected Behavior
Sub-agent starts within seconds, `systemSent: true`, tokens accumulate, task completes.
## Actual Behavior
- `sessions_spawn` returns `status: "accepted"` with valid session key
- Sub-agent appears in `subagents list` as `running`
- `sessions_history` returns `messages: []` indefinitely
- No transcript file created on disk
- `systemSent` never set to `true`
- `totalTokens` never set
- **Zero error output in gateway logs**
- Eventually times out via `runTimeoutSeconds`
## Bisect Results
Systematically tested with a simple one-line task (`Reply with exactly: ...`):
```

**Decision**

```json
{
  "id": "openclaw-openclaw-39248",
  "decision": "fix_labels",
  "final_labels": [
    "agent_runtime",
    "sessions",
    "sandboxing",
    "reliability"
  ],
  "notes": "it is not coding_agents as this applies to openclaw internal subagents rather than external tools."
}
```

## openclaw-openclaw-43246 / #43246 — fix(message): deny same-provider cross-context sends by default [AI-assisted]

- audit_reasons: `prior_benchmark_worst_failure`
- previous_expected_topics: `chat_integrations, config, notifications, security`
- gpt55_labels: `chat_integrations, config, notifications, security`
- possible_confusions: `tool_calling`
- agreement_jaccard: `1.0`

**Rationales**
- `chat_integrations`: The fix targets Slack, WhatsApp, iMessage, and similar provider/channel conversation routing.
- `config`: Behavior is controlled by the new default/opt-in setting `tools.message.crossContext.allowWithinProvider=true` and config help/type updates.
- `notifications`: Core change is an outbound message delivery policy that blocks cross-context sends by default.
- `security`: PR explicitly hardens a security boundary to prevent cross-channel/context data leaks.

**Excluded rationales**
- `tool_calling`: Although a model-supplied message tool target is involved, the change is policy/config for outbound delivery rather than tool-call protocol or schema behavior.

**Excerpt**

```markdown
## Summary
- Problem: bound `message` tool sends could still hop to a different target on the same provider by default if the model supplied an explicit `target`
- Why it matters: this allows cross-channel/context leaks on Slack, WhatsApp, iMessage, and other providers that share the outbound policy path
- What changed: same-provider cross-context sends are now denied by default; operators must opt in with `tools.message.crossContext.allowWithinProvider=true`
- What did NOT change (scope boundary): cross-provider behavior, explicit legacy override `tools.message.allowCrossContextSend`, and existing cross-context marker behavior
## Change Type (select all)
- [x] Bug fix
- [ ] Feature
- [ ] Refactor
- [x] Docs
- [x] Security hardening
- [ ] Chore/infra
## Scope (select all touched areas)
- [x] Gateway / orchestration
- [x] Skills / tool execution
- [ ] Auth / tokens
- [ ] Memory / storage
- [x] Integrations
- [x] API / contracts
- [ ] UI / DX
- [ ] CI/CD / infra
## Linked Issue/PR
- Closes #43245
- Related #2412
- Related #2414
- Related #10838
## User-visible / Behavior Changes
Bound `message` tool sends are now constrained to the active conversation by default even within the same provider. To intentionally forward from one Slack/WhatsApp/iMessage/etc. conversation to another on the same provider, set `tools.message.crossContext.allowWithinProvider=true`.
```

**Decision**

```json
{
  "id": "openclaw-openclaw-43246",
  "decision": "fix_labels",
  "final_labels": [
    "chat_integrations",
    "config",
    "tool_calling",
    "security"
  ],
  "notes": "tool_calling applies as this relates to how tools are used. security as this relates to potential leakage. "
}
```

## openclaw-openclaw-44202 / #44202 — [Bug]: local memory embeddings on Apple Silicon can crash gateway in ggml-metal / node-llama-cpp; need official Metal/GPU guidance

- audit_reasons: `teacher_previous_label_disagreement`
- previous_expected_topics: `gateway, local_models, memory, reliability`
- gpt55_labels: `gateway, local_models, self_hosted_inference, memory, reliability`
- possible_confusions: `open_weight_models`
- agreement_jaccard: `0.8`

**Rationales**
- `gateway`: The reported failure repeatedly crashes the OpenClaw gateway during restart/shutdown.
- `local_models`: The crash is in local GGUF/node-llama-cpp/ggml-metal execution on Apple Silicon GPU/Metal.
- `self_hosted_inference`: The issue centers on locally operated embedding inference via a local memory provider.
- `memory`: Local memory embeddings, memory search, indexing, chunks, and vector readiness are central to the report.
- `reliability`: It describes crash loops, native assertions, recovery steps, and mitigations for a restart/shutdown failure.

**Excluded rationales**
- `open_weight_models`: A Hugging Face GGUF embedding model is named, but the bug is about runtime crashes and embeddings, not model release or packaging.

**Excerpt**

```markdown
## Summary
Local memory embeddings on macOS Apple Silicon can crash the gateway in the `node-llama-cpp` / `ggml-metal` path during restart/shutdown, even when the main chat model is healthy.
This report is being filed by `@samersaibot` on behalf of Samer Haddad after reproducing and recovering the issue on a Mac Studio. We are also asking for guidance on the ideal supported path for **GPU-backed local embeddings on Apple Silicon**, because the stable recovery we reached required disabling the Metal path for embeddings.
## Environment
- OpenClaw: `2026.3.11`
- Install method: global npm/homebrew-style install under `/opt/homebrew/lib/node_modules/openclaw`
- OS: macOS Apple Silicon (Mac Studio, 64 GB RAM)
- Gateway service: LaunchAgent (`ai.openclaw.gateway`)
- Node seen by CLI: `v25.6.1`
- LaunchAgent runtime node: `/opt/homebrew/opt/node@22/bin/node` (`v22.22.0`)
- Main model: `openai-codex/gpt-5.4`
- Memory provider: `local`
- Local embedding model: `hf:ggml-org/embeddinggemma-300m-qat-q8_0-GGUF/embeddinggemma-300m-qat-Q8_0.gguf`
- Vector store: sqlite-vec (`vec0.dylib`)
## What happened
1. Main model config was fixed successfully and the gateway itself was healthy.
2. With local memory embeddings enabled, the gateway repeatedly hit a native assertion in the local embedding runtime.
3. The crash was in `ggml-metal` / `node-llama-cpp`, not the main model path.
4. Temporary recovery was achieved by disabling memory search and reinstalling the LaunchAgent.
5. Local memory was later restored with two mitigations:
   - sequential local embed batch generation (to avoid known `Promise.all` deadlock risk, related to #7547)
   - forcing the local embedding runtime to CPU-only (disabling the Metal/GPU path for embeddings)
6. After that recovery, local memory became operational again:
   - indexed `25/25` files
   - `111` chunks
   - embeddings/vector/fts all `ready`
So the current system is usable again, but **the only stable local recovery we found was to avoid the Metal path for embeddings**.
## Actual crash evidence
```

**Decision**

```json
{
  "id": "openclaw-openclaw-44202",
  "decision": "fix_labels",
  "final_labels": [
    "local_models",
    "self_hosted_inference",
    "memory",
    "reliability"
  ],
  "notes": "this issue mentions the gateway as a diagnostic point not a root cause so was removed."
}
```

## openclaw-openclaw-45841 / #45841 — [Feature]: Sandboxing + ACP

- audit_reasons: `repeated_prior_benchmark_failure`
- previous_expected_topics: `acp, sandboxing, security, sessions`
- gpt55_labels: `acp, sandboxing, security, sessions`
- possible_confusions: `api_surface`
- agreement_jaccard: `1.0`

**Rationales**
- `acp`: Issue is explicitly about enabling sandboxed OpenClaw sessions to spawn and control ACP sessions.
- `sandboxing`: Core problem is ACP compatibility when OpenClaw runs inside Docker/container sandboxes.
- `security`: Motivation centers on preserving isolation, limiting host access, and using an auditable opt-in bridge.
- `sessions`: The requested behavior concerns sandboxed sessions using sessions_spawn/spawn-steer-cancel for ACP sessions.

**Excluded rationales**
- `api_surface`: A narrow bridge API is proposed, but the main routing issue is ACP across sandbox/security/session boundaries, not general API contracts.

**Excerpt**

```markdown
### Summary
Sandboxed OpenClaw sessions should be able to spawn ACP sessions.
It's currently a [documented limitation](https://docs.openclaw.ai/tools/acp-agents#sandbox-compatibility) that breaks the use of 2 very important openclaw features - sandboxing and ACP.
ACP is great for better interop with coding harnesses, while sandboxing reduces blast radius when they make mistakes!
Continuation of #32935
### Problem to solve
Users running OpenClaw inside Docker containers (sandboxed) cannot use ACP at all. Sandboxed sessions cannot spawn ACP sessions because runtime='acp' runs on the host. This forces a binary choice: give up sandboxing (weakening security) or give up ACP orchestration (losing the ability to control Claude Code, Codex, etc. from within OpenClaw). For users who run OpenClaw in Docker for security isolation but want to orchestrate coding agents on the host, there's no middle ground.
### Proposed solution
Options:
1. Allow running ACP boxes in their own sandboxes, similar to sub-agents - re-use the same docker-based spawning method.
2. Allow running ACP INSIDE the session/bot sandboxes - they're already sandboxed, but ACP provides the neat interop layer.
3. Introduce a controlled bridge/proxy mechanism that lets sandboxed sessions request ACP spawns through a narrow, auditable API surface  - ACP proxy daemon on the host that accepts spawn/steer/cancel requests from the sandboxed container over a Unix socket or localhost port, with allowlisting by agent ID and rate limiting.  - sandbox: "bridge" mode for sessions_spawn that explicitly opts into host-side ACP execution with logged privilege escalation, so operators can audit what crossed the boundary.  - Config flag like acp.allowFromSandbox: true (with appropriate warnings) that relaxes the current blanket block for users who accept the tradeoff. A proxy/bridge approach would preserve the security boundary while enabling the orchestration use case. The key constraint: the bridge should be opt-in, auditable, and narrowly scoped (only ACP spawn/steer/cancel, not general host access).- borrowed from: #32935
### Alternatives considered
• Running OpenClaw unsandboxed: works but removes the security benefits of containerization entirely.
• Ditching ACP - I keep the security of sandboxes, and run coding harnesses inside existing sandbox, but no ACP interop.
• Using runtime: "subagent" instead: works for OpenClaw-native tasks but doesn't support external coding harnesses (Claude Code, Codex, G
[body trun
```

**Decision**

```json
{
  "id": "openclaw-openclaw-45841",
  "decision": "keep_easy",
  "final_labels": [
    "acp",
    "sandboxing",
    "security",
    "sessions"
  ],
  "notes": "User reviewed and said this row is correct."
}
```

## openclaw-openclaw-47083 / #47083 — fix: respect totalTokensFresh flag to avoid showing stale token counts

- audit_reasons: `repeated_prior_benchmark_failure`
- previous_expected_topics: `sessions, telemetry_usage, ui_tui`
- gpt55_labels: `sessions, telemetry_usage, ui_tui`
- possible_confusions: `api_surface`
- agreement_jaccard: `1.0`

**Rationales**
- `sessions`: Fix concerns session list/session info rows and a per-session totalTokensFresh state flag.
- `telemetry_usage`: Central behavior is whether token counts/usage totals are displayed when fresh versus stale.
- `ui_tui`: Changes directly affect both TUI and Web UI presentation of session token counts.

**Excluded rationales**
- `api_surface`: Although client types add totalTokensFresh, the PR consumes an existing gateway field rather than changing an HTTP endpoint contract.

**Excerpt**

```markdown
## Problem
When a session's `totalTokensFresh` flag is `false`, the `totalTokens` value may be stale/historical (e.g., accumulated from previous compaction) and should not be displayed.
This caused incorrect displays like "100% context used 2.6M / 200k" in both TUI and Web UI when the token count was stale.
## Root Cause
The Gateway already correctly filters stale token counts via `resolveFreshSessionTotalTokens`, but:
1. **TUI**: Type definition was missing `totalTokensFresh` field, so TUI couldn't check it
2. **UI**: `formatSessionTokens` function didn't check the freshness flag
## Solution
### TUI (commit 368ca03f1)
- Add `totalTokensFresh` to `GatewaySessionList` type in `gateway-chat.ts`
- Add `totalTokensFresh` to `SessionInfoEntry` type in `tui-session-actions.ts`
- Check `totalTokensFresh !== false` before updating `sessionInfo.totalTokens`
### UI (commit 446fdd13a)
- Add `totalTokensFresh` to `GatewaySessionRow` type in `types.ts`
- Check `totalTokensFresh === false` in `formatSessionTokens` function, return "n/a" when stale
## Testing
- TypeScript compilation passes for both TUI and UI
- The fix ensures stale token counts are not displayed in sessions list
## Files Changed
- `src/tui/gateway-chat.ts` - Add `totalTokensFresh` to type definition
- `src/tui/tui-session-actions.ts` - Add type and check before using `totalTokens`
- `ui/src/ui/types.ts` - Add `totalTokensFresh` to type definition
- `ui/src/ui/presenter.ts` - Check freshness before displaying tokens
```

**Decision**

```json
{
  "id": "openclaw-openclaw-47083",
  "decision": "keep_easy",
  "final_labels": [
    "sessions",
    "telemetry_usage",
    "ui_tui"
  ],
  "notes": "User reviewed and said this row is correct."
}
```

## openclaw-openclaw-51654 / #51654 — Support session-level environment variables for ACP sessions

- audit_reasons: `teacher_previous_label_disagreement`
- previous_expected_topics: `acp, acpx, auth_identity, sessions`
- gpt55_labels: `acp, acpx, sessions, auth_identity, security`
- possible_confusions: `config`
- agreement_jaccard: `0.8`

**Rationales**
- `acp`: The feature targets ACP sessions and adds an env parameter to sessions_spawn with runtime "acp".
- `acpx`: The issue says ACP sessions run via the acpx runtime and require injecting env vars into the acpx subprocess.
- `sessions`: The requested behavior is session-specific or per-spawn environment variables and preserved OpenClaw session management.
- `auth_identity`: Primary use cases include different API keys, auth provider endpoints, and temporary scoped credentials per session.
- `security`: The issue explicitly involves multi-tenant environment isolation and credential handling, with security-review labels.

**Excluded rationales**
- `config`: Although environment variables are mentioned, the change is per-session runtime state rather than general config files, defaults, or migration.

**Excerpt**

```markdown
## Feature Request: Session-level environment variables for ACP sessions
### Problem Statement
Currently, ACP sessions (via acpx runtime) inherit environment variables directly from the parent OpenClaw gateway process. There is no way to set session-specific or per-spawn environment variables.
This is problematic when:
1. Different sessions need different API keys or endpoint configurations
2. Users want to test different models/providers in isolated sessions
3. Multi-tenant or multi-user scenarios require environment isolation
### Desired Behavior
Ability to pass environment variables when spawning an ACP session, for example:
```

**Decision**

```json
{
  "id": "openclaw-openclaw-51654",
  "decision": "fix_labels",
  "final_labels": [
    "acp",
    "acpx",
    "sessions",
    "security"
  ],
  "notes": "auth_identity is intended to be used for direct auth issues or identity issues with openclaw, rather than a general term."
}
```

## openclaw-openclaw-52249 / #52249 — ACP parent session stuck until refresh when yielded waiting for child completion

- audit_reasons: `repeated_prior_benchmark_failure`
- previous_expected_topics: `acp, queueing, reliability, sessions`
- gpt55_labels: `acp, sessions, queueing, reliability`
- possible_confusions: `agent_runtime`
- agreement_jaccard: `1.0`

**Rationales**
- `acp`: Issue is explicitly about ACP child sessions, ACP parent-stream relay, and ACP yield/resume behavior.
- `sessions`: Core failure is parent/child session state: yielded parent remains stuck after child completion and needs proper yield-wait tracking.
- `queueing`: Fix routes child-completion follow-ups through enqueueSystemEvent and heartbeat wake scheduling instead of direct resume.
- `reliability`: Describes a wedged/non-responsive state and recovery problem where manual refresh is required to unblock the parent.

**Excluded rationales**
- `agent_runtime`: Although child completion and heartbeat are runtime-adjacent, the issue is specifically ACP session wake/state handling rather than general runner orchestration.

**Excerpt**

```markdown
When an ACP child session completes while a parent session is yielded waiting for the result, the parent session remains stuck/non-responsive until the user manually refreshes the UI.
Root cause: The ACP parent-stream relay was using transcript inspection (`isYieldedParentAwaitingResume()`) and direct gateway re-entry (`resumeYieldedParent()`) instead of the normal system-event + heartbeat wake path. This ad-hoc resumption path can leave parent session state wedged.
## Steps to Reproduce
1. Open control-ui or web chat
2. Spawn ACP child: `sessions_spawn({ runtime: "acp", agentId: "codex", task: "..." })`
3. Yield parent: `sessions_yield()`
4. Wait for child to complete
5. **Observe:** Parent session appears stuck, not responsive
6. **Verify:** Manual refresh required to unblock chat
## Expected Behavior
Parent session automatically resumes when child completes, without manual intervention.
## Root Cause
In `src/acp/parent-stream-relay.ts` (compiled to `dist/auth-profiles-CCgh0vEZ.js`):
The `emitOrResume(...)` helper was doing:
```

**Decision**

```json
{
  "id": "openclaw-openclaw-52249",
  "decision": "keep_easy",
  "final_labels": [
    "acp",
    "sessions",
    "queueing",
    "reliability"
  ],
  "notes": "User reviewed and said this row is correct."
}
```

## openclaw-openclaw-52747 / #52747 — fix(acp): time out stuck session lane tasks

- audit_reasons: `teacher_previous_label_disagreement`
- previous_expected_topics: `acp, queueing, reliability, sessions`
- gpt55_labels: `acp, sessions, queueing, reliability, config`
- possible_confusions: `acpx`
- agreement_jaccard: `0.8`

**Rationales**
- `acp`: Title and changed files explicitly fix ACP control-plane session lane behavior.
- `sessions`: The issue is a stuck ACP session/load or initializeSession flow tied to a session lane.
- `queueing`: Problem states the stuck lane blocks subsequent queued tasks; fix releases it and dequeues the next task.
- `reliability`: Adds timeout recovery for hung tasks to prevent wedged lanes and availability loss.
- `config`: Adds acp.sessionLane.taskTimeoutMs with defaulting and schema validation.

**Excluded rationales**
- `acpx`: ACPX files are touched, but the described behavior is ACP session-lane timeout, not ACPX protocol or transport.

**Excerpt**

```markdown
## Problem
When an ACP session gets stuck (e.g. Gemini CLI `session/load` fails), it holds the session lane forever, blocking all subsequent tasks from dequeuing and executing.
## Solution
Add a configurable `taskTimeoutMs` to the session lane. When a task exceeds this timeout:
1. The task is marked as failed with an `AcpRuntimeError`
2. The lane is released
3. The next queued task is automatically dequeued and executed
### Configuration
```

**Decision**

```json
{
  "id": "openclaw-openclaw-52747",
  "decision": "keep_easy",
  "final_labels": [
    "acp",
    "sessions",
    "queueing",
    "reliability",
    "config"
  ],
  "notes": "this is correct, config is debatable"
}
```

## openclaw-openclaw-55790 / #55790 — sessions_spawn(runtime="subagent") ignores inherited/per-agent subagent thinking defaults and initializes children at low

- audit_reasons: `teacher_previous_label_disagreement, low_previous_label_jaccard`
- previous_expected_topics: `coding_agents, config, sessions`
- gpt55_labels: `coding_agents, agent_runtime, sessions, config`
- possible_confusions: `acp`
- agreement_jaccard: `0.75`

**Rationales**
- `coding_agents`: Bug concerns subagent orchestration via sessions_spawn in an agent workflow.
- `agent_runtime`: The failing path is runtime="subagent" child spawning and initialization behavior.
- `sessions`: Issue centers on spawned parent/child sessions and their recorded thinking_level_change state.
- `config`: Expected behavior depends on resolving configured agent thinkingDefault and subagents.thinking defaults.

**Excluded rationales**
- `acp`: Although sessions_spawn is named, the report is about OpenClaw subagent default resolution, not ACP protocol/session compatibility.

**Excerpt**

```markdown
### Bug type
Regression / runtime bug
### Summary
`sessions_spawn(runtime="subagent")` appears to ignore documented subagent thinking inheritance/defaults and initializes spawned sessions with `thinkingLevel: low`.
On this install:
- parent session thinking is `high`
- per-agent `subagents.thinking` is `high`
- target agent `thinkingDefault` may also be `high`
- but spawned `runtime="subagent"` sessions still begin with `thinking_level_change ... low`
An explicit `sessions_spawn(..., thinking: "high")` **does** work, so the failure appears to be in the inherited/default resolution path, not in the thinking system generally.
### Steps to reproduce
Config excerpt:
```

**Decision**

```json
{
  "id": "openclaw-openclaw-55790",
  "decision": "fix_labels",
  "final_labels": [
    "agent_runtime",
    "sessions",
    "config"
  ],
  "notes": "this is not coding_agents as it does not directly involve external coding agents such as gemini, codex etc. "
}
```

## openclaw-openclaw-60979 / #60979 — feature: sessions_spawn ACP delivery to channel (stream output to Zulip/Discord topic)

- audit_reasons: `repeated_prior_benchmark_failure`
- previous_expected_topics: `acp, chat_integrations, notifications, sessions`
- gpt55_labels: `acp, sessions, chat_integrations, notifications`
- possible_confusions: `cron_automation`
- agreement_jaccard: `1.0`

**Rationales**
- `acp`: Request is specifically for `sessions_spawn` with `runtime="acp"` and ACP session output behavior.
- `sessions`: Feature concerns spawned session output binding and delivery for `sessions_spawn`.
- `chat_integrations`: Desired target is a Zulip/Discord channel conversation or topic via channel plugins.
- `notifications`: Core request is a `delivery.mode: "announce"` style channel delivery path for session output.

**Excluded rationales**
- `cron_automation`: Cron delivery is cited only as precedent; the feature is for ACP session spawning, not scheduled jobs.

**Excerpt**

```markdown
## Summary
When spawning an ACP session via `sessions_spawn` (e.g. OpenCode/Codex), there is no way to direct the session's output to a specific channel conversation or topic. This makes it impossible to observe long-running agent tasks in real-time from a chat surface without the parent agent acting as a relay.
## Desired Workflow
```

**Decision**

```json
{
  "id": "openclaw-openclaw-60979",
  "decision": "keep_easy",
  "final_labels": [
    "acp",
    "sessions",
    "chat_integrations",
    "notifications"
  ],
  "notes": "notifications is present because of the announce"
}
```

## openclaw-openclaw-69256 / #69256 — fix(cron): prevent premature session cleanup when subagents are running

- audit_reasons: `teacher_previous_label_disagreement`
- previous_expected_topics: `coding_agents, cron_automation, reliability, sessions`
- gpt55_labels: `cron_automation, sessions, agent_runtime, coding_agents, reliability`
- possible_confusions: `gateway`
- agreement_jaccard: `0.8`

**Rationales**
- `cron_automation`: The fix is in isolated cron delivery cleanup for jobs using deleteAfterRun.
- `sessions`: Core behavior is deferring sessions.delete so the cron run session is not removed prematurely.
- `agent_runtime`: The guard checks active descendant/subagent runs to preserve parent-worker orchestration lifecycle.
- `coding_agents`: The broken workflow is an orchestrator-worker agent pipeline where subagents must report back to the parent.
- `reliability`: This is a regression bug fix preventing orphaned workers and premature cleanup during active runs.

**Excluded rationales**
- `gateway`: Although callGateway invokes sessions.delete, the change is not about gateway routes, daemon startup, or service health.

**Excerpt**

```markdown
## Summary
- **Problem**: Isolated cron sessions with `deleteAfterRun: true` are being deleted prematurely during a run if a "Direct Delivery" (structured content or threaded reply) is triggered, even if subagents (workers) are still active.
- **Why it matters**: In orchestrator-worker patterns, the parent agent must survive to receive and aggregate results from its subagents. Premature cleanup orphans the workers and creates a fresh, context-less session, breaking the pipeline.
- **What changed**: Modified `cleanupDirectCronSessionIfNeeded` in `delivery-dispatch.ts` to check `countActiveDescendantRuns` before executing `sessions.delete`.
- **What did NOT change**: The cleanup logic for standard text-only deliveries (which already had subagent awareness via `finalizeTextDelivery`) was not altered.
## Change Type (select all)
- [x] Bug fix
- [ ] Feature
- [ ] Refactor required for the fix
- [ ] Docs
- [ ] Security hardening
- [ ] Chore/infra
## Scope (select all touched areas)
- [x] Gateway / orchestration
- [ ] Skills / tool execution
- [ ] Auth / tokens
- [ ] Memory / storage
- [ ] Integrations
- [ ] API / contracts
- [ ] UI / DX
- [ ] CI/CD / infra
## Linked Issue/PR
- Related #67807
- [x] This PR fixes a bug or regression
## Root Cause (if applicable)
- **Root cause**: PR #67807 introduced automated session cleanup in the `finally` block of `deliverViaDirectAndCleanup` but missed the subagent-counting guardrail that exists in the sibling `finalizeTextDelivery` path.
- **Missing detection / guardrail**: Lack of `countActiveDescendantRuns` verification in the Direct Delivery cleanup wrapper.
- **Contributing context**: Complex workflows using Feishu or threaded replies trigger the `useDirectDelivery` path, bypassing the subagent waiting orchestration.
```

**Decision**

```json
{
  "id": "openclaw-openclaw-69256",
  "decision": "fix_labels",
  "final_labels": [
    "cron_automation",
    "sessions",
    "agent_runtime",
    "queueing",
    "reliability"
  ],
  "notes": "coding_agents does not apply as it is not directly referring to external tool integrations. queueing applies as it relates to lock/orchestration type activities"
}
```

## openclaw-openclaw-70002 / #70002 — ci: skip docs sync & translate-trigger workflows in forks

- audit_reasons: `prior_benchmark_worst_failure`
- previous_expected_topics: `tests_ci`
- gpt55_labels: `tests_ci`
- possible_confusions: `docs`
- agreement_jaccard: `1.0`

**Rationales**
- `tests_ci`: Direct change to GitHub Actions workflow files to guard CI/CD jobs in forks.

**Excluded rationales**
- `docs`: Docs-related workflows are touched, but no documentation content or guides are changed.

**Excerpt**

```markdown
## Summary
- **Problem:** Two upstream-only workflows (`docs-sync-publish.yml`, `docs-translate-trigger-release.yml`) fail with `Authentication failed for 'https://github.com/openclaw/docs.git/'` on every push to `main` in any fork, because they rely on the `OPENCLAW_DOCS_SYNC_TOKEN` secret that only exists in `openclaw/openclaw`.
- **Why it matters:** Creates a red ✗ on every normal fork-sync (`git fetch upstream main && git push origin main`), confuses new contributors, and spams fork Actions dashboards with irrecoverable failures.
- **What changed:** Added `if: github.repository == 'openclaw/openclaw'` to the single job in each of the two workflows — the same guard pattern already used ~30 times across the repo (`ci.yml`, `codeql.yml`, `control-ui-locale-refresh.yml`).
- **What did NOT change (scope boundary):** No changes to workflow logic, secrets, the publish repo, the sync script (`scripts/docs-sync-publish.mjs`), documentation, or any other workflow. Behavior in `openclaw/openclaw` is byte-for-byte identical.
## Change Type (select all)
- [x] Bug fix
- [ ] Feature
- [ ] Refactor required for the fix
- [ ] Docs
- [ ] Security hardening
- [x] Chore/infra
## Scope (select all touched areas)
- [ ] Gateway / orchestration
- [ ] Skills / tool execution
- [ ] Auth / tokens
- [ ] Memory / storage
- [ ] Integrations
- [ ] API / contracts
- [ ] UI / DX
- [x] CI/CD / infra
## Linked Issue/PR
- Closes #
- Related #
- [x] This PR fixes a bug or regression
## Root Cause (if applicable)
- **Root cause:** The two workflows were added without the fork-guard expression that the rest of the CI already uses. When the workflow runs in a fork, `${{ secrets.OPENCLAW_DOCS_SYNC_TOKEN }}` expands to an empty string, so the clone/push URL becomes `https://x-access-token:@github.com/openclaw/docs.git/` and GitHub rejects it with `Invalid username or token. Password authentication is not supported for Git operations.`
- **Missing detection / guardrail:** No `if: github.repository == 'openclaw/openclaw'` on the job, even though the same repository relies on that exact check in ~30 other places to keep fork runs safe.
```

**Decision**

```json
{
  "id": "openclaw-openclaw-70002",
  "decision": "keep_easy",
  "final_labels": [
    "tests_ci"
  ],
  "notes": "User reviewed and said this row is correct."
}
```

## openclaw-openclaw-77827 / #77827 — fix: LM Studio thinking blocks invisible with Responses API

- audit_reasons: `repeated_prior_benchmark_failure`
- previous_expected_topics: `api_surface, local_models, model_serving`
- gpt55_labels: `model_serving, api_surface, local_models`
- possible_confusions: `local_model_providers`
- agreement_jaccard: `1.0`

**Rationales**
- `model_serving`: Fixes OpenAI-compatible Responses streaming parsing for `response.reasoning_text.done` events from LM Studio.
- `api_surface`: Implements handling for an official OpenAI Responses API stream event and its downstream event contract.
- `local_models`: Bug is explicitly reproduced with LM Studio local mode and a local Qwen reasoning model, affecting local model UX.

**Excluded rationales**
- `local_model_providers`: LM Studio provider compatibility is implicated, but the change is stream-event parsing rather than provider setup, discovery, auth, or routing.

**Excerpt**

```markdown
## Problem
When using LM Studio with the `openai-responses` API, the model's reasoning/thinking content was completely invisible, even though the model was actively thinking and producing reasoning tokens.
The root cause: LM Studio (and other OpenAI-compatible providers) deliver reasoning content via a single `response.reasoning_text.done` event carrying the full thinking text. OpenClaw's `processResponsesStream` had no handler for this event, so it was silently dropped on every request.
The standard OpenAI sequence OpenClaw expected:
1. `response.output_item.added` → `{ type: "reasoning" }`
2. `response.reasoning_summary_text.delta` (incremental chunks)
3. `response.output_item.done`
What LM Studio actually sends:
1. `response.reasoning_text.done` → full thinking text in one shot
No handler = no thinking block = thinking silently lost every time.
## Fix
Adds a handler for `response.reasoning_text.done` in `processResponsesStream` (`src/agents/openai-transport-stream.ts`):
- Reads the full reasoning text from `event.text`
- Creates a `thinking` content block and inserts it at the **front** of `output.content` (before any text blocks, preserving correct think-before-respond ordering)
- Fires the complete `thinking_start` -> `thinking_delta` -> `thinking_end` event sequence so all downstream consumers receive the thinking content correctly
Two paths are handled:
1. **Standard path** (provider sent `output_item.added(reasoning)` first): reuses the active reasoning block and fires only `thinking_end` to avoid duplicates
2. **LM Studio path** (no prior reasoning item): inserts a new thinking block at the front, but only when no thinking block and no text blocks exist yet
## Why This Is Correct
`response.reasoning_text.done` is not a non-standard event. It is part of the [official OpenAI Responses API spec](https://platform.openai.com/docs/api-reference/responses/streaming) (`ResponseReasoningTextDoneEvent`). This is a gap in spec coverage that affects any provider delivering reasoning this way.
## Real Behavior Proof
**Issue addressed:** Reasoning/thinking content from LM Studio was completely invisible when using the `openai-responses` API. No thinking block was rendered even though the model was actively reasoning.
**Real environment tested:** macOS, LM Studio running `ykimport/qwen3.5-9b-opus-openclaw-distilled` (Qwen3.5 reasoning model), OpenClaw gateway local mode, `openai-responses` API.
**Exact steps or command run after this patch:**
1.
[body truncated 
```

**Decision**

```json
{
  "id": "openclaw-openclaw-77827",
  "decision": "fix_labels",
  "final_labels": [
    "model_serving",
    "api_surface",
    "local_model_providers"
  ],
  "notes": "local_models does not apply as it does include a specific model or class of model. local_model_providers applies as this is about serving generally models with LM Studio via the Responses API - which is a local model provider"
}
```

## openclaw-openclaw-83863 / #83863 — ACP/Codex child tasks can be marked succeeded with progress-only output and no final deliverable

- audit_reasons: `teacher_previous_label_disagreement`
- previous_expected_topics: `acp, codex, coding_agents, reliability`
- gpt55_labels: `acp, codex, coding_agents, agent_runtime, reliability`
- possible_confusions: `sessions`
- agreement_jaccard: `0.8`

**Rationales**
- `acp`: The failure is explicitly in ACP child sessions and ACP manager done-event handling.
- `codex`: The issue specifically concerns Codex ACP child tasks returning only progress text.
- `coding_agents`: It affects parent/child agent workflows, subagents, task ledgers, and final-deliverable contracts.
- `agent_runtime`: The core bug is child task lifecycle/status being marked succeeded without a final deliverable.
- `reliability`: Incorrect success state after delivery retry failure creates silent failure and message-loss behavior.

**Excluded rationales**
- `sessions`: Child sessions and transcripts are involved, but the central problem is task runtime outcome/status handling rather than session identity or persistence.

**Excerpt**

```markdown
## Summary
ACP/Codex child sessions can terminate with only interim/progress text (for example "I'll inspect...", "I'm checking...", "I'm verifying now...") and OpenClaw records the durable task as `succeeded` / `outcome.status=ok` even though no final deliverable was captured and the completion announcement later fails.
This makes the parent agent correctly distrust the child ("Codex returned only progress, not delivery"), but the task ledger and UI still present the child run as successful. Operationally this looks like Codex/OpenClaw silently succeeded while no PR/diff/final report was delivered.
## Evidence Pattern
Observed on a real background ACP workflow. Operational identifiers and deployment details are intentionally redacted.
The affected child sessions had transcripts shaped like:
```

**Decision**

```json
{
  "id": "openclaw-openclaw-83863",
  "decision": "keep_easy",
  "final_labels": [
    "acp",
    "codex",
    "coding_agents",
    "agent_runtime",
    "reliability"
  ],
  "notes": "User reviewed and said this row is correct."
}
```

## openclaw-openclaw-84039 / #84039 — fix(cli): honor --no-prefix-cwd in acp

- audit_reasons: `teacher_previous_label_disagreement, low_previous_label_jaccard`
- previous_expected_topics: `acp, api_surface`
- gpt55_labels: `acp`
- possible_confusions: `api_surface`
- agreement_jaccard: `0.5`

**Rationales**
- `acp`: PR explicitly fixes the `openclaw acp` CLI path so `--no-prefix-cwd` is forwarded into the ACP bridge.

**Excluded rationales**
- `api_surface`: No HTTP/API endpoint or request/response contract changes; this is a CLI option parsing fix for ACP.
- `tests_ci`: Tests were added, but only as coverage for the ACP CLI behavior, not a CI/test infrastructure change.

**Excerpt**

```markdown
## Summary
- Let Commander own the negated option default for --no-prefix-cwd.
- Read the positive prefixCwd option that Commander actually populates.
- Add ACP CLI coverage for both the explicit opt-out and the default behavior.
Closes #83901.
## Verification
- node scripts/run-vitest.mjs src/cli/acp-cli.option-collisions.test.ts src/acp/translator.prompt-prefix.test.ts
- Crabbox AWS cbx_1689d0ad78e9, run run_a406418db6fe: regression failed before the source patch, then the focused ACP CLI and translator tests passed after the patch (15/15).
## Real behavior proof
Behavior addressed: openclaw acp --no-prefix-cwd now forwards prefixCwd=false into the ACP bridge so prompts are not prefixed with [Working directory: ...]; the default path still forwards prefixCwd=true.
Real environment tested: Fresh checkout of this PR branch after pnpm install and pnpm build, using a live ACP translator harness from the checkout; maintainer follow-up also verified focused behavior on AWS Crabbox Linux lease cbx_1689d0ad78e9.
Exact steps or command run after this patch: Build the PR checkout, run the ACP translator harness once with the default prefixCwd path and once with the --no-prefix-cwd / prefixCwd=false path, then run node scripts/run-vitest.mjs src/cli/acp-cli.option-collisions.test.ts src/acp/translator.prompt-prefix.test.ts -- --reporter=verbose.
Evidence after fix: The live ACP translator harness printed this after-fix output:
    default prefixCwd=true
    [Working directory: ~/openclaw-test]
    hello
    ---
    with --no-prefix-cwd / prefixCwd=false
    hello
Observed result after fix: The default path still prefixes the working directory, and the --no-prefix-cwd path suppresses that prefix. Focused tests also passed with 15 passed; the same regression test failed before the source patch with prefixCwd received as true.
What was not tested: No long-running interactive ACP server was left running; the live proof used a bounded ACP translator harness and the maintainer proof used focused CLI/translator tests.
```

**Decision**

```json
{
  "id": "openclaw-openclaw-84039",
  "decision": "keep_easy",
  "final_labels": [
    "acp"
  ],
  "notes": "User reviewed and said this row is correct."
}
```

## openclaw-openclaw-84301 / #84301 — [Bug]: Make Dream Diary narrative timeout configurable for slow/serial local model backends

- audit_reasons: `repeated_prior_benchmark_failure`
- previous_expected_topics: `config, local_models, queueing, reliability`
- gpt55_labels: `config, local_models, queueing, reliability`
- possible_confusions: `sessions`
- agreement_jaccard: `1.0`

**Rationales**
- `config`: The requested fix is a user-facing configurable Dream Diary narrative timeout and concurrency setting.
- `local_models`: The failure is tied to slow or serial local model backends such as LM Studio and local Qwen routing.
- `queueing`: The issue describes multiple narrative runs started in parallel/queued form exceeding the wait budget.
- `reliability`: Hardcoded 60s waits cause otherwise normal backend work to time out and fail, reducing completion reliability.

**Excluded rationales**
- `sessions`: Session-state errors appear in logs, but the central request is timeout/concurrency configuration rather than session persistence or resume behavior.

**Excerpt**

```markdown
### Bug type
Behavior bug (incorrect output/state without crash)
### Beta release blocker
No
### Summary
Dreaming’s Dream Diary narrative subagent wait timeout appears to be hardcoded to 60 seconds. On local model backends such as LM Studio, prompt processing may be serialized even when OpenClaw starts multiple dreaming narrative runs in parallel/queued form. This can cause dreaming narrative runs to exceed 60s and fail even though the backend is still working normally.
### Steps to reproduce
Dreaming starts multiple narrative prompts around the same sweep. LM Studio processes prompt work serially, so queued narrative runs can exceed the 60s wait budget.
Related logs include errors like:
EmbeddedAttemptSessionTakeoverError: session file changed while embedded prompt lock was released
and/or timeout-related narrative/embedded-run logs if present.
### Expected behavior
The Dream Diary narrative timeout should be configurable, or OpenClaw should reduce narrative concurrency for local/serial model backends so dreaming can complete reliably.
### Actual behavior
Related logs include errors like:
EmbeddedAttemptSessionTakeoverError: session file changed while embedded prompt lock was released
and/or timeout-related narrative/embedded-run logs if present.
### OpenClaw version
2025.5.12
### Operating system
Ubuntu
### Install method
npn
### Model
qwen/qwen3.6 35B
### Provider / routing chain
openclaw -> local
### Additional provider/model setup details
```

**Decision**

```json
{
  "id": "openclaw-openclaw-84301",
  "decision": "keep_easy",
  "final_labels": [
    "config",
    "local_models",
    "queueing",
    "reliability"
  ],
  "notes": "User reviewed and said this row is correct."
}
```

## openclaw-openclaw-84719 / #84719 — fix: preserve active webhook request counters

- audit_reasons: `prior_benchmark_worst_failure`
- previous_expected_topics: `api_surface, reliability, skills_plugins`
- gpt55_labels: `api_surface, reliability, skills_plugins`
- possible_confusions: `queueing`
- agreement_jaccard: `1.0`

**Rationales**
- `api_surface`: Changes webhook request-guard behavior, part of the webhook request handling/API contract.
- `reliability`: Fix preserves active in-flight counters and rejects new keys at capacity, preventing stale/incorrect limiter state.
- `skills_plugins`: The implementation is in src/plugin-sdk webhook request guards, affecting plugin SDK webhook handling.

**Excluded rationales**
- `queueing`: Although it involves in-flight capacity/backpressure, there is no queue, lane, or task ordering behavior changed.

**Excerpt**

```markdown
## Summary
- Treat `maxTrackedKeys` as an active-key capacity limit in `createWebhookInFlightLimiter`.
- Reject brand-new keys when the active key table is full instead of pruning active counters.
- Add regression coverage for full-capacity behavior and same-key reacquire behavior.
Fixes #84717.
## Verification
- `ASDF_NODEJS_VERSION=24.15.0 pnpm install --frozen-lockfile`
- `ASDF_NODEJS_VERSION=24.15.0 node scripts/run-vitest.mjs run --config test/vitest/vitest.unit-fast.config.ts src/plugin-sdk/webhook-request-guards.test.ts`
- `ASDF_NODEJS_VERSION=24.15.0 pnpm exec oxfmt --check src/plugin-sdk/webhook-request-guards.ts src/plugin-sdk/webhook-request-guards.test.ts`
- `ASDF_NODEJS_VERSION=24.15.0 pnpm lint:core`
- `ASDF_NODEJS_VERSION=24.15.0 pnpm tsgo:core:test`
## Real behavior proof
Behavior addressed: the webhook in-flight limiter no longer deletes active request counters when the tracked-key cap is reached.
Real environment tested: local macOS source checkout with the repo-declared package manager (`pnpm@11.1.0`) and `ASDF_NODEJS_VERSION=24.15.0` for repo tooling.
Exact steps or command run after this patch: ran the focused webhook guard test file through `node scripts/run-vitest.mjs` using `test/vitest/vitest.unit-fast.config.ts`, then ran format, lint, and core test type-check commands listed above.
Evidence after fix: regression tests assert that a new key is rejected when active key capacity is full, while an existing tracked key remains counted and can acquire up to `maxInFlightPerKey`.
Observed result after fix: focused test file passed with 16 tests; format check, core lint, and core test type-check completed with no errors.
What was not tested: full repository test suite and live webhook endpoint traffic.
```

**Decision**

```json
{
  "id": "openclaw-openclaw-84719",
  "decision": "fix_labels",
  "final_labels": [
    "queueing",
    "reliability",
  ],
  "notes": "this does not directly relate to skills_plugins. queueing label applies as this relates to a backpressure type problem"
}
```

## openclaw-openclaw-84746 / #84746 — [Bug]: Auto-compaction crashes active responses after 5.18 transcript lock scope change (#13744)

- audit_reasons: `repeated_prior_benchmark_failure`
- previous_expected_topics: `agent_runtime, memory, reliability, sessions`
- gpt55_labels: `agent_runtime, memory, reliability, sessions`
- possible_confusions: `queueing`
- agreement_jaccard: `1.0`

**Rationales**
- `agent_runtime`: The bug affects embedded agent runs and kills active model responses when auto-compaction fires.
- `memory`: Auto-compaction of the transcript/session context is the operation that rewrites state and triggers the failure.
- `reliability`: The issue reports crashes, message loss, a race around locks, wedged lanes, and recovery only after restart.
- `sessions`: The root error is a session-file/transcript-lock takeover during in-flight session persistence.

**Excluded rationales**
- `queueing`: Lane wedging is an observed consequence, but queue scheduling or task ordering is not the root issue.

**Excerpt**

```markdown
## Environment
- **OpenClaw:** 2026.5.18 → 2026.5.19-beta.2 (issue persists on both)
- **OS:** macOS Apple Silicon (MacBook Air)
- **Install:** npm global
- **Agents:** 15 agents, multi-channel (iMessage group chats, Telegram, Slack)
- **Prior version:** 2026.5.7 — zero crashes
## What happened
After upgrading from 5.7 to 5.18, every agent with an active group chat conversation crashes when auto-compaction fires. The error is `EmbeddedAttemptSessionTakeoverError: session file changed while embedded prompt lock was released`.
**Zero `SessionTakeoverError` on 5.7. 38 on the first day of 5.18.** The crashes correlate 1:1 with `embedded run auto-compaction start` log entries — not crons, not concurrent messages, not provider failures.
## Root cause
5.18 introduced the #13744 fix: "release the embedded run's coarse transcript lock before model I/O while locking persistence and cleanup separately." This was intended to prevent concurrent message timeouts. The unintended consequence: auto-compaction rewrites the session file during model I/O, triggering `SessionTakeoverError` and killing the active response.
## Evidence
24 auto-compaction events in one day, roughly every 55 minutes. Each one that coincides with an active model call crashes that response:
```

**Decision**

```json
{
  "id": "openclaw-openclaw-84746",
  "decision": "fix_labels",
  "final_labels": [
    "agent_runtime",
    "reliability",
    "sessions"
  ],
  "notes": "memory does not apply here - memory should be used for the specific memory features, not as a general term"
}
```

## openclaw-openclaw-84757 / #84757 — [Bug]: Telegram session can get stuck after compaction when encrypted reasoning content fails verification

- audit_reasons: `teacher_previous_label_disagreement, low_previous_label_jaccard`
- previous_expected_topics: `chat_integrations, memory, reliability, sessions`
- gpt55_labels: `chat_integrations, sessions, reliability`
- possible_confusions: `memory`
- agreement_jaccard: `0.75`

**Rationales**
- `chat_integrations`: The failure occurs in a Telegram direct-chat session and results in a Telegram fallback message.
- `sessions`: The bug is caused by persisted session history replay after compaction or restore, leaving the same session unusable until /new.
- `reliability`: The issue is a stuck-session recovery bug where retries keep failing and automatic cleanup/retry behavior is expected.

**Excluded rationales**
- `memory`: The compaction/history replay is described as session state persistence, not an active memory, embedding, vector-store, or memory-provider feature.

**Excerpt**

```markdown
### Bug type
Session recovery / Telegram integration
### Summary
A Telegram direct-chat session can become stuck after a context compaction or session restore when session history replay includes encrypted reasoning content that can no longer be verified. After that, each retry in the same session fails before assistant output and returns the generic Telegram fallback message.
This may be related to #84406, but this case is not file-upload specific. It reproduces on normal text messages after a long-running Telegram session is compacted/restored.
### Steps to reproduce
1. Use a Telegram direct-chat session long enough for context compaction or session restore to occur.
2. Send another normal text message in the same Telegram session.
3. Observe that the model request fails before producing assistant content.
4. Retry in the same session.
### Expected behavior
OpenClaw should not let one invalid encrypted reasoning payload leave the Telegram session permanently unusable. It should either sanitize/drop encrypted reasoning payloads that are unsafe to replay, or detect this specific provider error and recover with a clean checkpoint/session while giving the user a specific recovery message.
### Actual behavior
The provider rejects the replayed request with an error shaped like:
```

**Decision**

```json
{
  "id": "openclaw-openclaw-84757",
  "decision": "keep_easy",
  "final_labels": [
    "chat_integrations",
    "sessions",
    "reliability"
  ],
  "notes": ""
}
```

## openclaw-openclaw-84763 / #84763 — fix(acpx): scrub provider credential env from ACP harness spawns

- audit_reasons: `teacher_previous_label_disagreement`
- previous_expected_topics: `acp, acpx, auth_identity, config`
- gpt55_labels: `acpx, acp, auth_identity, security, config`
- possible_confusions: `exec_tools`
- agreement_jaccard: `0.8`

**Rationales**
- `acpx`: PR is explicitly under extensions/acpx and changes ACPX runtime/process launch decoration.
- `acp`: Bug occurs in sessions_spawn with runtime:"acp" and ACP harness children such as claude/codex/gemini.
- `auth_identity`: Core fix addresses OAuth/API-key credential scope so spawned harnesses use their own auth instead of gateway credentials.
- `security`: It scrubs provider credential/token environment variables from child processes and is described as security hardening.
- `config`: Adds the acp.scrubProviderEnv configuration knob and updates config schema/help metadata.

**Excluded rationales**
- `exec_tools`: Although implemented by prefixing launch commands with env -u, the central issue is ACPX harness auth/env handling, not generic shell tool execution.

**Excerpt**

```markdown
## Summary
- **Problem:** `sessions_spawn` with `runtime:"acp"` + `agentId:"claude"` fails immediately with `AcpRuntimeError: Internal error: Invalid API key · code=ACP_TURN_FAILED`.
- **Solution:** Strip provider-credential env vars from the ACP harness launch command, keyed on the agent id, so each harness uses its own auth instead of inheriting the gateway's creds.
- **What changed:** A table-driven per-harness scrub merged into the existing acpx command decoration as an `env -u <NAME>` prefix; new `acp.scrubProviderEnv` config knob (default `true`).
- **What did NOT change (scope boundary):** The gateway's own auth/model-call path is untouched; the OpenClaw ACP bridge keeps the full env; reuse identity stays the raw command (no session-reuse changes); no blanket env stripping — only named provider-credential vars.
## Motivation
Operators set `ANTHROPIC_API_KEY` in `~/.openclaw/.env` so the gateway can authenticate its own model calls. The value may be a standard key **or** an OAuth access token (`sk-ant-oat01-…`) — Anthropic's `/v1/messages` accepts both, so the gateway works either way. But Claude Code's CLI auth path **rejects** an OAuth token supplied via `ANTHROPIC_API_KEY` because it expects its own Keychain OAuth flow. Since an ACP harness inherits the gateway's environment, the spawned `claude` child sees `ANTHROPIC_API_KEY`, tries to use it, and dies with "Invalid API key" before doing any work.
## Change Type (select all)
- [x] Bug fix
- [ ] Feature
- [x] Refactor required for the fix
- [ ] Docs
- [x] Security hardening
- [ ] Chore/infra
## Scope (select all touched areas)
- [x] Gateway / orchestration
- [ ] Skills / tool execution
- [x] Auth / tokens
- [ ] Memory / storage
- [x] Integrations
- [ ] API / contracts
- [ ] UI / DX
- [ ] CI/CD / infra
## Linked Issue/PR
- Closes #
- Related #
- [x] This PR fixes a bug or regression
## Real behavior proof (required for external PRs)
```

**Decision**

```json
{
  "id": "openclaw-openclaw-84763",
  "decision": "keep_easy",
  "final_labels": [
    "acpx",
    "acp",
    "auth_identity",
    "security",
    "config"
  ],
  "notes": "User reviewed and said this row is correct."
}
```

## openclaw-openclaw-84802 / #84802 — fix(memory-core): allow bounded dreaming session cleanup

- audit_reasons: `repeated_prior_benchmark_failure`
- previous_expected_topics: `memory, reliability, sessions`
- gpt55_labels: `memory, sessions, reliability`
- possible_confusions: `tests_ci`
- agreement_jaccard: `1.0`

**Rationales**
- `memory`: PR is explicitly in memory-core/dreaming and changes dreaming narrative behavior.
- `sessions`: Core change reuses stable narrative subagent session keys and deletes bounded session keys.
- `reliability`: Fix prevents stale dreaming-narrative sessions from accumulating and adds cleanup on retries/finalization.

**Excluded rationales**
- `tests_ci`: Tests are updated to cover the fix, but the central change is memory session cleanup, not CI or test infrastructure.

**Excerpt**

```markdown
Makes https://github.com/openclaw/openclaw/pull/70464 merge-ready for the ClawSweeper automerge loop.
The edit pass should inspect the live PR diff, review comments, and failing checks; rebase if needed; keep the contributor branch credited; and stop only when validation is green or an external blocker is proven.
ClawSweeper 🐠 replacement reef notes:
- Cluster: automerge-openclaw-openclaw-70464
- Source PRs: https://github.com/openclaw/openclaw/pull/70464
- Credit: Source PR: https://github.com/openclaw/openclaw/pull/70464
- Validation: pnpm check:changed
- Replacement reason: ClawSweeper could not update the source PR branch directly, so it opened a writable replacement PR instead.
- Automerge requested by: @Takhoffman
<!-- clawsweeper-automerge-requested-by login="Takhoffman" id="781889" -->
- Repair fallback: GitHub rejected the repair branch push because it updates workflow files and the ClawSweeper app token does not have workflows permission
Co-author credit kept:
- @chiyouYCH: Co-authored-by: chiyouYCH <26790612+chiyouYCH@users.noreply.github.com>
fish notes: model gpt-5.5, reasoning high; reviewed against c752d0f75850.
```

**Decision**

```json
{
  "id": "openclaw-openclaw-84802",
  "decision": "keep_easy",
  "final_labels": [
    "memory",
    "sessions",
    "reliability"
  ],
  "notes": "User reviewed and said this row is correct."
}
```
