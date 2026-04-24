产品常见问题
Milvus 的成本是多少？
Milvus 是一个 100% 免费的开源项目。
在使用 Milvus 进行生产或发布时，请遵守
Apache License 2.0
。
Milvus 背后的公司 Zilliz 还为那些不想构建和维护自己的分布式实例的用户提供完全托管的云版平台。
Zilliz Cloud
可自动维护数据的可靠性，并允许用户只为其使用付费。
Milvus 支持非 x86 架构吗？
是的，Milvus 支持 x86 和 ARM 架构。ARM64 支持通过多种部署选项提供，包括 Docker 映像、RPM/DEB 包和 Milvus Lite。
对于 x86 平台，您的 CPU 应支持以下指令集之一，以获得最佳性能：SSE4.2、AVX、AVX2、AVX512。对于 ARM 平台，Milvus 可在基于 ARM64 的处理器上运行，包括苹果 M1/M2 芯片和其他 ARM64 系统。
Milvus 在哪里存储数据？
Milvus 处理两种类型的数据：插入数据和元数据。
插入数据（包括向量数据、标量数据和特定于 Collections 的 Schema）以增量日志的形式存储在持久存储中。Milvus 支持多种对象存储后端，包括
MinIO
、
AWS S3
、
谷歌云存储
（GCS）、
Azure Blob 存储
、
阿里云 OSS
和
腾讯云对象存储
（COS）。
元数据在 Milvus 内部生成。每个 Milvus 模块都有自己的元数据，这些元数据存储在 etcd 中。
为什么 etcd 中没有向量数据？
etcd 存储 Milvus 模块元数据；MinIO 存储实体。
Milvus 支持同时插入和搜索数据吗？
是的。插入操作和查询操作由两个相互独立的模块处理。从客户端的角度来看，当插入的数据进入消息队列时，插入操作符就完成了。但是，插入的数据在加载到查询节点之前是不可查询的。对于具有增量数据的增长数据段，Milvus 会自动建立临时索引，以确保高效的搜索性能，即使数据段大小未达到索引建立阈值（计算公式为
dataCoord.segment.maxSize
×
dataCoord.segment.sealProportion
）。你可以通过
Milvus 配置文件
中的配置参数
queryNode.segcore.interimIndex.enableIndex
来控制这种行为--将其设置为
true
可启用临时索引（默认），而将其设置为
false
则会禁用临时索引。
能否在 Milvus 中插入主键重复的向量？
可以。Milvus 不检查向量主键是否重复。
当插入主键重复的向量时，Milvus 是否将其视为更新操作？
Milvus目前不支持更新操作，也不检查实体主键是否重复。你有责任确保实体主键是唯一的，如果不是唯一的，Milvus 可能包含多个主键重复的实体。
如果出现这种情况，查询时将返回哪个数据副本仍是未知行为。这一限制将在今后的版本中修复。
自定义实体主键的最大长度是多少？
实体主键必须是非负 64 位整数。
每次插入操作可添加的最大数据量是多少？
插入操作的大小不得超过 1,024 MB。这是 gRPC 规定的限制。
在特定分区中搜索时，Collection 的大小会影响查询性能吗？
不会。如果为搜索指定了分区，Milvus 只搜索指定的分区。
为搜索指定分区时，Milvus 是否需要加载整个 Collections？
这取决于搜索需要哪些数据。搜索前必须加载搜索结果中可能显示的所有分区。
例如，如果只想搜索特定分区，则不需要加载所有分区。调用
load_partition()
加载目标分区，
然后
在
search()
方法调用中指定分区。
如果要搜索所有分区，请调用
load_collection()
加载包括所有分区在内的整个 Collections。
如果在搜索前未加载 Collections 或特定分区，Milvus 将返回错误。
插入向量后能否创建索引？
可以。如果之前已通过
create_index()
为某个 Collections 建立了索引，Milvus 会自动为随后插入的向量建立索引。不过，在新插入的向量填满整个数据段，且新创建的索引文件与之前的索引文件分开时，Milvus 才会建立索引。
FLAT 和 IVF_FLAT 索引有何不同？
IVF_FLAT 索引将向量空间划分为列表簇。在默认列表值为 16,384 时，Milvus 会比较目标向量与所有 16,384 个簇的中心点之间的距离，以返回探针最近的簇。然后，Milvus 会比较目标向量与所选簇中向量之间的距离，从而得到最近向量。与 IVF_FLAT 不同，FLAT 直接比较目标向量与其他每个向量之间的距离。
当向量总数近似等于 nlist 时，IVF_FLAT 和 FLAT 在计算要求和搜索性能上几乎没有距离。但是，当向量数量超过 nlist 的 2 倍或更多时，IVF_FLAT 就开始显示出性能优势。
更多信息，请参阅
向量索引
。
Milvus 如何刷新数据？
当插入的数据被摄取到消息队列时，Milvus 返回成功。但是，数据尚未刷新到磁盘。然后，Milvus 的数据节点会将消息队列中的数据作为增量日志写入持久存储。如果调用
flush()
，数据节点就会被迫立即将消息队列中的所有数据写入持久化存储。
什么是规范化？为什么需要规范化？
归一化指的是转换向量使其法等于 1 的过程。如果使用内积来计算向量的相似性，则必须对向量进行归一化。归一化后，内积等于余弦相似度。
更多信息，请参见
维基百科
。
为什么欧氏距离（L2）和内积（IP）返回的结果不同？
对于归一化向量，欧氏距离（L2）在数学上等同于内积（IP）。如果这些相似性度量返回不同的结果，请检查您的向量是否归一化
Milvus 中的 Collections 和分区总数有限制吗？
有。您最多可以在 Milvus 实例中创建 65,535 个集合。计算现有集合数量时，Milvus 会计算所有包含分片和分区的集合。
例如，假设您已经创建了 100 个 Collection，其中 60 个 Collection 有 2 个分片和 4 个分区，其余 40 个 Collection 有 1 个分片和 12 个分区。当前的 Collections 数量可以计算如下：
60 * 2 * 4 + 40 * 1 * 12 = 960
在搜索
topk
向量时，为什么得到的向量少于 k 个？
在 Milvus 支持的索引中，IVF_FLAT 和 IVF_SQ8 实现了 k-means 聚类方法。数据空间被划分为
nlist
个簇，插入的向量被分配到这些簇中。然后，Milvus 选择离其最近的
nprobe
个簇，并比较目标向量与所选簇中所有向量之间的距离，返回最终结果。
如果
nlist
和
topk
较大，而 nprobe 较小，则 nprobe 簇中的向量数量可能少于
k
。因此，当搜索
topk
最近的向量时，返回的向量数量少于
k
。
为避免这种情况，可尝试将
nprobe
设置得大一些，将
nlist
和
k
设置得小一些。
更多信息请参见
向量索引
。
Milvus 支持的最大向量维度是多少？
默认情况下，Milvus 最多可管理 32,768 维的向量。你可以增加
Proxy.maxDimension
的值，以允许更大维度的向量。
Milvus 是否支持苹果 M1 CPU？
是的，Milvus 支持苹果 M1/M2 CPU 和其他苹果硅处理器。通过 Docker 映像、RPM/DEB 包和 Milvus Lite，可支持 ARM64，使其与包括 M1、M2 和更新处理器在内的苹果硅芯片兼容。
Milvus 在主键字段上支持哪些数据类型？
在当前版本中，Milvus 支持 INT64 和字符串。
Milvus 可以扩展吗？
是的。您可以在 Kubernetes 上使用 Helm Chart 部署多节点的 Milvus 集群。更多说明请参阅《
扩展指南》
。
什么是增长段和封存段？
当有搜索请求时，Milvus 会同时搜索增量数据和历史数据。增量数据是最近更新的数据，它们存储在增长段中，在达到在对象存储中持久化的阈值之前在内存中缓冲，并为它们建立更高效的索引。历史数据是一段时间前的更新，它们位于已在对象存储中持久化的封存段中。增量数据和历史数据共同构成了整个搜索数据集。这种设计使任何输入到 Milvus 的数据都可以即时搜索。对于 Milvus Distributed 而言，有更复杂的因素来决定刚录入的记录何时可以显示在搜索结果中。在
一致性级别
了解更多细微差别。
Milvus 可用于并发搜索吗？
是的。对于同一 Collections 的查询，Milvus 会同时搜索增量数据和历史数据。不过，对不同 Collection 的查询是串联进行的。历史数据可能是一个极其庞大的数据集，因此对历史数据的搜索相对更耗时，而且基本上是串联进行的。
为什么相应的 Collections 被删除后，MinIO 中的数据仍会保留？
MinIO 中的数据被设计为保留一段时间，以方便数据回滚。
Milvus 是否支持 Pulsar 以外的消息引擎？
支持。Milvus 2.1.0 支持 Kafka。
搜索和查询有什么区别？
在 Milvus 中，向量相似性搜索根据相似性计算和向量索引加速检索向量。与向量相似性搜索不同，向量查询是通过基于布尔表达式的标量过滤来检索向量的。布尔表达式会对标量字段或主键字段进行过滤，并检索所有符合过滤条件的结果。在查询中，既不涉及相似度指标，也不涉及向量索引。
为什么在 Milvus 中，浮点向量值的精度是小数点后 7 位？
Milvus 支持将向量存储为 Float32 数组。Float32 值的精度为小数点后 7 位。即使是 Float64 值，例如 1.3476964684980388，Milvus 也将其存储为 1.347696。因此，当你从 Milvus 获取这样一个向量时，Float64 值的精度就会丢失。
Milvus 如何处理向量数据类型和精度？
Milvus 支持二进制、Float32、Float16 和 BFloat16 向量类型。
二进制向量：将二进制数据存储为 0 和 1 的序列，用于图像处理和信息检索。
Float32 向量：默认存储精度约为小数点后 7 位。即使是 Float64 值也是以 Float32 精度存储的，这可能会导致检索时的精度损失。
Float16 和 BFloat16 向量：可降低精度和内存使用量。Float16 适用于带宽和存储有限的应用，而 BFloat16 则兼顾了范围和效率，常用于深度学习，在不显著影响精度的情况下降低计算要求。
Milvus 是否支持为标量或向量场指定默认值？
目前，Milvus 2.4.x 不支持为标量或向量场指定默认值。该功能计划在未来版本中推出。
在 Milvus 中删除数据后，存储空间会立即释放吗？
不，在 Milvus 中删除数据后，存储空间不会立即释放。虽然删除数据会将实体标记为 "逻辑删除"，但实际空间可能不会立即释放。原因如下：
压缩
：Milvus 会在后台自动压缩数据。这个过程会将较小的数据段合并为较大的数据段，并删除逻辑上已删除的数据（标记为删除的实体）或已超过有效时间（TTL）的数据。不过，压缩会创建新的数据段，同时将旧数据段标记为 "已丢弃"。
垃圾收集
：一个名为 Garbage Collection (GC) 的独立进程会定期删除这些 "已删除 "的数据段，从而释放它们占用的存储空间。这样可以确保存储空间的有效利用，但在删除和空间回收之间会有轻微延迟。
操作符插入、删除或上插数据后，我能否立即看到这些数据，而无需等待刷新？
是的，在 Milvus，由于其存储-计算分解架构，数据可见性与刷新操作没有直接联系。您可以使用一致性级别管理数据可读性。
选择一致性级别时，请考虑一致性和性能之间的权衡。对于需要即时可见性的操作符，请使用 "强 "一致性级别。对于更快的写入，优先考虑较弱的一致性（数据可能不会立即可见）。有关详细信息，请参阅
一致性
。
启用分区密钥功能后，Milvus 中
num_partitions
的默认值是多少，为什么？
启用分区密钥功能后，Milvus 中
num_partitions
的默认值设置为
16
。选择这一默认值是出于稳定性和性能方面的考虑。您可以根据需要在
create_collection
功能中指定
num_partitions
值。
标量过滤表达式有最大长度限制吗？
有，标量过滤表达式的最大长度受 RPC 传输限制的约束，该限制在
milvus.yaml
配置文件中定义。具体来说，该限制由代理部分下的
serverMaxRecvSize
参数设置：
proxy:
grpc:
serverMaxRecvSize:
67108864
# The maximum size of each RPC request that the proxy can receive, unit: byte
默认情况下，每个 RPC 请求的最大大小为 64MB。因此，过滤表达式的长度必须小于此限制，才能确保成功处理。
执行批量向量搜索时，一次可以指定多少个向量？有限制吗？
是的，在批量向量搜索中可以指定的向量数量受 RPC 传输大小的限制，RPC 传输大小在
milvus.yaml
配置文件中定义。该限制由代理部分下的
serverMaxRecvSize
参数决定：
proxy:
grpc:
serverMaxRecvSize:
67108864
# The maximum size of each RPC request that the proxy can receive, unit: byte
默认情况下，每个 RPC 请求的最大大小为 64MB。因此，输入向量（包括其维度数据和元数据）的总大小必须小于此限制，以确保成功执行。
如何从 Collections 中获取给定标量字段的所有唯一值？
目前还没有直接的方法来实现这一目标。作为一种变通方法，我们建议使用查询迭代器检索特定字段的所有值，然后手动执行重复数据删除。我们计划在 Milvus 2.6 中添加对该功能的直接支持。使用 query_iterator 的示例：
# set up iterator
iterator = client.query_iterator(
    collection_name=
"demo_collection"
,
    output_fields=[
"target"
]
)
# do iteration and store target values into value_set
value_set =
set
()
while
True
:
    res = iterator.
