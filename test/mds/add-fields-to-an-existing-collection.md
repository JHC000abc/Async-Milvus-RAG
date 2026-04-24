向现有 Collections 添加字段
Compatible with Milvus 2.6.x
Milvus 允许你动态地添加新字段到现有的 Collections 中，使你可以很容易地随着应用需求的变化而发展你的数据 Schema。本指南通过实际例子向你展示如何在不同情况下添加字段。
注意事项
在向 Collections 添加字段之前，请牢记以下要点：
您可以添加标量字段（
INT64
,
VARCHAR
,
FLOAT
,
DOUBLE
等）。向量字段不能添加到现有的 Collections 中。
新字段必须是可归零的（nullable=True），以适应没有新字段值的现有实体。
向已加载的 Collections 添加字段会增加内存使用量。
每个 Collection 的字段总数有最大限制。详情请参阅
Milvus 限制
。
在静态字段中，字段名必须是唯一的。
对于最初未使用
enable_dynamic_field=True
创建的 Collections，不能添加
$meta
字段来启用动态字段功能。
前提条件
本指南假定您拥有
运行中的 Milvus 实例
已安装 Milvus SDK
现有的 Collections
有关
Collections
的创建和基本操作，请参阅我们的创建 Collections。
基本用法
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
MilvusClient, DataType
# Connect to your Milvus server
client = MilvusClient(
    uri=
"http://localhost:19530"
# Replace with your Milvus server URI
)
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.client.ConnectConfig;
ConnectConfig
config
=
ConnectConfig.builder()
        .uri(
"http://localhost:19530"
)
        .build();
MilvusClientV2
client
=
new
MilvusClientV2
(config);
import
{
MilvusClient
}
from
'@zilliz/milvus2-sdk-node'
;
const
milvusClient =
new
MilvusClient
({
address
:
'localhost:19530'
});
// go
# restful
export
CLUSTER_ENDPOINT=
"localhost:19530"
场景 1：快速添加可空字段
扩展 Collections 的最简单方法是添加可归零字段。当您需要为数据快速添加新属性时，这种方法再合适不过了。
Python
Java
NodeJS
Go
cURL
# Add a nullable field to an existing collection
# This operation:
# - Returns almost immediately (non-blocking)
# - Makes the field available for use with minimal delay
# - Sets NULL for all existing entities
client.add_collection_field(
    collection_name=
"product_catalog"
,
    field_name=
"created_timestamp"
,
# Name of the new field to add
data_type=DataType.INT64,
# Data type must be a scalar type
nullable=
True
# Must be True for added fields
# Allows NULL values for existing entities
)
import
io.milvus.v2.service.collection.request.AddCollectionFieldReq;

client.addCollectionField(AddCollectionFieldReq.builder()
        .collectionName(
"product_catalog"
)
        .fieldName(
"created_timestamp"
)
        .dataType(DataType.Int64)
        .isNullable(
true
)
        .build());
await
client.
addCollectionField
({
collection_name
:
'product_catalog'
,
field
: {
name
:
'created_timestamp'
,
dataType
:
'Int64'
,
nullable
:
true
}
});
// go
# restful
curl -X POST
"http://localhost:19530/v2/vectordb/collections/fields/add"
\
  -H
"Content-Type: application/json"
\
  -H
"Authorization: Bearer <token>"
\
  -d
'{
    "collectionName": "product_catalog",
    "schema": {
      "fieldName": "created_timestamp",
      "dataType": "Int64",
      "nullable": true
    }
  }'
预期行为：
现有实体的
新字段为 NULL
新实体
可以有 NULL 或实际值
由于内部 Schema 同步，
字段可用性
几乎立即发生，延迟极小
短暂同步后
可立即查询
Python
Java
NodeJS
Go
cURL
# Example query result
{
'id'
:
1
,
'created_timestamp'
:
None
# New field shows NULL for existing entities
}
// java
// nodejs
{
'id'
:
1
,
'created_timestamp'
:
None
#
New
field shows
NULL
for
existing entities
}
// go
# restful
{
"code"
: 0,
"data"
: {},
"cost"
: 0
}
方案 2：添加带默认值的字段
当您希望现有实体有一个有意义的初始值而不是 NULL 时，可指定默认值。
Python
Java
NodeJS
Go
cURL
# Add a field with default value
# This operation:
# - Sets the default value for all existing entities
# - Makes the field available with minimal delay
# - Maintains data consistency with the default value
client.add_collection_field(
    collection_name=
"product_catalog"
,
    field_name=
"priority_level"
,
# Name of the new field
data_type=DataType.VARCHAR,
# String type field
max_length=
20
,
# Maximum string length
nullable=
True
,
# Required for added fields
default_value=
"standard"
# Value assigned to existing entities
# Also used for new entities if no value provided
)
client.addCollectionField(AddCollectionFieldReq.builder()
        .collectionName(
"product_catalog"
)
        .fieldName(
"priority_level"
)
        .dataType(DataType.VarChar)
        .maxLength(
20
)
        .isNullable(
true
)
        .build());
