创建 Collections
您可以通过定义 Schema、索引参数、度量类型以及创建时是否加载来创建一个 Collection。本页将介绍如何从头开始创建 Collections。
集合概述
Collection 是一个二维表，具有固定的列和变化的行。每列代表一个字段，每行代表一个实体。要实现这样的结构化数据管理，需要一个 Schema。要插入的每个实体都必须符合 Schema 中定义的约束条件。
你可以确定 Collections 的方方面面，包括其 Schema、索引参数、度量类型，以及是否在创建时加载，以确保集合完全满足你的要求。
要创建一个 Collection，您需要
创建 Schema
设置索引参数
（可选）
创建 Collections
创建 Schema
Schema 定义了 Collections 的数据结构。创建 Collections 时，需要根据自己的要求设计模式。有关详细信息，请参阅
Schema Explained
。
以下代码片段创建了一个模式，其中包含启用的 Dynamic Field 和三个必填字段，分别命名为
my_id
、
my_vector
和
my_varchar
。
您可以为任何标量字段设置默认值，并使其可归零。有关详情，请参阅
Nullable & Default
。
Python
Java
NodeJS
Go
cURL
# 3. Create a collection in customized setup mode
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
# 3.1. Create schema
schema = MilvusClient.create_schema(
    auto_id=
False
,
    enable_dynamic_field=
True
,
)
# 3.2. Add fields to schema
schema.add_field(field_name=
"my_id"
, datatype=DataType.INT64, is_primary=
True
)
schema.add_field(field_name=
"my_vector"
, datatype=DataType.FLOAT_VECTOR, dim=
5
)
schema.add_field(field_name=
"my_varchar"
, datatype=DataType.VARCHAR, max_length=
512
)
import
io.milvus.v2.common.DataType;
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.service.collection.request.AddFieldReq;
import
io.milvus.v2.service.collection.request.CreateCollectionReq;
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
// 3. Create a collection in customized setup mode
// 3.1 Create schema
CreateCollectionReq.
CollectionSchema
schema
=
client.createSchema();
// 3.2 Add fields to schema
schema.addField(AddFieldReq.builder()
        .fieldName(
"my_id"
)
        .dataType(DataType.Int64)
        .isPrimaryKey(
true
)
        .autoID(
false
)
        .build());

schema.addField(AddFieldReq.builder()
        .fieldName(
"my_vector"
)
        .dataType(DataType.FloatVector)
        .dimension(
5
)
        .build());

schema.addField(AddFieldReq.builder()
        .fieldName(
"my_varchar"
)
        .dataType(DataType.VarChar)
        .maxLength(
512
)
        .build());
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
"my_id"
,
data_type
:
DataType
.
Int64
,
is_primary_key
:
true
,
auto_id
:
false
},
    {
name
:
"my_vector"
,
data_type
:
DataType
.
FloatVector
,
dim
:
5
},
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
}
]
import
(
"context"
"fmt"
"github.com/milvus-io/milvus/client/v2/entity"
"github.com/milvus-io/milvus/client/v2/index"
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

schema := entity.NewSchema().WithDynamicFieldEnabled(
true
).
        WithField(entity.NewField().WithName(
"my_id"
).WithIsAutoID(
false
).WithDataType(entity.FieldTypeInt64).WithIsPrimaryKey(
true
)).
        WithField(entity.NewField().WithName(
"my_vector"
).WithDataType(entity.FieldTypeFloatVector).WithDim(
5
)).
        WithField(entity.NewField().WithName(
"my_varchar"
).WithDataType(entity.FieldTypeVarChar).WithMaxLength(
512
))
export
schema=
'{
        "autoId": false,
        "enabledDynamicField": false,
        "fields": [
            {
                "fieldName": "my_id",
                "dataType": "Int64",
                "isPrimary": true
            },
            {
                "fieldName": "my_vector",
                "dataType": "FloatVector",
                "elementTypeParams": {
                    "dim": "5"
                }
            },
            {
                "fieldName": "my_varchar",
                "dataType": "VarChar",
                "elementTypeParams": {
                    "max_length": 512
                }
            }
        ]
    }'
