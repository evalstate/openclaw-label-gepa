# easy-final-v2 instability review packet

Purpose: review rows that remained unstable after row-aware GEPA and repeated best-policy test runs. Edit the `Decision` block for each row.

Suggested decision values:

- `keep_easy`: labels are clean enough for easy set
- `keep_easy_with_asi`: keep approved labels, but add explicit ASI/guidance
- `fix_labels`: replace labels in `final_labels`
- `drop_to_medium`: remove from easy exact-match eval; keep as boundary/ASI material
- `asi_only`: training/diagnostic row only; do not put in easy approved-label set
- `drop`: exclude from pilot
- `TODO`: needs human review

## Workflow guidance from prior handovers

Prior handovers established a stability-first loop: exact-stable teacher rows are good candidates for approved labels, while unstable rows should become manual-adjudication or ASI material. The easy-set handover also says medium/hard/boundary rows should be preserved as ASI rather than mixed into the first easy train/test set. Use this packet accordingly:

1. For rows marked `keep_easy_with_asi`, keep `expected_topics` in the approved-label/easy set only after human confirmation, and add the listed FP/FN pattern as concrete ASI examples.
2. For rows marked `fix_labels`, update the approved label artifact/split source first, then regenerate train/test/unused splits so benchmark labels and review decisions stay in sync.
3. For rows marked `drop_to_medium` or `asi_only`, remove them from easy exact-match evaluation and add them to medium/boundary ASI material; do not let GEPA memorize issue IDs/titles.
4. Use repeated-run instability as a review trigger, not as automatic relabeling. A stable wrong prediction can reveal unclear guidance; an unstable prediction can reveal taxonomy overlap.
5. After approved-label/ASI edits, rerun the v2 teacher relabel/stability check on changed rows before updating convenience files.

### Concrete application path

Use this packet as a bridge between the easy-set benchmark handover and the
label-generator/stability handovers:

1. **Approved-label changes**
   - Treat `easy-final-v2.jsonl` as the current approved-label source for the
     v2 pilot, but do not edit split files independently.
   - For each reviewed block below:
     - `keep_easy` / `keep_easy_with_asi`: keep the row in the easy source.
     - `fix_labels`: update that row's `expected_topics`,
       `expected_topics_json`, label rationales if needed, and record the review
       decision.
     - `drop_to_medium` / `asi_only`: remove it from easy source and move/copy
       it into medium/boundary ASI material.
   - Then regenerate deterministic split files using the same split script shape
     as the handover:

```bash
python scripts/openclaw-easy-set-pilot-split.py \
  --input eval/openclaw/easy-set-pilot/easy-final-v2.jsonl \
  --outdir eval/openclaw/easy-set-pilot \
  --train-size 80 \
  --test-size 40
```

   - If preserving the `easy-final-v2-*` filenames is required, write/regenerate
     those explicitly or copy the refreshed convenience files after verifying
     counts and IDs.

2. **Manual decision ledger**
   - Mirror final decisions into a JSONL ledger alongside
     `manual-review-decisions.jsonl`, e.g.
     `easy-final-v2-instability-review-decisions.jsonl`.
   - Keep original expected labels, final labels, decision, notes, and ASI action
     bullets. This makes the approved-label provenance auditable.

3. **ASI updates**
   - Convert recurring FP/FN patterns below into generalized cue→label rules,
     not issue-ID or title-specific exceptions.
   - Preferred targets from the handovers/current files:

```text
eval/openclaw/topic-boundary-guidance.md
eval/openclaw/static-labeling-guidance.md
eval/openclaw/asi-pack-v4.md
eval/openclaw/label-generator/asi-v1.json
src/openclaw_gepa/openclaw_benchmark.py   # dynamic scorer hints, if needed
```

   - For `label-generator/asi-v1.json`, follow the compile-guidance script's
     shape: topic-level `positive`/`negative` rules, row adjudications, and
     scoring notes. If creating a new version, prefer `asi-v2.json` rather than
     silently replacing historical artifacts.

4. **Validation loop after edits**
   - Rerun teacher relabel/stability on changed rows, then rerun small-model
     baseline and best-policy stability.
   - Use the prior handover threshold logic: exact stability is a gate for easy
     approved labels; unstable-but-informative rows are retained as ASI/medium
     material.
   - Do not optimize GEPA on the changed rows until the approved-label source and
     ASI version are frozen.

Source mining artifacts:

```text
runs/openclaw-vanilla-f1-gepa/easy-final-v2-instability-mining.json
runs/openclaw-vanilla-f1-gepa/easy-final-v2-instability-mining.md
```

## A. Held-out test rows needing review

## openclaw-openclaw-83863 / #83863 — ACP/Codex child tasks can be marked succeeded with progress-only output and no final deliverable

- source: `easy-final-v2-test`
- instability_rank: `1`
- pairwise_prediction_jaccard: `0.530`
- exact_rate_vs_expected: `0.000`
- avg_jaccard_vs_expected: `0.490`
- avg_symdiff_vs_expected: `3.50`
- unique_prediction_sets: `8/8`
- expected_topics: `acp, agent_runtime, codex, coding_agents, reliability`
- volatile_topics: `[['sessions', 6], ['notifications', 5], ['codex', 4], ['coding_agents', 4], ['agent_runtime', 2], ['queueing', 2], ['ui_tui', 1]]`
- recurring_false_positives: `[['sessions', 6], ['notifications', 5], ['queueing', 2], ['ui_tui', 1]]`
- recurring_false_negatives: `[['agent_runtime', 6], ['coding_agents', 4], ['codex', 4]]`

**Current rationales**
- `acp`: The failure is explicitly in ACP child sessions and ACP manager done-event handling.
- `agent_runtime`: The core bug is child task lifecycle/status being marked succeeded without a final deliverable.
- `codex`: The issue specifically concerns Codex ACP child tasks returning only progress text.
- `coding_agents`: It affects parent/child agent workflows, subagents, task ledgers, and final-deliverable contracts.
- `reliability`: Incorrect success state after delivery retry failure creates silent failure and message-loss behavior.

**Common predictions**
- `acp, codex, notifications, reliability, sessions` × 1
- `acp, agent_runtime, codex, reliability, sessions` × 1
- `acp, agent_runtime, codex, notifications, reliability` × 1

**Per-model predictions**
- deepseek4: `[['acp', 'coding_agents', 'reliability', 'sessions'], ['acp', 'codex', 'reliability', 'sessions', 'ui_tui']]`
- gpt-5.4-mini: `[['acp', 'codex', 'notifications', 'reliability', 'sessions'], ['acp', 'agent_runtime', 'codex', 'reliability', 'sessions'], ['acp', 'agent_runtime', 'codex', 'notifications', 'reliability']]`
- sonnet: `[['acp', 'coding_agents', 'notifications', 'queueing', 'reliability'], ['acp', 'coding_agents', 'notifications', 'queueing', 'reliability', 'sessions'], ['acp', 'coding_agents', 'notifications', 'reliability', 'sessions']]`

**Review focus**

- Confirm whether the expected labels are truly easy/exact or whether one or more labels are boundary-dependent.
- False positives to address in ASI: `sessions, notifications, queueing, ui_tui`.
- False negatives to address in ASI: `agent_runtime, coding_agents, codex`.

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: issue
- Number: 83863
- URL: https://github.com/openclaw/openclaw/issues/83863
- Title: ACP/Codex child tasks can be marked succeeded with progress-only output and no final deliverable
- State: OPEN
- Author: chac4l
- Labels: P1, clawsweeper:fix-shape-clear, clawsweeper:queueable-fix, clawsweeper:source-repro, impact:session-state, impact:message-loss, issue-rating: 🦞 diamond lobster

Body:
```markdown
## Summary

ACP/Codex child sessions can terminate with only interim/progress text (for example "I'll inspect...", "I'm checking...", "I'm verifying now...") and OpenClaw records the durable task as `succeeded` / `outcome.status=ok` even though no final deliverable was captured and the completion announcement later fails.

This makes the parent agent correctly distrust the child ("Codex returned only progress, not delivery"), but the task ledger and UI still present the child run as successful. Operationally this looks like Codex/OpenClaw silently succeeded while no PR/diff/final report was delivered.

## Evidence Pattern

Observed on a real background ACP workflow. Operational identifiers and deployment details are intentionally redacted.

The affected child sessions had transcripts shaped like:

```text
user: <task requiring concrete deliverables>
assistant: I'll inspect/check/verify/merge now... <progress-only text>
```

The durable task state then showed rows equivalent to:

```text
runtime=acp       status=succeeded  deliveryStatus=session_queued  progressSummary=<progress-only text>
runtime=subagent  status=succeeded  deliveryStatus=failed          progressSummary=<progress-only text>
runtime=cli       status=succee
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-83863",
  "decision": "drop_to_medium",
  "final_labels": [
    "acp",
    "agent_runtime",
    "codex",
    "coding_agents",
    "reliability"
  ],
  "asi_actions": [],
  "notes": "Mined stability shows zero exact match and broad boundary disagreement; use as ASI/boundary material unless human review confirms labels are still easy."
}
```

## openclaw-openclaw-70002 / #70002 — ci: skip docs sync & translate-trigger workflows in forks

- source: `easy-final-v2-test`
- instability_rank: `2`
- pairwise_prediction_jaccard: `0.536`
- exact_rate_vs_expected: `0.500`
- avg_jaccard_vs_expected: `0.688`
- avg_symdiff_vs_expected: `0.62`
- unique_prediction_sets: `3/8`
- expected_topics: `tests_ci`
- volatile_topics: `[['tests_ci', 7], ['reliability', 3], ['docs', 1]]`
- recurring_false_positives: `[['reliability', 3], ['docs', 1]]`
- recurring_false_negatives: `[['tests_ci', 1]]`

**Current rationales**
- `tests_ci`: Direct change to GitHub Actions workflow files to guard CI/CD jobs in forks.

**Common predictions**
- `tests_ci` × 4
- `reliability, tests_ci` × 3
- `docs` × 1

**Per-model predictions**
- deepseek4: `[['tests_ci'], ['docs']]`
- gpt-5.4-mini: `[['reliability', 'tests_ci'], ['reliability', 'tests_ci'], ['reliability', 'tests_ci']]`
- sonnet: `[['tests_ci'], ['tests_ci'], ['tests_ci']]`

**Review focus**

- Confirm whether the expected labels are truly easy/exact or whether one or more labels are boundary-dependent.
- False positives to address in ASI: `reliability, docs`.
- False negatives to address in ASI: `tests_ci`.

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: pull_request
- Number: 70002
- URL: https://github.com/openclaw/openclaw/pull/70002
- Title: ci: skip docs sync & translate-trigger workflows in forks
- State: OPEN
- Author: xudaiyanzi
- Labels: size: XS, triage: risky-infra, triage: needs-real-behavior-proof, proof: sufficient, P2, rating: 🐚 platinum hermit, merge-risk: 🚨 automation, status: 👀 ready for maintainer look, proof: 📸 screenshot
- Changed file count available to wrapper: 2
- Changed files: .github/workflows/docs-sync-publish.yml, .github/workflows/docs-translate-trigger-release.yml

Body:
```markdown
## Summary

- **Problem:** Two upstream-only workflows (`docs-sync-publish.yml`, `docs-translate-trigger-release.yml`) fail with `Authentication failed for 'https://github.com/openclaw/docs.git/'` on every push to `main` in any fork, because they rely on the `OPENCLAW_DOCS_SYNC_TOKEN` secret that only exists in `openclaw/openclaw`.
- **Why it matters:** Creates a red ✗ on every normal fork-sync (`git fetch upstream main && git push origin main`), confuses new contributors, and spams fork Actions dashboards with irrecoverable failures.
- **What changed:** Added `if: github.repository == 'openclaw/openclaw'` to the single job in each of the two workflows — the same guard pattern already used ~30 times across the repo (`ci.yml`, `codeql.yml`, `control-ui-locale-refresh.yml`).
- **What did NOT change (scope boundary):** No changes to workflow logic, secrets, the publish repo, the sync script (`scripts/docs-sync-publish.mjs`), documentation, or any other workflow. Behavior in `openclaw/openclaw` is byte-for-byte identical.

## Change Type (select all)

