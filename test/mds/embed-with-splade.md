SPLADE
SPLADE
Embeddings 是一种为文档和查询提供高度稀疏表示的模型，它继承了词袋（BOW）模型的理想特性，如精确的术语匹配和效率。
Milvus 通过
SpladeEmbeddingFunction
类与 SPLADE 模型集成。该类提供了对文档和查询进行编码并将嵌入作为与 Milvus 索引兼容的稀疏向量返回的方法。
要使用该功能，请安装必要的依赖项：
pip install --upgrade pymilvus
pip install
"pymilvus[model]"
要实例化
SpladeEmbeddingFunction
，请使用以下命令：
from
pymilvus
import
model

splade_ef = model.sparse.SpladeEmbeddingFunction(
    model_name=
"naver/splade-cocondenser-selfdistil"
, 
    device=
"cpu"
)
参数
：
model_name
（字符串）
用于编码的 SPLADE 模型名称。有效选项包括：
naver/splade-cocondenser-ensembledistil
（默认）、
naver/splade_v2_max
、
naver/splade_v2_distil
和
naver/splade-cocondenser-selfdistil
。更多信息，请参阅
玩转模型
。
设备
（字符串）
要使用的设备，
cpu
表示 CPU，
cuda:n
表示第 n 个 GPU 设备。
要为文档创建
Embeddings
，请使用
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

docs_embeddings = splade_ef.encode_documents(docs)
# Print embeddings
print
(
"Embeddings:"
, docs_embeddings)
# since the output embeddings are in a 2D csr_array format, we convert them to a list for easier manipulation.
print
(
"Sparse dim:"
, splade_ef.dim,
list
(docs_embeddings)[
0
].shape)
预期输出类似于下图：
Embeddings:   (
0
,
2001
)
0.6392706036567688
(
0
,
2034
)
0.024093208834528923
(
0
,
2082
)
0.3230178654193878
...
  (
2
,
23602
)
0.5671860575675964
(
2
,
26757
)
0.5770265460014343
(
2
,
28639
)
3.1990697383880615
Sparse dim:
30522
(
1
,
30522
)
要为查询创建 Embeddings，请使用
encode_queries()
方法：
queries = [
"When was artificial intelligence founded"
,
"Where was Alan Turing born?"
]

query_embeddings = splade_ef.encode_queries(queries)
# Print embeddings
print
(
"Embeddings:"
, query_embeddings)
# since the output embeddings are in a 2D csr_array format, we convert them to a list for easier manipulation.
print
(
"Sparse dim:"
, splade_ef.dim,
list
(query_embeddings)[
0
].shape)
预期输出类似于下图：
Embeddings:   (
0
,
2001
)
0.6353746056556702
(
0
,
2194
)
0.015553371049463749
(
0
,
2301
)
0.2756537199020386
...
  (
1
,
18522
)
0.1282549500465393
(
1
,
23602
)
0.13133203983306885
(
1
,
28639
)
2.8150033950805664
Sparse dim:
30522
(
1
,
30522
)