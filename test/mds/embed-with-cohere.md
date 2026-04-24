嵌入模型
Cohere 的嵌入模型用于生成文本嵌入，即捕捉文本语义信息的浮点数列表。这些嵌入模型可用于文本分类和语义搜索等任务。
Milvus 使用
CohereEmbeddingFunction
类集成了 Cohere 的嵌入模型。该类处理嵌入的计算，并以与 Milvus 兼容的格式返回，以便进行索引和搜索。
要使用该功能，请安装必要的依赖项：
pip install --upgrade pymilvus
pip install
"pymilvus[model]"
然后，实例化
CohereEmbeddingFunction
：
from
pymilvus.model.dense
import
CohereEmbeddingFunction

cohere_ef = CohereEmbeddingFunction(
    model_name=
"embed-english-light-v3.0"
,
    api_key=
"YOUR_COHERE_API_KEY"
,
    input_type=
"search_document"
,
    embedding_types=[
"float"
]
)
参数
model_name
(字符串）
用于编码的 Cohere Embeddings 模型名称。可以指定任何可用的 Cohere 嵌入模型名称，例如
embed-english-v3.0
,
embed-multilingual-v3.0
等。如果不指定此参数，将使用
embed-english-light-v3.0
。有关可用模型的列表，请参阅
Embed
。
api_key
（字符串）
访问 Cohere API 的 API 密钥。
input_type
（字符串）
传递给模型的输入类型。为嵌入模型 v3 及更高版本所必需。
"search_document"
:用于嵌入存储在向量数据库中的搜索用例。
"search_query"
:用于向量数据库搜索查询的嵌入，以查找相关文档。
"classification"
:用于通过文本分类器进行嵌入。
"clustering"
:用于通过聚类算法运行的嵌入。
embedding_types
(列表[str]
）。
您希望返回的嵌入类型。非必填项，默认为 "无"，即返回 Embed Floats 响应类型。目前只能为该参数指定一个值。可能的值
"float"
:当您想返回默认的浮点嵌入时，请使用此参数。对所有模型有效。
"binary"
:当您要返回带符号的二进制嵌入时使用此值。仅对 v3 模型有效。
"ubinary"
:当您要返回无符号二进制嵌入时使用此选项。仅对 v3 模型有效。
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

docs_embeddings = cohere_ef.encode_documents(docs)
# Print embeddings
print
(
"Embeddings:"
, docs_embeddings)
# Print dimension and shape of embeddings
print
(
"Dim:"
, cohere_ef.dim, docs_embeddings[
0
].shape)
预期输出类似于下图：
Embeddings: [array([
3.43322754e-02
,
1.16252899e-03
, -
5.25207520e-02
,
1.32846832e-03
,
       -
6.80541992e-02
,
6.10961914e-02
, -
7.06176758e-02
,
1.48925781e-01
,
1.54174805e-01
,
1.98516846e-02
,
2.43835449e-02
,
3.55224609e-02
,
1.82952881e-02
,
7.57446289e-02
, -
2.40783691e-02
,
4.40063477e-02
,
...
0.06359863
, -
0.01971436
, -
0.02253723
,
0.00354195
,
0.00222015
,
0.00184727
,
0.03408813
, -
0.00777817
,
0.04919434
,
0.01519775
,
       -
0.02862549
,
0.04760742
, -
0.07891846
,
0.0124054
], dtype=float32)]
Dim:
384
(
384
,)
要为查询创建嵌入式数据，请使用
encode_queries()
方法：
queries = [
"When was artificial intelligence founded"
,
"Where was Alan Turing born?"
]

query_embeddings = cohere_ef.encode_queries(queries)
print
(
"Embeddings:"
, query_embeddings)
print
(
"Dim"
, cohere_ef.dim, query_embeddings[
0
].shape)
预期输出类似于下面的内容：
Embeddings: [array([-
1.33361816e-02
,
9.79423523e-04
, -
7.28759766e-02
, -
1.93786621e-02
,
       -
9.71679688e-02
,
4.34875488e-02
, -
9.81445312e-02
,
1.16882324e-01
,
5.89904785e-02
, -
4.19921875e-02
,
4.95910645e-02
,
5.83496094e-02
,
3.47595215e-02
, -
5.87463379e-03
, -
7.30514526e-03
,
2.92816162e-02
,
...
0.00749969
, -
0.01192474
,
0.02719116
,
0.03347778
,
0.07696533
,
0.01409149
,
0.00964355
, -
0.01681519
, -
0.0073204
,
0.00043154
,
       -
0.04577637
,
0.03591919
, -
0.02807617
, -
0.04812622
], dtype=float32)]
Dim
384
(
384
,)