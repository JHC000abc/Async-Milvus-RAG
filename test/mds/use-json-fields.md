JSON 字段
Milvus 允许您使用
JSON
数据类型在单个字段中存储和索引结构化数据。这样就能实现具有嵌套属性的灵活 Schema，同时还能通过 JSON 索引进行高效过滤。
什么是 JSON 字段？
JSON 字段是 Milvus 中一个模式定义的字段，用于存储结构化的键值数据。值可以包括字符串、数字、布尔值、数组或深嵌套对象。
下面是文档中 JSON 字段的示例：
{
"metadata"
:
{
"category"
:
"electronics"
,
"brand"
:
"BrandA"
,
"in_stock"
:
true
,
"price"
:
99.99
,
"string_price"
:
"99.99"
,
"tags"
:
[
"clearance"
,
"summer_sale"
]
,
"supplier"
:
{
"name"
:
"SupplierX"
,
"country"
:
"USA"
,
"contact"
:
{
"email"
:
"support@supplierx.com"
,
"phone"
:
"+1-800-555-0199"
}
}
}
}
在这个例子中
metadata
是 Schema 中定义的 JSON 字段。
可以存储平面值（如
category
,
in_stock
）、数组（
tags
）和嵌套对象（
supplier
）。
在 Schema 中定义 JSON 字段
要使用 JSON 字段，请在 Collections 模式中明确定义该字段，指定
DataType
为
JSON
。
下面的示例创建了一个 Collections，其模式包含这些字段：
主键 (
product_id
)
一个
vector
字段（对于每个 Collections 都是必选字段）
一个
metadata
类型的字段
JSON
，可存储结构化数据，如平面值、数组或嵌套对象
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
# Create schema with a JSON field
schema = client.create_schema(auto_id=
False
, enable_dynamic_field=
True
)

schema.add_field(field_name=
"product_id"
, datatype=DataType.INT64, is_primary=
True
)
schema.add_field(field_name=
"vector"
, datatype=DataType.FLOAT_VECTOR, dim=
5
)
schema.add_field(field_name=
"metadata"
, datatype=DataType.JSON, nullable=
True
)
# JSON field that allows null values
client.create_collection(
    collection_name=
"product_catalog"
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
"product_id"
)
        .dataType(DataType.Int64)
        .isPrimaryKey(Boolean.TRUE)
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
schema.addField(AddFieldReq.builder()
        .fieldName(
"metadata"
)
        .dataType(DataType.JSON)
        .isNullable(
true
)
        .build());
CreateCollectionReq
requestCreate
=
CreateCollectionReq.builder()
        .collectionName(
"product_catalog"
)
        .collectionSchema(schema)
        .build();
client.createCollection(requestCreate);
import
{
MilvusClient
,
DataType
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
});
// Create collection
await
client.
createCollection
({
collection_name
:
"product_catalog"
,
fields
: [
  {
name
:
"product_id"
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
},
  {
name
:
"vector"
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
"metadata"
,
data_type
:
DataType
.
JSON
,
nullable
:
true
// JSON field that allows null values
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
"product_id"
).pk
    WithDataType(entity.FieldTypeInt64).
    WithIsPrimaryKey(
true
),
).WithField(entity.NewField().
    WithName(
"vector"
).
    WithDataType(entity.FieldTypeFloatVector).
    WithDim(
5
),
).WithField(entity.NewField().
    WithName(
"metadata"
).
    WithDataType(entity.FieldTypeJSON).
    WithNullable(
true
),
)

err = client.CreateCollection(ctx, milvusclient.NewCreateCollectionOption(
"product_catalog"
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
# 字段定义
export
productIdField=
'{
  "fieldName": "product_id",
  "dataType": "Int64",
  "isPrimary": true,
  "autoID": false
}'
export
vectorField=
'{
  "fieldName": "vector",
  "dataType": "FloatVector",
  "typeParams": {
    "dim": 5
  }
}'
export
metadataField=
'{
  "fieldName": "metadata",
  "dataType": "JSON",
  "isNullable": true
}'
# 构造 schema
export
schema=
"{
  \"autoID\": false,
  \"enableDynamicField\": true,
  \"fields\": [
$productIdField
,
$vectorField
,
$metadataField
]
}"
# 创建集合
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
  \"collectionName\": \"product_catalog\",
  \"schema\":
