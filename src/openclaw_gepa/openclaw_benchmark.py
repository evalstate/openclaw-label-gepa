from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REF = ROOT / "reference" / "openclaw-classification-dataset"
SOURCE = REF / "ds4.jsonl"
EVAL = ROOT / "eval" / "openclaw"
ENV_DIR = ROOT / ".fast-agent"
CARD = ENV_DIR / "agent-cards" / "openclaw-classifier.md"
SCHEMA = EVAL / "output.schema.json"
TASK_TEMPLATE = EVAL / "task-template.md"
SMOKE_TEMPLATE = EVAL / "smoke-template.md"
TOPIC_BOUNDARY_GUIDANCE = EVAL / "topic-boundary-guidance.md"
STATIC_LABELING_GUIDANCE = EVAL / "static-labeling-guidance.md"
VALIDATION_FEEDBACK = EVAL / "validation-feedback-policyaware-asi-v2.md"
LABEL_RATIONALE_GUIDANCE = EVAL / "label-rationales" / "gepa-ready-guidance.md"
ASI_PACK = EVAL / "asi-pack-v4.md"
ALLOWED_TOPICS = EVAL / "allowed-topics.md"

TOPIC_HINTS: dict[str, dict[str, str]] = {
    "api_surface": {
        "fp": "Tighten api_surface: require public API, CLI/API contract, HTTP contract, request/response shape, or compatibility contract. Exclude internal helpers, payload parsing, status text, UI events, ordinary commands, and local model compatibility.",
        "fn": "Add api_surface when a public API, CLI/API contract, HTTP request/response shape, schema, or compatibility contract is central.",
    },
    "coding_agent_integrations": {
        "fp": "Tighten coding_agent_integrations: require an external coding-agent backend/run such as Codex, Claude Code, Gemini CLI/coding agents, Pi, or coding-agent harness/tools/approvals. Do not use for internal OpenClaw subagent/session/queue/lock orchestration; prefer agent_runtime/sessions/queueing.",
        "fn": "Improve coding_agent_integrations recall: add when Codex, Claude Code, Gemini CLI/coding agents, Pi, external coding-agent harnesses, coding-agent approvals/sandboxing/tools, or provider behavior breaking an external coding-agent turn is central.",
    },
    "local_model_providers": {
        "fp": "Tighten local_model_providers: require local, self-hosted, or user-configured OpenAI-compatible provider setup/routing/auth/discovery/compatibility. Do not use for ordinary hosted cloud providers such as Vertex/Azure/Bedrock/Anthropic/DeepInfra/OpenRouter, local lifecycle knobs, model serving endpoint behavior, hosted catalogs, or generic local model mentions.",
        "fn": "Add local_model_providers when local/self-hosted/user-configured OpenAI-compatible provider setup, auth, discovery, routing, model resolution, or adapter compatibility is central.",
    },
    "config": {
        "fp": "Tighten config: do not add merely because an option, payload field, or example exists. Use only for config schema, persisted config, setup options, defaults, validation, or config read/write policy.",
        "fn": "Add config when setup options, defaults, validation, persisted config, config schema, or config read/write policy are central.",
    },
    "reliability": {
        "fp": "Tighten reliability: do not use as a generic bug tag. Require timeout, crash, hang, retry, stuck state, data loss, cleanup, lifecycle recovery, fallback loop, or leak evidence.",
        "fn": "Add reliability for crashes, hangs, timeouts, data loss, retries, fallback/recovery, stale state, cleanup, stuck lifecycle, or operational failure behavior.",
    },
    "sessions": {
        "fp": "Tighten sessions: require session lifecycle/state/storage/identity boundaries; do not use for every mention of session context or files.",
        "fn": "Add sessions when session lifecycle, state, persistence, identity, isolation, resume, or storage behavior is central.",
    },
    "model_serving": {
        "fp": "Tighten model_serving only when endpoint/protocol/model-serving behavior is central. Do not use for pure config metadata with no serving behavior, or local provider setup without endpoint compatibility.",
        "fn": "Add model_serving for hosted or local model endpoint behavior: Responses/Chat Completions, streaming/SSE, model registration/selection, endpoint lifecycle, serving metadata, request routing, or provider endpoint compatibility.",
    },
    "skills_plugins": {
        "fp": "Tighten skills_plugins: require a real skill/plugin surface such as plugin manifests/loading/registration, plugin SDK/runtime APIs, skill files/prelude/sync/wrappers, hooks, SecretRefs, MCP Apps, or plugin-owned user-visible behavior. Do not add just because an extension package or review skill is mentioned.",
        "fn": "Add skills_plugins for SKILL.md/managed skills, plugin manifests/loading/registration, plugin SDK/runtime APIs, plugin hooks, SecretRefs, skill sync/prelude/wrappers, MCP Apps, or plugin-owned tools/resources/UI.",
    },
    "chat_integrations": {
        "fp": "Tighten chat_integrations: require a named chat surface or user-facing chat integration behavior, not generic message delivery/recovery.",
        "fn": "Add chat_integrations for named Discord, Telegram, Slack, Zulip, Feishu, Matrix, webchat, or similar integration behavior.",
    },
    "tool_calling": {
        "fp": "Tighten tool_calling: require tool-call semantics/transcript/result handling; exclude generic command output, TTS, browser screenshot/vision, or config-like options.",
        "fn": "Add tool_calling for structured tool result display, stdout rendering for tool results, pre-tool text preservation, or tool-call transcript/content semantics.",
    },
    "gateway": {
        "fp": "Tighten gateway: require decisive gateway ownership: routing, state, startup/restart, protocol, service health, gateway-owned execution, or gateway-owned lifecycle. Exclude code that merely runs through the gateway, ordinary provider proxy, HTTP compatibility, browser command, or app-runtime bugs.",
        "fn": "Add gateway when gateway routing, state, startup/restart, protocol, service health, gateway-owned execution, or gateway-owned lifecycle is central.",
    },
    "exec_tools": {
        "fp": "Tighten exec_tools: require shell/PTY command execution, subprocess lifecycle, command approval/allowlist, browser command launch, TTS/speech execution, or execution output handling. Exclude API/tool schema semantics.",
        "fn": "Add exec_tools when shell/PTY commands, subprocesses, browser command launch, sidecar execution, command approval/allowlist, or execution output handling is central.",
    },
    "agent_runtime": {
        "fp": "Tighten agent_runtime: require core agent turn/runtime/planning/execution lifecycle behavior, not any agent-adjacent provider, UI, or config change.",
        "fn": "Add agent_runtime when the core agent turn lifecycle, runtime plan, harness execution path, agent state machine, or embedded runner behavior is central.",
    },
    "telemetry_usage": {
        "fp": "Tighten telemetry_usage: require usage/count/token/cost/metric/log/trace/quota/status diagnostics. Exclude generic reliability or UI text without measurement/status data.",
        "fn": "Add telemetry_usage for token/usage/cost counters, diagnostics, metrics, traces, usage chunks, quota/status reporting, or run logs.",
    },
    "notifications": {
        "fp": "Tighten notifications: require an outbound delivery path, sent-message handling, completion/notification delivery gate, notify setting, or announcement behavior to be implemented or changed. Exclude chat-only behavior, reliability-only recovery, generic message text, and events/hooks about sends.",
        "fn": "Add notifications when outbound delivery paths, sent-message handling, completion/notification delivery gates, notify settings, announcements, or generic notification delivery behavior are central.",
    },
    "browser_automation": {
        "fp": "Tighten browser_automation: require browser launch/control/CDP/Chrome/Playwright/screenshot/extension/proxy behavior, not generic UI or web API behavior.",
        "fn": "Add browser_automation for browser command launch, Chrome/DevTools/CDP, Playwright, screenshots, webview automation, browser profile/proxy/extension, or browser sidecars.",
    },
    "tests_ci": {
        "fp": "Tighten tests_ci: require tests, CI workflow, coverage, flake handling, lint/typecheck, or validation tooling as a central subject. Do not add only because a PR includes tests.",
        "fn": "Add tests_ci when test coverage, CI behavior, flakiness, validation scripts, lint/typecheck, or regression guardrails are central to the item.",
    },
    "ui_tui": {
        "fp": "Tighten ui_tui: require user-facing display/help/status/wizard/TUI/visual state. Exclude ordinary command internals, telemetry fields, or API behavior not shown to users.",
        "fn": "Add ui_tui for visible CLI/TUI/web UI output, help/status displays, user-facing settings screens, wizards, progress indicators, or presentation changes.",
    },
    "auth_identity": {
        "fp": "Tighten auth_identity: require auth profile, token, credential, identity, permission, or account boundary. Exclude generic provider config or security wording without identity/auth mechanics.",
        "fn": "Add auth_identity for auth profiles, tokens, credentials, account identity, permission checks, login/session identity, or auth-bound routing.",
    },
    "self_hosted_inference": {
        "fp": "Tighten self_hosted_inference: require self-operated or local inference behavior: vLLM, llama.cpp, Ollama, LM Studio, TGI, LocalAI, GGUF/quantization, local hardware/VRAM, model-family quirks, local fallback/context/UX, embeddings, speech, or memory providers. Exclude ordinary hosted cloud providers, generic provider config, or endpoint protocol behavior better covered by inference_api.",
        "fn": "Add self_hosted_inference when self-hosted/local inference backends, private/local inference servers, GGUF/quantization, local hardware/VRAM/cold-start, local model fallback/context/UX, self-hosted embeddings/speech/memory providers, proxy bypass for private inference, or operator-run inference services are central.",
    },
    "open_weight_models": {
        "fp": "Tighten open_weight_models: require open-weight model families, weights, quantization, context metadata for open-weight families, packaging/deployability, or hosted catalogs of open-weight models. Do not add merely because a provider serves a named model.",
        "fn": "Add open_weight_models when named open-weight families, model weights, GGUF/quantization, context windows for open-weight models, model cards/checkpoints, or open-weight catalog metadata are central.",
    },
    "model_releases": {
        "fp": "Tighten model_releases: require new, renamed, deprecated, or version-specific model availability, provider catalog updates, release metadata, or release tracking. Do not add merely because a model name appears.",
        "fn": "Add model_releases when adding/removing/updating model IDs, provider catalogs, release notes, model-family availability, version-specific model support, or deprecation/rename behavior is central.",
    },
    "acp": {
        "fp": "Tighten acp: require ACP protocol/runtime/session binding/delivery semantics. With acpx, add acp only when ACP binding, override, parent/child session, or delivery semantics are named as behavior being changed. Do not add merely because an item mentions an agent session or internal runtime behavior.",
        "fn": "Add acp when ACP protocol, ACP session tools, ACP binding/override, ACP parent/child delivery, ACP blocks, acp_send, sessions_spawn/cancel, or ACP client/server compatibility is central.",
    },
    "acpx": {
        "fp": "Tighten acpx: require ACPX-specific runtime, proxy, backend, worker, transport, configured binding, command, auth, or compatibility behavior. Do not use for generic ACP issues.",
        "fn": "Add acpx when files, commands, runtime paths, worker/proxy behavior, transport, configured binding, HMAC/auth, or compatibility are explicitly ACPX-specific.",
    },
    "codex": {
        "fp": "Tighten codex: require the Codex runtime, Codex CLI, Codex ACP, Codex auth, Codex command compatibility, or Codex harness behavior. Do not add merely because a coding-agent-like workflow is discussed.",
        "fn": "Add codex when Codex-specific runtime behavior, auth, ACP integration, command execution, plugin behavior, or harness compatibility is central.",
    },
    "mcp_tooling": {
        "fp": "Tighten mcp_tooling: require MCP server/client behavior, MCP config, tool/resource/prompt listing, tool invocation, handshake, routing, allow/deny policy, or MCP conformance. Do not add merely because MCP appears in examples or incidental config.",
        "fn": "Add mcp_tooling for MCP servers/clients, tools/list, resources/list, prompts/list, MCP tool routing, MCP config, MCP allow/deny rules, MCP conformance checks, or MCP invocation compatibility.",
    },
    "approvals": {
        "fp": "Tighten approvals: require approval prompts, approve/deny decisions, permission modes, pending approval state, approval policy checks, or approval UI/commands. Do not add merely because a command or tool might require permission.",
        "fn": "Add approvals when permission decisions, approval mode behavior, approve/reject flow, approval queues/state, exec approvals, or tool allow/deny decisions are central.",
    },
    "sandboxing": {
        "fp": "Tighten sandboxing: require containment or isolation behavior such as sandbox policy, inherited sandbox state, filesystem/process/container boundaries, sandbox escape, volumes, or runtime isolation. Do not add merely because command execution or security is mentioned.",
        "fn": "Add sandboxing when sandbox inheritance, sandbox escape/prevention, path isolation, containers, filesystem hiding, process limits, Docker/bubblewrap, or workspace boundary behavior is central.",
    },
    "hooks": {
        "fp": "Tighten hooks: require hook registration, lifecycle, trigger filtering, priority/order, payload shape, hook execution, hook security, or managed hook behavior. Do not add for generic plugin behavior unless hook mechanics are the owner surface.",
        "fn": "Add hooks when before/after lifecycle events, hook priority, hook ingress, hook payload validation, hook execution policy, managed hooks, or hook security are central.",
    },
    "cron_automation": {
        "fp": "Tighten cron_automation: require scheduled, recurring, or one-shot automation, cron jobs, force-run behavior, or job lifecycle. Do not add merely because an agent/runtime heartbeat is mentioned.",
        "fn": "Add cron_automation when cron jobs, scheduled runs, recurring task execution, force-run, deleteAfterRun, at-jobs, heartbeat automation jobs, or scheduler behavior is central.",
    },
    "memory": {
        "fp": "Tighten memory: require memory systems such as indexing, recall, active memory, embeddings/vector stores, memory provider state, archival, or recovery. Do not add merely for context window, session state, transcript, or generic remembering.",
        "fn": "Add memory when memory indexing/search, active-memory recall, embeddings, vector/LanceDB storage, memory provider config/state, archive/recovery, or memory hook behavior is central.",
    },
    "security": {
        "fp": "Tighten security: require a concrete security issue, improvement, or direct security feature such as SSRF/private-network access, credential/secret/token exposure or hardening, auth or permission boundary changes, access-control enforcement, sandbox escape/isolation hardening, vulnerability mitigation, supply-chain hardening, or signature/HMAC/verification behavior. Do not add for privacy-focused features, disappearing messages, retention/visibility preferences, generic privacy UX, or ordinary auth/profile configuration unless a security control changes.",
        "fn": "Add security when SSRF, private/internal network access, credential/secret/token exposure or hardening, HMAC/signature/verification behavior, unsafe permissions, sandbox escape/isolation hardening, vulnerability mitigation, supply-chain hardening, or access-control enforcement is central.",
    },
    "queueing": {
        "fp": "Tighten queueing: require queues, lanes, locks, pending/running state, scheduling, ordering, dispatch, backpressure, or stuck work queues. Do not add for any async/background task unless queue mechanics are the owner boundary.",
        "fn": "Add queueing when task queues, lanes, follow-up queues, run ordering, work dispatch, locks, pending/running state, backpressure, or stuck queue behavior is central.",
    },
    "docs": {
        "fp": "Tighten docs: require documentation, guides, README/reference text, spelling, taxonomy wording, or explanatory content to be the central subject. Do not add merely because docs are updated alongside implementation.",
        "fn": "Add docs when the item's main subject is documentation, examples/guides as docs, README/reference changes, explanatory text, taxonomy wording, or doc-only corrections.",
    },
    "packaging_deployment": {
        "fp": "Tighten packaging_deployment: require packaging, installers, release artifacts, Docker images, service managers, build distribution, dependency packaging, or deployment/runtime distribution. Do not add for ordinary runtime config.",
        "fn": "Add packaging_deployment when build/package/release artifacts, Docker images, SEA/single executable, systemd/launchd service files, installer behavior, dependency packaging, or deployment paths are central.",
    },
}


