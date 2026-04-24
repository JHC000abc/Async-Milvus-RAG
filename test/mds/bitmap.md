位图
位图索引是一种高效的索引技术，旨在提高低 Cardinal 标量字段的查询性能。Cardinal 指的是字段中不同值的数量。具有较少不同元素的字段被视为低 Cardinal。
这种索引类型以紧凑的二进制格式表示字段值，并对其执行高效的位操作符，有助于缩短标量查询的检索时间。与其他类型的索引相比，位图索引在处理低奇数字段时通常具有更高的空间效率和更快的查询速度。
概述
位图
一词由两个词组合而成：
位
（
Bit
）和映射（
Map
）。比特是计算机中最小的数据单位，只能保存
0
或
1 的
值。在这里，映射指的是根据 0 和 1 的赋值对数据进行转换和组织的过程。
位图索引由两个主要部分组成：位图和键。键代表索引字段中的唯一值。每个唯一值都有一个对应的位图。这些位图的长度等于 Collections 中的记录数。位图中的每个位对应集合中的一条记录。如果记录中索引字段的值与键相匹配，相应的位就会被设置为
1
，否则就会被设置为
0
。
考虑一个带有 "
类别
"和 "
公共
"字段的文档 Collections。我们想检索属于
Tech
类别并对
公众
开放的文档。在这种情况下，位图索引的键就是
Tech
和
Public
。
位图
如图所示，"
类别
"和
"公开
"
的位图索引是
Tech
：[1，0，1，0，0]，这表明只有第 1 和第 3 个文档属于
Tech
类别。
公共
：[1，0，0，1，0]，表明只有第 1 和第 4 个文档对
公众
开放。
为了找到符合这两个标准的文档，我们对这两个位图进行位和操作：
Tech
AND
Public
：[1, 0, 0, 0, 0]
得到的位图 [1, 0, 0, 0, 0] 表明只有第一个文档
（ID
1
）同时满足这两个条件。通过使用位图索引和高效的位操作符，我们可以快速缩小搜索范围，无需扫描整个数据集。
创建位图索引
要在 Milvus 中创建位图索引，请使用
create_index()
方法，并将
index_type
参数设置为
"BITMAP"
。
from
pymilvus
import
MilvusClient

client = MilvusClient(
    uri=
"http://localhost:19530"
,
)

index_params = client.create_index_params()
# Prepare an empty IndexParams object, without having to specify any index parameters
index_params.add_index(
    field_name=
"category"
,
# Name of the scalar field to be indexed
index_type=
"BITMAP"
,
# Type of index to be created
index_name=
"category_bitmap_index"
# Name of the index to be created
)

client.create_index(
    collection_name=
"my_collection"
,
# Specify the collection name
index_params=index_params
)
在本例中，我们在
my_collection
Collections 的
category
字段上创建位图索引。
add_index()
方法用于指定字段名称、索引类型和索引名称。
位图索引创建后，您可以在查询操作中使用
filter
参数，根据索引字段执行标量过滤。这样就可以使用位图索引有效地缩小搜索结果的范围。有关详细信息，请参阅
过滤说明
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
或更高版本开始，一旦不再需要标量索引，就可以直接删除，而无需先释放 Collections。
client.drop_index(
    collection_name=
"my_collection"
,
# Name of the collection
index_name=
"category_bitmap_index"
# Name of the index to drop
)
限制
位图索引仅支持非主键的标量字段。
字段的数据类型必须是以下类型之一：
BOOL
,
INT8
,
INT16
,
INT32
,
INT64
、
VARCHAR
ARRAY
(元素必须是以下之一：
BOOL
,
INT8
,
INT16
,
INT32
,
INT64
,
VARCHAR
)
位图索引不支持以下数据类型：
FLOAT
,
DOUBLE
: 浮点类型与位图索引的二进制性质不兼容。
JSON
:JSON 数据类型结构复杂，无法使用位图索引有效表示。
位图索引不适用于高 Cardinality 字段（即具有大量不同值的字段）。
一般来说，当字段的 Cardinality 小于 500 时，位图索引最为有效。
当 Cardinality 超过这个临界值时，位图索引的性能优势就会减弱，存储开销也会变得很大。
对于高 Cardinality 字段，可根据具体使用情况和查询要求，考虑使用其他索引技术，如倒排索引。