切换 Milvus 群集的 MQ 类型
本主题介绍如何为现有的 Milvus 群集部署切换消息队列（MQ）类型。Milvus 支持在 Pulsar、Kafka 和 Woodpecker 之间进行在线 MQ 切换，无需停机。
此功能尚未发布，可能会有变动。如果您想试用或有任何疑问，请联系 Milvus 支持人员。
前提条件
通过 Milvus
Operator
或
Helm
安装正在运行的 Milvus 集群实例。
Milvus 实例已升级到支持此 Switch MQ 功能的最新版本。
从 Pulsar/Kafka 切换到 Woodpecker (MinIO)
按照以下步骤将 MQ 类型从 Pulsar 或 Kafka 切换到使用 MinIO 存储的 Woodpecker。
步骤 1：确认 Milvus 实例正在运行
在切换之前，请确保您的 Milvus 集群实例运行正常。您可以通过创建一个测试 Collections、插入数据并运行查询来验证。
第 2 步：（可选）验证啄木鸟配置
默认的 Milvus 配置已将 Woodpecker 存储类型设置为 MinIO，因此在大多数情况下无需额外配置。
但是，如果以前自定义过 Woodpecker 配置，则必须确保
woodpecker.storage.type
设置为
minio
。更新 Milvus 配置
时，无需
更改
mqType
值：
woodpecker:
storage:
type:
minio
对于
Helm
，有关更新配置的说明，请参阅
使用 Helm 图表配置 Milvus
。
对于
Milvus 操作符
，请参阅
使用 Milvus Operator 配置 Milvus
，了解更新配置的说明。
步骤 3：执行 MQ 切换
运行以下命令触发向啄木鸟的切换：
curl -X POST http://<mixcoord_addr>:9091/management/wal/alter \
  -H "Content-Type: application/json" \
  -d '{"target_wal_name": "woodpecker"}'
将
<mixcoord_addr>
替换为 MixCoord 服务的实际地址。
第 4 步：验证切换是否完成
切换过程自动完成。监控 Milvus 日志中的以下关键信息，以确认切换已完成：
WAL
switch
success: <MQ1>
switch
to <MQ2> finish, re-opening required
AlterWAL broadcast message acknowledged
by
all vchannels
successfully updated mq.type configuration
in
etcd
在上述日志信息中，
<MQ1>
是源 MQ 类型（如
pulsar
或
kafka
），
<MQ2>
是目标 MQ 类型 (
woodpecker
)。
第一条信息表明，从源到目标的 WAL 切换已经完成。
第二条信息表示所有物理通道都已切换。
第三条消息表示
mq.type
配置已在 etcd 中更新。
从 Woodpecker (MinIO) 切换到 Pulsar 或 Kafka
按照以下步骤将 MQ 类型从 Woodpecker 切换回 Pulsar 或 Kafka。
步骤 1：确认 Milvus 实例正在运行
在切换之前，请确保 Milvus 集群实例运行正常。
第 2 步：配置目标 MQ
在触发切换之前，需要确保目标 MQ 服务（Pulsar 或 Kafka）可用，并且其访问配置已呈现到 Milvus 配置中。
本节的具体步骤取决于您使用的是内部（捆绑）还是外部 MQ 服务。
选项 A：内部 Pulsar/Kafka（与 Helm 捆绑使用）
如果使用的是 Helm 部署的捆绑 Pulsar 或 Kafka，请更新 Helm 版本以启用目标 MQ 服务并禁用 Woodpecker。
streaming.enabled=true
标志是启用流节点所必需的，而流节点是切换 MQ 功能的先决条件。例如，切换到 Pulsar：
helm upgrade -i my-release milvus/milvus \
  --set pulsarv3.enabled=true \
  --set woodpecker.enabled=false \
  --set streaming.enabled=true \
  -f values.yaml
升级后，验证目标 MQ 访问配置是否已呈现到 Milvus 配置中。例如，对于 Pulsar：
pulsar:
address:
<pulsar-proxy-address>
port:
6650
选项 B：内部 Pulsar/Kafka（由 Milvus Operator 管理）
如果使用 Milvus Operator，请更新 Milvus 自定义资源，以包含目标 MQ 访问配置。有关更新 Milvus 配置的详细信息，请参阅
使用 Milvus Operator
配置 Milvus。
选项 C：外部 Pulsar/Kafka
如果使用外部 Pulsar 或 Kafka 服务，则无需更改
mqType
。只需将外部 MQ 访问配置添加到
values.yaml
，然后重启 Milvus 实例以呈现配置。
第 3 步：执行 MQ 切换
运行以下命令触发切换到 Pulsar（如果切换到 Kafka，请将
pulsar
替换为
kafka
）：
curl -X POST http://<mixcoord_addr>:9091/management/wal/alter \
  -H "Content-Type: application/json" \
  -d '{"target_wal_name": "pulsar"}'
将
<mixcoord_addr>
替换为 MixCoord 服务的实际地址。
第 4 步：验证切换是否完成
切换过程自动完成。监控 Milvus 日志中的以下关键信息，以确认切换已完成：
WAL
switch
success: <MQ1>
switch
to <MQ2> finish, re-opening required
AlterWAL broadcast message acknowledged
by
all vchannels
successfully updated mq.type configuration
in
etcd
在上述日志信息中，
<MQ1>
是源 MQ 类型（
woodpecker
），
<MQ2>
是目标 MQ 类型（如
pulsar
或
kafka
）。
第一条信息表明，从源到目标的 WAL 切换已经完成。
第二条信息表示所有物理通道都已切换。
第三条消息表示
mq.type
配置已在 etcd 中更新。