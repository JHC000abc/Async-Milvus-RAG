主字段和自动识别
Milvus 中的每个 Collections 都必须有一个主字段，以唯一标识每个实体。这个字段确保每个实体都能被插入、更新、查询或删除，而不会产生歧义。
根据你的使用情况，你既可以让 Milvus 自动生成 ID（自动 ID），也可以手动分配你自己的 ID。
什么是主字段？
主字段是 Collections 中每个实体的唯一键，类似于传统数据库中的主键。在插入、上载、删除和查询操作过程中，Milvus 使用主字段管理实体。
关键要求
每个 Collection 必须有
一个
主字段。
主字段值不能为空。
数据类型必须在创建时指定，以后不能更改。
支持的数据类型
主字段必须使用可唯一标识实体的支持标量数据类型。
数据类型
描述
INT64
64 位整数类型，通常与 AutoID 一起使用。这是大多数使用情况下的推荐选项。
VARCHAR
长度可变的字符串类型。当实体标识符来自外部系统（如产品代码或用户 ID）时使用该类型。需要
max_length
属性来定义每个值允许的最大字节数。
在自动 ID 和手动 ID 之间进行选择
Milvus 支持两种分配主键值的模式。
模式
描述
建议
自动 ID
Milvus 自动为插入或导入的实体生成唯一标识符。
不需要手动管理 ID 的大多数情况。
手动 ID
在插入或导入数据时，您自己提供唯一 ID。
当 ID 必须与外部系统或已有数据集保持一致时。
如果不确定选择哪种模式，请
从自动 ID 开始
，这样可以简化输入并保证唯一性。
建议在所有情况下都使用
autoId
，除非手动设置主键是有益的。
快速入门：使用自动识别
你可以让 Milvus 自动处理 ID 生成。
步骤 1：使用 AutoID 创建 Collections
在主字段定义中启用
auto_id=True
。Milvus 将自动处理 ID 生成。
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
MilvusClient, DataType

client = MilvusClient(uri=
"http://localhost:19530"
)

schema = client.create_schema()
# Define primary field with AutoID enabled
schema.add_field(
field_name=
"id"
,
# Primary field name
is_primary=
True
,
auto_id=
True
,
# Milvus generates IDs automatically; Defaults to False
datatype=DataType.INT64
)
# Define the other fields
schema.add_field(field_name=
"embedding"
, datatype=DataType.FLOAT_VECTOR, dim=
4
)
# Vector field
schema.add_field(field_name=
"category"
, datatype=DataType.VARCHAR, max_length=
1000
)
# Scalar field of the VARCHAR type
# Create the collection
if
client.has_collection(
"demo_autoid"
):
    client.drop_collection(
"demo_autoid"
)
client.create_collection(collection_name=
"demo_autoid"
, schema=schema)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.service.collection.request.AddFieldReq;
import
io.milvus.v2.service.collection.request.CreateCollectionReq;
import
io.milvus.v2.service.collection.request.DropCollectionReq;
MilvusClientV2
client
=
new
MilvusClientV2
(ConnectConfig.builder()
        .uri(
"http://localhost:19530"
)
        .build());
        
CreateCollectionReq.
CollectionSchema
collectionSchema
=
CreateCollectionReq.CollectionSchema.builder()
        .build();
collectionSchema.addField(AddFieldReq.builder()
        .fieldName(
"id"
)
        .dataType(DataType.Int64)
        .isPrimaryKey(
true
)
        .autoID(
true
)
        .build());
collectionSchema.addField(AddFieldReq.builder()
        .fieldName(
"embedding"
)
        .dataType(DataType.FloatVector)
        .dimension(
4
)
        .build());
collectionSchema.addField(AddFieldReq.builder()
        .fieldName(
"category"
)
        .dataType(DataType.VarChar)
        .maxLength(
1000
)
        .build());

client.dropCollection(DropCollectionReq.builder()
        .collectionName(
"demo_autoid"
)
        .build());
CreateCollectionReq
requestCreate
=
CreateCollectionReq.builder()
        .collectionName(
"demo_autoid"
)
        .collectionSchema(collectionSchema)
        .build();
