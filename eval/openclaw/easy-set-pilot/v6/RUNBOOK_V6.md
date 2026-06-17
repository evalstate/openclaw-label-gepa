# V6 runbook — anchor-free label revalidation + overlay GEPA regime

V6 makes two changes relative to v5, in order:

1. **Label side:** revalidate the easy-set labels anchor-free against a frozen
   v6 boundary spec, so every gold label is reproducible from
   (row, taxonomy, guidance) without seeing the previous answer.
2. **GEPA side:** remove the teacher/task information asymmetry (Arm A gives the
   task model the boundary overlay as fixed context) and constrain the mutable
   policy to a compact overlay (hygiene penalty + 8k budget), with Arm B as the
   v5-style compression control.

Run phases in order. Phases marked CHECKPOINT end with "report back" — the next
phase's inputs depend on their outputs.

## Assets in this folder

| File | Role |
|---|---|
| `topic-boundary-guidance-v6b.md` | Active v6b label spec: maintainer MUST rules + do-not-include guards + cardinality law + tightened boundary/co-label tests |
| `allowed-topics-v6b.md` | Active v6b taxonomy: 33 topics (`local_models` folded into `self_hosted_inference`); see `V6_SPEC_CHANGELOG.md` for the crosswalk |
| `V6_SPEC_CHANGELOG.md` | Lineage, provenance, enum crosswalk, version discipline — never injected into prompts |
| `openclaw-vanilla-labeler-v6b.md` | Active v6b labeler card: taxonomy + fixed overlay + mutable policy slot |
| `teacher-card-v6b.md` | Anchor-free teacher card (no previous-label exposure; includes frozen v6b guidance) |
| `teacher-template-v6-anchor-free.md` | Row template without the `current_expected_topics` block |
| `task-boundary-overlay-v6b.md` | Condensed task-facing overlay for v6b |
| `seed-policy-overlay-v6b.md` | Structured overlay seed (Decision Procedure / Cardinality / Boundary Overlays / Suppression) |
| `seed-policy-vanilla-v6b.md` | Vanilla seed policy for v6b compression/baseline runs |
| `vanilla-asi-v6b-slim.md` | Slim reflection ASI: overlay contract, no cue tables |
| `v6-prereview-convergent-disagreements.md` | 8 disputed test rows for human decision before freezing |
| `V6_INTAKE_LADDER.md` | Reproducible 30-row intake/calibration workflow for the new-label build |
| `V6I_REGIME.md` | v6i GEPA ablation plan: feedback tightness and mutable task-overlay experiments on the frozen v6h split |
| `V6K_REGIME.md` | v6k final-data row-wise GEPA regime from the earlier mixed final pool |
| `V6L_REGIME.md` | Current gold-only row-wise GEPA regime: 330-row final pool, feedback192 divisible by minibatch 12, Pareto60, bench78, and launch commands |
| `V6M_REGIME.md` | v6m row-wise GEPA regime: v6l data with macro-F1, label over/under-application, and confusion-matrix reflection diagnostics |
| `V6N_REGIME.md` | v6n strict row-wise GEPA regime: Jaccard/exact scoring, no padded minibatches, label/co-error reflection diagnostics, and dashboard alignment on `gepa/iteration` |
| `V6O_REGIME.md` | v6o clean strict row-wise GEPA regime: v6o-named 300-row feedback artifacts, Jaccard/exact scoring, no padded minibatches |
| `V6P_REGIME.md` | v6p softened exactness ablation: v6o data with `row-soft-exact` scoring and cleaner Trackio objective/diagnostic metric namespaces |
| `V6Q_REGIME.md` | v6q GPT-5.4 minimal-seed ablation: v6p data/scoring/ASI with a deliberately sparse starting policy |
| `V6R_REGIME.md` | v6r GPT-5.4 surgical-reflection ablation: compact reflection background, minimal row deltas, lower policy budget, and anti-keyword/anti-rulebook mutation discipline |
| `env.sh` | Source me: run-stable settings (paths, trackio project + repo-local `TRACKIO_DIR`, models, `FAST_AGENT_BIN`) + `v6_intake_snapshot` helper |
| `intake/BATCH/` | Tracked curated batch records (row-ids, spec-manifest, consensus, adjudication, accepted/deferred); raw repeats stay under `runs/` |
| `v6-build-ledger.jsonl` | Tracked cumulative ledger of accepted rows — the source for final v6 train/test |

