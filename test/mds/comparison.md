Milvus 与替代产品的比较
在探索各种向量数据库选项时，本综合指南将帮助您了解 Milvus 的独特功能，确保您选择最适合自己特定需求的数据库。值得注意的是，Milvus 是领先的开源矢量数据库，
Zilliz Cloud
提供全面管理的 Milvus 服务。要对照竞争对手客观评估 Milvus，可以考虑使用
基准工具
分析性能指标。
Milvus 的亮点
功能性
：Milvus 不仅支持基本的向量相似性搜索，还支持
稀疏向量
、
批量向量
、
过滤搜索
和
混合搜索
功能等高级功能。
灵活性
：Milvus 支持多种部署模式和多个 SDK，所有这些都在一个强大的集成生态系统中实现。
性能
：Milvus 采用
HNSW
和
DiskANN
等优化索引算法以及先进的
GPU 加速
，可确保高吞吐量和低延迟的实时处理。
可扩展性
：其定制的分布式架构可轻松扩展，从小型数据集到超过 100 亿向量的 Collections 都能轻松应对。
整体比较
为了对 Milvus 和 Pinecone 这两个向量数据库解决方案进行比较，下表突出了各种功能之间的差异。
特征
Pinecone
Milvus
备注
部署模式
纯 SaaS
Milvus Lite、On-prem Standalone & Cluster、Zilliz Cloud Saas & BYOC
Milvus 提供更灵活的部署模式。
支持的 SDK
Python、JavaScript/TypeScript
Python、Java、NodeJS、Go、Restful API、C#、Rust
Milvus 支持更广泛的编程语言。
开源状态
已关闭
开源
Milvus 是一个流行的开源向量数据库。
可扩展性
仅向上/向下扩展
向外/向内扩展和向上/向下扩展
Milvus 采用分布式架构，增强了可扩展性。
可用性
可用区域内基于 Pod 的架构
可用区域故障切换和跨区域 HA
Milvus CDC（变更数据捕获）支持主备模式，以提高可用性。
性能成本（每百万次查询收费）
中型数据集 0.178 美元起，大型数据集 1.222 美元起
Zilliz Cloud 中型数据集的起价为 0.148 美元，大型数据集的起价为 0.635 美元；提供免费版本
请参阅
成本排名报告
。
GPU 加速
不支持
支持英伟达™（NVIDIA®）GPU
GPU 加速可大幅提升性能，通常可提升几个数量级。
术语比较
虽然两者作为向量数据库的功能相似，但 Milvus 和 Pinecone 的特定领域术语略有不同。详细的术语比较如下。
Pinecone
Milvus
备注
索引
Collections
在 Pinecone 中，索引是存储和管理相同大小向量的组织单位，这种索引与硬件（称为 pod）紧密结合在一起。相比之下，Milvus 的 Collections 功能类似，但能在单个实例中处理多个集合。
Collections
备份
在 Pinecone 中，Collection 本质上是索引的静态快照，主要用于备份目的，不能被查询。在 Milvus 中，用于创建备份的相应功能更加透明，命名也更直观。
命名空间
Partition Key
命名空间允许将索引中的向量分割成子集。Milvus 提供了分区或分区键等多种方法，以确保在 Collections 中实现高效的数据隔离。
元数据
标量字段
Pinecone 的元数据处理依赖于键值对，而 Milvus 允许使用复杂的标量字段，包括标准数据类型和动态 JSON 字段。
查询
查询
用于查找给定向量近邻的方法名称，可能会在上面应用一些额外的过滤器。
不可用
迭代器
Pinecone 缺乏对索引中所有向量进行迭代的功能。Milvus 引入了搜索迭代器和查询迭代器方法，增强了跨数据集的数据检索能力。
能力比较
功能
Pinecone
Milvus
部署模式
纯 SaaS
Milvus Lite、On-prem Standalone & Cluster、Zilliz Cloud Saas & BYOC
Embeddings 功能
不可用
支持
pymilvus[模型］
数据类型
字符串、数字、布尔、字符串列表
字符串、VarChar、数（Int、Float、Double）、Bool、数组、JSON、浮点矢量、二进制矢量、BFloat16、Float16、稀疏矢量
度量和索引类型
余弦、点、欧几里得
P-家族、S-家族
余弦、IP（点）、L2（欧几里得）、汉明、雅卡
FLAT、IVF_FLAT、IVF_SQ8、IVF_PQ、HNSW、SCANN、GPU 索引
Schema 设计
灵活模式
灵活模式、严格模式
多个向量场
不适用
多向量和混合搜索
工具
数据集、文本工具、Spark 连接器
Attu、Birdwatcher、备份、CLI、CDC、Spark 和 Kafka 连接器
主要见解
部署模式
：Milvus提供多种部署选项，包括本地部署、Docker、Kubernetes on-premises、云SaaS和面向企业的自带云（BYOC），而Pinecone仅限于SaaS部署。
嵌入功能
：Milvus 支持额外的嵌入库，可直接使用嵌入模型将源数据转换为向量。
数据类型
：与 Pinecone 相比，Milvus 支持更广泛的数据类型，包括数组和 JSON。Pinecone 只支持以字符串、数字、布尔值或字符串列表为值的扁平元数据结构，而 Milvus 可以在一个 JSON 字段内处理任何 JSON 对象，包括嵌套结构。Pinecone 限制每个向量的元数据大小为 40KB。
度量和索引类型
：Milvus 支持多种度量和索引类型，以适应各种使用情况，而 Pinecone 的选择较为有限。虽然在 Milvus 中必须为向量建立索引，但也提供了 AUTO_INDEX 选项来简化配置过程。
Schema 设计
：Milvus 为模式设计提供了灵活的
create_collection
模式，包括快速设置动态模式，以获得类似 Pinecone 的无模式体验，以及自定义设置预定义模式字段和索引，类似关系数据库管理系统（RDBMS）。
多向量字段
：Milvus 支持在单个 Collections 中存储多个向量字段，这些字段可以是稀疏的，也可以是密集的，维度也可能不同。Pinecone 不提供类似功能。
工具
：Milvus 为数据库管理和利用提供了更广泛的工具选择，如 Attu、Birdwatcher、Backup、CLI、CDC 以及 Spark 和 Kafka 连接器。