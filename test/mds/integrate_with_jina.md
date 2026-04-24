将 Milvus 与 Jina AI 相结合
本指南演示了如何使用 Jina AI 嵌入和 Milvus 进行相似性搜索和检索任务。
谁是 Jina AI
Jina AI 于 2020 年在柏林成立，是一家领先的人工智能公司，致力于通过其搜索基础彻底改变人工智能的未来。Jina AI 专注于多模态人工智能，旨在通过其集成的组件套件，包括 Embeddings、Rerankers、prompt ops 和核心基础设施，使企业和开发人员能够利用多模态数据的力量创造价值和节约成本。
Jina AI 的尖端 Embeddings 拥有顶级性能，其 8192 令牌长度模型是全面数据表示的理想选择。这些 Embeddings 提供多语言支持，并与 OpenAI 等领先平台无缝集成，为跨语言应用提供了便利。
Milvus 和 Jina AI 的嵌入式技术
为了高效、快速、大规模地存储和搜索这些 Embeddings，需要为此设计特定的基础设施。Milvus 是一个广为人知的先进开源向量数据库，能够处理大规模向量数据。Milvus 可根据大量指标实现快速、准确的向量（嵌入）搜索。它的可扩展性允许无缝处理海量图像数据，即使数据集不断增长，也能确保高性能的搜索操作。
实例
Jina 嵌入已经集成到 PyMilvus 模型库中。现在，我们将通过代码示例来展示如何实际使用 Jina embeddings。
在开始之前，我们需要为 PyMilvus 安装模型库。
$ pip install -U pymilvus milvus-lite
$ pip install
"pymilvus[model]"
如果您使用的是 Google Colab，为了启用刚刚安装的依赖项，您可能需要
重启运行时
。(点击屏幕上方的 "Runtime（运行时）"菜单，从下拉菜单中选择 "Restart session（重新启动会话）"）。
通用嵌入程序
Jina AI 的核心嵌入模型擅长理解详细文本，因此非常适合语义搜索、内容分类，从而支持高级情感分析、文本摘要和个性化推荐系统。
from
pymilvus.model.dense
import
JinaEmbeddingFunction

jina_api_key =
"<YOUR_JINA_API_KEY>"
ef = JinaEmbeddingFunction(
"jina-embeddings-v3"
, 
    jina_api_key,
    task=
"retrieval.passage"
,
    dimensions=
1024
)

query =
"what is information retrieval?"
doc =
"Information retrieval is the process of finding relevant information from a large collection of data or documents."
qvecs = ef.encode_queries([query])
# This method uses `retrieval.query` as the task
dvecs = ef.encode_documents([doc])
# This method uses `retrieval.passage` as the task
双语嵌入模型
Jina AI 的双语模型增强了多语言平台、全球支持和跨语言内容发现功能。这些模型专为德英和汉英翻译而设计，可促进不同语言群体之间的理解，简化跨语言交互。
from
pymilvus.model.dense
import
JinaEmbeddingFunction

jina_api_key =
"<YOUR_JINA_API_KEY>"
ef = JinaEmbeddingFunction(
"jina-embeddings-v2-base-de"
, jina_api_key)

query =
"what is information retrieval?"
doc =
"Information Retrieval ist der Prozess, relevante Informationen aus einer großen Sammlung von Daten oder Dokumenten zu finden."
qvecs = ef.encode_queries([query])
dvecs = ef.encode_documents([doc])
代码嵌入
Jina AI 的代码嵌入模型通过代码和文档提供搜索能力。它支持英语和 30 种常用编程语言，可用于增强代码导航、简化代码审查和自动文档协助。
from
pymilvus.model.dense
import
JinaEmbeddingFunction

jina_api_key =
"<YOUR_JINA_API_KEY>"
ef = JinaEmbeddingFunction(
"jina-embeddings-v2-base-code"
, jina_api_key)
# Case1: Enhanced Code Navigation
# query: text description of the functionality
# document: relevant code snippet
query =
"function to calculate average in Python."
doc =
"""
def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    return total / count
"""
# Case2: Streamlined Code Review
# query: text description of the programming concept
# document: relevante code snippet or PR
query =
"pull quest related to Collection"
doc =
"fix:[restful v2] parameters of create collection ..."
# Case3: Automatic Documentation Assistance
# query: code snippet you need explanation
# document: relevante document or DocsString
query =
"What is Collection in Milvus"
doc =
"""
In Milvus, you store your vector embeddings in collections. All vector embeddings within a collection share the same dimensionality and distance metric for measuring similarity.
Milvus collections support dynamic fields (i.e., fields not pre-defined in the schema) and automatic incrementation of primary keys.
"""
qvecs = ef.encode_queries([query])
dvecs = ef.encode_documents([doc])
使用 Jina 和 Milvus 进行语义搜索
借助强大的向量嵌入功能，我们可以将利用 Jina AI 模型检索到的嵌入与 Milvus Lite 向量数据库相结合，进行语义搜索。
from
pymilvus.model.dense
import
JinaEmbeddingFunction
from
pymilvus
import
MilvusClient

jina_api_key =
"<YOUR_JINA_API_KEY>"
DIMENSION =
1024
# `jina-embeddings-v3` supports flexible embedding sizes (32, 64, 128, 256, 512, 768, 1024), allowing for truncating embeddings to fit your application.
ef = JinaEmbeddingFunction(
"jina-embeddings-v3"
, 
    jina_api_key,
    task=
"retrieval.passage"
,
    dimensions=DIMENSION,
)


doc = [
"In 1950, Alan Turing published his seminal paper, 'Computing Machinery and Intelligence,' proposing the Turing Test as a criterion of intelligence, a foundational concept in the philosophy and development of artificial intelligence."
,
"The Dartmouth Conference in 1956 is considered the birthplace of artificial intelligence as a field; here, John McCarthy and others coined the term 'artificial intelligence' and laid out its basic goals."
,
"In 1951, British mathematician and computer scientist Alan Turing also developed the first program designed to play chess, demonstrating an early example of AI in game strategy."
,
"The invention of the Logic Theorist by Allen Newell, Herbert A. Simon, and Cliff Shaw in 1955 marked the creation of the first true AI program, which was capable of solving logic problems, akin to proving mathematical theorems."
,
]

dvecs = ef.encode_documents(doc)
# This method uses `retrieval.passage` as the task
data = [
    {
"id"
: i,
"vector"
: dvecs[i],
"text"
: doc[i],
"subject"
:
"history"
}
for
i
in
range
(
len
(dvecs))
]

milvus_client = MilvusClient(
"./milvus_jina_demo.db"
)
COLLECTION_NAME =
"demo_collection"
# Milvus collection name
if
milvus_client.has_collection(collection_name=COLLECTION_NAME):
    milvus_client.drop_collection(collection_name=COLLECTION_NAME)
milvus_client.create_collection(collection_name=COLLECTION_NAME, dimension=DIMENSION)

res = milvus_client.insert(collection_name=COLLECTION_NAME, data=data)
print
(res[
"insert_count"
])
至于
MilvusClient
的参数：
将
uri
设置为本地文件，如
./milvus.db
，是最方便的方法，因为它会自动利用
Milvus Lite
将所有数据存储在此文件中。
如果数据规模较大，可以在
docker 或 kubernetes
上设置性能更强的 Milvus 服务器。在此设置中，请使用服务器 uri，例如
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
有了 Milvus 向量数据库中的所有数据，我们现在就可以通过为查询生成向量 Embeddings 来执行语义搜索，并进行向量搜索。
queries =
"What event in 1956 marked the official birth of artificial intelligence as a discipline?"
qvecs = ef.encode_queries([queries])
# This method uses `retrieval.query` as the task
res = milvus_client.search(
    collection_name=COLLECTION_NAME,
# target collection
data=[qvecs[
0
]],
# query vectors
limit=
3
,
# number of returned entities
output_fields=[
"text"
,
"subject"
],
# specifies fields to be returned
)[
0
]
for
result
in
res:
print
(result)
{'id': 1, 'distance': 0.8802614808082581, 'entity': {'text': "The Dartmouth Conference in 1956 is considered the birthplace of artificial intelligence as a field; here, John McCarthy and others coined the term 'artificial intelligence' and laid out its basic goals.", 'subject': 'history'}}
Jina Reranker
在使用嵌入式搜索后，Jina Ai 还提供了 Rerankers 以进一步提高检索质量。
from
pymilvus.model.reranker
import
JinaRerankFunction

jina_api_key =
"<YOUR_JINA_API_KEY>"
rf = JinaRerankFunction(
"jina-reranker-v1-base-en"
, jina_api_key)

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
,
]

rf(query, documents)
[RerankResult(text="The Dartmouth Conference in 1956 is considered the birthplace of artificial intelligence as a field; here, John McCarthy and others coined the term 'artificial intelligence' and laid out its basic goals.", score=0.9370958209037781, index=1),
 RerankResult(text='The invention of the Logic Theorist by Allen Newell, Herbert A. Simon, and Cliff Shaw in 1955 marked the creation of the first true AI program, which was capable of solving logic problems, akin to proving mathematical theorems.', score=0.35420963168144226, index=3),
 RerankResult(text="In 1950, Alan Turing published his seminal paper, 'Computing Machinery and Intelligence,' proposing the Turing Test as a criterion of intelligence, a foundational concept in the philosophy and development of artificial intelligence.", score=0.3498658835887909, index=0),
 RerankResult(text='In 1951, British mathematician and computer scientist Alan Turing also developed the first program designed to play chess, demonstrating an early example of AI in game strategy.', score=0.2728956639766693, index=2)]