- [x
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-70002",
  "decision": "keep_easy_with_asi",
  "final_labels": [
    "tests_ci"
  ],
  "asi_actions": [],
  "notes": "Probably keep if labels are correct, but add targeted ASI for recurring FP/FN topics."
}
```

## openclaw-openclaw-84697 / #84697 — Custom OpenAI-compatible provider with baseUrl without /v1 fails with cryptic 'incomplete terminal response' error

- source: `easy-final-v2-test`
- instability_rank: `3`
- pairwise_prediction_jaccard: `0.545`
- exact_rate_vs_expected: `0.250`
- avg_jaccard_vs_expected: `0.677`
- avg_symdiff_vs_expected: `1.12`
- unique_prediction_sets: `5/8`
- expected_topics: `config, local_model_providers, model_serving`
- volatile_topics: `[['config', 5], ['model_serving', 5], ['reliability', 3]]`
- recurring_false_positives: `[['reliability', 3]]`
- recurring_false_negatives: `[['model_serving', 3], ['config', 3]]`

**Current rationales**
- `config`: Issue centers on manual/onboard provider configuration and the required baseUrl path suffix.
- `local_model_providers`: Custom OpenAI-compatible provider setup, baseUrl handling, and provider validation are central.
- `model_serving`: Failure occurs in chat/completions streaming response handling when the endpoint returns HTML instead of JSON/SSE.

**Common predictions**
- `config, local_model_providers, model_serving` × 2
- `config, local_model_providers` × 2
- `local_model_providers, model_serving, reliability` × 2

**Per-model predictions**
- deepseek4: `[['local_model_providers'], ['config', 'local_model_providers']]`
- gpt-5.4-mini: `[['config', 'local_model_providers', 'model_serving'], ['config', 'local_model_providers'], ['config', 'local_model_providers', 'model_serving']]`
- sonnet: `[['config', 'local_model_providers', 'model_serving', 'reliability'], ['local_model_providers', 'model_serving', 'reliability'], ['local_model_providers', 'model_serving', 'reliability']]`

**Review focus**

- Confirm whether the expected labels are truly easy/exact or whether one or more labels are boundary-dependent.
- False positives to address in ASI: `reliability`.
- False negatives to address in ASI: `model_serving, config`.

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: issue
- Number: 84697
- URL: https://github.com/openclaw/openclaw/issues/84697
- Title: Custom OpenAI-compatible provider with baseUrl without /v1 fails with cryptic 'incomplete terminal response' error
- State: OPEN
- Author: mz1009-web
- Labels: P2, clawsweeper:fix-shape-clear, clawsweeper:queueable-fix, clawsweeper:source-repro, impact:auth-provider, issue-rating: 🦞 diamond lobster

Body:
```markdown
## Bug Description

When configuring a custom OpenAI-compatible API provider (e.g., `spanagent.xyz`), if the `baseUrl` is set to `https://spanagent.xyz` (without `/v1` suffix), OpenClaw constructs the request URL as `https://spanagent.xyz/chat/completions`. This endpoint returns an HTML page (200 OK, Content-Type: text/html), which the streaming handler cannot parse. The error surfaced to the user is cryptic:

```
FailoverError: spanagent/deepseek-v4-flash ended with an incomplete terminal response
```

Meanwhile, the log shows `contentType=text/html; charset=utf-8` but no clear indication that the URL path is wrong.

## Steps to Reproduce

1. Add a custom provider via `openclaw onboard` or manual config:
   ```json
   {
     "baseUrl": "https://spanagent.xyz",
     "api": "openai-completions",
     "models": [{ "id": "deepseek-v4-flash", "reasoning": true, ... }]
   }
   ```
2. Run `openclaw agent --agent <agent> --message "hi" --model <provider>/deepseek-v4-flash --local`
3. Observe: request goes to `https://spanagent.xyz/chat/completions` (no `/v1` prefix)
4. API returns HTML page with 200 OK
5. Error: `incomplete terminal response` — no mention of wrong URL

## Expected Behavior

1. The onboard wizard or docs should
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-84697",
  "decision": "fix_labels_or_add_asi",
  "final_labels": [
    "config",
    "local_model_providers",
    "model_serving"
  ],
  "asi_actions": [],
  "notes": "Low exact rate. Check whether expected labels are over-specific; otherwise add targeted ASI examples."
}
```

## openclaw-openclaw-70518 / #70518 — fix(config): add heartbeat skill allowlist

- source: `easy-final-v2-test`
- instability_rank: `4`
- pairwise_prediction_jaccard: `0.569`
- exact_rate_vs_expected: `0.375`
- avg_jaccard_vs_expected: `0.727`
- avg_symdiff_vs_expected: `1.12`
- unique_prediction_sets: `6/8`
- expected_topics: `config, cron_automation, skills_plugins`
- volatile_topics: `[['cron_automation', 6], ['skills_plugins', 6], ['docs', 3], ['agent_runtime', 1], ['gateway', 1]]`
- recurring_false_positives: `[['docs', 3], ['gateway', 1], ['agent_runtime', 1]]`
- recurring_false_negatives: `[['cron_automation', 2], ['skills_plugins', 2]]`

**Current rationales**
- `config`: Adds new heartbeat configuration fields, schema/help/labels/types, and documented config surface.
- `cron_automation`: The behavior is specifically for periodic heartbeat runs and the heartbeat runner.
- `skills_plugins`: Introduces a heartbeat-specific allowSkills allowlist that restricts loaded skills for those runs.

**Common predictions**
- `config, cron_automation, skills_plugins` × 3
- `config, gateway, skills_plugins` × 1
- `config, skills_plugins` × 1

**Per-model predictions**
- deepseek4: `[['config', 'cron_automation', 'docs'], ['agent_runtime', 'config', 'cron_automation', 'docs']]`
- gpt-5.4-mini: `[['config', 'gateway', 'skills_plugins'], ['config', 'cron_automation', 'skills_plugins'], ['config', 'skills_plugins']]`
- sonnet: `[['config', 'cron_automation', 'skills_plugins'], ['config', 'cron_automation', 'skills_plugins'], ['config', 'cron_automation', 'docs', 'skills_plugins']]`

**Review focus**

- Confirm whether the expected labels are truly easy/exact or whether one or more labels are boundary-dependent.
- False positives to address in ASI: `docs, gateway, agent_runtime`.
- False negatives to address in ASI: `cron_automation, skills_plugins`.

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: pull_request
- Number: 70518
- URL: https://github.com/openclaw/openclaw/pull/70518
- Title: fix(config): add heartbeat skill allowlist
- State: OPEN
- Author: akai-shuuichi
- Labels: docs, gateway, size: S, triage: needs-real-behavior-proof, P2, rating: 🧂 unranked krab, merge-risk: 🚨 compatibility, status: 📣 needs proof
- Changed file count available to wrapper: 12
- Changed files: docs/gateway/configuration-reference.md, docs/gateway/heartbeat.md, src/config/heartbeat-config-honor.inventory.test.ts, src/config/schema.base.generated.ts, src/config/schema.help.ts, src/config/schema.labels.ts, src/config/types.agent-defaults.ts, src/config/zod-schema.agent-defaults.test.ts, src/config/zod-schema.agent-runtime.ts, src/infra/heartbeat-runner.model-override.test.ts, src/infra/heartbeat-runner.ts, test/helpers/config/heartbeat-config-honor.inventory.ts

Body:
```markdown
## Summary

- Problem: heartbeat runs currently inherit the target agent's full skill set, even when heartbeat only needs a small subset or none.
- Why it matters: large skill catalogs inflate the skills prompt and waste input context on every heartbeat turn.
- What changed: added `agents.defaults.heartbeat.allowSkills` and `agents.list[].heartbeat.allowSkills`, and threaded that allowlist into heartbeat reply runs.
- What did NOT change (scope boundary): default behavior is unchanged when `allowSkills` is unset; normal non-heartbeat agent turns are unaffected.

## Change Type (select all)

- [x] Bug fix
- [ ] Feature
- [ ] Refactor required for the fix
- [x] Docs
- [ ] Security hardening
- [ ] Chore/infra

## Scope (select all touched areas)

- [x] Gateway
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-70518",
  "decision": "keep_easy_with_asi",
  "final_labels": [
    "config",
    "cron_automation",
    "skills_plugins"
  ],
  "asi_actions": [],
  "notes": "Probably keep if labels are correct, but add targeted ASI for recurring FP/FN topics."
}
```

## openclaw-openclaw-87277 / #87277 — [Feature] Add MiMo-V2.5 to Xiaomi catalog + automatic multimodal routing when DeepSeek V4-Pro is primary model

- source: `easy-final-v2-test`
- instability_rank: `5`
- pairwise_prediction_jaccard: `0.584`
- exact_rate_vs_expected: `0.000`
- avg_jaccard_vs_expected: `0.562`
- avg_symdiff_vs_expected: `1.62`
- unique_prediction_sets: `5/8`
- expected_topics: `config, model_releases, model_serving`
- volatile_topics: `[['model_serving', 7], ['open_weight_models', 3], ['agent_runtime', 1], ['model_releases', 1], ['reliability', 1]]`
- recurring_false_positives: `[['open_weight_models', 3], ['reliability', 1], ['agent_runtime', 1]]`
- recurring_false_negatives: `[['model_releases', 7], ['model_serving', 1]]`

**Current rationales**
- `config`: (no rationale captured in source row)
- `model_releases`: Issue asks to add newly released MiMo-V2.5 with version-specific benchmarks and catalog metadata.
- `model_serving`: Core behavior request is automatic routing to a multimodal-capable model before dispatch based on input capabilities.

**Common predictions**
- `config, model_serving` × 3
- `config, model_serving, open_weight_models` × 2
- `config, model_serving, reliability` × 1

**Per-model predictions**
- deepseek4: `[['agent_runtime', 'config'], ['config', 'model_serving']]`
- gpt-5.4-mini: `[['config', 'model_serving'], ['config', 'model_serving', 'reliability'], ['config', 'model_serving']]`
- sonnet: `[['config', 'model_releases', 'model_serving', 'open_weight_models'], ['config', 'model_serving', 'open_weight_models'], ['config', 'model_serving', 'open_weight_models']]`

**Review focus**

- Confirm whether the expected labels are truly easy/exact or whether one or more labels are boundary-dependent.
- False positives to address in ASI: `open_weight_models, reliability, agent_runtime`.
- False negatives to address in ASI: `model_releases, model_serving`.

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: issue
- Number: 87277
- URL: https://github.com/openclaw/openclaw/issues/87277
- Title: [Feature] Add MiMo-V2.5 to Xiaomi catalog + automatic multimodal routing when DeepSeek V4-Pro is primary model
- State: OPEN
- Author: 0mlkrizzz655335v
- Labels: P2, clawsweeper:no-new-fix-pr, clawsweeper:needs-maintainer-review, clawsweeper:needs-product-decision, impact:message-loss, impact:auth-provider, issue-rating: 🌊 off-meta tidepool

Body:
```markdown
# [Feature] Add MiMo-V2.5 to Xiaomi catalog + automatic multimodal routing when DeepSeek V4-Pro is primary model

# [Feature] Add MiMo-V2.5 to Xiaomi catalog + automatic multimodal routing when DeepSeek V4-Pro is primary model

## Summary

Two related asks in one issue:

1. **Add `xiaomi/mimo-v2.5` to the built-in Xiaomi provider catalog** — it was released on April 22 2026 and supersedes `mimo-v2-omni` across every multimodal benchmark.
2. **Auto-route to a multimodal model when the primary model is text-only and the incoming message contains image / video / audio attachments** — so users running DeepSeek V4-Pro as their default never have to manually switch models.

---

## Why MiMo-V2.5 instead of MiMo-V2-Omni

| Property | `mimo-v2-omni` | `mimo-v2.5` |
|---|---|---|
| Parameters | — | 310B total / 15B active (sparse MoE) |
| Modalities | text, image | text, image, video, audio |
| Context window | 262,144 | 1,048,576 |
| Max output | 32,000 | 131,072 |
| Reasoning | ✅ | ✅ |
| Input price | — | $0.40 / 1M tokens |
| Output price | — | $2.00 / 1M tokens |
| API model id | `mimo-v2-omni` | `mimo-v2.5` |
| Base URL | `https://api.xiaomimimo.com/v1` | same |

MiMo-V2.5 trains im
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-87277",
  "decision": "review_or_drop_to_medium",
  "final_labels": [
    "config",
    "model_releases",
    "model_serving"
  ],
  "asi_actions": [],
  "notes": "Zero exact match with low prediction-set stability. Review labels; likely ASI/boundary material or needs label fix."
}
```

## openclaw-openclaw-85660 / #85660 — GitHub Copilot plugin: agents.defaults.imageModel for unknown Copilot model ID falls back to OpenAI provider with confusing 401

- source: `easy-final-v2-test`
- instability_rank: `6`
- pairwise_prediction_jaccard: `0.611`
- exact_rate_vs_expected: `0.125`
- avg_jaccard_vs_expected: `0.738`
- avg_symdiff_vs_expected: `1.12`
- unique_prediction_sets: `5/8`
- expected_topics: `config, model_serving, security, skills_plugins`
- volatile_topics: `[['security', 7], ['skills_plugins', 5], ['model_serving', 4], ['auth_identity', 1]]`
- recurring_false_positives: `[['auth_identity', 1]]`
- recurring_false_negatives: `[['model_serving', 4], ['skills_plugins', 3], ['security', 1]]`

**Current rationales**
- `config`: The repro centers on setting agents.defaults.imageModel to a Copilot model ID and how that config is resolved.
- `model_serving`: (no rationale captured in source row)
- `security`: A GitHub Copilot token is sent to OpenAI due to wrong provider fallback, creating a credential-scope/security concern.
- `skills_plugins`: The bug is in the GitHub Copilot plugin/extension manifest and model resolver paths.

**Common predictions**
- `config, security, skills_plugins` × 3
- `config, model_serving, security` × 2
- `auth_identity, config, security` × 1

**Per-model predictions**
- deepseek4: `[['config', 'model_serving', 'security'], ['config', 'model_serving', 'security', 'skills_plugins']]`
- gpt-5.4-mini: `[['auth_identity', 'config', 'security'], ['config', 'model_serving', 'security'], ['config', 'model_serving', 'skills_plugins']]`
- sonnet: `[['config', 'security', 'skills_plugins'], ['config', 'security', 'skills_plugins'], ['config', 'security', 'skills_plugins']]`

**Review focus**

- Confirm whether the expected labels are truly easy/exact or whether one or more labels are boundary-dependent.
- False positives to address in ASI: `auth_identity`.
- False negatives to address in ASI: `model_serving, skills_plugins, security`.

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: issue
- Number: 85660
- URL: https://github.com/openclaw/openclaw/issues/85660
- Title: GitHub Copilot plugin: agents.defaults.imageModel for unknown Copilot model ID falls back to OpenAI provider with confusing 401
- State: CLOSED
- Author: boycezhu

Body:
```markdown
# GitHub Copilot plugin: agents.defaults.imageModel for unknown Copilot model ID falls back to OpenAI provider with confusing 401

