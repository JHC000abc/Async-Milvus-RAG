本地运行 Milvus Lite
本页介绍如何使用 Milvus Lite 在本地运行 Milvus。Milvus Lite 是
Milvus
的轻量级版本，Milvus 是一个开源向量数据库，通过向量嵌入和相似性搜索为人工智能应用提供支持。
概述
Milvus Lite 可导入您的 Python 应用程序，提供 Milvus 的核心向量搜索功能。Milvus Lite 已包含在
Milvus 的 Python SDK
中。它可以通过
pip install pymilvus
简单地部署。
使用 Milvus Lite，您可以在几分钟内开始构建具有向量相似性搜索功能的人工智能应用程序！Milvus Lite 适合在以下环境中运行：
Jupyter Notebook / Google Colab
笔记本电脑
边缘设备
Milvus Lite 与 Milvus Standalone 和 Distributed 共享相同的 API，涵盖了向量数据持久化和管理、向量 CRUD 操作、稀疏和密集向量搜索、元数据过滤、多向量和混合搜索（hybrid_search）等大部分功能。它们共同为不同类型的环境提供了一致的体验，从边缘设备到云中的集群，适合不同规模的使用案例。使用相同的客户端代码，您可以在笔记本电脑或 Jupyter Notebook 上使用 Milvus Lite 运行 GenAI 应用程序，或在 Docker 容器上使用 Milvus Standalone 运行 GenAI 应用程序，或在大规模 Kubernetes 集群上使用 Milvus Distributed 运行 GenAI 应用程序，为生产提供数十亿向量。
先决条件
Milvus Lite 目前支持以下环境：
Ubuntu >= 20.04（x86_64 和 arm64）
MacOS >= 11.0（苹果硅 M1/M2 和 x86_64）
请注意，Milvus Lite 仅适用于小规模向量搜索使用案例。对于大规模用例，我们建议使用
Milvus Standalone
或
Milvus Distributed
。您也可以考虑在
Zilliz Cloud
上使用完全托管的 Milvus。
设置 Milvus Lite
pip install -U pymilvus[milvus-lite]
我们建议使用
pymilvus
。你可以通过
pip install
与
-U
强制更新到最新版本，
milvus-lite
会自动安装。
如果你想明确安装
milvus-lite
软件包，或者你已经安装了旧版本的
milvus-lite
并想更新它，可以使用
pip install -U milvus-lite
。
连接到 Milvus Lite
在
pymilvus
中，指定一个本地文件名作为 MilvusClient 的 uri 参数将使用 Milvus Lite。
from
pymilvus
import
MilvusClient
client = MilvusClient(
"./milvus_demo.db"
)
运行上述代码段后，将在当前文件夹下生成名为
milvus_demo.db 的
数据库文件。
注意：
请注意，同样的 API 也适用于 Milvus Standalone、Milvus Distributed 和 Zilliz Cloud，唯一的区别是将本地文件名替换为远程服务器端点和凭据，例如
client = MilvusClient(uri="http://localhost:19530", token="username:password")
。
示例
以下是如何使用 Milvus Lite 进行文本搜索的简单演示。还有更多使用 Milvus Lite 构建
RAG
、
图像搜索
等应用程序的综合
示例
，以及在
LangChain
和
LlamaIndex
等流行 RAG 框架中使用 Milvus Lite 的
示例
！
from
pymilvus
import
MilvusClient
import
numpy
as
np

