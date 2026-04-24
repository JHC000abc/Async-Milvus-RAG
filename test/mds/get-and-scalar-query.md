查询
除 ANN 搜索外，Milvus 还支持通过查询过滤元数据。本页将介绍如何使用查询、获取和查询迭代器来执行元数据过滤。
如果在创建 Collections 后动态添加新字段，包含这些字段的查询将返回定义的默认值，对于未显式设置值的实体，则返回 NULL。有关详细信息，请参阅
向现有 Collections 添加字段
。
集合概述
Collections 可以存储各种类型的标量字段。你可以让 Milvus 根据一个或多个标量字段过滤实体。Milvus 提供三种类型的查询：查询、获取和查询迭代器。下表比较了这三种查询类型。
获取
查询
查询迭代器
适用情况
查找持有指定主键的实体。
查找符合自定义筛选条件的所有实体或指定数量的实体
在分页查询中查找满足自定义筛选条件的所有实体。
过滤方法
通过主键
通过过滤表达式
通过过滤表达式
必填参数
Collections 名称
主键
Collections 名称
过滤表达式
Collections 名称
过滤表达式
每次查询返回的实体数量
可选参数
分区名称
输出字段
分区名称
要返回的实体数量
输出字段
分区名称
要返回的实体总数
输出字段
返回值
返回指定集合或分区中持有指定主键的实体。
返回指定集合或分区中符合自定义筛选条件的所有实体或指定数量的实体。
通过分页查询返回指定集合或分区中符合自定义过滤条件的所有实体。
有关元数据过滤的更多信息，请参阅 .NET Framework 3.0。
使用获取
当需要通过主键查找实体时，可以使用
Get
方法。以下代码示例假定在 Collections 中有三个字段，分别名为
id
、
vector
和
color
。
[
        {
"id"
:
0
,
"vector"
: [
0.3580376395471989
, -
0.6023495712049978
,
0.18414012509913835
, -
0.26286205330961354
,
0.9029438446296592
],
"color"
:
"pink_8682"
},
        {
"id"
:
1
,
"vector"
: [
0.19886812562848388
,
0.06023560599112088
,
0.6976963061752597
,
0.2614474506242501
,
0.838729485096104
],
"color"
:
"red_7025"
},
        {
"id"
:
2
,
"vector"
: [
0.43742130801983836
, -
0.5597502546264526
,
0.6457887650909682
,
0.7894058910881185
,
0.20785793220625592
],
"color"
:
"orange_6781"
},
        {
"id"
:
3
,
"vector"
: [
0.3172005263489739
,
0.9719044792798428
, -
0.36981146090600725
, -
0.4860894583077995
,
0.95791889146345
],
"color"
:
"pink_9298"
},
        {
"id"
:
4
,
"vector"
: [
0.4452349528804562
, -
0.8757026943054742
,
0.8220779437047674
,
0.46406290649483184
,
0.30337481143159106
],
"color"
:
"red_4794"
},
        {
"id"
:
5
,
"vector"
: [
0.985825131989184
, -
0.8144651566660419
,
0.6299267002202009
,
0.1206906911183383
, -
0.1446277761879955
],
"color"
:
"yellow_4222"
},
        {
"id"
:
6
,
"vector"
: [
0.8371977790571115
, -
0.015764369584852833
, -
0.31062937026679327
, -
0.562666951622192
, -
0.8984947637863987
],
"color"
:
"red_9392"
},
        {
"id"
:
7
,
"vector"
: [-
0.33445148015177995
, -
0.2567135004164067
,
0.8987539745369246
,
0.9402995886420709
,
0.5378064918413052
],
"color"
:
"grey_8510"
},
        {
"id"
:
8
,
"vector"
: [
0.39524717779832685
,
0.4000257286739164
, -
0.5890507376891594
, -
0.8650502298996872
, -
0.6140360785406336
],
"color"
:
"white_9381"
},
        {
"id"
:
9
,
"vector"
: [
0.5718280481994695
,
0.24070317428066512
, -
0.3737913482606834
, -
0.06726932177492717
, -
0.6980531615588608
],
"color"
:
"purple_4976"
},
]
您可以通过它们的 ID 获取实体，如下所示。
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

