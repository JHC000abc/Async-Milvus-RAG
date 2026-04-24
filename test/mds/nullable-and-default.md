可归零和默认值
Milvus 允许你为标量字段（主字段除外）设置
nullable
属性和默认值。对于标记为
nullable=True
的字段，您可以在插入数据时跳过该字段，或直接将其设置为空值，系统会将其视为空值而不会导致错误。当字段具有默认值时，如果在插入过程中没有为该字段指定数据，系统将自动应用该值。
默认值和可归零属性允许处理带有空值的数据集并保留默认值设置，从而简化了从其他数据库系统到 Milvus 的数据迁移。在创建 Collections 时，也可以启用可归零属性或为可能存在不确定值的字段设置默认值。
限制
只有标量字段（主字段除外）支持默认值和 nullable 属性。
JSON 和数组字段不支持默认值。
默认值或 nullable 属性只能在创建 Collections 时配置，之后不能修改。
标记为 nullable 的字段不能用作分区键。有关分区键的更多信息，请参阅
使用分区键
。
在启用 nullable 属性的标量字段上创建索引时，索引将排除空值。
JSON 和 ARRAY 字段
：当使用
IS NULL
或
IS NOT NULL
操作符对 JSON 或 ARRAY 字段进行过滤时，这些操作符在列级别工作，这表明它们只评估整个 JSON 对象或数组是否为空。例如，如果 JSON 对象中的某个键为空，
IS NULL
过滤器将无法识别该键。有关详细信息，请参阅
基本操作符
。
Nullable 属性
通过
nullable
属性，可以在 Collections 中存储空值，从而在处理未知数据时提供灵活性。
设置 nullable 属性
创建 Collections 时，使用
nullable=True
定义可归零字段（默认为
False
）。下面的示例创建了一个名为
my_collection
的 Collection，并将
age
字段设置为可归零：
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
'http://localhost:19530'
)
# Define collection schema
schema = client.create_schema(
    auto_id=
False
,
    enable_dynamic_schema=
True
,
)

schema.add_field(field_name=
"id"
, datatype=DataType.INT64, is_primary=
True
)
schema.add_field(field_name=
"vector"
, datatype=DataType.FLOAT_VECTOR, dim=
5
)
schema.add_field(field_name=
"age"
, datatype=DataType.INT64, nullable=
True
)
# Nullable field
# Set index params
index_params = client.prepare_index_params()
index_params.add_index(field_name=
"vector"
, index_type=
"AUTOINDEX"
, metric_type=
"L2"
)
# Create collection
client.create_collection(collection_name=
"my_collection"
, schema=schema, index_params=index_params)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.common.DataType;
import
io.milvus.v2.common.IndexParam;
import
io.milvus.v2.service.collection.request.AddFieldReq;
import
io.milvus.v2.service.collection.request.CreateCollectionReq;
import
java.util.*;
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

schema.addField(AddFieldReq.builder()
        .fieldName(
"age"
)
        .dataType(DataType.Int64)
        .isNullable(
true
)
        .build());

List<IndexParam> indexes =
new
ArrayList
<>();
Map<String,Object> extraParams =
new
HashMap
<>();

indexes.add(IndexParam.builder()
        .fieldName(
"vector"
)
        .indexType(IndexParam.IndexType.AUTOINDEX)
        .metricType(IndexParam.MetricType.L2)
        .build());
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
"http://localhost:19530"
,
token
:
"root:Milvus"
,
});
await
client.
createCollection
({
collection_name
:
"my_collection"
,
schema
: [
    {
name
:
"id"
,
is_primary_key
:
true
,
data_type
:
DataType
.
int64
,
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
Int64
,
dim
:
5
},

    {
name
:
"age"
,
data_type
:
DataType
.
FloatVector
,
nullable
:
true
},
  ],
index_params
: [
    {
index_name
:
"vector_inde"
,
field_name
:
"vector"
,
metric_type
:
MetricType
.
L2
,
index_type
:
IndexType
.
AUTOINDEX
,
    },
  ],
});
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
"id"
).
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
"age"
).
    WithDataType(entity.FieldTypeInt64).
    WithNullable(
true
),
)

indexOption := milvusclient.NewCreateIndexOption(
"my_collection"
,
"vector"
,
    index.NewAutoIndex(index.MetricType(entity.L2)))

