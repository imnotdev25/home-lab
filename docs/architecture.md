# Architecture

## Design goals

The lab separates public applications, home-network workloads, and private
administration while allowing the machines to share compute when appropriate.
The home-server laptop remains the primary local host; the Oracle Cloud VPS is
the public application host; and the Radxa boards provide network and utility
roles.

## Node inventory

| Location | Node | Resources | Primary responsibilities |
| --- | --- | --- | --- |
| Home | Void Linux laptop | Intel 7th-generation i3, 8 GB RAM, 1 TB NVMe | Headless home server, Podman media stack, Jellyfin, Hermes |
| Home | Radxa Cubie A5E | 2 GB RAM, 128 GB storage | Router; [DIY Gaming Router](https://github.com/imnotdev25/DIY-Gaming-Router) |
| Home | Radxa Cubie A7A | 6 GB RAM, 32 GB eMMC | General-purpose SBC node |
| Home | Radxa ZERO 3E | 1 GB RAM, 64 GB storage | AdGuard DNS filtering |
| Cloud | Oracle Cloud VPS | Provider-managed resources | Coolify and public self-hosted applications |

## Network and compute planes

### Private management: Tailscale

Tailscale is installed on every lab instance. It is the preferred path for
remote administration and private service access. Management interfaces should
not be exposed publicly simply because they are reachable over Tailscale.

### Distributed scheduling: Nomad

Nomad connects the instances into a shared compute pool. A job should declare
its resource and placement requirements so storage-bound, network-sensitive,
or low-memory services land on a suitable node. In particular, do not schedule
a workload needing the home media library onto the cloud VPS unless its storage
and data-transfer requirements have been explicitly designed for that move.

### Public ingress

Home Assistant uses Cloudflare Tunnel for internet access. Internet traffic
terminates at Cloudflare before reaching the home service; do not expose the
Home Assistant management port directly on the router. Public VPS applications
are managed by Coolify and should have an explicit authentication and backup
plan before publication.

## Identity boundary

Logto is the OIDC identity provider. Applications such as Karakeep use it for
central authentication. Client secrets, signing keys, callback URLs, and
Cloudflare credentials are deployment secrets, not repository content.
