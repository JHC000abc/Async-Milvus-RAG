Hugging Face TEI
Compatible with Milvus 2.6.x
Hugging Face
文本嵌入推理（TEI）
是专为文本嵌入模型设计的高性能推理服务器。本指南介绍了如何将 Hugging Face TEI 与 Milvus 结合使用，以高效生成文本嵌入。
TEI 可与 Hugging Face Hub 的许多文本嵌入模型配合使用，包括
BAAI/bge-* 系列
Sentence-transformers/* 系列
E5 模型
GTE 模型
以及更多
有关支持模型的最新列表，请参阅
TEI GitHub 存储库
和
Hugging Face 中枢
。
TEI 部署
在为 Milvus 配置 TEI 功能之前，您需要有一个正在运行的 TEI 服务。Milvus 支持两种 TEI 部署方法：
标准部署（外部）
您可以使用来自 Hugging Face 的官方方法，将 TEI 作为独立服务进行部署。这种方法为您的 TEI 服务提供了最大的灵活性和控制权。
有关使用 Docker 或其他方法部署 TEI 的详细说明，请参阅
Hugging Face Text Embeddings Inference 官方文档
。
部署完成后，请记下您的 TEI 服务端点（如
http://localhost:8080
），因为
在 Milvus 中使用 TEI 功能
时会用到它。
Milvus Helm 图表部署（已集成）
对于 Kubernetes 环境，Milvus 通过其 Helm 图表提供了集成部署选项。这通过与 Milvus 一起部署和配置 TEI 简化了流程。
在 Milvus Helm 部署中启用 TEI：
配置
values.yaml
以启用 TEI：
tei:
enabled:
true
image:
repository:
ghcr.io/huggingface/text-embeddings-inference
tag:
"1.7"
# Modify based on hardware
model:
"BAAI/bge-large-en-v1.5"
# Modify based on requirements
# revision: "main"
# hfTokenSecretName: "my-huggingface-token-secret"
# apiKey: "your_secure_api_key"
# apiKeySecret:
#   name: "my-tei-api-key-secret"
#   key: "api-key"
resources:
requests:
cpu:
"1"
memory:
"4Gi"
# nvidia.com/gpu: "1" # For GPU
limits:
cpu:
"2"
memory:
"8Gi"
# nvidia.com/gpu: "1" # For GPU
extraArgs:
[]
部署或升级 Milvus：
helm install my-release milvus/milvus -f values.yaml -n <your-milvus-namespace>
# or
helm upgrade my-release milvus/milvus -f values.yaml --reset-then-reuse-values -n <your-milvus-namespace>
使用 Helm 图表部署时，TEI 服务将可在 Kubernetes 集群中访问
http://my-release-milvus-tei:80
（使用您的版本名称）。在 TEI 功能配置中将其用作端点。
在 Milvus 中配置
部署 TEI 服务后，您需要在定义 TEI Embeddings 功能时提供其端点。在大多数情况下，不需要额外的配置，因为 TEI 在 Milvus 中是默认启用的。
不过，如果您的 TEI 服务在部署时使用了 API 密钥验证 (
--api-key
标志)，则需要配置 Milvus 以使用此密钥：
在
credential
部分定义 API 密钥：
# milvus.yaml
credential:
tei_key:
# You can use any label name
apikey:
<YOUR_TEI_API_KEY>
在 milvus.yaml 中引用凭证：
function:
textEmbedding:
providers:
tei:
credential:
tei_key
# ← choose any label you defined above
enable:
true
# enabled by default. no action required.
使用 Embeddings 函数
配置 TEI 服务后，请按照以下步骤定义和使用嵌入函数。
步骤 1：定义 Schema 字段
要使用嵌入函数，请创建一个具有特定 Schema 的 Collections。此 Schema 必须至少包含三个必要字段：
主字段，用于唯一标识 Collections 中的每个实体。
标量字段，用于存储要嵌入的原始数据。
一个向量字段，用于存储函数将为标量字段生成的向量嵌入。
下面的示例定义了一个 Schema 模式，其中一个标量字段
"document"
用于存储文本数据，一个向量字段
"dense_vector"
用于存储将由函数模块生成的嵌入。切记要设置向量维数 (
dim
) 以匹配所选嵌入模型的输出。
from
pymilvus
import
MilvusClient, DataType, Function, FunctionType, CollectionSchema, FieldSchema
# Assume you have connected to Milvus
# client = MilvusClient(uri="http://localhost:19530")
# 1. Create Schema
schema = MilvusClient.create_schema()
# 2. Add fields
schema.add_field(
"id"
, DataType.INT64, is_primary=
True
, auto_id=
False
)
schema.add_field(
"document"
, DataType.VARCHAR, max_length=
9000
)
# Store text data
# IMPORTANT: Set dim to exactly match the TEI model's output dimension
schema.add_field(
"dense_vector"
, DataType.FLOAT_VECTOR, dim=
1024
)
# Store embedding vectors (example dimension)
第 2 步：向 Schema 添加嵌入函数
Milvus 中的 Function 模块会自动将标量字段中存储的原始数据转换为嵌入数据，并将其存储到明确定义的向量字段中。
下面的示例添加了一个 Function 模块 (
tei_func
)，该模块将标量域
"document"
转换为嵌入，将得到的向量存储到之前定义的
"dense_vector"
向量域中。
定义好嵌入函数后，将其添加到 Collections Schema 中。这将指示 Milvus 使用指定的嵌入函数来处理和存储文本数据的嵌入。
# 3. Define TEI embedding function
text_embedding_function = Function(
    name=
"tei_func"
,
# Unique identifier for this embedding function
function_type=FunctionType.TEXTEMBEDDING,
# Indicates a text embedding function
input_field_names=[
"document"
],
# Scalar field(s) containing text data to embed
output_field_names=[
"dense_vector"
],
# Vector field(s) for storing embeddings
params={
# TEI specific parameters (function-level)
"provider"
:
"TEI"
,
# Must be set to "TEI"
"endpoint"
:
"http://your-tei-service-endpoint:80"
,
# Required: Points to your TEI service address
# Optional parameters:
# "truncate": "true",                   # Optional: Whether to truncate long input (default false)
# "truncation_direction": "right",      # Optional: Truncation direction (default right)
# "max_client_batch_size": 64,          # Optional: Client max batch size (default 32)
# "ingestion_prompt": "passage: ",      # Optional: (Advanced) Ingestion phase prompt
# "search_prompt": "query: "            # Optional: (Advanced) Search phase prompt
}
)
# Add the configured embedding function to your existing collection schema
schema.add_function(text_embedding_function)
参数
需要吗？
描述
示例值
provider
是
Embeddings 模型提供者。设置为 "TEI"。
"TEI
endpoint
是
指向已部署 TEI 服务的网络地址。如果通过 Milvus Helm Chart 部署，这通常是内部服务地址。
"http://localhost:8080"、"http://my-release-milvus-tei:80"
truncate
否
是否截断超过模型最大长度的输入文本。默认为假。
真
truncation_direction
否
截断为 true 时有效。指定从左侧还是右侧截断。默认为右侧。
"左"
max_client_batch_size
无
Milvus 客户端发送到 TEI 的最大批量大小。默认为 32。
64
prompt_name
否
(高级）指定 Sentence Transformers 配置提示字典中的键。用于某些需要特定提示格式的模型。TEI 支持可能有限，并取决于 Hub 上的模型配置。
"your_prompt_key
ingestion_prompt
无
(高级）指定在数据插入（摄取）阶段使用的提示。取决于所使用的 TEI 模型；模型必须支持提示。
"passage："
search_prompt
无
(高级）指定在搜索阶段使用的提示。取决于所使用的 TEI 模型；模型必须支持提示。
查询"
下一步
配置完 Embeddings 功能后，请参阅功能
概述
，了解有关索引配置、数据插入示例和语义搜索操作的其他指导。