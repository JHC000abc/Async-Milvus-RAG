LangChain Milvus 集成中的异步函数
本教程探讨如何利用
langchain-milvus
中的异步函数构建高性能应用程序。通过使用异步方法，您可以显著提高应用程序的吞吐量和响应速度，尤其是在处理大规模检索时。无论您是要构建实时推荐系统、在应用程序中实现语义搜索，还是要创建 RAG（检索增强生成）管道，async 操作符都能帮助您更高效地处理并发请求。高性能向量数据库 Milvus 与 LangChain 强大的 LLM 抽象相结合，可以为构建可扩展的人工智能应用奠定坚实的基础。
异步 API 概述
langchain-milvus 提供了全面的异步操作支持，显著提高了大规模并发场景下的性能。异步 API 与同步 API 保持一致的界面设计。
核心异步函数
要在 langchain-milvus 中使用异步操作，只需在方法名称中添加
a
前缀即可。这样，在处理并发检索请求时，可以更好地利用资源，提高吞吐量。
操作符类型
同步方法
异步方法
说明
添加文本
add_texts()
aadd_texts()
向向量存储中添加文本
添加文档
add_documents()
aadd_documents()
向向量存储中添加文档
添加嵌入向量
add_embeddings()
aadd_embeddings()
添加嵌入向量
相似性搜索
similarity_search()
asimilarity_search()
文本语义搜索
向量搜索
similarity_search_by_vector()
asimilarity_search_by_vector()
通过向量进行语义搜索
带分数搜索
similarity_search_with_score()
asimilarity_search_with_score()
通过文本进行语义搜索并返回相似度得分
带分数的向量搜索
similarity_search_with_score_by_vector()
asimilarity_search_with_score_by_vector()
通过向量进行语义搜索并返回相似性得分
多样性搜索
max_marginal_relevance_search()
amax_marginal_relevance_search()
MMR搜索（返回相似度，同时优化多样性）
向量多样性搜索
max_marginal_relevance_search_by_vector()
amax_marginal_relevance_search_by_vector()
按向量进行 MMR 搜索
删除操作符
delete()
adelete()
删除文件
增加操作符
upsert()
aupsert()
倒插（如果已有则更新，否则插入）文件
元数据搜索
search_by_metadata()
asearch_by_metadata()
元数据过滤查询
获取主键
get_pks()
aget_pks()
通过表达式获取主键
从文本创建
from_texts()
afrom_texts()
从文本创建向量存储
有关这些函数的更多详细信息，请参阅
API 参考资料
。
性能优势
在处理大量并发请求时，异步操作符可显著提高性能，尤其适用于以下情况：
批量文档处理
高并发搜索场景
生产型 RAG 应用程序
大规模数据导入/导出
在本教程中，我们将通过同步操作和异步操作的详细比较来展示这些性能优势，告诉您如何在应用程序中利用异步 API 获得最佳性能。
开始之前
本页面上的代码片段需要以下依赖项：
! pip install -U pymilvus langchain-milvus langchain langchain-core langchain-openai langchain-text-splitters nest-asyncio
如果您使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重新启动运行时
（点击屏幕顶部的 "运行时 "菜单，从下拉菜单中选择 "重新启动会话"）。
我们将使用 OpenAI 模型。您应将
api key
OPENAI_API_KEY
作为环境变量：
import
os

os.environ[
"OPENAI_API_KEY"
] =
"sk-***********"
如果使用的是 Jupyter Notebook，则需要在运行异步代码前运行这行代码：
import
nest_asyncio

nest_asyncio.apply()
探索异步 API 和性能比较
现在，让我们深入了解使用 langchain-milvus 进行同步操作和异步操作的性能比较。
首先，导入必要的库：
import
asyncio
import
random
import
time
from
langchain_core.documents
import
Document
from
langchain_openai
import
OpenAIEmbeddings
from
langchain_milvus
import
Milvus
# Define the Milvus URI
URI =
"http://localhost:19530"
设置测试函数
让我们创建辅助函数来生成测试数据：
def
random_id
():
"""Generate a random string ID"""
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
generate_test_documents
(
num_docs
):
"""Generate test documents for performance testing"""
docs = []
for
i
in
range
(num_docs):
        content = (
f"This is test document
{i}
with some random content:
{random.random()}
"
)
        metadata = {
"id"
:
f"doc_
{i}
"
,
"score"
: random.random(),
"category"
:
f"cat_
{i %
5
}
"
,
        }
        doc = Document(page_content=content, metadata=metadata)
        docs.append(doc)
