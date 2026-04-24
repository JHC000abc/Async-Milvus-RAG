字符串字段
在 Milvus 中，
VARCHAR
是用于存储字符串数据的数据类型。
定义
VARCHAR
字段时，有两个参数是必须的：
将
datatype
设置为
DataType.VARCHAR
。
指定
max_length
，它定义了
VARCHAR
字段可存储的最大字节数。
max_length
的有效范围为 1 至 65,535 字节。
Milvus 支持
VARCHAR
字段的空值和默认值。要启用这些功能，可将
nullable
设置为
True
，将
default_value
设置为字符串值。有关详情，请参阅
可空值和默认值
。
添加 VARCHAR 字段
要在 Milvus 中存储字符串数据，请在 Collections Schema 中定义一个
VARCHAR
字段。下面是一个定义了两个
VARCHAR
字段的 Collections 模式的示例：
varchar_field1
VARCHAR：最多存储 100 字节，允许空值，默认值为
"Unknown"
。
varchar_field2
：字段最多存储 200 字节，允许空值，但没有默认值。
如果在定义 Schema 时设置
enable_dynamic_fields=True
，Milvus 允许插入事先未定义的标量字段。不过，这可能会增加查询和管理的复杂性，并可能影响性能。有关详细信息，请参阅
动态字段
。
Python
Java
NodeJS
Go
cURL
# Import necessary libraries
from
pymilvus
import
MilvusClient, DataType
# Define server address
SERVER_ADDR =
"http://localhost:19530"
# Create a MilvusClient instance
client = MilvusClient(uri=SERVER_ADDR)
# Define the collection schema
schema = client.create_schema(
    auto_id=
False
,
    enable_dynamic_fields=
True
,
)
# Add `varchar_field1` that supports null values with default value "Unknown"
schema.add_field(field_name=
"varchar_field1"
, datatype=DataType.VARCHAR, max_length=
100
, nullable=
True
, default_value=
"Unknown"
)
# Add `varchar_field2` that supports null values without default value
schema.add_field(field_name=
"varchar_field2"
, datatype=DataType.VARCHAR, max_length=
200
, nullable=
True
)
schema.add_field(field_name=
"pk"
, datatype=DataType.INT64, is_primary=
True
)
schema.add_field(field_name=
"embedding"
, datatype=DataType.FLOAT_VECTOR, dim=
3
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
        .build());
        
CreateCollectionReq.
CollectionSchema
schema
=
client.createSchema();
schema.setEnableDynamicField(
true
);

schema.addField(AddFieldReq.builder()
        .fieldName(
"varchar_field1"
)
        .dataType(DataType.VarChar)
        .maxLength(
100
)
        .isNullable(
true
)
        .defaultValue(
"Unknown"
)
        .build());

schema.addField(AddFieldReq.builder()
        .fieldName(
"varchar_field2"
)
        .dataType(DataType.VarChar)
        .maxLength(
200
)
        .isNullable(
true
)
        .build());

schema.addField(AddFieldReq.builder()
        .fieldName(
"pk"
)
        .dataType(DataType.Int64)
        .isPrimaryKey(
true
)
        .build());

schema.addField(AddFieldReq.builder()
        .fieldName(
"embedding"
)
        .dataType(DataType.FloatVector)
        .dimension(
3
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
client =
new
MilvusClient
({
address
:
`http://localhost:19530`
});
const
schema = [
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
  },
  {
name
:
"pk"
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
  },
  {
name
:
"varchar_field2"
,
data_type
:
DataType
.
VarChar
,
max_length
:
200
,
  },
  {
name
:
"varchar_field1"
,
data_type
:
DataType
.
VarChar
,
max_length
:
100
,
  },
];
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

schema := entity.NewSchema()
schema.WithField(entity.NewField().
    WithName(
"pk"
).
    WithDataType(entity.FieldTypeInt64).
    WithIsPrimaryKey(
true
),
).WithField(entity.NewField().
    WithName(
"embedding"
).
    WithDataType(entity.FieldTypeFloatVector).
    WithDim(
3
),
).WithField(entity.NewField().
    WithName(
"varchar_field1"
).
    WithDataType(entity.FieldTypeVarChar).
    WithMaxLength(
100
).
    WithNullable(
true
).
    WithDefaultValueString(
"Unknown"
),
).WithField(entity.NewField().
    WithName(
"varchar_field2"
).
    WithDataType(entity.FieldTypeVarChar).
    WithMaxLength(
200
).
    WithNullable(
true
),
)
export
varcharField1=
'{
    "fieldName": "varchar_field1",
    "dataType": "VarChar",
    "elementTypeParams": {
        "max_length": 100
    },
    "nullable": true
}'
export
varcharField2=
'{
    "fieldName": "varchar_field2",
    "dataType": "VarChar",
    "elementTypeParams": {
        "max_length": 200
    },
    "nullable": true
}'
export
primaryField=
'{
    "fieldName": "pk",
    "dataType": "Int64",
    "isPrimary": true
}'
export
vectorField=
'{
    "fieldName": "embedding",
    "dataType": "FloatVector",
    "elementTypeParams": {
        "dim": 3
    }
}'
export
schema=
"{
    \"autoID\": false,
    \"fields\": [
