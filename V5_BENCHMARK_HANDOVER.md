# V5 benchmark handover

Date: 2026-06-11

This handover captures the current OpenClaw easy-set v5 GEPA benchmark state:
data split, runner changes, completed GEPA-best 3× test results, currently
running baseline jobs, and next steps.

## Current goal

Benchmark OpenClaw topic-label policies on the v5 easy-set split, with:

- batch-mode GEPA training;
- row-aware scoring;
- repeated test evaluation for stability;
- vanilla baseline vs GEPA-best improvement reporting.

The label generator/gold labels are considered stable. The main question is model
quality and run-to-run prediction stability for smaller/economical models.

## Important files

### Data split

Use exactly these v5 split files:

```text
eval/openclaw/easy-set-pilot/easy-set-400-full-120train-70test-train.jsonl   120 rows
eval/openclaw/easy-set-pilot/easy-set-400-full-120train-70test-test.jsonl     70 rows
eval/openclaw/easy-set-pilot/easy-set-400-full-120train-70test-unused.jsonl    5 rows
```

The 5-row unused split is only a smoke set, not a meaningful dev set.

### V5 runbook

```text
eval/openclaw/easy-set-pilot/V5_GEPA_RUNSET.md
```

This contains copy/paste commands for v5 batch GEPA and test evaluation.

### Runner

```text
scripts/openclaw-vanilla-f1-gepa.py
```

Relevant changes in the working tree:

- supports `--gepa-mode batch|row-wise`;
- supports `--reflection-minibatch-size`;
- moves `--static-asi` and `--optimizer-cues` into GEPA background;
- has row-wise GEPA adapter, though current v5 regime uses batch mode;
- adds policy length penalty:

```text
policy_char_budget = 12_000
policy_length_penalty = min(0.10, max(0, policy_chars - 12_000) / 10_000 * 0.05)
gepa_score = max(0, composite_score - policy_length_penalty)
```

- exposes frontier/detail fields:

```text
composite_score
policy_length_compliance
policy_length_penalty
policy_length_over_budget
policy_char_budget
```

For `--score-mode row-aware`, the composite score is:

```text
0.50 * topic_micro_f1
+ 0.20 * row_exact_accuracy
+ 0.30 * avg_row_jaccard
```

### Static ASI

```text
eval/openclaw/easy-set-pilot/vanilla-asi-v4.md
```

This was updated with train-mined instability overlays:

- `reliability`: runtime robustness only; not generic bug/CI/error-message UX.
- `config`: config must be the subject, not merely a mentioned mechanism/key.
- `agent_runtime` vs `coding_agents` vs `acp` vs `sessions`: decisive boundary rules.
- `model_releases`: adding/removing/updating model catalog entries/model IDs implies
  `model_releases`.

These were mined from train-set repeated rescoring, not final test leakage.

## Score modes available

In `scripts/openclaw-vanilla-f1-gepa.py`:

```text
--score-mode f1
--score-mode row-aware
```

Current v5 benchmark uses:

```text
--score-mode row-aware
```

## GEPA training regime

For the completed v5 GEPA-best policies:

```text
GEPA mode:      batch
score mode:     row-aware
metric budget:  --max-metric-calls 25
train rows:     120
reflection LM:  codexresponses.gpt-5.5?reasoning=high
static ASI:     eval/openclaw/easy-set-pilot/vanilla-asi-v4.md
optimizer cues: eval/openclaw/easy-set-pilot/allowed-topics-v4-cues.md
seed policy:    eval/openclaw/easy-set-pilot/seed-policy-vanilla-v4.md
project:        easy-v5-gepa-test
```

Important: `--max-metric-calls 25` produced only about 10-11 scored candidate
policies in the observed batch runs, not 25 useful mutations. The mc25 runs
look under-budgeted for at least GPT-5.4-mini and Gemma-e4 because their best
candidate was the last candidate.

## Completed GEPA train artifacts

Best policies used for current 3× test:

```text
runs/easy-set-v5/gepa/gpt-5.4-mini-vanilla-gepa-asi-cues-batch-mc25/best-policy.md
runs/easy-set-v5/gepa/gemma-e4-mini-vanilla-gepa-asi-cues-batch-mc25/best-policy.md
runs/easy-set-v5/gepa/deepseek4-mini-vanilla-gepa-asi-cues-batch-mc25/best-policy.md
```

