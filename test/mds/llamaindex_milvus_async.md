使用 Milvus 和 LlamaIndex 异步 API 的 RAG
本教程演示如何使用
LlamaIndex
和
Milvus
为 RAG 构建异步文档处理管道。LlamaIndex 提供了一种像 Milvus 一样处理文档并将其存储在向量数据库中的方法。通过利用 LlamaIndex 的异步 API 和 Milvus Python 客户端库，我们可以提高管道的吞吐量，从而高效地处理大量数据并编制索引。
在本教程中，我们将首先从高层介绍使用异步方法利用 LlamaIndex 和 Milvus 构建 RAG，然后介绍低层方法的使用以及同步和异步的性能比较。
开始之前
本页中的代码片段需要 pymilvus 和 llamaindex 依赖项。您可以使用以下命令安装它们：
$ pip install -U pymilvus llama-index-vector-stores-milvus llama-index nest-asyncio
如果您使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重新启动运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重新启动会话"）。
我们将使用 OpenAI 的模型。您应该将
api key
OPENAI_API_KEY
作为环境变量。
import
os

os.environ[
"OPENAI_API_KEY"
] =
"sk-***********"
如果使用的是 Jupyter Notebook，则需要在运行异步代码前运行这行代码。
import
nest_asyncio

nest_asyncio.apply()
准备数据
您可以使用以下命令下载示例数据：
$
mkdir
-p
'data/'
$ wget
'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt'
-O
'data/paul_graham_essay.txt'
$ wget
'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/10k/uber_2021.pdf'
-O
'data/uber_2021.pdf'
使用异步处理构建 RAG
本节将介绍如何构建一个能以异步方式处理文档的 RAG 系统。
导入必要的库，定义 Milvus URI 和 Embeddings 的尺寸。
import
asyncio
import
random
import
time
from
llama_index.core.schema
import
TextNode, NodeRelationship, RelatedNodeInfo
from
llama_index.core.vector_stores
import
VectorStoreQuery
from
llama_index.vector_stores.milvus
import
MilvusVectorStore

URI =
"http://localhost:19530"
DIM =
768
如果你有大规模的数据，你可以在
docker 或 kubernetes
上建立一个性能良好的 Milvus 服务器。在此设置中，请使用服务器 URI，例如
http://localhost:19530
，作为您的
uri
。
如果你想使用
Zilliz Cloud
（Milvus 的完全托管云服务），请调整
uri
和
token
，它们与 Zilliz Cloud 中的
公共端点和 Api 密钥
相对应。
在复杂系统（如网络通信）中，异步处理比同步处理更能提高性能。所以我们认为 Milvus-Lite 不适合使用异步接口，因为使用的场景并不适合。
定义一个初始化函数，我们可以再次使用它来重建 Milvus Collections。
def
init_vector_store
():
return
MilvusVectorStore(
        uri=URI,
# token=TOKEN,
dim=DIM,
        collection_name=
"test_collection"
,
        embedding_field=
"embedding"
,
        id_field=
"id"
,
        similarity_metric=
"COSINE"
,
        consistency_level=
"Bounded"
,
# Supported values are (`"Strong"`, `"Session"`, `"Bounded"`, `"Eventually"`). See https://milvus.io/docs/consistency.md#Consistency-Level for more details.
overwrite=
True
,
# To overwrite the collection if it already exists
)


vector_store = init_vector_store()
2025-01-24 20:04:39,414 [DEBUG][_create_connection]: Created new connection using: faa8be8753f74288bffc7e6d38942f8a (async_milvus_client.py:600)
使用 SimpleDirectoryReader 从文件
paul_graham_essay.txt
中封装一个 LlamaIndex 文档对象。
from
llama_index.core
import
SimpleDirectoryReader
# load documents
documents = SimpleDirectoryReader(
    input_files=[
"./data/paul_graham_essay.txt"
]
).load_data()
print
(
"Document ID:"
, documents[
0
].doc_id)
Document ID: 41a6f99c-489f-49ff-9821-14e2561140eb
在本地实例化一个 Hugging Face 嵌入模型。使用本地模型可以避免在异步数据插入过程中达到 API 速率限制的风险，因为并发 API 请求会迅速增加并耗尽你在公共 API 中的预算。不过，如果您的速率限制较高，您可以选择使用远程模型服务来代替。
from
llama_index.embeddings.huggingface
import
HuggingFaceEmbedding


embed_model = HuggingFaceEmbedding(model_name=
"BAAI/bge-base-en-v1.5"
)
创建索引并插入文档。
我们将
use_async
设置为
True
，以启用异步插入模式。
# Create an index over the documents
from
llama_index.core
import
VectorStoreIndex, StorageContext

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    embed_model=embed_model,
    use_async=
True
,
)
初始化 LLM。
from
llama_index.llms.openai
import
OpenAI