## Summary

Setting `agents.defaults.imageModel` to a Copilot model ID that is **not** in the plugin's static manifest (but is valid on the live Copilot `/models` endpoint) does not trigger the forward-compat path in `extensions/github-copilot/models.ts` (`resolveCopilotForwardCompatModel`). Instead the image tool dispatches the request through the OpenAI provider, sending the GitHub Copilot token (`ghu_…`) to OpenAI's API, which returns a misleading 401.

## Repro

- Copilot Enterprise plan
- Set `agents.defaults.imageModel = "github-copilot/gemini-3.5-flash"` (live API lists this model; static manifest in `extensions/github-copilot/openclaw.plugin.json` only ships `gemini-3-flash` / `gemini-2.5-pro` / `gemini-3.1-pro`)
- Restart gateway
- Trigger the `image` tool

## Observed

```
Image model failed (github-copilot/gemini-3.5-flash):
401 Incorrect API key provided: ghu_y1wl****************************8Kzb.
You can find your API key at https://platform.openai.com/account/api-keys.
```

The `ghu_` token is a GitHub Copilot token being sent to OpenAI. The request was routed to the wrong provider.

## Expected

One of:
1. Forward-compat resolver in `extensions/github-copilot/models.ts` runs for `imageModel` config (same as it wo
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-85660",
  "decision": "fix_labels_or_add_asi",
  "final_labels": [
    "config",
    "model_serving",
    "security",
    "skills_plugins"
  ],
  "asi_actions": [],
  "notes": "Low exact rate. Check whether expected labels are over-specific; otherwise add targeted ASI examples."
}
```

## openclaw-openclaw-74204 / #74204 — memory.qmd.update.embedTimeoutMs default (120 s) is too low for local GGUF; error message doesn't surface the fix

- source: `easy-final-v2-test`
- instability_rank: `7`
- pairwise_prediction_jaccard: `0.621`
- exact_rate_vs_expected: `0.000`
- avg_jaccard_vs_expected: `0.738`
- avg_symdiff_vs_expected: `1.25`
- unique_prediction_sets: `5/8`
- expected_topics: `config, local_models, memory, reliability`
- volatile_topics: `[['reliability', 6], ['local_models', 5], ['self_hosted_inference', 3], ['docs', 1], ['open_weight_models', 1]]`
- recurring_false_positives: `[['self_hosted_inference', 3], ['docs', 1], ['open_weight_models', 1]]`
- recurring_false_negatives: `[['local_models', 3], ['reliability', 2]]`

**Current rationales**
- `config`: Issue centers on the `memory.qmd.update.embedTimeoutMs` config default and making the override discoverable.
- `local_models`: Failure is specific to a local GGUF embedding model on CPU commodity hardware needing longer timeout.
- `memory`: QMD memory embedding and hybrid/vector memory search are the affected subsystem.
- `reliability`: The default timeout repeatedly kills embedding runs, causing backoff loops and disabled vector search.

**Common predictions**
- `config, memory, reliability` × 3
- `config, local_models, memory, reliability, self_hosted_inference` × 2
- `config, local_models, memory` × 1

**Per-model predictions**
- deepseek4: `[['config', 'docs', 'local_models', 'memory', 'reliability'], ['config', 'local_models', 'memory', 'open_weight_models', 'self_hosted_inference']]`
- gpt-5.4-mini: `[['config', 'memory', 'reliability'], ['config', 'memory', 'reliability'], ['config', 'memory', 'reliability']]`
- sonnet: `[['config', 'local_models', 'memory'], ['config', 'local_models', 'memory', 'reliability', 'self_hosted_inference'], ['config', 'local_models', 'memory', 'reliability', 'self_hosted_inference']]`

**Review focus**

- Confirm whether the expected labels are truly easy/exact or whether one or more labels are boundary-dependent.
- False positives to address in ASI: `self_hosted_inference, docs, open_weight_models`.
- False negatives to address in ASI: `local_models, reliability`.

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: issue
- Number: 74204
- URL: https://github.com/openclaw/openclaw/issues/74204
- Title: memory.qmd.update.embedTimeoutMs default (120 s) is too low for local GGUF; error message doesn't surface the fix
- State: OPEN
- Author: Skeptomenos

Body:
```markdown
## Environment

- **OpenClaw version:** 2026.4.25
- **QMD version:** 2.1.0 (bab86d5)
- **Platform:** Ubuntu 24.04, GCP e2-standard-4 (4 vCPU, 16 GB RAM)
- **Workspace size:** 37+ Markdown files in memory root + `memory/` tree
- **GGUF model:** default (`embeddinggemma-300m-qat-Q8_0.gguf`, ~0.6 GB, auto-downloaded)
- **searchMode:** `query` (hybrid BM25 + vector)

## Observed behavior

After enabling hybrid search (`searchMode: "query"`), the gateway emits this warning repeatedly every 2–4 minutes:

```
{"subsystem":"memory","message":"qmd embed failed (boot): Error: qmd embed timed out after 120000ms; backing off for 60s"}
{"subsystem":"memory","message":"qmd embed failed (interval): Error: qmd embed timed out after 120000ms; backing off for 120s"}
```

The embed process runs at 100–186% CPU on 4 vCPU for ~2 minutes before being killed. Peak RAM during GGUF model load: **9.6 GB**. The embed never completes — every attempt times out at exactly 120 s. Vector search is effectively disabled.

## Root cause

The GGUF embedding model takes **3–4 minutes** on a 4-core CPU to embed a 37-file workspace. The default `memory.qmd.update.embedTimeoutMs` is **120 s** — less than the actual embed duration.

The fix (`memory.qmd.update.embedTimeoutMs: 600000`) is only discoverable via `openclaw config schema` or the memory config reference page. The error message does not mention it.
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-74204",
  "decision": "review_or_drop_to_medium",
  "final_labels": [
    "config",
    "local_models",
    "memory",
    "reliability"
  ],
  "asi_actions": [],
  "notes": "Zero exact match with low prediction-set stability. Review labels; likely ASI/boundary material or needs label fix."
}
```

## openclaw-openclaw-72085 / #72085 — docs(commands): document bashForegroundMs clamp bounds (0–30 000 ms)

- source: `easy-final-v2-test`
- instability_rank: `8`
- pairwise_prediction_jaccard: `0.637`
- exact_rate_vs_expected: `0.375`
- avg_jaccard_vs_expected: `0.771`
- avg_symdiff_vs_expected: `0.62`
- unique_prediction_sets: `4/8`
- expected_topics: `config, docs`
- volatile_topics: `[['config', 7], ['exec_tools', 2], ['gateway', 2]]`
- recurring_false_positives: `[['gateway', 2], ['exec_tools', 2]]`
- recurring_false_negatives: `[['config', 1]]`

**Current rationales**
- `config`: Documents the accepted range and clamp behavior for the bashForegroundMs configuration key.
- `docs`: PR is explicitly docs-only and changes documentation in configuration-reference.md.

**Common predictions**
- `config, docs` × 3
- `config, docs, gateway` × 2
- `config, docs, exec_tools` × 2

**Per-model predictions**
- deepseek4: `[['docs'], ['config', 'docs', 'exec_tools']]`
- gpt-5.4-mini: `[['config', 'docs', 'gateway'], ['config', 'docs', 'gateway'], ['config', 'docs']]`
- sonnet: `[['config', 'docs'], ['config', 'docs'], ['config', 'docs', 'exec_tools']]`

**Review focus**

- Confirm whether the expected labels are truly easy/exact or whether one or more labels are boundary-dependent.
- False positives to address in ASI: `gateway, exec_tools`.
- False negatives to address in ASI: `config`.

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: pull_request
- Number: 72085
- URL: https://github.com/openclaw/openclaw/pull/72085
- Title: docs(commands): document bashForegroundMs clamp bounds (0–30 000 ms)
- State: OPEN
- Author: ayesha-aziz123
- Labels: docs, gateway, size: XS, triage: low-signal-docs, triage: needs-real-behavior-proof, P3, rating: 🧂 unranked krab, status: ⏳ waiting on author
- Changed file count available to wrapper: 1
- Changed files: docs/gateway/configuration-reference.md

Body:
```markdown
## Summary

- Problem: `bashForegroundMs` is silently clamped to 0–30 000 ms by `clampInt()` in `src/auto-reply/reply/bash-command.ts` (lines 22–23, 43–48), but the configuration reference did not mention this bound.
- Why it matters: A user setting `bashForegroundMs: 60000` expecting a 60 s timeout silently gets 30 s instead — no warning, no error, no indication in the docs.
- What changed: Added one bullet to the Commands accordion in `docs/gateway/configuration-reference.md` documenting the accepted range (0–30 000 ms) and silent-clamp behavior.
- What did NOT change: No code touched. No behavior changed. Scope boundary is documentation only.

## Change Type

- [ ] Bug fix
- [ ] Feature
- [ ] Refactor required for the fix
- [x] Docs
- [ ] Security hardening

## Linked Issue/PR

No linked issue — standalone docs gap fix.

## Test plan

Docs-only change; no code touched.
Verified bounds against `src/auto-reply/reply/bash-command.ts` lines 22–23 and 43–48.
```

Comments/context:
```markdown
- greptile-apps at 2026-04-26T09:20:54Z:
<h3>Greptile Summary</h3>

This PR adds a single documentation bullet to `docs/gateway/configuration-ref
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-72085",
  "decision": "keep_easy_with_asi",
  "final_labels": [
    "config",
    "docs"
  ],
  "asi_actions": [],
  "notes": "Probably keep if labels are correct, but add targeted ASI for recurring FP/FN topics."
}
```

## openclaw-openclaw-84753 / #84753 — [Feature]: Show display name instead of user ID in session list

- source: `easy-final-v2-test`
- instability_rank: `9`
- pairwise_prediction_jaccard: `0.651`
- exact_rate_vs_expected: `0.000`
- avg_jaccard_vs_expected: `0.569`
- avg_symdiff_vs_expected: `2.00`
- unique_prediction_sets: `4/8`
- expected_topics: `chat_integrations, sessions, ui_tui`
- volatile_topics: `[['config', 7], ['sessions', 7], ['chat_integrations', 5], ['acp', 4], ['api_surface', 1]]`
- recurring_false_positives: `[['config', 7], ['acp', 4], ['api_surface', 1]]`
- recurring_false_negatives: `[['chat_integrations', 3], ['sessions', 1]]`

**Current rationales**
- `chat_integrations`: Request concerns Feishu, Discord, Telegram, WhatsApp channel users and resolving channel peer IDs to display names.
- `sessions`: Core behavior is how session lists and session labels display user identity instead of session peer IDs.
- `ui_tui`: Visible surfaces include the Control UI session sidebar and `openclaw status` Sessions table.

**Common predictions**
- `acp, config, sessions, ui_tui` × 3
- `chat_integrations, config, sessions, ui_tui` × 3
- `acp, chat_integrations, config, sessions, ui_tui` × 1

**Per-model predictions**
- deepseek4: `[['acp', 'chat_integrations', 'config', 'sessions', 'ui_tui'], ['api_surface', 'chat_integrations', 'ui_tui']]`
- gpt-5.4-mini: `[['acp', 'config', 'sessions', 'ui_tui'], ['acp', 'config', 'sessions', 'ui_tui'], ['acp', 'config', 'sessions', 'ui_tui']]`
- sonnet: `[['chat_integrations', 'config', 'sessions', 'ui_tui'], ['chat_integrations', 'config', 'sessions', 'ui_tui'], ['chat_integrations', 'config', 'sessions', 'ui_tui']]`

**Review focus**