Script changes (already applied to `scripts/openclaw-vanilla-f1-gepa.py`):

- `--hygiene-penalty W` (per-finding gepa_score penalty; batch-mode candidate
  scoring) and `--policy-char-budget N`. The current runner default is 12,500
  chars; pass `--policy-char-budget 12000` to reproduce the old v5 budget
  exactly, or pass a lower explicit budget for compact-overlay ablations.
  `policy_hygiene()` now also flags copied
  false-positive/false-negative guard text and per-topic guide sections.
- `--boundary-guidance PATH`: replaces the in-code `TOPIC_HINTS` (the source of
  the dynamic-ASI guard injections) with hints parsed from the frozen v6 spec —
  single source of truth. Validates parsed topics against the schema enum,
  copies the file into the run dir, records it (path + sha256) in run.json.
  REQUIRED for all v6 GEPA runs; without it, reflection receives v4-era guard
  text.
- `--feedback-profile surgical` and `--reflection-background compact`: v6r
  anti-overfit controls. Surgical feedback exposes aggregate label/confusion
  diagnostics plus minimal row deltas; compact reflection background gives the
  tutor topic IDs rather than the full taxonomy definition block. Use these for
  GPT-5.4-mini-class runs where long GEPA policies have failed to transfer.
- The live classifier schema `eval/openclaw/output.schema.json` now matches the
  v6h teacher label contract: 33-topic enum, no `local_models`, and
  `topics_of_interest.maxItems == 3`. The GEPA runner preflights both
  `--allowed-topics` and input gold labels against that schema before any model
  calls. Use
  `pilot-splits/v6h-gepa-generous296-cap3-train.jsonl` for the current
  generous train reservoir; the four excluded over-cap rows are in
  `pilot-splits/v6h-gepa-generous296-overcap-review.jsonl`.
  text against v6 labels.
- Candidate lineage: every candidate dir now gets `lineage.json` (policy
  sha256, parent candidate index resolved via the producing reflection call,
  fixed-asset hashes, models). Validated against the v5 gpt run — it correctly
  reconstructs the search tree, including branches.

---

## Phase 0 — human freeze (no compute) — CHECKPOINT

1. Review `v6-prereview-convergent-disagreements.md` (8 rows where 2 of 3 task
   models stably converge against gold; all are dropped co-labels). Record one
   decision per row in `eval/openclaw/easy-set-pilot/v6/v6-prereview-decisions.jsonl`:

   ```json
   {"id": "openclaw-openclaw-52249", "decision": "keep", "note": "lane mechanics changed; queueing is central"}
   ```

   `decision` is `keep` (gold stands; guidance must teach it) or `flip`
   (co-label was anchoring/centrality artifact; provide `"labels": [...]`).

2. Review and edit `topic-boundary-guidance-v6b.md` and
   `task-boundary-overlay-v6b.md` until you'd defend every rule. These two files
   are the spec — Phase 1 results are only meaningful against the frozen text.
   If a Phase 0 decision contradicts a v6 rule draft, fix the rule now.

3. Freeze: commit the v6 folder before Phase 1.

```bash
git add eval/openclaw/easy-set-pilot/v6 scripts/openclaw-vanilla-f1-gepa.py
git commit -m "v6: frozen boundary spec, anchor-free teacher assets, overlay GEPA assets"
```

Report back with the 8 decisions (or "all keep") and any guidance edits.

---

## Phase 1 — anchor-free teacher revalidation

For the incremental build, use `V6_INTAKE_LADDER.md` instead of running the full
195-row revalidation in one shot. The commands below remain useful as the
full-set pattern after intake batches have stabilized the spec.

