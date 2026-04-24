删除实体
您可以通过筛选条件或主键删除不再需要的实体。
通过筛选条件删除实体
批量删除共享某些属性的多个实体时，可以使用过滤表达式。下面的示例代码使用
in
操作符批量删除了所有
颜色
字段设置为
红色
和
紫色的
实体。你也可以使用其他操作符来构建符合你要求的过滤表达式。有关过滤表达式的更多信息，请参阅《
过滤详解》
。
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

res = client.delete(
    collection_name=
"quick_setup"
,
filter
=
"color in ['red_7025', 'purple_4976]"
)
print
(res)
# Output
# {'delete_count': 2}
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.service.vector.request.DeleteReq;
import
io.milvus.v2.service.vector.response.DeleteResp;
ilvusClientV2
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
DeleteResp
deleteResp
=
client.delete(DeleteReq.builder()
        .collectionName(
"quick_setup"
)
        .filter(
"color in ['red_7025', 'purple_4976]"
)
        .build());
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
// 7. Delete entities
res =
await
client.
delete
({
collection_name
:
"quick_setup"
,
filter
:
"color in ['red_7025', 'purple_4976]"
})
console
.
log
(res.
delete_cnt
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

_, err = client.Delete(ctx, milvusclient.NewDeleteOption(
"quick_setup"
).WithExpr(
"color in ['red_7025', 'purple_4976']"
))
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
/v2/vectordb/entities/delete"
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
    "collectionName": "quick_setup",
    "filter": "color in [\"red_7025\", \"purple_4976\"]"
}'
通过主键删除实体
在大多数情况下，主键唯一标识一个实体。你可以通过在删除请求中设置实体的主键来删除实体。下面的示例代码演示了如何删除主键为
18
和
19
的两个实体。
Python
Java
NodeJS
Go
cURL
res = client.delete(
    collection_name=
"quick_setup"
,
ids=[
18
,
19
]
)
print
(res)
# Output
# {'delete_count': 2}
import
io.milvus.v2.service.vector.request.DeleteReq;
import
io.milvus.v2.service.vector.response.DeleteResp;
import
java.util.Arrays;
DeleteResp
deleteResp
=
client.delete(DeleteReq.builder()
        .collectionName(
"quick_setup"
)
        .ids(Arrays.asList(
18
,
19
))
        .build());
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

res =
await
client.
delete
({
collection_name
:
"quick_setup"
,
ids
: [
18
,
19
]
})
console
.
log
(res.
delete_cnt
)
// Output
//
// 2
//
_, err = client.Delete(ctx, milvusclient.NewDeleteOption(
"quick_setup"
).
    WithInt64IDs(
"id"
, []
int64
{
18
,
19
}))
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
/v2/vectordb/entities/delete"
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
    "collectionName": "quick_setup",
    "filter": "id in [18, 19]"
}'
## {"code":0,"cost":0,"data":{}}
从分区中删除实体
您还可以删除存储在特定分区中的实体。以下代码片段假定您的 Collection 中有一个名为
PartitionA
的分区。
Python
Java
NodeJS
Go
cURL
res = client.delete(
    collection_name=
"quick_setup"
,
    ids=[
18
,
19
],
    partition_name=
"partitionA"
)
print
(res)
# Output
# {'delete_count': 2}
import
io.milvus.v2.service.vector.request.DeleteReq;
import
io.milvus.v2.service.vector.response.DeleteResp;
import
java.util.Arrays;
DeleteResp
deleteResp
=
client.delete(DeleteReq.builder()
        .collectionName(
"quick_setup"
)
        .ids(Arrays.asList(
18
,
19
))
        .partitionName(
"partitionA"
)
        .build());
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

res =
await
client.
delete
({
collection_name
:
"quick_setup"
,
ids
: [
18
,
19
],
partition_name
:
"partitionA"
})
console
.
log
(res.
delete_cnt
)
// Output
//
// 2
//
_, err = client.Delete(ctx, milvusclient.NewDeleteOption(
"quick_setup"
).
    WithInt64IDs(
"id"
, []
int64
{
18
,
19
}).
    WithPartition(
"partitionA"
))
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
/v2/vectordb/entities/delete"
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
    "collectionName": "quick_setup",
    "partitionName": "partitionA",
    "filter": "id in [18, 19]"
}'
# {
#     "code": 0,
#     "cost": 0,
#     "data": {}
# }