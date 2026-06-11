# v3-relabel-opus disagreements vs easy-final-v3

- model: `opus`
- rows: 149
- exact agreement: 141
- changed rows: 8
- non-strict/not-easy rows: 139

## Changed rows

### openclaw-openclaw-48406 / #48406 — Docs: add saturated session recovery guide

- bucket: `medium` confidence: `0.62` strict_easy: `False`
- easy-final-v3: `docs, memory, sessions`
- opus: `docs, sessions, memory, config`
- opus additions: `config`
- opus removals: ``

### openclaw-openclaw-52249 / #52249 — ACP parent session stuck until refresh when yielded waiting for child completion

- bucket: `medium` confidence: `0.78` strict_easy: `False`
- easy-final-v3: `acp, sessions, queueing, reliability`
- opus: `acp, sessions, reliability, agent_runtime`
- opus additions: `agent_runtime`
- opus removals: `queueing`

### openclaw-openclaw-56442 / #56442 — feat: Add opt-in ACP parent completion notify for sessions_spawn

- bucket: `medium` confidence: `0.74` strict_easy: `False`
- easy-final-v3: `acp, sessions, notifications, api_surface`
- opus: `acp, sessions, notifications, agent_runtime`
- opus additions: `agent_runtime`
- opus removals: `api_surface`

### openclaw-openclaw-60381 / #60381 — browser tool: add force parameter for click and expose evaluate action

- bucket: `medium` confidence: `0.7` strict_easy: `False`
- easy-final-v3: `browser_automation, api_surface, security`
- opus: `browser_automation, security`
- opus additions: ``
- opus removals: `api_surface`

### openclaw-openclaw-65364 / #65364 — feat(plugins): add registerProviderRuntimeAuthOverride API

- bucket: `medium` confidence: `0.86` strict_easy: `False`
- easy-final-v3: `api_surface, auth_identity, security, skills_plugins`
- opus: `skills_plugins, auth_identity, security`
- opus additions: ``
- opus removals: `api_surface`

### openclaw-openclaw-72013 / #72013 — ACP startup identity reconcile warns on terminal one-shot sessions

- bucket: `medium` confidence: `0.85` strict_easy: `False`
- easy-final-v3: `acp, gateway, sessions`
- opus: `acp, acpx, gateway, sessions`
- opus additions: `acpx`
- opus removals: ``

### openclaw-openclaw-80008 / #80008 — feat(plugins): expose ACP spawn and prompt in plugin runtime

- bucket: `medium` confidence: `0.62` strict_easy: `False`
- easy-final-v3: `acp, api_surface, config, notifications, skills_plugins`
- opus: `skills_plugins, acp, config, notifications`
- opus additions: ``
- opus removals: `api_surface`

### openclaw-openclaw-84771 / #84771 — Event loop saturation during startup: synchronous model-prewarm and session-locks block event loop for 28-64 seconds

- bucket: `medium` confidence: `0.62` strict_easy: `False`
- easy-final-v3: `gateway, model_serving, reliability, sessions`
- opus: `reliability, gateway, sessions, chat_integrations`
- opus additions: `chat_integrations`
- opus removals: `model_serving`

## Non-strict / not-easy rows

