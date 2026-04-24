稀疏反转索引
SPARSE_INVERTED_INDEX
索引是 Milvus 用来高效存储和搜索稀疏向量的一种索引类型。这种索引类型利用了倒排索引的原理，为稀疏数据创建了一种高效的搜索结构。如需了解更多信息，请参阅
INVERTED
。
建立索引
要在 Milvus 中的稀疏向量场上建立
SPARSE_INVERTED_INDEX
索引，请使用
add_index()
方法，指定
index_type
,
metric_type
, 以及索引的附加参数。
from
pymilvus
import
MilvusClient
# Prepare index building params
index_params = MilvusClient.prepare_index_params()

index_params.add_index(
    field_name=
"your_sparse_vector_field_name"
,
# Name of the vector field to be indexed
index_type=
"SPARSE_INVERTED_INDEX"
,
# Type of the index to create
index_name=
"sparse_inverted_index"
,
# Name of the index to create
metric_type=
"IP"
,
# Metric type used to measure similarity
params={
"inverted_index_algo"
:
"DAAT_MAXSCORE"
},
# Algorithm used for building and querying the index
)
在此配置中
index_type
:要建立的索引类型。在本例中，将值设为
SPARSE_INVERTED_INDEX
。
metric_type
:用于计算稀疏向量之间相似性的度量。有效值：
IP
(内积）：使用点积衡量相似性。
BM25
:通常用于全文搜索，侧重于文本相似性。
有关详细信息，请参阅 "
度量类型
和
全文检索
"。
params.inverted_index_algo
:用于建立和查询索引的算法。有效值：
"DAAT_MAXSCORE"
(默认）：使用 MaxScore 算法进行优化的 Document-at-a-Time (DAAT) 查询处理。MaxScore 通过跳过可能影响最小的术语和文档，为高
k
值或包含大量术语的查询提供更好的性能。为此，它根据最大影响分值将术语划分为基本组和非基本组，并将重点放在对前 k 结果有贡献的术语上。
"DAAT_WAND"
:使用 WAND 算法优化 DAAT 查询处理。WAND 算法利用最大影响分数跳过非竞争性文档，从而评估较少的命中文档，但每次命中的开销较高。这使得 WAND 对于
k
值较小的查询或较短的查询更有效，因为在这些情况下跳过更可行。
"TAAT_NAIVE"
:基本术语一次查询处理（TAAT）。虽然与
DAAT_MAXSCORE
和
DAAT_WAND
相比速度较慢，但
TAAT_NAIVE
具有独特的优势。DAAT 算法使用的是缓存的最大影响分数，无论全局 Collections 参数（avgdl）如何变化，这些分数都保持静态，而
TAAT_NAIVE
不同，它能动态地适应这种变化。
要了解
SPARSE_INVERTED_INDEX
索引可用的更多构建
参数
，请参阅
索引构建参数
。
配置好索引参数后，可直接使用
create_index()
方法或在
create_collection
方法中传递索引参数来创建索引。有关详情，请参阅
创建 Collections
。
在索引上搜索
建立索引并插入实体后，就可以在索引上执行相似性搜索。
# Prepare the query vector
query_vector = [{
1
:
0.2
,
50
:
0.4
,
1000
:
0.7
}]

res = MilvusClient.search(
    collection_name=
"your_collection_name"
,
# Collection name
anns_field=
"vector_field"
,
# Vector field name
data=query_vector,
# Query vector
limit=
3
,
# TopK results to return
)
要了解
SPARSE_INVERTED_INDEX
索引可用的更多搜索参数，请参阅
特定于索引的搜索参数
。
索引参数
本节概述了用于建立索引和在索引上执行搜索的参数。
索引建立参数
下表列出了
建立索引
时可在
params
中配置的参数。
参数
说明
值范围
调整建议
inverted_index_algo
用于构建和查询索引的算法。它决定了索引处理查询的方式。
"DAAT_MAXSCORE"
(默认），
"DAAT_WAND"
、
"TAAT_NAIVE"
对于 k 值较高的情况或术语较多的查询，请使用
"DAAT_MAXSCORE"
，这样可以从跳过非竞争文档中获益。
对于 k 值较小的查询或较短的查询，请选择
"DAAT_WAND"
，以提高跳转效率。
如果需要根据 Collections 的变化（如 avgdl）进行动态调整，请使用
"TAAT_NAIVE"
。
特定于索引的搜索参数
下表列出了
在索引上搜索
时可在
search_params.params
中配置的参数。
参数
说明
值范围
调整建议
drop_ratio_search
搜索时忽略最小值的比例，有助于减少噪音。
介于 0.0 和 1.0 之间的百分比（例如，0.2 会忽略 20% 的最小值）
根据查询向量的稀疏程度和噪音水平调整该参数。
该参数控制搜索过程中丢弃的低幅度值的比例。增加该值（例如，增加到
0.2
）可以减少噪音，将搜索重点放在更重要的成分上，从而提高精确度和效率。但是，放弃更多的值也会排除潜在的相关信号，从而降低召回率。请根据您的工作量选择一个能平衡召回率和准确率的值。