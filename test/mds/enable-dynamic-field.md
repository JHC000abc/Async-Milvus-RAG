动态字段
Milvus 允许你通过
动态
字段这一特殊功能，插入结构灵活、不断变化的实体。该字段以名为
$meta
的隐藏 JSON 字段实现，它会自动存储数据中任何未在 Collections Schema 中
明确定义的
字段。
工作原理
启用动态字段后，Milvus 会为每个实体添加一个隐藏的
$meta
字段。该字段为 JSON 类型，这意味着它可以存储任何与 JSON 兼容的数据结构，并可使用 JSON 路径语法进行索引。
在数据插入过程中，任何未在 Schema 中声明的字段都会自动以键值对的形式存储在这个动态字段内。
您无需手动管理
$meta
，Milvus 会透明地处理它。
例如，如果您的 Collections Schema 只定义了
id
和
vector
，而您插入了以下实体：
{
"id"
:
1
,
"vector"
:
[
0.1
,
0.2
,
0.3
]
,
"name"
:
"Item A"
,
// Not in schema
"category"
:
"books"
// Not in schema
}
启用动态字段功能后，Milvus 将其内部存储为：
{
"id"
:
1
,
"vector"
:
[
0.1
,
0.2
,
0.3
]
,
"$meta"
:
{
"name"
:
"Item A"
,
"category"
:
"books"
}
}
这样，您就可以在不改变 Schema 的情况下发展数据结构。
常见用例包括
存储可选字段或不常检索的字段
捕获因实体而异的元数据
通过特定动态字段键上的索引支持灵活过滤
支持的数据类型
动态字段支持 Milvus 提供的所有标量数据类型，包括简单值和复杂值。这些数据类型适用于存储在
$meta
中的键的**值。
支持的类型包括
字符串 (
VARCHAR
)
整数 (
INT8
,
INT32
,
INT64
)
浮点 (
FLOAT
,
DOUBLE
)
布尔值 (
BOOL
)
标量值数组 (
ARRAY
)
JSON 对象 (
JSON
)
示例：
{
"brand"
:
"Acme"
,
"price"
:
29.99
,
"in_stock"
:
true
,
"tags"
:
[
"new"
,
"hot"
]
,
"specs"
:
{
"weight"
:
"1.2kg"
,
"dimensions"
:
{
"width"
:
10
,
"height"
:
20
}
}
}
上述每个键和值都将存储在
$meta
字段中。
启用动态字段
要使用动态字段功能，请在创建 Collections Schema 时设置
enable_dynamic_field=True
：
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
MilvusClient, DataType
# Initialize client
client = MilvusClient(uri=
"http://localhost:19530"
)
# Create schema with dynamic field enabled
schema = client.create_schema(
    auto_id=
False
,
enable_dynamic_field=
True
,
)
# Add explicitly defined fields
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
# Create the collection
client.create_collection(
    collection_name=
"my_collection"
,
    schema=schema
)
import
io.milvus.v2.client.*;
import
io.milvus.v2.service.collection.request.CreateCollectionReq;
import
io.milvus.v2.service.collection.request.AddFieldReq;
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

CreateCollectionReq.
CollectionSchema
schema
=
CreateCollectionReq.CollectionSchema.builder()
        .enableDynamicField(
true
)
        .build();