llm = OpenAI(model=
"gpt-3.5-turbo"
)
在构建查询引擎时，也可以将
use_async
参数设置为
True
，以启用异步搜索。
query_engine = index.as_query_engine(use_async=
True
, llm=llm)
response =
await
query_engine.aquery(
"What did the author learn?"
)
print
(response)
The author learned that the field of artificial intelligence, as practiced at the time, was not as promising as initially believed. The approach of using explicit data structures to represent concepts in AI was not effective in achieving true understanding of natural language. This realization led the author to shift his focus towards Lisp and eventually towards exploring the field of art.
探索异步 API
在本节中，我们将介绍较低级别的 API 使用，并比较同步和异步运行的性能。
异步添加
重新初始化向量存储。
vector_store = init_vector_store()
2025-01-24 20:07:38,727 [DEBUG][_create_connection]: Created new connection using: 5e0d130f3b644555ad7ea6b8df5f1fc2 (async_milvus_client.py:600)
让我们定义一个节点生成函数，用于为索引生成大量测试节点。
def
random_id
():
    random_num_str =
""
for
_
in
range
(
16
):
        random_digit =
str
(random.randint(
0
,
9
))
        random_num_str += random_digit
return
random_num_str
def
produce_nodes
(
num_adding
):
    node_list = []
for
i
in
range
(num_adding):
        node = TextNode(
            id_=random_id(),
            text=
f"n
{i}
_text"
,
            embedding=[
0.5
] * (DIM -
1
) + [random.random()],
            relationships={NodeRelationship.SOURCE: RelatedNodeInfo(node_id=
f"n
{i+
1
}
"
)},
        )
        node_list.append(node)
return
node_list
定义一个 aync 函数，将文档添加到向量存储中。我们在 Milvus 向量存储实例中使用
async_add()
函数。
async
def
async_add
(
num_adding
):
    node_list = produce_nodes(num_adding)
    start_time = time.time()
    tasks = []
for
i
in
range
(num_adding):
        sub_nodes = node_list[i]
        task = vector_store.async_add([sub_nodes])
# use async_add()
tasks.append(task)
    results =
await
asyncio.gather(*tasks)
    end_time = time.time()
return
end_time - start_time
add_counts = [
10
,
100
,
1000
]
获取事件循环。
loop = asyncio.get_event_loop()
异步将文档添加到向量存储中。
for
count
in
add_counts:
async
def
measure_async_add
():
        async_time =
await
async_add(count)
print
(
f"Async add for
{count}
took
{async_time:
.2
f}
seconds"
)
return
async_time

    loop.run_until_complete(measure_async_add())
Async add for 10 took 0.19 seconds
Async add for 100 took 0.48 seconds
Async add for 1000 took 3.22 seconds
vector_store = init_vector_store()
2025-01-24 20:07:45,554 [DEBUG][_create_connection]: Created new connection using: b14dde8d6d24489bba26a907593f692d (async_milvus_client.py:600)
与同步添加比较
定义一个同步添加函数。然后测量相同条件下的运行时间。
def
sync_add
(
num_adding
):
    node_list = produce_nodes(num_adding)
    start_time = time.time()
for
node
in
node_list:
        result = vector_store.add([node])
    end_time = time.time()
return
end_time - start_time
for
count
in
add_counts:
    sync_time = sync_add(count)
print
(
f"Sync add for
{count}
took
{sync_time:
.2
f}
seconds"
)
Sync add for 10 took 0.56 seconds
Sync add for 100 took 5.85 seconds
Sync add for 1000 took 62.91 seconds
结果显示，同步添加过程比异步添加过程慢得多。
异步搜索
在运行搜索之前，重新初始化向量存储并添加一些文档。
vector_store = init_vector_store()
node_list = produce_nodes(num_adding=
1000
)
inserted_ids = vector_store.add(node_list)
2025-01-24 20:08:57,982 [DEBUG][_create_connection]: Created new connection using: 351dc7ea4fb14d4386cfab02621ab7d1 (async_milvus_client.py:600)
定义一个异步搜索函数。我们使用 Milvus 向量存储实例中的
aquery()
函数。
async
def
async_search
(
num_queries
):
    start_time = time.time()
    tasks = []
for
_
in
range
(num_queries):
        query = VectorStoreQuery(
            query_embedding=[
0.5
] * (DIM -
1
) + [
0.6
], similarity_top_k=
3
)
        task = vector_store.aquery(query=query)
# use aquery()
tasks.append(task)
    results =
await
asyncio.gather(*tasks)
    end_time = time.time()
return
end_time - start_time
query_counts = [
10
,
100
,
1000
]
从 Milvus 存储中进行异步搜索。
for
count
in
query_counts:
async
def
measure_async_search
():
        async_time =
await
async_search(count)
print
(
f"Async search for
{count}
queries took
{async_time:
.2
f}
seconds"
)
return
async_time

    loop.run_until_complete(measure_async_search())
Async search for 10 queries took 0.55 seconds
Async search for 100 queries took 1.39 seconds
Async search for 1000 queries took 8.81 seconds
与同步搜索比较
定义一个同步搜索函数。然后测量相同条件下的运行时间。
def
sync_search
(
num_queries
):
    start_time = time.time()
for
_
in
range
(num_queries):
        query = VectorStoreQuery(
            query_embedding=[
0.5
] * (DIM -
1
) + [
0.6
], similarity_top_k=
3
)
        result = vector_store.query(query=query)
    end_time = time.time()
return
end_time - start_time
for
count
in
query_counts:
    sync_time = sync_search(count)
print
(
f"Sync search for
{count}
queries took
{sync_time:
.2
f}
seconds"
)
Sync search for 10 queries took 3.29 seconds
Sync search for 100 queries took 30.80 seconds
Sync search for 1000 queries took 308.80 seconds
结果显示，同步搜索过程比异步搜索过程慢得多。