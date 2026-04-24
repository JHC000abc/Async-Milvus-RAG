GPU_IVF_PQ
GPU_IVF_PQ
索引以
IVF_PQ
概念为基础，将反向文件聚类与乘积量化（PQ）相结合，后者将高维向量分解为更小的子空间并对其进行量化，从而实现高效的相似性搜索。GPU_IVF_PQ 专为 GPU 环境设计，利用并行处理加速计算并有效处理大规模向量数据。有关基础概念的更多信息，请参阅
IVF_PQ
。
建立索引
要在 Milvus 中的向量场上建立
GPU_IVF_PQ
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
"GPU_IVF_PQ"
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
"m"
:
4
,
# Number of sub-vectors to split eahc vector into
}
# Index building params
)
在此配置中
index_type
:要建立的索引类型。在本例中，将值设为
GPU_IVF_PQ
。
metric_type
:用于计算向量间距离的方法。支持的值包括
COSINE
,
L2
, 和
IP
。有关详情，请参阅
公制类型
。
params
:用于建立索引的附加配置选项。
m
:将向量分割成的子向量个数。
要了解
GPU_IVF_PQ
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
search_params=search_params
)
在此配置中
params
:在索引上搜索的其他配置选项。
nprobe
:要搜索的群集数量。
要了解
GPU_IVF_PQ
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
IVF
nlist
在索引创建过程中使用 k-means 算法创建的簇数。
类型
： 整数整数
范围
：[1, 65536]
默认值
：
128
nlist
值越大，创建的簇越精细，召回率越高，但会增加索引构建时间。根据数据集大小和可用资源进行优化。 在大多数情况下，我们建议在此范围内设置值：[32, 4096].
PQ
m
在量化过程中将每个高维向量分成的子向量数（用于量化）。
类型
： 整数整数
范围
： [1, 65536[1, 65536]
默认值
：无
m
m
必须是向量维数
(D
) 的除数，以确保正确分解。通常推荐的值是
m = D/2
。
在大多数情况下，我们建议在此范围内设置一个值：[D/8，D]。
nbits
用于以压缩形式表示每个子向量中心点索引的比特数。每个编码本将包含
2
个比特的中心点。例如，如果
nbits
设置为 8，则每个子向量将由一个 8 位的中心点索引表示。这样，该子向量的编码本中就有
28
（256）个可能的中心点。
类型
： 整数整数[1, 24]
默认值
：
8
nbits
值越大，编码本越大，可能会更精确地表示原始向量。在大多数情况下，我们建议在此范围内设置一个值：[1, 16].
cache_dataset_on_device
决定是否在 GPU 内存中缓存原始数据集。可能的值
"true"
:缓存原始数据集，通过细化搜索结果提高召回率。
"false"
:不缓存原始数据集，以节省 GPU 内存。
类型
： 字符串字符串
范围
[
"true"
,
"false"
]
默认值
：
"false"
将其设置为
"true"
可通过细化搜索结果提高召回率，但会占用更多 GPU 内存。设置为
"false"
可节省 GPU 内存。
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
IVF
nprobe
搜索候选集群的集群数。
类型
： 整数整数
范围
[1，
nlist］
默认值
：
8
较高的值允许搜索更多的簇，通过扩大搜索范围提高召回率，但代价是增加查询延迟。设置
nprobe
与
nlist
成比例，以平衡速度和准确性。
在大多数情况下，我们建议您在此范围内设置值：[1，nlist]。