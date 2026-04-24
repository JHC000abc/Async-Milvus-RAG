数组字段
ARRAY 字段存储相同数据类型元素的有序集合。下面举例说明 ARRAY 字段如何存储数据：
{
"tags"
:
[
"pop"
,
"rock"
,
"classic"
]
,
"ratings"
:
[
5
,
4
,
3
]
}
限制
默认值
：ARRAY 字段不支持默认值。但是，可以将
nullable
属性设置为
True
，以允许空值。有关详情，请参阅
Nullable & Default
。
数据类型：
ARRAY 字段中的所有元素必须共享相同的数据类型，该类型由
element_type
参数定义。当
element_type
设置为
VARCHAR
时，还必须为数组元素指定
max_length
。
element_type
接受 Milvus 支持的任何标量数据类型，但
JSON
除外。
数组容量
：ARRAY 字段中的元素数必须小于或等于创建数组时定义的最大容量，具体由
max_capacity
指定。该值应为
1
至
4096
范围内的整数。
字符串处理
：数组字段中的字符串值按原样存储，不进行语义转义或转换。例如，
'a"b'
、
"a'b"
、
'a\'b'
和
"a\"b"
按输入值存储，而
'a'b'
和
"a"b"
则被视为无效值。
添加 ARRAY 字段
要使用 ARRAY 字段，Milvus 需要在创建 Collections Schema 时定义相关字段类型。这一过程包括
将
datatype
设置为支持的数组数据类型
ARRAY
。
使用
element_type
参数指定数组中元素的数据类型。同一数组中的所有元素必须具有相同的数据类型。
使用
max_capacity
参数定义数组的最大容量，即数组可包含的最大元素数。
下面介绍如何定义包含 ARRAY 字段的 Collections Schema：
如果在定义模式时设置了
enable_dynamic_fields=True
，Milvus 允许你插入事先未定义的标量字段。不过，这可能会增加查询和管理的复杂性，并可能影响性能。有关详细信息，请参阅
动态字段
。
Python
Java
Go
NodeJS
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
#  Add `tags` and `ratings` ARRAY fields with nullable=True
schema.add_field(field_name=
"tags"
, datatype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=
10
, max_length=
65535
, nullable=
True
)
schema.add_field(field_name=
"ratings"
, datatype=DataType.ARRAY, element_type=DataType.INT64, max_capacity=
5
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
"tags"
)
        .dataType(DataType.Array)
        .elementType(DataType.VarChar)
        .maxCapacity(
10
)
        .maxLength(
65535
)
        .isNullable(
true
)
        .build());

