操作常见问题
什么是 QueryNode 委托器，它的职责是什么？
当 Collections 加载时，QueryNode 会订阅来自消息队列的插入和删除消息的 DML 通道。订阅这些通道的 QueryNode（称为委托人）负责
管理因持续插入而需要额外内存的增加区段。
接收删除信息，并将其传递给持有相关分段的其他 QueryNode。
如何识别 Collections 的委托人节点？
使用 Birdwatcher。
按照
以下
步骤安装 Birdwatcher，然后运行以下命令：
./birdwatcher
#
Find delegator nodes
for
your collection
Milvus(my-release) > show segment-loaded-grpc --collection <your-collectionID>

ServerID 2
Channel by-dev-rootcoord-dml_2, collection: 430123456789, version 1
Leader view for channel: by-dev-rootcoord-dml_2
Growing segments count: 1, ids: [430123456789_4]
#
Map server ID to pod IP
Milvus(my-release) > show session

Node(s) querynode
        ID: 1        Version: 2.4.0        Address: 10.0.0.4:19530
        ID: 2        Version: 2.4.0        Address: 10.0.0.5:19530
        ID: 3        Version: 2.4.0        Address: 10.0.0.6:19530
如果查询节点内存使用不平衡，可以调整哪些参数？
有时，查询节点的内存会发生变化，因为有些节点作为委托人会使用更多内存。如果某个委托人的内存较大，可调整 queryCoord.delegatorMemoryOverloadFactor 以将封存的程序段卸载到其他节点，减少内存使用量。
默认值为 0.1。
增加该值（如增加到 0.3 或更高）会使系统将更多密封线段从超载的 delegator 卸载到其他 QueryNodes，有助于平衡内存使用。你也可以尝试将值增加到 1，这意味着不会在委托节点中加载密封片段。
如果不想重启集群，可以用 Birdwatcher 修改 Milvus 配置：
.
/
birdwatcher
Offline
>
connect
--etcd <your-etcd-ip>:2379 --auto
# Change delegatorMemoryOverloadFactor
to
0.3
without
restart,
default
value
is
0.1
set
config
-
etcd
--key queryCoord.delegatorMemoryOverloadFactor --value 0.3
如何为 Collections 设置 shard_num？
最佳做法是，对于向量维度为 768 的 Collections，建议每 ~1 亿个向量至少使用 1 个 shard。对于重写使用情况，每 ~1 亿向量使用 4 个分区。
例如，如果有 1 亿向量，则使用 1-4 个碎片。如果有 5 亿向量，则使用 5-10 个碎片。
如果从 Docker Hub 拉取 Milvus Docker 镜像失败怎么办？
如果从 Docker Hub 拉取 Milvus Docker 镜像失败，请尝试添加其他注册镜像。
中国大陆的用户可以在
/etc.docker/daemon.json
中的 registry-mirrors 数组中添加网址 "https://registry.docker-cn.com"。
{
"registry-mirrors"
:
[
"https://registry.docker-cn.com"
]
}
Docker 是安装和运行 Milvus 的唯一方式吗？
Docker 是部署 Milvus 的有效方法，但不是唯一的方法。你也可以从源代码部署 Milvus。这需要 Ubuntu（18.04 或更高版本）或 CentOS（7 或更高版本）。更多信息，请参阅
从源代码构建 Milvus
。
影响召回率的主要因素是什么？
召回率主要受索引类型和搜索参数的影响。
对于 FLAT 索引，Milvus 在一个 Collection 内进行穷举扫描，100% 返回。
对于 IVF 索引，nprobe 参数决定了 Collections 内的搜索范围。增加 nprobe 会增加搜索到的向量比例和召回率，但会降低查询性能。
对于 HNSW 索引，ef 参数决定图搜索的广度。增加 ef 会增加在图上搜索的点数和召回率，但会降低查询性能。
有关详细信息，请参阅
向量索引
。
为什么我对配置文件的修改没有生效？
Milvus 不支持在运行期间修改配置文件。您必须重新启动 Milvus Docker，配置文件的更改才能生效。
如何知道 Milvus 是否已成功启动？
如果使用 Docker Compose 启动 Milvus，请运行
docker ps
观察有多少 Docker 容器正在运行，并检查 Milvus 服务是否正确启动。
对于 Milvus Standalone，应该至少能观察到三个运行中的 Docker 容器，其中一个是 Milvus 服务，其他两个是 etcd 管理和存储服务。有关详细信息，请参阅
安装 Milvus Standalone
。
为什么日志文件中的时间与系统时间不同？
时间不同通常是由于主机不使用协调世界时（UTC）。
Docker 映像中的日志文件默认使用 UTC。如果您的主机不使用 UTC，可能会出现这个问题。
我如何知道我的 CPU 是否支持 Milvus？
Milvus 的操作符取决于 CPU 对 SIMD（单指令、多数据）扩展指令集的支持。您的中央处理器是否支持 SIMD 扩展指令集对 Milvus 中的索引建立和向量相似性搜索至关重要。请确保您的 CPU 至少支持以下一种 SIMD 指令集：
SSE4.2
AVX
AVX2
AVX512
运行 lscpu 命令检查 CPU 是否支持上述 SIMD 指令集：
$
lscpu |
grep -e sse4_2 -e avx -e avx2 -e avx512
为什么 Milvus 在启动时返回
illegal instruction
？
Milvus 要求 CPU 支持 SIMD 指令集：SSE4.2、AVX、AVX2 或 AVX512。CPU 必须至少支持其中之一，以确保 Milvus 正常操作符。启动过程中返回的
illegal instruction
错误说明 CPU 不支持上述四种指令集中的任何一种。
请参阅
CPU 对 SIMD 指令集的支持
。
我可以在 Windows 上安装 Milvus 吗？
可以。您可以通过源代码编译或二进制包在 Windows 上安装 Milvus。
请参阅
在 Windows 上运行 Milvus
了解如何在 Windows 上安装 Milvus。
我在 Windows 上安装 pymilvus 时出错了。我该怎么办？
请尝试使用以下命令将 pymilvus 更新到最新版本。
pip install --upgrade pymilvus
我可以在断开互联网的情况下部署 Milvus 吗？
可以。您可以在离线环境下安装 Milvus。请参阅
离线安装 Milvus
获取更多信息。
在哪里可以找到 Milvus 生成的日志？
Milvus 日志默认打印到 stout（标准输出）和 stderr（标准错误），但是我们强烈建议在生产中将日志重定向到持久卷。为此，请更新
Milvus.yaml
中的
log.file.rootPath
。而如果你用
milvus-helm
chart 部署 Milvus，也需要先通过
--set log.persistence.enabled=true
启用日志持久性。
如果你没有更改配置，使用 kubectl logs
或 docker logs CONTAINER 也能帮你找到日志。
在插入数据之前，我可以为段创建索引吗？
可以。但我们建议在为每个数据段创建索引之前，分批插入数据，每批不应超过 256 MB。
能否在多个 Milvus 实例之间共享一个 etcd 实例？
可以，您可以在多个 Milvus 实例之间共享一个 etcd 实例。为此，在启动每个 Milvus 实例之前，需要在每个实例的配置文件中将
etcd.rootPath
更改为单独的值。
能否在多个 Milvus 实例之间共享一个 Pulsar 实例？
可以，你可以在多个 Milvus 实例之间共享一个 Pulsar 实例。为此，你可以
如果在你的 Pulsar 实例上启用了多租户，考虑为每个 Milvus 实例分配一个单独的租户或命名空间。为此，你需要在启动 Milvus 实例之前，将其配置文件中的
pulsar.tenant
或
pulsar.namespace
改为每个实例的唯一值。
如果不打算在 Pulsar 实例上启用多租户功能，可考虑在启动 Milvus 实例之前，将其配置文件中的
msgChannel.chanNamePrefix.cluster
更改为每个实例的唯一值。
我可以在多个 Milvus 实例之间共享一个 MinIO 实例吗？
可以，您可以在多个 Milvus 实例之间共享一个 MinIO 实例。为此，您需要在启动每个 Milvus 实例之前，在每个实例的配置文件中将
minio.rootPath
更改为唯一值。
如何处理
pymilvus.exceptions.ConnectionConfigException: <ConnectionConfigException: (code=1, message=Illegal uri: [example.db], expected form 'https://user:pwd@example.com:12345')>
错误信息？
错误信息
Illegal uri [example.db]
表明你正在尝试使用早期版本的 PyMilvus 连接 Milvus Lite，该版本不支持这种连接类型。要解决这个问题，请将你的 PyMilvus 安装升级到至少 2.4.2 版本，其中包括对连接 Milvus Lite 的支持。
您可以使用以下命令升级 PyMilvus：
pip install pymilvus>=2.4.2
为什么我得到的结果少于我在搜索/查询中设置的
limit
？
有几种原因可能导致您收到的结果少于您指定的
limit
：
数据有限
：Collections 可能没有足够的实体来满足您要求的限制。如果 Collections 中的实体总数少于限制，您收到的结果自然也会减少。
主键重复
：在搜索过程中遇到主键重复时，Milvus 会优先处理特定实体。这种行为根据搜索类型而有所不同：
查询（精确匹配）
：Milvus 选择具有匹配 PK 的最新实体。 ANN 搜索：Milvus 会选择相似度得分最高的实体，即使实体共享相同的 PK。 如果您的 Collections 有很多重复的主键，这种优先级可能会导致唯一结果少于限制。
匹配不足
：您的搜索过滤表达式可能过于严格，导致符合相似性阈值的实体较少。如果为搜索设置的条件限制性太强，匹配的实体就不够多，导致结果比预期的少。
MilvusClient("milvus_demo.db") gives an error: ModuleNotFoundError: No module named 'milvus_lite'
.什么原因导致这种情况，如何解决？
当你试图在 Windows 平台上使用 Milvus Lite 时，就会出现这个错误。Milvus Lite 主要为 Linux 环境设计，可能不支持 Windows。
解决办法是使用 Linux 环境：
使用基于 Linux 的操作系统或虚拟机来运行 Milvus Lite。
这种方法将确保与库的依赖关系和功能兼容。
Milvus 中的 "长度超过最大长度 "错误是什么，如何理解和解决？
Milvus 中的 "长度超过最大长度 "错误发生在数据元素的大小超过 Collections 或字段的最大允许大小时。下面是一些示例和解释：
JSON 字段错误：
<MilvusException: (code=1100, message=the length (398324) of json field (metadata) exceeds max length (65536): expected=valid length json string, actual=length exceeds max length: invalid parameter)>
字符串长度错误：
<ParamError: (code=1, message=invalid input, length of string exceeds max length. length: 74238, max length: 60535)>
VarChar 字段错误：
<MilvusException: (code=1100, message=the length (60540) of 0th VarChar paragraph exceeds max length (0)%!(EXTRA int64=60535): invalid parameter)>
要理解和处理这些错误，请
要理解
len(str)
在 Python 中代表的是字符数，而不是以字节为单位的大小。
对于基于字符串的数据类型，如 VARCHAR 和 JSON，使用
len(bytes(str, encoding='utf-8'))
来确定以字节为单位的实际大小，这就是 Milvus 使用的 "max-length"。
Python 示例
# Python Example: result of len() str cannot be used as "max-length" in Milvus
>>>
s =
"你好，世界！"
>>>
len
(s)
# Number of characters of s.
6
>>>
len
(
bytes
(s,
"utf-8"
))
# Size in bytes of s, max-length in Milvus.
18
pymilvus.exceptions.ConnectionConfigException: <ConnectionConfigException: (code=1, message=Illegal uri: [example.db], expected form 'https://user:pwd@example.com:12345')>
.什么原因导致这种情况，如何解决？
这个错误表明，你试图使用不支持 Milvus Lite 的早期版本 pymilvus 连接 Milvus Lite。要解决这个问题，请将你的 pymilvus 至少升级到 2.4.2 版。该版本支持连接 Milvus Lite。要升级，请使用以下命令：
pip install pymilvus>=2.4.2
仍有问题？
你可以
查看 GitHub 上的
Milvus
。随时提问、分享想法并帮助其他用户。
加入我们的
Milvus 论坛
或
Discord 频道
，寻求支持并参与我们的开源社区。