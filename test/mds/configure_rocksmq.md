rocksmq相关配置
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
rocksmq.path
说明
默认值
Milvus 在 RocksMQ 中存储数据的密钥前缀。
注意：在使用 Milvus 一段时间后更改此参数将影响您对旧数据的访问。
建议在首次启动 Milvus 前更改此参数。
如果已经存在 etcd 服务，为 Milvus 设置一个易于识别的根密钥前缀。
/var/lib/milvus/rdb_data
rocksmq.lrucacheratio
说明
默认值
rocksdb 缓存内存比率
0.06
rocksmq.rocksmqPageSize
说明
默认值
RocksMQ 中每页信息的最大容量。RocksMQ 中的消息会根据该参数进行批量检查和清除（过期时）。单位：字节：字节。
67108864
rocksmq.retentionTimeInMinutes
说明
默认值
RocksMQ 中已接收消息的最长保留时间。RocksMQ 中的已确认消息会保留指定的时间，然后被清除。单位：分钟：分钟。
4320
rocksmq.retentionSizeInMB
说明
默认值
RocksMQ 中各主题已接收消息的最大保留大小。如果每个主题中已接收消息的大小超过此参数，则会被清除。单位：MB：MB。
8192
rocksmq.compactionInterval
说明
默认值
触发 rocksdb 压缩以删除已删除数据的时间间隔。单位：秒秒
86400
rocksmq.compressionTypes
说明
默认值
压缩类型，只支持使用 0、7。0 表示不压缩，7 表示使用 zstd。类型的长度表示 rocksdb 级别的数量。
0,0,7,7,7