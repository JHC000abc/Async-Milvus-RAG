TIMESTAMPTZ 领域
Compatible with Milvus 2.6.6+
跨地区跟踪时间的应用程序（如电子商务系统、协作工具或分布式日志记录）需要精确处理带有时区的时间戳。Milvus 的
TIMESTAMPTZ
数据类型通过存储带有相关时区的时间戳提供了这种功能。
什么是 TIMESTAMPTZ 字段？
TIMESTAMPTZ
字段是 Milvus 中一种 Schema 定义的数据类型 (
DataType.TIMESTAMPTZ
)，可处理时区感知输入，并在内部将所有时间点存储为 UTC 绝对时间：
接受的输入格式
：带有时区偏移的
ISO 8601
字符串（例如，
"2025-05-01T23:59:59+08:00"
表示 2025 年 5 月 1 日晚上 11:59:59（UTC+08:00））。
内部存储
：所有
TIMESTAMPTZ
值均以
协调世界时
(UTC) 标准化和存储。
比较和筛选
：所有过滤和排序操作均以 UTC 进行，确保不同时区的结果一致且可预测。
您可以为
TIMESTAMPTZ
字段设置
nullable=True
，以允许缺失值。
您可以使用
ISO 8601
格式的
default_value
属性指定默认时间戳值。
有关详情，请参阅 "
可空值和默认值
"。
基本操作符
使用
TIMESTAMPTZ
字段的基本工作流程与 Milvus 中的其他标量字段如出一辙：定义字段 → 插入数据 → 查询/过滤。
步骤 1：定义 TIMESTAMPTZ 字段
要使用
TIMESTAMPTZ
字段，请在创建 Collections 时在 Collections Schema 中明确定义该字段。下面的示例演示了如何创建一个带有
tsz
类型字段
DataType.TIMESTAMPTZ
的 Collection。
Python
Java
NodeJS
Go
cURL
import
time
from
pymilvus
import
MilvusClient, DataType
import
datetime
import
pytz

server_address =
"http://localhost:19530"
collection_name =
"timestamptz_test123"
client = MilvusClient(uri=server_address)
if
client.has_collection(collection_name):
    client.drop_collection(collection_name)

schema = client.create_schema()
# Add a primary key field
schema.add_field(
"id"
, DataType.INT64, is_primary=
True
)
# Add a TIMESTAMPTZ field that allows null values
schema.add_field(
"tsz"
, DataType.TIMESTAMPTZ, nullable=
True
)
# Add a vector field
schema.add_field(
"vec"
, DataType.FLOAT_VECTOR, dim=
4
)

client.create_collection(collection_name, schema=schema, consistency_level=
"Session"
)
print
(
f"Collection '
{collection_name}
' with a TimestampTz field created successfully."
)
// java
// nodejs
// go
# restful
第 2 步：插入数据
插入包含时区偏移的 ISO 8601 字符串的实体。
下面的示例向 Collection 中插入了 8,193 行样本数据。每一行包括
一个唯一 ID
时区感知时间戳（上海时间）
一个简单的 4 维向量
Python
Java
NodeJS
Go
cURL
data_size =
8193
# Get the Asia/Shanghai time zone using the pytz library
# You can use any valid IANA time zone identifier such as:
#   "Asia/Tokyo", "America/New_York", "Europe/London", "UTC", etc.
# To view all available values:
#   import pytz; print(pytz.all_timezones)
# Reference:
#   IANA database – https://www.iana.org/time-zones
#   Wikipedia – https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
shanghai_tz = pytz.timezone(
"Asia/Shanghai"
)

data = [
    {
"id"
: i +
1
,
"tsz"
: shanghai_tz.localize(
            datetime.datetime(
2025
,
1
,
1
,
0
,
0
,
0
) + datetime.timedelta(days=i)
        ).isoformat(),
"vec"
: [
float
(i) /
10
for
i
in
range
(
4
)],
    }
for
i
in
range
(data_size)
]

