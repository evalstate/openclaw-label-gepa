# V4 label creation and stability workflow

## Goal

For label creation, keep the process separate from vanilla/guided model-under-test
benchmarks. Labels are created/adjudicated by strong teacher models, then checked for
repeat stability and cross-model agreement.

Current teacher assets:

```text
teacher-card-v4.md
teacher-template-v4-clean.md
teacher-output.schema.json
allowed-topics-v4.md
```

## Pass 1: single GPT-5.5 high relabel

Run a single relabel pass against the current v4 easy source:

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

Review `changed-rows.md`. Ideally, changes are limited to rows touched by improved
boundary conditions or rows that should move to a boundary bucket.

## Pass 2: repeated GPT-5.5 high stability

Use direct-batch stability mode for repeated teacher passes:

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

Outputs:

```text
runs/openclaw-easy-set-stability/easy-final-v4-gpt55-teacher-stability/
  stability-report.md
  stability-report.json
  unstable-rows.jsonl
  unstable-row-ids.txt
```

Important: the existing stability scorer expects classifier-style `topics_of_interest`.
Teacher outputs use `labels`, and the runner's `predicted_topics()` already supports
`labels`, so direct teacher stability works.

## Pass 3: Opus cross-check

Run the same one-pass relabel with Opus:

```bash
mkdir -p eval/openclaw/easy-set-pilot/v4-relabel-opus

fast-agent --no-update-check \
  --env .fast-agent \
  batch run \
  --agent-card eval/openclaw/easy-set-pilot/teacher-card-v4.md \
  --agent openclaw_easy_set_pilot_teacher \
  --input eval/openclaw/easy-set-pilot/easy-final-v4.jsonl \
  --output eval/openclaw/easy-set-pilot/v4-relabel-opus/teacher-labels.raw.jsonl \
  --template eval/openclaw/easy-set-pilot/teacher-template-v4-clean.md \
  --json-schema eval/openclaw/easy-set-pilot/teacher-output.schema.json \
  --model 'opus' \
  --id-field id \
  --include-input \
  --parallel 4 \
  --overwrite \
  --no-final-summary

python scripts/openclaw-easy-set-pilot-stratify.py \
  --input eval/openclaw/easy-set-pilot/easy-final-v4.jsonl \
  --outdir eval/openclaw/easy-set-pilot/v4-relabel-opus \
  --raw-output eval/openclaw/easy-set-pilot/v4-relabel-opus/teacher-labels.raw.jsonl

python scripts/openclaw-compare-teacher-labels.py \
  --source eval/openclaw/easy-set-pilot/easy-final-v4.jsonl \
  --teacher eval/openclaw/easy-set-pilot/v4-relabel-opus/teacher-labels.jsonl \
  --outdir eval/openclaw/easy-set-pilot/v4-relabel-opus \
  --name v4-relabel-opus
```

## Pass 4: focus boundary buckets

Run the same teacher relabel on boundary buckets to see whether improved boundary
conditions isolate changes there:

```text
easy-final-v4-confusion-bucket.jsonl
easy-final-v3-opus-disagreements.jsonl
medium-asi-easy-final-v2-instability.jsonl
```

Rows where GPT-5.5 high and Opus agree exactly under v4 guidance may be candidates for
promotion back into easy. Rows with repeated instability remain ASI/medium material.

## Promotion rule

Promote or keep a row in easy only when:

- repeated GPT-5.5 high labels are exact-stable;
- Opus agrees or any disagreement is manually adjudicated;
- teacher bucket is `easy` with high confidence and low ambiguity;
- label changes are consistent with v4 boundary rules;
- the row does not require several boundary exceptions.

Do not automatically replace human/adjudicated labels from a single teacher pass.
Use single-pass differences as review triggers.
