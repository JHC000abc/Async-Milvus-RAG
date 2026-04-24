句子转换器
Milvus 通过
SentenceTransformerEmbeddingFunction
类与
Sentence Transformer
预训练模型集成。该类提供了使用预训练的 Sentence Transformer 模型对文档和查询进行编码的方法，并将嵌入作为与 Milvus 索引兼容的密集向量返回。
要使用该功能，请安装必要的依赖项：
pip install --upgrade pymilvus
pip install
"pymilvus[model]"
然后，实例化
SentenceTransformerEmbeddingFunction
：
from
pymilvus
import
model

sentence_transformer_ef = model.dense.SentenceTransformerEmbeddingFunction(
    model_name=
'all-MiniLM-L6-v2'
,
# Specify the model name
device=
'cpu'
# Specify the device to use, e.g., 'cpu' or 'cuda:0'
)
参数
：
model_name
（字符串）
用于编码的 Sentence Transformer 模型名称。默认值为
all-MiniLM-L6-v2
。您可以使用任何一个 Sentence Transformers 的预训练模型。有关可用模型的列表，请参阅
预训练模型
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

docs_embeddings = sentence_transformer_ef.encode_documents(docs)
# Print embeddings
print
(
"Embeddings:"
, docs_embeddings)
# Print dimension and shape of embeddings
print
(
"Dim:"
, sentence_transformer_ef.dim, docs_embeddings[
0
].shape)
预期输出类似于下图：
Embeddings: [array([-
3.09392996e-02
, -
1.80662833e-02
,
1.34775648e-02
,
2.77156215e-02
,
       -
4.86349640e-03
, -
3.12581174e-02
, -
3.55921760e-02
,
5.76934684e-03
,
2.80773244e-03
,
1.35783911e-01
,
3.59678417e-02
,
6.17732145e-02
,
...
       -
4.61330153e-02
, -
4.85207550e-02
,
3.13997865e-02
,
7.82178566e-02
,
       -
4.75336798e-02
,
5.21207601e-02
,
9.04406682e-02
, -
5.36676683e-02
],
      dtype=float32)]
Dim:
384
(
384
,)
要为查询创建 Embeddings，请使用
encode_queries()
方法：
queries = [
"When was artificial intelligence founded"
,
"Where was Alan Turing born?"
]

query_embeddings = sentence_transformer_ef.encode_queries(queries)
# Print embeddings
print
(
"Embeddings:"
, query_embeddings)
# Print dimension and shape of embeddings
print
(
"Dim:"
, sentence_transformer_ef.dim, query_embeddings[
0
].shape)
预期输出类似于下图：
Embeddings: [array([-
2.52114702e-02
, -
5.29330298e-02
,
1.14570223e-02
,
1.95571519e-02
,
       -
2.46500354e-02
, -
2.66519729e-02
, -
8.48201662e-03
,
2.82961670e-02
,
       -
3.65092754e-02
,
7.50745758e-02
,
4.28900979e-02
,
7.18822703e-02
,
...
       -
6.76431581e-02
, -
6.45996556e-02
, -
4.67132553e-02
,
4.78532910e-02
,
       -
2.31596199e-03
,
4.13446948e-02
,
1.06935494e-01
, -
1.08258888e-01
],
      dtype=float32)]
Dim:
384
(
384
,)