更新实体
upsert
操作符为在 Collections 中插入或更新实体提供了一种便捷的方法。
操作概述
您可以使用
upsert
插入新实体或更新现有实体，具体取决于 upsert 请求中提供的主键是否存在于 Collections 中。如果找不到主键，则进行插入操作。否则，将执行更新操作。
在 Milvus 中，upsert 可在
覆盖
或
合并
模式下工作。
覆盖模式下的upsert
覆盖模式下的上载请求结合了插入和删除操作。当收到针对现有实体的
upsert
请求时，Milvus 会插入请求有效载荷中携带的数据，并同时删除数据中指定原始主键的现有实体。
覆盖模式下的上插入
如果目标 Collections 的主字段启用了
autoid
，Milvus 将为请求有效载荷中携带的数据生成一个新的主键，然后再插入。
对于启用了
nullable
的字段，如果不需要更新，可以在
upsert
请求中省略。
在合并模式下向上插入
Compatible with Milvus v2.6.2+
您还可以使用
partial_update
标志，使上载请求以合并模式运行。这样就可以在请求有效载荷中只包含需要更新的字段。
合并模式下的upsert
要执行合并，请在
upsert
请求中将
partial_update
设置为
True
，并将主键和要更新的字段设置为新值。
收到这样的请求后，Milvus 会执行强一致性查询以检索实体，根据请求中的数据更新字段值，插入修改后的数据，然后用请求中携带的原始主键删除现有实体。
向上插入行为：特别注意事项
在使用合并功能之前，有几个特别注意事项需要考虑。以下情况假设你有一个 Collections，其中有两个标量字段，分别命名为
title
和
issue
，同时还有一个主键
id
和一个向量字段
vector
。
启用
nullable
的向上插入字段
。
假设
issue
字段可以为空。在倒插这些字段时，请注意以下几点：
如果在
upsert
请求中省略
issue
字段并禁用
partial_update
，
issue
字段将更新为
null
，而不是保留其原始值。
要保留
issue
字段的原始值，要么启用
partial_update
并省略
issue
字段，要么在
upsert
请求中包含
issue
字段及其原始值。
在动态字段中倒插键
。
假设在示例 Collections 中启用了动态键，实体动态字段中的键值对与
{"author": "John", "year": 2020, "tags": ["fiction"]}
类似。
当你向上插入实体的键，如
author
,
year
, 或
tags
，或添加其他键时，请注意：
如果上载
partial_update
时禁用，默认行为是
覆盖
。这意味着动态字段的值将被请求中包含的所有非 Schema 定义的字段及其值覆盖。
例如，如果请求中包含的数据是
{"author": "Jane", "genre": "fantasy"}
，目标实体动态字段中的键值对将更新为该值。
如果在启用
partial_update
的情况下进行 upsert，默认行为是
合并
。这意味着动态字段的值将与请求中包含的所有非 Schema 定义的字段及其值合并。
例如，如果请求中包含的数据是
{"author": "John", "year": 2020, "tags": ["fiction"]}
，则目标实体动态字段中的键值对在 upsert 后将变成
{"author": "John", "year": 2020, "tags": ["fiction"], "genre": "fantasy"}
。
倒插一个 JSON 字段。
假设示例 Collections 有一个名为
extras
的 Schema 定义 JSON 字段，实体的此 JSON 字段中的键值对类似于
{"author": "John", "year": 2020, "tags": ["fiction"]}
。
当您使用修改后的 JSON 数据向上插入实体的
extras
字段时，请注意该 JSON 字段被视为一个整体，您不能有选择地更新单个键。换句话说，JSON 字段
不
支持
合并
模式下的上载。
限制和约束
基于上述内容，有几个限制和约束需要遵循：
upsert
请求必须始终包含目标实体的主键。
目标 Collections 必须已加载并可供查询。
请求中指定的所有字段必须存在于目标 Collections 的 Schema 中。
请求中指定的所有字段的值必须与 Schema 中定义的数据类型相匹配。
对于使用函数从另一个字段派生出来的任何字段，Milvus 将在倒插过程中删除派生字段，以便重新计算。
倒插 Collections 中的实体
在本节中，我们将把实体上载到名为
my_collection
的 Collections 中。该 Collections 只有两个字段，分别名为
id
,
vector
,
title
和
issue
。
id
字段是主字段，而
title
和
issue
字段是标量字段。
这三个实体如果存在于 Collections 中，将被包含 upsert 请求的实体覆盖。
Python
Java
NodeJS
Go
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

