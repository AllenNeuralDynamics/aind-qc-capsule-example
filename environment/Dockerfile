# hash:sha256:27ab782f2d1088f30f170d2f9b6c9dee928ca52a53227471540104c341a41853
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/py-r:python3.10.12-R4.2.3-IRkernel-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN pip install -U --no-cache-dir \
    aind-data-schema==1.1.0 \
    aws-requests-auth==0.4.3 \
    boto3==1.35.37

COPY postInstall /
RUN /postInstall
