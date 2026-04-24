吉纳人工智能
Jina AI 的嵌入模型是高性能的文本嵌入模型，可以将文本输入转化为数字表示，捕捉文本的语义。这些模型在密集检索、语义文本相似性和多语言理解等应用中表现出色。
Milvus 通过
JinaEmbeddingFunction
类与 Jina AI 的 Embeddings 模型集成。该类提供了使用 Jina AI 嵌入模型对文档和查询进行编码的方法，并将嵌入作为与 Milvus 索引兼容的密集向量返回。要使用此功能，请从
Jina AI
获取 API 密钥。
要使用此功能，请安装必要的依赖项：
pip install --upgrade pymilvus
pip install
"pymilvus[model]"
然后，实例化
JinaEmbeddingFunction
：
from
pymilvus.model.dense
import
JinaEmbeddingFunction

jina_ef = JinaEmbeddingFunction(
    model_name=
"jina-embeddings-v3"
,
# Defaults to `jina-embeddings-v3`
api_key=JINAAI_API_KEY,
# Provide your Jina AI API key
task=
"retrieval.passage"
,
# Specify the task
dimensions=
1024
,
# Defaults to 1024
)
参数
：
model_name
(字符串）
用于编码的 Jina AI 嵌入模型名称。您可以指定任何可用的 Jina AI 嵌入模型名称，例如
jina-embeddings-v3
,
jina-embeddings-v2-base-en
等。如果不指定此参数，则将使用
jina-embeddings-v3
。有关可用模型的列表，请参阅
Jina Embeddings
。
api_key
（字符串）
访问 Jina AI API 的 API 密钥。
task
（字符串）
传递给模型的输入类型。为嵌入模型 v3 及更高版本所必需。
"retrieval.passage"
:用于在索引时对检索任务中的大型文档进行编码。
"retrieval.query"
:用于在检索任务中对用户查询或问题进行编码。
"classification"
:用于对文本分类任务中的文本进行编码。
"text-matching"
:用于对相似性匹配的文本进行编码，如测量两个句子之间的相似性。
"clustering"
:用于聚类或 Rerankers 任务。
dimensions
维数
输出嵌入结果的维数。默认为 1024。仅支持嵌入模型 v3 及更高版本。
late_chunking
(二进制）
此参数控制是否使用
Jina AI 上个月推出的
新分块方法对一批句子进行编码。默认设置为
False
。当设置为
True
时，Jina AI API 会将输入字段中的所有句子串联起来，并作为单个字符串送入模型。在内部，模型会嵌入这个长串联字符串，然后执行后期分块，返回一个与输入列表大小相匹配的嵌入列表。
要创建文档嵌入，请使用
encode_documents()
方法。该方法专为非对称检索任务中的文档嵌入而设计，例如为搜索或推荐任务编制文档索引。该方法使用
retrieval.passage
作为任务。
```python
docs = [
    "Artificial intelligence was founded as an academic discipline in 1956.",
    "Alan Turing was the first person to conduct substantial research in AI.",
    "Born in Maida Vale, London, Turing was raised in southern England.",
]

docs_embeddings = jina_ef.encode_documents(docs)

# Print embeddings
print("Embeddings:", docs_embeddings)
# Print dimension and shape of embeddings
print("Dim:", jina_ef.dim, docs_embeddings[0].shape)
预期输出结果类似于下图：
Embeddings: [array([
9.80641991e-02
, -
8.51697400e-02
,
7.36531913e-02
,
1.42558888e-02
,
       -
2.23589484e-02
,
1.68494112e-03
, -
3.50753777e-02
, -
3.11530549e-02
,
       -
3.26012149e-02
,
5.04568312e-03
,
3.69836427e-02
,
3.48948985e-02
,
8.19722563e-03
,
5.88679723e-02
, -
6.71099266e-03
, -
1.82369724e-02
,
...
2.48654783e-02
,
3.43279652e-02
, -
1.66154150e-02
, -
9.90478322e-03
,
       -
2.96043139e-03
, -
8.57473817e-03
, -
7.39028037e-04
,
6.25024503e-03
,
       -
1.08831357e-02
, -
4.00776342e-02
,
3.25369164e-02
, -
1.42691191e-03
])]
Dim:
1024
(
1024
,)
要创建查询嵌入，请使用
encode_queries()
方法。这种方法是为非对称检索任务（如搜索查询或问题）中的查询嵌入而设计的。该方法使用
retrieval.query
作为任务。
queries = [
"When was artificial intelligence founded"
,
"Where was Alan Turing born?"
]

query_embeddings = jina_ef.encode_queries(queries)
print
(
"Embeddings:"
, query_embeddings)
print
(
"Dim"
, jina_ef.dim, query_embeddings[
0
].shape)
预期输出类似于下面的内容：
Embeddings: [array([
8.79201014e-03
,
1.47551354e-02
,
4.02722731e-02
, -
2.52991207e-02
,
1.12719582e-02
,
3.75947170e-02
,
3.97946090e-02
, -
7.36681819e-02
,
       -
2.17952449e-02
, -
1.16298944e-02
, -
6.83426252e-03
, -
5.12507409e-02
,
5.26071340e-02
,
6.75181448e-02
,
3.92445624e-02
, -
1.40817231e-02
,
...
8.81703943e-03
,
4.24629413e-02
, -
2.32944116e-02
, -
2.05193572e-02
,
       -
3.22035812e-02
,
2.81896023e-03
,
3.85326855e-02
,
3.64372656e-02
,
       -
1.65050142e-02
, -
4.26847413e-02
,
2.02664156e-02
, -
1.72684863e-02
])]
Dim
1024
(
1024
,)
要为相似性匹配（如 STS 或对称检索任务）、文本分类、聚类或重排任务创建输入嵌入，请在实例化
JinaEmbeddingFunction
类时使用适当的
task
参数值。
from
pymilvus.model.dense
import
JinaEmbeddingFunction

jina_ef = JinaEmbeddingFunction(
    model_name=
"jina-embeddings-v3"
,
# Defaults to `jina-embeddings-v3`
api_key=JINA_API_KEY,
# Provide your Jina AI API key
task=
"text-matching"
,
    dimensions=
1024
,
# Defaults to 1024
)

texts = [
"Follow the white rabbit."
,
# English
"Sigue al conejo blanco."
,
# Spanish
"Suis le lapin blanc."
,
# French
"跟着白兔走。"
,
# Chinese
"اتبع الأرنب الأبيض."
,
# Arabic
"Folge dem weißen Kaninchen."
,
# German
]

embeddings = jina_ef(texts)
# Compute similarities
print
(embeddings[
0
] @ embeddings[
1
].T)