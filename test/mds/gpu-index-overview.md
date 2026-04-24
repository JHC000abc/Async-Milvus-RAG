GPU 索引概述
在 Milvus 中建立一个支持 GPU 的索引，可以显著提高高吞吐量和高调用情况下的搜索性能。
下图比较了不同索引配置、硬件设置、向量数据集（Cohere 和 OpenAI）以及搜索批量大小的查询吞吐量（每秒查询次数），显示
GPU_CAGRA
始终优于其他方法。
GPU 索引性能
为 Milvus 配置 GPU 内存池
Milvus 支持全局 GPU 内存池，并在
Milvus 配置文件
中提供了两个配置参数：
initMemSize
和
maxMemSize
。
gpu:
initMemSize:
0
# set the initial memory pool size.
maxMemSize:
0
# sets the maximum memory usage limit. When the memory usage exceeds initMemSize, Milvus will attempt to expand the memory pool.
默认情况下，
initMemSize
通常是 Milvus 启动时 GPU 内存的一半，而
maxMemSize
默认为整个 GPU 内存。GPU 内存池大小初始设置为
initMemSize
，并会根据需要自动扩展到
maxMemSize
。
指定启用 GPU 的索引时，Milvus 会在搜索前将目标 Collections 数据加载到 GPU 内存中，因此
maxMemSize
必须至少是数据大小。
限制
对于
GPU_IVF_FLAT
，
limit
的最大值为 1,024。
对于
GPU_IVF_PQ
和
GPU_CAGRA
，
limit
的最大值为 1,024。
虽然
GPU_BRUTE_FORCE
没有设置
limit
，但建议不要超过 4,096 以避免潜在的性能问题。
目前，GPU 索引不支持
COSINE
距离。如果需要使用
COSINE
距离，应首先对数据进行归一化处理，然后使用内积 (IP) 距离作为替代。
GPU 索引不完全支持加载 OOM 保护，过多的数据可能会导致 QueryNode 崩溃。
GPU 索引不支持
范围
搜索和
分组搜索
等搜索功能。
支持的 GPU 索引类型
下表列出了 Milvus 支持的 GPU 索引类型。
索引类型
说明
内存使用量
GPU_CAGRA
与使用昂贵的训练级 GPU 相比，使用推理级 GPU 运行 Milvus GPU 版本更具成本效益。
内存使用量约为原始向量数据的 1.8 倍。
GPU_IVF_FLAT
GPU_IVF_FLAT 是最基本的 IVF 索引，每个单元中存储的编码数据与原始数据一致。在进行搜索时，请注意针对 GPU_IVF_FLAT 索引 Collections 的任何搜索，都可以将 top-k (
limit
) 设置为最多 256。
需要与原始数据大小相等的内存。
GPU_IVF_PQ
GPU_IVF_PQ 在量化向量的乘积之前执行 IVF 索引聚类。在进行搜索时，请注意可以将针对 GPU_IVF_FLAT 索引 Collections 的任何搜索的 top-k (
limit
) 设置为最高 8,192。
利用较小的内存占用，这取决于压缩参数的设置。
GPU_BRUTE_FORCE
GPU_BRUTE_FORCE 专为对召回率要求极高的情况定制，通过将每个查询与数据集中的所有向量进行比较，保证召回率为 1。它只需要度量类型 (
metric_type
) 和 top-k (
limit
) 作为索引构建和搜索参数。
所需的内存与原始数据的大小相等。
为 GPU 内存控制配置 Milvus 设置
Milvus 使用全局图形内存池分配 GPU 内存。它支持
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
在 Milvus 2.4.1 之前，Milvus 使用统一的 GPU 内存池。对于 2.4.1 之前的版本，建议将这两个值都设为 0。
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
要了解如何建立 GPU 索引，请参阅每种索引类型的具体指南。
常见问题
何时适合使用 GPU 索引？
GPU 索引尤其适用于需要高吞吐量或高召回率的情况。例如，在处理大批量数据时，GPU 索引的吞吐量可比 CPU 索引高出 100 倍之多。在批量较小的情况下，GPU 索引在性能上仍明显优于 CPU 索引。此外，如果需要快速插入数据，采用 GPU 可以大大加快索引的建立过程。
GPU_CAGRA、GPU_IVF_PQ、GPU_IVF_FLAT 和 GPU_BRUTE_FORCE 等 GPU 索引最适合哪些应用场景？
GPU_CAGRA
GPU_IVF_FLAT、GPU_BRUTE_FORCE 和 GPU_CAGRA 索引非常适合需要增强性能的应用场景，尽管代价是消耗更多内存。对于优先考虑节省内存的环境，
GPU_IVF_PQ
索引可以帮助最大限度地减少存储需求，不过这也会带来较高的精度损失。
GPU_IVF_FLAT
索引是一个平衡的选择，在性能和内存使用之间提供了一个折中方案。最后，
GPU_BRUTE_FORCE
索引专为穷举搜索操作而设计，通过执行遍历搜索可保证召回率为 1。