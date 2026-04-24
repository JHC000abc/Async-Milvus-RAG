数字字段
数字字段是一种存储数值的标量字段。这些数值可以是
整数（整数
）或十进制数
（浮点数
）。它们通常用于表示数量、测量值或任何需要进行数学处理的数据。
下表描述了 Milvus 中可用的数字字段数据类型。
字段类型
描述
BOOL
布尔类型，用于存储
true
或
false
，适合描述二进制状态。
INT8
8 位整数，适合存储小范围整数数据。
INT16
16 位整数，适用于中范围整数数据。
INT32
32 位整数，适合存储一般整数数据，如产品数量或用户 ID。
INT64
64 位整数，适合存储时间戳或标识符等大范围数据。
FLOAT
32 位浮点数，适用于需要一般精度的数据，如等级或温度。
DOUBLE
64 位双精度浮点数，用于高精度数据，如财务信息或科学计算。
要声明数字字段，只需将
datatype
设置为可用的数字数据类型之一。例如，
DataType.INT64
表示整数字段，
DataType.FLOAT
表示浮点字段。
Milvus 支持数字字段的空值和默认值。要启用这些功能，请将
nullable
设置为
True
，将
default_value
设置为数值。有关详情，请参阅
可空值和默认值
。
添加数字字段
要存储数值数据，请在 Collections Schema 中定义一个数字字段。下面是一个包含两个数字字段的 Collections 模式示例：
age
：存储整数数据，允许空值，默认值为
18
。
price
：存储浮点数据，允许空值，但没有默认值。
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
# Add an INT64 field `age` that supports null values with default value 18
schema.add_field(field_name=
"age"
, datatype=DataType.INT64, nullable=
True
, default_value=
18
)
# Add a FLOAT field `price` that supports null values without default value
schema.add_field(field_name=
"price"
, datatype=DataType.FLOAT, nullable=
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
"age"
)
        .dataType(DataType.Int64)
        .isNullable(
true
)
        .defaultValue(
18
)
        .build());

schema.addField(AddFieldReq.builder()
        .fieldName(
"price"
)
        .dataType(DataType.Float)
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
schema = [
  {
name
:
"age"
,
data_type
:
DataType
.
Int64
,
  },
  {
name
:
"price"
,
data_type
:
DataType
.
Float
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
"embedding"
,
data_type
:
DataType
.
FloatVector
,
dim
:
3
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
"price"
).
    WithDataType(entity.FieldTypeFloat).
    WithNullable(
true
),
).WithField(entity.NewField().
    WithName(
"age"
).
    WithDataType(entity.FieldTypeInt64).
    WithNullable(
true
).
    WithDefaultValueLong(
18
),
)
export
int64Field=
'{
    "fieldName": "age",
    "dataType": "Int64"
}'
export
floatField=
'{
    "fieldName": "price",
    "dataType": "Float"
}'
export
pkField=
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
$int64Field
,
$floatField
,
$pkField
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
age
创建了索引。使用这种类型，Milvus 会根据数据类型自动选择最合适的索引。您还可以自定义每个字段的索引类型和参数。有关详情，请参阅
索引说明
。
Python
Java
NodeJS
Go
cURL
# Set index params
index_params = client.prepare_index_params()
# Index `age` with AUTOINDEX
index_params.add_index(
    field_name=
"age"
,
    index_type=
"AUTOINDEX"
,
    index_name=
"age_index"
)
# Index `embedding` with AUTOINDEX and specify similarity metric type
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
"age"
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
import
{
IndexType
}
from
"@zilliz/milvus2-sdk-node"
;
const
indexParams = [
  {
field_name
:
"age"
,
index_name
:
"inverted_index"
,
index_type
:
IndexType
.
AUTOINDEX
,
  },
  {
field_name
:
"embedding"
,
metric_type
:
"COSINE"
,
index_type
:
IndexType
.
AUTOINDEX
,
  },
];
indexOption1 := milvusclient.NewCreateIndexOption(
"my_collection"
,
"embedding"
,
    index.NewAutoIndex(index.MetricType(entity.IP)))