data=[
    {
"id"
:
0
,
"vector"
: [-
0.619954382375778
,
0.4479436794798608
, -
0.17493894838751745
, -
0.4248030059917294
, -
0.8648452746018911
],
"title"
:
"Artificial Intelligence in Real Life"
,
"issue"
:
"vol.12"
}, {
"id"
:
1
,
"vector"
: [
0.4762662251462588
, -
0.6942502138717026
, -
0.4490002642657902
, -
0.628696575798281
,
0.9660395877041965
],
"title"
:
"Hollow Man"
,
"issue"
:
"vol.19"
}, {
"id"
:
2
,
"vector"
: [-
0.8864122635045097
,
0.9260170474445351
,
0.801326976181461
,
0.6383943392381306
,
0.7563037341572827
],
"title"
:
"Treasure Hunt in Missouri"
,
"issue"
:
"vol.12"
}
]

res = client.upsert(
    collection_name=
'my_collection'
,
    data=data
)
print
(res)
# Output
# {'upsert_count': 3}
import
com.google.gson.Gson;
import
com.google.gson.JsonObject;
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.service.vector.request.UpsertReq;
import
io.milvus.v2.service.vector.response.UpsertResp;
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
Gson
gson
=
new
Gson
();
List<JsonObject> data = Arrays.asList(
        gson.fromJson(
"{\"id\": 0, \"vector\": [-0.619954382375778, 0.4479436794798608, -0.17493894838751745, -0.4248030059917294, -0.8648452746018911], \"title\": \"Artificial Intelligence in Real Life\", \"issue\": \"\vol.12\"}"
, JsonObject.class),
        gson.fromJson(
"{\"id\": 1, \"vector\": [0.4762662251462588, -0.6942502138717026, -0.4490002642657902, -0.628696575798281, 0.9660395877041965], \"title\": \"Hollow Man\", \"issue\": \"vol.19\"}"
, JsonObject.class),
        gson.fromJson(
"{\"id\": 2, \"vector\": [-0.8864122635045097, 0.9260170474445351, 0.801326976181461, 0.6383943392381306, 0.7563037341572827], \"title\": \"Treasure Hunt in Missouri\", \"issue\": \"vol.12\"}"
, JsonObject.class),
);
UpsertReq
upsertReq
=
UpsertReq.builder()
        .collectionName(
"my_collection"
)
        .data(data)
        .build();
UpsertResp
upsertResp
=
client.upsert(upsertReq);
System.out.println(upsertResp);
// Output:
//
// UpsertResp(upsertCnt=3)
const
{
MilvusClient
,
DataType
} =
require
(
"@zilliz/milvus2-sdk-node"
)
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

data = [
    {
id
:
0
,
vector
: [-
0.619954382375778
,
0.4479436794798608
, -
0.17493894838751745
, -
0.4248030059917294
, -
0.8648452746018911
],
title
:
"Artificial Intelligence in Real Life"
,
issue
:
"vol.12"
},
    {
id
:
1
,
vector
: [
0.4762662251462588
, -
0.6942502138717026
, -
0.4490002642657902
, -
0.628696575798281
,
0.9660395877041965
],
title
:
"Hollow Man"
,
issue
:
"vol.19"
},
    {
id
:
2
,
vector
: [-
0.8864122635045097
,
0.9260170474445351
,
0.801326976181461
,
0.6383943392381306
,
0.7563037341572827
],
title
:
"Treasure Hunt in Missouri"
,
issue
:
"vol.12"
},
]

