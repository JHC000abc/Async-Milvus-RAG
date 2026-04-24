几何字段
Compatible with Milvus 2.6.4+
在构建地理信息系统（GIS）、制图工具或基于位置的服务等应用程序时，您经常需要存储和查询几何数据。Milvus 中的
GEOMETRY
数据类型提供了一种本地方式来存储和查询灵活的几何数据，从而解决了这一难题。
例如，当您需要将向量相似性与空间约束相结合时，请使用 GEOMETRY 字段：
位置服务（LBS）："查找该城市街区
内的
相似 POI
多种模式搜索："检索该点
1km 范围内的
相似照片
地图与物流："区域
内的
资产 "或 "
与
路径
相交的
路线"
要使用 GEOMETRY 字段，请将 SDK 升级到最新版本。
什么是 "地理坐标 "字段？
GEOMETRY 字段是 Milvus 中一种 Schema 定义的数据类型 (
DataType.GEOMETRY
) ，用于存储几何数据。在处理几何字段时，您可以使用 "
已知文本"（WKT）
格式与数据交互，这是一种用于插入数据和查询的人类可读表示法。在内部，Milvus 会将 WKT 转换为
已知二进制 (WKB)
，以提高存储和处理效率，但您不需要直接处理 WKB。
GEOMETRY
数据类型支持以下几何对象：
点
：
POINT (x y)
；例如，
POINT (13.403683 52.520711)
，其中
x
= 经度，
y
= 纬度
LINESTRING
:
LINESTRING (x1 y1, x2 y2, …)
；举例来说、
LINESTRING (13.40 52.52, 13.41 52.51)
POLYGON
:
POLYGON ((x1 y1, x2 y2, x3 y3, x1 y1))
；举例说明、
POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))
MULTIPOINT
:
MULTIPOINT ((x1 y1), (x2 y2), …)
, 例如、
MULTIPOINT ((10 40), (40 30), (20 20), (30 10))
multilinestring
：
MULTILINESTRING ((x1 y1, …), (xk yk, …))
例如
MULTILINESTRING ((10 10, 20 20, 10 40), (40 40, 30 30, 40 20, 30 10))
MULTIPOLYGON
:
MULTIPOLYGON (((outer ring ...)), ((outer ring ...)))
, 例如、
MULTIPOLYGON (((30 20, 45 40, 10 40, 30 20)), ((15 5, 40 10, 10 20, 5 10, 15 5)))
GEOMETRYCOLLECTION
:
GEOMETRYCOLLECTION(POINT(x y), LINESTRING(x1 y1, x2 y2), ...)
, 例如、
GEOMETRYCOLLECTION (POINT (40 10), LINESTRING (10 10, 20 20, 10 40), POLYGON ((40 40, 20 45, 45 30, 40 40)))
基本操作符
使用
GEOMETRY
字段的工作流程包括在 Collections Schema 中定义字段、插入几何数据，然后使用特定的过滤表达式查询数据。
步骤 1：定义几何字段
要使用
GEOMETRY
字段，请在创建 Collection 时在 Collection Schema 中明确定义该字段。下面的示例演示了如何创建一个带有
geo
类型字段
DataType.GEOMETRY
的 Collections。
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
MilvusClient, DataType
import
numpy
as
np

dim =
8
collection_name =
"geo_collection"
milvus_client = MilvusClient(
"http://localhost:19530"
)
# Create schema with a GEOMETRY field
schema = milvus_client.create_schema(enable_dynamic_field=
True
)
schema.add_field(
"id"
, DataType.INT64, is_primary=
True
)
schema.add_field(
"embeddings"
, DataType.FLOAT_VECTOR, dim=dim)
schema.add_field(
"geo"
, DataType.GEOMETRY, nullable=
True
)
schema.add_field(
"name"
, DataType.VARCHAR, max_length=
128
)

milvus_client.create_collection(collection_name, schema=schema, consistency_level=
"Strong"
)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.common.DataType;
private
static
final
String
COLLECTION_NAME
=
"geo_collection"
;
private
static
final
Integer
DIM
=
128
;
MilvusClientV2
client
=
new
MilvusClientV2
(ConnectConfig.builder()
        .uri(
"http://localhost:19530"
)
        .token(
"root:Milvus"
)
        .build());
        
CreateCollectionReq.
CollectionSchema
collectionSchema
=
CreateCollectionReq.CollectionSchema.builder()
        .enableDynamicField(
true
)
        .build();
collectionSchema.addField(AddFieldReq.builder()
        .fieldName(
"id"
)
        .dataType(DataType.Int64)
        .isPrimaryKey(
true
)
        .build());
