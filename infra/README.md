# Infrastructure scripts

Scripts in this directory create or update infrastructure that is described in
the repository. They are intentionally conservative: they do not remove
containers, pods, images, volumes, or media files.

## Media server

[`media-server/deploy-yams-pod.sh`](media-server/deploy-yams-pod.sh) creates
the rootful `yams_pod` Podman pod and starts the recorded YAMS services:
qBittorrent, SABnzbd, Sonarr, Radarr, Lidarr, Bazarr, and Prowlarr.

```sh
./infra/media-server/deploy-yams-pod.sh
```

It defaults to the deployment's current paths and IDs:

| Setting | Default |
| --- | --- |
| `MEDIA_ROOT` | `/home/boss/yams-media` |
| `CONFIG_ROOT` | `/opt/yams/config` |
| `PUID` / `PGID` | `1000` / `1000` |

Override them when applying the script to another machine:

```sh
MEDIA_ROOT=/srv/media CONFIG_ROOT=/srv/yams/config PUID=1000 PGID=1000 \
  ./infra/media-server/deploy-yams-pod.sh
```

The script will create the individual application configuration directories
with the supplied UID and GID. It refuses to create `MEDIA_ROOT`, preventing an
accidental empty library mount. Create or mount that directory first.

Jellyfin's port (`8096`) is reserved in the pod, but its container definition
is not yet recorded in this repository. Add it only after its storage, user,
and transcoding-device requirements have been documented.