$varcharField1
,
$varcharField2
,
$primaryField
,
$vectorField
]
}"
设置索引参数
索引有助于提高搜索和查询性能。在 Milvus 中，对于向量字段必须建立索引，但对于标量字段可选。
下面的示例使用
AUTOINDEX
索引类型为向量字段
embedding
和标量字段
varchar_field1
创建了索引。使用这种类型，Milvus 会根据数据类型自动选择最合适的索引。您还可以自定义每个字段的索引类型和参数。详情请参阅 "
索引说明"
。
您还可以建立
NGRAM
索引，以加速对
VARCHAR
字段的
LIKE
过滤。有关详情，请参阅
NGRAM
。
Python
Java
Go
NodeJS
cURL
# Set index params
index_params = client.prepare_index_params()
# Index `varchar_field1` with AUTOINDEX
index_params.add_index(
    field_name=
"varchar_field1"
,
    index_type=
"AUTOINDEX"
,
    index_name=
"varchar_index"
)
# Index `embedding` with AUTOINDEX and specify metric_type
index_params.add_index(
    field_name=
"embedding"
,
    index_type=
"AUTOINDEX"
,
# Use automatic indexing to simplify complex index settings
metric_type=
"COSINE"
# Specify similarity metric type, options include L2, COSINE, or IP
)
import
io.milvus.v2.common.IndexParam;
import
java.util.*;

List<IndexParam> indexes =
new
ArrayList
<>();
indexes.add(IndexParam.builder()
        .fieldName(
"varchar_field1"
)
        .indexName(
"varchar_index"
)
        .indexType(IndexParam.IndexType.AUTOINDEX)
        .build());
        
indexes.add(IndexParam.builder()
        .fieldName(
"embedding"
)
        .indexType(IndexParam.IndexType.AUTOINDEX)
        .metricType(IndexParam.MetricType.COSINE)
        .build());
indexOption1 := milvusclient.NewCreateIndexOption(
"my_collection"
,
"embedding"
,
    index.NewAutoIndex(index.MetricType(entity.IP)))
indexOption2 := milvusclient.NewCreateIndexOption(
"my_collection"
,
"varchar_field1"
,
    index.NewInvertedIndex())
const
indexParams = [{
index_name
:
'varchar_index'
,
field_name
:
'varchar_field1'
,
index_type
:
IndexType
.
AUTOINDEX
,
)];

indexParams.
push
({
index_name
:
'embedding_index'
,
field_name
:
'embedding'
,
metric_type
:
MetricType
.
COSINE
,
index_type
:
IndexType
.
AUTOINDEX
,
});
export
indexParams=
'[
        {
            "fieldName": "varchar_field1",
            "indexName": "varchar_index",
            "indexType": "AUTOINDEX"
        }
    ]'
export
indexParams=
'[
        {
            "fieldName": "varchar_field1",
            "indexName": "varchar_index",
            "indexType": "AUTOINDEX"
        },
        {
            "fieldName": "embedding",
            "metricType": "COSINE",
            "indexType": "AUTOINDEX"
        }
    ]'
创建 Collections
定义好 Schema 和索引后，创建一个包含字符串字段的 Collection。
Python
Java
Go
NodeJS
cURL
# Create Collection
client.create_collection(
    collection_name=
"my_collection"
,
    schema=schema,
    index_params=index_params
)
CreateCollectionReq
requestCreate
=
CreateCollectionReq.builder()
        .collectionName(
"my_collection"
)
        .collectionSchema(schema)
        .indexParams(indexes)
        .build();
client.createCollection(requestCreate);
err = client.CreateCollection(ctx,
    milvusclient.NewCreateCollectionOption(
"my_collection"
, schema).
        WithIndexOptions(indexOption1, indexOption2))
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
index_params
: index_params
});
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
    \"indexParams\":