schema.addField(AddFieldReq.builder()
        .fieldName(
"my_id"
)
        .dataType(DataType.Int64)
        .isPrimaryKey(Boolean.TRUE)
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
CreateCollectionReq
requestCreate
=
CreateCollectionReq.builder()
        .collectionName(
"my_collection"
)
        .collectionSchema(schema)
        .build();
client.createCollection(requestCreate);
import
{
MilvusClient
,
DataType
,
CreateCollectionReq
}
from
'@zilliz/milvus2-sdk-node'
;
// Initialize client
const
client =
new
MilvusClient
({
address
:
'localhost:19530'
});
// Create collection
const
res =
await
client.
createCollection
({
collection_name
:
'my_collection'
,
schema
:  [
      {
name
:
'my_id'
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
false
,
      },
      {
name
:
'my_vector'
,
data_type
:
DataType
.
FloatVector
,
type_params
: {
dim
:
'5'
,
      }
   ],
enable_dynamic_field
:
true
});
import
(
"context"
"github.com/milvus-io/milvus/client/v2/entity"
"github.com/milvus-io/milvus/client/v2/milvusclient"
)

ctx, cancel := context.WithCancel(context.Background())
defer
cancel()

client, err := milvusclient.New(ctx, &milvusclient.ClientConfig{
    Address:
"localhost:19530"
,
})
if
err !=
nil
{
return
err
}

schema := entity.NewSchema().WithDynamicFieldEnabled(
true
)
schema.WithField(entity.NewField().
    WithName(
"my_id"
).pk
    WithDataType(entity.FieldTypeInt64).
    WithIsPrimaryKey(
true
),
).WithField(entity.NewField().
    WithName(
"my_vector"
).
    WithDataType(entity.FieldTypeFloatVector).
    WithDim(
5
),
)

err = client.CreateCollection(ctx, milvusclient.NewCreateCollectionOption(
"my_collection"
, schema))
if
err !=
nil
{
return
err
}
# restful
export
TOKEN=
"root:Milvus"
export
CLUSTER_ENDPOINT=
"http://localhost:19530"
export
myIdField=
'{
  "fieldName": "my_id",
  "dataType": "Int64",
  "isPrimary": true,
  "autoID": false
}'
export
myVectorField=
'{
  "fieldName": "my_vector",
  "dataType": "FloatVector",
  "elementTypeParams": {
    "dim": 5
  }
}'
export
schema=
"{
  \"autoID\": false,
  \"enableDynamicField\": true,
  \"fields\": [
$myIdField
,
$myVectorField
]
}"
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
--data
"{
  \"collectionName\": \"my_collection\",
  \"schema\":
$schema
}"
向 Collections 插入实体
动态字段允许您插入未在 Schema 中定义的额外字段。这些字段将自动存储在
$meta
中。
Python
Java
NodeJS
Go
cURL
entities = [
    {
"my_id"
:
1
,
# Explicitly defined primary field
"my_vector"
: [
0.1
,
0.2
,
0.3
,
0.4
,
0.5
],
# Explicitly defined vector field
"overview"
:
"Great product"
,
# Scalar key not defined in schema
"words"
:
150
,
# Scalar key not defined in schema
"dynamic_json"
: {
# JSON key not defined in schema
"varchar"
:
"some text"
,
"nested"
: {
"value"
:
42.5
},
"string_price"
:
"99.99"
# Number stored as string
}
    }
]

client.insert(collection_name=
"my_collection"
, data=entities)
import
com.google.gson.Gson;
import
com.google.gson.JsonObject;
import
io.milvus.v2.service.vector.request.InsertReq;
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
"my_id"
,
1
);
row.add(
"my_vector"
, gson.toJsonTree(Arrays.asList(
0.1
,
0.2
,
0.3
,
0.4
,
0.5
)));
row.addProperty(
"overview"
,
"Great product"
);
row.addProperty(
"words"
,
150
);
JsonObject
dynamic
=
new
JsonObject
();
dynamic.addProperty(
"varchar"
,
"some text"
);
dynamic.addProperty(
"string_price"
,
"99.99"
);
JsonObject
nested
=
new
JsonObject
();
nested.addProperty(
"value"
,
42.5
);

dynamic.add(
"nested"
, nested);
row.add(
"dynamic_json"
, dynamic);

client.insert(InsertReq.builder()
        .collectionName(
"my_collection"
)
        .data(Collections.singletonList(row))
        .build());
