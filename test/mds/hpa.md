为 Milvus 配置水平 Pod 自动扩展 (HPA)
概述
水平 Pod 自动扩展（HPA）是 Kubernetes 的一项功能，可根据 CPU 或内存等资源利用率自动调整部署中 Pod 的数量。在 Milvus 中，HPA 可应用于
proxy
,
queryNode
,
dataNode
和
indexNode
等无状态组件，以根据工作负载变化动态扩展集群。
本指南介绍如何使用 Milvus 操作符为 Milvus 组件配置 HPA。
前提条件
使用 Milvus Operator 部署的运行中的 Milvus 群集。
访问
kubectl
以管理 Kubernetes 资源。
熟悉 Milvus 架构和 Kubernetes HPA。
使用 Milvus Operator 配置 HPA
要在由 Milvus Operator 管理的 Milvus 群集中启用 HPA，请按照以下步骤操作：
将副本设置为 -1
：
在 Milvus 自定义资源 (CR) 中，将希望使用 HPA 进行缩放的组件的
replicas
字段设置为
-1
。这将缩放控制权委托给 HPA，而不是操作符。您可以直接编辑 CR 或使用以下
kubectl patch
命令快速切换到 HPA 控制：
kubectl patch milvus <your-release-name> --
type
=
'json'
-p=
'[{"op": "replace", "path": "/spec/components/proxy/replicas", "value": -1}]'
将
<your-release-name>
替换为您的 Milvus 集群名称。
要验证更改是否已应用，请运行：
kubectl get milvus <your-release-name> -o jsonpath=
'{.spec.components.proxy.replicas}'
预期输出应为
-1
，确认
proxy
组件现在处于 HPA 控制之下。
或者，您也可以在 CR YAML 中定义它：
apiVersion:
milvus.io/v1beta1
kind:
Milvus
metadata:
name:
<your-release-name>
spec:
mode:
cluster
components:
proxy:
replicas:
-1
定义 HPA 资源
：
创建 HPA 资源，以部署所需的组件。下面是
proxy
组件的示例：
apiVersion:
autoscaling/v2
kind:
HorizontalPodAutoscaler
metadata:
name:
my-release-milvus-proxy-hpa
spec:
scaleTargetRef:
apiVersion:
apps/v1
kind:
Deployment
name:
my-release-milvus-proxy
minReplicas:
2
maxReplicas:
10
metrics:
-
type:
Resource
resource:
name:
cpu
target:
type:
Utilization
averageUtilization:
60
-
type:
Resource
resource:
name:
memory
target:
type:
Utilization
averageUtilization:
60
behavior:
scaleUp:
policies:
-
type:
Pods
value:
1
periodSeconds:
30
scaleDown:
stabilizationWindowSeconds:
300
policies:
-
type:
Pods
value:
1
periodSeconds:
60
将
metadata.name
和
spec.scaleTargetRef.name
中的
my-release
替换为实际的 Milvus 群集名称（如
<your-release-name>-milvus-proxy-hpa
和
<your-release-name>-milvus-proxy
）。
应用 HPA 配置
：
使用以下命令部署 HPA 资源：
kubectl apply -f hpa.yaml
要验证 HPA 是否已成功创建，请运行以下命令：
kubectl get hpa
您应该会看到类似的输出：
NAME                          REFERENCE                            TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
my
-
release
-
milvus
-
proxy
-
hpa   Deployment
/
my
-
release
-
milvus
-
proxy
<
some
>
/
60
%
2
10
2
<
time
>
NAME
和
REFERENCE
字段将反映群集名称（如
<your-release-name>-milvus-proxy-hpa
和
Deployment/<your-release-name>-milvus-proxy
）。
scaleTargetRef
:指定要缩放的部署（如
my-release-milvus-proxy
）。
minReplicas
和 : 设置扩展范围（本例中为 2 至 10 个 Pod）。
maxReplicas
metrics
:配置基于 CPU 和内存利用率的缩放，目标是 60% 的平均使用率。
结论
HPA 允许 Milvus 有效适应不同的工作负载。通过使用
kubectl patch
命令，你可以快速将一个组件切换到 HPA 控制，而无需手动编辑完整的 CR。更多详情，请参阅
Kubernetes HPA 文档
。