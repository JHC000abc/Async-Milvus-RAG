Milvus 文本嵌入功能与 LangChain 的整合
本指南演示了如何将 Milvus 2.6 的
文本嵌入功能
（也称为数据输入数据输出）与 LangChain 结合使用。该功能允许 Milvus 服务器自动将原始文本转换为向量嵌入，从而简化客户端代码并集中管理 API 密钥。
Milvus
是世界上最先进的开源向量数据库，专门为支持嵌入式相似性搜索和人工智能应用而构建。
LangChain
是一个由大型语言模型（LLMs）驱动的应用开发框架。通过集成 Milvus 的文本嵌入功能，您可以在 LangChain 应用程序中实现更简单、更高效的向量搜索解决方案。
前提条件
在运行本教程之前，请确保已安装以下依赖项：
! pip install --upgrade langchain-milvus langchain-core langchain-openai
如果使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
配置 Milvus 服务器
重要
：文本嵌入功能（数据输入数据输出）功能仅在
Milvus Server
中可用。
Milvus Lite 不支持该功能
。您需要使用部署有 Docker/Kubernetes 的 Milvus 服务器。
在使用文本嵌入功能之前，您需要在 Milvus 服务器上配置嵌入服务提供商的凭据。
在凭据下声明您的密钥：
你可以列出一个或多个 API 密钥--给每个密钥贴上你自创的标签，稍后再参考。
# milvus.yaml
credential:
apikey_dev:
apikey:
<YOUR_OPENAI_API_KEY>
告诉 Milvus 在调用 OpenAI 时使用哪个密钥
在同一文件中，将 OpenAI 提供者指向你希望它使用的标签。
function:
textEmbedding:
providers:
openai:
credential:
apikey_dev
# url: https://api.openai.com/v1/embeddings   # (optional) custom url
有关更多配置方法，请参阅
Milvus Embeddings 功能文档
。
启动 Milvus 服务
确保 Milvus 服务器正在运行，且嵌入功能已启用。可以使用
Docker
或
Kubernetes
部署 Milvus 服务器。注意：
Milvus Lite 不支持文本嵌入功能
。
了解 Embeddings：客户端与服务器端
在深入了解用法之前，我们先来了解两种嵌入方式的区别。
使用 LangChain 的
Embeddings
类进行嵌入（客户端）
在传统的 LangChain 方法中，嵌入生成是通过使用
Embeddings
类
在客户端进行的。您的应用程序需要使用该类的
embed_query
方法来调用嵌入 API，然后将生成的向量存储到 Milvus 中。
from
langchain_openai
import
OpenAIEmbeddings
from
langchain_milvus
import
Milvus
# Generate embedding on client side
embeddings = OpenAIEmbeddings()
vector = embeddings.embed_query(
"Hello, world!"
)
# [0.123, -0.456, ...] A vector of floats
vector_store = Milvus(
    embedding_function=embeddings,
    connection_args={
"uri"
:
"http://localhost:19530"
},
    collection_name=
"traditional_approach_collection"
,
)
序列图：
特征：
客户端直接调用 Embeddings API
需要在客户端管理 API 密钥
数据流：文本 → 客户端 → 嵌入 API → 向量 → Milvus
Milvus 文本嵌入功能（服务器端数据输入数据输出）
Milvus 2.6 的文本嵌入功能（数据输入数据输出）允许 Milvus 服务器自动将原始文本转换为向量嵌入。客户端只需提供文本，Milvus 就会自动处理嵌入生成。
序列图：
特征：
Milvus 服务器调用嵌入式 API
API 密钥在服务器端集中管理
数据流：文本 → Milvus → 嵌入式 API → 向量（存储在 Milvus 中）
两种方法的比较
特点
LangChain 嵌入（客户端）
Milvus 文本嵌入功能（服务器端）
处理位置
客户端应用程序
Milvus 服务器
API 调用
客户端直接调用嵌入 API
Milvus 服务器调用嵌入式 API
API 密钥管理
需要在客户端管理
服务器端集中管理，更安全
代码复杂性
需要在客户端管理 API 密钥和调用
只需在 Milvus 配置中配置一次
使用案例
- 需要客户端控制嵌入过程
- 需要在客户端缓存嵌入结果
- 需要支持多种嵌入模型切换
- 简化客户端代码
- 在服务器端集中管理 API 密钥
- 需要批量处理大量文件
- 希望减少客户端与外部 API 的交互
- 需要与 Milvus 内置功能（如 BM25）相结合
Milvus 版本要求
所有版本（包括 Milvus Lite）
不支持 Milvus Lite
本教程主要介绍 Milvus 服务器端文本嵌入函数（数据输入数据输出）方法
，这是 Milvus 2.6 中引入的新功能，可以大大简化客户端代码并提高安全性。
使用文本嵌入功能
示例 1：仅服务器端嵌入
这是最简单的使用案例，完全依赖 Milvus 服务器生成嵌入。客户端不需要任何嵌入功能。
from
langchain_milvus
import
Milvus
from
langchain_milvus.function
import
TextEmbeddingBuiltInFunction
from
langchain_core.documents
import
Document
# Create Text Embedding Function
text_embedding_func = TextEmbeddingBuiltInFunction(
    input_field_names=
"text"
,
# Input field name (field containing text)
output_field_names=
"vector"
,
# Output field name (field storing vectors)
dim=
1536
,
# Vector dimension (must specify)
params={
"provider"
:
"openai"
,
# Service provider
"model_name"
:
"text-embedding-3-small"
,
# Model name
"credential"
:
"apikey_dev"
,
# Optional: use credential label configured in milvus.yaml
},
)
# Create Milvus vector store
# Note: embedding_function=None, because embedding is done on server side
vector_store = Milvus(
    embedding_function=
None
,
# Do not use client-side embedding
builtin_function=text_embedding_func,
    connection_args={
"uri"
:
"http://localhost:19530"
},
    collection_name=
"my_collection"
,
# consistency_level="Strong",    # Strong consistency level, default is "Session"
auto_id=
True
,
# drop_old=True,  # If you want to drop old collection and create a new one
)
对于
connection_args
：
必须使用 Milvus 服务器
：文本嵌入功能功能只在 Milvus 服务器中提供，不支持 Milvus Lite。
使用服务器 uri，如
http://localhost:19530
（本地 Docker 部署）或
http://your-server:19530
（远程服务器）。
如果使用
Zilliz Cloud
，请使用公共端点作为
uri
，并设置
token
参数。
添加文档时，只需提供文本，无需预先计算向量。Milvus 会自动调用 OpenAI API 生成 Embeddings。
# Add documents (only need to provide text, no need to pre-compute vectors)
documents = [
    Document(page_content=
"Milvus simplifies semantic search through embeddings."
),
    Document(
        page_content=
"Vector embeddings convert text into searchable numeric data."
),
    Document(
        page_content=
"Semantic search helps users find relevant information quickly."
),
]

