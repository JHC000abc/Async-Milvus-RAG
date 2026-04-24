诺米客
Nomic
模型是由 Nomic AI 开发的一系列高级文本和图像嵌入解决方案，旨在将各种形式的数据转换为密集的数字向量，以捕捉其语义。
Milvus 通过 NomicEmbeddingFunction 类与 Nomic 的嵌入模型集成。该类提供使用 Nomic 嵌入模型对文档和查询进行编码的方法，并将嵌入结果返回为与 Milvus 索引兼容的密集向量。要使用该功能，请从
Nomic Atlas
获取一个 API 密钥。
要使用该功能，请安装必要的依赖项：
pip install --upgrade pymilvus
pip install
"pymilvus[model]"
然后，实例化 NomicEmbeddingFunction：
# Before accessing the Nomic Atlas API, configure your Nomic API token
import
nomic
nomic.login(
'YOUR_NOMIC_API_KEY'
)
# Import Nomic embedding function
from
pymilvus.model.dense
import
NomicEmbeddingFunction

ef = NomicEmbeddingFunction(
    model_name=
"nomic-embed-text-v1.5"
,
# Defaults to `mistral-embed`
)
参数
：
model_name
(字符串）
用于编码的 Nomic 嵌入模型名称。默认值为
nomic-embed-text-v1.5
。更多信息，请参阅
Nomic 官方文档
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
Embeddings: [array([
5.59997560e-02
,
7.23266600e-02
, -
1.51977540e-01
, -
4.53491200e-02
,
6.49414060e-02
,
4.33654800e-02
,
2.26593020e-02
, -
3.51867680e-02
,
3.49998470e-03
,
1.75571440e-03
, -
4.30297850e-03
,
1.81274410e-02
,
        ...
       -
1.64337160e-02
, -
3.85437000e-02
,
6.14318850e-02
, -
2.82745360e-02
,
       -
7.25708000e-02
, -
4.15563580e-04
, -
7.63320900e-03
,
1.88446040e-02
,
       -
5.78002930e-02
,
1.69830320e-02
, -
8.91876200e-03
, -
2.37731930e-02
])]
Dim:
768
(
768
,)
要为查询创建嵌入式编码，请使用
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
预期输出类似于以下内容：
Embeddings: [array([
3.24096680e-02
,
7.35473600e-02
, -
1.63940430e-01
, -
4.45556640e-02
,
7.83081050e-02
,
2.64587400e-02
,
1.35898590e-03
, -
1.59606930e-02
,
       -
3.33557130e-02
,
1.05056760e-02
, -
2.35290530e-02
,
2.23388670e-02
,
        ...
7.67211900e-02
,
4.54406740e-02
,
9.70459000e-02
,
4.00161740e-03
,
       -
3.12805180e-02
, -
7.05566400e-02
,
5.04760740e-02
,
5.22766100e-02
,
       -
3.87878400e-02
, -
3.03649900e-03
,
5.90515140e-03
, -
1.95007320e-02
])]
Dim
768
(
768
,)