(可选）设置索引参数
在特定字段上创建索引可加快对该字段的搜索。索引记录了 Collections 中实体的顺序。如以下代码片段所示，您可以使用
metric_type
和
index_type
为 Milvus 选择适当的方式为字段建立索引，并测量向量嵌入之间的相似性。
在 Milvus 上，您可以使用
AUTOINDEX
作为所有向量场的索引类型，并根据需要使用
COSINE
、
L2
和
IP
中的一种作为度量类型。
如上述代码片段所示，您需要为向量场同时设置索引类型和度量类型，而只需为标量场设置索引类型。索引对于向量字段是强制性的，建议您在筛选条件中经常使用的标量字段上创建索引。
有关详情，请参阅
索引向量
字段
和
索引标量字段
。
Python
Java
NodeJS
Go
cURL
# 3.3. Prepare index parameters
index_params = client.prepare_index_params()
# 3.4. Add indexes
index_params.add_index(
    field_name=
"my_id"
,
    index_type=
"AUTOINDEX"
)

index_params.add_index(
    field_name=
"my_vector"
, 
    index_type=
"AUTOINDEX"
,
    metric_type=
"COSINE"
)
import
io.milvus.v2.common.IndexParam;
import
java.util.*;
// 3.3 Prepare index parameters
IndexParam
indexParamForIdField
=
IndexParam.builder()
        .fieldName(
"my_id"
)
        .indexType(IndexParam.IndexType.AUTOINDEX)
        .build();
IndexParam
indexParamForVectorField
=
IndexParam.builder()
        .fieldName(
"my_vector"
)
        .indexType(IndexParam.IndexType.AUTOINDEX)
        .metricType(IndexParam.MetricType.COSINE)
        .build();

List<IndexParam> indexParams =
new
ArrayList
<>();
indexParams.add(indexParamForIdField);
indexParams.add(indexParamForVectorField);
// 3.2 Prepare index parameters
const
index_params = [{
field_name
:
"my_id"
,
index_type
:
"AUTOINDEX"
},{
field_name
:
"my_vector"
,
index_type
:
"AUTOINDEX"
,
metric_type
:
"COSINE"
}]
import
(
"github.com/milvus-io/milvus/client/v2/entity"
"github.com/milvus-io/milvus/client/v2/index"
"github.com/milvus-io/milvus/client/v2/milvusclient"
)

collectionName :=
"customized_setup_1"
indexOptions := []milvusclient.CreateIndexOption{
    milvusclient.NewCreateIndexOption(collectionName,
"my_vector"
, index.NewAutoIndex(entity.COSINE)),
    milvusclient.NewCreateIndexOption(collectionName,
"my_id"
, index.NewAutoIndex(entity.COSINE)),
}
export
indexParams=
'[
        {
            "fieldName": "my_vector",
            "metricType": "COSINE",
            "indexName": "my_vector",
            "indexType": "AUTOINDEX"
        },
        {
            "fieldName": "my_id",
            "indexName": "my_id",
            "indexType": "AUTOINDEX"
        }
    ]'
创建 Collections
如果创建了带有索引参数的 Collection，Milvus 会在创建时自动加载该 Collection。在这种情况下，索引参数中提到的所有字段都会被索引。
以下代码片段演示了如何创建带索引参数的 Collections 并检查其加载状态。
Python
Java
NodeJS
Go
cURL
# 3.5. Create a collection with the index loaded simultaneously
client.create_collection(
    collection_name=
"customized_setup_1"
,
    schema=schema,
    index_params=index_params
)

res = client.get_load_state(
    collection_name=
"customized_setup_1"
)
print
(res)
# Output
#
# {
#     "state": "<LoadState: Loaded>"
# }
import
io.milvus.v2.service.collection.request.CreateCollectionReq;
import
io.milvus.v2.service.collection.request.GetLoadStateReq;
// 3.4 Create a collection with schema and index parameters
CreateCollectionReq
customizedSetupReq1
=
CreateCollectionReq.builder()
        .collectionName(
"customized_setup_1"
)
        .collectionSchema(schema)
        .indexParams(indexParams)
        .build();

client.createCollection(customizedSetupReq1);
// 3.5 Get load state of the collection
GetLoadStateReq
customSetupLoadStateReq1
=
GetLoadStateReq.builder()
        .collectionName(
"customized_setup_1"
)
        .build();
