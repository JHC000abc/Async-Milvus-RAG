稀疏向量
稀疏向量是信息检索和自然语言处理中捕捉表层术语匹配的重要方法。虽然稠密向量在语义理解方面表现出色，但稀疏向量往往能提供更可预测的匹配结果，尤其是在搜索特殊术语或文本标识符时。
稀疏向量概述
稀疏向量是一种特殊的高维向量，其中大部分元素为零，只有少数维度的值不为零。如下图所示，稠密向量通常表示为连续数组，其中每个位置都有一个值（例如
[0.3, 0.8, 0.2, 0.3, 0.1]
）。相比之下，稀疏向量只存储非零元素及其维度的索引，通常以
{ index: value}
的键值对表示（如
[{2: 0.2}, ..., {9997: 0.5}, {9999: 0.7}]
）。
稀疏向量表示法
通过标记化和评分，文档可以表示为词袋向量，其中每个维度对应词汇表中的一个特定单词。只有文档中出现的单词才有非零值，从而形成稀疏向量表示法。稀疏向量可通过两种方法生成：
传统的统计技术
，如
TF-IDF
（词频-反向文档频率）和
BM25
（最佳匹配 25），根据词在语料库中的频率和重要性为词分配权重。这些方法将简单的统计数据计算为每个维度的分数，而每个维度代表一个标记。  Milvus 利用 BM25 方法提供内置的
全文搜索
功能，可自动将文本转换为稀疏向量，无需人工预处理。这种方法非常适合基于关键字的搜索，在这种搜索中，精确度和精确匹配非常重要。更多信息，请参阅
全文搜索
。
神经稀疏嵌入模型
是通过在大型数据集上训练生成稀疏表示的学习方法。它们通常是具有 Transformer 架构的深度学习模型，能够根据语义上下文对术语进行扩展和权衡。Milvus 还支持由
SPLADE
等模型外部生成的稀疏嵌入。详情请参阅
Embeddings
。
稀疏向量和原文可以存储在 Milvus 中，以便高效检索。下图概述了整个流程。
稀疏向量工作流程
除了稀疏向量，Milvus 还支持密集向量和二进制向量。密集向量是捕捉深层语义关系的理想选择，而二进制向量则在快速相似性比较和重复内容删除等场景中表现出色。更多信息，请参阅
密集向量
和
二进制向量
。
数据格式
在下面的章节中，我们将演示如何从 SPLADE 等学习到的稀疏嵌入模型中存储向量。如果您正在寻找对基于密集向量的语义搜索进行补充的东西，我们推荐使用 BM25 进行
全文搜索
，而不是 SPLADE，因为这样做比较简单。如果你已经进行了质量评估，并决定使用 SPLADE，那么你可以参考
Embeddings
，了解如何使用 SPLADE 生成稀疏向量。
Milvus 支持以下格式的稀疏向量输入：
字典列表（格式为
{dimension_index: value, ...}
)
# Represent each sparse vector using a dictionary
sparse_vectors = [{
27
:
0.5
,
100
:
0.3
,
5369
:
0.6
} , {
100
:
0.1
,
3
:
0.8
}]
稀疏矩阵（使用
scipy.sparse
类）
from
scipy.sparse
import
csr_matrix
# First vector: indices [27, 100, 5369] with values [0.5, 0.3, 0.6]
# Second vector: indices [3, 100] with values [0.8, 0.1]
indices = [[
27
,
100
,
5369
], [
3
,
100
]]
values = [[
0.5
,
0.3
,
0.6
], [
0.8
,
0.1
]]
sparse_vectors = [csr_matrix((vals, ([
0
]*
len
(idx), idx)), shape=(
1
,
5369
+
1
))
for
idx, vals
in
zip
(indices, values)]
元组迭代列表（如
[(dimension_index, value)]
)
# Represent each sparse vector using a list of iterables (e.g. tuples)
sparse_vector = [
    [(
27
,
0.5
), (
100
,
0.3
), (
5369
,
0.6
)],
    [(
100
,
0.1
), (
3
,
0.8
)]
    ]
定义 Collections Schema
创建 Collections 之前，需要指定 Collections Schema，其中定义字段，并可选择将文本字段转换为相应稀疏向量表示的函数。
添加字段
要在 Milvus 中使用稀疏向量，需要创建一个模式包括以下字段的 Collections：
一个
SPARSE_FLOAT_VECTOR
字段，预留用于存储稀疏向量，可以从
VARCHAR
字段自动生成，也可以直接在输入数据中提供。
通常，稀疏向量所代表的原始文本也会存储在 Collections 中。您可以使用
VARCHAR
字段来存储原始文本。
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

schema = client.create_schema(
    auto_id=
True
,
    enable_dynamic_fields=
True
,
)

