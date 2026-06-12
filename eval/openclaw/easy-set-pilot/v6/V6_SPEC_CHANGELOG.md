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
`allowed-topics-v6a.md`. Enum unchanged from v6 (34). Changes from the batch
001-002 review packet:

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

## v6b (2026-06-12) — post-run boundary cleanup

- `local_models` merged into `self_hosted_inference`; enum size is now 33.
  Former `local_models` cases (GGUF/quantization, local hardware/VRAM,
  model-family quirks, local model fallback/context/UX) now route to
  `self_hosted_inference`.
- `gateway` narrowed to decisive gateway ownership: routing, state, startup,
  protocol, restart/health, gateway-owned execution, or gateway-owned
  lifecycle. Merely identifying code that runs through the gateway no longer
  satisfies the topic.
- `notifications` co-label test made observable: include only when an outbound
  delivery path, sent-message handling, completion/notification delivery gate,
  notify setting, or announcement behavior is implemented or changed. Events or
  hooks about sends route to `hooks` unless the delivery path/gate itself
  changes. The same observable test is present in both the task overlay and the
  teacher-injected topic-boundary guidance.
- `acp` alongside `acpx` now requires named ACP binding, override,
  parent/child session, or delivery semantics. Pure ACPX worker/transport/
  harness/proxy/command/auth/compatibility work remains `acpx` only.
- `security` tightened to concrete security issues, improvements, or direct
  security features. Privacy-focused product features, disappearing messages,
  retention/visibility preferences, generic privacy UX, and ordinary auth/
  profile configuration do not qualify unless they change a security control.
  The `auth_identity` co-label now uses an observable trigger: access rule,
  exposure path, permission check, credential/secret/token handling,
  signature/HMAC/verification, or auth-boundary hardening.
- Active run settings (`env.sh` and intake manifests) now point to the v6b
  files: `allowed-topics-v6b.md`, `topic-boundary-guidance-v6b.md`,
  `task-boundary-overlay-v6b.md`, `teacher-card-v6b.md`, and
  `teacher-output-v6b.schema.json`. v6b-named seed/ASI copies
  (`seed-policy-overlay-v6b.md`, `seed-policy-vanilla-v6b.md`,
  `vanilla-asi-v6b-slim.md`) are used for GEPA auditability, although the slim
  ASI remains intentionally generic and does not duplicate taxonomy boundaries.
  v6a files are retained for auditability.

Files `topic-boundary-guidance-v6.md` / `allowed-topics-v6.md` remain as the
pre-feedback spec used by intake batches 001-002 (their spec-manifests
reference them); do not edit them further.

## v6d (2026-06-12) — acp/sessions ownership split

Current label-generation spec: `topic-boundary-guidance-v6d.md` +
`allowed-topics-v6d.md` + `task-boundary-overlay-v6d.md` +
`teacher-card-v6d.md` + `teacher-output-v6d.schema.json` (env.sh points here;
runs root `runs/easy-set-v6d`). Enum unchanged (33). One change, from the
batch-002 stability analysis:

- `acp` and `sessions` both claimed "binding" and "parent/child behavior"
  verbatim — the only spec-attributable pattern in batch-002's persistent
  instability (4 rows gpt-unstable under v6, v6a, AND v6b, all ACP-session
  rows: 43564, 51654, 54471, 56442). v6d splits ownership by layer: `acp` =
  protocol semantics (binding/override, spawn/cancel, parent/child message
  relay and delivery, event streams, completion notify, message blocks,
  client/server compatibility); `sessions` = the session objects themselves
  (identity, lifecycle, state, persistence, transcript, cleanup, stores);
  co-label only when the item changes both layers. Bare "binding" removed
  from `sessions`.

Predicted resolutions for the four hard rows (verify on the v6d rerun):
54471 (system_event relay) -> acp without sessions; 56442 (parent completion
notify) -> acp + notifications; 51654 (session env vars) -> sessions-led;
43564 (skill context injection) -> sessions + skills_plugins, acp only if the
protocol injection mechanism changes. Rows still unstable after v6d demote to
medium per the ladder rule, not further spec edits.

## v6g (2026-06-12) — deliverable test + 3-label cap

Spec: `topic-boundary-guidance-v6g.md` + `allowed-topics-v6f.md` (unchanged) +
`teacher-card-v6g.md` + `teacher-output-v6g.schema.json`. Label-only variant
like v6f (no task/eligibility overlay). Enum unchanged (33). Two changes, from
the v6f prompt-keyword-audit-40 rationale analysis:

- **Deliverable test (global tie-break).** 12 of 13 v6f GPT/Opus modal
  disagreements were strict superset relations where the disputed label was
  `config`, `agent_runtime`, `acp`, or `sessions` — one teacher labeling a
  surface that was merely the delivery mechanism (a toggle/parameter shipping
  another surface's feature), a producer/symptom location (paths emitting into
  a new trace schema, the daemon where a hang appears), the motivation
  (security rationale without a security-control change), or commenter
  discussion. The new section makes "behavior contract changes" the explicit
  inclusion bar for every label and adds **specific beats generic** (`codex` /
  `coding_agent_integrations`, `acpx`/`acp`) as a hard rule. The disputed
  label appeared in `possible_confusions` in 13/13 disagreement rows, and
  excluded-label rationales of the form "plausible but not central" already
  described the right call — the test tells the teacher to trust that
  exclusion.
- **Cardinality cap 5 → 3, priority-ordered.** v6f acceptance by GPT modal
  label count: 1 → 6/10, 2 → 8/9, 3 → 7/15, 4 → 1/4, 5 → 0/2; no accepted row
  had >4 labels and zero exact modal matches had 5. Schema `maxItems` is now 3
  and labels must be listed primary-surface-first (enables top-1/top-2 partial
  agreement scoring later). The consensus script's `hit_label_cap` /
  `too_many_labels` checks (hardcoded ==5/>5) become inert, not broken.

