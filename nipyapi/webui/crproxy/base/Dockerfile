FROM alpine:3.10.2
RUN apk add bash \
            curl \
            gzip \
            python3 \
            wget
RUN wget -O /bin/kubectl "https://storage.googleapis.com/kubernetes-release/release/v1.16.0/bin/linux/amd64/kubectl" && \
    chmod +x /bin/kubectl

RUN cd /opt && \
    wget -O - "https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-267.0.0-linux-x86_64.tar.gz" | \
    gunzip | \
    tar xv

RUN ln -s /opt/google-cloud-sdk/bin/gcloud /bin/gcloud
