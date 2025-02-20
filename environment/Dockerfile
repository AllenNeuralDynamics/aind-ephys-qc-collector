# hash:sha256:c7f6418843deb068783df2b92a9e1263d24e6dd201f000dbda1a20f34fc3e198
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/mambaforge3:23.1.0-4-python3.10.12-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN pip install -U --no-cache-dir \
    aind-data-schema==1.3.0 \
    numpy==2.2.3