Gemma train used the plain-label card/output contract. Keep `--plain-labels` for
Gemma evaluation.

### Train trajectory summary

#### GPT-5.4-mini mc25

```text
candidates: 10
best:       candidate-0010 (last candidate)
score:      0.7418
composite:  0.7439
F1:         0.8630
row exact:  0.4000
Jaccard:    0.7747
FP/FN:      32 / 74
chars:      12,437
penalty:    0.0022
```

Trajectory:

```text
0001 0.5930
0002 0.6694
0003 0.6898
0004 0.7244
0005 0.7118
0006 0.7325
0007 0.7045
0008 0.7144
0009 0.7308
0010 0.7418  <-- best, last
```

Interpretation: likely stopped too early.

#### Gemma-e4 mc25

```text
candidates: 10
best:       candidate-0010 (last candidate)
score:      0.6308
composite:  0.6308
F1:         0.7739
row exact:  0.2250
Jaccard:    0.6626
FP/FN:      72 / 105
chars:      10,431
penalty:    0.0000
```

Trajectory:

```text
0001 0.5955
0002 0.6044
0003 0.6047
0004 0.6045
0005 0.6025
0006 0.6041
0007 0.5814
0008 0.6049
0009 0.6130
0010 0.6308  <-- best, last
```

Interpretation: likely stopped too early, but model is mostly stably wrong on
test, so more budget may improve quality but stability is not the bottleneck.

#### DeepSeek mc25

```text
candidates: 11
best:       candidate-0010
last:       candidate-0011 regressed
score:      0.6742
composite:  0.6811
F1:         0.8126
row exact:  0.3083
Jaccard:    0.7105
FP/FN:      64 / 85
chars:      13,386
penalty:    0.0069
```

Trajectory:

```text
0001 0.5924
0002 0.6315
0003 0.6139
0004 0.6040
0005 0.6285
0006 0.6384
0007 0.6525
0008 0.5834
0009 0.6462
0010 0.6742  <-- best
0011 0.6252
```

Interpretation: maybe under-budgeted, but less clearly than GPT/Gemma.

## Completed GEPA-best 3× test results

All three GEPA-best policies have now completed 3 repeated test runs on the
70-row test split.

### Quality table

| model | score mean ± sd | F1 | row exact | Jaccard | symdiff | FP/FN mean |
|---|---:|---:|---:|---:|---:|---:|
| GPT-5.4-mini | **0.6902 ± 0.0117** | 0.8175 | 0.3333 | 0.7233 | 1.1476 | 28.3 / 52.0 |
| DeepSeek | **0.6228 ± 0.0260** | 0.7721 | 0.2333 | 0.6567 | 1.4714 | 45.7 / 57.3 |
| Gemma-e4 | **0.5608 ± 0.0034** | 0.7067 | 0.1619 | 0.5836 | 1.8857 | 59.0 / 73.0 |

### Stability table

| model | pairwise exact rate | pairwise prediction Jaccard | pairwise symdiff | stable correct | stable wrong | unstable/review |
|---|---:|---:|---:|---:|---:|---:|
| Gemma-e4 | **0.9619** | **0.9856** | **0.0667** | 11 | 55 | 4 |
| GPT-5.4-mini | 0.6000 | 0.8526 | 0.5714 | 16 | 17 | 37 |
| DeepSeek | 0.2667 | 0.6881 | 1.2286 | 6 | 3 | 61 |

### Interpretation

- GPT-5.4-mini is the quality leader but has meaningful output instability.
- Gemma-e4 is extremely stable but mostly stably wrong.
- DeepSeek is between GPT and Gemma on quality, but highly unstable in this 3× run.

## Completed GEPA-best stability dirs

```text
runs/easy-set-v5/stability/gpt-5.4-mini-gepa-best-test-3x/
runs/easy-set-v5/stability/gemma-e4-gepa-best-test-3x/
runs/easy-set-v5/stability/deepseek4-gepa-best-test-3x/
```

Each contains:

```text
stability-report.json
stability-report.md
repeat-01/
repeat-02/
repeat-03/
unstable-row-ids.txt
unstable-rows.jsonl
```

## Currently running jobs

### Vanilla baseline 3× jobs

These were launched in the background to produce improvement deltas:

```text
gpt-5.4-mini vanilla: PID 277748
gemma-e4 vanilla:     PID 277749
deepseek4 vanilla:    PID 277750
```

PID files:

