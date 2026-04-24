几何操作符
Compatible with Milvus 2.6.4+
Milvus 支持对
GEOMETRY
字段进行空间过滤的一系列操作符，这对于管理和分析几何数据至关重要。这些操作符允许您根据对象之间的几何关系检索实体。
所有几何操作符都通过接收两个几何参数来操作：
Collection
schema 中定义的
GEOMETRY
字段名
和以
Well-Known Text
(WKT) 格式表示的目标几何对象。
使用语法
要对
GEOMETRY
字段进行筛选，请在表达式中使用几何操作符：
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
要了解有关 Milvus 中
GEOMETRY
字段的更多信息，请参阅
几何字段
。
支持的几何操作符
下表列出了 Milvus 中可用的几何操作符。
操作符名称必须
全部大写
或
全部小写
。请勿在同一操作符名称中混合使用大小写。
操作符
说明
示例
ST_EQUALS(A, B)
/
st_equals(A, B)
如果两个几何图形在空间上完全相同，即具有相同的点集和尺寸，则返回 TRUE。
两个几何图形（A 和 B）在空间上是否完全相同？
ST_CONTAINS(A, B)
/
st_contains(A, B)
如果几何体 A 完全包含几何体 B，且它们的内部至少有一个共同点，则返回 TRUE。
一个城市边界（A）是否包含一个特定的公园（B）？
ST_CROSSES(A, B)
/
st_crosses(A, B)
如果几何体 A 和 B 部分相交但不完全包含对方，则返回 TRUE。
两条道路（A 和 B）是否交叉？
ST_INTERSECTS(A, B)
/
st_intersects(A, B)
如果几何图形 A 和 B 至少有一个公共点，则返回 TRUE。这是最通用、使用最广泛的空间查询。
搜索区域（A）是否与任何商店位置（B）相交？
ST_OVERLAPS(A, B)
/
st_overlaps(A, B)
如果几何图形 A 和 B 的尺寸相同、部分重叠且都不完全包含其他几何图形，则返回 TRUE。
两个地块（A 和 B）是否重叠？
ST_TOUCHES(A, B)
/
st_touches(A, B)
如果几何图形 A 和 B 有共同的边界，但内部不相交，则返回 TRUE。
两个相邻的属性（A 和 B）有共同边界吗？
ST_WITHIN(A, B)
/
st_within(A, B)
如果几何体 A 完全包含在几何体 B 中，且它们的内部至少有一个共同点，则返回 TRUE。这是
ST_Contains(B, A)
的逆运算。
特定兴趣点（A）是否在定义的搜索半径（B）内？
ST_DWITHIN(A, B, distance)
/
st_dwithin(A, B, distance)
如果几何体 A 和几何体 B 之间的距离小于或等于指定距离，则返回 TRUE。
注意
：几何体 B 目前只支持点。距离单位为米。
查找距离特定点（B）5000 米以内的所有点。
ST_EQUALS / ST_equals
如果两个几何图形在空间上相同，即具有相同的点集和尺寸，则
ST_EQUALS
操作符返回 TRUE。这对于验证两个存储的几何对象是否代表完全相同的位置和形状非常有用。
示例
假设您要检查存储的几何体（如点或多边形）是否与目标几何体完全相同。例如，您可以将存储的点与特定的兴趣点进行比较。
# The filter expression to check if a geometry matches a specific point
filter
=
"ST_EQUALS(geo_field, 'POINT(10 20)')"
ST_CONTAINS / st_contains
如果第一个几何体完全包含第二个几何体，则
ST_CONTAINS
操作符返回 TRUE。这对于查找多边形中的点或较大多边形中的较小多边形非常有用。
示例
想象一下，您有一个城市区域 Collections，并希望找到一个特定的兴趣点（如餐馆），该兴趣点位于给定区域的边界内。
# The filter expression to find geometries completely within a specific polygon.
filter
=
"ST_CONTAINS(geo_field, 'POLYGON ((0 0, 10 0, 10 10, 0 10, 0 0))')"
ST_CROSSES / st_crosses
如果两个几何图形的交点形成的几何图形的维度低于原始几何图形的维度，则
ST_CROSSES
操作符返回
TRUE
。这通常适用于与多边形或另一条直线相交的直线。
示例
您想查找所有穿越特定边界线（另一条线串）或进入保护区（多边形）的远足路径（线串）。
# The filter expression to find geometries that cross a line string.
filter
=
"ST_CROSSES(geo_field, 'LINESTRING(5 0, 5 10)')"
ST_INTERSECTS / ST_intersects
如果两个几何图形的边界或内部有任何共同点，
ST_INTERSECTS
操作符会返回
TRUE
。这是一个通用操作符，用于检测任何形式的空间重叠。
示例
如果您有一个道路 Collections，并希望找到所有与代表拟建新道路的特定线串交叉或接触的道路，您可以使用
ST_INTERSECTS
.
# The filter expression to find geometries that intersect with a specific line string.
filter
=
"ST_INTERSECTS(geo_field, 'LINESTRING (1 1, 2 2)')"
ST_OVERLAPS / st_overlaps
如果两个尺寸相同的几何图形有部分交集，即交集本身的尺寸与原始几何图形相同，但不等于其中任何一个，则
ST_OVERLAPS
操作符返回
TRUE
。
示例
您有一组重叠的销售区域，希望找到与新提议的销售区域部分重叠的所有区域。
# The filter expression to find geometries that partially overlap with a polygon.
filter
=
"ST_OVERLAPS(geo_field, 'POLYGON((0 0, 0 10, 10 10, 10 0, 0 0))')"
ST_TOUCHES / ST_TOUCHES
如果两个几何图形的边界相接触，但内部不相交，
ST_TOUCHES
操作符会返回
TRUE
。这对检测相邻关系非常有用。
示例
如果您有一张地产地块地图，并希望找到所有与公共公园直接相邻且没有任何重叠的地块。
# The filter expression to find geometries that only touch a line string at their boundaries.
filter
=
"ST_TOUCHES(geo_field, 'LINESTRING(0 0, 1 1)')"
ST_WITHIN / st_within
如果第一个几何图形完全位于第二个几何图形的内部或边界上，则
ST_WITHIN
操作符返回
TRUE
。它是
ST_CONTAINS
的逆运算。
示例
您想查找完全位于一个较大的指定公园区域内的所有小型住宅区。
# The filter expression to find geometries that are completely within a larger polygon.
filter
=
"ST_WITHIN(geo_field, 'POLYGON((110 38, 115 38, 115 42, 110 42, 110 38))')"
有关如何使用
GEOMETRY
字段的更多信息，请参阅
几何字段
。
ST_DWITHIN / ST_D WITHIN
如果几何体 A 与几何体 B 之间的距离小于或等于指定值（以米为单位），
ST_DWITHIN
操作符将返回
TRUE
。目前，几何体 B 必须是一个点。
示例
假设您有一个商店位置 Collections，想要查找距离特定客户位置 5000 米以内的所有商店。
# Find all stores within 5000 meters of the point (120 30)
filter
=
"ST_DWITHIN(geo_field, 'POINT(120 30)', 5000)"