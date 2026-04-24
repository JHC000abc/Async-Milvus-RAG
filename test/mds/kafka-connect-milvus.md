将 Apache Kafka® 与 Milvus/Zilliz Cloud 连接起来，实现矢量数据的实时摄取
在本快速入门指南中，我们将展示如何设置开源 kafka 和 Zilliz Cloud 以摄取向量数据。
本教程介绍了如何使用 Apache Kafka® 将向量数据流化并摄取到 Milvus 向量数据库和 Zilliz Cloud（完全托管 Milvus），从而实现语义搜索、推荐系统和 AI 驱动的分析等高级实时应用。
Apache Kafka 是一个分布式事件流平台，专为高吞吐量、低延迟管道而设计。它被广泛用于收集、存储和处理来自数据库、物联网设备、移动应用程序和云服务等来源的实时数据流。Kafka 处理海量数据的能力使其成为 Milvus 或 Zilliz Cloud 等向量数据库的重要数据源。
例如，Kafka可以捕获实时数据流--如用户交互、传感器读数以及来自机器学习模型的嵌入数据--并将这些数据流直接发布到Milvus或Zilliz Cloud。一旦进入向量数据库，就可以对这些数据进行索引、搜索和高效分析。
Kafka与Milvus和Zilliz Cloud的集成为非结构化数据工作流提供了一种无缝的方式来构建强大的管道。该连接器既适用于开源 Kafka 部署，也适用于
Confluent
和
StreamNative
等托管服务。
在本教程中，我们使用 Zilliz Cloud 作为演示：
第 1 步：下载 kafka-connect-milvus 插件
完成以下步骤下载 kafka-connect-milvus 插件。
从
此处
下载最新的插件压缩文件
zilliz-kafka-connect-milvus-xxx.zip
。
第 2 步：下载 Kafka
从
此处
下载最新的 kafka。
解压下载的文件并转到 kafka 目录。
$
tar -xzf kafka_2.13-3.6.1.tgz
$
cd
kafka_2.13-3.6.1
第 3 步：启动 Kafka 环境
注意：本地环境必须安装 Java 8 以上。
运行以下命令以按正确顺序启动所有服务：
启动 ZooKeeper 服务
$
bin/zookeeper-server-start.sh config/zookeeper.properties
启动 Kafka 代理服务
打开另一个终端会话并运行：
$
bin/kafka-server-start.sh config/server.properties
一旦所有服务都成功启动，你就拥有了一个基本的 Kafka 运行环境，可以随时使用了。
详情请查看 Kafka 官方快速入门指南：https://kafka.apache.org/quickstart
第 4 步：配置 Kafka 和 Zilliz Cloud
确保已设置并正确配置 Kafka 和 Zilliz Cloud。
如果 Kafka 中还没有主题，请在 Kafka 中创建一个主题（例如
topic_0
）。
$
bin/kafka-topics.sh --create --topic topic_0 --bootstrap-server localhost:9092
如果 Zilliz Cloud 中还没有 Collections，请创建一个带有向量字段的 Collections（本例中向量为
dimension=8
）。您可以在 Zilliz Cloud 上使用以下示例 Schema：
注意：确保双方的 Schema 相互匹配。在 Schema 中，正好有一个向量字段。双方每个字段的名称完全相同。
第 5 步：加载 kafka-connect-milvus 插件到 Kafka 实例
解压缩在步骤 1 中下载的
zilliz-kafka-connect-milvus-xxx.zip
文件。
将
zilliz-kafka-connect-milvus
目录复制到 Kafka 安装的
libs
目录中。
修改 Kafka 安装
config
目录中的
connect-standalone.properties
文件。
key.converter.schemas.enable=false
value.converter.schemas.enable=false
plugin.path=libs/zilliz-kafka-connect-milvus-xxx
在 Kafka 安装的
config
目录中创建并配置
milvus-sink-connector.properties
文件。
name=zilliz-kafka-connect-milvus
connector.class=com.milvus.io.kafka.MilvusSinkConnector
public.endpoint=https://<public.endpoint>:port
token=*****************************************
collection.name=topic_0
topics=topic_0
第 6 步：启动连接器
使用之前的配置文件启动连接器
$
bin/connect-standalone.sh config/connect-standalone.properties config/milvus-sink-connector.properties
尝试向刚刚在 Kafka 中创建的 Kafka 主题发送消息
bin/kafka-console-producer.sh --topic topic_0 --bootstrap-server localhost:9092
>
{
"id"
: 0,
"title"
:
"The Reported Mortality Rate of Coronavirus Is Not Important"
,
"title_vector"
: [0.041732933, 0.013779674, -0.027564144, -0.013061441, 0.009748648, 0.00082446384, -0.00071647146, 0.048612226],
"link"
:
"https://medium.com/swlh/the-reported-mortality-rate-of-coronavirus-is-not-important-369989c8d912"
}
检查实体是否已插入 Zilliz Cloud 中的 Collections。下面是插入成功后在 Zilliz Cloud 上的显示效果：
支持
如果您需要任何帮助或对 Kafka Connect Milvus 连接器有任何疑问，请随时联系该连接器的维护者：
电子邮件：
support@zilliz.com