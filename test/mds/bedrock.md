贝德洛克
Compatible with Milvus 2.6.x
本主题介绍如何在 Milvus 中配置和使用 Amazon Bedrock 嵌入功能。
选择嵌入模型
Milvus 支持 Amazon Bedrock 提供的嵌入模型。以下是当前可用的嵌入模型，供快速参考：
模型名称
尺寸
最大代币数
描述
amazon.titan-embed-text-v2:0
1,024（默认）、512、256
8,192
Rerankers、文档搜索、重排、分类等。
有关详情，请参阅
Amazon Titan Text Embeddings 模型
。
配置凭证
Milvus 必须知道你的 Bedrock 访问凭证，然后才能请求嵌入。Milvus 提供两种配置凭据的方法：
配置文件（推荐）：
将凭据存储在
milvus.yaml
中，以便每次重启和节点都能自动获取。
环境变量：
在部署时注入凭据--最适合 Docker Compose。
从以下两种方法中选择一种--配置文件在裸机和虚拟机上更容易维护，而环境变量方法适合容器工作流。
如果配置文件和环境变量中同时存在同一提供商的凭据，Milvus 将始终使用
milvus.yaml
中的值，而忽略环境变量。
选项 1：配置文件（推荐且优先级更高）
将凭据保存在
milvus.yaml
中；Milvus 会在启动时读取它们，并覆盖同一提供商的任何环境变量。
**在以下位置声明你的证书
credential:
你可以列出一个或多个凭据--给每个凭据贴上你自创的标签，稍后再引用。
# milvus.yaml
credential:
aksk_dev:
# dev environment
access_key_id:
<YOUR_DEV_ACCESS_KEY_ID>
secret_access_key:
<YOUR_DEV_SECRET_ACCESS_KEY>
aksk_prod:
# production environment
access_key_id:
<YOUR_PROD_ACCESS_KEY_ID>
secret_access_key:
<YOUR_PROD_SECRET_ACCESS_KEY>
将证书放在这里，可以使它们在重启时保持不变，并让你只需更改标签就能切换证书。
告诉 Milvus 调用服务时使用哪个证书
在同一文件中，将 Bedrock 提供程序指向你希望它使用的标签。
function:
textEmbedding:
providers:
bedrock:
credential:
aksk_dev
# ← choose any label you defined above
这样，Milvus 向 Bedrock 嵌入服务发送的每个请求都会绑定一个特定的凭据。
方案 2：环境变量
当你使用 Docker Compose 运行 Milvus，并希望不对文件和映像保密时，请使用这种方法。
只有在
milvus.yaml
中找不到提供者的凭据时，Milvus 才会使用环境变量。
变量
需要
描述
MILVUSAI_BEDROCK_ACCESS_KEY_ID
是
您的 AWS 访问密钥 ID，用于 Bedrock 服务的身份验证。
MILVUSAI_BEDROCK_SECRET_ACCESS_KEY
是
与访问密钥 ID 相对应的 AWS 秘密访问密钥。
在
docker-compose.yaml
文件中，设置
MILVUSAI_OPENAI_API_KEY
环境变量。
# docker-compose.yaml (standalone service section)
standalone:
# ... other configurations ...
environment:
# ... other environment variables ...
# Set the environment variable pointing to the Bedrock embedding service inside the container
MILVUSAI_BEDROCK_ACCESS_KEY_ID:
<MILVUSAI_BEDROCK_ACCESS_KEY_ID>
MILVUSAI_BEDROCK_SECRET_ACCESS_KEY:
<MILVUSAI_BEDROCK_SECRET_ACCESS_KEY>
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
用于存储将由函数模块生成的嵌入。切记要设置向量维数 (
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
1024
)
第 2 步：向 Schema 添加函数
Milvus 中的 Function 模块会自动将标量字段中存储的原始数据转换为嵌入数据，并将其存储到明确定义的向量字段中。
下面的示例添加了一个 Function 模块 (
bedrk
)，该模块将标量域
"document"
转换为嵌入，将得到的向量存储到之前定义的
"dense"
向量域中。
定义好嵌入函数后，将其添加到 Collections Schema 中。这将指示 Milvus 使用指定的嵌入函数来处理和存储文本数据中的嵌入。
# Define embedding function specifically for OpenAI provider
text_embedding_function = Function(
    name=
"bedrk"
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
# Provider-specific embedding parameters (function-level)
"provider"
:
"bedrock"
,
# Must be set to "bedrock"
"model_name"
:
"amazon.titan-embed-text-v2:0"
,
# Specifies the embedding model to use
"region"
:
"us-east-2"
,
# Required: AWS region where the Bedrock service is hosted
# Optional parameters:
# "credential": "aksk_dev",               # Optional: Credential label specified in milvus.yaml
# "dim": "1024",                          # Output dimension of the vector embeddings after truncation
# "normalize": "true",                    # Whether to normalize the output embeddings
}
)
# Add the configured embedding function to your existing collection schema
schema.add_function(text_embedding_function)
下一步
配置好嵌入函数后，请参阅 "
功能概述
"，了解有关索引配置、数据插入示例和语义搜索操作的其他指导。