err = client.CreateCollection(ctx,
    milvusclient.NewCreateCollectionOption(
"my_collection"
, schema).
        WithIndexOptions(indexOption))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
export
pkField=
'{
    "fieldName": "id",
    "dataType": "Int64",
    "isPrimary": true
}'
export
vectorField=
'{
    "fieldName": "vector",
    "dataType": "FloatVector",
    "elementTypeParams": {
        "dim": 5
    }
}'
export
nullField=
'{
    "fieldName": "age",
    "dataType": "Int64",
    "nullable": true
}'
export
schema=
"{
    \"autoID\": false,
    \"fields\": [
$pkField
,
$vectorField
,
$nullField
]
}"
export
indexParams=
'[
        {
            "fieldName": "vector",
            "metricType": "L2",
            "indexType": "AUTOINDEX"
        }
    ]'
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
插入实体
在可空字段中插入数据时，插入空值或直接省略该字段：
Python
Java
NodeJS
Go
cURL
data = [
    {
"id"
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
"age"
:
30
},
    {
"id"
:
2
,
"vector"
: [
0.2
,
0.3
,
0.4
,
0.5
,
0.6
],
"age"
:
None
},
    {
"id"
:
3
,
"vector"
: [
0.3
,
0.4
,
0.5
,
0.6
,
0.7
]}
]

client.insert(collection_name=
"my_collection"
, data=data)
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
"{\"id\": 1, \"vector\": [0.1, 0.2, 0.3, 0.4, 0.5], \"age\": 30}"
, JsonObject.class));
rows.add(gson.fromJson(
"{\"id\": 2, \"vector\": [0.2, 0.3, 0.4, 0.5, 0.6], \"age\": null}"
, JsonObject.class));
rows.add(gson.fromJson(
"{\"id\": 3, \"vector\": [0.3, 0.4, 0.5, 0.6, 0.7]}"
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
id
:
1
,
vector
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
age
:
30
},
  {
id
:
2
,
vector
: [
0.2
,
0.3
,
0.4
,
0.5
,
0.6
],
age
:
null
},
  {
id
:
3
,
vector
: [
0.3
,
0.4
,
0.5
,
0.6
,
0.7
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
column, _ := column.NewNullableColumnInt64(
"age"
,
    []
int64
{
30
},
    []
bool
{
true
,
false
,
false
})

_, err = client.Insert(ctx, milvusclient.NewColumnBasedInsertOption(
"my_collection"
).
    WithInt64Column(
"id"
, []
int64
{
1
,
2
,
3
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
        {
0.2
,
0.3
,
0.4
,
0.5
,
0.6
},
        {
0.3
,
0.4
,
0.5
,
0.6
,
0.7
},
    }).
    WithColumns(column),
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
        {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4, 0.5], "age": 30},
        {"id": 2, "vector": [0.2, 0.3, 0.4, 0.5, 0.6], "age": null}, 
        {"id": 3, "vector": [0.3, 0.4, 0.5, 0.6, 0.7]} 
    ],
    "collectionName": "my_collection"
}'
使用空值搜索和查询
使用
search
方法时，如果字段包含
null
值，则搜索结果将以空值返回该字段：
Python
Java
NodeJS
Go
cURL
res = client.search(
    collection_name=
"my_collection"
,
    data=[[
0.1
,
0.2
,
0.4
,
0.3
,
0.128
]],
    limit=
2
,
    search_params={
"params"
: {
"nprobe"
:
16
}},
    output_fields=[
"id"
,
"age"
]
)
print
(res)
# Output
# data: ["[{'id': 1, 'distance': 0.15838398039340973, 'entity': {'age': 30, 'id': 1}}, {'id': 2, 'distance': 0.28278401494026184, 'entity': {'age': None, 'id': 2}}]"]
import
io.milvus.v2.service.vector.request.SearchReq;
import
io.milvus.v2.service.vector.request.data.FloatVec;
import
io.milvus.v2.service.vector.response.SearchResp;

Map<String,Object> params =
new
HashMap
<>();
params.put(
"nprobe"
,
16
);
SearchResp
resp
=
client.search(SearchReq.builder()
        .collectionName(
"my_collection"
)
        .annsField(
"vector"
)
        .data(Collections.singletonList(
new
FloatVec
(
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
,
0.5f
})))
        .topK(
2
)
        .searchParams(params)
        .outputFields(Arrays.asList(
"id"
,
"age"
))
        .build());

