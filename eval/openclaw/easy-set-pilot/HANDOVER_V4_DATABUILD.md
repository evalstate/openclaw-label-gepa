# Handover: easy-final-v4 databuild

## Status

`easy-final-v4` is the current curated easy-set track.

It was built from the reviewed `easy-final-v3` source by removing the highest-confusion
rows identified from recent `easy-final-v3` benchmark/GEPA analysis. Topic IDs are
unchanged; v4 changes are data curation plus prompt/guidance restructuring.

Current v4 counts:

```text
easy-final-v4.jsonl                  125
easy-final-v4-train.jsonl             80
easy-final-v4-test.jsonl              40
easy-final-v4-unused.jsonl             5
easy-final-v4-confusion-bucket.jsonl  16
```

Validation performed:

- v4 train/test/unused partition `easy-final-v4.jsonl`;
- no confusion-bucket rows leak into v4 train/test/unused;
- all expected topics are schema-valid;
- v4 cards include concise `allowed-topics-v4.md`;
- v4 cards do not include cue-heavy `allowed-topics-v4-cues.md` by default.

## High-priority review artifacts

Review these first:

```text
V4_PROMPT_GUIDANCE_REVIEW.md       # why prompt/guidance was restructured
V4_GEPA_MUTATION_SURFACE.md        # exactly what GEPA mutates vs keeps fixed
V4_LABEL_CREATION_STABILITY.md     # GPT-5.5/Opus teacher relabel/stability workflow
V4_BOUNDARY_AND_TEST_PLAN.md       # benchmark/GEPA/stability commands and success criteria
```

Data summaries:

```text
easy-final-v4-build-summary.json
easy-final-v4-summary.json
easy-final-v4-confusion-bucket.jsonl
```

Evidence that motivated v4:

```text
runs/openclaw-vanilla-f1-gepa/easy-final-v3-row-stability-analysis.md
runs/openclaw-vanilla-f1-gepa/easy-final-v3-row-stability-analysis.json
```

## v4 data artifacts

Primary easy source and splits:

```text
eval/openclaw/easy-set-pilot/easy-final-v4.jsonl
eval/openclaw/easy-set-pilot/easy-final-v4-train.jsonl
eval/openclaw/easy-set-pilot/easy-final-v4-test.jsonl
eval/openclaw/easy-set-pilot/easy-final-v4-unused.jsonl
eval/openclaw/easy-set-pilot/easy-final-v4-summary.json
```

Boundary/confusion rows removed from easy exact-match evaluation:

```text
eval/openclaw/easy-set-pilot/easy-final-v4-confusion-bucket.jsonl
```

Other boundary/reference buckets that remain useful:

```text
eval/openclaw/easy-set-pilot/easy-final-v3-opus-disagreements.jsonl
eval/openclaw/easy-set-pilot/medium-asi-easy-final-v2-instability.jsonl
```

## v4 prompt/guidance artifacts

Model-facing taxonomy:

```text
eval/openclaw/easy-set-pilot/allowed-topics-v4.md
```

Long cue/reference taxonomy, not included by default in task prompts:

```text
eval/openclaw/easy-set-pilot/allowed-topics-v4-cues.md
```

True vanilla seed:

```text
eval/openclaw/easy-set-pilot/seed-policy-vanilla-v4.md
```

Compact guided/boundary seed:

```text
eval/openclaw/easy-set-pilot/seed-policy-guided-v4.md
```

Compatibility alias for older command shapes; prefer the clearer `seed-policy-guided-v4.md` name:

```text
eval/openclaw/easy-set-pilot/seed-policy-vanilla-v4-asi.md
```

Human/reflection ASI notes:

```text
eval/openclaw/easy-set-pilot/vanilla-asi-v4.md
```

Task cards:

```text
eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v4.md
eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-plain-v4.md
```

Teacher/adjudicator assets:

```text
eval/openclaw/easy-set-pilot/teacher-card-v4.md
eval/openclaw/easy-set-pilot/teacher-template-v4-clean.md
eval/openclaw/easy-set-pilot/teacher-output.schema.json
```

## Important terminology

### Vanilla benchmark

A vanilla benchmark uses:

```text
allowed-topics-v4.md
seed-policy-vanilla-v4.md
```

No topic-specific boundary seed. No static ASI.

Use it to measure raw model ability against the concise taxonomy and basic centrality
instruction.

### Guided benchmark

A guided benchmark uses:

```text
allowed-topics-v4.md
seed-policy-guided-v4.md
```

Use it to test whether compact model-facing boundary rules improve row-level label
reproduction.

### Teacher relabel / label creation

Teacher relabeling is separate from vanilla/guided model-under-test benchmarks. It uses:

