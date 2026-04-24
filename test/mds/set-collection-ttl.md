设置 Collections TTL
数据插入 Collections 后，默认情况下会保留在其中。不过，在某些情况下，你可能希望在一段时间后删除或清理数据。在这种情况下，你可以配置 Collections 的 "生存时间"（TTL）属性，这样一旦 TTL 过期，Milvus 就会自动删除数据。
概览
在数据库中，"有效时间"（TTL）通常用于数据插入或修改后只能保持有效或可访问一段时间的情况。然后，数据会被自动删除。
例如，如果你每天采集数据，但只需要保留 14 天的记录，你可以通过将 Collections 的 TTL 设置为
14 × 24 × 3600 = 1209600
秒，配置 Milvus 自动移除任何比这更早的数据。这样可以确保 Collection 中只保留最近 14 天的数据。
过期的实体不会出现在任何搜索或查询结果中。不过，它们可能会留在存储中，直到随后的数据压缩（应在接下来的 24 小时内进行）。
你可以通过设置 Milvus 配置文件中的
dataCoord.compaction.expiry.tolerance
配置项来控制何时触发数据压缩。
该配置项的默认值为
-1
，表示适用现有的数据压实间隔。不过，如果将其值改为正整数（如
12
），则会在任何实体过期后的指定小时数触发数据压缩。
Milvus Collections 中的 TTL 属性指定为以秒为单位的整数。一旦设定，任何超过 TTL 的数据都将自动从 Collections 中删除。
由于删除过程是异步的，因此一旦指定的 TTL 过期，数据可能不会准确地从搜索结果中删除。相反，可能会有延迟，因为删除取决于垃圾 Collections (GC) 和压缩过程，而这两个过程的时间间隔是不确定的。
设置 TTL
您可以在以下情况下设置 TTL 属性
创建一个 Collections。
更改现有 Collections 的 TTL 属性。
创建 Collections 时设置 TTL
以下代码片段演示了如何在创建 Collection 时设置 TTL 属性。
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
MilvusClient
# With TTL
client.create_collection(
    collection_name=
"my_collection"
,
    schema=schema,
properties={
"collection.ttl.seconds"
:
1209600
}
)
import
io.milvus.v2.service.collection.request.CreateCollectionReq;
import
io.milvus.v2.service.collection.request.AlterCollectionReq;
import
io.milvus.param.Constant;
import
java.util.HashMap;
import
java.util.Map;
// With TTL
CreateCollectionReq
customizedSetupReq
=
CreateCollectionReq.builder()
        .collectionName(
"my_collection"
)
        .collectionSchema(schema)
.property(Constant.TTL_SECONDS,
"1209600"
)
.build();
client.createCollection(customizedSetupReq);
const
createCollectionReq = {
collection_name
:
"my_collection"
,
schema
: schema,
properties
: {
"collection.ttl.seconds"
:
1209600
}
}
err = client.CreateCollection(ctx, milvusclient.NewCreateCollectionOption(
"my_collection"
, schema).
    WithProperty(common.CollectionTTLConfigKey,
1209600
))
//  TTL in seconds
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
export
params=
'{
    "ttlSeconds": 1209600
}'
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
/v2/vectordb/collections/create"
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
"{
    \"collectionName\": \"my_collection\",
    \"schema\":
$schema
,
    \"params\":
$params
}"
为现有 Collection 设置 TTL
以下代码片段演示了如何更改现有 Collection 中的 TTL 属性。
Python
Java
NodeJS
Go
cURL
client.alter_collection_properties(
    collection_name=
"my_collection"
,
    properties={
"collection.ttl.seconds"
:
1209600
}
)
Map<String, String> properties =
new
HashMap
<>();
properties.put(
"collection.ttl.seconds"
,
"1209600"
);
AlterCollectionReq
alterCollectionReq
=
AlterCollectionReq.builder()
        .collectionName(
"my_collection"
)
        .properties(properties)
        .build();

client.alterCollection(alterCollectionReq);
res =
await
client.
alterCollection
({
collection_name
:
"my_collection"
,
properties
: {
"collection.ttl.seconds"
:
1209600
}
})
err = client.AlterCollectionProperties(ctx, milvusclient.NewAlterCollectionPropertiesOption(
"my_collection"
).
    WithProperty(common.CollectionTTLConfigKey,
60
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/collections/alter_properties"
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
"{
    \"collectionName\": \"my_collection\",
    \"properties\": {
        \"collection.ttl.seconds\": 1209600
    }
}"
删除 TTL 设置
如果您决定无限期地保留某个 Collection 中的数据，您只需删除该 Collection 中的 TTL 设置即可。
Python
Java
NodeJS
Go
cURL
client.drop_collection_properties(
    collection_name=
"my_collection"
,
    property_keys=[
"collection.ttl.seconds"
]
)
propertyKeys =
new
String
[
1
]
propertyKeys[
0
] =
"collection.ttl.second"
DropCollectionReq
dropCollectionReq
=
DropCollectionReq.builder()
        .collectionName(
"my_collection"
)
        .propertyKeys(propertyKeys)
        .build();

client.dropCollection(dropCollectionReq);
res =
await
client.
dropCollectionProperties
({
collection_name
:
"my_collection"
,
properties
: [
"collection.ttl.seconds"
]
})
err = client.DropCollectionProperties(ctx, milvusclient.NewDropCollectionPropertiesOption(
"my_collection"
, common.CollectionTTLConfigKey))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/collections/alter_properties"
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
"{
    \"collectionName\": \""
my_collection
"\",
    \"properties\": {
        \"collection.ttl.seconds\": 60
    }
}"