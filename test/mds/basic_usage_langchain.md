将 Milvus 用作 LangChain 向量存储库
本笔记本介绍如何将
Milvus
作为
LangChain 向量存储
使用。
安装
您需要安装
langchain-milvus
和其他必要的依赖项。
$
pip install -qU langchain-milvus milvus-lite langchain-openai
最新版本的 pymilvus 自带本地向量数据库 Milvus Lite，适合原型开发。如果你有大规模数据，比如超过一百万个文档，我们建议你在
docker 或 kubernetes
上设置性能更强的 Milvus 服务器。
初始化
from
langchain_openai
import
OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model=
"text-embedding-3-large"
)
from
langchain_milvus
import
Milvus
# The easiest way is to use Milvus Lite where everything is stored in a local file.
# If you have a Milvus server you can use the server URI such as "http://localhost:19530".
URI =
"./milvus_example.db"
vector_store = Milvus(
    embedding_function=embeddings,
    connection_args={
"uri"
: URI},
)
使用 Milvus Collections 对数据进行分隔
你可以在同一个 Milvus 实例中将不同的无关文档存储在不同的 Collections 中，以保持上下文的一致性。
下面是如何创建一个新的向量文档存储 Collections：
from
langchain_core.documents
import
Document

vector_store_saved = Milvus.from_documents(
    [Document(page_content=
"foo!"
)],
    embeddings,
    collection_name=
"langchain_example"
,
    connection_args={
"uri"
: URI},
)
以下是如何检索存储的 Collections
vector_store_loaded = Milvus(
    embeddings,
    connection_args={
"uri"
: URI},
    collection_name=
"langchain_example"
,
)
管理向量存储
创建向量存储后，我们就可以通过添加和删除不同的项目与之交互。
向向量存储添加项目
我们可以使用
add_documents
函数将项目添加到向量存储中。
from
uuid
import
uuid4
from
langchain_core.documents
import
Document

document_1 = Document(
    page_content=
"I had chocalate chip pancakes and scrambled eggs for breakfast this morning."
,
    metadata={
"source"
:
"tweet"
},
)

document_2 = Document(
    page_content=
"The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees."
,
    metadata={
"source"
:
"news"
},
)

document_3 = Document(
    page_content=
"Building an exciting new project with LangChain - come check it out!"
,
    metadata={
"source"
:
"tweet"
},
)

document_4 = Document(
    page_content=
"Robbers broke into the city bank and stole $1 million in cash."
,
    metadata={
"source"
:
"news"
},
)

document_5 = Document(
    page_content=
"Wow! That was an amazing movie. I can't wait to see it again."
,
    metadata={
"source"
:
"tweet"
},
)

document_6 = Document(
    page_content=
"Is the new iPhone worth the price? Read this review to find out."
,
    metadata={
"source"
:
"website"
},
)

document_7 = Document(
    page_content=
"The top 10 soccer players in the world right now."
,
    metadata={
"source"
:
"website"
},
)

document_8 = Document(
    page_content=
"LangGraph is the best framework for building stateful, agentic applications!"
,
    metadata={
"source"
:
"tweet"
},
)

document_9 = Document(
    page_content=
"The stock market is down 500 points today due to fears of a recession."
,
    metadata={
"source"
:
"news"
},
)

document_10 = Document(
    page_content=
"I have a bad feeling I am going to get deleted :("
,
    metadata={
"source"
:
"tweet"
},
)

documents = [
    document_1,
    document_2,
    document_3,
    document_4,
    document_5,
    document_6,
    document_7,
    document_8,
    document_9,
    document_10,
]
uuids = [
str
(uuid4())
for
_
in
range
(
len
(documents))]

vector_store.add_documents(documents=documents, ids=uuids)
['31915e2d-55fd-4bfb-ae08-d441252b8e08',
 'dbf6560a-1487-4a6e-8797-245d57874f5b',
 'e991a253-5f37-46ae-850a-82a660e33013',
 '2818c051-5a1a-44cb-9deb-aaaac709f616',
 '91c7ef07-26d1-4319-b48c-9261df9ce8d7',
 'fb258085-6400-4cd7-aa92-fc5e32ca243e',
 'ffea9a9f-460d-4d8d-ba07-c45e9cfa1e33',
 'eb149e29-239a-4e2c-9f99-751cb7207abf',
 '119d4a42-fd6b-433d-842b-1e0be5df81e5',
 '5b099eb0-98fe-40a3-b13a-300c10250960']
