Milvus
OperatorHelm
使用 Helm 图表升级 Milvus 集群
本指南介绍如何使用 Helm Chart 将 Milvus 集群从 v2.5.x 升级到 v2.6.13。
开始之前
版本 2.6.13 的新功能
从 Milvus 2.5.x 升级到 2.6.13 涉及重大架构变化：
协调器合并
：传统的独立协调器 (
dataCoord
,
queryCoord
,
indexCoord
) 已合并为单一的协调器。
mixCoord
新组件
：引入流节点，增强数据处理能力
删除组件
：删除并合并
indexNode
此升级过程可确保向新架构的正常迁移。有关架构变化的更多信息，请参阅
Milvus 架构概述
。
系统要求
系统要求
Helm 版本 >= 3.14.0
Kubernetes 版本 >= 1.20.0
通过 Helm 图表部署 Milvus 集群
兼容性要求：
Milvus v2.6.0-rc1 与 v2.6.13
不兼容
。不支持从候选版本直接升级。
如果您当前正在运行 v2.6.0-rc1，并需要保留数据，请参考
本社区指南
以获取迁移帮助。
在升级到 v2.6.13 之前，您
必须
升级到 v2.5.16 或更高版本，并启用
mixCoordinator
。
消息队列限制
：升级到 Milvus v2.6.13 时，您必须保持当前的消息队列选择。不支持在升级过程中在不同的消息队列系统之间切换。未来版本将支持更改消息队列系统。
自 Milvus Helm 图表 4.2.21 版起，我们引入了 pulsar-v3.x 图表作为依赖。为了向后兼容，请将 Helm 升级到 v3.14 或更高版本，并确保在使用
helm upgrade
时添加
--reset-then-reuse-values
选项。
升级过程
步骤 1：升级 Helm 图表
首先，将您的 Milvus Helm 图表升级到 5.0.0 版本：
helm repo add zilliztech https://zilliztech.github.io/milvus-helm
helm repo update zilliztech
位于
https://milvus-io.github.io/milvus-helm/
的 Milvus Helm 图表 repo 已归档。对于 4.0.31 及更高版本的图表，请使用新版本库
https://zilliztech.github.io/milvus-helm/
。
要检查 Helm 图表版本与 Milvus 版本的兼容性：
helm search repo zilliztech/milvus --versions
本指南假定您安装的是最新版本。如果需要安装特定版本，请相应指定
--version
参数。
步骤 2：使用 mixCoordinator 升级到 v2.5.16
检查您的群集当前是否使用独立的协调器：
kubectl get pods
如果看到单独的协调器 pod (
datacoord
,
querycoord
,
indexcoord
) ，请升级到 v2.5.16 并启用
mixCoordinator
：
helm upgrade my-release zilliztech/milvus \
  --
set
image.all.tag=
"v2.5.16"
\
  --
set
mixCoordinator.enabled=
true
\
  --
set
rootCoordinator.enabled=
false
\
  --
set
indexCoordinator.enabled=
false
\
  --
set
queryCoordinator.enabled=
false
\
  --
set
dataCoordinator.enabled=
false
\
  --reset-then-reuse-values \
  --version=4.2.58
如果群集已使用
mixCoordinator
，只需升级映像即可：
helm upgrade my-release zilliztech/milvus \
  --
set
image.all.tag=
"v2.5.16"
\
  --reset-then-reuse-values \
  --version=4.2.58
等待升级完成：
# Verify all pods are ready
kubectl get pods
步骤 3：升级到 v2.6.13
在
mixCoordinator
上成功运行 v2.5.16 后，升级到 v2.6.13：
helm upgrade my-release zilliztech/milvus \
  --
set
image.all.tag=
"v2.6.13"
\
  --
set
streaming.enabled=
true
\
  --
set
indexNode.enabled=
false
\
  --reset-then-reuse-values \
  --version=5.0.0
验证升级
确认群集正在运行新版本：
# Check pod status
kubectl get pods
# Verify Helm release
helm list
如需其他支持，请查阅
Milvus 文档
或
社区论坛
。