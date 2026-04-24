使用 Milvus Operator 在 Kubernetes 中运行 Milvus
本页说明如何使用
Milvus Operator
在 Kubernetes 中启动 Milvus 实例。
概述
Milvus Operator 是一种解决方案，可帮助您在目标 Kubernetes (K8s) 集群中部署和管理完整的 Milvus 服务栈。该堆栈包括所有 Milvus 组件和相关依赖项，如 etcd、Pulsar 和 MinIO。
前提条件
创建 K8s 集群
。
安装一个
StorageClass
。可按以下步骤检查已安装的 StorageClass。
$ kubectl get sc

NAME                  PROVISIONER                  RECLAIMPOLICY    VOLUMEBIINDINGMODE    ALLOWVOLUMEEXPANSION     AGE
standard (default)    k8s.io/minikube-hostpath     Delete           Immediate
false
安装前检查
硬件和软件要求
。
安装 Milvus 前，建议使用
Milvus 大小工具
，根据数据大小估算硬件需求。这有助于确保 Milvus 安装的最佳性能和资源分配。
如果您在拉动映像时遇到任何问题，请通过
community@zilliz.com
联系我们，并提供有关问题的详细信息，我们将为您提供必要的支持。
安装 Milvus 操作符
Milvus Operator 在
Kubernetes 自定义资源
之上定义 Milvus 集群
自定义资源
。定义了自定义资源后，你就能以声明的方式使用 K8s API 并管理 Milvus 部署栈，确保其可扩展性和高可用性。
Helm
Kubectl
使用 Helm 安装 Milvus Operator，请运行以下命令。
$
helm install milvus-operator \
  -n milvus-operator --create-namespace \
  --
wait
--wait-for-jobs \
  https://github.com/zilliztech/milvus-operator/releases/download/v1.3.0/milvus-operator-1.3.0.tgz
安装过程结束后，你将看到类似下面的输出。
NAME: milvus-operator
LAST DEPLOYED: Thu Jul  7 13:18:40 2022
NAMESPACE: milvus-operator
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Milvus Operator Is Starting, use `kubectl get -n milvus-operator deploy/milvus-operator` to check if its successfully installed
If Operator not started successfully, check the checker's log with `kubectl -n milvus-operator logs job/milvus-operator-checker`
Full Installation doc can be found in https://github.com/zilliztech/milvus-operator/blob/main/docs/installation/installation.md
Quick start with `kubectl apply -f https://raw.githubusercontent.com/zilliztech/milvus-operator/main/config/samples/milvus_minimum.yaml`
More samples can be found in https://github.com/zilliztech/milvus-operator/tree/main/config/samples
CRD Documentation can be found in https://github.com/zilliztech/milvus-operator/tree/main/docs/CRD
如果之前安装过 Milvus Operator，请使用以下命令进行升级：
helm upgrade milvus-operator \
  -n milvus-operator --create-namespace \
  --wait --wait-for-jobs \
  https://github.com/zilliztech/milvus-operator/releases/download/v1.3.0/milvus-operator-1.3.0.tgz
