使用 LlamaIndex 和 Milvus 进行元数据过滤
本笔记本说明了如何在 LlamaIndex 中使用 Milvus 向量存储，重点是元数据过滤功能。您将学习如何为带有元数据的文档编制索引，如何使用 LlamaIndex 的内置元数据过滤器执行向量搜索，以及如何将 Milvus 的本地过滤表达式应用到向量存储中。
在本笔记本结束时，你将了解如何利用 Milvus 的过滤功能，根据文档元数据缩小搜索结果的范围。
先决条件
安装依赖项
在开始之前，请确保已安装以下依赖项：
$
pip install llama-index-vector-stores-milvus llama-index
如果使用的是 Google Colab，可能需要
重启运行时
（导航至界面顶部的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
设置账户
本教程使用 OpenAI 进行文本 Embeddings 和答案生成。您需要准备
OpenAI API 密钥
。
import
openai

openai.api_key =
"sk-"
要使用 Milvus 向量存储，请指定您的 Milvus 服务器
URI
（可选择使用
TOKEN
）。要启动 Milvus 服务器，可以按照
Milvus 安装指南
设置 Milvus 服务器，或者直接免费试用
Zilliz Cloud
。
URI =
"./milvus_filter_demo.db"
# Use Milvus-Lite for demo purpose
# TOKEN = ""
准备数据
在本例中，我们将使用一些书名相似或相同但元数据（作者、流派和出版年份）不同的书籍作为样本数据。这将有助于演示 Milvus 如何根据向量相似性和元数据属性过滤和检索文档。
from
llama_index.core.schema
import
TextNode

nodes = [
    TextNode(
        text=
"Life: A User's Manual"
,
        metadata={
"author"
:
"Georges Perec"
,
"genre"
:
"Postmodern Fiction"
,
"year"
:
1978
,
        },
    ),
    TextNode(
        text=
"Life and Fate"
,
        metadata={
"author"
:
"Vasily Grossman"
,
"genre"
:
"Historical Fiction"
,
"year"
:
1980
,
        },
    ),
    TextNode(
        text=
"Life"
,
        metadata={
"author"
:
"Keith Richards"
,
"genre"
:
"Memoir"
,
"year"
:
2010
,
        },
    ),
    TextNode(
        text=
"The Life"
,
        metadata={
"author"
:
"Malcolm Knox"
,
"genre"
:
"Literary Fiction"
,
"year"
:
2011
,
        },
    ),
]
建立索引
在本节中，我们将使用默认嵌入模型（OpenAI 的
text-embedding-ada-002
）在 Milvus 中存储样本数据。标题将转换为文本嵌入并存储在密集嵌入字段中，而所有元数据将存储在标量字段中。
from
llama_index.vector_stores.milvus
import
MilvusVectorStore
from
llama_index.core
import
StorageContext, VectorStoreIndex