collectionSchema.addField(AddFieldReq.builder()
        .fieldName(
"embeddings"
)
        .dataType(DataType.FloatVector)
        .dimension(DIM)
        .build());
collectionSchema.addField(AddFieldReq.builder()
        .fieldName(
"geo"
)
        .dataType(DataType.Geometry)
        .isNullable(
true
)
        .build());
collectionSchema.addField(AddFieldReq.builder()
        .fieldName(
"name"
)
        .dataType(DataType.VarChar)
        .maxLength(
128
)
        .build());
CreateCollectionReq
requestCreate
=
CreateCollectionReq.builder()
        .collectionName(COLLECTION_NAME)
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
'@zilliz/milvus2-sdk-node'
;
const
milvusClient =
new
MilvusClient
(
'http://localhost:19530'
);
const
schema = [
  {
name
:
'id'
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
},
  {
name
:
'embeddings'
,
data_type
:
DataType
.
FloatVector
,
dim
:
8
},
{
name
:
'geo'
,
data_type
:
DataType
.
Geometry
,
is_nullable
:
true
},
{
name
:
'name'
,
data_type
:
DataType
.
VarChar
,
max_length
:
128
},
];
await
milvusClient.
createCollection
({
collection_name
:
'geo_collection'
,
fields
: schema,
consistency_level
:
'Strong'
,
});
// go
# restful
在此示例中，在 Collection schema 中定义的
GEOMETRY
字段允许使用
nullable=True
的空值。有关详情，请参阅 "
可空值和默认值
"。
步骤 2：插入数据
插入带有
WKT
格式几何数据的实体。下面是一个包含多个地理点的示例：
Python
Java
NodeJS
Go
cURL
rng = np.random.default_rng(seed=
19530
)
geo_points = [
'POINT(13.399710 52.518010)'
,
'POINT(13.403934 52.522877)'
,
'POINT(13.405088 52.521124)'
,
'POINT(13.408223 52.516876)'
,
'POINT(13.400092 52.521507)'
,
'POINT(13.408529 52.519274)'
,
]

rows = [
    {
"id"
:
1
,
"name"
:
"Shop A"
,
"embeddings"
: rng.random((
1
, dim))[
0
],
"geo"
: geo_points[
0
]},
    {
"id"
:
2
,
"name"
:
"Shop B"
,
"embeddings"
: rng.random((
1
, dim))[
0
],
"geo"
: geo_points[
1
]},
    {
"id"
:
3
,
"name"
:
"Shop C"
,
"embeddings"
: rng.random((
1
, dim))[
0
],
"geo"
: geo_points[
2
]},
    {
"id"
:
4
,
"name"
:
"Shop D"
,
"embeddings"
: rng.random((
1
, dim))[
0
],
"geo"
: geo_points[
3
]},
    {
"id"
:
5
,
"name"
:
"Shop E"
,
"embeddings"
: rng.random((
1
, dim))[
0
],
"geo"
: geo_points[
4
]},
    {
"id"
:
6
,
"name"
:
"Shop F"
,
"embeddings"
: rng.random((
1
, dim))[
0
],
"geo"
: geo_points[
5
]},
]

insert_result = milvus_client.insert(collection_name, rows)
print
(insert_result)
# Expected output:
# {'insert_count': 6, 'ids': [1, 2, 3, 4, 5, 6]}
import
com.google.gson.Gson;
import
com.google.gson.JsonObject;
import
io.milvus.v2.service.vector.request.InsertReq;

List<String> geoPoints = Arrays.asList(
"POINT(13.399710 52.518010)"
,
"POINT(13.403934 52.522877)"
,
"POINT(13.405088 52.521124)"
,
"POINT(13.408223 52.516876)"
,
"POINT(13.400092 52.521507)"
,
"POINT(13.408529 52.519274)"
);
List<String> names = Arrays.asList(
"Shop A"
,
"Shop B"
,
"Shop C"
,
"Shop D"
,
"Shop E"
,
"Shop F"
);
Random
ran
=
new
Random
();
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
for
(
int
i
=
0
; i < geoPoints.size(); i++) {
JsonObject
row
=
new
JsonObject
();
    row.addProperty(
"id"
, i);
    row.addProperty(
"geo"
, geoPoints.get(i));
    row.addProperty(
"name"
, names.get(i));
    List<Float> vector =
new
ArrayList
<>();
for
(
int
d
=
0
; d < DIM; ++d) {
        vector.add(ran.nextFloat());
    }
    row.add(
"embeddings"
, gson.toJsonTree(vector));
    rows.add(row);
}

