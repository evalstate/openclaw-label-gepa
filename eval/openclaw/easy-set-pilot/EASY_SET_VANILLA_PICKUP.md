# Easy set vanilla pickup

This directory is the forward path for the OpenClaw easy-set vanilla pilot. Older
OpenClaw label-generator/benchmark artifacts are legacy unless explicitly pulled
forward.

## Canonical data

Use v2 easy-final files:

```text
eval/openclaw/easy-set-pilot/easy-final-v2.jsonl
eval/openclaw/easy-set-pilot/easy-final-v2-train.jsonl
eval/openclaw/easy-set-pilot/easy-final-v2-test.jsonl
eval/openclaw/easy-set-pilot/easy-final-v2-unused.jsonl
```

Current v2 counts before instability-review edits:

```text
easy-final-v2 rows: 178
train:              80
test:               40
unused:             58
```

## Vanilla prompt/card assets

```text
eval/openclaw/easy-set-pilot/allowed-topics-v2.md
eval/openclaw/easy-set-pilot/allowed-topics-v3.md
eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v2.md
eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-plain-v2.md
eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v3.md
eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-plain-v3.md
eval/openclaw/easy-set-pilot/seed-policy-vanilla-v2.md
eval/openclaw/easy-set-pilot/seed-policy-vanilla-v3.md
eval/openclaw/easy-set-pilot/seed-policy-vanilla-v3-asi.md
eval/openclaw/easy-set-pilot/easy-final-v2-vanilla-asi.md
eval/openclaw/easy-set-pilot/vanilla-asi-v3.md
eval/openclaw/easy-set-pilot/approved-label-guidance-v3.md
eval/openclaw/easy-set-pilot/V3_ASI_RUNSET.md
```

Use `V3_ASI_RUNSET.md` for the next easy-set vanilla baseline/GEPA runs. It uses
the v3 card/topic names plus `seed-policy-vanilla-v3-asi.md`, which folds the
instability-mined ASI into prompt-safe routing guidance while preserving the
vanilla labeler shape.

## Review/instability artifacts

```text
eval/openclaw/easy-set-pilot/easy-final-v2-instability-review-packet.md
runs/openclaw-vanilla-f1-gepa/easy-final-v2-instability-mining.json
runs/openclaw-vanilla-f1-gepa/easy-final-v2-instability-mining.md
```

The review packet is editable. Convert its `Decision` JSON blocks into:

```text
eval/openclaw/easy-set-pilot/easy-final-v2-instability-review-decisions.jsonl
```

Recommended actions from the mining:

- likely demote to medium/ASI unless human review says otherwise:
  - `openclaw-openclaw-83863`
  - `openclaw-openclaw-84753`
- likely keep easy with ASI/guidance updates:
  - `openclaw-openclaw-70002`
  - `openclaw-openclaw-84697`
  - `openclaw-openclaw-70518`
  - `openclaw-openclaw-87277`
  - `openclaw-openclaw-85660`
  - `openclaw-openclaw-74204`
  - `openclaw-openclaw-72085`
  - `openclaw-openclaw-75784`

## Applying approved-label decisions

Treat `easy-final-v2.jsonl` as the approved-label source for the v2 easy path.
Do not edit split files independently.

For each reviewed row:

- `keep_easy` / `keep_easy_with_asi`: keep in `easy-final-v2.jsonl`.
- `fix_labels`: update `expected_topics`, `expected_topics_json`, rationales,
  and provenance metadata in `easy-final-v2.jsonl`.
- `drop_to_medium` / `asi_only`: remove from `easy-final-v2.jsonl` and copy to a
  medium/boundary ASI file such as:

```text
eval/openclaw/easy-set-pilot/medium-asi-easy-final-v2-instability.jsonl
```

Suggested provenance fields for edited rows:

```json
{
  "easy_set_pilot_label_version": "easy-final-v2-instability-reviewed",
  "instability_review_decision": "keep_easy_with_asi",
  "instability_review_notes": "...",
  "pre_instability_review_expected_topics": ["..."]
}
```

## Regenerate splits

The split script now supports output prefixes:

```bash
python scripts/openclaw-easy-set-pilot-split.py \
  --input eval/openclaw/easy-set-pilot/easy-final-v2.jsonl \
  --outdir eval/openclaw/easy-set-pilot \
  --prefix easy-final-v2 \
  --train-size 80 \
  --test-size 40
```

This writes:

```text
easy-final-v2-train.jsonl
easy-final-v2-test.jsonl
easy-final-v2-unused.jsonl
easy-final-v2-summary.json
```

If the generic convenience files are still desired, rerun with `--prefix easy` or
copy after verifying counts/IDs.

## Next run commands

```bash
cd /home/shaun/temp/openclaw-gepa
export PYTHONPATH="src:/home/shaun/temp/gepa/src:${PYTHONPATH:-}"

TRAIN="eval/openclaw/easy-set-pilot/easy-final-v2-train.jsonl"
TEST="eval/openclaw/easy-set-pilot/easy-final-v2-test.jsonl"
CARD="eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v3.md"
PLAIN_CARD="eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-plain-v3.md"
TOPICS="eval/openclaw/easy-set-pilot/allowed-topics-v3.md"
SEED="eval/openclaw/easy-set-pilot/seed-policy-vanilla-v3-asi.md"
STATIC_ASI="eval/openclaw/easy-set-pilot/vanilla-asi-v3.md"
```

Baseline:

```bash
python scripts/openclaw-vanilla-f1-gepa.py \
  --evaluate-only \
  --input "$TEST" \
  --agent-card "$CARD" \
  --allowed-topics "$TOPICS" \
  --seed-policy "$SEED" \
  --static-asi "$STATIC_ASI" \
  --model 'MODEL_ALIAS' \
  --run-name easy-final-v2-test-MODEL-vanilla-v3 \
  --parallel 4 \
  --score-mode row-aware \
  --no-trackio
```

GEPA:

```bash
python scripts/openclaw-vanilla-f1-gepa.py \
  --input "$TRAIN" \
  --agent-card "$CARD" \
  --allowed-topics "$TOPICS" \
  --seed-policy "$SEED" \
  --static-asi "$STATIC_ASI" \
  --model 'MODEL_ALIAS' \
  --reflection-model 'codexresponses.gpt-5.5?reasoning=high' \
  --max-metric-calls 20 \
  --score-mode row-aware \
  --parallel 4 \
  --run-name easy-final-v2-MODEL-structured-gepa-vanilla-v3-rowaware-mc20
```

## Promotion rule

Keep these easy-set-pilot-local changes local until v3 improves held-out stability.
Only then promote rules into global legacy/shared guidance files.