@dataclass(frozen=True)
class PreparedRow:
    id: str
    expected_topics: list[str]
    keywords: list[str]
    title: str
    data: dict[str, Any]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run the OpenClaw topic-routing benchmark with fast-agent.")
    p.add_argument("--model", default="passthrough", help="fast-agent model override; passthrough is smoke-only.")
    p.add_argument("--input", type=Path, default=EVAL / "benchmark.jsonl")
    p.add_argument("--source", type=Path, default=SOURCE)
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--sample", type=int, default=None, help="Deterministic sample size from source.")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--run-name", default=None)
    p.add_argument("--output-dir", type=Path, default=ROOT / "runs" / "openclaw")
    p.add_argument("--parallel", type=int, default=4)
    p.add_argument("--fast-agent-bin", default="fast-agent")
    p.add_argument("--agent-card", type=Path, default=CARD, help="AgentCard to benchmark.")
    p.add_argument("--policy", type=Path, default=None, help="Policy file to render into a temporary benchmark AgentCard.")
    p.add_argument("--plain-labels", action="store_true", help="Ask for comma-separated labels instead of structured JSON.")
    p.add_argument("--prepare-only", action="store_true")
    p.add_argument("--score-only", type=Path, default=None, help="Score an existing fast-agent output JSONL.")
    p.add_argument("--no-prepare", action="store_true", help="Use existing --input file.")
    return p.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def truncate(text: str, max_chars: int, label: str) -> str:
    text = text or ""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"\n\n[{label} truncated after {max_chars} chars]"


