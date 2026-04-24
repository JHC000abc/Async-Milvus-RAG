管理分区
分区是一个 Collection 的子集。每个分区与其父集合共享相同的数据结构，但只包含集合中的一个数据子集。本页将帮助你了解如何管理分区。
分区概述
创建一个 Collection 时，Milvus 也会在该 Collection 中创建一个名为
_default 的
分区。如果不添加其他分区，所有插入到 Collections 中的实体都会进入默认分区，所有搜索和查询也都在默认分区内进行。
您可以添加更多分区，并根据特定条件将实体插入其中。这样就可以限制在某些分区内进行搜索和查询，从而提高搜索性能。
一个 Collections 最多可以有 1,024 个分区。
Partition Key
功能是基于分区的搜索优化，允许 Milvus 根据特定标量字段中的值将实体分配到不同的分区中。该功能有助于实现面向分区的多租户，并提高搜索性能。
本页将不讨论此功能。要了解更多信息，请参阅
使用 Partition Key
。
列出分区
创建 Collections 时，Milvus 还会在该 Collections 中创建一个名为
_default 的
分区。您可以按以下方式列出 Collections 中的分区。
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

res = client.list_partitions(
    collection_name=
"my_collection"
)
print
(res)
# Output
#
# ["_default"]
import
io.milvus.v2.service.partition.request.ListPartitionsReq;
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
java.util.*;
String
CLUSTER_ENDPOINT
=
"http://localhost:19530"
;
String
TOKEN
=
"root:Milvus"
;
// 1. Connect to Milvus server
ConnectConfig
connectConfig
=
ConnectConfig.builder()
        .uri(CLUSTER_ENDPOINT)
        .token(TOKEN)
        .build();
MilvusClientV2
client
=
new
MilvusClientV2
(connectConfig);
ListPartitionsReq
listPartitionsReq
=
ListPartitionsReq.builder()
        .collectionName(
"my_collection"
)
        .build();