await
client.
addCollectionField
({
collection_name
:
'product_catalog'
,
field
: {
name
:
'priority_level'
,
dataType
:
'VarChar'
,
nullable
:
true
,
default_value
:
'standard'
,
     }
});
// go
# restful
curl -X POST
"http://localhost:19530/v2/vectordb/collections/fields/add"
\
  -H
"Content-Type: application/json"
\
  -H
"Authorization: Bearer <token>"
\
  -d
'{
    "collectionName": "product_catalog",
    "schema": {
      "fieldName": "priority_level",
      "dataType": "VarChar",
      "nullable": true,
      "defaultValue": "standard",
      "elementTypeParams": {
        "max_length": "20"
      }
    }
  }'
预期行为：
现有实体
将拥有新添加字段的默认值 (
"standard"
)
新实体
可以覆盖默认值，或者在没有提供默认值的情况下使用默认值
字段
几乎立即
可用
，延迟极小
短暂同步后
可立即查询
Python
Java
NodeJS
Go
cURL
# Example query result
{
'id'
:
1
,
'priority_level'
:
'standard'
# Shows default value for existing entities
}
// java
{
'id'
:
1
,
'priority_level'
:
'standard'
#
Shows
default
value
for
existing entities
}
// go
# restful
{
'id'
: 1,
'priority_level'
:
'standard'
# Shows default value for existing entities
}
常见问题
是否可以通过添加
$meta
字段来启用动态 Schema 功能？
不能，您不能使用
add_collection_field
添加
$meta
字段来启用动态字段功能。例如，下面的代码将不起作用：
Python
Java
NodeJS
Go
cURL
# ❌ This is NOT supported
client.add_collection_field(
    collection_name=
"existing_collection"
,
    field_name=
"$meta"
,
    data_type=DataType.JSON
# This operation will fail
)
// ❌ This is NOT supported
client.addCollectionField(AddCollectionFieldReq.builder()
        .collectionName(
"existing_collection"
)
        .fieldName(
"$meta"
)
        .dataType(DataType.JSON)
        .build());
// ❌ This is NOT supported
await
client.
addCollectionField
({
collection_name
:
'product_catalog'
,
field
: {
name
:
'$meta'
,
dataType
:
'JSON'
,
     }
});
// go
# restful
# ❌ This is NOT supported
curl -X POST
"http://localhost:19530/v2/vectordb/collections/fields/add"
\
  -H
"Content-Type: application/json"
\
  -H
"Authorization: Bearer <token>"
\
  -d
'{
    "collectionName": "existing_collection",
    "schema": {
      "fieldName": "$meta",
      "dataType": "JSON",
      "nullable": true
    }
  }'
启用动态 Schema 功能：
新建 Collections
：创建 Collection 时将
enable_dynamic_field
设置为 True。有关详情，请参阅
创建 Collections
现有 Collections
：将 Collection-level 属性
dynamicfield.enabled
设置为 True。有关详情，请参阅
修改 Collections
。
添加与动态字段关键字同名的字段时会发生什么情况？
当你的 Collections 启用了动态字段 (
$meta
exists) 时，你可以添加与现有动态字段键同名的静态字段。新的静态字段将屏蔽动态字段键，但会保留原始动态数据。
为避免字段名称可能出现的冲突，在实际添加前，请参考现有字段和动态字段键，考虑要添加的字段名称。
示例场景：
Python
Java
NodeJS
Go
cURL
# Original collection with dynamic field enabled
# Insert data with dynamic field keys
data = [{
"id"
:
1
,
"my_vector"
: [
0.1
,
0.2
, ...],
"extra_info"
:
"this is a dynamic field key"
,
# Dynamic field key as string
"score"
:
99.5
# Another dynamic field key
}]
client.insert(collection_name=
"product_catalog"
, data=data)
# Add static field with same name as existing dynamic field key
client.add_collection_field(
    collection_name=
"product_catalog"
,
    field_name=
"extra_info"
,
# Same name as dynamic field key
data_type=DataType.INT64,
# Data type can differ from dynamic field key
nullable=
True
# Must be True for added fields
)
# Insert new data after adding static field
new_data = [{
"id"
:
2
,
"my_vector"
: [
0.3
,
0.4
, ...],
"extra_info"
:
100
,
# Now must use INT64 type (static field)
"score"
:
88.0
# Still a dynamic field key
}]
client.insert(collection_name=
"product_catalog"
, data=new_data)
import
com.google.gson.*;
import
io.milvus.v2.service.vector.request.InsertReq;
import
io.milvus.v2.service.vector.response.InsertResp;
Gson
gson
=
new
Gson
();
JsonObject
row
=
new
JsonObject
();
row.addProperty(
"id"
,
1
);
row.add(
"my_vector"
, gson.toJsonTree(
new
float
[]{
0.1f
,
0.2f
, ...}));
row.addProperty(
"extra_info"
,
"this is a dynamic field key"
);
row.addProperty(
"score"
,
99.5
);
InsertResp
insertR
=
client.insert(InsertReq.builder()
        .collectionName(
"product_catalog"
)
        .data(Collections.singletonList(row))
        .build());
        
