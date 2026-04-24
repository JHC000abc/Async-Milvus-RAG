使用 Milvus 和 LlamaIndex 混合搜索的 RAG
混合搜索利用语义检索和关键字匹配的优势，提供更准确、与上下文更相关的结果。通过结合语义检索和关键词匹配的优势，混合搜索在复杂的信息检索任务中尤为有效。
本笔记本演示了如何在
LlamaIndex
RAG 管道中使用 Milvus 进行混合搜索。我们将从推荐的默认混合搜索（语义 + BM25）开始，然后探索其他可供选择的稀疏嵌入方法和自定义混合 Reranker。
先决条件
安装依赖项
在开始之前，请确保您已安装以下依赖项：
$
pip install llama-index-vector-stores-milvus
$
pip install llama-index-embeddings-openai
$
pip install llama-index-llms-openai
如果您使用的是 Google Colab，可能需要
重新启动运行时
（导航至界面顶部的 "运行时 "菜单，然后从下拉菜单中选择 "重新启动会话"）。
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
Milvus Standalone、Milvus Distributed 和 Zilliz Cloud 目前支持全文搜索，但 Milvus Lite 尚不支持全文搜索（计划今后实施）。请联系 support@zilliz.com 了解更多信息。
URI =
"http://localhost:19530"
# TOKEN = ""
加载示例数据
运行以下命令将示例文档下载到 "data/paul_graham "目录：
$
mkdir
-p
'data/paul_graham/'
$
wget
'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt'
-O
'data/paul_graham/paul_graham_essay.txt'
然后使用
SimpleDirectoryReaderLoad
加载保罗-格雷厄姆的论文 "What I Worked On"：
from
llama_index.core
import
SimpleDirectoryReader

documents = SimpleDirectoryReader(
"./data/paul_graham/"
).load_data()
# Let's take a look at the first document
print
(
"Example document:\n"
, documents[
0
])
Example document:
 Doc ID: f9cece8c-9022-46d8-9d0e-f29d70e1dbbe
Text: What I Worked On  February 2021  Before college the two main
things I worked on, outside of school, were writing and programming. I
didn't write essays. I wrote what beginning writers were supposed to
write then, and probably still are: short stories. My stories were
awful. They had hardly any plot, just characters with strong feelings,
which I ...
使用 BM25 进行混合搜索
本节介绍如何使用 BM25 执行混合搜索。首先，我们将初始化
MilvusVectorStore
并为示例文档创建索引。默认配置使用
来自默认嵌入模型（OpenAI's
text-embedding-ada-002
）的高密度嵌入。
如果 enable_sparse 为 True，则使用 BM25 进行全文搜索
如果启用混合搜索，则使用 k=60 的 RRFRanker 来合并搜索结果
# Create an index over the documnts
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
dim=
1536
,
# vector dimension depends on the embedding model
enable_sparse=
True
,
# enable the default full-text search using BM25
overwrite=
True
,
# drop the collection if it already exists
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
2025-04-17 03:38:16,645 [DEBUG][_create_connection]: Created new connection using: cf0f4df74b18418bb89ec512063c1244 (async_milvus_client.py:547)
Sparse embedding function is not provided, using default.
Default sparse embedding function: BM25BuiltInFunction(input_field_names='text', output_field_names='sparse_embedding').
以下是关于在
MilvusVectorStore
中配置密集字段和稀疏字段的参数的更多信息：
密集字段
enable_dense (bool)
:布尔标志，用于启用或禁用密集嵌入。默认为 True。
dim (int, optional)
:Collections 的嵌入向量维度。
embedding_field (str, optional)
:Collections 的密集嵌入字段名称，默认为 DEFAULT_EMBEDDING_KEY。
index_config (dict, optional)
:用于构建密集嵌入索引的配置。默认为 "无"。
search_config (dict, optional)
:用于搜索 Milvus 密集索引的配置。注意必须与
index_config
指定的索引类型兼容。默认为无。
similarity_metric (str, optional)
:用于高密度 Embeddings 的相似度量，目前支持 IP、COSINE 和 L2。
稀疏字段
enable_sparse (bool)
:布尔标志，用于启用或禁用稀疏嵌入。默认为假。
sparse_embedding_field (str)
:稀疏嵌入字段的名称，默认为 DEFAULT_SPARSE_EMBEDDING_KEY。
sparse_embedding_function (Union[BaseSparseEmbeddingFunction, BaseMilvusBuiltInFunction], optional)
:如果 enable_sparse 为 True，则应提供此对象将文本转换为稀疏嵌入。如果为 None，则将使用默认的稀疏嵌入函数（BM25BuiltInFunction），或使用 BGEM3SparseEmbedding 给定的现有 Collections（无内置函数）。
sparse_index_config (dict, optional)
:用于构建稀疏嵌入索引的配置。默认为 "无"。
要在查询阶段启用混合搜索，请将
vector_store_query_mode
设置为 "hybrid"。这将对语义搜索和全文搜索的搜索结果进行合并和 Rerankers。让我们用一个查询示例进行测试："作者在 Viaweb 学到了什么？
import
textwrap

