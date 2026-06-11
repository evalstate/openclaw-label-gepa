# V4 prompt/guidance review

Purpose: assess whether allowed-topic definitions, seed policy, and ASI are overlapping/confusing the model, and summarize what GEPA runs suggest works.

## Executive summary

- The current `allowed-topics-v4.md` is already a full taxonomy plus cue-word guide. It is not just an enum.
- The current `seed-policy-vanilla-v4-asi.md` repeats and overrides many allowed-topic boundaries. This is too heavy for a vanilla run and creates instruction competition.
- The first v4 smoke test showed exactly that failure mode: nearly no false positives, but severe under-labeling. The prompt over-emphasized gates/conservatism relative to central co-label retention.
- `vanilla-asi-v4.md` is mostly a human/evaluator plan, not prompt-safe task guidance. It should not be passed as `--static-asi` to the task model unless the runner only uses it for reflection/side-info. In this runner it is copied into the score report/side info, not the task AgentCard, but names make this easy to misunderstand.
- High-capability adjudicators (GPT-5.5 high / Opus) agree on labels because they can absorb the full taxonomy. Smaller models are more sensitive to duplicated/negative instructions and tend to collapse labels.

## Recommended artifact split

Use four separate layers:

1. `allowed-topics-v4.md` — concise topic definitions only. No version history, no long cue lists that collide, no dataset curation commentary.
2. `seed-policy-vanilla-v4.md` — very short vanilla policy. No topic-specific rules except central-vs-incidental and co-label retention.
3. `seed-policy-guided-v4.md` or `seed-policy-boundary-v4.md` — compact model-facing boundary rules for known confusing families. No “v3/v4 changes” wording.
4. `vanilla-asi-v4.md` / `V4_BOUNDARY_AND_TEST_PLAN.md` — human/evaluator/GEPA reflection material, not direct task prompt text.

## Overlap and conflict findings

### Allowed topics vs seed policy

- `allowed-topics-v4.md`: 11722 chars.
- `seed-policy-vanilla-v4-asi.md`: 7242 chars.
- `vanilla-asi-v4.md`: 3729 chars.

The allowed-topics file already defines every topic, cue words, and some negative gates. The seed then repeats topic-specific gates for ACP, model providers, reliability, API surface, plugins, auth/security/approvals/exec, docs/tests/config/UI/chat/notifications. This causes two problems:

- **Instruction dilution:** the actual classification objective is buried under many boundary rules.
- **Over-conservatism:** repeated “only when” / “do not add” rules push smaller models to under-label, especially for multi-label rows.

### Cue-word/topic collisions in allowed-topics-v4

Some cue words appear under multiple topics, which is expected but risky if models treat cue words as triggers. Notable collisions:
- `agent run` → `coding_agents`, `agent_runtime`
- `api key` → `security`, `auth_identity`
- `auth` → `security`, `auth_identity`
- `chat completions` → `model_serving`, `api_surface`
- `codex` → `coding_agents`, `codex`
- `credential` → `security`, `auth_identity`
- `durable exec` → `coding_agents`, `exec_tools`
- `embeddings` → `self_hosted_inference`, `memory`
- `exec approval` → `coding_agents`, `approvals`
- `gguf` → `local_models`, `open_weight_models`
- `heartbeat` → `agent_runtime`, `cron_automation`
- `lancedb` → `self_hosted_inference`, `memory`
- `model card` → `open_weight_models`, `hub_workflows`
- `oauth` → `security`, `auth_identity`
- `sandbox` → `coding_agents`, `sandboxing`
- `session list` → `sessions`, `ui_tui`
- `ssrf` → `self_hosted_inference`, `security`
- `tool call` → `exec_tools`, `tool_calling`
- `tool_choice` → `exec_tools`, `tool_calling`
- `tools/invoke` → `exec_tools`, `api_surface`

### Seed topic mentions

Topics most repeated in the seed policy:
- `config` × 7
- `sessions` × 4
- `acp` × 3
- `security` × 3
- `docs` × 3
- `queueing` × 3
- `acpx` × 2
- `coding_agents` × 2
- `agent_runtime` × 2
- `approvals` × 2
- `tests_ci` × 2
- `api_surface` × 2
- `notifications` × 2
- `reliability` × 2
- `local_models` × 1
- `local_model_providers` × 1
- `model_serving` × 1
- `self_hosted_inference` × 1
- `open_weight_models` × 1
- `gateway` × 1

This repetition is useful for a guided boundary policy, but it is not vanilla.

## What the training runs suggest works

Parsed 73 train candidate score files; 73 non-degenerate/usable by avg row Jaccard >= 0.10.

