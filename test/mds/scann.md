SCANN
在谷歌
ScaNN
库的支持下，Milvus 中的
SCANN
索引旨在应对向量相似性搜索的扩展挑战，在速度和准确性之间取得平衡，即使是在传统上会给大多数搜索算法带来挑战的大型数据集上也是如此。
概述
ScaNN 是为解决向量搜索中最大的挑战之一而设计的：即使数据集越来越大、越来越复杂，也能在高维空间中高效地找到最相关的向量。它的架构将向量搜索过程分解为不同的阶段：
扫描
分区
：将数据集划分为簇。这种方法只关注相关数据子集，而不是扫描整个数据集，从而缩小了搜索空间，节省了时间和处理资源。ScaNN 通常使用
k-means
等聚类算法来识别聚类，从而更高效地执行相似性搜索。
量化
：ScaNN 在分区后采用一种称为
各向异性向量量化的量化
过程。传统的量化侧重于最小化原始向量和压缩向量之间的整体距离，这对于
最大内积搜索（MIPS）
等任务来说并不理想，因为在这类任务中，相似性是由向量的内积而非直接距离决定的。各向异性量化则优先保留向量之间的平行分量，或对计算精确内积最重要的部分。通过这种方法，ScaNN 可以仔细地将压缩向量与查询对齐，从而保持较高的 MIPS 精度，实现更快、更精确的相似性搜索。
重新排序
重新排序阶段是最后一步，ScaNN 在此阶段对分区和量化阶段的搜索结果进行微调。这种重新排序会对排名靠前的候选向量进行精确的内积计算，确保最终结果高度准确。重新排序在高速推荐引擎或图像搜索应用中至关重要，在这些应用中，最初的过滤和聚类是粗略的一层，而最后阶段则确保只向用户返回最相关的结果。
SCANN
的性能由两个关键参数控制，您可以对速度和准确性之间的平衡进行微调：
with_raw_data
:控制原始向量数据是否与量化表示同时存储。启用该参数可提高重新排序时的准确性，但会增加存储需求。
reorder_k
:确定在重新排序的最后阶段对多少候选对象进行细化。数值越大，准确率越高，但搜索延迟也会增加。
有关针对特定用例优化这些参数的详细指导，请参阅
索引参数
。
建立索引
要在 Milvus 中的向量场上建立
SCANN
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
"SCANN"
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
"with_raw_data"
:
True
,
# Whether to hold raw data
}
# Index building params
)
在此配置中
index_type
:要建立的索引类型。在本例中，将值设为
SCANN
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
with_raw_data
:是否在存储量化表示的同时存储原始向量数据。
要了解
SCANN
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
"reorder_k"
:
10
,
# Number of candidates to refine
"nprobe"
:
8
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
10
,
# TopK results to return
search_params=search_params
)
在此配置中
params
:在索引上搜索的其他配置选项。
reorder_k
:在重新排序阶段要细化的候选实体数量。
nprobe
:要搜索的簇数。
要了解
SCANN
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
群组单位数
[1, 65536]
较高的
nlist
会提高剪枝效率，通常会加快粗搜索速度，但分区可能会变小，从而降低召回率；较低的
nlist
会扫描较大的簇，提高召回率，但会减慢搜索速度。
with_raw_data
是否在量化表示的同时存储原始向量数据。启用后，在重新排序阶段，可以使用原始向量而不是量化近似值来进行更精确的相似性计算。
类型
：布尔布尔
范围
true
,
false
默认值
：
true
设置为
true
以获得
更高的搜索精度
，并且存储空间不是首要考虑因素。原始向量数据可在重新排序时进行更精确的相似性计算。
设置为
false
可
减少存储开销
和内存使用，尤其是对于大型数据集。不过，由于重新排序阶段将使用量化向量，这可能会导致搜索精度略微降低。
建议
使用：对于准确性要求较高的生产应用，请使用
true
。
特定索引搜索参数
下表列出了
在索引上搜索
时可在
search_params.params
中配置的参数。
参数
说明
值范围
调整建议
reorder_k
控制在重新排序阶段精炼的候选向量数量。该参数决定了使用更精确的相似性计算方法重新评估初始分区和量化阶段的前几名候选向量的数量。
类型
：整数
范围
： [1, int_max[1，
int_max］
默认值
：无无
reorder_k
越大，
搜索精度越高
，因为在最后的细化阶段会考虑更多的候选项。不过，这也会因为额外的计算而
增加搜索时间
。
如果实现高召回率至关重要，而搜索速度又不是那么重要，那么可以考虑提高
reorder_k
。一个好的起点是 2-5 倍于所需的
limit
（返回的前 K 个结果）。
考虑降低
reorder_k
以优先加快搜索速度，尤其是在可以接受准确率略有下降的情况下。
在大多数情况下，我们建议您在此范围内设置一个值：
[limit
，
limit
* 5]。
nprobe
搜索候选集群的数量。
类型
：整数
范围
： [1, nlist[1，
nlist］
默认值
：
8
较高的值允许搜索更多的群集，通过扩大搜索范围提高召回率，但代价是增加查询延迟。
设置
nprobe
与
nlist
成比例，以平衡速度和准确性。
在大多数情况下，我们建议您在此范围内设置值：[1，nlist]。