- Confirm whether the expected labels are truly easy/exact or whether one or more labels are boundary-dependent.
- False positives to address in ASI: `config, acp, api_surface`.
- False negatives to address in ASI: `chat_integrations, sessions`.

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: issue
- Number: 84753
- URL: https://github.com/openclaw/openclaw/issues/84753
- Title: [Feature]: Show display name instead of user ID in session list
- State: OPEN
- Author: hbs1313
- Labels: enhancement, P3, clawsweeper:no-new-fix-pr, clawsweeper:needs-maintainer-review, clawsweeper:needs-product-decision, clawsweeper:source-repro, issue-rating: 🦞 diamond lobster

Body:
```markdown
### Summary

## Feature Request: Show display name instead of user ID in session list

**What problem does this solve?**
When managing multiple Feishu (or other channel) users, the session list shows `ou_7f1ab2cd5fd91a2899c407e52bd75c18` instead of the user's actual name like "张三". The same applies to Discord (shows user IDs), Telegram, WhatsApp, etc.

This makes session management confusing and slow, especially when helping multiple users.

**Where is this visible?**
1. Control UI session sidebar — shows truncated `ou_7f1ab2…` instead of contact name
2. `openclaw status` → Sessions table — shows full `ou_7f1ab2cd5fd91a2899c407e52bd75c18`
3. `sessions_list` ACP tool output — same

**Proposed solution:**
Add a configurable `sessionLabelFormat` option (or similar) that lets the gateway resolve channel peer IDs to display names in session listings.

For Feishu specifically, `channels.feishu.resolveSenderNames: true` already exists for inbound message resolution — a similar mechanism could be used to resolve sender names into session labels for display purposes.

**Suggested implementation:**
- Add a config option like `channels.<channel>.sessionLabelFormat: "{displayName}"` that falls back to `"{peerId}"` if name resolution fails
- Or, auto-r
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-84753",
  "decision": "drop_to_medium",
  "final_labels": [
    "chat_integrations",
    "sessions",
    "ui_tui"
  ],
  "asi_actions": [],
  "notes": "Mined stability shows zero exact match and broad boundary disagreement; use as ASI/boundary material unless human review confirms labels are still easy."
}
```

## openclaw-openclaw-75784 / #75784 — Phantom user messages appear in webchat after heartbeat wakes / gateway restart / session repair

- source: `easy-final-v2-test`
- instability_rank: `10`
- pairwise_prediction_jaccard: `0.663`
- exact_rate_vs_expected: `0.375`
- avg_jaccard_vs_expected: `0.750`
- avg_symdiff_vs_expected: `1.38`
- unique_prediction_sets: `5/8`
- expected_topics: `chat_integrations, gateway, reliability, sessions`
- volatile_topics: `[['gateway', 7], ['chat_integrations', 5], ['agent_runtime', 4], ['ui_tui', 3]]`
- recurring_false_positives: `[['agent_runtime', 4], ['ui_tui', 3]]`
- recurring_false_negatives: `[['chat_integrations', 3], ['gateway', 1]]`

**Current rationales**
- `chat_integrations`: The reported symptom is phantom user messages appearing in the WebChat channel/history.
- `gateway`: The bug is tied to gateway restart, Gateway journal events, and synthetic messages submitted through the Gateway agent path.
- `reliability`: The issue involves restart recovery, orphan recovery, stuck diagnostics, and session repair producing incorrect state.
- `sessions`: Evidence centers on orphaned subagent sessions, resumeOrphanedSession, session file repair, and session history projection.

**Common predictions**
- `chat_integrations, gateway, reliability, sessions` × 3
- `agent_runtime, gateway, reliability, sessions, ui_tui` × 2
- `gateway, reliability, sessions, ui_tui` × 1

**Per-model predictions**
- deepseek4: `[['agent_runtime', 'chat_integrations', 'gateway', 'reliability', 'sessions'], ['agent_runtime', 'chat_integrations', 'reliability', 'sessions']]`
- gpt-5.4-mini: `[['chat_integrations', 'gateway', 'reliability', 'sessions'], ['chat_integrations', 'gateway', 'reliability', 'sessions'], ['chat_integrations', 'gateway', 'reliability', 'sessions']]`
- sonnet: `[['agent_runtime', 'gateway', 'reliability', 'sessions', 'ui_tui'], ['gateway', 'reliability', 'sessions', 'ui_tui'], ['agent_runtime', 'gateway', 'reliability', 'sessions', 'ui_tui']]`

**Review focus**

- Confirm whether the expected labels are truly easy/exact or whether one or more labels are boundary-dependent.
- False positives to address in ASI: `agent_runtime, ui_tui`.
- False negatives to address in ASI: `chat_integrations, gateway`.

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: issue
- Number: 75784
- URL: https://github.com/openclaw/openclaw/issues/75784
- Title: Phantom user messages appear in webchat after heartbeat wakes / gateway restart / session repair
- State: OPEN
- Author: maxbreaker1983

Body:
```markdown
## Environment
- OpenClaw: 2026.4.29 (commit a448042)
- OS: WSL2 (Linux 6.6.87.2-microsoft-standard-WSL2, x86_64)
- Node: v22.22.2
- Channel: webchat

## Description
Three phantom user messages appeared in webchat that the user did NOT send.

### Phantom 1 - Context bleed from tool call
After assistant ran a curl API test with "say hello in 3 words" as test prompt, a user message with that exact text appeared with no provenance.

### Phantom 2 - After gateway restart + session repair
Gateway restart at 00:46 triggered orphan recovery and session file repair, then phantom message appeared.

### Phantom 3 - During stuck subagent diagnostics
Stuck subagent triggered repeated diagnostics causing spurious wake events.

## Evidence
Gateway journal logs show:
- subagent-orphan-recovery events
- stuck session diagnostics (age 127s-183s)  
- session file repaired events (rewrote 1 assistant message)

## Impact
- Messages appear that user did not send
- Wastes tokens on unwanted replies
- Users cannot distinguish real vs system messages

## Reproduction
1. Spawn subagent with short test phrase in task
2. Wait for heartbeat/wake event
3. Observe: test phrase appears as user message

```

Comments/context:
```markdown
- clawsweeper at 2026-05-01T19:06:50Z:
Codex review: keeping this open for maintainer follow-up; there is still a little grit to resolve.

**Summary**
Keep this open. Current mai
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-75784",
  "decision": "keep_easy_with_asi",
  "final_labels": [
    "chat_integrations",
    "gateway",
    "reliability",
    "sessions"
  ],
  "asi_actions": [],
  "notes": "Probably keep if labels are correct, but add targeted ASI for recurring FP/FN topics."
}
```

## openclaw-openclaw-67539 / #67539 — [Feature]: Add provider-specific TTS prompt hints

- source: `easy-final-v2-test`
- instability_rank: `11`
- pairwise_prediction_jaccard: `0.679`
- exact_rate_vs_expected: `0.625`
- avg_jaccard_vs_expected: `0.812`
- avg_symdiff_vs_expected: `0.50`
- unique_prediction_sets: `4/8`
- expected_topics: `api_surface, self_hosted_inference`
- volatile_topics: `[['api_surface', 6], ['skills_plugins', 2]]`
- recurring_false_positives: `[['skills_plugins', 2]]`
- recurring_false_negatives: `[['api_surface', 2]]`

**Current rationales**
- `api_surface`: It proposes changing the speech provider contract with a new optional buildPromptHint hook and context shape.
- `self_hosted_inference`: The feature is centered on TTS speech providers and provider-specific speech prompt behavior.

**Common predictions**
- `api_surface, self_hosted_inference` × 5
- `api_surface, self_hosted_inference, skills_plugins` × 1
- `self_hosted_inference` × 1

**Per-model predictions**
- deepseek4: `[['self_hosted_inference'], ['self_hosted_inference', 'skills_plugins']]`
- gpt-5.4-mini: `[['api_surface', 'self_hosted_inference'], ['api_surface', 'self_hosted_inference'], ['api_surface', 'self_hosted_inference']]`
- sonnet: `[['api_surface', 'self_hosted_inference'], ['api_surface', 'self_hosted_inference'], ['api_surface', 'self_hosted_inference', 'skills_plugins']]`

**Review focus**

- Confirm whether the expected labels are truly easy/exact or whether one or more labels are boundary-dependent.
- False positives to address in ASI: `skills_plugins`.
- False negatives to address in ASI: `api_surface`.

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: issue
- Number: 67539
- URL: https://github.com/openclaw/openclaw/issues/67539
- Title: [Feature]: Add provider-specific TTS prompt hints
- State: OPEN
- Author: barronlroth
- Labels: P2, clawsweeper:no-new-fix-pr, clawsweeper:fix-shape-clear, clawsweeper:needs-maintainer-review, clawsweeper:needs-product-decision, clawsweeper:source-repro, issue-rating: 🦞 diamond lobster

Body:
```markdown
## Summary

Add provider-specific, model-aware TTS prompt hints so agents know which expressive controls are valid for the active speech provider.

## Problem to solve

OpenClaw already has a generic TTS runtime hint that tells agents they can use `[[tts:...]]` directives and optional `[[tts:text]]...[[/tts:text]]` blocks. That is enough for the transport layer, but it does not teach the model provider-specific expressive syntax.

For example, the Google Gemini TTS provider added in #67515 passes text directly to Gemini, so square-bracket audio tags such as `[whispers]` or `[laughs]` work when they appear inside the spoken TTS text. However, the active system hint does not tell the agent that Gemini supports those tags, so the feature is discoverable in docs but not reliably discoverable at runtime.

This is not unique to Gemini. Different TTS providers and models have different expressive surfaces: Gemini audio tags, ElevenLabs model-specific performance cues, OpenAI model-specific instructions support, Microsoft voice/rate/pitch behavior, etc. Without provider-scoped hints, agents may either miss useful expressive controls or mix syntax from one provider into another.

## Proposed solution

Add an optional provider-owned prompt hin
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-67539",
  "decision": "keep_easy_with_asi",
  "final_labels": [
    "api_surface",
    "self_hosted_inference"
  ],
  "asi_actions": [],
  "notes": "Probably keep if labels are correct, but add targeted ASI for recurring FP/FN topics."
}
```

## openclaw-openclaw-75043 / #75043 — Add provider-aware automatic TTS emotion mapping

- source: `easy-final-v2-test`
- instability_rank: `12`
- pairwise_prediction_jaccard: `0.690`
- exact_rate_vs_expected: `0.250`
- avg_jaccard_vs_expected: `0.729`
- avg_symdiff_vs_expected: `1.00`
- unique_prediction_sets: `4/8`
- expected_topics: `api_surface, config, self_hosted_inference`
- volatile_topics: `[['api_surface', 4], ['docs', 4]]`
- recurring_false_positives: `[['docs', 4]]`
- recurring_false_negatives: `[['api_surface', 4]]`

**Current rationales**
- `api_surface`: It maps inferred emotions into provider/request control surfaces and applies the behavior across normal, telephony, and streaming TTS synthesis paths.
- `config`: It adds opt-in `messages.tts.autoEmotion` configuration and updates config help/schema surfaces for the new setting.
- `self_hosted_inference`: The PR is centered on TTS synthesis behavior and speech provider adapters, including OpenAI, ElevenLabs, Volcengine, Xiaomi, and Azure.

**Common predictions**
- `config, self_hosted_inference` × 2
- `config, docs, self_hosted_inference` × 2
- `api_surface, config, self_hosted_inference` × 2

**Per-model predictions**
- deepseek4: `[['config', 'docs', 'self_hosted_inference'], ['api_surface', 'config', 'self_hosted_inference']]`
- gpt-5.4-mini: `[['config', 'self_hosted_inference'], ['config', 'docs', 'self_hosted_inference'], ['config', 'self_hosted_inference']]`
- sonnet: `[['api_surface', 'config', 'self_hosted_inference'], ['api_surface', 'config', 'docs', 'self_hosted_inference'], ['api_surface', 'config', 'docs', 'self_hosted_inference']]`

**Review focus**

- Confirm whether the expected labels are truly easy/exact or whether one or more labels are boundary-dependent.
- False positives to address in ASI: `docs`.
- False negatives to address in ASI: `api_surface`.

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: pull_request
- Number: 75043
- URL: https://github.com/openclaw/openclaw/pull/75043
- Title: Add provider-aware automatic TTS emotion mapping
- State: OPEN
- Author: xuruiray
- Labels: docs, size: XL, extensions: openai, extensions: tts-local-cli, plugin: azure-speech, triage: dirty-candidate, proof: supplied, extensions: microsoft, P2, rating: 🦪 silver shellfish, merge-risk: 🚨 compatibility, status: 📣 needs proof

