使用 Milvus 和 HayStack 进行全文检索
全文搜索
是一种通过匹配文本中特定关键词或短语来检索文档的传统方法。它根据术语频率等因素计算出的相关性分数对结果进行排序。语义搜索更善于理解含义和上下文，而全文搜索则擅长精确的关键词匹配，因此是语义搜索的有益补充。BM25 算法被广泛用于全文搜索的排序，并在检索增强生成（RAG）中发挥着关键作用。
Milvus 2.5
引入了使用 BM25 的本地全文搜索功能。这种方法将文本转换为代表 BM25 分数的稀疏向量。您只需输入原始文本，Milvus 就会自动生成并存储稀疏向量，无需手动生成稀疏嵌入。
HayStack
现在支持 Milvus 的这一功能，从而可以轻松地将全文搜索添加到 RAG 应用程序中。您可以将全文搜索与密集向量语义搜索结合起来，采用混合方法，从语义理解和关键词匹配精度中获益。这种组合提高了搜索的准确性，为用户提供了更好的搜索结果。
本教程演示了如何使用 HayStack 和 Milvus 在应用程序中实现全文和混合搜索。
要使用 Milvus 向量存储，请指定你的 Milvus 服务器
URI
（也可选择使用
TOKEN
）。要启动 Milvus 服务器，可以按照
Milvus 安装指南
设置 Milvus 服务器，或者直接免费
试用 Zilliz Cloud
（全面管理 Milvus）。
目前，Milvus Standalone、Milvus Distributed 和 Zilliz Cloud 均提供全文搜索功能，但 Milvus Lite 尚不支持该功能（该功能计划在未来实施）。如需了解更多信息，请访问 support@zilliz.com。
在继续本教程之前，请确保您已基本了解
全文检索
和 HayStack Milvus 集成的
基本用法
。
先决条件
在运行本笔记本之前，请确保已安装以下依赖项：
$
pip install --upgrade --quiet pymilvus milvus-haystack
如果使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
我们将使用 OpenAI 的模型。您应将
api key
OPENAI_API_KEY
作为环境变量。
import
os

os.environ[
"OPENAI_API_KEY"
] =
"sk-***********"
准备数据
在本笔记本中导入必要的软件包。然后准备一些示例文档。
from
haystack
import
Pipeline
from
haystack.components.embedders
import
OpenAIDocumentEmbedder, OpenAITextEmbedder
from
haystack.components.writers
import
DocumentWriter
from
haystack.utils
import
Secret
from
milvus_haystack
import
MilvusDocumentStore, MilvusSparseEmbeddingRetriever
from
haystack.document_stores.types
import
DuplicatePolicy
from
milvus_haystack.function
import
BM25BuiltInFunction
from
milvus_haystack
import
MilvusDocumentStore
from
milvus_haystack.milvus_embedding_retriever
import
MilvusHybridRetriever
from
haystack.utils
import
Secret
from
haystack.components.builders
import
PromptBuilder
from
haystack.components.generators
import
OpenAIGenerator
from
haystack
import
Document

