代理相关配置
代理的相关配置，用于验证客户端请求并减少返回结果。
proxy.timeTickInterval
说明
默认值
代理同步时间刻度的时间间隔，单位：毫秒。
200
proxy.healthCheckTimeout
说明
默认值
毫秒，进行组件健康检查的时间间隔
3000
proxy.msgStream.timeTick.bufSize
说明
默认值
生成信息时，代理的 timeTick 信息流中可缓冲的最大信息量。
512
proxy.maxNameLength
说明
默认值
Milvus 中可创建的名称或别名的最大长度，包括集合名称、集合别名、分区名称和字段名称。
255
proxy.maxFieldNum
说明
默认值
在 Collections 中创建时可创建字段的最大数量。强烈建议设置 maxFieldNum >= 64。
64
proxy.maxVectorFieldNum
说明
默认值
可在 Collections 中指定的最大向量字段数量。取值范围[1, 10].
4
proxy.maxShardNum
说明
默认值
在 Collections 中创建分片时可创建的最大数量。
16
proxy.maxDimension
描述
默认值
在集合中创建向量时的最大维数。
32768
proxy.ginLogging
描述
默认值
是否生成吟唱日志。
请在嵌入式 Milvus 中调整：false
true
proxy.ginLogSkipPaths
说明
默认值
跳过 gin 日志的 URL 路径
/
proxy.maxTaskNum
说明
默认值
代理任务队列中任务的最大数量。
1024
proxy.ddlConcurrency
说明
默认值
代理 DDL 的并发执行数。
16
proxy.dclConcurrency
说明
默认值
代理处 DCL 的并发执行次数。
16
proxy.mustUsePartitionKey
说明
默认值
代理是否必须使用 Collections 分区密钥的开关
假
proxy.accessLog.enable
说明
默认值
是否启用访问日志功能。
假
proxy.accessLog.minioEnable
说明
默认值
是否将本地访问日志文件上传到 MinIO。此参数可在 proxy.accessLog.filename 不为空时指定。
假
proxy.accessLog.localPath
说明
默认值
存储访问日志文件的本地文件夹路径。当 proxy.accessLog.filename 不为空时，可以指定此参数。
/tmp/milvus_access
proxy.accessLog.filename
说明
默认值
访问日志文件的名称。如果将此参数留空，访问日志将打印到 stdout。
proxy.accessLog.maxSize
说明
默认值
单个访问日志文件允许的最大大小。如果日志文件大小达到此限制，将触发一个轮转进程。该过程会封存当前访问日志文件，创建新的日志文件，并清除原始日志文件的内容。单位：MB：MB。
64
proxy.accessLog.rotatedTime
说明
默认值
允许轮换单个访问日志文件的最大时间间隔。达到指定时间间隔后，将触发轮换过程，创建新的访问日志文件并封存之前的文件。单位：秒
0
proxy.accessLog.remotePath
单位：秒
默认值
用于上传访问日志文件的对象存储路径。
access_log/
proxy.accessLog.remoteMaxTime
说明
默认值
允许上传访问日志文件的时间间隔。如果日志文件的上传时间超过此时间间隔，文件将被删除。将值设为 0 则禁用此功能。
0
proxy.accessLog.cacheSize
说明
默认值
写缓存日志的大小（字节）。(如果大小为 0，则关闭写缓存）
0
proxy.accessLog.cacheFlushInterval
说明
默认值
自动刷新写缓存的时间间隔，单位为秒。(如果间隔为 0，则关闭自动刷新）
3
proxy.connectionCheckIntervalSeconds
说明
默认值
连接管理器扫描非活动客户端信息的时间间隔（秒）。
120
proxy.connectionClientInfoTTLSeconds
说明
默认值
非活动客户端信息 TTL 持续时间（秒
86400
proxy.maxConnectionNum
说明
默认值
代理应管理的最大客户信息数量，避免客户信息过多
10000
proxy.gracefulStopTimeout
说明
默认值
秒。强制停止节点而不优雅停止
30
proxy.slowQuerySpanInSeconds
说明
默认值
执行时间超过 `slowQuerySpanInSeconds` 的查询将被视为慢查询，单位为秒。
5
proxy.queryNodePooling.size
说明
默认值
分片领导（查询节点）客户池的大小
10
proxy.http.enabled
说明
默认值
是否启用 http 服务器
真
proxy.http.debug_mode
说明
默认值
是否启用 http 服务器调试模式
假
proxy.http.port
说明
默认值
高级恢复性应用程序接口
proxy.http.acceptTypeAllowInt64
说明
默认值
高级重定向 api，http 客户端是否可以处理 int64
true
proxy.http.enablePprof
说明
默认值
是否在度量端口上启用 pprof 中间件
true
proxy.ip
说明
默认值
代理的 TCP/IP 地址。如果未指定，则使用第一个单播地址
proxy.port
说明
默认值
代理的 TCP 端口
19530
proxy.grpc.serverMaxSendSize
说明
默认值
代理可发送的每个 RPC 请求的最大大小，单位：字节
268435456
proxy.grpc.serverMaxRecvSize
单位：字节
默认值
代理可接收的每个 RPC 请求的最大大小，单位：字节
67108864
proxy.grpc.clientMaxSendSize
单位：字节
默认值
代理客户端可发送的每个 RPC 请求的最大大小，单位：字节
268435456
proxy.grpc.clientMaxRecvSize
单位：字节
默认值
代理客户端可接收的每个 RPC 请求的最大大小，单位：字节
67108864