# Oracle Cloud VPS services

The Oracle Cloud VPS hosts the public, self-hosted application group. Coolify
is the deployment manager for these services. Hermes is an exception: it stays
on the Void Linux home-server laptop.

| Service | Purpose | Operational note |
| --- | --- | --- |
| Coolify | Application deployment and management | Owns VPS application lifecycle |
| Karakeep | Bookmarking | Uses Logto for identity |
| LiteLLM Proxy | AI model gateway | Treat provider credentials as secrets |
| Langfuse | AI-call tracing | Avoid recording sensitive prompt or response data unintentionally |
| Immich | Photo management | Requires a documented storage and backup plan |
| Stirling PDF | PDF tools | Restrict access if documents may contain private data |
| SearXNG | Metasearch | Review upstream and outgoing-network policies |
| Logto | OIDC identity provider | Protect signing keys, database, and recovery access |

## Service ownership

Coolify manages deployment configuration; Logto manages identity for
OIDC-enabled applications; Beszel observes component health; and Tailscale
provides private administrative access. Each application should have a recorded
backup location, restore procedure, upgrade owner, and alert destination before
it is treated as a relied-upon service.