def neutralize_control_tags(text: str) -> str:
    return (
        str(text or "")
        .replace("<system", "< system")
        .replace("</system", "</ system")
        .replace("<developer", "< developer")
        .replace("</developer", "</ developer")
    )


def comments_text(comments: list[dict[str, Any]]) -> str:
    parts = []
    for c in comments:
        author = c.get("author") or "unknown"
        created = f" at {c.get('created_at')}" if c.get("created_at") else ""
        parts.append(f"- {author}{created}:\n{c.get('body') or ''}")
    return "\n\n".join(parts)


def selected_diff(diff: str, max_chars: int = 5000) -> str:
    diff = diff or ""
    if len(diff) <= max_chars:
        return diff
    keywords = [
        "localpager-agent", "local model", "local-model", "lm studio", "lmstudio", "vllm", "ollama",
        "llama.cpp", "gemma", "gitcrawl", "classifier", "topics_of_interest", "final_json",
        "final-schema", "mcp", "acp", "acpx", "codex", "huggingface", "hf", "hub workflow",
        "model serving", "open weight", "self-hosted", "post training", "memory", "security",
        "gateway", "session",
    ]
    picked: list[str] = []
    for line in diff.splitlines():
        lower = line.lower()
        if line.startswith(("diff --git", "+++", "---", "@@")) or any(k in lower for k in keywords):
            picked.append(line)
        if len("\n".join(picked)) >= max_chars:
            break
    text = "\n".join(picked)[:max_chars]
    return text + f"\n\n[diff selected/truncated after {max_chars} chars]"


