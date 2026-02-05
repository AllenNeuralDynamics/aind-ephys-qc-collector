# hash:sha256:c694d1d4a3075751d0c1043e45dd2a23919f07f08b97fb9f8fbbf3e620ac99cc
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/mambaforge3:23.1.0-4-python3.10.12-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_ASKPASS
COPY git-askpass /

RUN pip install -U --no-cache-dir \
    aind-data-schema==2.4.0 \
    numpy==2.2.3
