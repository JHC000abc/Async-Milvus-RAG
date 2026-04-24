指导者
Instructor
是一种根据指令调整的文本嵌入模型，只需提供任务指令，无需任何微调，就能生成适合任何任务（如分类、检索、聚类、文本评估等）和领域（如科学、金融等）的文本嵌入。
Milvus 通过 InstructorEmbeddingFunction 类与 Instructor 的嵌入模型集成。该类提供了使用 Instructor 嵌入模型对文档和查询进行编码的方法，并将嵌入作为与 Milvus 索引兼容的稠密向量返回。
要使用该功能，请安装必要的依赖项：
pip install --upgrade pymilvus
pip install
"pymilvus[model]"
然后，实例化 InstructorEmbeddingFunction：
from
pymilvus.model.dense
import
InstructorEmbeddingFunction

ef = InstructorEmbeddingFunction(
    model_name=
"hkunlp/instructor-xl"
,
# Defaults to `hkunlp/instructor-xl`
query_instruction=
"Represent the question for retrieval:"
,
    doc_instruction=
"Represent the document for retrieval:"
)
参数
：
model_name
(字符串）
用于编码的 Mistral AI 嵌入模型名称。默认值为
hkunlp/instructor-xl
。更多信息，请参阅
模型列表
。
query_instruction
（字符串）
特定于任务的指令，用于指导模型如何为查询或问题生成 Embeddings。
doc_instruction
（字符串）
指导模型为文档生成嵌入的特定任务指令。
要为文档创建嵌入，请使用
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
1.08575663e-02
,
3.87877878e-03
,
3.18090729e-02
, -
8.12458917e-02
,
       -
4.68971021e-02
, -
5.85585833e-02
, -
5.95418774e-02
, -
8.55880603e-03
,
       -
5.54775111e-02
, -
6.08020350e-02
,
1.76202394e-02
,
1.06648318e-02
,
       -
5.89960292e-02
, -
7.46861771e-02
,
6.60329172e-03
, -
4.25189249e-02
,
       ...
       -
1.26921125e-02
,
3.01475357e-02
,
8.25323071e-03
, -
1.88470203e-02
,
6.04814291e-03
, -
2.81618331e-02
,
5.91602828e-03
,
7.13866428e-02
],
      dtype=float32)]
Dim:
768
(
768
,)
要为查询创建嵌入，请使用
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
预期输出类似于下面的内容：
Embeddings: [array([
1.21721877e-02
,
1.88485277e-03
,
3.01732980e-02
, -
8.10302645e-02
,
       -
6.13401756e-02
, -
3.98149453e-02
, -
5.18723316e-02
, -
6.76784338e-03
,
       -
6.59285188e-02
, -
5.38365729e-02
, -
5.13435388e-03
, -
2.49210224e-02
,
       -
5.74403182e-02
, -
7.03031123e-02
,
6.63730130e-03
, -
3.42259370e-02
,
       ...
7.36595877e-03
,
2.85532661e-02
, -
1.55952033e-02
,
2.13342719e-02
,
1.51187545e-02
, -
2.82798670e-02
,
2.69396193e-02
,
6.16136603e-02
],
      dtype=float32)]
Dim
768
(
768
,)