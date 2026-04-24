索引向量字段
本指南将指导您完成在 Collections 中创建和管理向量字段索引的基本操作。
本页已被弃用。有关最新实现，请参阅
IVF_FLAT
、
HNSW
等。
概述
利用存储在索引文件中的元数据，Milvus 以专门的结构组织数据，便于在搜索或查询过程中快速检索所需的信息。
Milvus 提供多种索引类型和指标，可对字段值进行排序，以实现高效的相似性搜索。下表列出了不同向量字段类型所支持的索引类型和度量。目前，Milvus 支持各种类型的向量数据，包括浮点嵌入（通常称为浮点向量或密集向量）、二进制嵌入（也称为二进制向量）和稀疏嵌入（也称为稀疏向量）。详情请参阅
内存索引
和
相似度指标
。
浮点嵌入
二进制嵌入
稀疏嵌入
度量类型
索引类型
欧氏距离 (L2)
内积 (IP)
余弦相似度 (COSINE)
平面
IVF_FLAT
IVF_SQ8
IVF_PQ
GPU_IVF_FLAT
GPU_IVF_PQ
HNSW
DISKANN
度量类型
索引类型
Jaccard (JACCARD)
哈明 (HAMMING)
BIN_FLAT
BIN_IVF_FLAT
度量类型
索引类型
IP
稀疏反转索引
BM25
稀疏_反转索引
从 Milvus 2.5.4 起，
SPARSE_WAND
已被弃用。建议在保持兼容性的前提下，使用
"inverted_index_algo": "DAAT_WAND"
来实现等价。更多信息，请参阅
稀疏向量
。
建议为经常访问的向量场和标量场创建索引。
准备工作
正如
管理 Collections
中所解释的，如果在创建 Collections 请求中指定了以下任一条件，Milvus 会在创建 Collections 时自动生成索引并将其加载到内存中：
向量场的维度和度量类型，或
Schema 和索引参数。
下面的代码片段对现有代码进行了重新利用，以建立与 Milvus 实例的连接，并在不指定其索引参数的情况下创建 Collections。在这种情况下，Collection 缺乏索引并保持未加载状态。
要准备索引，请使用
MilvusClient
连接到 Milvus 服务器，并通过使用
create_schema()
,
add_field()
和
create_collection()
.
要准备索引，使用
MilvusClientV2
连接到 Milvus 服务器，并通过使用
createSchema()
,
addField()
和
createCollection()
.
要准备索引，使用
MilvusClient
连接到 Milvus 服务器，并通过使用
createCollection()
.
Python
Java
Node.js
from
pymilvus
import
MilvusClient, DataType
# 1. Set up a Milvus client
client = MilvusClient(
    uri=
"http://localhost:19530"
)
# 2. Create schema
# 2.1. Create schema
schema = MilvusClient.create_schema(
    auto_id=
False
,
    enable_dynamic_field=
True
,
)
# 2.2. Add fields to schema
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
# 3. Create collection
client.create_collection(
    collection_name=
"customized_setup"
, 
    schema=schema, 
)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.common.DataType;
import
io.milvus.v2.service.collection.request.CreateCollectionReq;
String
CLUSTER_ENDPOINT
=
"http://localhost:19530"
;
// 1. Connect to Milvus server
ConnectConfig
connectConfig
=
ConnectConfig.builder()
    .uri(CLUSTER_ENDPOINT)
    .build();
MilvusClientV2
client
=
new
MilvusClientV2
(connectConfig);
// 2. Create a collection
// 2.1 Create schema
CreateCollectionReq.
CollectionSchema
schema
=
client.createSchema();
// 2.2 Add fields to schema
schema.addField(AddFieldReq.builder().fieldName(
"id"
).dataType(DataType.Int64).isPrimaryKey(
true
).autoID(
false
).build());
schema.addField(AddFieldReq.builder().fieldName(
"vector"
).dataType(DataType.FloatVector).dimension(
5
).build());
// 3 Create a collection without schema and index parameters
CreateCollectionReq
customizedSetupReq
=
CreateCollectionReq.builder()
.collectionName(
"customized_setup"
)
.collectionSchema(schema)
.build();

