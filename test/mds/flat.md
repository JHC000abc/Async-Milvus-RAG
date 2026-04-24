FLAT
FLAT
索引是最简单、最直接的浮点向量索引和搜索方法之一。它依赖于一种 "蛮力 "方法，即直接将每个查询向量与数据集中的每个向量进行比较，而无需任何高级预处理或数据结构。这种方法保证了准确性，由于对每个潜在匹配都进行了评估，因此可提供 100% 的召回率。
不过，这种穷举式搜索方法也有代价。FLAT 索引是最慢的索引选项，因为每次查询都要对数据集进行一次全面扫描。因此，它并不适合海量数据集的环境，因为在这种环境中，性能是个问题。FLAT 索引的主要优点是简单可靠，因为它不需要训练或复杂的参数配置。
建立索引
要在 Milvus 中的向量场上建立
FLAT
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
"FLAT"
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
# No additional parameters required for FLAT
)
在此配置中
index_type
:要建立的索引类型。在本例中，将值设为
FLAT
。
metric_type
:用于计算向量间距离的方法。支持的值包括
COSINE
,
L2
, 和
IP
。有关详细信息，请参阅
公制类型
。
params
:FLAT 索引不需要额外参数。
配置好索引参数后，可直接使用
create_index()
方法或在
create_collection
方法中传递索引参数来创建索引。详情请参阅
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
# No additional parameters required for FLAT
)
索引参数
对于 FLAT 索引，在创建索引或搜索过程中都不需要额外的参数。