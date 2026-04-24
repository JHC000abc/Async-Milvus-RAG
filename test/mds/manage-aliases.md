管理别名
在 Milvus 中，别名是一个 Collection 的二级可变名称。使用别名提供了一个抽象层，使您可以在不修改应用程序代码的情况下动态切换 Collections。这对于生产环境中的无缝数据更新、A/B 测试和其他操作符特别有用。
本页演示了如何创建、列出、重新分配和删除 Collections 别名。
为什么使用别名？
使用别名的主要好处是将客户端应用程序与特定的物理 Collections 名称分离。
想象一下，你有一个实时应用程序，它查询一个名为
prod_data
的 Collections。当您需要更新底层数据时，可以在不中断服务的情况下执行更新。工作流程如下
创建一个新 Collection
：创建一个新的 Collections，例如
prod_data_v2
。
准备数据
：在
prod_data_v2
中加载新数据并编制索引。
切换别名
：一旦新的 Collections 准备就绪，原子式地将旧 Collections 的别名
prod_data
重新分配给
prod_data_v2
。
您的应用程序将继续向别名
prod_data
发送请求，不会出现停机。这种机制可以实现无缝更新，并简化向量搜索服务的蓝绿部署等操作符。
别名的关键属性：
一个 Collection 可以有多个别名。
一个别名一次只能指向一个 Collections。
处理请求时，Milvus 会首先检查是否存在提供名称的 Collection。如果不存在，它就会检查该名称是否是某个 Collection 的别名。
创建别名
下面的代码片段演示了如何为 Collection 创建别名。
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
# 9. Manage aliases
# 9.1. Create aliases
client.create_alias(
    collection_name=
"my_collection_1"
,
    alias=
"bob"
)

client.create_alias(
    collection_name=
"my_collection_1"
,
    alias=
"alice"
)
import
io.milvus.v2.service.utility.request.CreateAliasReq;
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
// 9. Manage aliases
// 9.1 Create alias
CreateAliasReq
createAliasReq
=
CreateAliasReq.builder()
        .collectionName(
"my_collection_1"
)
        .alias(
"bob"
)
        .build();

client.createAlias(createAliasReq);

createAliasReq = CreateAliasReq.builder()
        .collectionName(
"my_collection_1"
)
        .alias(
"alice"
)
        .build();

