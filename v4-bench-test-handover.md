# v4 bench / GEPA test handover

## Current state

`easy-final-v4` is the clean easy-set track. It was built from v3 by removing the
highest-confusion rows and separating model-facing guidance from reflection/reference
material.

Canonical v4 eval artifacts live under:

```text
eval/openclaw/easy-set-pilot/
```

Run-management workspace lives under:

```text
runs/easy-set-v4/
```

Important files:

```text
eval/openclaw/easy-set-pilot/easy-final-v4.jsonl
eval/openclaw/easy-set-pilot/easy-final-v4-train.jsonl
eval/openclaw/easy-set-pilot/easy-final-v4-test.jsonl
eval/openclaw/easy-set-pilot/allowed-topics-v4.md
eval/openclaw/easy-set-pilot/allowed-topics-v4-cues.md
eval/openclaw/easy-set-pilot/seed-policy-vanilla-v4.md
eval/openclaw/easy-set-pilot/seed-policy-guided-v4.md
eval/openclaw/easy-set-pilot/vanilla-asi-v4.md
eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v4.md
eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-plain-v4.md
eval/openclaw/easy-set-pilot/teacher-card-v4.md
eval/openclaw/topic-boundary-guidance.md
eval/openclaw/asi-pack-v4.md
```

`topic-boundary-guidance.md` is generated from:

```text
src/openclaw_gepa/openclaw_benchmark.py TOPIC_HINTS
```

Use:

```bash
python scripts/openclaw-sync-topic-boundary-guidance.py --check
```

to verify it is synchronized.

## Label generation status

The reference GPT-5.5 high teacher relabel evidence is copied under:

```text
runs/easy-set-v4/label-generation/gpt55-final-reference/
```

Current reference result:

```text
source rows:      125
teacher rows:     125
exact agreement:  125 / 125
changed rows:     0
teacher buckets:  easy: 125
```

Because `teacher-card-v4.md` was later changed to include benchmark-aligned boundary
overlays from `eval/openclaw/topic-boundary-guidance.md`, rerun one teacher relabel before
considering the new teacher prompt canonical.

Repeat command:

```bash
OUTDIR=runs/easy-set-v4/label-generation/gpt55-benchmark-aligned-$(date +%Y%m%d-%H%M%S)
mkdir -p "$OUTDIR"

fast-agent --no-update-check \
  --env .fast-agent \
  batch run \
  --agent-card eval/openclaw/easy-set-pilot/teacher-card-v4.md \
  --agent openclaw_easy_set_pilot_teacher \
  --input eval/openclaw/easy-set-pilot/easy-final-v4.jsonl \
  --output "$OUTDIR/teacher-labels.raw.jsonl" \
  --template eval/openclaw/easy-set-pilot/teacher-template-v4-clean.md \
  --json-schema eval/openclaw/easy-set-pilot/teacher-output.schema.json \
  --model 'codexresponses.gpt-5.5?reasoning=high' \
  --id-field id \
  --include-input \
  --parallel 4 \
  --overwrite \
  --no-final-summary

python scripts/openclaw-easy-set-pilot-stratify.py \
  --input eval/openclaw/easy-set-pilot/easy-final-v4.jsonl \
  --outdir "$OUTDIR" \
  --raw-output "$OUTDIR/teacher-labels.raw.jsonl"

python scripts/openclaw-compare-teacher-labels.py \
  --source eval/openclaw/easy-set-pilot/easy-final-v4.jsonl \
  --teacher "$OUTDIR/teacher-labels.jsonl" \
  --outdir "$OUTDIR" \
  --name "$(basename "$OUTDIR")-current-source"
```

Expected target remains `125 / 125` exact agreement and `0` changed rows.

## Prompt / information-flow design

Task model sees:

```text
openclaw-vanilla-labeler-v4.md
allowed-topics-v4.md
current candidate policy
GitHub row context
```

Task model does **not** directly see:

```text
vanilla-asi-v4.md
allowed-topics-v4-cues.md
topic-boundary-guidance.md
```

unless GEPA distills some of that into the mutable candidate policy.

GEPA reflection sees:

```text
objective.md              # optimization target and hygiene constraints
background.md             # fixed taxonomy, static ASI, optional cues
evaluator side_info       # candidate metrics, failures, topic errors, row examples
```

`--static-asi` and `--optimizer-cues` are now supplied through GEPA's `background` /
domain-context channel. Future candidate side-info drops the large duplicate
`static_asi_pack` emitted by the benchmark scorer and keeps only a path marker.

## Current GEPA command shape

For GPT-5.4-mini with GPT-5.5 high reflection:

