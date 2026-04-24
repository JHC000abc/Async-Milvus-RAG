GPU 索引
Milvus 支持各种 GPU 索引类型，以加快搜索性能和效率，尤其是在高吞吐量和高调用场景中。本主题概述了 Milvus 支持的 GPU 索引类型、适合的使用案例和性能特点。有关使用 GPU 建立索引的信息，请参阅《
使用 GPU 建立索引
》。
值得注意的是，与使用 CPU 索引相比，使用 GPU 索引并不一定能减少延迟。如果想充分发挥吞吐量，就需要极高的请求压力或大量的查询向量。
性能
Milvus 的 GPU 支持由 Nvidia
RAPIDS
团队贡献。以下是 Milvus 目前支持的 GPU 索引类型。
GPU_CAGRA
GPU_CAGRA 是为 GPU 优化的基于图的索引，与使用昂贵的训练级 GPU 相比，使用推理级 GPU 运行 Milvus GPU 版本可以获得更高的成本效益。
索引构建参数
参数
说明
默认值
intermediate_graph_degree
通过在剪枝之前确定图的度数来影响召回率和构建时间。推荐值为
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
选择剪枝前的图形生成算法。可能的值：
IVF_PQ
:提供更高的质量，但构建时间较慢。
NN_DESCENT
提供更快的生成速度，但召回率可能较低。
IVF_PQ
cache_dataset_on_device
决定是否在 GPU 内存中缓存原始数据集。可能的值
“true”
:缓存原始数据集，通过细化搜索结果提高召回率。
“false”
不缓存原始数据集，以节省 GPU 内存。
“false”
adapt_for_cpu
决定是否使用 GPU 建立索引和使用 CPU 进行搜索。
将该参数设置为
true
时，搜索请求中必须包含
ef
参数。
“false”
搜索参数
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
搜索限制
参数
范围
limit
（top-K）
<= 1024
limit
(top-K)
<=max((
itopk_size
+ 31)// 32,
search_width
)* 32
GPU_IVF_FLAT
与
IVF_FLAT
类似，GPU_IVF_
FLAT
也是将向量数据划分为
nlist
聚类单元，然后比较目标输入向量与每个聚类中心之间的距离。根据系统设置查询的簇数（
nprobe
），相似性搜索结果仅根据目标输入与最相似簇中向量的比较结果返回--大大缩短了查询时间。
通过调整
nprobe
，可以在特定情况下找到准确性和速度之间的理想平衡。
IVF_FLAT 性能测试
结果表明，随着目标输入向量数 (
nq
) 和要搜索的簇数 (
nprobe
) 的增加，查询时间也会急剧增加。
GPU_IVF_FLAT 是最基本的 IVF 索引，每个单元中存储的编码数据与原始数据一致。
在进行搜索时要注意，针对 GPU_IVF_FLAT 索引的 Collections 进行任何搜索时，都可以将 top-K 设置为最多 256。
索引建立参数
参数
说明
范围
默认值
nlist
群组单位数
[1, 65536]
128
cache_dataset_on_device
决定是否在 GPU 内存中缓存原始数据集。可能的值
“true”
:缓存原始数据集，通过细化搜索结果提高召回率。
“false”
：不缓存原始数据集，以节省 GPU 内存。
"true"
"flase"
"false"
搜索参数
普通搜索
参数
说明
范围
默认值
nprobe
要查询的单位数
[1，nlist］
8
搜索限制
参数
范围
limit
(top-K)
<=
2048
GPU_IVF_PQ
PQ
(乘积量化）将原始高维向量空间均匀分解为 低维向量空间的笛卡尔乘积，然后对分解后的低维向量空间进行量化。乘积量化不需要计算目标向量与所有单元中心的距离，而是能够计算目标向量与每个低维空间聚类中心的距离，大大降低了算法的时间复杂度和空间复杂度。
m
IVF_PQ 先进行 IVF 索引聚类，然后再对向量的乘积进行量化。其索引文件比 IVF_SQ8 更小，但在搜索向量时也会造成精度损失。
索引建立参数和搜索参数随 Milvus Distributed 分布而异。请先选择 Milvus Distributed。
在进行搜索时，请注意针对 GPU_IVF_FLAT 索引 Collections 的任何搜索都可以将 top-K 设置为 8192。
索引建立参数
参数
说明
范围
默认值
nlist
群组单位数
[1, 65536]
128
m
乘积量化因子数、
dim mod m or = 0
0
nbits
[可选项] 每个低维向量的存储位数。
[1, 16]
8
cache_dataset_on_device
决定是否在 GPU 内存中缓存原始数据集。可能的值：
“true”
:缓存原始数据集，通过细化搜索结果提高召回率。
“false”
不缓存原始数据集，以节省 GPU 内存。
"true"
"false"
"false"
搜索参数
普通搜索
参数
说明
范围
默认值
nprobe
要查询的单位数
[1，nlist］
8
搜索限制
参数
范围
limit
(top-K)
<=
1024
GPU_BRUTE_FORCE
GPU_BRUTE_FORCE 专为对召回率要求极高的情况定制，通过将每个查询与数据集中的所有向量进行比较，保证召回率为 1。它只需要度量类型 (
metric_type
) 和 top-k (
limit
) 作为索引构建和搜索参数。
对于 GPU_BRUTE_FORCE，不需要额外的索引建立参数或搜索参数。
结论
目前，Milvus 会将所有索引加载到 GPU 内存中，以便进行高效的搜索操作。可加载的数据量取决于 GPU 内存的大小：
GPU_CAGRA
：内存使用量约为原始向量数据的 1.8 倍。
GPU_IVF_FLAT
和
GPU_BRUTE_FORCE
：需要与原始数据大小相等的内存。
GPU_IVF_PQ
：占用内存较少，具体取决于压缩参数设置。