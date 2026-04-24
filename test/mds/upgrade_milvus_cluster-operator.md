Milvus
OperatorHelm
使用 Milvus Operator 升级 Milvus 群集
本指南介绍如何使用 Milvus Operator 将 Milvus 群集从 v2.5.x 升级到 v2.6.13。
开始之前
v2.6.13 中的新功能
从 Milvus 2.5.x 升级到 2.6.13 涉及重大架构更改：
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
系统要求：
通过 Milvus 操作符部署了 Milvus 的 Kubernetes 集群
kubectl
配置访问群集
已安装 Helm 3.x
兼容性要求：
Milvus v2.6.0-rc1 与 v2.6.13
不兼容
。不支持从候选版本直接升级。
如果当前运行的是 v2.6.0-rc1，需要保留数据，请参考
本社区指南
以获取迁移帮助。
在升级到 v2.6.13 之前，您
必须
升级到 v2.5.16 或更高版本，并启用
mixCoord
。
消息队列限制
：升级到 Milvus v2.6.13 时，您必须保持当前的消息队列选择。不支持在升级过程中在不同的消息队列系统之间切换。未来版本将支持更换消息队列系统。
升级流程
步骤 1：升级 Milvus Operator
首先，将您的 Milvus 操作符升级到 v1.3.0：
helm repo add zilliztech-milvus-operator https://zilliztech.github.io/milvus-operator/
helm repo update zilliztech-milvus-operator
helm -n milvus-operator upgrade milvus-operator zilliztech-milvus-operator/milvus-operator
验证操作符升级：
kubectl -n milvus-operator get pods
第 2 步：升级 Milvus 集群
2.1 检查当前协调器配置
检查您的群集是否已经使用
mixCoord
：
kubectl get pods
如果您看到的是单独的协调器 pod (
datacoord
,
querycoord
,
indexcoord
) ，则需要在下一步中启用
mixCoord
。
2.2 使用 mixCoord 升级到 v2.5.16
如果您的群集已运行 v2.5.16 或更高版本，且已启用
mixCoord
，请跳过此步骤。
创建配置文件
milvusupgrade.yaml
以启用
mixCoord
并升级到 v2.5.16：
apiVersion:
milvus.io/v1beta1
kind:
Milvus
metadata:
name:
my-release
# Replace with your actual release name
spec:
components:
mixCoord:
replicas:
1
image:
milvusdb/milvus:v2.5.16
应用配置：
kubectl patch -f milvusupgrade.yaml --patch-file milvusupgrade.yaml --
type
merge
等待完成：
# Verify all pods are ready
kubectl get pods
2.3 升级至 v2.6.13
在
mixCoord
上成功运行 v2.5.16 后，升级到 v2.6.13：
更新配置文件（本例中为
milvusupgrade.yaml
）：
apiVersion:
milvus.io/v1beta1
kind:
Milvus
metadata:
name:
my-release
# Replace with your actual release name
spec:
components:
image:
milvusdb/milvus:v2.6.13
应用最终升级：
kubectl patch -f milvusupgrade.yaml --patch-file milvusupgrade.yaml --
type
merge
验证升级
确认群集正在运行新版本：
# Check pod status
kubectl get pods
如需其他支持，请查阅
Milvus 文档
或
社区论坛
。