return
docs
初始化向量存储
在运行性能测试之前，我们需要建立一个干净的 Milvus 向量存储。该函数确保我们每次测试都从一个全新的 Collections 开始，消除先前数据的任何干扰：
def
init_vector_store
():
"""Initialize and return a fresh vector store for testing"""
return
Milvus(
        embedding_function=OpenAIEmbeddings(),
        collection_name=
"langchain_perf_test"
,
        connection_args={
"uri"
: URI},
        auto_id=
True
,
        drop_old=
True
,
# Always start with a fresh collection
)
异步与同步添加文档
现在，让我们比较一下同步与异步添加文档的性能。这些函数将帮助我们衡量在向量存储中添加多个文档时，异步操作能快多少。异步版本为每个文档添加创建任务并并发运行，而同步版本则逐个处理文档：
async
def
async_add
(
milvus_store, num_adding
):
"""Add documents asynchronously and measure the time"""
docs = generate_test_documents(num_adding)
    start_time = time.time()
    tasks = []
for
doc
in
docs:
# Create tasks for each document addition
task = milvus_store.aadd_documents([doc])
        tasks.append(task)
    results =
await
asyncio.gather(*tasks)
    end_time = time.time()
return
end_time - start_time
def
sync_add
(
milvus_store, num_adding
):
"""Add documents synchronously and measure the time"""
docs = generate_test_documents(num_adding)
    start_time = time.time()
for
doc
in
docs:
        result = milvus_store.add_documents([doc])
    end_time = time.time()
return
end_time - start_time
现在，让我们用不同的文档数量来执行性能测试，看看实际的性能差异。我们将使用不同的负载进行测试，以了解异步操作与同步操作相比如何扩展。测试将测量两种方法的执行时间，并帮助展示异步操作的性能优势：
add_counts = [
10
,
100
]
# Get the event loop
loop = asyncio.get_event_loop()
# Create a new vector store for testing
milvus_store = init_vector_store()
# Test async document addition
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
async_add(milvus_store, count)
print
(
f"Async add for
{count}
documents took
{async_time:
.2
f}
seconds"
)
return
async_time

    loop.run_until_complete(measure_async_add())
# Reset vector store for sync tests
milvus_store = init_vector_store()
# Test sync document addition
for
count
in
add_counts:
    sync_time = sync_add(milvus_store, count)
print
(
f"Sync add for
{count}
documents took
{sync_time:
.2
f}
seconds"
)
2025-06-05 10:44:12,274 [DEBUG][_create_connection]: Created new connection using: dd5f77bb78964c079da42c2446b03bf6 (async_milvus_client.py:599)


Async add for 10 documents took 1.74 seconds


2025-06-05 10:44:16,940 [DEBUG][_create_connection]: Created new connection using: 8b13404a78654cdd9b790371eb44e427 (async_milvus_client.py:599)


Async add for 100 documents took 2.77 seconds
Sync add for 10 documents took 5.36 seconds
Sync add for 100 documents took 65.60 seconds
异步与同步：搜索
为了进行搜索性能比较，我们需要先填充向量存储。通过创建多个并发搜索查询并比较同步和异步方法的执行时间，以下函数将帮助我们衡量搜索性能：
def
populate_vector_store
(
milvus_store, num_docs=
1000
):
"""Populate the vector store with test documents"""
docs = generate_test_documents(num_docs)
    milvus_store.add_documents(docs)
return
docs
async
def
async_search
(
milvus_store, num_queries
):
"""Perform async searches and measure the time"""
start_time = time.time()
    tasks = []
for
i
in
range
(num_queries):
        query =
f"test document
{i %
50
}
"
task = milvus_store.asimilarity_search(query=query, k=
3
)
        tasks.append(task)
    results =
await
asyncio.gather(*tasks)
    end_time = time.time()
return
end_time - start_time
def
sync_search
(
milvus_store, num_queries
):
"""Perform sync searches and measure the time"""
start_time = time.time()
for
i
in
range
(num_queries):
        query =
