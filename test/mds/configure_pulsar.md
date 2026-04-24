脉冲星相关配置
pulsar 的相关配置，用于管理 Milvus 最近的突变操作日志，输出流式日志，并提供日志发布-订阅服务。
pulsar.address
说明
默认值
Pulsar 服务的 IP 地址。
环境变量：PULSAR_ADDRESS
pulsar.address 和 pulsar.port 共同生成对 Pulsar 的有效访问。
启动 Milvus 时，Pulsar 优先从环境变量 PULSAR_ADDRESS 获取有效 IP 地址。
默认值适用于 Pulsar 与 Milvus 运行在同一网络时。
本地主机
pulsar.port
说明
默认值
Pulsar 服务的端口。
6650
pulsar.webport
说明
默认值
Pulsar 服务的 Web 端口。如果不使用代理直接连接，应使用 8080。
80
pulsar.maxMessageSize
说明
默认值
Pulsar 中每条信息的最大大小。单位：字节：字节。
默认情况下，Pulsar 在单条信息中最多可传输 2MB 的数据。当插入数据的大小大于此值时，代理会将数据分割成多条信息，以确保能正确传输。
如果 Pulsar 中的相应参数保持不变，增加该配置会导致 Milvus 失败，而减少该配置则不会产生任何优势。
2097152
pulsar.tenant
说明
默认值
可为特定租户配置 Pulsar，并为租户分配适当的容量。
要在多个 Milvus 实例之间共享一个 Pulsar 实例，可以在启动每个 Milvus 实例之前，将其更改为 Pulsar 租户，而不是默认的租户。不过，如果不想使用 Pulsar 多租户，建议将 msgChannel.chanNamePrefix.cluster 更改为不同的值。
公共
pulsar.namespace
描述
默认值
Pulsar 命名空间是租户内的管理单元命名。
默认
pulsar.requestTimeout
描述
默认值
Pulsar 客户端全局请求超时（秒
60
pulsar.enableClientMetrics
描述
默认值
是否将 pulsar 客户端指标注册到 Milvus 指标路径。
假