System.out.println(resp.getSearchResults());
// Output
//
// [[SearchResp.SearchResult(entity={id=1, age=30}, score=0.0, id=1), SearchResp.SearchResult(entity={id=2, age=null}, score=0.050000004, id=2)]]
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
,
0.3
,
0.5
],
limit
:
2
,
output_fields
: [
'age'
,
'id'
],
params
: {
nprobe
:
16
}
});
queryVector := []
float32
{
0.1
,
0.2
,
0.4
,
0.3
,
0.128
}

annParam := index.NewCustomAnnParam()
annParam.WithExtraParam(
"nprobe"
,
16
)
resultSets, err := client.Search(ctx, milvusclient.NewSearchOption(
"my_collection"
,
// collectionName
2
,
// limit
[]entity.Vector{entity.FloatVector(queryVector)},
).WithANNSField(
"vector"
).
    WithAnnParam(annParam).
    WithOutputFields(
"id"
,
"age"
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
).FieldData().GetScalars())
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
        [0.1, -0.2, 0.3, 0.4, 0.5]
    ],
    "annsField": "vector",
    "limit": 2,
    "outputFields": ["id", "age"]
}'
#{"code":0,"cost":0,"data":[{"age":30,"distance":0.16000001,"id":1},{"age":null,"distance":0.28999996,"id":2}]}
当您使用
query
方法进行标量过滤时，空值的过滤结果都是 false，表示不会选择它们。
Python
Java
NodeJS
Go
cURL
# Reviewing previously inserted data:
# {"id": 1, "vector": [0.1, 0.2, ..., 0.128], "age": 30}
# {"id": 2, "vector": [0.2, 0.3, ..., 0.129], "age": None}
# {"id": 3, "vector": [0.3, 0.4, ..., 0.130], "age": None}  # Omitted age  column is treated as None
results = client.query(
    collection_name=
"my_collection"
,
filter
=
"age >= 0"
,
    output_fields=[
"id"
,
"age"
]
)
# Example output:
# [
#     {"id": 1, "age": 30}
# ]
# Note: Entities with `age` as `null` (id 2 and 3) will not appear in the result.
import
io.milvus.v2.service.vector.request.QueryReq;
import
io.milvus.v2.service.vector.response.QueryResp;
QueryResp
resp
=
client.query(QueryReq.builder()
        .collectionName(
"my_collection"
)
        .filter(
"age >= 0"
)
        .outputFields(Arrays.asList(
"id"
,
"age"
))
        .build());