const
entities = [
  {
my_id
:
1
,
my_vector
: [
0.1
,
0.2
,
0.3
,
0.4
,
0.5
],
overview
:
'Great product'
,
words
:
150
,
dynamic_json
: {
varchar
:
'some text'
,
nested
: {
value
:
42.5
,
      },
string_price
:
'99.99'
,
    },
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
'my_collection'
,
data
: entities,
});
_, err = client.Insert(ctx, milvusclient.NewColumnBasedInsertOption(
"my_collection"
).
    WithInt64Column(
"my_id"
, []
int64
{
1
}).
    WithFloatVectorColumn(
"my_vector"
,
5
, [][]
float32
{
        {
0.1
,
0.2
,
0.3
,
0.4
,
0.5
},
    }).WithColumns(
    column.NewColumnVarChar(
"overview"
, []
string
{
"Great product"
}),
    column.NewColumnInt32(
"words"
, []
int32
{
150
}),
    column.NewColumnJSONBytes(
"dynamic_json"
, [][]
byte
{
        []
byte
(
`{
            varchar: 'some text',
            nested: {
                value: 42.5,
            },
            string_price: '99.99',
        }`
),
    }),
))
if
err !=
nil
{
return
err
}
# restful
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/entities/insert"
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
'{
  "data": [
    {
      "my_id": 1,
      "my_vector": [0.1, 0.2, 0.3, 0.4, 0.5],
      "overview": "Great product",
      "words": 150,
      "dynamic_json": {
        "varchar": "some text",
        "nested": {
          "value": 42.5
        },
        "string_price": "99.99"
      }
    }
  ],
  "collectionName": "my_collection"
}'
动态字段中的索引键
Compatible with Milvus 2.5.11+
Milvus 允许你使用
JSON 路径索引
为动态字段内的特定键创建索引。这些键可以是标量值，也可以是 JSON 对象中的嵌套值。
动态字段键的索引是
可选的
。在没有索引的情况下，您仍然可以通过动态字段键进行查询或过滤，但这可能会因暴力搜索而导致性能降低。
JSON 路径索引语法
要创建 JSON 路径索引，请指定
JSON path
(
json_path
)：要索引的 JSON 对象中的键或嵌套字段的路径。
举例说明：
metadata["category"]
这定义了索引引擎应在 JSON 结构中查找的位置。
JSON 铸造类型
(
json_cast_type
)：Milvus 在解释和索引指定路径上的值时应使用的数据类型。
该类型必须与被索引字段的实际数据类型相匹配。
有关完整列表，请参阅
支持的 JSON 类型
。
使用 JSON 路径索引动态字段键
由于动态字段是 JSON 字段，因此可以使用 JSON 路径语法索引其中的任何键。这既适用于简单的标量值，也适用于复杂的嵌套结构。
JSON 路径示例：
对于简单的键
overview
,
words
对于嵌套键
dynamic_json['varchar']
,
dynamic_json['nested']['value']
Python
Java
NodeJS
Go
cURL
index_params = client.prepare_index_params()
# Index a simple string key
index_params.add_index(
    field_name=
"overview"
,
# Key name in the dynamic field
index_type=
"AUTOINDEX"
,
# Must be set to AUTOINDEX or INVERTED for JSON path indexing
index_name=
"overview_index"
,
# Unique index name
params={
"json_cast_type"
:
"varchar"
,
# Data type that Milvus uses when indexing the values
"json_path"
:
"overview"
# JSON path to the key
}
)
# Index a simple numeric key
index_params.add_index(
    field_name=
"words"
,
# Key name in the dynamic field
index_type=
"AUTOINDEX"
,
# Must be set to AUTOINDEX or INVERTED for JSON path indexing
index_name=
"words_index"
,
# Unique index name
params={
"json_cast_type"
:
"double"
,
# Data type that Milvus uses when indexing the values
"json_path"
:
"words"
# JSON path to the key
}
)
# Index a nested key within a JSON object
index_params.add_index(
    field_name=
"dynamic_json"
,
# JSON key name in the dynamic field
index_type=
"AUTOINDEX"
,
# Must be set to AUTOINDEX or INVERTED for JSON path indexing
index_name=
"json_varchar_index"
,
# Unique index name
params={
"json_cast_type"
:
"varchar"
,
# Data type that Milvus uses when indexing the values
"json_path"
:
"dynamic_json['varchar']"
# JSON path to the nested key
}
)
# Index a deeply nested key
index_params.add_index(
    field_name=
"dynamic_json"
,
index_type=
"AUTOINDEX"
,
# Must be set to AUTOINDEX or INVERTED for JSON path indexing
index_name=
"json_nested_index"
,
# Unique index name
params={
"json_cast_type"
:
"double"
,
"json_path"
:
"dynamic_json['nested']['value']"
}
)
import
io.milvus.v2.common.IndexParam;

Map<String,Object> extraParams1 =
new
HashMap
<>();
extraParams1.put(
"json_path"
,
"overview"
);
extraParams1.put(
"json_cast_type"
,
"varchar"
);
indexParams.add(IndexParam.builder()
        .fieldName(
"overview"
)
        .indexName(
"overview_index"
)
        .indexType(IndexParam.IndexType.AUTOINDEX)
        .extraParams(extraParams1)
        .build());

