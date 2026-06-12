# v6f confused-only no-eligibility comparison

Input: `runs/easy-set-v6f/confused-noelig-20/input.jsonl` (20 rows where `group`/`selection_group` is `confused` from the v6b baseline selection).

| variant | accepted | deferred | GPT stable | Opus stable | GPT/Opus exact modal | mean Jaccard | 5-label modal rows |
|---|---:|---:|---:|---:|---:|---:|---:|
| v6d_current_edited_prompt | 2 | 18 | 12 | 18 | 4 | 0.707 | 3 |
| v6e_with_eligibility_overlay | 2 | 18 | 13 | 15 | 5 | 0.732 | 5 |
| v6f_no_eligibility_overlay_confused_only | 1 | 19 | 11 | 16 | 5 | 0.729 | 4 |

## Review reasons

- `v6d_current_edited_prompt`: `{"gpt_flagged_human_review": 2, "gpt_opus_modal_disagreement": 16, "gpt_unstable": 8, "opus_flagged_human_review": 3, "opus_unstable": 2}`
- `v6e_with_eligibility_overlay`: `{"gpt_flagged_human_review": 9, "gpt_opus_modal_disagreement": 15, "gpt_unstable": 7, "opus_flagged_human_review": 6, "opus_unstable": 5}`
- `v6f_no_eligibility_overlay_confused_only`: `{"gpt_flagged_human_review": 2, "gpt_opus_modal_disagreement": 15, "gpt_unstable": 9, "opus_flagged_human_review": 4, "opus_unstable": 4}`

## Status changes versus v6d

### v6e_with_eligibility_overlay
- `openclaw-openclaw-48580` #48580: accepted_consensus `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']` -> deferred `[]`; GPT modal `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']`, Opus modal `['acpx', 'codex', 'reliability', 'sessions']`, reasons `['gpt_flagged_human_review', 'opus_flagged_human_review', 'gpt_opus_modal_disagreement']`
- `openclaw-openclaw-60737` #60737: deferred `[]` -> accepted_consensus `['acp', 'chat_integrations', 'config']`; GPT modal `['acp', 'chat_integrations', 'config']`, Opus modal `['acp', 'chat_integrations', 'config']`, reasons `[]`

### v6f_no_eligibility_overlay_confused_only
- `openclaw-openclaw-48580` #48580: accepted_consensus `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']` -> deferred `[]`; GPT modal `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']`, Opus modal `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']`, reasons `['opus_unstable']`

## Accepted rows by variant

### v6d_current_edited_prompt
- `openclaw-openclaw-54471` #54471: `['acp']` fix(acp): add system_event stream relay to parent session for ACP spawn
- `openclaw-openclaw-48580` #48580: `['acpx', 'codex', 'coding_agent_integrations', 'reliability', 'sessions']` Bug: acpx codex sessions 创建的会话立即退出 - stdin is not a terminal

### v6e_with_eligibility_overlay
- `openclaw-openclaw-54471` #54471: `['acp']` fix(acp): add system_event stream relay to parent session for ACP spawn
- `openclaw-openclaw-60737` #60737: `['acp', 'chat_integrations', 'config']` [Feature]: Per-DM/per-chat default ACP binding for auto-spawning ACP sessions on new topics

### v6f_no_eligibility_overlay_confused_only
- `openclaw-openclaw-54471` #54471: `['acp']` fix(acp): add system_event stream relay to parent session for ACP spawn