```bash
python scripts/openclaw-vanilla-f1-gepa.py \
  --input eval/openclaw/easy-set-pilot/easy-final-v4-train.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v4.md \
  --allowed-topics eval/openclaw/easy-set-pilot/allowed-topics-v4.md \
  --seed-policy eval/openclaw/easy-set-pilot/seed-policy-vanilla-v4.md \
  --static-asi eval/openclaw/easy-set-pilot/vanilla-asi-v4.md \
  --optimizer-cues eval/openclaw/easy-set-pilot/allowed-topics-v4-cues.md \
  --model 'codexresponses.gpt-5.4-mini' \
  --reflection-model 'codexresponses.gpt-5.5?reasoning=high' \
  --run-root runs/easy-set-v4/gepa \
  --run-name gpt-5.4-mini-vanilla-gepa-asi-cues-rowaware-mc20 \
  --max-metric-calls 20 \
  --score-mode row-aware \
  --parallel 4 \
  --project easy-v4-gepa-test
```

Evaluate best policy on held-out:

```bash
python scripts/openclaw-vanilla-f1-gepa.py \
  --evaluate-only \
  --input eval/openclaw/easy-set-pilot/easy-final-v4-test.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v4.md \
  --allowed-topics eval/openclaw/easy-set-pilot/allowed-topics-v4.md \
  --seed-policy runs/easy-set-v4/gepa/gpt-5.4-mini-vanilla-gepa-asi-cues-rowaware-mc20/best-policy.md \
  --model 'codexresponses.gpt-5.4-mini' \
  --run-root runs/easy-set-v4/baselines \
  --run-name gpt-5.4-mini-gepa-best-test \
  --parallel 4 \
  --score-mode row-aware \
  --project easy-v4-gepa-test
```

For weak/local models, use `--plain-labels`:

```bash
python scripts/openclaw-vanilla-f1-gepa.py \
  --plain-labels \
  --input eval/openclaw/easy-set-pilot/easy-final-v4-train.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v4.md \
  --allowed-topics eval/openclaw/easy-set-pilot/allowed-topics-v4.md \
  --seed-policy eval/openclaw/easy-set-pilot/seed-policy-vanilla-v4.md \
  --static-asi eval/openclaw/easy-set-pilot/vanilla-asi-v4.md \
  --optimizer-cues eval/openclaw/easy-set-pilot/allowed-topics-v4-cues.md \
  --model 'gemma-e4' \
  --reflection-model 'codexresponses.gpt-5.5?reasoning=high' \
  --run-root runs/easy-set-v4/gepa \
  --run-name gemma-e4-plain-vanilla-gepa-asi-cues-rowaware-mc20 \
  --max-metric-calls 20 \
  --score-mode row-aware \
  --parallel 4 \
  --project easy-v4-gepa-test
```

`--plain-labels` now resolves the v4 sibling card automatically:

```text
eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-plain-v4.md
```

## Current v4 vs v3 results

Caveat: v3 and v4 are not the same test set. v4 removed high-confusion rows, so higher
v4 scores partly reflect cleaner/easier exact-match easy rows. That is expected and is the
point of v4.

### GPT-5.4-mini held-out

```text
v3 base test:
  GEPA score:       0.6233
  F1:               0.7739
  row exact:        0.200
  row Jaccard:      0.6546
  avg symdiff:      1.30
  FP / FN:          4 / 48
  avg pred / exp:   2.325 / 3.425

v3 GEPA-best test:
  GEPA score:       0.7190
  F1:               0.8450
  row exact:        0.350
  row Jaccard:      0.7550
  avg symdiff:      1.00
  FP / FN:          12 / 28
  avg pred / exp:   3.025 / 3.425

v4 vanilla test:
  GEPA score:       0.6554
  F1:               0.7860
  row exact:        0.300
  row Jaccard:      0.6746
  avg symdiff:      1.225
  FP / FN:          3 / 46
  avg pred / exp:   2.325 / 3.400

v4 guided test:
  GEPA score:       0.6074
  F1:               0.7434
  row exact:        0.225
  row Jaccard:      0.6358
  avg symdiff:      1.45
  FP / FN:          6 / 52
  avg pred / exp:   2.250 / 3.400

v4 GEPA-best test:
  GEPA score:       0.8064
  F1:               0.8996
  row exact:        0.525
  row Jaccard:      0.8388
  avg symdiff:      0.675
  FP / FN:          12 / 15
  avg pred / exp:   3.325 / 3.400
```

Interpretation for GPT-5.4-mini:

- v4 vanilla beats v3 base.
- v4 guided is worse than v4 vanilla.
- v4 GEPA-best beats v3 GEPA-best clearly on held-out.
- Best current strategy is short vanilla seed + ASI/cues as GEPA background.

### GPT-5.4-mini train GEPA

```text
v3 best train:
  GEPA score:       0.8162
  F1:               0.9037
  row exact:        0.550
  Jaccard:          0.8479
  symdiff:          0.6125
  FP / FN:          16 / 33
  policy chars:     12775

v4 best train:
  GEPA score:       0.8114
  F1:               0.9069
  row exact:        0.5125
  Jaccard:          0.8515
  symdiff:          0.5875
  FP / FN:          20 / 27
  policy chars:     10813
```

