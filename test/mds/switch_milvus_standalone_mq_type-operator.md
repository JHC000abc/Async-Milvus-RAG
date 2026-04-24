为 Milvus 单机版切换 MQ 类型
本主题介绍如何为现有的 Milvus 单机部署切换消息队列（MQ）类型。Milvus 支持在线 MQ 切换，无需停机。
此功能尚未发布，可能会有变动。如果您想尝试或有任何问题，请联系 Milvus 支持。
前提条件
通过
Docker
或
Docker Compose
安装的运行中的 Milvus Standalone 实例。
Milvus 实例已升级到支持此 Switch MQ 功能的最新版本。
一般工作流程
切换 MQ 类型的一般工作流程如下：
确保 Milvus 实例运行正常。
确认源 MQ 类型和目标 MQ 类型。
将目标 MQ 的访问设置配置到 Milvus 配置中，不更改
mqType
值。
通过调用 WAL alter API 触发切换。
监控日志以验证切换是否成功完成。
切换前，请确保目标 MQ 不包含与当前 Milvus 实例所用主题名称相同的主题。如果目标 MQ 服务以前曾被另一个 Milvus 实例使用过，这一点尤为重要，因为冲突的主题名称可能会导致意想不到的行为。
从 RocksMQ 切换到啄木鸟（本地存储）
本步骤适用于默认使用 RocksMQ 的
Milvus Standalone Docker
部署。
步骤 1：确认 Milvus 实例正在运行
确保你的 Milvus Standalone Docker 实例运行正常。你可以通过创建一个测试 Collections、插入数据并运行查询来验证。
第 2 步：使用本地存储配置啄木鸟
更新 Milvus 配置，
在不
更改
mqType
值的情况下添加 Woodpecker 设置。创建或更新
user.yaml
文件，内容如下：
woodpecker:
storage:
type:
local
然后重启 Milvus 实例以应用配置：
bash standalone_embed.sh restart
步骤 3：执行 MQ 切换
运行以下命令触发向 Woodpecker 的切换：
curl -X POST http://<mixcoord_addr>:9091/management/wal/alter \
  -H "Content-Type: application/json" \
  -d '{"target_wal_name": "woodpecker"}'
将
<mixcoord_addr>
替换为 MixCoord 服务的实际地址（默认情况下，独立部署的地址为
localhost
）。
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
是源 MQ 类型 (
rocksmq
)，
<MQ2>
是目标 MQ 类型 (
woodpecker
)。
第一条信息表明，从源到目标的 WAL 切换已经完成。
第二条信息表示所有物理通道都已切换。
第三条消息表示
mq.type
配置已在 etcd 中更新。
从 RocksMQ 切换到啄木鸟（MinIO 存储）
此步骤适用于
Milvus Standalone Docker Compose
部署。
从 Milvus v2.6 开始，默认
docker-compose.yaml
已将
mqType
声明为 Woodpecker。除非修改了默认配置或从 v2.5 升级，否则可能不需要此步骤。
步骤 1：验证 Milvus 实例是否正在运行
确保 Milvus Standalone Docker Compose 实例正常运行。
第 2 步：（可选）验证啄木鸟配置
默认的 Milvus 配置已经将 Woodpecker 存储类型设置为 MinIO，因此在大多数情况下无需额外配置。
但是，如果以前定制过 Woodpecker 配置，则必须确保
woodpecker.storage.type
设置为
minio
。用以下内容创建或更新
user.yaml
文件：
woodpecker:
storage:
type:
minio
然后重启 Milvus 实例以应用配置：
docker compose down
docker compose up -d
第 3 步：执行 MQ 切换
运行以下命令触发向啄木鸟的切换：
curl -X POST http://<mixcoord_addr>:9091/management/wal/alter \
  -H "Content-Type: application/json" \
  -d '{"target_wal_name": "woodpecker"}'
将
<mixcoord_addr>
替换为 MixCoord 服务的实际地址（默认情况下，独立部署的地址为
localhost
）。
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
是源 MQ 类型 (
rocksmq
)，
<MQ2>
是目标 MQ 类型 (
woodpecker
)。
第一条信息表明，从源到目标的 WAL 切换已经完成。
第二条信息表示所有物理通道都已切换。
第三条消息表示
mq.type
配置已在 etcd 中更新。