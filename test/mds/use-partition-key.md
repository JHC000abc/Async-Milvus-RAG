使用分区密钥
分区关键字是一种基于分区的搜索优化解决方案。通过指定特定标量字段作为 Partition Key，并在搜索过程中根据 Partition Key 指定过滤条件，可以将搜索范围缩小到多个分区，从而提高搜索效率。本文将介绍如何使用 Partition Key 以及相关注意事项。
概述
在 Milvus 中，你可以使用分区来实现数据隔离，并通过将搜索范围限制在特定分区来提高搜索性能。如果选择手动管理分区，可以在 Collections 中创建最多 1,024 个分区，并根据特定规则将实体插入这些分区，这样就可以通过限制在特定数量的分区内进行搜索来缩小搜索范围。
Milvus 引入了分区密钥，供你在数据隔离中重复使用分区，以克服在集合中创建分区数量的限制。创建 Collections 时，可以使用标量字段作为 Partition Key。一旦集合准备就绪，Milvus 就会在集合内创建指定数量的分区。收到插入的实体后，Milvus 会使用实体的分区密钥值计算一个哈希值，根据哈希值和集合的
partitions_num
属性执行求模操作，以获得目标分区 ID，并将实体存储到目标分区中。
分区与分区 Key
下图说明了在启用或未启用分区密钥功能的情况下，Milvus 如何处理 Collections 中的搜索请求。
如果禁用了 Partition Key，Milvus 会在 Collections 中搜索与查询向量最相似的实体。如果知道哪个分区包含最相关的结果，就可以缩小搜索范围。
如果启用了分区关键字，Milvus 会根据搜索过滤器中指定的分区关键字值确定搜索范围，并只扫描分区内匹配的实体。
有无分区密钥
使用分区密钥
要使用分区密钥，您需要
设置分区密钥
、
设置要创建的分区数量
（可选），以及
根据分区密钥创建过滤条件
。
设置分区密钥
要将标量字段指定为分区密钥，需要在添加标量字段时将其
is_partition_key
属性设置为
true
。
将标量字段设置为 Partition Key 时，字段值不能为空或 null。
Python
Java
Go
NodeJS
cURL
from
pymilvus
import
(
    MilvusClient, DataType
)

client = MilvusClient(
    uri=
"http://localhost:19530"
,
    token=
"root:Milvus"
)

schema = client.create_schema()

schema.add_field(field_name=
"id"
,
    datatype=DataType.INT64,
    is_primary=
True
)
    
schema.add_field(field_name=
"vector"
,
    datatype=DataType.FLOAT_VECTOR,
    dim=
5
)
# Add the partition key
schema.add_field(
    field_name=
"my_varchar"
, 
    datatype=DataType.VARCHAR, 
    max_length=
512
,
is_partition_key=
True
,
)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.common.DataType;
import
io.milvus.v2.service.collection.request.AddFieldReq;
import
io.milvus.v2.service.collection.request.CreateCollectionReq;
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
// Create schema
CreateCollectionReq.
CollectionSchema
schema
=
client.createSchema();

schema.addField(AddFieldReq.builder()
        .fieldName(
"id"
)
        .dataType(DataType.Int64)
        .isPrimaryKey(
true
)
        .build());

schema.addField(AddFieldReq.builder()
        .fieldName(
"vector"
)
        .dataType(DataType.FloatVector)
        .dimension(
5
)
        .build());
// Add the partition key
schema.addField(AddFieldReq.builder()
        .fieldName(
"my_varchar"
)
        .dataType(DataType.VarChar)
        .maxLength(
512
)
.isPartitionKey(
true
)
.build());
import
(
"context"
"fmt"
"github.com/milvus-io/milvus/client/v2/column"
"github.com/milvus-io/milvus/client/v2/entity"
"github.com/milvus-io/milvus/client/v2/index"
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

schema := entity.NewSchema().WithDynamicFieldEnabled(
false
)
schema.WithField(entity.NewField().
    WithName(
"id"
).
    WithDataType(entity.FieldTypeInt64).
    WithIsPrimaryKey(
true
),
).WithField(entity.NewField().
    WithName(
"my_varchar"
).
    WithDataType(entity.FieldTypeVarChar).
    WithIsPartitionKey(
true
).
    WithMaxLength(
512
),
).WithField(entity.NewField().
    WithName(
"vector"
).
    WithDataType(entity.FieldTypeFloatVector).
    WithDim(
5
),
)
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
// 3. Create a collection in customized setup mode
// 3.1 Define fields
const
fields = [
    {
name
:
"my_varchar"
,
data_type
:
DataType
.
VarChar
,
max_length
:
512
,
is_partition_key
:
true
}
]
export
schema=
'{
        "autoId": true,
        "enabledDynamicField": false,
        "fields": [
            {
                "fieldName": "id",
                "dataType": "Int64",
                "isPrimary": true
            },
            {
                "fieldName": "vector",
                "dataType": "FloatVector",
                "elementTypeParams": {
                    "dim": "5"
                }
            },
            {
                "fieldName": "my_varchar",
                "dataType": "VarChar",
                "isPartitionKey": true,
                "elementTypeParams": {
                    "max_length": 512
                }
            }
        ]
    }'
