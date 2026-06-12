general note on `coding_agents`:

### Coding-agent boundary

Do not use `coding_agents` merely because the item mentions agents, subagents,
`sessions_spawn`, agent runs, tool use, approvals, sandboxing, compaction, traces, or
orchestration inside OpenClaw.

Route those internal OpenClaw concerns to the concrete owning surface instead:
`agent_runtime`, `acp`, `acpx`, `sessions`, `queueing`, `tool_calling`, `approvals`,
`sandboxing`, or `telemetry_usage`.

ACP is an integration protocol. It may be used by coding agents, but ACP work is not
`coding_agents` unless the issue/PR is specifically about a coding-agent integration
through ACP.

For the two example rows, the expected action would be:

- 68204: remove `coding_agents`; this is trace/observability plus ACP/runtime producer
coverage, not a coding-agent integration.
- 10467: remove `coding_agents`; this is internal `sessions_spawn` queue/config/tool
plumbing for OpenClaw subagents, not an external coding-agent integration.

That should be enough to steer the review packet without row-by-row micro-rules.

### openclaw-openclaw-42408


telemetry_usage should not appear here -- it may have appeared because it is adjacent to benchmark. telemetry_usage should be used when speaking specifically about that aspect of the openclaw product.

###  openclaw-openclaw-68204

telemetry_usage is appropriate here. 

this issue does not directly address coding_agents: it does affect agent_runtime which is the openclaw internal. for this case, there is no reference to external coding_agents such as codex, claude code or pi.

### openclaw-openclaw-68916

the issue specifically does refer to gateway as the issue source; and the guidance seems to indicate it should be selected for this case. 

### openclaw-openclaw-71487

this specifically requests config changes -- for some reason opus is in disagreement. perhaps a small adjustment to the wording may help here.

### openclaw-openclaw-76724

Adjudication: `mcp_tooling`

`mcp_tooling` is correct. The central failure is MCP tool discovery/materialization: the
remote MCP server handshakes successfully, but OpenClaw does not issue or complete the
`tools/list` discovery path, so the tools never become available.

Remove `ui_tui`. The dashboard and reload button are only where the user observes or
triggers the problem. The issue is not about UI rendering, navigation, layout, display
logic, or control behavior.

Guidance clarification:

Do not include `ui_tui` merely because a defect is observed through a dashboard, button,
status count, tool list, footer, or other visible UI surface. Include `ui_tui` only when
the UI display, interaction, navigation, rendering, or user-facing control behavior is
itself the failing or changed surface.

### openclaw-openclaw-78528

this is an opus/gpt firm disagreement with opus not including auth_identity. in this case, we should not have `auth_identity` as it doesn't directly relate to the authorization/login surface of the openclaw product itself.


### openclaw-openclaw-76724

this should not be u

### openclaw-openclaw-10467