### Best policies by GEPA score

- `easy-final-v3-sonnet-vanilla-gepa-rowaware-mc20/candidate-0007` — gepa=0.838, f1=0.921, exact=0.575, j=0.875, sym=0.54, chars=13499
- `easy-final-v3-sonnet-vanilla-gepa-rowaware-mc20/candidate-0010` — gepa=0.832, f1=0.914, exact=0.575, j=0.865, sym=0.57, chars=13114
- `easy-final-v3-sonnet-vanilla-gepa-rowaware-mc20/candidate-0005` — gepa=0.829, f1=0.913, exact=0.575, j=0.859, sym=0.57, chars=11769
- `easy-final-v3-sonnet-vanilla-gepa-rowaware-mc20/candidate-0009` — gepa=0.827, f1=0.914, exact=0.550, j=0.867, sym=0.59, chars=14217
- `easy-final-v3-sonnet-vanilla-gepa-rowaware-mc20/candidate-0008` — gepa=0.825, f1=0.912, exact=0.562, j=0.857, sym=0.59, chars=12671
- `easy-final-v3-sonnet-vanilla-gepa-rowaware-mc20/candidate-0004` — gepa=0.825, f1=0.908, exact=0.575, j=0.853, sym=0.60, chars=10009
- `easy-final-v3-sonnet-vanilla-gepa-rowaware-mc20/candidate-0014` — gepa=0.823, f1=0.915, exact=0.537, j=0.862, sym=0.57, chars=13191
- `easy-final-v3-sonnet-vanilla-gepa-rowaware-mc20/candidate-0015` — gepa=0.822, f1=0.912, exact=0.537, j=0.860, sym=0.60, chars=15441

### Worst non-degenerate policies by GEPA score

- `easy-final-v3-qwen-3-5-9b-vanilla-gepa-rowaware-mc20/candidate-0001` — gepa=0.489, f1=0.633, exact=0.113, j=0.499, sym=2.16, chars=5436
- `easy-final-v3-deepseek4-mini-vanilla-gepa-rowaware-mc20/candidate-0009` — gepa=0.527, f1=0.656, exact=0.275, j=0.482, sym=1.85, chars=12999
- `easy-final-v3-kimi26-vanilla-gepa-rowaware-mc20/candidate-0001` — gepa=0.538, f1=0.693, exact=0.163, j=0.528, sym=1.64, chars=5436
- `easy-final-v3-qwen-3-5-9b-vanilla-gepa-rowaware-mc20/candidate-0002` — gepa=0.549, f1=0.694, exact=0.150, j=0.574, sym=1.88, chars=7908
- `easy-final-v3-gemma-e4-vanilla-gepa-rowaware-mc20/candidate-0001` — gepa=0.609, f1=0.755, exact=0.200, j=0.637, sym=1.52, chars=5436
- `easy-final-v3-minimax27-mini-vanilla-gepa-rowaware-mc20/candidate-0001` — gepa=0.639, f1=0.784, exact=0.225, j=0.675, sym=1.31, chars=5436
- `easy-final-v3-deepseek4-mini-vanilla-gepa-rowaware-mc20/candidate-0001` — gepa=0.655, f1=0.784, exact=0.287, j=0.684, sym=1.34, chars=5436
- `easy-final-v3-minimax27-mini-vanilla-gepa-rowaware-mc20/candidate-0003` — gepa=0.661, f1=0.792, exact=0.275, j=0.701, sym=1.39, chars=11347

### Policy-feature correlations (rough, observational)

| feature | n with | avg gepa with | avg gepa without | avg exact with | avg exact without | avg chars with | avg chars without |
|---|---:|---:|---:|---:|---:|---:|---:|
| mentions co-label/cardinality | 47 | 0.721 | 0.730 | 0.368 | 0.389 | 13373.404 | 11300.962 |
| topic-by-topic table | 73 | 0.724 |  | 0.376 |  | 12635.274 |  |
| negative gates | 73 | 0.724 |  | 0.376 |  | 12635.274 |  |
| few-shot/examples/row-ish | 73 | 0.724 |  | 0.376 |  | 12635.274 |  |
| format/output instructions | 53 | 0.746 | 0.665 | 0.413 | 0.276 | 13125.113 | 11337.200 |
| model/provider boundary | 73 | 0.724 |  | 0.376 |  | 12635.274 |  |
| acp/session boundary | 73 | 0.724 |  | 0.376 |  | 12635.274 |  |
| reliability gate | 73 | 0.724 |  | 0.376 |  | 12635.274 |  |
| api_surface gate | 59 | 0.720 | 0.740 | 0.372 | 0.390 | 12125.085 | 14785.357 |
| skills_plugins gate | 73 | 0.724 |  | 0.376 |  | 12635.274 |  |

