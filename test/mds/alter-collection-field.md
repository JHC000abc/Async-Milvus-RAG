更改 Collections 字段
您可以更改 Collections 字段的属性，以更改列约束或执行更严格的数据完整性规则。
每个 Collection 只包含一个主字段。一旦在创建 Collections 时设置，就不能更改主字段或改变其属性。
每个 Collection 只能有一个 Partition Key。一旦在创建 Collections 时设置，就不能更改分区键。
更改 VarChar 字段
VarChar 字段有一个名为
max_length
的属性，用于限制字段值可包含的最大字符数。您可以更改
max_length
属性。
下面的示例假定 Collections 有一个名为
varchar
的 VarChar 字段，并设置了它的
max_length
属性。
Python
Java
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

client.alter_collection_field(
    collection_name=
"my_collection"
,
    field_name=
"varchar"
,
    field_params={
"max_length"
:
1024
}
)
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.service.collection.request.*;
ConnectConfig
config
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
(config);

client.alterCollectionField(AlterCollectionFieldReq.builder()
        .collectionName(
"my_collection"
)
        .fieldName(
"varchar"
)
        .property(
"max_length"
,
"1024"
)
        .build());
NodeJS
Go
cURL
await
client.
alterCollectionFieldProperties
({
collection_name
:
LOAD_COLLECTION_NAME
,
field_name
:
'varchar'
,
properties
: {
max_length
:
1024
},
});
import
(
"context"
"fmt"
"github.com/milvus-io/milvus/client/v2/entity"
"github.com/milvus-io/milvus/client/v2/milvusclient"
"github.com/milvus-io/milvus/pkg/v2/common"
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

err = client.AlterCollectionFieldProperty(ctx, milvusclient.NewAlterCollectionFieldPropertiesOption(
"my_collection"
,
"varchar"
).WithProperty(common.MaxLengthKey,
1024
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
# restful
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/collections/fields/alter_properties"
\
--header
"Authorization: Bearer
${TOKEN}
"
\
--header
"Content-Type: application/json"
\
--data
"{
    "
collectionName
": "
my_collection
",
    "
field_name
": "
varchar
",
    "
properties
": {
        "
max_length
": "
1024
"
    }
}"
更改 ARRAY 字段
数组字段有两个属性，即
element_type
和
max_capacity
。前者决定数组中元素的数据类型，后者限制数组中元素的最大数量。您只能更改
max_capacity
属性。
下面的示例假定 Collections 有一个名为
array
的数组字段，并设置了它的
max_capacity
属性。
Python
Java
NodeJS
Go
cURL
client.alter_collection_field(
    collection_name=
"my_collection"
,
    field_name=
"array"
,
    field_params={
"max_capacity"
:
64
}
)
client.alterCollectionField(AlterCollectionFieldReq.builder()
        .collectionName(
"my_collection"
)
        .fieldName(
"array"
)
        .property(
"max_capacity"
,
"64"
)
        .build());
await
client.
alterCollectionFieldProperties
({
collection_name
:
"my_collection"
,
field_name
:
'array'
,
properties
: {
max_capacity
:
64
}
});
err = client.AlterCollectionFieldProperty(ctx, milvusclient.NewAlterCollectionFieldPropertiesOption(
"my_collection"
,
"array"
).WithProperty(common.MaxCapacityKey,
64
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
# restful
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/collections/fields/alter_properties"
\
--header
"Authorization: Bearer
${TOKEN}
"
\
--header
"Content-Type: application/json"
\
--data
"{
    "
collectionName
": "
my_collection
",
    "
field_name
": "
array
",
    "
properties
": {
        "
max_capacity
": "
64
"
    }
}"
更改字段级 mmap 设置
内存映射（Mmap）可实现对磁盘上大型文件的直接内存访问，允许 Milvus 在内存和硬盘中同时存储索引和数据。这种方法有助于根据访问频率优化数据放置策略，在不影响搜索性能的情况下扩大 Collections 的存储容量。
下面的示例假定 Collections 有一个名为
doc_chunk
的字段，并设置其
mmap_enabled
属性。
Python
Java
NodeJS
Go
cURL
client.alter_collection_field(
    collection_name=
"my_collection"
,
    field_name=
"doc_chunk"
,
    field_params={
"mmap.enabled"
:
True
}
)
client.alterCollectionField(AlterCollectionFieldReq.builder()
        .collectionName(
"my_collection"
)
        .fieldName(
"doc_chunk"
)
        .property(
"mmap.enabled"
,
"True"
)
        .build());
await
client.
alterCollectionProperties
({
collection_name
:
"my_collection"
,
field_name
:
'doc_chunk'
,
properties
: {
'mmap.enabled'
:
true
, 
  }
});
err = client.AlterCollectionFieldProperty(ctx, milvusclient.NewAlterCollectionFieldPropertiesOption(
"my_collection"
,
"doc_chunk"
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
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/collections/fields/alter_properties"
\
--header
"Authorization: Bearer
${TOKEN}
"
\
--header
"Content-Type: application/json"
\
--data
"{
    "
collectionName
": "
my_collection
",
    "
field_name
": "
doc_chunk
",
    "
properties
": {
        "
mmap.enabled
": True
    }
}"