documents = [
    Document(content=
"Alice likes this apple"
, meta={
"category"
:
"fruit"
}),
    Document(content=
"Bob likes swimming"
, meta={
"category"
:
"sport"
}),
    Document(content=
"Charlie likes white dogs"
, meta={
"category"
:
"pets"
}),
]
将全文检索集成到 RAG 系统中，可以在语义搜索和基于关键字的精确、可预测检索之间取得平衡。您也可以选择只使用全文检索，但建议将全文检索与语义搜索结合起来，以获得更好的搜索结果。在此，我们将展示单独的全文搜索和混合搜索。
不使用 Embeddings 的 BM25 搜索
创建索引管道
对于全文搜索，Milvus MilvusDocumentStore 接受一个
builtin_function
参数。通过这个参数，你可以传入
BM25BuiltInFunction
的一个实例，它在 Milvus 服务器端实现了 BM25 算法。将
builtin_function
指定为 BM25 函数实例。例如
connection_args = {
"uri"
:
"http://localhost:19530"
}
# connection_args = {"uri": YOUR_ZILLIZ_CLOUD_URI, "token": Secret.from_env_var("ZILLIZ_CLOUD_API_KEY")}
document_store = MilvusDocumentStore(
    connection_args=connection_args,
    sparse_vector_field=
"sparse_vector"
,
# The sparse vector field.
text_field=
"text"
,
    builtin_function=[
        BM25BuiltInFunction(
# The BM25 function converts the text into a sparse vector.
input_field_names=
"text"
,
            output_field_names=
"sparse_vector"
,
        )
    ],
    consistency_level=
"Bounded"
,
# Supported values are (`"Strong"`, `"Session"`, `"Bounded"`, `"Eventually"`).
drop_old=
True
,
# Drop the old collection if it exists and recreate it.
)
对于 connection_args：
你可以在
docker 或 kubernetes
上设置性能更强的 Milvus 服务器。在此设置中，请使用服务器地址，如
http://localhost:19530
，作为您的
uri
。
如果你想使用
Zilliz Cloud
（Milvus 的全托管云服务），请调整
uri
和
token
，它们与 Zilliz Cloud 中的
公共端点和 Api 密钥
相对应。
建立索引管道，将文档写入 Milvus 文档存储。
writer = DocumentWriter(document_store=document_store, policy=DuplicatePolicy.NONE)

indexing_pipeline = Pipeline()
indexing_pipeline.add_component(
"writer"
, writer)
indexing_pipeline.run({
"writer"
: {
"documents"
: documents}})
{'writer': {'documents_written': 3}}
创建检索管道
创建一个检索管道，使用
MilvusSparseEmbeddingRetriever
从 Milvus 文档存储中检索文档，该管道是
document_store
的一个包装器。
retrieval_pipeline = Pipeline()
retrieval_pipeline.add_component(
"retriever"
, MilvusSparseEmbeddingRetriever(document_store=document_store)
)

question =
"Who likes swimming?"
retrieval_results = retrieval_pipeline.run({
"retriever"
: {
"query_text"
: question}})

retrieval_results[
"retriever"
][
"documents"
][
0
]
Document(id=bd334348dd2087c785e99b5a0009f33d9b8b8198736f6415df5d92602d81fd3e, content: 'Bob likes swimming', meta: {'category': 'sport'}, score: 1.2039074897766113)
使用语义搜索和全文搜索的混合搜索
创建索引管道
在混合搜索中，我们使用 BM25 函数来执行全文搜索，并指定密集向量场
vector
，来执行语义搜索。
document_store = MilvusDocumentStore(
    connection_args=connection_args,
    vector_field=
"vector"
,
# The dense vector field.
sparse_vector_field=
"sparse_vector"
,
# The sparse vector field.
text_field=
"text"
,
    builtin_function=[
        BM25BuiltInFunction(
# The BM25 function converts the text into a sparse vector.
input_field_names=
"text"
,
            output_field_names=
"sparse_vector"
,
        )
    ],
    consistency_level=
"Bounded"
,
# Supported values are (`"Strong"`, `"Session"`, `"Bounded"`, `"Eventually"`).
drop_old=
True
,
# Drop the old collection and recreate it.
)
创建索引管道，将文档转换为 Embeddings。然后将文档写入 Milvus 文档存储区。
writer = DocumentWriter(document_store=document_store, policy=DuplicatePolicy.NONE)

indexing_pipeline = Pipeline()
indexing_pipeline.add_component(
"dense_doc_embedder"
, OpenAIDocumentEmbedder())
indexing_pipeline.add_component(
"writer"
, writer)
indexing_pipeline.connect(
"dense_doc_embedder"
,
"writer"
)
indexing_pipeline.run({
"dense_doc_embedder"
: {
"documents"
: documents}})
print
(
"Number of documents:"
, document_store.count_documents())
Calculating embeddings: 100%|██████████| 1/1 [00:01<00:00,  1.15s/it]