```text
teacher-card-v4.md
teacher-template-v4-clean.md
teacher-output.schema.json
allowed-topics-v4.md
```

It is intended for GPT-5.5 high / Opus label adjudication, repeated-run stability, and
cross-model agreement checks.

## What GEPA mutates

For `scripts/openclaw-vanilla-f1-gepa.py`, GEPA mutates only the candidate variable:

```json
{"policy": "..."}
```

That variable is injected into the task AgentCard at:

```md
## Routing policy

{{policy}}
```

GEPA does **not** mutate:

```text
--agent-card
--allowed-topics
--input
--template
--schema
```

For v4, the model under test sees:

```text
openclaw-vanilla-labeler-v4.md
allowed-topics-v4.md
mutable policy from --seed-policy
GitHub row input
```

`--static-asi` is not inserted into the task AgentCard by the current runner. It is copied
into the run directory and attached to the score/report side-info, so GEPA reflection may
see it, but the task model does not directly see it during batch labeling.

See:

```text
eval/openclaw/easy-set-pilot/V4_GEPA_MUTATION_SURFACE.md
```

## Label creation / validation workflow

Use this when checking whether v4 boundary conditions change labels.

### 1. Single GPT-5.5 high relabel

```bash
mkdir -p eval/openclaw/easy-set-pilot/v4-relabel-gpt55

fast-agent --no-update-check \
  --env .fast-agent \
  batch run \
  --agent-card eval/openclaw/easy-set-pilot/teacher-card-v4.md \
  --agent openclaw_easy_set_pilot_teacher \
  --input eval/openclaw/easy-set-pilot/easy-final-v4.jsonl \
  --output eval/openclaw/easy-set-pilot/v4-relabel-gpt55/teacher-labels.raw.jsonl \
  --template eval/openclaw/easy-set-pilot/teacher-template-v4-clean.md \
  --json-schema eval/openclaw/easy-set-pilot/teacher-output.schema.json \
  --model 'codexresponses.gpt-5.5?reasoning=high' \
  --id-field id \
  --include-input \
  --parallel 4 \
  --overwrite \
  --no-final-summary
```

Postprocess:

```bash
python scripts/openclaw-easy-set-pilot-stratify.py \
  --input eval/openclaw/easy-set-pilot/easy-final-v4.jsonl \
  --outdir eval/openclaw/easy-set-pilot/v4-relabel-gpt55 \
  --raw-output eval/openclaw/easy-set-pilot/v4-relabel-gpt55/teacher-labels.raw.jsonl
```

Compare to current v4 labels:

```bash
python scripts/openclaw-compare-teacher-labels.py \
  --source eval/openclaw/easy-set-pilot/easy-final-v4.jsonl \
  --teacher eval/openclaw/easy-set-pilot/v4-relabel-gpt55/teacher-labels.jsonl \
  --outdir eval/openclaw/easy-set-pilot/v4-relabel-gpt55 \
  --name v4-relabel-gpt55
```

Review:

```text
eval/openclaw/easy-set-pilot/v4-relabel-gpt55/changed-rows.md
eval/openclaw/easy-set-pilot/v4-relabel-gpt55/comparison-to-source.json
```

Expected outcome: changes should be rare in the easy source. Any changes should be
review triggers, not automatic replacements.

### 2. Repeated GPT-5.5 high stability

```bash
python scripts/openclaw-easy-set-stability.py \
  --direct-batch \
  --input eval/openclaw/easy-set-pilot/easy-final-v4.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/teacher-card-v4.md \
  --agent-name openclaw_easy_set_pilot_teacher \
  --template eval/openclaw/easy-set-pilot/teacher-template-v4-clean.md \
  --schema eval/openclaw/easy-set-pilot/teacher-output.schema.json \
  --model 'codexresponses.gpt-5.5?reasoning=high' \
  --runs 3 \
  --parallel 4 \
  --run-name easy-final-v4-gpt55-teacher-stability \
  --overwrite
```

Review:

```text
runs/openclaw-easy-set-stability/easy-final-v4-gpt55-teacher-stability/stability-report.md
runs/openclaw-easy-set-stability/easy-final-v4-gpt55-teacher-stability/unstable-rows.jsonl
```

### 3. Opus cross-check

Same pattern, with:

```text
--model 'opus'
--outdir eval/openclaw/easy-set-pilot/v4-relabel-opus
```

Review:

```text
eval/openclaw/easy-set-pilot/v4-relabel-opus/changed-rows.md
eval/openclaw/easy-set-pilot/v4-relabel-opus/comparison-to-source.json
```

### 4. Boundary bucket relabeling

Run teacher relabels on:

```text
easy-final-v4-confusion-bucket.jsonl
easy-final-v3-opus-disagreements.jsonl
medium-asi-easy-final-v2-instability.jsonl
```

