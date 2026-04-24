GPU_IVF_FLAT
GPU_IVF_FLAT
索引是 IVF_FLAT 索引的 GPU 加速版本，专为 GPU 环境设计。它将向量数据划分为
nlist
个聚类单元，并通过首先比较目标查询向量和每个聚类的中心来计算相似性。通过调整
nprobe
参数，只搜索最有希望的簇，从而减少查询时间，同时保持准确性和速度之间的平衡。有关基础概念的更多信息，请参阅
IVF_FLAT
。
建立索引
要在 Milvus 中的向量场上建立
GPU_IVF_FLAT
索引，请使用
add_index()
方法，为索引指定
index_type
,
metric_type
, 以及附加参数。
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
"GPU_IVF_FLAT"
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
params={
"nlist"
:
1024
,
# Number of clusters for the index
}
# Index building params
)
在此配置中
index_type
:要建立的索引类型。在本例中，将值设为
GPU_IVF_FLAT
。
metric_type
:用于计算向量间距离的方法。有关详情，请参阅 "
度量类型
"。
params
:用于建立索引的其他配置选项。
nlist
:划分数据集的簇数。
要了解
GPU_IVF_FLAT
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
search_params = {
"params"
: {
"nprobe"
:
10
,
# Number of clusters to search
}
}

res = MilvusClient.search(
    collection_name=
"your_collection_name"
,
# Collection name
anns_field=
"vector_field"
,
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
search_params=search_params
)
在此配置中
params
:在索引上搜索的其他配置选项。
nprobe
:要搜索的群集数量。
要了解
GPU_IVF_FLAT
索引可用的更多搜索
参数
，请参阅
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
nlist
在建立索引时使用 K-means 算法创建的簇的数量。 每个簇由一个中心点表示，存储一个向量列表。增加该参数可减少每个簇中的向量数量，从而创建更小、更集中的分区。
类型
： 整数整数
范围
：[1, 65536]
默认值
：
128
nlist
值越大，通过创建更精细的簇来提高召回率，但会增加索引构建时间。根据数据集大小和可用资源进行优化。 在大多数情况下，我们建议在此范围内设置值：[32, 4096].
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
nprobe
搜索候选集群的集群数。 数值越大，搜索的集群数越多，搜索范围越大，召回率越高，但代价是查询延迟增加。
类型
： 整数整数[1，
nlist］
默认值
：
8
增加该值可提高召回率，但可能会减慢搜索速度。将
nprobe
设置为与
nlist
成比例，以平衡速度和准确性。
在大多数情况下，我们建议您在此范围内设置一个值：[1，nlist]。