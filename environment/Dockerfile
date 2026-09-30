# hash:sha256:811ae7c1ed9441122d5bd8d1efb50d22716c7961d0bebe257a7bf293f927cd0e
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/mambaforge3:23.1.0-4-python3.10.12-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_ASKPASS
COPY git-ask-pass /

RUN pip install -U --no-cache-dir \
    aind-data-schema==2.8.1 \
    log-schema==0.2.10.dev1 \
    numpy==2.2.3
