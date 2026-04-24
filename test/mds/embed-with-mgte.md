mGTE
mGTE 是用于文本检索任务的多语言文本表示模型和 Rerankers 模型。
Milvus 通过 MGTEEmbeddingFunction 类与 mGTE 嵌入模型集成。该类提供了使用 mGTE 嵌入模型对文档和查询进行编码的方法，并将嵌入结果返回为与 Milvus 索引兼容的密集向量和稀疏向量。
要使用该功能，请安装必要的依赖项：
pip install --upgrade pymilvus
pip install
"pymilvus[model]"
然后，实例化 MGTEEmbeddingFunction：
from
pymilvus.model.hybrid
import
MGTEEmbeddingFunction

ef = MGTEEmbeddingFunction(
    model_name=
"Alibaba-NLP/gte-multilingual-base"
,
# Defaults to `Alibaba-NLP/gte-multilingual-base`
)
参数
model_name
(字符串）
用于编码的 mGTE 嵌入模型名称。默认值为
Alibaba-NLP/gte-multilingual-base
。
要为文档创建嵌入模型，请使用
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
# Print dimension of embeddings
print
(ef.dim)
预期输出类似于下图：
Embeddings: {
'dense'
: [tensor([-
4.9149e-03
,
1.6553e-02
, -
9.5524e-03
, -
2.1800e-02
,
1.2075e-02
,
1.8500e-02
, -
3.0632e-02
,
5.5909e-02
,
8.7365e-02
,
1.8763e-02
,
2.1708e-03
, -
2.7530e-02
, -
1.1523e-01
,
6.5810e-03
, -
6.4674e-02
,
6.7966e-02
,
1.3005e-01
,
1.1942e-01
, -
1.2174e-02
, -
4.0426e-02
,
        ...
2.0129e-02
, -
2.3657e-02
,
2.2626e-02
,
2.1858e-02
, -
1.9181e-02
,
6.0706e-02
, -
2.0558e-02
, -
4.2050e-02
], device=
'mps:0'
)],
'sparse'
: <Compressed Sparse Row sparse array of dtype
'float64'
with
41
stored elements
and
shape (
3
,
250002
)>}

{
'dense'
:
768
,
'sparse'
:
250002
}
要为查询创建嵌入模型，请使用
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
(ef.dim)
预期输出类似于下面的内容：
Embeddings: {
'dense'
: [tensor([
6.5883e-03
, -
7.9415e-03
, -
3.3669e-02
, -
2.6450e-02
,
1.4345e-02
,
1.9612e-02
, -
8.1679e-02
,
5.6361e-02
,
6.9020e-02
,
1.9827e-02
,
       -
9.2933e-03
, -
1.9995e-02
, -
1.0055e-01
, -
5.4053e-02
, -
8.5991e-02
,
8.3004e-02
,
1.0870e-01
,
1.1565e-01
,
2.1268e-02
, -
1.3782e-02
,
        ...
3.2847e-02
, -
2.3751e-02
,
3.4475e-02
,
5.3623e-02
, -
3.3894e-02
,
7.9408e-02
,
8.2720e-03
, -
2.3459e-02
], device=
'mps:0'
)],
'sparse'
: <Compressed Sparse Row sparse array of dtype
'float64'
with
13
stored elements
and
shape (
2
,
250002
)>}

{
'dense'
:
768
,
'sparse'
:
250002
}