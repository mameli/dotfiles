---
name: arr-automation
description: "Add films or series to Radarr/Sonarr with verified writes."
---

# Radarr / Sonarr

1. Read [connection and defaults](references/connection-defaults.md) for inputs, host/key resolution and profile/root/monitor/search defaults.
2. Follow [add and verification](references/add-workflow.md) for API endpoints, payloads, duplicate checks, UI fallback and the result contract.

Prefer the API. Resolve ambiguous works before writing, never expose credentials, and never duplicate an existing canonical ID. Verify the exact entity after a write; distinguish already present from newly created and a requested search from an initiated search.