System.out.println(resp.getQueryResults());
// Output
//
// [QueryResp.QueryResult(entity={id=1, age=30})]
const
results =
await
client.
query
(
collection_name
:
"my_collection"
,
filter
:
"age >= 0"
,
output_fields
: [
"id"
,
"age"
]
);
resultSet, err := client.Query(ctx, milvusclient.NewQueryOption(
"my_collection"
).
    WithFilter(
"age >= 0"
).
    WithOutputFields(
"id"
,
"age"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(
"id: "
, resultSet.GetColumn(
"id"
).FieldData().GetScalars())
fmt.Println(
"age: "
, resultSet.GetColumn(
"age"
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
    "filter": "age >= 0",
    "outputFields": ["id", "age"]
}'
# {"code":0,"cost":0,"data":[{"age":30,"id":1}]}
要返回具有
null
值的实体，可在不使用任何标量过滤条件的情况下进行如下查询：
query
方法在不带任何过滤条件的情况下使用时，会检索 Collections 中的所有实体，包括具有空值的实体。要限制返回实体的数量，必须指定
limit
参数。
Python
Java
NodeJS
Go
cURL
null_results = client.query(
    collection_name=
"my_collection"
,
filter
=
""
,
# Query without any filtering condition
output_fields=[
"id"
,
"age"
],
    limit=
10
)
# Example output:
# [{"id": 2, "age": None}, {"id": 3, "age": None}]
QueryResp
resp
=
client.query(QueryReq.builder()
        .collectionName(
"my_collection"
)
        .filter(
""
)
        .outputFields(Arrays.asList(
"id"
,
"age"
))
        .limit(
10
)
        .build());

System.out.println(resp.getQueryResults());
const
results =
await
client.
query
(
collection_name
:
"my_collection"
,
filter
:
""
,
output_fields
: [
"id"
,
"age"
],
limit
:
10
);
resultSet, err = client.Query(ctx, milvusclient.NewQueryOption(
"my_collection"
).
    WithFilter(
""
).
    WithLimit(
10
).
    WithOutputFields(
"id"
,
"age"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(
"id: "
, resultSet.GetColumn(
"id"
))
fmt.Println(
"age: "
, resultSet.GetColumn(
"age"
))
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
    "expr": "",
    "outputFields": ["id", "age"],
    "limit": 10
}'
# {"code":0,"cost":0,"data":[{"age":30,"id":1},{"age":null,"id":2},{"age":null,"id":3}]}
默认值
默认值是分配给标量字段的预设值。如果在插入时没有为有默认值的字段提供值，系统会自动使用默认值。
设置默认值
创建 Collections 时，使用
default_value
参数定义字段的默认值。下面的示例显示了如何将
age
的默认值设置为
18
，将
status
的默认值设置为
"active"
：
Python
Java
NodeJS
Go
cURL
schema = client.create_schema(
    auto_id=
False
,
    enable_dynamic_schema=
True
,
)

schema.add_field(field_name=
"id"
, datatype=DataType.INT64, is_primary=
True
)
schema.add_field(field_name=
"vector"
, datatype=DataType.FLOAT_VECTOR, dim=
5
)
schema.add_field(field_name=
"age"
, datatype=DataType.INT64, default_value=
18
)
schema.add_field(field_name=
"status"
, datatype=DataType.VARCHAR, default_value=
"active"
, max_length=
10
)

index_params = client.prepare_index_params()
index_params.add_index(field_name=
"vector"
, index_type=
"AUTOINDEX"
, metric_type=
"L2"
)

client.create_collection(collection_name=
"my_collection"
, schema=schema, index_params=index_params)
import
io.milvus.v2.common.DataType;
import
io.milvus.v2.common.IndexParam;
import
io.milvus.v2.service.collection.request.AddFieldReq;
import
io.milvus.v2.service.collection.request.CreateCollectionReq;
import
java.util.*;

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

schema.addField(AddFieldReq.builder()
        .fieldName(
"age"
)
        .dataType(DataType.Int64)
        .defaultValue(
18L
)
        .build());

schema.addField(AddFieldReq.builder()
        .fieldName(
"status"
)
        .dataType(DataType.VarChar)
        .maxLength(
10
)
        .defaultValue(
"active"
)
        .build());

List<IndexParam> indexes =
new
ArrayList
<>();
Map<String,Object> extraParams =
new
HashMap
<>();

indexes.add(IndexParam.builder()
        .fieldName(
"vector"
)
        .indexType(IndexParam.IndexType.AUTOINDEX)
        .metricType(IndexParam.MetricType.L2)
        .build());
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
"http://localhost:19530"
,
token
:
"root:Milvus"
,
});
await
client.
createCollection
({
collection_name
:
"my_collection"
,
schema
: [
    {
name
:
"id"
,
is_primary_key
:
true
,
data_type
:
DataType
.
int64
,
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
"age"
,
data_type
:
DataType
.
Int64
,
default_value
:
18
},
    {
name
:
'status'
,
data_type
:
DataType
.
VarChar
,
max_length
:
30
,
default_value
:
'active'
},
  ],
index_params
: [
    {
index_name
:
"vector_inde"
,
field_name
:
"vector"
,
metric_type
:
MetricType
.
L2
,
index_type
:
IndexType
.
AUTOINDEX
,
    },
  ],
});
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

schema := entity.NewSchema()
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
"vector"
).
    WithDataType(entity.FieldTypeFloatVector).
    WithDim(
5
),
).WithField(entity.NewField().
    WithName(
"age"
).
    WithDataType(entity.FieldTypeInt64).
    WithDefaultValueLong(
18
),
).WithField(entity.NewField().
    WithName(
"status"
).
    WithDataType(entity.FieldTypeVarChar).
    WithMaxLength(
10
).
    WithDefaultValueString(
"active"
),
)

