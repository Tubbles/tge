# syntax=docker/dockerfile:1
FROM docker.io/ubuntu:22.04 AS tge-builder

RUN apt update -y
RUN apt install -y python3
RUN apt install -y pip

RUN pip install \
    numpy==1.26.4 \
    pgzero==1.2.1 \
    pygame==2.5.2

RUN apt install -y \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6

# RUN apt install -y \
#     xauth

RUN apt install -y \
    libsdl2-mixer-2.0-0