vector_store = MilvusVectorStore(
    uri=URI,
# token=TOKEN,
collection_name=
"test_filter_collection"
,
# Change collection name here
dim=
1536
,
# Vector dimension depends on the embedding model
overwrite=
True
,
# Drop collection if exists
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex(nodes, storage_context=storage_context)
2025-04-22 08:31:09,871 [DEBUG][_create_connection]: Created new connection using: 19675caa8f894772b3db175b65d0063a (async_milvus_client.py:547)
元数据过滤器
在本节中，我们将把 LlamaIndex 内置的元数据过滤器和条件应用到 Milvus 搜索中。
定义元数据过滤器
from
llama_index.core.vector_stores
import
(
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)

filters = MetadataFilters(
    filters=[
        MetadataFilter(
            key=
"year"
, value=
2000
, operator=FilterOperator.GT
        )
# year > 2000
]
)
用过滤器从向量存储中检索
retriever = index.as_retriever(filters=filters, similarity_top_k=
5
)
result_nodes = retriever.retrieve(
"Books about life"
)
for
node
in
result_nodes:
print
(node.text)
print
(node.metadata)
print
(
"\n"
)
The Life
{'author': 'Malcolm Knox', 'genre': 'Literary Fiction', 'year': 2011}


Life
{'author': 'Keith Richards', 'genre': 'Memoir', 'year': 2010}
多个元数据过滤器
您还可以将多个元数据过滤器组合起来，创建更复杂的查询。LlamaIndex 支持
AND
和
OR
条件来组合过滤器。这样就能根据元数据属性更精确、更灵活地检索文档。
条件
AND
举例说明如何筛选 1979 年至 2010 年出版的图书（具体来说，1979 < 年份 ≤ 2010）：
from
llama_index.core.vector_stores
import
FilterCondition

filters = MetadataFilters(
    filters=[
        MetadataFilter(
            key=
"year"
, value=
1979
, operator=FilterOperator.GT
        ),
# year > 1979
MetadataFilter(
            key=
"year"
, value=
2010
, operator=FilterOperator.LTE
        ),
# year <= 2010
],
    condition=FilterCondition.AND,
)

retriever = index.as_retriever(filters=filters, similarity_top_k=
5
)
result_nodes = retriever.retrieve(
"Books about life"
)
for
node
in
result_nodes:
print
(node.text)
print
(node.metadata)
print
(
"\n"
)
Life and Fate
{'author': 'Vasily Grossman', 'genre': 'Historical Fiction', 'year': 1980}


Life
{'author': 'Keith Richards', 'genre': 'Memoir', 'year': 2010}
条件
OR
试试另一个例子，过滤乔治-佩雷克（Georges Perec）或凯斯-理查兹（Keith Richards）所写的书籍：
filters = MetadataFilters(
    filters=[
        MetadataFilter(
            key=
"author"
, value=
"Georges Perec"
, operator=FilterOperator.EQ
        ),
# author is Georges Perec
MetadataFilter(
            key=
"author"
, value=
"Keith Richards"
, operator=FilterOperator.EQ
        ),
# author is Keith Richards
],
    condition=FilterCondition.OR,
)

retriever = index.as_retriever(filters=filters, similarity_top_k=
5
)
result_nodes = retriever.retrieve(
"Books about life"
)
for
node
in
result_nodes:
print
(node.text)
print
(node.metadata)
print
(
"\n"
)
Life
{'author': 'Keith Richards', 'genre': 'Memoir', 'year': 2010}


Life: A User's Manual
{'author': 'Georges Perec', 'genre': 'Postmodern Fiction', 'year': 1978}
使用 Milvus 的关键字参数
除了内置过滤功能外，您还可以通过
string_expr
关键字参数使用 Milvus 的本地过滤表达式。这样，您就可以在搜索操作过程中直接向 Milvus 传递特定的过滤表达式，从而超越标准元数据过滤，访问 Milvus 的高级过滤功能。
Milvus 提供强大而灵活的过滤选项，可实现对向量数据的精确查询：
基本操作符：比较操作符、范围筛选器、算术操作符和逻辑操作符
过滤表达式模板：用于常见过滤情况的预定义模式
专用操作符：针对 JSON 或数组字段的特定数据类型操作符
有关 Milvus 过滤表达式的全面文档和示例，请参阅
Milvus 过滤
的官方文档。
retriever = index.as_retriever(
    vector_store_kwargs={
"string_expr"
:
"genre like '%Fiction'"
,
    },
    similarity_top_k=
5
,
)
result_nodes = retriever.retrieve(
"Books about life"
)
for
node
in
result_nodes:
print
(node.text)
print
(node.metadata)
print
(
"\n"
)
The Life
{'author': 'Malcolm Knox', 'genre': 'Literary Fiction', 'year': 2011}


Life and Fate
{'author': 'Vasily Grossman', 'genre': 'Historical Fiction', 'year': 1980}


Life: A User's Manual
{'author': 'Georges Perec', 'genre': 'Postmodern Fiction', 'year': 1978}