Body:
```markdown
# Add provider-aware automatic TTS emotion mapping

## Summary
- Add opt-in `messages.tts.autoEmotion` support that infers a conservative abstract emotion from synthesized text.
- Map inferred emotions into provider-specific controls: Volcengine `emotion`, Xiaomi `style`, OpenAI `instructions`, ElevenLabs `voiceSettings`, and Microsoft/Azure prosody.
- Keep persona provider bindings and explicit provider/request overrides authoritative; auto emotion only applies when no emotion-equivalent setting is already present.
- Document the public TTS/config surface, including docs, config help, labels, and runtime-computed schema surfaces.
- Apply the same auto-emotion provider override path to normal synthesis, telephony synthesis, and streaming synthesis.

## Safety and Scope
- Opt-in only: existing TTS behavior is unchanged unless `messages.tts.autoEmotion.enabled` is set.
- Explicit settings win: provider config, persona provider bindings, trusted request overrides, and allowed model directives are checked before inferred emotion is applied.
- Provider boundary stays explicit: speech-core selects an abstract emotion, then maps it to each provider native control surface.
- The PR touches runtime,
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-75043",
  "decision": "fix_labels_or_add_asi",
  "final_labels": [
    "api_surface",
    "config",
    "self_hosted_inference"
  ],
  "asi_actions": [],
  "notes": "Low exact rate. Check whether expected labels are over-specific; otherwise add targeted ASI examples."
}
```

## openclaw-openclaw-78977 / #78977 — fix(providers): skip store:false for proxy-like Responses API endpoints (#78897)

- source: `easy-final-v2-test`
- instability_rank: `13`
- pairwise_prediction_jaccard: `0.699`
- exact_rate_vs_expected: `0.625`
- avg_jaccard_vs_expected: `0.823`
- avg_symdiff_vs_expected: `0.62`
- unique_prediction_sets: `3/8`
- expected_topics: `local_model_providers, model_serving, reliability`
- volatile_topics: `[['local_model_providers', 7], ['reliability', 5], ['api_surface', 1]]`
- recurring_false_positives: `[['api_surface', 1]]`
- recurring_false_negatives: `[['reliability', 3], ['local_model_providers', 1]]`

**Current rationales**
- `local_model_providers`: Fix targets LiteLLM/custom baseUrl proxy-like OpenAI-compatible provider handling.
- `model_serving`: Changes Responses API endpoint payload behavior for the `store` field and continuation handling.
- `reliability`: Prevents multi-turn continuation failures caused by backends rejecting unpersisted `rs_*` items.

**Common predictions**
- `local_model_providers, model_serving, reliability` × 5
- `local_model_providers, model_serving` × 2
- `api_surface, model_serving` × 1

**Per-model predictions**
- deepseek4: `[['local_model_providers', 'model_serving'], ['local_model_providers', 'model_serving', 'reliability']]`
- gpt-5.4-mini: `[['local_model_providers', 'model_serving'], ['local_model_providers', 'model_serving', 'reliability'], ['api_surface', 'model_serving']]`
- sonnet: `[['local_model_providers', 'model_serving', 'reliability'], ['local_model_providers', 'model_serving', 'reliability'], ['local_model_providers', 'model_serving', 'reliability']]`

**Review focus**

- Confirm whether the expected labels are truly easy/exact or whether one or more labels are boundary-dependent.
- False positives to address in ASI: `api_surface`.
- False negatives to address in ASI: `reliability, local_model_providers`.

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: pull_request
- Number: 78977
- URL: https://github.com/openclaw/openclaw/pull/78977
- Title: fix(providers): skip store:false for proxy-like Responses API endpoints (#78897)
- State: OPEN
- Author: SymbolStar
- Labels: agents, size: XS, triage: needs-real-behavior-proof, P2, rating: 🧂 unranked krab, merge-risk: 🚨 compatibility, merge-risk: 🚨 security-boundary, status: 📣 needs proof
- Changed file count available to wrapper: 2
- Changed files: src/agents/openai-responses-payload-policy.test.ts, src/agents/openai-responses-payload-policy.ts

Body:
```markdown
## Summary

For non-native OpenAI endpoints (e.g. LiteLLM proxies) using the Responses API, the transport stream unconditionally sends `store: false` in disable mode. This causes continuation failures when prior `rs_*` response items are replayed in subsequent turns — the backend rejects them because those items were never persisted.

## Root Cause

In `resolveOpenAIResponsesPayloadPolicy`, the `"disable"` store mode checked only `supportsResponsesStoreField` (true for any Responses API endpoint) without considering whether the endpoint is a known native OpenAI route. Proxy-like endpoints (custom baseUrl, non-OpenAI provider) received `store: false` even though they need persistence for multi-turn continuations.

## Fix

Only emit `store: false` in disable mode when `usesKnownNativeOpenAIRoute` is true. For proxy-like endpoints, `explicitStore` becomes `undefined` (omitted from payload), letting the backend use its default behavior (typically `store: true`).

## Test

Added a unit test verifying that a LiteLLM proxy endpoint with `storeMode: "disable"` does not emit
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-78977",
  "decision": "keep_easy_with_asi",
  "final_labels": [
    "local_model_providers",
    "model_serving",
    "reliability"
  ],
  "asi_actions": [],
  "notes": "Probably keep if labels are correct, but add targeted ASI for recurring FP/FN topics."
}
```

## openclaw-openclaw-56613 / #56613 — [Feature]: Talk/Voice tab — agent/session switching + per-agent TTS voice

- source: `easy-final-v2-test`
- instability_rank: `14`
- pairwise_prediction_jaccard: `0.714`
- exact_rate_vs_expected: `0.000`
- avg_jaccard_vs_expected: `0.708`
- avg_symdiff_vs_expected: `1.00`
- unique_prediction_sets: `2/8`
- expected_topics: `config, sessions, ui_tui`
- volatile_topics: `[['config', 4], ['self_hosted_inference', 4]]`
- recurring_false_positives: `[['self_hosted_inference', 4]]`
- recurring_false_negatives: `[['config', 4]]`

**Current rationales**
- `config`: Requests per-agent TTS voice settings via agents.list configuration overriding global TTS settings.
- `sessions`: Core remaining request is Voice/Talk tab routing to the selected agent/session instead of hardcoded main session.
- `ui_tui`: Feature is a user-facing Talk/Voice tab session picker similar to the Chat tab session switcher.

**Common predictions**
- `config, self_hosted_inference, sessions, ui_tui` × 4
- `sessions, ui_tui` × 4

**Per-model predictions**
- deepseek4: `[['sessions', 'ui_tui'], ['sessions', 'ui_tui']]`
- gpt-5.4-mini: `[['config', 'self_hosted_inference', 'sessions', 'ui_tui'], ['sessions', 'ui_tui'], ['sessions', 'ui_tui']]`
- sonnet: `[['config', 'self_hosted_inference', 'sessions', 'ui_tui'], ['config', 'self_hosted_inference', 'sessions', 'ui_tui'], ['config', 'self_hosted_inference', 'sessions', 'ui_tui']]`

**Review focus**

- Confirm whether the expected labels are truly easy/exact or whether one or more labels are boundary-dependent.
- False positives to address in ASI: `self_hosted_inference`.
- False negatives to address in ASI: `config`.

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: issue
- Number: 56613
- URL: https://github.com/openclaw/openclaw/issues/56613
- Title: [Feature]: Talk/Voice tab — agent/session switching + per-agent TTS voice
- State: OPEN
- Author: kenchen3000
- Labels: P3, clawsweeper:no-new-fix-pr, clawsweeper:fix-shape-clear, clawsweeper:needs-maintainer-review, clawsweeper:needs-product-decision, clawsweeper:source-repro, impact:session-state, issue-rating: 🦞 diamond lobster

Body:
```markdown
### Summary

Two related feature requests for the Android (and iOS/macOS) Talk/Voice mode:

## 1. Voice/Talk tab agent switching

Currently the Voice tab is hardcoded to the `main` session (default agent). The Chat tab already has a session picker that lets users switch between agents, but the Voice tab does not.

**Request:** Allow users to select which agent to talk to in the Voice tab, similar to how the Chat tab session picker works.

**Use case:** Users with multiple agents (e.g., IT Director, Data Scientist, Marketing Director) want to have voice conversations with each of them, not just the default agent.

**Current behavior:** Voice tab always sends to `main` session via `chat.send`. Switching sessions in the Chat tab does not affect the Voice tab.

**Expected behavior:** Voice tab respects the selected session/agent, or has its own agent picker.

**Code reference:** `VoiceTabScreen.kt` has no session selection. `TalkModeManager.kt` uses `mainSessionKey` which defaults to `"main"`. The Chat tab's session switcher (`ChatSheetContent.kt`) already demonstrates the pattern.

## 2. Per-agent TTS voice configuration

Currently TTS voice is a global setting (`messages.tts.microsoft.voice
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-56613",
  "decision": "fix_labels_or_add_asi",
  "final_labels": [
    "config",
    "sessions",
    "ui_tui"
  ],
  "asi_actions": [],
  "notes": "Low exact rate. Check whether expected labels are over-specific; otherwise add targeted ASI examples."
}
```

## openclaw-openclaw-71157 / #71157 — [Feature]: Support WhatsApp disappearing-message expiration for outbound replies

- source: `easy-final-v2-test`
- instability_rank: `15`
- pairwise_prediction_jaccard: `0.726`
- exact_rate_vs_expected: `0.250`
- avg_jaccard_vs_expected: `0.771`
- avg_symdiff_vs_expected: `0.75`
- unique_prediction_sets: `3/8`
- expected_topics: `chat_integrations, config, security`
- volatile_topics: `[['security', 4], ['notifications', 2]]`
- recurring_false_positives: `[['notifications', 2]]`
- recurring_false_negatives: `[['security', 4]]`

**Current rationales**
- `chat_integrations`: Feature is specifically for WhatsApp outbound replies and Baileys send behavior.
- `config`: Requests channel- and account-level WhatsApp disappearingMessagesSeconds configuration with override behavior.
- `security`: Core motivation is privacy retention mismatch for disappearing-message chats and policy-sensitive message persistence.

**Common predictions**
- `chat_integrations, config` × 4
- `chat_integrations, config, security` × 2
- `chat_integrations, config, notifications, security` × 2

**Per-model predictions**
- deepseek4: `[['chat_integrations', 'config', 'security'], ['chat_integrations', 'config']]`
- gpt-5.4-mini: `[['chat_integrations', 'config'], ['chat_integrations', 'config'], ['chat_integrations', 'config']]`
- sonnet: `[['chat_integrations', 'config', 'security'], ['chat_integrations', 'config', 'notifications', 'security'], ['chat_integrations', 'config', 'notifications', 'security']]`

**Review focus**

- Confirm whether the expected labels are truly easy/exact or whether one or more labels are boundary-dependent.
- False positives to address in ASI: `notifications`.
- False negatives to address in ASI: `security`.

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: issue
- Number: 71157
- URL: https://github.com/openclaw/openclaw/issues/71157
- Title: [Feature]: Support WhatsApp disappearing-message expiration for outbound replies
- State: OPEN
- Author: dougvk
- Labels: enhancement, P2, clawsweeper:fix-shape-clear, clawsweeper:queueable-fix, clawsweeper:source-repro, impact:security, issue-rating: 🦞 diamond lobster

Body:
```markdown
### Summary

Allow WhatsApp channel/account config to apply a default disappearing-message expiration to outbound OpenClaw replies.

### Problem to solve

WhatsApp supports disappearing messages, but OpenClaw’s WhatsApp outbound sends do not currently expose a reliable way to apply an expiration to agent replies. In chats where disappearing messages are expected, OpenClaw replies can persist longer than the surrounding conversation policy, creating a privacy mismatch and requiring manual cleanup.

### Proposed solution

