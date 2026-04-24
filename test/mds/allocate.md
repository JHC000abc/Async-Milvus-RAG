在 Kubernetes 上分配资源
本主题介绍如何在 Kubernetes 上为 Milvus 群集分配资源。
一般来说，在生产中分配给 Milvus 集群的资源应与机器工作量成比例。分配资源时还应考虑机器类型。虽然您可以在群集运行时更新配置，但我们建议您在
部署群集
之前设置这些值。
有关如何使用 Milvus Operator 分配资源的信息，请参阅
使用 Milvus Operator 分配资源
。
1.查看可用资源
运行
kubectl describe nodes
查看已配置的实例上的可用资源。
2.分配资源
使用 Helm 为 Milvus 组件分配 CPU 和内存资源。
使用 Helm 升级资源会使运行中的 pod 执行滚动更新。
分配资源有两种方法：
使用以下命令
在
YAML
文件中设置参数
使用命令分配资源
如果使用
--set
更新资源配置，需要为每个 Milvus 组件设置资源变量。
Milvus 独立运行
Milvus 集群
helm upgrade my-release milvus/milvus --reuse-values --set standalone.resources.limits.cpu=2 --set standalone.resources.limits.memory=4Gi --set standalone.resources.requests.cpu=0.1 --set standalone.resources.requests.memory=128Mi
helm upgrade my-release milvus/milvus --reuse-values --set dataNode.resources.limits.cpu=2 --set dataNode.resources.limits.memory=4Gi --set dataNode.resources.requests.cpu=0.1 --set dataNode.resources.requests.memory=128Mi
通过设置配置文件分配资源
您还可以通过在
resources.yaml
文件中指定参数
resources.requests
和
resources.limits
来分配 CPU 和内存资源。
dataNode:
resources:
limits:
cpu:
"4"
memory:
"16Gi"
requests:
cpu:
"1"
memory:
"4Gi"
queryNode:
resources:
limits:
cpu:
"4"
memory:
"16Gi"
requests:
cpu:
"1"
memory:
"4Gi"
3.应用配置
运行以下命令将新配置应用到 Milvus 群集。
helm upgrade my-release milvus/milvus --reuse-values -f resources.yaml
如果未指定
resources.limits
，pod 将消耗所有可用的 CPU 和内存资源。因此，请确保指定
resources.requests
和
resources.limits
，以避免在同一实例上的其他运行任务需要消耗更多内存时出现资源过度分配的情况。
有关资源管理的更多信息，请参阅
Kubernetes 文档
。
下一步
你可能还想了解如何
扩展 Milvus 集群
升级 Milvus 集群
升级 Milvus Standalone
如果你已准备好在云上部署集群：
了解如何
使用 Terraform 在亚马逊 EKS 上部署 Milvus
学习如何
使用 Kubernetes 在 GCP 上部署 Milvus 集群
了解如何
使用 Kubernetes 在 Microsoft Azure 上部署 Milvus