# Homelab documentation

This directory holds operational documentation for the homelab. It describes
the intended topology and service responsibilities, but never contains
credentials, recovery codes, tunnel tokens, private hostnames, or client
secrets.

| Document | Scope |
| --- | --- |
| [Architecture](architecture.md) | Node placement, compute, network, and trust boundaries |
| [Home automation](home-automation.md) | Home Assistant, RF fan bridge, Cloudflare Tunnel, and OIDC |
| [Media server](media-server.md) | Podman YAMS deployment, storage, ports, and lifecycle |
| [Cloud services](cloud-services.md) | Oracle Cloud VPS workloads and ownership |
| [Operations](operations.md) | Nomad, Tailscale, Beszel, and routine checks |

For the Radxa enclosure fabrication guide, see
[`../radxa-enclosure/README.md`](../radxa-enclosure/README.md).
