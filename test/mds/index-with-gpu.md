使用 GPU 建立索引
本指南概述了在 Milvus 中建立支持 GPU 的索引的步骤，这可以显著提高高吞吐量和高调用场景中的搜索性能。有关 Milvus 支持的 GPU 索引类型的详细信息，请参阅
GPU 索引
。
此页面已被弃用。有关最新实现，请参阅
GPU 索引概述
为 GPU 内存控制配置 Milvus 设置
Milvus 使用全局图形内存池分配 GPU 内存。
它支持
Milvus 配置文件
中的两个参数
initMemSize
和
maxMemSize
。内存池大小初始设置为
initMemSize
，超过此限制后将自动扩展至
maxMemSize
。
Milvus 启动时，默认
initMemSize
为可用 GPU 内存的 1/2，默认
maxMemSize
等于所有可用 GPU 内存。
在 Milvus 2.4.1（包括 2.4.1 版）之前，Milvus 使用统一的 GPU 内存池。对于 2.4.1 之前的版本（包括 2.4.1 版），建议将这两个值都设为 0。
gpu:
initMemSize:
0
#set the initial memory pool size.
maxMemSize:
0
#maxMemSize sets the maximum memory usage limit. When the memory usage exceed initMemSize, Milvus will attempt to expand the memory pool.
从 Milvus 2.4.1 起，GPU 内存池仅用于搜索期间的临时 GPU 数据。因此，建议将其设置为 2048 和 4096。
gpu:
initMemSize:
2048
#set the initial memory pool size.
maxMemSize:
4096
#maxMemSize sets the maximum memory usage limit. When the memory usage exceed initMemSize, Milvus will attempt to expand the memory pool.
建立索引
以下示例演示了如何建立不同类型的 GPU 索引。
准备索引参数
设置 GPU 索引参数时，请定义
index_type
、
metric_type
和
params
：
index_type
（字符串
）：用于加速向量搜索的索引类型。有效选项包括
GPU_CAGRA
、
GPU_IVF_FLAT
、
GPU_IVF_PQ
和
GPU_BRUTE_FORCE
。
metric_type
（字符串
）：用于衡量向量相似性的度量类型。有效选项为
IP
和
L2
。
params
（dict
）：特定于索引
的
构建
参数
：特定于索引的构建参数。该参数的有效选项取决于索引类型。
以下是不同索引类型的配置示例：
GPU_CAGRA
索引
index_params = {
"metric_type"
:
"L2"
,
"index_type"
:
"GPU_CAGRA"
,
"params"
: {
'intermediate_graph_degree'
:
64
,
'graph_degree'
:
32
}
}
参数
的可能选项包括
intermediate_graph_degree
(int
)：通过在剪枝之前确定图的度数来影响召回率和构建时间。推荐值为
32
或
64
。
graph_degree
（int
）：通过设置剪枝后图形的度数来影响搜索性能和召回率。通常，它是
中间图度
的一半。这两个度数之间的差值越大，构建时间就越长。它的值必须小于
intermediate_graph_degree
的值。
build_algo
（字符串
）：选择剪枝前的图形生成算法。可能的选项：
IVF_PQ
：提供更高的质量，但构建时间较慢。
NN_DESCENT
：提供更快的生成速度，但可能会降低召回率。
cache_dataset_on_device
（字符串
，
"true"
|
"false"）
：决定是否在 GPU 内存中缓存原始数据集。将其设置为
"true "
可通过完善搜索结果提高召回率，而将其设置为
"false "
则可节省 GPU 内存。
GPU_IVF_FLAT
或
GPU_IVF_PQ
索引
index_params = {
"metric_type"
:
"L2"
,
"index_type"
:
"GPU_IVF_FLAT"
,
# Or GPU_IVF_PQ
"params"
: {
"nlist"
:
1024
}
}
参数
选项与
IVF_FLAT
和
IVF_PQ
中使用的选项相同。
GPU_BRUTE_FORCE
索引
index_params = {
'index_type'
:
'GPU_BRUTE_FORCE'
,
'metric_type'
:
'L2'
,
'params'
: {}
}
不需要额外的
参数
配置。
构建索引
在
index_params
中配置索引参数后，调用
create_index()
方法来构建索引。
# Get an existing collection
collection = Collection(
"YOUR_COLLECTION_NAME"
)

