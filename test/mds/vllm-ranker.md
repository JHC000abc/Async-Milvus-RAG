vLLM 排序器
Compatible with Milvus 2.6.x
vLLM Ranker 利用
vLLM
推论框架，通过语义重新排序来提高搜索相关性。它代表了一种超越传统向量相似性的先进搜索结果排序方法。
vLLM Ranker 对于精确度和上下文至关重要的应用特别有价值，例如
需要深入理解概念的技术文档搜索
语义关系超过关键词匹配的研究数据库
需要将用户问题与相关解决方案相匹配的客户支持系统
必须了解产品属性和用户意图的电子商务搜索
前提条件
在 Milvus 中实施 vLLM Ranker 之前，请确保您拥有
具有
VARCHAR
字段的 Milvus Collections，其中包含要重新排名的文本
运行中的具有 Reranker 功能的 vLLM 服务。有关设置 vLLM 服务的详细说明，请参阅
官方 vLLM 文档
。验证 vLLM 服务的可用性：
# Replace YOUR_VLLM_ENDPOINT_URL with the actual URL (e.g., http://<service-ip>:<port>/v1/rerank)
# Replace 'BAAI/bge-reranker-base' if you deployed a different model
curl -X
'POST'
\
'YOUR_VLLM_ENDPOINT_URL'
\
  -H
'accept: application/json'
\
  -H
'Content-Type: application/json'
\
  -d
'{
  "model": "BAAI/bge-reranker-base",
  "query": "What is the capital of France?",
  "documents": [
    "The capital of Brazil is Brasilia.",
    "The capital of France is Paris.",
    "Horses and cows are both animals"
  ]
}'
成功的响应应返回按相关性得分排序的文档，类似于 OpenAI rerankers API 响应。
有关更多服务器参数和选项，请参阅
vLLM OpenAI Compatible Server 文档
。
创建 vLLM Ranker 函数
要在你的 Milvus 应用程序中使用 vLLM Ranker，请创建一个 Function 对象，指定 Reranking 的操作符。该函数将传递给 Milvus 搜索操作符，以增强结果排名。
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
# Create a vLLM Ranker function
vllm_ranker = Function(
    name=
"vllm_semantic_ranker"
,
# Choose a descriptive name
input_field_names=[
"document"
],
# Field containing text to rerank
function_type=FunctionType.RERANK,
# Must be RERANK
params={
"reranker"
:
"model"
,
# Specifies model-based reranking
"provider"
:
"vllm"
,
# Specifies vLLM service
"queries"
: [
"renewable energy developments"
],
# Query text
"endpoint"
:
"http://localhost:8080"
,
# vLLM service address
"max_client_batch_size"
:
32
,
# Optional: batch size
"truncate_prompt_tokens"
:
256
,
# Optional: Use last 256 tokens
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
"vllm_semantic_ranker"
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
"vllm"
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
"truncate_prompt_tokens"
,
"256"
)
                       .build();
// nodejs
// go
# restful
vLLM 排序器专用参数
以下参数是 vLLM 排序器的特定参数：
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
"vllm"
queries
是
Rerankers 模型用于计算相关性得分的查询字符串列表。查询字符串的数量必须与搜索操作中的查询数量完全匹配（即使使用查询向量代替文本），否则将报错。
["搜索查询"]
endpoint
是
您的 vLLM 服务地址。
"http://localhost:8080"
max_client_batch_size
否
由于模型服务可能无法一次性处理所有数据，因此此处设置了在多个请求中访问模型服务的批量大小。
32
(默认值）
truncate_prompt_tokens
无
如果设置为整数
k
，将只使用提示符中的最后
k 个
标记（即左截断）。默认为无（即不截断）。
256
关于所有模型排序器共享的一般参数（如
provider
,
queries
），请参阅
创建模型排序器
。
应用于标准向量搜索
将 vLLM Ranker 应用于标准向量搜索：
Python
Java
NodeJS
Go
cURL
# Execute search with vLLM reranking
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
ranker=vllm_ranker,
# Apply vLLM reranking
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