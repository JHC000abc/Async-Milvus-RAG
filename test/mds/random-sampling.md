随机抽样
Compatible with Milvus 2.6.x
在处理大规模数据集时，您往往不需要处理所有数据来获得洞察力或测试过滤逻辑。随机抽样提供了一种解决方案，让您可以处理数据中具有统计代表性的子集，从而大大减少查询时间和资源消耗。
随机抽样在分段级别上操作，在确保高效性能的同时，还能在整个 Collections 的数据分布中保持样本的随机性。
主要用例
数据探索
：以最少的资源使用量快速预览 Collections 的结构和内容
开发测试
：在全面部署之前，在可管理的数据样本上测试复杂的过滤逻辑
资源优化
：降低探索性查询和统计分析的计算成本
语法
Python
Java
Go
NodeJS
cURL
filter
=
"RANDOM_SAMPLE(sampling_factor)"
String
filter
=
"RANDOM_SAMPLE(sampling_factor)"
filter :=
"RANDOM_SAMPLE(sampling_factor)"
// node
# restful
参数
sampling_factor
:取样系数，取样范围为 (0，1)，不包括边界。例如，
RANDOM_SAMPLE(0.001)
会选择大约 0.1% 的结果。
重要规则
表达式不区分大小写 (
RANDOM_SAMPLE
或
random_sample
)
取样因子必须在 (0, 1) 范围内，不包括边界
与其他筛选器结合使用
随机抽样操作符必须与其他过滤表达式相结合，使用逻辑
AND
。组合过滤器时，Milvus 首先应用其他条件，然后对结果集执行随机抽样。
Python
Java
Go
NodeJS
cURL
# Correct: Filter first, then sample
filter
=
'color == "red" AND RANDOM_SAMPLE(0.001)'
# Processing: Find all red items → Sample 0.1% of those red items
# Incorrect: OR doesn't make logical sense
filter
=
'color == "red" OR RANDOM_SAMPLE(0.001)'
# ❌ Invalid logic
# This would mean: "Either red items OR sample everything" - which is meaningless
// Correct: Filter first, then sample
String
filter
=
'color == "red" AND RANDOM_SAMPLE(0.001)'
;
// Processing: Find all red items → Sample 0.1% of those red items
// Incorrect: OR doesn't make logical sense
String
filter
=
'color == "red" OR RANDOM_SAMPLE(0.001)'
;
// ❌ Invalid logic
// This would mean: "Either red items OR sample everything" - which is meaningless
// Correct: Filter first, then sample
filter :=
'color == "red" AND RANDOM_SAMPLE(0.001)'
// Processing: Find all red items → Sample 0.1% of those red items
filter :=
'color == "red" OR RANDOM_SAMPLE(0.001)'
// ❌ Invalid logic
// This would mean: "Either red items OR sample everything" - which is meaningless
// node
# restful
示例
示例 1：数据探索
快速预览您的 Collection 结构：
Python
Java
Go
NodeJS
cURL
from
pymilvus
import
MilvusClient

client = MilvusClient(uri=
"http://localhost:19530"
)
# Sample approximately 1% of the entire collection
result = client.query(
    collection_name=
"product_catalog"
,
filter
=
"RANDOM_SAMPLE(0.01)"
,
output_fields=[
"id"
,
"product_name"
],
    limit=
10
)
print
(
f"Sampled
{
len
(result)}
products from collection"
)
import
io.milvus.v2.client.*;
import
io.milvus.v2.service.vector.request.QueryReq
import
io.milvus.v2.service.vector.request.QueryResp
ConnectConfig
config
=
ConnectConfig.builder()
        .uri(
"http://localhost:19530"
)
        .build();
MilvusClientV2
client
=
new
MilvusClientV2
(config);
QueryReq
queryReq
=
QueryReq.builder()
        .collectionName(
"product_catalog"
)
        .filter(
"RANDOM_SAMPLE(0.01)"
)
        .outputFields(Arrays.asList(
"id"
,
"product_name"
))
        .limit(
10
)
        .build();
QueryResp
queryResp
=
client.query(queryReq);

List<QueryResp.QueryResult> results = queryResp.getQueryResults();
for
(QueryResp.QueryResult result : results) {
    System.out.println(result.getEntity());
}
import
(
"context"
"fmt"
"github.com/milvus-io/milvus/client/v2/entity"
"github.com/milvus-io/milvus/client/v2/milvusclient"
)

ctx, cancel := context.WithCancel(context.Background())
defer
cancel()

milvusAddr :=
"localhost:19530"
client, err := milvusclient.New(ctx, &milvusclient.ClientConfig{
    Address: milvusAddr,
})
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
defer
client.Close(ctx)