schema.add_field(field_name=
"pk"
, datatype=DataType.VARCHAR, is_primary=
True
, max_length=
100
)
schema.add_field(field_name=
"sparse_vector"
, datatype=DataType.SPARSE_FLOAT_VECTOR)
schema.add_field(field_name=
"text"
, datatype=DataType.VARCHAR, max_length=
65535
, enable_analyzer=
True
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
"pk"
)
        .dataType(DataType.VarChar)
        .isPrimaryKey(
true
)
        .autoID(
true
)
        .maxLength(
100
)
        .build());
schema.addField(AddFieldReq.builder()
        .fieldName(
"sparse_vector"
)
        .dataType(DataType.SparseFloatVector)
        .build());
schema.addField(AddFieldReq.builder()
        .fieldName(
"text"
)
        .dataType(DataType.VarChar)
        .maxLength(
65535
)
        .enableAnalyzer(
true
)
        .build());
import
{
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
"sparse_vector"
,
data_type
:
DataType
.
SparseFloatVector
,
  },
  {
name
:
"text"
,
data_type
:
"VarChar"
,
enable_analyzer
:
true
,
enable_match
:
true
,
max_length
:
65535
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
    WithDataType(entity.FieldTypeVarChar).
    WithIsAutoID(
true
).
    WithIsPrimaryKey(
true
).
    WithMaxLength(
100
),
).WithField(entity.NewField().
    WithName(
"sparse_vector"
).
    WithDataType(entity.FieldTypeSparseVector),
).WithField(entity.NewField().
    WithName(
"text"
).
    WithDataType(entity.FieldTypeVarChar).
    WithEnableAnalyzer(
true
).
    WithMaxLength(
65535
),
)
export
primaryField=
'{
    "fieldName": "pk",
    "dataType": "VarChar",
    "isPrimary": true,
    "elementTypeParams": {
        "max_length": 100
    }
}'
export
vectorField=
'{
    "fieldName": "sparse_vector",
    "dataType": "SparseFloatVector"
}'
export
textField=
'{
    "fieldName": "text",
    "dataType": "VarChar",
    "elementTypeParams": {
        "max_length": 65535,
        "enable_analyzer": true
    }
}'
export
schema=
"{
    \"autoID\": true,
    \"fields\": [
$primaryField
,
$vectorField
,
$textField
]
}"
在此示例中，添加了三个字段：
pk
:该字段使用
VARCHAR
数据类型存储主键，该数据类型是自动生成的，最大长度为 100 字节。
sparse_vector
:该字段使用
SPARSE_FLOAT_VECTOR
数据类型存储稀疏向量。
text
:该字段使用
VARCHAR
数据类型存储文本字符串，最大长度为 65535 字节。
要启用 Milvus 或在数据插入过程中从指定文本字段生成稀疏向量 Embeddings，必须采取涉及函数的额外步骤。有关详细信息，请参阅
全文搜索
。
设置索引参数
为稀疏向量创建索引的过程与为
稠密向量
创建索引的过程类似，但在指定的索引类型 (
index_type
)、距离度量 (
metric_type
) 和索引参数 (
params
) 上有所不同。
Python
Java
NodeJS
Go
cURL
index_params = client.prepare_index_params()

index_params.add_index(
    field_name=
"sparse_vector"
,
    index_name=
"sparse_inverted_index"
,
    index_type=
"SPARSE_INVERTED_INDEX"
,
    metric_type=
"IP"
,
    params={
"inverted_index_algo"
:
"DAAT_MAXSCORE"
},
# or "DAAT_WAND" or "TAAT_NAIVE"
)
import
io.milvus.v2.common.IndexParam;
import
java.util.*;

List<IndexParam> indexes =
new
ArrayList
<>();

Map<String,Object> extraParams =
new
HashMap
<>();
extraParams.put(
"inverted_index_algo"
:
"DAAT_MAXSCORE"
);
// Algorithm used for building and querying the index
indexes.add(IndexParam.builder()
        .fieldName(
"sparse_vector"
)
        .indexName(
"sparse_inverted_index"
)
        .indexType(IndexParam.IndexType.SPARSE_INVERTED_INDEX)
        .metricType(IndexParam.MetricType.IP)
        .extraParams(extraParams)
        .build());
const
indexParams =
await
client.
createIndex
({
field_name
:
'sparse_vector'
,
metric_type
:
MetricType
.
IP
,
index_name
:
'sparse_inverted_index'
,
index_type
:
IndexType
.
SPARSE_INVERTED_INDEX
,
params
: {
inverted_index_algo
:
'DAAT_MAXSCORE'
, 
    },
});
idx := index.NewSparseInvertedIndex(entity.IP,
0.2
)
indexOption := milvusclient.NewCreateIndexOption(
"my_collection"
,
"sparse_vector"
, idx)
export
indexParams=
'[
        {
            "fieldName": "sparse_vector",
            "metricType": "IP",
            "indexName": "sparse_inverted_index",
            "indexType": "SPARSE_INVERTED_INDEX",
            "params":{"inverted_index_algo": "DAAT_MAXSCORE"}
        }
    ]'
