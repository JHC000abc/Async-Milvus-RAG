Milvus 2.2 基准测试报告
本报告展示了 Milvus 2.2.0 的主要测试结果，旨在介绍 Milvus 2.2.0 的搜索性能，特别是扩展和缩小的能力。
我们最近对 Milvus 2.2.3 进行了一次基准测试，主要结果如下：
搜索延迟降低 2.5 倍
QPS 提高 4.5 倍
十亿规模的相似性搜索，性能几乎没有下降
使用多个副本时的线性可扩展性
有关详细信息，请参阅
本白皮书
和
相关基准测试代码
。
总结
与 Milvus 2.1 相比，Milvus 2.2.0 的 QPS 在集群模式下提高了 48%，在 Standalone 模式下提高了 75%。
Milvus 2.2.0 的扩展和缩小能力令人印象深刻：
当 CPU 内核从 8 个扩展到 32 个时，QPS 呈线性增长。
将 Querynode 复制从 1 个扩展到 8 个时，QPS 呈线性增长。
术语
点击查看测试中使用的术语详情
术语
说明
nq
一次搜索请求中要搜索的向量数量
topk
搜索请求中每个向量（以 nq 为单位）的最近向量数
ef
HNSW 索引
特有的搜索参数
RT
从发送请求到接收响应的响应时间
QPS
每秒成功处理的搜索请求数
测试环境
所有测试均在以下环境下进行。
硬件环境
硬件环境
规格
中央处理器
英特尔® 至强® Gold 6226R CPU @ 2.90GHz
内存
16*/32 GB RDIMM，3200 MT/s
固态硬盘
SATA 6 Gbps
软件环境
软件环境
版本
Milvus
v2.2.0
Milvus GO SDK
v2.2.0
部署方案
Milvus 实例（单机或集群）通过
Helm
部署在基于物理机或虚拟机的 Kubernetes 集群上。
不同的测试仅在 CPU 内核数量、内存大小和副本（工作节点）数量上有所不同，这仅适用于 Milvus 集群。
未指定的配置与
默认配置
相同。
Milvus 依赖项（MinIO、Pulsar 和 Etcd）将数据存储在每个节点的本地固态硬盘上。
搜索请求通过
Milvus GO SDK
发送到 Milvus 实例。
数据集
测试使用
ANN-Benchmarks
的开源数据集 SIFT（128 维）。
测试流程
使用 Helm 启动 Milvus 实例，并按照每个测试中列出的各自服务器配置。
通过 Milvus GO SDK 连接到 Milvus 实例并获取相应的测试结果。
创建一个 Collection。
插入 100 万个 SIFT 向量。建立 HNSW 索引并配置索引参数，将
M
设置为
8
，将
efConstruction
设置为
200
。
加载 Collections。
使用不同的并发数进行搜索，搜索参数为
nq=1, topk=1, ef=64
，每个并发数的持续时间至少为 1 小时。
测试结果
Milvus 2.2.0 对 Milvus 2.1.0
群集
服务器配置（群集）
yaml queryNode: replicas: 1 resources: limits: cpu: "12.0" memory: 8Gi requests: cpu: "12.0" memory: 8Gi
搜索性能
Milvus
QPS
RT(TP99) / ms
RT(TP50) / ms
故障/秒
2.1.0
6904
59
28
0
2.2.0
10248
63
24
0
群集搜索性能
单机
服务器配置（单机）
yaml standalone: replicas: 1 resources: limits: cpu: "12.0" memory: 16Gi requests: cpu: "12.0" memory: 16Gi
搜索性能
Milvus
QPS
RT(TP99) / ms
RT(TP50) / ms
故障/秒
2.1.0
4287
104
76
0
2.2.0
7522
127
79
0
独立搜索性能
Milvus 2.2.0 扩展能力
扩展一个 Querynode 中的 CPU 内核，检查扩展能力。
服务器配置（群集）
yaml queryNode: replicas: 1 resources: limits: cpu: "8.0" /"12.0" /"16.0" /"32.0" memory: 8Gi requests: cpu: "8.0" /"12.0" /"16.0" /"32.0" memory: 8Gi
搜索性能
CPU 内核
并发数
QPS
RT(TP99) / ms
RT(TP50) / ms
故障/秒
8
500
7153
127
83
0
12
300
10248
63
24
0
16
600
14135
85
42
0
32
600
20281
63
28
0
按 Querynode CPU 内核分列的搜索性能
Milvus 2.2.0 扩展能力
使用更多 Querynodes 扩展更多副本，以检查扩展能力。
注意：加载 Collections 时，Querynodes 的数量等于
replica_number
。
服务器配置（群集）
yaml queryNode: replicas: 1 / 2 / 4 / 8 resources: limits: cpu: "8.0" memory: 8Gi requests: cpu: "8.0" memory: 8Gi
副本
并发数
QPS
RT(TP99) / ms
RT(TP50) / ms
故障/秒
1
500
7153
127
83
0
2
500
15903
105
27
0
4
800
19281
109
40
0
8
1200
30655
93
38
0
按 Querynode 复制的搜索性能
下一步
请参照
本指南
，尝试自行执行 Milvus 2.2.0 基准测试，只是在本指南中应改用 Milvus 2.2 和 Pymilvus 2.2。