Map<String,Object> extraParams2 =
new
HashMap
<>();
extraParams2.put(
"json_path"
,
"words"
);
extraParams2.put(
"json_cast_type"
,
"double"
);
indexParams.add(IndexParam.builder()
        .fieldName(
"words"
)
        .indexName(
"words_index"
)
        .indexType(IndexParam.IndexType.AUTOINDEX)
        .extraParams(extraParams2)
        .build());

Map<String,Object> extraParams3 =
new
HashMap
<>();
extraParams3.put(
"json_path"
,
"dynamic_json['varchar']"
);
extraParams3.put(
"json_cast_type"
,
"varchar"
);
indexParams.add(IndexParam.builder()
        .fieldName(
"dynamic_json"
)
        .indexName(
"json_varchar_index"
)
        .indexType(IndexParam.IndexType.AUTOINDEX)
        .extraParams(extraParams3)
        .build());

Map<String,Object> extraParams4 =
new
HashMap
<>();
extraParams4.put(
"json_path"
,
"dynamic_json['nested']['value']"
);
extraParams4.put(
"json_cast_type"
,
"double"
);
indexParams.add(IndexParam.builder()
        .fieldName(
"dynamic_json"
)
        .indexName(
"json_nested_index"
)
        .indexType(IndexParam.IndexType.AUTOINDEX)
        .extraParams(extraParams4)
        .build());
const
indexParams = [
    {
collection_name
:
'my_collection'
,
field_name
:
'overview'
,
index_name
:
'overview_index'
,
index_type
:
'AUTOINDEX'
,
metric_type
:
'NONE'
,
params
: {
json_path
:
'overview'
,
json_cast_type
:
'varchar'
,
      },
    },
    {
collection_name
:
'my_collection'
,
field_name
:
'words'
,
index_name
:
'words_index'
,
index_type
:
'AUTOINDEX'
,
metric_type
:
'NONE'
,
params
: {
json_path
:
'words'
,
json_cast_type
:
'double'
,
      },
    },
    {
collection_name
:
'my_collection'
,
field_name
:
'dynamic_json'
,
index_name
:
'json_varchar_index'
,
index_type
:
'AUTOINDEX'
,
metric_type
:
'NONE'
,
params
: {
json_cast_type
:
'varchar'
,
json_path
:
"dynamic_json['varchar']"
,
      },
    },
    {
collection_name
:
'my_collection'
,
field_name
:
'dynamic_json'
,
index_name
:
'json_nested_index'
,
index_type
:
'AUTOINDEX'
,
metric_type
:
'NONE'
,
params
: {
json_cast_type
:
'double'
,
json_path
:
"dynamic_json['nested']['value']"
,
      },
    },
  ];
import
(
"github.com/milvus-io/milvus/client/v2/index"
)

jsonIndex1 := index.NewJSONPathIndex(index.AUTOINDEX,
"varchar"
,
"overview"
)
    .WithIndexName(
"overview_index"
)
jsonIndex2 := index.NewJSONPathIndex(index.AUTOINDEX,
"double"
,
"words"
)
    .WithIndexName(
"words_index"
)
jsonIndex3 := index.NewJSONPathIndex(index.AUTOINDEX,
"varchar"
,
`dynamic_json['varchar']`
)
    .WithIndexName(
"json_varchar_index"
)
jsonIndex4 := index.NewJSONPathIndex(index.AUTOINDEX,
"double"
,
`dynamic_json['nested']['value']`
)
    .WithIndexName(
"json_nested_index"
)

indexOpt1 := milvusclient.NewCreateIndexOption(
"my_collection"
,
"overview"
, jsonIndex1)
indexOpt2 := milvusclient.NewCreateIndexOption(
"my_collection"
,
"words"
, jsonIndex2)
indexOpt3 := milvusclient.NewCreateIndexOption(
"my_collection"
,
"dynamic_json"
, jsonIndex3)
indexOpt4 := milvusclient.NewCreateIndexOption(
"my_collection"
,
"dynamic_json"
, jsonIndex4)
export
TOKEN=
"root:Milvus"
export
CLUSTER_ENDPOINT=
"http://localhost:19530"
export
overviewIndex=
'{
  "fieldName": "dynamic_json",
  "indexName": "overview_index",
  "params": {
    "index_type": "AUTOINDEX",
    "json_cast_type": "varchar",
    "json_path": "dynamic_json[\"overview\"]"
  }
}'
export
wordsIndex=
'{
  "fieldName": "dynamic_json",
  "indexName": "words_index",
  "params": {
    "index_type": "AUTOINDEX",
    "json_cast_type": "double",
    "json_path": "dynamic_json[\"words\"]"
  }
}'
export
varcharIndex=
'{
  "fieldName": "dynamic_json",
  "indexName": "json_varchar_index",
  "params": {
    "index_type": "AUTOINDEX",
    "json_cast_type": "varchar",
    "json_path": "dynamic_json[\"varchar\"]"
  }
}'
export
nestedIndex=
'{
  "fieldName": "dynamic_json",
  "indexName": "json_nested_index",
  "params": {
    "index_type": "AUTOINDEX",
    "json_cast_type": "double",
          "json_path": "dynamic_json[\"nested\"][\"value\"]"
    }
  }'