$schema
}"
您也可以启用动态字段功能来灵活存储未声明的字段，但这不是 JSON 字段发挥作用的必要条件。更多信息，请参阅
动态
字段。
插入带有 JSON 数据的实体
创建 Collections 后，在
metadata
JSON 字段中插入包含结构化 JSON 对象的实体。
Python
Java
NodeJS
Go
cURL
entities = [
    {
"product_id"
:
1
,
"vector"
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
"metadata"
: {
"category"
:
"electronics"
,
"brand"
:
"BrandA"
,
"in_stock"
:
True
,
"price"
:
99.99
,
"string_price"
:
"99.99"
,
"tags"
: [
"clearance"
,
"summer_sale"
],
"supplier"
: {
"name"
:
"SupplierX"
,
"country"
:
"USA"
,
"contact"
: {
"email"
:
"support@supplierx.com"
,
"phone"
:
"+1-800-555-0199"
}
            }
        }
    }
]

client.insert(collection_name=
"product_catalog"
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
"product_id"
,
1
);
row.add(
"vector"
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
JsonObject
metadata
=
new
JsonObject
();
metadata.addProperty(
"category"
,
"electronics"
);
metadata.addProperty(
"brand"
,
"BrandA"
);
metadata.addProperty(
"in_stock"
,
true
);
metadata.addProperty(
"price"
,
99.99
);
metadata.addProperty(
"string_price"
,
"99.99"
);
metadata.add(
"tags"
, gson.toJsonTree(Arrays.asList(
"clearance"
,
"summer_sale"
)));
JsonObject
supplier
=
new
JsonObject
();
supplier.addProperty(
"name"
,
"SupplierX"
);
supplier.addProperty(
"country"
,
"USA"
);
JsonObject
contact
=
new
JsonObject
();
contact.addProperty(
"email"
,
"support@supplierx.com"
);
contact.addProperty(
"phone"
,
"+1-800-555-0199"
);

supplier.add(
"contact"
, contact);
metadata.add(
"supplier"
, supplier);
row.add(
"metadata"
, metadata);

client.insert(InsertReq.builder()
        .collectionName(
"product_catalog"
)
        .data(Collections.singletonList(row))
        .build());
const
entities = [
    {
"product_id"
:
1
,
"vector"
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
"metadata"
: {
"category"
:
"electronics"
,
"brand"
:
"BrandA"
,
"in_stock"
:
True
,
"price"
:
99.99
,
"string_price"
:
"99.99"
,
"tags"
: [
"clearance"
,
"summer_sale"
],
"supplier"
: {
"name"
:
"SupplierX"
,
"country"
:
"USA"
,
"contact"
: {
"email"
:
"support@supplierx.com"
,
"phone"
:
"+1-800-555-0199"
}
            }
        }
    }
]
await
client.
insert
({
collection_name
:
"product_catalog"
,
data
: entities
});
_, err = client.Insert(ctx, milvusclient.NewColumnBasedInsertOption(
"product_catalog"
).
    WithInt64Column(
"product_id"
, []
int64
{
1
}).
    WithFloatVectorColumn(
"vector"
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
    column.NewColumnJSONBytes(
"metadata"
, [][]
byte
{
        []
byte
(
`{
            "category": "electronics",
            "brand": "BrandA",
            "in_stock": True,
            "price": 99.99,
            "string_price": "99.99",
            "tags": ["clearance", "summer_sale"],
            "supplier": {
                "name": "SupplierX",
                "country": "USA",
                "contact": {
                    "email": "support@supplierx.com",
                    "phone": "+1-800-555-0199"
                }
            }
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
export
TOKEN=
"root:Milvus"
export
CLUSTER_ENDPOINT=
"http://localhost:19530"
export
entities=
'[
  {
    "product_id": 1,
    "vector": [0.1, 0.2, 0.3, 0.4, 0.5],
    "metadata": {
      "category": "electronics",
      "brand": "BrandA",
      "in_stock": true,
      "price": 99.99,
      "string_price": "99.99",
      "tags": ["clearance", "summer_sale"],
      "supplier": {
        "name": "SupplierX",
        "country": "USA",
        "contact": {
          "email": "support@supplierx.com",
          "phone": "+1-800-555-0199"
        }
      }
    }
  }
]'
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/collections/product_catalog/insert"
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
  \"data\":
$entities
}"
JSON 字段内的索引值
为了加速对 JSON 字段的标量过滤，Milvus 支持以下类型的索引：
JSON 路径索引
--使用声明的标量类型索引特定的 JSON 路径。
JSON 平面索引
--通过自动类型推断索引整个 JSON 对象（或子树）。
JSON 字段索引是
可选的
。在没有索引的情况下，您仍然可以通过 JSON 路径进行查询或过滤，但这可能会因暴力搜索而导致性能降低。
在路径索引和平面索引之间进行选择
Compatible with Milvus 2.6.x
能力
JSON 路径索引
JSON 扁平索引
索引内容
您指定的特定路径
对象路径下的所有扁平化路径
类型处理
您声明
json_cast_type
（标量类型）
必须是 JSON（自动类型推断）
数组作为 LHS¹
支持
不支持
查询速度
索引路径
高
高
，平均略低
磁盘使用
较低
高
¹
数组作为 LHS
表示过滤表达式的左侧是一个 JSON 数组（例如）：
metadata["tags"] == ["clearance", "summer_sale"]
json_contains(metadata["tags"], "clearance")
在这些情况下，
metadata["tags"]
是一个数组。JSON 平面索引无法加速此类过滤器--请使用具有数组铸型的 JSON 路径索引。
在以下情况下使用 JSON 路径索引
事先知道要查询的热键。
需要过滤左侧为数组的内容。
希望尽量减少磁盘使用量。
在以下情况下使用 JSON 平面索引
需要索引整个子树（包括根）。
JSON 结构经常变化。
希望在不声明每个路径的情况下扩大查询范围。
JSON 路径索引
要创建 JSON 路径索引，请指定
JSON path
(
json_path
)：您要索引的 JSON 对象中的键或嵌套字段的路径。
例如
对于键、
metadata["category"]
对于嵌套字段、
metadata["contact"]["email"]
这定义了索引引擎应在 JSON 结构中查找的位置。
JSON 转换类型
(
json_cast_type
)：Milvus 在指定路径上解释和索引值时应使用的数据类型。
该类型必须与被索引字段的实际数据类型相匹配。如果要在索引过程中将数据类型转换为另一种类型，请考虑
使用铸型函数
。
有关完整列表，请参阅
下文
。
支持的 JSON 转换类型
铸入类型不区分大小写。支持以下类型：
类型
描述
示例 JSON 值
bool
布尔值
true
,
false
double
数值（整数或浮点数）
42
,
99.99
、
-15.5
varchar
字符串值
"electronics"
,
"BrandA"
array_bool
布尔数组
[true, false, true]
array_double
数字数组
[1.2, 3.14, 42]
array_varchar
字符串数组
["tag1", "tag2", "tag3"]
数组应包含相同类型的元素，以优化索引。更多信息，请参阅
数组字段
。
示例创建 JSON 路径索引
使用介绍中的
metadata
JSON 结构，下面举例说明如何在不同的 JSON 路径上创建索引：
Python
Java
NodeJS
Go
cURL
# Index the category field as a string
index_params = client.prepare_index_params()

index_params.add_index(
    field_name=
"metadata"
,
index_type=
"AUTOINDEX"
,
# Must be set to AUTOINDEX or INVERTED for JSON path indexing
index_name=
"category_index"
,
# Unique index name
params={
"json_path"
:
"metadata[\"category\"]"
,
# Path to the JSON key to be indexed
"json_cast_type"
:
"varchar"
# Data cast type
}
)
# Index the tags array as string array
index_params.add_index(
    field_name=
"metadata"
,
index_type=
"AUTOINDEX"
,
# Must be set to AUTOINDEX or INVERTED for JSON path indexing
index_name=
"tags_array_index"
,
# Unique index name
params={
"json_path"
:
"metadata[\"tags\"]"
,
# Path to the JSON key to be indexed
"json_cast_type"
:
"array_varchar"
# Data cast type
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
"metadata[\"category\"]"
);
extraParams1.put(
"json_cast_type"
,
"varchar"
);
indexParams.add(IndexParam.builder()
        .fieldName(
"metadata"
)
        .indexName(
"category_index"
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
"metadata[\"tags\"]"
);
extraParams2.put(
"json_cast_type"
,
"array_varchar"
);
indexParams.add(IndexParam.builder()
        .fieldName(
"metadata"
)
        .indexName(
"tags_array_index"
)
        .indexType(IndexParam.IndexType.AUTOINDEX)
        .extraParams(extraParams2)
        .build());
const
indexParams = [
  {
collection_name
:
"product_catalog"
,
field_name
:
"metadata"
,
index_name
:
"category_index"
,
index_type
:
"AUTOINDEX"
,
// Can also use "INVERTED" for JSON path indexing
extra_params
: {
json_path
:
'metadata["category"]'
,
json_cast_type
:
"varchar"
,
    },
  },
  {
collection_name
:
"product_catalog"
,
field_name
:
"metadata"
,
index_name
:
"tags_array_index"
,
index_type
:
"AUTOINDEX"
,
// Can also use "INVERTED" for JSON path indexing
extra_params
: {
json_path
:
'metadata["tags"]'
,
json_cast_type
:
"array_varchar"
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
`metadata["category"]`
)
    .WithIndexName(
"category_index"
)
jsonIndex2 := index.NewJSONPathIndex(index.AUTOINDEX,
"array_varchar"
,
`metadata["tags"]`
)
    .WithIndexName(
"tags_array_index"
)

indexOpt1 := milvusclient.NewCreateIndexOption(
"product_catalog"
,
"metadata"
, jsonIndex1)
indexOpt2 := milvusclient.NewCreateIndexOption(
"product_catalog"
,
"metadata"
, jsonIndex2)
# restful
export
categoryIndex=
'{
  "fieldName": "metadata",
  "indexName": "category_index",
  "params": {
    "index_type": "AUTOINDEX",
    "json_path": "metadata[\\\"category\\\"]",
    "json_cast_type": "varchar"
  }
}'
export
tagsArrayIndex=
'{
  "fieldName": "metadata",
  "indexName": "tags_array_index",
  "params": {
    "index_type": "AUTOINDEX",
    "json_path": "metadata[\\\"tags\\\"]",
    "json_cast_type": "array_varchar"
  }
}'
使用 JSON 转换函数进行类型转换
Compatible with Milvus 2.5.14+
如果您的 JSON 字段键包含格式不正确的值（例如，存储为字符串的数字），您可以在索引过程中使用铸型函数转换值。
支持的投影函数
铸型函数不区分大小写。支持以下类型：
转换函数
转换自 → 转换为
用例
"STRING_TO_DOUBLE"
字符串 → 数值（双）
将
"99.99"
转换为
99.99
举例说明：将字符串数字转换为 double
Python
Java
NodeJS
Go
cURL
# Convert string numbers to double for indexing
index_params.add_index(
    field_name=
"metadata"
,
index_type=
"AUTOINDEX"
,
# Must be set to AUTOINDEX or INVERTED for JSON path indexing
index_name=
"string_to_double_index"
,
# Unique index name
params={
"json_path"
:
"metadata[\"string_price\"]"
,
# Path to the JSON key to be indexed
"json_cast_type"
:
"double"
,
# Data cast type
"json_cast_function"
:
"STRING_TO_DOUBLE"
# Cast function; case insensitive
}
)
Map<String,Object> extraParams3 =
new
HashMap
<>();
extraParams3.put(
"json_path"
,
"metadata[\"string_price\"]"
);
extraParams3.put(
"json_cast_type"
,
"double"
);
extraParams3.put(
"json_cast_function"
,
"STRING_TO_DOUBLE"
);
indexParams.add(IndexParam.builder()
        .fieldName(
"metadata"
)
        .indexName(
"string_to_double_index"
)
        .indexType(IndexParam.IndexType.AUTOINDEX)
        .extraParams(extraParams3)
        .build());
indexParams.
push
({
collection_name
:
"product_catalog"
,
field_name
:
"metadata"
,
index_name
:
"string_to_double_index"
,
index_type
:
"AUTOINDEX"
,
// Can also use "INVERTED"
extra_params
: {
json_path
:
'metadata["string_price"]'
,
json_cast_type
:
"double"
,
json_cast_function
:
"STRING_TO_DOUBLE"
,
// Case insensitive
},
});
jsonIndex3 := index.NewJSONPathIndex(index.AUTOINDEX,
"double"
,
`metadata["string_price"]`
)
                    .WithIndexName(
"string_to_double_index"
)

indexOpt3 := milvusclient.NewCreateIndexOption(
"product_catalog"
,
"metadata"
, jsonIndex3)
# restful
export
stringToDoubleIndex=
'{
  "fieldName": "metadata",
  "indexName": "string_to_double_index",
  "params": {
    "index_type": "AUTOINDEX",
    "json_path": "metadata[\\\"string_price\\\"]",
    "json_cast_type": "double",
    "json_cast_function": "STRING_TO_DOUBLE"
  }
}'
json_cast_type
参数是强制性的，必须与转换函数的输出类型相同。
如果转换失败（如非数字字符串），该值将被跳过，不会被索引。
JSON 扁平索引
Compatible with Milvus 2.6.x
对于 JSON
扁平化索引
，Milvus 通过
扁平化
JSON 结构和自动推断每个值的类型，对 JSON 对象路径（包括嵌套对象）中的所有键值对进行索引。
扁平化和类型推断如何工作
当你在对象路径上创建一个 JSON 扁平化索引时，Milvus 将：
扁平化
- 从指定的
json_path
开始递归遍历对象，并将嵌套的键值对提取为完全限定路径。使用先前的
metadata
示例：
"metadata"
:
{
"category"
:
"electronics"
,
"price"
:
99.99
,
"supplier"
:
{
"country"
:
"USA"
}
}
成为：
metadata["category"] = "electronics"
metadata["price"] = 99.99
metadata["supplier"]["country"] = "USA"
自动推断类型
- 对于每个值，Milvus 会按以下顺序确定其类型：
unsigned integer → signed integer → floating-point → string
第一个符合值的类型将用于索引。
这意味着推断出的类型总是
这四种类型之一
。
类型推断是
按文档
进行的，因此同一路径在不同文档中可能有不同的推断类型。
例如，在类型推断之后，扁平化数据在内部表示为带有推断类型的术语：
("category", Text, "electronics")
("price", Double, 99.99)
("supplier.country", Text, "USA")
例如创建 JSON 扁平化索引
Python
Java
NodeJS
Go
cURL
# 1. Create a flat index on the root object of the JSON column (covers the entire JSON subtree)
index_params.add_index(
    field_name=
"metadata"
,
    index_type=
"AUTOINDEX"
,
# Or "INVERTED", same as Path Index
index_name=
"metadata_flat"
,
# Unique index name
params={
"json_path"
:
'metadata'
,
# Object path: the root object of the column
"json_cast_type"
:
"JSON"
# Key difference: must be "JSON" for Flat Index; case-insensitive
}
)
# 2. Optionally, create a flat index on a sub-object (e.g., supplier subtree)
index_params.add_index(
    field_name=
"metadata"
,
    index_type=
"AUTOINDEX"
,
    index_name=
"metadata_supplier_flat"
,
    params={
"json_path"
:
'metadata["supplier"]'
,
# Object path: sub-object path
"json_cast_type"
:
"JSON"
}
)
// java
// nodejs
// go
# restful
向 Collections 应用索引
定义索引参数后，可以使用
create_index()
将其应用到 Collections 中：
Python
Java
NodeJS
Go
cURL
client.create_index(
    collection_name=
"product_catalog"
,
    index_params=index_params
)
import
io.milvus.v2.service.index.request.CreateIndexReq;

client.createIndex(CreateIndexReq.builder()
        .collectionName(
"product_catalog"
)
        .indexParams(indexParams)
        .build());
await
client.
createIndex
(indexParams)
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
# restful
export
indexParams=
"[
$categoryIndex
,
$tagsArrayIndex
,
$stringToDoubleIndex
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
  \"collectionName\": \"product_catalog\",
  \"indexParams\":
$indexParams
}"
按 JSON 字段值过滤
在插入 JSON 字段并建立索引后，可以使用 JSON 路径语法的标准过滤表达式对其进行过滤。
例如
Python
Java
NodeJS
Go
cURL
filter
=
'metadata["category"] == "electronics"'
filter
=
'metadata["price"] > 50'
filter
=
'json_contains(metadata["tags"], "featured")'
String
filter
=
'metadata["category"] == "electronics"'
;
String
filter
=
'metadata["price"] > 50'
;
String
filter
=
'json_contains(metadata["tags"], "featured")'
;
let
filter =
'metadata["category"] == "electronics"'
let
filter =
'metadata["price"] > 50'
let
filter =
'json_contains(metadata["tags"], "featured")'
filter :=
'metadata["category"] == "electronics"'
filter :=
'metadata["price"] > 50'
filter :=
'json_contains(metadata["tags"], "featured")'
# restful
export
filterCategory=
'metadata["category"] == "electronics"'
export
filterPrice=
'metadata["price"] > 50'
export
filterTags=
'json_contains(metadata["tags"], "featured")'
要在搜索或查询中使用这些表达式，请确保
已在每个向量字段上创建索引。
Collections 已加载到内存中。
有关支持的操作符和表达式的完整列表，请参阅
JSON 操作符
。
将所有内容整合在一起
至此，您已经学会了如何在 JSON 字段中定义、插入结构化值并为其建立索引。
要在实际应用中完成工作流程，您还需要
为您的向量字段创建索引
（必须为 Collections 中的每个向量字段
创建索引）
请参阅
设置索引参数
加载 Collections
请参阅
加载和发布
使用 JSON 路径过滤器进行搜索或查询
请参阅
过滤搜索
和
JSON 操作符
常见问题
JSON 字段与动态字段有何不同？
JSON 字段
是 Schema 定义的。您必须在 Schema 中明确声明字段。
动态字段
是一个隐藏的 JSON 对象 (
$meta
) ，可自动存储模式中未定义的任何字段。
两者都支持嵌套结构和 JSON 路径索引，但动态字段更适合可选或不断演化的数据结构。
详情请参阅
动态
字段。
JSON 字段的大小有限制吗？
有。每个 JSON 字段的大小限制为 65,536 字节。
JSON 字段是否支持设置默认值？
不，JSON 字段不支持默认值。不过，您可以在定义字段时设置
nullable=True
，以允许空条目。
有关详情，请参阅 "
可为空和默认值
"。
JSON 字段键有任何命名约定吗？
有，以确保与查询和索引的兼容性：
JSON 键只能使用字母、数字和下划线。
避免使用特殊字符、空格或点（
.
,
/
等）。
不兼容的键可能会导致过滤表达式出现解析问题。
Milvus 如何处理 JSON 字段中的字符串值？
Milvus 完全按照 JSON 输入中的字符串值进行存储，不进行语义转换。引号不当的字符串可能会在解析过程中导致错误。
有效字符串示例
"a\"b", "a'b", "a\\b"
无效字符串示例
'a"b', 'a\'b'
Milvus 对索引的 JSON 路径使用什么过滤逻辑？
数字索引
：
如果使用
json_cast_type="double"
创建索引，则只有数字过滤条件（如
>
,
<
,
== 42
）才会利用该索引。非数字条件可能会退回到暴力扫描。
字符串索引
：
如果索引使用
json_cast_type="varchar"
，则只有字符串过滤条件可从索引中获益；其他类型可能会退回到暴力扫描。
布尔索引
：
布尔索引的行为与字符串索引类似，只有当条件严格匹配真或假时，才会使用索引。
索引 JSON 字段时的数字精度如何？
Milvus 将所有索引数值存储为双倍。
如果数值超过
2^53
，可能会失去精度。这种精度损失可能导致过滤查询无法精确匹配超出范围的值。
能否在同一 JSON 路径上创建具有不同铸型的多个索引？
不能，每个 JSON 路径
只
支持
一个索引
。您必须选择一个与您的数据相匹配的
json_cast_type
。不支持在同一路径上创建多个不同类型的索引。
如果 JSON 路径上的值类型不一致怎么办？
实体间类型不一致会导致
部分索引
。例如，如果
metadata["price"]
同时以数字 (
99.99
) 和字符串 (
"99.99"
) 的形式存储，而索引是以
json_cast_type="double"
定义的，则只有数字值会被索引。字符串形式的条目将被跳过，不会出现在筛选结果中。
能否使用与索引铸型类型不同的过滤器？
如果您的筛选表达式使用的类型与索引的
json_cast_type
不同，系统将
不会使用索引
，如果数据允许，可能会退回到较慢的暴力扫描。为获得最佳性能，请务必使您的过滤表达式与索引的类型保持一致。