Add WhatsApp-specific config for outbound disappearing-message expiration:

  channels.whatsapp.disappearingMessagesSeconds?: number
  channels.whatsapp.accounts.<accountId>.disappearingMessagesSeconds?: number

  Behavior:

  - Account-level setting overrides channel-level setting.
  - Positive values are passed to WhatsApp/Baileys outbound sends as ephemeralExpiration.
  - 0, null, or omitted means no explicit OpenClaw override.
  - If no config override exists, optionally honor Baileys credential default disappearing mode when available.
  - Apply consistently across WhatsApp outbound send paths: normal text, quoted replies, polls, media, and tool/channel sends.
  - Keep existing behavior unchanged unless configured or a WhatsApp a
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-71157",
  "decision": "fix_labels_or_add_asi",
  "final_labels": [
    "chat_integrations",
    "config",
    "security"
  ],
  "asi_actions": [],
  "notes": "Low exact rate. Check whether expected labels are over-specific; otherwise add targeted ASI examples."
}
```

## B. GEPA-train rows to use as ASI/boundary material

## openclaw-openclaw-43495 / #43495 — feat(tts): add <notts> tag support for visual-only content

- source: `easy-final-v2-train` GEPA candidate mining
- pairwise_prediction_jaccard: `0.340`
- exact_rate_vs_expected: `0.056`
- avg_jaccard_vs_expected: `0.346`
- avg_symdiff_vs_expected: `2.78`
- unique_prediction_sets: `29/54`
- expected_topics: `api_surface, self_hosted_inference`
- recurring_false_positives: `[['config', 33], ['gateway', 29], ['docs', 20], ['security', 18], ['sessions', 5]]`
- recurring_false_negatives: `[['api_surface', 24], ['self_hosted_inference', 14]]`

**Current rationales**
- `api_surface`: The PR defines user-facing TTS tag semantics and updates gateway/TTS payload behavior and RPC documentation around visible versus spoken text.
- `self_hosted_inference`: The main feature changes TTS preprocessing and spoken output behavior for text-to-speech content.

**Common predictions**
- `api_surface, config, docs, gateway, security, self_hosted_inference` × 6
- `api_surface, config` × 5
- `api_surface, config, gateway, security, self_hosted_inference` × 4

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: pull_request
- Number: 43495
- URL: https://github.com/openclaw/openclaw/pull/43495
- Title: feat(tts): add <notts> tag support for visual-only content
- State: OPEN
- Author: dmiv
- Labels: docs, app: macos, gateway, scripts, agents, size: L, triage: dirty-candidate, triage: needs-real-behavior-proof, mantis: telegram-visible-proof, P1, rating: 🧂 unranked krab, merge-risk: 🚨 compatibility, merge-risk: 🚨 message-delivery, merge-risk: 🚨 security-boundary, status: 📣 needs proof
- Changed file count available to wrapper: 17
- Changed files: apps/macos/Sources/OpenClaw/TalkModeRuntime.swift, docs/tts-agent-guide.md, docs/tts.md, scripts/tts-filter.sh, src/agents/pi-embedded-runner/run/params.ts, src/agents/pi-embedded-subscribe.ts, src/agents/pi-embedded-subscribe.types.ts, src/auto-reply/reply/agent-runner-execution.ts, src/config/types.tts.ts, src/config/zod-schema.core.ts, src/gateway/method-scopes.ts, src/gateway/role-policy.ts, src/media-understanding/runner.entries.ts, src/media/mime.ts, src/tts/tts-core.ts, src/tts/tts-preprocess.test.ts, src/tts/tts.ts

Body:
```markdown
## Summary

Adds `<notts>...</notts>` tag support to TTS text preprocessing, complementing the existing `<tts>...</tts>` tags.

### What it does

- **`<notts>...</notts>`**: Content is **visible** in chat but **not spoken** by TTS. Ideal for code blocks, tables, and technical details.
- **`<tts>...</tts>`** (existing): Content is **spoken** but **not visible** in chat. Ideal for alternative voice summaries.

Combined usage: wrap a table in `<notts>`, follow with a `<tts>` summary — the reader sees the table, the listener hears the summary.

### Chan
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-43495",
  "decision": "asi_only",
  "final_labels": [
    "api_surface",
    "self_hosted_inference"
  ],
  "asi_actions": [],
  "notes": "GEPA-candidate instability on train split; do not use for easy exact-match evaluation without manual adjudication."
}
```

## openclaw-openclaw-84706 / #84706 — [Bug]: subagent spawn validation rejects every non-off thinking level on all canonical openai/* models — error cites canonical alias even when openai-codex/* is requested

- source: `easy-final-v2-train` GEPA candidate mining
- pairwise_prediction_jaccard: `0.400`
- exact_rate_vs_expected: `0.019`
- avg_jaccard_vs_expected: `0.438`
- avg_symdiff_vs_expected: `3.56`
- unique_prediction_sets: `39/54`
- expected_topics: `api_surface, codex, coding_agents, config, sessions`
- recurring_false_positives: `[['acp', 29], ['agent_runtime', 15], ['model_serving', 10], ['reliability', 6], ['local_model_providers', 1]]`
- recurring_false_negatives: `[['coding_agents', 48], ['codex', 29], ['api_surface', 27], ['config', 23], ['sessions', 4]]`

**Current rationales**
- `api_surface`: The bug concerns the sessions_spawn request contract and validation/error response for the subagent API.
- `codex`: The failing route is explicitly openai-codex/* and the environment reports the OpenAI Codex runtime.
- `coding_agents`: The affected behavior is subagent creation/spawn validation inside the agent workflow.
- `config`: (no rationale captured in source row)
- `sessions`: The concrete failing entry point is sessions_spawn and related subagent session creation paths.

**Common predictions**
- `acp, api_surface, config, sessions` × 3
- `api_surface, codex, sessions` × 3
- `acp, api_surface, codex, config, sessions` × 3

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: issue
- Number: 84706
- URL: https://github.com/openclaw/openclaw/issues/84706
- Title: [Bug]: subagent spawn validation rejects every non-off thinking level on all canonical openai/* models — error cites canonical alias even when openai-codex/* is requested
- State: OPEN
- Author: aaajiao

Body:
```markdown
### Summary

On v2026.5.19, `sessions_spawn` (and any subagent-creation path) rejects every non-off thinking level for the canonical `openai/*` model namespace. The error consistently cites `openai/gpt-5.5` even when the caller specified `openai-codex/gpt-5.5` — subagent validation appears to fold `openai-codex/*` through `openai/*` alias routing before consulting the catalog, then the canonical catalog's missing reasoning metadata causes the rejection.

This is the same root cause as the picker / `/think` directive surface tracked in #84646, but a distinct surface and worth its own narrow report because it breaks the subagent API contract and is environment-affecting (not just UX).

### Environment

- OpenClaw `v2026.5.19` stable
- Channel: Telegram (also reproduces via main agent calling the `sessions_spawn` tool)
- Active agent: `main`, runtime `pi`
- Auth: `auth.order.openai = ["openai-codex:aaajiao@gmail.com"]` (OAuth, no api-key fallback)
- `/status` confirms runtime: `OpenAI Codex`

### Reproduction

A subagent spawn request:

```jsonc
sessions_spawn({
  model: "openai-codex/gpt-5.5",
  thinking: "xhigh",
  // ...prompt etc.
})
```

returns:

```
Thinking level xhigh is not supported for openai/gpt-5.5.
Use one of: off.
```

Notes from this run:

- The caller passed `openai-codex/gpt-5.5`, but the validation
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-84706",
  "decision": "asi_only",
  "final_labels": [
    "api_surface",
    "codex",
    "coding_agents",
    "config",
    "sessions"
  ],
  "asi_actions": [],
  "notes": "GEPA-candidate instability on train split; do not use for easy exact-match evaluation without manual adjudication."
}
```

## openclaw-openclaw-76724 / #76724 — [Bug]: MCP tools not discovered by Agent despite successful handshake (200 OK)

- source: `easy-final-v2-train` GEPA candidate mining
- pairwise_prediction_jaccard: `0.536`
- exact_rate_vs_expected: `0.333`
- avg_jaccard_vs_expected: `0.654`
- avg_symdiff_vs_expected: `1.00`
- unique_prediction_sets: `13/54`
- expected_topics: `mcp_tooling, ui_tui`
- recurring_false_positives: `[['config', 11], ['gateway', 10], ['reliability', 7], ['api_surface', 2], ['agent_runtime', 1]]`
- recurring_false_negatives: `[['ui_tui', 23]]`

**Current rationales**
- `mcp_tooling`: Issue is explicitly about an MCP server handshake succeeding but tools/list not being sent and MCP tools not being discovered.
- `ui_tui`: User-visible failure is in the Agent Tools/dashboard view showing 33/33 enabled and not listing the new tools after reload.

**Common predictions**
- `mcp_tooling, ui_tui` × 18
- `mcp_tooling` × 12
- `gateway, mcp_tooling` × 5

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: issue
- Number: 76724
- URL: https://github.com/openclaw/openclaw/issues/76724
- Title: [Bug]: MCP tools not discovered by Agent despite successful handshake (200 OK)
- State: OPEN
- Author: profgnpenatieri-sudo
- Labels: bug, regression, P2, clawsweeper:fix-shape-clear, clawsweeper:queueable-fix, clawsweeper:source-repro, issue-rating: 🦞 diamond lobster

Body:
```markdown
### Bug type

Regression (worked before, now fails)

### Beta release blocker

No

### Summary

 MCP Server connected (200 OK) but tools not appearing in Agent (Stuck at 33/33)

Body: Hi everyone, I'm having trouble getting my MCP tools to show up in the OpenClaw agent. Here is my setup:

Transport: SSE (Flask server on port 5000).
Handshake: Successful. I can see the initialize method hitting my server and returning 200 OK.
Config: I have manually created ~/.openclaw/workspace/config/mcporter.json with the correct URL and token.
Problem: The agent dashboard shows "33/33 enabled" and does not list the new MCP server tools. Clicking "Reload Config" or "Infrastructure > MCP > Reload" doesn't trigger a tools/list request.
Attempted: Restarted gateway, verified connection via cURL (working), and checked workspace paths.
Any idea why the Gateway initializes the connection but the Agent doesn't discover the tools?

### Steps to reproduce

1. Configure a remote MCP server using SSE transport.
2. Verify that the Gateway successfully connects to the MCP server (Server logs show 200 OK on 'initialize' method).
3. Manually verify that mcporter.json exists in ~/.openclaw/workspace/config/.
4. Open the Agent Chat and check the tool list.
5. Click "Reload Config" i
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-76724",
  "decision": "asi_only",
  "final_labels": [
    "mcp_tooling",
    "ui_tui"
  ],
  "asi_actions": [],
  "notes": "GEPA-candidate instability on train split; do not use for easy exact-match evaluation without manual adjudication."
}
```

## openclaw-openclaw-10467 / #10467 — [Feature Request]: Multi-lane concurrency support for sub-agents via sessions_spawn

- source: `easy-final-v2-train` GEPA candidate mining
- pairwise_prediction_jaccard: `0.581`
- exact_rate_vs_expected: `0.000`
- avg_jaccard_vs_expected: `0.593`
- avg_symdiff_vs_expected: `2.41`
- unique_prediction_sets: `24/54`
- expected_topics: `acp, agent_runtime, config, queueing, sessions`
- recurring_false_positives: `[['api_surface', 35], ['reliability', 11]]`
- recurring_false_negatives: `[['agent_runtime', 36], ['acp', 28], ['sessions', 14], ['config', 6]]`

**Current rationales**
- `acp`: (no rationale captured in source row)
- `agent_runtime`: (no rationale captured in source row)
- `config`: Proposal requires per-lane maxConcurrent settings in openclaw.json and schema/default compatibility.
- `queueing`: Core problem is a single subagent queue lane, lane exhaustion, concurrency limits, and independent queue lanes.
- `sessions`: The requested change is an optional lane parameter on the sessions_spawn tool and mentions session file locks.

**Common predictions**
- `api_surface, config, queueing, sessions` × 8
- `acp, api_surface, config, queueing, sessions` × 6
- `agent_runtime, api_surface, config, queueing` × 3

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: issue
- Number: 10467
- URL: https://github.com/openclaw/openclaw/issues/10467
- Title: [Feature Request]: Multi-lane concurrency support for sub-agents via sessions_spawn
- State: OPEN
- Author: lexobe
- Labels: enhancement, P2, clawsweeper:fix-shape-clear, clawsweeper:queueable-fix, clawsweeper:source-repro, impact:session-state, issue-rating: 🦞 diamond lobster

Body:
```markdown
## Summary

Currently, all sub-agents spawned via the `sessions_spawn` tool are funneled into a single global queue lane: `subagent`. The concurrency is governed by a single limit `agents.defaults.subagents.maxConcurrent`.

This creates a bottleneck and reliability risk for complex multi-agent workflows (e.g., 'Evolution Engineering' patterns) where multiple independent paths of reasoning or tool usage are required.

## Problem

1. **Lane Exhaustion**: A burst of slow 'research' sub-agents can fill the `subagent` lane, blocking high-priority 'monitoring' or 'security' sub-agents.
2. **Lock Contention**: As noted in issue #4355, concurrent sub-agents often collide on session file locks. Named lanes would allow grouping related tasks to better manage these risks.
3. **Implicit Serialization**: Agents cannot currently specify parallel 'lanes' for different logic branches, forcing a flatter, more congested execution model.

## Proposed Solution

Add an optional `lane` parameter to the `sessions_spawn` tool.

```javascript
// Example usage in an agent turn
sessions_spawn(task: "Research market trends", lane: "research")
sessions_spawn(task: "Monitor security logs", lane: "security")
```

