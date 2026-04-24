删除 Collections
如果不再需要某个 Collection，您可以删除该 Collection。
示例
以下代码片段假定您有一个名为
my_collection
的 Collection。
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

client.drop_collection(
    collection_name=
"my_collection"
)
import
io.milvus.v2.service.collection.request.DropCollectionReq;
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
DropCollectionReq
dropQuickSetupParam
=
DropCollectionReq.builder()
        .collectionName(
"my_collection"
)
        .build();

client.dropCollection(dropQuickSetupParam);
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
// 10. Drop the collection
res =
await
client.
dropCollection
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
import
(
"context"
"fmt"
"log"
"github.com/milvus-io/milvus/client/v2/milvusclient"
)

ctx, cancel := context.WithCancel(context.Background())
defer
cancel()

milvusAddr :=
"127.0.0.1:19530"
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
// handle error
}
defer
client.Close(ctx)

err = client.DropCollection(ctx, milvusclient.NewDropCollectionOption(
"my_collection"
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
/v2/vectordb/collections/drop"
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