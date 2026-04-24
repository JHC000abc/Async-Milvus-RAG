嵌入概述
Embeddings 是一种机器学习概念，用于将数据映射到高维空间，将语义相似的数据放在一起。嵌入模型通常是 BERT 或其他 Transformer 系列中的深度神经网络，可以用一系列称为向量的数字有效地表示文本、图像和其他数据类型的语义。这些模型的一个主要特点是，向量之间在高维空间中的数学距离可以表示原始文本或图像语义的相似性。这一特性开启了许多信息检索应用，如谷歌和必应等网络搜索引擎、电子商务网站上的产品搜索和推荐，以及最近流行的生成式人工智能中的检索增强生成（RAG）范式。
嵌入有两大类，每一类都能产生不同类型的向量：
密集嵌入
：大多数嵌入模型将信息表示为数百到数千维的浮点向量。由于大多数维度的值都不为零，因此输出的向量被称为 "密集 "向量。例如，流行的开源嵌入模型 BAAI/bge-base-en-v1.5 输出的向量为 768 个浮点数（768 维浮点向量）。
稀疏嵌入
：相比之下，稀疏嵌入的输出向量大部分维数为零，即 "稀疏 "向量。这些向量通常具有更高的维度（数万或更多），这是由标记词汇量的大小决定的。稀疏向量可由深度神经网络或文本语料库统计分析生成。由于稀疏嵌入向量具有可解释性和更好的域外泛化能力，越来越多的开发人员采用稀疏嵌入向量作为高密度嵌入向量的补充。
Milvus 是一个向量数据库，专为向量数据管理、存储和检索而设计。通过整合主流的嵌入和
重排
模型，您可以轻松地将原始文本转换为可搜索的向量，或使用强大的模型对结果进行重排，从而获得更准确的 Rerankers 结果。这种集成简化了文本转换，无需额外的嵌入或重排组件，从而简化了 RAG 的开发和验证。
要在实际操作中创建嵌入，请参阅
使用 PyMilvus 的模型生成文本嵌入
。
嵌入函数
类型
API 或开源
openai
密集
API
句子转换器
密集
开源
SPLADE
稀疏
开源
bge-m3
混合
开源
远航
密集型
应用程序接口
jina
密集
API
cohere
密集
API
指导员
密集
开源
Mistral AI
密集
应用程序接口
Nomic
密集
API
mGTE
混合型
开源
Model2Vec
混合型
开源
双子座
混合型
私有
例 1：使用默认嵌入函数生成密集向量
要在 Milvus 中使用嵌入函数，首先要安装 PyMilvus 客户端库和
model
子包，该子包封装了嵌入生成的所有实用程序。
pip install
"pymilvus[model]"
model
子包支持各种嵌入模型，从
OpenAI
、
Sentence Transformers
、
BGE M3
到
SPLADE
预训练模型。为简便起见，本示例使用的
DefaultEmbeddingFunction
是
全-MiniLM-L6-v2
句子转换器模型，该模型约 70MB，首次使用时会下载：
from
pymilvus
import
model
# This will download "all-MiniLM-L6-v2", a light weight model.
ef = model.DefaultEmbeddingFunction()
# Data from which embeddings are to be generated
docs = [
"Artificial intelligence was founded as an academic discipline in 1956."
,
"Alan Turing was the first person to conduct substantial research in AI."
,
"Born in Maida Vale, London, Turing was raised in southern England."
,
]

embeddings = ef.encode_documents(docs)
# Print embeddings
print
(
"Embeddings:"
, embeddings)
# Print dimension and shape of embeddings
print
(
"Dim:"
, ef.dim, embeddings[
0
].shape)
预期输出类似于下面的内容：
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
例 2：使用 BGE M3 模型一次调用生成密集向量和稀疏向量
在本例中，我们使用
BGE M3
混合模型将文本嵌入密集向量和稀疏向量，并用它们检索相关文档。总体步骤如下：
使用 BGE-M3 模型将文本嵌入为密集向量和稀疏向量；
建立一个 Milvus Collections 来存储密集向量和稀疏向量；
将数据插入 Milvus；
搜索并检查结果。
首先，我们需要安装必要的依赖项。
from
pymilvus.model.hybrid
import
BGEM3EmbeddingFunction
from
pymilvus
import
(
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection, AnnSearchRequest, RRFRanker, connections,
)
使用 BGE M3 对文档和查询进行编码，以便进行 Embeddings 检索。
# 1. prepare a small corpus to search
docs = [
"Artificial intelligence was founded as an academic discipline in 1956."
,
"Alan Turing was the first person to conduct substantial research in AI."
,
"Born in Maida Vale, London, Turing was raised in southern England."
,
]
query =
"Who started AI research?"
# BGE-M3 model can embed texts as dense and sparse vectors.
# It is included in the optional `model` module in pymilvus, to install it,
# simply run "pip install pymilvus[model]".
bge_m3_ef = BGEM3EmbeddingFunction(use_fp16=
False
, device=
"cpu"
)

docs_embeddings = bge_m3_ef(docs)
query_embeddings = bge_m3_ef([query])