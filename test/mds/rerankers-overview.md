Rerankers 概览
在信息检索和生成式人工智能领域，重排序器是优化初始搜索结果排序的重要工具。重排器与传统的
嵌入模型
不同，它将查询和文档作为输入，直接返回相似度得分，而不是嵌入得分。该分数表示输入查询和文档之间的相关性。
Rerankers 通常在第一阶段检索后使用，一般通过向量近似近邻（ANN）技术完成。虽然 ANN 搜索能高效地获取大量潜在的相关结果，但它们可能并不总是根据与查询的实际语义接近程度来确定结果的优先级。在这里，Rerankers 利用更深入的上下文分析来优化结果顺序，通常利用先进的机器学习模型，如 BERT 或其他基于 Transformer 的模型。通过这样做，Rerankers 可以显著提高呈现给用户的最终结果的准确性和相关性。
PyMilvus 模型库集成了 Rerankers 函数，用于优化初始搜索返回结果的顺序。从 Milvus 检索到最近的 Embeddings 后，您可以利用这些 Rerankers 工具来完善搜索结果，从而提高搜索结果的精确度。
Rerankers 功能
应用程序接口或开源
BGE
开源
交叉编码器
开源
Voyage
应用程序接口
Cohere
应用程序接口
Jina AI
API
在使用开源 Rerankers 之前，请确保下载并安装所有必需的依赖项和模型。
对于基于 API 的 Reranker，请从提供商处获取 API 密钥，并将其设置在相应的环境变量或参数中。
示例 1：使用 BGE Rerankers 函数根据查询对文档进行重排
在本例中，我们将演示如何使用
BGE reranker
根据特定查询对搜索结果进行重排。
要使用带有
PyMilvus 模型库
的 Reranker，首先要安装 PyMilvus 模型库以及包含所有必要 Reranking 工具的模型子包：
pip install pymilvus[model]
# or pip install "pymilvus[model]" for zsh.
要使用 BGE Reranker，首先要导入
BGERerankFunction
类：
from
pymilvus.model.reranker
import
BGERerankFunction
然后，创建一个
BGERerankFunction
实例用于 Reranker：
bge_rf = BGERerankFunction(
    model_name=
"BAAI/bge-reranker-v2-m3"
,
# Specify the model name. Defaults to `BAAI/bge-reranker-v2-m3`.
device=
"cpu"
# Specify the device to use, e.g., 'cpu' or 'cuda:0'
)
要根据查询对文档进行排序，请使用以下代码：
query =
"What event in 1956 marked the official birth of artificial intelligence as a discipline?"
documents = [
"In 1950, Alan Turing published his seminal paper, 'Computing Machinery and Intelligence,' proposing the Turing Test as a criterion of intelligence, a foundational concept in the philosophy and development of artificial intelligence."
,
"The Dartmouth Conference in 1956 is considered the birthplace of artificial intelligence as a field; here, John McCarthy and others coined the term 'artificial intelligence' and laid out its basic goals."
,
"In 1951, British mathematician and computer scientist Alan Turing also developed the first program designed to play chess, demonstrating an early example of AI in game strategy."
,
"The invention of the Logic Theorist by Allen Newell, Herbert A. Simon, and Cliff Shaw in 1955 marked the creation of the first true AI program, which was capable of solving logic problems, akin to proving mathematical theorems."
]

