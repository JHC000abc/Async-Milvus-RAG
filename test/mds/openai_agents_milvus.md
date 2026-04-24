Milvus 与 OpenAI Agents 的集成：分步指南
本手册展示了如何创建一个可以通过函数调用使用自然语言查询 Milvus 的 Agents。我们将把 OpenAI 的 Agents 框架与 Milvus 强大的向量搜索功能结合起来，以创建良好的搜索体验。
OpenAI Agents
OpenAI Agents SDK 使您能够在一个轻量级、易于使用且抽象程度极低的软件包中构建 Agents AI 应用程序。这是他们之前的代理实验 Swarm 的生产就绪升级版。Agents SDK 有一套非常小的基元：
代理（Agents），即配备了指令和工具的 LLMs
交接（Handoffs），允许代理委托其他代理执行特定任务
护栏（Guardrails），可对代理的输入进行验证
与 Python 结合使用，这些基元功能强大，足以表达工具和 Agents 之间的复杂关系，让您无需经过陡峭的学习曲线就能构建真实世界的应用程序。此外，SDK 还带有内置跟踪功能，可让您可视化和调试 Agents 流程，并对其进行评估，甚至微调适合您应用的模型。
Milvus
Milvus 是一款高性能、高扩展性的开源向量数据库，可在从笔记本电脑到大型分布式系统等各种环境中高效运行。它既可以开源软件的形式提供，也可以
云服务
的形式提供。
设置和依赖性
首先，我们需要在环境中设置必要的库，并初始化 asyncio 以兼容 Jupyter。
$
pip install openai pymilvus pydantic nest_asyncio
如果使用的是 Google Colab，要启用刚安装的依赖项，可能需要
重启运行时
（点击屏幕顶部的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
import
asyncio
import
nest_asyncio
from
dotenv
import
load_dotenv

load_dotenv()

nest_asyncio.apply()
我们将使用 OpenAI 的模型。请将
api key
OPENAI_API_KEY
作为环境变量。
import
os

os.environ[
"OPENAI_API_KEY"
] =
"sk-***********"
连接 Milvus 并创建 Schema
现在，我们将连接到 Milvus 实例，并为我们的 Collections 创建一个 Schema。该 Schema 将定义数据的结构，包括
作为主键的 ID 字段
一个文本字段，用于存储文档内容
用于存储 BM25 嵌入的稀疏向量字段
Milvus 2.5 中的全文搜索
向量和关键词搜索的统一系统（统一 API）
内置稀疏 BM25 算法（与 Elasticsearch 使用的算法类似，但基于向量）
无需为关键词搜索手动生成 Embeddings
使用 Docker 安装 Milvus
在运行本示例之前，请务必安装 Milvus 并使用 Docker 启动它，请参阅我们的文档 - https://milvus.io/docs/install_standalone-docker.md。
from
pymilvus
import
DataType, FunctionType, MilvusClient

client = MilvusClient(uri=
"http://localhost:19530"
)

schema = client.create_schema()
# Simple schema that handles both text and vectors
schema.add_field(
    field_name=
"id"
, datatype=DataType.INT64, is_primary=
True
, auto_id=
True
)
schema.add_field(
    field_name=
"text"
, datatype=DataType.VARCHAR, max_length=
1000
, enable_analyzer=
True
)
schema.add_field(field_name=
"sparse"
, datatype=DataType.SPARSE_FLOAT_VECTOR)
{'auto_id': False, 'description': '', 'fields': [{'name': 'id', 'description': '', 'type': <DataType.INT64: 5>, 'is_primary': True, 'auto_id': True}, {'name': 'text', 'description': '', 'type': <DataType.VARCHAR: 21>, 'params': {'max_length': 1000, 'enable_analyzer': True}}, {'name': 'sparse', 'description': '', 'type': <DataType.SPARSE_FLOAT_VECTOR: 104>}], 'enable_dynamic_field': False}
为全文搜索设置 BM25
Milvus 通过 BM25 函数支持全文搜索。在此，我们定义了一个函数，该函数将自动把文本数据转换为针对文本搜索优化的稀疏向量表示。
from
pymilvus
import
Function
# Milvus handles tokenization and BM25 conversion
bm25_function = Function(
    name=
"text_bm25_emb"
,
# Function name
input_field_names=[
"text"
],
# Name of the VARCHAR field containing raw text data
output_field_names=[
"sparse"
],
# Name of the SPARSE_FLOAT_VECTOR field reserved to store generated embeddings
function_type=FunctionType.BM25,
)

