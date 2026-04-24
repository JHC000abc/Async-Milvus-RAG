Milvus 系统配置检查表
本主题介绍 Milvus 系统配置的一般部分。
Milvus 维护着相当多的系统配置参数。每个配置都有一个默认值，可以直接使用。您可以灵活修改这些参数，使 Milvus 能更好地服务于您的应用程序。更多信息，请参阅
配置 Milvus
。
在当前版本中，所有参数只有在启动 Milvus 时配置后才会生效。
章节
为方便维护，Milvus 根据组件、依赖关系和一般用法将配置分为 %s 个部分。
etcd
etcd 的相关配置，用于存储 Milvus 元数据和服务发现。
请参阅
etcd 相关配置
，了解该部分下每个参数的详细说明。
metastore
本节下各参数的详细说明，请参见
元存储相关配置
。
tikv
用于存储 Milvus 元数据的 tikv 的相关配置。
请注意，启用 TiKV 作为元存储时，仍需要使用 etcd 来发现服务。
当元数据大小需要更好的横向扩展能力时，TiKV 是一个不错的选择。
有关本节下各参数的详细说明，请参见
tikv 相关配置
。
localStorage
本节下各参数的详细说明，请参见
localStorage 相关配置
。
minio
MinIO/S3/GCS 或其他支持 S3 API 的服务的相关配置，S3 API 负责 Milvus 的数据持久化。
为简单起见，我们在下文中将存储服务称为 MinIO/S3。
本节下每个参数的详细说明请参见
minio 相关配置
。
mq
Milvus 支持四种 MQ：rocksmq（基于 RockDB）、Pulsar、Kafka 和 Woodpecker。
你可以通过设置 mq.type 字段来更改你的 MQ。
如果不将 mq.type 字段设为默认值，那么在该文件中，如果我们配置了多个 MQ，会有一个关于启用优先级的说明。
独立（本地）模式：Rocksmq（默认） > Pulsar > Kafka
集群模式：  Pulsar（默认） > Kafka（集群模式下不支持 rocksmq）
通过将 mq.type 设置为 woodpecker，Woodpecker 可在独立模式和集群模式下使用。
本节下每个参数的详细说明，请参见
mq 相关配置
。
pulsar
pulsar 的相关配置，用于管理最近突变操作的 Milvus 日志，输出流式日志，并提供日志发布-订阅服务。
本节下各参数的详细说明，请参见
pulsar 相关配置
。
rocksmq
如果要启用 kafka，需要对 pulsar 配置进行注释
kafka：
brokerList: localhost:9092
saslUsername：
saslPassword：
saslMechanisms：
securityProtocol：
ssl：
enabled: false # whether to enable ssl mode

tlsCert:  # path to client's public key (PEM) used for authentication

tlsKey:  # path to client's private key (PEM) used for authentication

tlsCaCert:  # file or directory path to CA certificate(s) for verifying the broker's key

tlsKeyPassword:  # private key passphrase for use with ssl.key.location and set_ssl_cert(), if any
readTimeout：10
本节下各参数的详细说明，请参见
rocksmq 相关配置
。
rootCoord
rootCoord 的相关配置，用于处理数据定义语言（DDL）和数据控制语言（DCL）请求
有关本节中各参数的详细说明，请参见
rootCoord 相关配置
。
proxy
代理相关配置，用于验证客户端请求并减少返回结果。
有关本节中各参数的详细说明，请参见
代理相关配置
。
queryCoord
queryCoord 的相关配置用于管理查询节点的拓扑和负载平衡，以及从增长网段到封存网段的切换。
有关本节中每个参数的详细说明，请参阅
queryCoord 相关配置
。
queryNode
queryNode 的相关配置，用于在向量和标量数据之间运行混合搜索。
有关本节中各参数的详细说明，请参见
查询
节点
相关配置
。
indexCoord
有关本节中每个参数的详细说明，请参见
indexCoord 相关配置
。
indexNode
有关本节中每个参数的详细说明，请参见
indexNode 相关配置
。
dataCoord
请参阅
dataCoord-related Configurations（数据
节点
相关配置
），了解本节中各参数的详细说明。
dataNode
请参阅
dataNode-related Configurations（数据节点相关配置
），了解本节下各参数的详细说明。
msgChannel
本主题介绍 Milvus 的消息通道相关配置。
本节下各参数的详细说明，请参见
msgChannel 相关配置
。
log
配置系统日志输出。
本节下各参数的详细说明，请参见
日志相关配置
。
grpc
本节下各参数的详细说明，请参见
grpc 相关配置
。
tls
配置外部 tls。
本节下各参数的详细说明，请参见
tls 相关配置
。
internaltls
配置内部 tls。
有关本节下各参数的详细说明，请参见
internaltls 相关配置
。
common
本节下各参数的详细说明，请参见
常用相关配置
。
quotaAndLimits
配额配置（QuotaConfig），Milvus 配额和限制的配置。
默认情况下，我们启用
TT 保护；
内存保护
磁盘配额保护。
可以启用
DML 吞吐量限制；
DDL 和 DQL qps/rps 限制；
DQL 队列长度/延迟保护；
DQL 结果速率保护；
如有必要，也可以手动强制拒绝 RW 请求。
有关本节下各参数的详细说明，请参见
配额和限制相关配置
。
trace
本节下各参数的详细说明，请参见
与跟踪相关的配置
。
gpu
#当使用 GPU 索引时，Milvus 将利用内存池来避免频繁的内存分配和删除。
#在这里，你可以设置内存池占用内存的大小，单位为 MB。
#注意，当实际内存需求超过 maxMemSize 设置的值时，Milvus 有可能崩溃。
#如果 initMemSize 和 MaxMemSize 都设置为零、
#milvus 将自动初始化 GPU 可用内存的一半、
#maxMemSize则为整个可用 GPU 内存。
本节下每个参数的详细说明，请参见
与 GPU 相关的配置
。
streamingNode
与流节点服务器相关的任何配置。
本节下每个参数的详细说明，请参见
streamingNode-related Configurations
（
流节点相关配置
）。
streaming
与流媒体服务相关的任何配置。
有关本节下各参数的详细说明，请参见
流媒体相关配置
。
knowhere
与 knowhere 向量搜索引擎相关的任何配置
请参阅 "
knowhere 相关配置"
，了解本节下各参数的详细说明。