bge_rf(query, documents)
预期输出结果类似于下图：
[RerankResult(text=
"The Dartmouth Conference in 1956 is considered the birthplace of artificial intelligence as a field; here, John McCarthy and others coined the term 'artificial intelligence' and laid out its basic goals."
, score=
0.9911615761470803
, index=
1
),
 RerankResult(text=
"In 1950, Alan Turing published his seminal paper, 'Computing Machinery and Intelligence,' proposing the Turing Test as a criterion of intelligence, a foundational concept in the philosophy and development of artificial intelligence."
, score=
0.0326971950177779
, index=
0
),
 RerankResult(text=
'The invention of the Logic Theorist by Allen Newell, Herbert A. Simon, and Cliff Shaw in 1955 marked the creation of the first true AI program, which was capable of solving logic problems, akin to proving mathematical theorems.'
, score=
0.006514905766152258
, index=
3
),
 RerankResult(text=
'In 1951, British mathematician and computer scientist Alan Turing also developed the first program designed to play chess, demonstrating an early example of AI in game strategy.'
, score=
0.0042116724917325935
, index=
2
)]
例 2：使用 Reranker 增强搜索结果的相关性
在本指南中，我们将探讨如何利用 PyMilvus 中的
search()
方法进行相似性搜索，以及如何使用 Reranker 增强搜索结果的相关性。我们将使用以下数据集进行演示：
entities = [
    {
'doc_id'
:
0
,
'doc_vector'
: [-
0.0372721
,
0.0101959
,...,-
0.114994
],
'doc_text'
:
"In 1950, Alan Turing published his seminal paper, 'Computing Machinery and Intelligence,' proposing the Turing Test as a criterion of intelligence, a foundational concept in the philosophy and development of artificial intelligence."
}, 
    {
'doc_id'
:
1
,
'doc_vector'
: [-
0.00308882
,-
0.0219905
,...,-
0.00795811
],
'doc_text'
:
"The Dartmouth Conference in 1956 is considered the birthplace of artificial intelligence as a field; here, John McCarthy and others coined the term 'artificial intelligence' and laid out its basic goals."
}, 
    {
'doc_id'
:
2
,
'doc_vector'
: [
0.00945078
,
0.00397605
,...,-
0.0286199
],
'doc_text'
:
'In 1951, British mathematician and computer scientist Alan Turing also developed the first program designed to play chess, demonstrating an early example of AI in game strategy.'
}, 
    {
'doc_id'
:
3
,
'doc_vector'
: [-
0.0391119
,-
0.00880096
,...,-
0.0109257
],
'doc_text'
:
'The invention of the Logic Theorist by Allen Newell, Herbert A. Simon, and Cliff Shaw in 1955 marked the creation of the first true AI program, which was capable of solving logic problems, akin to proving mathematical theorems.'
}
]
数据集组件
doc_id
:每个文档的唯一标识符。
doc_vector
:代表文档的向量嵌入。有关生成 embeddings 的指导，请参阅
Embeddings
。
doc_text
:文档的文本内容。
准备工作
在启动相似性搜索之前，您需要与 Milvus 建立连接，创建一个 Collections，并准备和插入数据到该 Collections 中。以下代码片段说明了这些初步步骤。
from
pymilvus
import
MilvusClient, DataType

client = MilvusClient(
    uri=
"http://10.102.6.214:19530"
# replace with your own Milvus server address
)

client.drop_collection(
'test_collection'
)
# define schema
schema = client.create_schema(auto_id=
False
, enabel_dynamic_field=
True
)

schema.add_field(field_name=
"doc_id"
, datatype=DataType.INT64, is_primary=
True
, description=
"document id"
)
schema.add_field(field_name=
"doc_vector"
, datatype=DataType.FLOAT_VECTOR, dim=
384
, description=
"document vector"
)
schema.add_field(field_name=
"doc_text"
, datatype=DataType.VARCHAR, max_length=
65535
, description=
"document text"
)
# define index params
index_params = client.prepare_index_params()