client.addCollectionField(AddCollectionFieldReq.builder()
        .collectionName(
"product_catalog"
)
        .fieldName(
"extra_info"
)
        .dataType(DataType.Int64)
        .isNullable(
true
)
        .build());
JsonObject
newRow
=
new
JsonObject
();
newRow.addProperty(
"id"
,
2
);
newRow.add(
"my_vector"
, gson.toJsonTree(
new
float
[]{
0.3f
,
0.4f
, ...}));
newRow.addProperty(
"extra_info"
,
100
);
newRow.addProperty(
"score"
,
88.0
);

insertR = client.insert(InsertReq.builder()
        .collectionName(
"product_catalog"
)
        .data(Collections.singletonList(newRow))
        .build());
// Original collection with dynamic field enabled
// Insert data with dynamic field keys
const
data = [{
"id"
:
1
,
"my_vector"
: [
0.1
,
0.2
, ...],
"extra_info"
:
"this is a dynamic field key"
,
// Dynamic field key as string
"score"
:
99.5
// Another dynamic field key
}]
await
client.
insert
({
collection_name
:
"product_catalog"
,
data
: data
});
// Add static field with same name as existing dynamic field key
await
client.
add_collection_field
({
collection_name
:
"product_catalog"
,
field_name
:
"extra_info"
,
// Same name as dynamic field key
data_type
:
DataType
.
INT64
,
// Data type can differ from dynamic field key
nullable
:
true
// Must be True for added fields
});
// Insert new data after adding static field
const
new_data = [{
"id"
:
2
,
"my_vector"
: [
0.3
,
0.4
, ...],
"extra_info"
:
100
,               #
Now
must use
INT64
type
(
static
field)
"score"
:
88.0
#
Still
a dynamic field key
}];
await
client.
insert
({
collection_name
:
"product_catalog"
,
data
: new_data
});
// go
# restful
#!/bin/bash
export
MILVUS_HOST=
"localhost:19530"
export
AUTH_TOKEN=
"your_token_here"
export
COLLECTION_NAME=
"product_catalog"
echo
"Step 1: Insert initial data with dynamic fields..."
curl -X POST
"http://
${MILVUS_HOST}
/v2/vectordb/entities/insert"
\
  -H
"Content-Type: application/json"
\
  -H
"Authorization: Bearer
${AUTH_TOKEN}
"
\
  -d
"{
    \"collectionName\": \"
${COLLECTION_NAME}
\",
    \"data\": [{
      \"id\": 1,
      \"my_vector\": [0.1, 0.2, 0.3, 0.4, 0.5],
      \"extra_info\": \"this is a dynamic field key\",
      \"score\": 99.5
    }]
  }"
echo
-e
"\n\nStep 2: Add static field with same name as dynamic field..."
curl -X POST
"http://
${MILVUS_HOST}
/v2/vectordb/collections/fields/add"
\
  -H
"Content-Type: application/json"
\
  -H
"Authorization: Bearer
${AUTH_TOKEN}
"
\
  -d
"{
    \"collectionName\": \"
${COLLECTION_NAME}
\",
    \"schema\": {
      \"fieldName\": \"extra_info\",
      \"dataType\": \"Int64\",
      \"nullable\": true
    }
  }"
echo
-e
"\n\nStep 3: Insert new data after adding static field..."
curl -X POST
"http://
${MILVUS_HOST}
/v2/vectordb/entities/insert"
\
  -H
"Content-Type: application/json"
\
  -H
