BIN_FLAT
BIN_FLAT
索引是
FLAT
索引的一种变体，专门为二进制嵌入而定制。在向量相似性搜索要求在相对较小、百万级别的数据集上达到完美精确度的应用中，它表现出色。通过采用一种穷举搜索方法--将每个目标输入与数据集中的所有向量进行比较--BIN_FLAT 可以保证得到精确的结果。这种精确性使其成为评估其他可能提供不到 100%召回率的索引性能的理想基准，尽管其彻底的方法也使其成为处理大规模数据最慢的选择。
建立索引
要在 Milvus 中的向量场上建立
BIN_FLAT
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
"your_binary_vector_field_name"
,
# Name of the vector field to be indexed
index_type=
"BIN_FLAT"
,
# Type of the index to create
index_name=
"vector_index"
,
# Name of the index to create
metric_type=
"HAMMING"
,
# Metric type used to measure similarity
params={}
# No additional parameters required for BIN_FLAT
)
在此配置中
index_type
:要建立的索引类型。在本例中，将值设为
BIN_FLAT
。
metric_type
:用于计算向量间距离的方法。二进制 Embeddings 的支持值包括
HAMMING
（默认）和
JACCARD
。有关详情，请参阅 "
度量类型
"。
params
:BIN_FLAT 索引不需要额外参数。
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
"binary_vector_field"
,
# Binary vector field name
data=[query_binary_vector],
# Query binary vector
limit=
3
,
# TopK results to return
search_params={
"params"
: {}}
# No additional parameters required for BIN_FLAT
)
详情请参阅
二进制向量
。
索引参数
对于 BIN_FLAT 索引，在创建索引或搜索过程中都不需要额外的参数。