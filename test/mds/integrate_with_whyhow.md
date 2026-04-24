Milvus 与 WhyHow 的集成
本指南演示如何使用 whyHow.ai 和 Milvus Lite 进行基于规则的检索。
概述
WhyHow是一个平台，它为开发者提供了组织、上下文化和可靠检索非结构化数据以执行复杂RAG所需的构建模块。基于规则的检索包是WhyHow开发的一个Python包，使人们能够创建和管理具有高级过滤功能的检索增强生成（RAG）应用程序。
安装
在开始之前，请安装所有必要的 Python 软件包，以便日后使用。
pip install --upgrade pymilvus, whyhow_rbr
接下来，我们需要初始化 Milvus 客户端，通过使用 Milvus Lite 实现基于规则的检索。
from
pymilvus
import
MilvusClient
# Milvus Lite local path
path=
"./milvus_demo.db"
# random name for local milvus lite db path
# Initialize the ClientMilvus
milvus_client = ClientMilvus(path)
你也可以通过 Milvus 云初始化 Milvus 客户端
from
pymilvus
import
MilvusClient
# Milvus Cloud credentials
YOUR_MILVUS_CLOUD_END_POINT =
"YOUR_MILVUS_CLOUD_END_POINT"
YOUR_MILVUS_CLOUD_TOKEN =
"YOUR_MILVUS_CLOUD_TOKEN"
# Initialize the ClientMilvus
milvus_client = ClientMilvus(
        milvus_uri=YOUR_MILVUS_CLOUD_END_POINT, 
        milvus_token=YOUR_MILVUS_CLOUD_TOKEN,
)
创建 Collections
定义必要的变量
# Define collection name
COLLECTION_NAME=
"YOUR_COLLECTION_NAME"
# take your own collection name
# Define vector dimension size
DIMENSION=
1536
# decide by the model you use
添加 Schema
在向 Milvus Lite 数据库插入任何数据之前，我们需要先定义数据字段，这里称为 Schema。通过创建对象
CollectionSchema
和添加数据字段
add_field()
，我们可以控制数据类型及其特征。在向 Milvus 插入任何数据之前，这一步是必须的。
schema = milvus_client.create_schema(auto_id=
True
)
# Enable id matching
schema = milvus_client.add_field(schema=schema, field_name=
"id"
, datatype=DataType.INT64, is_primary=
True
)
schema = milvus_client.add_field(schema=schema, field_name=
"embedding"
, datatype=DataType.FLOAT_VECTOR, dim=DIMENSION)
创建索引
对于每个 Schema，最好都有一个索引，这样查询效率会更高。要创建索引，我们首先需要一个
index_params
，然后在这个
IndexParams
对象上添加更多索引数据。
# Start to indexing data field
index_params = milvus_client.prepare_index_params()
index_params = milvus_client.add_index(
    index_params=index_params,
# pass in index_params object
field_name=
"embedding"
,
    index_type=
"AUTOINDEX"
,
# use autoindex instead of other complex indexing method
metric_type=
"COSINE"
,
# L2, COSINE, or IP
)
该方法是对 Milvus 官方实现
（官方文档
）的精简封装。
创建 Collections
定义好所有数据字段并建立索引后，我们现在需要创建数据库 Collections，这样就能快速、准确地访问数据了。需要说明的是，我们将
enable_dynamic_field
初始化为 true，这样就可以自由上传任何数据。这样做的代价是数据查询可能会效率低下。
# Create Collection
milvus_client.create_collection(
    collection_name=COLLECTION_NAME,
    schema=schema,
    index_params=index_params
)
上传文件
创建完 Collections 后，我们就可以用文档填充了。在
whyhow_rbr
中，这是通过
MilvusClient
的
upload_documents
方法完成的。它在引擎盖下执行以下步骤：
预处理
：读取并将提供的 PDF 文件分割成块
嵌入
：使用 OpenAI 模型嵌入所有数据块
插入
：将嵌入和元数据上传到 Milvus Lite
# get pdfs
pdfs = [
"harry-potter.pdf"
,
"game-of-thrones.pdf"
]
# replace to your pdfs path
# Uploading the PDF document
milvus_client.upload_documents(
    collection_name=COLLECTION_NAME,
    documents=pdfs
)
问题解答
现在，我们终于可以进入检索增强生成阶段了。
# Search data and implement RAG!
res = milvus_client.search(
    question=
'What food does Harry Potter like to eat?'
,
    collection_name=COLLECTION_NAME,
    anns_field=
'embedding'
,
    output_fields=
'text'
)
print
(res[
'answer'
])
print
(res[
'matches'
])
规则
在前面的例子中，我们考虑了索引中的每一份文档。不过，有时只检索满足某些预定义条件（如
filename=harry-potter.pdf
）的文档可能是有益的。在
whyhow_rbr
通过 Milvus Lite，这可以通过调整搜索参数来实现。
规则可以控制以下元数据属性
filename
文件名
page_numbers
对应页码的整数列表（0 索引）
id
块的唯一标识符（这是最 "极端 "的过滤器）
其他基于
布尔表达式
的规则
# RULES(search on book harry-potter on page 8):
PARTITION_NAME=
'harry-potter'
# search on books
page_number=
'page_number == 8'
# first create a partitions to store the book and later search on this specific partition:
milvus_client.crate_partition(
    collection_name=COLLECTION_NAME,
    partition_name=PARTITION_NAME
# separate base on your pdfs type
)
# search with rules
res = milvus_client.search(
    question=
'Tell me about the greedy method'
,
    collection_name=COLLECTION_NAME,
    partition_names=PARTITION_NAME,
filter
=page_number,
# append any rules follow the Boolean Expression Rule
anns_field=
'embedding'
,
    output_fields=
'text'
)
print
(res[
'answer'
])
print
(res[
'matches'
])
在这个例子中，我们首先创建了一个分区来存储与哈利-波特相关的 PDF 文件，通过在这个分区内搜索，我们可以获得最直接的信息。此外，我们还应用页码作为过滤器，以指定我们希望搜索的确切页面。请记住，过滤器参数需要遵循
布尔规则
。
清理
最后，在执行完所有指令后，可以调用
drop_collection()
清理数据库。
# Clean up
milvus_client.drop_collection(
    collection_name=COLLECTION_NAME
)