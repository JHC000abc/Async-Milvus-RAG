TEI 排名器
Compatible with Milvus 2.6.x
TEI Ranker 利用 Hugging Face 提供的
文本嵌入推理（TEI）
服务，通过语义重排来提高搜索相关性。它代表了一种先进的搜索结果排序方法，超越了传统的向量相似性。
前提条件
在 Milvus 中实施 TEI Ranker 之前，请确保您拥有
具有
VARCHAR
字段的 Milvus Collections，其中包含要重新排序的文本
运行中的具有 Reranker 功能的 TEI 服务。有关设置 TEI 服务的详细说明，请参阅
TEI 官方文档
。
创建 TEI 排序器函数
要在你的 Milvus 应用程序中使用 TEI Ranker，请创建一个函数对象，指定重排应该如何操作。该函数将传递给 Milvus 搜索操作符，以增强结果排名。
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
# Configure TEI Ranker
tei_ranker = Function(
    name=
"tei_semantic_ranker"
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
"tei"
,
# Specifies TEI as the service provider
"queries"
: [
"renewable energy developments"
],
# Query text for relevance evaluation
"endpoint"
:
"http://localhost:8080"
,
# Your TEI service URL
"max_client_batch_size"
:
32
,
# Optional: batch size for processing (default: 32)
"truncate"
:
True
,
# Optional: Truncate the inputs that are longer than the maximum supported size
"truncation_direction"
:
"Right"
,
# Optional: Direction to truncate the inputs
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
        .inputFieldNames(Collections.singletonList(NAME_FIELD))
        .param(
"reranker"
,
"model"
)
        .param(
"provider"
,
"tei"
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
"truncate"
,
"true"
)
        .param(
"truncation_direction"
,
"Right"
)
        .build();
searchWithRanker(scientists, ranker);
// nodejs
// go
# restful
TEI 排序器专用参数
以下参数是 TEI 排序器的特定参数：
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
"tei"
queries
是
Rerankers 模型用于计算相关性得分的查询字符串列表。查询字符串的数量必须与搜索操作中的查询数量完全匹配（即使使用查询向量代替文本），否则将报错。
["搜索查询"]
endpoint
是
您的 TEI 服务 URL。
"http://localhost:8080"
max_client_batch_size
否
由于模型服务可能无法一次性处理所有数据，因此此处设置了在多个请求中访问模型服务的批量大小。
32
(默认值）
truncate
否
是否截断超过最大序列长度的输入。如果
False
，过长的输入会引发错误。
True
或
False
truncation_direction
否
当输入过长时截断的方向：
"Right"
(默认）：  从序列末尾删除标记，直到符合最大支持大小。
"Left"
:从序列的开头开始删除标记。
"Right"
或
"Left"
有关所有模型排序器共享的一般参数（如
provider
,
queries
），请参阅
创建模型排序器
。
应用于标准向量搜索
将 TEI Ranker 应用于标准向量搜索：
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
ranker=tei_ranker,
# Apply tei reranking
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