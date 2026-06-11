# V4 GEPA mutation surface

## What GEPA mutates

For `scripts/openclaw-vanilla-f1-gepa.py`, GEPA mutates only the candidate variable:

```json
{"policy": "..."}
```

That variable is injected into the AgentCard at:

```md
## Routing policy

{{policy}}
```

So the mutable model-facing text is the routing policy loaded from `--seed-policy`
and evolved by GEPA.

## What is fixed during a GEPA run

These are copied into the run directory and are not mutated by GEPA:

```text
--agent-card      eval/openclaw/easy-set-pilot/openclaw-vanilla-labeler-v4.md
--allowed-topics  eval/openclaw/easy-set-pilot/allowed-topics-v4.md
--input           eval/openclaw/easy-set-pilot/easy-final-v4-train.jsonl
--template        eval/openclaw/task-template.md
--schema          eval/openclaw/output.schema.json
```

The fixed AgentCard includes the allowed-topic file, so the task model sees
`allowed-topics-v4.md` plus the mutable `policy`.

## Static ASI behavior

`--static-asi` is not inserted into the task AgentCard by `openclaw-vanilla-f1-gepa.py`.
It is copied into the run directory and attached to the score/report side info:

```python
report["static_asi_pack"] = args.static_asi.read_text(...)
```

This means the task model under evaluation does not directly see the static ASI during
batch labeling. The reflection/optimization loop may see it as side information when
creating the next candidate policy.

## Recommended v4 run modes

### True vanilla baseline

Mutable seed:

```text
seed-policy-vanilla-v4.md
```

No static ASI.

Purpose: measure the model with concise centrality/co-label guidance only.

### Guided baseline

Mutable seed:

```text
seed-policy-guided-v4.md
```

No static ASI.

Purpose: measure model-facing boundary rules directly.

### GEPA with reflection ASI

Mutable seed should usually start short:

```text
seed-policy-vanilla-v4.md
```

Static ASI may be supplied:

```text
vanilla-asi-v4.md
```

Purpose: let reflection use human/analysis notes while GEPA still mutates only the
routing policy.

## Naming convention

Use names that reveal what the task model saw:

```text
easy-final-v4-test-MODEL-vanilla-v4
easy-final-v4-test-MODEL-guided-v4
easy-final-v4-MODEL-vanilla-gepa-rowaware-mc20
easy-final-v4-MODEL-guided-gepa-rowaware-mc20
easy-final-v4-MODEL-vanilla-gepa-reflection-asi-rowaware-mc20
```

Avoid calling runs `vanilla` when the mutable seed contains boundary ASI.
