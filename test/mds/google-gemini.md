谷歌双子座
通过选择一个模型，并使用您的双子座 API 密钥配置 Milvus，即可在 Milvus 中使用谷歌双子座嵌入模型。
选择嵌入模型
Milvus 支持 Google Gemini 提供的嵌入模型。以下是当前可用的 Gemini 嵌入模型，供快速参考：
模型名称
尺寸
最大代币数
描述
gemini-embedding-001
默认：3,072（建议：768、1,536 或 3,072）
8,192
具有灵活维度的文本嵌入模型，使用 Matryoshka Representation Learning (MRL) 训练。
gemini-embeddings-2
默认：3,072（建议：768、1,536 或 3,072）
8,192
Google 首款原生多模态嵌入模型，在统一的嵌入空间中支持文本、图片、视频、音频和文档。
这两种模型都是使用 Matryoshka 表征学习（MRL）技术训练的，可以通过
dim
参数实现灵活的输出维度。建议从 768 维度开始，必要时可扩展到 1,536 或 3,072 维度。更多详情，请参阅
双子座嵌入模型
。
Gemini 嵌入模型还支持
任务类型
参数，可针对特定用例优化嵌入。Milvus 会根据操作符自动设置任务类型：
插入/倒插
：
RETRIEVAL_DOCUMENT
搜索
：
RETRIEVAL_QUERY
您可以通过明确指定
task
参数（如
SEMANTIC_SIMILARITY
,
CLASSIFICATION
,
CLUSTERING
）来覆盖这一点。
配置凭证
Milvus 在请求 Embeddings 之前必须知道您的 Gemini API 密钥。Milvus 提供两种配置凭据的方法：
配置文件（推荐）：
将 API 密钥存储在
milvus.yaml
中，这样每次重启和节点都会自动获取该密钥。
环境变量：
在部署时注入密钥--最适合 Docker Compose。
从以下两种方法中选择一种--配置文件在裸机和虚拟机上更易于维护，而环境变量方法适合容器工作流。
如果同一提供商的 API 密钥同时存在于配置文件和环境变量中，Milvus 将始终使用
milvus.yaml
中的值，而忽略环境变量。
选项 1：配置文件（推荐且优先级更高）
将 API 密钥保存在
milvus.yaml
中；Milvus 会在启动时读取它们，并覆盖同一提供商的任何环境变量。
在凭据下声明你的密钥：
你可以列出一个或多个 API 密钥--给每个密钥贴上你自创的标签，以便日后参考。
# milvus.yaml
credential:
apikey_dev:
# dev environment
apikey:
<YOUR_DEV_KEY>
apikey_prod:
# production environment
apikey:
<YOUR_PROD_KEY>
把 API 密钥放在这里，可以让它们在重启时保持不变，而且只需更改标签就能切换密钥。
告诉 Milvus 在调用 Gemini 时使用哪个密钥
在同一文件中，将 Gemini 提供者指向你希望它使用的标签。
function:
textEmbedding:
providers:
gemini:
credential:
apikey_dev
# ← choose any label you defined above
这样，Milvus 向 Gemini embeddings 端点发送的每个请求都会绑定特定密钥。
方案 2：环境变量
当你使用 Docker Compose 运行 Milvus，并希望不对文件和映像保密时，请使用这种方法。
只有在
milvus.yaml
中找不到提供程序的密钥时，Milvus 才会使用环境变量。
变量
需要
描述
milvus_gemini_api_key
是
让每个 Milvus 容器都能使用 Gemini 密钥（如果在 milvus.yaml 中存在 Gemini 密钥，则忽略该变量）。
在
docker-compose.yaml
文件中，设置
MILVUS_GEMINI_API_KEY
环境变量。
# docker-compose.yaml (standalone service section)
standalone:
# ... other configurations ...
environment:
# ... other environment variables ...
# Set the environment variable pointing to the Gemini API key inside the container
MILVUS_GEMINI_API_KEY:
<YOUR_GEMINI_API_KEY>
environment:
块只将密钥注入 Milvus 容器，而不会触及你的主机操作系统。详情请参阅《
使用 Docker Compose 配置 Milvus
》。
第 1 步：创建具有文本嵌入功能的 Collections
定义 Schema 字段
要使用嵌入功能，请创建一个具有特定 Schema 的 Collections。此 Schema 必须至少包含三个必要字段：
唯一标识 Collections 中每个实体的主字段。
VARCHAR
字段，用于存储要嵌入的原始数据。
一个预留向量字段，用于存储文本嵌入函数将为
VARCHAR
字段生成的密集向量嵌入。
下面的示例定义了一个 Schema 模式，其中一个标量字段
"document"
用于存储文本数据，一个向量字段
"dense"
用于存储将由函数模块生成的嵌入。切记设置向量维数 (
dim
) 以匹配所选嵌入模型的输出。
from
pymilvus
import
MilvusClient, DataType, Function, FunctionType
# Initialize Milvus client
client = MilvusClient(
    uri=
"http://localhost:19530"
,
)
# Create a new schema for the collection
schema = client.create_schema()
# Add primary field "id"
schema.add_field(
"id"
, DataType.INT64, is_primary=
True
, auto_id=
False
)
# Add scalar field "document" for storing textual data
schema.add_field(
"document"
, DataType.VARCHAR, max_length=
9000
)
# Add vector field "dense" for storing embeddings.
# IMPORTANT: Set dim to match the exact output dimension of the embedding model.
# For instance, Gemini's gemini-embedding-001 model outputs 3072-dimensional vectors by default,
# but can be shortened to 768 or 1536 dimensions.
schema.add_field(
"dense"
, DataType.FLOAT_VECTOR, dim=
768
)
定义文本嵌入函数
文本嵌入函数会自动将存储在
VARCHAR
字段中的原始数据转换为嵌入数据，并将其存储到明确定义的向量字段中。
下面的示例添加了一个 Function 模块 (
gemini_embedding
) ，该模块将标量字段
"document"
转换为嵌入式数据，将得到的向量存储到前面定义的
"dense"
向量字段中。
# Define embedding function (example: Gemini provider)
text_embedding_function = Function(
    name=
"gemini_embedding"
,
# Unique identifier for this embedding function
function_type=FunctionType.TEXTEMBEDDING,
# Type of embedding function
input_field_names=[
"document"
],
# Scalar field to embed
output_field_names=[
"dense"
],
# Vector field to store embeddings
params={
# Provider-specific configuration (highest priority)
"provider"
:
"gemini"
,
# Embedding model provider
"model_name"
:
"gemini-embedding-001"
,
# Embedding model
# Optional parameters:
# "credential": "apikey_dev",               # Optional: Credential label specified in milvus.yaml
# "dim": "768",                             # Optional: Output vector dimension (default 3072)
# "task": "RETRIEVAL_DOCUMENT",             # Optional: Task type for embedding optimization
}
)
# Add the embedding function to your schema
schema.add_function(text_embedding_function)
任务参数支持的任务类型：
RETRIEVAL_DOCUMENT
- 优化嵌入式文档索引（默认为插入/上插）。
RETRIEVAL_QUERY
- 为查询检索优化嵌入（默认为搜索）。
SEMANTIC_SIMILARITY
- 优化用于测量文本相似性的嵌入。
CLASSIFICATION
- 优化嵌入式文本分类。
CLUSTERING
- 优化聚类嵌入。
如果没有明确设置，Milvus 会在插入/上载时自动使用
RETRIEVAL_DOCUMENT
，在搜索时自动使用
RETRIEVAL_QUERY
。
配置索引
在定义了包含必要字段和内置函数的 Schema 后，请为您的 Collections 设置索引。为简化这一过程，请使用
AUTOINDEX
作为
index_type
，该选项允许 Milvus 根据数据结构选择和配置最合适的索引类型。
# Prepare index parameters
index_params = client.prepare_index_params()
# Add AUTOINDEX to automatically select optimal indexing method
index_params.add_index(
    field_name=
"dense"
,
    index_type=
"AUTOINDEX"
,
    metric_type=
"COSINE"
)
创建 Collections
现在使用定义的 Schema 和索引参数创建 Collections。
# Create collection named "demo"
client.create_collection(
    collection_name=
'demo'
, 
    schema=schema, 
    index_params=index_params
)
第 2 步：插入数据
设置好集合和索引后，就可以插入原始数据了。在此过程中，您只需提供原始文本。我们之前定义的 Function 模块会为每个文本条目自动生成相应的稀疏向量。
# Insert sample documents
client.insert(
'demo'
, [
    {
'id'
:
1
,
'document'
:
'Milvus simplifies semantic search through embeddings.'
},
    {
'id'
:
2
,
'document'
:
'Vector embeddings convert text into searchable numeric data.'
},
    {
'id'
:
3
,
'document'
:
'Semantic search helps users find relevant information quickly.'
},
])
步骤 3：搜索文本
插入数据后，使用原始查询文本执行语义搜索。Milvus 会自动将你的查询转换成 Embeddings 向量，根据相似度检索相关文档，并返回匹配度最高的结果。
# Perform semantic search
results = client.search(
    collection_name=
'demo'
, 
    data=[
'How does Milvus handle semantic search?'
],
# Use text query rather than query vector
anns_field=
'dense'
,
# Use the vector field that stores embeddings
limit=
1
,
    output_fields=[
'document'
],
)
print
(results)
有关搜索和查询操作的更多信息，请参阅
基本向量搜索
和
查询
。