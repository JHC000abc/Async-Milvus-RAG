在 Milvus v2.5.x 中使用 Pulsar v2
Milvus 建议你将 Pulsar 升级到 v3 以运行 Milvus v2.5.x，详情请参阅升级
Pulsar
。不过，如果你更喜欢使用 Pulsar v2 与 Milvus v2.5.x，本文将指导你使用 Pulsar v2 运行 Milvus v2.5.x 的程序。
如果你已经有一个正在运行的 Milvus 实例，并希望将其升级到 v2.5.x，但继续使用 Pulsar v2，你可以按照本页的步骤进行操作。
升级 Milvus v2.5.x 时继续使用 Pulsar v2
本节将指导你在将运行中的 Milvus 实例升级到 Milvus v2.5.x 时继续使用 Pulsar v2 的步骤。
针对 Milvus 操作符用户
Milvus Operator 默认兼容 Pulsar v2 升级。您可以参照
使用 Milvus Operator 升级 Milvus 群集
将您的
Milvus
实例升级到 v2.5.x。
升级完成后，您可以继续在 Milvus 实例中使用 Pulsar v2。
对于 Helm 用户
升级前，请确保
Helm 版本高于 v3.12，建议使用最新版本。
更多信息，请参阅
安装 Helm
。
您的 Kubernetes 版本高于 v1.20。
本文中的操作符假定
已在
default
命名空间中安装 Milvus。
Milvus 的版本名称是
my-release
。
在升级 Milvus 之前，您需要更改
values.yaml
文件，指定 Pulsar 版本为 v2。具体步骤如下
获取 Milvus 实例的当前
values.yaml
文件。
namespace=default
release=my-release
helm -n
${namespace}
get values
${release}
-o yaml > values.yaml
cat
values.yaml
编辑
values.yaml
文件，指定 Pulsar 版本为 v2。
# ... omit existing values
pulsar:
enabled:
true
pulsarv3:
enabled:
false
image:
all:
repository:
milvusdb/milvus
tag:
v2.5.0-beta
对于
image
，将
tag
更改为所需的 Milvus 版本（如
v2.5.0-beta
）。
更新 Milvus Helm 图表。
helm repo add milvus https://zilliztech.github.io/milvus-helm
helm repo update milvus
升级 Milvus 实例。
helm -n
$namespace
upgrade
$releaase
milvus/milvus -f values.yaml
使用 Pulsar v2 创建新的 Milvus 实例
本节将指导您使用 Pulsar v2 创建一个新的 Milvus 实例。
针对 Milvus 操作符用户
在部署 Milvus v2.5.x 之前，您需要下载并编辑 Milvus 客户资源定义 (CRD) 文件。有关如何使用 Milvus Operator 安装 Milvus 的详细信息，请参阅
使用 Milvus Operator 安装 Milvus 群集
。
下载 CRD 文件。
wget https://raw.githubusercontent.com/zilliztech/milvus-operator/main/config/samples/milvus_cluster_default.yaml
编辑
milvus_cluster_default.yaml
文件，指定 Pulsar 版本为 v2。
apiVersion:
milvus.io/v1beta1
kind:
Milvus
metadata:
name:
my-release
namespace:
default
labels:
app:
milvus
spec:
mode:
cluster
dependencies:
pulsar:
inCluster:
chartVersion:
pulsar-v2
对于
dependencies
，将
pulsar.inCluster.chartVersion
更改为
pulsar-v2
。
继续执行 "
使用 Milvus Operator 安装 Milvus 群集
"中的步骤，使用编辑后的 CRD 文件部署带有 Pulsar v2 的 Milvus v2.5.x。
kubectl apply -f milvus_cluster_default.yaml
针对 Helm 用户
在部署 Milvus v2.5.x 之前，可以准备一个
values.yaml
文件，或者使用内联参数指定 Pulsar 版本。有关如何使用 Helm
安装
Milvus 的详情，请参阅
使用 Helm 安装 Milvus 群集
。
使用内联参数指定 Pulsar 版本为 v2。
helm install my-release milvus/milvus --
set
pulsar.enabled=
true
,pulsarv3.enabled=
false
使用
values.yaml
文件指定 Pulsar 版本为 v2。
pulsar:
enabled:
true
pulsarv3:
enabled:
false
然后，使用
values.yaml
文件与 Pulsar v2 一起部署 Milvus v2.5.x。
helm install my-release milvus/milvus -f values.yaml