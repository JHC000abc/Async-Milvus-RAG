HNSW_SQ
HNSW_SQ
将层次导航小世界（HNSW）图与标量量化（SQ）相结合，创建了一种先进的向量索引方法，提供了可控的大小与精度权衡。与标准
HNSW
相比，这种索引类型保持了较高的查询处理速度，同时索引构建时间略有增加。
概览
HNSW_SQ 结合了两种索引技术：
HNSW
用于基于图的快速导航，
SQ
用于高效的向量压缩。
HNSW
HNSW 构建了一个多层图，其中每个节点都对应数据集中的一个向量。在这个图中，节点根据其相似性进行连接，从而实现数据空间的快速遍历。分层结构允许搜索算法缩小候选邻域的范围，从而大大加快了高维空间的搜索过程。
更多信息，请参阅
HNSW
。
SQ
SQ 是一种用较少比特表示向量的压缩方法。例如
SQ8
使用 8 位，将数值映射为 256 个级别。  更多信息，请参阅
IVF_SQ8
。
SQ6
使用 6 位来表示每个浮点数值，从而产生 64 个离散级。
Hnsw Sq
这种精度的降低大大减少了内存占用，加快了计算速度，同时保留了数据的基本结构。
SQ4U
Compatible with Milvus 2.6.8+
针对要求极高查询速度和最小内存占用的应用场景，Milvus 推出了
SQ4U
，一种 4 位统一标量量化。这是一种积极的标量量化形式，可将每个维度的浮点数值压缩为
4 位
无符号整数。
SQ4U 中的 "U "代表 Uniform（统一）。非统一标量量化通常会为每个维度独立计算最小值和最大值（按维度量化），而 SQ4U 则不同，它执行的是
全局统一量化
策略：
全局统计
：系统计算适用于向量
所有维度
（或整个向量段）的
单一
最小值
vmin
和
单一
值范围
vdiff
。
统一映射
：全局值范围分为 16 个相等的区间。向量中的每个浮点数值，无论属于哪个维度，都使用这些共享参数映射为 4 位整数（0-15）。
性能优势
8 倍压缩比：
与
FP32
相比，压缩率提高了 8 倍，与
SQ8
相比，压缩率提高了 2 倍，大大降低了内存带宽压力--内存带宽往往是向量搜索的瓶颈。
SIMD 优化：
紧凑的结构允许现代 CPU（AVX2/AVX-512）在每个周期内处理更多的维数。最重要的是，全局参数的使用消除了在距离计算过程中加载不同标度/偏移值的需要，使指令流水线保持完全饱和。
高速缓存效率：
较小的向量尺寸意味着更多的数据可以放入 CPU 高速缓存，从而减少内存访问造成的延迟。
由于全局参数共享，SQ4U 在规范化数据或各维度值分布一致的数据集上表现最佳。
HNSW + SQ
HNSW_SQ 结合了 HNSW 和 SQ 的优势，实现了高效的近似近邻搜索。以下是该过程的工作原理：
数据压缩：
SQ 使用
sq_type
（例如 SQ6 或 SQ8）压缩向量，从而减少内存使用量。这种压缩可能会降低精度，但却能让系统处理更大的数据集。
图形构建：
压缩向量用于构建 HNSW 图形。由于数据经过压缩，生成的图更小，搜索速度更快。
候选检索：
当提供查询向量时，算法会使用压缩数据从 HNSW 图中快速识别出候选邻域池。
(可选）结果完善：
可根据以下参数对初始候选结果进行改进，以提高准确性：
refine
:控制是否激活该细化步骤。当设置为
true
时，系统会使用更高精度或未压缩的表示法重新计算距离。
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
HNSW_SQ
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
"HNSW_SQ"
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
64
,
# Maximum number of neighbors each node can connect to in the graph
"efConstruction"
:
100
,
# Number of candidate neighbors considered for connection during index construction
"sq_type"
:
"SQ6"
,
# Scalar quantizer type
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
HNSW_SQ
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
图中每个节点可拥有的最大连接数（或边），包括出站边和入站边。
该参数直接影响索引构建和搜索。
类型
：整数
范围
： [2, 2048[2, 2048]
默认值
：
30
（每个节点最多 30 条出边和 30 条入边）
较大的
M
通常会
提高准确率
，但会
增加内存开销
，并
减慢索引构建和搜索速度
。
对于高维度数据集或高召回率至关重要时，可考虑提高
M
。
当内存使用和搜索速度是首要考虑因素时，可考虑降低
M
。
在大多数情况下，我们建议您在此范围内设置一个值：[5, 100].
efConstruction
索引构建过程中考虑连接的候选邻居数量。
每个新元素都会评估一个更大的候选池，但实际建立的最大连接数仍受
M
限制。
类型
：整数
范围
： [1, int_max[1，
int_max］
默认值
：
360
efConstruction
越高，
索引
越
准确
，因为会探索更多潜在连接。不过，这也会导致建立
索引的时间延长和内存使用量增加
。
考虑增加
efConstruction
以提高准确性，尤其是在索引时间不太重要的情况下。
在资源紧张的情况下，可考虑降低
efConstruction
，以加快索引构建速度。
在大多数情况下，我们建议在此范围内设置一个值：[50, 500].
SQ
sq_type
指定用于压缩向量的标量量化方法。每个选项都在压缩和准确性之间提供了不同的平衡：
SQ4U
:使用 4 位均匀量化对向量进行编码。该模式提供最高的速度和压缩率。
SQ6
:使用 6 位整数编码向量。
SQ8
:使用 8 位整数编码向量。
BF16
:使用 Bfloat16 格式。
FP16
:使用标准 16 位浮点格式。
类型
：字符串
范围
[
SQ4U
,
SQ6
,
SQ8
,
BF16
,
FP16
]
默认值
：
SQ8
选择
sq_type
取决于具体应用的需求。选择
SQ4U
是为了最大限度地提高速度和内存效率。
SQ6
或
SQ8
可能适合平衡性能。另一方面，如果精度是最重要的，
BF16
或
FP16
可能是首选。
refine
布尔标志，用于控制搜索过程中是否应用细化步骤。细化包括通过计算查询向量和候选向量之间的精确距离对初始结果进行重新排序。
类型
：布尔布尔
范围
[
true
,
false
]
默认值
：
false
如果需要高精确度，并且可以忍受稍慢的搜索时间，则设置为
true
。如果速度是首要考虑因素，并且可以接受在精确度上稍有妥协，则使用
false
。
refine_type
决定用于细化的数据精度。
该精度必须高于压缩向量的精度（由
sq_type
设置），这会影响重新排序向量的精度及其内存占用。
类型
： 字符串字符串
范围
:[
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
：整数
范围
： [1, int_max[1，
int_max］
默认值
：
limit
（返回的前 K 个近邻）
ef
越大，
搜索精度越高
，因为会考虑更多的潜在近邻。不过，这也会
增加搜索时间
。
如果实现高召回率至关重要，而搜索速度则不那么重要，则可考虑提高
ef
。
考虑降低
ef
以优先提高搜索速度，尤其是在可以接受稍微降低准确率的情况下。
在大多数情况下，我们建议您在此范围内设置一个值：[K，10K]。
SQ
refine_k
放大系数，用于控制相对于请求的前 K 个结果，在细化阶段检查多少额外的候选结果。
类型
：浮点数
范围
： [1, float_max[1,
float_max
)
默认值
：1
refine_k
的较高值可提高召回率和准确率，但也会增加搜索时间和资源占用。值为 1 意味着细化过程只考虑最初的前 K 个结果。