使用 JSON 转换函数进行类型转换
Compatible with Milvus 2.5.14+
如果动态字段键包含格式不正确的值（例如以字符串形式存储的数字），可以使用铸型函数进行转换：
Python
Java
NodeJS
Go
cURL
# Convert a string to double before indexing
index_params.add_index(
    field_name=
"dynamic_json"
,
# JSON key name
index_type=
"AUTOINDEX"
,
    index_name=
"json_string_price_index"
,
    params={
"json_path"
:
"dynamic_json['string_price']"
,
"json_cast_type"
:
"double"
,
# Must be the output type of the cast function
"json_cast_function"
:
"STRING_TO_DOUBLE"
# Case insensitive; convert string to double
}
)
Map<String,Object> extraParams5 =
new
HashMap
<>();
extraParams5.put(
"json_path"
,
"dynamic_json['string_price']"
);
extraParams5.put(
"json_cast_type"
,
"double"
);
indexParams.add(IndexParam.builder()
        .fieldName(
"dynamic_json"
)
        .indexName(
"json_string_price_index"
)
        .indexType(IndexParam.IndexType.AUTOINDEX)
        .extraParams(extraParams5)
        .build());
indexParams.
push
({
collection_name
:
'my_collection'
,
field_name
:
'dynamic_json'
,
index_name
:
'json_string_price_index'
,
index_type
:
'AUTOINDEX'
,
metric_type
:
'NONE'
,
params
: {
json_path
:
"dynamic_json['string_price']"
,
json_cast_type
:
'double'
,
json_cast_function
:
'STRING_TO_DOUBLE'
,
    },
  });
jsonIndex5 := index.NewJSONPathIndex(index.AUTOINDEX,
"double"
,
`dynamic_json['string_price']`
)
    .WithIndexName(
"json_string_price_index"
)
indexOpt5 := milvusclient.NewCreateIndexOption(
"my_collection"
,
"dynamic_json"
, jsonIndex5)
export
TOKEN=
"root:Milvus"
export
CLUSTER_ENDPOINT=
"http://localhost:19530"
export
stringPriceIndex=
'{
  "fieldName": "dynamic_json",
  "indexName": "json_string_price_index",
  "params": {
    "index_type": "AUTOINDEX",
    "json_path": "dynamic_json[\"string_price\"]",
    "json_cast_type": "double",
    "json_cast_function": "STRING_TO_DOUBLE"
  }
}'
如果类型转换失败（例如，值
"not_a_number"
无法转换为数字），该值将被跳过并取消索引。
有关铸型函数参数的详细信息，请参阅
JSON 字段
。
为 Collections 应用索引
定义索引参数后，可使用
create_index()
将其应用到 Collections：
Python
Java
NodeJS
Go
cURL
client.create_index(
    collection_name=
"my_collection"
,
    index_params=index_params
)
import
io.milvus.v2.service.index.request.CreateIndexReq;

client.createIndex(CreateIndexReq.builder()
        .collectionName(
"my_collection"
)
        .indexParams(indexParams)
        .build());
await
client.
createIndex
(indexParams);
indexTask1, err := client.CreateIndex(ctx, indexOpt1)
if
err !=
nil
{
return
err
}
indexTask2, err := client.CreateIndex(ctx, indexOpt2)
if
err !=
nil
{
return
err
}
indexTask3, err := client.CreateIndex(ctx, indexOpt3)
if
err !=
nil
{
return
err
}
indexTask4, err := client.CreateIndex(ctx, indexOpt4)
if
err !=
nil
{
return
err
}
indexTask5, err := client.CreateIndex(ctx, indexOpt5)
if
err !=
nil
{
return
err
}
# restful
export
indexParams=
"[
$varcharIndex
,
$nestedIndex
,
$overviewIndex
,
$wordsIndex
,
$stringPriceIndex
]"
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/indexes/create"
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
  \"collectionName\": \"my_collection\",
  \"indexParams\":
