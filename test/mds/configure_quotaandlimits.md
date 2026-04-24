配额和限制相关配置
QuotaConfig，Milvus 配额和限制的配置。
默认情况下，我们启用
TT 保护；
内存保护
磁盘配额保护。
可以启用
DML 吞吐量限制；
DDL、DQL qps/rps 限制；
DQL 队列长度/延迟保护；
DQL 结果速率保护；
如有必要，也可以手动强制拒绝 RW 请求。
quotaAndLimits.enabled
说明
默认值
true "表示启用配额和限制，"false "表示禁用。
假
quotaAndLimits.quotaCenterCollectInterval
说明
默认值
quotaCenterCollectInterval 是 quotaCenter
从代理、查询群集和数据群集收集指标的时间间隔。
秒，（0 ~ 65536）
3
quotaAndLimits.limits.allocRetryTimes
说明
默认值
从速率限制删除分配转发数据失败时的重试次数
15
quotaAndLimits.limits.allocWaitInterval
说明
默认值
删除分配转发数据速率失败时的重试等待时间，毫秒
1000
quotaAndLimits.limits.complexDeleteLimitEnable
说明
默认值
是否通过限制器复杂删除检查前向数据
假
quotaAndLimits.limits.maxCollectionNumPerDB
说明
默认值
每个数据库的最大 Collections 数量。
65536
quotaAndLimits.limits.maxInsertSize
说明
默认值
单个插入请求的最大大小，以字节为单位，-1 表示无限制
-1
quotaAndLimits.limits.maxResourceGroupNumOfQueryNode
说明
默认值
查询节点资源组的最大数量
1024
quotaAndLimits.limits.maxGroupSize
说明
默认值
按搜索分组时单个组的最大大小
10
quotaAndLimits.ddl.enabled
说明
默认值
是否启用 DDL 请求节流。
假
quotaAndLimits.ddl.collectionRate
说明
默认值
每秒与 Collections 相关的 DDL 请求的最大数量。
将该项设置为 10 表示 Milvus 每秒处理的集合相关 DDL 请求不超过 10 个，包括集合创建请求、集合删除请求、集合加载请求和集合释放请求。
要使用此设置，请同时将 quotaAndLimits.ddl.enabled 设置为 true。
-1
quotaAndLimits.ddl.partitionRate
说明
默认值
每秒与分区相关的 DDL 请求的最大数量。
将该项设置为 10 表示 Milvus 每秒处理的分区相关请求不超过 10 个，包括分区创建请求、分区删除请求、分区加载请求和分区释放请求。
要使用此设置，请同时将 quotaAndLimits.ddl.enabled 设置为 true。
-1
quotaAndLimits.ddl.db.collectionRate
说明
默认值
db 级别的 qps，默认无限制，用于 CreateCollection、DropCollection、LoadCollection、ReleaseCollection 的速率
-1
quotaAndLimits.ddl.db.partitionRate
说明
默认值
数据库级别的 qps，默认无限制，创建分区、删除分区、加载分区、释放分区的速率
-1
quotaAndLimits.indexRate.enabled
说明
默认值
是否启用与索引相关的请求节流。
假
quotaAndLimits.indexRate.max
说明
默认值
每秒索引相关请求的最大数量。
将该项设置为 10 表示 Milvus 每秒处理的分区相关请求不超过 10 个，包括索引创建请求和索引删除请求。
要使用此设置，请同时将 quotaAndLimits.indexRate.enabled 设置为 true。
-1
quotaAndLimits.indexRate.db.max
说明
默认值
db 级别的 qps，默认无限制，CreateIndex、DropIndex 的速率
-1
quotaAndLimits.flushRate.enabled
说明
默认值
是否启用刷新请求节流。
真
quotaAndLimits.flushRate.max
说明
默认值
每秒刷新请求的最大数量。
将该项设置为 10 表示 Milvus 每秒处理的刷新请求不超过 10 个。
要使用此设置，请同时将 quotaAndLimits.flushRate.enabled 设置为 true。
-1
quotaAndLimits.flushRate.collection.max
说明
默认值
qps，默认无限制，在 Collections 级别的刷新率。
0.1
quotaAndLimits.flushRate.db.max
说明
默认值
数据库级的 qps，默认无限制，冲洗速率
-1
quotaAndLimits.compactionRate.enabled
说明
默认值
是否启用手动压缩请求节流。
假
quotaAndLimits.compactionRate.max
说明
默认值
每秒手动压缩请求的最大数量。
将该项设置为 10 表示 Milvus 每秒处理的手动压缩请求不超过 10 个。
要使用此设置，请同时将 quotaAndLimits.compaction.enabled 设置为 true。
-1
quotaAndLimits.compactionRate.db.max
说明
默认值
db 级别的 qps，默认无限制，用于手动压缩的速率
-1
quotaAndLimits.dml.enabled
说明
默认值
是否启用 DML 请求节流。
假
quotaAndLimits.dml.insertRate.max
说明
默认值
每秒最高数据插入速率。
将该项设置为 5 表示 Milvus 只允许以每秒 5 MB 的速度插入数据。
要使用此设置，请同时将 quotaAndLimits.dml.enabled 设置为 true。
-1
quotaAndLimits.dml.insertRate.db.max
说明
默认值
MB/秒，默认无限制
-1
quotaAndLimits.dml.insertRate.collection.max
说明
默认值
每 Collection 每秒的最高数据插入速率。
将该项设置为 5 表示 Milvus 只允许以每秒 5 MB 的速度向任何 Collections 插入数据。
要使用此设置，请同时将 quotaAndLimits.dml.enabled 设置为 true。
-1
quotaAndLimits.dml.insertRate.partition.max
说明
默认值
MB/s，默认无限制
-1
quotaAndLimits.dml.upsertRate.max
说明
默认值
MB/s，默认无限制
-1
quotaAndLimits.dml.upsertRate.db.max
说明
默认值
MB/s，默认无限制
-1
quotaAndLimits.dml.upsertRate.collection.max
说明
默认值
MB/s，默认无限制
-1
quotaAndLimits.dml.upsertRate.partition.max
说明
默认值
MB/s，默认无限制
-1
quotaAndLimits.dml.deleteRate.max
说明
默认值
每秒最高数据删除速率。
将此项设置为 0.1 表示 Milvus 只允许以每秒 0.1 MB 的速度删除数据。
要使用此设置，请同时将 quotaAndLimits.dml.enabled 设置为 true。
-1
quotaAndLimits.dml.deleteRate.db.max
说明
默认值
MB/s, 默认无限制
-1
quotaAndLimits.dml.deleteRate.collection.max
说明
默认值
每秒最高数据删除速率。
将此项设置为 0.1 表示 Milvus 只允许以每秒 0.1 MB 的速度删除任何 Collections 中的数据。
要使用此设置，请同时将 quotaAndLimits.dml.enabled 设置为 true。
-1
quotaAndLimits.dml.deleteRate.partition.max
说明
默认值
MB/s，默认无限制
-1
quotaAndLimits.dml.bulkLoadRate.max
说明
默认值
MB/s，默认无限制，暂不支持。TODO：限制 bulkLoad 速率
-1
quotaAndLimits.dml.bulkLoadRate.db.max
说明
默认值
MB/s，默认无限制，暂不支持。TODO：限制数据库批量加载速率
-1
quotaAndLimits.dml.bulkLoadRate.collection.max
说明
默认值
MB/s，默认无限制，暂不支持。TODO：限制 Collections 批量加载速率
-1
quotaAndLimits.dml.bulkLoadRate.partition.max
说明
默认值
MB/s，默认无限制，暂不支持。TODO：限制分区批量加载速率
-1
quotaAndLimits.dql.enabled
说明
默认值
是否启用 DQL 请求节流。
假
quotaAndLimits.dql.searchRate.max
说明
默认值
每秒搜索向量的最大数量。
将此项设置为 100 表示 Milvus 每秒只允许搜索 100 个向量，无论这 100 个向量是集中在一次搜索中还是分散在多次搜索中。
要使用此设置，请同时将 quotaAndLimits.dql.enabled 设置为 true。
-1
quotaAndLimits.dql.searchRate.db.max
说明
默认值
vps（每秒向量数），默认无限制
-1
quotaAndLimits.dql.searchRate.collection.max
说明
默认值
每秒每个 Collections 搜索向量的最大数量。
将此项设置为 100 表示 Milvus 每秒只允许搜索每个 Collections 中的 100 个向量，无论这 100 个向量是集中在一次搜索中还是分散在多次搜索中。
要使用此设置，请同时将 quotaAndLimits.dql.enabled 设置为 true。
-1
quotaAndLimits.dql.searchRate.partition.max
说明
默认值
vps（每秒向量数），默认无限制
-1
quotaAndLimits.dql.queryRate.max
说明
默认值
每秒最大查询次数。
将此项设置为 100 表示 Milvus 每秒只允许 100 次查询。
要使用此设置，请同时将 quotaAndLimits.dql.enabled 设置为 true。
-1
quotaAndLimits.dql.queryRate.db.max
说明
默认值
qps，默认无限制
-1
quotaAndLimits.dql.queryRate.collection.max
说明
默认值
每秒每个 Collection 的最大查询次数。
将此项设置为 100 表示 Milvus 每秒只允许每个 Collection 进行 100 次查询。
要使用此设置，请同时将 quotaAndLimits.dql.enabled 设置为 true。
-1
quotaAndLimits.dql.queryRate.partition.max
说明
默认值
qps，默认无限制
-1
quotaAndLimits.limitWriting.forceDeny
说明
默认值
forceDeny false 表示允许 dml 请求（某些特定条件除外，如水标记的节点内存
true表示始终拒绝所有 dml 请求。
假
quotaAndLimits.limitWriting.ttProtection.maxTimeTickDelay
描述
默认值
maxTimeTickDelay 表示 DML 操作符的反向压力。
DML 速率将根据滴答延迟时间与 maxTimeTickDelay 的比率降低、
如果滴答延迟时间大于 maxTimeTickDelay，所有 DML 请求都将被拒绝。
秒数
300
quotaAndLimits.limitWriting.memProtection.enabled
说明
默认值
当内存使用率 > 内存高水位时，所有 DML 请求都将被拒绝；
内存使用率 < 内存高水位时，降低 dml 速率；
当内存使用率 < 内存低水位时，不执行任何操作。
true
quotaAndLimits.limitWriting.memProtection.dataNodeMemoryLowWaterLevel
说明
默认值
(0,1]，数据节点中的内存低水位
0.85
quotaAndLimits.limitWriting.memProtection.dataNodeMemoryHighWaterLevel
说明
默认值
(0,1]，数据节点中的内存高水位
0.95
quotaAndLimits.limitWriting.memProtection.queryNodeMemoryLowWaterLevel
说明
默认值
(0,1]，查询节点中的内存低水位
0.85
quotaAndLimits.limitWriting.memProtection.queryNodeMemoryHighWaterLevel
说明
默认值
(0,1]，查询节点中的内存高水位
0.95
quotaAndLimits.limitWriting.growingSegmentsSizeProtection.enabled
说明
默认值
如果增长的分段大小小于低水位线，则不会采取任何措施。
当增长的分段大小超过低水位时，将降低 dml 速率、
但速率不会低于 minRateRatio * dmlRate。
假
quotaAndLimits.limitWriting.diskProtection.enabled
说明
默认值
当对象存储的总文件大小大于 `diskQuota` 时，所有 dml 请求将被拒绝；
真
quotaAndLimits.limitWriting.diskProtection.diskQuota
说明
默认值
MB，（0，+inf），默认无限制
-1
quotaAndLimits.limitWriting.diskProtection.diskQuotaPerDB
说明
默认值
MB，（0，+inf），默认无限制
-1
quotaAndLimits.limitWriting.diskProtection.diskQuotaPerCollection
说明
默认值
MB，（0，+inf），默认无限制
-1
quotaAndLimits.limitWriting.diskProtection.diskQuotaPerPartition
说明
默认值
MB，（0，+inf），默认无限制
-1
quotaAndLimits.limitWriting.l0SegmentsRowCountProtection.enabled
说明
默认值
启用 l0 段行数配额的开关
假
quotaAndLimits.limitWriting.l0SegmentsRowCountProtection.lowWaterLevel
说明
默认值
l0 段行数配额，低水位
30000000
quotaAndLimits.limitWriting.l0SegmentsRowCountProtection.highWaterLevel
说明
默认值
l0 段行数配额，高水位
50000000
quotaAndLimits.limitWriting.deleteBufferRowCountProtection.enabled
说明
默认值
启用删除缓冲区行数配额的开关
假
quotaAndLimits.limitWriting.deleteBufferRowCountProtection.lowWaterLevel
说明
默认值
删除缓冲区行数配额，低水位
32768
quotaAndLimits.limitWriting.deleteBufferRowCountProtection.highWaterLevel
说明
默认值
删除缓冲区行数配额，高水位
65536
quotaAndLimits.limitWriting.deleteBufferSizeProtection.enabled
说明
默认值
启用删除缓冲区大小配额的开关
假
quotaAndLimits.limitWriting.deleteBufferSizeProtection.lowWaterLevel
说明
默认值
删除缓冲区大小配额，低水位
134217728
quotaAndLimits.limitWriting.deleteBufferSizeProtection.highWaterLevel
说明
默认值
删除缓冲区大小配额，高水位
268435456
quotaAndLimits.limitReading.forceDeny
说明
默认值
forceDeny false 表示允许 dql 请求（某些特殊情况除外，如收集已放弃），true 表示始终拒绝所有 dql 请求。
true表示始终拒绝所有 dql 请求。
false