def github_context(row: dict[str, Any]) -> str:
    labels = neutralize_control_tags(", ".join(row.get("labels") or []))
    changed = truncate(neutralize_control_tags(", ".join(row.get("changed_files") or [])), 2000, "changed files")
    context_caveats = ", ".join(row.get("context_caveats") or [])
    body = truncate(neutralize_control_tags(row.get("body") or ""), 2500, "body")
    ctext = truncate(neutralize_control_tags(comments_text(row.get("comments") or [])), 1500, "comments/context")
    diff = selected_diff(neutralize_control_tags(row.get("diff") or ""), 5000)
    parts = [
        f"GitHub item:",
        f"- Repository: {row.get('repo')}",
        f"- Type: {'pull_request' if row.get('item_type') == 'github_pr' else 'issue'}",
        f"- Number: {row.get('number')}",
        f"- URL: {row.get('url')}",
        f"- Title: {neutralize_control_tags(row.get('title') or '')}",
        f"- State: {row.get('state')}",
        f"- Author: {row.get('author')}",
    ]
    if labels:
        parts.append(f"- Labels: {labels}")
    if row.get("changed_file_count"):
        parts.append(f"- Changed file count available to wrapper: {row.get('changed_file_count')}")
    if changed:
        parts.append(f"- Changed files: {changed}")
    if context_caveats:
        parts.append(f"- Context caveats: {context_caveats}")
    parts.extend([
        "",
        "Body:",
        "```markdown",
        body,
        "```",
    ])
    if ctext:
        parts.extend(["", "Comments/context:", "```markdown", ctext, "```"])
    if diff:
        parts.extend(["", "Diff/context:", "```diff", diff, "```"])
    return "\n".join(parts)


def prepare_dataset(source: Path, output: Path, *, limit: int, sample: int | None, seed: int) -> None:
    rows = load_jsonl(source)
    if sample is not None:
        import random
        rng = random.Random(seed)
        rows = rng.sample(rows, min(sample, len(rows)))
    else:
        rows = rows[:limit]
    prepared = []
    for row in rows[:limit if sample is None else len(rows)]:
        expected = list(row.get("topics_of_interest") or [])
        prepared.append({
            "id": row["id"],
            "target": f"{row.get('repo')} {row.get('item_type')} #{row.get('number')}: {row.get('title')}",
            "github_context": github_context(row),
            "expected_topics": expected,
            "expected_topics_json": json.dumps(expected),
            "keywords": list(row.get("keywords") or []),
            "title": row.get("title") or "",
        })
    write_jsonl(output, prepared)
    print(f"wrote {len(prepared)} rows to {output}")


def refresh_github_context(input_path: Path, output: Path, source: Path = SOURCE) -> None:
    """Copy a prepared JSONL input while rebuilding github_context from raw seed rows.

    Historical prepared splits only contain a truncated/rendered github_context.  Keep the
    split order and labels, but replace context with the full raw body/comments/diff when
    the row id is present in the reference seed file.
    """
    source_by_id = {row["id"]: row for row in load_jsonl(source)}
    rows = load_jsonl(input_path)
    refreshed = []
    missing = 0
    for row in rows:
        raw = source_by_id.get(row.get("id"))
        if raw is None:
            missing += 1
            refreshed.append(row)
            continue
        refreshed.append({**row, "github_context": github_context(raw)})
    write_jsonl(output, refreshed)
    print(f"copied prepared input {input_path} to {output}; refreshed github_context for {len(rows) - missing}/{len(rows)} rows")


