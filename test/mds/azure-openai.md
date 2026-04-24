Azure OpenAI
Compatible with Milvus 2.6.x
本主题介绍如何在 Milvus 中配置和使用 Azure OpenAI 嵌入函数。
选择嵌入模型
Milvus 支持 Azure OpenAI 提供的所有嵌入模型。以下是当前可用的 Azure OpenAI 嵌入模型，供快速参考：
模型
尺寸
最大令牌数
描述
text-embedding-3-small
默认：1,536（可截断至 1536 以下的尺寸大小）
8,191
成本敏感型和可扩展语义搜索的理想选择--以较低的价格提供较强的性能。
文本-Embeddings-3-大号
默认：3,072（可截断至 3072 以下的尺寸大小）
8,191
最适合需要更高的检索准确性和更丰富的语义表述的应用。
文本嵌入-ADA-002
固定：1,536（不支持截断）
8,191
上一代模型适用于传统管道或需要向后兼容的场景。
第三代嵌入模型
（text-embedding-3
）支持通过
dim
参数减小嵌入的大小。通常情况下，从计算、内存和存储的角度来看，较大的嵌入会更加昂贵。通过调整维数，可以更好地控制总体成本和性能。有关每种模型的更多详情，请参阅
Embeddings
。
配置凭据
Milvus 必须知道你的 Azure OpenAI API 密钥，才能请求嵌入。Milvus 提供两种配置凭据的方法：
配置文件（推荐）：
将 API 密钥存储在
milvus.yaml
中，以便每次重启和节点都能自动获取。
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
**在
credential:
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
告诉 Milvus 在 Azure OpenAI 调用中使用哪个密钥
在同一文件中，将 Azure OpenAI 提供程序指向你希望它使用的标签。
function:
textEmbedding:
providers:
azure_openai:
credential:
apikey_dev
# ← choose any label you defined above
resource_name:
# Your azure openai resource name
# url: # Your azure openai embedding url
这样，Milvus 向 Azure OpenAI embeddings 端点发送的每个请求都会绑定特定密钥。
方案 2：环境变量
当你使用 Docker Compose 运行 Milvus，并希望不对文件和映像保密时，请使用这种方法。
只有在
milvus.yaml
中找不到提供程序的密钥时，Milvus 才会使用环境变量。
变量
需要
描述
MILVUSAI_AZURE_OPENAI_API_KEY
是
使 Azure OpenAI 密钥在每个 Milvus 容器中可用
（当
milvus.yaml
中存在 Azure OpenAI 密钥时忽略
该变量）
MILVUSAI_AZURE_OPENAI_RESOURCE_NAME
是
创建 Azure OpenAI 服务资源时定义的 Azure OpenAI 资源名称。
在
docker-compose.yaml
文件中设置环境变量。
# docker-compose.yaml (standalone service section)
standalone:
# ... other configurations ...
environment:
# ... other environment variables ...
# Set the environment variable pointing to the Azure OpenAI API key inside the container
MILVUSAI_AZURE_OPENAI_API_KEY:
<MILVUSAI_AZURE_OPENAI_API_KEY>
MILVUSAI_AZURE_OPENAI_RESOURCE_NAME:
<MILVUSAI_AZURE_OPENAI_RESOURCE_NAME>
environment:
块只将密钥注入 Milvus 容器，而不会触及你的主机操作系统。有关详情，请参阅
使用 Docker Compose 配置 Milvus
。
使用 Embeddings 功能
配置凭证后，请按照以下步骤定义和使用嵌入函数。
步骤 1：定义 Schema 字段
要使用嵌入函数，请创建一个具有特定 Schema 的 Collections。此 Schema 必须至少包含三个必要字段：
主字段，用于唯一标识 Collections 中的每个实体。
标量字段，用于存储要嵌入的原始数据。
一个向量字段，用于存储函数将为标量字段生成的向量嵌入。
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
schema.add_field(
"dense"
, DataType.FLOAT_VECTOR, dim=
1536
)
第 2 步：向 Schema 添加嵌入函数
定义好嵌入函数后，将其添加到 Collections Schema 中。这将指示 Milvus 使用指定的嵌入函数来处理和存储文本数据的嵌入。
# Define embedding function specifically for Azure OpenAI provider
text_embedding_function = Function(
    name=
"azopenai"
,
# Unique identifier for this embedding function
function_type=FunctionType.TEXTEMBEDDING,
# Indicates a text embedding function
input_field_names=[
"document"
],
# Scalar field(s) containing text data to embed
output_field_names=[
"dense"
],
# Vector field(s) for storing embeddings
params={
# Provider-specific embedding parameters
"provider"
:
"azure_openai"
,
# Embedding provider name (must be "azure_openai")
"model_name"
:
"zilliz-text-embedding-3-small"
,
# Model should be set to the deployment name you chose when you deployed the embedding model
# Optional parameters (only specify if necessary):
# "url": "https://{resource_name}.openai.azure.com/" # Optional: Your Azure OpenAI service endpoint
# "credential": "apikey_dev",               # Optional: Credential label specified in milvus.yaml
# "dim": "1536",                            # Optional: Shorten the output vector dimension
# "user": "user123",                        # Optional: identifier for API tracking
}
)
# Add the configured embedding function to your existing collection schema
schema.add_function(text_embedding_function)
下一步
配置嵌入功能后，请参阅
功能概述
，了解有关索引配置、数据插入示例和语义搜索操作的其他指导。