Verify on the same 40-row audit set (`runs/easy-set-v6d/prompt-keyword-audit-40/input.jsonl`)
against the b/d/e/f baselines; success = exact modal matches 27 → 31+ and
deferrals 18 → ~10. If met, freeze the spec and route residual superset
disputes to the deterministic intersection rule instead of further prompt
variants.

**Verification result (runs/easy-set-v6g/prompt-keyword-audit-40):** accepted
25 (v6f: 22), deferred 15 (18), exact modal matches 30 (27), mean Jaccard
0.900 (0.870), review flags 0 (3). 30 vs the 31 target, but every
cross-teacher metric improved and a manual rationale audit of the five
riskiest drops (40332, 48580, 48406, 82880, 44379) confirmed the compression
is label-truth-improving, not agreement-by-forcing: 5 of 6 newly-accepted
rows had no cap binding (the deliverable test did the work). Residual: 8
single-label superset disputes (intersection rule), 2 cap-churn cross
disputes (48406, 48580 — human adjudication; also deferred under v6f). v6g is
FROZEN as the label standard.

## v6g GEPA-side crystallization (2026-06-12)

The student/GEPA stack moves to the same standard. New tracked assets, all
pointed to by `env.sh`:

- `task-boundary-overlay-v6g.md` — based on v6d (the v6e benchmark-eligibility
  section is dropped for good; it only inflated review flags). Cardinality law
  → at most 3 priority-ordered; adds the deliverable test and
  specific-beats-generic; hooks bullet gains the #44379 rule (a caller
  suppressing/bypassing hooks is the caller's surface).
- `openclaw-vanilla-labeler-v6g.md` — taxonomy include moves v6b → v6f (picks
  up the acp/sessions ownership split), overlay include moves to v6g, output
  instruction states the 3-cap and priority order.
- `seed-policy-vanilla-v6g.md` / `seed-policy-overlay-v6g.md` — seed candidate
  restated around the deliverable test; cardinality section no longer says
  "include every qualifying topic, cap 5".
- `vanilla-asi-v6g-slim.md` — reflection constraints updated: cap 3
  priority-ordered; reflection must not restate the (now fixed) deliverable
  test; names the expected over-labeling failure modes (mechanism, producer/
  symptom, motivation, generic-beside-specific) and steers GEPA toward
  suppression rules.

Deliberately NOT changed: `eval/openclaw/output.schema.json` (shared scoring
plumbing; adding `maxItems: 3` would break re-scoring of pre-v6g runs). The
student cap is enforced by prompt text plus capped gold labels under
row-aware scoring, not by schema validation. The teacher schema
(`teacher-output-v6g.schema.json`) IS capped at 3.

## v6h (2026-06-12) — reliability-mechanism and inference-dispatch tie-breaks

Spec: `topic-boundary-guidance-v6h.md` + `allowed-topics-v6f.md` (unchanged) +
`task-boundary-overlay-v6h.md` + `teacher-card-v6h.md` +
`teacher-output-v6h.schema.json` (content-identical to v6g schema). GEPA-side
assets bumped in lockstep (`openclaw-vanilla-labeler-v6h.md`,
`seed-policy-*-v6h.md`, `vanilla-asi-v6h-slim.md`); env.sh points here. Enum
unchanged (33). This is the build spec for the full ~700-row intake.

Provenance note first: v6g's `docs` section gained a `Do not include:` guard
*after* the prompt-keyword-audit-40 run (needed so
`load_topic_hints_from_guidance` materializes 33/33 dynamic-ASI topics — a
section with no guard bullet is skipped). The intake-100-slim and reinforce-50
runs used that amended text. Recorded here instead of silently; v6h formally
owns the guard.

Two tie-breaks, from the intake-100-slim disagreement rationales (top
disputed labels: reliability 9, inference_api 7, security 6):

- **`reliability` requires a changed mechanism.** Include only when the item
  adds or changes a recovery/retry/cleanup/lifecycle/watchdog/hardening
  mechanism itself. A defect that *manifested* as message loss, a hang, a
  race, or a crash inside another surface's logic is that surface only;
  `impact:*` severity tags do not confer ownership. (Opus was labeling
  reliability off impact tags and "operational failure mode" framing; GPT
  excluded it as symptom/motivation — 9 rows, all the same undecided
  question.)
- **`inference_api` owns the wire contract.** Internal model selection —
  dispatch, fallback ordering, capability-based routing — is `agent_runtime`/
  `model_lifecycle` unless provider request/response handling itself changes.

`security` disputes (6 rows: centrality of credential/access changes) were
judged adjudication material, not spec-fixable; no change.

**Probe (runs/easy-set-v6h/tiebreak-probe, 21 rows, 1×GPT + 1×Opus):**
the 15 reliability/inference_api dispute rows went 0/15 → 9/15 exact match
(most of the rest is ordinary single-run flicker or cross disputes). Controls:
accepted rows 88400, 84771, 51667 unchanged; 39248 upgraded to exact match
(both teachers now drop motivation-reliability); 71646 needs re-adjudication —
under the v6h reading Opus drops `mcp_tooling` (leak's location, not its
changed surface), which is arguably the deliverable test applied correctly to
a row v6g accepted with it.

Open item: reinforce-50 ran under v6g; its accepted rows that contain
`reliability` or `inference_api` should be cheaply re-probed under v6h before
entering the bench ledger (same targeted-probe pattern).

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