resultSet, err := client.Query(ctx, milvusclient.NewQueryOption(
"product_catalog"
).
    WithFilter(
"RANDOM_SAMPLE(0.01)"
).
    WithOutputFields(
"id"
,
"product_name"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}

fmt.Println(
"id: "
, resultSet.GetColumn(
"id"
).FieldData().GetScalars())
fmt.Println(
"product_name: "
, resultSet.GetColumn(
"product_name"
).FieldData().GetScalars())
// node
# restful
示例 2：过滤与随机抽样相结合
在可管理的子集上测试过滤逻辑：
Python
Java
Go
NodeJS
cURL
# First filter by category and price, then sample 0.5% of results
filter_expression =
'category == "electronics" AND price > 100 AND RANDOM_SAMPLE(0.005)'
result = client.query(
    collection_name=
"product_catalog"
,
filter
=filter_expression,
output_fields=[
"product_name"
,
"price"
,
"rating"
],
    limit=
10
)
print
(
f"Found
{
len
(result)}
electronics products in sample"
)
String
filter
=
"category == \"electronics\" AND price > 100 AND RANDOM_SAMPLE(0.005)"
;
QueryReq
queryReq
=
QueryReq.builder()
        .collectionName(
"product_catalog"
)
        .filter(filter)
        .outputFields(Arrays.asList(
"product_name"
,
"price"
,
"rating"
))
        .limit(
10
)
        .build();
QueryResp
queryResp
=
client.query(queryReq);
filter :=
"category == \"electronics\" AND price > 100 AND RANDOM_SAMPLE(0.005)"
resultSet, err := client.Query(ctx, milvusclient.NewQueryOption(
"product_catalog"
).
    WithFilter(filter).
    WithOutputFields(
"product_name"
,
"price"
,
"rating"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
// node
# restful
示例 3：快速分析
对过滤后的数据进行快速统计分析：
Python
Java
Go
NodeJS
cURL
# Get insights from ~0.1% of premium customer data
filter_expression =
'customer_tier == "premium" AND region == '
North America
' AND RANDOM_SAMPLE(0.001)'
result = client.query(
    collection_name=
"customer_profiles"
,
filter
=filter_expression,
output_fields=[
"purchase_amount"
,
"satisfaction_score"
,
"last_purchase_date"
],
    limit=
10
)
# Analyze sample for quick insights
if
result:
    average_purchase =
sum
(r[
"purchase_amount"
]
for
r
in
result) /
len
(result)
    average_satisfaction =
sum
(r[
"satisfaction_score"
]
for
r
in
result) /
len
(result)
print
(
f"Sample size:
{
len
(result)}
"
)
print
(
f"Average purchase amount: $
{average_purchase:
.2
f}
"
)
print
(
f"Average satisfaction score:
{average_satisfaction:
.2
f}
"
)
String
filter
=
"customer_tier == \"premium\" AND region == \"North America\" AND RANDOM_SAMPLE(0.001)"
;
QueryReq
queryReq
=
QueryReq.builder()
        .collectionName(
"customer_profiles"
)
        .filter(filter)
        .outputFields(Arrays.asList(
"purchase_amount"
,
"satisfaction_score"
,
"last_purchase_date"
))
        .limit(
10
)
        .build();
QueryResp
queryResp
=
client.query(queryReq);
filter :=
"customer_tier == \"premium\" AND region == \"North America\" AND RANDOM_SAMPLE(0.001)"
resultSet, err := client.Query(ctx, milvusclient.NewQueryOption(
"customer_profiles"
).
    WithFilter(filter).
    WithOutputFields(
"purchase_amount"
,
"satisfaction_score"
,
"last_purchase_date"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
// node
# restful
示例 4：与向量搜索相结合
在过滤搜索场景中使用随机抽样：
Python
Java
Go
NodeJS
cURL
# Search for similar products within a sampled subset
search_results = client.search(
    collection_name=
"product_catalog"
,
    data=[[
0.1
,
0.2
,
0.3
,
0.4
,
0.5
]],
# query vector
filter
=
'category == "books" AND RANDOM_SAMPLE(0.01)'
,
search_params={
"metric_type"
:
"L2"
,
"params"
: {}},
    output_fields=[
"title"
,
"author"
,
"price"
],
    limit=
10
)
print
(
f"Found
{
len
(search_results[
0
])}
similar books in sample"
)
import
io.milvus.v2.service.vector.request.SearchReq
import
io.milvus.v2.service.vector.request.data.FloatVec;
import
io.milvus.v2.service.vector.response.SearchResp
FloatVec
queryVector
=
new
FloatVec
(
new
float
[]{
0.1f
,
0.2f
,
0.3f
,
0.4f
,
0.5f
});
SearchReq
searchReq
=
SearchReq.builder()
        .collectionName(
"product_catalog"
)
        .data(Collections.singletonList(queryVector))
        .topK(
10
)
        .filter(
"category == \"books\" AND RANDOM_SAMPLE(0.01)"
)
        .outputFields(Arrays.asList(
"title"
,
"author"
,
"price"
))
        .build();
SearchResp
searchResp
=
client.search(searchReq);

List<List<SearchResp.SearchResult>> searchResults = searchResp.getSearchResults();
for
(List<SearchResp.SearchResult> results : searchResults) {
    System.out.println(
"TopK results:"
);
for
(SearchResp.SearchResult result : results) {
        System.out.println(result);
    }
}
queryVector := []
float32
{
0.1
,
0.2
,
0.3
,
0.4
,
0.5
}

resultSets, err := client.Search(ctx, milvusclient.NewSearchOption(
"product_catalog"
,
// collectionName
10
,
// limit
[]entity.Vector{entity.FloatVector(queryVector)},
).WithConsistencyLevel(entity.ClStrong).
    WithFilter(
"category == \"books\" AND RANDOM_SAMPLE(0.01)"
).
    WithOutputFields(
"title"
,
"author"
,
"price"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
for
_, resultSet :=
range
resultSets {
    fmt.Println(
"title: "
, resultSet.GetColumn(
"title"
).FieldData().GetScalars())
    fmt.Println(
"author: "
, resultSet.GetColumn(
"author"
).FieldData().GetScalars())
    fmt.Println(
"price: "
, resultSet.GetColumn(
"price"
).FieldData().GetScalars())
}
// node
# restful
最佳实践
从小处入手
： 从较小的采样因子（0.001-0.01）开始进行初步探索
开发工作流程
：在开发过程中使用采样，在生产查询中移除采样
统计有效性
：较大的样本可提供更准确的统计表示
性能测试
：监控查询性能，并根据需要调整取样系数