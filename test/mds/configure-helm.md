使用 Helm Charts 配置 Milvus
本主题介绍如何使用 Helm Charts 配置 Milvus 组件及其第三方依赖项。
在当前版本中，所有参数仅在 Milvus 重新启动后生效。
通过配置文件配置 Milvus
您可以通过配置文件
values.yaml
配置 Milvus。
下载配置文件
直接或使用以下命令
下载
values.yaml
。
$
wget
https:
/
/raw.githubusercontent.com/milvus
-io/milvus-helm/master/charts/milvus/values.yaml
修改配置文件
通过调整
values.yaml
中的相应参数，配置 Milvus 实例，以适应您的应用场景。
具体来说，在
values.yaml
中搜索
extraConfigFiles
，然后将配置文件放入该部分，如下所示：
# Extra configs for milvus.yaml
# If set, this config will merge into milvus.yaml
# Please follow the config structure in the milvus.yaml
# at https://github.com/milvus-io/milvus/blob/master/configs/milvus.yaml
#
Note:
this config will be the top priority which will override the config
# in the image and helm chart.
extraConfigFiles:
user.yaml:
|+
    #    For example to set the graceful time for query nodes
    #    queryNodes:
    #      gracefulTime: 10
查看以下链接，了解有关各参数的更多信息。
排序方式
组件或依赖项
配置目的
依赖项
组件
etcd
MinIO 或 S3
脉冲星
RocksMQ
Root coord
代理
Query coord
查询节点
索引节点
数据坐标
数据节点
本地存储
日志
信息通道
通用
图形处理器
GRPC
索引坐标
元存储
消息队列
Tikv
跟踪
配额和限制
用途
参数
性能调整
queryNode.gracefulTime
rootCoord.minSegmentSizeToEnableIndex
dataCoord.segment.maxSize
dataCoord.segment.sealProportion
dataNode.flush.insertBufSize
queryCoord.autoHandoff
queryCoord.autoBalance
localStorage.enabled
数据和元
common.retentionDuration
rocksmq.retentionTimeInMinutes
dataCoord.enableCompaction
dataCoord.enableGarbageCollection
dataCoord.gc.dropTolerance
管理
log.level
log.file.rootPath
log.file.maxAge
minio.accessKeyID
minio.secretAccessKey
配额和限制
quotaAndLimits.ddl.enabled
quotaAndLimits.ddl.collectionRate
quotaAndLimits.ddl.partitionRate
quotaAndLimits.indexRate.enabled
quotaAndLimits.indexRate.max
quotaAndLimits.flushRate.enabled
quotaAndLimits.flush.max
quotaAndLimits.compation.enabled
quotaAndLimits.compaction.max
quotaAndLimits.dml.enabled
quotaAndLimits.dml.insertRate.max
quotaAndLimits.dml.deleteRate.max
quotaAndLimits.dql.enabled
quotaAndLimits.dql.searchRate.max
quotaAndLimits.dql.queryRate.max
quotaAndLimits.limitWriting.ttProtection.enabled
quotaAndLimits.limitWriting.ttProtection.maxTimeTickDelay
quotaAndLimits.limitWriting.memProtection.enabled
quotaAndLimits.limitWriting.memProtection.dataNodeMemoryLowWaterLevel
quotaAndLimits.limitWriting.memProtection.queryNodeMemoryLowWaterLevel
quotaAndLimits.limitWriting.memProtection.dataNodeMemoryHighWaterLevel
quotaAndLimits.limitWriting.memProtection.queryNodeMemoryHighWaterLevel
quotaAndLimits.limitWriting.diskProtection.enabled
quotaAndLimits.limitWriting.diskProtection.diskQuota
quotaAndLimits.limitWriting.forceDeny
quotaAndLimits.limitReading.queueProtection.enabled
quotaAndLimits.limitReading.queueProtection.nqInQueueThreshold
quotaAndLimits.limitReading.queueProtection.queueLatencyThreshold
quotaAndLimits.limitReading.resultProtection.enabled
quotaAndLimits.limitReading.resultProtection.maxReadResultRate
quotaAndLimits.limitReading.forceDeny
有关专门针对 Kubernetes 安装的其他参数，请参阅
Milvus Helm 图表配置
。
启动 Milvus
完成修改配置文件后，就可以用该文件启动 Milvus。
$
helm upgrade my-release milvus/milvus -f values.yaml
通过命令行配置 Milvus
或者，你也可以直接使用 Helm 命令升级 Milvus 配置。
检查可配置参数
升级前，可以使用 Helm 图表检查可配置参数。
$
helm show values milvus/milvus
启动 Milvus
在升级命令中添加
--values
或
--set
，配置并启动 Milvus。
#
For instance, upgrade the Milvus cluster with compaction disabled
$
helm upgrade my-release milvus/milvus --
set
dataCoord.enableCompaction=
false
下一步
如果你想了解如何监控 Milvus 服务并创建警报：
学习
在 Kubernetes 上使用 Prometheus 操作符监控 Milvus
学习
在 Grafana 中可视化 Milvus 指标
。
如果您正在寻找如何分配资源的说明：
在 Kubernetes 上分配资源