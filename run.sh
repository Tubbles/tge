#!/usr/bin/env bash

set -x

# Automatically update steamdeck
if uname -a | grep -iq steamdeck; then
    git pull && podman build -t tge-builder .
fi

rm -fr build dist
./docker.sh pyinstaller --bootloader-ignore-signals --noconfirm ./editor.py
./docker.sh pyinstaller --bootloader-ignore-signals --noconfirm ./log_printer.py

# Run editor
# (
#     cd dist/editor/_internal/
#     ln -s libpython3.10.so.1.0 libpython3.10.so
# )
cat /dev/null > log
dist/editor/editor | tee -a log

# Run log printer
# (
#     cd dist/log_printer/_internal/
#     ln -s libpython3.10.so.1.0 libpython3.10.so
# )
dist/log_printer/log_printer
