# syntax=docker/dockerfile:1
FROM docker.io/ubuntu:22.04 AS tge-builder

RUN apt update && apt install -y \
    libglib2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    pip \
    python3 \
    && rm -fr /var/lib/apt/lists/*

RUN pip install \
    jurigged==0.5.8 \
    numpy==2.0.1 \
    pygame==2.6.0 \
    pyinstaller==6.10.0
