使用 Milvus Operator 配置消息存储
Milvus 使用 RocksMQ、Pulsar 或 Kafka 管理最近更改的日志、输出流日志并提供日志订阅。本主题介绍如何在使用 Milvus Operator 安装 Milvus 时配置消息存储依赖关系。有关详细信息，请参阅 Milvus Operator 存储库中的
使用 Milvus Operator 配置消息存储
。
本主题假定您已部署 Milvus Operator。
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
中的代码模板，即可配置第三方依赖关系。以下各节将分别介绍如何配置对象存储、etcd 和 Pulsar。
开始之前
下表显示了在 Milvus 独立模式和集群模式下是否支持 RocksMQ、Pulsar、Kafka 和 Woodpecker。
RocksMQ
脉冲星
卡夫卡
啄木鸟
单机模式
✔️
✔️
✔️
✔️
集群模式
✖️
✔️
✔️
✔️
指定消息存储还有其他限制：
一个 Milvus 实例只支持一个消息存储。不过，我们仍然向后兼容为一个实例设置多个消息存储空间。优先级如下：
独立模式：  RocksMQ（默认） > Pulsar > Kafka
集群模式：Pulsar （默认） > Kafka
Milvus 系统运行时，消息存储不能更改。
仅支持 Kafka 2.x 或 3.x 版本。
升级限制
：
消息队列限制
：升级到 Milvus v2.6.13 时，必须保持当前的消息队列选择。不支持在升级过程中在不同的消息队列系统之间切换。未来版本将支持更换消息队列系统。
配置 RocksMQ
RocksMQ 是 Milvus Standalone 的默认消息存储。
目前，你只能通过 Milvus Operator 将 RocksMQ 配置为 Milvus Standalone 的消息存储。
示例
下面的示例配置了一个 RocksMQ 服务。
apiVersion:
milvus.io/v1beta1
kind:
Milvus
metadata:
name:
milvus
spec:
mode:
standalone
dependencies:
msgStreamType:
rocksmq
rocksmq:
persistence:
enabled:
true
pvcDeletion:
true
persistentVolumeClaim:
spec:
accessModes:
[
"ReadWriteOnce"
]
storageClassName:
"local-path"
# Specify your storage class
resources:
requests:
storage:
10Gi
# Specify your desired storage size
components:
{}
config:
{}
主要配置选项：
msgStreamType
rocksmq: 明确设置 RocksMQ 为消息队列。
persistence.enabled
:启用 RocksMQ 数据的持久存储
persistence.pvcDeletion
:为 true 时，PVC 将在 Milvus 实例删除时被删除。
persistentVolumeClaim.spec
:标准 Kubernetes PVC 规范
accessModes
:通常
ReadWriteOnce
用于块存储
storageClassName
:您的集群的存储类
storage
:持久卷的大小
配置啄木鸟
Woodpecker 是专为对象存储设计的云原生前向写日志（WAL）。它具有高吞吐量、低操作符和无缝可扩展性。有关详细信息，请参阅
使用 Woodpecker
。
配置 Pulsar
Pulsar 管理最近更改的日志、输出流日志并提供日志订阅。Milvus Standalone 和 Milvus 集群都支持为消息存储配置 Pulsar。不过，使用 Milvus Operator，只能将 Pulsar 配置为 Milvus 集群的消息存储。添加
spec.dependencies.pulsar
下的必填字段以配置 Pulsar。
pulsar
支持
external
和
inCluster
。
外部 Pulsar
external
表示使用外部 Pulsar 服务。 用于配置外部 Pulsar 服务的字段包括：
external
:
true
值表示 Milvus 使用外部 Pulsar 服务。
endpoints
:Pulsar 的端点。
示例
下面的示例配置了外部 Pulsar 服务。
apiVersion:
milvus.io/v1alpha1
kind:
Milvus
metadata:
name:
my-release
labels:
app:
milvus
spec:
dependencies:
# Optional
pulsar:
# Optional
# Whether (=true) to use an existed external pulsar as specified in the field endpoints or
# (=false) create a new pulsar inside the same kubernetes cluster for milvus.
external:
true
# Optional default=false
# The external pulsar endpoints if external=true
endpoints:
-
192.168
.1
.1
:6650
components:
{}
config:
{}
内部 Pulsar
inCluster
表示当 Milvus 集群启动时，集群中的 Pulsar 服务会自动启动。
示例
下面的示例配置了内部 Pulsar 服务。
apiVersion:
milvus.io/v1alpha1
kind:
Milvus
metadata:
name:
my-release
labels:
app:
milvus
spec:
dependencies:
pulsar:
inCluster:
values:
components:
autorecovery:
false
zookeeper:
replicaCount:
1
bookkeeper:
replicaCount:
1
resoureces:
limit:
cpu:
'4'
memory:
8Gi
requests:
cpu:
200m
memory:
512Mi
broker:
replicaCount:
1
configData:
## Enable `autoSkipNonRecoverableData` since bookkeeper is running
## without persistence
autoSkipNonRecoverableData:
"true"
managedLedgerDefaultEnsembleSize:
"1"
managedLedgerDefaultWriteQuorum:
"1"
managedLedgerDefaultAckQuorum:
"1"
proxy:
replicaCount:
1
components:
{}
config:
{}
该示例指定了 Pulsar 各组件的副本数量、Pulsar BookKeeper 的计算资源以及其他配置。
在
values.yaml
中查找配置内部 Pulsar 服务的完整配置项。如上例所示，根据需要在
pulsar.inCluster.values
下添加配置项。
假设配置文件名为
milvuscluster.yaml
，运行以下命令应用配置。
kubectl apply -f milvuscluster.yaml
配置 Kafka
Pulsar 是 Milvus 集群的默认消息存储。如果要使用 Kafka，请添加可选字段
msgStreamType
以配置 Kafka。
kafka
支持
external
和
inCluster
。
外部 Kafka
external
表示使用外部 Kafka 服务。
用于配置外部 Kafka 服务的字段包括
external
:
true
值表示 Milvus 使用外部 Kafka 服务。
brokerList
:要向其发送消息的代理列表。
示例
以下示例配置了外部 Kafka 服务。
apiVersion:
milvus.io/v1alpha1
kind:
Milvus
metadata:
name:
my-release
labels:
app:
milvus
spec:
config:
kafka:
# securityProtocol supports: PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL
securityProtocol:
PLAINTEXT
# saslMechanisms supports: PLAIN, SCRAM-SHA-256, SCRAM-SHA-512
saslMechanisms:
PLAIN
saslUsername:
""
saslPassword:
""
# Omit other fields ...
dependencies:
# Omit other fields ...
msgStreamType:
"kafka"
kafka:
external:
true
brokerList:
-
"kafkaBrokerAddr1:9092"
-
"kafkaBrokerAddr2:9092"
# ...
操作符 v0.8.5 或更高版本支持 SASL 配置。
内部 Kafka
inCluster
表示当 milvus 集群启动时，集群中的 Kafka 服务会自动启动。
示例
下面的示例配置了内部 Kafka 服务。
apiVersion:
milvus.io/v1alpha1
kind:
Milvus
metadata:
name:
my-release
labels:
app:
milvus
spec:
dependencies:
msgStreamType:
"kafka"
kafka:
inCluster:
values:
{}
# values can be found in https://artifacthub.io/packages/helm/bitnami/kafka
components:
{}
config:
{}
在此处
查找配置内部 Kafka 服务的完整配置项。根据需要在
kafka.inCluster.values
下添加配置项。
假设配置文件名为
milvuscluster.yaml
，运行以下命令应用配置。
kubectl
apply -f milvuscluster.yaml
下一步
了解如何使用 Milvus Operator 配置其他 Milvus 依赖项：
使用 Milvus Operator 配置对象存储
使用 Milvus Operator 配置元存储