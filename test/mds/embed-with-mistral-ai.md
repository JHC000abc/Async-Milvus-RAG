Mistral AI
Mistral AI
的 Embeddings 模型是文本嵌入模型，旨在将文本输入转换为密集的数字向量，有效捕捉文本的潜在含义。这些模型针对语义搜索、自然语言理解和上下文感知应用等任务进行了高度优化，因此适用于各种人工智能驱动的解决方案。
Milvus 通过 MistralAIEmbeddingFunction 类与 Mistral AI 的嵌入模型集成。该类提供了使用 Mistral AI 嵌入模型对文档和查询进行编码的方法，并将嵌入作为与 Milvus 索引兼容的稠密向量返回。要使用该功能，请从
Mistral AI
获取 API 密钥。
要使用此功能，请安装必要的依赖项：
pip install --upgrade pymilvus
pip install
"pymilvus[model]"
然后，实例化 MistralAIEmbeddingFunction：
from
pymilvus.model.dense
import
MistralAIEmbeddingFunction

ef = MistralAIEmbeddingFunction(
    model_name=
"mistral-embed"
,
# Defaults to `mistral-embed`
api_key=
"MISTRAL_API_KEY"
# Provide your Mistral AI API key
)
参数
：
model_name
(字符串）
用于编码的 Mistral AI 嵌入模型名称。默认值为
mistral-embed
。更多信息，请参阅
Embeddings
。
api_key
(字符串）
访问 Mistral AI API 的 API 密钥。
要为文档创建 Embeddings，请使用
encode_documents()
方法：
docs = [
"Artificial intelligence was founded as an academic discipline in 1956."
,
"Alan Turing was the first person to conduct substantial research in AI."
,
"Born in Maida Vale, London, Turing was raised in southern England."
,
]

docs_embeddings = ef.encode_documents(docs)
# Print embeddings
print
(
"Embeddings:"
, docs_embeddings)
# Print dimension and shape of embeddings
print
(
"Dim:"
, ef.dim, docs_embeddings[
0
].shape)
预期输出类似于下图：
Embeddings: [array([-
0.06051636
,
0.03207397
,
0.04684448
, ..., -
0.01618958
,
0.02442932
, -
0.01302338
]), array([-
0.04675293
,
0.06512451
,
0.04290771
, ..., -
0.01454926
,
0.0014801
,
0.00686646
]), array([-
0.05978394
,
0.08728027
,
0.02217102
, ..., -
0.00681305
,
0.03634644
, -
0.01802063
])]
Dim:
1024
(
1024
,)
要为查询创建 Embeddings，请使用
encode_queries()
方法：
queries = [
"When was artificial intelligence founded"
,
"Where was Alan Turing born?"
]

query_embeddings = ef.encode_queries(queries)
print
(
"Embeddings:"
, query_embeddings)
print
(
"Dim"
, ef.dim, query_embeddings[
0
].shape)
预期输出类似于下面的内容：
Embeddings: [array([-
0.04916382
,
0.04568481
,
0.03594971
, ..., -
0.02653503
,
0.02804565
,
0.00600815
]), array([-
0.05938721
,
0.07098389
,
0.01773071
, ..., -
0.01708984
,
0.03582764
,
0.00366592
])]
Dim
1024
(
1024
,)