GPU_BRUTE_FORCE
GPU_BRUTE_FORCE
索引专为
GPU
环境设计，适用于对准确性要求极高的场景。它通过将每个查询与数据集中的所有向量进行详尽比较，确保不会忽略任何潜在匹配，从而保证召回率为 1。利用 GPU 加速，GPU_BRUTE_FORCE 适用于要求向量相似性搜索绝对精确的应用。
建立索引
要在 Milvus 中的向量场上建立
GPU_BRUTE_FORCE
索引，请使用
add_index()
方法，为索引指定
index_type
和
metric_type
参数。
from
pymilvus
import
MilvusClient
# Prepare index building params
index_params = MilvusClient.prepare_index_params()

index_params.add_index(
    field_name=
"your_vector_field_name"
,
# Name of the vector field to be indexed
index_type=
"GPU_BRUTE_FORCE"
,
# Type of the index to create
index_name=
"vector_index"
,
# Name of the index to create
metric_type=
"L2"
,
# Metric type used to measure similarity
params={}
# No additional parameters required for GPU_BRUTE_FORCE
)
在此配置中
index_type
:要建立的索引类型。在本例中，将值设为
GPU_BRUTE_FORCE
。
metric_type
:用于计算向量间距离的方法。有关详情，请参阅 "
度量类型
"。
params
:GPU_BRUTE_FORCE 索引不需要额外参数。
配置好索引参数后，可直接使用
create_index()
方法或在
create_collection
方法中传递索引参数来创建索引。有关详情，请参阅
创建 Collections
。
在索引上搜索
建立索引并插入实体后，就可以在索引上执行相似性搜索。
res = MilvusClient.search(
    collection_name=
"your_collection_name"
,
# Collection name
anns_field=
"vector_field"
,
# Vector field name
data=[[
0.1
,
0.2
,
0.3
,
0.4
,
0.5
]],
# Query vector
limit=
3
,
# TopK results to return
search_params={
"params"
: {}}
# No additional parameters required for GPU_BRUTE_FORCE
)
索引参数
对于
GPU_BRUTE_FORCE
索引，在创建索引或搜索过程中都不需要额外参数。