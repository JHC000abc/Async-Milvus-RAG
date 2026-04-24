模型排名器概述
Compatible with Milvus 2.6.x
传统的向量搜索纯粹通过数学相似度--向量在高维空间中的匹配程度--对结果进行排序。这种方法虽然高效，但往往会忽略真正的语义相关性。考虑搜索
"数据库优化的最佳实践"：
您可能会收到具有高向量相似性的文档，这些文档经常提到这些术语，但实际上并没有提供可操作的优化策略。
模型排名器通过集成高级语言模型来理解查询和文档之间的语义关系，从而改变了 Milvus 搜索。它不完全依赖向量相似性，而是对内容含义和上下文进行评估，从而提供更智能、更相关的结果。
限制
模型排名器不能用于分组搜索。
用于模型重排的字段必须是文本类型 (
VARCHAR
)。
每个模型排名器一次只能使用一个
VARCHAR
字段进行评估。
工作原理
模型排序器通过一个定义明确的工作流程，将语言模型理解能力整合到 Milvus 搜索流程中：
模型排序器概述
初始查询
：您的应用程序向 Milvus 发送查询
向量搜索
：Milvus 执行标准向量搜索以识别候选文档
候选检索
：系统根据向量相似性识别初始候选文档集
模型评估
：模型排序器功能处理查询-文档对：
将原始查询和候选文档发送至外部模型服务
语言模型评估查询和每个文档之间的语义相关性
根据语义理解为每个文档打分
智能 Rerankers
：根据模型生成的相关性得分对文档重新排序
增强结果
：您的应用程序将收到根据语义相关性而不仅仅是向量相似性排序的结果
根据您的需求选择模型提供商
Milvus 支持以下模型服务提供商进行重新排序，每个服务提供商都具有不同的特点：
提供商
最适合
特点
使用案例示例
vLLM
需要深入语义理解和定制的复杂应用
支持各种大型语言模型
灵活的部署选项
更高的计算要求
更大的定制潜力
部署特定领域模型的法律研究平台，可理解法律术语和判例法关系
TEI
快速实施，有效利用资源
针对文本操作优化的轻量级服务
部署更简单，资源需求更低
预先优化的 Rerankers 模型
基础设施开销最小
内容管理系统需要具有标准要求的高效 Rerankers 功能
一致性
优先考虑可靠性和易集成性的企业应用程序
企业级可靠性和可扩展性
托管服务，无需维护基础设施
多语言 Rerankers 功能
内置速率限制和错误处理功能
需要高可用性搜索、一致的 API 性能和多语言产品目录的电子商务平台
Voyage AI
具有特定性能和上下文要求的 RAG 应用程序
专为 Rerankers 任务训练的模型
针对不同文档长度的精细截断控制
针对生产工作负载进行优化推理
多种模型变体（Rerank-2、Rerank-lite 等）
具有不同文档长度的研究数据库，需要微调性能控制和专门的语义理解
SiliconFlow
具有成本效益优先级的长文档处理应用
可配置重叠的高级文档分块
基于分块的评分（得分最高的分块代表文档）
支持多种 Rerankers 模型
通过标准和专业模型变体实现成本效益
技术文档搜索系统处理需要智能分割和重叠控制的冗长手册和论文
有关各模型服务实施的详细信息，请参阅专用文档：
vLLM 排序器
TEI 排序器
Cohere 排序器
Voyage AI 排序器
SiliconFlow Ranker
实施
在实施模型排名器之前，请确保您拥有
具有
VARCHAR
字段的 Milvus Collections，其中包含要重新排名的文本
可访问 Milvus 实例的正在运行的外部模型服务
Milvus 与所选模型服务之间有适当的网络连接
模型排序器可与标准向量搜索和混合搜索操作无缝集成。实现方法包括创建一个定义 Reranker 配置的 Function 对象，并将其传递给搜索操作。
创建模型排序器
要实现模型 Rerankers，首先要定义一个具有相应配置的 Function 对象。在本例中，我们使用 TEI 作为服务提供商：
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
# Create a model ranker function
model_ranker = Function(
    name=
"semantic_ranker"
,
# Function identifier
input_field_names=[
"document"
],
# VARCHAR field to use for reranking
function_type=FunctionType.RERANK,
# Must be set to RERANK
params={
"reranker"
:
"model"
,
# Specify model reranker. Must be "model"
"provider"
:
"tei"
,
# Choose provider: "tei", "vllm", etc.
"queries"
: [
"machine learning for time series"
],
# Query text
"endpoint"
:
"http://model-service:8080"
,
# Model service endpoint
# "maxBatch": 32  # Optional: batch size for processing
}
)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.service.vector.request.ranker.ModelRanker;
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
ModelRanker
ranker
=
ModelRanker.builder()
        .name(
"semantic_ranker"
)
        .inputFieldNames(Collections.singletonList(
"document"
))
        .provider(
"tei"
)
        .queries(Collections.singletonList(
"machine learning for time series"
))
        .endpoint(
"http://model-service:8080"
)
        .build();
// nodejs
// go
# restful
参数
是否需要？
说明
值/示例
name
是
执行搜索时使用的功能标识符。
"semantic_ranker"
input_field_names
是
用于 Rerankers 的文本字段名称。
必须是
VARCHAR
类型的字段。
["document"]
function_type
是
指定创建的函数类型。
所有模型排名器必须设置为
RERANK
。
FunctionType.RERANK
params
是
包含基于模型的 Rerankers 功能配置的字典。可用参数（键）因服务提供商而异。
{...}
params.reranker
是
必须设置为
"model"
才能启用模型重排。
"model"
params.provider
是
用于重新排序的模型服务提供商。
"tei"
params.queries
是
Rerankers 模型用于计算相关性得分的查询字符串列表。
查询字符串的数量必须与搜索操作中的查询数量完全匹配（即使使用查询向量代替文本），否则将报错。
["search query"]
params.endpoint
是
模型服务的 URL。
"http://localhost:8080"
max_client_batch_size
否
单个批次中要处理的最大文档数。数值越大，吞吐量越大，但需要的内存也越多。
32
(默认值）
应用于标准向量搜索
定义模型排序器后，您可以通过将其传递给排序器参数，在搜索操作过程中应用该排序器：
Python
Java
NodeJS
Go
cURL
# Use the model ranker in standard vector search
results = client.search(
    collection_name,
    data=[your_query_vector],
# Number of query vectors must match that specified in model_ranker.params["queries"]
anns_field=
"vector_field"
,
    limit=
10
,
    output_fields=[
"document"
],
# Include the text field in outputs
ranker=model_ranker,
# Apply the model ranker here
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
        .data(Collections.singletonList(
new
EmbeddedText
(
"machine learning for time series"
)))
        .annsField(
"vector_field"
)
        .limit(
10
)
        .outputFields(Collections.singletonList(document))
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