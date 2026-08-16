# Media server

## Deployment model

The headless Void Linux home-server laptop uses rootful Podman. The media
applications share the `yams_pod` pod network so their published ports are
defined once at the pod level. Media data is mounted at `/data` for the
downloaders and media managers; each application keeps independent state below
`/opt/yams/config`.

The recorded deployment is automated by
[`../infra/media-server/deploy-yams-pod.sh`](../infra/media-server/deploy-yams-pod.sh).
It creates a pod and missing application configuration directories, but skips
existing containers instead of replacing them.

## Service inventory

| Service | Responsibility | Container image |
| --- | --- | --- |
| qBittorrent | Torrent downloader | `lscr.io/linuxserver/qbittorrent:4.6.3` |
| SABnzbd | Usenet downloader | `lscr.io/linuxserver/sabnzbd:latest` |
| Sonarr | TV-series management | `lscr.io/linuxserver/sonarr:latest` |
| Radarr | Movie management | `lscr.io/linuxserver/radarr:latest` |
| Lidarr | Music management | `lscr.io/linuxserver/lidarr:latest` |
| Bazarr | Subtitle management | `lscr.io/linuxserver/bazarr:latest` |
| Prowlarr | Indexer synchronization | `lscr.io/linuxserver/prowlarr:latest` |
| Jellyfin | Media streaming | Definition not yet recorded here |

## Published pod ports

| Host port | Known assignment |
| ---: | --- |
| 8096 | Reserved for Jellyfin |
| 8081 | qBittorrent web UI |
| 8080, 8989, 7878, 8686, 6767, 9696, 8888 | Reserved by the YAMS pod; keep the active service mapping documented in its application configuration |

## Storage and maintenance

- The default media mount is `/home/boss/yams-media:/data`.
- Application configuration is stored at `/opt/yams/config/<service>`.
- The containers run with `PUID=1000` and `PGID=1000`; keep host ownership
  aligned to avoid libraries or configuration files becoming root-owned.
- The `:z` volume suffix comes from the recorded Podman deployment. Confirm the
  host's SELinux requirements before changing or removing it.
- `latest` image tags are intentionally preserved from the current deployment,
  but should be pinned after a tested upgrade policy is established.

The deployment script does not delete or recreate running containers. Plan
image upgrades, database migrations, and rollback before manually replacing a
container.
