顶点人工智能
Compatible with Milvus 2.6.x
Google Cloud
Vertex AI
是专为文本嵌入模型设计的高性能服务。本指南介绍如何将 Google Cloud Vertex AI 与 Milvus 结合使用，高效生成文本嵌入。
Vertex AI 支持多种嵌入模型，适用于不同的使用案例：
gemini-embedding-001 （在英语、多语种和代码任务中的一流性能）
text-embedding-005（最新文本嵌入模型）
text-multilingual-embedding-002（最新的多语言文本嵌入模型）
更多信息，请参阅
Vertex AI 文本嵌入模型
。
前提条件
在配置 Vertex AI 之前，请确保满足以下要求：
运行 Milvus 2.6 或更高版本
- 确认您的部署满足最低版本要求。
创建 Google 云服务帐户
- 至少，您可能需要 "Vertex AI 用户 "等角色或其他更具体的角色。有关详细信息，请参阅
创建服务帐户
。
下载服务帐户的 JSON 密钥文件
- 将此凭证文件安全地存储在服务器或本地计算机上。有关详情，请参阅
创建服务帐户密钥
。
配置凭据
在 Milvus 调用顶点人工智能之前，它需要访问你的 GCP 服务账户 JSON 密钥。我们支持两种方法，请根据您的部署和操作符选择其中一种。
选项
优先级
最适合
配置文件 (
milvus.yaml
)
高
全群集、持久设置
环境变量 (
MILVUSAI_GOOGLE_APPLICATION_CREDENTIALS
)
低
容器工作流程、快速测试
选项 1：配置文件（推荐且优先级更高）
Milvus 总是优先选择在
milvus.yaml
中声明的凭据，而不是同一提供商的任何环境变量。
对 JSON 密钥进行 Base64 编码
cat
credentials.json | jq . |
base64
在
milvus.yaml
# milvus.yaml
credential:
gcp_vertex:
# arbitrary label
credential_json:
|
      <YOUR_BASE64_ENCODED_JSON>
将证书绑定到顶点 AI 提供商
# milvus.yaml
function:
textEmbedding:
providers:
vertexai:
credential:
gcp_vertex
# must match the label above
url:
<optional:
custom
Vertex
AI
endpoint>
如果以后需要轮换密钥，只需更新
credential_json
下的 Base64 字符串，然后重启 Milvus--无需更改环境或容器。
选项 2：环境变量
如果喜欢在部署时注入秘密，请使用此方法。只有当
milvus.yaml
中不存在匹配的条目时，Milvus 才会使用环境变量。
配置步骤取决于 Milvus 的部署模式（独立集群与分布式集群）和协调平台（Docker Compose 与 Kubernetes）。
Docker Compose
Helm
要获取 Milvus 配置文件
（docker-compose.yaml
），请参阅
下载安装文件
。
将密钥挂载到容器中
编辑
docker-compose.yaml
文件，加入凭证卷映射：
services:
standalone:
volumes:
# Map host credential file to container path
-
/path/to/your/credentials.json:/milvus/configs/google_application_credentials.json:ro
在前面的配置中：
使用绝对路径进行可靠的文件访问 (
/home/user/credentials.json
而不是
~/credentials.json
)
容器路径必须以
.json
扩展名结尾
:ro
标志确保只读访问的安全性
设置环境变量
在同一
docker-compose.yaml
文件中，添加指向凭证路径的环境变量：
services:
standalone:
environment:
# Essential for Vertex AI authentication
MILVUSAI_GOOGLE_APPLICATION_CREDENTIALS:
/milvus/configs/google_application_credentials.json
应用更改
重启 Milvus 容器，激活配置：
docker-compose down && docker-compose up -d
要获取你的 Milvus 配置文件
（values.yaml
），请参阅
通过配置文件配置 Milvus
。
创建 Kubernetes 密钥
在控制机器（配置
kubectl
的地方）上执行此命令：
kubectl create secret generic vertex-ai-secret \
  --from-file=credentials.json=/path/to/your/credentials.json \
  -n <your-milvus-namespace>
