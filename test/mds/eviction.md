驱逐
Compatible with Milvus 2.6.4+
Eviction 管理 Milvus 中每个查询节点的缓存资源。启用后，一旦达到资源阈值，它就会自动删除缓存数据，确保性能稳定，防止内存或磁盘耗尽。
驱逐使用
最近最少使用（LRU）
策略来回收缓存空间。元数据始终处于缓存状态，从不驱逐，因为元数据对查询规划至关重要，而且通常很小。
必须显式启用驱逐。如果没有配置，缓存数据将继续累积，直到资源耗尽。
驱逐类型
Milvus 支持两种互补的驱逐模式
（
sync
和
async
），这两种模式可共同实现最佳资源管理：
方面
同步驱逐
异步驱逐
触发
当内存或磁盘使用量超过内部限制时，在查询或搜索过程中发生。
当使用量超过高水位线或缓存数据达到其生存时间 (TTL) 时，由后台线程触发。
行为
查询节点回收缓存空间时，查询或搜索操作会暂时停止。驱逐将继续进行，直到使用率降到低水位线以下或出现超时。如果超时且无法回收足够的数据，查询或搜索可能会失败。
定期在后台运行，当使用率超过高水位或数据根据 TTL 过期时，主动驱逐缓存数据。驱逐会一直持续，直到使用量降至低水位线以下。不会阻止查询。
最适合
能承受高峰使用期间短暂延迟峰值或暂时停顿的工作负载。当异步驱逐不能足够快地回收空间时非常有用。
需要流畅、可预测查询性能的延迟敏感型工作负载。是主动资源管理的理想选择。
注意事项
如果可驱逐数据不足，可能会导致短暂的查询延迟或超时。
需要适当调整高/低水印和 TTL 设置。后台线程有轻微开销。
配置
通过
evictionEnabled: true
通过
backgroundEvictionEnabled: true
启用（同时需要
evictionEnabled: true
）
建议设置
：
两种驱逐模式可同时启用，以实现最佳平衡，前提是您的工作负载受益于分层存储，并能承受与驱逐相关的获取延迟。
对于性能测试或对延迟要求较高的场景，可考虑完全禁用驱逐，以避免驱逐后的网络获取开销。
对于可驱逐字段和索引，驱逐单元与加载粒度相匹配--标量/向量字段按块驱逐，标量/向量索引按段驱逐。
启用驱逐
在
milvus.yaml
的
queryNode.segcore.tieredStorage
下配置驱逐：
queryNode:
segcore:
tieredStorage:
evictionEnabled:
true
# Enables synchronous eviction
backgroundEvictionEnabled:
true
# Enables background (asynchronous) eviction
参数
类型
值
说明
建议用例
evictionEnabled
二进制
true
/
false
驱逐策略的主开关。默认为
false
。启用同步驱逐模式。
在分层存储中始终设置为
true
。
backgroundEvictionEnabled
bool
true
/
false
在后台异步运行驱逐。需要
evictionEnabled: true
。默认为
false
。
使用
true
可提高查询性能，减少同步驱逐频率。
配置水印
水印定义内存和磁盘的缓存驱逐开始和结束时间。每种资源类型有两个阈值：
高水印
：当使用量超过此值时，开始驱逐。
低水印
：继续驱逐，直到使用率低于此值。
此配置仅在
启用驱逐
时生效。
示例 YAML
：
queryNode:
segcore:
tieredStorage:
# Memory watermarks
memoryLowWatermarkRatio:
0.75
# Eviction stops below 75% memory usage
memoryHighWatermarkRatio:
0.8
# Eviction starts above 80% memory usage
# Disk watermarks
diskLowWatermarkRatio:
0.75
# Eviction stops below 75% disk usage
diskHighWatermarkRatio:
0.8
# Eviction starts above 80% disk usage
参数
类型
范围
说明
推荐用例
memoryLowWatermarkRatio
浮点数
(0.0, 1.0]
停止驱逐的内存使用水平。
从
0.75
开始。如果查询节点内存有限，可略微降低。
memoryHighWatermarkRatio
浮点数
(0.0, 1.0]
异步驱逐开始时的内存使用水平。
从
0.8
开始。与低水位线保持适当差距（例如 0.05-0.10），以防止频繁触发。
diskLowWatermarkRatio
浮动
(0.0, 1.0]
停止驱逐的磁盘使用水平。
从
0.75
开始。如果磁盘 I/O 受限，可将其调低。
diskHighWatermarkRatio
浮动
(0.0, 1.0]
开始异步驱逐的磁盘使用级别。
从
0.8
开始。与低水位线保持合理的差距（如 0.05-0.10），以防止频繁触发。
最佳实践
：
不要将高水印或低水印设置在 ~0.80 以上，以便为 QueryNode 的静态使用和查询时间突发留出余地。
避免在高水印和低水印之间出现大的间隙；大的间隙会延长每个驱逐周期并增加延迟。
配置缓存 TTL
即使未达到资源阈值，
缓存生存时间（TTL）
也会在设定的持续时间后自动删除缓存数据。它与 LRU 驱逐一起防止陈旧数据无限期占用缓存。
缓存 TTL 需要
backgroundEvictionEnabled: true
，因为它在同一个后台线程上运行。
YAML 示例
queryNode:
segcore:
tieredStorage:
evictionEnabled:
true
backgroundEvictionEnabled:
true
# Set the cache expiration time to 604,800 seconds (7 days),
# and expired caches will be cleaned up by a background thread.
cacheTtl:
604800
参数
类型
单位
说明
推荐用例
cacheTtl
整数
秒
缓存数据过期前的持续时间。过期项目会在后台删除。
对于高度动态的数据，使用较短的 TTL（小时）；对于稳定的数据集，使用较长的 TTL（天）。设置 0 则禁用基于时间的过期。