client.createCollection(customizedSetupReq);
// 1. Set up a Milvus Client
client =
new
MilvusClient
({address, token});
// 2. Define fields for the collection
const
fields = [
    {
name
:
"id"
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
]
// 3. Create a collection
res =
await
client.
createCollection
({
collection_name
:
"customized_setup"
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
索引一个 Collection
要为一个 Collection 创建索引或为一个 Collection 建立索引，请使用
prepare_index_params()
准备索引参数，并使用
create_index()
来创建索引。
要为集合创建索引或为集合建立索引，请使用
IndexParam
准备索引参数和
createIndex()
来创建索引。
要为集合创建索引或为集合创建索引，请使用
createIndex()
.
Python
Java
Node.js
# 4.1. Set up the index parameters
index_params = MilvusClient.prepare_index_params()
# 4.2. Add an index on the vector field.
index_params.add_index(
    field_name=
"vector"
,
    metric_type=
"COSINE"
,
    index_type=
"IVF_FLAT"
,
    index_name=
"vector_index"
,
    params={
"nlist"
:
128
}
)
# 4.3. Create an index file
client.create_index(
    collection_name=
"customized_setup"
,
    index_params=index_params,
    sync=
False
# Whether to wait for index creation to complete before returning. Defaults to True.
)
import
io.milvus.v2.common.IndexParam;
import
io.milvus.v2.service.index.request.CreateIndexReq;
// 4 Prepare index parameters
// 4.2 Add an index for the vector field "vector"
IndexParam
indexParamForVectorField
=
IndexParam.builder()
    .fieldName(
"vector"
)
    .indexName(
"vector_index"
)
    .indexType(IndexParam.IndexType.IVF_FLAT)
    .metricType(IndexParam.MetricType.COSINE)
    .extraParams(Map.of(
"nlist"
,
128
))
    .build();

List<IndexParam> indexParams =
new
ArrayList
<>();
indexParams.add(indexParamForVectorField);
// 4.3 Crate an index file
CreateIndexReq
createIndexReq
=
CreateIndexReq.builder()
    .collectionName(
"customized_setup"
)
    .indexParams(indexParams)
    .build();

client.createIndex(createIndexReq);
// 4. Set up index for the collection
// 4.1. Set up the index parameters
res =
await
client.
createIndex
({
collection_name
:
"customized_setup"
,
field_name
:
"vector"
,
index_type
:
"AUTOINDEX"
,
metric_type
:
"COSINE"
,
index_name
:
"vector_index"
,
params
: {
"nlist"
:
128
}
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
参数
参数
field_name
应用此对象的目标文件名称。
metric_type
用于衡量向量间相似性的算法。可能的值有
IP
、
L2
、
COSINE
、
JACCARD
、
HAMMING
。只有当指定字段是向量字段时才可用。更多信息，请参阅
Milvus 支持的索引
。
index_type
用于在特定字段中排列数据的算法名称。有关适用算法，请参阅
内存索引
和
磁盘索引
。
index_name
应用此对象后生成的索引文件名称。
params
指定索引类型的微调参数。有关可能的键和值范围的详细信息，请参阅
内存索引
。
collection_name
现有 Collections 的名称。
index_params
包含
IndexParam
对象列表的
IndexParams
对象。
sync
控制与客户端请求相关的索引构建方式。有效值：
True
(默认）：客户端等待索引完全建立后才返回。这意味着在该过程完成之前不会收到响应。
False
:客户端收到请求后立即返回，索引正在后台建立。要了解索引创建是否已完成，请使用
describe_index()
方法。
参数
说明
fieldName
应用此 IndexParam 对象的目标字段的名称。
indexName
应用此对象后生成的索引文件的名称。
indexType
用于在特定字段中排列数据的算法名称。有关适用算法，请参阅
内存索引
和
磁盘索引
。
metricType
索引使用的距离度量。可能的值有
IP
、
L2
、
COSINE
、
JACCARD
、
HAMMING
。
extraParams
额外的索引参数。有关详情，请参阅
内存索引
和
磁盘索引
。
参数
说明
collection_name
现有 Collections 的名称。
field_name
要创建索引的字段名称。
index_type
要创建索引的类型。
metric_type
用于测量向量距离的度量类型。
index_name
要创建的索引名称。
params
其他特定于索引的参数。
备注
目前，只能为 Collections 中的每个字段创建一个索引文件。
检查索引详细信息
创建索引后，可以检查其详细信息。
要检查索引详细信息，请使用
list_indexes()
列出索引名称，并用
describe_index()
获取索引详细信息。
要检查索引详情，请使用
describeIndex()
获取索引详情。
要检查索引详情，请使用
describeIndex()
获取索引详情。
Python
Java
Node.js
# 5. Describe index
res = client.list_indexes(
    collection_name=
"customized_setup"
)
print
(res)
# Output
#
# [
#     "vector_index",
# ]
res = client.describe_index(
    collection_name=
"customized_setup"
,
    index_name=
"vector_index"
)
print
(res)
# Output
#
# {
#     "index_type": ,
#     "metric_type": "COSINE",
#     "field_name": "vector",
#     "index_name": "vector_index"
# }
import
io.milvus.v2.service.index.request.DescribeIndexReq;
import
io.milvus.v2.service.index.response.DescribeIndexResp;
// 5. Describe index
// 5.1 List the index names
ListIndexesReq
listIndexesReq
=
ListIndexesReq.builder()
    .collectionName(
"customized_setup"
)
    .build();

List<String> indexNames = client.listIndexes(listIndexesReq);

System.out.println(indexNames);
// Output:
// [
//     "vector_index"
// ]
// 5.2 Describe an index
DescribeIndexReq
describeIndexReq
=
DescribeIndexReq.builder()
    .collectionName(
"customized_setup"
)
    .indexName(
"vector_index"
)
    .build();
DescribeIndexResp
describeIndexResp
=
client.describeIndex(describeIndexReq);

System.out.println(JSONObject.toJSON(describeIndexResp));
// Output:
// {
//     "metricType": "COSINE",
//     "indexType": "AUTOINDEX",
//     "fieldName": "vector",
//     "indexName": "vector_index"
// }
// 5. Describe the index
res =
await
client.
describeIndex
({
collection_name
:
"customized_setup"
,
index_name
:
"vector_index"
})
console
.
log
(
JSON
.
stringify
(res.
index_descriptions
,
null
,
2
))
// Output
//
// [
//   {
//     "params": [
//       {
//         "key": "index_type",
//         "value": "AUTOINDEX"
//       },
//       {
//         "key": "metric_type",
//         "value": "COSINE"
//       }
//     ],
//     "index_name": "vector_index",
//     "indexID": "449007919953063141",
//     "field_name": "vector",
//     "indexed_rows": "0",
//     "total_rows": "0",
//     "state": "Finished",
//     "index_state_fail_reason": "",
//     "pending_index_rows": "0"
//   }
// ]
//
您可以检查在特定字段上创建的索引文件，并收集使用该索引文件索引的行数统计。
删除索引
如果不再需要索引，可以直接将其删除。
在丢弃索引之前，首先要确保它已被释放。
要删除索引，请使用
drop_index()
.
要删除索引，请使用
dropIndex()
.
要删除索引，请使用
dropIndex()
.
Python
Java
Node.js
# 6. Drop index
client.drop_index(
    collection_name=
"customized_setup"
,
    index_name=
"vector_index"
)
// 6. Drop index
DropIndexReq
dropIndexReq
=
DropIndexReq.builder()
    .collectionName(
"customized_setup"
)
    .indexName(
"vector_index"
)
    .build();

client.dropIndex(dropIndexReq);
// 6. Drop the index
res =
await
client.
dropIndex
({
collection_name
:
"customized_setup"
,
index_name
:
"vector_index"
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