schema.addField(AddFieldReq.builder()
        .fieldName(
"ratings"
)
        .dataType(DataType.Array)
        .elementType(DataType.Int64)
        .maxCapacity(
5
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
"tags"
).
    WithDataType(entity.FieldTypeArray).
    WithElementType(entity.FieldTypeVarChar).
    WithMaxCapacity(
10
).
    WithMaxLength(
65535
).
    WithNullable(
true
),
).WithField(entity.NewField().
    WithName(
"ratings"
).
    WithDataType(entity.FieldTypeArray).
    WithElementType(entity.FieldTypeInt64).
    WithMaxCapacity(
5
).
    WithNullable(
true
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
schema = [
  {
name
:
"tags"
,
data_type
:
DataType
.
Array
,
element_type
:
DataType
.
VarChar
,
max_capacity
:
10
,
max_length
:
65535
},
  {
name
:
"rating"
,
data_type
:
DataType
.
Array
,
element_type
:
DataType
.
Int64
,
max_capacity
:
5
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
export
arrayField1=
'{
    "fieldName": "tags",
    "dataType": "Array",
    "elementDataType": "VarChar",
    "elementTypeParams": {
        "max_capacity": 10,
        "max_length": 65535
    }
}'
export
arrayField2=
'{
    "fieldName": "ratings",
    "dataType": "Array",
    "elementDataType": "Int64",
    "elementTypeParams": {
        "max_capacity": 5
    }
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
$arrayField1
,
$arrayField2
,
$pkField
,
$vectorField
]
}"
设置索引参数
索引有助于提高搜索和查询性能。在 Milvus 中，向量字段必须建立索引，标量字段则可选。
下面的示例使用
AUTOINDEX
索引类型为向量字段
embedding
和 ARRAY 字段
tags
创建了索引。使用这种类型，Milvus 会根据数据类型自动选择最合适的索引。您还可以自定义每个字段的索引类型和参数。有关详情，请参阅
索引说明
。
Python
Java
Go
NodeJS
cURL
# Set index params
index_params = client.prepare_index_params()
# Index `age` with AUTOINDEX
index_params.add_index(
    field_name=
"tags"
,
    index_type=
"AUTOINDEX"
,
    index_name=
"tags_index"
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
"tags"
)
        .indexName(
"tags_index"
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
indexOpt1 := milvusclient.NewCreateIndexOption(
"my_collection"
,
"tags"
, index.NewInvertedIndex())
indexOpt2 := milvusclient.NewCreateIndexOption(
"my_collection"
,
"embedding"
, index.NewAutoIndex(entity.COSINE))
const
indexParams = [{
index_name
:
'inverted_index'
,
field_name
:
'tags'
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
            "fieldName": "tags",
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
定义好 Schema 和索引后，创建一个包含 ARRAY 字段的 Collection。
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
err = client.CreateCollection(ctx, milvusclient.NewCreateCollectionOption(
"my_collection"
, schema).
    WithIndexOptions(indexOpt1, indexOpt2))
if
err !=
nil
{
    fmt.Println(err.Error())
// handler err
}
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
创建 Collections 后，就可以插入包含 ARRAY 字段的数据。
Python
Java
Go
NodeJS
cURL
# Sample data
data = [
  {
"tags"
: [
"pop"
,
"rock"
,
"classic"
],
"ratings"
: [
5
,
4
,
3
],
"pk"
:
1
,
"embedding"
: [
0.12
,
0.34
,
0.56
]
  },
  {
"tags"
:
None
,
# Entire ARRAY is null
"ratings"
: [
4
,
5
],
"pk"
:
2
,
"embedding"
: [
0.78
,
0.91
,
0.23
]
  },
  {
# The tags field is completely missing
"ratings"
: [
9
,
5
],
"pk"
:
3
,
"embedding"
: [
0.18
,
0.11
,
0.23
]
  }
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
"{\"tags\": [\"pop\", \"rock\", \"classic\"], \"ratings\": [5, 4, 3], \"pk\": 1, \"embedding\": [0.12, 0.34, 0.56]}"
, JsonObject.class));
rows.add(gson.fromJson(
"{\"tags\": null, \"ratings\": [4, 5], \"pk\": 2, \"embedding\": [0.78, 0.91, 0.23]}"
, JsonObject.class));
rows.add(gson.fromJson(
"{\"ratings\": [9, 5], \"pk\": 3, \"embedding\": [0.18, 0.11, 0.23]}"
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
column1, _ := column.NewNullableColumnVarCharArray(
"tags"
,
    [][]
string
{{
"pop"
,
"rock"
,
"classic"
}},
    []
bool
{
true
,
false
,
false
})
column2, _ := column.NewNullableColumnInt64Array(
"ratings"
,
    [][]
int64
{{
5
,
4
,
3
}, {
4
,
5
}, {
9
,
5
}},
    []
bool
{
true
,
true
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
}).
    WithFloatVectorColumn(
"embedding"
,
3
, [][]
float32
{
        {
0.12
,
0.34
,
0.56
},
        {
0.78
,
0.91
,
0.23
},
        {
0.18
,
0.11
,
0.23
},
    }).WithColumns(column1, column2))
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
"tags"
: [
"pop"
,
"rock"
,
"classic"
],
"ratings"
: [
5
,
4
,
3
],
"pk"
:
1
,
"embedding"
: [
0.12
,
0.34
,
0.56
]
    },
    {
"tags"
: [
"jazz"
,
"blues"
],
"ratings"
: [
4
,
5
],
"pk"
:
2
,
"embedding"
: [
0.78
,
0.91
,
0.23
]
    },
    {
"tags"
: [
"electronic"
,
"dance"
],
"ratings"
: [
3
,
3
,
4
],
"pk"
:
3
,
"embedding"
: [
0.67
,
0.45
,
0.89
]
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
        {
        "tags": ["pop", "rock", "classic"],
        "ratings": [5, 4, 3],
        "pk": 1,
        "embedding": [0.12, 0.34, 0.56]
    },
    {
        "tags": ["jazz", "blues"],
        "ratings": [4, 5],
        "pk": 2,
        "embedding": [0.78, 0.91, 0.23]
    },
    {
        "tags": ["electronic", "dance"],
        "ratings": [3, 3, 4],
        "pk": 3,
        "embedding": [0.67, 0.45, 0.89]
    }       
    ],
    "collectionName": "my_collection"
}'
使用过滤表达式查询
插入实体后，使用
query
方法检索与指定过滤表达式匹配的实体。
检索
tags
不为空的实体：
Python
Java
Go
NodeJS
cURL
# Query to exclude entities where `tags` is not null
filter
=
'tags IS NOT NULL'
res = client.query(
    collection_name=
"my_collection"
,
filter
=
filter
,
    output_fields=[
"tags"
,
"ratings"
,
"pk"
]
)
print
(res)
# Example output:
# data: [
#     "{'tags': ['pop', 'rock', 'classic'], 'ratings': [5, 4, 3], 'pk': 1}"
# ]
import
io.milvus.v2.service.vector.request.QueryReq;
import
io.milvus.v2.service.vector.response.QueryResp;
String
filter
=
"tags IS NOT NULL"
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
"tags"
,
"ratings"
,
"pk"
))
        .build());

