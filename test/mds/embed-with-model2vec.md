Model2Vec
Model2Vec
是一种轻量级、高性能的 Embeddings 技术，可将 Sentence Transformer 模型转换为紧凑的静态模型。它可将模型大小缩小 50 倍，推理速度提高 500 倍，而性能损失却微乎其微。Model2Vec 是资源有限设备的理想选择。
Milvus 通过
Model2VecEmbeddingFunction
类与
Model2Vec
的模型集成。该类提供了使用预训练的 Model2Vec 模型对文档和查询进行编码的方法，并将嵌入作为与 Milvus 索引兼容的密集向量返回。
它既支持从 Hugging Face 中枢加载模型，也支持上传本地 Model2Vec 模型，为在各种环境中部署提供了灵活性。
要使用此功能，请安装必要的依赖项：
pip install --upgrade pymilvus
pip install
"pymilvus[model]"
然后，实例化
Model2VecEmbeddingFunction
：
from
pymilvus
import
model

model2vec_ef = model.dense.Model2VecEmbeddingFunction(
    model_source=
'minishlab/potion-base-8M'
,
# or local directory
)
参数
：
model_source
（字符串）
指定用于生成嵌入的 Model2Vec 模型的源。它支持两种加载模型的方法：
从 Hugging Face Hub 加载（推荐）：
以字符串形式提供模型名称（如
"minishlab/potion-base-8M"
）。
模型选项列举如下：
minishlab/potion-base-8M
默认
minishlab/potion-base-4M
minishlab/potion-base-2M
minishlab/potion-base-32M
minishlab/potion-retrieval-32M
本地加载：
提供存储 Model2Vec 模型的本地文件路径（例如，
"/path/to/local/model"
）。
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

docs_embeddings = model2vec_ef.encode_documents(docs)
# Print embeddings
print
(
"Embeddings:"
, docs_embeddings)
# Print dimension and shape of embeddings
print
(
"Dim:"
, model2vec_ef.dim, docs_embeddings[
0
].shape)
预期输出类似于下图：
Embeddings: [array([
0.02220882
,
0.11436888
, -
0.15094341
,
0.08149259
,
0.20425692
,
       -
0.15727402
, -
0.25320682
, -
0.00669029
,
0.03157463
,
0.08974048
,
       -
0.00148778
, -
0.01803541
,
0.00230828
, -
0.0137875
, -
0.19242321
,
...
       -
7.29782460e-03
, -
2.15345751e-02
, -
4.13905866e-02
,
3.70773636e-02
,
5.45082428e-02
,
1.36436718e-02
,
1.38598625e-02
,
3.91175086e-03
],
      dtype=float32)]
Dim:
256
(
256
,)
要为查询创建 Embeddings，请使用
encode_queries()
方法：
queries = [
"When was artificial intelligence founded"
,
"Where was Alan Turing born?"
]

query_embeddings = model2vec_ef.encode_queries(queries)
# Print embeddings
print
(
"Embeddings:"
, query_embeddings)
# Print dimension and shape of embeddings
print
(
"Dim"
, model2vec_ef.dim, query_embeddings[
0
].shape)
预期输出类似于下图：
Embeddings: [array([-
1.87109038e-02
, -
2.81724217e-03
, -
1.67356253e-01
, -
5.30372337e-02
,
1.08304240e-01
, -
1.09269567e-01
, -
2.53464818e-01
, -
1.77880954e-02
,
3.05427872e-02
,
1.68244764e-01
, -
7.25950347e-03
, -
2.52178032e-02
,
...
8.60440824e-03
,
2.12906860e-03
,
1.50156394e-02
, -
1.29304864e-02
,
       -
3.66544276e-02
,
5.01735881e-03
, -
1.53137008e-02
,
9.57900891e-04
],
      dtype=float32)]
Dim
256
(
256
,)