client.insert(collection_name, data)
print
(
"Data inserted successfully."
)
// java
// nodejs
// go
# restful
步骤 3：过滤操作符
TIMESTAMPTZ
在对  字段执行过滤操作之前，您必须确保该字段是唯一的，并支持标量比较、区间运算和时间成分提取。
在对
TIMESTAMPTZ
字段执行过滤操作之前，请确保
已为每个向量字段创建索引。
已将 Collections 载入内存。
显示示例代码
Python
Java
NodeJS
Go
cURL
# Create index on vector field
index_params = client.prepare_index_params()
index_params.add_index(
    field_name=
"vec"
,
    index_type=
"AUTOINDEX"
,
    index_name=
"vec_index"
,
    metric_type=
"COSINE"
)
client.create_index(collection_name, index_params)
print
(
"Index created successfully."
)
# Load the collection
client.load_collection(collection_name)
print
(
f"Collection '
{collection_name}
' loaded successfully."
)
// java
// nodejs
// go
# restful
使用时间戳过滤进行查询
使用算术操作符，如
==
,
!=
,
<
,
>
,
<=
,
>=
。有关 Milvus 可用算术操作符的完整列表，请参阅
算术操作符
。
下面的示例过滤了时间戳 (
tsz
) 不等于
2025-01-03T00:00:00+08:00
的实体：
Python
Java
NodeJS
Go
cURL
# Query for entities where tsz is not equal to '2025-01-03T00:00:00+08:00'
expr =
"tsz != ISO '2025-01-03T00:00:00+08:00'"
results = client.query(
    collection_name=collection_name,
filter
=expr,
    output_fields=[
"id"
,
"tsz"
],
    limit=
10
)
print
(
"Query result: "
, results)
# Expected output:
# Query result:  data: ["{'id': 1, 'tsz': '2024-12-31T16:00:00Z'}", "{'id': 2, 'tsz': '2025-01-01T16:00:00Z'}", "{'id': 4, 'tsz': '2025-01-03T16:00:00Z'}", "{'id': 5, 'tsz': '2025-01-04T16:00:00Z'}", "{'id': 6, 'tsz': '2025-01-05T16:00:00Z'}", "{'id': 7, 'tsz': '2025-01-06T16:00:00Z'}", "{'id': 8, 'tsz': '2025-01-07T16:00:00Z'}", "{'id': 9, 'tsz': '2025-01-08T16:00:00Z'}", "{'id': 10, 'tsz': '2025-01-09T16:00:00Z'}", "{'id': 11, 'tsz': '2025-01-10T16:00:00Z'}"]
// java
// nodejs
// go
# restful
在上面的示例中
tsz
是 Schema 中定义的
TIMESTAMPTZ
字段名。
ISO '2025-01-03T00:00:00+08:00'
是
ISO 8601
格式的时间戳文字，包括时区偏移。
!=
将字段值与字面值进行比较。其他支持的操作符包括
==
,
<
,
<=
,
>
和
>=
。
间隔操作符
您可以使用
ISO 8601 时长格式
中的
INTERVAL
值对
TIMESTAMPTZ
字段进行运算。这样，在筛选数据时，就可以从时间戳中添加或减去持续时间，如天、小时或分钟。
例如，下面的查询可过滤时间戳 (
tsz
) 加上零天
不等于
2025-01-03T00:00:00+08:00
的实体：
Python
Java
NodeJS
Go
cURL
expr =
"tsz + INTERVAL 'P0D' != ISO '2025-01-03T00:00:00+08:00'"
results = client.query(
    collection_name,
filter
=expr, 
    output_fields=[
"id"
,
"tsz"
], 
    limit=
10
)
print
(
"Query result: "
, results)
# Expected output:
# Query result:  data: ["{'id': 1, 'tsz': '2024-12-31T16:00:00Z'}", "{'id': 2, 'tsz': '2025-01-01T16:00:00Z'}", "{'id': 4, 'tsz': '2025-01-03T16:00:00Z'}", "{'id': 5, 'tsz': '2025-01-04T16:00:00Z'}", "{'id': 6, 'tsz': '2025-01-05T16:00:00Z'}", "{'id': 7, 'tsz': '2025-01-06T16:00:00Z'}", "{'id': 8, 'tsz': '2025-01-07T16:00:00Z'}", "{'id': 9, 'tsz': '2025-01-08T16:00:00Z'}", "{'id': 10, 'tsz': '2025-01-09T16:00:00Z'}", "{'id': 11, 'tsz': '2025-01-10T16:00:00Z'}"]
// java
// nodejs
// go
# restful
INTERVAL
值遵循
ISO 8601 时长语法
。例如
P1D
→ 1 天
PT3H
→ 3 小时
P2DT6H
→ 2 天 6 小时
您可以在筛选表达式中直接使用
INTERVAL
算法，例如
tsz + INTERVAL 'P3D'
→ 增加 3 天
tsz - INTERVAL 'PT2H'
→ 减去 2 小时
使用时间戳过滤进行搜索
您可以将
TIMESTAMPTZ
过滤与向量相似性搜索结合起来，通过时间和相似性来缩小搜索结果的范围。
Python
Java
NodeJS
Go
cURL
# Define a time-based filter expression
filter
=
"tsz > ISO '2025-01-05T00:00:00+08:00'"
res = client.search(
    collection_name=collection_name,
# Collection name
data=[[
0.1
,
0.2
,
0.3
,
0.4
]],
# Query vector (must match collection's vector dim)
limit=
5
,
# Max. number of results to return
filter
=
filter
,
# Filter expression using TIMESTAMPTZ
output_fields=[
"id"
,
"tsz"
],
# Fields to include in the search results
)
print
(
"Search result: "
, res)
# Expected output:
# Search result:  data: [[{'id': 10, 'distance': 0.9759000539779663, 'entity': {'tsz': '2025-01-09T16:00:00Z', 'id': 10}}, {'id': 9, 'distance': 0.9759000539779663, 'entity': {'tsz': '2025-01-08T16:00:00Z', 'id': 9}}, {'id': 8, 'distance': 0.9759000539779663, 'entity': {'tsz': '2025-01-07T16:00:00Z', 'id': 8}}, {'id': 7, 'distance': 0.9759000539779663, 'entity': {'tsz': '2025-01-06T16:00:00Z', 'id': 7}}, {'id': 6, 'distance': 0.9759000539779663, 'entity': {'tsz': '2025-01-05T16:00:00Z', 'id': 6}}]]
// java
// nodejs
// go
# restful
如果您的 Collections 有两个或更多向量字段，您可以使用时间戳过滤执行混合搜索操作符。有关详情，请参阅
多向量混合搜索
。
高级用法
对于高级用法，您可以在不同级别（如数据库、Collection 或查询）管理时区，或使用索引加速对
TIMESTAMPTZ
字段的查询。
管理不同级别的时区
您可以在
数据库
、
Collection
或
查询/搜索
级别控制
TIMESTAMPTZ
字段的时区。
级别
参数
范围
优先级
数据库
timezone
数据库中所有 Collections 的默认值
最低
Collections
timezone
覆盖该 Collection 的数据库默认时区设置
中
查询/搜索/混合搜索
timezone
临时覆盖一个特定操作符
最高
有关分步说明和代码示例，请参阅专用页面：
修改 Collections
数据库
查询
基本向量搜索
多向量混合搜索
加速查询
在没有索引的情况下，对
TIMESTAMPTZ
字段的查询默认会对所有行执行全扫描，这在大型数据集中可能会比较慢。要加速时间戳查询，请在
TIMESTAMPTZ
字段上创建
STL_SORT
索引。
有关详情，请参阅
STL_SORT
。