query_engine = index.as_query_engine(
    vector_store_query_mode=
"hybrid"
, similarity_top_k=
5
)
response = query_engine.query(
"What did the author learn at Viaweb?"
)
print
(textwrap.fill(
str
(response),
100
))
The author learned about retail, the importance of user feedback, and the significance of growth
rate as the ultimate test of a startup at Viaweb.
自定义文本分析器
分析器在全文搜索中发挥着重要作用，它可以将句子分解成词块，并执行词法处理，如词干和停止词删除。它们通常针对特定语言。有关详细信息，请参阅
Milvus 分析器指南
。
Milvus 支持两种类型的分析器：
内置分析器
和
自定义分析器
。默认情况下，如果
enable_sparse
设置为 True，
MilvusVectorStore
会使用
BM25BuiltInFunction
的默认配置，采用标准内置分析器，根据标点符号标记文本。
要使用不同的分析器或自定义现有的分析器，可以在构建
BM25BuiltInFunction
时为
analyzer_params
参数提供值。然后，在
MilvusVectorStore
中将此函数设置为
sparse_embedding_function
。
from
llama_index.vector_stores.milvus.utils
import
BM25BuiltInFunction

bm25_function = BM25BuiltInFunction(
    analyzer_params={
"tokenizer"
:
"standard"
,
"filter"
: [
"lowercase"
,
# Built-in filter
{
"type"
:
"length"
,
"max"
:
40
},
# Custom cap size of a single token
{
"type"
:
"stop"
,
"stop_words"
: [
"of"
,
"to"
]},
# Custom stopwords
],
    },
    enable_match=
True
,
)

vector_store = MilvusVectorStore(
    uri=URI,
# token=TOKEN,
dim=
1536
,
    enable_sparse=
True
,
    sparse_embedding_function=bm25_function,
# BM25 with custom analyzer
overwrite=
True
,
)
2025-04-17 03:38:48,085 [DEBUG][_create_connection]: Created new connection using: 61afd81600cb46ee89f887f16bcbfe55 (async_milvus_client.py:547)
与其他稀疏嵌入的混合搜索
除了将语义搜索与 BM25 结合起来，Milvus 还支持使用稀疏嵌入函数（如
BGE-M3
）进行混合搜索。下面的示例使用内置的
BGEM3SparseEmbeddingFunction
生成稀疏嵌入。
首先，我们需要安装
FlagEmbedding
软件包：
$
pip install -q FlagEmbedding
然后，让我们使用用于 densen embedding 的默认 OpenAI 模型和用于稀疏嵌入的内置 BGE-M3 来构建向量存储和索引：
from
llama_index.vector_stores.milvus.utils
import
BGEM3SparseEmbeddingFunction