```text
runs/easy-set-v5/logs/gpt-5.4-mini-vanilla-test-3x.pid
runs/easy-set-v5/logs/gemma-e4-vanilla-test-3x.pid
runs/easy-set-v5/logs/deepseek4-vanilla-test-3x.pid
```

Nohup logs:

```text
runs/easy-set-v5/logs/gpt-5.4-mini-vanilla-test-3x.nohup.log
runs/easy-set-v5/logs/gemma-e4-vanilla-test-3x.nohup.log
runs/easy-set-v5/logs/deepseek4-vanilla-test-3x.nohup.log
```

Expected output dirs:

```text
runs/easy-set-v5/stability/gpt-5.4-mini-vanilla-test-3x/
runs/easy-set-v5/stability/gemma-e4-vanilla-test-3x/
runs/easy-set-v5/stability/deepseek4-vanilla-test-3x/
```

### Other running jobs noticed

There are continuation/other GEPA jobs running in the environment. They are not
part of the completed 3× GEPA-best comparison above:

- qwen3-5-9b v5 train is still running.
- GPT-5.4-mini continuation from mc25 is running under:

```text
runs/easy-set-v5/gepa/gpt-5.4-mini-vanilla-gepa-asi-cues-batch-from-mc25-mc50/
```

- Gemma continuation from mc25 is running under:

```text
runs/easy-set-v5/gepa/gemma-e4-mini-vanilla-gepa-asi-cues-batch-from-mc25-mc50/
```

Caveat: the continuation process command observed used `--max-metric-calls 25`
despite the `mc50` name. Treat those as “from mc25 + 25 calls” unless rerun with
`--max-metric-calls 50`.

## How to check running jobs

```bash
ps -fp $(cat runs/easy-set-v5/logs/*vanilla-test-3x.pid)

for f in runs/easy-set-v5/logs/*vanilla-test-3x.nohup.log; do
  echo "### $f"
  tail -40 "$f"
done

find runs/easy-set-v5/stability -maxdepth 2 -type f \
  \( -name 'stability-report.json' -o -name 'score.json' \) | sort
```

## How to aggregate stability result summaries

Use this snippet to summarize all `*test-3x` stability dirs:

```bash
python - <<'PY'
import json, statistics as st
from pathlib import Path

for stab in sorted(Path('runs/easy-set-v5/stability').glob('*test-3x')):
    print('\n##', stab.name)
    reps = sorted(stab.glob('repeat-*/score.json'))
    vals = []
    for p in reps:
        d = json.loads(p.read_text())
        side = d.get('side_info', d)
        scores = side.get('scores', {})
        details = side.get('score_details', {})
        vals.append({
            'score': float(d.get('score', scores.get('gepa_score', 0))),
            'f1': scores.get('topic_micro_f1', details.get('topic_micro_f1')),
            'exact': scores.get('row_exact_accuracy', details.get('row_exact_accuracy')),
            'jaccard': scores.get('avg_row_jaccard', details.get('avg_row_jaccard')),
            'symdiff': details.get('avg_row_symdiff'),
            'fp': details.get('false_positives'),
            'fn': details.get('false_negatives'),
        })
    print('repeats:', len(vals))
    for key in ['score', 'f1', 'exact', 'jaccard', 'symdiff', 'fp', 'fn']:
        xs = [v[key] for v in vals if isinstance(v.get(key), (int, float))]
        if xs:
            print(f'{key}: mean={st.mean(xs):.4f} sd={(st.pstdev(xs) if len(xs) > 1 else 0):.4f}')
    report = stab / 'stability-report.json'
    if report.exists():
        data = json.loads(report.read_text())
        print('prediction_stability:', data.get('prediction_stability'))
        print('bucket_counts:', data.get('bucket_counts'))
PY
```

## Baseline commands that were launched

### GPT-5.4-mini vanilla baseline 3×

```bash
python scripts/openclaw-easy-set-stability.py \
  --input eval/openclaw/easy-set-pilot/easy-set-400-full-120train-70test-test.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v4.md \
  --allowed-topics eval/openclaw/easy-set-pilot/allowed-topics-v4.md \
  --seed-policy eval/openclaw/easy-set-pilot/seed-policy-vanilla-v4.md \
  --model 'codexresponses.gpt-5.4-mini' \
  --runs 3 \
  --parallel 4 \
  --run-name gpt-5.4-mini-vanilla-test-3x \
  --run-root runs/easy-set-v5/stability \
  --wrapped-run-root runs/easy-set-v5/baselines \
  --score-mode row-aware \
  --keep-vanilla-runs
```