Input is `v6/revalidation-input.jsonl` (195 rows; the v5 train+test+dev rows
stripped to id/title/repo/item_type/number/target/github_context — no label or
teacher metadata). The v5 gold labels live separately in
`v6/v5-gold-reference.jsonl` (with v5 split membership) for the Phase 2
crosswalk comparison; the source sets themselves are on the `legacy` branch.

```bash
wc -l eval/openclaw/easy-set-pilot/v6/revalidation-input.jsonl   # expect 195
```

3× GPT-5.5-high anchor-free passes (same direct-batch stability harness as the
v4 teacher workflow):

```bash
python scripts/openclaw-easy-set-stability.py \
  --direct-batch \
  --input eval/openclaw/easy-set-pilot/v6/revalidation-input.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/v6/teacher-card-v6b.md \
  --agent-name openclaw_easy_set_pilot_teacher \
  --template eval/openclaw/easy-set-pilot/v6/teacher-template-v6-anchor-free.md \
  --schema eval/openclaw/easy-set-pilot/v6/teacher-output-v6b.schema.json \
  --model 'codexresponses.gpt-5.5?reasoning=high' \
  --runs 3 \
  --parallel 4 \
  --run-root runs/easy-set-v6b/revalidation \
  --run-name v6b-gpt55-anchor-free-3x \
  --trackio-project easy-v6b-databuild \
  --trackio-every 10 \
  --overwrite
```

2× Opus cross-check (2 runs so Opus self-stability is also measurable):

```bash
python scripts/openclaw-easy-set-stability.py \
  --direct-batch \
  --input eval/openclaw/easy-set-pilot/v6/revalidation-input.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/v6/teacher-card-v6b.md \
  --agent-name openclaw_easy_set_pilot_teacher \
  --template eval/openclaw/easy-set-pilot/v6/teacher-template-v6-anchor-free.md \
  --schema eval/openclaw/easy-set-pilot/v6/teacher-output-v6b.schema.json \
  --model 'opus' \
  --runs 2 \
  --parallel 4 \
  --run-root runs/easy-set-v6b/revalidation \
  --run-name v6b-opus-anchor-free-2x \
  --trackio-project easy-v6b-databuild \
  --trackio-every 10 \
  --overwrite
```

Budget note: 5 teacher passes × 195 rows ≈ 975 high-reasoning teacher
inferences. Run gpt-5.5 first; if its self-stability is poor (< ~80% exact-set
agreement), stop and report before spending the Opus passes — that would mean
the v6 guidance underdetermines too many rows and needs another freeze pass.

**CHECKPOINT — report completion.** I will then write the adjudication builder
against the actual output layout. The builder applies this decision matrix per
row:

| Anchor-free outcome | Action |
|---|---|
| gpt-5.5 exact-stable (3/3) AND Opus matches AND == current gold | confirm |
| gpt-5.5 exact-stable AND Opus matches AND != current gold | flip → review list |
| gpt-5.5 stable but Opus stable-disagrees | spec gap → review list |
| gpt-5.5 unstable across repeats | demote out of easy |

plus your Phase 0 decisions overriding gold on the 8 pre-reviewed rows. Output:
`easy-final-v6.jsonl`, a flips/demotions report for your adjudication, and
train/test splits that preserve v5 test membership for surviving rows.

---

## Phase 2 — build the v6 set (after Phase 1 checkpoint)

Commands will be finalized at the Phase 1 checkpoint (builder script
`scripts/openclaw-v6-build.py` to be written against the real revalidation
outputs). Expected flow:

```bash
python scripts/openclaw-v6-build.py \
  --revalidation-root runs/easy-set-v6b/revalidation \
  --source eval/openclaw/easy-set-pilot/v6/revalidation-input.jsonl \
  --prereview-decisions eval/openclaw/easy-set-pilot/v6/v6-prereview-decisions.jsonl \
  --v5-gold eval/openclaw/easy-set-pilot/v6/v5-gold-reference.jsonl \
  --outdir eval/openclaw/easy-set-pilot/v6
# → easy-final-v6.jsonl, easy-final-v6-train.jsonl, easy-final-v6-test.jsonl,
#   v6-flips-report.md (adjudicate), v6-demotions.jsonl (goes to medium/ASI pool)
```

