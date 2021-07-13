# kubernetes-inventory

Create a kubernetes inventory report and upload it to a S3 bucket

Currently collect :

- cluster version
- nodes
- for each namespace :
  - DaemonSets
  - StatefulSets
  - Deployments
  - Cronjobs
- Velero backups

This report can then be imported in an inventory tool, for example OCS inventory.


## Installation

```
# you have to create a dedicated namespace to install the chart.
kubectl create namespace lbn-inventory

# Add helm repository
helm repo add linkbynet https://linkbynet.github.io/kubernetes-repo-helm

helm upgrade --install kubernetes-inventory \
        --set aws.access_key_id=… \
        --set aws.secret_access_key=… \
        --set s3.bucket=… \
        --set kube.cluster=… \
        --set lbnref=… \
        … \ 
        linkbynet/kubernetes-inventory
```

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| inventory.image | string | `linkby/kubernetes-inventory` | Image repository |
| inventory.tag   | string | `latest` | Image tag |
| aws.access_key_id | string | `nil` | AWS access key id |
| aws.secret_access_key | string | `nil` | AWS secret access key |
| s3.bucket | string | `nil` | bucket name |
| s3.folder | string | `Kubernetes` | bucket folder |
| s3.region | string | `eu-west-1` | bucket folder |
| proxy | string | `nil` | HTTP/HTTPS proxy |
| kube.cluster | string | `nil` | Cluster name |
| lbnref | string | `nil` | Cluster identifier (CMDB Id…) |
