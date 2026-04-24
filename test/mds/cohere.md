Cohere
Compatible with Milvus 2.6.x
本主题介绍如何在 Milvus 中配置和使用 Cohere 嵌入功能。
选择嵌入模型
Milvus 支持 Cohere 提供的嵌入模型。以下是当前可用的嵌入模型，供快速参考：
模型名称
尺寸
最大标记数
描述
embed-english-v3.0
1,024
512
可对文本进行分类或将其转化为 Embeddings 的模型。仅限英语。
embed-multilingual-v3.0
1,024
512
提供多语言分类和嵌入支持。
在此查看支持的语言
。
embed-english-light-v3.0
384
512
embed-english-v3.0
更小、更快的版本。功能差不多，但速度更快。仅支持英语。
embed-multilingual-light-v3.0
384
512
embed-multilingual-v3.0
的更小更快版本。功能几乎一样，但速度更快。支持多种语言。
embed-english-v2.0
4,096
512
较早的嵌入式模型，可对文本进行分类或将其转化为嵌入式。仅支持英语。
embed-english-light-v2.0
1,024
512
embed-english-v2.0 更小、更快的版本。功能差不多，但速度更快。仅支持英语。
embed-multilingual-v2.0
768
256
提供多语言分类和嵌入支持。
在此查看支持的语言
。
有关详情，请参阅
Cohere 的嵌入模型
。
配置证书
Milvus 必须知道您的 Cohere API 密钥，才能请求嵌入。Milvus 提供两种配置凭据的方法：
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
告诉 Milvus 调用 OpenAI 时使用哪个密钥
在同一文件中，将 Cohere 提供程序指向您希望它使用的标签。
function:
textEmbedding:
providers:
cohere:
credential:
apikey_dev
# ← choose any label you defined above
# url: https://api.cohere.com/v2/embed   # (optional) custom url
这样，Milvus 向 Cohere embeddings 端点发送的每个请求都会绑定特定密钥。
方案 2：环境变量
当你使用 Docker Compose 运行 Milvus，并希望不对文件和镜像保密时，请使用这种方法。
只有在
milvus.yaml
中找不到提供程序的密钥时，Milvus 才会使用环境变量。
变量
需要
描述
MILVUSAI_COHERE_API_KEY
是
有效的 Cohere API 密钥。
在
docker-compose.yaml
文件中，设置
MILVUSAI_COHERE_API_KEY
环境变量。
# docker-compose.yaml (standalone service section)
standalone:
# ... other configurations ...
environment:
# ... other environment variables ...
# Set the environment variable pointing to the OpenAI API key inside the container
MILVUSAI_COHERE_API_KEY:
<MILVUSAI_COHERE_API_KEY>
environment:
块只将密钥注入 Milvus 容器，而不会触及主机操作系统。有关详情，请参阅
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
1024
)
第 2 步：向 Schema 添加嵌入函数
Milvus 中的 Function 模块会自动将标量字段中存储的原始数据转换为嵌入数据，并将其存储到明确定义的向量字段中。
下面的示例添加了一个 Function 模块 (
cohere_func
)，该模块将标量域
"document"
转换为嵌入，将得到的向量存储到之前定义的
"dense"
向量域中。
定义好嵌入函数后，将其添加到 Collections Schema 中。这将指示 Milvus 使用指定的嵌入函数来处理和存储文本数据中的嵌入。
# Define embedding function specifically for embedding model provider
text_embedding_function = Function(
    name=
"cohere_func"
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
"cohere"
,
# Must be set to "cohere"
"model_name"
:
"embed-english-v3.0"
,
# Specifies the embedding model to use
# Optional parameters:
# "credential": "apikey_dev",               # Optional: Credential label specified in milvus.yaml
# "url": "https://api.cohere.com/v2/embed",     # Defaults to the official endpoint if omitted
# "truncate": "NONE",                           # Specifies how the API will handle inputs longer than the maximum token length.
}
)
# Add the configured embedding function to your existing collection schema
schema.add_function(text_embedding_function)
下一步
配置好嵌入函数后，请参阅 "
功能概述
"，了解有关索引配置、数据插入示例和语义搜索操作的更多指导。