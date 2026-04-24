预热
Compatible with Milvus 2.6.4+
预热
是对分层存储的补充，可在段可查询前将选定字段或索引预加载到缓存中。您可以在集群、 Collections 或单个字段/索引级别配置预热，从而实现对首次查询延迟和资源使用的精细控制。
为什么要预热
分层存储中的 "
懒加载
"通过最初只加载元数据来提高效率。但是，这可能会导致首次查询冷数据时出现延迟，因为必须从远程存储中获取所需的数据块或索引。
预热
可在段初始化过程中主动缓存关键数据，从而解决这一问题。
它在以下情况下尤其有用
某些标量索引经常用于过滤条件。
向量索引对搜索性能至关重要，必须立即准备就绪。
查询节点重启或新网段加载后的冷启动延迟是不可接受的。
相反，对于不经常查询的字段或索引，
不建议
使用预热功能。禁用 "预热 "功能可缩短数据段加载时间并节省缓存空间，非常适合大型向量字段或非关键标量字段。
配置级别
配置级别
范围
配置方法
优先级
字段/索引
单个字段或索引
SDK 方法：
add_field()
alter_collection_field()
add_index()
alter_index_properties()
最高
Collections
Collections 中的所有字段/索引
SDK 方法：
create_collection()
alter_collection_properties()
中等
群集
集群中的所有 Collections
milvus.yaml
配置文件
最低（默认）
覆盖行为：
如果字段有自己的预热设置，则该设置优先于 Collections 级别和群集级别的设置。
如果不存在字段或索引级设置，则适用 Collection 级设置。
如果既不存在字段或索引级设置，也不存在 Collection 级设置，则适用群集级设置。
使用更改操作时，最新的更改值生效。
配置群集级预热
集群级预热在 Milvus 配置文件
milvus.yaml
中配置，适用于集群中的所有 Collections。这是基准默认值。
每种目标类型都支持两种设置：
预热设置
说明
典型场景
sync
在网段可查询前进行预加载。加载时间会略有增加，但首次查询不会产生延迟。
用于必须立即可用的性能关键型数据，如搜索中使用的高频标量索引或关键向量索引。
disable
跳过预加载。数据段可查询的速度更快，但首次查询可能会触发按需加载。
适用于不常访问的数据或大型数据，如原始向量字段或非关键标量字段。
YAML 示例
queryNode:
segcore:
tieredStorage:
warmup:
# options: sync, disable.
# Specifies the timing for warming up the Tiered Storage cache.
# - `sync`: data will be loaded into the cache before a segment is considered loaded.
# - `disable`: data will not be proactively loaded into the cache, and loaded only if needed by search/query tasks.
# Defaults to `sync`, except for vector field which defaults to `disable`.
scalarField:
sync
scalarIndex:
sync
vectorField:
disable
# cache warmup for vector field raw data is by default disabled.
vectorIndex:
sync
参数
预热设置
说明
建议用例
scalarField
sync
|
disable
控制是否预加载标量字段数据。
只有当标量字段较小并且在过滤器中被频繁访问时，才使用
sync
。否则，
disable
，以减少加载时间。
scalarIndex
sync
|
disable
控制是否预加载标量索引。
对于涉及频繁筛选条件或范围查询的标量索引，请使用
sync
。
vectorField
sync
|
disable
控制是否预加载向量字段数据。
一般情况下，
disable
，以避免大量使用缓存。只有在搜索后必须立即检索原始向量时（例如，具有向量召回功能的相似性结果），才启用
sync
。
vectorIndex
sync
|
disable
控制是否预加载向量索引。
对于对搜索延迟至关重要的向量索引，请使用
sync
。在批量或低频率工作负载中，
disable
，以加快分段准备。
在 Collections 级别配置预热
Compatible with Milvus 2.6.11+
集合级预热允许您覆盖特定集合的集群默认值。当某个 Collection 的访问模式与整个群集的基线不同时，这将非常有用。
创建 Collections 时设置预热
from
pymilvus
import
MilvusClient

client = MilvusClient(uri=
"http://localhost:19530"
)

