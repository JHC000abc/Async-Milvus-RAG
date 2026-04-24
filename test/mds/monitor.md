在 Kubernetes 上部署监控服务
本主题介绍如何使用 Prometheus 为 Kubernetes 上的 Milvus 集群部署监控服务。
使用 Prometheus 监控指标
指标是提供系统运行状态信息的指示器。例如，通过度量指标，您可以了解 Milvus 中数据节点消耗了多少内存或 CPU 资源。了解 Milvus 集群中各组件的性能和状态，能让你心中有数，从而做出更好的决策，更及时地调整资源分配。
一般来说，度量指标存储在时间序列数据库（TSDB）中，如
Prometheus
，度量指标记录有时间戳。在监控 Milvus 服务的情况下，可以使用 Prometheus 从出口程序设置的端点提取数据。然后，Prometheus 在
http://<component-host>:9091/metrics
上导出每个 Milvus 组件的指标。
不过，一个组件可能有多个副本，这使得 Prometheus 的手动配置过于复杂。因此，您可以使用 Prometheus
Operator
（Kubernetes 的扩展）来自动有效地管理 Prometheus 监控实例。使用 Prometheus Operator 可以省去手动添加度量目标和服务提供商的麻烦。
通过 ServiceMonitor 自定义资源（CRD），您可以声明式地定义如何监控一组动态服务。它还允许使用标签选择以所需配置监控哪些服务。使用 Prometheus 操作符，您可以引入约定，指定如何暴露度量。新服务可以按照您设置的约定自动发现，而无需手动重新配置。
下图说明了 Prometheus 工作流程。
普罗米修斯架构
前提条件
本教程使用
Kube-prometheus
，省去了安装和手动配置每个监控和警报组件的麻烦。
Kube-prometheus Collections Kubernetes 清单、
Grafana
面板和
Prometheus 规则
与文档和脚本相结合。
在部署监控服务之前，您需要使用 kube-prometheus manifests 目录中的配置创建一个监控栈。
$
git
clone
https://github.com/prometheus-operator/kube-prometheus.git
$
cd
kube-prometheus
$
kubectl apply --server-side -f manifests/setup
$
kubectl
wait
\
        --
for
condition=Established \
        --all CustomResourceDefinition \
        --namespace=monitoring
$
kubectl apply -f manifests/
默认的 prometheus-k8s clusterrole 无法捕获 milvus 的指标，需要打补丁：
kubectl patch clusterrole prometheus-k8s --
type
=json -p=
'[{"op": "add", "path": "/rules/-", "value": {"apiGroups": [""], "resources": ["pods", "services", "endpoints"], "verbs": ["get", "watch", "list"]}}]'
要删除堆栈，请运行
kubectl delete --ignore-not-found=true -f manifests/ -f manifests/setup
。
在 Kubernetes 上部署监控服务
1.访问仪表板
将 Prometheus 服务转发至
9090
端口，将 Grafana 服务转发至
3000
端口。
$
kubectl --namespace monitoring --address 0.0.0.0 port-forward svc/prometheus-k8s 9090
$
kubectl --namespace monitoring --address 0.0.0.0 port-forward svc/grafana 3000
2.启用服务监控器
Milvus Helm 默认未启用 ServiceMonitor。在 Kubernetes 集群中安装 Prometheus 操作符后，可以通过添加参数
metrics.serviceMonitor.enabled=true
来启用它。
使用 Helm
如果安装了 Milvus Helm 图表，您可以通过设置参数
metrics.serviceMonitor.enabled=true
来启用 ServiceMonitor，方法如下。
```
$ helm upgrade my-release milvus/milvus --set metrics.serviceMonitor.enabled=true --reuse-values
```
安装完成后，使用
kubectl
检查 ServiceMonitor 资源。
使用 Milvus 操作符
如果使用 Milvus 操作符安装了 Milvus，可以按如下方法启用 ServiceMonitor。
运行以下命令编辑 Milvus 自定义资源。以下命令假定自定义资源名为
my-release
。
$
kubectl edit milvus my-release
将
spec.components.disableMetric
字段编辑为
false
。
...
spec:
components:
disableMetric:
false
# set to true to disable metrics
...
保存并退出编辑器。
等待操作符核对更改。运行以下命令可检查 Milvus 自定义资源的状态。
$ kubectl
get
milvus my
-
release
-
o yaml
status.components.metrics.serviceMonitor.enabled
字段应为
true
。
3.检查指标
启用 ServiceMonitor 后，您可以访问 Prometheus 仪表板
http://localhost:9090/
。
单击
Status
选项卡，然后单击
Targets
。您应该能看到 Milvus 组件的目标。
Prometheus_targets
单击
Graph
选项卡，在表达式输入框中输入表达式
up{job="default/my-release"}
。你应该能看到 Milvus 组件的度量。
Prometheus_graph
4.检查 ServiceMonitor
$ kubectl
get
servicemonitor
NAME                           AGE
my
-release-milvus              54s
下一步
如果你已经为 Milvus 集群部署了监控服务，你可能还想学习以下内容：
在 Grafana 中可视化 Milvus 指标
为 Milvus 服务创建警报
调整
资源分配
如果你正在寻找有关如何扩展 Milvus 集群的信息：
学习如何
扩展 Milvus 集群
如果你有兴趣升级 Milvus 版本、
请阅读
Milvus 集群升级指南
和
Milvus 单机升级
指南
。