This checks whether label changes are isolated to rows where boundary conditions changed.
Rows where GPT-5.5 high and Opus agree exactly under v4 guidance can be considered for
promotion; unstable rows stay boundary/ASI/medium.

## Promotion rule

Keep/promote a row as easy only when:

- repeated GPT-5.5 high labels are exact-stable;
- Opus agrees, or disagreement is manually adjudicated;
- teacher bucket is `easy`;
- confidence is high and ambiguity is low;
- labels follow v4 boundary rules;
- the row does not require several boundary exceptions.

Do not automatically replace human/adjudicated labels from one teacher pass.

## Benchmark commands

### Vanilla held-out benchmark

```bash
python scripts/openclaw-vanilla-f1-gepa.py \
  --evaluate-only \
  --input eval/openclaw/easy-set-pilot/easy-final-v4-test.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v4.md \
  --allowed-topics eval/openclaw/easy-set-pilot/allowed-topics-v4.md \
  --seed-policy eval/openclaw/easy-set-pilot/seed-policy-vanilla-v4.md \
  --model 'MODEL_ALIAS' \
  --run-name easy-final-v4-test-MODEL-vanilla-v4 \
  --parallel 4 \
  --score-mode row-aware \
  --no-trackio
```

### Guided held-out benchmark

```bash
python scripts/openclaw-vanilla-f1-gepa.py \
  --evaluate-only \
  --input eval/openclaw/easy-set-pilot/easy-final-v4-test.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v4.md \
  --allowed-topics eval/openclaw/easy-set-pilot/allowed-topics-v4.md \
  --seed-policy eval/openclaw/easy-set-pilot/seed-policy-guided-v4.md \
  --model 'MODEL_ALIAS' \
  --run-name easy-final-v4-test-MODEL-guided-v4 \
  --parallel 4 \
  --score-mode row-aware \
  --no-trackio
```

Compare vanilla vs guided on:

```text
row_exact_accuracy
avg_row_jaccard
avg_row_symdiff
false_positives
false_negatives
avg_predicted_topics vs avg_expected_topics
```

## GEPA commands

### Vanilla GEPA

```bash
python scripts/openclaw-vanilla-f1-gepa.py \
  --input eval/openclaw/easy-set-pilot/easy-final-v4-train.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v4.md \
  --allowed-topics eval/openclaw/easy-set-pilot/allowed-topics-v4.md \
  --seed-policy eval/openclaw/easy-set-pilot/seed-policy-vanilla-v4.md \
  --model 'MODEL_ALIAS' \
  --reflection-model 'codexresponses.gpt-5.5?reasoning=high' \
  --max-metric-calls 20 \
  --score-mode row-aware \
  --parallel 4 \
  --run-name easy-final-v4-MODEL-vanilla-gepa-rowaware-mc20
```

### GEPA with reflection-side ASI

```bash
python scripts/openclaw-vanilla-f1-gepa.py \
  --input eval/openclaw/easy-set-pilot/easy-final-v4-train.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v4.md \
  --allowed-topics eval/openclaw/easy-set-pilot/allowed-topics-v4.md \
  --seed-policy eval/openclaw/easy-set-pilot/seed-policy-vanilla-v4.md \
  --static-asi eval/openclaw/easy-set-pilot/vanilla-asi-v4.md \
  --model 'MODEL_ALIAS' \
  --reflection-model 'codexresponses.gpt-5.5?reasoning=high' \
  --max-metric-calls 20 \
  --score-mode row-aware \
  --parallel 4 \
  --run-name easy-final-v4-MODEL-vanilla-gepa-reflection-asi-rowaware-mc20
```

Only run guided GEPA if guided held-out benchmarks clearly improve over vanilla.

## Suggested next steps

1. Run single GPT-5.5 high v4 teacher relabel on `easy-final-v4.jsonl`.
2. Compare changes with `scripts/openclaw-compare-teacher-labels.py`.
3. Run repeated GPT-5.5 high teacher stability if the single pass is clean.
4. Run Opus cross-check.
5. Run vanilla and guided held-out benchmarks for one or two target models.
6. If label creation is stable and guided improves held-out metrics, proceed to v4 GEPA.
7. Keep confusion/boundary buckets separate unless strong-model stability supports promotion.

## Notes / cautions

- Do not compare runs named `vanilla` if they used `seed-policy-guided-v4.md` or the old
  `seed-policy-vanilla-v4-asi.md` alias.
- Do not use `allowed-topics-v4-cues.md` in task-model prompts by default; it is a
  reference artifact.
- Do not automatically apply single-pass teacher changes.
- Watch for under-labeling: previous over-conservative guidance produced very low false
  positives but many false negatives.
