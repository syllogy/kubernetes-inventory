FROM docker.io/library/python:3-slim

RUN mkdir /lbn
RUN pip install kubernetes invoke boto3

RUN apt-get update \
 && apt-get install --no-install-recommends -y curl \
 && rm -rf /var/lib/apt/lists/*

RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
 && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl \
 && rm kubectl

RUN curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 \
 && chmod 700 get_helm.sh \
 && ./get_helm.sh \
 && rm get_helm.sh

COPY  inventory.py inventory.sh push_on_s3.py /lbn/
