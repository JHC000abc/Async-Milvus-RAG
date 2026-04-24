标量字段索引
在 Milvus 中，标量索引用于通过特定的非向量字段值加速元过滤，类似于传统的数据库索引。本指南将指导你为整数、字符串等字段创建和配置标量索引。
本页面已被弃用。有关最新实现，请参阅
BITMAP
、
INVERTED
、
NGRAM
、
RTREE
STL_SORT
等。
标量索引类型
自动索引
：Milvus 根据标量字段的数据类型自动决定索引类型。这适用于不需要控制特定索引类型的情况。
自定义索引
：你可以指定精确的索引类型，如反转索引
或位图索引
。这为索引类型选择提供了更多控制。
自动索引
要使用自动
索引
，请在
add_index()
中省略 index_type 参数，以便 Milvus 根据标量字段类型推断索引类型。
要使用自动
索引
，请省略
IndexParam
中的 indexType 参数，以便 Milvus 根据标量字段类型推断索引类型。
要使用自动
索引
，请省略
createIndex()
中的 index_type 参数，以便 Milvus 根据标量字段类型推断索引类型。
有关标量数据类型和默认索引算法之间的映射，请参阅
标量字段索引算法
。
Python
Java
Node.js
# Auto indexing
client = MilvusClient(
    uri=
"http://localhost:19530"
)

index_params = MilvusClient.prepare_index_params()
# Prepare an empty IndexParams object, without having to specify any index parameters
index_params.add_index(
    field_name=
"scalar_1"
,
# Name of the scalar field to be indexed
index_type=
""
,
# Type of index to be created. For auto indexing, leave it empty or omit this parameter.
index_name=
"default_index"
# Name of the index to be created
)

client.create_index(
  collection_name=
"test_scalar_index"
,
# Specify the collection name
index_params=index_params
)
import
io.milvus.v2.common.IndexParam;
import
io.milvus.v2.service.index.request.CreateIndexReq;
IndexParam
indexParamForScalarField
=
IndexParam.builder()
    .fieldName(
"scalar_1"
)
// Name of the scalar field to be indexed
.indexName(
"default_index"
)
// Name of the index to be created
.indexType(
""
)
// Type of index to be created. For auto indexing, leave it empty or omit this parameter.
.build();

List<IndexParam> indexParams =
new
ArrayList
<>();
indexParams.add(indexParamForVectorField);
CreateIndexReq
createIndexReq
=
CreateIndexReq.builder()
    .collectionName(
"test_scalar_index"
)
// Specify the collection name
.indexParams(indexParams)
    .build();

client.createIndex(createIndexReq);
await
client.
createIndex
({
collection_name
:
"test_scalar_index"
,
// Specify the collection name
field_name
:
"scalar_1"
,
// Name of the scalar field to be indexed
index_name
:
"default_index"
,
// Name of the index to be created
index_type
:
""
// Type of index to be created. For auto indexing, leave it empty or omit this parameter.
})
自定义索引
要使用自定义
索引
，请在
add_index()
.
要使用自定义索引，请在.NET 文件中使用
indexType
参数指定特定的索引类型。
IndexParam
.
要使用自定义索引，请在 .NET 文件中使用
index_type
参数指定特定的索引类型。
createIndex()
.
下面的示例为标量字段
scalar_2
创建了一个反转索引。
Python
Java
Node.js
index_params = MilvusClient.prepare_index_params()
#  Prepare an IndexParams object
index_params.add_index(
    field_name=
"scalar_2"
,
# Name of the scalar field to be indexed
index_type=
"INVERTED"
,
# Type of index to be created
index_name=
"inverted_index"
# Name of the index to be created
)

client.create_index(
  collection_name=
"test_scalar_index"
,
# Specify the collection name
index_params=index_params
)
import
io.milvus.v2.common.IndexParam;
import
io.milvus.v2.service.index.request.CreateIndexReq;
IndexParam
indexParamForScalarField
=
IndexParam.builder()
    .fieldName(
"scalar_1"
)
// Name of the scalar field to be indexed
.indexName(
"inverted_index"
)
// Name of the index to be created
.indexType(
"INVERTED"
)
// Type of index to be created
.build();

List<IndexParam> indexParams =
new
ArrayList
<>();
indexParams.add(indexParamForVectorField);
CreateIndexReq
createIndexReq
=
CreateIndexReq.builder()
    .collectionName(
"test_scalar_index"
)
// Specify the collection name
.indexParams(indexParams)
    .build();