$indexParams
}"
## {"code":0,"data":{}}
插入数据
创建 Collections 后，插入与 Schema 匹配的实体。
Python
Java
Go
NodeJS
cURL
# Sample data
data = [
    {
"varchar_field1"
:
"Product A"
,
"varchar_field2"
:
"High quality product"
,
"pk"
:
1
,
"embedding"
: [
0.1
,
0.2
,
0.3
]},
    {
"varchar_field1"
:
"Product B"
,
"pk"
:
2
,
"embedding"
: [
0.4
,
0.5
,
0.6
]},
# varchar_field2 field is missing, which should be NULL
{
"varchar_field1"
:
None
,
"varchar_field2"
:
None
,
"pk"
:
3
,
"embedding"
: [
0.2
,
0.3
,
0.1
]},
# `varchar_field1` should default to `Unknown`, `varchar_field2` is NULL
{
"varchar_field1"
:
"Product C"
,
"varchar_field2"
:
None
,
"pk"
:
4
,
"embedding"
: [
0.5
,
0.7
,
0.2
]},
# `varchar_field2` is NULL
{
"varchar_field1"
:
None
,
"varchar_field2"
:
"Exclusive deal"
,
"pk"
:
5
,
"embedding"
: [
0.6
,
0.4
,
0.8
]},
# `varchar_field1` should default to `Unknown`
{
"varchar_field1"
:
"Unknown"
,
"varchar_field2"
:
None
,
"pk"
:
6
,
"embedding"
: [
0.8
,
0.5
,
0.3
]},
# `varchar_field2` is NULL
{
"varchar_field1"
:
""
,
"varchar_field2"
:
"Best seller"
,
"pk"
:
7
,
"embedding"
: [
0.8
,
0.5
,
0.3
]},
# Empty string is not treated as NULL
]
# Insert data
client.insert(
    collection_name=
"my_collection"
,
    data=data
)
import
com.google.gson.Gson;
import
com.google.gson.JsonObject;
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
rows.add(gson.fromJson(
"{\"varchar_field1\": \"Product A\", \"varchar_field2\": \"High quality product\", \"pk\": 1, \"embedding\": [0.1, 0.2, 0.3]}"
, JsonObject.class));
rows.add(gson.fromJson(
"{\"varchar_field1\": \"Product B\", \"pk\": 2, \"embedding\": [0.4, 0.5, 0.6]}"
, JsonObject.class));
rows.add(gson.fromJson(
"{\"varchar_field1\": null, \"varchar_field2\": null, \"pk\": 3, \"embedding\": [0.2, 0.3, 0.1]}"
, JsonObject.class));
rows.add(gson.fromJson(
"{\"varchar_field1\": \"Product C\", \"varchar_field2\": null, \"pk\": 4, \"embedding\": [0.5, 0.7, 0.2]}"
, JsonObject.class));
rows.add(gson.fromJson(
"{\"varchar_field1\": null, \"varchar_field2\": \"Exclusive deal\", \"pk\": 5, \"embedding\": [0.6, 0.4, 0.8]}"
, JsonObject.class));
rows.add(gson.fromJson(
"{\"varchar_field1\": \"Unknown\", \"varchar_field2\": null, \"pk\": 6, \"embedding\": [0.8, 0.5, 0.3]}"
, JsonObject.class));
rows.add(gson.fromJson(
"{\"varchar_field1\": \"\", \"varchar_field2\": \"Best seller\", \"pk\": 7, \"embedding\": [0.8, 0.5, 0.3]}"
, JsonObject.class));
InsertResp
insertR
=
client.insert(InsertReq.builder()
        .collectionName(
"my_collection"
)
        .data(rows)
        .build());
column1, _ := column.NewNullableColumnVarChar(
"varchar_field1"
,
    []
string
{
"Product A"
,
"Product B"
,
"Product C"
,
"Unknown"
,
""
},
    []
bool
{
true
,
true
,
false
,
true
,
false
,
true
,
true
})
column2, _ := column.NewNullableColumnVarChar(
"varchar_field2"
,
    []
string
{
"High quality product"
,
"Exclusive deal"
,
"Best seller"
},
    []
bool
{
true
,
false
,
false
,
false
,
true
,
false
,
true
})