indexOption2 := milvusclient.NewCreateIndexOption(
"my_collection"
,
"age"
,
    index.NewInvertedIndex())
export
indexParams=
'[
        {
            "fieldName": "age",
            "indexName": "inverted_index",
            "indexType": "AUTOINDEX"
        },
        {
            "fieldName": "embedding",
            "metricType": "COSINE",
            "indexType": "AUTOINDEX"
        }
    ]'
创建 Collections
定义好 Schema 和索引后，创建一个包含数字字段的 Collection。
Python
Java
NodeJS
Go
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
: indexParams
})
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
插入数据
创建 Collections 后，插入与 Schema 匹配的实体。
Python
Java
NodeJS
Go
cURL
# Sample data
data = [
    {
"age"
:
25
,
"price"
:
99.99
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
"age"
:
30
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
# `price` field is missing, which should be null
{
"age"
:
None
,
"price"
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
# `age` should default to 18, `price` is null
{
"age"
:
45
,
"price"
:
None
,
"pk"
:
4
,
"embedding"
: [
0.9
,
0.1
,
0.4
]},
# `price` is null
{
"age"
:
None
,
"price"
:
59.99
,
"pk"
:
5
,
"embedding"
: [
0.8
,
0.5
,
0.3
]},
# `age` should default to 18
{
"age"
:
60
,
"price"
:
None
,
"pk"
:
6
,
"embedding"
: [
0.1
,
0.6
,
0.9
]}
# `price` is null
]

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
"{\"age\": 25, \"price\": 99.99, \"pk\": 1, \"embedding\": [0.1, 0.2, 0.3]}"
, JsonObject.class));
rows.add(gson.fromJson(
"{\"age\": 30, \"pk\": 2, \"embedding\": [0.4, 0.5, 0.6]}"
, JsonObject.class));
rows.add(gson.fromJson(
"{\"age\": null, \"price\": null, \"pk\": 3, \"embedding\": [0.2, 0.3, 0.1]}"
, JsonObject.class));
rows.add(gson.fromJson(
"{\"age\": 45, \"price\": null, \"pk\": 4, \"embedding\": [0.9, 0.1, 0.4]}"
, JsonObject.class));
rows.add(gson.fromJson(
"{\"age\": null, \"price\": 59.99, \"pk\": 5, \"embedding\": [0.8, 0.5, 0.3]}"
, JsonObject.class));
rows.add(gson.fromJson(
"{\"age\": 60, \"price\": null, \"pk\": 6, \"embedding\": [0.1, 0.6, 0.9]}"
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
const
data = [
  {
age
:
25
,
price
:
99.99
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
] },
  {
age
:
30
,
price
:
149.5
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
] },
  {
age
:
35
,
price
:
199.99
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
] },
];

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
column1, _ := column.NewNullableColumnFloat(
"price"
,
    []
float32
{
99.99
,
59.99
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
})
column2, _ := column.NewNullableColumnInt64(
"age"
,
    []
int64
{
25
,
30
,
45
,
60
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
0.9
,
0.1
,
0.4
},
        {
0.8
,
0.5
,
0.3
},
        {
0.1
,
0.6
,
0.9
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
-d
'{
    "data": [
        {"age": 25, "price": 99.99, "pk": 1, "embedding": [0.1, 0.2, 0.3]},
        {"age": 30, "price": 149.50, "pk": 2, "embedding": [0.4, 0.5, 0.6]},
        {"age": 35, "price": 199.99, "pk": 3, "embedding": [0.7, 0.8, 0.9]}       
    ],
    "collectionName": "my_collection"
}'
使用过滤表达式查询
插入实体后，使用
query
方法检索与指定过滤表达式匹配的实体。
检索
age
大于 30 的实体：
Python
Java
NodeJS
Go
cURL
filter
=
'age > 30'
res = client.query(
    collection_name=
"my_collection"
,
filter
=
filter
,
    output_fields=[
"age"
,
"price"
,
"pk"
]
)
print
(res)
# Example output:
# data: [
#     "{'age': 45, 'price': None, 'pk': 4}",
#     "{'age': 60, 'price': None, 'pk': 6}"
# ]
import
io.milvus.v2.service.vector.request.QueryReq;
import
io.milvus.v2.service.vector.response.QueryResp;
String
filter
=
"age > 30"
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
"age"
,
"price"
,
"pk"
))
        .build());
