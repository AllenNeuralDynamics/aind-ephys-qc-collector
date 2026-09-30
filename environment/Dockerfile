# hash:sha256:b2d156f9ebb15b418f77c78b4833dbe062580ed15ed62112020eae4804a35a95
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/mambaforge3:23.1.0-4-python3.10.12-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_ASKPASS
COPY git-ask-pass /

RUN pip install -U --no-cache-dir \
    aind-data-schema==2.8.1 \
    log-schema \
    numpy==2.2.3