运行以下命令安装 Milvus Operator 和
kubectl
。
$
kubectl apply -f https://raw.githubusercontent.com/zilliztech/milvus-operator/main/deploy/manifests/deployment.yaml
安装过程结束后，您将看到类似下面的输出。
namespace/milvus-operator created
customresourcedefinition.apiextensions.k8s.io/milvusclusters.milvus.io created
serviceaccount/milvus-operator-controller-manager created
role.rbac.authorization.k8s.io/milvus-operator-leader-election-role created
clusterrole.rbac.authorization.k8s.io/milvus-operator-manager-role created
clusterrole.rbac.authorization.k8s.io/milvus-operator-metrics-reader created
clusterrole.rbac.authorization.k8s.io/milvus-operator-proxy-role created
rolebinding.rbac.authorization.k8s.io/milvus-operator-leader-election-rolebinding created
clusterrolebinding.rbac.authorization.k8s.io/milvus-operator-manager-rolebinding created
clusterrolebinding.rbac.authorization.k8s.io/milvus-operator-proxy-rolebinding created
configmap/milvus-operator-manager-config created
service/milvus-operator-controller-manager-metrics-service created
service/milvus-operator-webhook-service created
deployment.apps/milvus-operator-controller-manager created
您可以按如下方法检查 Milvus Operator pod 是否正在运行：
$
kubectl get pods -n milvus-operator
NAME                               READY   STATUS    RESTARTS   AGE
milvus-operator-5fd77b87dc-msrk4   1/1     Running   0          46s
部署 Milvus
1.部署 Milvus 群集
一旦运行了 Milvus Operator pod，就可以按如下方式部署 Milvus 群集。
$
kubectl apply -f https://raw.githubusercontent.com/zilliztech/milvus-operator/main/config/samples/milvus_cluster_woodpecker.yaml
上面的命令部署的是以
Woodpecker
作为消息队列（推荐用于 v2.6.13）和包括流节点在内的所有新架构组件的 Milvus 群集。
此部署中的架构要点：
消息队列
：
使用 Woodpecker
（减少基础设施维护）
流节点
：为增强数据处理功能而启用
混合协调器
：合并协调器组件，提高效率
要自定义这些设置，我们建议您使用
Milvus 大小工具
，根据实际数据大小调整配置，然后下载相应的 YAML 文件。要了解有关配置参数的更多信息，请参阅
Milvus 系统配置检查表
。
版本名称只能包含字母、数字和破折号。版本名称中不允许有圆点。
你也可以在独立模式下部署 Milvus 实例，即所有组件都包含在一个 pod 中。为此，请将上述命令中的配置文件 URL 更改为
https://raw.githubusercontent.com/zilliztech/milvus-operator/main/config/samples/milvus_default.yaml
2.检查 Milvus 集群状态
运行以下命令检查 Milvus 集群状态
$
kubectl get milvus my-release -o yaml
一旦你的 Milvus 集群准备就绪，上述命令的输出应该与下面类似。如果
status.status
字段保持
Unhealthy
，您的 Milvus 群集仍在创建中。
apiVersion:
milvus.io/v1alpha1
kind:
Milvus
metadata:
...
status:
conditions:
-
lastTransitionTime:
"xxxx-xx-xxTxx:xx:xxZ"
reason:
StorageReady
status:
"True"
type:
StorageReady
-
lastTransitionTime:
"xxxx-xx-xxTxx:xx:xxZ"
message:
Pulsar
is
ready
reason:
PulsarReady
status:
"True"
type:
PulsarReady
-
lastTransitionTime:
"xxxx-xx-xxTxx:xx:xxZ"
message:
Etcd
endpoints
is
healthy
reason:
EtcdReady
status:
"True"
type:
EtcdReady
-
lastTransitionTime:
"xxxx-xx-xxTxx:xx:xxZ"
message:
All
Milvus
components
are
healthy
reason:
MilvusClusterHealthy
status:
"True"
type:
MilvusReady
endpoint:
my-release-milvus.default:19530
status:
Healthy
Milvus Operator 会创建 Milvus 依赖项，如 etcd、Pulsar 和 MinIO，然后创建 Milvus 组件，如代理、协调器和节点。
Milvus 集群准备就绪后，Milvus 集群中所有 pod 的状态应该与下面类似。
$
kubectl get pods
NAME                                             READY   STATUS    RESTARTS   AGE
my-release-etcd-0                                1/1     Running   0          2m36s
my-release-etcd-1                                1/1     Running   0          2m36s
my-release-etcd-2                                1/1     Running   0          2m36s
my-release-milvus-datanode-58955c65b9-j4j7s      1/1     Running   0          92s
my-release-milvus-mixcoord-686f84968f-jcv5d      1/1     Running   0          92s
my-release-milvus-proxy-646f48fc7c-4lctb         1/1     Running   0          92s
my-release-milvus-querynode-0-d89d7677b-x7j7q    1/1     Running   0          91s
my-release-milvus-streamingnode-556bdcc87c-2qwcc 1/1     Running   0          92s
my-release-minio-0                               1/1     Running   0          2m36s
my-release-minio-1                               1/1     Running   0          2m36s
my-release-minio-2                               1/1     Running   0          2m35s
my-release-minio-3                               1/1     Running   0          2m35s
3.将本地端口转发给 Milvus
运行以下命令获取 Milvus 集群的服务端口。
$
kubectl get pod my-release-milvus-proxy-84f67cdb7f-pg6wf --template
='{{(index (index .spec.containers 0).ports 0).containerPort}}{{"\n"}}'
19530
输出结果显示，Milvus 实例在默认端口
19530
上提供服务。
如果以独立模式部署了 Milvus，请将 pod 名称从
my-release-milvus-proxy-xxxxxxxxxx-xxxxx
更改为
my-release-milvus-xxxxxxxxxx-xxxxx
。
然后，运行以下命令将本地端口转发到 Milvus 服务的端口。
$
kubectl port-forward service/my-release-milvus 27017:19530
Forwarding from 127.0.0.1:27017 -> 19530
可以选择在上述命令中使用
:19530
而不是
27017:19530
，让
kubectl
为你分配一个本地端口，这样你就不必管理端口冲突了。
默认情况下，kubectl 的端口转发只监听
localhost
。如果想让 Milvus 监听所选或所有 IP 地址，请使用
address
标志。下面的命令使端口转发监听主机上的所有 IP 地址。
$
kubectl port-forward --address 0.0.0.0 service/my-release-milvus 27017:19530
Forwarding from 0.0.0.0:27017 -> 19530
现在，你可以使用转发的端口连接 Milvus。
(可选）更新 Milvus 配置
你可以通过调用
patch
命令来查看和更新 Milvus 集群的配置，方法如下：
运行以下命令预览可能的配置。
以下命令假定您要将
spec.components.disableMetric
参数更新为
false
ms。
$
kubectl patch milvus my-release --
type
=
'merge'
\
  -p
'{"spec":{"components":{"disableMetric":false}}}'
\
  --dry-run=client -o yaml
有关适用的配置项目，请参阅
系统配置
。
更新配置。
$
kubectl patch milvus my-release --
type
=
'merge'
\
  -p
'{"spec":{"components":{"disableMetric":false}}}'
访问 Milvus WebUI
Milvus 配备了一个名为 Milvus WebUI 的内置图形用户界面工具，您可以通过浏览器访问该工具。Milvus Web UI 采用简单直观的界面，增强了系统的可观察性。你可以使用 Milvus Web UI 观察 Milvus 组件和依赖关系的统计和指标，检查数据库和 Collections 的详细信息，并列出详细的 Milvus 配置。有关 Milvus Web UI 的详细信息，请参阅
Milvus WebUI
。
要启用对 Milvus Web UI 的访问，需要将代理 pod 的端口转发到本地端口。
$
kubectl port-forward --address 0.0.0.0 service/my-release-milvus 27018:9091
Forwarding from 0.0.0.0:27018 -> 9091
现在，你可以通过
http://localhost:27018
访问 Milvus Web UI。
卸载 Milvus
运行以下命令卸载 Milvus 群集。
$
kubectl delete milvus my-release
使用默认配置删除 Milvus 群集时，不会删除 etcd、Pulsar 和 MinIO 等依赖项。因此，下次安装同一个 Milvus 群集实例时，将再次使用这些依赖项。
要连同 Milvus 群集一起删除依赖项和持久卷主张（PVC），请参阅
配置文件
。
卸载 Milvus 操作符
卸载 Milvus Operator 也有两种方法。
使用 Helm 卸载
使用 kubectl 卸载
使用 Helm 卸载
$
helm -n milvus-operator uninstall milvus-operator
使用 kubectl 卸载
$
kubectl delete -f https://raw.githubusercontent.com/zilliztech/milvus-operator/v1.3.0/deploy/manifests/deployment.yaml
下一步
在 Docker 中安装 Milvus 后，你就可以：
查看
Hello Milvus
，了解 Milvus 的功能。
学习 Milvus 的基本操作：
管理数据库
管理 Collections
管理分区
插入、倒置和删除
单向量搜索
混合搜索
使用 Helm 图表升级 Milvus
。
扩展你的 Milvus 集群
。
在云上部署你的 Milvu 集群：
亚马逊 EKS
谷歌云
微软 Azure
探索
Milvus WebUI
，一个用于 Milvus 可观察性和管理的直观 Web 界面。
探索
Milvus 备份
，一个用于 Milvus 数据备份的开源工具。
探索
Birdwatcher
，用于调试 Milvus 和动态配置更新的开源工具。
探索
Attu
，一个用于直观管理 Milvus 的开源图形用户界面工具。
使用 Prometheus 监控 Milvus
。