def extract_result(row: dict[str, Any]) -> dict[str, Any]:
    for key in ("result", "output", "response", "structured_output"):
        value = row.get(key)
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                return parsed
    return {}


def extract_output_text(row: dict[str, Any]) -> str:
    for key in ("result", "output", "response", "structured_output"):
        value = row.get(key)
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            return json.dumps(value, ensure_ascii=False)
    return ""


def parse_label_text(text: str, allowed: set[str]) -> list[str]:
    """Parse local-model plain-text labels robustly.

    Handles comma-separated labels, `labels: ...` lines, JSON-ish lists, and
    accidental prose. Keeps allowed enum order from first appearance and drops
    duplicates.
    """
    text = text.strip()
    if not text:
        return []
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        parsed = None
    if isinstance(parsed, dict):
        value = parsed.get("topics_of_interest", parsed.get("labels", []))
        if isinstance(value, list):
            return [x for x in dict.fromkeys(value) if isinstance(x, str) and x in allowed]
    if isinstance(parsed, list):
        return [x for x in dict.fromkeys(parsed) if isinstance(x, str) and x in allowed]

    label_line = text
    for line in text.splitlines():
        if re.match(r"^\s*(labels|topics_of_interest|topics)\s*:", line, re.I):
            label_line = line.split(":", 1)[1]
            break
    found = re.findall(r"[a-z][a-z0-9_]*", label_line.lower())
    return [x for x in dict.fromkeys(found) if x in allowed]


def f1(tp: int, fp: int, fn: int) -> float:
    denom = 2 * tp + fp + fn
    return 0.0 if denom == 0 else (2 * tp) / denom


def classify_problem(tp: int, fp: int, fn: int) -> str:
    if fp > fn * 1.5 and fp >= 3:
        return "over_predicted"
    if fn > fp * 1.5 and fn >= 3:
        return "under_predicted"
    if fp or fn:
        return "mixed"
    return "ok"


def evidence_excerpt(text: str, max_chars: int = 900) -> str:
    text = text or ""
    body = text.split("Body:\n```markdown\n", 1)[-1] if "Body:\n```markdown\n" in text else text
    body = body.split("\n```", 1)[0] if "\n```" in body else body
    body = "\n".join(line.rstrip() for line in body.splitlines() if line.strip())
    return truncate(body, max_chars, "evidence")


def failure_example(
    inp: dict[str, Any],
    result: dict[str, Any],
    expected: set[str],
    actual: set[str],
    row_score: float,
) -> dict[str, Any]:
    return {
        "id": inp.get("id"),
        "title": inp.get("title"),
        "expected": sorted(expected),
        "actual": sorted(actual),
        "keywords": (inp.get("keywords") or [])[:8],
        "description": result.get("description") if isinstance(result, dict) else None,
        "evidence_excerpt": evidence_excerpt(inp.get("github_context") or ""),
        "row_score": round(row_score, 3),
    }


def load_topic_hints_from_guidance(path: Path | str) -> dict[str, dict[str, str]]:
    """Replace TOPIC_HINTS from a frozen boundary-guidance markdown file.

    Makes the markdown spec the single source of truth for the dynamic-ASI
    topic hints. Parses `## \\`topic\\`` sections. Recognized bullet labels:
    `MUST include:` / `False-negative guard:` become the `fn` hint (when to
    add the topic) and `Do not include:` / `False-positive guard:` become the
    `fp` hint (when to withhold it). Any additional bullets in a section
    (decision rules, co-label and version notes) are appended to both
    directions.
    """
    text = Path(path).read_text(encoding="utf-8")
    parsed: dict[str, dict[str, str]] = {}
    section_re = re.compile(r"(?m)^## `([a-z][a-z0-9_]+)`[^\n]*\n(.*?)(?=^## |\Z)", re.S)
    bullet_re = re.compile(r"(?m)^- (.*?)(?=^- |\Z)", re.S)
    for match in section_re.finditer(text):
        topic, body = match.group(1), match.group(2)
        fp = fn = ""
        extras: list[str] = []
        for bullet in bullet_re.findall(body):
            flat = " ".join(bullet.split())
            lower = flat.lower()
            if lower.startswith(("false-positive guard:", "do not include:")):
                guard = flat.split(":", 1)[1].strip()
                fp = guard if not fp else f"{fp} {guard}"
            elif lower.startswith(("false-negative guard:", "must include:")):
                rule = flat.split(":", 1)[1].strip()
                if lower.startswith("must include:"):
                    rule = f"MUST include when central: {rule}"
                fn = rule if not fn else f"{fn} {rule}"
            elif flat:
                extras.append(flat)
        if not fp and not fn:
            continue
        suffix = (" " + " ".join(extras)) if extras else ""
        parsed[topic] = {"fp": (fp + suffix).strip(), "fn": (fn + suffix).strip()}
    if not parsed:
        raise ValueError(f"No `## \\`topic\\`` guard sections parsed from {path}")
    TOPIC_HINTS.clear()
    TOPIC_HINTS.update(parsed)
    return parsed


def topic_hint(topic: str, problem: str) -> str:
    hints = TOPIC_HINTS.get(topic, {})
    if problem == "over_predicted":
        return hints.get("fp", f"Tighten `{topic}`: add a clearer centrality gate and false-positive exclusions.")
    if problem == "under_predicted":
        return hints.get("fn", f"Improve `{topic}` recall: add stronger positive cues and examples for central evidence.")
    fp = hints.get("fp", f"Tighten false-positive rules for `{topic}`.")
    fn = hints.get("fn", f"Add positive cues for true `{topic}` cases.")
    return f"Mixed `{topic}` errors. {fp} {fn}"


