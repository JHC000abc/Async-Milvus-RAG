IVF_RABITQ
Compatible with Milvus 2.6.x
IVF_RABITQ
索引是一种
基于二进制量化的
索引算法，可将 FP32 向量量化为二进制表示。该索引具有出色的存储效率，压缩比为 1 比 32，同时保持相对较高的召回率。在内存受限的情况下，该索引可替代
IVF_SQ8
和
IVF_FLAT
。
概览
IVF_RABITQ
是
反转文件与 RaBitQ 量化的缩写
，它结合了高效向量搜索和存储的两种强大技术。
反转文件
反转文件（IVF）
使用
k-means 聚类
将向量空间组织成易于管理的区域。每个聚类都有一个中心点，作为该聚类内向量的参考点。这种聚类方法允许算法在查询处理过程中只关注最相关的聚类，从而减少了搜索空间。
要了解有关 IVF 技术细节的更多信息，请参阅
IVF_FLAT
。
RaBitQ
RaBitQ
是一种具有理论保证的最先进的二进制量化方法，由高建阳和龙成的研究论文《RaBitQ: Quantizing High-Dimensional Vectors with a Theoretical Error Bound for Approximate Nearest Neighbor Search》介绍。
RaBitQ 引入了几个创新概念：
角度信息编码
：与传统的空间编码不同，RaBitQ 通过向量归一化对角度信息进行编码。在 IVF_RABITQ 中，数据向量根据其最近的 IVF 中心点进行归一化，从而提高了量化过程的精度。
理论基础
：核心距离近似公式为
∥
o
r
−
q
r
∥
2
≈
∥
o
r
−
c
o
∥
2
+
∥
q
r
−
c
o
∥
2
−
2
⋅
C
(
o
r
,
c
o
)
⋅
⟨
o
~
,
q
r
−
c
o
⟩
+
C
1
(
o
r
,
c
o
)
\lVert \mathbf{o_r} - \mathbf{q_r} \rVert^2 \approx \lVert \mathbf{o_r} - \mathbf{c_o} \rVert^2 + \lVert \mathbf{q_r} - \mathbf{c_o} \rVert^2 - 2 \cdot C(\mathbf{o_r}, \mathbf{c_o}) \cdot \langle \tilde{\mathbf{o}}, \mathbf{q_r} - \mathbf{c_o} \rangle + C_1(\mathbf{o_r}, \mathbf{c_o})
∥
o
r
−
q
r
∥
2
≈
∥
o
r
−
c
o
∥
2
+
∥
q
r
−
c
o
∥
2
−
2
⋅
C
(
o
r
,
c
o
)
⋅
⟨
o
~
,
q
r
−
c
o
⟩
+
C
1
(
o
r
,
c
o
)
其中
or\mathbf{o_r}
o
r
是数据集中的数据向量
qr\mathbf{q_r}
q
r
是一个查询向量
co\mathbf{c_o}
c
o
是
or\mathbf{o_r}
o
r 的最近 IVF 中心向量
C
(
or
,
co
)
C(\mathbf{o_r}, \mathbf{c_o})
C
(
o
r
,
c
o
) 和
C1
(
or
,
co
)
C_1(\mathbf{o_r}, \mathbf{c_o})
C
1
(o
r
,
c
o
) 是预先计算的常数
o~\tilde\{mathbf{o}}
o
~ 是存储在索引中的量化二进制向量
⟨o~
,
qr-co⟩\langle
\tilde{\mathbf{o}}, \mathbf{q_r} - \mathbf{c_o}\rangle
⟨
o
~
,
q
r
-
c
o
⟩
表示点积操作符
计算效率
：
o~\tilde{\mathbf{o}}
o
~ 的二进制性质使得距离计算速度极快，尤其受益于英特尔 Ice Lake+ 或 AMD Zen 4+ 处理器上带有专用
AVX-512 VPOPCNTDQ
指令的现代 CPU 架构。
算法增强
：RaBitQ 与
FastScan
方法
和
随机旋转
等成熟技术有效整合，提高了性能。
IVF + RaBitQ
IVF_RABITQ
索引将 IVF 的高效聚类与 RaBitQ 先进的二进制量化相结合：
粗过滤
：IVF 将向量空间划分为若干簇，通过聚焦于最相关的簇区域，大大缩小了搜索范围。
二进制量化
：在每个簇内，RaBitQ 将向量压缩为二进制表示，同时通过理论保证保留基本的距离关系。
可选细化
：启用后，索引会使用更高精度格式（SQ6、SQ8、FP16、BF16 或 FP32）存储额外的精炼数据，以提高召回率，但存储空间会增加。
Milvus 使用以下 FAISS 工厂字符串实现 IVF_RABITQ：
有细化
"RR({dim}),IVF{nlist},RaBitQ,Refine({refine_index})"
无细化
"RR({dim}),IVF{nlist},RaBitQ"
建立索引
要在 Milvus 中的向量场上建立
IVF_RABITQ
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
"IVF_RABITQ"
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
"refine"
:
True
,
# Enable refinement for higher recall
"refine_type"
:
"SQ8"
# Refinement data format
}
# Index building params
)
在此配置中
index_type
:要建立的索引类型。在本例中，将值设为
IVF_RABITQ
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
"nprobe"
:
128
,
# Number of clusters to search
"rbq_query_bits"
:
0
,
# Query vector quantization bits
"refine_k"
:
1
# Refinement magnification factor
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
IVF_RABITQ 索引严重依赖
popcount
硬件指令以获得最佳性能。英特尔 IceLake+ 或 AMD Zen 4+ 等现代 CPU 架构采用
AVX512VPOPCNTDQ
指令集，可显著提高 RaBitQ 操作的性能。
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
在索引创建过程中使用 k-means 算法创建的簇数。每个簇由一个中心点代表，存储一个向量列表。增加该参数可减少每个簇中的向量数量，从而创建更小、更集中的分区。
类型
：整数整数
范围
： [1, 65536[1, 65536]
默认值
：
128
nlist
值越大，通过创建更精细的簇来提高召回率，但会增加索引构建时间。请根据数据集大小和可用资源进行优化。大多数情况下，我们建议在此范围内设置值：[32, 4096].
RaBitQ
refine
启用细化过程并存储细化后的数据。
类型
：布尔布尔值
范围
：[
true
,
false
]
默认值
：
false
如果需要 0.9+ 的召回率，则设置为
true
。启用细化功能可提高准确性，但会增加存储需求和索引构建时间。
refine_type
定义启用
refine
时用于细化的数据表示。
类型
：字符串
范围
[
SQ6
,
SQ8
,
FP16
,
BF16
,
FP32
]
默认值
：无
所列值按召回率递增、QPS 递减和存储容量递增的顺序排列。建议将
SQ8
作为起点，在准确性和资源使用之间取得良好平衡。
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
IVF
nprobe
搜索候选集群的集群数。数值越大，搜索的簇数越多，通过扩大搜索范围提高召回率，但代价是查询延迟增加。
类型
：整数
范围
： [1, nlist[1，
nlist］
默认值
：
8
增加该值可提高召回率，但可能会减慢搜索速度。设置
nprobe
与
nlist
成比例，以平衡速度和准确性。在大多数情况下，我们建议您在此范围内设置一个值：[1，
nlist
]。
RaBitQ
rbq_query_bits
设置是否对查询向量进行额外的标量量化。如果设置为
0
，查询将不进行量化。如果设置为[1, 8]，则使用 n 位标量量化对查询进行预处理。
类型
：整数
范围
： [0, 8[0, 8]
默认值
：
0
默认值
0
可提供最大的召回率，但性能最慢。我们建议测试值
0
、
8
和
6
，因为它们的召回率相似，其中
6
的召回率最快。如果召回率要求较高，可使用较小的值。
refine_k
精炼过程使用更高质量的量化，从使用 IVF_RABITQ 选出的
refine_k
倍大的候选池中挑选所需的近邻数量。
类型
：浮点数
范围
： [1, float_max[1,
float_max
)
默认值
：
1
refine_k
值越高，QPS 越低，但召回率越高。从
1
开始，然后测试值
2
,
3
,
4
, 和
5
，为您的数据集找到 QPS 和召回率之间的最佳权衡。