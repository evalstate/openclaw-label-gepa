# easy-final-v4 boundary and test plan

## Goal

Build a stricter easy set by removing high-confusion v3 rows and making the ASI
boundary rules explicit and testable.

## Data changes

Source:

```text
easy-final-v3.jsonl
```

V4 outputs:

```text
easy-final-v4.jsonl                 # 125 easy rows
easy-final-v4-train.jsonl           # 80 rows
easy-final-v4-test.jsonl            # 40 rows
easy-final-v4-unused.jsonl          # 5 held-out rows
easy-final-v4-confusion-bucket.jsonl # 16 demoted rows
```

Demoted rows: worst 10 held-out + worst 6 train rows from
`runs/openclaw-vanilla-f1-gepa/easy-final-v3-row-stability-analysis.*`.

## ASI / label rule changes

See:

```text
seed-policy-vanilla-v4.md       # short true-vanilla seed
seed-policy-guided-v4.md        # compact model-facing boundary seed
allowed-topics-v4.md            # concise model-facing taxonomy
allowed-topics-v4-cues.md       # longer cue/reference artifact, not default prompt
vanilla-asi-v4.md               # human/reflection ASI notes
V4_GEPA_MUTATION_SURFACE.md     # what GEPA can mutate
```

The rule deltas are:

1. cardinality discipline;
2. ACP / ACPX / sessions / agent_runtime / coding_agents / queueing split;
3. model/provider/local/self-hosted split;
4. stricter `reliability` gate;
5. stricter `api_surface` gate;
6. clearer `skills_plugins` positive evidence;
7. ensemble diagnostics for boundary buckets.

## Benchmark commands

Base held-out run:

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

GEPA training run:

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

Guided held-out run (task model sees compact boundary rules):

```bash
python scripts/openclaw-vanilla-f1-gepa.py   --evaluate-only   --input eval/openclaw/easy-set-pilot/easy-final-v4-test.jsonl   --agent-card eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v4.md   --allowed-topics eval/openclaw/easy-set-pilot/allowed-topics-v4.md   --seed-policy eval/openclaw/easy-set-pilot/seed-policy-guided-v4.md   --model 'MODEL_ALIAS'   --run-name easy-final-v4-test-MODEL-guided-v4   --parallel 4   --score-mode row-aware   --no-trackio
```

GEPA with reflection-side ASI (task model starts from short vanilla seed; reflection may see `vanilla-asi-v4.md` in score side-info):

```bash
python scripts/openclaw-vanilla-f1-gepa.py   --input eval/openclaw/easy-set-pilot/easy-final-v4-train.jsonl   --agent-card eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v4.md   --allowed-topics eval/openclaw/easy-set-pilot/allowed-topics-v4.md   --seed-policy eval/openclaw/easy-set-pilot/seed-policy-vanilla-v4.md   --static-asi eval/openclaw/easy-set-pilot/vanilla-asi-v4.md   --model 'MODEL_ALIAS'   --reflection-model 'codexresponses.gpt-5.5?reasoning=high'   --max-metric-calls 20   --score-mode row-aware   --parallel 4   --run-name easy-final-v4-MODEL-vanilla-gepa-reflection-asi-rowaware-mc20
```

Boundary ensemble diagnostic:

```bash
python scripts/openclaw-easy-set-stability.py \
  --input eval/openclaw/easy-set-pilot/easy-final-v4-confusion-bucket.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v4.md \
  --allowed-topics eval/openclaw/easy-set-pilot/allowed-topics-v4.md \
  --seed-policy eval/openclaw/easy-set-pilot/seed-policy-guided-v4.md \
  --model MODEL_ALIAS \
  --runs 3 \
  --parallel 4 \
  --run-name easy-final-v4-confusion-bucket-MODEL-stability \
  --overwrite
```

## Success criteria

Compare to `easy-final-v3-row-stability-analysis.md`:

- held-out never-exact rows decrease;
- held-out avg row Jaccard increases;
- held-out avg symdiff decreases;
- fewer recurring FP/FN in the named boundary families;
- confusion-bucket rows remain outside easy train/test.
