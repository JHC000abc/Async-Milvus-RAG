数据节点相关配置
dataNode.dataSync.flowGraph.maxQueueLength
说明
默认值
流程图中任务队列的最大长度
16
dataNode.dataSync.flowGraph.maxParallelism
说明
默认值
流程图中并行执行任务的最大数量
1024
dataNode.dataSync.maxParallelSyncMgrTasks
说明
默认值
数据节点同步管理器的全球最大并发同步任务数
256
dataNode.dataSync.skipMode.enable
说明
默认值
支持跳过某些时间戳信息以降低 CPU 占用率
真
dataNode.dataSync.skipMode.skipNum
说明
默认值
每跳过 n 条记录消耗一条
4
dataNode.dataSync.skipMode.coldTime
说明
默认值
在 x 秒内只有时间戳消息后开启跳过模式
60
dataNode.segment.insertBufSize
说明
默认值
内存缓冲段中每个 Binlog 文件的最大大小。超过此值的日志文件会被刷新到 MinIO 或 S3 服务。
单位：字节字节
将此参数设置得过小，会导致系统过于频繁地存储少量数据。设置过大则会增加系统对内存的需求。
16777216
dataNode.segment.deleteBufBytes
说明
默认值
单通道刷新 del 的最大缓冲区大小（字节），默认为 16MB。
16777216
dataNode.segment.syncPeriod
说明
默认值
缓冲区未清空时同步段的周期。
600
dataNode.memory.forceSyncEnable
说明
默认值
设置为 true 可在内存使用率过高时强制同步
true
dataNode.memory.forceSyncSegmentNum
说明
默认值
要同步的分段数，缓冲区最大的分段将被同步。
1
dataNode.memory.checkInterval
说明
默认值
检查数据节点内存使用情况的间隔时间（毫秒
3000
dataNode.memory.forceSyncWatermark
说明
默认值
单机版内存水印，达到此水印后，将同步分段。
0.5
dataNode.channel.workPoolSize
说明
默认值
指定所有通道的全局工作池大小
如果该参数 <= 0，则将其设置为可执行 CPU 的最大数量
建议在收集数量较大时将其设置得更大，以避免阻塞
-1
dataNode.channel.updateChannelCheckpointMaxParallel
说明
默认值
指定通道检查点更新的全局工作池大小
如果该参数 <= 0，则设置为 10
10
dataNode.channel.updateChannelCheckpointInterval
说明
默认值
数据节点更新每个通道的通道检查点的时间间隔（以秒为单位
60
dataNode.channel.updateChannelCheckpointRPCTimeout
说明
默认值
UpdateChannelCheckpoint RPC 调用的超时时间（秒
20
dataNode.channel.maxChannelCheckpointsPerPRC
说明
默认值
每次 UpdateChannelCheckpoint RPC 的最大通道检查点数量。
128
dataNode.channel.channelCheckpointUpdateTickInSeconds
说明
默认值
通道检查点更新器执行更新的频率（以秒为单位）。
10
dataNode.import.maxConcurrentTaskNum
说明
默认值
数据节点上允许同时运行的导入/预导入任务的最大数量。
16
dataNode.import.maxImportFileSizeInGB
说明
默认值
导入文件的最大文件大小（GB），其中导入文件指基于行的文件或基于列的文件集。
16
dataNode.import.readBufferSizeInMB
说明
默认值
导入期间数据节点从块管理器读取的数据块大小（单位 MB）。
16
dataNode.import.maxTaskSlotNum
说明
默认值
每个导入/预导入任务占用的最大槽位数。
16
dataNode.compaction.levelZeroBatchMemoryRatio
说明
默认值
以批处理模式执行零级压缩时可用内存的最小内存比率
0.5
dataNode.compaction.levelZeroMaxBatchSize
说明
默认值
最大批量大小是指执行 L0 压缩时，批量中 L1/L2 段的最大数量。默认值为-1，任何小于 1 的值都表示没有限制。有效范围>= 1.
-1
dataNode.compaction.useMergeSort
说明
默认值
执行 mixCompaction 时是否启用 mergeSort（合并排序）模式。
假
dataNode.compaction.maxSegmentMergeSort
说明
默认值
在合并排序模式下要合并的最大数据段数。
30
dataNode.gracefulStopTimeout
说明
默认值
秒。强制停止节点而不优雅停止
1800
dataNode.slot.slotCap
说明
默认值
允许在数据节点上并发运行的任务（如压缩、导入）的最大数量
16
dataNode.clusteringCompaction.memoryBufferRatio
说明
默认值
集群压缩内存缓冲区的比率。大于阈值的数据将被刷新到存储空间。
0.3
dataNode.clusteringCompaction.workPoolSize
说明
默认值
一个聚类压缩任务的工作池大小。
8
dataNode.bloomFilterApplyParallelFactor
说明
默认值
将 pk 应用于 bloom 过滤器时的并行因子，默认为 4*CPU_CORE_NUM
4
dataNode.storage.deltalog
说明
默认值
deltalog 格式，选项[json, parquet］
json
dataNode.ip
说明
默认值
数据节点的 TCP/IP 地址。如果未指定，则使用第一个可单播地址
dataNode.port
说明
默认值
数据节点的 TCP 端口
21124
dataNode.grpc.serverMaxSendSize
说明
默认值
数据节点可发送的每个 RPC 请求的最大大小，单位：字节
536870912
dataNode.grpc.serverMaxRecvSize
单位：字节
默认值
数据节点可接收的每个 RPC 请求的最大大小，单位：字节
268435456
dataNode.grpc.clientMaxSendSize
单位：字节
默认值
数据节点客户端可发送的每个 RPC 请求的最大大小，单位：字节
268435456
dataNode.grpc.clientMaxRecvSize
单位：字节
默认值
数据节点客户端可接收的每个 RPC 请求的最大大小，单位：字节
536870912