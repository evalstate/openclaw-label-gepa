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

## Directory layout

Each intake batch should live under:

```text
runs/easy-set-v6/v6-databuild/intake/BATCH_NAME/
```

Expected files:

```text
row-ids.txt
input.jsonl
v5-gold-reference.jsonl
spec-manifest.json
gpt55-3x/
opus-2x/
consensus.jsonl
review-packet.md
adjudication.jsonl
accepted.jsonl
deferred.jsonl
prompt-deltas.md
```

`row-ids.txt` is the source of truth for the batch. All joins use `id`.

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
FAST_AGENT_BIN="${FAST_AGENT_BIN:-fast-agent}" \
python scripts/openclaw-easy-set-stability.py \
  --direct-batch \
  --input runs/easy-set-v6/v6-databuild/intake/BATCH_NAME/input.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/v6/teacher-card-v6.md \
  --agent-name openclaw_easy_set_pilot_teacher \
  --template eval/openclaw/easy-set-pilot/v6/teacher-template-v6-anchor-free.md \
  --schema eval/openclaw/easy-set-pilot/v6/teacher-output.schema.json \
  --model 'codexresponses.gpt-5.5?reasoning=high' \
  --runs 3 \
  --parallel 4 \
  --run-root runs/easy-set-v6/v6-databuild/intake/BATCH_NAME \
  --run-name gpt55-3x \
  --trackio-project openclaw-v6-intake \
  --trackio-group BATCH_NAME \
  --trackio-every 5 \
  --overwrite
```

If GPT-5.5 self-stability is poor, stop and fix the spec before spending Opus
passes. Then run Opus:

```bash
FAST_AGENT_BIN="${FAST_AGENT_BIN:-fast-agent}" \
python scripts/openclaw-easy-set-stability.py \
  --direct-batch \
  --input runs/easy-set-v6/v6-databuild/intake/BATCH_NAME/input.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/v6/teacher-card-v6.md \
  --agent-name openclaw_easy_set_pilot_teacher \
  --template eval/openclaw/easy-set-pilot/v6/teacher-template-v6-anchor-free.md \
  --schema eval/openclaw/easy-set-pilot/v6/teacher-output.schema.json \
  --model 'opus' \
  --runs 2 \
  --parallel 4 \
  --run-root runs/easy-set-v6/v6-databuild/intake/BATCH_NAME \
  --run-name opus-2x \
  --trackio-project openclaw-v6-intake \
  --trackio-group BATCH_NAME \
  --trackio-every 5 \
  --overwrite
```

The current stability script can execute the teacher repeats, but its
`stable_correct` and score fields are not authoritative for stripped v6 inputs.
Use a dedicated consensus/adjudication builder to compare teacher predictions.

Before the Trackio-enabled `fast-agent batch run` release is installed on PATH,
point the wrapper at a local checkout:

```bash
export FAST_AGENT_BIN=/home/ssmith/source/fast-agent-pr/.venv/bin/fast-agent
```

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

Accepted rows should be appended to a cumulative ledger, for example:

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
