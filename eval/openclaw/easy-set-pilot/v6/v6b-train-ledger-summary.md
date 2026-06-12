# V6b Train-Quality Ledger

This artifact is for sharing and early investigation. It does not change the adjudicated v6b set.

## Gates

- Benchmark/adjudicated rows require GPT 3/3 exact stability, Opus 2/2 exact stability, matching modal label sets, and no teacher validity flags.
- Strict benchmark-quality rows additionally require every teacher run to have confidence >= 0.90 and low ambiguity.
- Train-only rows require GPT 3/3 exact stability and an Opus modal set matching GPT. Opus may wobble across its two repeats.
- Deferred rows with GPT/Opus modal disagreement, invalid labels, over-cardinality, failed runs, or human-review flags are excluded.

## Counts

- Attempted rows: 260
- Existing accepted consensus rows: 71
- Strict benchmark-quality rows: 30
- Train-quality rows total: 78
- Additional train-only soft-modal rows: 7

## Additional Train-Only Rows

### openclaw-openclaw-41892

- Batch: `batch-001`
- Title: feat(control-ui): add cron calendar timeline view
- GitHub: https://github.com/openclaw/openclaw/pull/41892
- Labels: `cron_automation`, `ui_tui`
- Review reasons retained for provenance: `['opus_unstable']`

### openclaw-openclaw-82145

- Batch: `batch-001`
- Title: cron: allow retries for local model preflight
- GitHub: https://github.com/openclaw/openclaw/pull/82145
- Labels: `config`, `cron_automation`, `reliability`, `self_hosted_inference`
- Review reasons retained for provenance: `['opus_unstable']`

### openclaw-openclaw-84732

- Batch: `batch-001`
- Title: Slack channel sends fail: `reconcileUnknownSend` required but no channel adapter implements it
- GitHub: https://github.com/openclaw/openclaw/issues/84732
- Labels: `chat_integrations`, `notifications`, `reliability`
- Review reasons retained for provenance: `['opus_unstable']`

### openclaw-openclaw-46949

- Batch: `batch-003`
- Title: fix(acp): release dormant oneshot runtimes under pressure
- GitHub: https://github.com/openclaw/openclaw/pull/46949
- Labels: `acp`, `reliability`, `sessions`
- Review reasons retained for provenance: `['opus_unstable']`

### openclaw-openclaw-55723

- Batch: `batch-003`
- Title: fix(agents): preserve ACP requester agent overrides
- GitHub: https://github.com/openclaw/openclaw/pull/55723
- Labels: `acp`
- Review reasons retained for provenance: `['opus_unstable']`

### openclaw-openclaw-69669

- Batch: `batch-003`
- Title: ACP: keep thread-bound follow-ups parent-orchestrated by default, not raw pass-through
- GitHub: https://github.com/openclaw/openclaw/issues/69669
- Labels: `acp`, `sessions`
- Review reasons retained for provenance: `['opus_unstable']`

### openclaw-openclaw-83030

- Batch: `batch-003`
- Title: feat(image-generation): Add ReCraft V4.1 model family support (Standard, Utility, Vector) via OpenRouter
- GitHub: https://github.com/openclaw/openclaw/issues/83030
- Labels: `api_surface`, `inference_api`, `model_lifecycle`
- Review reasons retained for provenance: `['opus_unstable']`
