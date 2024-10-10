# hash:sha256:6b081f198ef788235d7b808290684c351ba12af1a1fc519be3eaae89bc537241
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/py-r:python3.10.12-R4.2.3-IRkernel-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG AWS_ACCESS_KEY_ID
ARG AWS_DEFAULT_REGION
ARG AWS_SECRET_ACCESS_KEY

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN pip install -U --no-cache-dir \
    aind-data-schema==1.1.0 \
    aws-requests-auth==0.4.3 \
    boto3==1.35.37

COPY postInstall /
RUN /postInstall
