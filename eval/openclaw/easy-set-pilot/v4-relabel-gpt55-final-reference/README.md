# v4 GPT-5.5 final-reference labels

This directory is the reference GPT-5.5 high teacher relabel for
`eval/openclaw/easy-set-pilot/easy-final-v4.jsonl`.

Current evidence:

- `post-adjudication-consistency.md`: exact agreement with current adjudicated v4 source.
- `comparison-to-source.json`: `125 / 125` exact-agreement rows, `0` changed rows.
- `teacher-labels.jsonl`: normalized teacher labels.
- `teacher-labels.raw.jsonl`: raw `fast-agent batch run` output.

## Repeat label generation

Run from the repository root. Use a fresh `OUTDIR` for a new repeat so this reference
artifact is not overwritten accidentally.

```bash
OUTDIR=eval/openclaw/easy-set-pilot/v4-relabel-gpt55-repeat-$(date +%Y%m%d-%H%M%S)
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

Expected check:

```bash
cat "$OUTDIR/comparison-to-source.json"
```

The current reference expectation is:

```text
source rows:      125
teacher rows:     125
exact agreement:  125 / 125
changed rows:     0
teacher buckets:  easy: 125
```

If a future repeat produces changed rows, treat them as review triggers, not automatic
source-label replacements.
