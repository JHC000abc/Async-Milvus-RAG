IVF_SQ8
IVF_SQ8
索引是一种
基于量化的
索引算法，旨在解决大规模相似性搜索难题。与穷举搜索方法相比，这种索引类型的搜索速度更快，占用内存更少。
概览
IVF_SQ8 索引基于两个关键组件：
反转文件 (IVF)：
将数据组织成群，使搜索算法只关注最相关的向量子集。
标量量化 (SQ8)：
将向量压缩成更紧凑的形式，大幅减少内存使用量，同时保持足够的精度，以实现快速的相似性计算。
IVF
IVF 就像在一本书中创建索引。你不用扫描每一页（或者，在我们的情况下，每一个向量），而是在索引中查找特定的关键词（簇），从而快速找到相关的页面（向量）。在我们的方案中，向量被归入簇，算法将在与查询向量接近的几个簇内进行搜索。
下面是其工作原理：
聚类：
使用 k-means 等聚类算法，将向量数据集划分为指定数量的簇。每个聚类都有一个中心点（聚类的代表向量）。
分配：
每个向量被分配到其中心点最接近的聚类中。
反向索引：
创建一个索引，将每个聚类的中心点映射到分配给该聚类的向量列表中。
搜索：
搜索近邻时，搜索算法会将查询向量与群集中心点进行比较，并选择最有希望的群集。然后将搜索范围缩小到这些选定簇内的向量。
要了解更多技术细节，请参阅
IVF_FLAT
。
SQ8
标量量化（SQ）是一种用于减少高维向量大小的技术，它将向量的值替换为更小、更紧凑的表示形式。
SQ8
变体使用 8 位整数而不是典型的 32 位浮点数来存储向量的每个维度值。这大大减少了存储数据所需的内存量。
以下是 SQ8 的工作原理：
范围识别：
首先，确定向量内的最小值和最大值。这个范围定义了量化的边界。
归一化：
使用公式将向量值归一化为 0 和 1 之间的范围：
normalized_value
=
value
−
min
max
−
min
\text{normalized\_value} = \frac{\text{value} - \text{min}}{\text{max} - \text{min}}
normalized_value
=
max
−
min
value
−
min
这样可以确保所有值都在标准化范围内按比例映射，为压缩做好准备。
8 位压缩：
将规范化值乘以 255（8 位整数的最大值），然后将结果四舍五入为最接近的整数。这样就能有效地将每个值压缩为 8 位表示。
假设维度值为 1.2，最小值为-1.7，最大值为 2.3。下图显示了如何应用 SQ8 将 float32 值转换为 int8 整数。
IVF SQ8
IVF + SQ8
IVF_SQ8 索引结合了 IVF 和 SQ8，可以高效地执行相似性搜索：
IVF 缩小了搜索范围
：数据集被划分为若干簇，当发出查询时，IVF 首先将查询与簇中心点进行比较，然后选择最相关的簇。
SQ8 加快了距离计算速度
：在选定的簇内，SQ8 会将向量压缩成 8 位整数，从而减少内存使用量，加快距离计算速度。
通过使用 IVF 集中搜索和 SQ8 加速计算，IVF_SQ8 实现了快速搜索时间和内存效率。
建立索引
要在 Milvus 中的向量场上建立
IVF_SQ8
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
"IVF_SQ8"
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
# Number of clusters to create using the k-means algorithm during index building
}
# Index building params
)
在此配置中
index_type
:要建立的索引类型。在本例中，将值设为
IVF_SQ8
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
:在索引构建过程中使用 k-means 算法创建的簇数。
要了解
IVF_SQ8
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
8
,
# Number of clusters to search for candidates
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
nprobe
:搜索候选对象的簇数。
要了解
IVF_SQ8
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