# V6 spec changelog and lineage (NOT model-facing)

This file is never included in any prompt. It records provenance, version
discipline, and the crosswalk that model-facing spec files must not contain
(a fresh teacher/task model has no prior versions to reason about — history
notes in prompts are noise).

## Version discipline

`topic-boundary-guidance-v6.md` + `allowed-topics-v6.md` +
`eval/openclaw/output.schema.json` together are the frozen v6 label spec.
Any edit is a spec change: record it here, re-run the anchor-free teacher
revalidation, and re-baseline. Do not edit silently.

## Provenance

- Per-topic MUST rules transcribed from the project maintainer's production
  DS4 topic-inventory classifier guidance (authoritative consumer spec),
  shared 2026-06-11.
- Do-not-include guards derived from v4 `TOPIC_HINTS` and the v5 test-error
  analysis (`runs/easy-set-v5`).
- Where v5-era guidance conflicted with the maintainer spec, the maintainer
  spec won: `coding_agents` (internal subagent orchestration now qualifies),
  `local_model_providers` (local-only restriction removed, later superseded by
  enum change below), `security` (credential/auth boundaries qualify),
  `config` (operator-facing options qualify), `model_releases` (no MUST rule;
  superseded by enum change below).

## Enum changes vs v4 (40 → 38 topics)

Decided 2026-06-11 to simplify the inference family (the largest v5 confusion
cluster):

- `model_serving` → `inference_api`: tightened to the integration layer
  between OpenClaw and model serving/providers (Responses, Chat Completions,
  Anthropic Messages, TTS/vision/embeddings APIs); also absorbs the
  provider-setup/catalog/routing scope of removed `local_model_providers`.
- `local_model_providers` → removed (provider layer → `inference_api`;
  engine-specific hookup → `self_hosted_inference`).
- `self_hosted_inference` → redefined as the engine-integration layer (vLLM,
  llama.cpp, Ollama, LM Studio, TGI, LocalAI), on device or self-hosted
  elsewhere.
- `local_models` → narrowed to the model-artifact/hardware layer on device
  (GGUF/quantization behavior, VRAM, model-family quirks, UX/fallback/context).
  OPEN QUESTION for calibration: if teachers keep confusing this with
  `self_hosted_inference`, fold it in.
- `open_weight_models` → removed (catalog/release metadata →
  `model_lifecycle`; on-device artifact behavior → `local_models`).
- `model_releases` → `model_lifecycle`: introduction, decommissioning, or
  adjustment of model configurations.
- `hf_agents`, `hub_workflows`, `post_training`, `agent_demos` → removed
  entirely (no maintainer MUST rule, near-zero traffic: 1 occurrence of
  `agent_demos` in 195 v5 gold rows, zero for the others). Final v6 enum: 34
  topics.

Crosswalk for relabel comparison and v5-gold migration:

| v4/v5 label | v6 label |
|---|---|
| `model_serving` | `inference_api` |
| `local_model_providers` | `inference_api` (provider setup/auth/routing/catalogs) or `self_hosted_inference` (engine hookup) |
| `open_weight_models` | `model_lifecycle` (catalog/release metadata) or `local_models` (on-device artifact) |
| `model_releases` | `model_lifecycle` |

Affected v5 gold (190 rows): model_serving 16, local_model_providers 11,
self_hosted_inference 10, local_models 9, model_releases 2, open_weight_models
1; 10 rows carried 2+ family labels. The anchor-free revalidation relabels
these under the v6 enum; the builder compares via this crosswalk.

## v6a (2026-06-11) — review-packet feedback from intake batches 001-002

Current label-generation spec: `topic-boundary-guidance-v6a.md` +
`allowed-topics-v6a.md` (teacher card and env.sh point here). Enum unchanged
from v6 (34). Changes from the batch 001-002 review packet:

- `coding_agent_integrations` replaces the v6 topic id `coding_agents`; the
  rename is intended to make the external-integration boundary explicit.
  Semantics are also NARROWED to external coding-agent integrations only
  (Codex, Claude Code, Gemini CLI, Pi, or external coding agents in general).
  Internal subagents, `sessions_spawn`, tool use, approvals, sandboxing,
  compaction, traces, and orchestration route to their owning surfaces. New
  top-level "Coding-agent boundary" section; `agent_runtime` now owns internal
  subagent execution/orchestration. NOTE: this deliberately diverges from the
  maintainer's production MUST rule ("subagents... agent orchestration"),
  which had been adopted in v6 — prior prompt-hacking had produced
  overlabelling on this topic. Adjudications applied: 68204 and 10467 drop
  `coding_agent_integrations`.
- `telemetry_usage` scoped to OpenClaw's own telemetry/usage surface; benchmark
  adjacency excluded (42408); trace/observability producer coverage included
  (68204 keeps telemetry_usage + agent_runtime).
- `ui_tui` observation-vs-surface rule: UI must be the failing/changed surface,
  not merely where a defect is observed/triggered (76724 drops ui_tui;
  mcp_tooling confirmed — tools/list discovery added to mcp_tooling MUST).
- `config` wording: user/operator-facing settings additions (toggles, pickers,
  defaults, persisted preferences) qualify, including via a settings UI
  (71487 Opus wobble).
- `auth_identity` scoped to OpenClaw's own auth/identity surface; incidental
  external-service auth excluded (78528 drops auth_identity).
- `gateway` confirmed unchanged (68916 correct as labeled).
- Style: ownership-rationale phrasing ("label the surface whose behavior the
  item changes, not where it is visible") for frontier-teacher reasoning;
  caveat count kept flat.

Files `topic-boundary-guidance-v6.md` / `allowed-topics-v6.md` remain as the
pre-feedback spec used by intake batches 001-002 (their spec-manifests
reference them); do not edit them further.

## Divergence from the maintainer's production enum

The maintainer's DS4 guidance uses the v4 enum (`model_serving`,
`local_model_providers`, `open_weight_models`, `model_releases` as separate
topics). The v6 enum diverges deliberately for clarity; the crosswalk above
maps v6 labels back to the production inventory if results need to be
translated. If the production taxonomy adopts these changes, update this note.

## Repo hygiene

Old artifacts (v2-v5 sets, runs, prompts) move to a `legacy` branch; `main`
carries the v6 lineage only. Cut the legacy branch BEFORE committing the v6
schema change — `eval/openclaw/output.schema.json` is shared plumbing, and the
enum change breaks re-scoring of pre-v6 runs on whatever branch it lands on.
