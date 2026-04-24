动态配置 Milvus
Milvus 允许你动态更改一些配置。
开始之前
您需要确保
已安装 Birdwatcher。详情请参阅
安装 Birdwatcher
、
安装了 etcdctl。有关详情，请参阅
与 etcd 交互
，或
安装了其他 etcd 客户端，例如 Python 客户端。
本指南中的示例将
proxy.minPasswordLength
的值更改为
8
。您可以使用 "
适用的配置项
"中列出的适用密钥替换这些密钥。
本指南中的示例假定 Milvus 的根路径是
by-dev
。所有配置都列在
by-dev/config
路径下。Milvus 根路径因安装方式而异。对于使用 Helm 图表安装的实例，根路径默认为
by-dev
。如果不知道根路径，请参阅
连接到 etcd
。
更改配置
在 Milvus 上，
proxy.minPasswordLength
默认设置为
6
。要更改此值，可按以下步骤操作：
$
etcdctl put by-dev/config/proxy/minPasswordLength 8
#
or
$
birdwatcher -olc
"#connect --etcd 127.0.0.1:2379 --rootPath=by-dev,set config-etcd --key by-dev/config/proxy/minPasswordLength --value 8"
然后按如下步骤检查配置：
$
etcdctl get by-dev/config/proxy/minPasswordLength
回滚配置
如果更改的值不再适用，Milvus 还允许您回滚配置。
$
etcdctl del by-dev/config/proxy/minPasswordLength
#
or
$
birdwatcher -olc
"#connect --etcd 127.0.0.1:2379 --rootPath=by-dev,remove config-etcd --key by-dev/config/proxy/minPasswordLength"
然后可以按如下方式检查配置：
$
etcdctl get by-dev/config/proxy/minPasswordLength
查看配置
除了查看特定配置项的值，您还可以列出所有配置项。
$
etcdctl get --prefix by-dev/config
#
or
$
birdwatcher -olc
"#connect --etcd 127.0.0.1:2379 --rootPath=by-dev,show config-etcd"
查看特定节点的配置：
Offline > connect --etcd ip:port 
Milvus(by-dev) > show session          # List all nodes with their server ID
Milvus(by-dev) > visit querycoord 1    # Visit a node by server ID
QueryCoord-1(ip:port) > configuration  # List the configuration of the node
适用的配置项
目前，您可以动态更改以下配置项目。
配置项目
默认值
pulsar.maxMessageSize
5242880
common.retentionDuration
86400
common.entityExpiration
-1
common.gracefulTime
5000
common.gracefulStopTimeout
30
quotaAndLimits.ddl.enabled
假
quotaAndLimits.indexRate.enabled
启用
quotaAndLimits.flushRate.enabled
启用
quotaAndLimits.compactionRate.enabled
启用
quotaAndLimits.dml.enabled
启用
quotaAndLimits.dql.enabled
启用
quotaAndLimits.limits.Collections.maxNum
64
quotaAndLimits.limitWriting.forceDeny
无
quotaAndLimits.limitWriting.ttProtection.enabled
启用
quotaAndLimits.limitWriting.ttProtection.maxTimeTickDelay
9223372036854775807
quotaAndLimits.limitWriting.memProtection.enabled
启用
quotaAndLimits.limitWriting.memProtection.dataNodeMemoryLowWaterLevel
0.85
quotaAndLimits.limitWriting.memProtection.dataNodeMemoryHighWaterLevel
0.95
配额和限制.limitWriting.memProtection.queryNodeMemoryLowWaterLevel（查询节点内存低水位
0.85
配额和限制.limitWriting.memProtection.queryNodeMemoryHighWaterLevel（查询节点内存高水位
0.95
quotaAndLimits.limitWriting.diskProtection.enabled
启用
quotaAndLimits.limitWriting.diskProtection.diskQuota
+INF
quotaAndLimits.limitReading.forceDeny
假
quotaAndLimits.limitReading.queueProtection.enabled
启用
quotaAndLimits.limitReading.queueProtection.nqInQueueThreshold
9223372036854775807
quotaAndLimits.limitReading.queueProtection.queueLatencyThreshold
+INF
quotaAndLimits.limitReading.resultProtection.enabled
FALSE
quotaAndLimits.limitReading.resultProtection.maxReadResultRate
+INF
quotaAndLimits.limitReading.coolOffSpeed
0.9
自动索引启用
假
autoIndex.params.build
""
autoIndex.params.extra
""
autoIndex.params.search
""
proxy.maxNameLength
255
proxy.maxUsernameLength
32
proxy.minPasswordLength
6
proxy.maxPasswordLength
256
proxy.maxFieldNum
64
proxy.maxShardNum
256
代理最大维度
32768
代理的最大用户数
100
代理的最大角色数
10
查询节点启用磁盘
TRUE
dataCoord.segment.diskSegmentMaxSize
2048
dataCoord.compaction.enableAutoCompaction
TRUE
下一步
了解有关
系统配置的
更多信息。
了解如何使用
Milvus Operator
、
Helm 图表
和
Docker
配置已安装的
Milvus
。