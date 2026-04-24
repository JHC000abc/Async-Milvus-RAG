修改 Collections
您可以重命名一个 Collection 或更改其设置。本页主要介绍如何修改 Collections。
重新命名 Collections
您可以按以下方式重命名一个 Collection。
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

client.rename_collection(
    old_name=
"my_collection"
,
    new_name=
"my_new_collection"
)
import
io.milvus.v2.service.collection.request.RenameCollectionReq;
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
RenameCollectionReq
renameCollectionReq
=
RenameCollectionReq.builder()
        .collectionName(
"my_collection"
)
        .newCollectionName(
"my_new_collection"
)
        .build();

client.renameCollection(renameCollectionReq);
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
res =
await
client.
renameCollection
({
oldName
:
"my_collection"
,
newName
:
"my_new_collection"
});
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
// handle error
}
defer
client.Close(ctx)

err = client.RenameCollection(ctx, milvusclient.NewRenameCollectionOption(
"my_collection"
,
"my_new_collection"
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
/v2/vectordb/collections/rename"
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
    "newCollectionName": "my_new_collection"
}'
设置集合属性
创建集合后，您可以修改集合级属性。
支持的属性
属性
说明
collection.ttl.seconds
如果需要在特定时间后删除 Collections 的数据，可考虑设置其生存时间（TTL）（以秒为单位）。一旦 TTL 超时，Milvus 就会删除 Collection 中的所有实体。
删除是异步的，这表明在删除完成之前，搜索和查询仍然可以进行。
详情请参阅
设置 Collections TTL
。
mmap.enabled
内存映射（Mmap）可实现对磁盘上大型文件的直接内存访问，允许 Milvus 在内存和硬盘中同时存储索引和数据。这种方法有助于根据访问频率优化数据放置策略，在不影响搜索性能的情况下扩大 Collections 的存储容量。
有关详情，请参阅
使用 mmap
。
partitionkey.isolation
启用分区密钥隔离后，Milvus 会根据分区密钥值对实体进行分组，并为每个分组创建单独的索引。收到搜索请求后，Milvus 会根据过滤条件中指定的 Partition Key 值定位索引，并将搜索范围限制在索引所包含的实体内，从而避免在搜索过程中扫描不相关的实体，大大提高搜索性能。
有关详情，请参阅
使用 Partition Key Isolation
。
dynamicfield.enabled
为创建时未启用动态字段的 Collections 启用动态字段。启用后，就可以插入带有原始 Schema 中未定义字段的实体。有关详情，请参阅
动态
字段。
allow_insert_auto_id
当为 Collections 启用自动 ID 时，是否允许 Collections 接受用户提供的主键值。
设置为
"true "
时：插入、向上插入和批量导入时，如果存在用户提供的主键，则使用用户提供的主键；否则，将自动生成主键值。
设置为
"false "
时：用户提供的主键值将被拒绝或忽略，主键值始终是自动生成的。默认值为
"false"
。
timezone
在处理对时间敏感的操作（尤其是
TIMESTAMPTZ
字段）时，指定此 Collections 的默认时区。时间戳在内部以 UTC 保存，Milvus 会根据此设置转换值以进行显示和比较。如果设置，Collection 时区会覆盖数据库的默认时区；查询的时区参数可临时覆盖两者。该值必须是有效的
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
例 1：设置 Collections TTL
以下代码片段演示了如何设置 Collections TTL。
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
MilvusClient

client.alter_collection_properties(
    collection_name=
"my_collection"
,
    properties={
"collection.ttl.seconds"
:
60
}
)
import
io.milvus.v2.service.collection.request.AlterCollectionReq;
import
java.util.HashMap;
import
java.util.Map;

Map<String, String> properties =
new
HashMap
<>();
properties.put(
"collection.ttl.seconds"
,
"60"
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
60
}
})
err = client.AlterCollectionProperties(ctx, milvusclient.NewAlterCollectionPropertiesOption(
"my_collection"
).WithProperty(common.CollectionTTLConfigKey,
60
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
'{
    "collectionName": "test_collection",
    "properties": {
        "collection.ttl.seconds": 60
    }
}'
例 2：启用 mmap
以下代码片段演示了如何启用 mmap。
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
MilvusClient

client.alter_collection_properties(
    collection_name=
"my_collection"
,
    properties={
"mmap.enabled"
:
True
}
)
Map<String, String> properties =
new
HashMap
<>();
properties.put(
"mmap.enabled"
,
"True"
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
await
client.
alterCollectionProperties
({
collection_name
:
"my_collection"
,
properties
: {
"mmap.enabled"
:
true
}
});
err = client.AlterCollectionProperties(ctx, milvusclient.NewAlterCollectionPropertiesOption(
"my_collection"
).WithProperty(common.MmapEnabledKey,
true
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
# restful
curl -X POST
"http://localhost:19530/v2/vectordb/collections/alter_properties"
\
  -H
"Content-Type: application/json"
\
  -d
'{
    "collectionName": "my_collection",
    "properties": {
      "mmap.enabled": "true"
    }
  }'
例 3：启用 Partition Key
以下代码片段演示了如何启用分区密钥。
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
MilvusClient

client.alter_collection_properties(
    collection_name=
"my_collection"
,
    properties={
"partitionkey.isolation"
:
True
}
)
Map<String, String> properties =
new
HashMap
<>();
properties.put(
"partitionkey.isolation"
,
"True"
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
await
client.
alterCollectionProperties
({
collection_name
:
"my_collection"
,
properties
: {
"partitionkey.isolation"
:
true
}
});
err = client.AlterCollectionProperties(ctx, milvusclient.NewAlterCollectionPropertiesOption(
"my_collection"
).WithProperty(common.PartitionKeyIsolationKey,
true
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
# restful
curl -X POST
"http://localhost:19530/v2/vectordb/collections/alter_properties"
\
  -H
"Content-Type: application/json"
\
  -H
"Authorization: Bearer <token>"
\
  -d
'{
    "collectionName": "my_collection",
    "properties": {
      "partitionkey.isolation": "true"
    }
  }'
例 4：启用动态字段
以下代码片段演示了如何启用动态字段。
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
MilvusClient

client.alter_collection_properties(
    collection_name=
"my_collection"
,
    properties={
"dynamicfield.enabled"
:
True
}
)
Map<String, String> properties =
new
HashMap
<>();
properties.put(
"dynamicfield.enabled"
,
"True"
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
await
client.
alterCollectionProperties
({
collection_name
:
"my_collection"
,
properties
: {
"dynamicfield.enabled"
:
true
}
});
err = client.AlterCollectionProperties(ctx, milvusclient.NewAlterCollectionPropertiesOption(
"my_collection"
).WithProperty(common.EnableDynamicSchemaKey,
true
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
# restful
curl -X POST
"http://localhost:19530/v2/vectordb/collections/alter_properties"
\
  -H
"Content-Type: application/json"
\
  -H
"Authorization: Bearer <token>"
\
  -d
'{
    "collectionName": "my_collection",
    "properties": {
      "dynamicfield.enabled": "true"
    }
  }'
例 5：启用 allow_insert_auto_id
allow_insert_auto_id
属性允许启用了 AutoID 的 Collections 在插入、上载和批量导入时接受用户提供的主键值。当设置为
"true "
时
，
Milvus
会
使用用户提供的主键值（如果存在），否则
会
自动生成。默认值为
"假"。
下面的示例展示了如何启用
allow_insert_auto_id
：
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
"allow_insert_auto_id"
:
"true"
}
)
# After enabling, inserts with a PK column will use that PK; otherwise Milvus auto-generates.
Map<String, String> properties =
new
HashMap
<>();
properties.put(
"allow_insert_auto_id"
,
"True"
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
await
client.
alterCollectionProperties
({
collection_name
:
"my_collection"
,
properties
: {
"allow_insert_auto_id"
:
true
}
});
err = client.AlterCollectionProperties(ctx, milvusclient.NewAlterCollectionPropertiesOption(
"my_collection"
).WithProperty(common.AllowInsertAutoIDKey,
true
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
# restful
curl -X POST
"http://localhost:19530/v2/vectordb/collections/alter_properties"
\
  -H
"Content-Type: application/json"
\
  -H
"Authorization: Bearer <token>"
\
  -d
'{
    "collectionName": "my_collection",
    "properties": {
      "allow_insert_auto_id": "true"
    }
  }'
例 6：设置 Collections 时区
您可以使用
timezone
属性为您的 Collections 设置默认时区。这将决定集合内所有操作（包括数据插入、查询和结果展示）如何解释和显示与时间相关的数据。
timezone
的值必须是有效的
IANA 时区标识符
，如
Asia/Shanghai
、
America/Chicago
或
UTC
。使用无效或非标准值将导致在修改 Collections 属性时出错。
下面的示例展示了如何将 Collections 时区设置为
亚洲/上海
：
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
"timezone"
:
"Asia/Shanghai"
}
)
Map<String, String> properties =
new
HashMap
<>();
properties.put(
"timezone"
,
"Asia/Shanghai"
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
// js
err = client.AlterCollectionProperties(ctx, milvusclient.NewAlterCollectionPropertiesOption(
"my_collection"
).WithProperty(common.CollectionDefaultTimezone,
true
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
# restful
curl -X POST
"http://localhost:19530/v2/vectordb/collections/alter_properties"
\
  -H
"Content-Type: application/json"
\
  -H
"Authorization: Bearer <token>"
\
  -d
'{
    "collectionName": "my_collection",
    "properties": {
      "timezone": "Asia/Shanghai"
    }
  }'
删除 Collection 属性
您还可以通过删除 Collection 属性来重置该属性，方法如下。
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
client.dropCollectionProperties(DropCollectionPropertiesReq.builder()
        .collectionName(
"my_collection"
)
        .propertyKeys(Collections.singletonList(
"collection.ttl.seconds"
))
        .build());
client.
dropCollectionProperties
({
collection_name
:
"my_collection"
,
properties
: [
'collection.ttl.seconds'
],
});
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
/v2/vectordb/collections/drop_properties"
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
    "propertyKeys": [
        "collection.ttl.seconds"
    ]
}'