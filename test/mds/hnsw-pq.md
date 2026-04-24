HNSW_PQ
HNSW_PQ
利用分层可导航小世界（HNSW）图与乘积量化（PQ），创建了一种先进的向量索引方法，提供了可控的大小与准确性权衡。与
HNSW_SQ
相比，尽管查询处理速度较低，索引构建时间较长，但在相同压缩级别下，该索引类型的召回率更高。
概览
HNSW_PQ 结合了两种索引技术：
HNSW
用于基于图的快速导航，
PQ
用于高效向量压缩。
HNSW
HNSW 构建了一个多层图，其中每个节点都对应数据集中的一个向量。在该图中，节点根据其相似性进行连接，从而实现在数据空间中的快速遍历。分层结构允许搜索算法缩小候选邻域的范围，从而大大加快了高维空间的搜索过程。
更多信息，请参阅
HNSW
。
PQ
PQ 是一种向量压缩技术，可将高维向量分解成更小的子向量，然后对子向量进行量化和压缩。这种压缩技术大大降低了内存需求，并加快了距离计算速度。
更多信息，请参阅
IVF_PQ
。
HNSW + PQ
HNSW_PQ 结合了 HNSW 和 PQ 的优势，实现了高效的近似近邻搜索。它使用 PQ 压缩数据（从而减少内存使用），然后在这些压缩向量上构建 HNSW 图，以实现快速候选检索。在搜索过程中，该算法可以选择使用更高精度的数据来完善候选结果，以提高准确性。以下是该过程的工作原理：
数据压缩
：PQ 会将每个向量分割成多个子向量，并使用中心编码本对其进行量化，中心编码本由
m
（子向量数）和
nbits
（每个子向量的比特数）等参数控制。
图形构建
：压缩后的向量将用于构建 HNSW 图。由于向量是以压缩的形式存储的，因此生成的图通常更小，所需的内存更少，遍历速度更快，从而大大加快了候选检索步骤。
候选检索
：当执行查询时，算法会使用 HNSW 图中的压缩数据来有效地识别候选邻居池。这种基于图的查找大大减少了必须考虑的向量数量，与暴力搜索相比，提高了查询延迟。
(可选）结果完善
：可根据以下参数对初始候选结果进行改进，以提高准确性：
refine
:控制是否激活该细化步骤。当设置为
true
时，系统会使用更高精度或非压缩表示法重新计算距离。
refine_type
:指定细化过程中使用的数据精度级别（如 SQ6、SQ8、BF16）。选择更高精度的数据，如
FP32
，可以得到更精确的结果，但需要更多内存。这必须比原始压缩数据集的精度高
sq_type
。
refine_k
:放大系数。例如，如果您的前
k
值是 100，而
refine_k
是 2，系统就会对前 200 个候选项重新排序，并返回最好的 100 个，从而提高整体准确性。
有关参数和有效值的完整列表，请参阅
索引参数
。
建立索引
要在 Milvus 中的向量场上建立
HNSW_PQ
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
"HNSW_PQ"
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
"M"
:
30
,
# Maximum number of neighbors each node can connect to in the graph
"efConstruction"
:
360
,
# Number of candidate neighbors considered for connection during index construction
"m"
:
384
,
"nbits"
:
8
,
"refine"
: true,
# Whether to enable the refinement step
"refine_type"
:
"SQ8"
# Precision level of data used for refinement
}
# Index building params
)
在此配置中
index_type
:要建立的索引类型。在本例中，将值设为
HNSW_PQ
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
:用于构建索引的附加配置选项。详情请参阅
索引构建参数
。
配置好索引参数后，可直接使用
create_index()
方法或在
create_collection
方法中传递索引参数来创建索引。详情请参阅
创建 Collections
。
在索引上搜索
建立索引并插入实体后，就可以在索引上执行相似性搜索。
search_params = {
"params"
: {
"ef"
:
10
,
# Parameter controlling query time/accuracy trade-off
"refine_k"
:
1
# The magnification factor
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
:在索引上搜索的其他配置选项。有关详情，请参阅
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
HNSW
M
图中每个节点可拥有的最大连接数（或边），包括出站边和入站边。 该参数直接影响索引构建和搜索。
类型
： 整数整数
范围
：[2, 2048]
默认值
：
30
（每个节点最多有 30 条出边和 30 条入边）
较大的
M
通常会
提高准确率
，但会
增加内存开销
，并
减慢索引构建和搜索速度
。对于高维度数据集或高召回率至关重要时，可考虑增加
M
。
当内存使用和搜索速度是首要考虑因素时，可考虑降低
M
。
在大多数情况下，我们建议您在此范围内设置一个值：[5, 100].
efConstruction
索引构建过程中考虑连接的候选邻居数量。 每个新元素都会评估更多的候选邻居，但实际建立的最大连接数仍受
M
限制。
类型
： 整数整数
范围
：[1，
int_max］
默认值
：
360
efConstruction
越高，
索引
越
准确
，因为会探索更多潜在连接。考虑增加
efConstruction
以提高准确性
，
尤其是在索引时间不太重要的情况下。
在资源紧张的情况下，可考虑降低
efConstruction
，以加快索引构建速度。
在大多数情况下，我们建议在此范围内设置一个值：[50, 500].
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
refine
布尔标志，用于控制搜索过程中是否应用细化步骤。细化包括通过计算查询向量和候选向量之间的精确距离，对初始结果进行重新排序。
类型
：布尔布尔
范围
：[
true
,
false
]
默认值
：
false
如果需要高精确度，并且可以忍受稍慢的搜索时间，则设置为
true
。如果速度是首要考虑因素，并且可以接受在精确度上略有妥协，则使用
false
。
refine_type
确定细化过程中使用的数据精度。 该精度必须高于压缩向量的精度（由
m
和
nbits
参数设置）。
类型
： 字符串字符串
范围
：[
SQ6
,
SQ8
,
BF16
,
FP16
,
FP32
]
默认值
：无
使用
FP32
可获得最高精度，但内存成本较高；使用
SQ6
/
SQ8
可获得更好的压缩效果。
BF16
和
FP16
提供了一个平衡的替代方案。
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
HNSW
ef
控制近邻检索时的搜索范围。它决定访问多少节点并将其评估为潜在近邻。 
 该参数只影响搜索过程，并且只适用于图形的底层。
类型
： 整数整数
范围
：[1，
int_max］
默认值
：
limit
（返回的前 K 个近邻）
ef
越大，通常
搜索精度越高
，因为会考虑更多的潜在近邻。当实现高召回率至关重要，而
搜索
速度则不那么重要时，可考虑增加
ef
。
考虑降低
ef
以优先提高搜索速度，尤其是在可以接受稍微降低准确率的情况下。
在大多数情况下，我们建议您在此范围内设置一个值：[K，10K]。
PQ
refine_k
放大系数，用于控制相对于请求的前 K 个结果，在细化（重新排序）阶段检查多少额外的候选结果。
类型
： 浮动浮动
范围
：[1,
float_max
)
默认值
：1
refine_k
的值越大，召回率和准确率越高，但也会增加搜索时间和资源占用。值为 1 意味着细化过程只考虑最初的前 K 个结果。