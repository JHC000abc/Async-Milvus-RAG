收集数量限制
Milvus 实例最多允许 65,536 个 Collection。不过，过多的 Collections 可能会导致性能问题。因此，建议限制在 Milvus 实例中创建的 Collection 数量。
本指南说明了如何设置 Milvus 实例中的 Collection 数量限制。
配置因安装 Milvus 实例的方式而异。
对于使用 Helm Charts 安装的 Milvus 实例
将配置添加到
values.yaml
文件的
config
部分。有关详细信息，请参阅
使用 Helm Charts 配置 Milvus
。
对于使用 Docker Compose 安装的 Milvus 实例
将配置添加到用于启动 Milvus 实例的
milvus.yaml
文件中。有关详细信息，请参阅
使用 Docker Compose 配置 Milvus
。
对于使用 Operator 安装的 Milvus 实例
将配置添加到
Milvus
自定义资源的
spec.components
部分。有关详情，请参阅
使用 Operator 配置 Milvus
。
配置选项
rootCoord:
maxGeneralCapacity:
65536
quotaAndLimits:
limits:
maxCollectionNum:
65536
maxCollectionNumPerDB:
65536
要更改 Collections 限制，需要将三个参数一起修改：
参数
参数
默认值
rootCoord.maxGeneralCapacity
当前实例可容纳的最大集合单元数（分片×分区）。
65536
quotaAndLimits.limits.maxCollectionNum
当前实例中所有数据库允许的最大集合数。
65536
quotaAndLimits.limits.maxCollectionNumPerDB
单个数据库中允许的最大集合数。
65536
例如，将限制增加到 200,000 个 Collections：
rootCoord:
maxGeneralCapacity:
200000
quotaAndLimits:
limits:
maxCollectionNum:
200000
maxCollectionNumPerDB:
200000
只设置
maxGeneralCapacity
而不同时调整
maxCollectionNum
和
maxCollectionNumPerDB
将不会生效。必须将所有三个参数设置为相同值或更高，才能提高 Collections 限制。
计算 Collection 数量
在一个 Collections 中，可以设置多个分片和分区。分片是用于在多个数据节点之间分配数据写入操作的逻辑单元。分区是逻辑单元，用于通过只加载 Collections 数据的子集来提高数据检索效率。在计算当前 Milvus 实例中的 Collections 数量时，还需要计算分片和分区的数量。
例如，假设您已经创建了
100 个
Collection，其中
60 个
Collection 有
2
个分块和
4 个
分区，其余
40 个
Collection 有
1 个
分块和
12 个
分区。收集单元总数（计算公式为
shards × partitions
）可按如下方式确定：
60 (collections) x 2 (shards) x 4 (partitions) + 40 (collections) x 1 (shard) x 12 (partitions) = 960
在本例中，计算出的 960 个 Collections 单元总数代表了当前的使用情况。
maxGeneralCapacity
定义了实例可支持的最大 Collections 单位数，默认设置为
65536
。这意味着实例最多可容纳 65,536 个 Collections 单元。如果总数超过此限制，系统将显示以下错误信息：
failed checking constraint: sum_collections(parition*shard) exceeding the max general capacity:
为避免出现此错误，可以减少现有或新收集中的分片或分区数量，删除某些收集，或通过同时修改
maxGeneralCapacity
、
maxCollectionNum
和
maxCollectionNumPerDB
来增加收集限制。