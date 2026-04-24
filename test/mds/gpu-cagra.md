GPU_CAGRA
GPU_CAGRA
索引是为 GPU 优化的基于图的索引。与使用昂贵的训练级 GPU 相比，使用推理级 GPU 运行 Milvus GPU 版本可以更具成本效益。
建立索引
要在 Milvus 中的向量场上建立
GPU_CAGRA
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
"GPU_CAGRA"
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
"intermediate_graph_degree"
:
64
,
# Affects recall and build time by determining the graph’s degree before pruning
"graph_degree"
:
32
,
# Affets search performance and recall by setting the graph’s degree after pruning
"build_algo"
:
"IVF_PQ"
,
# Selects the graph generation algorithm before pruning
"cache_dataset_on_device"
:
"true"
,
# Decides whether to cache the original dataset in GPU memory
"adapt_for_cpu"
:
"false"
,
# Decides whether to use GPU for index-building and CPU for search
}
# Index building params
)
在此配置中
index_type
:要建立的索引类型。在本例中，将值设为
GPU_CAGRA
。
metric_type
:用于计算向量间距离的方法。有关详情，请参阅 "
度量类型
"。
params
:用于构建索引的其他配置选项。要了解
GPU_CAGRA
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
"itopk_size"
:
16
,
# Determines the size of intermediate results kept during the search
"search_width"
:
8
,
# Specifies the number of entry points into the CAGRA graph during the search
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
:在索引上搜索的其他配置选项。要了解
GPU_CAGRA
索引可用的更多搜索
参数
，请参阅
特定于索引的搜索参数
。
加载时启用 CPU 搜索
Compatible with Milvus 2.6.4+
要在加载时动态启用 CPU 搜索，请在
milvus.yaml
中编辑以下配置：
# milvus.yaml
knowhere:
GPU_CAGRA:
load:
adapt_for_cpu:
true
行为
当
load.adapt_for_cpu
设置为
true
时，Milvus 会在加载时将
GPU_CAGRA
索引转换为 CPU 可执行格式（类似 HNSW）。
随后的搜索操作将在 CPU 上执行，即使索引最初是为 GPU 构建的。
如果省略或为假，索引将保留在 GPU 上，搜索也在 GPU 上运行。
在混合或对成本敏感的环境中，GPU 资源被保留用于索引构建，但搜索在 CPU 上运行，此时可使用负载时 CPU 适应。
索引参数
本节概述了用于构建索引和在索引上执行搜索的参数。
索引构建参数
下表列出了
建立索引
时可在
params
中配置的参数。
参数
默认值
默认值
intermediate_graph_degree
通过在剪枝前确定图的度数来影响召回率和建立时间。推荐值为
32
或
64
。
128
graph_degree
通过设置剪枝后图形的度数来影响搜索性能和召回率。这两个度数之间的差值越大，构建时间就越长。其值必须小于
intermediate_graph_degree
的值。
64
build_algo
选择剪枝前的图生成算法。可能的值
IVF_PQ
:提供更高的质量，但构建时间较慢。
NN_DESCENT
:提供更快的构建速度，但可能会降低召回率。
IVF_PQ
cache_dataset_on_device
决定是否在 GPU 内存中缓存原始数据集。可能的值
"true"
:缓存原始数据集，通过完善搜索结果来提高召回率。
"false"
:不缓存原始数据集，以节省 GPU 内存。
"false"
adapt_for_cpu
决定是否使用 GPU 建立索引和使用 CPU 进行搜索。
将该参数设置为
"true"
时，搜索请求中必须包含
ef
参数。
"false"
特定于索引的搜索参数
下表列出了
在索引上搜索
时可在
search_params.params
中配置的参数。
参数
默认值
默认值
itopk_size
决定搜索过程中保留的中间结果的大小。较大的值可能会提高召回率，但会降低搜索性能。它至少应等于最终的 top-k（极限）值，通常是 2 的幂次（例如 16、32、64、128）。
空
search_width
指定搜索过程中进入 CAGRA 图的入口点数量。增加该值可以提高召回率，但可能会影响搜索性能（如 1、2、4、8、16、32）。
空
min_iterations
/
max_iterations
控制搜索迭代过程。默认设置为
0
，CAGRA 会根据
itopk_size
和
search_width
自动确定迭代次数。手动调整这些值有助于平衡性能和准确性。
0
team_size
指定用于在 GPU 上计算度量距离的 CUDA 线程数。常用值是 2 的幂次，最高可达 32（例如 2、4、8、16、32）。它对搜索性能影响不大。默认值为
0
，Milvus 会根据向量维度自动选择
team_size
。
0
ef
指定查询时间/准确性的权衡。
ef
值越高，搜索越准确，但速度越慢。
如果在建立索引时将
adapt_for_cpu
设置为
true
，则必须使用此参数。
[top_k, int_max]