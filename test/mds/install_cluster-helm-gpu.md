使用 Helm Chart 在支持 GPU 的情况下运行 Milvus
本页说明如何使用 Helm Chart 启动支持 GPU 的 Milvus 实例。
概述
Helm 使用一种称为图表的打包格式。图表是描述一组相关 Kubernetes 资源的文件 Collection。Milvus 提供了一组图表来帮助你部署 Milvus 依赖项和组件。
Milvus Helm Chart
是一个使用 Helm 包管理器在 Kubernetes (K8s) 集群上引导 Milvus 部署的解决方案。
前提条件
安装 Helm CLI
。
创建带有 GPU 工作节点的 K8s 集群
。
安装
StorageClass
。您可以按以下步骤检查已安装的 StorageClass。
$ kubectl get sc

NAME                  PROVISIONER                  RECLAIMPOLICY    VOLUMEBIINDINGMODE    ALLOWVOLUMEEXPANSION     AGE
standard (default)    k8s.io/minikube-hostpath     Delete           Immediate
false
安装前请检查
硬件和软件要求
。
如果在绘制镜像时遇到任何问题，请通过
community@zilliz.com
联系我们并提供问题详情，我们将为您提供必要的支持。
为 Milvus 安装 Helm 图表
Helm 是一个 K8s 软件包管理器，可以帮助你快速部署 Milvus。
添加 Milvus Helm 资源库。
$ helm repo
add
milvus https:
//zilliztech.github.io/milvus-helm/
https://milvus-io.github.io/milvus-helm/
上的 Milvus Helm Charts 软件仓库已经存档，你可以从
https://zilliztech.github.io/milvus-helm/
获取进一步更新，具体如下：
helm repo add zilliztech https://zilliztech.github.io/milvus-helm
helm repo update
#
upgrade existing helm release
helm upgrade my-release zilliztech/milvus
归档软件源仍可用于 4.0.31 之前的图表。对于后续版本，请使用新版本库。
在本地更新图表。
$
helm repo update
启动 Milvus
安装 Helm 图表后，就可以在 Kubernetes 上启动 Milvus。在本节中，我们将指导你完成启动支持 GPU 的 Milvus 的步骤。
您应该使用 Helm 启动 Milvus，具体方法是指定版本名称、图表和您期望更改的参数。在本指南中，我们使用
my-release
作为版本名称。要使用不同的版本名称，请将以下命令中的
my-release
替换为您正在使用的版本名称。
Milvus 允许您为 Milvus 分配一个或多个 GPU 设备。
1.分配单个 GPU 设备
支持 GPU 的 Milvus 允许您分配一个或多个 GPU 设备。
Milvus 集群
cat
<<
EOF > custom-values.yaml
dataNode:
  resources:
    requests:
      nvidia.com/gpu: "1"
    limits:
      nvidia.com/gpu: "1"
queryNode:
  resources:
    requests:
      nvidia.com/gpu: "1"
    limits:
      nvidia.com/gpu: "1"
EOF
$ helm install my-release milvus/milvus -f custom-values.yaml
独立的 Milvus
cat
<<
EOF > custom-values.yaml
standalone:
  resources:
    requests:
      nvidia.com/gpu: "1"
    limits:
      nvidia.com/gpu: "1"
EOF
$ helm install my-release milvus/milvus --
set
cluster.enabled=
false
--
set
etcd.replicaCount=1 --
set
minio.mode=standalone --
set
pulsarv3.enabled=
false
-f custom-values.yaml
2.分配多个 GPU 设备
除了单个 GPU 设备，您还可以为 Milvus 分配多个 GPU 设备。
Milvus 集群
cat
<<
EOF > custom-values.yaml
dataNode:
  resources:
    requests:
      nvidia.com/gpu: "2"
    limits:
      nvidia.com/gpu: "2"
queryNode:
  resources:
    requests:
      nvidia.com/gpu: "2"
    limits:
      nvidia.com/gpu: "2"
EOF
在上述配置中，有四个可用 CPU，每个数据节点和查询节点使用两个 GPU。要为数据节点和查询节点分配不同的 GPU，可以通过在配置文件中设置
extraEnv
来相应修改配置，具体如下：
cat
<<
EOF > custom-values.yaml
dataNode:
  resources:
    requests:
      nvidia.com/gpu: "1"
    limits:
      nvidia.com/gpu: "1"
  extraEnv:
    - name: CUDA_VISIBLE_DEVICES
      value: "0"
queryNode:
  resources:
    requests:
      nvidia.com/gpu: "1"
    limits:
      nvidia.com/gpu: "1"
  extraEnv:
    - name: CUDA_VISIBLE_DEVICES
      value: "1"
EOF
$ helm install my-release milvus/milvus -f custom-values.yaml
版本名称只能包含字母、数字和破折号。版本名称中不允许使用圆点。
在使用 Helm 安装 Milvus 时，默认命令行会安装群集版本的 Milvus。独立安装 Milvus 时需要进一步设置。
根据
Kuberenetes 的废弃 API 迁移指南
，PodDisruptionBudget 的
policy/v1beta1
API 版本自 v1.25 起不再提供服务。建议您迁移清单和 API 客户端，改用
policy/v1
API 版本。
对于仍在 Kuberenetes v1.25 及更高版本上使用 PodDisruptionBudget 的
policy/v1beta1
API 版本的用户，作为一种变通方法，您可以运行以下命令来安装 Milvus：
helm install my-release milvus/milvus --set pulsar.bookkeeper.pdb.usePolicy=false,pulsar.broker.pdb.usePolicy=false,pulsar.proxy.pdb.usePolicy=false,pulsar.zookeeper.pdb.usePolicy=false
请参阅
Milvus Helm 图表
和
Helm
了解更多信息。
Milvus 单机版
cat
<<
EOF > custom-values.yaml
dataNode:
  resources:
    requests:
      nvidia.com/gpu: "2"
    limits:
      nvidia.com/gpu: "2"