schema.add_function(bm25_function)
{'auto_id': False, 'description': '', 'fields': [{'name': 'id', 'description': '', 'type': <DataType.INT64: 5>, 'is_primary': True, 'auto_id': True}, {'name': 'text', 'description': '', 'type': <DataType.VARCHAR: 21>, 'params': {'max_length': 1000, 'enable_analyzer': True}}, {'name': 'sparse', 'description': '', 'type': <DataType.SPARSE_FLOAT_VECTOR: 104>, 'is_function_output': True}], 'enable_dynamic_field': False, 'functions': [{'name': 'text_bm25_emb', 'description': '', 'type': <FunctionType.BM25: 1>, 'input_field_names': ['text'], 'output_field_names': ['sparse'], 'params': {}}]}
创建 Collections 并加载样本数据
现在，我们将使用 Schema 和索引参数创建我们的 Collections，然后加载一些有关信息检索和 Milvus 的示例数据。
index_params = client.prepare_index_params()

index_params.add_index(field_name=
"sparse"
, index_type=
"AUTOINDEX"
, metric_type=
"BM25"
)
if
client.has_collection(
"demo"
):
    client.drop_collection(
"demo"
)

client.create_collection(
    collection_name=
"demo"
,
    schema=schema,
    index_params=index_params,
)
## 3. Loading Test Data
client.insert(
"demo"
,
    [
        {
"text"
:
"Information retrieval helps users find relevant documents in large datasets."
},
        {
"text"
:
"Search engines use information retrieval techniques to index and rank web pages."
},
        {
"text"
:
"The core of IR is matching user queries with the most relevant content."
},
        {
"text"
:
"Vector search is revolutionising modern information retrieval systems."
},
        {
"text"
:
"Machine learning improves ranking algorithms in information retrieval."
},
        {
"text"
:
"IR techniques include keyword-based search, semantic search, and vector search."
},
        {
"text"
:
"Boolean retrieval is one of the earliest information retrieval methods."
},
        {
"text"
:
"TF-IDF is a classic method used to score document relevance in IR."
},
        {
"text"
:
"Modern IR systems integrate deep learning for better contextual understanding."
},
        {
"text"
:
"Milvus is an open-source vector database designed for AI-powered search."
},
        {
"text"
:
"Milvus enables fast and scalable similarity search on high-dimensional data."
},
        {
"text"
:
"With Milvus, developers can build applications that support image, text, and video retrieval."
},
        {
"text"
:
"Milvus integrates well with deep learning frameworks like PyTorch and TensorFlow."
},
        {
"text"
:
"The core of Milvus is optimised for approximate nearest neighbour (ANN) search."
},
        {
"text"
:
"Milvus supports hybrid search combining structured and unstructured data."
},
        {
"text"
:
"Large-scale AI applications rely on Milvus for efficient vector retrieval."
},
        {
"text"
:
"Milvus makes it easy to perform high-speed similarity searches."
},
        {
"text"
:
"Cloud-native by design, Milvus scales effortlessly with demand."
},
        {
"text"
:
"Milvus powers applications in recommendation systems, fraud detection, and genomics."
},
        {
"text"
:
"The latest version of Milvus introduces faster indexing and lower latency."
},
        {
"text"
:
"Milvus supports HNSW, IVF_FLAT, and other popular ANN algorithms."
},
        {
"text"
:
"Vector embeddings from models like OpenAI’s CLIP can be indexed in Milvus."
},
        {
"text"
:
"Milvus has built-in support for multi-tenancy in enterprise use cases."
},
        {
"text"
:
"The Milvus community actively contributes to improving its performance."
},
        {
"text"
:
"Milvus integrates with data pipelines like Apache Kafka for real-time updates."
},
        {
"text"
:
"Using Milvus, companies can enhance search experiences with vector search."
},
        {
"text"
:
"Milvus plays a crucial role in powering AI search in medical research."
},
        {
"text"
:
"Milvus integrates with LangChain for advanced RAG pipelines."
},
        {
"text"
:
"Open-source contributors continue to enhance Milvus’ search performance."
},
        {
"text"
:
"Multi-modal search in Milvus enables applications beyond text and images."
},
        {
"text"
:
"Milvus has an intuitive REST API for easy integration."
},
        {
"text"
:
"Milvus’ FAISS and HNSW backends provide flexibility in indexing."
},
        {
"text"
:
"The architecture of Milvus ensures fault tolerance and high availability."
},
        {
"text"
:
"Milvus integrates seamlessly with LLM-based applications."
},
        {
"text"
:
"Startups leverage Milvus to build next-gen AI-powered products."
},
        {
"text"
:
"Milvus Cloud offers a managed solution for vector search at scale."
},
        {
"text"
:
"The future of AI search is being shaped by Milvus and similar vector databases."
},
    ],
)
{'insert_count': 37, 'ids': [456486814660619140, 456486814660619141, 456486814660619142, 456486814660619143, 456486814660619144, 456486814660619145, 456486814660619146, 456486814660619147, 456486814660619148, 456486814660619149, 456486814660619150, 456486814660619151, 456486814660619152, 456486814660619153, 456486814660619154, 456486814660619155, 456486814660619156, 456486814660619157, 456486814660619158, 456486814660619159, 456486814660619160, 456486814660619161, 456486814660619162, 456486814660619163, 456486814660619164, 456486814660619165, 456486814660619166, 456486814660619167, 456486814660619168, 456486814660619169, 456486814660619170, 456486814660619171, 456486814660619172, 456486814660619173, 456486814660619174, 456486814660619175, 456486814660619176], 'cost': 0}
为结构化结果定义输出类型
为了使我们的搜索结果更结构化、更易于使用，我们将定义 Pydantic 模型，指定搜索结果的格式。
from
pydantic
import
BaseModel
# Simplified output model for search results
class
MilvusSearchResult
(
BaseModel
):
id
:
int
text:
str
class
MilvusSearchResults
(
BaseModel
):
    results:
list
[MilvusSearchResult]
    query:
str
创建自定义搜索工具
接下来，我们将创建一个自定义功能工具，以便我们的 Agents 用来搜索 Milvus 数据库。该工具将
接受 Collections 名称、查询文本和限制参数
针对 Milvus Collections 执行 BM25 搜索
以结构化格式返回结果
import
json
from
typing
import
Any
from
pymilvus
import
MilvusClient
from
agents
import
function_tool, RunContextWrapper
@function_tool
async
def
search_milvus_text
(
ctx: RunContextWrapper[
Any
], collection_name:
str
, query_text:
str
, limit:
int
) ->
str
:
"""Search for text documents in a Milvus collection using full text search.

    Args:
        collection_name: Name of the Milvus collection to search.
        query_text: The text query to search for.
        limit: Maximum number of results to return.
    """
try
:
# Initialize Milvus client
client = MilvusClient()
# Prepare search parameters for BM25
search_params = {
"metric_type"
:
"BM25"
,
"params"
: {
"drop_ratio_search"
:
0.2
}}
# Execute search with text query
results = client.search(
            collection_name=collection_name,
            data=[query_text],
            anns_field=
"sparse"
,
            limit=limit,
            search_params=search_params,
            output_fields=[
"text"
],
        )
return
json.dumps(
            {
"results"
: results,
"query"
: query_text,
"collection"
: collection_name}
        )
except
Exception
as
e:
print
(
f"Exception is:
{e}
"
)
return
f"Error searching Milvus:
{
str
(e)}
"
创建 Agents
现在，我们将创建一个可以使用搜索工具的 Agents。我们将指导它如何处理搜索请求，并指定它以我们的结构化格式返回结果。
from
agents
import
Agent, Runner, WebSearchTool, trace
async
def
main
():
    agent = Agent(
        name=
"Milvus Searcher"
,
        instructions=
"""
        You are a helpful agent that can search through Milvus vector database using full text search. Return the results in a structured format.
        """
,
        tools=[
            WebSearchTool(user_location={
"type"
:
"approximate"
,
"city"
:
"New York"
}),
            search_milvus_text,
        ],
        output_type=MilvusSearchResults,
    )
with
trace(
"Milvus search example"
):
        result =
await
Runner.run(
            agent,
"Find documents in the 'demo' collection that are similar to this concept: 'information retrieval'"
,
        )
# print(result.final_output.results)
formatted_results =
"\n"
.join(
f"
{i+
1
}
. ID:
{res.
id
}
, Text:
{res.text}
"
for
i, res
in
enumerate
(result.final_output.results)
        )
print
(
f"Search results:\n
{formatted_results}
"
)
asyncio.run(main())
Search results:
1. ID: 456486814660619146, Text: Boolean retrieval is one of the earliest information retrieval methods.
2. ID: 456486814660619144, Text: Machine learning improves ranking algorithms in information retrieval.
3. ID: 456486814660619143, Text: Vector search is revolutionising modern information retrieval systems.
4. ID: 456486814660619140, Text: Information retrieval helps users find relevant documents in large datasets.
5. ID: 456486814660619141, Text: Search engines use information retrieval techniques to index and rank web pages.