f"test document
{i %
50
}
"
result = milvus_store.similarity_search(query=query, k=
3
)
    end_time = time.time()
return
end_time - start_time
现在让我们运行全面的搜索性能测试，看看异步操作与同步操作相比如何扩展。我们将使用不同的查询量进行测试，以展示异步操作的性能优势，尤其是当并发操作的数量增加时：
# Initialize and populate the vector store
milvus_store = init_vector_store()
populate_vector_store(milvus_store,
1000
)

query_counts = [
10
,
100
]
# Test async search
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
async_search(milvus_store, count)
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
# Test sync search
for
count
in
query_counts:
    sync_time = sync_search(milvus_store, count)
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
2025-06-05 10:45:28,131 [DEBUG][_create_connection]: Created new connection using: 851824591c64415baac843e676e78cdd (async_milvus_client.py:599)


Async search for 10 queries took 2.31 seconds
Async search for 100 queries took 3.72 seconds
Sync search for 10 queries took 6.07 seconds
Sync search for 100 queries took 54.22 seconds
异步与同步删除
删除操作是异步操作可以显著提高性能的另一个关键方面。让我们创建函数来测量同步和异步删除操作的性能差异。这些测试将有助于展示异步操作如何更高效地处理批量删除：
async
def
async_delete
(
milvus_store, num_deleting
):
"""Delete documents asynchronously and measure the time"""
start_time = time.time()
    tasks = []
for
i
in
range
(num_deleting):
        expr =
f"id == 'doc_
{i}
'"
task = milvus_store.adelete(expr=expr)
        tasks.append(task)
    results =
await
asyncio.gather(*tasks)
    end_time = time.time()
return
end_time - start_time
def
sync_delete
(
milvus_store, num_deleting
):
"""Delete documents synchronously and measure the time"""
start_time = time.time()
for
i
in
range
(num_deleting):
        expr =
f"id == 'doc_
{i}
'"
result = milvus_store.delete(expr=expr)
    end_time = time.time()
return
end_time - start_time
现在，让我们执行删除性能测试，量化性能差异。我们将从一个填充了测试数据的全新向量存储开始，然后使用同步和异步两种方法执行删除操作：
delete_counts = [
10
,
100
]
# Initialize and populate the vector store
milvus_store = init_vector_store()
populate_vector_store(milvus_store,
1000
)
# Test async delete
for
count
in
delete_counts:
async
def
measure_async_delete
():
        async_time =
await
async_delete(milvus_store, count)
print
(
f"Async delete for
{count}
operations took
{async_time:
.2
f}
seconds"
)
return
async_time

    loop.run_until_complete(measure_async_delete())
# Reset and repopulate the vector store for sync tests
milvus_store = init_vector_store()
populate_vector_store(milvus_store,
1000
)
# Test sync delete
for
count
in
delete_counts:
    sync_time = sync_delete(milvus_store, count)
print
(
f"Sync delete for
{count}
operations took
{sync_time:
.2
f}
seconds"
)
2025-06-05 10:46:57,211 [DEBUG][_create_connection]: Created new connection using: 504e9ce3be92411e87077971c82baca2 (async_milvus_client.py:599)


Async delete for 10 operations took 0.58 seconds


2025-06-05 10:47:12,309 [DEBUG][_create_connection]: Created new connection using: 22c1513b444e4c40936e2176d7a1a154 (async_milvus_client.py:599)


Async delete for 100 operations took 0.61 seconds
Sync delete for 10 operations took 2.82 seconds
Sync delete for 100 operations took 29.21 seconds
结论
本教程展示了使用 LangChain 和 Milvus 进行异步操作的显著性能优势。我们比较了同步和异步版本的添加、搜索和删除操作，展示了异步操作如何大幅提高速度，尤其是在大批量操作时。
主要启示
在执行许多可以并行运行的单个操作时，异步操作能带来最大收益
对于产生较高吞吐量的工作负载，同步操作和非同步操作之间的性能差距会拉大
异步操作可充分利用机器的计算能力
在使用 LangChain 和 Milvus 构建生产型 RAG 应用程序时，如果对性能有要求，尤其是并发操作，请考虑使用 async API。