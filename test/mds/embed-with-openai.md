OpenAI
Milvus 通过
OpenAIEmbeddingFunction
类与 OpenAI 的模型集成。该类提供了使用预训练的 OpenAI 模型对文档和查询进行编码的方法，并将嵌入作为与 Milvus 索引兼容的密集向量返回。要使用该功能，请通过在
OpenAI
平台上创建账户从
OpenAI
获取 API 密钥。
要使用该功能，请安装必要的依赖项：
pip install --upgrade pymilvus
pip install
"pymilvus[model]"
然后，实例化
OpenAIEmbeddingFunction
：
from
pymilvus
import
model

openai_ef = model.dense.OpenAIEmbeddingFunction(
    model_name=
'text-embedding-3-large'
,
# Specify the model name
api_key=
'YOUR_API_KEY'
,
# Provide your OpenAI API key
dimensions=
512
# Set the embedding dimensionality
)
参数
：
model_name
（字符串）
用于编码的 OpenAI 模型名称。有效选项为
text-embedding-3-small
、
text-
embedding-
3-large
和
text-embedding-ada-002
（默认）。
api_key
（字符串）
访问 OpenAI API 的 API 密钥。
base_url
（字符串）
访问 OpenAI API 的基本 URL。该值默认为
https://api.openai.com/v1。
不过，如果访问的是不同模型提供商或本地 vLLM 实例（如
http://localhost:8080/v1
）的兼容 API 端点，则可以在此处指定 URL。
维数
（整数）
输出嵌入结果的维数。仅支持
text-embedding-3
及更高版本的模型。
要创建文档嵌入，请使用
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

docs_embeddings = openai_ef.encode_documents(docs)
# Print embeddings
print
(
"Embeddings:"
, docs_embeddings)
# Print dimension and shape of embeddings
print
(
"Dim:"
, openai_ef.dim, docs_embeddings[
0
].shape)
预期输出类似于下图：
Embeddings: [array([
1.76741909e-02
, -
2.04964578e-02
, -
1.09788161e-02
, -
5.27223349e-02
,
4.23139781e-02
, -
6.64533582e-03
,
4.21088142e-03
,
1.04644023e-01
,
5.10009527e-02
,
5.32827862e-02
, -
3.26061808e-02
, -
3.66494283e-02
,
...
       -
8.93232748e-02
,
6.68255147e-03
,
3.55093405e-02
, -
5.09071983e-02
,
3.74144339e-03
,
4.72541340e-02
,
2.11916920e-02
,
1.00753829e-02
,
       -
5.76633997e-02
,
9.68257990e-03
,
4.62721288e-02
, -
4.33261096e-02
])]
Dim:
512
(
512
,)
要为查询创建嵌入信息，请使用
encode_queries()
方法：
queries = [
"When was artificial intelligence founded"
,
"Where was Alan Turing born?"
]

query_embeddings = openai_ef.encode_queries(queries)
# Print embeddings
print
(
"Embeddings:"
, query_embeddings)
# Print dimension and shape of embeddings
print
(
"Dim"
, openai_ef.dim, query_embeddings[
0
].shape)
预期输出类似于下图：
Embeddings: [array([
0.00530251
, -
0.01907905
, -
0.01672608
, -
0.05030033
,
0.01635982
,
       -
0.03169853
, -
0.0033602
,
0.09047844
,
0.00030747
,
0.11853652
,
       -
0.02870182
, -
0.01526102
,
0.05505067
,
0.00993909
, -
0.07165466
,
...
       -
9.78106782e-02
, -
2.22669560e-02
,
1.21873049e-02
, -
4.83198799e-02
,
5.32377362e-02
, -
1.90469325e-02
,
5.62430918e-02
,
1.02650477e-02
,
       -
6.21757433e-02
,
7.88027793e-02
,
4.91846527e-04
, -
1.51633881e-02
])]
Dim
512
(
512
,)