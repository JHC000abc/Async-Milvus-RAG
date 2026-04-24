mq 相关配置
Milvus 支持四种 MQ：rocksmq（基于 RockDB）、Pulsar、Kafka 和 Woodpecker。
您可以通过设置 mq.type 字段来更改您的 MQ。
如果不将 mq.type 字段设为默认值，那么在该文件中，如果我们配置了多个 MQ，会有一个关于启用优先级的说明。
独立（本地）模式：Rocksmq（默认） > Pulsar > Kafka
集群模式：  Pulsar（默认） > Kafka（集群模式下不支持 rocksmq）
通过将 mq.type 设置为 woodpecker，Woodpecker 可以在单机和集群模式下使用。
mq.type
说明
默认值
默认值："默认"
有效值：[默认、脉冲星、卡夫卡、rocksmq、啄木鸟］
默认
mq.enablePursuitMode
描述
默认值
默认值："true
true
mq.pursuitLag
说明
默认值
进入追赶模式的时间勾选滞后阈值，单位为秒
10
mq.pursuitBufferSize
描述
默认值
追赶模式缓冲区大小（字节
8388608
mq.pursuitBufferTime
说明
默认值
追赶模式缓冲时间（秒
60
mq.mqBufSize
说明
默认值
MQ 客户端消费者缓冲区长度
16
mq.dispatcher.mergeCheckInterval
说明
默认值
派发器检查是否合并的间隔时间（秒）。
1
mq.dispatcher.targetBufSize
说明
默认值
用于合并的通道缓冲区长度
16
mq.dispatcher.maxTolerantLag
说明
默认值
默认值：3"，目标发送 msgPack 的超时（秒）。
3
mq.dispatcher.maxDispatcherNumPerPchannel
说明
默认值
每个物理通道的最大调度器数量，主要用于限制消费者数量，防止出现性能问题（例如，在恢复过程中需要监控大量通道时）。
5
mq.dispatcher.retrySleep
说明
默认值
寄存器重试休眠时间（秒
3
mq.dispatcher.retryTimeout
说明
默认值
寄存器重试超时（秒
60