与 knowhere 相关的配置
任何与 knowhere 向量搜索引擎相关的配置
knowhere.enable
说明
默认值
启用此配置后，以下定义的索引参数将自动填充为索引参数，无需用户输入。
真
knowhere.DISKANN.build.max_degree
说明
默认值
Vamana 图形的最大度数
56
knowhere.DISKANN.build.pq_code_budget_gb_ratio
描述
默认值
PQ 代码大小限制（与原始数据相比）
0.125
knowhere.DISKANN.build.search_cache_budget_gb_ratio
说明
默认值
缓存节点数与原始数据之比
0.1
knowhere.DISKANN.build.search_list_size
说明
默认值
构建图形时候选列表的大小
100
knowhere.DISKANN.search.beam_width_ratio
说明
默认值
每次搜索迭代的最大 IO 请求数与 CPU 数量之比
4