def topic_action(topic: str, problem: str, expected: int, actual: int, tp: int, fp: int, fn: int, p: float, r: float) -> str:
    stats = (
        f"`{topic}` {problem}: expected in {expected} rows, predicted in {actual}, "
        f"TP={tp}, FP={fp}, FN={fn}, precision={p:.3f}, recall={r:.3f}."
    )
    if problem == "over_predicted":
        return f"{stats} Precision is the bottleneck. {topic_hint(topic, problem)}"
    if problem == "under_predicted":
        return f"{stats} Recall is the bottleneck. {topic_hint(topic, problem)}"
    if problem == "mixed":
        return f"{stats} Both precision and recall need boundary work. {topic_hint(topic, problem)}"
    return f"{stats} Boundary looks acceptable."


def load_topic_boundary_guidance(path: Path = TOPIC_BOUNDARY_GUIDANCE) -> dict[str, str]:
    if not path.exists():
        return {}
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## `") and line.endswith("`"):
            current = line.removeprefix("## `").removesuffix("`")
            sections[current] = [line]
        elif current:
            sections[current].append(line)
    return {topic: "\n".join(lines).strip() for topic, lines in sections.items()}


def load_static_labeling_guidance(path: Path = STATIC_LABELING_GUIDANCE) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8").strip()


def compact_example(example: dict[str, Any]) -> dict[str, Any]:
    return {
        "expected": example.get("expected"),
        "actual": example.get("actual"),
        "keywords": (example.get("keywords") or [])[:8],
        "row_score": example.get("row_score"),
    }


def compact_pattern(pattern: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "topic",
        "problem",
        "expected",
        "actual",
        "true_positives",
        "false_positives",
        "false_negatives",
        "precision",
        "recall",
        "f1",
        "action",
    ]
    out = {k: pattern[k] for k in keys if k in pattern}
    if "examples" in pattern:
        out["examples"] = [
            {
                "expected": x.get("expected"),
                "actual": x.get("actual"),
                "keywords": (x.get("keywords") or [])[:8],
                "error_type": x.get("error_type"),
            }
            for x in pattern["examples"][:3]
        ]
    for k in ["true_positive_examples", "false_positive_examples", "false_negative_examples"]:
        if k in pattern:
            out[k] = [compact_example(x) for x in pattern[k][:3]]
    return out


def compact_confusion(conf: dict[str, Any]) -> dict[str, Any]:
    out = {k: conf[k] for k in ["expected", "predicted", "count", "action"] if k in conf}
    out["examples"] = [compact_example(x) for x in conf.get("examples", [])[:2]]
    return out


def compact_failure(failure: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": failure.get("id"),
        "title": failure.get("title"),
        "expected": failure.get("expected"),
        "actual": failure.get("actual"),
        "false_positives": failure.get("false_positives"),
        "false_negatives": failure.get("false_negatives"),
        "invalid_topics": failure.get("invalid_topics"),
        "keywords": (failure.get("keywords") or [])[:8],
        "row_score": failure.get("row_score"),
    }


