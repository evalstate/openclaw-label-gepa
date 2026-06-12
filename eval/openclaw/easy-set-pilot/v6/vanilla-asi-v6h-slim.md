# OpenClaw reflection ASI (v6h)

Use this as GEPA/reflection side information. Do not insert it verbatim into the
task AgentCard.

## Optimization target

Optimize exact topic membership for maintainer-interest routing against v6h
gold labels: at most 3 topics per row, priority-ordered, selected by the
deliverable test (label only surfaces whose behavior contract the item
changes). The task model already sees the full fixed taxonomy, the fixed
boundary overlay, and the deliverable test. The mutable candidate is an
OVERLAY on top of those fixed inputs.

Hard constraints on the candidate policy:

- Do NOT restate topic definitions, the allowed-topic enum, cue-word lists,
  the deliverable test, or the cardinality law. The fixed prompt already
  contains them; restating them wastes budget, invites keyword matching, and
  goes stale.
- Add only compact decision rules that change behavior beyond the fixed
  inputs: centrality tests, targeted boundary tie-breakers, suppression rules,
  and corrections for this model's observed failure patterns.
- Keep the section structure of the seed policy (Decision Procedure /
  Cardinality Rules / Boundary Overlays / Suppression Rules) and respect the
  stated bullet budgets.
- Prefer editing or replacing an existing rule over appending a new one.
- Respect the fixed cardinality law: at most 3 topics, priority-ordered.
  Within that cap, inclusion is recall-oriented — include every central
  qualifying topic; do not write rules that trade clearly qualifying co-labels
  away for precision, and do not write rules that pad to 3 when fewer are
  central.
- Expected failure modes under v6h gold labels skew toward OVER-labeling:
  mechanism labels (`config`/`tool_calling` for a parameter that ships another
  surface's feature), producer/symptom labels (`agent_runtime`/`sessions`/
  `gateway` where behavior is owned elsewhere), motivation labels
  (`security`/`reliability` as rationale), and generic-beside-specific
  (`acp` with `acpx`, `coding_agent_integrations` with `codex`). Suppression
  rules targeting these patterns are usually higher-value than new inclusion
  rules.

Detailed per-row failures (false positives, false negatives, and the rows they
occurred on) arrive dynamically in the evaluation side information; write rules
that generalize those failures rather than memorizing rows.