client.createCollection(requestCreate);
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
client =
new
MilvusClient
({
address
:
"localhost:19530"
,
});
// Define schema fields
const
schema = [
  {
name
:
"id"
,
description
:
"Primary field"
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
autoID
:
true
,
// Milvus generates IDs automatically
},
  {
name
:
"embedding"
,
description
:
"Vector field"
,
data_type
:
DataType
.
FloatVector
,
dim
:
4
,
  },
  {
name
:
"category"
,
description
:
"Scalar field"
,
data_type
:
DataType
.
VarChar
,
max_length
:
1000
,
  },
];
// Create the collection
await
client.
createCollection
({
collection_name
:
"demo_autoid"
,
fields
: schema,
});
// go
# restful
export
SCHEMA=
'{
    "autoID": true,
    "fields": [
        {
            "fieldName": "id",
            "dataType": "Int64",
            "isPrimary": true,
            "elementTypeParams": {}
        },
        {
            "fieldName": "embedding",
            "dataType": "FloatVector",
            "isPrimary": false,
            "elementTypeParams": {
                "dim": "4"
            }
        },
        {
            "fieldName": "category",
            "dataType": "VarChar",
            "isPrimary": false,
            "elementTypeParams": {
                "max_length": "1000"
            }
        }
    ]
}'
curl -X POST
'http://localhost:19530/v2/vectordb/collections/create'
\
-H
'Content-Type: application/json'
\
-d
"{
    \"collectionName\": \"demo_autoid\",
    \"schema\":
$SCHEMA
}"
第 2 步：插入数据
重要：
不要在数据中包含主字段列。Milvus 会自动生成 ID。
Python
Java
NodeJS
Go
cURL
data = [
    {
"embedding"
: [
0.1
,
0.2
,
0.3
,
0.4
],
"category"
:
"book"
},
    {
"embedding"
: [
0.2
,
0.3
,
0.4
,
0.5
],
"category"
:
"toy"
},
]

res = client.insert(collection_name=
"demo_autoid"
, data=data)
print
(
"Generated IDs:"
, res.get(
"ids"
))
# Output example:
# Generated IDs: [461526052788333649, 461526052788333650]
import
com.google.gson.*;
import
io.milvus.v2.service.vector.request.InsertReq;
import
io.milvus.v2.service.vector.response.InsertResp;

List<JsonObject> rows =
new
ArrayList
<>();
Gson
gson
=
new
Gson
();
JsonObject
row1
=
new
JsonObject
();
row1.add(
"embedding"
, gson.toJsonTree(
new
float
[]{
0.1f
,
0.2f
,
0.3f
,
0.4f
}));
row1.addProperty(
"category"
,
"book"
);
rows.add(row1);
JsonObject
row2
=
new
JsonObject
();
row2.add(
"embedding"
, gson.toJsonTree(
new
float
[]{
0.2f
,
0.3f
,
0.4f
,
0.5f
}));
row2.addProperty(
"category"
,
"toy"
);
rows.add(row2);
InsertResp
insertR
=
client.insert(InsertReq.builder()
        .collectionName(
"demo_autoid"
)
        .data(rows)
        .build());
System.out.printf(
"Generated IDs: %s\n"
, insertR.getPrimaryKeys());
const
data = [
    {
"embedding"
: [
0.1
,
0.2
,
0.3
,
0.4
],
"category"
:
"book"
},
    {
"embedding"
: [
0.2
,
0.3
,
0.4
,
0.5
],
"category"
:
"toy"
},
];
const
res =
await
client.
insert
({
collection_name
:
"demo_autoid"
,
fields_data
: data,
});
console
.
log
(res);
// go
# restful
export
INSERT_DATA=
'[
    {
        "embedding": [0.1, 0.2, 0.3, 0.4],
        "category": "book"
    },
    {
        "embedding": [0.2, 0.3, 0.4, 0.5],
        "category": "toy"
    }
]'
curl -X POST
'http://localhost:19530/v2/vectordb/entities/insert'
\
-H
'Content-Type: application/json'
\
-d
"{
    \"collectionName\": \"demo_autoid\",
    \"data\":
$INSERT_DATA
}"
在处理现有实体时，请使用
upsert()
而不是
insert()
，以避免 ID 重复错误。
使用手动 ID
如果需要手动控制 ID，请禁用 AutoID 并提供自己的值。
步骤 1：创建不带 AutoID 的 Collections
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
MilvusClient, DataType

client = MilvusClient(uri=
"http://localhost:19530"
)

