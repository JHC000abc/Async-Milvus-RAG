使用 Docker Compose 配置 Milvus
本主题介绍如何使用 Docker Compose 配置 Milvus 组件及其第三方依赖项。
在当前版本中，所有参数只有在 Milvus 重新启动后才会生效。
下载配置文件
直接或使用以下命令
下载
milvus.yaml
。
$
wget https://raw.githubusercontent.com/milvus-io/milvus/v2.6.13/configs/milvus.yaml
修改配置文件
通过调整
milvus.yaml
中的相应参数，配置你的 Milvus 实例，以适应你的应用场景。
有关各参数的详细信息，请查看以下链接。
排序方式
组件或依赖项
配置目的
依赖项
组件
etcd
MinIO 或 S3
脉冲星
RocksMQ
Root coord
代理
Query coord
查询节点
索引节点
数据坐标
数据节点
本地存储
日志
信息通道
通用
图形处理器
GRPC
索引坐标
元存储
消息队列
Tikv
跟踪
配额和限制
用途
参数
性能调整
queryNode.gracefulTime
rootCoord.minSegmentSizeToEnableIndex
dataCoord.segment.maxSize
dataCoord.segment.sealProportion
dataNode.flush.insertBufSize
queryCoord.autoHandoff
queryCoord.autoBalance
localStorage.enabled
数据和元
common.retentionDuration
rocksmq.retentionTimeInMinutes
dataCoord.enableCompaction
dataCoord.enableGarbageCollection
dataCoord.gc.dropTolerance
管理
log.level
log.file.rootPath
log.file.maxAge
minio.accessKeyID
minio.secretAccessKey
配额和限制
quotaAndLimits.ddl.enabled
quotaAndLimits.ddl.collectionRate
quotaAndLimits.ddl.partitionRate
quotaAndLimits.indexRate.enabled
quotaAndLimits.indexRate.max
quotaAndLimits.flushRate.enabled
quotaAndLimits.flush.max
quotaAndLimits.compation.enabled
quotaAndLimits.compaction.max
quotaAndLimits.dml.enabled
quotaAndLimits.dml.insertRate.max
quotaAndLimits.dml.deleteRate.max
quotaAndLimits.dql.enabled
quotaAndLimits.dql.searchRate.max
quotaAndLimits.dql.queryRate.max
quotaAndLimits.limitWriting.ttProtection.enabled
quotaAndLimits.limitWriting.ttProtection.maxTimeTickDelay
quotaAndLimits.limitWriting.memProtection.enabled
quotaAndLimits.limitWriting.memProtection.dataNodeMemoryLowWaterLevel
quotaAndLimits.limitWriting.memProtection.queryNodeMemoryLowWaterLevel
quotaAndLimits.limitWriting.memProtection.dataNodeMemoryHighWaterLevel
quotaAndLimits.limitWriting.memProtection.queryNodeMemoryHighWaterLevel
quotaAndLimits.limitWriting.diskProtection.enabled
quotaAndLimits.limitWriting.diskProtection.diskQuota
quotaAndLimits.limitWriting.forceDeny
quotaAndLimits.limitReading.queueProtection.enabled
quotaAndLimits.limitReading.queueProtection.nqInQueueThreshold
quotaAndLimits.limitReading.queueProtection.queueLatencyThreshold
quotaAndLimits.limitReading.resultProtection.enabled
quotaAndLimits.limitReading.resultProtection.maxReadResultRate
quotaAndLimits.limitReading.forceDeny
下载安装文件
下载 Milvus
Standalone
的安装文件，并将其保存为
docker-compose.yml
。
也可以直接运行以下命令。
#
For Milvus standalone
$
wget https://github.com/milvus-io/milvus/releases/download/v2.6.13/milvus-standalone-docker-compose.yml -O docker-compose.yml
修改安装文件
在
docker-compose.yml
中，在每个
milvus-standalone
下添加
volumes
部分。
将
milvus.yaml
文件的本地路径映射到所有
volumes
部分下配置文件
/milvus/configs/milvus.yaml
的相应 docker 容器路径上。
...
standalone:
container_name:
milvus-standalone
image:
milvusdb/milvus:v2.2.13
command:
[
"milvus"
,
"run"
,
"standalone"
]
environment:
ETCD_ENDPOINTS:
etcd:2379
MINIO_ADDRESS:
minio:9000
volumes:
-
/local/path/to/your/milvus.yaml:/milvus/configs/milvus.yaml
# Map the local path to the container path
-
${DOCKER_VOLUME_DIRECTORY:-.}/volumes/milvus:/var/lib/milvus
ports:
-
"19530:19530"
-
"9091:9091"
depends_on:
-
"etcd"
-
"minio"
...
数据会根据
docker-compose.yml
中的默认配置存储在
/volumes
文件夹中。要更改存储数据的文件夹，请编辑
docker-compose.yml
或运行
$ export DOCKER_VOLUME_DIRECTORY=
。
启动 Milvus
修改完配置文件和安装文件后，就可以启动 Milvus 了。
$
sudo
docker compose up -d
下一步
了解如何使用 Docker Compose 或 Helm 管理以下 Milvus 依赖项：
使用 Docker Compose 或 Helm 配置对象存储
使用 Docker Compose 或 Helm 配置元存储
使用 Docker Compose 或 Helm 配置消息存储