vector_store = MilvusVectorStore(
    uri=URI,
# token=TOKEN,
dim=
1536
,
    enable_sparse=
True
,
    sparse_embedding_function=BGEM3SparseEmbeddingFunction(),
    overwrite=
True
,
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
Fetching 30 files: 100%|██████████| 30/30 [00:00<00:00, 68871.99it/s]
2025-04-17 03:39:02,074 [DEBUG][_create_connection]: Created new connection using: ff4886e2f8da44e08304b748d9ac9b51 (async_milvus_client.py:547)
Chunks: 100%|██████████| 1/1 [00:00<00:00,  1.07it/s]
现在，让我们用一个示例问题执行混合搜索查询：
query_engine = index.as_query_engine(
    vector_store_query_mode=
"hybrid"
, similarity_top_k=
5
)
response = query_engine.query(
"What did the author learn at Viaweb??"
)
print
(textwrap.fill(
str
(response),
100
))
Chunks: 100%|██████████| 1/1 [00:00<00:00, 17.29it/s]


The author learned about retail, the importance of user feedback, the value of growth rate in a
startup, the significance of pricing strategy, the benefits of working on things that weren't
prestigious, and the challenges and rewards of running a startup.
自定义稀疏嵌入功能
您也可以自定义稀疏嵌入函数，只要它继承自
BaseSparseEmbeddingFunction
，包括以下方法：
encode_queries
:该方法将文本转换为稀疏嵌入列表，用于查询。
encode_documents
:该方法将文本转换为稀疏嵌入列表，用于文档。
每个方法的输出都应遵循稀疏嵌入的格式，即字典列表。每个字典应该有一个代表维度的键（整数）和一个对应的值（浮点数），代表嵌入在该维度中的大小（例如，{1: 0.5, 2: 0.3}）。
例如，下面是使用 BGE-M3 实现的自定义稀疏嵌入函数：
from
FlagEmbedding
import
BGEM3FlagModel
from
typing
import
List
from
llama_index.vector_stores.milvus.utils
import
BaseSparseEmbeddingFunction
class
ExampleEmbeddingFunction
(
BaseSparseEmbeddingFunction
):
def
__init__
(
self
):
self
.model = BGEM3FlagModel(
"BAAI/bge-m3"
, use_fp16=
False
)
def
encode_queries
(
self, queries:
List
[
str
]
):
        outputs =
self
.model.encode(
            queries,
            return_dense=
False
,
            return_sparse=
True
,
            return_colbert_vecs=
False
,
        )[
"lexical_weights"
]
return
[
self
._to_standard_dict(output)
for
output
in
outputs]
def
encode_documents
(
self, documents:
List
[
str
]
):
        outputs =
self
.model.encode(
            documents,
            return_dense=
False
,
            return_sparse=
True
,
            return_colbert_vecs=
False
,
        )[
"lexical_weights"
]
return
[
self
._to_standard_dict(output)
for
output
in
outputs]
def
_to_standard_dict
(
self, raw_output
):
        result = {}
for
k
in
raw_output:
            result[
int
(k)] = raw_output[k]
return
result
自定义混合 Reranker
Milvus 支持两种
重排策略
：互惠排名融合（RRF）和加权评分。
MilvusVectorStore
混合搜索的默认排序器是 k=60 的 RRF。要自定义混合排名器，请修改以下参数：
hybrid_ranker (str)
:指定混合搜索查询中使用的排名器类型。目前只支持 ["RRFRanker", "WeightedRanker"]。默认为 "RRFRanker"。
hybrid_ranker_params (dict, optional)
:混合排名器的配置参数。该字典的结构取决于所使用的特定排名器：
对于 "RRFRanker"，它应包括
"k"（int）：互易排序融合（RRF）中使用的参数。该值用于计算 RRF 算法中的排名分数，该算法将多个排名策略合并为一个分数，以提高搜索相关性。如果未指定，默认值为 60。
对于 "WeightedRanker"，它的期望值是
"权重"（浮点数列表）：一个包含两个权重的列表：
密集嵌入组件的权重。
稀疏嵌入成分的权重。 这些权重用于平衡混合检索过程中密集嵌入成分和稀疏嵌入成分的重要性。如果没有指定，默认权重为 [1.0，1.0]。
vector_store = MilvusVectorStore(
    uri=URI,
# token=TOKEN,
dim=
1536
,
    overwrite=
False
,
# Use the existing collection created in the previous example
enable_sparse=
True
,
    hybrid_ranker=
"WeightedRanker"
,
    hybrid_ranker_params={
"weights"
: [
1.0
,
0.5
]},
)
index = VectorStoreIndex.from_vector_store(vector_store)
query_engine = index.as_query_engine(
    vector_store_query_mode=
"hybrid"
, similarity_top_k=
5
)
response = query_engine.query(
"What did the author learn at Viaweb?"
)
print
(textwrap.fill(
str
(response),
100
))
2025-04-17 03:44:00,419 [DEBUG][_create_connection]: Created new connection using: 09c051fb18c04f97a80f07958856587b (async_milvus_client.py:547)
Sparse embedding function is not provided, using default.
No built-in function detected, using BGEM3SparseEmbeddingFunction().
Fetching 30 files: 100%|██████████| 30/30 [00:00<00:00, 136622.28it/s]
Chunks: 100%|██████████| 1/1 [00:00<00:00,  1.07it/s]


The author learned several valuable lessons at Viaweb, including the importance of understanding
growth rate as the ultimate test of a startup, the significance of user feedback in shaping the
software, and the realization that web applications were the future of software development.
Additionally, the experience at Viaweb taught the author about the challenges and rewards of running
a startup, the value of simplicity in software design, and the impact of pricing strategies on
attracting customers.