schema = client.create_schema()
# Define the primary field without AutoID
schema.add_field(
field_name=
"product_id"
,
is_primary=
True
,
auto_id=
False
,
# You'll provide IDs manually at data ingestion
datatype=DataType.VARCHAR,
max_length=
100
# Required when datatype is VARCHAR
)
# Define the other fields
schema.add_field(field_name=
"embedding"
, datatype=DataType.FLOAT_VECTOR, dim=
4
)
# Vector field
schema.add_field(field_name=
"category"
, datatype=DataType.VARCHAR, max_length=
1000
)
# Scalar field of the VARCHAR type
# Create the collection
if
client.has_collection(
"demo_manual_ids"
):
    client.drop_collection(
"demo_manual_ids"
)
client.create_collection(collection_name=
"demo_manual_ids"
, schema=schema)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.service.collection.request.AddFieldReq;
import
io.milvus.v2.service.collection.request.CreateCollectionReq;
import
io.milvus.v2.service.collection.request.DropCollectionReq;
MilvusClientV2
client
=
new
MilvusClientV2
(ConnectConfig.builder()
        .uri(
"http://localhost:19530"
)
        .build());
        
CreateCollectionReq.
CollectionSchema
collectionSchema
=
CreateCollectionReq.CollectionSchema.builder()
        .build();
collectionSchema.addField(AddFieldReq.builder()
        .fieldName(
"product_id"
)
        .dataType(DataType.VarChar)
        .isPrimaryKey(
true
)
        .autoID(
false
)
        .maxLength(
100
)
        .build());
collectionSchema.addField(AddFieldReq.builder()
        .fieldName(
"embedding"
)
        .dataType(DataType.FloatVector)
        .dimension(
4
)
        .build());
collectionSchema.addField(AddFieldReq.builder()
        .fieldName(
"category"
)
        .dataType(DataType.VarChar)
        .maxLength(
1000
)
        .build());

client.dropCollection(DropCollectionReq.builder()
        .collectionName(
"demo_manual_ids"
)
        .build());
CreateCollectionReq
requestCreate
=
CreateCollectionReq.builder()
        .collectionName(
"demo_manual_ids"
)
        .collectionSchema(collectionSchema)
        .build();
client.createCollection(requestCreate);
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
client =
new
MilvusClient
({
address
:
"localhost:19530"
,
username
:
"username"
,
password
:
"Aa12345!!"
,
});
const
schema = [
  {
name
:
"product_id"
,
data_type
:
DataType
.
VARCHAR
,
is_primary_key
:
true
,
autoID
:
false
,
  },
  {
name
:
"embedding"
,
data_type
:
DataType
.
FLOAT_VECTOR
,
dim
:
4
,
  },
  {
name
:
"category"
,
data_type
:
DataType
.
VARCHAR
,
max_length
:
1000
,
  },
];
const
res =
await
client.
createCollection
({
collection_name
:
"demo_autoid"
,
schema
: schema,
});
// go
# restful
export
SCHEMA=
'{
    "autoID": false,
    "fields": [
        {
            "fieldName": "product_id",
            "dataType": "VarChar",
            "isPrimary": true,
            "elementTypeParams": {
                "max_length": "100"
            }
        },
        {
            "fieldName": "embedding",
            "dataType": "FloatVector",
            "isPrimary": false,
            "elementTypeParams": {
                "dim": "4"
            }
        },
        {
            "fieldName": "category",
            "dataType": "VarChar",
            "isPrimary": false,
            "elementTypeParams": {
                "max_length": "1000"
            }
        }
    ]
}'
curl -X POST
'http://localhost:19530/v2/vectordb/collections/create'
\
-H
'Content-Type: application/json'
\
-d
"{
    \"collectionName\": \"demo_manual_ids\",
    \"schema\":
$SCHEMA
}"
第 2 步：用 ID 插入数据
您必须在每次插入操作中包含主字段列。
Python
Java
NodeJS
Go
cURL
# Each entity must contain the primary field `product_id`
data = [
    {
"product_id"
:
"PROD-001"
,
"embedding"
: [
0.1
,
0.2
,
0.3
,
0.4
],
"category"
:
"book"
},
    {
"product_id"
:
"PROD-002"
,
"embedding"
: [
0.2
,
0.3
,
0.4
,
0.5
],
"category"
:
"toy"
},
]