index_params.add_index(field_name=
"doc_vector"
, index_type=
"IVF_FLAT"
, metric_type=
"IP"
, params={
"nlist"
:
128
})
# create collection
client.create_collection(collection_name=
"test_collection"
, schema=schema, index_params=index_params)
# insert data into collection
client.insert(collection_name=
"test_collection"
, data=entities)
# Output:
# {'insert_count': 4, 'ids': [0, 1, 2, 3]}
进行相似性搜索
插入数据后，使用
search
方法执行相似性搜索。
# search results based on our query
res = client.search(
    collection_name=
"test_collection"
,
    data=[[-
0.045217834
,
0.035171617
, ..., -
0.025117004
]],
# replace with your query vector
limit=
3
,
    output_fields=[
"doc_id"
,
"doc_text"
]
)
for
i
in
res[
0
]:
print
(
f'distance:
{i[
"distance"
]}
'
)
print
(
f'doc_text:
{i[
"entity"
][
"doc_text"
]}
'
)
预期输出类似于下面的内容：
distance:
0.7235960960388184
doc_text: The Dartmouth Conference
in
1956
is
considered the birthplace of artificial intelligence
as
a field; here, John McCarthy
and
others coined the term
'artificial intelligence'
and
laid out its basic goals.
distance:
0.6269873976707458
doc_text: In
1950
, Alan Turing published his seminal paper,
'Computing Machinery and Intelligence,'
proposing the Turing Test
as
a criterion of intelligence, a foundational concept
in
the philosophy
and
development of artificial intelligence.
distance:
0.5340118408203125
doc_text: The invention of the Logic Theorist by Allen Newell, Herbert A. Simon,
and
Cliff Shaw
in
1955
marked the creation of the first true AI program, which was capable of solving logic problems, akin to proving mathematical theorems.
使用 Reranker 增强搜索结果
然后，通过 Rerankers 步骤提高搜索结果的相关性。在本例中，我们使用 PyMilvus 内置的
CrossEncoderRerankFunction
对结果进行重排，以提高准确性。
# use reranker to rerank search results
from
pymilvus.model.reranker
import
CrossEncoderRerankFunction

ce_rf = CrossEncoderRerankFunction(
    model_name=
"cross-encoder/ms-marco-MiniLM-L-6-v2"
,
# Specify the model name.
device=
"cpu"
# Specify the device to use, e.g., 'cpu' or 'cuda:0'
)

reranked_results = ce_rf(
    query=
'What event in 1956 marked the official birth of artificial intelligence as a discipline?'
,
    documents=[
"In 1950, Alan Turing published his seminal paper, 'Computing Machinery and Intelligence,' proposing the Turing Test as a criterion of intelligence, a foundational concept in the philosophy and development of artificial intelligence."
,
"The Dartmouth Conference in 1956 is considered the birthplace of artificial intelligence as a field; here, John McCarthy and others coined the term 'artificial intelligence' and laid out its basic goals."
,
"In 1951, British mathematician and computer scientist Alan Turing also developed the first program designed to play chess, demonstrating an early example of AI in game strategy."
,
"The invention of the Logic Theorist by Allen Newell, Herbert A. Simon, and Cliff Shaw in 1955 marked the creation of the first true AI program, which was capable of solving logic problems, akin to proving mathematical theorems."
],
    top_k=
3
)
# print the reranked results
for
result
in
reranked_results:
print
(
f'score:
{result.score}
'
)
print
(
f'doc_text:
{result.text}
'
)
预期的输出结果类似于下图：
score:
6.250532627105713
doc_text: The Dartmouth Conference
in
1956
is
considered the birthplace of artificial intelligence
as
a field; here, John McCarthy
and
others coined the term
'artificial intelligence'
and
laid out its basic goals.
score: -
2.9546022415161133
doc_text: In
1950
, Alan Turing published his seminal paper,
'Computing Machinery and Intelligence,'
proposing the Turing Test
as
a criterion of intelligence, a foundational concept
in
the philosophy
and
development of artificial intelligence.
score: -
4.771512031555176
doc_text: The invention of the Logic Theorist by Allen Newell, Herbert A. Simon,
and
Cliff Shaw
in
1955
marked the creation of the first true AI program, which was capable of solving logic problems, akin to proving mathematical theorems.