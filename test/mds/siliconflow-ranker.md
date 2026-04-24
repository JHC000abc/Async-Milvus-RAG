SiliconFlow 排名器
Compatible with Milvus 2.6.x
SiliconFlow Ranker 利用
SiliconFlow 的
综合 Reranking 模型，通过语义 Reranking 增强搜索相关性。它提供灵活的文档分块功能，并支持来自不同提供商的各种专业重排模型。
SiliconFlow Ranker 对于需要以下功能的应用特别有价值：
先进的文档分块功能，可配置重叠部分以处理长文档
可访问各种重排模型，包括 BAAI/bge-reranker 系列和其他专业模型
灵活的基于分块的评分，其中得分最高的分块代表文档得分
具有成本效益的 Reranker，支持标准和专业模型变体
前提条件
在 Milvus 中实施 SiliconFlow Ranker 之前，请确保您拥有
具有
VARCHAR
字段的 Milvus Collections，其中包含要重新排名的文本
可访问 Rerankers 模型的有效 SiliconFlow API 密钥。在
SiliconFlow 平台
上注册，以获取 API 凭据。您可以
设置
SILICONFLOW_API_KEY
环境变量，或
在排名器配置中直接指定 API 密钥
创建 SiliconFlow 排名器函数
要在您的 Milvus 应用程序中使用 SiliconFlow Ranker，请创建一个 Function 对象，指定 Reranking 应如何操作。该函数将传递给 Milvus 搜索操作，以增强结果排名。
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
# Configure SiliconFlow Ranker
siliconflow_ranker = Function(
    name=
"siliconflow_semantic_ranker"
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
"siliconflow"
,
# Specifies SiliconFlow as the service provider
"model_name"
:
"BAAI/bge-reranker-v2-m3"
,
# SiliconFlow reranking model to use
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
"max_chunks_per_doc"
:
5
,
# Optional: max chunks per document for supported models
"overlap_tokens"
:
50
,
# Optional: token overlap between chunks for supported models
# "credential": "your-siliconflow-api-key" # Optional: if not set, uses SILICONFLOW_API_KEY env var
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
"siliconflow_semantic_ranker"
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
"siliconflow"
)
                       .param(
"model_name"
,
"BAAI/bge-reranker-v2-m3"
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
"32"
)
                       .param(
"max_chunks_per_doc"
,
"5"
)
                       .param(
"overlap_tokens"
,
"50"
)
                       .build();
// nodejs
// go
# restful
SiliconFlow 排序器特定参数
以下参数是 SiliconFlow 排序器的特定参数：
参数
是否需要？
描述
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
"siliconflow"
model_name
是
要从 SiliconFlow 平台支持的模型中使用的 SiliconFlow 重排模型。
有关可用 Rerankers 模型的列表，请参阅
SiliconFlow 文档
。
"BAAI/bge-reranker-v2-m3"
queries
是
Rerankers 模型用于计算相关性得分的查询字符串列表。查询字符串的数量必须与搜索操作中的查询数量完全匹配（即使使用查询向量代替文本），否则将报错。
["搜索查询"]
max_client_batch_size
否
由于模型服务可能无法一次性处理所有数据，因此此项设置了在多个请求中访问模型服务的批量大小。
128
(默认值）
max_chunks_per_doc
无
从文档中生成的最大块数。长文档会被分成多个分块进行计算，分块中的最高分将作为文档的得分。仅特定模型支持：
BAAI/bge-reranker-v2-m3
,
Pro/BAAI/bge-reranker-v2-m3
, 和
netease-youdao/bce-reranker-base_v1
。
5
,
10
overlap_tokens
无
文档分块时，相邻分块之间的标记重叠数。这可确保各分块边界之间的连续性，以便更好地理解语义。仅受特定模型支持：
BAAI/bge-reranker-v2-m3
,
Pro/BAAI/bge-reranker-v2-m3
, 和
netease-youdao/bce-reranker-base_v1
。
50
credential
不支持
访问 SiliconFlow API 服务的身份验证凭证。如果未指定，系统将查找
SILICONFLOW_API_KEY
环境变量。
"your-siliconflow-api-key
特定于模型的功能支持
：
max_chunks_per_doc
和
overlap_tokens
参数仅受特定模型支持。使用其他模型时，这些参数将被忽略。
有关所有模型排序器共享的一般参数（如
provider
,
queries
），请参阅
创建模型排序器
。
应用于标准向量搜索
将 SiliconFlow Ranker 应用于标准向量搜索：
Python
Java
NodeJS
Go
cURL
# Execute search with SiliconFlow reranking
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
ranker=siliconflow_ranker,
# Apply SiliconFlow reranking
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
        .collectionName(
"your_collection"
)
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