next
()
if
len
(res) ==
0
:
print
(
"query iteration finished, close"
)
        iterator.close()
break
for
i
in
range
(
len
(res)):
        value_set.add(res[i][
"target"
])
# value_set will contain unique values for target column
使用动态字段有什么限制？例如，是否有大小限制、修改方法或索引限制？
动态字段在内部使用 JSON 字段表示，大小限制为 65,536 字节。它们支持向上插入修改，允许您添加或更新字段。不过，从 Milvus 2.5.1 开始，动态字段不支持索引。未来版本将支持为 JSON 添加索引。
Milvus 支持 Schema 更改吗？
从 Milvus 2.5.0 版开始，模式更改仅限于特定的修改，如调整
mmap
参数等属性。用户还可以修改 varchar 字段的
max_length
和数组字段的
max_capacity
。不过，计划在今后的版本中实现在模式中添加或删除字段的功能，增强 Milvus 内模式管理的灵活性。
修改 VarChar 的 max_length 是否需要重新组织数据？
不需要，修改 VarChar 字段的
max_length
不需要进行数据重组，如压缩或重组。这一调整主要是更新插入字段的新数据的验证标准，现有数据不受影响。因此，这一更改被认为是轻量级的，不会给系统带来显著的开销。
仍有问题？
您可以
在 GitHub 上查看
Milvus
。欢迎提出问题、分享想法并帮助其他用户。
加入我们的
Discord 频道
，寻求支持并与我们的开源社区互动。