Interpretation: these are not causal, because GEPA candidates co-vary by model and iteration. Still, the strong policies tend to have targeted boundary rules and cardinality/co-label instructions. Degenerate policies often either return empty/under-label or become long topic tables that copy the taxonomy.

## Concrete lessons from successful vs failed runs

### What generally works

- A short global objective: central maintainer-routing labels only.
- Explicit co-label retention: do not collapse independent central interests.
- Targeted negative gates for the few families that repeatedly confuse models: ACP/session/runtime/coding_agents, provider/local/model_serving, reliability, api_surface, skills_plugins.
- Keeping topic-specific rules compact and asymmetric: only clarify boundaries that are actually confused.
- Row-aware score helped expose under-labeling; pure F1 alone can hide row-level exact-match problems.

### What generally does not work

- Putting a second full taxonomy in the seed policy on top of `allowed-topics`.
- Too many “do not add”/“only when” gates without equally explicit “include all central co-labels”. The v4 smoke test produced 1 FP but 61 FN.
- Cue-word-heavy topic definitions. They help recall but create collisions (`auth`, `gateway`, `session`, `provider`, `tool`, etc.).
- Passing human curation/version rationale to the task model. “v3/v4 changes”, demotion policy, and ensemble strategy should be human/evaluator material.
- Using boundary-bucket rows as easy exact-match rows. Opus/GPT-5.5 can adjudicate them, but small models use them as conflicting examples.

## Proposed clean model-facing guidance

### Vanilla seed policy

```md
Classify the GitHub issue or pull request for OpenClaw maintainer-interest routing.

Use only the supplied GitHub context. Prefer the title and main problem or feature statement. Use body, comments, labels, changed files, and diff as supporting evidence.

Select every allowed topic that is central to routing the item to the right maintainer interest. Do not select topics that are only incidental implementation details, examples, tests, file paths, or possible consequences.

Use the smallest label set that captures the central routing interests. Do not collapse away explicit central co-labels when the row clearly has multiple independent maintainer interests.

Return an empty list only if no allowed topic centrally applies.
```

### Guided boundary addendum

Keep this under ~1200-1800 words, only operational rules, no version history. Include:

- central co-label retention;
- ACP/session/runtime/coding_agents/queueing split;
- provider/local/model_serving/self_hosted split;
- reliability central-failure gate;
- api_surface public-contract gate;
- skills_plugins product-surface gate.

## Recommended immediate changes

1. Create `seed-policy-vanilla-v4.md` as the short seed above.
2. Rename current `seed-policy-vanilla-v4-asi.md` to a guided/boundary seed, or rewrite it without `v4` historical language.
3. Stop passing `vanilla-asi-v4.md` as if it were task prompt guidance unless intentionally doing guided/ASI experiments. Keep it for reflection/evaluation docs.
4. Trim `allowed-topics-v4.md` cue words or split it into:
   - `allowed-topics-v4.md` = enum + concise definitions;
   - `allowed-topics-v4-cues.md` = optional human/teacher cue list.
5. Re-run the v4 smoke test with:
   - vanilla seed only;
   - guided seed only;
   - guided seed plus static ASI only if the runner confirms it is not inserted into the task prompt.
6. Compare false positives/false negatives. The target is not zero FP; it is balanced row-level reproduction.

## Suggested experiment matrix

| run | allowed topics | seed | static ASI | purpose |
|---|---|---|---|---|
| vanilla | concise v4 | short vanilla | none | true baseline |
| guided | concise v4 | compact boundary seed | none | test model-facing rules |
| reflection-ASI | concise v4 | short vanilla | vanilla-asi-v4 | GEPA/reflection side info only |
| boundary ensemble | concise v4 | compact boundary seed | none | diagnose demoted rows |

Do not compare “vanilla” and “ASI” runs under the same name.
## Restructuring status

Implemented after this review:

- `allowed-topics-v4.md` is now concise model-facing taxonomy.
- `allowed-topics-v4-cues.md` preserves the previous long cue-word artifact for human/teacher reference.
- `seed-policy-vanilla-v4.md` is the short true-vanilla seed.
- `seed-policy-guided-v4.md` is the compact model-facing boundary seed.
- `seed-policy-vanilla-v4-asi.md` is retained only as a compatibility alias of the guided seed; prefer the clearer name for new runs.
- `V4_GEPA_MUTATION_SURFACE.md` documents what GEPA mutates and what is fixed.