$indexParams
}"
按动态字段键过滤
使用动态字段键插入实体后，可以使用标准过滤表达式对其进行过滤。
对于非 JSON 键（如字符串、数字、布尔值），可直接通过键名引用。
对于存储 JSON 对象的键，可使用 JSON 路径语法访问嵌套值。
根据上一节中
的
实体示例
，有效的过滤表达式包括
Python
Java
NodeJS
Go
cURL
filter
=
'overview == "Great product"'
# Non-JSON key
filter
=
'words >= 100'
# Non-JSON key
filter
=
'dynamic_json["nested"]["value"] < 50'
# JSON object key
String
filter
=
'overview == "Great product"'
;
String
filter
=
'words >= 100'
;
String
filter
=
'dynamic_json["nested"]["value"] < 50'
;
filter =
'overview == "Great product"'
// Non-JSON key
filter =
'words >= 100'
// Non-JSON key
filter =
'dynamic_json["nested"]["value"] < 50'
// JSON object key
filter :=
'overview == "Great product"'
filter :=
'words >= 100'
filter :=
'dynamic_json["nested"]["value"] < 50'
# restful
export
filterOverview=
'overview == "Great product"'
export
filterWords=
'words >= 100'
export
filterNestedValue=
'dynamic_json["nested"]["value"] < 50'
检索动态字段键
：要在搜索或查询结果中返回动态字段键，必须使用与过滤相同的 JSON 路径语法在
output_fields
参数中明确指定它们：
Python
Java
NodeJS
Go
cURL
# Example: Include dynamic field keys in search results
results = client.search(
    collection_name=
"my_collection"
,
    data=[[
0.1
,
0.2
,
0.3
,
0.4
,
0.5
]],
filter
=
filter
,
# Filter expression defined earlier
limit=
10
,
output_fields=[
"overview"
,
# Simple dynamic field key
'dynamic_json["varchar"]'
# Nested JSON key
]
)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.service.vector.request.SearchReq
import
io.milvus.v2.service.vector.request.data.FloatVec;
import
io.milvus.v2.service.vector.response.SearchResp
MilvusClientV2
client
=
new
MilvusClientV2
(ConnectConfig.builder()
        .uri(
"YOUR_CLUSTER_ENDPOINT"
)
        .token(
"YOUR_CLUSTER_TOKEN"
)
        .build());
FloatVec
queryVector
=
new
FloatVec
(
new
float
[]{
0.1
,
0.2
,
0.3
,
0.4
,
0.5
});
SearchReq
searchReq
=
SearchReq.builder()
        .collectionName(
"my_collection"
)
        .data(Collections.singletonList(queryVector))
        .topK(
5
)
        .filter(filter)
        .outputFields(Arrays.asList(
"overview"
,
"dynamic_json['varchar']"
))
        .build();
SearchResp
searchResp
=
client.search(searchReq);
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
"YOUR_CLUSTER_ENDPOINT"
;
const
token =
"YOUR_CLUSTER_TOKEN"
;
const
client =
new
MilvusClient
({address, token});
const
query_vector = [
0.1
,
0.2
,
0.3
,
0.4
,
0.5
]
const
res =
await
client.
search
({
collection_name
:
"my_collection"
,
data
: [query_vector],
limit
:
5
,
filters
: filter,
output_fields
: [
"overview"
,
"dynamic_json['varchar']"
]
})
import
(
"context"
"fmt"
"github.com/milvus-io/milvus/client/v2/entity"
"github.com/milvus-io/milvus/client/v2/milvusclient"
)

ctx, cancel := context.WithCancel(context.Background())
defer
cancel()

