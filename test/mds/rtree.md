RTREE
Compatible with Milvus 2.6.4+
RTREE
索引是一种基于树的数据结构，可加速对 Milvus 中
GEOMETRY
字段的查询。如果您的 Collections 以
已知文本 (WKT)
格式存储点、线或多边形等几何对象，并且希望加速空间过滤，
RTREE
是理想的选择。
工作原理
Milvus 使用
RTREE
索引来高效地组织和过滤几何数据，过程分为两个阶段：
第一阶段：建立索引
创建叶节点：
对于每个几何对象，计算其
最小边界矩形
(MBR)，即完全包含该对象的最小矩形，并将其存储为叶节点。
组合成较大的方框：
将附近的叶节点聚拢在一起，并用新的 MBR 对每个组进行包装，形成内部节点。例如，
B
组包含
D
和
E
；
C
组包含
F
和
G
。
添加根节点：
添加一个根节点，其 MBR 覆盖所有内部组，形成高度平衡的树形结构。
Retree 如何工作
第二阶段：加速查询
形成查询 MBR：
为查询几何图形计算 MBR。
修剪分支：
从根部开始，将查询 MBR 与每个内部节点进行比较。跳过 MBR 与查询 MBR 不相交的任何分支。
收集候选：
下降到相交的分支，收集候选叶节点。
精确匹配：
对于每个候选节点，执行精确空间谓词以确定真正的匹配。
创建 RTREE 索引
您可以在 Collections Schema 中定义的
GEOMETRY
字段上创建
RTREE
索引。
from
pymilvus
import
MilvusClient

client = MilvusClient(uri=
"http://localhost:19530"
)
# Replace with your server address
# Assume you have defined a GEOMETRY field named "geo" in your collection schema
# Prepare index parameters
index_params = client.prepare_index_params()
# Add RTREE index on the "geo" field
index_params.add_index(
field_name=
"geo"
,
index_type=
"RTREE"
,
# Spatial index for GEOMETRY
index_name=
"rtree_geo"
,
# Optional, name your index
params={}
# No extra params needed
)
# Create the index on the collection
client.create_index(
    collection_name=
"geo_demo"
,
    index_params=index_params
)
使用 RTREE 查询
您可以使用
filter
表达式中的几何操作符进行过滤。当目标
GEOMETRY
字段上存在
RTREE
时，Milvus 会使用它来自动修剪候选项。如果没有索引，过滤器将退回到全扫描。
有关可用的特定几何操作符的完整列表，请参阅
几何操作符
。
例 1：仅筛选
查找给定多边形内的所有几何对象：
filter_expr =
"ST_CONTAINS(geo, 'POLYGON ((0 0, 10 0, 10 10, 0 10, 0 0))')"
res = client.query(
    collection_name=
"geo_demo"
,
filter
=filter_expr,
    output_fields=[
"id"
,
"geo"
],
    limit=
10
)
print
(res)
# Expected: a list of rows where geo is entirely inside the polygon
例 2：向量搜索 + 空间过滤
查找同时与直线相交的最近向量：
# Assume you've also created an index on "vec" and loaded the collection.
query_vec = [[
0.1
,
0.2
,
0.3
,
0.4
,
0.5
]]
filter_expr =
"ST_INTERSECTS(geo, 'LINESTRING (1 1, 2 2)')"
hits = client.search(
    collection_name=
"geo_demo"
,
    data=query_vec,
    limit=
5
,
filter
=filter_expr,
    output_fields=[
"id"
,
"geo"
]
)
print
(hits)
# Expected: top-k by vector similarity among rows whose geo intersects the line
有关如何使用
GEOMETRY
字段的更多信息，请参阅
几何字段
。
删除索引
使用
drop_index()
方法从 Collections 中删除现有索引。
在
v2.6.3
或更早版本中，删除标量索引前必须释放 Collections。
从
v2.6.4
或更高版本开始，一旦不再需要标量索引，就可以直接删除，无需先释放 Collections。
client.drop_index(
    collection_name=
"geo_demo"
,
# Name of the collection
index_name=
"rtree_geo"
# Name of the index to drop
)