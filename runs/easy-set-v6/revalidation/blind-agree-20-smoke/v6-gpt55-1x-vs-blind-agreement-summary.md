# v6 GPT-5.5 1x vs prior blind agreement on 20 rows

- rows: 20
- v6 == current: 5
- v6 == prior blind agreement: 8
- v6 other: 7

| id | v6 match | current | prior blind agreement | v6 |
|---|---|---|---|---|
| openclaw-openclaw-47083 | blind | `['sessions', 'telemetry_usage', 'ui_tui']` | `['telemetry_usage', 'ui_tui']` | `['telemetry_usage', 'ui_tui']` |
| openclaw-openclaw-51849 | blind | `['agent_demos', 'docs']` | `['docs']` | `['docs']` |
| openclaw-openclaw-53997 | other | `['acp', 'acpx', 'reliability']` | `['acpx', 'reliability']` | `['acpx', 'agent_runtime', 'exec_tools', 'reliability']` |
| openclaw-openclaw-68916 | blind | `['acp', 'reliability', 'sessions']` | `['acp', 'gateway', 'reliability', 'sessions']` | `['acp', 'gateway', 'reliability', 'sessions']` |
| openclaw-openclaw-71157 | other | `['chat_integrations', 'config', 'security']` | `['chat_integrations', 'config']` | `['chat_integrations', 'config', 'notifications']` |
| openclaw-openclaw-71487 | blind | `['config', 'self_hosted_inference', 'ui_tui']` | `['config', 'ui_tui']` | `['config', 'ui_tui']` |
| openclaw-openclaw-71976 | blind | `['memory', 'reliability']` | `['memory']` | `['memory']` |
| openclaw-openclaw-72138 | other | `['chat_integrations', 'hooks', 'notifications']` | `['chat_integrations', 'hooks']` | `['chat_integrations', 'hooks', 'notifications', 'skills_plugins']` |
| openclaw-openclaw-77694 | other | `['acp', 'acpx', 'agent_runtime', 'reliability']` | `['acp', 'acpx']` | `['acp', 'acpx', 'coding_agents']` |
| openclaw-openclaw-78528 | blind | `['auth_identity', 'exec_tools', 'security', 'skills_plugins']` | `['exec_tools', 'security', 'skills_plugins']` | `['exec_tools', 'security', 'skills_plugins']` |
| openclaw-openclaw-82642 | other | `['chat_integrations', 'notifications', 'reliability']` | `['chat_integrations']` | `['chat_integrations', 'notifications']` |
| openclaw-openclaw-84761 | blind | `['auth_identity', 'config', 'security']` | `['security']` | `['security']` |
| openclaw-openclaw-84771 | other | `['gateway', 'model_serving', 'reliability', 'sessions']` | `['gateway', 'reliability', 'sessions']` | `['gateway', 'model_serving', 'queueing', 'reliability', 'sessions']` |
| openclaw-openclaw-84997 | other | `['auth_identity', 'model_serving']` | `['auth_identity', 'model_releases', 'model_serving']` | `['api_surface', 'auth_identity', 'model_releases', 'model_serving']` |
| openclaw-openclaw-88400 | blind | `['config', 'model_serving']` | `['config']` | `['config']` |
| openclaw-openclaw-65640 | current | `['acp', 'acpx', 'reliability', 'sessions']` | `['acp', 'reliability', 'sessions']` | `['acp', 'acpx', 'reliability', 'sessions']` |
| openclaw-openclaw-68204 | current | `['acp', 'agent_runtime', 'sessions', 'telemetry_usage']` | `['acp', 'agent_runtime', 'telemetry_usage']` | `['acp', 'agent_runtime', 'sessions', 'telemetry_usage']` |
| openclaw-openclaw-76724 | current | `['mcp_tooling', 'ui_tui']` | `['mcp_tooling']` | `['mcp_tooling', 'ui_tui']` |
| openclaw-openclaw-84732 | current | `['chat_integrations', 'notifications', 'reliability']` | `['chat_integrations', 'reliability']` | `['chat_integrations', 'notifications', 'reliability']` |
| openclaw-openclaw-87277 | current | `['model_releases', 'model_serving', 'reliability']` | `['model_releases', 'model_serving']` | `['model_releases', 'model_serving', 'reliability']` |