System.out.println(resp.getQueryResults());
// Output
//
// [QueryResp.QueryResult(entity={ratings=[5, 4, 3], pk=1, tags=[pop, rock, classic]})]
filter :=
"tags IS NOT NULL"
rs, err := client.Query(ctx, milvusclient.NewQueryOption(
"my_collection"
).
    WithFilter(filter).
    WithOutputFields(
"tags"
,
"ratings"
,
"pk"
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
, rs.GetColumn(
"pk"
).FieldData().GetScalars())
fmt.Println(
"tags"
, rs.GetColumn(
"tags"
).FieldData().GetScalars())
fmt.Println(
"ratings"
, rs.GetColumn(
"ratings"
).FieldData().GetScalars())
client.
query
({
collection_name
:
'my_collection'
,
filter
:
'tags IS NOT NULL'
,
output_fields
: [
'tags'
,
'ratings'
,
'embedding'
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
    "filter": "tags IS NOT NULL",
    "outputFields": ["tags", "ratings", "embedding"]
}'
检索
ratings
第一个元素的值大于 4 的实体：
Python
Java
Go
NodeJS
cURL
filter
=
'ratings[0] > 4'
res = client.query(
    collection_name=
"my_collection"
,
filter
=
filter
,
    output_fields=[
"tags"
,
"ratings"
,
"embedding"
]
)
print
(res)
# Example output:
# data: [
#     "{'tags': ['pop', 'rock', 'classic'], 'ratings': [5, 4, 3], 'embedding': [0.12, 0.34, 0.56], 'pk': 1}",
#     "{'tags': None, 'ratings': [9, 5], 'embedding': [0.18, 0.11, 0.23], 'pk': 3}"
# ]
String
filter
=
"ratings[0] > 4"
QueryResp
resp
=
client.query(QueryReq.builder()
        .collectionName(
"my_collection"
)
        .filter(filter)
        .outputFields(Arrays.asList(
"tags"
,
"ratings"
,
"pk"
))
        .build());

System.out.println(resp.getQueryResults());
// Output
// [
//    QueryResp.QueryResult(entity={ratings=[5, 4, 3], pk=1, tags=[pop, rock, classic]}),
//    QueryResp.QueryResult(entity={ratings=[9, 5], pk=3, tags=[]})
// ]
filter =
"ratings[0] > 4"
rs, err = client.Query(ctx, milvusclient.NewQueryOption(
"my_collection"
).
    WithFilter(filter).
    WithOutputFields(
"tags"
,
"ratings"
,
"pk"
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
, rs.GetColumn(
"pk"
))
fmt.Println(
"tags"
, rs.GetColumn(
"tags"
))
fmt.Println(
"ratings"
, rs.GetColumn(
"ratings"
))
// node
const
filter =
'ratings[0] > 4'
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
output_fields
: [
"tags"
,
"ratings"
,
"embedding"
]
});
console
.
log
(res)
// Example output:
// data: [
//     "{'tags': ['pop', 'rock', 'classic'], 'ratings': [5, 4, 3], 'embedding': [0.12, 0.34, 0.56], 'pk': 1}",
//     "{'tags': None, 'ratings': [9, 5], 'embedding': [0.18, 0.11, 0.23], 'pk': 3}"
// ]
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
  "filter": "ratings[0] > 4",
  "outputFields": ["tags", "ratings", "embedding"]
}'
使用过滤表达式进行向量搜索
除了基本的标量字段筛选外，您还可以将向量相似性搜索与标量字段筛选结合起来。例如，下面的代码展示了如何在向量搜索中添加标量字段过滤器：
Python
Java
Go
NodeJS
cURL
filter
=
'tags[0] == "pop"'
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
"tags"
,
"ratings"
,
"embedding"
],
filter
=
filter
)
print
(res)
# Example output:
# data: [
#     "[{'id': 1, 'distance': -0.2479381263256073, 'entity': {'tags': ['pop', 'rock', 'classic'], 'ratings': [5, 4, 3], 'embedding': [0.11999999731779099, 0.3400000035762787, 0.5600000023841858]}}]"
# ]
import
io.milvus.v2.service.vector.request.SearchReq;
import
io.milvus.v2.service.vector.response.SearchResp;
String
filter
=
"tags[0] == \"pop\""
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
"tags"
,
"ratings"
,
"embedding"
))
        .filter(filter)
        .build());