You adjudicate `v6-flips-report.md`; re-run the builder with
`--adjudications` to finalize. Expect some shrinkage — a smaller test set you
can trust exact-match on beats 70 rows with anchor echoes.

Builder asserts (code-level, build fails loudly):

- every label in the schema enum; ids unique; splits disjoint
- no gold row exceeds 5 labels (maintainer cardinality cap)
- stability gate verified per row (3/3 gpt-5.5 exact-set + Opus match, or an
  adjudication record)
- every label that differs from v5 gold traceable to a decision record
- no retired labels in any v6 output (`model_serving`,
  `local_model_providers`, `open_weight_models`, `model_releases`,
  `hf_agents`, `hub_workflows`, `post_training`, `agent_demos`); relabel
  diffs on the inference family compared via the changelog crosswalk, not as
  plain flips
- cardinality-distribution sanity report vs v5 (avg expected ~3.3)

Judge audit (recorded artifact, not recomputed): on every flipped row plus a
random 15% sample, a teacher-model pass that cites, per label, the v6 MUST
rule justifying inclusion and confirms no satisfied MUST rule was omitted.
Disagreements feed the calibration loop, not silent edits.

---

## Phase 3 — GEPA arms (after v6 splits exist)

Models (v5 aliases): `codexresponses.gpt-5.4-mini`, `sonnet`, `deepseek`.
Drop qwen3.5-9b (not competitive in v5). gemma-e4 optional Arm A-only
(deterministic; one repeat suffices everywhere; add `--plain-labels`).

### Arm A — fair context + compact overlay (primary)

```bash
# repeat per MODEL_ALIAS / NAME in:
#   codexresponses.gpt-5.4-mini / gpt-5.4-mini ; sonnet / sonnet ; deepseek / deepseek4
python scripts/openclaw-vanilla-f1-gepa.py \
  --input eval/openclaw/easy-set-pilot/v6/easy-final-v6-train.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/v6/openclaw-vanilla-labeler-v6b.md \
  --allowed-topics eval/openclaw/easy-set-pilot/v6/allowed-topics-v6b.md \
  --seed-policy eval/openclaw/easy-set-pilot/v6/seed-policy-overlay-v6b.md \
  --static-asi eval/openclaw/easy-set-pilot/v6/vanilla-asi-v6b-slim.md \
  --boundary-guidance eval/openclaw/easy-set-pilot/v6/topic-boundary-guidance-v6b.md \
  --model 'MODEL_ALIAS' \
  --reflection-model 'codexresponses.gpt-5.5?reasoning=high' \
  --run-root runs/easy-set-v6b/gepa \
  --run-name NAME-v6b-overlay-batch-mc25 \
  --gepa-mode batch \
  --max-metric-calls 25 \
  --score-mode row-aware \
  --hygiene-penalty 0.03 \
  --policy-char-budget 8000 \
  --parallel 4 \
  --project easy-v6-gepa
```

No `--optimizer-cues` in Arm A: the reflection LM gets the slim ASI plus dynamic
per-candidate failure ASI only.

### Arm B — compression control (gpt-5.4-mini only)

No overlay in the task card; the full frozen v6 guidance goes to reflection as
static ASI, anti-copy penalties on. Measures what the task-context asymmetry
costs. (Do NOT use the v4 card or v4 static ASI here — both contain pre-
maintainer boundary text that now contradicts the v6 spec.)

