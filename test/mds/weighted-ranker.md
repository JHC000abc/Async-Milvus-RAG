加权排名器
加权排名器通过为每个搜索路径分配不同的重要性权重，智能地组合来自多个搜索路径的结果并确定其优先级。与技艺高超的厨师平衡多种配料以制作完美菜肴的方式类似，加权排名器也会平衡不同的搜索结果，以提供最相关的综合结果。这种方法非常适合在多个向量场或模式中进行搜索，其中某些场对最终排名的贡献应比其他场更大。
何时使用加权排名器
加权排名器是专门为混合搜索方案设计的，在这种方案中，您需要将来自多个 矢量搜索路径的结果进行组合。它对以下情况特别有效
使用案例
实例
为什么加权排名器效果好
电子商务搜索
结合图片相似度和文字描述的产品搜索
允许零售商优先考虑时尚产品的视觉相似性，同时强调技术产品的文字描述
媒体内容搜索
使用视觉特征和音频转录进行视频检索
根据查询意图平衡视觉内容和语音对话的重要性
文档检索
针对不同部分使用多种 Embeddings 的企业文档搜索
在考虑全文嵌入的同时，赋予标题和摘要嵌入更高的权重
如果您的混合搜索应用需要结合多种搜索路径，同时控制其相对重要性，那么加权排名器就是您的理想选择。
加权排序器的机制
加权排名策略的主要工作流程如下：
Collections 搜索得分
：收集向量搜索各路径的结果和分数（score_1、score_2）。
分数归一化
：每次搜索可能会使用不同的相似度指标，从而导致不同的分数分布。例如，使用 "内积"（IP）作为相似度类型可能会产生[-∞,+∞]的分数，而使用 "欧氏距离"（L2）则会产生[0,+∞]的分数。由于不同搜索的得分范围各不相同，无法直接比较，因此有必要对每条搜索路径的得分进行归一化处理。通常，
arctan
函数用于将分数转换为 [0, 1] 之间的范围（score_1_normalized, score_2_normalized）。分数越接近 1 表示相似度越高。
分配权重
：根据分配给不同向量场的重要性，为归一化分数（score_1_normalized，score_2_normalized）分配权重（
wi
）。每条路径的权重范围应在 [0,1] 之间。由此得出的加权分数为 score_1_weighted 和 score_2_weighted。
合并分数
：将加权分数（score_1_weighted、score_2_weighted）从高到低排序，得出最终分数集（score_final）。
加权排名器
加权排序器示例
本例演示了涉及图像和文本的多模态混合搜索（topK=5），并说明了加权 Ranker 策略如何对两次 ANN 搜索的结果进行重新排序。
图像的 ANN 搜索结果（topK=5）： ID
ID
得分（图像）
101
0.92
203
0.88
150
0.85
198
0.83
175
0.8
文本的 ANN 搜索结果（topK=5）： ID
ID
得分（文本）
198
0.91
101
0.87
110
0.85
175
0.82
250
0.78
使用 WeightedRanker 为图像和文本搜索结果分配权重。假设图像 ANN 搜索的权重为 0.6，文本搜索的权重为 0.4。
ID
得分（图像）
得分（文本）
加权得分
101
0.92
0.87
0.6×0.92+0.4×0.87=0.90
203
0.88
不适用
0.6×0.88+0.4×0=0.528
150
0.85
不适用
0.6×0.85+0.4×0=0.51
198
0.83
0.91
0.6×0.83+0.4×0.91=0.86
175
0.80
0.82
0.6×0.80+0.4×0.82=0.81
110
不在图像中
0.85
0.6×0+0.4×0.85=0.34
250
不在图像中
0.78
0.6×0+0.4×0.78=0.312
重新排序后的最终结果（topK=5）： 0.6×0+0.4×0.85=0.34
排名
ID
最终得分
1
101
0.90
2
198
0.86
3
175
0.81
4
203
0.528
5
150
0.51
加权排名器的使用
使用加权排名策略时，需要输入权重值。输入权重值的数量应与混合搜索中基本 ANN 搜索请求的数量一致。输入的权重值范围应为 [0,1]，数值越接近 1 表示重要性越高。
创建加权排序器
例如，假设混合搜索中有两个基本 ANN 搜索请求：文本搜索和图像搜索。如果认为文本搜索更重要，就应该赋予它更大的权重。
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

rerank = Function(
    name=
"weight"
,
    input_field_names=[],
# Must be an empty list
function_type=FunctionType.RERANK,
    params={
"reranker"
:
"weighted"
,
"weights"
: [
0.1
,
0.9
],
"norm_score"
:
True
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
"weight"
)
                .functionType(FunctionType.RERANK)
                .param(
"reranker"
,
"weighted"
)
                .param(
"weights"
,
"[0.1, 0.9]"
)
                .param(
"norm_score"
,
"true"
)
                .build();
import
{
FunctionType
}
from
'@zilliz/milvus2-sdk-node'
;
const
rerank = {
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
}
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
"weight"
input_field_names
是
要应用该函数的向量场列表（对于加权排序器必须为空）
[]
function_type
是
要调用的函数类型；使用
RERANK
指定重排策略
FunctionType.RERANK
params.reranker
是
指定要使用的排序方法。
必须设置为
weighted
才能使用加权排名器。
"weighted"
params.weights
是
每个搜索路径对应的权重数组；值∈ [0,1]。
有关详情，请参阅
加权排序器机制
。
[0.1, 0.9]
params.norm_score
是否
是否在加权前对原始分数进行归一化处理（使用 arctan）。
详情请参阅
加权排序器机制
。
True
应用于混合搜索
加权排名器是专门为结合多个向量场的混合搜索操作而设计的。执行混合搜索时，必须为每条搜索路径指定权重：
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
# Apply Weighted Ranker to product hybrid search
# Text search has 0.8 weight, image search has 0.3 weight
hybrid_results = milvus_client.hybrid_search(
    collection_name,
    [text_search, image_search],
# Multiple search requests
ranker=rerank,
# Apply the weighted ranker
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
rerank = {
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
limit
:
10
,
data
: [text_search, image_search],
rerank
: rerank,
  output_fields = [
"product_name"
,
"price"
,
"category"
],
});
// go
# restful
有关混合搜索的更多信息，请参阅
多向量混合搜索
。