client.insert(InsertReq.builder()
        .collectionName(COLLECTION_NAME)
        .data(rows)
        .build());
const
geo_points = [
'POINT(13.399710 52.518010)'
,
'POINT(13.403934 52.522877)'
,
'POINT(13.405088 52.521124)'
,
'POINT(13.408223 52.516876)'
,
'POINT(13.400092 52.521507)'
,
'POINT(13.408529 52.519274)'
,
];
const
rows = [
    {
"id"
:
1
,
"name"
:
"Shop A"
,
"embeddings"
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
,
0.6
,
0.7
,
0.8
],
"geo"
: geo_points[
0
]},
    {
"id"
:
2
,
"name"
:
"Shop B"
,
"embeddings"
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
,
0.7
,
0.8
,
0.9
],
"geo"
: geo_points[
1
]},
    {
"id"
:
3
,
"name"
:
"Shop C"
,
"embeddings"
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
,
0.8
,
0.9
,
1.0
],
"geo"
: geo_points[
2
]},
    {
"id"
:
4
,
"name"
:
"Shop D"
,
"embeddings"
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
,
0.9
,
1.0
,
0.1
],
"geo"
: geo_points[
3
]},
    {
"id"
:
5
,
"name"
:
"Shop E"
,
"embeddings"
: [
0.5
,
0.6
,
0.7
,
0.8
,
0.9
,
1.0
,
0.1
,
0.2
],
"geo"
: geo_points[
4
]},
    {
"id"
:
6
,
"name"
:
"Shop F"
,
"embeddings"
: [
0.6
,
0.7
,
0.8
,
0.9
,
1.0
,
0.1
,
0.2
,
0.3
],
"geo"
: geo_points[
5
]},
];
const
insert_result =
await
milvusClient.
insert
({
collection_name
:
'geo_collection'
,
data
: rows,
});
console
.
log
(insert_result);
// go
# restful
第 3 步：过滤操作符
在对
GEOMETRY
字段执行过滤操作之前，请确保：
已为每个向量字段创建索引。
已将 Collections 载入内存。
显示代码
Python
Java
NodeJS
Go
cURL
index_params = milvus_client.prepare_index_params()
index_params.add_index(field_name=
"embeddings"
, metric_type=
"L2"
)

milvus_client.create_index(collection_name, index_params)
milvus_client.load_collection(collection_name)
import
io.milvus.v2.common.IndexParam;
import
io.milvus.v2.service.index.request.CreateIndexReq;

List<IndexParam> indexParams =
new
ArrayList
<>();
indexParams.add(IndexParam.builder()
        .fieldName(
"embeddings"
)
        .indexType(IndexParam.IndexType.AUTOINDEX)
        .metricType(IndexParam.MetricType.L2)
        .build());
client.createIndex(CreateIndexReq.builder()
        .collectionName(COLLECTION_NAME)
        .indexParams(indexParams)
        .build());
