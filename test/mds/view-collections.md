查看收藏集
您可以获取当前连接的数据库中所有 Collections 的名称列表，并查看特定 Collections 的详细信息。
列出收藏集
下面的示例演示了如何获取当前连接的数据库中所有集合的名称列表。
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
MilvusClient, DataType

client = MilvusClient(
    uri=
"http://localhost:19530"
,
    token=
"root:Milvus"
)

res = client.list_collections()
print
(res)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.service.collection.response.ListCollectionsResp;
ConnectConfig
connectConfig
=
ConnectConfig.builder()
        .uri(
"http://localhost:19530"
)
        .token(
"root:Milvus"
)
        .build();
MilvusClientV2
client
=
new
MilvusClientV2
(connectConfig);
ListCollectionsResp
resp
=
client.listCollections();
System.out.println(resp.getCollectionNames());
import
{
MilvusClient
}
from
'@zilliz/milvus2-sdk-node'
;
const
client =
new
MilvusClient
({
address
:
'localhost:19530'
,
token
:
'root:Milvus'
});
const
collections =
await
client.
listCollections
();
console
.
log
(collections);
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
token :=
"root:Milvus"
client, err := milvusclient.New(ctx, &milvusclient.ClientConfig{
    Address: milvusAddr,
    APIKey:  token,
})
if
err !=
nil
{
    fmt.Println(err.Error())
// handle err
}
defer
client.Close(ctx)

collectionNames, err := client.ListCollections(ctx, milvusclient.NewListCollectionOption())
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}

fmt.Println(collectionNames)
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/collections/list"
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
如果您已经创建了一个名为
quick_setup
的 Collection，则上述示例的结果应类似于下面的内容。
[
"quick_setup"
]
描述 Collection
您还可以获取特定 Collection 的详细信息。下面的示例假定您已经创建了名为 quick_setup 的 Collection。
Python
Java
NodeJS
Go
cURL
res = client.describe_collection(
    collection_name=
"quick_setup"
)
print
(res)
import
io.milvus.v2.service.collection.request.DescribeCollectionReq;
import
io.milvus.v2.service.collection.response.DescribeCollectionResp;
DescribeCollectionReq
request
=
DescribeCollectionReq.builder()
        .collectionName(
"quick_setup"
)
        .build();
DescribeCollectionResp
resp
=
client.describeCollection(request);
System.out.println(resp);
const
res =
await
client.
describeCollection
({
collection_name
:
"quick_setup"
});
console
.
log
(res);
collection, err := client.DescribeCollection(ctx, milvusclient.NewDescribeCollectionOption(
"quick_setup"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle err
}

fmt.Println(collection)
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/collections/describe"
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
    "collectionName": "quick_setup"
}'
上述示例的结果应类似于下面的内容。
{
    'collection_name': 'quick_setup', 
    'auto_id': False, 
    'num_shards': 1, 
    'description': '', 
    'fields': [
        {
            'field_id': 100, 
            'name': 'id', 
            'description': '', 
            'type': <DataType.INT64: 5>, 
            'params': {}, 
            'is_primary': True
        }, 
        {
            'field_id': 101, 
            'name': 'vector', 
            'description': '', 
            'type': <DataType.FLOAT_VECTOR: 101>, 
            'params': {'dim': 768}
        }
    ], 
    'functions': [], 
    'aliases': [], 
    'collection_id': 456909630285026300, 
    'consistency_level': 2, 
    'properties': {}, 
    'num_partitions': 1, 
    'enable_dynamic_field': True
}