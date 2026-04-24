嵌入函数概述
Compatible with Milvus 2.6.x
通过 Milvus 的 Function 模块，您可以自动调用外部嵌入服务提供商（如 OpenAI、AWS Bedrock、Google Vertex AI 等），将原始文本数据转换为向量嵌入。有了 Function 模块，您就不再需要手动与嵌入式 API 接口--Milvus 会处理向提供商发送请求、接收嵌入式数据并将其存储到您的 Collections 中的整个过程。对于语义搜索，您只需要提供原始查询数据，而不需要查询向量。Milvus 使用与您用于接收的相同模型生成查询向量，将其与存储的向量进行比较，并返回最相关的结果。
限制
功能模块嵌入的任何输入字段必须始终包含一个值；如果提供的是空值，模块会出错。
Function 模块只处理 Collections Schema 中明确定义的字段；不会生成动态字段的嵌入。
要嵌入的输入字段必须是
VARCHAR
类型。
Function 模块可将输入字段嵌入到以下地址：
FLOAT_VECTOR
INT8_VECTOR
不支持转换为
BINARY_VECTOR
、
FLOAT16_VECTOR
或
BFLOAT16_VECTOR
。
支持的嵌入服务提供商
提供商
典型模型
Embeddings 类型
验证方法
OpenAI
text-embedding-3-*
FLOAT_VECTOR
API 密钥
Azure OpenAI
基于部署
FLOAT_VECTOR
API 密钥
DashScope
text-embedding-v3
FLOAT_VECTOR
API 密钥
基岩
Amazon.titan-embed-text-v2
FLOAT_VECTOR
AK/SK 对
顶点人工智能
text-embedding-005
FLOAT_VECTOR
GCP 服务帐户 JSON 凭证
Voyage AI
Voyage-3, Voyage-lite-02
FLOAT_VECTOR
/
INT8_VECTOR
API 密钥
嵌入
embed-english-v3.0
FLOAT_VECTOR
/
INT8_VECTOR
API 密钥
SiliconFlow
BAAI/bge-large-zh-v1.5
FLOAT_VECTOR
API 密钥
Hugging Face
任何 TEI 服务的模型
FLOAT_VECTOR
可选的 API 密钥
工作原理
下图显示了该功能在 Milvus 中的工作原理。
输入文本
：用户将原始数据（如文档）输入 Milvus。
生成 Embeddings
：Milvus 中的 Function 模块会自动调用配置的模型提供程序，将原始数据转换为向量嵌入。
存储嵌入
：生成的嵌入会存储在 Milvus Collections 中明确定义的向量字段中。
查询文本
：用户向 Milvus 提交文本查询。
语义搜索
：Milvus 在内部将查询转换为向量嵌入，根据存储的嵌入进行相似性搜索，并检索相关结果。
返回结果
：Milvus 向应用程序返回匹配度最高的结果。
Embeddings 功能概述
配置凭证
在与 Milvus 一起使用嵌入函数之前，请配置嵌入服务凭据以便 Milvus 访问。
Milvus 可通过两种方式提供嵌入服务凭证：
配置文件
(
milvus.yaml
)：
本主题中的示例演示了使用
milvus.yaml
的
推荐设置
。
环境变量
：
有关通过环境变量配置凭据的详细信息，请参阅嵌入服务提供商的文档（例如，
OpenAI
或
Azure OpenAI
）。
下图显示了通过 Milvus 配置文件 (
milvus.yaml
) 配置凭据，然后在 Milvus 内调用函数的过程。
凭证配置溢出
步骤 1：在 Milvus 配置文件中添加凭据
在
milvus.yaml
文件中，编辑
credential
块，为需要访问的每个提供商添加条目：
# milvus.yaml credential store section
# This section defines all your authentication credentials for external embedding providers
# Each credential gets a unique name (e.g., aksk1, apikey1) that you'll reference elsewhere
credential:
# For AWS Bedrock or services using access/secret key pairs
# 'aksk1' is just an example name - you can choose any meaningful identifier
aksk1:
access_key_id:
<YOUR_AK>
secret_access_key:
<YOUR_SK>
# For OpenAI, Voyage AI, or other API key-based services
# 'apikey1' is a custom name you choose to identify this credential
apikey1:
apikey:
<YOUR_API_KEY>
# For Google Vertex AI using service account credentials
# 'gcp1' is an example name for your Google Cloud credentials
gcp1:
credential_json:
<BASE64_OF_JSON>
第 2 步：配置提供商设置
在同一个配置文件 (
milvus.yaml
) 中，编辑
function
块，告诉 Milvus 使用哪个密钥嵌入服务调用：
function:
textEmbedding:
providers:
openai:
# calls OpenAI
credential:
apikey1
# Reference to the credential label
# url:                        # (optional) custom url
bedrock:
# calls AWS Bedrock
credential:
aksk1
# Reference to the credential label
region:
us-east-2
vertexai:
# calls Google Vertex AI
credential:
gcp1
# Reference to the credential label
# url:                        # (optional) custom url
tei:
# Built-in Tiny Embedding model
enable:
true
# Whether to enable TEI model service
有关如何应用 Milvus 配置的更多信息，请参阅《
动态配置 Milvus
》。
使用 Embeddings 功能
在 Milvus 配置文件中配置凭证后，请按照以下步骤定义和使用嵌入函数。
步骤 1：定义 Schema 字段
要使用嵌入功能，请创建一个具有特定 Schema 的 Collections。该 Schema 必须至少包含三个必要字段：
主字段
，用于唯一标识 Collections 中的每个实体。
标量字段
，用于存储要嵌入的原始数据。
一个
向量
字段，用于存储函数将为标量字段生成的向量嵌入。
下面的示例定义了一个 Schema 模式，其中一个标量字段
"document"
用于存储文本数据，一个向量字段
"dense"
用于存储将由函数模块生成的嵌入。切记设置向量维数 (
dim
) 以匹配您所选嵌入模型的输出。
Python
Java
NodeJS
Go
cURL
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
# For instance, OpenAI's text-embedding-3-small model outputs 1536-dimensional vectors.
# For dense vector, data type can be FLOAT_VECTOR or INT8_VECTOR
schema.add_field(
"dense"
, DataType.FLOAT_VECTOR, dim=
1536
)
// java
// nodejs
// go
# restful
第 2 步：向 Schema 添加嵌入函数
Milvus 中的 Function 模块会自动将存储在标量字段中的原始数据转换为嵌入数据，并将其存储到明确定义的向量字段中。
下面的示例添加了一个 Function 模块 (
openai_embedding
) ，该模块可将标量字段
"document"
转换为嵌入，将生成的向量存储到之前定义的
"dense"
向量字段中。
Python
Java
NodeJS
Go
cURL
# Define embedding function (example: OpenAI provider)
text_embedding_function = Function(
    name=
"openai_embedding"
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
"openai"
,
# Embedding model provider
"model_name"
:
"text-embedding-3-small"
,
# Embedding model
# "credential": "apikey1",            # Optional: Credential label
# Optional parameters:
# "dim": "1536",       # Optionally shorten the vector dimension
# "user": "user123"    # Optional: identifier for API tracking
}
)
# Add the embedding function to your schema
schema.add_function(text_embedding_function)
// java
// nodejs
// go
# restful
参数
说明
示例值
name
嵌入函数在 Milvus 中的唯一标识符。
"openai_embedding"
function_type
使用的函数类型。对于文本嵌入，将值设为
FunctionType.TEXTEMBEDDING
。
注
：Milvus 接受
FunctionType.BM25
（用于稀疏嵌入转换）和
FunctionType.RERANK
（用于 Reranker）作为该参数。详情请参阅
全文搜索
和
衰减排名器概述
。
FunctionType.TEXTEMBEDDING
input_field_names
包含要嵌入的原始数据的标量字段。目前，该参数只接受一个字段名称。
["document"]
output_field_names
向量字段，用于存储生成的 Embeddings。目前，该参数只接受一个字段名称。
["dense"]
params
包含嵌入配置的字典。注：
params
中的参数因嵌入模型提供者而异。
{...}
provider
嵌入模型提供者。
"openai"
model_name
指定要使用的嵌入模型。
"text-embedding-3-small"
credential
milvus.yaml
顶层
credential:
部分定义的凭证标签。
提供时，Milvus 会检索匹配的密钥对或 API 令牌，并在服务器端签署请求。
省略时（
None
），Milvus 会退回到
milvus.yaml
中为目标模型提供者明确配置的凭据。
如果标签未知或引用的密钥丢失，则调用失败。
"apikey1"
dim
输出嵌入的维数。对于 OpenAI 的第三代模型，您可以缩短全向量以降低成本和延迟，同时不会损失大量语义信息。更多信息，请参阅
OpenAI 公告博文
。
注意：
如果您缩短了向量维度，请确保 Schema 的
add_field
方法中为向量字段指定的
dim
值与您的嵌入函数的最终输出维度相匹配。
"1536"
user
用于跟踪 API 使用情况的用户级标识符。
"user123"
对于具有多个需要进行文本到向量转换的标量字段的 Collections，请在 Collections Schema 中添加单独的函数，确保每个函数都有唯一的名称和
output_field_names
值。
第 3 步：配置索引
在定义了包含必要字段和内置函数的 Schema 后，请为您的 Collection 设置索引。为简化这一过程，请使用
AUTOINDEX
作为
index_type
，该选项允许 Milvus 根据数据结构选择和配置最合适的索引类型。
Python
Java
NodeJS
Go
cURL
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
// java
// nodejs
// go
# restful
第 4 步：创建 Collections
现在使用定义的 Schema 和索引参数创建 Collections。
Python
Java
NodeJS
Go
cURL
# Create collection named "demo"
client.create_collection(
    collection_name=
'demo'
, 
    schema=schema, 
    index_params=index_params
)
// java
// nodejs
// go
# restful
第 5 步：插入数据
设置好集合和索引后，就可以插入原始数据了。在此过程中，您只需提供原始文本。我们之前定义的 Function 模块会为每个文本条目自动生成相应的稀疏向量。
Python
Java
NodeJS
Go
cURL
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
// java
// nodejs
// go
# restful
步骤 6：执行向量搜索
插入数据后，使用原始查询文本执行语义搜索。Milvus 会自动将查询转换为嵌入向量，根据相似度检索相关文档，并返回匹配度最高的结果。
Python
Java
NodeJS
Go
cURL
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
# Example output:
# data: ["[{'id': 1, 'distance': 0.8821347951889038, 'entity': {'document': 'Milvus simplifies semantic search through embeddings.'}}]"]
// java
// nodejs
// go
# restful
有关搜索和查询操作的更多信息，请参阅
基本向量搜索
和
查询
。
常见问题
在 milvus.yaml 与环境变量中配置证书有什么区别？
两种方法都可以使用，但建议使用
milvus.yaml
，因为它提供了集中的凭据管理和跨所有提供商的一致凭据命名。使用环境变量时，变量名称因嵌入服务提供商而异，因此请参阅每个提供商的专用页面，了解所需的特定环境变量名称（例如，
OpenAI
或
Azure OpenAI
）。
如果我没有在函数定义中指定凭据参数，会发生什么情况？
Milvus 遵循这种凭据解析顺序：
首先，它会在
milvus.yaml
文件中查找为该提供商配置的默认凭据
如果 Milvus.yaml 中不存在默认凭据，它就会返回到环境变量（如果已配置）。
如果
milvus.yaml
凭据和环境变量都没有配置，Milvus 会出错
如何验证 Embeddings 生成是否正确？
您可以通过以下方式进行检查
插入后查询 Collections，查看向量字段是否包含数据
检查向量字段的长度是否符合你的预期尺寸
执行简单的相似性搜索，验证嵌入是否产生了有意义的结果
执行相似性搜索时，可以使用查询向量而不是原始文本吗？
可以，您可以使用预计算的查询向量代替原始文本进行相似性搜索。虽然 Function 模块会自动将原始文本查询转换为嵌入，但您也可以在搜索操作中直接向
data
参数提供向量数据。
注意
：您提供的查询向量的维度大小必须与您的 Function 模块生成的向量嵌入的维度大小一致。
示例
Python
Java
NodeJS
Go
cURL
# Using raw text (Function module converts automatically)
results = client.search(
    collection_name=
'demo'
, 
    data=[
'How does Milvus handle semantic search?'
],
    anns_field=
'dense'
,
    limit=
1
)
# Using pre-computed query vector (must match stored vector dimensions)
query_vector = [
0.1
,
0.2
,
0.3
, ...]
# Must be same dimension as stored embeddings
results = client.search(
    collection_name=
'demo'
, 
    data=[query_vector],
    anns_field=
'dense'
,
    limit=
1
)
// java
// nodejs
// go
# restful