res =
await
client.
upsert
({
collection_name
:
"my_collection"
,
data
: data,
})
console
.
log
(res.
upsert_cnt
)
// Output
//
// 3
//
import
(
"context"
"fmt"
"github.com/milvus-io/milvus/client/v2/column"
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

titleColumn := column.NewColumnString(
"title"
, []
string
{
"Artificial Intelligence in Real Life"
,
"Hollow Man"
,
"Treasure Hunt in Missouri"
, 
})

issueColumn := column.NewColumnString(
"issue"
, []
string
{
"vol.12"
,
"vol.19"
,
"vol.12"
})

_, err = client.Upsert(ctx, milvusclient.NewColumnBasedInsertOption(
"my_collection"
).
    WithInt64Column(
"id"
, []
int64
{
0
,
1
,
2
,
3
,
4
,
5
,
6
,
7
,
8
,
9
}).
    WithFloatVectorColumn(
"vector"
,
5
, [][]
float32
{
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
},
        {
0.19886812562848388
,
0.06023560599112088
,
0.6976963061752597
,
0.2614474506242501
,
0.838729485096104
},
        {
0.43742130801983836
,
-0.5597502546264526
,
0.6457887650909682
,
0.7894058910881185
,
0.20785793220625592
},
    }).
    WithColumns(titleColumn, issueColumn),
)
if
err !=
nil
{
    fmt.Println(err.Error())
// handle err
}
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
/v2/vectordb/entities/upsert"
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
    "data": [
        {"id": 0, "vector": [0.3580376395471989, -0.6023495712049978, 0.18414012509913835, -0.26286205330961354, 0.9029438446296592], "title": "Artificial Intelligence in Real Life", "issue": "vol.12"},
        {"id": 1, "vector": [0.19886812562848388, 0.06023560599112088, 0.6976963061752597, 0.2614474506242501, 0.838729485096104], "title": "Hollow Man", "issue": "vol.19"},
        {"id": 2, "vector": [0.43742130801983836, -0.5597502546264526, 0.6457887650909682, 0.7894058910881185, 0.20785793220625592], "title": "Treasure Hunt in Missouri", "issue": "vol.12"},
],
    "collectionName": "my_collection"
}'
# {
#     "code": 0,
#     "data": {
#         "upsertCount": 3,
#         "upsertIds": [
#             0,
#             1,
#             2,
#         ]
#     }
# }
向上插入分区中的实体
您还可以将实体上载到指定的分区中。以下代码片段假定你的 Collection 中有一个名为
PartitionA
的分区。
如果分区中存在三个实体，它们将被请求中包含的实体覆盖。
Python
Java
NodeJS
Go
cURL
data=[
    {
"id"
:
10
,
"vector"
: [
0.06998888224297328
,
0.8582816610326578
, -
0.9657938677934292
,
0.6527905683627726
, -
0.8668460657158576
],
"title"
:
"Layour Design Reference"
,
"issue"
:
"vol.34"
},
    {
"id"
:
11
,
"vector"
: [
0.6060703043917468
, -
0.3765080534566074
, -
0.7710758854987239
,
0.36993888322346136
,
0.5507513364206531
],
"title"
:
"Doraemon and His Friends"
,
"issue"
:
"vol.2"
},
    {
"id"
:
12
,
"vector"
: [-
0.9041813104515337
, -
0.9610546012461163
,
0.20033003106083358
,
0.11842506351635174
,
0.8327356724591011
],
"title"
:
"Pikkachu and Pokemon"
,
"issue"
:
"vol.12"
},
]

