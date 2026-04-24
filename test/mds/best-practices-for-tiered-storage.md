分层存储的最佳实践
Compatible with Milvus 2.6.4+
Milvus 提供分层存储，帮助您有效处理大规模数据，同时平衡查询延迟、容量和资源使用。本指南总结了典型工作负载的推荐配置，并解释了每种调整策略背后的原因。
开始之前
Milvus v2.6.4 或更高版本
查询节点必须有专用的本地资源（内存和磁盘）。共享环境可能会扭曲缓存估算并导致驱逐判断错误。
选择正确的策略
分层存储提供灵活的加载和缓存策略，可根据工作负载进行组合。
目标
建议重点
关键机制
最大限度地减少首次查询延迟
预加载关键字段
预热
高效处理大规模数据
按需加载
懒加载 + 部分加载
保持长期稳定性
防止缓存溢出
驱逐
平衡性能和容量
结合预加载和动态缓存
混合配置
方案 1：实时、低延迟检索
何时使用
查询延迟至关重要（例如，实时推荐或搜索排名）
频繁访问核心向量索引和标量过滤器
稳定的性能比启动速度更重要
推荐配置
# milvus.yaml
queryNode:
segcore:
tieredStorage:
warmup:
# scalar field/index warm-up to eliminate first-time latency
scalarField:
sync
scalarIndex:
sync
# warm-up of vector fields is disabled (if the original vector is not required)
vectorField:
disable
# vector indexes warm-up to elminate first-time latenct
vectorIndex:
sync
# enable cache eviction, and also turn on background asynchronous eviction
# to reduce the triggering of synchronous eviction.
evictionEnabled:
true
backgroundEvictionEnabled:
true
memoryLowWatermarkRatio:
0.75
memoryHighWatermarkRatio:
0.8
diskLowWatermarkRatio:
0.75
diskHighWatermarkRatio:
0.8
# no expiration time, which avoids frequent reloading
cacheTtl:
0
理由
预热可消除高频标量和向量索引的首次访问延迟。
后台驱逐可在不阻塞查询的情况下保持稳定的缓存压力。
禁用缓存 TTL 可避免对热数据进行不必要的重新加载。
场景 2：离线批量分析
何时使用
查询延迟容忍度高
工作负载涉及海量数据集或许多数据段
容量和吞吐量优先于响应速度
建议配置
# milvus.yaml
queryNode:
segcore:
tieredStorage:
enabled:
true
warmup:
# disable scalar field/index warm-up to speed up loading
scalarField:
disable
scalarIndex:
disable
# disable vector field/index warm-up to speed up loading
vectorField:
disable
vectorIndex:
disable
# enable cache eviction, and also turn on background asynchronous eviction
# to reduce the triggering of synchronous eviction.
evictionEnabled:
true
backgroundEvictionEnabled:
true
memoryLowWatermarkRatio:
0.7
memoryHighWatermarkRatio:
0.85
diskLowWatermarkRatio:
0.7
diskHighWatermarkRatio:
0.85
# use 1 day expiration to clean unused cache
cacheTtl:
86400
理由
在初始化许多分段时，禁用预热可加快启动速度。
更高的水印允许更密集地使用缓存，从而提高总负载能力。
缓存 TTL 会自动清除未使用的数据，以释放本地空间。
方案 3：混合部署（混合在线 + 离线）
何时使用
单个集群同时为在线和分析工作负载提供服务
某些集合要求低延迟，其他集合优先考虑容量
建议策略
将
实时配置
应用于对延迟敏感的集合
将
离线配置
应用于分析或存档收集
针对每种工作负载类型独立调整 evictableMemoryCacheRatio、cacheTtl 和水印比率
理由
结合配置可对资源分配进行细粒度控制。
关键收集可保持低延迟保证，而辅助收集则可处理更多的数据段和数据量。
其他调整技巧
方面
建议
说明
预热范围
只预载查询频率高的字段或索引。
不必要的预加载会增加加载时间和资源使用。
驱逐调整
从默认水印（75-80%）开始，逐步调整。
间隙过小会导致频繁驱逐；间隙过大则会延迟资源释放。
缓存 TTL
对稳定的热数据集禁用；对动态数据启用（如 1-3 天）。
防止陈旧缓存堆积，同时平衡清理开销。
超量提交比率
除非资源余量很大，否则避免使用 > 0.7 的值。
过多的超量提交可能会导致缓存中断和不稳定的延迟。
监控
跟踪缓存命中率、资源利用率和驱逐频率。
频繁的冷负载可能表明需要调整预热或水印。