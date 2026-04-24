使用啄木鸟
Compatible with Milvus 2.6.x
本指南介绍如何在 Milvus 2.6.x 中启用和使用 Woodpecker 作为先写日志（WAL）。Woodpecker 是专为对象存储设计的云原生 WAL，具有高吞吐量、低操作符和无缝可扩展性。有关架构和基准的详细信息，请参阅
Woodpecker
。
概述
从 Milvus 2.6 开始，Woodpecker 是一种可选的 WAL，作为日志服务提供有序写入和恢复。
作为一种消息队列选择，它的行为与 Pulsar/Kafka 类似，可通过配置启用。
支持两种存储后端：本地文件系统（
local
）和对象存储（
minio
/S3-兼容）。
快速启动
要启用 Woodpecker，请将 MQ 类型设为 Woodpecker：
mq:
type:
woodpecker
注意：为正在运行的群集切换
mq.type
是一项升级操作。请仔细遵循升级步骤，并在新群集上进行验证，然后再切换到生产群集。
配置
以下是完整的 Woodpecker 配置块（在
user.yaml
中编辑
milvus.yaml
或覆盖）：
# Related configuration of woodpecker, used to manage Milvus logs of recent mutation operations, output streaming log, and provide embedded log sequential read and write.
woodpecker:
meta:
type:
etcd
# The Type of the metadata provider. currently only support etcd.
prefix:
woodpecker
# The Prefix of the metadata provider. default is woodpecker.
client:
segmentAppend:
queueSize:
10000
# The size of the queue for pending messages to be sent of each log.
maxRetries:
3
# Maximum number of retries for segment append operations.
segmentRollingPolicy:
maxSize:
256M
# Maximum size of a segment.
maxInterval:
10m
# Maximum interval between two segments, default is 10 minutes.
maxBlocks:
1000
# Maximum number of blocks in a segment
auditor:
maxInterval:
10s
# Maximum interval between two auditing operations, default is 10 seconds.
logstore:
segmentSyncPolicy:
maxInterval:
200ms
# Maximum interval between two sync operations, default is 200 milliseconds.
maxIntervalForLocalStorage:
10ms
# Maximum interval between two sync operations local storage backend, default is 10 milliseconds.
maxBytes:
256M
# Maximum size of write buffer in bytes.
maxEntries:
10000
# Maximum entries number of write buffer.
maxFlushRetries:
5
# Maximum size of write buffer in bytes.
retryInterval:
1000ms
# Maximum interval between two retries. default is 1000 milliseconds.
maxFlushSize:
2M
# Maximum size of a fragment in bytes to flush.
maxFlushThreads:
32
# Maximum number of threads to flush data
segmentCompactionPolicy:
maxSize:
2M
# The maximum size of the merged files.
maxParallelUploads:
4
# The maximum number of parallel upload threads for compaction.
maxParallelReads:
8
# The maximum number of parallel read threads for compaction.
segmentReadPolicy:
maxBatchSize:
16M
# Maximum size of a batch in bytes.
maxFetchThreads:
32
# Maximum number of threads to fetch data.
storage:
type:
minio
# The Type of the storage provider. Valid values: [minio, local]
rootPath:
/var/lib/milvus/woodpecker
# The root path of the storage provider.
主要说明：
woodpecker.meta
类型
：目前仅支持
etcd
。重复使用与 Milvus 相同的 etcd 来存储轻量级元数据。
前缀
：元数据的关键前缀。默认值：
woodpecker
。
woodpecker.client
控制客户端的段附加/滚动/审核行为，以平衡吞吐量和端到端延迟。
woodpecker.logstore
控制日志段的同步/刷新/压缩/读取策略。这些是吞吐量/延迟调整的主要旋钮。
woodpecker.storage
type
：
minio
，用于 MinIO/S3 兼容对象存储（MinIO/S3/GCS/OSS 等）；
local
，用于本地/共享文件系统。
rootPath
：存储后端的根路径（对
local
有效；对于
minio
，路径由桶/前缀决定）。
部署模式
Milvus 支持独立模式和集群模式。啄木鸟存储后端支持矩阵：
storage.type=local
storage.type=minio
Milvus 单机版
支持
支持
Milvus 集群
有限（需要共享 FS）
支持
备注
使用
minio
，啄木鸟与 Milvus 共享相同的对象存储（MinIO/S3/GCS/OSS 等）。
通过
local
，单节点本地磁盘仅适用于 Standalone。如果所有 pod 都能访问共享文件系统（如 NFS），集群模式也可以使用
local
。
部署指南
为 Kubernetes 上的 Milvus 群集启用啄木鸟（Milvus 操作符，存储=minio）
安装
Milvus 操作符
后，使用官方示例启动启用 Woodpecker 的 Milvus 群集：
kubectl apply -f https://raw.githubusercontent.com/zilliztech/milvus-operator/main/config/samples/milvus_cluster_woodpecker.yaml
该示例将 Woodpecker 配置为消息队列，并启用流节点。第一次启动可能需要一些时间来提取图像；请等待，直到所有 pod 都准备就绪：
kubectl get pods
kubectl get milvus my-release -o yaml | grep -A2 status
准备就绪后，你应该会看到类似于以下的 pod：
NAME                                               READY   STATUS    RESTARTS   AGE
my
-
release
-
etcd
-0
1
/
1
Running
0
17
m
my
-
release
-
etcd
-1
1
/
1
Running
0
17
m
my
-
release
-
etcd
-2
1
/
1
Running
0
17
m
my
-
release
-
milvus
-
datanode
-7
f8f88499d
-
kc66r
1
/
1
Running
0
16
m
my
-
release
-
milvus
-
mixcoord
-7
cd7998d
-
x59kg
1
/
1
Running
0
16
m
my
-
release
-
milvus
-
proxy
-5
b56cf8446
-
pbnjm
1
/
1
Running
0
16
m
my
-
release
-
milvus
-
querynode
-0
-558
d9cdd57
-
sgbfx
1
/
1
Running
0
16
m
my
-
release
-
milvus
-
streamingnode
-58
fbfdfdd8
-
vtxfd
1
/
1
Running
0
16
m
my
-
release
-
minio
-0
1
/
1
Running
0
17
m
my
-
release
-
minio
-1
1
/
1
Running
0
17
m
my
-
release
-
minio
-2
1
/
1
Running
0
17
m
my
-
release
-
minio
-3
1
/
1
Running
0
17
m
运行以下命令卸载 Milvus 集群。
kubectl delete milvus my-release
如果需要调整 Woodpecker 参数，请按照
消息存储配置
中所述进行设置。
为 Kubernetes 上的 Milvus 群集启用 Woodpecker（Helm 图表，存储=minio）
首先按照在
Kubernetes 中使用 Helm 运行 Milvus 中的
描述，添加并更新
Milvus
Helm 图表。
然后使用以下示例之一进行部署：
- 集群部署（建议设置为启用 Woodpecker 和流节点）：
helm install my-release zilliztech/milvus \
  --
