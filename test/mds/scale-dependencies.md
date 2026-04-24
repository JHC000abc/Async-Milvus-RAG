扩展 Milvus 依赖项
Milvus 依赖于 MinIO、Kafka、Pulsar 和 etcd 等各种依赖项。扩展这些组件可以增强 Milvus 对不同需求的适应性。
Milvus Operator 用户请参阅《
使用 Milvus Operator 配置对象存储
》、《
使用 Milvus Operator 配置元存储
》和《
使用 Milvus
Operator
配置消息存储
》。
扩展 MinIO
增加每个 MinIO pod 的资源
MinIO 是 Milvus 使用的对象存储系统，可以为每个 pod 增加 CPU 和内存资源。
# new-values.yaml
minio:
resources:
limits:
cpu:
2
memory:
8Gi
保存文件后，使用以下命令应用更改：
helm upgrade <milvus-release> --reuse-values -f new-values.yaml milvus/milvus
您还可以通过手动更改每个 MioIO Persistent Volume Claim (PVC) 的
spec.resources.requests.storage
值来增加 MioIO 集群的磁盘容量。请注意，您的默认存储类别应允许卷扩展。
添加额外的 MinIO 服务器池（推荐）
建议您为 Milvus 实例添加一个额外的 MinIO 服务器池。
# new-values.yam;
minio:
zones:
2
保存文件后，使用以下命令应用更改：
helm upgrade <milvus-release> --reuse-values -f new-values.yaml milvus/milvus
这将为你的 MinIO 集群添加一个额外的服务器池，允许 Milvus 根据每个服务器池的可用磁盘容量写入 MinIO 服务器池。例如，如果一个由三个服务器池组成的群集共有 10 TiB 可用空间，各服务器池的分配情况如下：
可用空间
写入可能性
池 A
3 TiB
30% (3/10)
资源库 B
2 TiB
20% (2/10)
C 组
5 个 TiB
50% (5/10)
MinIO 不会自动重新平衡新服务器池中的对象。如有需要，您可以通过
mc admin rebalance
手动启动重新平衡程序。
卡夫卡
增加每个 Kafka 代理 pod 的资源
通过调整每个 Kafka 代理 pod 的 CPU 和内存资源来提高 Kafka 代理的容量。
# new-values.yaml
kafka:
resources:
limits:
cpu:
2
memory:
12Gi
保存文件后，使用以下命令应用更改：
helm upgrade <milvus-release> --reuse-values -f new-values.yaml milvus/milvus
您还可以通过手动更改每个 Kafka Persistent Volume Claim (PVC) 的
spec.resources.requests.storage
值来增加 Kafka 集群的磁盘容量。确保默认存储类允许卷扩展。
添加额外的 Kafka 代理池（推荐）
建议您为 Milvus 实例添加一个额外的 Kafka 服务器池。
# new-values.yaml
kafka:
replicaCount:
4
保存文件后，使用以下命令应用更改：
helm upgrade <milvus-release> --reuse-values -f new-values.yaml milvus/milvus
这将为你的 Kafka 集群添加一个额外的代理。
Kafka 不会自动在所有代理之间重新平衡主题。如有需要，请在登录每个 Kafka 代理 pod 后使用
bin/kafka-reassign-partitions.sh
手动重新平衡所有 Kafka 代理的主题/分区。
脉冲星
Pulsar 分离了计算和存储。您可以独立增加 Pulsar 代理（计算）和 Pulsar 账本（存储）的容量。
增加每个 Pulsar 代理 pod 的资源
# new-values.yaml
pulsar:
broker:
resources:
limits:
cpu:
4
memory:
16Gi
保存文件后，使用以下命令应用更改：
helm upgrade <milvus-release> --reuse-values -f new-values.yaml milvus/milvus
增加每个 Pulsar 博彩机 pod 的资源
# new-values.yaml
pulsar:
bookkeeper:
resources:
limits:
cpu:
4
memory:
16Gi
保存文件后，使用以下命令应用更改：
helm upgrade <milvus-release> --reuse-values -f new-values.yaml milvus/milvus
您还可以通过手动更改每个 Pulsar 代理的持久卷索赔 (PVC) 的
spec.resources.requests.storage
值来增加 Pulsar 集群的磁盘容量。请注意，默认存储类别应允许卷扩展。
Pulsar 托管 pod 有两种存储类型：
journal
和
legers
。对于
journal
类型的存储，可考虑使用
ssd
或
gp3
作为存储类。下面是一个为 Pulsar 日志指定存储类的示例。
pulsar:
bookkeeper:
volumes:
journal:
size:
20Gi
storageClassName:
gp3
添加额外的 Pulsar 代理 pod
# new-values.yaml
pulsar:
broker:
replicaCount:
3
保存文件后，使用以下命令应用更改：
helm upgrade <milvus-release> --reuse-values -f new-values.yaml milvus/milvus
添加一个额外的 Pulsar bookie pod（推荐）
# new-values.yaml
pulsar:
bookkeeper:
replicaCount:
3
保存文件后，使用以下命令应用更改：
helm upgrade <milvus-release> --reuse-values -f new-values.yaml milvus/milvus
etcd
增加每个 etcd pod 的资源（推荐）
# new-values.yaml
etcd:
resources:
limits:
cpu:
2
memory:
8Gi
保存文件后，使用以下命令应用更改：
helm upgrade <milvus-release> --reuse-values -f new-values.yaml milvus/milvus
增加额外的 etcd pod
etcd pod 的总数应为奇数。
# new-values.yaml
etcd:
replicaCount:
5
保存文件后，使用以下命令应用更改：
helm upgrade <milvus-release> --reuse-values -f new-values.yaml milvus/milvus