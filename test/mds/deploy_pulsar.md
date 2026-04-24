使用 Docker Compose 或 Helm 配置消息存储
Milvus 使用 Pulsar 或 Kafka 管理最近更改的日志、输出流日志并提供日志订阅。Pulsar 是默认的消息存储系统。本主题介绍如何使用 Docker Compose 或 Helm 配置消息存储。
您可以使用
Docker Compose
或在 K8s 上配置 Pulsar，并在 K8s 上配置 Kafka。
消息队列限制
：升级到 Milvus v2.6.13 时，必须保持当前的消息队列选择。不支持在升级期间在不同的消息队列系统之间切换。未来版本将支持更改消息队列系统。
使用 Docker Compose 配置 Pulsar
1.配置 Pulsar
要使用 Docker Compose 配置 Pulsar，请在 Milvus/configs 路径下的
milvus.yaml
文件中提供
pulsar
部分的值。
pulsar:
address:
localhost
# Address of pulsar
port:
6650
# Port of pulsar
maxMessageSize:
5242880
# 5 * 1024 * 1024 Bytes, Maximum size of each message in pulsar.
更多信息，请参阅
Pulsar 相关配置
。
2.运行 Milvus
运行以下命令启动使用 Pulsar 配置的 Milvus。
docker
compose up
配置仅在 Milvus 启动后生效。更多信息，请参阅
启动 Milvus
。
使用 Helm 配置 Pulsar
对于 K8s 上的 Milvus 群集，可以在启动 Milvus 的同一命令中配置 Pulsar。或者，你也可以在启动 Milvus 之前，使用
milvus-helm
资源库中 /charts/milvus 路径下的
values.yml
文件配置 Pulsar。
有关如何使用 Helm 配置 Milvus 的详情，请参阅
使用 Helm 图表配置 Milvus
。有关 Pulsar 相关配置项的详情，请参阅
Pulsar 相关配置
。
使用 YAML 文件
在
values.yaml
文件中配置
externalConfigFiles
部分。
extraConfigFiles:
user.yaml:
|+
    pulsar:
      address: localhost # Address of pulsar
      port: 6650 # Port of Pulsar
      webport: 80 # Web port of pulsar, if you connect direcly without proxy, should use 8080
      maxMessageSize: 5242880 # 5 * 1024 * 1024 Bytes, Maximum size of each message in pulsar.
      tenant: public
      namespace: default
配置完前面的部分并保存
values.yaml
文件后，运行以下命令安装使用 Pulsar 配置的 Milvus。
helm install <your_release_name> milvus/milvus -f values.yaml
使用 Helm 配置啄木鸟
对于 K8s 上的 Milvus 集群，可以在启动 Milvus 的同一命令中配置啄木鸟。或者，也可以在启动 Milvus 之前，使用
milvus-helm
资源库中 /charts/milvus 路径下的
values.yml
文件配置 Woodpecker。
有关如何使用 Helm
配置
Milvus 的详情，请参阅
使用 Helm 图表配置 Milvus
。有关 Woodpecker 相关配置项的详情，请参阅
woodpecker 相关配置
。
使用 YAML 文件
在
values.yaml
文件中配置
externalConfigFiles
部分。
extraConfigFiles:
user.yaml:
|+
    woodpecker:
      meta:
        type: etcd # The Type of the metadata provider. currently only support etcd.
        prefix: woodpecker # The Prefix of the metadata provider. default is woodpecker.
      client:
        segmentAppend:
          queueSize: 10000 # The size of the queue for pending messages to be sent of each log.
          maxRetries: 3 # Maximum number of retries for segment append operations.
        segmentRollingPolicy:
          maxSize: 256M # Maximum size of a segment.
          maxInterval: 10m # Maximum interval between two segments, default is 10 minutes.
          maxBlocks: 1000 # Maximum number of blocks in a segment
        auditor:
          maxInterval: 10s # Maximum interval between two auditing operations, default is 10 seconds.
      logstore:
        segmentSyncPolicy:
          maxInterval: 200ms # Maximum interval between two sync operations, default is 200 milliseconds.
          maxIntervalForLocalStorage: 10ms # Maximum interval between two sync operations local storage backend, default is 10 milliseconds.
          maxBytes: 256M # Maximum size of write buffer in bytes.
          maxEntries: 10000 # Maximum entries number of write buffer.
          maxFlushRetries: 5 # Maximum size of write buffer in bytes.
          retryInterval: 1000ms # Maximum interval between two retries. default is 1000 milliseconds.
          maxFlushSize: 2M # Maximum size of a fragment in bytes to flush.
          maxFlushThreads: 32 # Maximum number of threads to flush data
        segmentCompactionPolicy:
          maxSize: 2M # The maximum size of the merged files.
          maxParallelUploads: 4 # The maximum number of parallel upload threads for compaction.
          maxParallelReads: 8 # The maximum number of parallel read threads for compaction.
        segmentReadPolicy:
          maxBatchSize: 16M # Maximum size of a batch in bytes.
          maxFetchThreads: 32 # Maximum number of threads to fetch data.
      storage:
        type: minio # The Type of the storage provider. Valid values: [minio, local]
        rootPath: /var/lib/milvus/woodpecker # The root path of the storage provider.
