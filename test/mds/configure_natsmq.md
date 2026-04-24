natsmq 相关配置
natsmq 配置。
更多详情： https://docs.nats.io/running-a-nats-service/configuration
natsmq.server.port
说明
默认值
NATS 服务器的监听端口。
4222
natsmq.server.storeDir
说明
默认值
用于 JetStream 存储 NATS 的目录
/var/lib/milvus/nats
natsmq.server.maxFileStore
说明
默认值
文件 "存储的最大大小
17179869184
natsmq.server.maxPayload
说明
默认值
信息有效载荷的最大字节数
8388608
natsmq.server.maxPending
说明
默认值
连接缓冲的最大字节数 适用于客户端连接
67108864
natsmq.server.initializeTimeout
说明
默认值
等待 natsmq 初始化完成
4000
natsmq.server.monitor.trace
说明
默认值
如果为 true，则启用协议跟踪日志信息
假
natsmq.server.monitor.debug
说明
默认值
如果为 true，则启用调试日志信息
假
natsmq.server.monitor.logTime
说明
默认值
如果设置为 false，日志将不带时间戳。
true
natsmq.server.monitor.logFile
说明
默认值
如果使用相对路径，则日志文件路径为 milvus 二进制文件的...相对路径
/tmp/milvus/logs/nats.log
natsmq.server.monitor.logSizeLimit
说明
默认值
日志文件滚动到新文件后的大小（以字节为单位
536870912
natsmq.server.retention.maxAge
说明
默认值
P 信道中任何报文的最大年龄
4320
natsmq.server.retention.maxBytes
说明
默认值
单个 P 信道可包含的字节数。如果 P 信道超过此大小，则删除最旧的报文
natsmq.server.retention.maxMsgs
说明
默认值
单个 P 信道可包含的报文数量。如果 P 信道超过此限制，则删除最旧的信息