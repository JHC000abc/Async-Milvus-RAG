按工作负载身份配置 GCS 访问
本主题介绍如何在使用 Helm 安装 Milvus 时，通过工作负载身份配置 gcs 访问。 更多详情，请参阅
工作负载身份
。
开始之前
请使用 Google Cloud CLI 或 Google Cloud 控制台在群集和节点池上启用 Workload Identity。必须在群集级别启用 Workload Identity，然后才能在节点池上启用 Workload Identity。
配置应用程序以使用 Workload Identity
创建存储桶。
gcloud storage buckets create gs://milvus-testing-nonprod --project=milvus-testing-nonprod --default-storage-class=STANDARD --location=us-west1 --uniform-bucket-level-access
为应用程序创建一个 Kubernetes 服务账户。
kubectl create serviceaccount milvus-gcs-access-sa
为应用程序创建 IAM 服务帐户，或使用现有的 IAM 服务帐户。您可以在组织中的任何项目中使用任何 IAM 服务帐户。
gcloud iam service-accounts create milvus-gcs-access-sa \
    --project=milvus-testing-nonprod
确保 IAM 服务帐户具有所需的角色。您可以使用以下命令授予其他角色：
gcloud projects add-iam-policy-binding milvus-testing-nonprod \
    --member
"serviceAccount:milvus-gcs-access-sa@milvus-testing-nonprod.iam.gserviceaccount.com"
\
    --role
"roles/storage.admin"
\
    --condition=
'title=milvus-testing-nonprod,expression=resource.service == "storage.googleapis.com" && resource.name.startsWith("projects/_/buckets/milvus-testing-nonprod")'
通过在两个服务账户之间添加 IAM 策略绑定，允许 Kubernetes 服务账户冒充 IAM 服务账户。该绑定允许 Kubernetes 服务账户充当 IAM 服务账户。
gcloud iam service-accounts add-iam-policy-binding milvus-gcs-access-sa@milvus-testing-nonprod.iam.gserviceaccount.com \
    --role
"roles/iam.workloadIdentityUser"
\
    --member
"serviceAccount:milvus-testing-nonprod.svc.id.goog[default/milvus-gcs-access-sa]"
用 IAM 服务账户的电子邮件地址注释 Kubernetes 服务账户。
kubectl annotate serviceaccount milvus-gcs-access-sa \
    --namespace default \
    iam.gke.io/gcp-service-account=milvus-gcs-access-sa@milvus-testing-nonprod.iam.gserviceaccount.com
验证工作量身份设置
请参阅 "
工作负载身份
"。在 Pod 内运行以下命令：
curl -H
"Metadata-Flavor: Google"
http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/email
如果结果是
milvus-gcs-access-sa@milvus-testing-nonprod.iam.gserviceaccount.com
，就没问题。
部署 Milvus
helm install -f values.yaml my-release milvus/milvus
values.yaml内容：
cluster:
enabled:
true
service:
type:
LoadBalancer
minio:
enabled:
false
serviceAccount:
create:
false
name:
milvus-gcs-access-sa
externalS3:
enabled:
true
host:
storage.googleapis.com
port:
443
rootPath:
milvus/my-release
bucketName:
milvus-testing-nonprod
cloudProvider:
gcp
useSSL:
true
useIAM:
true