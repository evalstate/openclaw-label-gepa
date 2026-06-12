# v6g full-40 label-only comparison

Input: same 40 items as the v6d/v6e/v6f prompt-keyword audit
(`runs/easy-set-v6d/prompt-keyword-audit-40/input.jsonl`).

v6g spec changes vs v6f (see `V6_SPEC_CHANGELOG.md`): deliverable test
(global tie-break) + specific-beats-generic rule in
`topic-boundary-guidance-v6g.md`; cardinality cap 5 → 3 priority-ordered in
guidance, card, and schema (`maxItems: 3`).

| variant | accepted | deferred | GPT stable | Opus stable | GPT/Opus exact modal | mean Jaccard | needs-review flags |
|---|---:|---:|---:|---:|---:|---:|---:|
| v6d_current_edited_prompt | 20 | 20 | 32 | 37 | 23 | 0.845 | 5 |
| v6e_with_eligibility_overlay | 18 | 22 | 32 | 34 | 23 | 0.849 | 16 |
| v6f_current_label_only | 22 | 18 | 32 | 34 | 27 | 0.870 | 3 |
| **v6g_deliverable_test_cap3** | **25** | **15** | 31 | 34 | **30** | **0.900** | **0** |

Success criterion from the changelog: exact modal matches 27 → 31+,
deferrals 18 → ~10. Result: 30 exact (just under), 15 deferred. Cross-teacher
agreement improved on every metric; GPT self-stability dipped by one row
(32 → 31), all of it cap-churn (see below).

## Status changes vs v6f

Newly accepted (6): 71487, 43564, 54471, 68204, 84771, 51667 — all were
v6f umbrella-label disputes that the deliverable test resolved
(e.g. 68204 both teachers now say just `telemetry_usage`; 51667 dropped the
commenter-discussion `sessions`).

Newly deferred (3): 47083 (`telemetry_usage` flicker), 51654 and 48851
(cap-churn: 4 central candidates compressed to 3, repeats/teachers pick a
different third label).

## Residual structure (10 modal disagreements)

- 8 single-label superset disputes: `telemetry_usage` (47083), `tool_calling`
  (56442, 10467), `acp` (77694), `config` (84740), `hooks` (44379), `ui_tui`
  (48851), `exec_tools` (82880).
- 2 cross disputes, both cap-compression of former 4-5 label rows: 48406,
  48580.

Deferred rows with identical GPT/Opus modals (train-ready as-is): 82642,
51654, 39248, 40332, 46740.

## Routing implication

Residual disputes are one-marginal-label or cap-churn; none are topic
confusion. Freeze the v6g spec, route superset disputes through the
deterministic intersection rule, and send cap-churn rows to the train/fuzzy
pool. Do not iterate the prompt further on this audit set.
