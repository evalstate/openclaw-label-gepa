# V6 intake ladder

Purpose: build v6 labels incrementally in small, validated batches so teacher
model failures and spec problems are found before they contaminate the full set.

V6 is a new label build. V5 labels are legacy audit context only; they are not
gold for v6.

## Principles

- Process rows in batches of about 30 stable row ids.
- Prompt teacher models with stripped row context only: no previous labels.
- Compare teacher runs to each other first, then compare to v5 by id for audit.
- Patch the v6 spec or task overlay when a batch exposes systematic confusion.
- Rerun the same batch after prompt/spec changes before accepting rows.
- Accept rows into the cumulative build ledger only when the current spec version
  produced stable labels or a human adjudication explicitly resolved the row.

## Environment

All run-stable settings (paths, trackio project/dir, models, fast-agent binary)
live in one sourceable script:

```bash
source eval/openclaw/easy-set-pilot/v6/env.sh
```

This sets `TRACKIO_DIR` to the repo-local `.trackio/` (untracked), defaults
`FAST_AGENT_BIN` to the repo venv's dev/0.7.18 install, and exports the `V6_*`
variables used by the commands below.

## Directory layout

Each intake batch has a raw working dir (untracked) and a curated record dir
(tracked):

```text
$V6_RUNS_INTAKE/BATCH_NAME/    runs/easy-set-v6/v6-databuild/intake/ — raw
$V6_INTAKE/BATCH_NAME/         eval/openclaw/easy-set-pilot/v6/intake/ — tracked
```

Raw working dir files:

```text
row-ids.txt
input.jsonl
v5-gold-reference.jsonl
spec-manifest.json
gpt55-3x/
opus-2x/
consensus.jsonl
consensus-summary.json
review-packet.md
adjudication.jsonl
accepted.jsonl
deferred.jsonl
prompt-deltas.md
```

`row-ids.txt` is the source of truth for the batch. All joins use `id`.

After the consensus pass and any adjudication, snapshot the decision-bearing
files into the tracked dir and commit:

```bash
v6_intake_snapshot BATCH_NAME    # helper from env.sh
git add "$V6_INTAKE/BATCH_NAME" "$V6_LEDGER"
```

Raw teacher repeats and `input.jsonl` stay untracked; `input.jsonl` is
reproducible from `$V6_SOURCE_ROWS` + `row-ids.txt`.

## Batch creation

Choose rows deliberately. Early batches should include:

- known disagreement rows;
- ordinary rows that should be easy under v6;
- rows touching changed taxonomy boundaries, especially the inference family;
- rows likely to trigger cardinality pressure.

Create the stripped input by selecting from:

```text
eval/openclaw/easy-set-pilot/v6/revalidation-input.jsonl
```

Join legacy labels by id from:

```text
eval/openclaw/easy-set-pilot/v6/v5-gold-reference.jsonl
```

The legacy labels are for review and diff reporting only. They must not be
injected into teacher prompts.

Use the intake script to create batch directories reproducibly:

```bash
python scripts/openclaw-v6-intake.py \
  --batch BATCH_NAME \
  --include-blind-agree-20 \
  --control-from-all-equal 10
```

## Teacher runs

Run GPT-5.5 first:

```bash
python scripts/openclaw-easy-set-stability.py \
  --direct-batch \
  --input "$V6_RUNS_INTAKE/BATCH_NAME/input.jsonl" \
  --agent-card "$V6_TEACHER_CARD" \
  --agent-name openclaw_easy_set_pilot_teacher \
  --template "$V6_TEACHER_TEMPLATE" \
  --schema "$V6_TEACHER_SCHEMA" \
  --model "$V6_TEACHER_PRIMARY" \
  --runs 3 \
  --parallel 4 \
  --repeat-parallel 3 \
  --run-root "$V6_RUNS_INTAKE/BATCH_NAME" \
  --run-name gpt55-3x \
  --trackio-project "$V6_TRACKIO_PROJECT" \
  --trackio-group BATCH_NAME \
  --trackio-every "$V6_TRACKIO_EVERY" \
  --overwrite
```

If GPT-5.5 self-stability is poor, stop and fix the spec before spending Opus
passes. Then run Opus:

```bash
python scripts/openclaw-easy-set-stability.py \
  --direct-batch \
  --input "$V6_RUNS_INTAKE/BATCH_NAME/input.jsonl" \
  --agent-card "$V6_TEACHER_CARD" \
  --agent-name openclaw_easy_set_pilot_teacher \
  --template "$V6_TEACHER_TEMPLATE" \
  --schema "$V6_TEACHER_SCHEMA" \
  --model "$V6_TEACHER_CROSS" \
  --runs 2 \
  --parallel 4 \
  --repeat-parallel 2 \
  --run-root "$V6_RUNS_INTAKE/BATCH_NAME" \
  --run-name opus-2x \
  --trackio-project "$V6_TRACKIO_PROJECT" \
  --trackio-group BATCH_NAME \
  --trackio-every "$V6_TRACKIO_EVERY" \
  --overwrite
```

The current stability script can execute the teacher repeats, but its
`stable_correct` and score fields are not authoritative for stripped v6 inputs.
Use a dedicated consensus/adjudication builder to compare teacher predictions.

`--repeat-parallel` parallelizes independent repeats. Total request concurrency
is approximately `--repeat-parallel * --parallel`, so reduce one of them if the
provider or local environment starts throttling.

`env.sh` already points `FAST_AGENT_BIN` at the repo venv, which carries the
Trackio-enabled dev/0.7.18 editable install; override the variable only to test
a different checkout.

## Consensus pass

After GPT and Opus repeats finish, build the batch review artifacts:

```bash
python scripts/openclaw-v6-consensus.py \
  --batch-dir "$V6_RUNS_INTAKE/BATCH_NAME" \
  --overwrite
```

This writes:

```text
consensus.jsonl
consensus-summary.json
review-packet.md
adjudication.jsonl
accepted.jsonl
deferred.jsonl
```

`accepted.jsonl` contains only strict teacher consensus rows. `deferred.jsonl`
and `adjudication.jsonl` are the working queue for human review or prompt/spec
tuning.

## Consensus buckets

For each row, compute:

- GPT exact-set stability across 3 repeats;
- Opus exact-set stability across 2 repeats;
- GPT modal label set;
- Opus modal label set;
- GPT/Opus exact agreement;
- label count;
- bucket/confidence agreement;
- possible-confusion labels;
- v5 diff through the v6 crosswalk.

Recommended row statuses:

```text
accepted_consensus
accepted_human
needs_prompt_change
deferred
demoted
```

Recommended decision dispositions:

```text
confirm_consensus
replace_with_adjudicated
demote_from_easy
defer_to_later_batch
requires_spec_change
```

## Acceptance gate

Accept a row only when one of these is true:

- GPT is exact-stable, Opus agrees, and the row satisfies v6 cardinality and
  rationale requirements;
- a human adjudication explicitly sets the v6 labels and records the reason.

Do not accept rows merely because they match v5. Do not accept rows merely
because one teacher is confident.

Rows with unstable teacher outputs, more than 5 labels, low confidence,
medium/high ambiguity, or repeated omitted-MUST-rule concerns should go to
review or prompt tuning.

## Prompt/spec tuning loop

After each batch:

1. Identify recurring confusion pairs and omitted/extra labels.
2. Decide whether each issue is a row-specific adjudication or a spec problem.
3. Patch only the relevant v6 spec files:
   - `topic-boundary-guidance-v6.md`
   - `task-boundary-overlay-v6.md`
   - `teacher-card-v6.md` only when the teacher procedure itself is wrong
   - `teacher-output.schema.json` only for validation constraints
4. Record the change in `V6_SPEC_CHANGELOG.md`.
5. Rerun the same batch against the new spec.

Only move to the next batch when the current batch has no unresolved systematic
prompt/spec failures.

## Cumulative ledger

Accepted rows are appended to the tracked cumulative ledger (`$V6_LEDGER`):

```text
eval/openclaw/easy-set-pilot/v6/v6-build-ledger.jsonl
```

Each record should include:

```json
{
  "id": "openclaw-openclaw-10467",
  "batch": "batch-001",
  "status": "accepted_consensus",
  "labels": ["coding_agents", "sessions", "queueing", "config"],
  "source": "teacher_consensus",
  "spec_manifest": "runs/easy-set-v6/v6-databuild/intake/batch-001/spec-manifest.json",
  "legacy_v5_labels": ["coding_agents", "sessions", "queueing", "config"],
  "decision_note": "Stable under v6 teacher consensus."
}
```

The final v6 train/test files should be generated from this ledger, not from raw
teacher outputs.