设置分区编号
当你指定一个 Collections 中的标量字段作为 Partition Key 时，Milvus 会自动在 Collections 中创建 16 个分区。在接收到一个实体时，Milvus 会根据这个实体的 Partition Key 值选择一个分区，并将实体存储在分区中，从而导致部分或全部分区持有不同 Partition Key 值的实体。
您还可以确定与 Collections 一起创建的分区数量。只有将标量字段指定为 Partition Key 时，这种方法才有效。
Python
Java
Go
NodeJS
cURL
client.create_collection(
    collection_name=
"my_collection"
,
    schema=schema,
num_partitions=
128
)
import
io.milvus.v2.service.collection.request.CreateCollectionReq;
CreateCollectionReq
createCollectionReq
=
CreateCollectionReq.builder()
                .collectionName(
"my_collection"
)
                .collectionSchema(schema)
                .numPartitions(
128
)
                .build();
        client.createCollection(createCollectionReq);
err = client.CreateCollection(ctx,
    milvusclient.NewCreateCollectionOption(
"my_collection"
, schema).
        WithNumPartitions(
128
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
await
client.
create_collection
({
collection_name
:
"my_collection"
,
schema
: schema,
num_partitions
:
128
})
export
params=
'{
    "partitionsNum": 128
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
创建过滤条件
在启用分区关键字功能的 Collections 中进行 ANN 搜索时，需要在搜索请求中包含涉及分区关键字的过滤表达式。在过滤表达式中，你可以将 Partition Key 的值限制在特定范围内，这样 Milvus 就会将搜索范围限制在相应的分区内。
在执行删除操作时，建议加入指定单一分区键的过滤表达式，以实现更高效的删除。这种方法将删除操作限制在特定分区内，减少了压缩过程中的写入放大，节省了用于压缩和索引的资源。
下面的示例演示了基于 Partition Key 的过滤，它基于一个特定的 Partition Key 值和一组 Partition Key 值。
Python
Java
Go
NodeJS
cURL
# Filter based on a single partition key value, or
filter
=
'partition_key == "x" && <other conditions>'
# Filter based on multiple partition key values
filter
=
'partition_key in ["x", "y", "z"] && <other conditions>'
// Filter based on a single partition key value, or
String
filter
=
"partition_key == 'x' && <other conditions>"
;
// Filter based on multiple partition key values
String
filter
=
"partition_key in ['x', 'y', 'z'] && <other conditions>"
;
// Filter based on a single partition key value, or
filter =
"partition_key == 'x' && <other conditions>"
// Filter based on multiple partition key values
filter =
"partition_key in ['x', 'y', 'z'] && <other conditions>"
// Filter based on a single partition key value, or
const
filter =
'partition_key == "x" && <other conditions>'
// Filter based on multiple partition key values
const
filter =
'partition_key in ["x", "y", "z"] && <other conditions>'
# Filter based on a single partition key value, or
export
filter=
'partition_key == "x" && <other conditions>'
# Filter based on multiple partition key values
export
filter=
'partition_key in ["x", "y", "z"] && <other conditions>'
必须将
partition_key
替换为指定为分区密钥的字段名称。
使用 Partition Key 隔离
在多租户场景中，可以将与租户身份相关的标量字段指定为分区密钥，并根据此标量字段中的特定值创建过滤器。为了进一步提高类似情况下的搜索性能，Milvus 引入了分区密钥隔离功能。
分区密钥隔离
如上图所示，Milvus 根据分区键值对实体进行分组，并为每个分组创建单独的索引。收到搜索请求后，Milvus 会根据过滤条件中指定的 Partition Key 值定位索引，并将搜索范围限制在索引所包含的实体内，从而避免在搜索过程中扫描不相关的实体，大大提高搜索性能。
启用 "分区密钥隔离 "后，必须在基于分区密钥的过滤条件中只包含一个特定值，这样 Milvus 才能在匹配的索引所包含的实体内限制搜索范围。
目前，分区密钥隔离功能只适用于索引类型设置为 HNSW 的搜索。
启用分区密钥隔离功能
以下代码示例演示了如何启用分区键隔离。
Python
Java
Go
NodeJS
cURL
client.create_collection(
    collection_name=
"my_collection"
,
    schema=schema,
properties={
"partitionkey.isolation"
:
True
}
)
import
io.milvus.v2.service.collection.request.CreateCollectionReq;

Map<String, String> properties =
new
HashMap
<>();
properties.put(
"partitionkey.isolation"
,
"true"
);
CreateCollectionReq
createCollectionReq
=
CreateCollectionReq.builder()
        .collectionName(
"my_collection"
)
        .collectionSchema(schema)
        .properties(properties)
        .build();
client.createCollection(createCollectionReq);
err = client.CreateCollection(ctx,
    milvusclient.NewCreateCollectionOption(
"my_collection"
, schema).
        WithProperty(
"partitionkey.isolation"
,
true
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
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
"partitionkey.isolation"
:
true
}
})
export
params=
'{
    "partitionKeyIsolation": true
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
启用分区密钥隔离后，仍可按照
设置分区编号
中的说明设置分区密钥和分区数量。请注意，基于 Partition Key 的过滤器应只包含特定的 Partition Key 值。