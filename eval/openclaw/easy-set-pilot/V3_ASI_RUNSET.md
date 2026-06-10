# Easy-set v3 ASI runset

This is the current easy-set-local v3 guidance set. It intentionally avoids the
old global `asi-pack-v4.md` name.

## Files

```text
eval/openclaw/easy-set-pilot/allowed-topics-v3.md
eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v3.md
eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-plain-v3.md
eval/openclaw/easy-set-pilot/seed-policy-vanilla-v3-asi.md
eval/openclaw/easy-set-pilot/vanilla-asi-v3.md
eval/openclaw/easy-set-pilot/approved-label-guidance-v3.md
```

## Recommended evaluate-only run

```bash
export PYTHONPATH="src:${PYTHONPATH:-}"

python scripts/openclaw-vanilla-f1-gepa.py \
  --evaluate-only \
  --input eval/openclaw/easy-set-pilot/easy-final-v2-test.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v3.md \
  --allowed-topics eval/openclaw/easy-set-pilot/allowed-topics-v3.md \
  --seed-policy eval/openclaw/easy-set-pilot/seed-policy-vanilla-v3-asi.md \
  --static-asi eval/openclaw/easy-set-pilot/vanilla-asi-v3.md \
  --model 'gpt-5.4-mini' \
  --run-name easy-final-v2-test-gpt-5.4-mini-v3-asi \
  --parallel 4 \
  --score-mode row-aware \
  --no-trackio
```

## Recommended GEPA run

```bash
export PYTHONPATH="src:${PYTHONPATH:-}"

python scripts/openclaw-vanilla-f1-gepa.py \
  --input eval/openclaw/easy-set-pilot/easy-final-v2-train.jsonl \
  --agent-card eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v3.md \
  --allowed-topics eval/openclaw/easy-set-pilot/allowed-topics-v3.md \
  --seed-policy eval/openclaw/easy-set-pilot/seed-policy-vanilla-v3-asi.md \
  --static-asi eval/openclaw/easy-set-pilot/vanilla-asi-v3.md \
  --model 'gpt-5.4-mini' \
  --reflection-model 'codexresponses.gpt-5.5?reasoning=high' \
  --max-metric-calls 20 \
  --score-mode row-aware \
  --parallel 4 \
  --run-name easy-final-v2-gpt-5.4-mini-structured-gepa-v3-asi-rowaware-mc20
```

## Naming note

Until instability-review decisions are applied to the approved-label source, the
label data remains `easy-final-v2`; the runset/guidance is v3. Use run names that
say `easy-final-v2-...-v3-asi` for clarity.