const
index_params = {
field_name
:
"embeddings"
,
index_type
:
"IVF_FLAT"
,
metric_type
:
"L2"
,
params
: {
nlist
:
128
},
};
await
milvusClient.
createIndex
({
collection_name
:
'geo_collection'
,
index_name
:
'embeddings_index'
,
index_params
: index_params,
});
await
milvusClient.
loadCollection
({
collection_name
:
'geo_collection'
,
});
// go
# restful
满足这些要求后，您就可以使用带有专用几何操作符的表达式，根据几何值对集合进行过滤。
定义过滤表达式
要在
GEOMETRY
字段上进行筛选，请在表达式中使用几何操作符：
一般：
{operator}(geo_field, '{wkt}')
基于距离：
ST_DWITHIN(geo_field, '{wkt}', distance)
其中
operator
是支持的几何操作符之一（如
ST_CONTAINS
,
ST_INTERSECTS
）。操作符名称必须全部大写或小写。有关支持的操作符列表，请参阅
支持的几何图形操作符
。
geo_field
是
GEOMETRY
字段的名称。
'{wkt}'
是要查询的几何体的 WKT 表示形式。
distance
是专门用于
ST_DWITHIN
的阈值。
以下示例演示了如何在筛选表达式中使用不同的几何图形专用操作符：
示例 1：查找矩形区域内的实体
Python
Java
NodeJS
Go
cURL
top_left_lon, top_left_lat =
13.403683
,
52.520711
bottom_right_lon, bottom_right_lat =
13.455868
,
52.495862
bounding_box_wkt =
f"POLYGON((
{top_left_lon}
{top_left_lat}
,
{bottom_right_lon}
{top_left_lat}
,
{bottom_right_lon}
{bottom_right_lat}
,
{top_left_lon}
{bottom_right_lat}
,
{top_left_lon}
{top_left_lat}
))"
query_results = milvus_client.query(
    collection_name,
filter
=
f"st_within(geo, '
{bounding_box_wkt}
')"
,
output_fields=[
"name"
,
"geo"
]
)
for
ret
in
query_results:
print
(ret)
# Expected output:
# {'name': 'Shop D', 'geo': 'POINT (13.408223 52.516876)', 'id': 4}
# {'name': 'Shop F', 'geo': 'POINT (13.408529 52.519274)', 'id': 6}
# {'name': 'Shop A', 'geo': 'POINT (13.39971 52.51801)', 'id': 1}
# {'name': 'Shop B', 'geo': 'POINT (13.403934 52.522877)', 'id': 2}
# {'name': 'Shop C', 'geo': 'POINT (13.405088 52.521124)', 'id': 3}
# {'name': 'Shop D', 'geo': 'POINT (13.408223 52.516876)', 'id': 4}
# {'name': 'Shop E', 'geo': 'POINT (13.400092 52.521507)', 'id': 5}
# {'name': 'Shop F', 'geo': 'POINT (13.408529 52.519274)', 'id': 6}
import
io.milvus.v2.service.vector.request.QueryReq;
import
io.milvus.v2.service.vector.response.QueryResp;
float
topLeftLon
=
13.403683f
;
float
topLeftLat
=
52.520711f
;
float
bottomRightLon
=
13.455868f
;
float
bottomRightLat
=
52.495862f
;
String
boundingBoxWkt
=
String.format(
"POLYGON((%f %f, %f %f, %f %f, %f %f, %f %f))"
,
        topLeftLon, topLeftLat, bottomRightLon, topLeftLat, bottomRightLon, bottomRightLat,
        topLeftLon, bottomRightLat, topLeftLon, topLeftLat);
String
filter
=
String.format(
"st_within(geo, '%s')"
, boundingBoxWkt);
QueryResp
queryResp
=
client.query(QueryReq.builder()
        .collectionName(COLLECTION_NAME)
        .filter(filter)
        .outputFields(Arrays.asList(
"name"
,
"geo"
))
        .build());
List<QueryResp.QueryResult> queryResults = queryResp.getQueryResults();
System.out.println(
"Query results:"
);
for
(QueryResp.QueryResult result : queryResults) {
    System.out.println(result.getEntity());
}
const
top_left_lon =
13.403683
;
const
top_left_lat =
52.520711
;
const
bottom_right_lon =
13.455868
;
const
bottom_right_lat =
52.495862
;
const
bounding_box_wkt =
`POLYGON((
${top_left_lon}
${top_left_lat}
,
${bottom_right_lon}
${top_left_lat}
,
${bottom_right_lon}
${bottom_right_lat}
,
${top_left_lon}
${bottom_right_lat}
,
${top_left_lon}
${top_left_lat}
))`
;
const
query_results =
await
milvusClient.
query
({
collection_name
:
'geo_collection'
,
filter
:
`st_within(geo, '
${bounding_box_wkt}
')`
,
output_fields
: [
'name'
,
'geo'
],
});
for
(
const
ret
of
query_results.
data
) {
console
.
log
(ret);
}
// go
# restful
例 2：查找距离中心点 1km 范围内的实体
Python
Java
NodeJS
Go
cURL
center_point_lon, center_point_lat =
13.403683
,
52.520711
radius_meters =
1000.0
central_point_wkt =
f"POINT(
{center_point_lon}
{center_point_lat}
)"
query_results = milvus_client.query(
    collection_name,
filter
=
f"st_dwithin(geo, '
{central_point_wkt}
',
{radius_meters}
)"
,
output_fields=[
"name"
,
"geo"
]
)
for
ret
in
query_results:
print
(ret)
# Expected output:
# hit: {'id': 4, 'distance': 0.9823770523071289, 'entity': {'name': 'Shop D', 'geo': 'POINT (13.408223 52.516876)'}}
import
io.milvus.v2.service.vector.request.QueryReq;
import
io.milvus.v2.service.vector.response.QueryResp;
float
centerPointLon
=
13.403683f
;
float
centerPointLat
=
52.520711f
;
float
radiusMeters
=
1000.0f
;
String
centralPointWkt
=
String.format(
"POINT(%f %f)"
, centerPointLon, centerPointLat);
String filter=String.format(
"st_dwithin(geo, '%s', %f)"
, centralPointWkt, radiusMeters);
QueryResp
queryResp
=
client.query(QueryReq.builder()
        .collectionName(COLLECTION_NAME)
        .filter(filter)
        .outputFields(Arrays.asList(
"name"
,
"geo"
))
        .build());