System.out.println(resp.getQueryResults());
// Output
//
// [
//    QueryResp.QueryResult(entity={price=null, pk=4, age=45}),
//    QueryResp.QueryResult(entity={price=null, pk=6, age=60})
// ]
client.
query
({
collection_name
:
'my_collection'
,
filter
:
'age > 30'
,
output_fields
: [
'age'
,
'price'
,
'pk'
]
});
filter :=
"age > 30"
queryResult, err := client.Query(ctx, milvusclient.NewQueryOption(
"my_collection"
).
    WithFilter(filter).
    WithOutputFields(
"pk"
,
"age"
,
"price"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(
"pk"
, queryResult.GetColumn(
"pk"
).FieldData().GetScalars())
fmt.Println(
"age"
, queryResult.GetColumn(
"age"
).FieldData().GetScalars())
fmt.Println(
"price"
, queryResult.GetColumn(
"price"
).FieldData().GetScalars())
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
    "filter": "age > 30",
    "outputFields": ["age","price", "pk"]
}'
## {"code":0,"cost":0,"data":[{"age":30,"pk":2,"price":149.5},{"age":35,"pk":3,"price":199.99}]}
检索
price
为空的实体：
Python
Java
NodeJS
Go
cURL
filter
=
'price is null'
res = client.query(
    collection_name=
"my_collection"
,
filter
=
filter
,
    output_fields=[
"age"
,
"price"
,
"pk"
]
)
print
(res)
# Example output:
# data: [
#     "{'age': 30, 'price': None, 'pk': 2}",
#     "{'age': 18, 'price': None, 'pk': 3}",
#     "{'age': 45, 'price': None, 'pk': 4}",
#     "{'age': 60, 'price': None, 'pk': 6}"
# ]
String
filter
=
"price is null"
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
"age"
,
"price"
,
"pk"
))
        .build());
System.out.println(resp.getQueryResults());
// Output
// [
//    QueryResp.QueryResult(entity={price=null, pk=2, age=30}),
//    QueryResp.QueryResult(entity={price=null, pk=3, age=18}),
//    QueryResp.QueryResult(entity={price=null, pk=4, age=45}),
//    QueryResp.QueryResult(entity={price=null, pk=6, age=60})
// ]
// node
const
filter =
'price is null'
;
const
res =
await
client.
query
({
collection_name
:
"my_collection"
,
filter
:filter,
    output_fields=[
"age"
,
"price"
,
"pk"
]
});
console
.
log
(res);
// Example output:
// data: [
//     "{'age': 18, 'price': None, 'pk': 3}",
//     "{'age': 18, 'price': 59.99, 'pk': 5}"
// ]
filter =
"price is null"
queryResult, err = client.Query(ctx, milvusclient.NewQueryOption(
"my_collection"
).
    WithFilter(filter).
    WithOutputFields(
"pk"
,
"age"
,
"price"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(
"pk"
, queryResult.GetColumn(
"pk"
))
fmt.Println(
"age"
, queryResult.GetColumn(
"age"
))
fmt.Println(
"price"
, queryResult.GetColumn(
"price"
))
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
  "filter": "price is null",
  "outputFields": ["age", "price", "pk"]
}'
要检索
age
的值为
18
的实体，请使用下面的表达式。由于
age
的默认值是
18
，因此预期结果应包括将
age
明确设置为
18
或将
age
设置为空的实体。
Python
Java
NodeJS
Go
cURL
filter
=
'age == 18'
res = client.query(
    collection_name=
"my_collection"
,
filter
=
filter
,
    output_fields=[
"age"
,
"price"
,
"pk"
]
)
print
(res)
# Example output:
# data: [
#     "{'age': 18, 'price': None, 'pk': 3}",
#     "{'age': 18, 'price': 59.99, 'pk': 5}"
# ]
String
filter
=
"age == 18"
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
"age"
,
"price"
,
"pk"
))
        .build());