_, err = client.Insert(ctx, milvusclient.NewColumnBasedInsertOption(
"my_collection"
).
    WithInt64Column(
"pk"
, []
int64
{
1
,
2
,
3
,
4
,
5
,
6
,
7
}).
    WithFloatVectorColumn(
"embedding"
,
3
, [][]
float32
{
        {
0.1
,
0.2
,
0.3
},
        {
0.4
,
0.5
,
0.6
},
        {
0.2
,
0.3
,
0.1
},
        {
0.5
,
0.7
,
0.2
},
        {
0.6
,
0.4
,
0.8
},
        {
0.8
,
0.5
,
0.3
},
        {
0.8
,
0.5
,
0.3
},
    }).
    WithColumns(column1, column2),
)
if
err !=
nil
{
    fmt.Println(err.Error())
// handle err
}
const
data = [
  {
varchar_field1
:
"Product A"
,
varchar_field2
:
"High quality product"
,
pk
:
1
,
embedding
: [
0.1
,
0.2
,
0.3
],
  },
  {
varchar_field1
:
"Product B"
,
varchar_field2
:
"Affordable price"
,
pk
:
2
,
embedding
: [
0.4
,
0.5
,
0.6
],
  },
  {
varchar_field1
:
"Product C"
,
varchar_field2
:
"Best seller"
,
pk
:
3
,
embedding
: [
0.7
,
0.8
,
0.9
],
  },
];
await
client.
insert
({
collection_name
:
"my_collection"
,
data
: data,
});
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
        {"varchar_field1": "Product A", "varchar_field2": "High quality product", "pk": 1, "embedding": [0.1, 0.2, 0.3]},
        {"varchar_field1": "Product B", "pk": 2, "embedding": [0.4, 0.5, 0.6]},
        {"varchar_field1": null, "varchar_field2": null, "pk": 3, "embedding": [0.2, 0.3, 0.1]},  
        {"varchar_field1": "Product C", "varchar_field2": null, "pk": 4, "embedding": [0.5, 0.7, 0.2]},  
        {"varchar_field1": null, "varchar_field2": "Exclusive deal", "pk": 5, "embedding": [0.6, 0.4, 0.8]},  
        {"varchar_field1": "Unknown", "varchar_field2": null, "pk": 6, "embedding": [0.8, 0.5, 0.3]},  
        {"varchar_field1": "", "varchar_field2": "Best seller", "pk": 7, "embedding": [0.8, 0.5, 0.3]}  
    ],
    "collectionName": "my_collection"
}'
## {"code":0,"cost":0,"data":{"insertCount":3,"insertIds":[1,2,3]}}
使用过滤表达式查询
插入实体后，使用
query
方法检索与指定过滤表达式匹配的实体。
要检索
varchar_field1
与字符串
"Product A"
匹配的实体：
Python
Java
Go
NodeJS
cURL
# Filter `varchar_field1` with value "Product A"
filter
=
'varchar_field1 == "Product A"'
res = client.query(
    collection_name=
"my_collection"
,
filter
=
filter
,
    output_fields=[
"varchar_field1"
,
"varchar_field2"
]
)
print
(res)
# Example output:
# data: [
#     "{'varchar_field1': 'Product A', 'varchar_field2': 'High quality product', 'pk': 1}"
# ]
import
io.milvus.v2.service.vector.request.QueryReq;
import
io.milvus.v2.service.vector.response.QueryResp;
String
filter
=
"varchar_field1 == \"Product A\""
;
QueryResp
resp
=
client.query(QueryReq.builder()
        .collectionName(
"my_collection"
)
        .filter(filter)
        .outputFields(Arrays.asList(
"varchar_field1"
,
"varchar_field2"
))
        .build());

