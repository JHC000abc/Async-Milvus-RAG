常用相关配置
common.defaultPartitionName
说明
默认值
创建 Collections 时的默认分区名称
默认
common.defaultIndexName
默认值
默认值
创建未指定名称的索引时的索引名称
_default_idx
common.entityExpiration
说明
默认值
实体过期时间，以秒为单位，注意 -1 表示永不过期
-1
common.indexSliceSize
说明
默认值
索引片大小（MB
16
common.threadCoreCoefficient.highPriority
说明
默认值
该参数指定线程数是高优先级池中内核数的多少倍
10
common.threadCoreCoefficient.middlePriority
说明
默认值
该参数指定线程数是中优先级池核心数的多少倍
5
common.threadCoreCoefficient.lowPriority
说明
默认值
该参数用于指定线程数是低优先级池核心数的多少倍
1
common.gracefulTime
说明
默认值
毫秒，表示在有界一致性情况下需要减去请求到达时间的间隔（毫秒）。
5000
common.gracefulStopTimeout
描述
默认值
秒，如果在这段时间内未完成优雅停止过程，它将强制退出服务器。
1800
common.storageType
说明
默认值
请在嵌入式 Milvus 中调整：本地，可用值为 [本地、远程、opendal]，minio 值已过时，请使用 remote 代替。
远程
common.simdType
说明
默认值
默认值：自动
有效值：[自动、AVX512、AVX2、AVX、SSE4_2］
该配置仅用于 querynode 和 indexnode，它为搜索和建立索引选择 CPU 指令集。
自动
common.security.superUsers
说明
默认值
超级用户将忽略某些系统检查进程、
如更新证书时的旧密码验证。
common.security.defaultRootPassword
说明
默认值
根用户的默认密码。最大长度为 72 个字符，需要双引号。
Milvus
common.security.rootShouldBindRole
说明
默认值
启用授权时，根用户是否应绑定角色。
假
common.security.rbac.overrideBuiltInPrivilegeGroups.enabled
说明
默认值
是否覆盖内置特权组
假
common.security.rbac.cluster.readonly.privileges
说明
默认值
群集级只读权限
ListDatabases,SelectOwnership,SelectUser,DescribeResourceGroup,ListResourceGroups,ListPrivilegeGroups
common.security.rbac.cluster.readwrite.privileges
说明
默认值
群集级读写权限
ListDatabases,SelectOwnership,SelectUser,DescribeResourceGroup,ListResourceGroups,ListPrivilegeGroups,FlushAll,TransferNode,TransferReplica,UpdateResourceGroups
common.security.rbac.cluster.admin.privileges
说明
默认值
群集级管理员权限
ListDatabases,SelectOwnership,SelectUser,DescribeResourceGroup,ListResourceGroups,ListPrivilegeGroups,FlushAll,TransferNode,TransferReplica,UpdateResourceGroups,BackupRBAC,RestoreRBAC,CreateDatabase、DropDatabase,CreateOwnership,DropOwnership,ManageOwnership,CreateResourceGroup,DropResourceGroup,UpdateUser,RenameCollection,CreatePrivilegeGroup,DropPrivilegeGroup,OperatePrivilegeGroup
common.security.rbac.database.readonly.privileges
说明
默认值
数据库级只读权限
显示集合,描述数据库
common.security.rbac.database.readwrite.privileges
说明
默认值
数据库级读写权限
显示收藏、描述数据库、更改数据库
common.security.rbac.database.admin.privileges
说明
默认值
数据库级管理员权限
显示收藏集,描述数据库,更改数据库,创建收藏集,删除收藏集
common.security.rbac.collection.readonly.privileges
说明
默认值
Collections 级别的只读权限
查询,搜索,索引详情,获取冲洗状态,获取加载状态,获取加载进度,已分区,显示分区,描述集合,描述别名,获取统计数据,列出别名
common.security.rbac.collection.readwrite.privileges
描述
默认值
集合级读写权限
Query,Search,IndexDetail,GetFlushState,GetLoadState,GetLoadingProgress,HasPartition,ShowPartitions,DescribeCollection,DescribeAlias,GetStatistics,ListAliases,Load,Release,Insert,Delete,Upsert,Import,Flush,Compaction,LoadBalance,CreateIndex,DropIndex,CreatePartition,DropPartition
common.security.rbac.collection.admin.privileges
说明
默认值
Collection 级别管理员权限
Query,Search,IndexDetail,GetFlushState,GetLoadState,GetLoadingProgress,HasPartition,ShowPartitions,DescribeCollection,DescribeAlias,GetStatistics,ListAliases,Load,Release,Insert,Delete,Upsert,Import,Flush,Compaction,LoadBalance,CreateIndex,DropIndex,CreatePartition,DropPartition,CreateAlias,DropAlias
common.session.ttl
说明
默认值
会话授予注册服务租期时的 ttl 值
30
common.session.retryTimes
会话授予注册服务租约时的 ttl 值
默认值
会话发送 etcd 请求时的重试次数
30
common.locks.metrics.enable
描述
默认值
是否为度量锁收集统计数据
假
common.locks.threshold.info
说明
默认值
信息级打印持续时间的最小毫秒数
500
common.locks.threshold.warn
说明
默认值
警告级别中打印持续时间的最小毫秒数
1000
common.locks.maxWLockConditionalWaitTime
说明
默认值
等待锁定条件的最长秒数
600
common.ttMsgEnabled
说明
默认值
是否禁用系统内部时间消息机制。
如果禁用（设置为 false），系统将不允许进行 DML 操作，包括插入、删除、查询和搜索。
这有助于 Milvus-CDC 同步增量数据
真
common.traceLogMode
说明
默认值
跟踪请求信息
0
common.bloomFilterSize
描述
默认值
bloom 过滤器初始大小
100000
common.bloomFilterType
说明
默认值
bloom 过滤器类型，支持 BasicBloomFilter 和 BlockedBloomFilter
阻塞式 BloomFilter
common.maxBloomFalsePositive
描述
默认值
Bloom 过滤器的最大误报率
0.001
common.bloomFilterApplyBatchSize
说明
默认值
将 pk 应用于 Bloom 过滤器时的批量大小
1000
common.collectionReplicateEnable
说明
默认值
是否启用 Collections 复制。
假
common.usePartitionKeyAsClusteringKey
说明
默认值
如果为 true，则在 Partition Key 字段上进行聚类压缩和分段剪枝
假
common.useVectorAsClusteringKey
说明
默认值
如果为 true，则对向量字段进行聚类压缩和分段剪裁
假
common.enableVectorClusteringKey
描述
默认值
如果为 true，则启用向量聚类键和向量聚类压缩
假
common.localRPCEnabled
描述
默认值
在混合或独立模式下，启用本地 rpc 进行内部通信。
假
common.sync.taskPoolReleaseTimeoutSeconds
说明
默认值
等待任务完成并释放池中资源的最长时间
60
common.clusterID
说明
默认值
集群的唯一标识符，用于生成自动标识符，以确保多个 Milvus 集群的全局唯一性。
有效值：[0、1、2、3、4、5、6、7] （最多支持 8 个集群）
每个群集必须有一个唯一的 clusterID，以防止运行多个群集时出现 AutoID 重叠。
此 ID 作为 cluster_id 段的一部分嵌入 64 位 AutoID 结构中。
有关详细信息，请参阅
主字段和 AutoID
。
0