Train is roughly tied; held-out favors v4.

### Sonnet train GEPA

```text
v3 sonnet best:
  GEPA score:       0.8378
  F1:               0.9205
  row exact:        0.575
  Jaccard:          0.8750
  symdiff:          0.5375
  FP / FN:          29 / 14
  policy chars:     13499

v4 sonnet best:
  GEPA score:       0.8675
  F1:               0.9369
  row exact:        0.650
  Jaccard:          0.8967
  symdiff:          0.4125
  FP / FN:          22 / 11
  policy chars:     10663
```

Sonnet is a clean v4 win on train.

### DeepSeek train GEPA

```text
v3 deepseek4 best:
  GEPA score:       0.7538
  F1:               0.8691
  row exact:        0.400
  Jaccard:          0.7976
  symdiff:          0.8625
  FP / FN:          35 / 34
  policy chars:     11763

v4 deepseek4 best:
  GEPA score:       0.7429
  F1:               0.8703
  row exact:        0.3625
  Jaccard:          0.7842
  symdiff:          0.775
  FP / FN:          14 / 48
  policy chars:     5983
```

DeepSeek v4 is more conservative: fewer FPs, more FNs. Aggregate is slightly worse.

### Gemma train GEPA

```text
v3 gemma best:
  GEPA score:       0.7218
  F1:               0.8442
  row exact:        0.3625
  Jaccard:          0.7575
  symdiff:          0.9875
  FP / FN:          30 / 49
  policy chars:     14211

v4 gemma best:
  GEPA score:       0.6643
  F1:               0.7940
  row exact:        0.300
  Jaccard:          0.6910
  symdiff:          1.20
  FP / FN:          25 / 71
  policy chars:     3213
```

Gemma is lackluster in v4. It under-labels hard and should be treated as a weak-model
stress test, not the primary validation signal.

## Current conclusions

1. **v4 works well for GPT-5.4-mini.** Held-out GEPA-best improved materially over v3.
2. **v4 works well for Sonnet.** Train metrics improve with shorter policy.
3. **Guided task seed hurts GPT-5.4-mini.** Do not use `seed-policy-guided-v4.md` as the default task seed.
4. **Weak models under-label.** Gemma and DeepSeek need different treatment if they matter.
5. **Best default setup:**

```text
seed policy:       seed-policy-vanilla-v4.md
GEPA background:   vanilla-asi-v4.md + allowed-topics-v4-cues.md
score mode:        row-aware
```

## Mutation / reflection observations

For the GPT-5.4-mini v4 run:

- Candidate 1 was the short vanilla seed and under-labeled badly.
- Candidate 2 improved strongly by adding reusable co-label/boundary rules.
- Candidate policies did **not** copy `Allowed Topics v4`, cue-word tables, row IDs,
  `easy-final`, or `confusion-bucket` text.
- Candidate 2 improved train GEPA score from `0.6704` to `0.7578`.
- Best scored train candidate was candidate 8 with GEPA score `0.8114`.
- Held-out GEPA-best score was `0.8064`, so train-to-test transfer looks good.

Patch note: the current GPT-5.4-mini run was started before removing duplicate
`static_asi_pack` from candidate side-info. Future runs will be cleaner and smaller.

## Recommended next steps

1. Rerun the teacher label generation once with the benchmark-aligned teacher card.
2. Use GPT-5.4-mini as the main v4 validation model.
3. Optionally run Sonnet as upper-bound confirmation.
4. Do not spend much budget on Gemma unless weak-model support is important.
5. For DeepSeek/Gemma, try a shorter, recall-friendlier weak-model policy if needed.
6. Keep `seed-policy-guided-v4.md` as a diagnostic/baseline only; do not use it by default.
7. For new GEPA runs, use the patched runner so static ASI is in `background` and not duplicated in every side-info trajectory.

## Useful comparison command

```bash
python - <<'PY'
import json
from pathlib import Path

paths = {
    'v4 vanilla': Path('runs/easy-set-v4/baselines/gpt-5.4-mini-vanilla-test/evaluate-only.json'),
    'v4 guided': Path('runs/easy-set-v4/baselines/gpt-5.4-mini-guided-test/evaluate-only.json'),
    'v4 gepa-best': Path('runs/easy-set-v4/baselines/gpt-5.4-mini-gepa-best-test/evaluate-only.json'),
}

for name, path in paths.items():
    data = json.loads(path.read_text())
    side = data.get('side_info', data)
    scores = side.get('scores', {})
    details = side.get('score_details', {})
    print('\n' + name)
    for key in ['gepa_score', 'topic_micro_f1', 'row_exact_accuracy', 'avg_row_jaccard']:
        print(f'  {key}:', scores.get(key, details.get(key)))
    for key in ['avg_row_symdiff', 'false_positives', 'false_negatives', 'avg_predicted_topics', 'avg_expected_topics']:
        print(f'  {key}:', details.get(key))
PY
```