indexOption := milvusclient.NewCreateIndexOption(
"my_collection"
,
"vector"
,
    index.NewAutoIndex(index.MetricType(entity.L2)))

err = client.CreateCollection(ctx,
    milvusclient.NewCreateCollectionOption(
"my_collection"
, schema).
        WithIndexOptions(indexOption))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
export
pkField=
'{
    "fieldName": "id",
    "dataType": "Int64",
    "isPrimary": true
}'
export
vectorField=
'{
    "fieldName": "vector",
    "dataType": "FloatVector",
    "elementTypeParams": {
        "dim": 5
    }
}'
export
defaultValueField1=
'{
    "fieldName": "age",
    "dataType": "Int64",
    "defaultValue": 18
}'
export
defaultValueField2=
'{
    "fieldName": "status",
    "dataType": "VarChar",
    "defaultValue": "active",
    "elementTypeParams": {
        "max_length": 10
    }
}'
export
schema=
"{
    \"autoID\": false,
    \"fields\": [
$pkField
,
$vectorField
,
$defaultValueField1
,
$defaultValueField2
]
}"
export
indexParams=
'[
        {
            "fieldName": "vector",
            "metricType": "L2",
            "indexType": "AUTOINDEX"
        }
    ]'
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
插入实体
插入数据时，如果省略有默认值的字段或将其值设为空，系统就会使用默认值：
Python
Java
NodeJS
Go
cURL
data = [
    {
"id"
:
1
,
"vector"
: [
0.1
,
0.2
, ...,
0.128
],
"age"
:
30
,
"status"
:
"premium"
},
    {
"id"
:
2
,
"vector"
: [
0.2
,
0.3
, ...,
0.129
]},
# `age` and `status` use default values
{
"id"
:
3
,
"vector"
: [
0.3
,
0.4
, ...,
0.130
],
"age"
:
25
,
"status"
:
None
},
# `status` uses default value
{
"id"
:
4
,
"vector"
: [
0.4
,
0.5
, ...,
0.131
],
"age"
:
None
,
"status"
:
"inactive"
}
# `age` uses default value
]

