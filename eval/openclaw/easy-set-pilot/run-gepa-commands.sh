#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
export PYTHONPATH="src:/home/shaun/temp/gepa/src:${PYTHONPATH:-}"

TRAIN="eval/openclaw/easy-set-pilot/easy-final-train.jsonl"
TEST="eval/openclaw/easy-set-pilot/easy-final-test.jsonl"
CARD="eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v2.md"
PLAIN_CARD="eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-plain-v2.md"
TOPICS="eval/openclaw/easy-set-pilot/allowed-topics-v2.md"
SEED="eval/openclaw/easy-set-pilot/seed-policy-vanilla-v2.md"

# ---- Baselines on easy-test ----
# GPT-5.5 reference baseline
PYTHONPATH="$PYTHONPATH" python scripts/openclaw-vanilla-f1-gepa.py \
  --evaluate-only --input "$TEST" --agent-card "$CARD" --allowed-topics "$TOPICS" \
  --seed-policy "$SEED" --model 'codexresponses.gpt-5.5?reasoning=medium' \
  --run-name easy-final-test-gpt55-seed-v2 --parallel 4 --no-trackio

# Example smaller-model structured baseline; replace MODEL_ALIAS with your fast-agent alias.
# PYTHONPATH="$PYTHONPATH" python scripts/openclaw-vanilla-f1-gepa.py \
#   --evaluate-only --input "$TEST" --agent-card "$CARD" --allowed-topics "$TOPICS" \
#   --seed-policy "$SEED" --model 'MODEL_ALIAS' \
#   --run-name easy-final-test-MODEL-seed-v2 --parallel 4 --no-trackio

# Example smaller-model plain-label baseline; useful for local/plain models.
# PYTHONPATH="$PYTHONPATH" python scripts/openclaw-vanilla-f1-gepa.py \
#   --evaluate-only --plain-labels --input "$TEST" --agent-card "$PLAIN_CARD" --allowed-topics "$TOPICS" \
#   --seed-policy "$SEED" --model 'MODEL_ALIAS' \
#   --run-name easy-final-test-MODEL-plain-seed-v2 --parallel 4 --no-trackio

# ---- GEPA train on easy-train ----
# A few more iterations than earlier: max_metric_calls 20. Increase to 28 if budget allows.
# DeepSeek/Gemma/local plain example; replace model aliases.
# PYTHONPATH="$PYTHONPATH" python scripts/openclaw-vanilla-f1-gepa.py \
#   --plain-labels --input "$TRAIN" --agent-card "$PLAIN_CARD" --allowed-topics "$TOPICS" \
#   --seed-policy "$SEED" --model 'MODEL_ALIAS' \
#   --reflection-model 'codexresponses.gpt-5.5?reasoning=high' \
#   --max-metric-calls 20 --score-mode row-aware --parallel 4 \
#   --run-name easy-final-MODEL-plain-gepa-v2-rowaware-mc20

# Structured smaller-model example.
# PYTHONPATH="$PYTHONPATH" python scripts/openclaw-vanilla-f1-gepa.py \
#   --input "$TRAIN" --agent-card "$CARD" --allowed-topics "$TOPICS" \
#   --seed-policy "$SEED" --model 'MODEL_ALIAS' \
#   --reflection-model 'codexresponses.gpt-5.5?reasoning=high' \
#   --max-metric-calls 20 --score-mode row-aware --parallel 4 \
#   --run-name easy-final-MODEL-structured-gepa-v2-rowaware-mc20
