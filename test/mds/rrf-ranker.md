RRF 排序器
互惠排名融合（RRF）排名器是 Milvus 混合搜索的一种重新排名策略，它根据多个向量搜索路径的排名位置而不是原始相似度得分来平衡搜索结果。就像体育比赛考虑的是球员的排名而不是个人统计数据一样，RRF Ranker 根据每个项目在不同搜索路径中的排名高低来组合搜索结果，从而创建一个公平、均衡的最终排名。
何时使用 RRF Ranker
RRF Ranker 专门设计用于混合搜索场景，在这种场景中，您需要平衡来自多个向量搜索路径的结果，而无需分配明确的重要性权重。它对以下情况特别有效：
使用案例
示例
为什么 RRF Ranker 运行良好
具有同等重要性的多模式搜索
两种模式同等重要的图像-文本搜索
无需任意分配权重即可平衡结果
集合向量搜索
综合不同 Embeddings 模型的结果
民主合并排名，不偏向任何特定模型的得分分布
跨语言搜索
跨多种语言查找文件
不考虑特定语言的 Embeddings 特征，对结果进行公平排名
专家建议
综合多个专家系统的建议
在不同系统使用无法比拟的评分方法时创建一致的排名
如果您的混合搜索应用程序需要在不分配明确权重的情况下以民主方式平衡多个搜索路径，那么 RRF Ranker 就是您的理想选择。
RRF Ranker 的机制
RRFRanker 策略的主要工作流程如下：
收集搜索排名
：收集向量搜索各路径的结果排名（rank_1、rank_2）。
合并排名
：根据公式转换各路径的排名（rank_rrf_1，rank_rrf_2）。
计算公式中的
N
代表检索次数，
ranki
(d
)
是
第 i 个
检索器生成的文档
d
的排名位置，
k
是平滑参数，通常设置为 60。
汇总排名
：根据综合排名对搜索结果重新排序，得出最终结果。
RRF 排序器
RRF 排序器示例
本例演示了稀疏密集向量上的混合搜索（topK=5），并说明了 RRFRanker 策略如何对两次 ANN 搜索的结果进行重新排序。
文本稀疏向量上的 ANN 搜索结果（topK=5）： ID
ID
排名（稀疏）
101
1
203
2
150
3
198
4
175
5
对文本密集向量进行 ANN 搜索的结果（topK=5）： ID
ID
排名（密集）
198
1
101
2
110
3
175
4
250
5
使用 RRF 重新排列两组搜索结果的排名。假设平滑参数
k
设置为 60。
ID
得分（稀疏）
得分（密集）
最终得分
101
1
2
1/(60+1)+1/(60+2) = 0.03252247
198
4
1
1/(60+4)+1/(60+1) = 0.03201844
175
5
4
1/(60+5)+1/(60+4) = 0.03100962
203
2
不适用
1/(60+2) = 0.01612903
150
3
不适用
1/(60+3) = 0.01587302
110
不适用
3
1/(60+3) = 0.01587302
250
不适用
5
1/(60+5) = 0.01538462
重排后的最终结果（topK=5):.............
排名
ID
最终得分
1
101
0.03252247
2
198
0.03201844
3
175
0.03100962
4
203
0.01612903
5
150
0.01587302
5
110
0.01587302
RRF 排序器的使用
使用 RRF 重排策略时，需要配置参数
k
。这是一个平滑参数，可以有效改变全文搜索与向量搜索的相对权重。该参数的默认值为 60，可在 (0, 16384) 的范围内调整。该值应为浮点数。推荐值在 [10, 100] 之间。虽然
k=60
是常见的选择，但
k
的最佳值可能因具体应用和数据集而异。我们建议根据具体使用情况测试和调整该参数，以实现最佳性能。
创建 RRF 排序器
用多个向量场设置好 Collections 后，使用适当的平滑参数创建 RRF 排序器：
Milvus 2.6.x 及更高版本可让您直接通过
Function
API 配置 Reranker 策略。如果您使用的是早期版本（v2.6.0 之前），请参考
Rerankers
文档中的设置说明。
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
Function, FunctionType

ranker = Function(
    name=
"rrf"
,
    input_field_names=[],
# Must be an empty list
function_type=FunctionType.RERANK,
    params={
"reranker"
:
"rrf"
,
"k"
:
100
# Optional
}
)
import
io.milvus.common.clientenum.FunctionType;
import
io.milvus.v2.service.collection.request.CreateCollectionReq;

