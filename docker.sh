#!/usr/bin/env bash

my_dir="$(dirname "$(realpath "$0")")"
cw_dir="$(pwd)"

pactl load-module module-native-protocol-unix socket="/tmp/pulseaudio.socket" &>/dev/null

cat >> /tmp/pulseaudio.client.conf << 'EOF'
default-server = unix:/tmp/pulseaudio.socket
# Prevent a server running in the container
autospawn = no
daemon-binary = /bin/true
# Prevent the use of shared memory
enable-shm = false
EOF

set -x
# shellcheck disable=SC2086
podman run --rm -it \
    --env DISPLAY=${DISPLAY} \
    --env PULSE_SERVER="unix:/tmp/pulseaudio.socket" \
    --env PULSE_COOKIE="/tmp/pulseaudio.cookie" \
    --network host \
    --userns keep-id \
    --volume "/tmp/pulseaudio.socket":"/tmp/pulseaudio.socket" \
    --volume "/tmp/pulseaudio.client.conf":"/etc/pulse/client.conf" \
    --volume="${HOME}/.Xauthority":"/${cw_dir}/.Xauthority:rw" \
    --volume "${my_dir}":"${my_dir}" \
    --workdir "${cw_dir}" \
    tge-builder "$@"
