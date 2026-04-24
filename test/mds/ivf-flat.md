IVF_FLAT
IVF_FLAT
索引是一种可以提高浮点向量搜索性能的索引算法。
这种索引类型非常适合需要快速查询响应和高精确度的大规模数据集，尤其是在对数据集进行聚类可以减少搜索空间，并且有足够内存存储聚类数据的情况下。
概览
术语
IVF_FLAT
代表
反转文件扁平
，概括了其索引和搜索浮点向量的双层方法：
反转文件 (IVF)：
指使用
K 均值
聚类将向量空间
聚类
为可管理的区域。每个聚类都有一个
中心点
，作为内部向量的参考点。
扁平：
表示在每个聚类中，向量以原始形式（扁平结构）存储，不做任何压缩或量化，以便进行精确的距离计算。
下图显示了其工作原理：
IVF FLAT 工作流程
这种索引方法加快了搜索过程，但也有潜在的缺点：找到的最接近查询嵌入的候选嵌入可能并不是准确的最近嵌入。如果与查询嵌入点最近的嵌入点所在的聚类与根据最近中心点选择的聚类不同，就会出现这种情况（见下面的可视化图示）。
为了解决这个问题，
IVF_FLAT
提供了两个超参数供我们调整：
nlist
:指定使用 k-means 算法创建的分区数量。
nprobe
:指定在搜索候选对象时要考虑的分区数量。
现在，如果我们将
nprobe
设置为 3，而不是 1，就会得到如下结果：
IVF FLAT 工作流程 2
通过增加
nprobe
值，可以在搜索中包含更多分区，这有助于确保不会错过与查询最接近的嵌入，即使它位于不同的分区中。不过，这样做的代价是增加搜索时间，因为需要评估更多候选项。有关索引参数调整的更多信息，请参阅
索引参数
。
建立索引
要在 Milvus 中的向量场上建立
IVF_FLAT
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
"your_vector_field_name"
,
# Name of the vector field to be indexed
index_type=
"IVF_FLAT"
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
64
,
# Number of clusters for the index
}
# Index building params
)
在此配置中
index_type
:要建立的索引类型。在本例中，将值设为
IVF_FLAT
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
:用于建立索引的附加配置选项。
nlist
:划分数据集的簇数。
要了解
IVF_FLAT
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
IVF_FLAT
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
在建立索引时使用 k-means 算法创建的簇数。每个簇由一个中心点代表，存储一个向量列表。增加该参数可减少每个簇中的向量数量，从而创建更小、更集中的分区。
类型
： 整数整数
范围
：[1, 65536]
默认值
：
128
nlist
值越大，通过创建更精细的簇来提高召回率，但会增加索引构建时间。请根据数据集大小和可用资源进行优化。大多数情况下，我们建议在此范围内设置值：[32, 4096].
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
搜索候选集群的集群数。数值越大，搜索的簇数越多，搜索范围越大，召回率越高，但代价是查询延迟增加。
类型
： 整数整数
范围
[1，
nlist］
默认值
：
8
增加该值可提高召回率，但可能会减慢搜索速度。设置
nprobe
与
nlist
成比例，以平衡速度和准确性。
在大多数情况下，我们建议您在此范围内设置一个值：[1，nlist]。