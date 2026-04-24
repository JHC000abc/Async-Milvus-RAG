BGE M3
BGE-M3
因其在多语言、多功能和多粒度方面的能力而得名。BGE-M3 能够支持 100 多种语言，为多语言和跨语言检索任务树立了新的标杆。它在单一框架内执行密集检索、多向量检索和稀疏检索的独特能力，使其成为各种信息检索（IR）应用的理想选择。
Milvus 使用
BGEM3EmbeddingFunction
类与 BGE M3 模型集成。该类处理嵌入的计算，并以与 Milvus 兼容的格式返回，用于索引和搜索。要使用此功能，必须安装 FlagEmbedding。
要使用此功能，请安装必要的依赖项：
pip install --upgrade pymilvus
pip install
"pymilvus[model]"
然后，实例化
BGEM3EmbeddingFunction
：
from
pymilvus.model.hybrid
import
BGEM3EmbeddingFunction

bge_m3_ef = BGEM3EmbeddingFunction(
    model_name=
'BAAI/bge-m3'
,
# Specify the model name
device=
'cpu'
,
# Specify the device to use, e.g., 'cpu' or 'cuda:0'
use_fp16=
False
# Specify whether to use fp16. Set to `False` if `device` is `cpu`.
)
参数
：
model_name
（字符串）
用于编码的模型名称。默认值为
BAAI/bge-m3
。
设备
（字符串）
要使用的设备，
cpu
表示 CPU，
cuda:n
表示第 n 个 GPU 设备。
use_fp16
（bool）
是否使用 16 位浮点精度（fp16）。当
设备
为
cpu
时指定为
False
。
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

docs_embeddings = bge_m3_ef.encode_documents(docs)
# Print embeddings
print
(
"Embeddings:"
, docs_embeddings)
# Print dimension of dense embeddings
print
(
"Dense document dim:"
, bge_m3_ef.dim[
"dense"
], docs_embeddings[
"dense"
][
0
].shape)
# Since the sparse embeddings are in a 2D csr_array format, we convert them to a list for easier manipulation.
print
(
"Sparse document dim:"
, bge_m3_ef.dim[
"sparse"
],
list
(docs_embeddings[
"sparse"
])[
0
].shape)
预期输出类似于下图：
Embeddings: {
'dense'
: [array([-
0.02505937
, -
0.00142193
,
0.04015467
, ..., -
0.02094924
,
0.02623661
,
0.00324098
], dtype=float32), array([
0.00118463
,
0.00649292
, -
0.00735763
, ..., -
0.01446293
,
0.04243685
, -
0.01794822
], dtype=float32), array([
0.00415287
, -
0.0101492
,
0.0009811
, ..., -
0.02559666
,
0.08084674
,
0.00141647
], dtype=float32)],
'sparse'
: <3x250002 sparse array of
type
'<class '
numpy.float32
'>'
with
43
stored elements
in
Compressed Sparse Row
format
>}
Dense document dim:
1024
(
1024
,)
Sparse document dim:
250002
(
1
,
250002
)
要为查询创建 Embeddings，请使用
encode_queries()
方法：
queries = [
"When was artificial intelligence founded"
,
"Where was Alan Turing born?"
]

query_embeddings = bge_m3_ef.encode_queries(queries)
# Print embeddings
print
(
"Embeddings:"
, query_embeddings)
# Print dimension of dense embeddings
print
(
"Dense query dim:"
, bge_m3_ef.dim[
"dense"
], query_embeddings[
"dense"
][
0
].shape)
# Since the sparse embeddings are in a 2D csr_array format, we convert them to a list for easier manipulation.
print
(
"Sparse query dim:"
, bge_m3_ef.dim[
"sparse"
],
list
(query_embeddings[
"sparse"
])[
0
].shape)
预期输出类似于下图：
Embeddings: {
'dense'
: [array([-
0.02024024
, -
0.01514386
,
0.02380808
, ...,
0.00234648
,
       -
0.00264978
, -
0.04317448
], dtype=float32), array([
0.00648045
, -
0.0081542
, -
0.02717067
, ..., -
0.00380103
,
0.04200587
, -
0.01274772
], dtype=float32)],
'sparse'
: <2x250002 sparse array of
type
'<class '
numpy.float32
'>'
with
14
stored elements
in
Compressed Sparse Row
format
>}
Dense query dim:
1024
(
1024
,)
Sparse query dim:
250002
(
1
,
250002
)