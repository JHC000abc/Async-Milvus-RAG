衰减排名器概述
Compatible with Milvus 2.6.x
在传统的向量搜索中，搜索结果的排名完全取决于向量的相似性--向量在数学空间中的匹配程度。但在实际应用中，真正相关的内容往往不仅仅取决于语义相似性。
考虑一下这些日常场景：
在新闻搜索中，昨天的文章应该比三年前的类似文章排名靠前
餐厅搜索器，优先考虑 5 分钟车程内的餐厅，而不是需要 30 分钟车程的餐厅
一个电子商务平台，即使流行产品与搜索查询的相似度稍低，也能提升它们的排名
这些场景都有一个共同的需求：平衡向量相似性与时间、距离或流行度等其他数字因素。
Milvus 的衰减排名器根据数值字段值调整搜索排名，从而满足了这一需求。它们可让您平衡向量相似性与数据的 "新鲜度"、"接近度 "或其他数值属性，从而创建更直观、与上下文更相关的搜索体验。
使用注意事项
衰减排名不能与分组搜索一起使用。
用于衰减排名的字段必须是数字（
INT8
,
INT16
,
INT32
,
INT64
,
FLOAT
或
DOUBLE
）。
每个衰减排序器只能使用一个数字字段。
时间单位一致性
：使用基于时间的衰减排名时，
origin
、
scale
和
offset
参数的单位必须与您的 Collections 数据中使用的单位一致：
如果您的 Collections 以
秒
为单位存储时间戳，则所有参数都使用秒为单位
如果您的 Collections 以
毫秒
为单位存储时间戳，则所有参数均使用毫秒。
如果您的 Collections 以
微秒
为单位存储时间戳，则所有参数都使用微秒
工作原理
衰减排序将时间或地理距离等数字因素纳入排序过程，从而增强了传统的向量搜索。整个过程分为以下几个阶段
阶段 1：计算归一化的相似性得分
首先，Milvus 计算并归一化向量相似性得分，以确保比较的一致性：
对于
L2
和
JACCARD
距离指标（数值越小，表示相似度越高）：
normalized_score = 1.0 - (2 × arctan(score))/π
这将距离转化为 0-1 之间的相似性分数，越高越好。
对于
IP
、
COSINE
和
BM25
指标（分数越高表示匹配度越高）：直接使用分数，无需进行归一化处理。
第二阶段：计算衰减分数
接下来，Milvus 根据数值字段值（如时间戳或距离），使用您选择的衰减排名器计算衰减分数：
每个衰减排名器将原始数值转化为 0-1 之间的归一化相关性分数。
衰减分数表示一个项目与理想点的 "距离 "相关程度
具体计算公式因衰减排名器类型而异。有关如何计算衰减分数的详情，请参阅
高斯衰减
、
指数衰减
和
线性衰减的
专门页面。
第三阶段：计算最终得分
最后，Milvus 将归一化的相似度得分和衰减得分结合起来，得出最终排名得分：
final_score = normalized_similarity_score × decay_score
在混合搜索（结合多个向量场）的情况下，Milvus 取搜索请求中最大的归一化相似度得分：
final_score = max([normalized_score₁, normalized_score₂, ..., normalized_scoreₙ]) × decay_score
例如，在混合搜索中，如果一篇研究论文的向量相似度得分是 0.82，而基于 BM25 的文本检索得分是 0.91，那么 Milvus 在应用衰减因子之前，会先使用 0.91 作为基本相似度得分。
实际的衰减排名
让我们在实际场景中看看衰减排名--基于时间的衰减搜索
"人工智能研究论文"：
在这个例子中，衰减得分反映了相关性随时间的推移而降低的情况--较新的论文得分接近 1.0，较老的论文得分较低。这些值是使用特定的衰减排序器计算得出的。有关详情，请参阅 "
选择合适的衰减排名器
"。
论文
向量相似度
归一化相似度得分
发表日期
衰减得分
最终得分
最终排名
论文 A
高分
0.85 (
COSINE
)
2 周前
0.80
0.68
2
纸张 B
非常高
0.92 (
COSINE
)
6 个月前
0.45
0.41
3
纸张 C
中
0.75 (
COSINE
)
1 天前
0.98
0.74
1
纸张 D
中-高
0.76 (
COSINE
)
3 周之前
0.70
0.53
4
如果不进行衰减重排，根据纯向量相似度（0.92），论文 B 的排名最高。然而，在应用了衰减重排后：
尽管相似度中等，论文 C 还是跃居第一，因为它是最近发表的（昨天发表的）。
论文 B 因发表时间较早，尽管相似度很高，但排名却降至第 3 位
论文 D 使用的是 L2 距离（越低越好），因此在应用衰减排序之前，其得分从 1.2 降为 0.76。
选择正确的衰减排序器
Milvus 提供不同的衰减排名器 -
gauss
,
exp
,
linear
，每个排名器都是针对特定的使用情况而设计的：
衰减排名器
特征
理想的使用案例
示例场景
高斯 (
gauss
)
自然的渐进式下降，延伸适度
需要平衡结果的一般搜索
用户对距离有直观感觉的应用
当距离适中时，结果不应受到严重影响
在餐厅搜索中，3 公里以外的优质餐厅仍然可以被发现，尽管排名低于附近的选择
指数 (
exp
)
起初迅速减少，但保持长尾效应
新闻馈送，时效性至关重要
社交媒体，新鲜内容应占主导地位
当强烈偏好近距离内容，但特殊的远距离内容应保持可见时
在新闻应用程序中，昨天的新闻比一周前的内容排名要高得多，但高度相关的旧文章仍会出现
线性 (
linear
)
持续、可预测的下降，有明确的分界线
有自然边界的应用
有距离限制的服务
有过期日期或明确阈值的内容
在事件查找器中，超过两周未来窗口的事件根本不会出现
有关每个衰减排名器如何计算分数和具体衰减模式的详细信息，请参阅专用文档：
高斯衰减
指数衰减
线性衰减
实施示例
衰减排名器可应用于 Milvus 中的标准向量搜索和混合搜索操作符。以下是实现这一功能的关键代码片段。
在使用衰减函数之前，必须先创建一个带有适当数值字段（如时间戳、距离等）的 Collection，这些数值字段将用于衰减计算。有关包括集合设置、Schema 定义和数据插入在内的完整工作示例，请参阅
教程：在 Milvus 中实施基于时间的排名
。
创建衰减排名器
要实现衰减排名，首先要定义一个具有适当配置的
Function
对象：
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
Function, FunctionType
# Create a decay function for timestamp-based decay
# Note: All time parameters must use the same unit as your collection data
decay_ranker = Function(
    name=
"time_decay"
,
# Function identifier
input_field_names=[
"timestamp"
],
# Numeric field to use for decay
function_type=FunctionType.RERANK,
# Must be set to RERANK for decay rankers
params={
"reranker"
:
"decay"
,
# Specify decay reranker. Must be "decay"
"function"
:
"gauss"
,
# Choose decay function type: "gauss", "exp", or "linear"
"origin"
:
int
(datetime.datetime(
2025
,
1
,
15
).timestamp()),
# Reference point (seconds)
"scale"
:
7
*
24
*
60
*
60
,
# 7 days in seconds (must match collection data unit)
"offset"
:
24
*
60
*
60
,
# 1 day no-decay zone (must match collection data unit)
"decay"
:
0.5
# Half score at scale distance
}
)
import
io.milvus.v2.service.vector.request.ranker.DecayRanker;
import
java.time.ZoneId;
import
java.time.ZonedDateTime;
ZonedDateTime
zdt
=
ZonedDateTime.of(
2025
,
1
,
25
,
0
,
0
,
0
,
0
, ZoneId.systemDefault());
DecayRanker
ranker
=
DecayRanker.builder()
        .name(
"time_decay"
)
        .inputFieldNames(Collections.singletonList(
"timestamp"
))
        .function(
"gauss"
)
        .origin(zdt.toInstant().toEpochMilli())
        .scale(
7
*
24
*
60
*
60
)
        .offset(
24
*
60
*
60
)
        .decay(
0.5
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
decayRanker = {
name
:
"time_decay"
,
input_field_names
: [
"timestamp"
],
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
"decay"
,
function
:
"gauss"
,
origin
:
new
Date
(
2025
,
1
,
15
).
getTime
(),
scale
:
7
*
24
*
60
*
60
,
offset
:
24
*
60
*
60
,
decay
:
0.5
,
  },
};
// go
# restful
参数
是否需要？
说明
值/示例
name
是
执行搜索时使用的函数标识符。选择一个与您的用例相关的描述性名称。
"time_decay"
input_field_names
是
用于计算衰减分数的数字字段。确定用于计算衰减的数据属性（例如，基于时间的衰减使用时间戳，基于位置的衰减使用坐标）。
必须是 Collections 中包含相关数值的字段。支持 INT8/16/32/64、FLOAT、DOUBLE。
["timestamp"]
function_type
是
指定创建的函数类型。
对于所有衰减排名器，必须设置为
RERANK
。
FunctionType.RERANK
params.reranker
是
指定要使用的 Reranker 方法。
必须设置为
"decay"
才能启用衰减排名功能。
"decay"
params.function
是
指定要应用的数学衰减排名器。确定相关性下降的曲线形状。
请参阅 "
选择合适的衰减排序器
"部分，了解如何选择合适的函数。
"gauss"
,
"exp"
, 或
"linear"
params.origin
是
计算衰减分数的参考点。处于此值的项目会获得最大相关性分数。
对于基于时间的衰减，时间单位必须与您的 Collections 数据相匹配。
对于时间戳：当前时间（如
int(time.time())
)
对于地理位置：用户当前坐标
params.scale
是
相关性下降到
decay
值的距离或时间。控制相关性下降的速度。
对于基于时间的衰减，时间单位必须与您的 Collections 数据相匹配。
数值越大，相关性下降越慢；数值越小，相关性下降越快。
对于时间：以秒为单位的周期（例如，
7 * 24 * 60 * 60
为 7 天）
距离：米（例如，
5000
表示 5 公里）
params.offset
无
在
origin
周围创建一个 "无衰减区"，在该区域内，项目保持满分（衰减分数 = 1.0）。
对于基于时间的衰减，时间单位必须与您的 Collections 数据一致。
在
origin
这个范围内的项目将保持最大相关性。
时间：以秒为单位的时间段（例如，
24 * 60 * 60
为 1 天）
对于距离：米（例如，
500
表示 500 米）
params.decay
无
scale
距离上的分数值，控制曲线陡度。数值越小，下降曲线越陡峭；数值越大，下降曲线越平缓。
必须介于 0 和 1 之间。
0.5
(默认值）
应用于标准向量搜索
定义衰减排序器后，您可以通过将其传递给
ranker
参数，在搜索操作过程中应用该排序器：
Python
Java
NodeJS
Go
cURL
# Use the decay function in standard vector search
results = milvus_client.search(
    collection_name,
    data=[your_query_vector],
# Replace with your query vector
anns_field=
"vector_field"
,
    limit=
10
,
    output_fields=[
"document"
,
"timestamp"
],
# Include the decay field in outputs to see values
ranker=decay_ranker,
# Apply the decay ranker here
consistency_level=
"Strong"
)
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
"search query"
)))
        .annsField(
"vector_field"
)
        .limit(
10
)
        .outputFields(Arrays.asList(
"document"
,
"timestamp"
))
        .functionScore(FunctionScore.builder()
                .addFunction(ranker)
                .build())
        .build();
SearchResp
searchResp
=
client.search(searchReq);
const
result =
await
milvusClient.
search
({
collection_name
:
"collection_name"
,
data
: [your_query_vector],
// Replace with your query vector
anns_field
:
"dense"
,
limit
:
10
,
output_fields
: [
"document"
,
"timestamp"
],
rerank
: ranker,
consistency_level
:
"Strong"
,
});
// go
# restful