client.insert(collection_name=
"my_collection"
, data=data)
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
"{\"id\": 1, \"vector\": [0.1, 0.2, 0.3, 0.4, 0.5], \"age\": 30, \"status\": \"premium\"}"
, JsonObject.class));
rows.add(gson.fromJson(
"{\"id\": 2, \"vector\": [0.2, 0.3, 0.4, 0.5, 0.6]}"
, JsonObject.class));
rows.add(gson.fromJson(
"{\"id\": 3, \"vector\": [0.3, 0.4, 0.5, 0.6, 0.7], \"age\": 25, \"status\": null}"
, JsonObject.class));
rows.add(gson.fromJson(
"{\"id\": 4, \"vector\": [0.4, 0.5, 0.6, 0.7, 0.8], \"age\": null, \"status\": \"inactive\"}"
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
"id"
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
"age"
:
30
,
"status"
:
"premium"
},
    {
"id"
:
2
,
"vector"
: [
0.2
,
0.3
,
0.4
,
0.5
,
0.6
]}, 
    {
"id"
:
3
,
"vector"
: [
0.3
,
0.4
,
0.5
,
0.6
,
0.7
],
"age"
:
25
,
"status"
:
null
}, 
    {
"id"
:
4
,
"vector"
: [
0.4
,
0.5
,
0.6
,
0.7
,
0.8
],
"age"
:
null
,
"status"
:
"inactive"
}  
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
column1, _ := column.NewNullableColumnInt64(
"age"
,
    []
int64
{
30
,
25
},
    []
bool
{
true
,
false
,
true
,
false
})
column2, _ := column.NewNullableColumnVarChar(
"status"
,
    []
string
{
"premium"
,
"inactive"
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
true
})

_, err = client.Insert(ctx, milvusclient.NewColumnBasedInsertOption(
"my_collection"
).
    WithInt64Column(
"id"
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
        {
0.2
,
0.3
,
0.4
,
0.5
,
0.6
},
        {
0.3
,
0.4
,
0.5
,
0.6
,
0.7
},
        {
0.4
,
0.5
,
0.6
,
0.7
,
0.8
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
        {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4, 0.5], "age": 30, "status": "premium"},
        {"id": 2, "vector": [0.2, 0.3, 0.4, 0.5, 0.6]},
        {"id": 3, "vector": [0.3, 0.4, 0.5, 0.6, 0.7], "age": 25, "status": null}, 
        {"id": 4, "vector": [0.4, 0.5, 0.6, 0.7, 0.8], "age": null, "status": "inactive"}      
    ],
    "collectionName": "my_collection"
}'
有关可空值和默认值设置如何生效的更多信息，请参阅
适用规则
。
使用默认值进行搜索和查询
在向量搜索和标量过滤过程中，包含默认值的实体与其他实体的处理方式相同。您可以将默认值作为
search
和
query
操作符的一部分。
例如，在
search
操作符中，将
age
设置为默认值
18
的实体将包含在结果中：
Python
Java
NodeJS
Go
cURL
res = client.search(
    collection_name=
"my_collection"
,
    data=[[
0.1
,
0.2
,
0.4
,
0.3
,
0.5
]],
    search_params={
"params"
: {
"nprobe"
:
16
}},
filter
=
"age == 18"
,
# 18 is the default value of the `age` field
limit=
10
,
    output_fields=[
"id"
,
"age"
,
"status"
]
)
print
(res)
# Output
# data: ["[{'id': 2, 'distance': 0.050000004, 'entity': {'id': 2, 'age': 18, 'status': 'active'}}, {'id': 4, 'distance': 0.45000002, 'entity': {'id': 4, 'age': 18, 'status': 'inactive'}}]"]
import
io.milvus.v2.service.vector.request.SearchReq;
import
io.milvus.v2.service.vector.request.data.FloatVec;
import
io.milvus.v2.service.vector.response.SearchResp;

Map<String,Object> params =
new
HashMap
<>();
params.put(
"nprobe"
,
16
);
SearchResp
resp
=
client.search(SearchReq.builder()
        .collectionName(
"my_collection"
)
        .annsField(
"vector"
)
        .data(Collections.singletonList(
new
FloatVec
(
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
,
0.5f
})))
        .searchParams(params)
        .filter(
"age == 18"
)
        .topK(
10
)
        .outputFields(Arrays.asList(
"id"
,
"age"
,
"status"
))
        .build());

System.out.println(resp.getSearchResults());
// Output
//
// [[SearchResp.SearchResult(entity={id=2, age=18, status=active}, score=0.050000004, id=2), SearchResp.SearchResult(entity={id=4, age=18, status=inactive}, score=0.45000002, id=4)]]
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
,
0.3
,
0.5
],
limit
:
2
,
output_fields
: [
'age'
,
'id'
,
'status'
],
filter
:
'age == 18'
,
params
: {
nprobe
:
16
}
});
queryVector := []
float32
{
0.1
,
0.2
,
0.4
,
0.3
,
0.5
}

annParam := index.NewCustomAnnParam()
annParam.WithExtraParam(
"nprobe"
,
16
)
resultSets, err := client.Search(ctx, milvusclient.NewSearchOption(
"my_collection"
,
// collectionName
10
,
// limit
[]entity.Vector{entity.FloatVector(queryVector)},
).WithANNSField(
"vector"
).
    WithFilter(
"age == 18"
).
    WithAnnParam(annParam).
    WithOutputFields(
"id"
,
"age"
,
"status"
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
).FieldData().GetScalars())
    fmt.Println(
"status: "
, resultSet.GetColumn(
"status"
).FieldData().GetScalars())
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
        [0.1, 0.2, 0.3, 0.4, 0.5]
    ],
    "annsField": "vector",
    "limit": 10,
    "filter": "age == 18",
    "outputFields": ["id", "age", "status"]
}'
# {"code":0,"cost":0,"data":[{"age":18,"distance":0.050000004,"id":2,"status":"active"},{"age":18,"distance":0.45000002,"id":4,"status":"inactive"}]}
在
query
操作符中，可以直接通过默认值进行匹配或过滤：
Python
Java
NodeJS
Go
cURL
# Query all entities where `age` equals the default value (18)
default_age_results = client.query(
    collection_name=
"my_collection"
,
filter
=
"age == 18"
,
    output_fields=[
"id"
,
"age"
,
"status"
]
)
# Query all entities where `status` equals the default value ("active")
default_status_results = client.query(
    collection_name=
"my_collection"
,
filter
=
'status == "active"'
,
    output_fields=[
"id"
,
"age"
,
"status"
]
)
import
io.milvus.v2.service.vector.request.QueryReq;
import
io.milvus.v2.service.vector.response.QueryResp;
QueryResp
ageResp
=
client.query(QueryReq.builder()
        .collectionName(
"my_collection"
)
        .filter(
"age == 18"
)
        .outputFields(Arrays.asList(
"id"
,
"age"
,
"status"
))
        .build());