CreateCollectionReq.
Function
rerank
=
CreateCollectionReq.Function.builder()
        .name(
"rrf"
)
        .functionType(FunctionType.RERANK)
        .param(
"reranker"
,
"rrf"
)
        .param(
"k"
,
"100"
)
        .build();
import
{
FunctionType
}
from
"@zilliz/milvus2-sdk-node"
;
const
ranker = {
name
:
"weight"
,
input_field_names
: [],
function_type
:
FunctionType
.
RERANK
,
params
: {
reranker
:
"weighted"
,
weights
: [
0.1
,
0.9
],
norm_score
:
true
,
  },
};
// Go
# Restful
参数
是否需要？
说明
值/示例
name
是
此功能的唯一标识符
"rrf"
input_field_names
是
要应用该函数的向量字段列表（对于 RRF Ranker 必须为空）
[]
function_type
是
要调用的函数类型；使用
RERANK
指定 Rerankers 排序策略
FunctionType.RERANK
params.reranker
是
指定要使用的排序方法。
必须设置为
rrf
才能使用 RRF Ranker。
"weighted"
params.k
无
平滑参数，用于控制文档排名的影响；
k
越高，对排名靠前的敏感度越低。范围：（0，16384）；默认值：
60
。
有关详情，请参阅
RRF Ranker 的机制
。
100
应用于混合搜索
RRF Ranker 专为结合多个向量场的混合搜索操作而设计。下面介绍如何在混合搜索中使用它：
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
MilvusClient, AnnSearchRequest
# Connect to Milvus server
milvus_client = MilvusClient(uri=
"http://localhost:19530"
)
# Assume you have a collection setup
# Define text vector search request
text_search = AnnSearchRequest(
    data=[
"modern dining table"
],
    anns_field=
"text_vector"
,
    param={},
    limit=
10
)
# Define image vector search request
image_search = AnnSearchRequest(
    data=[image_embedding],
# Image embedding vector
anns_field=
"image_vector"
,
    param={},
    limit=
10
)
# Apply RRF Ranker to product hybrid search
# The smoothing parameter k controls the balance
hybrid_results = milvus_client.hybrid_search(
    collection_name,
    [text_search, image_search],
# Multiple search requests
ranker=ranker,
# Apply the RRF ranker
limit=
10
,
    output_fields=[
"product_name"
,
"price"
,
"category"
]
)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.service.vector.request.AnnSearchReq;
import
io.milvus.v2.service.vector.request.HybridSearchReq;
import
io.milvus.v2.service.vector.response.SearchResp;
import
io.milvus.v2.service.vector.request.data.EmbeddedText;
import
io.milvus.v2.service.vector.request.data.FloatVec;
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
        
List<AnnSearchReq> searchRequests =
new
ArrayList
<>();
searchRequests.add(AnnSearchReq.builder()
        .vectorFieldName(
"text_vector"
)
        .vectors(Collections.singletonList(
new
EmbeddedText
(
"\"modern dining table\""
)))
        .limit(
10
)
        .build());
searchRequests.add(AnnSearchReq.builder()
        .vectorFieldName(
"image_vector"
)
        .vectors(Collections.singletonList(
new
FloatVec
(imageEmbedding)))
        .limit(
10
)
        .build());
HybridSearchReq
hybridSearchReq
=
HybridSearchReq.builder()
                .collectionName(COLLECTION_NAME)
                .searchRequests(searchRequests)
                .ranker(ranker)
                .limit(
10
)
                .outputFields(Arrays.asList(
"product_name"
,
"price"
,
"category"
))
                .build();
SearchResp
searchResp
=
client.hybridSearch(hybridSearchReq);
import
{
MilvusClient
,
FunctionType
}
from
"@zilliz/milvus2-sdk-node"
;
const
milvusClient =
new
MilvusClient
({
address
:
"http://localhost:19530"
});
const
text_search = {
data
: [
"modern dining table"
],
anns_field
:
"text_vector"
,
param
: {},
limit
:
10
,
};
const
image_search = {
data
: [image_embedding],
anns_field
:
"image_vector"
,
param
: {},
limit
:
10
,
};
const
ranker = {
name
:
"weight"
,
input_field_names
: [],
function_type
:
FunctionType
.
RERANK
,
params
: {
reranker
:
"weighted"
,
weights
: [
0.1
,
0.9
],
norm_score
:
true
,
  },
};
const
search =
await
milvusClient.
search
({
collection_name
: collection_name,
data
: [text_search, image_search],
output_fields
: [
"product_name"
,
"price"
,
"category"
],
limit
:
10
,
rerank
: ranker,
});
// go
# restful
有关混合搜索的更多信息，请参阅
多向量混合搜索
。