milvusAddr :=
"YOUR_CLUSTER_ENDPOINT"
token :=
"YOUR_CLUSTER_TOKEN"
client, err := client.New(ctx, &client.ClientConfig{
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

queryVector := []
float32
{
0.1
,
0.2
,
0.3
,
0.4
,
0.5
}

resultSets, err := client.Search(ctx, milvusclient.NewSearchOption(
"my_collection"
,
// collectionName
5
,
// limit
[]entity.Vector{entity.FloatVector(queryVector)},
).WithConsistencyLevel(entity.ClStrong).
    WithANNSField(
"my_vector"
).
    WithFilter(filter).
    WithOutputFields(
"overview"
,
"dynamic_json['varchar']"
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
"YOUR_CLUSTER_ENDPOINT"
export
TOKEN=
"YOUR_CLUSTER_TOKEN"
export
FILTER=
'color like "red%" and likes > 50'
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/entities/search"
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
  \"collectionName\": \"my_collection\",
  \"data\": [
    [0.1, 0.2, 0.3, 0.4, 0.5]
  ],
  \"annsField\": \"my_vector\",
  \"filter\": \"
${FILTER}
\",
  \"limit\": 5,
  \"outputFields\": [\"overview\", \"dynamic_json.varchar\"]
}"
默认情况下，结果中不包含动态字段键，必须明确请求。
有关支持的操作符和过滤表达式的完整列表，请参阅
过滤搜索
。
将所有内容放在一起
至此，你已经学会了如何使用动态字段来灵活存储和索引 Schema 中未定义的键。一旦插入了动态字段键，就可以像在筛选表达式中使用其他字段一样使用它--不需要特殊的语法。
要完成实际应用中的工作流程，你还需要
在你的向量字段上创建索引
（每个 Collections 都必须这样做）
请参阅
设置索引参数
加载 Collections
请参阅
加载和释放
使用 JSON 路径过滤器进行搜索或查询
请参阅
过滤搜索
和
JSON 操作符
常见问题
何时应在 Schema 中明确定义字段，而不是使用动态字段键？
在以下情况下，您应在模式中明确定义字段，而不是使用动态字段键：
字段经常包含在 output_fields 中
：只有明确定义的字段才能保证通过
output_fields
有效检索。动态字段键没有针对高频检索进行优化，可能会产生性能开销。
字段被频繁访问或过滤
：虽然索引动态字段键可提供与固定 Schema 字段类似的过滤性能，但明确定义的字段可提供更清晰的结构和更好的可维护性。
您需要完全控制字段行为
：显式字段支持 Schema 级约束、验证和更清晰的类型，这对于管理数据完整性和一致性非常有用。
您希望避免索引不一致
：动态字段键中的数据更容易出现类型或结构不一致的情况。使用固定的 Schema 有助于确保数据质量，尤其是在计划使用索引或铸造的情况下。
能否在同一动态字段键上创建多个具有不同数据类型的索引？
不能，
每个 JSON 路径只能
创建
一个索引
。即使动态字段键包含混合类型的值（例如，一些字符串和一些数字），在为该路径创建索引时也必须选择单一的
json_cast_type
。目前还不支持对同一键建立不同类型的多个索引。
索引动态字段键时，如果数据铸造失败怎么办？
如果在动态字段键上创建了索引，但数据转换失败，例如，要转换到
double
的值是一个非数字字符串，如
"abc"
，那么
在创建索引时，
这些特定值将被
静默跳过
。它们不会出现在索引中，因此也
不会在基于过滤器的搜索或
依赖索引
的查询结果中返回
。
这将产生一些重要影响：
无法回退到完全扫描
：如果大多数实体都被成功索引，过滤查询将完全依赖索引。即使实体在逻辑上与过滤条件相匹配，结果集中也会排除筛选失败的实体。
搜索准确性风险
：在数据质量不一致的大型数据集中（尤其是动态字段键），这种行为会导致意外的结果丢失。在编制索引之前，确保数据格式的一致性和有效性至关重要。
谨慎使用铸型函数
：如果在索引编制过程中使用
json_cast_function
将字符串转换为数字，请确保字符串值可以可靠地转换。
json_cast_type
与实际转换类型不匹配会导致错误或跳过条目。
如果我的查询使用的数据类型与索引铸型不同，会发生什么情况？
如果您的查询使用的动态字段键的
数据类型
与索引中使用的
数据类型不同
（例如，当索引被转换为
double
时使用字符串比较进行查询），系统将
不会使用索引
，并可能
在可能的情况
下退回到全扫描。为获得最佳性能和准确性，请确保您的查询类型与创建索引时使用的
json_cast_type
匹配。