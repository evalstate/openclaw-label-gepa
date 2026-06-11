# easy-set-400 build notes

Goal: expand v4 with a stricter 3-teacher consensus over a new ds4 sample while
keeping non-easy/confounded rows available for analysis.

Source:

```text
refdata/ds4.jsonl
```

Current v4 rows are preserved and excluded from the new sample:

```text
eval/openclaw/easy-set-pilot/easy-final-v4.jsonl
eval/openclaw/easy-set-pilot/easy-final-v4-confusion-bucket.jsonl
```

## 1. Prepare the 200-row candidate sample

```bash
python scripts/openclaw-easy-set-400.py prepare-sample
```

Outputs:

```text
eval/openclaw/easy-set-pilot/easy-set-400-candidates-200.jsonl
eval/openclaw/easy-set-pilot/easy-set-400-candidates-200.manifest.json
```

Legacy `topics_of_interest` labels from ds4 are copied into
`legacy_expected_topics`, `ds4_topics`, and the template's comparison-only
`expected_topics_json`. They are not final labels.

## 2. Run three teacher passes

The intended consensus is:

- `gpt55-r1`: `codexresponses.gpt-5.5?reasoning=high`
- `gpt55-r2`: `codexresponses.gpt-5.5?reasoning=high`
- `opus`: project `opus` alias

```bash
OUTDIR=runs/easy-set-400/label-generation/consensus-$(date +%Y%m%d-%H%M%S)
mkdir -p "$OUTDIR"

for NAME in gpt55-r1 gpt55-r2; do
  fast-agent --no-update-check \
    --env .fast-agent \
    batch run \
    --agent-card eval/openclaw/easy-set-pilot/teacher-card-v4.md \
    --agent openclaw_easy_set_pilot_teacher \
    --input eval/openclaw/easy-set-pilot/easy-set-400-candidates-200.jsonl \
    --output "$OUTDIR/$NAME.raw.jsonl" \
    --template eval/openclaw/easy-set-pilot/teacher-template-easy-set-400-clean.md \
    --json-schema eval/openclaw/easy-set-pilot/teacher-output.schema.json \
    --model 'codexresponses.gpt-5.5?reasoning=high' \
    --id-field id \
    --include-input \
    --parallel 4 \
    --overwrite \
    --no-final-summary
done

fast-agent --no-update-check \
  --env .fast-agent \
  batch run \
  --agent-card eval/openclaw/easy-set-pilot/teacher-card-v4.md \
  --agent openclaw_easy_set_pilot_teacher \
  --input eval/openclaw/easy-set-pilot/easy-set-400-candidates-200.jsonl \
  --output "$OUTDIR/opus.raw.jsonl" \
  --template eval/openclaw/easy-set-pilot/teacher-template-easy-set-400-clean.md \
  --json-schema eval/openclaw/easy-set-pilot/teacher-output.schema.json \
  --model 'opus' \
  --id-field id \
  --include-input \
  --parallel 4 \
  --overwrite \
  --no-final-summary
```

## 3. Build consensus buckets

```bash
python scripts/openclaw-consensus-teacher-buckets.py \
  --input eval/openclaw/easy-set-pilot/easy-set-400-candidates-200.jsonl \
  --teacher gpt55-r1="$OUTDIR/gpt55-r1.raw.jsonl" \
  --teacher gpt55-r2="$OUTDIR/gpt55-r2.raw.jsonl" \
  --teacher opus="$OUTDIR/opus.raw.jsonl" \
  --outdir "$OUTDIR/consensus" \
  --target-easy 200
```

For `len(teachers) == 3`, the consensus script requires all three teachers to
be strict-easy and to return the exact same label set for `easy-consensus.jsonl`.

## 4. Finalize easy-set-400 and splits

```bash
python scripts/openclaw-easy-set-400.py finalize \
  --consensus-dir "$OUTDIR/consensus"
```

Outputs:

```text
eval/openclaw/easy-set-pilot/easy-set-400.jsonl
eval/openclaw/easy-set-pilot/easy-set-400-train.jsonl
eval/openclaw/easy-set-pilot/easy-set-400-validate.jsonl
eval/openclaw/easy-set-pilot/easy-set-400-test.jsonl
eval/openclaw/easy-set-pilot/easy-set-400-new-easy.jsonl
eval/openclaw/easy-set-pilot/easy-set-400-consensus-medium.jsonl
eval/openclaw/easy-set-pilot/easy-set-400-review-needed.jsonl
eval/openclaw/easy-set-pilot/easy-set-400-invalid.jsonl
eval/openclaw/easy-set-pilot/easy-set-400-confusion-bucket.jsonl
eval/openclaw/easy-set-pilot/easy-set-400-summary.json
```

The final split is deterministic and stratifies across final topics, item type,
v4-vs-new source, and inferred confusion families. Defaults are 70/15/15
train/validate/test.

The confusion bucket intentionally keeps:

- v4 demoted confusion rows;
- new medium-stable consensus rows;
- new review-needed rows;
- invalid/missing teacher rows.