The OpenClaw gateway should:
1. Treat these as independent q
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-10467",
  "decision": "asi_only",
  "final_labels": [
    "acp",
    "agent_runtime",
    "config",
    "queueing",
    "sessions"
  ],
  "asi_actions": [],
  "notes": "GEPA-candidate instability on train split; do not use for easy exact-match evaluation without manual adjudication."
}
```

## openclaw-openclaw-84038 / #84038 — [Bug]: doctor --fix silently migrates intentional openai-codex/ config to openai/, breaking PI+OAuth runtime and causing 3-4x token inflation

- source: `easy-final-v2-train` GEPA candidate mining
- pairwise_prediction_jaccard: `0.592`
- exact_rate_vs_expected: `0.167`
- avg_jaccard_vs_expected: `0.696`
- avg_symdiff_vs_expected: `1.37`
- unique_prediction_sets: `18/54`
- expected_topics: `agent_runtime, auth_identity, codex, config`
- recurring_false_positives: `[['reliability', 11], ['coding_agents', 8]]`
- recurring_false_negatives: `[['agent_runtime', 30], ['auth_identity', 15], ['codex', 10]]`

**Current rationales**
- `agent_runtime`: A configured `agentRuntime: { id: "pi" }` override is removed, switching users to a different runtime.
- `auth_identity`: The regression affects PI+OAuth usage and includes `auth.order` provider/account configuration.
- `codex`: The issue explicitly concerns `openai-codex/` routes and the native Codex runtime.
- `config`: The bug is about `doctor --fix` silently migrating configured model routes and removing config entries.

**Common predictions**
- `auth_identity, codex, config` × 15
- `agent_runtime, auth_identity, codex, config` × 9
- `codex, config, reliability` × 4

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: issue
- Number: 84038
- URL: https://github.com/openclaw/openclaw/issues/84038
- Title: [Bug]: doctor --fix silently migrates intentional openai-codex/ config to openai/, breaking PI+OAuth runtime and causing 3-4x token inflation
- State: OPEN
- Author: danielsan1
- Labels: bug, P1, clawsweeper:no-new-fix-pr, clawsweeper:source-repro, clawsweeper:linked-pr-open, impact:data-loss, impact:auth-provider, issue-rating: 🦞 diamond lobster

Body:
```markdown
### Bug type

Regression (worked before, now fails)

### Beta release blocker

No

### Summary

 The native Codex runtime produces 3–4× higher token usage compared to the
  OpenClaw PI runtime for the same GPT-5.x requests. This is a known upstream
  issue that OpenClaw cannot fix — but `doctor --fix` silently forces users onto
  the broken runtime by migrating intentional `openai-codex/` configs to
  `openai/`, removing the `agentRuntime: { id: "pi" }` override in the process.
  Users have no way to opt out of this migration short of manually reverting
  after every doctor run.

### Steps to reproduce

  1. Configure an explicit PI-runtime setup to avoid the broken Codex runtime:
     ```json
     {
       "agents": {
         "defaults": {
           "model": {
             "primary": "openai-codex/gpt-5.4"
           },
           "models": {
             "openai-codex/gpt-5.4": {
               "agentRuntime": { "id": "pi" }
             }
           }
         }
       },
       "auth": {
         "order": {
           "openai-codex": ["openai-codex:user@example.com"]
         }
       },
       "plugins": {
         "entries": { "codex": { "enabled": false } }
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-84038",
  "decision": "asi_only",
  "final_labels": [
    "agent_runtime",
    "auth_identity",
    "codex",
    "config"
  ],
  "asi_actions": [],
  "notes": "GEPA-candidate instability on train split; do not use for easy exact-match evaluation without manual adjudication."
}
```

## openclaw-openclaw-51667 / #51667 — Feature: Native Audio Input for Omni-Modal Models (skip STT transcription)

- source: `easy-final-v2-train` GEPA candidate mining
- pairwise_prediction_jaccard: `0.603`
- exact_rate_vs_expected: `0.093`
- avg_jaccard_vs_expected: `0.713`
- avg_symdiff_vs_expected: `1.30`
- unique_prediction_sets: `15/54`
- expected_topics: `chat_integrations, config, model_serving, sessions`
- recurring_false_positives: `[['self_hosted_inference', 17], ['security', 4], ['reliability', 1], ['api_surface', 1]]`
- recurring_false_negatives: `[['chat_integrations', 20], ['sessions', 20], ['model_serving', 6], ['config', 1]]`

**Current rationales**
- `chat_integrations`: Feature is triggered by voice notes from WhatsApp/Telegram-style channels.
- `config`: Proposes explicit tools.media.audio.native and fallbackToTranscription configuration options.
- `model_serving`: Requests routing audio as a native media part to omni-modal model endpoints instead of STT.
- `sessions`: Maintainer comment centers on transcript durability, session restore, and snapshot continuity when STT is bypassed.

**Common predictions**
- `config, model_serving, sessions` × 10
- `chat_integrations, config, model_serving, self_hosted_inference, sessions` × 10
- `chat_integrations, config, model_serving` × 8

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: issue
- Number: 51667
- URL: https://github.com/openclaw/openclaw/issues/51667
- Title: Feature: Native Audio Input for Omni-Modal Models (skip STT transcription)
- State: OPEN
- Author: jojo2a
- Labels: P2, clawsweeper:no-new-fix-pr, clawsweeper:fix-shape-clear, clawsweeper:needs-maintainer-review, clawsweeper:needs-product-decision, clawsweeper:needs-security-review, clawsweeper:source-repro, impact:session-state, impact:security, impact:auth-provider, issue-rating: 🦞 diamond lobster

Body:
```markdown
## Summary

When using omni-modal models (e.g. `mimo-v2-omni`, Gemini 3 Flash) that natively support audio input, OpenClaw should be able to send voice notes directly to the model instead of routing them through Whisper/transcription first.

## Current Behavior

- User sends a voice note (WhatsApp/Telegram/etc.)
- OpenClaw downloads the audio file
- Audio is sent to a transcription provider (Whisper, Deepgram, OpenAI transcribe)
- Transcript text is injected into the agent context
- **Result:** Tone, emotion, prosody, and multi-speaker separation are lost

## Desired Behavior

Add a configuration option (e.g. `tools.media.audio.native: true`) that, when enabled:

1. Detects the audio MIME type
2. Sends the audio data directly to the configured omni-modal model as a native media part (same way images are handled)
3. The model processes the audio natively — preserving tone, emotion, and speaker diarization

## Why This Matters

- **Latency:** No intermediate STT step = faster response
- **Richness:** Preserves emotional context, tone, prosody that transcription discards
- **Multi-speaker:** Native omni-modal models can se
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-51667",
  "decision": "asi_only",
  "final_labels": [
    "chat_integrations",
    "config",
    "model_serving",
    "sessions"
  ],
  "asi_actions": [],
  "notes": "GEPA-candidate instability on train split; do not use for easy exact-match evaluation without manual adjudication."
}
```

## openclaw-openclaw-84761 / #84761 — feat(secrets): scan backup files for plaintext provider apiKey values

- source: `easy-final-v2-train` GEPA candidate mining
- pairwise_prediction_jaccard: `0.603`
- exact_rate_vs_expected: `0.204`
- avg_jaccard_vs_expected: `0.627`
- avg_symdiff_vs_expected: `1.15`
- unique_prediction_sets: `6/54`
- expected_topics: `auth_identity, config, security`
- recurring_false_positives: `[['tests_ci', 5]]`
- recurring_false_negatives: `[['auth_identity', 34], ['config', 23]]`

**Current rationales**
- `auth_identity`: The scanned secrets are provider apiKey credentials used for authentication.
- `config`: The feature inspects backup config files such as models.json.* and openclaw.json.old in config/agent directories.
- `security`: Adds secret scanning for plaintext API keys left in backup files, closing a credential exposure gap.

**Common predictions**
- `security` × 18
- `config, security` × 15
- `auth_identity, config, security` × 11

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: pull_request
- Number: 84761
- URL: https://github.com/openclaw/openclaw/pull/84761
- Title: feat(secrets): scan backup files for plaintext provider apiKey values
- State: OPEN
- Author: jing11223344
- Labels: size: S, triage: needs-real-behavior-proof, P2, rating: 🧂 unranked krab, merge-risk: 🚨 security-boundary, merge-risk: 🚨 availability, status: 📣 needs proof
- Changed file count available to wrapper: 3
- Changed files: src/secrets/audit.test.ts, src/secrets/audit.ts, src/secrets/storage-scan.ts

Body:
```markdown
## Summary

Adds backup file secret scanning to the `openclaw secrets audit` command. This addresses a security gap identified in issue #11829 where old backup files (e.g., `models.json.20260501.bak`, `openclaw.json.old`) may retain plaintext provider API keys even after the active config is sanitized.

## Changes

- **storage-scan.ts**: New `listKnownSecretFileBackups()` function that discovers backup files in the config directory and agents directory matching patterns like `models.json.*`, `openclaw.json.*`, `*.bak`, `*.backup`, `*.old`
- **audit.ts**: New `collectBackupResidue()` function that scans backup files for plaintext `apiKey` values and reports them as `LEGACY_RESIDUE` findings
- **audit.test.ts**: 3 test cases covering:
  - Detecting plaintext apiKey in `.bak` files
  - Detecting plaintext apiKey in `.old` files  
  - Not flagging non-secret markers (env var names) in backup files

Part of #11829 - Protecting API Keys from Agent Access
```

Comments/context:
```markdown
- clawsweeper at 2026-05-21T02:06:06Z:
Codex review: needs real behavior proof before merge.

**Workflow note:** Future ClawS
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-84761",
  "decision": "asi_only",
  "final_labels": [
    "auth_identity",
    "config",
    "security"
  ],
  "asi_actions": [],
  "notes": "GEPA-candidate instability on train split; do not use for easy exact-match evaluation without manual adjudication."
}
```

## openclaw-openclaw-77345 / #77345 — google-vertex SSRF guard blocks fake-IP DNS (model.baseUrl not set for built-in providers)

- source: `easy-final-v2-train` GEPA candidate mining
- pairwise_prediction_jaccard: `0.604`
- exact_rate_vs_expected: `0.278`
- avg_jaccard_vs_expected: `0.674`
- avg_symdiff_vs_expected: `1.02`
- unique_prediction_sets: `10/54`
- expected_topics: `model_serving, security`
- recurring_false_positives: `[['config', 25], ['reliability', 14], ['local_model_providers', 2], ['self_hosted_inference', 1]]`
- recurring_false_negatives: `[['model_serving', 13]]`

**Current rationales**
- `model_serving`: Bug is in model transport/endpoint hostname handling for the built-in Google Vertex provider request URL.
- `security`: Core failure is SSRF guard behavior blocking fake-IP private/special-use DNS results and requiring a scoped security fix.

**Common predictions**
- `model_serving, security` × 15
- `config, model_serving, security` × 14
- `model_serving, reliability, security` × 9

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: issue
- Number: 77345
- URL: https://github.com/openclaw/openclaw/issues/77345
- Title: google-vertex SSRF guard blocks fake-IP DNS (model.baseUrl not set for built-in providers)
- State: OPEN
- Author: oottlee

Body:
```markdown
## Description

The 5.3 fix for Surge/Clash/sing-box fake-IP DNS (commit ref #76530, #76549) does not work for the **built-in google-vertex provider**. The SSRF guard still blocks `198.18.0.0/15` (RFC 2544 benchmarking range) addresses resolved by fake-IP DNS.

## Root Cause

In `resolveModelTransportSsrFPolicy` (`openai-transport-stream`), the fake-IP policy is only created when:

```javascript
const baseHostname = resolveHttpHostname(params.model.baseUrl);
const requestHostname = resolveHttpHostname(params.url);
const fakeIpPolicy = baseHostname && requestHostname === baseHostname 
    ? ssrfPolicyFromHttpBaseUrlFakeIpHostnameAllowlist(baseUrl) 
    : void 0;
```

The **built-in google-vertex provider** does not set `model.baseUrl` on its model objects. The actual request URL (`aiplatform.googleapis.com`) is constructed dynamically in `resolveGoogleVertexBaseOrigin()`, but `model.baseUrl` remains `undefined`.

Result: `baseHostname` is `undefined` → `fakeIpPolicy` is never created → SSRF guard uses default strict policy → blocks `198.18.0.34`.

## Steps to Reproduce

1. Configure a proxy with fake-IP DNS (Shadowrocket/Clash/Surge) on macOS
2. Set `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION=global` in env
3. Configure `jojo` agent with `model.primary: "google-vertex/gemini-3.1-pro-preview"`
4. Send a message to jojo
5. Error: `"Blocked: resolves to private/internal/special-use IP address
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-77345",
  "decision": "asi_only",
  "final_labels": [
    "model_serving",
    "security"
  ],
  "asi_actions": [],
  "notes": "GEPA-candidate instability on train split; do not use for easy exact-match evaluation without manual adjudication."
}
```

## openclaw-openclaw-71537 / #71537 — Recover archived (.reset) session transcripts in memory hook + session-logs skill

- source: `easy-final-v2-train` GEPA candidate mining
- pairwise_prediction_jaccard: `0.611`
- exact_rate_vs_expected: `0.148`
- avg_jaccard_vs_expected: `0.646`
- avg_symdiff_vs_expected: `1.72`
- unique_prediction_sets: `15/54`
- expected_topics: `memory, sessions, skills_plugins`
- recurring_false_positives: `[['hooks', 32], ['docs', 24], ['reliability', 12], ['tests_ci', 8]]`
- recurring_false_negatives: `[['skills_plugins', 15], ['sessions', 2]]`

**Current rationales**
- `memory`: Fixes the session-memory hook so reset-archived transcripts are recovered for memory summarization.
- `sessions`: Core behavior concerns session reset archives, session transcript filenames, and finding previous session logs.
- `skills_plugins`: Updates the session-logs skill guidance so it can search active and archived session transcripts.

**Common predictions**
- `hooks, memory, sessions, skills_plugins` × 11
- `memory, sessions, skills_plugins` × 8
- `docs, hooks, memory, sessions, skills_plugins, tests_ci` × 7

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: pull_request
- Number: 71537
- URL: https://github.com/openclaw/openclaw/pull/71537
- Title: Recover archived (.reset) session transcripts in memory hook + session-logs skill
- State: OPEN
- Author: injinj
- Labels: size: S, triage: needs-real-behavior-proof, P2, rating: 🧂 unranked krab, merge-risk: 🚨 session-state, status: 📣 needs proof
- Changed file count available to wrapper: 4
- Changed files: pnpm-lock.yaml, skills/session-logs/SKILL.md, src/hooks/bundled/session-memory/handler.test.ts, src/hooks/bundled/session-memory/transcript.ts

Body:
```markdown
## Summary

