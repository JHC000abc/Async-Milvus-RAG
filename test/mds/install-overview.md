Milvus 部署选项概述
Milvus 是一个高性能、可扩展的向量数据库。它支持各种规模的用例，从在 Jupyter 笔记本中本地运行的演示到处理数百亿向量的大规模 Kubernetes 集群。目前，Milvus 有三种部署选项：Milvus Lite、Milvus Standalone 和 Milvus Distributed。
Milvus Lite
Milvus Lite
是一个 Python 库，可导入到您的应用程序中。作为 Milvus 的轻量级版本，它非常适合在 Jupyter 笔记本或资源有限的智能设备上运行快速原型。Milvus Lite 支持与 Milvus 其他部署相同的 API。与 Milvus Lite 交互的客户端代码也能与其他部署模式下的 Milvus 实例协同工作。
要将 Milvus Lite 集成到应用程序中，请运行
pip install pymilvus
进行安装，并使用
MilvusClient("./demo.db")
语句实例化一个带有本地文件的向量数据库，以持久化所有数据。更多详情，请参阅
运行 Milvus Lite
。
Milvus 单机版
Milvus Standalone 是单机服务器部署。Milvus Standalone 的所有组件都打包到一个
Docker 镜像
中，部署起来非常方便。如果你有生产工作负载，但又不想使用 Kubernetes，在内存充足的单机上运行 Milvus Standalone 是个不错的选择。
Milvus Distributed
Milvus Distributed 可部署在
Kubernetes
集群上。这种部署采用云原生架构，摄取负载和搜索查询分别由独立节点处理，允许关键组件冗余。它具有最高的可扩展性和可用性，并能灵活定制每个组件中分配的资源。Milvus Distributed 是在生产中运行大规模向量搜索系统的企业用户的首选。
为您的使用案例选择正确的部署方式
部署模式的选择通常取决于应用程序的开发阶段：
用于快速原型开发
如果您想快速构建原型或用于学习，如检索增强生成（RAG）演示、人工智能聊天机器人、多模态搜索，Milvus Lite 本身或 Milvus Lite 与 Milvus Standalone 的组合都很适合。您可以在笔记本中使用 Milvus Lite 进行快速原型开发，并探索各种方法，如 RAG 中的不同分块策略。您可能希望在小规模生产中部署用 Milvus Lite 构建的应用程序，为真正的用户提供服务，或在更大的数据集（例如超过几百万个向量）上验证想法。Milvus Standalone 是合适的选择。Milvus Lite 的应用逻辑仍可共享，因为所有 Milvus 部署都有相同的客户端应用程序接口。Milvus Lite 中存储的数据也可以通过命令行工具移植到 Milvus Standalone 中。
小规模生产部署
对于早期生产阶段，当项目仍在寻求产品与市场的契合，敏捷性比可扩展性更重要时，Milvus Standalone 是最佳选择。只要有足够的机器资源，它仍然可以扩展到 1 亿向量，同时对 DevOps 的要求也比维护 K8s 集群低得多。
大规模生产部署
当你的业务快速增长，数据规模超过单台服务器的容量时，是时候考虑 Milvus Distributed 了。你可以继续使用Milvus Standalone作为开发或暂存环境，并操作运行Milvus Distributed的K8s集群。这可以支持你处理数百亿个向量，还能根据你的特定工作负载（如高读取、低写入或高写入、低读取的情况）灵活调整节点大小。
边缘设备上的本地搜索
对于在边缘设备上通过私有或敏感信息进行搜索，您可以在设备上部署 Milvus Lite，而无需依赖基于云的服务来进行文本或图像搜索。这适用于专有文档搜索或设备上对象检测等情况。
Milvus 部署模式的选择取决于项目的阶段和规模。Milvus 为从快速原型开发到大规模企业部署的各种需求提供了灵活而强大的解决方案。
Milvus Lite
建议用于较小的数据集，多达几百万个向量。
Milvus Standalone
适用于中型数据集，可扩展至 1 亿向量。
Milvus Distributed 专为
大规模部署而设计，能够处理从一亿到数百亿向量的数据集。
选择适合您使用情况的部署选项
功能比较
功能
Milvus Lite
Milvus 单机版
分布式 Milvus
SDK / 客户端软件
Python
gRPC
Python
Go
Java
Node.js
C#
RESTful
Python
Java
Go
Node.js
C#
RESTful
数据类型
密集向量
稀疏向量
二进制向量
布尔值
整数
浮点
VarChar
数组
JSON
密集向量
稀疏向量
二进制向量
布尔型
整数
浮点型
VarChar
数组
JSON
密集向量
稀疏向量
二进制向量
布尔值
整数
浮点
VarChar
数组
JSON
搜索功能
向量搜索（ANN 搜索）
元数据过滤
范围搜索
标量查询
通过主键获取实体
混合搜索
向量搜索（ANN 搜索）
元数据过滤
范围搜索
标量查询
通过主键获取实体
混合搜索
向量搜索（ANN 搜索）
元数据过滤
范围搜索
标量查询
通过主键获取实体
混合搜索
CRUD 操作符
✔️
✔️
✔️
高级数据管理
不适用
访问控制
分区
分区密钥
访问控制
分区
分区密钥
物理资源分组
一致性级别
强
强
有界停滞
会话
最终
强
有界稳定性
会话
最终