def score(output_path: Path) -> dict[str, Any]:
    rows = load_jsonl(output_path)
    failures: list[dict[str, Any]] = []
    topic_stats: dict[str, Counter[str]] = defaultdict(Counter)
    topic_examples: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: {
        "false_positive_examples": [],
        "false_negative_examples": [],
        "true_positive_examples": [],
    })
    confusion: Counter[tuple[str, str]] = Counter()
    confusion_examples: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    invalid_topics: Counter[str] = Counter()
    tp = fp = fn = exact = valid_json = 0
    row_jaccard_total = 0.0
    row_symdiff_total = 0
    expected_total = actual_total = 0

    allowed = set(json.loads(SCHEMA.read_text())["properties"]["topics_of_interest"]["items"]["enum"])
    static_asi_pack = load_static_labeling_guidance(ASI_PACK)

    for row in rows:
        inp = row.get("input") if isinstance(row.get("input"), dict) else row
        expected = set(inp.get("expected_topics") or [])
        result = extract_result(row)
        actual_raw = result.get("topics_of_interest") if isinstance(result, dict) else None
        if isinstance(actual_raw, list):
            actual_list = actual_raw
        else:
            actual_list = parse_label_text(extract_output_text(row), allowed)
        actual = {x for x in actual_list if isinstance(x, str) and x in allowed}
        invalid = [x for x in actual_list if not isinstance(x, str) or x not in allowed]
        for x in invalid:
            invalid_topics[str(x)] += 1

        row_valid = ((isinstance(result, dict) and isinstance(actual_raw, list)) or bool(extract_output_text(row).strip())) and not invalid
        valid_json += int(row_valid)
        row_tp = expected & actual
        row_fp = actual - expected
        row_fn = expected - actual
        row_union = expected | actual
        row_jaccard_total += 1.0 if not row_union else len(row_tp) / len(row_union)
        row_symdiff_total += len(expected ^ actual)
        row_score = f1(len(row_tp), len(row_fp), len(row_fn))
        example = failure_example(inp, result, expected, actual, row_score)
        tp += len(row_tp); fp += len(row_fp); fn += len(row_fn)
        expected_total += len(expected); actual_total += len(actual)
        exact += int(not row_fp and not row_fn and row_valid)

        for t in row_tp:
            topic_stats[t]["tp"] += 1
            if len(topic_examples[t]["true_positive_examples"]) < 3:
                topic_examples[t]["true_positive_examples"].append(example)
        for t in row_fp:
            topic_stats[t]["fp"] += 1
            if len(topic_examples[t]["false_positive_examples"]) < 4:
                topic_examples[t]["false_positive_examples"].append(example)
        for t in row_fn:
            topic_stats[t]["fn"] += 1
            if len(topic_examples[t]["false_negative_examples"]) < 4:
                topic_examples[t]["false_negative_examples"].append(example)
        for missed in row_fn:
            for extra in row_fp:
                confusion[(missed, extra)] += 1
                if len(confusion_examples[(missed, extra)]) < 3:
                    confusion_examples[(missed, extra)].append(example)

        if row_fp or row_fn or not row_valid:
            failures.append({
                "id": inp.get("id") or row.get("id"),
                "title": inp.get("title"),
                "expected": sorted(expected),
                "actual": sorted(actual),
                "false_positives": sorted(row_fp),
                "false_negatives": sorted(row_fn),
                "invalid_topics": invalid,
                "keywords": inp.get("keywords") or [],
                "description": result.get("description") if isinstance(result, dict) else None,
                "evidence_excerpt": example["evidence_excerpt"],
                "row_score": row_score,
            })

    n = max(1, len(rows))
    precision = 0.0 if tp + fp == 0 else tp / (tp + fp)
    recall = 0.0 if tp + fn == 0 else tp / (tp + fn)
    micro_f1 = f1(tp, fp, fn)
    row_exact_accuracy = exact / n
    avg_row_jaccard = row_jaccard_total / n
    avg_row_symdiff = row_symdiff_total / n
    per_topic_metrics = []
    for c in topic_stats.values():
        ttp, tfp, tfn = c["tp"], c["fp"], c["fn"]
        if ttp + tfp + tfn == 0:
            continue
        topic_precision = 0.0 if ttp + tfp == 0 else ttp / (ttp + tfp)
        topic_recall = 0.0 if ttp + tfn == 0 else ttp / (ttp + tfn)
        per_topic_metrics.append(
            {
                "precision": topic_precision,
                "recall": topic_recall,
                "f1": f1(ttp, tfp, tfn),
            }
        )
    macro_precision = (
        sum(x["precision"] for x in per_topic_metrics) / len(per_topic_metrics)
        if per_topic_metrics
        else 0.0
    )
    macro_recall = (
        sum(x["recall"] for x in per_topic_metrics) / len(per_topic_metrics)
        if per_topic_metrics
        else 0.0
    )
    macro_f1 = (
        sum(x["f1"] for x in per_topic_metrics) / len(per_topic_metrics)
        if per_topic_metrics
        else 0.0
    )

    patterns = []
    for topic, c in topic_stats.items():
        ttp, tfp, tfn = c["tp"], c["fp"], c["fn"]
        expected_count = ttp + tfn
        actual_count = ttp + tfp
        p = 0.0 if actual_count == 0 else ttp / actual_count
        r = 0.0 if expected_count == 0 else ttp / expected_count
        problem = classify_problem(ttp, tfp, tfn)
        if problem == "ok":
            continue
        examples = []
        for fail in failures:
            if topic in fail["false_positives"] or topic in fail["false_negatives"]:
                examples.append({
                    "id": fail["id"],
                    "title": fail["title"],
                    "expected": fail["expected"],
                    "actual": fail["actual"],
                    "keywords": fail["keywords"][:8],
                    "error_type": "false_positive" if topic in fail["false_positives"] else "false_negative",
                })
            if len(examples) >= 3:
                break
        patterns.append({
            "topic": topic,
            "problem": problem,
            "expected": expected_count,
            "actual": actual_count,
            "true_positives": ttp,
            "false_positives": tfp,
            "false_negatives": tfn,
            "precision": round(p, 3),
            "recall": round(r, 3),
            "f1": round(f1(ttp, tfp, tfn), 3),
            "action": topic_action(topic, problem, expected_count, actual_count, ttp, tfp, tfn, p, r),
            **topic_examples[topic],
            "examples": examples,
        })
    patterns.sort(key=lambda x: (x["false_positives"] + x["false_negatives"], min(x["precision"], x["recall"])), reverse=True)

    confusions = []
    for (expected_topic, predicted_topic), count in confusion.most_common(10):
        confusions.append({
            "expected": expected_topic,
            "predicted": predicted_topic,
            "count": count,
            "action": f"Clarify `{expected_topic}` vs `{predicted_topic}`. For missed `{expected_topic}`: {topic_hint(expected_topic, 'under_predicted')} For extra `{predicted_topic}`: {topic_hint(predicted_topic, 'over_predicted')}",
            "examples": confusion_examples[(expected_topic, predicted_topic)],
        })

    avg_expected = expected_total / n
    avg_actual = actual_total / n
    cardinality_closeness = max(0.0, 1.0 - abs(avg_actual - avg_expected) / max(1.0, avg_expected))
    feedback = []
    if avg_actual > avg_expected + 0.25:
        feedback.append(f"Candidate is over-labeling: avg predicted topics {avg_actual:.2f} vs expected {avg_expected:.2f}. Strengthen title-first centrality and second-topic gates.")
    elif avg_actual < avg_expected - 0.25:
        feedback.append(f"Candidate is under-labeling: avg predicted topics {avg_actual:.2f} vs expected {avg_expected:.2f}. Loosen gates for genuinely cross-topic rows and add positive cues for missed topics.")
    else:
        feedback.append(f"Topic cardinality is close: avg predicted topics {avg_actual:.2f} vs expected {avg_expected:.2f}. Focus on boundary-specific errors.")
    for ptn in patterns[:6]:
        feedback.append(ptn["action"])
    if invalid_topics:
        feedback.append(f"Invalid topics returned: {dict(invalid_topics.most_common(5))}. Enforce exact enum IDs only.")

    asi_score = min(1.0, (len(patterns[:8]) + len(confusions[:5]) + len(failures[:12])) / 25)
    return {
        "scores": {
            "gepa_score": micro_f1,
            "topic_micro_f1": micro_f1,
            "topic_micro_precision": precision,
            "topic_micro_recall": recall,
            "topic_macro_f1": macro_f1,
            "topic_macro_precision": macro_precision,
            "topic_macro_recall": macro_recall,
            "exact_match": row_exact_accuracy,
            "row_exact_accuracy": row_exact_accuracy,
            "avg_row_jaccard": avg_row_jaccard,
            "valid_json": valid_json / n,
            "cardinality_closeness": cardinality_closeness,
        },
        "score_details": {
            "false_positives": fp,
            "false_negatives": fn,
            "row_exact_accuracy": row_exact_accuracy,
            "avg_row_jaccard": avg_row_jaccard,
            "avg_row_symdiff": avg_row_symdiff,
            "avg_expected_topics": avg_expected,
            "avg_predicted_topics": avg_actual,
            "topic_macro_active_labels": len(per_topic_metrics),
            "asi_score": asi_score,
        },
        "evaluated": len(rows),
        "failures": [compact_failure(x) for x in failures[:12]],
        "worst_failures": [
            compact_failure(x)
            for x in sorted(failures, key=lambda x: (x["row_score"], -(len(x["false_positives"]) + len(x["false_negatives"]))))[:8]
        ],
        "topic_error_patterns": [compact_pattern(x) for x in patterns[:8]],
        "confusions": [compact_confusion(x) for x in confusions[:6]],
        "invalid_topics": dict(invalid_topics.most_common(10)),
        "actionable_feedback": feedback[:10],
        "static_asi_pack": static_asi_pack,
    }


