STL_SORT
STL_SORT
索引是一种专门设计用于提高数值字段（INT8、INT16 等）、
VARCHAR
字段或
TIMESTAMPTZ
字段查询性能的索引类型，其方法是按排序顺序组织数据。
如果您经常运行以下查询，请使用
STL_SORT
索引：
使用
==
,
!=
,
>
,
<
,
>=
和
<=
操作符进行比较筛选
使用
IN
和
LIKE
操作符进行范围过滤
支持的数据类型
数字字段（如
INT8
,
INT16
,
INT32
,
INT64
,
FLOAT
,
DOUBLE
）。有关详情，请参阅
布尔和数值
。
VARCHAR
字段。有关详细信息，请参阅
字符串字段
。
TIMESTAMPTZ
字段。有关详情，请参阅
TIMESTAMPTZ 字段
。
工作原理
Milvus 分两个阶段实现
STL_SORT
：
建立索引
在采集过程中，Milvus 会收集索引字段的所有值。
这些值使用 C++ STL 的
std::sort
按升序排序。
每个值与其实体 ID 配对，排序后的数组作为索引持久化。
加速查询
在查询时，Milvus 对排序数组使用
二进制搜索
（std::lower_bound
和
std::upper
_
bound
）。
对于相等值，Milvus 能快速找到所有匹配值。
对于范围，Milvus 会定位开始和结束位置，并返回两者之间的所有值。
匹配的实体 ID 会被传递给查询执行器，以便组装最终结果。
这将查询复杂度从
O(n)
（全扫描）降低到
O(log n + m)
，其中
m
是匹配数。
创建 STL_SORT 索引
您可以在数字或
TIMESTAMPTZ
字段上创建
STL_SORT
索引。无需额外参数。
下面的示例显示了如何在
TIMESTAMPTZ
字段上创建
STL_SORT
索引：
from
pymilvus
import
MilvusClient

client = MilvusClient(uri=
"http://localhost:19530"
)
# Replace with your server address
# Assume you have defined a TIMESTAMPTZ field named "tsz" in your collection schema
# Prepare index parameters
index_params = client.prepare_index_params()
# Add RTREE index on the "tsz" field
index_params.add_index(
field_name=
"tsz"
,
index_type=
"STL_SORT"
,
# Index for TIMESTAMPTZ
index_name=
"tsz_index"
,
# Optional, name your index
params={}
# No extra params needed
)
# Create the index on the collection
client.create_index(
    collection_name=
"tsz_demo"
,
    index_params=index_params
)
删除索引
使用
drop_index()
方法从 Collections 中删除现有索引。
client.drop_index(
    collection_name=
"tsz_demo"
,
# Name of the collection
index_name=
"tsz_index"
# Name of the index to drop
)
使用说明
字段类型：
适用于数字和
TIMESTAMPTZ
字段。有关数据类型的更多信息，请参阅
布尔与数字
以及
TIMESTAMPTZ 字段
。
参数：
不需要索引参数。
不支持内存映射：
STL_SORT
不支持内存映射模式。