盘上索引
本文介绍了用于磁盘优化向量搜索的磁盘索引算法 DiskANN。DiskANN 基于 Vamana 图，可在大型数据集中进行高效的磁盘上向量搜索。
为了提高查询性能，可以为每个向量字段
指定一种索引类型
。
目前，一个向量字段只支持一种索引类型。切换索引类型时，Milvus 会自动删除旧索引。
前提条件
要在 Milvus 中使用 DiskANN，请注意
Milvus 实例运行在 Ubuntu 18.04.6 或更高版本上。
Milvus 数据路径应挂载到 NVMe SSD 上，以充分发挥性能：
对于 Milvus Standalone 实例，数据路径应为实例运行容器中的
/var/lib/milvus/data
。
对于 Milvus 群集实例，数据路径应为查询节点和索引节点所在容器中的
/var/lib/milvus/data
。
限制
要使用 DiskANN，请确保
数据中只使用至少 1 维的浮点型向量。
仅使用欧氏距离 (L2)、内积 (IP) 或 COSINE 来测量向量之间的距离。
索引和搜索设置
索引构建参数
建立 DiskANN 索引时，请使用
DISKANN
作为索引类型。无需索引参数。
搜索参数
参数
说明
范围
默认值
search_list
候选列表的大小，越大召回率越高，但性能越差。
[topk,int32_max]（最大值
16
与 DiskANN 相关的 Milvus 配置
DiskANN 是可调的。您可以在
${MILVUS_ROOT_PATH}/configs/milvus.yaml
中修改与 DiskANN 相关的参数，以提高其性能。
...
DiskIndex:
MaxDegree:
56
SearchListSize:
100
PQCodeBudgetGBRatio:
0.125
SearchCacheBudgetGBRatio:
0.125
BeamWidthRatio:
4.0
...
参数
说明
值范围
默认值
MaxDegree
Vamana 图形的最大阶数。
数值越大，召回率越高，但会增加索引的大小和建立索引的时间。
[1, 512]
56
SearchListSize
候选列表的大小。
该值越大，建立索引的时间越长，但召回率越高。
除非需要缩短建立索引的时间，否则请将其设置为小于
MaxDegree
的值。
[1，int32_max］
100
PQCodeBudgetGBRatio
PQ 代码的大小限制。
该值越大，调用率越高，但会增加内存使用量。
(0.0, 0.25]
0.125
SearchCacheBudgetGBRatio
缓存节点数与原始数据之比。
数值越大，建立索引的性能越好，但内存使用量也会增加。
[0.0, 0.3)
0.10
BeamWidthRatio
每次搜索迭代的最大 IO 请求数与 CPU 数量之比。
[1，max(128 / CPU 数量，16)
4.0
故障排除
如何处理
io_setup() failed; returned -11, errno=11:Resource temporarily unavailable
错误？
Linux 内核提供了异步非阻塞 I/O（AIO）功能，允许一个进程同时启动多个 I/O 操作，而无需等待任何一个操作完成。这有助于提高处理和 I/O 重叠的应用程序的性能。
可以使用 proc 文件系统中的
/proc/sys/fs/aio-max-nr
虚拟文件来调整性能。
aio-max-nr
参数决定允许的最大并发请求数。
aio-max-nr
默认为
65535
，也可设置为
10485760
。