Boolean
loaded
=
client.getLoadState(customSetupLoadStateReq1);
System.out.println(loaded);
// Output:
// true
// 3.3 Create a collection with fields and index parameters
res =
await
client.
createCollection
({
collection_name
:
"customized_setup_1"
,
fields
: fields,
index_params
: index_params,
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
"customized_setup_1"
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
err = client.CreateCollection(ctx, milvusclient.NewCreateCollectionOption(
"customized_setup_1"
, schema).
    WithIndexOptions(indexOptions...))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(
"collection created"
)
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
    \"collectionName\": \"customized_setup_1\",
    \"schema\":
$schema
,
    \"indexParams\":
$indexParams
}"
您也可以创建不带任何索引参数的 Collections，然后再添加索引参数。在这种情况下，Milvus 不会在创建时加载 Collection。.
下面的代码片段演示了如何创建一个不带索引的 Collection，创建时 Collection 的加载状态仍为未加载。
Python
Java
NodeJS
Go
cURL
# 3.6. Create a collection and index it separately
client.create_collection(
    collection_name=
"customized_setup_2"
,
    schema=schema,
)

res = client.get_load_state(
    collection_name=
"customized_setup_2"
)
print
(res)
# Output
#
# {
#     "state": "<LoadState: NotLoad>"
# }
// 3.6 Create a collection and index it separately
CreateCollectionReq
customizedSetupReq2
=
CreateCollectionReq.builder()
    .collectionName(
"customized_setup_2"
)
    .collectionSchema(schema)
    .build();

client.createCollection(customizedSetupReq2);
GetLoadStateReq
customSetupLoadStateReq2
=
GetLoadStateReq.builder()
        .collectionName(
"customized_setup_2"
)
        .build();
Boolean
loaded
=
client.getLoadState(customSetupLoadStateReq2);
System.out.println(loaded);
// Output:
// false
// 3.4 Create a collection and index it seperately
res =
await
client.
createCollection
({
collection_name
:
"customized_setup_2"
,
fields
: fields,
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
"customized_setup_2"
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
err = client.CreateCollection(ctx, milvusclient.NewCreateCollectionOption(
"customized_setup_2"
, schema))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(
"collection created"
)

state, err := client.GetLoadState(ctx, milvusclient.NewGetLoadStateOption(
"customized_setup_2"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(state.State)
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
    \"collectionName\": \"customized_setup_2\",
    \"schema\":
$schema
}"
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
"{
    \"collectionName\": \"customized_setup_2\"
}"
设置集合属性
您可以为要创建的 Collection 设置属性，使其适合您的服务。适用的属性如下。
设置分片数
分片是 Collections 的水平切片，每个分片对应一个数据输入通道。默认情况下，每个 Collections 都有一个分区。您可以在创建 Collections 时指定分片数量，以便更好地适应数据量和工作负载。
作为一般指导原则，在设置分片数量时应考虑以下几点：
数据大小：
通常的做法是每 2 亿个实体设置一个分区。也可以根据总数据量进行估算，例如，计划插入的数据量每 100 GB 就增加一个分区。
流节点利用率：
如果你的 Milvus 实例有多个流节点，建议使用多个分片。这样可以确保数据插入工作量分布在所有可用的流节点上，防止一些节点闲置，而其他节点超负荷工作。
下面的代码片段演示了如何在创建 Collections 时设置分片编号。
Python
Java
NodeJS
Go
cURL
# With shard number
client.create_collection(
    collection_name=
"customized_setup_3"
,
    schema=schema,
num_shards=
1
)
// With shard number
CreateCollectionReq
customizedSetupReq3
=
CreateCollectionReq.builder()
    .collectionName(
"customized_setup_3"
)
    .collectionSchema(collectionSchema)
.numShards(
1
)
.build();
client.createCollection(customizedSetupReq3);
const
createCollectionReq = {
collection_name
:
"customized_setup_3"
,
schema
: schema,
shards_num
:
1
}
err = client.CreateCollection(ctx, milvusclient.NewCreateCollectionOption(
"customized_setup_3"
, schema).WithShardNum(
1
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(
"collection created"
)
export
params=
'{
    "shardsNum": 1
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
    \"collectionName\": \"customized_setup_3\",
    \"schema\":
$schema
,
    \"params\":
$params
}"
启用 mmap
Milvus 默认在所有 Collections 上启用 mmap，允许 Milvus 将原始字段数据映射到内存中，而不是完全加载它们。这样可以减少内存占用，提高 Collections 的容量。有关 mmap 的详细信息，请参阅
使用 mmap
。
Python
Java
NodeJS
Go
纯文本
# With mmap
client.create_collection(
    collection_name=
"customized_setup_4"
,
    schema=schema,
enable_mmap=
False
)
import
io.milvus.param.Constant;
// With MMap
CreateCollectionReq
customizedSetupReq4
=
CreateCollectionReq.builder()
        .collectionName(
"customized_setup_4"
)
        .collectionSchema(schema)
.property(Constant.MMAP_ENABLED,
"false"
)
.build();
client.createCollection(customizedSetupReq4);
client.
create_collection
({
collection_name
:
"customized_setup_4"
,
schema
: schema,
properties
: {
'mmap.enabled'
:
true
,
     },
})
err = client.CreateCollection(ctx, milvusclient.NewCreateCollectionOption(
"customized_setup_4"
, schema).
    WithProperty(common.MmapEnabledKey,
true
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(
"collection created"
)
export
params=
'{
    "mmap.enabled": True
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
    \"collectionName\": \"customized_setup_5\",
    \"schema\":
$schema
,
    \"params\":
$params
}"
设置 Collections TTL
如果需要在特定时间段内删除 Collections 中的数据，可以考虑以秒为单位设置其 Time-To-Live (TTL)。一旦 TTL 超时，Milvus 就会删除 Collection 中的实体。删除是异步的，这表明在删除完成之前，搜索和查询仍然可以进行。
下面的代码片段将 TTL 设置为一天（86400 秒）。建议至少将 TTL 设置为几天。
Python
Java
NodeJS
Go
cURL
# With TTL
client.create_collection(
    collection_name=
"customized_setup_5"
,
    schema=schema,
properties={
"collection.ttl.seconds"
:
86400
}
)
import
io.milvus.param.Constant;
// With TTL
CreateCollectionReq
customizedSetupReq5
=
CreateCollectionReq.builder()
        .collectionName(
"customized_setup_5"
)
        .collectionSchema(schema)
.property(Constant.TTL_SECONDS,
"86400"
)
.build();
client.createCollection(customizedSetupReq5);
const
createCollectionReq = {
collection_name
:
"customized_setup_5"
,
schema
: schema,
properties
: {
"collection.ttl.seconds"
:
86400
}
}
err = client.CreateCollection(ctx, milvusclient.NewCreateCollectionOption(
"customized_setup_5"
, schema).
    WithProperty(common.CollectionTTLConfigKey,
true
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(
"collection created"
)
export
params=
'{
    "ttlSeconds": 86400
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
    \"collectionName\": \"customized_setup_5\",
    \"schema\":
$schema
,
    \"params\":
$params
}"
设置一致性级别
创建 Collections 时，可以为集合中的搜索和查询设置一致性级别。您还可以在特定搜索或查询过程中更改 Collections 的一致性级别。
Python
Java
NodeJS
Go
cURL
# With consistency level
client.create_collection(
    collection_name=
"customized_setup_6"
,
    schema=schema,
consistency_level=
"Bounded"
,
)
import
io.milvus.v2.common.ConsistencyLevel;
// With consistency level
CreateCollectionReq
customizedSetupReq6
=
CreateCollectionReq.builder()
        .collectionName(
"customized_setup_6"
)
        .collectionSchema(schema)
.consistencyLevel(ConsistencyLevel.BOUNDED)
.build();
client.createCollection(customizedSetupReq6);
const
createCollectionReq = {
collection_name
:
"customized_setup_6"
,
schema
: schema,
consistency_level
:
"Bounded"
,
}

client.
createCollection
(createCollectionReq);
err = client.CreateCollection(ctx, milvusclient.NewCreateCollectionOption(
"customized_setup_6"
, schema).
    WithConsistencyLevel(entity.ClBounded))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(
"collection created"
)
export
params=
'{
    "consistencyLevel": "Bounded"
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
    \"collectionName\": \"customized_setup_6\",
    \"schema\":
$schema
,
    \"params\":
$params
}"
有关一致性级别的更多信息，请参阅
一致性
级别。
启用动态字段
Collections 中的动态字段是一个保留的 JavaScript Object Notation (JSON) 字段，名为
$meta
。启用该字段后，Milvus 会将每个实体中携带的所有非 Schema 定义字段及其值作为键值对保存在保留字段中。
有关如何使用动态字段的详细信息，请参阅
动态字段
。