# hash:sha256:3b1cd35a070ddf068c18fdee5ec1f49d3fa6c0f00700114c0f3569c7bf782ee5
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/mambaforge3:23.1.0-4-python3.10.12-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_ASKPASS
COPY git-askpass /

RUN pip install -U --no-cache-dir \
    aind-data-schema==2.3.0 \
    numpy==2.2.3