vector_store.add_documents(documents)
[462726375729313252, 462726375729313253, 462726375729313254]
搜索时，直接使用文本查询，Milvus 会自动将查询文本转换为向量进行搜索。
# Search (directly use text query)
results = vector_store.similarity_search(
    query=
"How does Milvus handle semantic search?"
, k=
2
)
for
doc
in
results:
print
(
f"Content:
{doc.page_content}
"
)
print
(
f"Metadata:
{doc.metadata}
\n"
)
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1765186679.227345 12227536 fork_posix.cc:71] Other threads are currently calling into gRPC, skipping fork() handlers


Content: Milvus simplifies semantic search through embeddings.
Metadata: {'pk': 462726375729313252}

Content: Semantic search helps users find relevant information quickly.
Metadata: {'pk': 462726375729313254}
示例 2：结合文本嵌入和 BM25（混合搜索）
将语义搜索（文本嵌入）和关键词搜索（BM25）结合起来，可以实现更强大的混合搜索功能。语义搜索擅长理解查询意图，而关键词搜索则擅长精确匹配。
from
langchain_milvus
import
Milvus
from
langchain_milvus.function
import
TextEmbeddingBuiltInFunction, BM25BuiltInFunction
# Text Embedding Function (semantic search)
text_embedding_func = TextEmbeddingBuiltInFunction(
    input_field_names=
"text"
,
    output_field_names=
"vector_dense"
,
    dim=
1536
,
    params={
"provider"
:
"openai"
,
"model_name"
:
"text-embedding-3-small"
,
    },
)
# BM25 Function (keyword search)
bm25_func = BM25BuiltInFunction(
    input_field_names=
"text"
,
    output_field_names=
"vector_sparse"
,
)
# Create Milvus vector store
vector_store = Milvus(
    embedding_function=
None
,
    builtin_function=[text_embedding_func, bm25_func],
    connection_args={
"uri"
:
"http://localhost:19530"
},
    vector_field=[
"vector_dense"
,
"vector_sparse"
],
    collection_name=
"hybrid_search_collection"
,
# consistency_level="Strong",    # Strong consistency level, default is "Session"
auto_id=
True
,
# drop_old=True,  # If you want to drop old collection and create a new one
)
# Add documents
documents = [
    Document(page_content=
"Machine learning and artificial intelligence"
),
    Document(page_content=
"The cat sat on the mat"
),
]

vector_store.add_documents(documents)
[462726375729313255, 462726375729313256]
使用
WeightedRanker
可以控制语义搜索和关键词搜索的权重。当密集权重较高时，结果更偏向于语义相似性；当稀疏权重较高时，结果更偏向于关键词匹配。
# Hybrid search, use WeightedRanker to control weights
# 70% semantic search, 30% keyword search
results = vector_store.similarity_search(
    query=
"AI technology"
,
    k=
2
,
    ranker_type=
"weighted"
,
    ranker_params={
"weights"
: [
0.7
,
0.3
]},
)
# If you want to be more biased towards keyword matching, you can adjust weights
# 30% semantic search, 70% keyword search
results_keyword_focused = vector_store.similarity_search(
    query=
"cat mat"
,
    k=
2
,
    ranker_type=
"weighted"
,
    ranker_params={
"weights"
: [
0.3
,
0.7
]},
)
results
[Document(metadata={'pk': 462726375729313255}, page_content='Machine learning and artificial intelligence'),
 Document(metadata={'pk': 462726375729313256}, page_content='The cat sat on the mat')]
results_keyword_focused
[Document(metadata={'pk': 462726375729313256}, page_content='The cat sat on the mat'),
 Document(metadata={'pk': 462726375729313255}, page_content='Machine learning and artificial intelligence')]
总结
恭喜你！您已经学会了如何在 LangChain 中使用 Milvus 的文本嵌入功能（数据输入数据输出）。通过将嵌入生成转移到服务器端，您可以简化客户端代码，集中管理 API 密钥，并轻松实现混合搜索。结合文本嵌入功能和 BM25，Milvus 可为您提供强大的向量搜索功能。