client.createAlias(createAliasReq);
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
// 9. Manage aliases
// 9.1 Create aliases
res =
await
client.
createAlias
({
collection_name
:
"my_collection_1"
,
alias
:
"bob"
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
createAlias
({
collection_name
:
"my_collection_1"
,
alias
:
"alice"
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

err = client.CreateAlias(ctx, milvusclient.NewCreateAliasOption(
"my_collection_1"
,
"bob"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}

err = client.CreateAlias(ctx, milvusclient.NewCreateAliasOption(
"my_collection_1"
,
"alice"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
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
/v2/vectordb/aliases/create"
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
    "aliasName": "bob",
    "collectionName": "my_collection_1"
}'
# {
#     "code": 0,
#     "data": {}
# }
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/aliases/create"
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
    "aliasName": "alice",
    "collectionName": "my_collection_1"
}'
# {
#     "code": 0,
#     "data": {}
# }
列出别名
以下代码片段演示了列出分配给特定 Collection 的别名的过程。
Python
Java
NodeJS
Go
cURL
# 9.2. List aliases
res = client.list_aliases(
    collection_name=
"my_collection_1"
)
print
(res)
# Output
#
# {
#     "aliases": [
#         "bob",
#         "alice"
#     ],
#     "collection_name": "my_collection_1",
#     "db_name": "default"
# }
import
io.milvus.v2.service.utility.request.ListAliasesReq;
import
io.milvus.v2.service.utility.response.ListAliasResp;
// 9.2 List alises
ListAliasesReq
listAliasesReq
=
ListAliasesReq.builder()
    .collectionName(
"my_collection_1"
)
    .build();
ListAliasResp
listAliasRes
=
client.listAliases(listAliasesReq);

System.out.println(listAliasRes.getAlias());
// Output:
// [bob, alice]
// 9.2 List aliases
res =
await
client.
listAliases
({
collection_name
:
"my_collection_1"
})
console
.
log
(res.
aliases
)
// Output
//
// [ 'bob', 'alice' ]
//
aliases, err := client.ListAliases(ctx, milvusclient.NewListAliasesOption(
"my_collection_1"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(aliases)
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
/v2/vectordb/aliases/list"
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
'{}'
# {
#     "code": 0,
#     "data": [
#         "bob",
#         "alice"
#     ]
# }
描述别名
以下代码片段详细描述了特定别名，包括分配给该别名的 Collections 名称。
Python
Java
NodeJS
Go
cURL
# 9.3. Describe aliases
res = client.describe_alias(
    alias=
"bob"
)
print
(res)
# Output
#
# {
#     "alias": "bob",
#     "collection_name": "my_collection_1",
#     "db_name": "default"
# }
import
io.milvus.v2.service.utility.request.DescribeAliasReq;
import
io.milvus.v2.service.utility.response.DescribeAliasResp;
// 9.3 Describe alias
DescribeAliasReq
describeAliasReq
=
DescribeAliasReq.builder()
    .alias(
"bob"
)
    .build();
DescribeAliasResp
describeAliasRes
=
client.describeAlias(describeAliasReq);

System.out.println(describeAliasRes);
// Output:
// DescribeAliasResp(collectionName=my_collection_1, alias=bob)
// 9.3 Describe aliases
res =
await
client.
describeAlias
({
collection_name
:
"my_collection_1"
,
alias
:
"bob"
})
console
.
log
(res)
// Output
//
// {
//   status: {
//     extra_info: {},
//     error_code: 'Success',
//     reason: '',
//     code: 0,
//     retriable: false,
//     detail: ''
//   },
//   db_name: 'default',
//   alias: 'bob',
//   collection: 'my_collection_1'
// }
//
alias, err := client.DescribeAlias(ctx, milvusclient.NewDescribeAliasOption(
"bob"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(alias)
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
/v2/vectordb/aliases/describe"
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
    "aliasName": "bob"
}'
# {
#     "code": 0,
#     "data": {
#         "aliasName": "bob",
#         "collectionName": "my_collection_1",
#         "dbName": "default"
#     }
# }
更改别名
您可以将已分配给特定集合的别名重新分配给另一个集合。
Python
Java
NodeJS
Go
cURL
# 9.4 Reassign aliases to other collections
client.alter_alias(
    collection_name=
"my_collection_2"
,
    alias=
"alice"
)

res = client.list_aliases(
    collection_name=
"my_collection_2"
)
print
(res)
# Output
#
# {
#     "aliases": [
#         "alice"
#     ],
#     "collection_name": "my_collection_2",
#     "db_name": "default"
# }
res = client.list_aliases(
    collection_name=
"my_collection_1"
)
print
(res)
# Output
#
# {
#     "aliases": [
#         "bob"
#     ],
#     "collection_name": "my_collection_1",
#     "db_name": "default"
# }
import
io.milvus.v2.service.utility.request.AlterAliasReq;
// 9.4 Reassign alias to other collections
AlterAliasReq
alterAliasReq
=
AlterAliasReq.builder()
        .collectionName(
"my_collection_2"
)
        .alias(
"alice"
)
        .build();

client.alterAlias(alterAliasReq);
ListAliasesReq
listAliasesReq
=
ListAliasesReq.builder()
        .collectionName(
"my_collection_2"
)
        .build();
ListAliasResp
listAliasRes
=
client.listAliases(listAliasesReq);

System.out.println(listAliasRes.getAlias());

listAliasesReq = ListAliasesReq.builder()
        .collectionName(
"my_collection_1"
)
        .build();

listAliasRes = client.listAliases(listAliasesReq);

System.out.println(listAliasRes.getAlias());
// Output:
// [bob]
// 9.4 Reassign aliases to other collections
res =
await
client.
alterAlias
({
collection_name
:
"my_collection_2"
,
alias
:
"alice"
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
listAliases
({
collection_name
:
"my_collection_2"
})
console
.
log
(res.
aliases
)
// Output
//
// [ 'alice' ]
//
res =
await
client.
listAliases
({
collection_name
:
"my_collection_1"
})
console
.
log
(res.
aliases
)
// Output
//
// [ 'bob' ]
//
err = client.AlterAlias(ctx, milvusclient.NewAlterAliasOption(
"alice"
,
"my_collection_2"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}

aliases, err := client.ListAliases(ctx, milvusclient.NewListAliasesOption(
"my_collection_2"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(aliases)

aliases, err = client.ListAliases(ctx, milvusclient.NewListAliasesOption(
"my_collection_1"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(aliases)
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
/v2/vectordb/aliases/alter"
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
    "aliasName": "alice",
    "collectionName": "my_collection_2"
}'
# {
#     "code": 0,
#     "data": {}
# }
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/aliases/describe"
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
    "aliasName": "alice"
}'
# {
#     "code": 0,
#     "data": {
#         "aliasName": "alice",
#         "collectionName": "my_collection_2",
#         "dbName": "default"
#     }
# }
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/aliases/describe"
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
    "aliasName": "bob"
}'
# {
#     "code": 0,
#     "data": {
#         "aliasName": "alice",
#         "collectionName": "my_collection_1",
#         "dbName": "default"
#     }
# }
删除别名
下面的代码片段演示了删除别名的过程。
Python
Java
NodeJS
Go
cURL
# 9.5 Drop aliases
client.drop_alias(
    alias=
"bob"
)

client.drop_alias(
    alias=
"alice"
)
import
io.milvus.v2.service.utility.request.DropAliasReq;
// 9.5 Drop alias
DropAliasReq
dropAliasReq
=
DropAliasReq.builder()
    .alias(
"bob"
)
    .build();

client.dropAlias(dropAliasReq);

dropAliasReq = DropAliasReq.builder()
    .alias(
"alice"
)
    .build();

client.dropAlias(dropAliasReq);
// 9.5 Drop aliases
res =
await
client.
dropAlias
({
alias
:
"bob"
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
dropAlias
({
alias
:
"alice"
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
err = client.DropAlias(ctx, milvusclient.NewDropAliasOption(
"bob"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}

err = client.DropAlias(ctx, milvusclient.NewDropAliasOption(
"alice"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
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
/v2/vectordb/aliases/drop"
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
    "aliasName": "bob"
}'
# {
#     "code": 0,
#     "data": {}
# }
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/aliases/drop"
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
    "aliasName": "alice"
}'
# {
#     "code": 0,
#     "data": {}
# }