client = MilvusClient(
"./milvus_demo.db"
)
client.create_collection(
    collection_name=
"demo_collection"
,
    dimension=
384
# The vectors we will use in this demo has 384 dimensions
)
# Text strings to search from.
docs = [
"Artificial intelligence was founded as an academic discipline in 1956."
,
"Alan Turing was the first person to conduct substantial research in AI."
,
"Born in Maida Vale, London, Turing was raised in southern England."
,
]
# For illustration, here we use fake vectors with random numbers (384 dimension).
vectors = [[ np.random.uniform(-
1
,
1
)
for
_
in
range
(
384
) ]
for
_
in
range
(
len
(docs)) ]
data = [ {
"id"
: i,
"vector"
: vectors[i],
"text"
: docs[i],
"subject"
:
"history"
}
for
i
in
range
(
len
(vectors)) ]
res = client.insert(
    collection_name=
"demo_collection"
,
    data=data
)
# This will exclude any text in "history" subject despite close to the query vector.
res = client.search(
    collection_name=
"demo_collection"
,
    data=[vectors[
0
]],
filter
=
"subject == 'history'"
,
    limit=
2
,
    output_fields=[
"text"
,
"subject"
],
)
print
(res)
# a query that retrieves all entities matching filter expressions.
res = client.query(
    collection_name=
"demo_collection"
,
filter
=
"subject == 'history'"
,
    output_fields=[
"text"
,
"subject"
],
)
print
(res)
# delete
res = client.delete(
    collection_name=
"demo_collection"
,
filter
=
"subject == 'history'"
,
)
print
(res)
限制
运行 Milvus Lite 时，请注意某些功能不受支持。下表总结了 Milvus Lite 的使用限制。
Collections
方法/参数
Milvus Lite 支持
创建集合()
支持有限参数
collection_name
Y
dimension
Y
primary_field_name
Y
id_type
Y
vector_field_name
Y
metric_type
Y
auto_id
Y
schema
Y
index_params
Y
enable_dynamic_field
Y
num_shards
N
partition_key_field
N
num_partitions
N
consistency_level
N（仅支持
Strong
；任何配置都将被视为
Strong
。）
get_collection_stats()
支持获取 Collections 统计信息。
collection_name
Y
timeout
Y
describe_collection()
num_shards
、
consistency_level
和
collection_id
响应无效。
timeout
Y
has_collection()
支持检查集合是否存在。
collection_name
Y
timeout
Y
list_collections()
支持列出所有 Collections。
drop_collection()
支持删除 Collections。
collection_name
Y
timeout
Y
rename_collection()
不支持重命名 Collections。
字段和 Schema
方法/参数
Milvus Lite 支持
创建模式
支持有限参数
auto_id
Y
enable_dynamic_field
Y
primary_field
Y
partition_key_field
N
add_field()
支持有限参数
field_name
Y
datatype
Y
is_primary
Y
max_length
Y
element_type
Y
max_capacity
Y
dim
Y
is_partition_key
N
插入和搜索
方法/参数
Milvus Lite 支持
搜索()
支持有限参数
collection_name
Y
data
Y
filter
Y
limit
Y
output_fields
Y
search_params
Y
timeout
Y
partition_names
N
anns_field
Y
查询()
支持有限参数
collection_name
Y
filter
Y
output_fields
Y
timeout
Y
ids
Y
partition_names
N
获取()
支持有限参数
collection_name
Y
ids
Y
output_fields
Y
timeout
Y
partition_names
N
删除()
支持有限参数
collection_name
Y
ids
Y
timeout
Y
filter
Y
partition_name
N
插入()
支持有限参数
collection_name
Y
data
Y
timeout
Y
partition_name
N
upsert()
支持有限参数
collection_name
Y
data
Y
timeout
Y
partition_name
N
加载和释放
方法/参数
Milvus Lite 支持
load_collection()
Y
collection_name
Y
timeout
Y
release_collection()
Y
collection_name
Y
timeout
Y
get_load_state()
不支持获取加载状态。
refresh_load()
不支持加载已加载集合的未加载数据。
close()
Y
索引
方法/参数
Milvus Lite 支持
list_indexes()
支持列出索引。
collection_name
Y
field_name
Y
创建索引
仅支持
FLAT
索引类型。
index_params
Y
timeout
Y
drop_index()
支持删除索引。
collection_name
Y
index_name
Y
timeout
Y
describe_index()
支持描述索引。
collection_name
Y
index_name
Y
timeout
Y
向量索引类型
Milvus Lite 仅支持
FLAT
索引类型。无论在 Collections 中指定了哪种索引类型，它都使用 FLAT 类型。
搜索功能
Milvus Lite 支持稀疏向量、多向量和混合搜索。
分区
Milvus Lite 不支持分区和与分区相关的方法。
用户和角色
Milvus Lite 不支持用户和角色及相关方法。
别名
Milvus Lite 不支持别名和与别名相关的方法。
从 Milvus Lite 迁移数据
所有存储在 Milvus Lite 中的数据都可以轻松导出并加载到其他类型的 Milvus 部署中，例如 Docker 上的 Milvus Standalone、K8s 上的 Milvus Distributed 或
Zilliz Cloud
上的全托管 Milvus。
Milvus Lite 提供了一个命令行工具，可以将数据转储到 json 文件，该文件可以导入
Milvus
和
Zilliz Cloud
（Milvus 的完全托管云服务）。milvus-lite 命令将与 milvus-lite python 软件包一起安装。
#
Install
pip install -U "pymilvus[bulk_writer]"

milvus-lite dump -h

usage: milvus-lite dump [-h] [-d DB_FILE] [-c COLLECTION] [-p PATH]

optional arguments:
  -h, --help            show this help message and exit
  -d DB_FILE, --db-file DB_FILE
                        milvus lite db file
  -c COLLECTION, --collection COLLECTION
                        collection that need to be dumped
  -p PATH, --path PATH  dump file storage dir
下面的示例转储了
demo_collection
Collections 中的所有数据，这些数据存储在
./milvus_demo.db
（Milvus Lite 数据库文件）中。
导出数据：
milvus-lite dump -d ./milvus_demo.db -c demo_collection -p ./data_dir
#
./milvus_demo.db: milvus lite db file
#
demo_collection: collection that need to be dumped
#
./data_dir : dump file storage
dir
有了转储文件，你可以通过
数据导入
将数据上传到 Zilliz Cloud，或通过
批量插入
将数据上传到 Milvus 服务器。
下一步
连接 Milvus Lite 后，您可以
查看
快速入门
，了解 Milvus 的功能。
学习 Milvus 的基本操作：
管理数据库
管理 Collections
管理分区
插入、倒置和删除
单向量搜索
混合搜索
使用 Helm 图表升级 Milvus
。
扩展你的 Milvus 集群
。
在云上部署你的 Milvus 集群：
亚马逊 EKS
谷歌云
微软 Azure
探索
Milvus 备份
，一个用于 Milvus 数据备份的开源工具。
探索
Birdwatcher
，用于调试 Milvus 和动态配置更新的开源工具。
探索
Attu
，一款用于直观管理 Milvus 的开源图形用户界面工具。
使用 Prometheus 监控 Milvus
。