Number of documents: 3
创建检索管道
创建一个检索管道，使用
MilvusHybridRetriever
从 Milvus 文档存储区检索文档，其中包含
document_store
并接收有关混合搜索的参数。
# from pymilvus import WeightedRanker
retrieval_pipeline = Pipeline()
retrieval_pipeline.add_component(
"dense_text_embedder"
, OpenAITextEmbedder())
retrieval_pipeline.add_component(
"retriever"
,
    MilvusHybridRetriever(
        document_store=document_store,
# top_k=3,
# reranker=WeightedRanker(0.5, 0.5),  # Default is RRFRanker()
),
)

retrieval_pipeline.connect(
"dense_text_embedder.embedding"
,
"retriever.query_embedding"
)
<haystack.core.pipeline.pipeline.Pipeline object at 0x3383ad990>
🚅 Components
  - dense_text_embedder: OpenAITextEmbedder
  - retriever: MilvusHybridRetriever
🛤️ Connections
  - dense_text_embedder.embedding -> retriever.query_embedding (List[float])
在使用
MilvusHybridRetriever
执行混合搜索时，我们可以选择性地设置 topK 和 Reranker 参数。它会自动处理向量嵌入和内置函数，最后使用 Reranker 来完善结果。搜索过程的底层实现细节对用户是隐藏的。
有关混合搜索的更多信息，请参阅
混合搜索介绍
。
question =
"Who likes swimming?"
retrieval_results = retrieval_pipeline.run(
    {
"dense_text_embedder"
: {
"text"
: question},
"retriever"
: {
"query_text"
: question},
    }
)

retrieval_results[
"retriever"
][
"documents"
][
0
]
Document(id=bd334348dd2087c785e99b5a0009f33d9b8b8198736f6415df5d92602d81fd3e, content: 'Bob likes swimming', meta: {'category': 'sport'}, score: 0.032786883413791656, embedding: vector of size 1536)
自定义分析器
分析器是全文搜索中必不可少的工具，它能将句子分解为词块，并执行词性分析，如词干分析和停止词删除。分析器通常针对特定语言。您可以参考
本指南
，了解有关 Milvus 分析器的更多信息。
Milvus 支持两种类型的分析器：
内置分析器
和
自定义分析器
。默认情况下，
BM25BuiltInFunction
将使用
标准的内置分析器
，这是最基本的分析器，会用标点符号标记文本。
如果想使用其他分析器或自定义分析器，可以在
BM25BuiltInFunction
初始化时传递
analyzer_params
参数。
analyzer_params_custom = {
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
# Custom filter
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
# Custom filter
],
}

document_store = MilvusDocumentStore(
    connection_args=connection_args,
    vector_field=
"vector"
,
    sparse_vector_field=
"sparse_vector"
,
    text_field=
"text"
,
    builtin_function=[
        BM25BuiltInFunction(
            input_field_names=
"text"
,
            output_field_names=
"sparse_vector"
,
            analyzer_params=analyzer_params_custom,
# Custom analyzer parameters.
enable_match=
True
,
# Whether to enable match.
)
    ],
    consistency_level=
"Bounded"
,
    drop_old=
True
,
)
# write documents to the document store
writer = DocumentWriter(document_store=document_store, policy=DuplicatePolicy.NONE)
indexing_pipeline = Pipeline()
indexing_pipeline.add_component(
"dense_doc_embedder"
, OpenAIDocumentEmbedder())
indexing_pipeline.add_component(
"writer"
, writer)
indexing_pipeline.connect(
"dense_doc_embedder"
,
"writer"
)
indexing_pipeline.run({
"dense_doc_embedder"
: {
"documents"
: documents}})
Calculating embeddings: 100%|██████████| 1/1 [00:00<00:00,  1.39it/s]