从向量存储中删除项目
vector_store.delete(ids=[uuids[-
1
]])
True
查询向量存储空间
创建向量存储并添加相关文件后，您很可能希望在运行链或 Agents 时对其进行查询。
直接查询
相似性搜索
执行简单的相似性搜索并对元数据进行过滤的方法如下：
results = vector_store.similarity_search(
"LangChain provides abstractions to make working with LLMs easy"
,
    k=
2
,
    expr=
'source == "tweet"'
,
# param=...  # Search params for the index type
)
for
res
in
results:
print
(
f"*
{res.page_content}
[
{res.metadata}
]"
)
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1761298048.354308 7886403 fork_posix.cc:71] Other threads are currently calling into gRPC, skipping fork() handlers


* Building an exciting new project with LangChain - come check it out! [{'source': 'tweet', 'pk': 'e991a253-5f37-46ae-850a-82a660e33013'}]
* LangGraph is the best framework for building stateful, agentic applications! [{'source': 'tweet', 'pk': 'eb149e29-239a-4e2c-9f99-751cb7207abf'}]
用分数进行相似性搜索
您也可以使用分数进行搜索：
results = vector_store.similarity_search_with_score(
"Will it be hot tomorrow?"
, k=
1
, expr=
'source == "news"'
)
for
res, score
in
results:
print
(
f"* [SIM=
{score:3f}
]
{res.page_content}
[
{res.metadata}
]"
)
* [SIM=0.893776] The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees. [{'source': 'news', 'pk': 'dbf6560a-1487-4a6e-8797-245d57874f5b'}]
有关使用
Milvus
向量存储时可用的所有搜索选项的完整列表，您可以访问
API 参考
。
通过转化为检索器进行查询
您还可以将向量存储转化为检索器，以便在您的链中更方便地使用。
retriever = vector_store.as_retriever(search_type=
"mmr"
, search_kwargs={
"k"
:
1
})
retriever.invoke(
"Stealing from the bank is a crime"
, expr=
'source == "news"'
)
I0000 00:00:1761298049.275354 7886403 fork_posix.cc:71] Other threads are currently calling into gRPC, skipping fork() handlers





[Document(metadata={'source': 'news', 'pk': '2818c051-5a1a-44cb-9deb-aaaac709f616'}, page_content='Robbers broke into the city bank and stole $1 million in cash.')]
检索增强生成的用法
有关如何将此向量存储用于检索增强生成（RAG）的指南，请参阅此
RAG 指南
。
按用户检索
在构建检索应用程序时，您往往需要考虑到多个用户。这意味着您可能不仅要为一个用户存储数据，还要为许多不同的用户存储数据，而且这些用户不能查看彼此的数据。
Milvus 建议使用
partition_key
来实现多租户，下面是一个例子。
现在，Milvus Lite 不提供分区密钥功能，如果要使用，需要从
docker 或 kubernetes
启动 Milvus 服务器。
from
langchain_core.documents
import
Document

docs = [
    Document(page_content=
"i worked at kensho"
, metadata={
"namespace"
:
"harrison"
}),
    Document(page_content=
"i worked at facebook"
, metadata={
"namespace"
:
"ankush"
}),
]
vectorstore = Milvus.from_documents(
    docs,
    embeddings,
    collection_name=
"partitioned_collection"
,
# Use a different collection name
connection_args={
"uri"
: URI},
# drop_old=True,
partition_key_field=
"namespace"
,
# Use the "namespace" field as the partition key
)
要使用 Partition Key 进行搜索，应在搜索请求的布尔表达式中包含以下任一内容：
search_kwargs={"expr": '<partition_key> == "xxxx"'}
search_kwargs={"expr": '<partition_key> == in ["xxx", "xxx"]'}
请将
<partition_key>
替换为指定为分区密钥的字段名称。
Milvus 会根据指定的分区键更改为一个分区，根据分区键过滤实体，并在过滤后的实体中进行搜索。
# This will only get documents for Ankush
vectorstore.as_retriever(search_kwargs={
"expr"
:
'namespace == "ankush"'
}).invoke(
"where did i work?"
)
[Document(metadata={'namespace': 'ankush', 'pk': 460829372217788296}, page_content='i worked at facebook')]
# This will only get documents for Harrison
vectorstore.as_retriever(search_kwargs={
"expr"
:
'namespace == "harrison"'
}).invoke(
"where did i work?"
)
[Document(metadata={'namespace': 'harrison', 'pk': 460829372217788295}, page_content='i worked at kensho')]
应用程序接口参考
有关详细文档，请访问应用程序接口参考： https://reference.langchain.com/python/integrations/langchain_milvus/