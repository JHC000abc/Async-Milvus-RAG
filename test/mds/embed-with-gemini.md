双子座
Milvus 通过
GeminiEmbeddingFunction
类与
Gemini
的模型集成。该类提供使用预训练的 Gemini 模型对文档和查询进行编码的方法，并将嵌入作为与 Milvus 索引兼容的密集向量返回。要使用该功能，请通过在
Gemini
平台上创建账户从
Gemini
获取 API 密钥。
要使用此功能，请安装必要的依赖项：
pip install --upgrade pymilvus
pip install
"pymilvus[model]"
然后，实例化
GeminiEmbeddingFunction
：
from
pymilvus
import
model

gemini_ef = model.dense.GeminiEmbeddingFunction(
    model_name=
'gemini-embedding-exp-03-07'
,
# Specify the model name
api_key=
'YOUR_API_KEY'
,
# Provide your OpenAI API key
)
参数
：
model_name
（字符串）
用于编码的 Gemini 模型名称。有效选项为
gemini-embedding-exp-03-07
（默认）、
models/
embedding-001
和
models/text-embedding-004
。
api_key
（字符串）
访问 Gemini API 的 API 密钥。
config
（type.EmbedContentConfig
）嵌入模型的可选配置。
output_dimensionality
可以指定输出嵌入的数量。
可以指定
task_type
，以便为特定任务生成优化的嵌入模型，从而节省时间和成本并提高性能。仅支持
gemini-embedding-exp-03-07
模型。
模型名称
尺寸
gemini-embedding-exp-03-07
3072
(default
),1536,768
模型/嵌入式-001
768
模型/文本嵌入-004
768
任务类型
任务类型
语义相似性
用于生成为评估文本相似性而优化的 Embeddings。
分类
用于生成经过优化的嵌入信息，以便根据预设标签对文本进行分类。
聚类
用于生成经过优化的嵌入信息，以便根据文本的相似性对文本进行聚类。
返回文档（RETRIEVAL_DOCUMENT）、返回查询（RETRIEVAL_QUERY）、问题解答（QUESTION_ANSWERING）和事实验证（FACT_VERIFICATION
用于生成针对文档搜索或信息检索进行优化的嵌入。
代码检索查询
用于根据自然语言查询检索代码块，如数组排序或反向链接列表。代码块的嵌入使用 RETRIEVAL_DOCUMENT 计算。
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

docs_embeddings = gemini_ef.encode_documents(docs)
# Print embeddings
print
(
"Embeddings:"
, docs_embeddings)
# Print dimension and shape of embeddings
print
(
"Dim:"
, gemini_ef.dim, docs_embeddings[
0
].shape)
预期输出类似于下图：
Embeddings: [array([-
0.00894029
,
0.00573813
,
0.013351
, ..., -
0.00042766
,
       -
0.00603091
, -
0.00341043
], shape=(
3072
,)), array([
0.00222347
,
0.03725113
,
0.01152256
, ...,
0.01047272
,
       -
0.01701597
,
0.00565377
], shape=(
3072
,)), array([
0.00661134
,
0.00232328
, -
0.01342973
, ..., -
0.00514429
,
       -
0.02374139
, -
0.00701721
], shape=(
3072
,))]
Dim:
3072
(
3072
,)
要为查询创建嵌入
代码
，请使用
encode_queries()
方法：
queries = [
"When was artificial intelligence founded"
,
"Where was Alan Turing born?"
]

query_embeddings = gemini_ef.encode_queries(queries)
# Print embeddings
print
(
"Embeddings:"
, query_embeddings)
# Print dimension and shape of embeddings
print
(
"Dim"
, gemini_ef.dim, query_embeddings[
0
].shape)
预期输出类似于下面的内容：
Embeddings: [array([-
0.02066572
,
0.02459551
,
0.00707774
, ...,
0.00259341
,
       -
0.01797572
, -
0.00626168
], shape=(
3072
,)), array([
0.00674969
,
0.03023903
,
0.01230692
, ...,
0.00160009
,
       -
0.01710967
,
0.00972728
], shape=(
3072
,))]
Dim
3072
(
3072
,)