本示例使用
SPARSE_INVERTED_INDEX
索引类型和
IP
作为度量。有关详细信息，请参阅以下资源：
SPARSE_INVERTED_INDEX
: 已解释的索引及其参数
度量类型
：不同字段类型支持的度量类型
全文搜索
：全文搜索的详细教程
创建 Collections
完成稀疏向量和索引设置后，就可以创建包含稀疏向量的 Collections。下面的示例使用
create_collection
方法创建一个名为
my_collection
的 Collection。
Python
Java
NodeJS
Go
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
import
{
MilvusClient
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
'http://localhost:19530'
});
await
client.
createCollection
({
collection_name
:
'my_collection'
,
schema
: schema,
index_params
: indexParams
});
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
必须为创建 Collections 时定义的所有字段提供数据，自动生成的字段除外（例如启用了
auto_id
的主键）。如果使用内置的 BM25 函数自动生成稀疏向量，则在插入数据时也应省略稀疏向量字段。
Python
Java
NodeJS
Go
cURL
data = [
    {
"text"
:
"information retrieval is a field of study."
,
"sparse_vector"
: {
1
:
0.5
,
100
:
0.3
,
500
:
0.8
}
    },
    {
"text"
:
"information retrieval focuses on finding relevant information in large datasets."
,
"sparse_vector"
: {
10
:
0.1
,
200
:
0.7
,
1000
:
0.9
}
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
import
java.util.ArrayList;
import
java.util.List;
import
java.util.SortedMap;
import
java.util.TreeMap;
Gson
gson
=
new
Gson
();
List<JsonObject> rows =
new
ArrayList
<>();

{
JsonObject
row
=
new
JsonObject
();
    row.addProperty(
"text"
,
"information retrieval is a field of study."
);
    
    SortedMap<Long, Float> sparse =
new
TreeMap
<>();
    sparse.put(
1L
,
0.5f
);
    sparse.put(
100L
,
0.3f
);
    sparse.put(
500L
,
0.8f
);
    row.add(
"sparse_vector"
, gson.toJsonTree(sparse));
    rows.add(row);
}
{
JsonObject
row
=
new
JsonObject
();
    row.addProperty(
"text"
,
"information retrieval focuses on finding relevant information in large datasets."
);
    
    SortedMap<Long, Float> sparse =
new
TreeMap
<>();
    sparse.put(
10L
,
0.1f
);
    sparse.put(
200L
,
0.7f
);
    sparse.put(
1000L
,
0.9f
);
    row.add(
"sparse_vector"
, gson.toJsonTree(sparse));
    rows.add(row);
}
InsertResp
insertResp
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
text
:
'information retrieval is a field of study.'
,
sparse_vector
: {
1
:
0.5
,
100
:
0.3
,
500
:
0.8
}
    {
text
:
'information retrieval focuses on finding relevant information in large datasets.'
,
sparse_vector
: {
10
:
0.1
,
200
:
0.7
,
1000
:
0.9
}
    },
];

client.
insert
({
collection_name
:
"my_collection"
,
data
: data
});
texts := []
string
{
"information retrieval is a field of study."
,
"information retrieval focuses on finding relevant information in large datasets."
,
}
textColumn := entity.NewColumnVarChar(
"text"
, texts)
// Prepare sparse vectors
sparseVectors :=
make
([]entity.SparseEmbedding,
0
,
2
)
sparseVector1, _ := entity.NewSliceSparseEmbedding([]
uint32
{
1
,
100
,
500
}, []
float32
{
0.5
,
0.3
,
0.8
})
sparseVectors =
append
(sparseVectors, sparseVector1)
sparseVector2, _ := entity.NewSliceSparseEmbedding([]
uint32
{
10
,
200
,
1000
}, []
float32
{
0.1
,
0.7
,
0.9
})
sparseVectors =
append
(sparseVectors, sparseVector2)
sparseVectorColumn := entity.NewColumnSparseVectors(
"sparse_vector"
, sparseVectors)

_, err = client.Insert(ctx, milvusclient.NewColumnBasedInsertOption(
"my_collection"
).
    WithColumns(
        sparseVectorColumn,
        textColumn
        
    ))
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
        {
            "text": "information retrieval is a field of study.",
            "sparse_vector": {"1": 0.5, "100": 0.3, "500": 0.8}
        },
        {
            "text": "information retrieval focuses on finding relevant information in large datasets.",
            "sparse_vector": {"10": 0.1, "200": 0.7, "1000": 0.9}
        }     
    ],
    "collectionName": "my_collection"
}'
执行相似性搜索
要使用稀疏向量执行相似性搜索，请准备好查询数据和搜索参数。
Python
Java
Go
NodeJS
cURL
# Prepare search parameters
search_params = {
"params"
: {
"drop_ratio_search"
:
0.2
},
# A tunable drop ratio parameter with a valid range between 0 and 1
}
# Query with sparse vector
query_data = [{
1
:
0.2
,
50
:
0.4
,
1000
:
0.7
}]
import
io.milvus.v2.service.vector.request.data.EmbeddedText;
import
io.milvus.v2.service.vector.request.data.SparseFloatVec;
// Prepare search parameters
Map<String,Object> searchParams =
new
HashMap
<>();
searchParams.put(
"drop_ratio_search"
,
0.2
);
// Query with the sparse vector
SortedMap<Long, Float> sparse =
new
TreeMap
<>();
sparse.put(
1L
,
0.2f
);
sparse.put(
50L
,
0.4f
);
sparse.put(
1000L
,
0.7f
);
SparseFloatVec
queryData
=
new
SparseFloatVec
(sparse);
// Prepare search parameters
annSearchParams := index.NewCustomAnnParam()
annSearchParams.WithExtraParam(
"drop_ratio_search"
,
0.2
)
// Query with the sparse vector
queryData, _ := entity.NewSliceSparseEmbedding([]
uint32
{
1
,
50
,
1000
}, []
float32
{
0.2
,
0.4
,
0.7
})
// Prepare search parameters
const
searchParams = {
drop_ratio_search
:
0.2
}
// Query with the sparse vector
const
queryData = [{
1
:
0.2
,
50
:
0.4
,
1000
:
0.7
}]
# Prepare search parameters
export
queryData=
'["What is information retrieval?"]'
# Query with the sparse vector
export
queryData=
'[{1: 0.2, 50: 0.4, 1000: 0.7}]'
然后，使用
search
方法执行相似性搜索：
Python
Java
NodeJS
Go
cURL
res = client.search(
    collection_name=
"my_collection"
,
    data=query_data,
    limit=
3
,
    output_fields=[
"pk"
],
    search_params=search_params,
    consistency_level=
"Strong"
)
print
(res)
# Output
# data: ["[{'id': '453718927992172266', 'distance': 0.6299999952316284, 'entity': {'pk': '453718927992172266'}}, {'id': '453718927992172265', 'distance': 0.10000000149011612, 'entity': {'pk': '453718927992172265'}}]"]
import
io.milvus.v2.service.vector.request.SearchReq;
import
io.milvus.v2.service.vector.response.SearchResp;
SparseFloatVec
queryVector
=
new
SparseFloatVec
(sparse);
SearchResp
searchR
=
client.search(SearchReq.builder()
        .collectionName(
"my_collection"
)
        .data(Collections.singletonList(queryData))
        .annsField(
"sparse_vector"
)
        .searchParams(searchParams)
        .consistencyLevel(ConsistencyLevel.STRONG)
        .topK(
3
)
        .outputFields(Collections.singletonList(
"pk"
))
        .build());
        
