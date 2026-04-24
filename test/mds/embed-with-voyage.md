Voyage
Milvus 通过 VoyageEmbeddingFunction 类与 Voyage 的模型集成。该类提供了使用 Voyage 模型对文档和查询进行编码的方法，并将嵌入返回为与 Milvus 索引兼容的密集向量。要使用该功能，请通过在
Voyage
平台上创建账户从
Voyage
获取 API 密钥。
要使用此功能，请安装必要的依赖项：
pip install --upgrade pymilvus
pip install
"pymilvus[model]"
然后，实例化
VoyageEmbeddingFunction
：
from
pymilvus.model.dense
import
VoyageEmbeddingFunction

voyage_ef = VoyageEmbeddingFunction(
    model_name=
"voyage-3"
,
# Defaults to `voyage-3`
api_key=VOYAGE_API_KEY
# Provide your Voyage API key
)
参数
：
model_name
(字符串）用于编码的 Voyage 模型名称。可以指定任何可用的 Voyage 模型名称，例如 , 等。如果不指定此参数，则将使用 。有关可用模型的列表，请参阅
voyage-3-lite
voyage-finance-2
voyage-3
Voyage 官方文档
。
api_key
(字符串）访问 Voyage API 的 API 密钥。有关如何创建 API 密钥的信息，请参阅
API 密钥和 Python 客户端
。
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

docs_embeddings = voyage_ef.encode_documents(docs)
# Print embeddings
print
(
"Embeddings:"
, docs_embeddings)
# Print dimension and shape of embeddings
print
(
"Dim:"
, voyage_ef.dim, docs_embeddings[
0
].shape)
预期输出类似于下图：
Embeddings: [array([
0.02582654
, -
0.00907086
, -
0.04604037
, ..., -
0.01227521
,
0.04420955
, -
0.00038829
]), array([
0.03844212
, -
0.01597065
, -
0.03728884
, ..., -
0.02118733
,
0.03349845
,
0.0065346
]), array([
0.05143557
, -
0.01096631
, -
0.02690451
, ..., -
0.02416254
,
0.07658645
,
0.03064499
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

query_embeddings = voyage_ef.encode_queries(queries)
print
(
"Embeddings:"
, query_embeddings)
print
(
"Dim"
, voyage_ef.dim, query_embeddings[
0
].shape)
预期输出类似于下面的内容：
Embeddings: [array([
0.01733501
, -
0.0230672
, -
0.05208827
, ..., -
0.00957995
,
0.04493361
,
0.01485138
]), array([
0.05937521
, -
0.00729363
, -
0.02184347
, ..., -
0.02107683
,
0.05706626
,
0.0263358
])]
Dim
1024
(
1024
,)