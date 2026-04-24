使用 LlamaIndex 和 Milvus 进行全文搜索
全文搜索
使用精确的关键词匹配，通常利用 BM25 等算法按相关性对文档进行排序。在
检索增强生成（RAG）
系统中，这种方法检索相关文本，以增强人工智能生成的响应。
同时，
语义搜索
可以解释上下文的含义，从而提供更广泛的结果。将这两种方法结合起来，就能创建一种
混合搜索
，从而改进信息检索，尤其是在单一方法无法满足要求的情况下。
利用
Milvus 2.5
的 Sparse-BM25 方法，原始文本会自动转换为稀疏向量。这样就无需手动生成稀疏嵌入，从而实现了混合搜索策略，在语义理解和关键词相关性之间取得了平衡。
在本教程中，您将学习如何使用 LlamaIndex 和 Milvus 建立一个使用全文搜索和混合搜索的 RAG 系统。我们将首先单独实施全文搜索，然后通过整合语义搜索来增强其功能，以获得更全面的结果。
在继续本教程之前，请确保您熟悉
全文搜索
和
在 LlamaIndex 中使用 Milvus 的基础知识
。
先决条件
安装依赖项
在开始之前，请确保您已安装以下依赖项：
$
$pip
install llama-index-vector-stores-milvus
$
$pip
install llama-index-embeddings-openai
$
$pip
install llama-index-llms-openai
如果使用的是 Google Colab，则可能需要
重启运行时
（导航至界面顶部的 "运行时 "菜单，然后从下拉菜单中选择 "重启会话"）。
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
Milvus Standalone、Milvus Distributed 和 Zilliz Cloud 目前支持全文搜索，但 Milvus Lite 尚不支持全文搜索（计划今后实施）。如需了解更多信息，请联系 support@zilliz.com。
URI =
"http://localhost:19530"
# TOKEN = ""
下载示例数据
运行以下命令可将示例文档下载到 "data/paul_graham "目录：
$
mkdir
-p
'data/paul_graham/'
$
$wget
'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt'
-O
'data/paul_graham/paul_graham_essay.txt'
--2025-03-27 07:49:01--  https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.108.133, 185.199.109.133, 185.199.110.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.108.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 75042 (73K) [text/plain]
Saving to: ‘data/paul_graham/paul_graham_essay.txt’

data/paul_graham/pa 100%[===================>]  73.28K  --.-KB/s    in 0.07s   

2025-03-27 07:49:01 (1.01 MB/s) - ‘data/paul_graham/paul_graham_essay.txt’ saved [75042/75042]
带有全文搜索功能的 RAG
将全文搜索集成到 RAG 系统中，可在语义搜索与基于关键字的精确、可预测检索之间取得平衡。您也可以选择只使用全文检索，但建议将全文检索与语义搜索结合起来，以获得更好的搜索结果。在此，我们将单独演示全文搜索和混合搜索。
要开始使用，请使用
SimpleDirectoryReaderLoad
加载保罗-格雷厄姆（Paul Graham）的文章 "What I Worked On"：
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
 Doc ID: 16b7942f-bf1a-4197-85e1-f31d51ea25a9
Text: What I Worked On  February 2021  Before college the two main
things I worked on, outside of school, were writing and programming. I
didn't write essays. I wrote what beginning writers were supposed to
write then, and probably still are: short stories. My stories were
awful. They had hardly any plot, just characters with strong feelings,
which I ...
使用 BM25 进行全文搜索
LlamaIndex 的
MilvusVectorStore
支持全文检索，可实现基于关键字的高效检索。通过使用内置函数作为
sparse_embedding_function
，它可以应用 BM25 评分对搜索结果进行排序。
在本节中，我们将演示如何使用 BM25 为全文检索实现 RAG 系统。
from
llama_index.core
import
VectorStoreIndex, StorageContext
from
llama_index.vector_stores.milvus
import
MilvusVectorStore
from
llama_index.vector_stores.milvus.utils
import
BM25BuiltInFunction
from
llama_index.core
import
Settings
# Skip dense embedding model
Settings.embed_model =
None
# Build Milvus vector store creating a new collection
vector_store = MilvusVectorStore(
    uri=URI,
# token=TOKEN,
enable_dense=
False
,
    enable_sparse=
True
,
# Only enable sparse to demo full text search
sparse_embedding_function=BM25BuiltInFunction(),
    overwrite=
True
,
)
# Store documents in Milvus
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
Embeddings have been explicitly disabled. Using MockEmbedding.
上述代码将示例文档插入 Milvus 并建立索引，以启用 BM25 排名进行全文搜索。它禁用了密集嵌入（dense embedding），并使用带有默认参数的
BM25BuiltInFunction
。
您可以在
BM25BuiltInFunction
参数中指定输入和输出字段：
input_field_names (str)
:输入文本字段（默认："text"）。它表示 BM25 算法应用于哪个文本字段。如果使用不同文本字段名称的自己的 Collections，请更改此项。
output_field_names (str)
:存储此 BM25 函数输出的字段（默认值："sparse_embedding"）。
向量存储设置完成后，就可以使用 Milvus 执行全文搜索查询，查询模式为 "sparse "或 "text_search"：
import
textwrap