res = client.upsert(
    collection_name=
"my_collection"
,
    data=data,
    partition_name=
"partitionA"
)
print
(res)
# Output
# {'upsert_count': 3}
import
io.milvus.v2.service.vector.request.UpsertReq;
import
io.milvus.v2.service.vector.response.UpsertResp;
Gson
gson
=
new
Gson
();
List<JsonObject> data = Arrays.asList(
        gson.fromJson(
"{\"id\": 10, \"vector\": [0.06998888224297328, 0.8582816610326578, -0.9657938677934292, 0.6527905683627726, -0.8668460657158576], \"title\": \"Layour Design Reference\", \"issue\": \"vol.34\"}"
, JsonObject.class),
        gson.fromJson(
"{\"id\": 11, \"vector\": [0.6060703043917468, -0.3765080534566074, -0.7710758854987239, 0.36993888322346136, 0.5507513364206531], \"title\": \"Doraemon and His Friends\", \"issue\": \"vol.2\"}"
, JsonObject.class),
        gson.fromJson(
"{\"id\": 12, \"vector\": [-0.9041813104515337, -0.9610546012461163, 0.20033003106083358, 0.11842506351635174, 0.8327356724591011], \"title\": \"Pikkachu and Pokemon\", \"issue\": \"vol.12\"}"
, JsonObject.class),
);
UpsertReq
upsertReq
=
UpsertReq.builder()
        .collectionName(
"my_collection"
)
        .partitionName(
"partitionA"
)
        .data(data)
        .build();
UpsertResp
upsertResp
=
client.upsert(upsertReq);
System.out.println(upsertResp);
// Output:
//
// UpsertResp(upsertCnt=3)
const
{
MilvusClient
,
DataType
} =
require
(
"@zilliz/milvus2-sdk-node"
)
// 6. Upsert data in partitions
data = [
    {
id
:
10
,
vector
: [
0.06998888224297328
,
0.8582816610326578
, -
0.9657938677934292
,
0.6527905683627726
, -
0.8668460657158576
],
title
:
"Layour Design Reference"
,
issue
:
"vol.34"
},
    {
id
:
11
,
vector
: [
0.6060703043917468
, -
0.3765080534566074
, -
0.7710758854987239
,
0.36993888322346136
,
0.5507513364206531
],
title
:
"Doraemon and His Friends"
,
issue
:
"vol.2"
},
    {
id
:
12
,
vector
: [-
0.9041813104515337
, -
0.9610546012461163
,
0.20033003106083358
,
0.11842506351635174
,
0.8327356724591011
],
title
:
"Pikkachu and Pokemon"
,
issue
:
"vol.12"
},
]

res =
await
client.
upsert
({
collection_name
:
"my_collection"
,
data
: data,
partition_name
:
"partitionA"
})
console
.
log
(res.
upsert_cnt
)
// Output
//
// 3
//
titleColumn = column.NewColumnString(
"title"
, []
string
{
"Layour Design Reference"
,
"Doraemon and His Friends"
,
"Pikkachu and Pokemon"
, 
})
issueColumn = column.NewColumnString(
"issue"
, []
string
{
"vol.34"
,
"vol.2"
,
"vol.12"
, 
})