def render_policy_card(policy_path: Path, card_path: Path, *, plain_labels: bool = False) -> None:
    allowed = ALLOWED_TOPICS.read_text(encoding="utf-8")
    policy = policy_path.read_text(encoding="utf-8").strip()
    if plain_labels:
        schema_topics = json.loads(SCHEMA.read_text(encoding="utf-8"))["properties"]["topics_of_interest"]["items"]["enum"]
        output_instruction = f"""Return only comma-separated topic IDs. No JSON, markdown, prose, explanation, confidence, or extra fields.
Example output:
reliability,browser_automation,exec_tools

Allowed topic IDs:
{", ".join(schema_topics)}

If no listed topic applies, return exactly:
none

Ignore any policy wording about structured JSON output; for this local-model run, comma-separated labels are the required output format."""
    else:
        output_instruction = """Return only the final structured JSON required by the schema. No prose, markdown, analysis, or extra fields.

Required output shape:

```json
{"topics_of_interest":[],"description":"One concise evidence-backed sentence.","caveats":[]}
```"""
    card_path.write_text(
        f"""---
type: agent
name: openclaw_classifier
model: "$system.default"
skills: []
use_history: false
---

# OpenClaw Routing Classifier

Classify one OpenClaw GitHub issue or pull request according to the routing policy below.
{output_instruction}

{allowed}

{policy}
""",
        encoding="utf-8",
    )


def resolve_agent_card(args: argparse.Namespace, run_dir: Path) -> Path:
    if args.policy is None:
        return args.agent_card
    card = run_dir / "openclaw-classifier.from-policy.md"
    render_policy_card(args.policy, card, plain_labels=args.plain_labels)
    return card


def run_batch(args: argparse.Namespace, run_dir: Path) -> Path:
    run_dir.mkdir(parents=True, exist_ok=True)
    output = run_dir / "results.jsonl"
    summary = run_dir / "batch-summary.json"
    telemetry = run_dir / "telemetry.jsonl"
    template = SMOKE_TEMPLATE if args.model == "passthrough" else TASK_TEMPLATE
    agent_card = resolve_agent_card(args, run_dir)
    cmd = [
        args.fast_agent_bin, "--no-update-check", "--env", str(ENV_DIR), "batch", "run",
        "--agent-card", str(agent_card), "--agent", "openclaw_classifier",
        "--input", str(args.input), "--output", str(output),
        "--template", str(template),
    ]
    if not args.plain_labels:
        cmd.extend(["--json-schema", str(SCHEMA)])
    cmd.extend([
        "--model", args.model, "--id-field", "id", "--include-input",
        "--summary-output", str(summary), "--telemetry-output", str(telemetry),
        "--parallel", str(args.parallel), "--overwrite", "--no-final-summary",
    ])
    (run_dir / "command.json").write_text(json.dumps(cmd, indent=2), encoding="utf-8")
    (run_dir / "benchmark-config.json").write_text(
        json.dumps(
            {
                "model": args.model,
                "input": str(args.input),
                "agent_card": str(agent_card),
                "policy": str(args.policy) if args.policy else None,
                "schema": str(SCHEMA),
                "template": str(template),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)
    (run_dir / "stdout.txt").write_text(proc.stdout, encoding="utf-8")
    (run_dir / "stderr.txt").write_text(proc.stderr, encoding="utf-8")
    if proc.returncode:
        raise RuntimeError(f"fast-agent batch failed with exit {proc.returncode}\n{proc.stderr[-2000:]}")
    return output


def main() -> int:
    args = parse_args()
    if args.score_only:
        report = score(args.score_only)
        print(json.dumps(report, indent=2))
        return 0
    if not args.no_prepare:
        prepare_dataset(args.source, args.input, limit=args.limit, sample=args.sample, seed=args.seed)
    if args.prepare_only:
        return 0
    run_name = args.run_name or time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    run_dir = args.output_dir / run_name
    output = run_batch(args, run_dir)
    report = score(output)
    (run_dir / "score.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"run_dir": str(run_dir), **report}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
