queryNode 相关配置
queryNode 的相关配置，用于在向量和标量数据之间进行混合搜索。
queryNode.stats.publishInterval
说明
默认值
查询节点发布节点统计信息（包括网段状态、CPU 使用率、内存使用率、健康状况等）的时间间隔。单位：毫秒。
1000
queryNode.segcore.knowhereThreadPoolNumRatio
说明
默认值
knowhere 线程池中的线程数。如果启用磁盘，线程池的大小将与 knowhereThreadPoolNumRatio([1, 32]) 相乘。
4
queryNode.segcore.chunkRows
说明
默认值
Segcore 将段划分为块的行数。
128
queryNode.segcore.interimIndex.enableIndex
说明
默认值
是否为不断增长的数据段和尚未建立索引的封存数据段创建临时索引，以提高搜索性能。
Milvus 最终会封存所有数据段并创建索引，但启用此功能可优化数据插入后即时查询的搜索性能。
默认值为 true，表示 Milvus 会为不断增长的数据段和搜索时未编入索引的密封数据段创建临时索引。
真
queryNode.segcore.interimIndex.nlist
描述
默认值
临时索引 nlist，建议设置为 sqrt（chunkRows），必须小于 chunkRows/8
128
queryNode.segcore.interimIndex.nprobe
说明
默认值
nprobe 用于搜索小索引，基于您的精度要求，必须小于 nlist
16
queryNode.segcore.interimIndex.memExpansionRate
说明
默认值
建立临时索引所需的额外内存
1.15
queryNode.segcore.interimIndex.buildParallelRate
说明
默认值
建立临时索引与 CPU 数量并行匹配的比率
0.5
queryNode.segcore.multipleChunkedEnable
说明
默认值
启用多分块搜索
真
queryNode.segcore.knowhereScoreConsistency
说明
默认值
启用 knowhere 强一致性得分计算逻辑
假
queryNode.loadMemoryUsageFactor
描述
默认值
计算加载分段时内存使用量的乘数系数
1
queryNode.enableDisk
说明
默认值
启用 querynode 加载磁盘索引，并在磁盘索引上搜索
假
queryNode.cache.memoryLimit
说明
默认值
2GB, 2 * 1024 *1024 *1024
2147483648
queryNode.cache.readAheadPolicy
说明
默认值
分块缓存的超前读取策略，可选项：正常、随机、顺序、需要、不需要
需要
queryNode.cache.warmup
说明
默认值
选项：async、sync、disable。
指定预热块缓存的必要性。
1.如果设置为 "sync"（同步）或 "async"（异步），原始向量数据将在加载过程中同步/异步加载到
在加载过程中，原始矢量数据将同步/异步加载到块缓存中。这种方法有可能在加载后的特定时间内大幅减少查询/搜索延迟。
尽管同时会增加磁盘使用量；
2.如果设置为 "禁用"，原始向量数据只会在搜索/查询过程中加载到块缓存中。
禁用
queryNode.mmap.vectorField
说明
默认值
启用 mmap 以加载向量数据
假
queryNode.mmap.vectorIndex
说明
默认值
启用 mmap 以加载向量索引
假
queryNode.mmap.scalarField
说明
默认值
为加载标量数据启用 mmap
假
queryNode.mmap.scalarIndex
说明
默认值
启用 mmap 以加载标量索引
假
queryNode.mmap.chunkCache
说明
默认值
启用用于大块缓存（原始向量检索）的 mmap。
真
queryNode.mmap.growingMmapEnabled
描述
默认值
启用内存映射（mmap）以优化处理不断增长的原始数据。
激活此功能后，与新添加或修改数据相关的内存开销将大大降低。
不过，这种优化可能会导致受影响数据段的查询延迟略有降低。
错误
queryNode.mmap.fixedFileSizeForMmapAlloc
说明
默认值
mmap 块管理器的 tmp 文件大小
1
queryNode.mmap.maxDiskUsagePercentageForMmapAlloc
说明
默认值
分块管理器使用的磁盘百分比
50
queryNode.lazyload.enabled
说明
默认值
启用加载数据的 lazyload
假
queryNode.lazyload.waitTimeout
说明
默认值
开始执行 lazyload 搜索和检索前的最大等待超时时间（毫秒
30000
queryNode.lazyload.requestResourceTimeout
说明
默认值
等待懒加载请求资源的最大超时（毫秒），默认为 5 秒
5000
queryNode.lazyload.requestResourceRetryInterval
说明
默认值
等待懒加载请求资源的重试间隔（毫秒），默认为 2 秒
2000
queryNode.lazyload.maxRetryTimes
说明
默认值
懒加载的最大重试次数，默认为 1
1
queryNode.lazyload.maxEvictPerRetry
说明
默认值
懒加载的最大驱逐次数，默认为 1
1
queryNode.indexOffsetCacheEnabled
说明
默认值
启用某些标量索引的索引偏移缓存，现在仅适用于位图索引，启用此参数可提高从索引中检索原始数据的性能
假
queryNode.scheduler.maxReadConcurrentRatio
说明
默认值
maxReadConcurrentRatio 是读取任务（搜索任务和查询任务）的并发比率。
最大读并发率为 hardware.GetCPUNum * maxReadConcurrentRatio 的值。
默认值为 2.0，即最大读并发量为 hardware.GetCPUNum * 2 的值。
最大读并发量必须大于或等于 1，小于或等于 hardware.GetCPUNum * 100。
(0, 100]
1
queryNode.scheduler.cpuRatio
说明
默认值
用于估算读取任务 CPU 占用率的比率。
10
queryNode.scheduler.scheduleReadPolicy.name
说明
默认值
fifo：支持计划的先进先出队列。
user-task-polling（用户任务轮询）：
用户任务将被逐个轮询并调度。
根据任务粒度进行公平调度。
策略基于用户名进行验证。
空用户名被视为同一用户。
当没有多用户时，策略衰减为先进先出"
先进先出
queryNode.scheduler.scheduleReadPolicy.taskQueueExpire
说明
默认值
控制队列清空后的保留时间（秒数
60
queryNode.scheduler.scheduleReadPolicy.enableCrossUserGrouping
说明
默认值
使用用户任务轮询策略时启用跨用户分组。(如果用户任务不能相互合并，则禁用）。
假
queryNode.scheduler.scheduleReadPolicy.maxPendingTaskPerUser
说明
默认值
调度程序中每个用户的最大待处理任务数
1024
queryNode.levelZeroForwardPolicy
说明
默认值
委托人级别的零删除前向策略，可能的选项["FilterByBF", "RemoteLoad"] （"FilterByBF"，"RemoteLoad
通过 BF 过滤
queryNode.streamingDeltaForwardPolicy
说明
默认值
委托人流删除前向策略，可选项["FilterByBF", "Direct"] （直接删除
过滤方式
queryNode.dataSync.flowGraph.maxQueueLength
说明
默认值
查询节点流图中任务队列缓存的最大大小。
16
queryNode.dataSync.flowGraph.maxParallelism
说明
默认值
流程图中并行执行的最大任务数
1024
queryNode.enableSegmentPrune
说明
默认值
在分片委托人的搜索/查询中使用分区统计剪裁数据
假
queryNode.queryStreamBatchSize
描述
默认值
返回流查询的最小批次大小
4194304
queryNode.queryStreamMaxBatchSize
说明
默认值
返回数据流查询的最大批次大小
134217728
queryNode.bloomFilterApplyParallelFactor
说明
默认值
将 pk 应用于 bloom 过滤器时的并行因子，默认为 4*CPU_CORE_NUM
4
queryNode.workerPooling.size
说明
默认值
工作流节点客户端池的大小
10
queryNode.ip
说明
默认值
查询节点的 TCP/IP 地址。如果未指定，则使用第一个单播地址
queryNode.port
说明
默认值
查询节点的 TCP 端口
21123
queryNode.grpc.serverMaxSendSize
说明
默认值
查询节点可发送的每个 RPC 请求的最大大小，单位：字节
536870912
queryNode.grpc.serverMaxRecvSize
单位：字节
默认值
查询节点可接收的每个 RPC 请求的最大大小，单位：字节
268435456
queryNode.grpc.clientMaxSendSize
单位：字节
默认值
查询节点客户端可发送的每个 RPC 请求的最大大小，单位：字节
268435456
queryNode.grpc.clientMaxRecvSize
单位：字节
默认值
查询节点客户端可接收的每个 RPC 请求的最大大小，单位：字节
536870912