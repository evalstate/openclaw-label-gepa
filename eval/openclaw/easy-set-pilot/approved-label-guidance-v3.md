# Approved-label guidance v3

Use this for easy-set-pilot curation before promoting `easy-final-v2` data to a
true v3 approved-label source.

## Rules

1. Treat `easy-final-v2.jsonl` as the only editable source until a new v3 source
   is created. Never edit split files independently.
2. Exact-match easy rows must be stable and taxonomically clean. If a row needs
   several boundary exceptions to justify the labels, move it to medium/ASI.
3. For every reviewed unstable row, record:
   - `pre_instability_review_expected_topics`
   - final `expected_topics`
   - `instability_review_decision`
   - `instability_review_notes`
   - whether it stays easy, moves to medium, or becomes ASI-only
4. Regenerate train/test/unused splits after source edits.
5. Do not move easy-set-local guidance into global/shared guidance until v3
   improves held-out stability.

## Decision values

- `keep_easy`: labels are clean enough for exact-match easy evaluation.
- `keep_easy_with_asi`: labels are clean, but a generalized boundary rule should
  remain in ASI/prompt guidance.
- `fix_labels`: update labels and provenance in the source.
- `drop_to_medium`: remove from easy exact-match evaluation; keep for boundary
  ASI or medium evaluation.
- `asi_only`: use only as diagnostic/training guidance; do not include in easy.
- `drop`: exclude from pilot.

## Source files

- Current source: `easy-final-v2.jsonl`
- Instability packet: `easy-final-v2-instability-review-packet.md`
- Suggested ledger: `easy-final-v2-instability-review-decisions.jsonl`
- Suggested boundary rows: `medium-asi-easy-final-v2-instability.jsonl`
- Prompt-safe v3 ASI: `seed-policy-vanilla-v3-asi.md`
- Expanded v3 ASI: `vanilla-asi-v3.md`