### Gemma-e4 vanilla baseline 3×

```bash
python scripts/openclaw-easy-set-stability.py \
  --input eval/openclaw/easy-set-pilot/easy-set-400-full-120train-70test-test.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v4.md \
  --allowed-topics eval/openclaw/easy-set-pilot/allowed-topics-v4.md \
  --seed-policy eval/openclaw/easy-set-pilot/seed-policy-vanilla-v4.md \
  --model 'gemma-e4' \
  --runs 3 \
  --parallel 4 \
  --run-name gemma-e4-vanilla-test-3x \
  --run-root runs/easy-set-v5/stability \
  --wrapped-run-root runs/easy-set-v5/baselines \
  --plain-labels \
  --score-mode row-aware \
  --keep-vanilla-runs
```

### DeepSeek vanilla baseline 3×

```bash
python scripts/openclaw-easy-set-stability.py \
  --input eval/openclaw/easy-set-pilot/easy-set-400-full-120train-70test-test.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v4.md \
  --allowed-topics eval/openclaw/easy-set-pilot/allowed-topics-v4.md \
  --seed-policy eval/openclaw/easy-set-pilot/seed-policy-vanilla-v4.md \
  --model 'deepseek' \
  --runs 3 \
  --parallel 4 \
  --run-name deepseek4-vanilla-test-3x \
  --run-root runs/easy-set-v5/stability \
  --wrapped-run-root runs/easy-set-v5/baselines \
  --score-mode row-aware \
  --keep-vanilla-runs
```

## Reporting plan after baselines finish

Produce two tables.

### 1. Absolute performance table

Rows:

```text
gpt-5.4-mini vanilla
gpt-5.4-mini GEPA-best
gemma-e4 vanilla
gemma-e4 GEPA-best
deepseek vanilla
deepseek GEPA-best
```

Columns:

```text
model
policy
score mean ± sd
F1 mean
row exact mean
Jaccard mean
symdiff mean
FP/FN mean
pairwise prediction Jaccard
pairwise exact rate
stable_correct
stable_wrong
unstable/review
```

### 2. Improvement delta table

Rows:

```text
gpt-5.4-mini
gemma-e4
deepseek
```

Columns:

```text
Δ score
Δ F1
Δ row exact
Δ Jaccard
Δ symdiff
Δ stable_correct
Δ unstable/review
stability change
```

## Recommended next steps

1. Let the vanilla baseline 3× jobs finish.
2. Aggregate baseline vs GEPA-best results.
3. If reporting preliminary results, use 3× means/stddevs.
4. For final/high-confidence results, rerun finalists with 5× or 10×.
5. Consider longer GEPA budgets:
   - GPT-5.4-mini: continue or clean rerun with more budget.
   - Gemma-e4: only if weak-model quality matters; stability is already high.
   - DeepSeek: quality is middling and stability poor in 3×; diagnose before spending much more.
6. Keep clean-start and continued-best runs separate in any report:
   - clean-start = fair benchmark regime;
   - continued-best = best operational policy found so far.

## Quick command: continue GEPA from best policy

This starts a fresh GEPA run from the old best. It is not a true resume.

Example GPT-5.4-mini:

```bash
python scripts/openclaw-vanilla-f1-gepa.py \
  --input eval/openclaw/easy-set-pilot/easy-set-400-full-120train-70test-train.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v4.md \
  --allowed-topics eval/openclaw/easy-set-pilot/allowed-topics-v4.md \
  --seed-policy runs/easy-set-v5/gepa/gpt-5.4-mini-vanilla-gepa-asi-cues-batch-mc25/best-policy.md \
  --static-asi eval/openclaw/easy-set-pilot/vanilla-asi-v4.md \
  --optimizer-cues eval/openclaw/easy-set-pilot/allowed-topics-v4-cues.md \
  --model 'codexresponses.gpt-5.4-mini' \
  --reflection-model 'codexresponses.gpt-5.5?reasoning=high' \
  --run-root runs/easy-set-v5/gepa \
  --run-name gpt-5.4-mini-vanilla-gepa-asi-cues-batch-from-mc25-mc50 \
  --gepa-mode batch \
  --max-metric-calls 50 \
  --score-mode row-aware \
  --parallel 4 \
  --project easy-v5-gepa-test
```

