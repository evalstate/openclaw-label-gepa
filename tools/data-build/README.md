# OpenClaw Data-Build Scripts

These scripts are the repo-owned copy of the construction routines used for the
current label-dataset data line.

They are intentionally kept separate from the stable package code because most
of them are provenance and batch-building utilities rather than reusable library
APIs.

## Scripts

```text
analyze-easy-set-stability.py  stability and teacher agreement analysis
build-consensus.py             consensus/adjudication merge
build-dataset-splits.py        split builder with label-order preservation
build-feedback300.py           feedback300 construction
build-final-splits.py          final Pareto/bench split construction
build-intake.py                intake batch construction
build-slim-tiers.py            slim-check tiering
build-train-ledger.py          train-ledger derivation and quality flags
```

The frozen publication copy of the construction specs and scripts lives under
`datasets/openclaw-label-v7a/artifacts/`.