System.out.println(ageResp.getQueryResults());
// Output
//
// [QueryResp.QueryResult(entity={id=2, age=18, status=active}), QueryResp.QueryResult(entity={id=4, age=18, status=inactive})]
QueryResp
statusResp
=
client.query(QueryReq.builder()
        .collectionName(
"my_collection"
)
        .filter(
"status == \"active\""
)
        .outputFields(Arrays.asList(
"id"
,
"age"
,
"status"
))
        .build());

System.out.println(statusResp.getQueryResults());
// Output
//
// [QueryResp.QueryResult(entity={id=2, age=18, status=active}), QueryResp.QueryResult(entity={id=3, age=25, status=active})]
// Query all entities where `age` equals the default value (18)
const
default_age_results =
await
client.
query
(
collection_name
:
"my_collection"
,
filter
:
"age == 18"
,
output_fields
: [
"id"
,
"age"
,
"status"
]
);
// Query all entities where `status` equals the default value ("active")
const
default_status_results =
await
client.
query
(
collection_name
:
"my_collection"
,
filter
:
'status == "active"'
,
output_fields
: [
"id"
,
"age"
,
"status"
]
)
resultSet, err := client.Query(ctx, milvusclient.NewQueryOption(
"my_collection"
).
    WithFilter(
"age == 18"
).
    WithOutputFields(
"id"
,
"age"
,
"status"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(
"id: "
, resultSet.GetColumn(
"id"
).FieldData().GetScalars())
fmt.Println(
"age: "
, resultSet.GetColumn(
"age"
).FieldData().GetScalars())
fmt.Println(
"status: "
, resultSet.GetColumn(
"status"
).FieldData().GetScalars())

resultSet, err = client.Query(ctx, milvusclient.NewQueryOption(
"my_collection"
).
    WithFilter(
"status == \"active\""
).
    WithOutputFields(
"id"
,
"age"
,
"status"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
fmt.Println(
"id: "
, resultSet.GetColumn(
"id"
).FieldData().GetScalars())
fmt.Println(
"age: "
, resultSet.GetColumn(
"age"
).FieldData().GetScalars())
fmt.Println(
"status: "
, resultSet.GetColumn(
"status"
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
    "filter": "age == 18",
    "outputFields": ["id", "age", "status"]
}'
# {"code":0,"cost":0,"data":[{"age":18,"id":2,"status":"active"},{"age":18,"id":4,"status":"inactive"}]}
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
    "filter": "status == \"active\"",
    "outputFields": ["id", "age", "status"]
}'
# {"code":0,"cost":0,"data":[{"age":18,"id":2,"status":"active"},{"age":25,"id":3,"status":"active"}]}
适用规则
下表总结了可空列和默认值在不同配置组合下的行为。这些规则决定了 Milvus 在尝试插入空值或未提供字段值时如何处理数据。
可归零
默认值
默认值类型
用户输入
结果
示例
✅
✅
非空
无/空
使用默认值
字段：
age
默认值：
18
用户输入：空
结果：存储为
18
✅
❌
-
无/空
存储为空
字段：
middle_name
默认值： -
用户输入：空
结果：存储为空
❌
✅
非空
无/空
使用默认值
字段：
status
默认值：
"active"
用户输入：空
结果：存储为
"active"
❌
❌
-
无/空
抛出错误
字段：
email
默认值：-
用户输入：空
结果：操作被拒绝，系统提示错误
❌
✅
空
无/空
抛出错误
字段：
username
默认值：空
用户输入：空
结果：操作符被拒绝，系统提示错误