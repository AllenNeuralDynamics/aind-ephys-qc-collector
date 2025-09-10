# hash:sha256:18497294ce838fb9f8db387b35f5808eb1ab0730a6448b5470ecdd4b25e93714
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/mambaforge3:23.1.0-4-python3.10.12-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_ASKPASS
COPY git-askpass /

RUN pip install -U --no-cache-dir \
    aind-data-schema==2.0.1 \
    numpy==2.2.3
