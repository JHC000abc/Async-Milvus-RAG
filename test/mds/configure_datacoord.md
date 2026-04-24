数据相关配置
dataCoord.channel.watchTimeoutInterval
说明
默认值
观察通道的超时（秒）。数据节点 tickler 更新观察进度将重置超时计时器。
300
dataCoord.channel.legacyVersionWithoutRPCWatch
说明
默认值
<= 此版本的数据节点被视为传统节点，没有基于 rpc 的 watch()。只有在滚动升级时才会使用，此时传统节点不会获得新通道。
2.4.1
dataCoord.channel.balanceSilentDuration
说明
默认值
通道管理器开始后台通道平衡的持续时间
300
dataCoord.channel.balanceInterval
说明
默认值
频道管理器检查 dml 频道平衡状态的时间间隔
360
dataCoord.channel.checkInterval
说明
默认值
通道管理器前进通道状态的时间间隔（以秒为单位
1
dataCoord.channel.notifyChannelOperationTimeout
说明
默认值
通道操作通知超时（秒）。
5
dataCoord.segment.maxSize
说明
默认值
数据段的最大大小，单位：MB：datacoord.segment.maxSize 和 datacoord.segment.sealProportion 共同决定是否可以封存段。
1024
dataCoord.segment.diskSegmentMaxSize
说明
默认值
具有磁盘索引的 Collections 的最大数据段大小（MB
2048
dataCoord.segment.sealProportion
说明
默认值
datacoord.segment.maxSize 与 datacoord.segment.sealProportion 的最小比例，用于封存数据段。datacoord.segment.maxSize 和 datacoord.segment.sealProportion 共同决定是否可以封存数据段。
0.12
dataCoord.segment.sealProportionJitter
说明
默认值
段密封比例抖动率，默认值 0.1（10%），如果密封比例为 12%，抖动率=0.1，则实际应用比例为 10.8~12
0.1
dataCoord.segment.assignmentExpiration
说明
默认值
段分配的有效时间，单位：毫秒
2000
dataCoord.segment.allocLatestExpireAttempt
说明
默认值
重启后尝试从 rootCoord 分配最新 lastExpire 的时间
200
dataCoord.segment.maxLife
说明
默认值
段的最大生命周期（秒），24*60*60
86400
dataCoord.segment.maxIdleTime
说明
默认值
如果一个网段在 maxIdleTime 内没有接受 dml 记录，且网段大小大于
minSizeFromIdleToSealed 时，Milvus 会自动将其封存。
段的最大空闲时间，单位为秒，10*60。
600
dataCoord.segment.minSizeFromIdleToSealed
说明
默认值
从密封到空闲的最小分段大小（MB）。
16
dataCoord.segment.maxBinlogFileNumber
说明
默认值
一个段的最大 binlog 数量（等于主键的 binlog 文件数）、
如果 binlog 文件数达到最大值，则将封段。
32
dataCoord.segment.smallProportion
说明
默认值
当数据段的行数小于
0.5
dataCoord.segment.compactableProportion
说明
默认值
(smallProportion * segment max # of rows）。
如果压缩后的数据段有
0.85
dataCoord.segment.expansionRate
说明
默认值
超过 (compactableProportion * segment max # of rows) 行数。
必须大于或等于
!!!！
在压缩过程中，段的行数可以超过段的最大行数 (expansionRate-1) * 100%。
1.25
dataCoord.sealPolicy.channel.growingSegmentsMemSize
说明
默认值
以 MB 为单位的大小阈值。
如果每个分片的增长分段的总大小超过此阈值，最大的增长分段将被封存。
4096
dataCoord.autoUpgradeSegmentIndex
说明
默认值
是否将分段索引自动升级为索引引擎版本
假
dataCoord.segmentFlushInterval
说明
默认值
对同一分段进行复用操作的最小间隔时间（单位：秒
2
dataCoord.enableCompaction
说明
默认值
控制是否启用段压缩的开关值。
压缩会将较小的分段合并为一个较大的分段，并清除超出 Time Travel 租期的已删除实体。
真
dataCoord.compaction.enableAutoCompaction
描述
默认值
控制是否启用自动分段压缩的开关值，在此过程中 Data coord 会在后台定位并合并可压缩的分段。
此配置仅在 dataCoord.enableCompaction 设置为 true 时生效。
true
dataCoord.compaction.taskPrioritizer
说明
默认值
compaction 任务优先级，选项：[默认值为 FIFO。］
默认为先进先出。
级别优先：首先是 L0 压缩，然后是混合压缩，最后是聚类压缩。
mix 按级别排序：先混合压缩，再 L0 压缩，最后聚类压缩。
默认值
dataCoord.compaction.taskQueueCapacity
说明
默认值
压实任务队列大小
100000
dataCoord.compaction.dropTolerance
描述
默认值
压实任务完成时间超过此时间（秒）后将被清理
86400
dataCoord.compaction.gcInterval
说明
默认值
压实时间间隔（秒） gc
1800
dataCoord.compaction.mix.triggerInterval
说明
默认值
触发混合压实的时间间隔（以秒为单位
60
dataCoord.compaction.levelzero.triggerInterval
说明
默认值
触发 L0 压实的时间间隔（以秒为单位
10
dataCoord.compaction.levelzero.forceTrigger.minSize
描述
默认值
强制触发零级压缩的最小大小（以字节为单位），默认为 8MB
8388608
dataCoord.compaction.levelzero.forceTrigger.maxSize
说明
默认值
强制触发零级压缩的最大字节数，默认为 64MB
67108864
dataCoord.compaction.levelzero.forceTrigger.deltalogMinNum
说明
默认值
强制触发零级压缩的最小 deltalog 文件数量
10
dataCoord.compaction.levelzero.forceTrigger.deltalogMaxNum
说明
默认值
强制触发零级压缩的最大分录文件数，默认为 30
30
dataCoord.compaction.single.ratio.threshold
说明
默认值
触发单次压缩的段比率阈值，默认为 0.2
0.2
dataCoord.compaction.single.deltalog.maxsize
说明
默认值
触发单次压缩的分段日志大小，默认为 16MB
16777216
dataCoord.compaction.single.deltalog.maxnum
说明
默认值
触发压缩的分段日志计数，默认为 200
200
dataCoord.compaction.single.expiredlog.maxsize
说明
默认值
触发压缩的段的过期日志大小，默认为 10MB
10485760
dataCoord.compaction.clustering.enable
说明
默认值
启用群集压缩
真
dataCoord.compaction.clustering.autoEnable
说明
默认值
启用自动聚类压缩
假
dataCoord.compaction.clustering.triggerInterval
描述
默认值
聚类压缩触发间隔（秒
600
dataCoord.compaction.clustering.minInterval
描述
默认值
执行一个 Collection 的聚类压缩之间的最小间隔，以避免冗余压缩
3600
dataCoord.compaction.clustering.maxInterval
说明
默认值
如果一个 Collections 的聚类压缩时间没有超过 maxInterval，则强制压缩
259200
dataCoord.compaction.clustering.newDataSizeThreshold
说明
默认值
如果新数据大小大于 newDataSizeThreshold，则执行聚类压缩
512m
dataCoord.compaction.clustering.maxTrainSizeRatio
说明
默认值
Kmeans 训练中的最大数据大小比率，如果大于该比率，将减少采样以满足此限制
0.8
dataCoord.compaction.clustering.maxCentroidsNum
说明
默认值
均值训练中的最大中心点数量
10240
dataCoord.compaction.clustering.minCentroidsNum
说明
默认值
均值序列中的最小中心点数
16
dataCoord.compaction.clustering.minClusterSizeRatio
说明
默认值
均值训练中的最小聚类大小/平均大小
0.01
dataCoord.compaction.clustering.maxClusterSizeRatio
说明
默认值
最大聚类大小/克均值训练中的平均大小
10
dataCoord.compaction.clustering.maxClusterSize
说明
默认值
均值训练中的最大聚类规模
5g
dataCoord.syncSegmentsInterval
描述
默认值
定期同步片段的时间间隔
300
dataCoord.index.memSizeEstimateMultiplier
说明
默认值
索引程序未设置内存大小时，用于估算索引数据内存大小的乘数
2
dataCoord.enableGarbageCollection
说明
默认值
用于控制 MinIO 或 S3 服务中是否启用垃圾 Collections 以清除丢弃数据的开关值。
真
dataCoord.gc.interval
说明
默认值
Data coord 执行垃圾收集的时间间隔，单位：秒。
3600
dataCoord.gc.missingTolerance
说明
默认值
未记录的二进制日志 (binlog) 文件的保留时间。为该参数设置一个合理的大值可避免错误删除新创建的缺少元数据的 binlog 文件。单位：秒。
86400
dataCoord.gc.dropTolerance
说明
默认值
已删除段的 binlog 文件被清除前的保留时间，单位：秒。
10800
dataCoord.gc.removeConcurrent
说明
默认值
删除已删除 s3 对象的并发程序数
32
dataCoord.gc.scanInterval
说明
默认值
对象存储上的无主文件（文件在 oss 上，但尚未在 meta 上注册）垃圾收集扫描间隔（小时
168
dataCoord.brokerTimeout
说明
默认值
5000ms，dataCoord 代理 rpc 超时
5000
dataCoord.autoBalance
说明
默认值
启用自动平衡
真
dataCoord.checkAutoBalanceConfigInterval
说明
默认值
检查自动平衡配置的时间间隔
10
dataCoord.import.filesPerPreImportTask
说明
默认值
每个预导入任务允许的最大文件数。
2
dataCoord.import.taskRetention
说明
默认值
已完成或已失败状态下任务的保留时间（以秒为单位）。
10800
dataCoord.import.maxSizeInMBPerImportTask
说明
默认值
为防止生成小片段，我们将对导入的文件重新分组。该参数表示每个组（每个 ImportTask）中文件大小的总和。
6144
dataCoord.import.scheduleInterval
说明
默认值
调度导入的时间间隔，以秒为单位。
2
dataCoord.import.checkIntervalHigh
说明
默认值
检查导入的时间间隔（以秒为单位）设置为导入检查器的高频率。
2
dataCoord.import.checkIntervalLow
说明
默认值
检查导入的时间间隔（以秒为单位）设置为导入检查器的低频率。
120
dataCoord.import.maxImportFileNumPerReq
说明
默认值
单个导入请求允许的最大文件数。
1024
dataCoord.import.maxImportJobNum
说明
默认值
正在执行或等待执行的导入任务的最大数量。
1024
dataCoord.import.waitForIndex
说明
默认值
表示导入操作是否等待索引建立完成。
真
dataCoord.gracefulStopTimeout
说明
默认值
强制停止节点而不优雅停止
5
dataCoord.slot.clusteringCompactionUsage
说明
默认值
聚类压缩任务的槽位使用量。
16
dataCoord.slot.mixCompactionUsage
说明
默认值
混合压缩任务的槽位使用量。
8
dataCoord.slot.l0DeleteCompactionUsage
说明
默认值
L0 压实任务的插槽使用量。
8
dataCoord.ip
说明
默认值
dataCoord 的 TCP/IP 地址。如果未指定，则使用第一个单播地址
dataCoord.port
说明
默认值
数据协调中心的 TCP 端口
13333
dataCoord.grpc.serverMaxSendSize
说明
默认值
dataCoord 可以发送的每个 RPC 请求的最大大小，单位：字节
536870912
dataCoord.grpc.serverMaxRecvSize
单位：字节
默认值
dataCoord 可以接收的每个 RPC 请求的最大大小，单位：字节
268435456
dataCoord.grpc.clientMaxSendSize
单位：字节
默认值
dataCoord 客户端可发送的每个 RPC 请求的最大大小，单位：字节
268435456
dataCoord.grpc.clientMaxRecvSize
单位：字节
默认值
dataCoord 客户端可接收的每个 RPC 请求的最大大小，单位：字节
536870912