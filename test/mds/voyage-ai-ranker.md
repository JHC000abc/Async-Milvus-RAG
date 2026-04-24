Voyage 人工智能排名器
Compatible with Milvus 2.6.x
Voyage AI Ranker 利用
Voyage AI 的
专业 Rerankers，通过语义重排提高搜索相关性。它提供高性能的重排功能，针对检索增强生成（RAG）和搜索应用进行了优化。
Voyage AI Ranker 对于需要以下功能的应用特别有价值：
通过专门为 Reranker 任务训练的模型进行高级语义理解
高性能处理，针对生产工作负载进行优化推理
灵活的截断控制，可处理不同长度的文档
在不同的模型变体（Rerank-2、Rerank-lite 等）中对性能进行微调
前提条件
在 Milvus 中实施 Voyage AI Ranker 之前，请确保您已具备以下条件：
具有
VARCHAR
字段的 Milvus Collections，其中包含要进行 Reranker 的文本
可访问 Rerankers 的有效 Voyage AI API 密钥。在
Voyage AI 平台
上注册，获取 API 证书。您可以
设置
VOYAGE_API_KEY
环境变量，或
在排名器配置中直接指定 API 密钥
创建Voyage AI排名器函数
要在您的 Milvus 应用程序中使用 Voyage AI Ranker，请创建一个函数对象，指定 Reranking 应如何操作。该函数将传递给 Milvus 搜索操作，以增强结果排名。
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
# Configure Voyage AI Ranker
voyageai_ranker = Function(
    name=
"voyageai_semantic_ranker"
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
"voyageai"
,
# Specifies Voyage AI as the service provider
"model_name"
:
"rerank-2.5"
,
# Voyage AI reranker to use
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
"truncation"
:
True
,
# Optional: enable input truncation (default: True)
# "credential": "your-voyage-api-key" # Optional: if not set, uses VOYAGE_API_KEY env var
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
"voyageai_semantic_ranker"
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
"voyageai"
)
                       .param(
"model_name"
,
"rerank-2.5"
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
"truncation"
,
"true"
)
                       .build();
// nodejs
// go
# restful
Voyage AI 排序器专用参数
以下参数是 Voyage AI 排序器的特定参数：
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
"voyageai"
model_name
是
Voyage AI 平台支持的模型中要使用的 Voyage AI Reranker。
有关可用 Reranker 的列表，请参阅
Voyage AI
文档
。
"rerank-2.5"
queries
是
Reranker 模型用于计算相关性得分的查询字符串列表。查询字符串的数量必须与搜索操作中的查询数量完全匹配（即使使用查询向量代替文本），否则会报错。
["搜索查询"]
max_client_batch_size
否
由于模型服务可能无法一次性处理所有数据，因此此项设置了在多个请求中访问模型服务的批量大小。
128
(默认值）
truncation
无
是否截断输入以满足查询和文档的 "上下文长度限制"。
如果
True
，查询和文档将被截断以符合上下文长度限制，然后再由 Reranker 模型处理。
如果是
False
，当查询超过 8,000 个词组（
rerank-2.5
和
rerank-2.5-lite
）；超过 4,000 个词组（
rerank-2
）；超过 2,000 个词组（
rerank-2-lite
和
rerank-1
）；以及超过 1,000 个词组（
rerank-lite-1
），或者查询中的词组数与任何单个文档中的词组数之和超过 16,000 个词组（
rerank-2
）；超过 8,000 个词组（
rerank-2-lite
和
rerank-1
）；以及超过 4,000 个词组（
rerank-lite-1
）时，将引发错误。
True
(默认）或
False
credential
无
访问 Voyage AI API 服务的身份验证凭据。如果未指定，系统将查找
VOYAGE_API_KEY
环境变量。
"您的 Voyage-api-key"
关于所有模型排序器共享的一般参数（如
provider
,
queries
），请参阅
创建模型排序器
。
应用于标准向量搜索
将 Voyage AI Ranker 应用于标准向量搜索：
Python
Java
NodeJS
Go
cURL
# Execute search with Voyage AI reranker
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
ranker=voyageai_ranker,
# Apply Voyage AI reranker
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