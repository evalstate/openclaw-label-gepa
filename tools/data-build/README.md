# OpenClaw Data-Build Scripts

These scripts are the repo-owned copy of the construction routines used for the
v6h/v6o/v7a data line.

They are intentionally kept separate from the stable package code because most
of them are provenance and batch-building utilities rather than reusable library
APIs.

## Scripts

```text
openclaw-v6-intake.py             intake batch construction
openclaw-easy-set-stability.py    stability and teacher agreement analysis
openclaw-v6-consensus.py          consensus/adjudication merge
openclaw-v6b-train-ledger.py      train-ledger derivation and quality flags
openclaw-build-splits.py          split builder with label-order preservation
openclaw-v6-slim-tiers.py         slim-check tiering
openclaw-v6k-final-splits.py      final Pareto/bench split construction
openclaw-v6n-feedback300.py       feedback300 construction
openclaw-v6o-feedback300.py       v6o/v7a feedback300 construction
```

The frozen publication copy of the construction specs and scripts lives under
`datasets/openclaw-label-v7a/artifacts/`.
