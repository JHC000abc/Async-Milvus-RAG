msgChannel 相关配置
本主题介绍 Milvus 的消息通道相关配置。
msgChannel.chanNamePrefix.cluster
说明
默认值
创建消息通道时通道的根名称前缀。
建议在首次启动 Milvus 前更改此参数。
若要在多个 Milvus 实例中共享一个 Pulsar 实例，可考虑在启动每个 Milvus 实例前将其更改为一个名称，而不是默认名称。
by-dev
msgChannel.chanNamePrefix.rootCoordTimeTick
说明
默认值
Root coord 发布时间刻度信息的信息通道的子名称前缀。
完整的频道名称前缀是 ${msgChannel.chanNamePrefix.cluster}-${msgChannel.chanNamePrefix.rootCoordTimeTick} 。
注意：在使用 Milvus 一段时间后更改此参数将影响您对旧数据的访问。
建议在首次启动 Milvus 之前更改此参数。
根节点时间
msgChannel.chanNamePrefix.rootCoordStatistics
说明
默认值
Root coord 发布自己统计信息的信息通道的子名称前缀。
完整的频道名称前缀为 ${msgChannel.chanNamePrefix.cluster}-${msgChannel.chanNamePrefix.rootCoordStatistics} 。
注意：在使用 Milvus 一段时间后更改此参数将影响您对旧数据的访问。
建议在首次启动 Milvus 之前更改此参数。
根节点统计
msgChannel.chanNamePrefix.rootCoordDml
说明
默认值
Root coord 发布 Data Manipulation Language（DML）信息的信息通道的子名称前缀。
完整的通道名称前缀为 ${msgChannel.chanNamePrefix.cluster}-${msgChannel.chanNamePrefix.rootCoordDml} 。
注意：在使用 Milvus 一段时间后更改此参数将影响您对旧数据的访问。
建议在首次启动 Milvus 之前更改此参数。
根节点数据表
msgChannel.chanNamePrefix.queryTimeTick
说明
默认值
查询节点发布时间刻度信息的信息通道的子名称前缀。
完整的通道名称前缀为 ${msgChannel.chanNamePrefix.cluster}-${msgChannel.chanNamePrefix.queryTimeTick} 。
注意：在使用 Milvus 一段时间后更改此参数将影响您对旧数据的访问。
建议在首次启动 Milvus 之前更改此参数。
查询时间
msgChannel.chanNamePrefix.dataCoordTimeTick
说明
默认值
Data coord 发布时间刻度信息的信息通道的子名称前缀。
完整的通道名称前缀为 ${msgChannel.chanNamePrefix.cluster}-${msgChannel.chanNamePrefix.dataCoordTimeTick} 。
注意：在使用 Milvus 一段时间后更改此参数将影响您对旧数据的访问。
建议在首次启动 Milvus 之前更改此参数。
数据记录-时间-通道
msgChannel.chanNamePrefix.dataCoordSegmentInfo
说明
默认值
Data coord 发布分段信息的信息通道的子名称前缀。
完整的信道名称前缀为 ${msgChannel.chanNamePrefix.cluster}-${msgChannel.chanNamePrefix.dataCoordSegmentInfo} 。
注意：在使用 Milvus 一段时间后更改此参数将影响您对旧数据的访问。
建议在首次启动 Milvus 之前更改此参数。
段落信息通道
msgChannel.subNamePrefix.dataCoordSubNamePrefix
说明
默认值
数据 coord 的订阅名称前缀。
注意：在使用 Milvus 一段时间后更改此参数将影响您对旧数据的访问。
建议在首次启动 Milvus 之前更改此参数。
数据坐标
msgChannel.subNamePrefix.dataNodeSubNamePrefix
说明
默认值
数据节点的订阅名称前缀。
注意：在使用 Milvus 一段时间后更改此参数将影响您对旧数据的访问。
建议在首次启动 Milvus 前更改此参数。
数据节点