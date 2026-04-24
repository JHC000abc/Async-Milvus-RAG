queryCoord 相关配置
queryCoord 的相关配置，用于管理查询节点的拓扑和负载平衡，以及从增长区段到封存区段的切换。
queryCoord.autoHandoff
说明
默认值
开关值，用于控制当增长区段达到密封阈值时，是否用相应的索引密封区段自动替换增长区段。
如果该参数设置为 false，Milvus 就会简单地使用蛮力搜索正在增长的数据段。
真
queryCoord.autoBalance
描述
默认值
切换值，用于控制是否通过平均分配分段加载和释放操作来自动平衡查询节点之间的内存使用。
true
queryCoord.autoBalanceChannel
说明
默认值
启用自动平衡通道
true
queryCoord.balancer
说明
默认值
用于查询节点上分段的自动平衡器
基于分数的平衡器
queryCoord.globalRowCountFactor
说明
默认值
平衡查询节点上的分段时使用的权重
0.1
queryCoord.scoreUnbalanceTolerationFactor
说明
默认值
进行平衡时，从节点到节点之间不平衡范围的最小值
0.05
queryCoord.reverseUnBalanceTolerationFactor
说明
默认值
平衡后起点和终点节点间不平衡范围的最大值
1.3
queryCoord.overloadedMemoryThresholdPercentage
说明
默认值
查询节点中内存使用量的阈值（百分比），用于触发密封段平衡。
90
queryCoord.balanceIntervalSeconds
说明
默认值
query coord 平衡各查询节点内存使用量的时间间隔。
60
queryCoord.memoryUsageMaxDifferencePercentage
说明
默认值
任意两个查询节点之间内存使用量差异（百分比）的阈值，用于触发密封段平衡。
30
queryCoord.rowCountFactor
说明
默认值
平衡查询节点之间的分段时使用的行计数权重
0.4
queryCoord.segmentCountFactor
说明
默认值
平衡查询节点之间的分段时使用的分段计数权重
0.4
queryCoord.globalSegmentCountFactor
说明
默认值
平衡查询节点之间的分段时使用的分段计数权重
0.1
queryCoord.collectionChannelCountFactor
说明
默认值
在平衡查询节点之间的通道时使用的通道计数权重、
数值越大，将同一 Collections 中的通道分配给同一查询节点的可能性就越小。设为 1 则禁用此功能。
10
queryCoord.segmentCountMaxSteps
说明
默认值
基于段计数的计划生成器最大步长
50
queryCoord.rowCountMaxSteps
说明
默认值
基于段计数的计划生成器最大步数
50
queryCoord.randomMaxSteps
说明
默认值
基于段计数的计划生成器最大步数
10
queryCoord.growingRowCountWeight
说明
默认值
增长段行数的内存权重
4
queryCoord.delegatorMemoryOverloadFactor
说明
默认值
委托人超载内存系数
0.1
queryCoord.balanceCostThreshold
说明
默认值
平衡成本阈值，如果执行平衡计划后群组成本的差值小于此值，则不执行该计划
0.001
queryCoord.channelTaskTimeout
说明
默认值
1 分钟
60000
queryCoord.segmentTaskTimeout
说明
默认值
2 分钟
120000
queryCoord.heartbeatAvailableInterval
说明
默认值
10s，只有在持续时间内获取心跳的查询节点可用
10000
queryCoord.distRequestTimeout
说明
默认值
querycoord 从查询节点获取数据分发的请求超时，毫秒数
5000
queryCoord.heatbeatWarningLag
说明
默认值
当最后一次热量采集时间过长时，querycoord 报告警告的滞后值（毫秒
5000
queryCoord.checkHealthInterval
说明
默认值
3 秒，Query coord 尝试检查查询节点健康状况的时间间隔
3000
queryCoord.checkHealthRPCTimeout
说明
默认值
100ms，向查询节点发送检查健康状况 rpc 的超时时间
2000
queryCoord.brokerTimeout
说明
默认值
5000ms，querycoord 代理 rpc 超时
5000
queryCoord.collectionRecoverTimes
说明
默认值
如果在加载状态下，Collection 恢复时间达到上限，则将其释放
3
queryCoord.observerTaskParallel
说明
默认值
并行观察者调度任务编号
16
queryCoord.checkAutoBalanceConfigInterval
说明
默认值
检查自动平衡配置的时间间隔
10
queryCoord.checkNodeSessionInterval
说明
默认值
检查多节点集群会话的时间间隔（秒
60
queryCoord.gracefulStopTimeout
说明
默认值
强制停止节点而不优雅停止
5
queryCoord.enableStoppingBalance
说明
默认值
是否启用停止平衡
真
queryCoord.channelExclusiveNodeFactor
说明
默认值
启用通道独占模式的最小节点编号
4
queryCoord.collectionObserverInterval
说明
默认值
Collections 观察器的时间间隔
200
queryCoord.checkExecutedFlagInterval
描述
默认值
检查执行标志的时间间隔，以强制拉取 dist
100
queryCoord.updateCollectionLoadStatusInterval
说明
默认值
5m，为检查健康状况更新 Collections 已加载状态的最大时间间隔
5
queryCoord.cleanExcludeSegmentInterval
说明
默认值
用于过滤无效数据的清理管道排除段的持续时间，以秒为单位
60
queryCoord.ip
说明
默认值
queryCoord 的 TCP/IP 地址。如果未指定，则使用第一个单播地址
queryCoord.port
说明
默认值
查询协调中心的 TCP 端口
19531
queryCoord.grpc.serverMaxSendSize
说明
默认值
queryCoord 可以发送的每个 RPC 请求的最大大小，单位：字节
536870912
queryCoord.grpc.serverMaxRecvSize
单位：字节
默认值
queryCoord 可以接收的每个 RPC 请求的最大大小，单位：字节
268435456
queryCoord.grpc.clientMaxSendSize
单位：字节
默认值
queryCoord 上的客户端可发送的每个 RPC 请求的最大大小，单位：字节
268435456
queryCoord.grpc.clientMaxRecvSize
单位：字节
默认值
queryCoord 客户端可接收的每个 RPC 请求的最大大小，单位：字节
536870912