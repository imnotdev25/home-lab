#!/bin/sh
# Create the recorded YAMS Podman pod without replacing existing containers.
# Requires Podman and either root access or sudo on the target host.

set -eu

POD_NAME=yams_pod
MEDIA_ROOT=${MEDIA_ROOT:-/home/boss/yams-media}
CONFIG_ROOT=${CONFIG_ROOT:-/opt/yams/config}
PUID=${PUID:-1000}
PGID=${PGID:-1000}

run_as_root() {
  if [ "$(id -u)" -eq 0 ]; then
    "$@"
  elif command -v sudo >/dev/null 2>&1; then
    sudo "$@"
  else
    printf '%s\n' 'error: run as root or install sudo' >&2
    exit 1
  fi
}

podman_cmd() {
  run_as_root podman "$@"
}

ensure_config_dir() {
  run_as_root install -d -m 0750 -o "$PUID" -g "$PGID" "$1"
}

ensure_container() {
  container_name=$1
  shift

  if podman_cmd container exists "$container_name"; then
    printf '%s\n' "Skipping existing container: $container_name"
    return 0
  fi

  podman_cmd run -d --name "$container_name" --pod "$POD_NAME" "$@"
}

if ! command -v podman >/dev/null 2>&1; then
  printf '%s\n' 'error: Podman is required' >&2
  exit 1
fi

if [ ! -d "$MEDIA_ROOT" ]; then
  printf '%s\n' "error: media directory does not exist: $MEDIA_ROOT" >&2
  printf '%s\n' 'Create or mount it before deploying the media stack.' >&2
  exit 1
fi

for service in qbittorrent sabnzbd sonarr radarr lidarr bazarr prowlarr; do
  ensure_config_dir "$CONFIG_ROOT/$service"
done

if podman_cmd pod exists "$POD_NAME"; then
  printf '%s\n' "Using existing pod: $POD_NAME"
else
  podman_cmd pod create \
    --name "$POD_NAME" \
    -p 8096:8096 -p 8081:8081 -p 8080:8080 -p 8989:8989 \
    -p 7878:7878 -p 8686:8686 -p 6767:6767 -p 9696:9696 -p 8888:8888
fi

ensure_container qbittorrent \
  -e "PUID=$PUID" -e "PGID=$PGID" -e WEBUI_PORT=8081 \
  -v "$MEDIA_ROOT:/data" \
  -v "$CONFIG_ROOT/qbittorrent:/config:z" \
  lscr.io/linuxserver/qbittorrent:4.6.3

ensure_container sabnzbd \
  -e "PUID=$PUID" -e "PGID=$PGID" \
  -v "$MEDIA_ROOT:/data" \
  -v "$CONFIG_ROOT/sabnzbd:/config:z" \
  lscr.io/linuxserver/sabnzbd:latest

ensure_container sonarr \
  -e "PUID=$PUID" -e "PGID=$PGID" \
  -v "$MEDIA_ROOT:/data" \
  -v "$CONFIG_ROOT/sonarr:/config:z" \
  lscr.io/linuxserver/sonarr:latest

ensure_container radarr \
  -e "PUID=$PUID" -e "PGID=$PGID" \
  -v "$MEDIA_ROOT:/data" \
  -v "$CONFIG_ROOT/radarr:/config:z" \
  lscr.io/linuxserver/radarr:latest

ensure_container lidarr \
  -e "PUID=$PUID" -e "PGID=$PGID" \
  -v "$MEDIA_ROOT:/data" \
  -v "$CONFIG_ROOT/lidarr:/config:z" \
  lscr.io/linuxserver/lidarr:latest

ensure_container bazarr \
  -e "PUID=$PUID" -e "PGID=$PGID" \
  -v "$MEDIA_ROOT:/data" \
  -v "$CONFIG_ROOT/bazarr:/config:z" \
  lscr.io/linuxserver/bazarr:latest

ensure_container prowlarr \
  -e "PUID=$PUID" -e "PGID=$PGID" \
  -v "$CONFIG_ROOT/prowlarr:/config:z" \
  lscr.io/linuxserver/prowlarr:latest

printf '%s\n' 'YAMS pod deployment complete.'
podman_cmd ps --pod