res = client.get(
    collection_name=
"my_collection"
,
    ids=[
0
,
1
,
2
],
    output_fields=[
"vector"
,
"color"
]
)
print
(res)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.service.vector.request.GetReq
import
io.milvus.v2.service.vector.request.GetResp
import
io.milvus.v2.service.vector.response.QueryResp;
import
java.util.*;
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
GetReq
getReq
=
GetReq.builder()
        .collectionName(
"my_collection"
)
        .ids(Arrays.asList(
0
,
1
,
2
))
        .outputFields(Arrays.asList(
"vector"
,
"color"
))
        .build();
GetResp
getResp
=
client.get(getReq);

List<QueryResp.QueryResult> results = getResp.getGetResults();
for
(QueryResp.QueryResult result : results) {
    System.out.println(result.getEntity());
}
// Output
// {color=pink_8682, vector=[0.35803765, -0.6023496, 0.18414013, -0.26286206, 0.90294385], id=0}
// {color=red_7025, vector=[0.19886813, 0.060235605, 0.6976963, 0.26144746, 0.8387295], id=1}
// {color=orange_6781, vector=[0.43742132, -0.55975026, 0.6457888, 0.7894059, 0.20785794], id=2}
import
(
"context"
"fmt"
"github.com/milvus-io/milvus/client/v2/column"
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

resultSet, err := client.Get(ctx, milvusclient.NewQueryOption(
"my_collection"
).
    WithConsistencyLevel(entity.ClStrong).
    WithIDs(column.NewColumnInt64(
"id"
, []
int64
{
0
,
1
,
2
})).
    WithOutputFields(
"vector"
,
"color"
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
"vector: "
, resultSet.GetColumn(
"vector"
).FieldData().GetVectors())
fmt.Println(
"color: "
, resultSet.GetColumn(
"color"
).FieldData().GetScalars())
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
res = client.
get
({
    collection_name=
"my_collection"
,
    ids=[
0
,
1
,
2
],
    output_fields=[
"vector"
,
"color"
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
/v2/vectordb/entities/get"
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
    "id": [0, 1, 2],
    "outputFields": ["vector", "color"]
}'
# {"code":0,"cost":0,"data":[{"color":"pink_8682","id":0,"vector":[0.35803765,-0.6023496,0.18414013,-0.26286206,0.90294385]},{"color":"red_7025","id":1,"vector":[0.19886813,0.060235605,0.6976963,0.26144746,0.8387295]},{"color":"orange_6781","id":2,"vector":[0.43742132,-0.55975026,0.6457888,0.7894059,0.20785794]}]}
使用查询
当您需要通过自定义过滤条件查找实体时，请使用
Query
方法。以下代码示例假定有三个字段，分别名为
id
、
vector
和
color
，并返回从
red
开始持有
color
值的实体的指定数目。
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

res = client.query(
    collection_name=
"my_collection"
,
filter
=
"color like \"red%\""
,
    output_fields=[
"vector"
,
"color"
],
    limit=
3
)
import
io.milvus.v2.service.vector.request.QueryReq
import
io.milvus.v2.service.vector.request.QueryResp
QueryReq
queryReq
=
QueryReq.builder()
        .collectionName(
"my_collection"
)
        .filter(
"color like \"red%\""
)
        .outputFields(Arrays.asList(
"vector"
,
"color"
))
        .limit(
3
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
// Output
// {color=red_7025, vector=[0.19886813, 0.060235605, 0.6976963, 0.26144746, 0.8387295], id=1}
// {color=red_4794, vector=[0.44523495, -0.8757027, 0.82207793, 0.4640629, 0.3033748], id=4}
// {color=red_9392, vector=[0.8371978, -0.015764369, -0.31062937, -0.56266695, -0.8984948], id=6}
resultSet, err := client.Query(ctx, milvusclient.NewQueryOption(
"my_collection"
).
    WithFilter(
"color like \"red%\""
).
    WithOutputFields(
"vector"
,
"color"
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
"vector: "
, resultSet.GetColumn(
"vector"
).FieldData().GetVectors())
fmt.Println(
"color: "
, resultSet.GetColumn(
"color"
).FieldData().GetScalars())
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
res = client.
query
({
    collection_name=
"my_collection"
,
    filter=
'color like "red%"'
,
    output_fields=[
"vector"
,
"color"
],
limit
(
3
)
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
/v2/vectordb/entities/query"
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
    "filter": "color like \"red%\"",
    "limit": 3,
    "outputFields": ["vector", "color"]
}'
#{"code":0,"cost":0,"data":[{"color":"red_7025","id":1,"vector":[0.19886813,0.060235605,0.6976963,0.26144746,0.8387295]},{"color":"red_4794","id":4,"vector":[0.44523495,-0.8757027,0.82207793,0.4640629,0.3033748]},{"color":"red_9392","id":6,"vector":[0.8371978,-0.015764369,-0.31062937,-0.56266695,-0.8984948]}]}
使用查询迭代器
当您需要通过分页查询按自定义过滤条件查找实体时，可创建一个
QueryIterator
并使用其
next()
方法遍历所有实体，以查找满足过滤条件的实体。以下代码示例假定有三个字段，分别名为
id
、
vector
和
color
，并从
red
开始返回持有
color
值的所有实体。
Python
Java
Go
NodeJS
cURL
from
pymilvus
import
connections, Collection

connections.connect(
    uri=
"http://localhost:19530"
,
    token=
"root:Milvus"
)

collection = Collection(
"my_collection"
)

iterator = collection.query_iterator(
    batch_size=
10
,
    expr=
"color like \"red%\""
,
    output_fields=[
"color"
]
)

results = []
while
True
:
    result = iterator.
next
()
if
not
result:
        iterator.close()
break
print
(result)
    results += result
import
io.milvus.orm.iterator.QueryIterator;
import
io.milvus.response.QueryResultsWrapper;
import
io.milvus.v2.common.ConsistencyLevel;
import
io.milvus.v2.service.vector.request.QueryIteratorReq;
QueryIteratorReq
req
=
QueryIteratorReq.builder()
        .collectionName(
"my_collection"
)
        .expr(
"color like \"red%\""
)
        .batchSize(
50L
)
        .outputFields(Collections.singletonList(
"color"
))
        .consistencyLevel(ConsistencyLevel.BOUNDED)
        .build();
QueryIterator
queryIterator
=
client.queryIterator(req);
while
(
true
) {
    List<QueryResultsWrapper.RowRecord> res = queryIterator.next();
if
(res.isEmpty()) {
        queryIterator.close();
break
;
    }
for
(QueryResultsWrapper.RowRecord record : res) {
        System.out.println(record);
    }
}
// Output
// [color:red_7025, id:1]
// [color:red_4794, id:4]
// [color:red_9392, id:6]
// go
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
iterator =
await
milvusClient.
queryIterator
({
collection_name
:
'my_collection'
,
batchSize
:
10
,
expr
:
'color like "red%"'
,
output_fields
: [
'color'
],
});
const
results = [];
for
await
(
const
value
of
iterator) {
  results.
push
(...value);
  page +=
1
;
}
# Not available
分区中的查询
您还可以通过在 Get、Query 或 QueryIterator 请求中包含分区名称，在一个或多个分区中执行查询。以下代码示例假定 Collections 中有一个名为
PartitionA
的分区。
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

res = client.get(
    collection_name=
"my_collection"
,
partitionNames=[
"partitionA"
],
ids=[
10
,
11
,
12
],
    output_fields=[
"vector"
,
"color"
]
)
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

res = client.query(
    collection_name=
"my_collection"
,
partitionNames=[
"partitionA"
],
filter
=
"color like \"red%\""
,
    output_fields=[
"vector"
,
"color"
],
    limit=
3
)
# Use QueryIterator
from
pymilvus
import
connections, Collection

connections.connect(
    uri=
"http://localhost:19530"
,
    token=
"root:Milvus"
)

collection = Collection(
"my_collection"
)

iterator = collection.query_iterator(
partition_names=[
"partitionA"
],
batch_size=
10
,
    expr=
"color like \"red%\""
,
    output_fields=[
"color"
]
)

results = []
while
True
:
    result = iterator.
next
()
if
not
result:
        iterator.close()
break
print
(result)
    results += result
GetReq
getReq
=
GetReq.builder()
        .collectionName(
"my_collection"
)
        .partitionName(
"partitionA"
)
        .ids(Arrays.asList(
10
,
11
,
12
))
        .outputFields(Collections.singletonList(
"color"
))
        .build();
GetResp
getResp
=
client.get(getReq);
QueryReq
queryReq
=
QueryReq.builder()
        .collectionName(
"my_collection"
)
        .partitionNames(Collections.singletonList(
"partitionA"
))
        .filter(
"color like \"red%\""
)
        .outputFields(Collections.singletonList(
"color"
))
        .limit(
3
)
        .build();
QueryResp
getResp
=
client.query(queryReq);
QueryIteratorReq
req
=
QueryIteratorReq.builder()
        .collectionName(
"my_collection"
)
        .partitionNames(Collections.singletonList(
"partitionA"
))
        .expr(
"color like \"red%\""
)
        .batchSize(
50L
)
        .outputFields(Collections.singletonList(
"color"
))
        .consistencyLevel(ConsistencyLevel.BOUNDED)
        .build();
QueryIterator
queryIterator
=
client.queryIterator(req);
resultSet, err := client.Get(ctx, milvusclient.NewQueryOption(
"my_collection"
).
    WithPartitions(
"partitionA"
).
    WithIDs(column.NewColumnInt64(
"id"
, []
int64
{
10
,
11
,
12
})).
    WithOutputFields(
"vector"
,
"color"
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
"vector: "
, resultSet.GetColumn(
"vector"
).FieldData().GetVectors())
fmt.Println(
"color: "
, resultSet.GetColumn(
"color"
).FieldData().GetScalars())

resultSet, err := client.Query(ctx, milvusclient.NewQueryOption(
"my_collection"
).
    WithPartitions(
"partitionA"
).
    WithFilter(
"color like \"red%\""
).
    WithOutputFields(
"vector"
,
"color"
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
"vector: "
, resultSet.GetColumn(
"vector"
).FieldData().GetVectors())
fmt.Println(
"color: "
, resultSet.GetColumn(
"color"
).FieldData().GetScalars())
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
// Use get
var
res = client.
query
({
    collection_name=
"my_collection"
,
partition_names=[
"partitionA"
],
filter=
'color like "red%"'
,
    output_fields=[
"vector"
,
"color"
],
limit
(
3
)
})
// Use query
res = client.
query
({
    collection_name=
"my_collection"
,
partition_names=[
"partitionA"
],
filter=
"color like \"red%\""
,
    output_fields=[
"vector"
,
"color"
],
limit
(
3
)
})
// Use queryiterator
const
iterator =
await
milvusClient.
queryIterator
({
collection_name
:
'my_collection'
,
partition_names
: [
'partitionA'
],
batchSize
:
10
,
expr
:
'color like "red%"'
,
output_fields
: [
'vector'
,
'color'
],
});
const
results = [];
for
await
(
const
value
of
iterator) {
  results.
push
(...value);
  page +=
1
;
}
export
CLUSTER_ENDPOINT=
"http://localhost:19530"
export
TOKEN=
"root:Milvus"
# Use get
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/entities/get"
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
    "partitionNames": ["partitionA"],
    "id": [0, 1, 2],
    "outputFields": ["vector", "color"]
}'
# Use query
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/entities/get"
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
    "partitionNames": ["partitionA"],
    "filter": "color like \"red%\"",
    "limit": 3,
    "outputFields": ["vector", "color"],
    "id": [0, 1, 2]
}'
使用查询进行随机抽样
要从 Collections 中提取具有代表性的数据子集用于数据探索或开发测试，请使用
RANDOM_SAMPLE(sampling_factor)
表达式，其中
sampling_factor
是介于 0 和 1 之间的浮点数，代表要采样的数据百分比。
有关详细用法、高级示例和最佳实践，请参阅
随机抽样
。
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
# Sample 1% of the entire collection
res = client.query(
    collection_name=
"my_collection"
,
filter
=
"RANDOM_SAMPLE(0.01)"
,
output_fields=[
"vector"
,
"color"
]
)
print
(
f"Sampled
{
len
(res)}
entities from collection"
)
# Combine with other filters - first filter, then sample
res = client.query(
    collection_name=
"my_collection"
,
filter
=
"color like \"red%\" AND RANDOM_SAMPLE(0.005)"
,
output_fields=[
"vector"
,
"color"
],
    limit=
10
)
print
(
f"Found
{
len
(res)}
red items in sample"
)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.service.vector.request.GetReq
import
io.milvus.v2.service.vector.request.GetResp
import
io.milvus.v2.service.vector.request.QueryReq
import
io.milvus.v2.service.vector.request.QueryResp
import
java.util.*;
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
QueryReq
queryReq
=
QueryReq.builder()
        .collectionName(
"my_collection"
)
        .filter(
"RANDOM_SAMPLE(0.01)"
)
        .outputFields(Arrays.asList(
"vector"
,
"color"
))
        .build();
QueryResp
getResp
=
client.query(queryReq);
for
(QueryResp.QueryResult result : getResp.getQueryResults()) {
    System.out.println(result.getEntity());
}

queryReq = QueryReq.builder()
        .collectionName(
"my_collection"
)
        .filter(
"color like \"red%\" AND RANDOM_SAMPLE(0.005)"
)
        .outputFields(Arrays.asList(
"vector"
,
"color"
))
        .limit(
10
)
        .build();

getResp = client.query(queryReq);
for
(QueryResp.QueryResult result : getResp.getQueryResults()) {
    System.out.println(result.getEntity());
}
import
(
"context"
"fmt"
"github.com/milvus-io/milvus/client/v2/column"
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
return
err
}

resultSet, err := client.Query(ctx, milvusclient.NewQueryOption(
"my_collection"
).
    WithFilter(
"RANDOM_SAMPLE(0.01)"
).
    WithOutputFields(
"vector"
,
"color"
))
if
err !=
nil
{
return
err
}

resultSet, err = client.Query(ctx, milvusclient.NewQueryOption(
"my_collection"
).
    WithFilter(
"color like \"red%\" AND RANDOM_SAMPLE(0.005)"
).
    WithLimit(
10
).
    WithOutputFields(
"vector"
,
"color"
))
if
err !=
nil
{
return
err
}
// node
# restful
为查询临时设置时区
如果您的 Collections 有
TIMESTAMPTZ
字段，您可以通过在查询调用中设置
timezone
参数，为单次操作临时覆盖数据库或 Collections 的默认时区。这可以控制
TIMESTAMPTZ
值在操作过程中的显示和比较方式。
timezone
的值必须是有效的
IANA 时区标识符
（例如，
亚洲/上海
、
美国/芝加哥
或
UTC
）。有关如何使用
TIMESTAMPTZ
字段的详细信息，请参阅
TIMESTAMPTZ 字段
。
下面的示例展示了如何为查询操作临时设置时区：
Python
Java
NodeJS
Go
cURL
# Query data and display the tsz field converted to "America/Havana"
results = client.query(
    collection_name,
filter
=
"id <= 10"
,
    output_fields=[
"id"
,
"tsz"
,
"vec"
],
    limit=
2
,
timezone=
"America/Havana"
,
)
// java
// js
// go
# restful