System.out.println(resp.getSearchResults());
// Output
//
// [[SearchResp.SearchResult(entity={ratings=[5, 4, 3], embedding=[0.12, 0.34, 0.56], tags=[pop, rock, classic]}, score=-0.24793813, id=1)]]
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
"tags[0] == \"pop\""
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
    WithOutputFields(
"tags"
,
"ratings"
,
"embedding"
).
    WithAnnParam(annParam))
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
"tags"
, resultSet.GetColumn(
"tags"
).FieldData().GetScalars())
    fmt.Println(
"ratings"
, resultSet.GetColumn(
"ratings"
).FieldData().GetScalars())
    fmt.Println(
"embedding"
, resultSet.GetColumn(
"embedding"
).FieldData().GetVectors())
}
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
'tags'
,
'ratings'
,
'embdding'
],
filter
:
'tags[0] == "pop"'
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
    "annsField": "embedding",
    "limit": 5,
    "filter": "tags[0] == \"pop\"",
    "outputFields": ["tags", "ratings", "embedding"]
}'
# {"code":0,"cost":0,"data":[{"distance":-0.24793813,"embedding":[0.12,0.34,0.56],"id":1,"ratings":{"Data":{"LongData":{"data":[5,4,3]}}},"tags":{"Data":{"StringData":{"data":["pop","rock","classic"]}}}}]}
此外，Milvus 还支持高级数组过滤操作符，如
ARRAY_CONTAINS
,
ARRAY_CONTAINS_ALL
,
ARRAY_CONTAINS_ANY
和
ARRAY_LENGTH
，以进一步增强查询功能。更多详情，请参阅
ÂRAY 操作符
。