System.out.println(resp.getQueryResults());
// Output
// [
//    QueryResp.QueryResult(entity={price=null, pk=3, age=18}),
//    QueryResp.QueryResult(entity={price=59.99, pk=5, age=18})
// ]
// node
const
filter =
'age == 18'
;
const
res =
await
client.
query
({
collection_name
:
"my_collection"
,
filter
:filter,
    output_fields=[
"age"
,
"price"
,
"pk"
]
});
console
.
log
(res);
// Example output:
// data: [
//     "{'age': 18, 'price': None, 'pk': 3}",
//     "{'age': 18, 'price': 59.99, 'pk': 5}"
// ]
filter =
"age == 18"
queryResult, err = client.Query(ctx, milvusclient.NewQueryOption(
"my_collection"
).
    WithFilter(filter).
    WithOutputFields(
"pk"
,
"age"
,
"price"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(
"pk"
, queryResult.GetColumn(
"pk"
))
fmt.Println(
"age"
, queryResult.GetColumn(
"age"
))
fmt.Println(
"price"
, queryResult.GetColumn(
"price"
))
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
  "filter": "age == 18",
  "outputFields": ["age", "price", "pk"]
}'
使用过滤表达式进行向量搜索
除了基本的数字字段过滤外，您还可以将向量相似性搜索与数字字段过滤器结合起来。例如，下面的代码展示了如何在向量搜索中添加数字字段过滤器：
Python
Java
NodeJS
Go
cURL
filter
=
"25 <= age <= 35"
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
"age"
,
"price"
],
filter
=
filter
)
print
(res)
# Example output:
# data: [
#     "[{'id': 2, 'distance': -0.2016308456659317, 'entity': {'age': 30, 'price': None}}, {'id': 1, 'distance': -0.23643313348293304, 'entity': {'age': 25, 'price': 99.98999786376953}}]"
# ]
import
io.milvus.v2.service.vector.request.SearchReq;
import
io.milvus.v2.service.vector.request.data.FloatVec;
import
io.milvus.v2.service.vector.response.SearchResp;
String
filter
=
"25 <= age <= 35"
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
"age"
,
"price"
))
        .filter(filter)
        .build());

System.out.println(resp.getSearchResults());
// Output
//
// [
//   [
//     SearchResp.SearchResult(entity={price=null, age=30}, score=-0.20163085, id=2),
//     SearchResp.SearchResult(entity={price=99.99, age=25}, score=-0.23643313, id=1)
//   ]
// ]
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
'age'
,
'price'
],
filter
:
'25 <= age <= 35'
});
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
"25 <= age <= 35"
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
"age"
,
"price"
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
"age: "
, resultSet.GetColumn(
"age"
))
    fmt.Println(
"price: "
, resultSet.GetColumn(
"price"
))
}
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
    "annsField": "embedding",
    "limit": 5,
    "outputFields": ["age", "price"]
}'
## {"code":0,"cost":0,"data":[{"age":35,"distance":-0.19054288,"id":3,"price":199.99},{"age":30,"distance":-0.20163085,"id":2,"price":149.5},{"age":25,"distance":-0.2364331,"id":1,"price":99.99}]}
在这个示例中，我们首先定义了一个查询向量，并在搜索过程中添加了一个过滤条件
25 <= age <= 35
。这样不仅能确保搜索结果与查询向量相似，还能满足指定的年龄范围。更多信息，请参阅
过滤
。