{'dense_doc_embedder': {'meta': {'model': 'text-embedding-ada-002-v2',
   'usage': {'prompt_tokens': 11, 'total_tokens': 11}}},
 'writer': {'documents_written': 3}}
我们可以看看 Milvus Collections 的 Schema，确保定制的分析器设置正确。
document_store.col.schema
{'auto_id': False, 'description': '', 'fields': [{'name': 'text', 'description': '', 'type': <DataType.VARCHAR: 21>, 'params': {'max_length': 65535, 'enable_match': True, 'enable_analyzer': True, 'analyzer_params': {'tokenizer': 'standard', 'filter': ['lowercase', {'type': 'length', 'max': 40}, {'type': 'stop', 'stop_words': ['of', 'to']}]}}}, {'name': 'id', 'description': '', 'type': <DataType.VARCHAR: 21>, 'params': {'max_length': 65535}, 'is_primary': True, 'auto_id': False}, {'name': 'vector', 'description': '', 'type': <DataType.FLOAT_VECTOR: 101>, 'params': {'dim': 1536}}, {'name': 'sparse_vector', 'description': '', 'type': <DataType.SPARSE_FLOAT_VECTOR: 104>, 'is_function_output': True}], 'enable_dynamic_field': True, 'functions': [{'name': 'bm25_function_7b6e15a4', 'description': '', 'type': <FunctionType.BM25: 1>, 'input_field_names': ['text'], 'output_field_names': ['sparse_vector'], 'params': {}}]}
更多概念详情，如
analyzer
,
tokenizer
,
filter
,
enable_match
,
analyzer_params
，请参阅
分析器文档
。
在 RAG 管道中使用混合搜索
我们已经学习了如何在 HayStack 和 Milvus 中使用基本的 BM25 内置函数，并准备了一个加载的
document_store
。下面我们来介绍使用混合搜索的优化 RAG 实现。
此图显示了混合检索与 Rerankers 流程，结合了用于关键词匹配的 BM25 和用于语义检索的密集向量搜索。来自两种方法的结果会被合并、Rerankers 并传递给 LLM 以生成最终答案。
混合搜索兼顾了精确性和语义理解，提高了各种查询的准确性和稳健性。它通过 BM25 全文检索和向量搜索检索候选内容，同时确保语义、上下文感知和精确检索。
让我们尝试使用混合搜索优化 RAG 实现。
prompt_template =
"""Answer the following query based on the provided context. If the context does
                     not include an answer, reply with 'I don't know'.\n
                     Query: {{query}}
                     Documents:
                     {% for doc in documents %}
                        {{ doc.content }}
                     {% endfor %}
                     Answer:
                  """
rag_pipeline = Pipeline()
rag_pipeline.add_component(
"text_embedder"
, OpenAITextEmbedder())
rag_pipeline.add_component(
"retriever"
, MilvusHybridRetriever(document_store=document_store, top_k=
1
)
)
rag_pipeline.add_component(
"prompt_builder"
, PromptBuilder(template=prompt_template))
rag_pipeline.add_component(
"generator"
,
    OpenAIGenerator(
        api_key=Secret.from_token(os.getenv(
"OPENAI_API_KEY"
)),
        generation_kwargs={
"temperature"
:
0
},
    ),
)
rag_pipeline.connect(
"text_embedder.embedding"
,
"retriever.query_embedding"
)
rag_pipeline.connect(
"retriever.documents"
,
"prompt_builder.documents"
)
rag_pipeline.connect(
"prompt_builder"
,
"generator"
)

results = rag_pipeline.run(
    {
"text_embedder"
: {
"text"
: question},
"retriever"
: {
"query_text"
: question},
"prompt_builder"
: {
"query"
: question},
    }
)
print
(
"RAG answer:"
, results[
"generator"
][
"replies"
][
0
])
RAG answer: Bob likes swimming.
有关如何使用 Milvus-hayStack 的更多信息，请参阅
Milvus-hayStack 官方资源库
。