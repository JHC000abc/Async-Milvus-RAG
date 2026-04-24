过滤搜索
ANN 搜索能找到与指定向量嵌入最相似的向量嵌入。但是，搜索结果不一定总是正确的。您可以在搜索请求中包含过滤条件，以便 Milvus 在进行 ANN 搜索前进行元数据过滤，将搜索范围从整个 Collections 缩小到只搜索符合指定过滤条件的实体。
概述
在 Milvus 中，过滤搜索根据应用过滤的阶段分为两种类型--
标准过滤
和
迭代过滤
。
标准过滤
如果 Collections 同时包含向量嵌入及其元数据，您可以在 ANN 搜索之前过滤元数据，以提高搜索结果的相关性。Milvus 收到携带过滤条件的搜索请求后，会将搜索范围限制在符合指定过滤条件的实体内。
过滤搜索
如上图所示，搜索请求携带
chunk like "%red%"
作为过滤条件，表明 Milvus 应在
chunk
字段中包含
red
的所有实体内进行 ANN 搜索。具体来说，Milvus 会执行以下操作：
过滤符合搜索请求中过滤条件的实体。
在过滤后的实体中进行 ANN 搜索。
返回前 K 个实体。
迭代过滤
标准过滤过程能有效地将搜索范围缩小到很小的范围。但是，过于复杂的过滤表达式可能会导致非常高的搜索延迟。在这种情况下，迭代过滤可以作为一种替代方法，帮助减少标量过滤的工作量。
迭代过滤
如上图所示，使用迭代过滤的搜索以迭代的方式执行向量搜索。迭代器返回的每个实体都要经过标量过滤，这个过程一直持续到达到指定的 topK 结果为止。
这种方法大大减少了进行标量过滤的实体数量，特别有利于处理高度复杂的过滤表达式。
不过，值得注意的是，迭代器一次处理一个实体。这种顺序方法可能会导致较长的处理时间或潜在的性能问题，尤其是在对大量实体进行标量过滤时。
示例
本节演示如何进行过滤搜索。本节中的代码片段假定你已经在 Collections 中拥有以下实体。每个实体都有四个字段，即
id
、
向量
、
颜色
和
喜欢
。
[
{
"id"
:
0
,
"vector"
:
[
0.3580376395471989
,
-0.6023495712049978
,
0.18414012509913835
,
-0.26286205330961354
,
0.9029438446296592
]
,
"color"
:
"pink_8682"
,
"likes"
:
165
}
,
{
"id"
:
1
,
"vector"
:
[
0.19886812562848388
,
0.06023560599112088
,
0.6976963061752597
,
0.2614474506242501
,
0.838729485096104
]
,
"color"
:
"red_7025"
,
"likes"
:
25
}
,
{
"id"
:
2
,
"vector"
:
[
0.43742130801983836
,
-0.5597502546264526
,
0.6457887650909682
,
0.7894058910881185
,
0.20785793220625592
]
,
"color"
:
"orange_6781"
,
"likes"
:
764
}
,
{
"id"
:
3
,
"vector"
:
[
0.3172005263489739
,
0.9719044792798428
,
-0.36981146090600725
,
-0.4860894583077995
,
0.95791889146345
]
,
"color"
:
"pink_9298"
,
"likes"
:
234
}
,
{
"id"
:
4
,
"vector"
:
[
0.4452349528804562
,
-0.8757026943054742
,
0.8220779437047674
,
0.46406290649483184
,
0.30337481143159106
]
,
"color"
:
"red_4794"
,
"likes"
:
122
}
,
{
"id"
:
5
,
"vector"
:
[
0.985825131989184
,
-0.8144651566660419
,
0.6299267002202009
,
0.1206906911183383
,
-0.1446277761879955
]
,
"color"
:
"yellow_4222"
,
"likes"
:
12
}
,
{
"id"
:
6
,
"vector"
:
[
0.8371977790571115
,
-0.015764369584852833
,
-0.31062937026679327
,
-0.562666951622192
,
-0.8984947637863987
]
,
"color"
:
"red_9392"
,
"likes"
:
58
}
,
{
"id"
:
7
,
"vector"
:
[
-0.33445148015177995
,
-0.2567135004164067
,
0.8987539745369246
,
0.9402995886420709
,
0.5378064918413052
]
,
"color"
:
"grey_8510"
,
"likes"
:
775
}
,
{
"id"
:
8
,
"vector"
:
[
0.39524717779832685
,
0.4000257286739164
,
-0.5890507376891594
,
-0.8650502298996872
,
-0.6140360785406336
]
,
"color"
:
"white_9381"
,
"likes"
:
876
}
,
{
"id"
:
9
,
"vector"
:
[
0.5718280481994695
,
0.24070317428066512
,
-0.3737913482606834
,
-0.06726932177492717
,
-0.6980531615588608
]
,
"color"
:
"purple_4976"
,
"likes"
:
765
}
]
如果目标 Collections 中已经存在查询向量，可以考虑使用
ids
，而不是在搜索前检索它们。有关详情，请参阅
主键搜索
。
使用标准过滤进行搜索
下面的代码片段演示了使用标准过滤进行搜索，下面代码片段中的请求带有一个过滤条件和多个输出字段。
Python
Java
Go
NodeJS
cURL
from
pymilvus
import
MilvusClient