queryNode:
  resources:
    requests:
      nvidia.com/gpu: "2"
    limits:
      nvidia.com/gpu: "2"
EOF
在上述配置中，有四个可用 CPU，每个数据节点和查询节点使用两个 GPU。要为数据节点和查询节点分配不同的 GPU，可以通过在配置文件中设置 extraEnv 来相应修改配置，具体如下：
cat
<<
EOF > custom-values.yaml
dataNode:
  resources:
    requests:
      nvidia.com/gpu: "1"
    limits:
      nvidia.com/gpu: "1"
  extraEnv:
    - name: CUDA_VISIBLE_DEVICES
      value: "0"
queryNode:
  resources:
    requests:
      nvidia.com/gpu: "1"
    limits:
      nvidia.com/gpu: "1"
  extraEnv:
    - name: CUDA_VISIBLE_DEVICES
      value: "1"
EOF
$ helm install my-release milvus/milvus --
set
cluster.enabled=
false
--
set
etcd.replicaCount=1 --
set
minio.mode=standalone --
set
pulsarv3.enabled=
false
-f custom-values.yaml
2.检查 Milvus 状态
运行以下命令检查 Milvus 状态：
$ kubectl get pods
Milvus 启动后，
READY
列会显示所有 pod 的
1/1
。
Milvus 集群
NAME                                             READY  STATUS   RESTARTS  AGE
my-release-etcd-0                                  1/1     Running     0             3m24s
my-release-etcd-1                                  1/1     Running     0             3m24s
my-release-etcd-2                                  1/1     Running     0             3m24s
my-release-milvus-datanode-698dbf7d77-rjkkq        1/1     Running     0             3m24s
my-release-milvus-mixcoord-856d666559-rpj8z        1/1     Running     0             3m24s
my-release-milvus-proxy-7f7cf47689-pzltw           1/1     Running     0             3m24s
my-release-milvus-querynode-7fb6d5b5f8-92phj       1/1     Running     0             3m24s
my-release-milvus-streamingnode-5867bfbcbf-cg9xx   1/1     Running     0             3m24s
my-release-minio-0                                 1/1     Running     0             3m24s
my-release-minio-1                                 1/1     Running     0             3m24s
my-release-minio-2                                 1/1     Running     0             3m24s
my-release-minio-3                                 1/1     Running     0             3m24s
my-release-pulsarv3-bookie-0                       1/1     Running     0             3m24s
my-release-pulsarv3-bookie-1                       1/1     Running     0             3m24s
my-release-pulsarv3-bookie-2                       1/1     Running     0             3m24s
my-release-pulsarv3-bookie-init-p8hcq              0/1     Completed   0             3m24s
my-release-pulsarv3-broker-0                       1/1     Running     0             3m24s
my-release-pulsarv3-broker-1                       1/1     Running     0             3m24s
my-release-pulsarv3-proxy-0                        1/1     Running     0             3m24s
my-release-pulsarv3-proxy-1                        1/1     Running     0             3m24s
my-release-pulsarv3-pulsar-init-8kjsj              0/1     Completed   0             3m24s
my-release-pulsarv3-recovery-0                     1/1     Running     0             3m24s
my-release-pulsarv3-zookeeper-0                    1/1     Running     0             3m24s
my-release-pulsarv3-zookeeper-1                    1/1     Running     0             3m24s
my-release-pulsarv3-zookeeper-2                    1/1     Running     0             3m24s
Milvus Standalone
NAME                                               READY   STATUS      RESTARTS   AGE
my-release-etcd-0                                  1/1     Running     0          30s
my-release-milvus-standalone-54c4f88cb9-f84pf      1/1     Running     0          30s
my-release-minio-5564fbbddc-mz7f5                  1/1     Running     0          30s
3.将本地端口转发给 Milvus
确认 Milvus 服务器正在监听哪个本地端口。用自己的 pod 名称替换 pod 名称。
$ kubectl get pod my-release-milvus-proxy-6bd7f5587-ds2xv --template
=
'{{(index (index .spec.containers 0).ports 0).containerPort}}{{"\n"}}'
19530
然后，运行以下命令将本地端口转发到 Milvus 服务的端口。
$ kubectl port-forward service/my-release-milvus 27017:19530
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
$ kubectl port-forward --address 0.0.0.0 service/my-release-milvus 27017:19530
Forwarding from 0.0.0.0:27017 -> 19530
现在，你可以使用转发的端口连接 Milvus。
访问 Milvus WebUI
Milvus 配备了一个名为 Milvus WebUI 的内置图形用户界面工具，可通过浏览器访问。Milvus Web UI 采用简单直观的界面，增强了系统的可观察性。你可以使用 Milvus Web UI 观察 Milvus 组件和依赖关系的统计和指标，检查数据库和 Collections 的详细信息，并列出详细的 Milvus 配置。有关 Milvus Web UI 的详细信息，请参阅
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
运行以下命令卸载 Milvus。
$ helm uninstall my-release
下一步
安装 Milvus 后，您可以
查看
快速入门
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