#!/usr/bin/env bash

# Automatically update steamdeck
if uname -a | grep -iq steamdeck; then
    git pull && podman build -t tge-builder .
fi

./docker.sh pyinstaller -y ./editor.py
dist/editor/editor
