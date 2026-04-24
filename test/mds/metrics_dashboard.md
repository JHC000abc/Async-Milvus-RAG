Milvus 指标控制面板
Milvus 会在运行期间输出详细的时间序列指标列表。您可以使用
Prometheus
和
Grafana
将指标可视化。本主题介绍 Grafana Milvus 仪表板中显示的监控指标。
本主题中的时间单位是毫秒。本主题中的 "第 99 百分位数 "指的是 99% 的时间统计数据控制在某一数值范围内。
建议先阅读
Milvus 监控框架概述
，了解 Prometheus 指标。
代理
面板
面板描述
PromQL （Prometheus 查询语言）
使用的 Milvus 指标
Milvus 指标说明
搜索向量计数率
过去两分钟内每个代理平均每秒查询的向量数。
sum(increase(milvus_proxy_search_vectors_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])/120) by (pod, node_id)
milvus_proxy_search_vectors_count
累计查询的向量数。
插入向量计数率
每个代理在过去两分钟内平均每秒插入的向量数。
sum(increase(milvus_proxy_insert_vectors_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])/120) by (pod, node_id)
milvus_proxy_insert_vectors_count
插入向量的累计数量。
搜索延迟
每个代理在过去两分钟内接收搜索和查询请求的平均延迟和第 99 百分位数。
P99:
histogram_quantile(0.99, sum by (le, query_type, pod, node_id) (rate(milvus_proxy_sq_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_proxy_sq_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (pod, node_id, query_type) / sum(increase(milvus_proxy_sq_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (pod, node_id, query_type)
milvus_proxy_sq_latency
搜索和查询请求的延迟。
Collections 搜索延迟
每个代理在过去两分钟内接收对特定 Collections 的搜索和查询请求的平均延迟时间和第 99 百分位数。
P99:
histogram_quantile(0.99, sum by (le, query_type, pod, node_id) (rate(milvus_proxy_collection_sq_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace", collection_name=~"$collection"}[2m])))
AVG:
sum(increase(milvus_proxy_collection_sq_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace", collection_name=~"$collection"}[2m])) by (pod, node_id, query_type) / sum(increase(milvus_proxy_collection_sq_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace", collection_name=~"$collection"}[2m])) by (pod, node_id, query_type)
milvus_proxy_collection_sq_latency_sum
对特定 Collections 的搜索和查询请求的延迟时间
突变延迟
每个代理在过去两分钟内接收突变请求的平均延迟时间和延迟时间的第 99 百分位数。
p99:
histogram_quantile(0.99, sum by (le, msg_type, pod, node_id) (rate(milvus_proxy_mutation_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
avg:
sum(increase(milvus_proxy_mutation_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (pod, node_id, msg_type) / sum(increase(milvus_proxy_mutation_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (pod, node_id, msg_type)
milvus_proxy_mutation_latency_sum
突变请求的延迟。
Collections 突变延迟
每个代理在过去两分钟内接收特定 Collections 变异请求的平均延迟和第 99 百分位数。
P99:
histogram_quantile(0.99, sum by (le, query_type, pod, node_id) (rate(milvus_proxy_collection_sq_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace", collection_name=~"$collection"}[2m])))
AVG:
sum(increase(milvus_proxy_collection_sq_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace", collection_name=~"$collection"}[2m])) by (pod, node_id, query_type) / sum(increase(milvus_proxy_collection_sq_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace", collection_name=~"$collection"}[2m])) by (pod, node_id, query_type)
milvus_proxy_collection_sq_latency_sum
向特定 Collections 发送突变请求的延迟时间
等待搜索结果延迟
代理在过去两分钟内发送搜索和查询请求以及接收结果之间的平均延迟和第 99 百分位数。
p99:
histogram_quantile(0.99, sum by (le, query_type, pod, node_id) (rate(milvus_proxy_sq_wait_result_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
avg:
sum(increase(milvus_proxy_sq_wait_result_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (pod, node_id, query_type) / sum(increase(milvus_proxy_sq_wait_result_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (pod, node_id, query_type)
milvus_proxy_sq_wait_result_latency
发送搜索和查询请求与接收结果之间的延迟。
减少搜索结果延迟
过去两分钟内通过代理聚合搜索和查询结果的平均延迟和第 99 百分位数延迟。
P99:
histogram_quantile(0.99, sum by (le, query_type, pod, node_id) (rate(milvus_proxy_sq_reduce_result_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_proxy_sq_reduce_result_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (pod, node_id, query_type) / sum(increase(milvus_proxy_sq_reduce_result_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (pod, node_id, query_type)
milvus_proxy_sq_reduce_result_latency
汇总每个查询节点返回的搜索和查询结果的延迟。
解码搜索结果延迟
过去两分钟内通过代理解码搜索和查询结果的平均延迟和第 99 百分位数延迟。
P99:
histogram_quantile(0.99, sum by (le, query_type, pod, node_id) (rate(milvus_proxy_sq_decode_result_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_proxy_sq_decode_result_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (pod, node_id, query_type) / sum(increase(milvus_proxy_sq_decode_resultlatency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (pod, node_id, query_type)
milvus_proxy_sq_decode_result_latency
解码每个搜索和查询结果的延迟。
信息流对象数
过去两分钟内，每个代理在相应物理主题上创建的 msgstream 对象的平均、最大和最小数量。
avg(milvus_proxy_msgstream_obj_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id) max(milvus_proxy_msgstream_obj_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id) min(milvus_proxy_msgstream_obj_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id)
milvus_proxy_msgstream_obj_num
在每个物理主题上创建的 msgstream 对象数量。
突变发送延迟
每个代理在过去两分钟内发送插入或删除请求的平均延迟和第 99 百分位数。
P99:
histogram_quantile(0.99, sum by (le, msg_type, pod, node_id) (rate(milvus_proxy_mutation_send_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_proxy_mutation_send_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (pod, node_id, msg_type) / sum(increase(milvus_proxy_mutation_send_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (pod, node_id, msg_type)
milvus_proxy_mutation_send_latency
发送插入或删除请求的延迟。
缓存命中率
过去两分钟内每秒操作（包括
GeCollectionID
、
GetCollectionInfo
和
GetCollectionSchema
）的平均缓存命中率。
sum(increase(milvus_proxy_cache_hit_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace", cache_state="hit"}[2m])/120) by(cache_name, pod, node_id) / sum(increase(milvus_proxy_cache_hit_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])/120) by(cache_name, pod, node_id)
milvus_proxy_cache_hit_count
每个缓存读取操作的命中率和失败率统计。
缓存更新延迟
过去两分钟内各代理的平均延迟和第 99 百分位数缓存更新延迟。
P99:
histogram_quantile(0.99, sum by (le, pod, node_id) (rate(milvus_proxy_cache_update_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_proxy_cache_update_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (pod, node_id) / sum(increase(milvus_proxy_cache_update_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (pod, node_id)
milvus_proxy_cache_update_latency
每次更新缓存的延迟。
同步时间
每个代理在其相应物理通道中同步的平均、最大和最小历时。
avg(milvus_proxy_sync_epoch_time{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id) max(milvus_proxy_sync_epoch_time{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id) min(milvus_proxy_sync_epoch_time{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id)
milvus_proxy_sync_epoch_time
每个物理通道的纪元时间（Unix 时间，自 1970 年 1 月 1 日起经过的毫秒数）。
除了物理通道外，还有一个默认的
ChannelName
。
应用 PK 延迟
每个代理在过去两分钟内主键应用延迟的平均值和第 99 百分位数。
p99:
histogram_quantile(0.99, sum by (le, pod, node_id) (rate(milvus_proxy_apply_pk_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
avg:
sum(increase(milvus_proxy_apply_pk_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (pod, node_id) / sum(increase(milvus_proxy_apply_pk_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (pod, node_id)
milvus_proxy_apply_pk_latency
应用主键的延迟。
应用时间戳延迟
过去两分钟内每个代理应用时间戳延迟的平均延迟和第 99 百分位数。
p99:
histogram_quantile(0.99, sum by (le, pod, node_id) (rate(milvus_proxy_apply_timestamp_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
avg:
sum(increase(milvus_proxy_apply_timestamp_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (pod, node_id) / sum(increase(milvus_proxy_apply_timestamp_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (pod, node_id)
milvus_proxy_apply_timestamp_latency
应用时间戳的延迟。
请求成功率
每个代理每秒收到的成功请求数，包括每种请求类型的详细分类。可能的请求类型包括 DescribeCollection、DescribeIndex、GetCollectionStatistics、HasCollection、Search、Query、ShowPartitions、Insert 等。
sum(increase(milvus_proxy_req_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace", status="success"}[2m])/120) by(function_name, pod, node_id)
milvus_proxy_req_count
所有类型接收请求的数量
请求失败率
每个代理每秒收到的失败请求数，包括每种请求类型的详细分类。可能的请求类型包括 DescribeCollection、DescribeIndex、GetCollectionStatistics、HasCollection、Search、Query、ShowPartitions、Insert 等。
sum(increase(milvus_proxy_req_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace", status="fail"}[2m])/120) by(function_name, pod, node_id)
milvus_proxy_req_count
所有类型接收请求的数量
请求延迟
每个代理接收所有类型请求的平均延迟时间和延迟时间的第 99 百分位数
p99:
histogram_quantile(0.99, sum by (le, pod, node_id, function_name) (rate(milvus_proxy_req_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
avg:
sum(increase(milvus_proxy_req_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (pod, node_id, function_name) / sum(increase(milvus_proxy_req_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (pod, node_id, function_name)
milvus_proxy_req_latency
所有类型接收请求的延迟
插入/删除请求字节率
代理在过去两分钟内每秒收到的插入和删除请求的字节数。
sum(increase(milvus_proxy_receive_bytes_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])/120) by(pod, node_id)
milvus_proxy_receive_bytes_count
插入和删除请求的计数。
发送字节率
每个代理在过去两分钟内响应搜索和查询请求时，每秒发回客户端的字节数。
sum(increase(milvus_proxy_send_bytes_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])/120) by(pod, node_id)
milvus_proxy_send_bytes_count
每个代理在响应搜索和查询请求时发回客户端的字节数。
根协调器
面板
面板描述
PromQL （普罗米修斯查询语言）
使用的 Milvus 指标
Milvus 指标说明
代理节点数
创建的代理节点数。
sum(milvus_rootcoord_proxy_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance)
milvus_rootcoord_proxy_num
代理节点数。
同步时间
每个物理通道（PChannel）中每个 Root coord 同步的平均、最大和最小历元时间数。
avg(milvus_rootcoord_sync_epoch_time{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance) max(milvus_rootcoord_sync_epoch_time{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance) min(milvus_rootcoord_sync_epoch_time{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance)
milvus_rootcoord_sync_epoch_time
每个物理通道的纪元时间（Unix 时间，自 1970 年 1 月 1 日起经过的毫秒数）。
DDL 请求率
过去两分钟内每秒 DDL 请求的状态和数量。
sum(increase(milvus_rootcoord_ddl_req_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])/120) by (status, function_name)
milvus_rootcoord_ddl_req_count
DDL 请求总数，包括
CreateCollection
,
DescribeCollection
,
DescribeSegments
,
HasCollection
,
ShowCollections
,
ShowPartitions
, 和
ShowSegments
。
DDL 请求延迟
过去两分钟内 DDL 请求延迟的平均值和第 99 百分位数。
P99:
histogram_quantile(0.99, sum by (le, function_name) (rate(milvus_rootcoord_ddl_req_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_rootcoord_ddl_req_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (function_name) / sum(increase(milvus_rootcoord_ddl_req_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by (function_name)
milvus_rootcoord_ddl_req_latency
所有类型 DDL 请求的延迟。
同步定时器延迟
过去两分钟内 Root coord 将所有时间戳同步到 PChannel 所用时间的平均延迟和第 99 百分位数。
p99:
histogram_quantile(0.99, sum by (le) (rate(milvus_rootcoord_sync_timetick_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
avg:
sum(increase(milvus_rootcoord_sync_timetick_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) / sum(increase(milvus_rootcoord_sync_timetick_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m]))
milvus_rootcoord_sync_timetick_latency
Root coord 将所有时间戳同步到 PChannel 所用的时间。
ID 分配率
根协调器在过去两分钟内每秒分配的 ID 数量。
sum(increase(milvus_rootcoord_id_alloc_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])/120)
milvus_rootcoord_id_alloc_count
根协调器分配的 ID 的累计数量。
时间戳
Root coord 的最新时间戳。
milvus_rootcoord_timestamp{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}
milvus_rootcoord_timestamp
Root coord 的最新时间戳。
保存的时间戳
根协调器保存在元存储中的预分配时间戳。
milvus_rootcoord_timestamp_saved{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}
milvus_rootcoord_timestamp_saved
Root coord 保存在元存储中的预分配时间戳。
时间戳提前 3 秒分配。时间戳每 50 毫秒更新一次并保存在元存储中。
Collections 数量
集合总数。
sum(milvus_rootcoord_collection_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance)
milvus_rootcoord_collection_num
Milvus 当前存在的 Collections 总数。
分区数
分区总数。
sum(milvus_rootcoord_partition_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance)
milvus_rootcoord_partition_num
Milvus 当前存在的分区总数。
DML 通道数
DML 通道总数。
sum(milvus_rootcoord_dml_channel_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance)
milvus_rootcoord_dml_channel_num
Milvus 当前存在的 DML 通道总数。
消息流总数
msgstream 总数。
sum(milvus_rootcoord_msgstream_obj_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance)
milvus_rootcoord_msgstream_obj_num
Milvus 当前的 msgstream 总数。
凭证总数
凭证总数。
sum(milvus_rootcoord_credential_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance)
milvus_rootcoord_credential_num
Milvus 当前的证书总数。
时间刻度延迟
所有数据节点和查询节点上流量图的最大时间刻度延迟之和。
sum(milvus_rootcoord_time_tick_delay{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance)
milvus_rootcoord_time_tick_delay
每个数据节点和查询节点上流量图的最大时间刻度延迟。
查询协调器
面板
面板描述
PromQL （Prometheus 查询语言）
使用的 Milvus 指标
Milvus 指标说明
Collections Loaded Num（已加载的集合数
当前加载到内存中的 Collections 数量。
sum(milvus_querycoord_collection_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance)
milvus_querycoord_collection_num
Milvus 当前加载的 Collection 数量。
加载的实体数
当前加载到内存中的实体数量。
sum(milvus_querycoord_entity_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance)
milvus_querycoord_entitiy_num
Milvus 当前加载的实体数量。
加载请求率
过去两分钟内每秒的加载请求数。
sum(increase(milvus_querycoord_load_req_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])120) by (status)
milvus_querycoord_load_req_count
累计加载请求数。
释放请求率
过去两分钟内每秒的释放请求数。
sum(increase(milvus_querycoord_release_req_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])/120) by (status)
milvus_querycoord_release_req_count
累计释放请求数。
负载请求延迟
过去两分钟内负载请求延迟的平均值和第 99 百分位数。
P99:
histogram_quantile(0.99, sum by (le) (rate(milvus_querycoord_load_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_querycoord_load_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) / sum(increase(milvus_querycoord_load_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m]))
milvus_querycoord_load_latency
完成负载请求所用的时间。
释放请求延迟
过去两分钟内发布请求延迟的平均延迟和第 99 百分位数。
p99:
histogram_quantile(0.99, sum by (le) (rate(milvus_querycoord_release_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
avg:
sum(increase(milvus_querycoord_release_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) / sum(increase(milvus_querycoord_release_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m]))
milvus_querycoord_release_latency
完成一个释放请求所用的时间。
子负载任务
子负载任务的数量。
sum(milvus_querycoord_child_task_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance)
milvus_querycoord_child_task_num
子负载任务的数量。
一个 Query coord 将一个负载请求拆分为多个子负载任务。
父负载任务
父负载任务数。
sum(milvus_querycoord_parent_task_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance)
milvus_querycoord_parent_task_num
子负载任务的数量。
每个负载请求对应任务队列中的一个父任务。
子负载任务延迟
子负载任务在过去两分钟内的平均延迟和第 99 百分位延迟。
P99:
histogram_quantile(0.99, sum by (le) (rate(milvus_querycoord_child_task_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_querycoord_child_task_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) / sum(increase(milvus_querycoord_child_task_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) namespace"}[2m])))
milvus_querycoord_child_task_latency
完成子加载任务的延迟。
查询节点数
query coord 管理的查询节点数。
sum(milvus_querycoord_querynode_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance)
milvus_querycoord_querynode_num
由 Query coord 管理的查询节点数。
查询节点
面板
面板描述
PromQL（普罗米修斯查询语言）
使用的 Milvus 指标
Milvus 指标描述
Collections Loaded Num（加载的集合数
每个查询节点加载到内存中的 Collection 数量。
sum(milvus_querynode_collection_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id)
milvus_querynode_collection_num
每个查询节点加载的 Collection 数量。
加载的分区数
每个查询节点加载到内存中的分区数。
sum(milvus_querynode_partition_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id)
milvus_querynode_partition_num
每个查询节点加载的分区数。
加载的分段数
每个查询节点加载到内存中的分段数。
sum(milvus_querynode_segment_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id)
milvus_querynode_segment_num
每个查询节点加载的分段数。
可查询实体数
每个查询节点上可查询和可搜索实体的数量。
sum(milvus_querynode_entity_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id)
milvus_querynode_entity_num
每个查询节点上可查询和可搜索实体的数量。
DML 虚拟通道
每个查询节点监视的 DML 虚拟通道数。
sum(milvus_querynode_dml_vchannel_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id)
milvus_querynode_dml_vchannel_num
每个查询节点监视的 DML 虚拟通道数。
三角虚拟通道
每个查询节点监视的 delta 通道数。
sum(milvus_querynode_delta_vchannel_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id)
milvus_querynode_delta_vchannel_num
每个查询节点查看的 delta 通道数。
用户数
每个查询节点中消费者的数量。
sum(milvus_querynode_consumer_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id)
milvus_querynode_consumer_num
每个查询节点中消费者的数量。
搜索请求率
每个查询节点每秒收到的搜索和查询请求总数，以及过去两分钟内成功搜索和查询请求的数量。
sum(increase(milvus_querynode_sq_req_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])/120) by (query_type, status, pod, node_id)
milvus_querynode_sq_req_count
搜索和查询请求的累计数量。
搜索请求延迟
每个查询节点在过去两分钟内搜索和查询请求所用时间的平均延迟和第 99 百分位数。
此面板显示状态为 "成功 "或 "总计 "的搜索和查询请求的延迟。
P99:
histogram_quantile(0.99, sum by (le, pod, node_id) (rate(milvus_querynode_sq_req_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_querynode_sq_req_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id, query_type) / sum(increase(milvus_querynode_sq_req_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id, query_type)
milvus_querynode_sq_req_latency
查询节点的搜索请求延迟。
队列中搜索延迟
过去两分钟内队列中搜索和查询请求的平均延迟和第 99 百分位数延迟。
P99:
histogram_quantile(0.99, sum by (le, pod, node_id, query_type) (rate(milvus_querynode_sq_queue_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_querynode_sq_queue_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id, query_type) / sum(increase(milvus_querynode_sq_queue_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id, query_type)
milvus_querynode_sq_queue_latency
查询节点收到的搜索和查询请求的延迟。
搜索段延迟
每个查询节点在过去两分钟内搜索和查询一个数据段所需时间的平均延迟和第 99 百分位数。
段的状态可以是封存或增长。
p99:
histogram_quantile(0.99, sum by (le, query_type, segment_state, pod, node_id) (rate(milvus_querynode_sq_segment_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
avg:
sum(increase(milvus_querynode_sq_segment_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id, query_type, segment_state) / sum(increase(milvus_querynode_sq_segment_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id, query_type, segment_state)
milvus_querynode_sq_segment_latency
每个查询节点搜索和查询每个分段所需的时间。
Segcore 请求延迟
每个查询节点在过去两分钟内搜索和查询 segcore 所花时间的平均延迟和第 99 百分位数。
P99:
histogram_quantile(0.99, sum by (le, query_type, pod, node_id) (rate(milvus_querynode_sq_core_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_querynode_sq_core_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id, query_type) / sum(increase(milvus_querynode_sq_core_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id, query_type)
milvus_querynode_sq_core_latency
每个查询节点在 segcore 中搜索和查询所需的时间。
搜索减少延迟
过去两分钟内每个查询节点在搜索或查询还原阶段所用时间的平均延迟和第 99 百分位数。
P99:
histogram_quantile(0.99, sum by (le, pod, node_id, query_type) (rate(milvus_querynode_sq_reduce_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_querynode_sq_reduce_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id, query_type) / sum(increase(milvus_querynode_sq_reduce_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id, query_type)
milvus_querynode_sq_reduce_latency
每个查询在缩减阶段花费的时间。
负载分段延迟
在过去两分钟内，每个查询节点加载段所需时间的平均延迟和第 99 百分位数。
P99:
histogram_quantile(0.99, sum by (le, pod, node_id) (rate(milvus_querynode_load_segment_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_querynode_load_segment_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id) / sum(increase(milvus_querynode_load_segment_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id)
milvus_querynode_load_segment_latency_bucket
每个查询节点加载分段所需的时间。
流程图总数
每个查询节点中的流程图数量。
sum(milvus_querynode_flowgraph_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id)
milvus_querynode_flowgraph_num
每个查询节点中的流程图数量。
未解决的读取任务长度
每个查询节点中未解决的读取请求队列的长度。
sum(milvus_querynode_read_task_unsolved_len{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id)
milvus_querynode_read_task_unsolved_len
未解决读取请求队列的长度。
就绪读取任务长度
每个查询节点中待执行读取请求队列的长度。
sum(milvus_querynode_read_task_ready_len{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id)
milvus_querynode_read_task_ready_len
待执行读取请求队列的长度。
并行读取任务数
每个查询节点中当前执行的并发读取请求数。
sum(milvus_querynode_read_task_concurrency{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id)
milvus_querynode_read_task_concurrency
当前执行的并发读取请求数。
估计 CPU 占用率
调度程序估算的每个查询节点的 CPU 占用率。
sum(milvus_querynode_estimate_cpu_usage{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id)
milvus_querynode_estimate_cpu_usage
调度程序估算的每个查询节点的 CPU 占用率。
当值为 100 时，表示使用了整个虚拟 CPU (vCPU)。
搜索组大小
过去两分钟内搜索组大小（即每个查询节点执行的合并搜索请求中原始搜索请求的总数）的平均值和第 99 百分位数。
P99:
histogram_quantile(0.99, sum by (le, pod, node_id) (rate(milvus_querynode_search_group_size_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_querynode_search_group_size_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id) / sum(increase(milvus_querynode_search_group_size_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id)
milvus_querynode_load_segment_latency_bucket
不同搜索任务组合中的原始搜索任务数（即搜索组大小）。
搜索 NQ
每个查询节点在过去两分钟内执行搜索请求时完成的查询次数 (NQ) 的平均值和第 99 百分位数。
P99:
histogram_quantile(0.99, sum by (le, pod, node_id) (rate(milvus_querynode_search_group_size_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_querynode_search_group_size_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id) / sum(increase(milvus_querynode_search_group_size_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id)
milvus_querynode_load_segment_latency_bucket
搜索请求的查询次数（NQ）。
搜索组 NQ
过去两分钟内每个查询节点合并执行的搜索请求 NQ 的平均数和第 99 百分位数。
P99:
histogram_quantile(0.99, sum by (le, pod, node_id) (rate(milvus_querynode_search_group_nq_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_querynode_search_group_nq_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id) / sum(increase(milvus_querynode_search_group_nq_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id)
milvus_querynode_load_segment_latency_bucket
来自不同分组的搜索请求的 NQ 值。
搜索 Top_K
每个查询节点在过去两分钟内执行的
Top_K
搜索请求的平均数和第 99 百分位数。
p99:
histogram_quantile(0.99, sum by (le, pod, node_id) (rate(milvus_querynode_search_topk_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
avg:
sum(increase(milvus_querynode_search_topk_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id) / sum(increase(milvus_querynode_search_topk_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id)
milvus_querynode_load_segment_latency_bucket
搜索请求的
Top_K
。
搜索组 Top_K
每个查询节点在过去两分钟内执行的
Top_K
搜索请求的平均值和第 99 百分位数。
p99:
histogram_quantile(0.99, sum by (le, pod, node_id) (rate(milvus_querynode_search_group_topk_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
avg:
sum(increase(milvus_querynode_search_group_topk_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id) / sum(increase(milvus_querynode_search_group_topk_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id)
milvus_querynode_load_segment_latency_bucket
来自不同数据桶的合并搜索请求的
Top_K
。
驱逐读取请求率
每个查询节点在过去两分钟内每秒驱逐的读取请求数。
sum(increase(milvus_querynode_read_evicted_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])/120) by (pod, node_id)
milvus_querynode_sq_req_count
查询节点因流量限制而驱逐的读取请求累计数。
数据协调器
面板
面板描述
PromQL（普罗米修斯查询语言）
使用的 Milvus 指标
Milvus 指标说明
数据节点数
由 data coord. 管理的数据节点数。
sum(milvus_datacoord_datanode_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance)
milvus_datacoord_datanode_num
由 data coord 管理的数据节点数。
数据段数
Data coord 记录在元数据中的所有类型数据段的数量。
sum(milvus_datacoord_segment_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (segment_state)
milvus_datacoord_segment_num
Data coord 记录在元数据中的所有类型数据段的数量。
数据段类型包括：丢弃、刷新、冲洗、增长和密封。
Collections Num（收集数
元数据中按数据坐标记录的 Collections 数量。
sum(milvus_datacoord_collection_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance)
milvus_datacoord_collection_num
按数据坐标在元数据中记录的 Collections 数量。
存储行数
Data coord 中有效数据和刷新数据的累计行数。
sum(milvus_datacoord_stored_rows_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance)
milvus_datacoord_stored_rows_num
Data coord 中有效数据和刷新数据的累计行数。
存储行速率
过去两分钟内平均每秒刷新的行数。
sum(increase(milvus_datacoord_stored_rows_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])/120) by (pod, node_id)
milvus_datacoord_stored_rows_count
Data coord 刷新数据的累计行数。
同步时间
Data coord 在每个物理通道中同步的平均、最大和最小历时。
avg(milvus_datacoord_sync_epoch_time{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance) max(milvus_datacoord_sync_epoch_time{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance) min(milvus_datacoord_sync_epoch_time{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance)
milvus_datacoord_sync_epoch_time
每个物理通道的纪元时间（Unix 时间，1970 年 1 月 1 日以来的毫秒数）。
存储的日志大小
存储的 binlog 的总大小。
sum(milvus_datacoord_stored_binlog_size{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance)
milvus_datacoord_stored_binlog_size
存储在 Milvus 中的 binlog 的总大小。
数据节点
面板
面板描述
PromQL （Prometheus 查询语言）
使用的 Milvus 指标
Milvus 指标说明
流图数量
每个数据节点对应的 flowgraph 对象数量。
sum(milvus_datanode_flowgraph_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id)
milvus_datanode_flowgraph_num
流图对象的数量。
Collections 中的每个分片对应一个 flowgraph 对象。
信息行消耗率
每个数据节点在过去两分钟内每秒消耗的流媒体消息行数。
sum(increase(milvus_datanode_msg_rows_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])/120) by (msg_type, pod, node_id)
milvus_datanode_msg_rows_count
消耗的流式信息行数。
目前，按数据节点计算的流式信息只包括插入和删除信息。
刷新数据大小率
每个数据节点在过去两分钟内每秒记录的每条刷新信息的大小。
sum(increase(milvus_datanode_flushed_data_size{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])/120) by (msg_type, pod, node_id)
milvus_datanode_flushed_data_size
每条刷新信息的大小。
目前，按数据节点计算的流媒体信息只包括插入和删除信息。
用户数
每个数据节点上创建的消费者数量。
sum(milvus_datanode_consumer_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id)
milvus_datanode_consumer_num
每个数据节点上创建的消费者数量。
每个流程图对应一个消费者。
生产者编号
每个数据节点上创建的生产者数量。
sum(milvus_datanode_producer_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id)
milvus_datanode_producer_num
每个数据节点上创建的消费者数量。
Collections 中的每个分片对应一个 delta 通道生产者和一个 timetick 通道生产者。
同步时间
所有物理主题中每个数据节点同步的平均、最大和最小纪元时间数。
avg(milvus_datanode_sync_epoch_time{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id) max(milvus_datanode_sync_epoch_time{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id) min(milvus_datanode_sync_epoch_time{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id)
milvus_datanode_sync_epoch_time
数据节点上每个物理主题的纪元时间（Unix 时间，自 1970 年 1 月 1 日起流逝的毫秒数）。
未刷新段数
每个数据节点上创建的未刷新段的数量。
sum(milvus_datanode_unflushed_segment_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (pod, node_id)
milvus_datanode_unflushed_segment_num
每个数据节点上创建的未刷新段的数量。
编码缓冲区延迟
每个数据节点在过去两分钟内编码缓冲区所用时间的平均延迟和第 99 百分位数。
P99:
histogram_quantile(0.99, sum by (le, pod, node_id) (rate(milvus_datanode_encode_buffer_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_datanode_encode_buffer_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id) / sum(increase(milvus_datanode_encode_buffer_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id)
milvus_datanode_encode_buffer_latency
每个数据节点对缓冲区进行编码所需的时间。
保存数据延迟
每个数据节点在过去两分钟内将缓冲区写入存储层所用时间的平均延迟和第 99 百分位数。
P99:
histogram_quantile(0.99, sum by (le, pod, node_id) (rate(milvus_datanode_save_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_datanode_save_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id) / sum(increase(milvus_datanode_save_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id)
milvus_datanode_save_latency
每个数据节点将缓冲区写入存储层所需的时间。
刷新操作符率
每个数据节点在过去两分钟内每秒刷新缓冲区的次数。
sum(increase(milvus_datanode_flush_buffer_op_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])/120) by (status, pod, node_id)
milvus_datanode_flush_buffer_op_count
数据节点刷新缓冲区的累计次数。
自动冲洗操作符率
过去两分钟内每个数据节点每秒自动刷新缓冲区的次数。
sum(increase(milvus_datanode_autoflush_buffer_op_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])/120) by (status, pod, node_id)
milvus_datanode_autoflush_buffer_op_count
数据节点自动刷新缓冲区的累计次数。
冲洗请求率
每个数据节点在过去两分钟内每秒收到缓冲区刷新请求的次数。
sum(increase(milvus_datanode_flush_req_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])/120) by (status, pod, node_id)
milvus_datanode_flush_req_count
数据节点从 Data coord 接收刷新请求的累计次数。
压缩延迟
每个数据节点在过去两分钟内执行压缩任务所用时间的平均延迟和百分位数 99。
P99:
histogram_quantile(0.99, sum by (le, pod, node_id) (rate(milvus_datanode_compaction_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_datanode_compaction_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id) / sum(increase(milvus_datanode_compaction_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id)
milvus_datanode_compaction_latency
每个数据节点执行压缩任务所需的时间。
索引协调器
面板
面板描述
PromQL（普罗米修斯查询语言）
使用的 Milvus 指标
Milvus 指标说明
索引请求率
过去两分钟内平均每秒收到的索引构建请求数。
sum(increase(milvus_indexcoord_indexreq_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])/120) by (status)
milvus_indexcoord_indexreq_count
收到的索引构建请求数。
索引任务计数
索引元数据中记录的所有索引任务的计数。
sum(milvus_indexcoord_indextask_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (index_task_status)
milvus_indexcoord_indextask_count
索引元数据中记录的所有索引任务的计数。
索引节点数
受管索引节点的数量。
sum(milvus_indexcoord_indexnode_num{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}) by (app_kubernetes_io_instance)
milvus_indexcoord_indexnode_num
受管索引节点的数量。
索引节点
面板
面板描述
PromQL （Prometheus 查询语言）
使用的 Milvus 指标
Milvus 指标说明
索引任务率
过去两分钟内每个索引节点每秒收到的索引构建任务的平均数量。
sum(increase(milvus_indexnode_index_task_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])/120) by (status, pod, node_id)
milvus_indexnode_index_task_count
收到的索引构建任务数。
负载字段延迟
过去两分钟内，每个索引节点每次加载段字段数据所用时间的平均延迟和第 99 百分位数。
P99:
histogram_quantile(0.99, sum by (le, pod, node_id) (rate(milvus_indexnode_load_field_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_indexnode_load_field_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id) / sum(increase(milvus_indexnode_load_field_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id)
milvus_indexnode_load_field_latency
索引节点加载分段字段数据所用的时间。
解码字段延迟
每个索引节点在过去两分钟内每次编码字段数据所用时间的平均延迟和第 99 百分位数。
P99:
histogram_quantile(0.99, sum by (le, pod, node_id) (rate(milvus_indexnode_decode_field_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
AVG:
sum(increase(milvus_indexnode_decode_field_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id) / sum(increase(milvus_indexnode_decode_field_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id)
milvus_indexnode_decode_field_latency
用于解码字段数据的时间。
建立索引延迟
每个索引节点在过去两分钟内建立索引所用时间的平均延迟和第 99 百分位数。
p99:
histogram_quantile(0.99, sum by (le, pod, node_id) (rate(milvus_indexnode_build_index_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
avg:
sum(increase(milvus_indexnode_build_index_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id) / sum(increase(milvus_indexnode_build_index_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id)
milvus_indexnode_build_index_latency
用于建立索引的时间。
编码索引延迟
每个索引节点在过去两分钟内编码索引文件所用时间的平均延迟和第 99 百分位数。
p99:
histogram_quantile(0.99, sum by (le, pod, node_id) (rate(milvus_indexnode_encode_index_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
avg:
sum(increase(milvus_indexnode_encode_index_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id) / sum(increase(milvus_indexnode_encode_index_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id)
milvus_indexnode_encode_index_latency
用于编码索引文件的时间。
保存索引延迟
每个索引节点在过去两分钟内保存索引文件所用时间的平均延迟和第 99 百分位数。
p99:
histogram_quantile(0.99, sum by (le, pod, node_id) (rate(milvus_indexnode_save_index_latency_bucket{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])))
avg:
sum(increase(milvus_indexnode_save_index_latency_sum{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id) / sum(increase(milvus_indexnode_save_index_latency_count{app_kubernetes_io_instance=~"$instance", app_kubernetes_io_name="$app_name", namespace="$namespace"}[2m])) by(pod, node_id)
milvus_indexnode_save_index_latency
保存索引文件所用的时间。