collection.create_index(
    field_name=
"vector"
,
# Name of the vector field on which an index is built
index_params=index_params
)
搜索
建立 GPU 索引后，下一步是在进行搜索前准备搜索参数。
准备搜索参数
以下是不同索引类型的配置示例：
GPU_BRUTE_FORCE
索引
search_params = {
"metric_type"
:
"L2"
,
"params"
: {}
}
不需要额外的
参数
配置。
GPU_CAGRA
索引
search_params = {
"metric_type"
:
"L2"
,
"params"
: {
"itopk_size"
:
128
,
"search_width"
:
4
,
"min_iterations"
:
0
,
"max_iterations"
:
0
,
"team_size"
:
0
}
}
主要搜索参数包括
itopk_size
：决定搜索过程中保留的中间结果的大小。较大的值可能会提高召回率，但会降低搜索性能。它至少应等于最终的 top-k
（极限
）值，通常是 2 的幂次（如 16、32、64、128）。
search_width
：指定搜索过程中进入 CAGRA 图的入口点数量。增加该值可以提高召回率，但可能会影响搜索性能。
min_iterations
/
max
_
iterations
：这些参数控制搜索迭代过程。默认情况下，它们被设置为
0
，CAGRA 会根据
itopk_size
和
search_width
自动确定迭代次数。手动调整这些值有助于平衡性能和准确性。
team_size
（
团队规模
）：指定用于在 GPU 上计算度量距离的 CUDA 线程数。常用值为 2 的幂次，最高为 32（例如 2、4、8、16、32）。它对搜索性能影响不大。默认值为
0
，Milvus 会根据向量维度自动选择
team_size
。
GPU_IVF_FLAT
或
GPU_IVF_PQ
索引
search_params = {
"metric_type"
:
"L2"
,
"params"
: {
"nprobe"
:
10
}
}
这两种索引类型的搜索参数与
IVF_FLAT
和
IVF_PQ
中使用的参数类似。更多信息，请参阅
进行向量相似性搜索
。
进行搜索
使用
search()
方法对 GPU 索引执行向量相似性搜索。
# Load data into memory
collection.load()

collection.search(
    data=[[query_vector]],
# Your query vector
anns_field=
"vector"
,
# Name of the vector field
param=search_params,
    limit=
100
# Number of the results to return
)
限制
使用 GPU 索引时，请注意某些限制：
对于
GPU_IVF_FLAT
，
限制
的最大值为 1024。
对于
GPU_IVF_PQ
和
GPU_CAGRA
，
limit
的最大值为 1024。
虽然
GPU_BRUTE_FORCE
没有设定
限制
，但建议不要超过 4096，以避免潜在的性能问题。
目前，GPU 索引不支持 COSINE 距离。如果需要使用 COSINE 距离，应首先对数据进行归一化处理，然后使用内积（IP）距离作为替代。
GPU 索引不完全支持加载 OOM 保护，过多的数据可能会导致 QueryNode 崩溃。
GPU 索引不支持
范围
搜索和
分组搜索
等搜索功能。
常见问题
什么情况下适合使用 GPU 索引？
GPU 索引尤其适用于需要高吞吐量或高召回率的情况。例如，在处理大批量数据时，GPU 索引的吞吐量可比 CPU 索引高出 100 倍之多。在批量较小的情况下，GPU 索引在性能上仍明显优于 CPU 索引。此外，如果需要快速插入数据，采用 GPU 可以大大加快索引的建立过程。
CAGRA、GPU_IVF_PQ、GPU_IVF_FLAT 和 GPU_BRUTE_FORCE 等 GPU 索引最适合哪些应用场景？
CAGRA 索引非常适合需要增强性能的应用场景，尽管代价是消耗更多内存。对于优先考虑节省内存的环境，
GPU_IVF_PQ
索引可以帮助最大限度地减少存储需求，不过这也会带来较高的精度损失。
GPU_IVF_FLAT
索引是一个平衡的选择，它在性能和内存使用之间提供了一个折中方案。最后，
GPU_BRUTE_FORCE
索引专为穷举搜索操作而设计，通过执行遍历搜索保证召回率为 1。