配置完前面的部分并保存
values.yaml
文件后，运行以下命令安装使用 Woodpecker 配置的 Milvus。
helm install <your_release_name> milvus/milvus -f values.yaml
使用 Helm 配置 Kafka
对于 K8s 上的 Milvus 集群，可以在启动 Milvus 的同一命令中配置 Kafka。或者，你也可以在启动 Milvus 之前，使用
Milvus-helm
资源库中 /charts/milvus 路径下的
values.yml
文件配置 Kafka。
有关如何使用 Helm
配置
Milvus 的详情，请参阅《
使用 Helm 图表配置 Milvus
》。有关 Pulsar 相关配置项的详情，请参阅
Pulsar 相关配置
。
使用 YAML 文件
如果要使用 Kafka 作为消息存储系统，请配置
values.yaml
文件中的
externalConfigFiles
部分。
extraConfigFiles:
user.yaml:
|+
    kafka:
      brokerList:
        -  <your_kafka_address>:<your_kafka_port>
      saslUsername:
      saslPassword:
      saslMechanisms: PLAIN
      securityProtocol: SASL_SSL
配置完前面的部分并保存
values.yaml
文件后，运行以下命令安装使用 Kafka 配置的 Milvus。
helm install <your_release_name> milvus/milvus -f values.yaml
使用 Helm 配置 RocksMQ
Milvus Standalone 使用 RocksMQ 作为默认消息存储。关于如何使用 Helm 配置 Milvus 的详细步骤，请参阅《
使用 Helm 图表配置 Milvus》
。有关 RocksMQ 相关配置项的详情，请参阅
RocksMQ 相关配置
。
如果你用 RocksMQ 启动 Milvus 并想更改其设置，你可以用以下 YAML 文件中更改后的设置运行
helm upgrade -f
。
如果你使用 Helm 独立安装了 Milvus Standalone，并使用了 RocksMQ 以外的消息存储空间，但想把它改回 RocksMQ，可以在刷新所有 Collections 并停止 Milvus 后，使用下面的 YAML 文件运行
helm upgrade -f
。
extraConfigFiles:
user.yaml:
|+
    rocksmq:
      # The path where the message is stored in rocksmq
      # please adjust in embedded Milvus: /tmp/milvus/rdb_data
      path: /var/lib/milvus/rdb_data
      lrucacheratio: 0.06 # rocksdb cache memory ratio
      rocksmqPageSize: 67108864 # 64 MB, 64 * 1024 * 1024 bytes, The size of each page of messages in rocksmq
      retentionTimeInMinutes: 4320 # 3 days, 3 * 24 * 60 minutes, The retention time of the message in rocksmq.
      retentionSizeInMB: 8192 # 8 GB, 8 * 1024 MB, The retention size of the message in rocksmq.
      compactionInterval: 86400 # 1 day, trigger rocksdb compaction every day to remove deleted data
      # compaction compression type, only support use 0,7.
      # 0 means not compress, 7 will use zstd
      # len of types means num of rocksdb level.
      compressionTypes: [0, 0, 7, 7, 7]
不建议更改消息存储。如果你想这样做，请先停止所有 DDL 操作，然后调用 FlushAll API 来刷新所有 Collections，最后在真正更改消息存储之前停止 Milvus。
下一步
了解如何使用 Docker Compose 或 Helm 配置 Milvus 的其他依赖项：
使用 Docker Compose 或 Helm 配置对象存储
使用 Docker Compose 或 Helm 配置元存储