res = client.insert(collection_name=
"demo_manual_ids"
, data=data)
print
(
"Generated IDs:"
, res.get(
"ids"
))
# Output example:
# Generated IDs: ['PROD-001', 'PROD-002']
import
com.google.gson.*;
import
io.milvus.v2.service.vector.request.InsertReq;
import
io.milvus.v2.service.vector.response.InsertResp;

List<JsonObject> rows =
new
ArrayList
<>();
Gson
gson
=
new
Gson
();
JsonObject
row1
=
new
JsonObject
();
row1.addProperty(
"product_id"
,
"PROD-001"
);
row1.add(
"embedding"
, gson.toJsonTree(
new
float
[]{
0.1f
,
0.2f
,
0.3f
,
0.4f
}));
row1.addProperty(
"category"
,
"book"
);
rows.add(row1);
JsonObject
row2
=
new
JsonObject
();
row2.addProperty(
"product_id"
,
"PROD-002"
);
row2.add(
"embedding"
, gson.toJsonTree(
new
float
[]{
0.2f
,
0.3f
,
0.4f
,
0.5f
}));
row2.addProperty(
"category"
,
"toy"
);
rows.add(row2);
InsertResp
insertR
=
client.insert(InsertReq.builder()
        .collectionName(
"demo_manual_ids"
)
        .data(rows)
        .build());
System.out.printf(
"Generated IDs: %s\n"
, insertR.getPrimaryKeys());
const
data = [
    {
"product_id"
:
"PROD-001"
,
"embedding"
: [
0.1
,
0.2
,
0.3
,
0.4
],
"category"
:
"book"
},
    {
"product_id"
:
"PROD-002"
,
"embedding"
: [
0.2
,
0.3
,
0.4
,
0.5
],
"category"
:
"toy"
},
];
const
insert =
await
client.
insert
({
collection_name
:
"demo_autoid"
,
fields_data
: data,
});
console
.
log
(insert);
// go
# restful
export
INSERT_DATA=
'[
    {
        "product_id": "PROD-001",
        "embedding": [0.1, 0.2, 0.3, 0.4],
        "category": "book"
    },
    {
        "product_id": "PROD-002",
        "embedding": [0.2, 0.3, 0.4, 0.5],
        "category": "toy"
    }
]'
# 插入数据
curl -X POST
'http://localhost:19530/v2/vectordb/entities/insert'
\
-H
'Content-Type: application/json'
\
-d
"{
    \"collectionName\": \"demo_manual_ids\",
    \"data\":
$INSERT_DATA
}"
您的责任
确保所有 ID 在所有实体中都是唯一的
在每次插入/导入操作中包含主字段
自行处理 ID 冲突和重复检测
高级用法
迁移带有现有 AutoID 的数据
要在数据迁移过程中保留现有 ID，请通过调用
alter_collection_properties
启用
allow_insert_auto_id
属性。当设置为 true 时，即使启用了 AutoID，Milvus 也会接受用户提供的 ID。
有关配置详情，请参阅
修改 Collections
。
确保跨集群的全局 AutoID 唯一性
运行多个 Milvus 集群时，为每个集群配置唯一的集群 ID，以确保 AutoID 绝不重叠。
配置：
在初始化群集之前，编辑
milvus.yaml
中的
common.clusterID
配置：
common:
clusterID:
3
# Must be unique across all clusters (Range: 0-7)
在此配置中，
clusterID
指定了生成 AutoID 时使用的唯一标识符，范围从 0 到 7（最多支持 8 个集群）。
Milvus 在内部处理位反转，以便将来扩展时不会出现 ID 重叠。除设置群集 ID 外，无需手动配置。
参考：AutoID 如何工作
了解 AutoID 如何在内部生成唯一标识符，有助于正确
配置群集 ID
和排除 ID 相关问题。
AutoID 使用结构化的 64 位格式来保证唯一性：
[sign_bit][cluster_id][physical_ts][logical_ts]
段
说明
sign_bit
保留供内部使用
cluster_id
标识生成 ID 的群集（值范围：0-7）
physical_ts
以毫秒为单位的 ID 生成时间戳
logical_ts
用于区分同一毫秒内创建的 ID 的计数器
即使启用了以
VARCHAR
作为数据类型的 AutoID，Milvus 仍会生成数字 ID。这些 ID 以数字字符串形式存储，最大长度为 20 个字符（uint64 范围）。