_, err = client.Upsert(ctx, milvusclient.NewColumnBasedInsertOption(
"my_collection"
).
    WithPartition(
"partitionA"
).
    WithInt64Column(
"id"
, []
int64
{
10
,
11
,
12
,
13
,
14
,
15
,
16
,
17
,
18
,
19
}).
    WithFloatVectorColumn(
"vector"
,
5
, [][]
float32
{
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
},
        {
0.19886812562848388
,
0.06023560599112088
,
0.6976963061752597
,
0.2614474506242501
,
0.838729485096104
},
        {
0.43742130801983836
,
-0.5597502546264526
,
0.6457887650909682
,
0.7894058910881185
,
0.20785793220625592
},
    }).
    WithColumns(titleColumn, issueColumn),
)
if
err !=
nil
{
    fmt.Println(err.Error())
// handle err
}
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
/v2/vectordb/entities/upsert"
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
    "data": [
        {"id": 10, "vector": [0.06998888224297328, 0.8582816610326578, -0.9657938677934292, 0.6527905683627726, -0.8668460657158576], "title": "Layour Design Reference", "issue": "vol.34"},
        {"id": 11, "vector": [0.6060703043917468, -0.3765080534566074, -0.7710758854987239, 0.36993888322346136, 0.5507513364206531], "title": "Doraemon and His Friends", "issue": "vol.2"},
        {"id": 12, "vector": [-0.9041813104515337, -0.9610546012461163, 0.20033003106083358, 0.11842506351635174, 0.8327356724591011], "title": "Pikkachu and Pokemon", "issue": "vol.12"},
    ],
    "collectionName": "my_collection",
    "partitionName": "partitionA"
}'
# {
#     "code": 0,
#     "data": {
#         "upsertCount": 3,
#         "upsertIds": [
#             10,
#             11,
#             12,
#         ]
#     }
# }
在合并模式下倒插实体
Compatible with Milvus v2.6.2+
下面的代码示例演示了如何通过部分更新来倒插实体。只提供需要更新的字段及其新值，以及显式部分更新标记。
在下面的示例中，upsert 请求中指定的实体的
issue
字段将更新为请求中包含的值。
在合并模式下执行 upsert 时，请确保请求中涉及的实体具有相同的字段集。假设有两个或更多实体要进行upsert，如以下代码片段所示，它们必须包含相同的字段，以防止出现错误并保持数据完整性。
Python
Java
Go
NodeJS
cURL
data=[
    {
"id"
:
1
,
"issue"
:
"vol.14"
},
    {
"id"
:
2
,
"issue"
:
"vol.7"
}
]

res = client.upsert(
    collection_name=
"my_collection"
,
    data=data,
    partial_update=
True
)
print
(res)
# Output
# {'upsert_count': 2}
JsonObject
row1
=
new
JsonObject
();
row1.addProperty(
"id"
,
1
);
row1.addProperty(
"issue"
,
"vol.14"
);
JsonObject
row2
=
new
JsonObject
();
row2.addProperty(
"id"
,
2
);
row2.addProperty(
"issue"
,
"vol.7"
);
UpsertReq
upsertReq
=
UpsertReq.builder()
        .collectionName(
"my_collection"
)
        .data(Arrays.asList(row1, row2))
        .partialUpdate(
true
)
        .build();
UpsertResp
upsertResp
=
client.upsert(upsertReq);
System.out.println(upsertResp);
// Output:
//
// UpsertResp(upsertCnt=2)
pkColumn := column.NewColumnInt64(
"id"
, []
int64
{
1
,
2
})
issueColumn = column.NewColumnString(
"issue"
, []
string
{
"vol.17"
,
"vol.7"
,
})

_, err = client.Upsert(ctx, milvusclient.NewColumnBasedInsertOption(
"my_collection"
).
    WithColumns(pkColumn, issueColumn).
    WithPartialUpdate(
true
),
)
if
err !=
nil
{
    fmt.Println(err.Error())
// handle err
}
const
data=[
    {
"id"
:
1
,
"issue"
:
"vol.14"
},
    {
"id"
:
2
,
"issue"
:
"vol.7"
}
];
const
res =
await
client.
upsert
({
collection_name
:
"my_collection"
,
    data,
partial_update
:
true
});
console
.
log
(res)
// Output
//
// 2
//
export
CLUSTER_ENDPOINT=
"http://localhost:19530"
export
TOKEN=
"root:Milvus"
export
COLLECTION_NAME=
"my_collection"
export
UPSERT_DATA=
'[
  {
    "id": 1,
    "issue": "vol.14"
  },
  {
    "id": 2,
    "issue": "vol.7"
  }
]'
curl -X POST
"http://localhost:19530/v2/vectordb/entities/upsert"
\
  -H
"Content-Type: application/json"
\
  -H
"Authorization: Bearer
${TOKEN}
"
\
  -d
"{
    \"collectionName\": \"
${COLLECTION_NAME}
\",
    \"data\":
${UPSERT_DATA}
,
    \"partialUpdate\": true
  }"
# {
#     "code": 0,
#     "data": {
#         "upsertCount": 2,
#         "upsertIds": [
#              3,
#             12,
#         ]
#     }
# }