client = MilvusClient(
    uri=
"http://localhost:19530"
,
    token=
"root:Milvus"
)

query_vector = [
0.3580376395471989
, -
0.6023495712049978
,
0.18414012509913835
, -
0.26286205330961354
,
0.9029438446296592
]

res = client.search(
    collection_name=
"my_collection"
,
    data=[query_vector],
    limit=
5
,
filter
=
'color like "red%" and likes > 50'
,
output_fields=[
"color"
,
"likes"
]
)
for
hits
in
res:
print
(
"TopK results:"
)
for
hit
in
hits:
print
(hit)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.service.vector.request.SearchReq
import
io.milvus.v2.service.vector.request.data.FloatVec;
import
io.milvus.v2.service.vector.response.SearchResp
MilvusClientV2
client
=
new
MilvusClientV2
(ConnectConfig.builder()
        .uri(
"http://localhost:19530"
)
        .token(
"root:Milvus"
)
        .build());
FloatVec
queryVector
=
new
FloatVec
(
new
float
[]{
0.3580376395471989f
, -
0.6023495712049978f
,
0.18414012509913835f
, -
0.26286205330961354f
,
0.9029438446296592f
});
SearchReq
searchReq
=
SearchReq.builder()
        .collectionName(
"my_collection"
)
        .data(Collections.singletonList(queryVector))
        .topK(
5
)
        .filter(
"color like \"red%\" and likes > 50"
)
        .outputFields(Arrays.asList(
"color"
,
"likes"
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
// Output
// TopK results:
// SearchResp.SearchResult(entity={color=red_4794, likes=122}, score=0.5975797, id=4)
// SearchResp.SearchResult(entity={color=red_9392, likes=58}, score=-0.24996188, id=6)
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
token :=
"root:Milvus"
client, err := client.New(ctx, &client.ClientConfig{
    Address: milvusAddr,
    APIKey:  token,
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

queryVector := []
float32
{
0.3580376395471989
,
-0.6023495712049978
,
0.18414012509913835
,
-0.26286205330961354
,
0.9029438446296592
}

resultSets, err := client.Search(ctx, milvusclient.NewSearchOption(
"my_collection"
,
// collectionName
5
,
// limit
[]entity.Vector{entity.FloatVector(queryVector)},
).WithConsistencyLevel(entity.ClStrong).
    WithANNSField(
"vector"
).
    WithFilter(
"color like 'red%' and likes > 50"
).
    WithOutputFields(
"color"
,
"likes"
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
"IDs: "
, resultSet.IDs.FieldData().GetScalars())
    fmt.Println(
"Scores: "
, resultSet.Scores)
    fmt.Println(
"color: "
, resultSet.GetColumn(
"color"
).FieldData().GetScalars())
    fmt.Println(
"likes: "
, resultSet.GetColumn(
"likes"
).FieldData().GetScalars())
}
import
{
MilvusClient
,
DataType
}
from
"@zilliz/milvus2-sdk-node"
;
const
address =
"http://localhost:19530"
;
const
token =
"root:Milvus"
;
const
client =
new
MilvusClient
({address, token});
const
query_vector = [
0.3580376395471989
, -
0.6023495712049978
,
0.18414012509913835
, -
0.26286205330961354
,
0.9029438446296592
]
const
res =
await
client.
search
({
collection_name
:
"my_collection"
,
data
: [query_vector],
limit
:
5
,
filters
:
'color like "red%" and likes > 50'
,
output_fields
: [
"color"
,
"likes"
]
})
export
CLUSTER_ENDPOINT=
"http://localhost:19530"
export
TOKEN=
"root:Milvus"
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/entities/search"
\
--header
"Authorization: Bearer
${TOKEN}
"
\
--header
"Content-Type: application/json"
\
-d
'{
    "collectionName": "my_collection",
    "data": [
        [0.3580376395471989, -0.6023495712049978, 0.18414012509913835, -0.26286205330961354, 0.9029438446296592]
    ],
    "annsField": "vector",
    "filter": "color like \"red%\" and likes > 50",
    "limit": 5,
    "outputFields": ["color", "likes"]
}'
# {"code":0,"cost":0,"data":[]}
搜索请求中的过滤条件为
color like "red%" and likes > 50
。它使用 and 操作符包含两个条件：第一个条件要求在
color
字段中查找值以
red
开头的实体，其他条件要求在
likes
字段中查找值大于
50
的实体。只有两个实体符合这些要求。当 top-K 设置为
3
时，Milvus 将计算这两个实体与查询向量的距离，并将它们作为搜索结果返回。
[
{
"id"
:
4
,
"distance"
:
0.3345786594834839
,
"entity"
:
{
"vector"
:
[
0.4452349528804562
,
-0.8757026943054742
,
0.8220779437047674
,
0.46406290649483184
,
0.30337481143159106
]
,
"color"
:
"red_4794"
,
"likes"
:
122
}
}
,
{
"id"
:
6
,
"distance"
:
0.6638239834383389
，
"entity"
:
{
"vector"
:
[
0.8371977790571115
,
-0.015764369584852833
,
-0.31062937026679327
,
-0.562666951622192
,
-0.8984947637863987
]
,
"color"
:
"red_9392"
,
"likes"
:
58
}
}
,
]
有关元数据过滤中可使用的操作符的更多信息，请参阅
过滤
。
使用迭代过滤搜索
使用迭代过滤进行过滤搜索的方法如下：
Python
Java
Go
NodeJS
cURL
from
pymilvus
import
MilvusClient

client = MilvusClient(
    uri=
"http://localhost:19530"
,
    token=
"root:Milvus"
)

query_vector = [
0.3580376395471989
, -
0.6023495712049978
,
0.18414012509913835
, -
0.26286205330961354
,
0.9029438446296592
]

res = client.search(
    collection_name=
"my_collection"
,
    data=[query_vector],
    limit=
5
,
filter
=
'color like "red%" and likes > 50'
,
output_fields=[
"color"
,
"likes"
],
search_params={
"hints"
:
"iterative_filter"
}
)
for
hits
in
res:
print
(
"TopK results:"
)
for
hit
in
hits:
print
(hit)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.service.vector.request.SearchReq;
import
io.milvus.v2.service.vector.request.data.FloatVec;
import
io.milvus.v2.service.vector.response.SearchResp;
MilvusClientV2
client
=
new
MilvusClientV2
(ConnectConfig.builder()
        .uri(
"http://localhost:19530"
)
        .token(
"root:Milvus"
)
        .build());
FloatVec
queryVector
=
new
FloatVec
(
new
float
[]{
0.3580376395471989f
, -
0.6023495712049978f
,
0.18414012509913835f
, -
0.26286205330961354f
,
0.9029438446296592f
});
SearchReq
searchReq
=
SearchReq.builder()
        .collectionName(
"my_collection"
)
        .data(Collections.singletonList(queryVector))
        .topK(
5
)
        .filter(
"color like \"red%\" and likes > 50"
)
        .outputFields(Arrays.asList(
"color"
,
"likes"
))
        .searchParams(
new
HashMap
<>(
"hints"
,
"iterative_filter"
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
// Output
// TopK results:
// SearchResp.SearchResult(entity={color=red_4794, likes=122}, score=0.5975797, id=4)
// SearchResp.SearchResult(entity={color=red_9392, likes=58}, score=-0.24996188, id=6)
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
token :=
"root:Milvus"
client, err := client.New(ctx, &client.ClientConfig{
    Address: milvusAddr,
    APIKey:  token,
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

queryVector := []
float32
{
0.3580376395471989
,
-0.6023495712049978
,
0.18414012509913835
,
-0.26286205330961354
,
0.9029438446296592
}

resultSets, err := client.Search(ctx, milvusclient.NewSearchOption(
"my_collection"
,
// collectionName
5
,
// limit
[]entity.Vector{entity.FloatVector(queryVector)},
).WithConsistencyLevel(entity.ClStrong).
    WithANNSField(
"vector"
).
    WithFilter(
"color like 'red%' and likes > 50"
).
    WithOutputFields(
"color"
,
"likes"
).
    WithSearchParam(
"hints"
,
"iterative_filter"
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
"IDs: "
, resultSet.IDs.FieldData().GetScalars())
    fmt.Println(
"Scores: "
, resultSet.Scores)
    fmt.Println(
"color: "
, resultSet.GetColumn(
"color"
).FieldData().GetScalars())
    fmt.Println(
"likes: "
, resultSet.GetColumn(
"likes"
).FieldData().GetScalars())
}
import
{
MilvusClient
,
DataType
}
from
"@zilliz/milvus2-sdk-node"
;
const
address =
"http://localhost:19530"
;
const
token =
"root:Milvus"
;
const
client =
new
MilvusClient
({address, token});
const
query_vector = [
0.3580376395471989
, -
0.6023495712049978
,
0.18414012509913835
, -
0.26286205330961354
,
0.9029438446296592
]
const
res =
await
client.
search
({
collection_name
:
"filtered_search_collection"
,
data
: [query_vector],
limit
:
5
,
filters
:
'color like "red%" and likes > 50'
,
hints
:
"iterative_filter"
,
output_fields
: [
"color"
,
"likes"
]
})
export
CLUSTER_ENDPOINT=
"http://localhost:19530"
export
TOKEN=
"root:Milvus"
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/entities/search"
\
--header
"Authorization: Bearer
${TOKEN}
"
\
--header
"Content-Type: application/json"
\
-d
'{
    "collectionName": "my_collection",
    "data": [
        [0.3580376395471989, -0.6023495712049978, 0.18414012509913835, -0.26286205330961354, 0.9029438446296592]
    ],
    "annsField": "vector",
    "filter": "color like \"red%\" and likes > 50",
    "searchParams": {"hints": "iterative_filter"},
    "limit": 5,
    "outputFields": ["color", "likes"]
}'
# {"code":0,"cost":0,"data":[]}