When a session is reset (`/new` or `/reset`), the gateway renames its
`<id>.jsonl` transcript to `<id>.jsonl.reset.<timestamp>Z`. After that
rename, two surfaces silently lose the conversation:

1. **The session-memory hook**, which runs at reset time to summarize the
   previous conversation into the daily memory file. It only ever looked
   at live `.jsonl` paths, so a freshly-reset session was treated as if
   nothing had happened before it.
2. **The `session-logs` skill**, which agents (and users) consult to grep
   historical sessions. Every example used a `*.jsonl` glob and quietly
   skipped both `.reset.*Z` and `.deleted.*Z` archives.

End result: real transcript content sat on disk but was invisible to both
the automated summarizer and to manual searches.

This branch fixes both halves so archives stop being a black hole.

## Changes

### 1. `fix(session-memory): recover archived reset transcripts`

`src/hooks/bundled/session-memory/transcript.ts`

- `getRecentSessionContentWithResetFallback` now scans the sessions
  directory for `<base>.reset.<
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-71537",
  "decision": "asi_only",
  "final_labels": [
    "memory",
    "sessions",
    "skills_plugins"
  ],
  "asi_actions": [],
  "notes": "GEPA-candidate instability on train split; do not use for easy exact-match evaluation without manual adjudication."
}
```

## openclaw-openclaw-55888 / #55888 — [Feature]: 🚀 [Performance Insight] Unlocking 26.7k Context Window on M4 Pro: Fixing the 8k Compaction Lag (64GB RAM Only)

- source: `easy-final-v2-train` GEPA candidate mining
- pairwise_prediction_jaccard: `0.613`
- exact_rate_vs_expected: `0.352`
- avg_jaccard_vs_expected: `0.719`
- avg_symdiff_vs_expected: `1.04`
- unique_prediction_sets: `11/54`
- expected_topics: `config, local_models, memory`
- recurring_false_positives: `[['sessions', 10], ['agent_runtime', 6], ['open_weight_models', 5]]`
- recurring_false_negatives: `[['memory', 27], ['local_models', 8]]`

**Current rationales**
- `config`: The proposed fix is an openclaw.json agents.defaults.compaction configuration override and discusses config hierarchy/defaults.
- `local_models`: The report centers on a local Ollama Qwen model running on M4 Pro hardware with RAM/context-window constraints.
- `memory`: It specifically targets memoryFlush, compaction, summarization thresholds, and retained context behavior.

**Common predictions**
- `config, local_models, memory` × 19
- `config, local_models` × 12
- `agent_runtime, config, local_models` × 5

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: issue
- Number: 55888
- URL: https://github.com/openclaw/openclaw/issues/55888
- Title: [Feature]: 🚀 [Performance Insight] Unlocking 26.7k Context Window on M4 Pro: Fixing the 8k Compaction Lag (64GB RAM Only)
- State: OPEN
- Author: Vic-HA
- Labels: enhancement, P3, clawsweeper:fix-shape-clear, clawsweeper:queueable-fix, clawsweeper:source-repro, impact:session-state, issue-rating: 🦞 diamond lobster

Body:
```markdown
### Summary

Optimization report for OpenClaw 2026.3.24 (cff6dc9) on Mac Mini M4 Pro (64GB RAM). Identified a hidden ~4k token system buffer in the memoryFlush logic that causes unnecessary background compaction (20-30s latency) at only 8k tokens. Successfully increased usable context to 26.7k tokens with <1,000ms latency.

Target Model Details:

Model: ollama/qwen2.5-coder:7b (High-performance coding model)

Quantization: Q4_K_M (Standard Ollama default)

Native Context Window: 32,768 tokens

Actual Performance: On M4 Pro 64GB, this model is capable of near-instant inference, but was throttled by OpenClaw's 8k compaction threshold.

### Problem to solve

Default compaction thresholds are too conservative for 64GB RAM machines, triggering frequent summarization loops that ignore the hardware's unified memory capacity.

The Discovery (Triple-Deduction Formula):
Through black-box testing, I've decoded the internal Threshold calculation:
Actual Threshold = ContextWindow (32768) - reserveTokensFloor - SystemBuffer (~4000).
This fixed 4k buffer prevents high-spec users from reaching the physical limit unless they understand this specific offset.

### Proposed solution

Crucial: The configuration MUST start wit
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-55888",
  "decision": "asi_only",
  "final_labels": [
    "config",
    "local_models",
    "memory"
  ],
  "asi_actions": [],
  "notes": "GEPA-candidate instability on train split; do not use for easy exact-match evaluation without manual adjudication."
}
```

## openclaw-openclaw-58135 / #58135 — [Feature]: expose promptMode parameter in sessions_spawn for deterministic blank sub-agents

- source: `easy-final-v2-train` GEPA candidate mining
- pairwise_prediction_jaccard: `0.614`
- exact_rate_vs_expected: `0.222`
- avg_jaccard_vs_expected: `0.719`
- avg_symdiff_vs_expected: `1.17`
- unique_prediction_sets: `13/54`
- expected_topics: `acp, agent_runtime, api_surface, sessions`
- recurring_false_positives: `[['config', 6]]`
- recurring_false_negatives: `[['acp', 24], ['agent_runtime', 22], ['api_surface', 9], ['sessions', 2]]`

**Current rationales**
- `acp`: The requested change is to the sessions_spawn ACP-style session tool parameter set.
- `agent_runtime`: (no rationale captured in source row)
- `api_surface`: It asks to add an optional promptMode parameter to the spawn handler schema and request contract.
- `sessions`: It concerns child session/sub-agent spawning behavior and inherited session prompt state.

**Common predictions**
- `acp, agent_runtime, api_surface, sessions` × 12
- `api_surface, sessions` × 10
- `acp, api_surface, sessions` × 10

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: issue
- Number: 58135
- URL: https://github.com/openclaw/openclaw/issues/58135
- Title: [Feature]: expose promptMode parameter in sessions_spawn for deterministic blank sub-agents
- State: OPEN
- Author: esteban-dozsa
- Labels: enhancement, P2, clawsweeper:no-new-fix-pr, clawsweeper:fix-shape-clear, clawsweeper:needs-maintainer-review, clawsweeper:needs-product-decision, clawsweeper:source-repro, impact:session-state, issue-rating: 🦞 diamond lobster

Body:
```markdown
### Summary

When spawning sub-agents via sessions_spawn, there is no way to control the promptMode used for the child agent run. Sub-agents always default to minimal prompt mode, which injects AGENTS.md and TOOLS.md into the system prompt.

### Problem to solve

The PromptMode `none` mode is exactly what's needed for deterministic blank sub-agents — specialist workers that run with no inherited persona, no memory, and no workspace context. This is critical for use cases like:

• Contract review against a fixed playbook (no ambient context leaking in)
• Document analysis with strictly controlled input/output
• Any workflow where reproducibility requires eliminating inherited state


### Proposed solution

### The OpenClaw codebase already supports three prompt modes internally (system-prompt.ts):

• full — all sections (default for main sessions)
• minimal — omits Skills, Memory Recall, Self-Update, Reply Tags, Heartbeats (default for sub-agents)
• none — returns only the base identity line, no workspace files injected

Add promptMode as an optional parameter to sessions_spawn:
```
// In the spawn handler parameter schema, add:
promptMode?: "full" | "minim
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-58135",
  "decision": "asi_only",
  "final_labels": [
    "acp",
    "agent_runtime",
    "api_surface",
    "sessions"
  ],
  "asi_actions": [],
  "notes": "GEPA-candidate instability on train split; do not use for easy exact-match evaluation without manual adjudication."
}
```

## openclaw-openclaw-68725 / #68725 — feat(amazon-bedrock-mantle): add known context windows for open-weight Mantle models

- source: `easy-final-v2-train` GEPA candidate mining
- pairwise_prediction_jaccard: `0.622`
- exact_rate_vs_expected: `0.574`
- avg_jaccard_vs_expected: `0.744`
- avg_symdiff_vs_expected: `0.76`
- unique_prediction_sets: `9/54`
- expected_topics: `config, open_weight_models`
- recurring_false_positives: `[['model_serving', 16], ['local_model_providers', 4], ['reliability', 1]]`
- recurring_false_negatives: `[['config', 18], ['open_weight_models', 2]]`

**Current rationales**
- `config`: (no rationale captured in source row)
- `open_weight_models`: The lookup is explicitly for open-weight model families such as Qwen, DeepSeek, GLM, Nemotron, and MiniMax.

**Common predictions**
- `config, open_weight_models` × 31
- `model_serving, open_weight_models` × 11
- `open_weight_models` × 4

**Excerpt**

```markdown
GitHub item:
- Repository: openclaw/openclaw
- Type: pull_request
- Number: 68725
- URL: https://github.com/openclaw/openclaw/pull/68725
- Title: feat(amazon-bedrock-mantle): add known context windows for open-weight Mantle models
- State: OPEN
- Author: wirjo
- Labels: size: S, triage: needs-real-behavior-proof, P2, rating: 🧂 unranked krab, merge-risk: 🚨 compatibility, status: 📣 needs proof

Body:
```markdown
# feat(amazon-bedrock-mantle): add known context windows for open-weight Mantle models

## Problem

Mantle's `/v1/models` endpoint returns only model IDs — no token limit metadata. Discovery hardcodes `contextWindow: 32000` for every model, which is wrong for most:

- MiniMax M2/M2.1: **1,000,000** (gets 32K)
- Qwen3 Coder: **256,000** (gets 32K)
- DeepSeek V3.x, GLM 4.x, Nemotron: **128,000** (gets 32K)

This causes the same premature context overflow and wrong compaction thresholds as #65952 (the amazon-bedrock equivalent).

## Fix

Add a `KNOWN_CONTEXT_WINDOWS` lookup table for open-weight models currently available on Mantle. Raise the default fallback from 32K → 128K for unknown models.

```
MiniMax M2 / M2.1              → 1,000,000
Qwen3 Coder (480B/Next/30B)    → 256,000
Qwen3 235B / 32B               → 128,000
DeepSeek V3.1 / V3.2           → 128,000
GLM 4.6 / 4.7 / 4.7 Flash      → 128,000
NVIDIA Nemotron (all variants)  → 128,000
```

**Claude models are intentionally excluded** — they use a separate Anthropic-native endpoint on Mantle (`/anthropic/v1/messages`), not the OpenAI-compatible `/v1/chat/completions` endpoint that this extension handles. Claude model metadata is managed by the `amazon-bedrock` extension (#65952).

## Changes

| File | Change |
...
```

**Decision**

```json
{
  "id": "openclaw-openclaw-68725",
  "decision": "asi_only",
  "final_labels": [
    "config",
    "open_weight_models"
  ],
  "asi_actions": [],
  "notes": "GEPA-candidate instability on train split; do not use for easy exact-match evaluation without manual adjudication."
}
```

## C. ASI update checklist

- **coding_agents / codex / agent_runtime / acp**: Rows 83863, 84706, 10467, 84038. Add examples separating external coding-agent products from internal OpenClaw orchestration and ACP protocol lifecycle.
- **model_releases under-prediction**: Row 87277. Adding/updating named model catalog entries should trigger model_releases even when config/model_serving are also present.
- **open_weight_models over-prediction**: Rows 87277, 74204. Do not add open_weight_models from mere model-family mentions; require central open-weight behavior/support/benchmarking.
- **skills_plugins inconsistency**: Rows 70518, 85660, 71537. Require real skill/plugin product surface: manifests/loading/allowlists/hooks/plugin-owned behavior.
- **reliability over-prediction**: Rows 70002, 84697, 77345. Do not add reliability for any cryptic error/CI safety; require robustness/recovery/crash/timeout/data-loss/stale-state behavior.
- **local/self-hosted/provider boundaries**: Rows 74204, 84697, 55888, 51667. Separate local_models, local_model_providers, self_hosted_inference with concrete examples.
- **docs/config/tooling boundaries**: Rows 72085, 75043. Documentation of config option bounds is docs+config, not necessarily exec_tools/gateway.