System.out.println(searchR.getSearchResults());
// Output
//
// [[SearchResp.SearchResult(entity={pk=457270974427187729}, score=0.63, id=457270974427187729), SearchResp.SearchResult(entity={pk=457270974427187728}, score=0.1, id=457270974427187728)]]
await
client.
search
({
collection_name
:
'my_collection'
,
data
: queryData,
limit
:
3
,
output_fields
: [
'pk'
],
params
: searchParams,
consistency_level
:
"Strong"
});
resultSets, err := client.Search(ctx, milvusclient.NewSearchOption(
"my_collection"
,
3
,
// limit
[]entity.Vector{queryData},
).WithANNSField(
"sparse_vector"
).
    WithOutputFields(
"pk"
).
    WithAnnParam(annSearchParams))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle err
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
"Pks: "
, resultSet.GetColumn(
"pk"
).FieldData().GetScalars())
}
// Results:
//   IDs:  string_data:{data:"457270974427187705"  data:"457270974427187704"}
//   Scores:  [0.63 0.1]
//   Pks:  string_data:{data:"457270974427187705"  data:"457270974427187704"}
export
params=
'{
    "consistencyLevel": "Strong"
}'
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
    "data": $queryData,
    "annsField": "sparse_vector",
    "limit": 3,
    "searchParams": $searchParams,
    "outputFields": ["pk"],
    "params": $params
}'
## {"code":0,"cost":0,"data":[{"distance":0.63,"id":"453577185629572535","pk":"453577185629572535"},{"distance":0.1,"id":"453577185629572534","pk":"453577185629572534"}]}
有关相似性搜索参数的更多信息，请参阅
基本向量搜索
。