query_engine = index.as_query_engine(
    vector_store_query_mode=
"sparse"
, similarity_top_k=
5
)
answer = query_engine.query(
"What did the author learn at Viaweb?"
)
print
(textwrap.fill(
str
(answer),
100
))
The author learned several important lessons at Viaweb. They learned about the importance of growth
rate as the ultimate test of a startup, the value of building stores for users to understand retail
and software usability, and the significance of being the "entry level" option in a market.
Additionally, they discovered the accidental success of making Viaweb inexpensive, the challenges of
hiring too many people, and the relief felt when the company was acquired by Yahoo.
自定义文本分析器
分析器在全文检索中发挥着重要作用，它能将句子分解成词块，并执行词法处理，如词干和停止词删除。它们通常针对特定语言。有关详细信息，请参阅
Milvus 分析器指南
。
Milvus 支持两种类型的分析器：
内置分析器
和
自定义分析器
。默认情况下，
BM25BuiltInFunction
使用标准内置分析器，该分析器根据标点符号对文本进行标记。
要使用其他分析器或自定义现有分析器，可以向
analyzer_params
参数传递值：
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
带 Reranker 的混合搜索
混合搜索系统结合了语义搜索和全文搜索，可优化 RAG 系统的检索性能。
以下示例使用 OpenAI Embeddings 进行语义搜索，使用 BM25 进行全文搜索：
# Create index over the documnts
vector_store = MilvusVectorStore(
    uri=URI,
# token=TOKEN,
# enable_dense=True,  # enable_dense defaults to True
dim=
1536
,
    enable_sparse=
True
,
    sparse_embedding_function=BM25BuiltInFunction(),
    overwrite=
True
,
# hybrid_ranker="RRFRanker",  # hybrid_ranker defaults to "RRFRanker"
# hybrid_ranker_params={},  # hybrid_ranker_params defaults to {}
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    embed_model=
"default"
,
# "default" will use OpenAI embedding
)
工作原理
这种方法将文档存储在 Milvus Collections 中，同时带有两个向量字段：
embedding
:由 OpenAI 嵌入模型生成的用于语义搜索的高密度嵌入。
sparse_embedding
:使用 BM25BuiltInFunction 计算的稀疏嵌入，用于全文搜索。
此外，我们还使用 "RRFRanker "及其默认参数应用了重排策略。要定制 Reranker，可以按照《
Milvus Reranking 指南
》配置
hybrid_ranker
和
hybrid_ranker_params
。
现在，让我们用一个示例查询来测试 RAG 系统：
# Query
query_engine = index.as_query_engine(
    vector_store_query_mode=
"hybrid"
, similarity_top_k=
5
)
answer = query_engine.query(
"What did the author learn at Viaweb?"
)
print
(textwrap.fill(
str
(answer),
100
))
The author learned several important lessons at Viaweb. These included the importance of
understanding growth rate as the ultimate test of a startup, the impact of hiring too many people,
the challenges of being at the mercy of investors, and the relief experienced when Yahoo bought the
company. Additionally, the author learned about the significance of user feedback, the value of
building stores for users, and the realization that growth rate is crucial for the long-term success
of a startup.
这种混合方法通过同时利用语义检索和基于关键词的检索，确保 RAG 系统能做出更准确、更能感知上下文的响应。