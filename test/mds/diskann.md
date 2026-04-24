DISKANN
在大规模场景中，数据集可能包括数十亿甚至数万亿向量，标准的内存索引方法（如
HNSW
、
IVF_FLAT
）往往会因内存限制而跟不上步伐。
DISKANN
提供了一种基于磁盘的方法，可以在数据集大小超过可用 RAM 时保持较高的搜索精度和速度，从而应对这些挑战。
概述
DISKANN
结合了高效向量搜索的两项关键技术：
Vamana 图形
- 一种
基于磁盘的
图形
索引，可将数据点（或向量）连接起来，以便在搜索过程中高效导航。
乘积量化 (PQ)
- 一种
内存
压缩方法，可减小向量的大小，从而快速计算向量之间的近似距离。
索引构建
瓦马纳图
Vamana 图是 DISKANN 基于磁盘策略的核心。它可以处理非常大的数据集，因为在构建过程中或之后，它不需要完全驻留在内存中。
下图显示了 Vamana 图的构建过程。
Diskann
初始随机连接：
每个数据点（向量）在图中表示为一个节点。这些节点最初是随机连接的，形成一个密集的网络。通常情况下，一个节点开始时会有大约 500 条边（或连接），以实现广泛的连接。
细化以提高效率：
初始随机图需要经过优化过程，以提高搜索效率。这包括两个关键步骤：
修剪多余的边：
算法根据节点之间的距离丢弃不必要的连接。这一步优先处理质量较高的边。
max_degree
参数限制了每个节点的最大边数。
max_degree
越高，图的密度越大，有可能找到更多相关的邻居（召回率更高），但也会增加内存使用量和搜索时间。
添加战略捷径：
Vamana 引入了长距离边，将向量空间中相距甚远的数据点连接起来。这些捷径允许搜索在图中快速跳转，绕过中间节点，大大加快了导航速度。
search_list_size
参数决定了图细化过程的广度。较高的
search_list_size
可以在构建过程中扩展对邻接节点的搜索，从而提高最终准确性，但会增加索引构建时间。
要了解有关参数调整的更多信息，请参阅
DISKANN params
。
PQ
DISKANN 使用
PQ
将高维向量压缩成较小的表示
（PQ 代码
），并将其存储在内存中，以便快速计算近似距离。
pq_code_budget_gb_ratio
参数用于管理存储这些 PQ 代码的内存占用。它表示向量的总大小（千兆字节）与分配用于存储 PQ 代码的空间之间的比率。您可以通过以下公式计算实际的 PQ 代码预算（以千兆字节为单位）：
PQ Code Budget (GB) = vec_field_size_gb * pq_code_budget_gb_ratio
其中
vec_field_size_gb
是向量的总大小（千兆字节）。
pq_code_budget_gb_ratio
是用户定义的比率，表示为 PQ 代码保留的总数据大小的一部分。该参数允许在搜索精度和内存资源之间进行权衡。有关参数调整的更多信息，请参阅
DISKANN configs
。
有关底层 PQ 方法的技术细节，请参阅
IVF_PQ
。
搜索过程
建立索引（磁盘上的 Vamana 图和内存中的 PQ 代码）后，DISKANN 将执行 ANN 搜索，具体过程如下：
Diskann 2
查询和入口点：
提供一个查询向量以定位其最近的邻居。DISKANN 从 Vamana 图中选定的入口点开始，通常是数据集全球中心点附近的一个节点。全局中心点代表所有向量的平均值，这有助于最小化图中的遍历距离，从而找到所需的邻居。
邻居探索：
该算法从当前节点的边缘收集潜在的候选邻居（图中红色圆圈），利用内存中的 PQ 代码来近似这些候选邻居与查询向量之间的距离。这些潜在的候选邻居是通过 Vamana 图中的边直接连接到所选入口点的节点。
选择节点进行精确距离计算：
从近似结果中，选择最有希望的邻居（图中绿色圆圈）子集，使用它们未经压缩的原始向量进行精确距离评估。这需要从磁盘中读取数据，非常耗时。DISKANN 使用两个参数来控制精确度和速度之间的微妙平衡：
beam_width_ratio
:一个控制搜索广度的比率，它决定了有多少候选邻域会被并行选择以探索其邻域。
beam_width_ratio
越大，搜索范围越广，可能带来更高的精度，但也会增加计算成本和磁盘 I/O。波束宽度或选择的节点数由公式确定：
Beam width = Number of CPU cores * beam_width_ratio
.
search_cache_budget_gb_ratio
:为缓存频繁访问的磁盘数据而分配的内存比例。这种缓存有助于最大限度地减少磁盘 I/O，使重复搜索更快，因为数据已经在内存中。
要了解有关参数调整的更多信息，请参阅
DISKANN configs
。
迭代探索：
搜索会迭代完善候选集，反复执行近似评估（使用 PQ），然后进行精确检查（使用磁盘中的原始向量），直到找到足够数量的邻域。
在 Milvus 中启用 DISKANN
默认情况下，Milvus 会禁用
DISKANN
，以优先提高内存中索引的速度，以适应 RAM 中的数据集。不过，如果你正在处理海量数据集，或想利用
DISKANN
的可扩展性和固态硬盘优化，你可以轻松启用它。
下面介绍如何在 Milvus 中启用 DISKANN：
更新 Milvus 配置文件
找到 Milvus 配置文件
。
(有关查找该文件的详细信息，请参阅 Milvus 配置文档）。
找到
queryNode.enableDisk
参数，并将其值设为
true
：
queryNode:
enableDisk:
true
# Enables query nodes to load and search using the on-disk index
为 DISKANN 优化存储
为确保 DISKANN 的最佳性能，建议将 Milvus 数据存储在快速 NVMe SSD 上。下面介绍如何在 Milvus 单机和集群部署中做到这一点：
Milvus 单机版
将 Milvus 数据目录挂载到 Milvus 容器内的 NVMe 固态硬盘上。你可以在
docker-compose.yml
文件中或使用其他容器管理工具这样做。
例如，如果您的 NVMe SSD 挂载在
/mnt/nvme
上，您可以像这样更新
docker-compose.yml
的
volumes
部分：
volumes:
-
/mnt/nvme/volumes/milvus:/var/lib/milvus
Milvus 群集
在 QueryNode 和 IndexNode 容器中将 Milvus 数据目录挂载到 NVMe SSD 上。您可以通过容器协调设置来实现这一点。
通过将数据挂载到两种节点类型中的 NVMe SSD 上，可以确保搜索和索引操作的快速读写速度。
完成这些更改后，重启 Milvus 实例，使设置生效。现在，Milvus 将利用 DISKANN 处理大型数据集的能力，提供高效和可扩展的向量搜索。
配置 DISKANN
DISKANN 相关参数只能通过 Milvus 配置文件 (
milvus.yaml
) 进行配置：
# milvus.yaml
common:
DiskIndex:
MaxDegree:
56
# Maximum degree of the Vamana graph
SearchListSize:
100
# Size of the candidate list during building graph
PQCodeBudgetGBRatio:
0.125
# Size limit on the PQ code (compared with raw data)
SearchCacheBudgetGBRatio:
0.1
# Ratio of cached node numbers to raw data
BeamWidthRatio:
4
# Ratio between the maximum number of IO requests per search iteration and CPU number
有关参数描述的详细信息，请参阅
DISKANN params
。
DISKANN 参数
对 DISKANN 的参数进行微调，可让您根据特定的数据集和搜索工作量调整其行为，在速度、准确性和内存使用之间取得适当的平衡。
索引构建参数
这些参数会影响 DISKANN 索引的构建方式。调整这些参数会影响索引大小、构建时间和搜索质量。
下面列出的所有索引构建参数只能通过 Milvus 配置文件 (
milvus.yaml
) 进行配置。
参数
参数
值范围
调整建议
连接数
MaxDegree
控制每个数据点在 Vamana 图表中的最大连接（边）数。
类型
： 整数整数
范围
：[1, 512]
默认值
：
56
较高的值可创建更密集的图形，可能会提高召回率（找到更多相关结果），但也会增加内存使用量和构建时间。 
 在大多数情况下，我们建议您在此范围内设置值：[10, 100].
SearchListSize
在索引构建过程中，该参数定义了为每个节点搜索近邻时使用的候选池大小。对于添加到图中的每个节点，算法都会维护一个列表，其中包含迄今为止找到的
search_list_size
个最佳候选节点。当该列表无法再改进时，就会停止搜索邻居。从这个最终候选库中，
max_degree
，选出最靠前的节点组成最终的边。
类型
： 整数整数
范围
：[1，
int_max］
默认值
：
100
search_list_size
越大，为每个节点找到真正近邻的可能性就越大，这可能会带来更高质量的图和更好的搜索性能（召回率）。但是，这样做的代价是索引建立时间大大延长。该值应始终大于或等于
max_degree
。
SearchCacheBudgetGBRatio
控制在索引构建过程中为缓存图的频繁访问部分而分配的内存量。
类型
：浮点
范围
：[0.0, 0.3)
默认值
：
0.10
较高的值会分配更多内存用于缓存，从而显著减少磁盘 I/O，但会消耗更多系统内存。在大多数情况下，我们建议在此范围内设置值：[0.0, 0.3).
PQ
PQCodeBudgetGBRatio
控制 PQ 代码（数据点的压缩表示）相对于未压缩数据的大小。
类型
：浮点
范围
：（0.0, 0.25］
默认值
：
0.125
比率越高，搜索结果越精确，因为 PQ 代码分配的内存比例越大，有效存储的原始向量信息就越多。然而，这需要更多内存，限制了处理大型数据集的能力。 较低的比率可减少内存使用量，但可能会牺牲精确度，因为较小的 PQ 代码保留的信息较少。这种方法适用于内存受限的情况，有可能实现对大型数据集的索引。
在大多数情况下，我们建议在此范围内设置一个值：（0.0625, 0.25］
特定于索引的搜索参数
这些参数会影响 DISKANN 执行搜索的方式。调整这些参数会影响搜索速度、延迟和资源使用。
下面列表中的
BeamWidthRatio
只能通过 Milvus 配置文件进行配置 (
milvus.yaml
)
下表中的
search_list
只能在 SDK 的搜索参数中配置。
参数
说明
值范围
调整建议
并行
BeamWidthRatio
通过确定相对于可用 CPU 内核数的最大并行磁盘 I/O 请求数，控制搜索过程中的并行程度。
类型
：浮点
范围
：[1，max(128 / CPU 核数，16)
默认值
：
4.0
数值越大，并行性越高，这可以加快使用强大 CPU 和 SSD 的系统的搜索速度。在大多数情况下，我们建议在此范围内设置值：[1.0, 4.0].
search_list
在搜索操作过程中，该参数决定了算法在遍历图时所维护的候选池的大小。数值越大，找到真正近邻的几率越大（召回率更高），但也会增加搜索延迟。
类型
： 整数整数[1，
int_max］
默认值
：
100
为了在性能和准确性之间取得良好平衡，建议将此值设置为等于或略大于要检索的结果数（top_k）。