set
image.all.tag=v2.6.0 \
  --
set
pulsarv3.enabled=
false
\
  --
set
woodpecker.enabled=
true
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
- 独立部署（启用 Woodpecker）：
helm install my-release zilliztech/milvus \
  --
set
image.all.tag=v2.6.0 \
  --
set
cluster.enabled=
false
\
  --
set
pulsarv3.enabled=
false
\
  --
set
standalone.messageQueue=woodpecker \
  --
set
woodpecker.enabled=
true
\
  --
set
streaming.enabled=
true
部署后，按照文档进行端口转发和连接。要调整 Woodpecker 参数，请按照
消息存储配置
中所述的设置进行。
在 Docker 中为 Milvus Standalone 启用啄木鸟（存储=本地）
按照
在 Docker 中运行 Milvus 的
步骤操作。示例：
mkdir
milvus-wp &&
cd
milvus-wp
curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh -o standalone_embed.sh
# Create user.yaml to enable Woodpecker with local filesystem
cat
> user.yaml <<
'EOF'
mq:
type
: woodpecker
woodpecker:
  storage:
type
:
local
rootPath: /var/lib/milvus/woodpecker
EOF

bash standalone_embed.sh start
要进一步更改 Woodpecker 设置，请更新
user.yaml
并运行
bash standalone_embed.sh restart
。
使用 Docker Compose 为 Milvus Standalone 启用啄木鸟 (存储空间=minio)
使用 Docker Compose 运行 Milvus
。示例：
mkdir
milvus-wp-compose &&
cd
milvus-wp-compose
wget https://github.com/milvus-io/milvus/releases/download/v2.6.0/milvus-standalone-docker-compose.yml -O docker-compose.yml
# By default, the Docker Compose standalone uses Woodpecker
sudo
docker compose up -d
# If you need to change Woodpecker parameters further, write an override:
docker
exec
-it milvus-standalone bash -lc
'cat > /milvus/configs/user.yaml <<EOF
mq:
  type: woodpecker