List<String> partitionNames = client.listPartitions(listPartitionsReq);
System.out.println(partitionNames);
// Output:
// [_default]
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
let
res =
await
client.
listPartitions
({
collection_name
:
"my_collection"
})
console
.
log
(res);
// Output
// ["_default"]
import
(
"context"
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

partitionNames, err := client.ListPartitions(ctx, milvusclient.NewListPartitionOption(
"my_collection"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}

fmt.Println(partitionNames)
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
/v2/vectordb/partitions/list"
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
    "collectionName": "my_collection"
}'
# {
#     "code": 0,
#     "data": [
#         "_default"
#     ]
# }
创建分区
您可以向 Collection 添加更多分区，并根据特定条件向这些分区插入实体。
Python
Java
NodeJS
Go
cURL
client.create_partition(
    collection_name=
"my_collection"
,
    partition_name=
"partitionA"
)

res = client.list_partitions(
    collection_name=
"my_collection"
)
print
(res)
# Output
#
# ["_default", "partitionA"]
import
io.milvus.v2.service.partition.request.CreatePartitionReq;
CreatePartitionReq
createPartitionReq
=
CreatePartitionReq.builder()
        .collectionName(
"my_collection"
)
        .partitionName(
"partitionA"
)
        .build();

client.createPartition(createPartitionReq);
ListPartitionsReq
listPartitionsReq
=
ListPartitionsReq.builder()
        .collectionName(
"my_collection"
)
        .build();

List<String> partitionNames = client.listPartitions(listPartitionsReq);
System.out.println(partitionNames);
// Output:
// [_default, partitionA]
await
client.
createPartition
({
collection_name
:
"my_collection"
,
partition_name
:
"partitionA"
})

res =
await
client.
listPartitions
({
collection_name
:
"my_collection"
})
console
.
log
(res)
// Output
// ["_default", "partitionA"]
import
(
"fmt"
client
"github.com/milvus-io/milvus/client/v2/milvusclient"
)

ctx, cancel := context.WithCancel(context.Background())
defer
cancel()

err = client.CreatePartition(ctx, milvusclient.NewCreatePartitionOption(
"my_collection"
,
"partitionA"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}

partitionNames, err := client.ListPartitions(ctx, milvusclient.NewListPartitionOption(
"my_collection"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}

fmt.Println(partitionNames)
// Output
// ["_default", "partitionA"]
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
/v2/vectordb/partitions/create"
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
    "partitionName": "partitionA"
}'
# {
#     "code": 0,
#     "data": {}
# }
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/partitions/list"
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
    "collectionName": "my_collection"
}'
# {
#     "code": 0,
#     "data": [
#         "_default",
#         "partitionA"
#     ]
# }
检查特定分区
以下代码片段演示了如何检查特定 Collections 中是否存在分区。
Python
Java
NodeJS
Go
cURL
res = client.has_partition(
    collection_name=
"my_collection"
,
    partition_name=
"partitionA"
)
print
(res)
# Output
#
# True
import
io.milvus.v2.service.partition.request.HasPartitionReq;
HasPartitionReq
hasPartitionReq
=
HasPartitionReq.builder()
        .collectionName(
"my_collection"
)
        .partitionName(
"partitionA"
)
        .build();
Boolean
hasPartitionRes
=
client.hasPartition(hasPartitionReq);
System.out.println(hasPartitionRes);
// Output:
// true
res =
await
client.
hasPartition
({
collection_name
:
"my_collection"
,
partition_name
:
"partitionA"
})
console
.
log
(res.
value
)
// Output
// true
result, err := client.HasPartition(ctx, milvusclient.NewHasPartitionOption(
"my_collection"
,
"partitionA"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}

fmt.Println(result)
// Output:
// true
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
/v2/vectordb/partitions/has"
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
    "partitionName": "partitionA"
}'
# {
#     "code": 0,
#     "data": {
#        "has": true
#     }
# }
加载和释放分区
您可以分别加载或释放一个或多个分区。
加载分区
可以分别加载集合中的特定分区。值得注意的是，如果集合中有未加载的分区，则集合的加载状态会保持未加载状态。
Python
Java
NodeJS
Go
cURL
client.load_partitions(
    collection_name=
"my_collection"
,
    partition_names=[
"partitionA"
]
)

res = client.get_load_state(
    collection_name=
"my_collection"
,
    partition_name=
"partitionA"
)
print
(res)
# Output
#
# {
#     "state": "<LoadState: Loaded>"
# }
import
io.milvus.v2.service.partition.request.LoadPartitionsReq;
import
io.milvus.v2.service.collection.request.GetLoadStateReq;
LoadPartitionsReq
loadPartitionsReq
=
LoadPartitionsReq.builder()
        .collectionName(
"my_collection"
)
        .partitionNames(Collections.singletonList(
"partitionA"
))
        .build();

client.loadPartitions(loadPartitionsReq);
GetLoadStateReq
getLoadStateReq
=
GetLoadStateReq.builder()
        .collectionName(
"my_collection"
)
        .partitionName(
"partitionA"
)
        .build();
Boolean
getLoadStateRes
=
client.getLoadState(getLoadStateReq);
System.out.println(getLoadStateRes);
// True
await
client.
loadPartitions
({
collection_name
:
"my_collection"
,
partition_names
: [
"partitionA"
]
})

res =
await
client.
getLoadState
({
collection_name
:
"my_collection"
,
partition_name
:
"partitionA"
})
console
.
log
(res)
// Output
//
// LoadStateLoaded
//
task, err := client.LoadPartitions(ctx, milvusclient.NewLoadPartitionsOption(
"my_collection"
,
"partitionA"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
// sync wait collection to be loaded
err = task.Await(ctx)
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}

state, err := client.GetLoadState(ctx, milvusclient.NewGetLoadStateOption(
"my_collection"
,
"partitionA"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(state)
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
/v2/vectordb/partitions/load"
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
    "partitionNames": ["partitionA"]
}'
# {
#     "code": 0,
#     "data": {}
# }
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/collections/get_load_state"
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
    "partitionNames": ["partitionA"]
}'
# {
#     "code": 0,
#     "data": {
#         "loadProgress": 100,
#         "loadState": "LoadStateLoaded",
#         "message": ""
#     }
# }
释放分区
您还可以释放特定分区。
Python
Java
NodeJS
Go
cURL
client.release_partitions(
    collection_name=
"my_collection"
,
    partition_names=[
"partitionA"
]
)

res = client.get_load_state(
    collection_name=
"my_collection"
,
    partition_name=
"partitionA"
)
print
(res)
# Output
#
# {
#     "state": "<LoadState: NotLoaded>"
# }
import
io.milvus.v2.service.partition.request.ReleasePartitionsReq;
ReleasePartitionsReq
releasePartitionsReq
=
ReleasePartitionsReq.builder()
        .collectionName(
"my_collection"
)
        .partitionNames(Collections.singletonList(
"partitionA"
))
        .build();

client.releasePartitions(releasePartitionsReq);
GetLoadStateReq
getLoadStateReq
=
GetLoadStateReq.builder()
        .collectionName(
"my_collection"
)
        .partitionName(
"partitionA"
)
        .build();
Boolean
getLoadStateRes
=
client.getLoadState(getLoadStateReq);
System.out.println(getLoadStateRes);
// False
await
client.
releasePartitions
({
collection_name
:
"my_collection"
,
partition_names
: [
"partitionA"
]
})

res =
await
client.
getLoadState
({
collection_name
:
"my_collection"
,
partition_name
:
"partitionA"
})
console
.
log
(res)
// Output
//
// LoadStateNotLoaded
//
err = client.ReleasePartitions(ctx, milvusclient.NewReleasePartitionsOptions(
"my_collection"
,
"partitionA"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}

state, err := client.GetLoadState(ctx, milvusclient.NewGetLoadStateOption(
"my_collection"
,
"partitionA"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(state)
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
/v2/vectordb/partitions/release"
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
    "partitionNames": ["partitionA"]
}'
# {
#     "code": 0,
#     "data": {}
# }
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/collections/get_load_state"
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
    "partitionNames": ["partitionA"]
}'
# {
#     "code": 0,
#     "data": {
#         "loadProgress": 0,
#         "loadState": "LoadStateNotLoaded",
#         "message": ""
#     }
# }
分区内的数据操作符
插入和删除实体
您可以在特定操作符中执行插入、向上插入和删除操作。有关详情，请参阅
将实体插入分区
将实体倒插入分区
从分区删除实体
搜索和查询
可以在特定分区内进行搜索和查询。详情请参阅
在分区内进行 ANN 搜索
在分区内进行元数据过滤
删除分区
您可以丢弃不再需要的分区。在丢弃分区之前，请确保该分区已被释放。
Python
Java
NodeJS
Go
cURL
client.release_partitions(
    collection_name=
"my_collection"
,
    partition_names=[
"partitionA"
]
)

client.drop_partition(
    collection_name=
"my_collection"
,
    partition_name=
"partitionA"
)

res = client.list_partitions(
    collection_name=
"my_collection"
)
print
(res)
# ["_default"]
import
io.milvus.v2.service.partition.request.DropPartitionReq;
import
io.milvus.v2.service.partition.request.ReleasePartitionsReq;
import
io.milvus.v2.service.partition.request.ListPartitionsReq;
ReleasePartitionsReq
releasePartitionsReq
=
ReleasePartitionsReq.builder()
        .collectionName(
"my_collection"
)
        .partitionNames(Collections.singletonList(
"partitionA"
))
        .build();

client.releasePartitions(releasePartitionsReq);
DropPartitionReq
dropPartitionReq
=
DropPartitionReq.builder()
        .collectionName(
"my_collection"
)
        .partitionName(
"partitionA"
)
        .build();

client.dropPartition(dropPartitionReq);
ListPartitionsReq
listPartitionsReq
=
ListPartitionsReq.builder()
        .collectionName(
"my_collection"
)
        .build();

List<String> partitionNames = client.listPartitions(listPartitionsReq);
System.out.println(partitionNames);
// Output:
// [_default]
await
client.
releasePartitions
({
collection_name
:
"my_collection"
,
partition_names
: [
"partitionA"
]
})
await
client.
dropPartition
({
collection_name
:
"my_collection"
,
partition_name
:
"partitionA"
})

res =
await
client.
listPartitions
({
collection_name
:
"my_collection"
})
console
.
log
(res)
// Output
// ["_default"]
err = client.ReleasePartitions(ctx, milvusclient.NewReleasePartitionsOptions(
"my_collection"
,
"partitionA"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}

err = client.DropPartition(ctx, milvusclient.NewDropPartitionOption(
"my_collection"
,
"partitionA"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}

partitionNames, err := client.ListPartitions(ctx, milvusclient.NewListPartitionOption(
"my_collection"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(partitionNames)
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
/v2/vectordb/partitions/release"
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
    "partitionNames": ["partitionA"]
}'
# {
#     "code": 0,
#     "data": {}
# }
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/partitions/drop"
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
    "partitionName": "partitionA"
}'
# {
#     "code": 0,
#     "data": {}
# }
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/partitions/list"
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
    "collectionName": "my_collection"
}'
# {
#     "code": 0,
#     "data": [
#         "_default"
#     ]
# }