List<QueryResp.QueryResult> queryResults = queryResp.getQueryResults();
System.out.println(
"Query results:"
);
for
(QueryResp.QueryResult result : queryResults) {
    System.out.println(result.getEntity());
}
const
center_point_lon =
13.403683
;
const
center_point_lat =
52.520711
;
const
radius_meters =
1000.0
;
const
central_point_wkt =
`POINT(
${center_point_lon}
${center_point_lat}
)`
;
const
query_results_dwithin =
await
milvusClient.
query
({
collection_name
:
'geo_collection'
,
filter
:
`st_dwithin(geo, '
${central_point_wkt}
',
${radius_meters}
)`
,
output_fields
: [
'name'
,
'geo'
],
});
for
(
const
ret
of
query_results_dwithin.
data
) {
console
.
log
(ret);
}
// go
# restful
例 3：将向量相似性与空间过滤器相结合
Python
Java
NodeJS
Go
cURL
vectors_to_search = rng.random((
1
, dim))
result = milvus_client.search(
    collection_name,
    vectors_to_search,
    limit=
3
,
    output_fields=[
"name"
,
"geo"
],
filter
=
f"st_within(geo, '
{bounding_box_wkt}
')"
)
for
hits
in
result:
for
hit
in
hits:
print
(
f"hit:
{hit}
"
)
# Expected output:
# hit: {'id': 6, 'distance': 1.3406795263290405, 'entity': {'name': 'Shop F', 'geo': 'POINT (13.408529 52.519274)'}}
import
io.milvus.v2.service.vector.request.SearchReq;
import
io.milvus.v2.service.vector.request.data.FloatVec;
import
io.milvus.v2.service.vector.response.SearchResp;
Random
ran
=
new
Random
();
List<Float> vector =
new
ArrayList
<>();
for
(
int
d
=
0
; d < DIM; ++d) {
    vector.add(ran.nextFloat());
}
String filter=String.format(
"st_within(geo, '%s')"
, boundingBoxWkt);
SearchReq
request
=
SearchReq.builder()
        .collectionName(COLLECTION_NAME)
        .data(Collections.singletonList(
new
FloatVec
(vector)))
        .limit(
3
)
        .filter(filter)
        .outputFields(Arrays.asList(
"name"
,
"geo"
))
        .build();
SearchResp
statusR
=
client.search(request);
List<List<SearchResp.SearchResult>> searchResults = statusR.getSearchResults();
for
(List<SearchResp.SearchResult> results : searchResults) {
for
(SearchResp.SearchResult result : results) {
        System.out.printf(
"ID: %d, Score: %f, %s\n"
, (
long
)result.getId(), result.getScore(), result.getEntity().toString());
    }
}
const
vectors_to_search = [[
0.1
,
0.2
,
0.3
,
0.4
,
0.5
,
0.6
,
0.7
,
0.8
]];
const
search_results =
await
milvusClient.
search
({
collection_name
:
"geo_collection"
,
vectors
: vectors_to_search,
limit
:
3
,
output_fields
: [
"name"
,
"geo"
],
filter
:
`st_within(geo, '
${bounding_box_wkt}
')`
,
});
for
(
const
hits
of
search_results.
results
) {
for
(
const
hit
of
hits) {
console
.
log
(
`hit:
${
JSON
.stringify(hit)}
`
);
  }
}
// go
# restful
下一步：加速查询
默认情况下，在没有索引的情况下对
GEOMETRY
字段的查询将对所有行执行全扫描，这在大型数据集上可能会很慢。要加速几何查询，请在 GEOMETRY 字段上创建
RTREE
索引。
有关详细信息，请参阅
RTREE
。
常见问题
如果我为我的 Collections 启用了动态字段功能，我是否可以在动态字段键中插入几何数据？
不能，几何数据不能插入动态字段。在插入几何数据之前，请确保
GEOMETRY
字段已在 Collections Schema 中明确定义。
几何字段支持 mmap 功能吗？
是的，
GEOMETRY
字段支持 mmap。有关详细信息，请参阅
使用 mmap
。
能否将 GEOMETRY 字段定义为可空或设置默认值？
可以，GEOMETRY 字段支持
nullable
属性和 WKT 格式的默认值。有关详细信息，请参阅
可归零和默认值
。