- openclaw-openclaw-39714 / #39714 — bucket `medium`, confidence `0.88`, strict `False`, labels `sandboxing, browser_automation, reliability`
- openclaw-openclaw-40332 / #40332 — bucket `medium`, confidence `0.82`, strict `False`, labels `acpx, acp, approvals, config, security`
- openclaw-openclaw-42027 / #42027 — bucket `medium`, confidence `0.82`, strict `False`, labels `exec_tools, browser_automation, cron_automation, queueing, reliability`
- openclaw-openclaw-42122 / #42122 — bucket `easy`, confidence `0.93`, strict `False`, labels `packaging_deployment, tests_ci`
- openclaw-openclaw-42408 / #42408 — bucket `medium`, confidence `0.72`, strict `False`, labels `memory, config, docs`
- openclaw-openclaw-42425 / #42425 — bucket `easy`, confidence `0.92`, strict `False`, labels `hooks, gateway, sessions`
- openclaw-openclaw-42606 / #42606 — bucket `easy`, confidence `0.92`, strict `False`, labels `browser_automation, security, api_surface`
- openclaw-openclaw-43564 / #43564 — bucket `medium`, confidence `0.82`, strict `False`, labels `acp, sessions, skills_plugins, security`
- openclaw-openclaw-44379 / #44379 — bucket `medium`, confidence `0.83`, strict `False`, labels `agent_runtime, reliability, hooks, memory`
- openclaw-openclaw-45200 / #45200 — bucket `medium`, confidence `0.86`, strict `False`, labels `agent_runtime, notifications, reliability`
- openclaw-openclaw-45393 / #45393 — bucket `medium`, confidence `0.75`, strict `False`, labels `tool_calling, reliability, sessions, security`
- openclaw-openclaw-45508 / #45508 — bucket `medium`, confidence `0.7`, strict `False`, labels `self_hosted_inference, chat_integrations, gateway, config`
- openclaw-openclaw-45841 / #45841 — bucket `medium`, confidence `0.86`, strict `False`, labels `sandboxing, acp, security, sessions`
- openclaw-openclaw-46552 / #46552 — bucket `medium`, confidence `0.86`, strict `False`, labels `docs, queueing, tool_calling`
- openclaw-openclaw-47083 / #47083 — bucket `easy`, confidence `0.92`, strict `False`, labels `telemetry_usage, ui_tui, sessions`
- openclaw-openclaw-47446 / #47446 — bucket `medium`, confidence `0.83`, strict `False`, labels `chat_integrations, gateway, reliability, config`
- openclaw-openclaw-48406 / #48406 — bucket `medium`, confidence `0.62`, strict `False`, labels `docs, sessions, memory, config`
- openclaw-openclaw-48580 / #48580 — bucket `easy`, confidence `0.93`, strict `False`, labels `acpx, codex, sessions, reliability`
- openclaw-openclaw-48606 / #48606 — bucket `easy`, confidence `0.91`, strict `False`, labels `browser_automation, reliability`
- openclaw-openclaw-48851 / #48851 — bucket `easy`, confidence `0.92`, strict `False`, labels `telemetry_usage, sessions, ui_tui`
- openclaw-openclaw-48877 / #48877 — bucket `easy`, confidence `0.93`, strict `False`, labels `chat_integrations, config`
- openclaw-openclaw-48940 / #48940 — bucket `medium`, confidence `0.82`, strict `False`, labels `acp, gateway, agent_runtime, sessions, reliability`
- openclaw-openclaw-49310 / #49310 — bucket `easy`, confidence `0.92`, strict `False`, labels `ui_tui, sessions`
- openclaw-openclaw-49502 / #49502 — bucket `easy`, confidence `0.92`, strict `False`, labels `gateway, telemetry_usage, api_surface`
- openclaw-openclaw-50054 / #50054 — bucket `medium`, confidence `0.84`, strict `False`, labels `acp, sessions, reliability`
- openclaw-openclaw-51849 / #51849 — bucket `easy`, confidence `0.92`, strict `False`, labels `docs, agent_demos`
- openclaw-openclaw-52249 / #52249 — bucket `medium`, confidence `0.78`, strict `False`, labels `acp, sessions, reliability, agent_runtime`
- openclaw-openclaw-53319 / #53319 — bucket `medium`, confidence `0.83`, strict `False`, labels `acpx, acp, sessions, reliability`
- openclaw-openclaw-54471 / #54471 — bucket `easy`, confidence `0.92`, strict `False`, labels `acp, sessions, notifications`
- openclaw-openclaw-55790 / #55790 — bucket `easy`, confidence `0.91`, strict `False`, labels `sessions, agent_runtime, config`
- openclaw-openclaw-56442 / #56442 — bucket `medium`, confidence `0.74`, strict `False`, labels `acp, sessions, notifications, agent_runtime`
- openclaw-openclaw-56532 / #56532 — bucket `easy`, confidence `0.92`, strict `False`, labels `memory, config, reliability`
- openclaw-openclaw-56613 / #56613 — bucket `medium`, confidence `0.8`, strict `False`, labels `ui_tui, sessions, config`
- openclaw-openclaw-57597 / #57597 — bucket `medium`, confidence `0.83`, strict `False`, labels `acp, sessions, reliability`
- openclaw-openclaw-58411 / #58411 — bucket `medium`, confidence `0.82`, strict `False`, labels `acp, sessions, chat_integrations, api_surface`
- openclaw-openclaw-59208 / #59208 — bucket `easy`, confidence `0.91`, strict `False`, labels `auth_identity, telemetry_usage, ui_tui`
- openclaw-openclaw-59878 / #59878 — bucket `easy`, confidence `0.92`, strict `False`, labels `sessions, queueing, reliability, gateway`
- openclaw-openclaw-60381 / #60381 — bucket `medium`, confidence `0.7`, strict `False`, labels `browser_automation, security`
- openclaw-openclaw-60737 / #60737 — bucket `medium`, confidence `0.86`, strict `False`, labels `acp, chat_integrations, config, sessions`
- openclaw-openclaw-60979 / #60979 — bucket `easy`, confidence `0.91`, strict `False`, labels `acp, sessions, chat_integrations, notifications`
- openclaw-openclaw-61775 / #61775 — bucket `easy`, confidence `0.92`, strict `False`, labels `packaging_deployment, tests_ci`
- openclaw-openclaw-62428 / #62428 — bucket `medium`, confidence `0.86`, strict `False`, labels `exec_tools, approvals, security, tests_ci`
- openclaw-openclaw-62552 / #62552 — bucket `medium`, confidence `0.85`, strict `False`, labels `acp, sessions, reliability, queueing`
- openclaw-openclaw-62769 / #62769 — bucket `easy`, confidence `0.91`, strict `False`, labels `acp, chat_integrations, sessions`
- openclaw-openclaw-63007 / #63007 — bucket `medium`, confidence `0.83`, strict `False`, labels `gateway, hooks, notifications, sessions`
- openclaw-openclaw-63229 / #63229 — bucket `medium`, confidence `0.86`, strict `False`, labels `gateway, local_models, model_serving, reliability`
- openclaw-openclaw-64181 / #64181 — bucket `easy`, confidence `0.9`, strict `False`, labels `hooks, memory, reliability`
- openclaw-openclaw-64199 / #64199 — bucket `medium`, confidence `0.78`, strict `False`, labels `acpx, acp, sessions, chat_integrations, security`
- openclaw-openclaw-64718 / #64718 — bucket `easy`, confidence `0.92`, strict `False`, labels `security, exec_tools, approvals, auth_identity`
- openclaw-openclaw-65242 / #65242 — bucket `medium`, confidence `0.82`, strict `False`, labels `acp, notifications, reliability, sessions, agent_runtime`
- openclaw-openclaw-65364 / #65364 — bucket `medium`, confidence `0.86`, strict `False`, labels `skills_plugins, auth_identity, security`
- openclaw-openclaw-65640 / #65640 — bucket `easy`, confidence `0.91`, strict `False`, labels `acp, sessions, reliability, acpx`
- openclaw-openclaw-66000 / #66000 — bucket `easy`, confidence `0.91`, strict `False`, labels `config, gateway, packaging_deployment`
- openclaw-openclaw-66125 / #66125 — bucket `medium`, confidence `0.86`, strict `False`, labels `local_model_providers, model_serving, reliability`
- openclaw-openclaw-66327 / #66327 — bucket `easy`, confidence `0.92`, strict `False`, labels `chat_integrations, approvals, notifications`
- openclaw-openclaw-67244 / #67244 — bucket `medium`, confidence `0.84`, strict `False`, labels `acpx, acp, agent_runtime, sessions, reliability`
- openclaw-openclaw-68187 / #68187 — bucket `easy`, confidence `0.92`, strict `False`, labels `mcp_tooling, sessions, gateway, reliability`
- openclaw-openclaw-68204 / #68204 — bucket `medium`, confidence `0.82`, strict `False`, labels `telemetry_usage, agent_runtime, acp, sessions`
- openclaw-openclaw-68843 / #68843 — bucket `easy`, confidence `0.92`, strict `False`, labels `acp, sessions, reliability`
- openclaw-openclaw-69260 / #69260 — bucket `medium`, confidence `0.71`, strict `False`, labels `acp, auth_identity, security, hooks`
- openclaw-openclaw-69328 / #69328 — bucket `medium`, confidence `0.82`, strict `False`, labels `acp, reliability, sessions, ui_tui`
- openclaw-openclaw-69669 / #69669 — bucket `medium`, confidence `0.78`, strict `False`, labels `acp, sessions, agent_runtime, coding_agents`
- openclaw-openclaw-70002 / #70002 — bucket `easy`, confidence `0.95`, strict `False`, labels `tests_ci`
- openclaw-openclaw-70529 / #70529 — bucket `medium`, confidence `0.78`, strict `False`, labels `browser_automation, packaging_deployment, auth_identity, exec_tools`
- openclaw-openclaw-70882 / #70882 — bucket `easy`, confidence `0.91`, strict `False`, labels `mcp_tooling, tool_calling, security`
- openclaw-openclaw-71157 / #71157 — bucket `easy`, confidence `0.9`, strict `False`, labels `chat_integrations, config`
- openclaw-openclaw-71216 / #71216 — bucket `medium`, confidence `0.72`, strict `False`, labels `config, gateway, sandboxing, security, local_model_providers`
- openclaw-openclaw-71487 / #71487 — bucket `easy`, confidence `0.91`, strict `False`, labels `ui_tui, self_hosted_inference, config`
- openclaw-openclaw-71594 / #71594 — bucket `easy`, confidence `0.93`, strict `False`, labels `docs, gateway`
- openclaw-openclaw-71646 / #71646 — bucket `easy`, confidence `0.91`, strict `False`, labels `mcp_tooling, approvals, reliability`
- openclaw-openclaw-71648 / #71648 — bucket `easy`, confidence `0.92`, strict `False`, labels `mcp_tooling, approvals, reliability`
- openclaw-openclaw-71784 / #71784 — bucket `easy`, confidence `0.91`, strict `False`, labels `memory, reliability`
- openclaw-openclaw-71803 / #71803 — bucket `medium`, confidence `0.78`, strict `False`, labels `reliability, sessions, agent_runtime, exec_tools`
- openclaw-openclaw-71930 / #71930 — bucket `easy`, confidence `0.92`, strict `False`, labels `chat_integrations, reliability`
- openclaw-openclaw-71976 / #71976 — bucket `medium`, confidence `0.78`, strict `False`, labels `memory, reliability`
- openclaw-openclaw-72001 / #72001 — bucket `easy`, confidence `0.91`, strict `False`, labels `hooks, config, gateway`
- openclaw-openclaw-72013 / #72013 — bucket `medium`, confidence `0.85`, strict `False`, labels `acp, acpx, gateway, sessions`
- openclaw-openclaw-72015 / #72015 — bucket `medium`, confidence `0.85`, strict `False`, labels `memory, reliability, gateway`
- openclaw-openclaw-72087 / #72087 — bucket `medium`, confidence `0.7`, strict `False`, labels `codex, packaging_deployment, auth_identity`
- openclaw-openclaw-72133 / #72133 — bucket `easy`, confidence `0.92`, strict `False`, labels `telemetry_usage, ui_tui, chat_integrations`
- openclaw-openclaw-72138 / #72138 — bucket `easy`, confidence `0.92`, strict `False`, labels `chat_integrations, hooks, notifications`
- openclaw-openclaw-72262 / #72262 — bucket `easy`, confidence `0.93`, strict `False`, labels `docs, chat_integrations, reliability`
- openclaw-openclaw-73910 / #73910 — bucket `medium`, confidence `0.8`, strict `False`, labels `acpx, acp, codex, auth_identity, config`
- openclaw-openclaw-74305 / #74305 — bucket `medium`, confidence `0.86`, strict `False`, labels `acpx, acp, codex, reliability`
- openclaw-openclaw-74484 / #74484 — bucket `medium`, confidence `0.82`, strict `False`, labels `auth_identity, gateway, reliability`
- openclaw-openclaw-75657 / #75657 — bucket `easy`, confidence `0.92`, strict `False`, labels `local_models, memory, gateway, reliability`
- openclaw-openclaw-77694 / #77694 — bucket `medium`, confidence `0.84`, strict `False`, labels `acpx, acp, agent_runtime, reliability`
- openclaw-openclaw-77748 / #77748 — bucket `medium`, confidence `0.68`, strict `False`, labels `codex, chat_integrations, packaging_deployment, auth_identity, skills_plugins`
- openclaw-openclaw-78528 / #78528 — bucket `medium`, confidence `0.86`, strict `False`, labels `security, exec_tools, skills_plugins, auth_identity`
- openclaw-openclaw-78919 / #78919 — bucket `medium`, confidence `0.88`, strict `False`, labels `acp, acpx, codex, sessions`
- openclaw-openclaw-78977 / #78977 — bucket `easy`, confidence `0.9`, strict `False`, labels `model_serving, reliability`
- openclaw-openclaw-79447 / #79447 — bucket `medium`, confidence `0.82`, strict `False`, labels `auth_identity, config`
- openclaw-openclaw-79897 / #79897 — bucket `easy`, confidence `0.92`, strict `False`, labels `local_models, model_serving, telemetry_usage`
- openclaw-openclaw-80008 / #80008 — bucket `medium`, confidence `0.62`, strict `False`, labels `skills_plugins, acp, config, notifications`
- openclaw-openclaw-80255 / #80255 — bucket `medium`, confidence `0.86`, strict `False`, labels `memory, reliability, queueing, agent_runtime`
- openclaw-openclaw-80431 / #80431 — bucket `easy`, confidence `0.92`, strict `False`, labels `acpx, mcp_tooling, tests_ci`
- openclaw-openclaw-80475 / #80475 — bucket `easy`, confidence `0.94`, strict `False`, labels `acpx, tests_ci, mcp_tooling`
- openclaw-openclaw-80479 / #80479 — bucket `easy`, confidence `0.92`, strict `False`, labels `local_model_providers, self_hosted_inference, memory`
- openclaw-openclaw-81200 / #81200 — bucket `medium`, confidence `0.85`, strict `False`, labels `acpx, security, auth_identity, acp`
- openclaw-openclaw-81249 / #81249 — bucket `medium`, confidence `0.85`, strict `False`, labels `self_hosted_inference, security, config, local_models`
- openclaw-openclaw-81488 / #81488 — bucket `easy`, confidence `0.92`, strict `False`, labels `approvals, exec_tools, security`
- openclaw-openclaw-81957 / #81957 — bucket `medium`, confidence `0.86`, strict `False`, labels `tests_ci, security, packaging_deployment, auth_identity`
- openclaw-openclaw-82145 / #82145 — bucket `medium`, confidence `0.88`, strict `False`, labels `cron_automation, local_model_providers, config, reliability`
- openclaw-openclaw-82507 / #82507 — bucket `medium`, confidence `0.84`, strict `False`, labels `acpx, codex, sandboxing, skills_plugins`
- openclaw-openclaw-82596 / #82596 — bucket `easy`, confidence `0.93`, strict `False`, labels `exec_tools, approvals, security`
- openclaw-openclaw-82642 / #82642 — bucket `easy`, confidence `0.91`, strict `False`, labels `chat_integrations, notifications, reliability`
- openclaw-openclaw-83333 / #83333 — bucket `easy`, confidence `0.91`, strict `False`, labels `memory, self_hosted_inference, reliability`
- openclaw-openclaw-83982 / #83982 — bucket `medium`, confidence `0.82`, strict `False`, labels `api_surface, config, skills_plugins`
- openclaw-openclaw-84094 / #84094 — bucket `easy`, confidence `0.92`, strict `False`, labels `gateway, api_surface, model_serving`
- openclaw-openclaw-84297 / #84297 — bucket `medium`, confidence `0.6`, strict `False`, labels `chat_integrations, cron_automation, notifications, auth_identity`
- openclaw-openclaw-84301 / #84301 — bucket `medium`, confidence `0.82`, strict `False`, labels `config, local_models, queueing, reliability`
- openclaw-openclaw-84316 / #84316 — bucket `easy`, confidence `0.92`, strict `False`, labels `chat_integrations, notifications, reliability`
- openclaw-openclaw-84337 / #84337 — bucket `easy`, confidence `0.93`, strict `False`, labels `security, gateway, hooks, auth_identity`
- openclaw-openclaw-84385 / #84385 — bucket `medium`, confidence `0.86`, strict `False`, labels `ui_tui`
- openclaw-openclaw-84418 / #84418 — bucket `easy`, confidence `0.91`, strict `False`, labels `cron_automation, security, tests_ci`
- openclaw-openclaw-84419 / #84419 — bucket `easy`, confidence `0.93`, strict `False`, labels `sessions, tool_calling, reliability`
- openclaw-openclaw-84567 / #84567 — bucket `easy`, confidence `0.92`, strict `False`, labels `codex, cron_automation, agent_runtime, reliability`
- openclaw-openclaw-84570 / #84570 — bucket `easy`, confidence `0.92`, strict `False`, labels `approvals, exec_tools, skills_plugins`
- openclaw-openclaw-84583 / #84583 — bucket `easy`, confidence `0.91`, strict `False`, labels `cron_automation, sessions, reliability, notifications, chat_integrations`
- openclaw-openclaw-84637 / #84637 — bucket `medium`, confidence `0.74`, strict `False`, labels `codex, agent_runtime, config, sessions`
- openclaw-openclaw-84645 / #84645 — bucket `easy`, confidence `0.93`, strict `False`, labels `exec_tools, approvals, security`
- openclaw-openclaw-84648 / #84648 — bucket `easy`, confidence `0.91`, strict `False`, labels `exec_tools, hooks, security`
- openclaw-openclaw-84660 / #84660 — bucket `easy`, confidence `0.9`, strict `False`, labels `chat_integrations, self_hosted_inference, queueing, reliability`
- openclaw-openclaw-84681 / #84681 — bucket `medium`, confidence `0.86`, strict `False`, labels `codex, tool_calling, sessions`
- openclaw-openclaw-84697 / #84697 — bucket `easy`, confidence `0.91`, strict `False`, labels `local_model_providers, model_serving, config`
- openclaw-openclaw-84709 / #84709 — bucket `medium`, confidence `0.88`, strict `False`, labels `codex, cron_automation, exec_tools, reliability`
- openclaw-openclaw-84715 / #84715 — bucket `medium`, confidence `0.86`, strict `False`, labels `codex, packaging_deployment, skills_plugins, reliability`
- openclaw-openclaw-84729 / #84729 — bucket `medium`, confidence `0.82`, strict `False`, labels `tests_ci, ui_tui`
- openclaw-openclaw-84732 / #84732 — bucket `medium`, confidence `0.86`, strict `False`, labels `chat_integrations, notifications, reliability`
- openclaw-openclaw-84752 / #84752 — bucket `medium`, confidence `0.72`, strict `False`, labels `reliability, queueing, chat_integrations, auth_identity, codex`
- openclaw-openclaw-84757 / #84757 — bucket `easy`, confidence `0.91`, strict `False`, labels `chat_integrations, sessions, reliability`
- openclaw-openclaw-84763 / #84763 — bucket `medium`, confidence `0.85`, strict `False`, labels `acpx, acp, auth_identity, security, config`
- openclaw-openclaw-84771 / #84771 — bucket `medium`, confidence `0.62`, strict `False`, labels `reliability, gateway, sessions, chat_integrations`
- openclaw-openclaw-84789 / #84789 — bucket `easy`, confidence `0.9`, strict `False`, labels `memory, sessions, chat_integrations, reliability`
- openclaw-openclaw-84794 / #84794 — bucket `easy`, confidence `0.93`, strict `False`, labels `cron_automation, sessions, reliability`
- openclaw-openclaw-84802 / #84802 — bucket `easy`, confidence `0.92`, strict `False`, labels `memory, sessions, reliability`
- openclaw-openclaw-85999 / #85999 — bucket `medium`, confidence `0.86`, strict `False`, labels `gateway, reliability, auth_identity, chat_integrations`
- openclaw-openclaw-88816 / #88816 — bucket `medium`, confidence `0.7`, strict `False`, labels `model_serving, config, auth_identity`
- openclaw-openclaw-90146 / #90146 — bucket `medium`, confidence `0.72`, strict `False`, labels `config, reliability, agent_runtime, model_releases`