client.createIndex(createIndexReq);
await
client.
createIndex
({
collection_name
:
"test_scalar_index"
,
// Specify the collection name
field_name
:
"scalar_1"
,
// Name of the scalar field to be indexed
index_name
:
"inverted_index"
,
// Name of the index to be created
index_type
:
"INVERTED"
// Type of index to be created
})
方法和参数
prepare_index_params()
准备一个
IndexParams
对象。
add_index()
向
IndexParams
对象添加索引配置。
field_name
（字符串）
要索引的标量字段的名称。
index_type
（字符串
）：
要创建的标量索引的类型。对于隐式索引，请将其留空或省略此参数。
对于自定义索引，有效值为
倒排
：（推荐）倒排索引由术语字典组成，其中包含按字母顺序排序的所有标记词。有关详情，请参阅
标量索引
。
BITMAP
：
位图
索引：一种存储字段中所有唯一值的位图的索引类型。有关详情，请参阅
BITMAP
。
STL_SORT
：使用标准模板库排序算法对标量字段进行排序。仅支持数值字段（如 INT8、INT16、INT32、INT64、FLOAT、DOUBLE）。
Trie
用于快速前缀搜索和检索的树形数据结构。支持 VARCHAR 字段。
index_name
（字符串）
要创建的标量索引的名称。每个标量字段支持一个索引。
create_index()
在指定的 Collection 中创建索引。
collection_name
（字符串）
创建索引的 Collection 的名称。
索引参数
包含索引配置的
IndexParams
对象。
方法和参数
IndexParam
准备一个 IndexParam 对象。
fieldName
（字符串
） 要索引的标量字段的名称。
indexName
（字符串
） 要创建的标量索引的名称。每个标量字段支持一个索引。
indexType
（字符串
） 要创建的标量索引的类型。对于隐式索引，留空或省略此参数。 对于自定义索引，有效值为
倒排
：（推荐）倒排索引由术语字典组成，其中包含按字母顺序排序的所有标记词。有关详情，请参阅
标量索引
。
STL_SORT
：使用标准模板库排序算法对标量字段进行排序。支持布尔和数值字段（如 INT8、INT16、INT32、INT64、FLOAT、DOUBLE）。
Trie
用于快速前缀搜索和检索的树形数据结构。支持 VARCHAR 字段。
CreateIndexReq
在指定的 Collections 中创建索引。
collectionName
（字符串
） 创建索引的集合名称。
indexParams
(List
) 包含索引配置的 IndexParam 对象列表。
方法和参数
创建索引
在指定的 Collection 中创建索引。
collection_name
（字符串
） 创建索引的集合名称。
field_name
（字符串
） 要创建索引的标量字段的名称。
index_name
（字符串
） 要创建的标量索引的名称。每个标量字段支持一个索引。
index_type
（字符串
） 要创建的标量索引的类型。对于隐式索引，请将其留空或省略此参数。 对于自定义索引，有效值为
倒排
：（推荐）倒排索引由包含按字母顺序排序的所有标记词的术语字典组成。有关详情，请参阅
标量索引
。
STL_SORT
：使用标准模板库排序算法对标量字段进行排序。支持布尔和数值字段（如 INT8、INT16、INT32、INT64、FLOAT、DOUBLE）。
Trie
用于快速前缀搜索和检索的树形数据结构。支持 VARCHAR 字段。
验证结果
使用
list_indexes()
方法验证标量索引的创建：
使用
listIndexes()
方法验证标量索引的创建：
使用
listIndexes()
方法验证标量索引的创建：
Python
Java
Node.js
client.list_indexes(
    collection_name=
"test_scalar_index"
# Specify the collection name
)
# Output:
# ['default_index','inverted_index']
import
java.util.List;
import
io.milvus.v2.service.index.request.ListIndexesReq;
ListIndexesReq
listIndexesReq
=
ListIndexesReq.builder()
    .collectionName(
"test_scalar_index"
)
// Specify the collection name
.build();

List<String> indexNames = client.listIndexes(listIndexesReq);

System.out.println(indexNames);
// Output:
// [
//     "default_index",
//     "inverted_index"
// ]
res =
await
client.
listIndexes
({
collection_name
:
'test_scalar_index'
})
console
.
log
(res.
indexes
)
// Output:
// [
//     "default_index",
//     "inverted_index"
// ]