woodpecker:
  logstore:
    segmentSyncPolicy: 
      maxFlushThreads: 16
  storage:
    type: minio
EOF'
# Restart the container to apply the changes
docker restart milvus-standalone
吞吐量调整技巧
根据
Woodpecker
中的基准和后端限制，从以下方面优化端到端写吞吐量：
存储端
对象存储（兼容 minio/S3）
：增加并发量和对象大小（避免微小对象）。注意网络和桶带宽限制。固态硬盘上的单个 MinIO 节点本地带宽上限通常在 100 MB/s 左右；单个 EC2 到 S3 的带宽上限可达 GB/s。
本地/共享文件系统（本地）
：首选 NVMe/高速磁盘。确保文件系统能很好地处理小规模写入和同步延迟。
啄木鸟旋钮
增加
logstore.segmentSyncPolicy.maxFlushSize
和
maxFlushThreads
，以实现更大的刷新和更高的并行性。
根据介质特性调整
maxInterval
（以延迟换取吞吐量，延长聚合时间）。
对于对象存储，可考虑增加
segmentRollingPolicy.maxSize
，以减少段切换。
客户端/应用端
使用更大的批次规模和更多并发写入器/客户端。
控制刷新/索引建立时间（在触发前进行批处理），避免频繁的小规模写入。
批量插入演示
from
pymilvus
import
MilvusClient
import
random
# 1. Set up a Milvus client
client = MilvusClient(
    uri=
"http://<Proxy Pod IP>:27017"
,
)
# 2. Create a collection
res = client.create_collection(
    collection_name=
"test_milvus_wp"
,
    dimension=
512
,
    metric_type=
"IP"
,
    shards_num=
2
,
)
print
(res)
# 3. Insert randomly generated vectors
colors = [
"green"
,
"blue"
,
"yellow"
,
"red"
,
"black"
,
"white"
,
"purple"
,
"pink"
,
"orange"
,
"brown"
,
"grey"
]
data = []

batch_size =
1000
batch_count =
2000
for
j
in
range
(batch_count):
    start_time = time.time()
print
(
f"Inserting
{j}
th vectors
{j * batch_size}
startTime
{start_time}
"
)
for
i
in
range
(batch_size):
        current_color = random.choice(colors)
        data.append({
"id"
: (j*batch_size + i),
"vector"
: [ random.uniform(-
1
,
1
)
for
_
in
range
(
512
) ],
"color"
: current_color,
"color_tag"
:
f"
{current_color}
_
{
str
(random.randint(
1000
,
9999
))}
"
})
    res = client.insert(
        collection_name=
"test_milvus_wp"
,
        data=data
    )
    data = []
print
(
f"Inserted
{j}
th vectors endTime:
{time.time()}
costTime:
{time.time() - start_time}
"
)
延迟
啄木鸟是一款云原生 WAL，设计用于对象存储，在吞吐量、成本和延迟之间进行权衡。目前支持的轻量级嵌入式模式优先考虑成本和吞吐量优化，因为大多数场景只要求在一定时间内写入数据，而不是要求单个写入请求的低延迟。因此，啄木鸟采用分批写入的方式，本地文件系统存储后端的默认写入间隔为 10 毫秒，类 MinIO 存储后端的默认写入间隔为 200 毫秒。在慢速写操作期间，最大延迟等于间隔时间加上刷新时间。
请注意，批量插入不仅由时间间隔触发，还由批量大小（默认为 2MB）触发。
有关架构、部署模式（MemoryBuffer / QuorumBuffer）和性能的详细信息，请参阅
啄木鸟架构
。
更多参数详情，请参阅 Woodpecker
GitHub 代码库
。