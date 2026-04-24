搜索排名器
Compatible with Milvus 2.6.x
Cohere Ranker 利用
Cohere
强大的 Rerankers 模型，通过语义 Reranking 增强搜索相关性。它通过强大的 API 基础设施和优化的性能为生产环境提供企业级的 Reranker 功能。
Cohere Ranker 对于需要以下功能的应用特别有价值：
通过最先进的 Reranker 模型实现高质量的语义理解
针对生产工作负载的企业级可靠性和可扩展性
跨不同内容类型的多语言 Reranker 能力
具有内置速率限制和错误处理功能的一致 API 性能
前提条件
在 Milvus 中实施 Cohere Ranker 之前，请确保您拥有
具有
VARCHAR
字段的 Milvus Collections，其中包含要重新排名的文本
可访问 Rerankers 模型的有效 Cohere API 密钥。在
Cohere 平台
上注册，以获取 API 证书。您可以
设置
COHERE_API_KEY
环境变量，或
在
排名器配置
的
credential
中直接指定 API 密钥
创建 Cohere 排名器函数
要在您的 Milvus 应用程序中使用 Cohere Ranker，请创建一个 Function 对象，指定 Reranker 应如何操作。该函数将传递给 Milvus 搜索操作符，以增强结果排名。
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
MilvusClient, Function, FunctionType
# Connect to your Milvus server
client = MilvusClient(
    uri=
"http://localhost:19530"
# Replace with your Milvus server URI
)
# Configure Cohere Ranker
cohere_ranker = Function(
    name=
"cohere_semantic_ranker"
,
# Unique identifier for your ranker
input_field_names=[
"document"
],
# VARCHAR field containing text to rerank
function_type=FunctionType.RERANK,
# Must be RERANK for reranking functions
params={
"reranker"
:
"model"
,
# Enables model-based reranking
"provider"
:
"cohere"
,
# Specifies Cohere as the service provider
"model_name"
:
"rerank-english-v3.0"
,
# Cohere rerank model to use
"queries"
: [
"renewable energy developments"
],
# Query text for relevance evaluation
"max_client_batch_size"
:
128
,
# Optional: batch size for model service requests (default: 128)
"max_tokens_per_doc"
:
4096
,
# Optional: max tokens per document (default: 4096)
# "credential": "your-cohere-api-key" # Optional: authentication credential for Cohere API
}
)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.common.clientenum.FunctionType;
import
io.milvus.v2.service.collection.request.CreateCollectionReq;
MilvusClientV2
client
=
new
MilvusClientV2
(ConnectConfig.builder()
        .uri(
"http://localhost:19530"
)
        .build());

CreateCollectionReq.
Function
ranker
=
CreateCollectionReq.Function.builder()
                       .functionType(FunctionType.RERANK)
                       .name(
"cohere_semantic_ranker"
)
                       .inputFieldNames(Collections.singletonList(
"document"
))
                       .param(
"reranker"
,
"model"
)
                       .param(
"provider"
,
"cohere"
)
                       .param(
"model_name"
,
"rerank-english-v3.0"
)
                       .param(
"queries"
,
"[\"renewable energy developments\"]"
)
                       .param(
"endpoint"
,
"http://localhost:8080"
)
                       .param(
"max_client_batch_size"
,
"128"
)
                       .param(
"max_tokens_per_doc"
,
"4096"
)
                       .build();
// nodejs
// go
# restful
Cohere 排序器专用参数
以下参数是 Cohere 排序器的特定参数：
参数
是否需要？
说明
值/示例
reranker
是
必须设置为
"model"
才能启用模型重排。
"model"
provider
是
用于重排的模型服务提供商。
"cohere"
model_name
是
从 Cohere 平台支持的模型中选择要使用的 Cohere Rerankers 模型。
有关可用 Rerankers 模型的列表，请参阅
Cohere 文档
。
"rerank-english-v3.0"
,
"rerank-multilingual-v3.0"
queries
是
Rerankers 模型用于计算相关性得分的查询字符串列表。查询字符串的数量必须与搜索操作中的查询数量完全一致（即使使用查询向量代替文本），否则将报错。
["搜索查询"]
max_client_batch_size
否
由于模型服务可能无法一次性处理所有数据，因此此项设置了在多个请求中访问模型服务的批量大小。
128
(默认值）
max_tokens_per_doc
无
每个文档的最大标记数。长文档将自动截断为指定的标记数。
4096
（默认值）
credential
无
访问 Cohere API 服务的身份验证凭据。如果未指定，系统将查找
COHERE_API_KEY
环境变量。
"your-cohere-api-key
有关所有模型排序器共享的一般参数（如
provider
,
queries
），请参阅
创建模型排序器
。
应用于标准向量搜索
将 Cohere Ranker 应用于标准向量搜索：
Python
Java
NodeJS
Go
cURL
# Execute search with Cohere reranking
results = client.search(
    collection_name=
"your_collection"
,
    data=[your_query_vector],
# Replace with your query vector
anns_field=
"dense_vector"
,
# Vector field to search
limit=
5
,
# Number of results to return
output_fields=[
"document"
],
# Include text field for reranking
ranker=cohere_ranker,
# Apply Cohere reranking
consistency_level=
"Bounded"
)
import
io.milvus.v2.common.ConsistencyLevel;
import
io.milvus.v2.service.vector.request.SearchReq;
import
io.milvus.v2.service.vector.response.SearchResp;
import
io.milvus.v2.service.vector.request.data.EmbeddedText;
SearchReq
searchReq
=
SearchReq.builder()
        .collectionName(COLLECTION_NAME)
        .data(Arrays.asList(
new
EmbeddedText
(
"AI Research Progress"
),
new
EmbeddedText
(
"What is AI"
)))
        .annsField(
"vector_field"
)
        .limit(
10
)
        .outputFields(Collections.singletonList(
"document"
))
        .functionScore(FunctionScore.builder()
                .addFunction(ranker)
                .build())
        .consistencyLevel(ConsistencyLevel.BOUNDED)
        .build();
SearchResp
searchResp
=
client.search(searchReq);
// nodejs
// go
# restful