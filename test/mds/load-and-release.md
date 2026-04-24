加载和释放
加载集合是在集合中进行相似性搜索和查询的前提。本页主要介绍加载和释放 Collections 的步骤。
加载 Collections
加载 Collections 时，Milvus 会将索引文件和所有字段的原始数据加载到内存中，以便快速响应搜索和查询。在载入 Collections 后插入的实体会自动编入索引并载入。
以下代码片段演示了如何加载 Collections。
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
# 7. Load the collection
client.load_collection(
    collection_name=
"my_collection"
)

res = client.get_load_state(
    collection_name=
"my_collection"
)
print
(res)
# Output
#
# {
#     "state": "<LoadState: Loaded>"
# }
import
io.milvus.v2.service.collection.request.LoadCollectionReq;
import
io.milvus.v2.service.collection.request.GetLoadStateReq;
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
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
// 6. Load the collection
LoadCollectionReq
loadCollectionReq
=
LoadCollectionReq.builder()
        .collectionName(
"my_collection"
)
        .build();

client.loadCollection(loadCollectionReq);
// 7. Get load state of the collection
GetLoadStateReq
loadStateReq
=
GetLoadStateReq.builder()
        .collectionName(
"my_collection"
)
        .build();
Boolean
res
=
client.getLoadState(loadStateReq);
System.out.println(res);
// Output:
// true
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
// 7. Load the collection
res =
await
client.
loadCollection
({
collection_name
:
"my_collection"
})
console
.
log
(res.
error_code
)
// Output
//
// Success
//
res =
await
client.
getLoadState
({
collection_name
:
"my_collection"
})
console
.
log
(res.
state
)
// Output
//
// LoadStateLoaded
//
import
(
"context"
"fmt"
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
    
loadTask, err := client.LoadCollection(ctx, milvusclient.NewLoadCollectionOption(
"my_collection"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle err
}
// sync wait collection to be loaded
err = loadTask.Await(ctx)
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}

state, err := client.GetLoadState(ctx, milvusclient.NewGetLoadStateOption(
"my_collection"
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
/v2/vectordb/collections/load"
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
    "collectionName": "my_collection"
}'
# {
#     "code": 0,
#     "data": {
#         "loadProgress": 100,
#         "loadState": "LoadStateLoaded",
#         "message": ""
#     }
# }
加载特定字段
Milvus 可以只加载搜索和查询所涉及的字段，从而减少内存使用并提高搜索性能。
部分 Collections 加载目前还处于测试阶段，不建议在生产中使用。
以下代码片段假定您创建了一个名为
my_collection
的 Collection，且 Collection 中有两个名为
my_id
和
my_vector 的
字段。
Python
Java
NodeJS
Go
cURL
client.load_collection(
    collection_name=
"my_collection"
,
load_fields=[
"my_id"
,
"my_vector"
]
# Load only the specified fields
skip_load_dynamic_field=
True
# Skip loading the dynamic field
)

res = client.get_load_state(
    collection_name=
"my_collection"
)
print
(res)
# Output
#
# {
#     "state": "<LoadState: Loaded>"
# }
// 6. Load the collection
LoadCollectionReq
loadCollectionReq
=
LoadCollectionReq.builder()
        .collectionName(
"my_collection"
)
        .loadFields(Arrays.asList(
"my_id"
,
"my_vector"
))
        .build();

client.loadCollection(loadCollectionReq);
// 7. Get load state of the collection
GetLoadStateReq
loadStateReq
=
GetLoadStateReq.builder()
        .collectionName(
"my_collection"
)
        .build();
Boolean
res
=
client.getLoadState(loadStateReq);
System.out.println(res);
await
client.
load_collection
({
collection_name
:
"my_collection"
,
load_fields
: [
"my_id"
,
"my_vector"
],
// Load only the specified fields
skip_load_dynamic_field
:
true
//Skip loading the dynamic field
});
const
loadState = client.
getCollectionLoadState
({
collection_name
:
"my_collection"
,
})
console
.
log
(loadState);
loadTask, err := client.LoadCollection(ctx, milvusclient.NewLoadCollectionOption(
"my_collection"
).
        WithLoadFields(
"my_id"
,
"my_vector"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
// sync wait collection to be loaded
err = loadTask.Await(ctx)
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}

state, err := client.GetLoadState(ctx, milvusclient.NewGetLoadStateOption(
"my_collection"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(state)
# REST
Not support yet
如果您选择加载特定字段，值得注意的是，只有
load_fields
中包含的字段才能用作搜索和查询中的过滤器和输出字段。您应始终在
load_fields
中包含主字段和至少一个向量字段的名称。
您还可以使用
skip_load_dynamic_field
来确定是否加载动态字段。动态字段是一个保留的 JSON 字段，名为
$meta
，以键值对的形式保存所有非 Schema 定义的字段及其值。加载动态字段时，字段中的所有键都会被加载，并可用于过滤和输出。如果动态字段中的所有键都不参与元数据过滤和输出，请将
skip_load_dynamic_field
设置为
True
。
要在 Collections 加载后加载更多字段，需要先释放 Collections，以避免因索引更改而提示可能的错误。
释放 Collections
搜索和查询是内存密集型操作。为节约成本，建议释放当前不使用的 Collection。
下面的代码片段演示了如何释放一个 Collection。
Python
Java
NodeJS
Go
cURL
# 8. Release the collection
client.release_collection(
    collection_name=
"my_collection"
)

res = client.get_load_state(
    collection_name=
"my_collection"
)
print
(res)
# Output
#
# {
#     "state": "<LoadState: NotLoad>"
# }
import
io.milvus.v2.service.collection.request.ReleaseCollectionReq;
// 8. Release the collection
ReleaseCollectionReq
releaseCollectionReq
=
ReleaseCollectionReq.builder()
        .collectionName(
"my_collection"
)
        .build();

client.releaseCollection(releaseCollectionReq);
GetLoadStateReq
loadStateReq
=
GetLoadStateReq.builder()
        .collectionName(
"my_collection"
)
        .build();
Boolean
res
=
client.getLoadState(loadStateReq);
System.out.println(res);
// Output:
// false
// 8. Release the collection
res =
await
client.
releaseCollection
({
collection_name
:
"my_collection"
})
console
.
log
(res.
error_code
)
// Output
//
// Success
//
res =
await
client.
getLoadState
({
collection_name
:
"my_collection"
})
console
.
log
(res.
state
)
// Output
//
// LoadStateNotLoad
//
err = client.ReleaseCollection(ctx, milvusclient.NewReleaseCollectionOption(
"my_collection"
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
/v2/vectordb/collections/release"
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
    "collectionName": "my_collection"
}'
# {
#     "code": 0,
#     "data": {
#         "loadProgress": 0,
#         "loadState": "LoadStateNotLoaded",
#         "message": ""
#     }
# }