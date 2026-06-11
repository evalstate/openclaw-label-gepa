# V5 GEPA runset

V5 uses the full 120-train / 70-test split. The remaining rows are written as
`unused`; for immediate diagnostics they can serve as a tiny smoke/dev set, but
they are too small for serious model selection.

```text
train: eval/openclaw/easy-set-pilot/easy-set-400-full-120train-70test-train.jsonl
test:  eval/openclaw/easy-set-pilot/easy-set-400-full-120train-70test-test.jsonl
dev:   eval/openclaw/easy-set-pilot/easy-set-400-full-120train-70test-unused.jsonl
```

Current row counts in this checkout:

```text
train 120
test   70
dev     5
```

Batch-mode budget note: `--max-metric-calls 25` is up to about `25 * 120 = 3000`
train row-inferences per GEPA run, before any dev/test repeats.

## Batch-mode GEPA train

Replace `MODEL_ALIAS` and `RUN_MODEL_NAME`.

```bash
python scripts/openclaw-vanilla-f1-gepa.py \
  --input eval/openclaw/easy-set-pilot/easy-set-400-full-120train-70test-train.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v4.md \
  --allowed-topics eval/openclaw/easy-set-pilot/allowed-topics-v4.md \
  --seed-policy eval/openclaw/easy-set-pilot/seed-policy-vanilla-v4.md \
  --static-asi eval/openclaw/easy-set-pilot/vanilla-asi-v4.md \
  --optimizer-cues eval/openclaw/easy-set-pilot/allowed-topics-v4-cues.md \
  --model 'MODEL_ALIAS' \
  --reflection-model 'codexresponses.gpt-5.5?reasoning=high' \
  --run-root runs/easy-set-v5/gepa \
  --run-name RUN_MODEL_NAME-vanilla-gepa-asi-cues-batch-mc25 \
  --gepa-mode batch \
  --max-metric-calls 25 \
  --score-mode row-aware \
  --parallel 4 \
  --project easy-v5-gepa-test
```

For weak/local models, add `--plain-labels`:

```bash
  --plain-labels \
```

## Smoke-evaluate best policy on unused/dev

The 5-row unused split is useful for a quick sanity check, but not enough for
serious model selection. Use repeated test runs for stability reporting only
after policy/scoring/ASI choices are frozen.

```bash
python scripts/openclaw-vanilla-f1-gepa.py \
  --evaluate-only \
  --input eval/openclaw/easy-set-pilot/easy-set-400-full-120train-70test-unused.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v4.md \
  --allowed-topics eval/openclaw/easy-set-pilot/allowed-topics-v4.md \
  --seed-policy runs/easy-set-v5/gepa/RUN_MODEL_NAME-vanilla-gepa-asi-cues-batch-mc25/best-policy.md \
  --model 'MODEL_ALIAS' \
  --run-root runs/easy-set-v5/baselines \
  --run-name RUN_MODEL_NAME-gepa-best-dev \
  --parallel 4 \
  --score-mode row-aware \
  --project easy-v5-gepa-test
```

For smoke stability, run this 3 times with distinct run names, for example:

```text
RUN_MODEL_NAME-gepa-best-dev-r01
RUN_MODEL_NAME-gepa-best-dev-r02
RUN_MODEL_NAME-gepa-best-dev-r03
```

## Final frozen test

Only run this after policy/scoring/ASI choices are frozen.

```bash
python scripts/openclaw-vanilla-f1-gepa.py \
  --evaluate-only \
  --input eval/openclaw/easy-set-pilot/easy-set-400-full-120train-70test-test.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v4.md \
  --allowed-topics eval/openclaw/easy-set-pilot/allowed-topics-v4.md \
  --seed-policy runs/easy-set-v5/gepa/RUN_MODEL_NAME-vanilla-gepa-asi-cues-batch-mc25/best-policy.md \
  --model 'MODEL_ALIAS' \
  --run-root runs/easy-set-v5/baselines \
  --run-name RUN_MODEL_NAME-gepa-best-test \
  --parallel 4 \
  --score-mode row-aware \
  --project easy-v5-gepa-test
```

For small-model stability claims, run the frozen test 5 times and report mean/stddev,
same-set rate, and unstable rows rather than a single best score.