client.create_collection(
    collection_name=
"my_collection"
,
    schema=schema,
properties={
"warmup.scalarField"
:
"sync"
,
"warmup.scalarIndex"
:
"sync"
,
"warmup.vectorField"
:
"disable"
,
"warmup.vectorIndex"
:
"sync"
}
)
更改现有 Collection 上的预热设置
必须在调用
load()
之前更改 Collection 属性。更改已加载的 Collection 会返回错误。对预热设置的更改会在下次加载集合时生效。
client.alter_collection_properties(
    collection_name=
"my_collection"
,
    properties={
"warmup.vectorIndex"
:
"disable"
,
"warmup.scalarField"
:
"sync"
}
)
属性参考
：
属性
预热设置
说明
warmup.scalarField
sync
|
disable
Collections 中所有标量字段的预热设置。
warmup.scalarIndex
sync
|
disable
集合中所有标量索引的预热设置。
warmup.vectorField
sync
|
disable
Collections 中所有向量场的预热设置。
warmup.vectorIndex
sync
|
disable
集合中所有向量索引的预热设置。
在字段级别配置预热
Compatible with Milvus 2.6.11+
字段级预热提供了最精细的粒度，允许你控制单个字段的预热行为。这在特定字段具有独特访问模式时非常有用。
字段级预热
仅
适用于
字段原始数据
，不适用于该字段上的索引。要为索引配置预热，请使用
索引级配置
。
创建字段时设置预热
from
pymilvus
import
MilvusClient, DataType

schema = MilvusClient.create_schema()

schema.add_field(
    field_name=
"id"
,
    datatype=DataType.INT64,
    is_primary=
True
)

schema.add_field(
    field_name=
"category"
,
    datatype=DataType.VARCHAR,
    max_length=
128
,
    warmup=
"sync"
# Preload this field at load time
)

schema.add_field(
    field_name=
"embedding"
,
    datatype=DataType.FLOAT_VECTOR,
    dim=
768
,
    warmup=
"disable"
# Do not preload vector raw data
)
更改现有字段的预热设置
必须在调用
load()
之前更改字段设置。在已加载的 Collections 上更改字段会返回错误。对预热设置的更改在下次加载集合时生效。
client.alter_collection_field(
    collection_name=
"my_collection"
,
    field_name=
"category"
,
    field_params={
"warmup"
:
"sync"
}
)
在索引级配置预热
Compatible with Milvus 2.6.11+
通过索引级预热，可以控制单个索引的预加载，与底层字段的预热设置无关。
创建索引时设置预热
from
pymilvus
import
MilvusClient

client = MilvusClient(uri=
"http://localhost:19530"
)

index_params = client.prepare_index_params()

index_params.add_index(
    field_name=
"embedding"
,
    index_type=
"HNSW"
,
    metric_type=
"COSINE"
,
    params={
"M"
:
16
,
"efConstruction"
:
256
,
"warmup"
:
"sync"
# Preload this index at load time
}
)

index_params.add_index(
    field_name=
"category"
,
    index_type=
"AUTOINDEX"
,
    params={
"warmup"
:
"disable"
}
# Do not preload this index
)

client.create_index(
    collection_name=
"my_collection"
,
    index_params=index_params
)
更改现有索引的预热设置
必须在调用
load()
之前更改索引设置。在已加载的 Collections 上更改索引会返回错误。对预热设置的更改会在下次加载集合时生效。
client.alter_index_properties(
    collection_name=
"my_collection"
,
    index_name=
"embedding"
,
    properties={
"warmup"
:
"sync"
}
)
预热行为参考
下表总结了段生命周期不同阶段的预热行为。
预热设置
加载阶段
搜索/查询阶段
释放阶段
sync
数据加载到本地存储。目的地（磁盘或内存）取决于 mmap 设置。
查询直接命中本地缓存。
本地缓存数据被清除。
disable
数据不加载到本地存储。
按需从对象存储获取数据，然后根据 mmap 设置在本地缓存。
本地缓存数据被清除。
与 mmap 交互：
预热设置
启用毫米映射
数据位置
sync
true
本地磁盘 (
localStorage.path/cache/...
)
sync
false
本地内存
disable
true
首次访问时读取到本地磁盘
disable
false
首次访问时抓取到本地内存
本地缓存目录结构（启用 mmap 时）：
数据类型
目录路径
标量/向量字段数据
localStorage.path/cache/<collection_id>/local_chunk/...
标量/向量索引文件
localStorage.path/cache/<collection_id>/local_chunk/index_files/...
最佳实践
预热只影响初始加载。如果缓存数据后来被驱逐，下一次查询将按需重新加载。
避免过度使用
sync
。预加载太多字段会增加加载时间和缓存压力。
保守起步--仅对频繁访问的字段和索引启用预热。
监控查询延迟和缓存指标，然后根据需要扩大预加载。
对于混合工作负载，将
sync
应用于对性能敏感的 Collections，将
disable
应用于面向容量的 Collections。