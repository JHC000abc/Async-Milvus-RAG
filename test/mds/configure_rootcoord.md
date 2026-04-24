rootCoord 相关配置
rootCoord 的相关配置，用于处理数据定义语言 (DDL) 和数据控制语言 (DCL) 请求
rootCoord.dmlChannelNum
说明
默认值
在 Root coord 启动时创建的 DML 通道数。
16
rootCoord.maxPartitionNum
说明
默认值
每个 Collection 中分区的最大数量。
如果该参数设置为 0 或 1，则无法创建新分区。
范围[0，INT64MAX］
1024
rootCoord.minSegmentSizeToEnableIndex
说明
默认值
创建索引所需的最小段行数。
小于此参数的分段将不会被索引，而会被暴力搜索。
1024
rootCoord.maxDatabaseNum
说明
默认值
数据库的最大数量
64
rootCoord.maxGeneralCapacity
说明
默认值
分区编号与分区编号乘积之和的上限
65536
rootCoord.gracefulStopTimeout
说明
默认值
秒。强制停止节点而不优雅停止
5
rootCoord.ip
说明
默认值
rootCoord 的 TCP/IP 地址。如果未指定，则使用第一个单播地址。
rootCoord.port
说明
默认值
根节点的 TCP 端口
53100
rootCoord.grpc.serverMaxSendSize
说明
默认值
rootCoord 可以发送的每个 RPC 请求的最大大小，单位：字节
536870912
rootCoord.grpc.serverMaxRecvSize
单位：字节
默认值
rootCoord 可以接收的每个 RPC 请求的最大大小，单位：字节
268435456
rootCoord.grpc.clientMaxSendSize
单位：字节
默认值
rootCoord 上的客户端可发送的每个 RPC 请求的最大大小，单位：字节
268435456
rootCoord.grpc.clientMaxRecvSize
单位：字节
默认值
rootCoord 上的客户端可以接收的每个 RPC 请求的最大大小，单位：字节
536870912