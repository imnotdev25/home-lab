# Operations

## Monitoring

Beszel monitors components across the lab, including the home server and Oracle
Cloud VPS workloads. Monitor the Radxa nodes where agents are available. At a
minimum, review availability, disk usage, memory pressure, CPU temperature, and
container or service health.

## Nomad

Nomad makes the instances available as a shared compute pool. Before deploying
a job, check that its resource request, network exposure, storage locality, and
architecture are compatible with its target nodes. Label nodes by role and
capacity so routing, DNS, media storage, and low-memory SBC duties are not
scheduled accidentally.

## Tailscale

Tailscale is the standard path for remote access. Use its device inventory to
remove retired instances and confirm that access policies follow the least
privilege principle. Prefer Tailscale access for administration even when a
service also has a public Cloudflare or VPS route.

## Routine checklist

1. Review Beszel alerts and disk capacity on the home server and VPS.
2. Confirm that Nomad clients are healthy and that jobs remain on appropriate
   nodes.
3. Check the Tailscale device list for stale or unexpected devices.
4. Verify backups and perform a restore test for stateful services, especially
   Immich, Logto, Langfuse, and media-service configuration.
5. Upgrade one component at a time and keep a documented rollback path.

## Incident priorities

1. Preserve access: retain a private Tailscale route or local console path.
2. Protect identity: recover Logto before broad application authentication
   changes.
3. Protect state: stop destructive actions and verify backup freshness before
   repairing databases or storage.
4. Restore the smallest affected service first; avoid broad restarts that hide
   the original failure.
