# V6 environment — single source of run-stable settings for the v6 databuild
# and GEPA regime. Source from anywhere:
#
#   source eval/openclaw/easy-set-pilot/v6/env.sh
#
# Conventions:
#   tracked   (git): $V6_DIR spec/assets, $V6_INTAKE curated batch records,
#                    $V6_LEDGER, generated train/test sets
#   untracked      : $V6_RUNS_* raw teacher/GEPA outputs, $TRACKIO_DIR
#
# shellcheck shell=bash

V6_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/../../../.." && pwd)"
export V6_ROOT
export V6_DIR="$V6_ROOT/eval/openclaw/easy-set-pilot/v6"

# --- run roots ---------------------------------------------------------------
export V6_RUNS="$V6_ROOT/runs/easy-set-v6h"
export V6_RUNS_INTAKE="$V6_RUNS/v6b-databuild/intake"  # raw batch workdirs (untracked)
export V6_INTAKE="$V6_DIR/intake-v6b"                  # curated batch records (tracked)
export V6_LEDGER="$V6_DIR/v6b-build-ledger.jsonl"      # cumulative accepted rows (tracked)

# --- trackio -----------------------------------------------------------------
# TRACKIO_DIR pins trackio's sqlite/dashboard storage inside the repo without
# redirecting the whole Hugging Face cache. If you prefer everything HF under
# the repo (hub downloads included), set HF_HOME instead and drop TRACKIO_DIR:
#   export HF_HOME="$V6_ROOT/.hf-home"
export TRACKIO_DIR="$V6_ROOT/.trackio"
export V6_TRACKIO_PROJECT="openclaw-v6b-intake"
export V6_TRACKIO_EVERY=5

# --- frozen spec & prompt assets (tracked) ------------------------------------
# v6h standard: v6g (deliverable test + specific-beats-generic + 3-label cap)
# + reliability-mechanism and inference-dispatch tie-breaks
# (see V6_SPEC_CHANGELOG.md; verified on runs/easy-set-v6g/prompt-keyword-audit-40 + runs/easy-set-v6h/tiebreak-probe)
export V6_SPEC="$V6_DIR/topic-boundary-guidance-v6h.md"
export V6_TAXONOMY="$V6_DIR/allowed-topics-v6f.md"
export V6_OVERLAY="$V6_DIR/task-boundary-overlay-v6h.md"
export V6_TEACHER_CARD="$V6_DIR/teacher-card-v6h.md"
export V6_TEACHER_TEMPLATE="$V6_DIR/teacher-template-v6-anchor-free.md"
export V6_TEACHER_SCHEMA="$V6_DIR/teacher-output-v6h.schema.json"
export V6_LABELER_A="$V6_DIR/openclaw-vanilla-labeler-v6h.md"   # fair-context arm
export V6_LABELER_B="$V6_DIR/openclaw-vanilla-labeler-v6h.md"   # compression arm not split
export V6_SEED_OVERLAY="$V6_DIR/seed-policy-overlay-v6h.md"
export V6_SEED_VANILLA="$V6_DIR/seed-policy-vanilla-v6h.md"
export V6_SLIM_ASI="$V6_DIR/vanilla-asi-v6h-slim.md"

# --- source rows -------------------------------------------------------------
export V6_SOURCE_ROWS="$V6_DIR/revalidation-input.jsonl"   # 195 stripped rows
export V6_V5_GOLD="$V6_DIR/v5-gold-reference.jsonl"        # legacy audit labels by id

# --- models ------------------------------------------------------------------
export V6_TEACHER_PRIMARY='codexresponses.gpt-5.5?reasoning=high'
export V6_TEACHER_CROSS='opus'
export V6_REFLECTION_MODEL='codexresponses.gpt-5.5?reasoning=high'

# --- fast-agent binary (dev/0.7.18 editable install in the repo venv) ---------
export FAST_AGENT_BIN="${FAST_AGENT_BIN:-$V6_ROOT/.venv/bin/fast-agent}"

# --- helpers -------------------------------------------------------------------
# Snapshot the curated, decision-bearing files of a raw intake batch into the
# tracked intake dir. Raw teacher repeats (gpt55-3x/, opus-2x/) and the bulky
# input.jsonl stay untracked; input.jsonl is reproducible from
# $V6_SOURCE_ROWS + row-ids.txt.
v6_intake_snapshot() {
  local batch="$1"
  if [ -z "$batch" ] || [ ! -d "$V6_RUNS_INTAKE/$batch" ]; then
    echo "usage: v6_intake_snapshot BATCH_NAME (raw dir must exist under \$V6_RUNS_INTAKE)" >&2
    return 1
  fi
  local dest="$V6_INTAKE/$batch"
  mkdir -p "$dest"
  local f copied=0
  for f in row-ids.txt spec-manifest.json consensus.jsonl consensus-summary.json \
           review-packet.md adjudication.jsonl accepted.jsonl deferred.jsonl \
           prompt-deltas.md; do
    if [ -f "$V6_RUNS_INTAKE/$batch/$f" ]; then
      cp "$V6_RUNS_INTAKE/$batch/$f" "$dest/$f"
      copied=$((copied + 1))
    fi
  done
  echo "v6_intake_snapshot: $batch -> $dest ($copied files)"
}

echo "v6 env: root=$V6_ROOT trackio=$TRACKIO_DIR project=$V6_TRACKIO_PROJECT fast-agent=$FAST_AGENT_BIN"