System.out.println(resp.getQueryResults());
// Output
//
// [QueryResp.QueryResult(entity={varchar_field1=Product A, varchar_field2=High quality product, pk=1})]
filter :=
"varchar_field1 == \"Product A\""
queryResult, err := client.Query(ctx, milvusclient.NewQueryOption(
"my_collection"
).
    WithFilter(filter).
    WithOutputFields(
"varchar_field1"
,
"varchar_field2"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(
"varchar_field1"
, queryResult.GetColumn(
"varchar_field1"
).FieldData().GetScalars())
fmt.Println(
"varchar_field2"
, queryResult.GetColumn(
"varchar_field2"
).FieldData().GetScalars())
// Output
//
// varchar_field1 string_data:{data:"Product A"}
// varchar_field2 string_data:{data:"High quality product"}
await
client.
query
({
collection_name
:
'my_collection'
,
filter
:
'varchar_field1 == "Product A"'
,
output_fields
: [
'varchar_field1'
,
'varchar_field2'
]
});
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/entities/query"
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
    "filter": "varchar_field1 == \"Product A\"",
    "outputFields": ["varchar_field1", "varchar_field2"]
}'
## {"code":0,"cost":0,"data":[{"pk":1,"varchar_field1":"Product A","varchar_field2":"High quality product"}]}
检索
varchar_field2
为空的实体：
Python
Java
Go
NodeJS
cURL
# Filter entities where `varchar_field2` is null
filter
=
'varchar_field2 is null'
res = client.query(
    collection_name=
"my_collection"
,
filter
=
filter
,
    output_fields=[
"varchar_field1"
,
"varchar_field2"
]
)
print
(res)
# Example output:
# data: [
#     "{'varchar_field1': 'Product B', 'varchar_field2': None, 'pk': 2}",
#     "{'varchar_field1': 'Unknown', 'varchar_field2': None, 'pk': 3}",
#     "{'varchar_field1': 'Product C', 'varchar_field2': None, 'pk': 4}",
#     "{'varchar_field1': 'Unknown', 'varchar_field2': None, 'pk': 6}"
# ]
String
filter
=
"varchar_field2 is null"
;
QueryResp
resp
=
client.query(QueryReq.builder()
        .collectionName(
"my_collection"
)
        .filter(filter)
        .outputFields(Arrays.asList(
"varchar_field1"
,
"varchar_field2"
))
        .build());

System.out.println(resp.getQueryResults());
// Output
//
// [
//    QueryResp.QueryResult(entity={varchar_field1=Product B, varchar_field2=null, pk=2}),
//    QueryResp.QueryResult(entity={varchar_field1=Unknown, varchar_field2=null, pk=3}),
//    QueryResp.QueryResult(entity={varchar_field1=Product C, varchar_field2=null, pk=4}),
//    QueryResp.QueryResult(entity={varchar_field1=Unknown, varchar_field2=null, pk=6})
// ]
filter =
"varchar_field2 is null"
queryResult, err = client.Query(ctx, milvusclient.NewQueryOption(
"my_collection"
).
    WithFilter(filter).
    WithOutputFields(
"varchar_field1"
,
"varchar_field2"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(
"varchar_field1"
, queryResult.GetColumn(
"varchar_field1"
))
fmt.Println(
"varchar_field2"
, queryResult.GetColumn(
"varchar_field2"
))
await
client.
query
({
collection_name
:
'my_collection'
,
filter
:
'varchar_field2 is null'
,
output_fields
: [
'varchar_field1'
,
'varchar_field2'
]
});
# restful
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/entities/query"
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
    "filter": "varchar_field2 is null",
    "outputFields": ["varchar_field1", "varchar_field2"]
}'
要检索
varchar_field1
的值为
"Unknown"
的实体，请使用下面的表达式。由于
varchar_field1
的默认值是
"Unknown"
，因此预期结果应包括将
varchar_field1
明确设置为
"Unknown"
或将
varchar_field1
设置为空的实体。
Python
Java
Go
NodeJS
cURL
# Filter entities with `varchar_field1` with value `Unknown`
filter
=
'varchar_field1 == "Unknown"'
res = client.query(
    collection_name=
"my_collection"
,
filter
=
filter
,
    output_fields=[
"varchar_field1"
,
"varchar_field2"
]
)
print
(res)
# Example output:
# data: [
#     "{'varchar_field1': 'Unknown', 'varchar_field2': None, 'pk': 3}",
#     "{'varchar_field1': 'Unknown', 'varchar_field2': 'Exclusive deal', 'pk': 5}",
#     "{'varchar_field1': 'Unknown', 'varchar_field2': None, 'pk': 6}"
# ]
String
filter
=
"varchar_field1 == \"Unknown\""
;
QueryResp
resp
=
client.query(QueryReq.builder()
        .collectionName(
"my_collection"
)
        .filter(filter)
        .outputFields(Arrays.asList(
"varchar_field1"
,
"varchar_field2"
))
        .build());

System.out.println(resp.getQueryResults());
// Output
//
// [
//    QueryResp.QueryResult(entity={varchar_field1=Unknown, varchar_field2=null, pk=3}),
//    QueryResp.QueryResult(entity={varchar_field1=Unknown, varchar_field2=Exclusive deal, pk=5}),
//    QueryResp.QueryResult(entity={varchar_field1=Unknown, varchar_field2=null, pk=6})
// ]
filter =
"varchar_field1 == \"Unknown\""
queryResult, err = client.Query(ctx, milvusclient.NewQueryOption(
"my_collection"
).
    WithFilter(filter).
    WithOutputFields(
"varchar_field1"
,
"varchar_field2"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(
"varchar_field1"
, queryResult.GetColumn(
"varchar_field1"
))
fmt.Println(
"varchar_field2"
, queryResult.GetColumn(
"varchar_field2"
))
// node
await
client.
query
({
collection_name
:
'my_collection'
,
filter
:
'varchar_field1 == "Unknown"'
,
output_fields
: [
'varchar_field1'
,
'varchar_field2'
]
});
# restful
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/entities/query"
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
    "filter": "varchar_field1 == \"Unknown\"",
    "outputFields": ["varchar_field1", "varchar_field2"]
}'
使用过滤表达式进行向量搜索
除了基本的标量字段筛选外，您还可以将向量相似性搜索与标量字段筛选结合起来。例如，下面的代码展示了如何在向量搜索中添加标量字段过滤器：
Python
Java
Go
NodeJS
cURL
# Search with string filtering
# Filter `varchar_field2` with value "Best seller"
filter
=
'varchar_field2 == "Best seller"'
res = client.search(
    collection_name=
"my_collection"
,
    data=[[
0.3
, -
0.6
,
0.1
]],
    limit=
5
,
    search_params={
"params"
: {
"nprobe"
:
10
}},
    output_fields=[
"varchar_field1"
,
"varchar_field2"
],
filter
=
filter
)
print
(res)
# Example output:
# data: [
#     "[{'id': 7, 'distance': -0.04468163847923279, 'entity': {'varchar_field1': '', 'varchar_field2': 'Best seller'}}]"
# ]
import
io.milvus.v2.service.vector.request.SearchReq;
import
io.milvus.v2.service.vector.response.SearchResp;
String
filter
=
"varchar_field2 == \"Best seller\""
;
SearchResp
resp
=
client.search(SearchReq.builder()
        .collectionName(
"my_collection"
)
        .annsField(
"embedding"
)
        .data(Collections.singletonList(
new
FloatVec
(
new
float
[]{
0.3f
, -
0.6f
,
0.1f
})))
        .topK(
5
)
        .outputFields(Arrays.asList(
"varchar_field1"
,
"varchar_field2"
))
        .filter(filter)
        .build());

System.out.println(resp.getSearchResults());
// Output
//
// [[SearchResp.SearchResult(entity={varchar_field1=, varchar_field2=Best seller}, score=-0.04468164, id=7)]]
queryVector := []
float32
{
0.3
,
-0.6
,
0.1
}
filter =
"varchar_field2 == \"Best seller\""
annParam := index.NewCustomAnnParam()
annParam.WithExtraParam(
"nprobe"
,
10
)
resultSets, err := client.Search(ctx, milvusclient.NewSearchOption(
"my_collection"
,
// collectionName
5
,
// limit
[]entity.Vector{entity.FloatVector(queryVector)},
).WithANNSField(
"embedding"
).
    WithFilter(filter).
    WithAnnParam(annParam).
    WithOutputFields(
"varchar_field1"
,
"varchar_field2"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
for
_, resultSet :=
range
resultSets {
    fmt.Println(
"IDs: "
, resultSet.IDs.FieldData().GetScalars())
    fmt.Println(
"Scores: "
, resultSet.Scores)
    fmt.Println(
"varchar_field1: "
, resultSet.GetColumn(
"varchar_field1"
))
    fmt.Println(
"varchar_field2: "
, resultSet.GetColumn(
"varchar_field2"
))
}
await
client.
search
({
collection_name
:
'my_collection'
,
data
: [
0.3
, -
0.6
,
0.1
],
limit
:
5
,
output_fields
: [
'varchar_field1'
,
'varchar_field2'
],
filter
:
'varchar_field2 == "Best seller"'
params
: {
nprobe
:
10
}
});
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
-d
'{
    "collectionName": "my_collection",
    "data": [
        [0.3, -0.6, 0.1]
    ],
    "limit": 5,
    "searchParams":{
        "params":{"nprobe":10}
    },
    "outputFields": ["varchar_field1", "varchar_field2"],
    "filter": "varchar_field2 == \"Best seller\""
}'
## {"code":0,"cost":0,"data":[{"distance":-0.2364331,"id":1,"varchar_field1":"Product A","varchar_field2":"High quality product"}]}