在前面的命令中
vertex-ai-secret
:秘密名称（可定制）
/path/to/your/credentials.json
:GCP 证书文件的本地文件名
<your-milvus-namespace>
:托管 Milvus 的 Kubernetes 命名空间
配置 Helm 值
根据部署类型更新
values.yaml
：
独立部署
standalone:
extraEnv:
-
name:
MILVUSAI_GOOGLE_APPLICATION_CREDENTIALS
value:
/milvus/configs/credentials.json
# Container path
volumes:
-
name:
vertex-ai-credentials-vol
secret:
secretName:
vertex-ai-secret
# Must match Step 1
volumeMounts:
-
name:
vertex-ai-credentials-vol
mountPath:
/milvus/configs/credentials.json
# Must match extraEnv value
subPath:
credentials.json
# Must match secret key name
readOnly:
true
分布式部署（添加到每个组件）
proxy:
extraEnv:
-
name:
MILVUSAI_GOOGLE_APPLICATION_CREDENTIALS
value:
/milvus/configs/credentials.json
volumes:
-
name:
vertex-ai-credentials-vol
secret:
secretName:
vertex-ai-secret
volumeMounts:
-
name:
vertex-ai-credentials-vol
mountPath:
/milvus/configs/credentials.json
subPath:
credentials.json
readOnly:
true
# Repeat same configuration for dataNode, etc.
应用 Helm 配置
将更新的配置部署到群集：
helm upgrade milvus milvus/milvus -f values.yaml -n <your-milvus-namespace>
使用 Embeddings 功能
Vertex AI 配置完成后，请按照以下步骤定义和使用嵌入函数。
步骤 1：定义 Schema 字段
要使用嵌入功能，请创建一个具有特定 Schema 的 Collections。此 Schema 必须至少包含三个必要字段：
主字段，用于唯一标识 Collections 中的每个实体。
标量字段，用于存储要嵌入的原始数据。
一个向量字段，用于存储函数将为标量字段生成的向量嵌入。
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
# IMPORTANT: Set dim to match the output dimension of the model and parameters
schema.add_field(
"dense_vector"
, DataType.FLOAT_VECTOR, dim=
768
)
# Store embedding vectors (example dimension)
步骤 2：向 Schema 添加嵌入函数
Milvus 中的函数模块会自动将标量字段中存储的原始数据转换为嵌入数据，并将其存储到明确定义的向量字段中。
# 3. Define Vertex AI embedding function
text_embedding_function = Function(
    name=
"vert_func"
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
# Vertex AI specific parameters (function-level)
"provider"
:
"vertexai"
,
# Must be set to "vertexai"
"model_name"
:
"text-embedding-005"
,
# Required: Specifies the Vertex AI model to use
"projectid"
:
"your-gcp-project-id"
,
# Required: Your Google Cloud project ID
# Optional parameters (include these only if necessary):
# "location": "us-central1",            # Optional: Vertex AI service region (default us-central1)
# "task": "DOC_RETRIEVAL",              # Optional: Embedding task type (default DOC_RETRIEVAL)
# "dim": 768                            # Optional: Output vector dimension (1-768)
}
)
# Add the configured embedding function to your existing collection schema
schema.add_function(text_embedding_function)
参数
描述
是否需要？
示例值
provider
Embeddings 模型提供者。设为 "vertexai"。
是
"vertexai"
model_name
指定要使用的 Vertex AI 嵌入模型。
是
"text-embedding-005"
projectid
您的 Google 云项目 ID。
是
"your-gcp-project-id"
location
Vertex AI 服务的区域。目前，Vertex AI 嵌入主要支持 us-central1。默认为 us-central1。
不支持
"us-central1"
task
指定嵌入任务类型，影响嵌入结果。可接受的值：DOC_RETRIEVAL（默认）、CODE_RETRIEVAL（仅支持 005）、STS（语义文本相似性）。
不支持
"DOC_RETRIEVAL"
dim
输出嵌入向量的维度。接受 1 到 768 之间的整数。
注意：
如果指定，请确保 Schema 中向量字段的维数与此值相匹配。
无
768
下一步
配置完 Embeddings 功能后，请参阅功能
概述
，了解有关索引配置、数据插入示例和语义搜索操作的其他指导。