```bash
python scripts/openclaw-vanilla-f1-gepa.py \
  --input eval/openclaw/easy-set-pilot/v6/easy-final-v6-train.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/v6/openclaw-vanilla-labeler-v6b.md \
  --allowed-topics eval/openclaw/easy-set-pilot/v6/allowed-topics-v6b.md \
  --seed-policy eval/openclaw/easy-set-pilot/v6/seed-policy-vanilla-v6b.md \
  --static-asi eval/openclaw/easy-set-pilot/v6/topic-boundary-guidance-v6b.md \
  --boundary-guidance eval/openclaw/easy-set-pilot/v6/topic-boundary-guidance-v6b.md \
  --model 'codexresponses.gpt-5.4-mini' \
  --reflection-model 'codexresponses.gpt-5.5?reasoning=high' \
  --run-root runs/easy-set-v6b/gepa \
  --run-name gpt-5.4-mini-v6b-compress-batch-mc25 \
  --gepa-mode batch \
  --max-metric-calls 25 \
  --score-mode row-aware \
  --hygiene-penalty 0.03 \
  --parallel 4 \
  --project easy-v6-gepa
```

### Candidate selection (winner's-curse guard — new in v6)

Do NOT take `best-policy.md` at face value for sampled models. After each run,
re-evaluate the top-3 candidates by recorded score, twice each, on the train
set, and pick the best mean:

```bash
# per candidate NNNN in top-3:
for r in 01 02; do
python scripts/openclaw-vanilla-f1-gepa.py \
  --evaluate-only \
  --input eval/openclaw/easy-set-pilot/v6/easy-final-v6-train.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/v6/openclaw-vanilla-labeler-v6b.md \
  --allowed-topics eval/openclaw/easy-set-pilot/v6/allowed-topics-v6b.md \
  --seed-policy runs/easy-set-v6b/gepa/RUN_NAME/candidate-NNNN/policy.md \
  --model 'MODEL_ALIAS' \
  --run-root runs/easy-set-v6b/selection \
  --run-name RUN_NAME-cNNNN-reval-r$r \
  --score-mode row-aware \
  --parallel 4 \
  --project easy-v6-gepa
done
```

(For gemma this is unnecessary — deterministic.) mc25 only; v5 showed the
mc25→mc50 continuation buys nothing.

**CHECKPOINT — report run names; I'll pull the candidate trajectories, check
hygiene/length of winning policies, and confirm selections before Phase 4.**

---

## Phase 4 — frozen test + baselines (3× repeats)

For each model, two stability runs on the v6 test set: the selected GEPA
policy and the seed (vanilla) policy. Pattern (Arm A; swap `--seed-policy` and
`--run-name` per row of the matrix):

```bash
python scripts/openclaw-easy-set-stability.py \
  --input eval/openclaw/easy-set-pilot/v6/easy-final-v6-test.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/v6/openclaw-vanilla-labeler-v6b.md \
  --allowed-topics eval/openclaw/easy-set-pilot/v6/allowed-topics-v6b.md \
  --seed-policy <SELECTED_POLICY.md | v6/seed-policy-overlay-v6b.md> \
  --model 'MODEL_ALIAS' \
  --runs 3 \
  --parallel 4 \
  --run-root runs/easy-set-v6b/stability \
  --wrapped-run-root runs/easy-set-v6b/baselines \
  --score-mode row-aware \
  --keep-vanilla-runs \
  --run-name NAME-<gepa-best|vanilla>-v6a-test-3x
```

Arm B test uses the v6b card. Also rerun the v5 winning policy
(`runs/easy-set-v5/gepa/gpt-5.4-mini-vanilla-gepa-asi-cues-batch-mc25/best-policy.md`
with the v4 card) on the v6 test once, so the v5→v6 label-spec shift is
quantified and v5 numbers are explicitly retired.

Headline comparisons this produces:

1. Arm A vanilla vs v5-style vanilla → value of fixed overlay alone
2. Arm A GEPA vs Arm A vanilla → what GEPA adds with fair context
3. Arm A GEPA vs Arm B GEPA → cost of the information asymmetry
4. Policy chars + hygiene findings A vs B → did the overlay contract hold
5. stable-wrong bucket vs v5 → did the label revalidation actually pay

**Final CHECKPOINT — report; I'll do the cross-arm analysis.**
