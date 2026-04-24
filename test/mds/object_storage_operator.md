使用 Milvus Operator 配置对象存储
Milvus 使用 MinIO 或 S3 作为对象存储来持久化大型文件，如索引文件和二进制日志。本主题介绍如何在使用 Milvus Operator 安装 Milvus 时配置对象存储依赖关系。有关详细信息，请参阅 Milvus Operator 存储库中的
使用 Milvus Operator 配置对象存储
。
本主题假设您已部署 Milvus Operator。
有关详细信息，请参阅
部署 Milvus Operator
。
您需要指定使用 Milvus Operator 启动 Milvus 群集的配置文件。
kubectl
apply
-f
https://raw.githubusercontent.com/zilliztech/milvus-operator/main/config/samples/milvus_cluster_default.yaml
您只需编辑
milvus_cluster_default.yaml
中的代码模板，即可配置第三方依赖关系。下文将分别介绍如何配置对象存储、etcd 和 Pulsar。
配置对象存储
Milvus 集群使用 MinIO 或 S3 作为对象存储来持久化大型文件，如索引文件和二进制日志。在
spec.dependencies.storage
下添加必填字段以配置对象存储，可能的选项有
external
和
inCluster
。
内部对象存储
默认情况下，Milvus Operator 会为 Milvus 部署一个集群内 MinIO。下面是一个配置示例，演示如何将该 MinIO 用作内部对象存储。
apiVersion:
milvus.io/v1beta1
kind:
Milvus
metadata:
name:
my-release
labels:
app:
milvus
spec:
# Omit other fields ...
dependencies:
# Omit other fields ...
storage:
inCluster:
values:
mode:
standalone
resources:
requests:
memory:
100Mi
deletionPolicy:
Delete
# Delete | Retain, default: Retain
pvcDeletion:
true
# default: false
应用上述配置后，集群内 MinIO 将以独立模式运行，内存上限为 100Mi。请注意
deletionPolicy
字段指定了群集内 MinIO 的删除策略。其默认值为
Delete
，并有
Retain
作为替代选项。
Delete
表示在停止 Milvus 实例时删除群集内对象存储。
Retain
表示集群内对象存储作为依赖服务保留，供以后启动 Milvus 实例时使用。
pvcDeletion
字段指定在删除群集内 MinIO 时是否删除 PVC（持久卷要求）。
inCluster.values
下的字段与 Milvus Helm Chart 中的字段相同，你可以
在这里
找到它们。
外部对象存储
在模板 YAML 文件中使用
external
表示使用外部对象存储服务。要使用外部对象存储，需要在 Milvus CRD 中正确设置
spec.dependencies.storage
和
spec.config.minio
下的字段。
使用亚马逊网络服务（AWS）S3 作为外部对象存储
按 AK/SK 配置 AWS S3 访问权限
通常可以通过一对访问密钥和访问秘钥访问 S3 存储桶。您可以创建一个
Secret
对象，将它们存储在 Kubernetes 中，如下所示：
# # change the <parameters> to match your environment
apiVersion:
v1
kind:
Secret
metadata:
name:
my-release-s3-secret
type:
Opaque
stringData:
accesskey:
<my-access-key>
secretkey:
<my-secret-key>
然后就可以配置 AWS S3 存储桶作为外部对象存储：
# # change the <parameters> to match your environment
apiVersion:
milvus.io/v1beta1
kind:
Milvus
metadata:
name:
my-release
labels:
app:
milvus
spec:
# Omit other fields ...
config:
minio:
# your bucket name
bucketName:
<my-bucket>
# Optional, config the prefix of the bucket milvus will use
rootPath:
milvus/my-release
useSSL:
true
dependencies:
storage:
# enable external object storage
external:
true
type:
S3
# MinIO | S3
# the endpoint of AWS S3
endpoint:
s3.amazonaws.com:443
# the secret storing the access key and secret key
secretRef:
"my-release-s3-secret"
通过 AssumeRole 配置 AWS S3 访问
或者，你也可以让 Milvus 使用
AssumeRole
访问你的 AWS S3 存储桶，这样只涉及临时凭据，而不是你的实际 AK/SK。
如果你希望这样做，你需要在 AWS 控制台上准备一个角色，并获取其 ARN，通常是
arn:aws:iam::<your account id>:role/<role-name>
的形式。
然后创建一个
ServiceAccount
对象，将其存储在 Kubernetes 中，如下所示：
apiVersion:
v1
kind:
ServiceAccount
metadata:
name:
my-release-sa
annotations:
eks.amazonaws.com/role-arn:
<my-role-arn>
全部设置完成后，在模板 YAML 文件中引用上述
ServiceAccount
，并将
spec.config.minio.useIAM
设置为
true
，以启用 AssumeRole。
apiVersion:
milvus.io/v1beta1
kind:
Milvus
metadata:
name:
my-release
labels:
app:
milvus
spec:
# Omit other fields ...
components:
# use the above ServiceAccount
serviceAccountName:
my-release-sa
config:
minio:
# enable AssumeRole
useIAM:
true
# Omit other fields ...
dependencies:
storage:
# Omit other fields ...
#
Note:
you must use regional endpoint here, otherwise the minio client that milvus uses will fail to connect
endpoint:
s3.<my-bucket-region>.amazonaws.com:443
secretRef:
""
# we don't need to specify the secret here
使用谷歌云存储（GCS）作为外部对象存储
AWS S3 对象存储不是唯一的选择。您也可以使用其他公共云提供商的对象存储服务，如 Google Cloud。
通过 AK/SK 配置 GCS 访问
配置大多与使用 AWS S3 相似。你仍然需要创建一个
Secret
对象，以便在 Kubernetes 中存储凭证。
# # change the <parameters> to match your environment
apiVersion:
v1
kind:
Secret
metadata:
name:
my-release-gcp-secret
type:
Opaque
stringData:
accesskey:
<my-access-key>
secretkey:
<my-secret-key>
然后，您只需将
endpoint
更改为
storage.googleapis.com:443
，并将
spec.config.minio.cloudProvider
设置为
gcp
，如下所示：
# # change the <parameters> to match your environment
apiVersion:
milvus.io/v1beta1
kind:
Milvus
metadata:
name:
my-release
labels:
app:
milvus
spec:
# Omit other fields ...
config:
minio:
cloudProvider:
gcp
dependencies:
storage:
# Omit other fields ...
endpoint:
storage.googleapis.com:443
通过 AssumeRole 配置 GCS 访问权限
与 AWS S3 类似，如果使用 GKE 作为 Kubernetes 集群，也可以使用
Workload Identity
以临时凭据访问 GCS。
ServiceAccount
的注释与 AWS EKS 不同。您需要指定 GCP 服务账户名称，而不是角色 ARN。
apiVersion:
v1
kind:
ServiceAccount
metadata:
name:
my-release-sa
annotations:
iam.gke.io/gcp-service-account:
<my-gcp-service-account-name>
然后，你就可以将你的 Milvus 实例配置为使用上述
ServiceAccount
，并通过将
spec.config.minio.useIAM
设置为
true
来启用 AssumeRole，如下所示：
labels:
app:
milvus
spec:
# Omit other fields ...
components:
# use the above ServiceAccount
serviceAccountName:
my-release-sa
config:
minio:
cloudProvider:
gcp
# enable AssumeRole
useIAM:
true
# Omit other fields ...
下一步
了解如何使用 Milvus Operator 配置其他 Milvus 依赖项：
使用 Milvus Operator 配置元存储
使用 Milvus Operator 配置消息存储