"Authorization: Bearer
${AUTH_TOKEN}
"
\
  -d
"{
    \"collectionName\": \"
${COLLECTION_NAME}
\",
    \"data\": [{
      \"id\": 2,
      \"my_vector\": [0.3, 0.4, 0.5, 0.6, 0.7],
      \"extra_info\": 100,
      \"score\": 88.0
    }]
  }"
预期行为：
现有实体
将为新静态字段设置 NULL
extra_info
新实体
必须使用静态字段的数据类型 (
INT64
)
保留
原始动态字段键值
，并可通过
$meta
语法访问
在正常查询中，
静态字段会屏蔽动态字段键值
同时访问静态值和动态值：
Python
Java
NodeJS
Go
cURL
# 1. Query static field only (dynamic field key is masked)
results = client.query(
    collection_name=
"product_catalog"
,
filter
=
"id == 1"
,
    output_fields=[
"extra_info"
]
)
# Returns: {"id": 1, "extra_info": None}  # NULL for existing entity
# 2. Query both static and original dynamic values
results = client.query(
    collection_name=
"product_catalog"
,
filter
=
"id == 1"
,
    output_fields=[
"extra_info"
,
"$meta['extra_info']"
]
)
# Returns: {
#     "id": 1,
#     "extra_info": None,                           # Static field value (NULL)
#     "$meta['extra_info']": "this is a dynamic field key"  # Original dynamic value
# }
# 3. Query new entity with static field value
results = client.query(
    collection_name=
"product_catalog"
,
filter
=
"id == 2"
, 
    output_fields=[
"extra_info"
]
)
# Returns: {"id": 2, "extra_info": 100}  # Static field value
// java
// 1. Query static field only (dynamic field key is masked)
let
results = client.
query
({
collection_name
:
"product_catalog"
,
filter
:
"id == 1"
,
output_fields
: [
"extra_info"
]
})
// Returns: {"id": 1, "extra_info": None}  # NULL for existing entity
// 2. Query both static and original dynamic values
results = client.
query
({
collection_name
:
"product_catalog"
,
filter
:
"id == 1"
,
output_fields
: [
"extra_info"
,
"$meta['extra_info']"
]
});
// Returns: {
//     "id": 1,
//     "extra_info": None,                           # Static field value (NULL)
//     "$meta['extra_info']": "this is a dynamic field key"  # Original dynamic value
// }
// 3. Query new entity with static field value
results = client.
query
({
collection_name
:
"product_catalog"
,
filter
:
"id == 2"
,
output_fields
: [
"extra_info"
]
})
// Returns: {"id": 2, "extra_info": 100}  # Static field value
// go
# restful
#!/bin/bash
export
MILVUS_HOST=
"localhost:19530"
export
AUTH_TOKEN=
"your_token_here"
export
COLLECTION_NAME=
"product_catalog"
echo
"Query 1: Static field only (dynamic field masked)..."
curl -X POST
"http://
${MILVUS_HOST}
/v2/vectordb/entities/query"
\
  -H
"Content-Type: application/json"
\
  -H
"Authorization: Bearer
${AUTH_TOKEN}
"
\
  -d
"{
    \"collectionName\": \"
${COLLECTION_NAME}
\",
    \"filter\": \"id == 1\",
    \"outputFields\": [\"extra_info\"]
  }"
echo
-e
"\n\nQuery 2: Both static and original dynamic values..."
curl -X POST
"http://
${MILVUS_HOST}
/v2/vectordb/entities/query"
\
  -H
"Content-Type: application/json"
\
  -H
"Authorization: Bearer
${AUTH_TOKEN}
"
\
  -d
"{
    \"collectionName\": \"
${COLLECTION_NAME}
\",
    \"filter\": \"id == 1\",
    \"outputFields\": [\"extra_info\", \"\$meta['extra_info']\"]
  }"
echo
-e
"\n\nQuery 3: New entity with static field value..."
curl -X POST
"http://
${MILVUS_HOST}
/v2/vectordb/entities/query"
\
  -H
"Content-Type: application/json"
\
  -H
"Authorization: Bearer
${AUTH_TOKEN}
"
\
  -d
"{
    \"collectionName\": \"
${COLLECTION_NAME}
\",
    \"filter\": \"id == 2\",
    \"outputFields\": [\"extra_info\"]
  }"
新字段可用需要多长时间？
新增字段几乎立即可用，但由于整个 Milvus 集群的内部 Schema 变化广播，可能会有短暂延迟。这种同步可确保在处理涉及新字段的查询之前，所有节点都知道 Schema 的更新。