JSON 字段概述
在构建产品目录、内容管理系统或用户偏好引擎等应用程序时，您往往需要在存储向量 Embeddings 的同时存储灵活的元数据。产品属性因类别而异，用户偏好随时间演变，文档属性具有复杂的嵌套结构。Milvus 中的 JSON 字段解决了这一难题，允许您在不牺牲性能的情况下存储和查询灵活的结构化数据。
什么是 JSON 字段？
JSON 字段是 Milvus 中的一种 Schema 定义数据类型 (
DataType.JSON
)，用于存储结构化的键值数据。与传统的刚性数据库列不同，JSON 字段可容纳嵌套对象、数组和混合数据类型，同时提供多种索引选项，以实现快速查询。
JSON 字段结构示例：
{
"metadata"
:
{
"category"
:
"electronics"
,
"brand"
:
"BrandA"
,
"in_stock"
:
true
,
"price"
:
99.99
,
"string_price"
:
"99.99"
,
"tags"
:
[
"clearance"
,
"summer_sale"
]
,
"supplier"
:
{
"name"
:
"SupplierX"
,
"country"
:
"USA"
,
"contact"
:
{
"email"
:
"support@supplierx.com"
,
"phone"
:
"+1-800-555-0199"
}
}
}
}
在这个示例中，
metadata
是一个单一的 JSON 字段，包含平面值（如
category
,
in_stock
）、数组 (
tags
) 和嵌套对象 (
supplier
) 的混合数据。
命名约定：
在 JSON 键中只能使用字母、数字和下划线。避免使用特殊字符、空格或点，因为它们可能会在查询中导致解析问题。
JSON 字段与动态字段
一个常见的混淆点是 JSON 字段与
动态
字段的区别。虽然两者都与 JSON 有关，但目的不同。
下表总结了 JSON 字段和动态字段的主要区别：
特征
JSON 字段
动态字段
Schema 定义
标量字段，必须在 Collections Schema 中以
DataType.JSON
类型明确声明。
一个隐藏的 JSON 字段（名为
$meta
），可自动存储未声明的字段。
使用情况
存储模式已知且一致的结构化数据。
存储不适合固定模式的灵活、不断变化或半结构化数据。
控制
由您控制字段名称和结构。
系统管理未定义的字段。
查询
使用字段名或 JSON 字段内的目标键进行查询：
metadata["key"]
。
直接使用 Dynamic Field 关键字查询：
"dynamic_key"
或通过
$meta
：
$meta["dynamic_key"]
基本操作符
使用 JSON 字段的基本工作流程包括在 Schema 中定义字段、插入数据，然后使用特定的过滤表达式查询数据。
定义 JSON 字段
要使用 JSON 字段，请在创建 Collection 时在模式 Schema 中明确定义该字段。下面的示例演示了如何创建一个带有
metadata
类型字段
DataType.JSON
的 Collections：
from
pymilvus
import
MilvusClient, DataType

client = MilvusClient(uri=
"http://localhost:19530"
)
# Replace with your server address
# Create schema
schema = client.create_schema(auto_id=
False
, enable_dynamic_field=
True
)

schema.add_field(field_name=
"product_id"
, datatype=DataType.INT64, is_primary=
True
)
# Primary field
schema.add_field(field_name=
"vector"
, datatype=DataType.FLOAT_VECTOR, dim=
5
)
# Vector field
# Define a JSON field that allows null values
schema.add_field(field_name=
"metadata"
, datatype=DataType.JSON, nullable=
True
)
client.create_collection(
    collection_name=
"product_catalog"
,
    schema=schema
)
在本例中，集合模式 Schema 中定义的 JSON 字段允许使用
nullable=True
的空值。有关详情，请参阅 "
可为空值和默认值
"。
插入数据
创建 Collections 后，在指定的 JSON 字段中插入包含结构化 JSON 对象的实体。数据格式应为字典列表。
entities = [
    {
"product_id"
:
1
,
"vector"
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
],
"metadata"
: {
# JSON field
"category"
:
"electronics"
,
"brand"
:
"BrandA"
,
"in_stock"
:
True
,
"price"
:
99.99
,
"string_price"
:
"99.99"
,
"tags"
: [
"clearance"
,
"summer_sale"
],
"supplier"
: {
"name"
:
"SupplierX"
,
"country"
:
"USA"
,
"contact"
: {
"email"
:
"support@supplierx.com"
,
"phone"
:
"+1-800-555-0199"
}
}
}
}
]

client.insert(collection_name=
"product_catalog"
, data=entities)
过滤操作符
在对 JSON 字段执行过滤操作前，请确保
您已在每个向量字段上创建了索引。
Collections 已加载到内存中。
显示代码
index_params = client.prepare_index_params()
index_params.add_index(
    field_name=
"vector"
,
    index_type=
"AUTOINDEX"
,
    index_name=
"vector_index"
,
    metric_type=
"COSINE"
)

client.create_index(collection_name=
"product_catalog"
, index_params=index_params)

client.load_collection(collection_name=
"product_catalog"
)
满足这些要求后，您就可以使用下面的表达式，根据 JSON 字段内的值对 Collections 进行过滤。这些过滤表达式利用了特定的 JSON 路径语法和专用操作符。
使用 JSON 路径语法进行筛选
要查询特定键，请使用括号符号访问 JSON 键：
json_field_name["key"]
。对于嵌套键，可将它们串联起来：
json_field_name["key1"]["key2"]
。
要过滤
category
是
"electronics"
的实体：
# Define filter expression
filter
=
'metadata["category"] == "electronics"'
client.search(
    collection_name=
"product_catalog"
,
# Collection name
data=[[
0.1
,
0.2
,
0.3
,
0.4
,
0.5
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
# Filter expression
output_fields=[
"product_id"
,
"metadata"
]
# Fields to include in the search results
)
过滤嵌套键
supplier["country"]
为
"USA"
的实体：
# Define filter expression
filter
=
'metadata["supplier"]["country"] == "USA"'
res = client.search(
    collection_name=
"product_catalog"
,
# Collection name
data=[[
0.1
,
0.2
,
0.3
,
0.4
,
0.5
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
# Filter expression
output_fields=[
"product_id"
,
"metadata"
]
# Fields to include in the search results
)
print
(res)
使用特定于 JSON 的操作符进行过滤
Milvus 还提供特殊操作符，用于查询特定 JSON 字段键上的数组值。例如
json_contains(identifier, expr)
:检查 JSON 数组中是否存在特定元素或子数组
json_contains_all(identifier, expr)
:确保指定 JSON 表达式的所有元素都存在于字段中
json_contains_any(identifier, expr)
:过滤字段中至少存在一个 JSON 表达式成员的实体
查找
tags
关键字下具有
"summer_sale"
值的产品：
# Define filter expression
filter
=
'json_contains(metadata["tags"], "summer_sale")'
res = client.search(
    collection_name=
"product_catalog"
,
# Collection name
data=[[
0.1
,
0.2
,
0.3
,
0.4
,
0.5
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
# Filter expression
output_fields=[
"product_id"
,
"metadata"
]
# Fields to include in the search results
)
print
(res)
查找在
tags
关键字下至少有一个
"electronics"
、
"new"
或
"clearance"
值的产品：
# Define filter expression
filter
=
'json_contains_any(metadata["tags"], ["electronics", "new", "clearance"])'
res = client.search(
    collection_name=
"product_catalog"
,
# Collection name
data=[[
0.1
,
0.2
,
0.3
,
0.4
,
0.5
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
# Filter expression
output_fields=[
"product_id"
,
"metadata"
]
# Fields to include in the search results
)
print
(res)
有关 JSON 特定操作符的更多信息，请参阅
JSON 操作符
。
下一步：加速 JSON 查询
默认情况下，在没有加速的情况下，对 JSON 字段的查询将对所有行执行全扫描，这在大型数据集上可能会比较慢。为了加快 JSON 查询，Milvus 提供了高级索引和存储优化功能。
下表总结了它们的区别和最佳使用场景：
技术
最适合
阵列 加速
注释
JSON 索引
一小部分频繁访问的键，特定数组键上的数组
是（在索引数组键上）
必须预先选择键，如果 Schema 发生变化则需要维护
JSON 粉碎
普遍加快多个键的速度，灵活适用于各种查询
否（不加速数组内的值）
额外的存储配置，数组仍需要按键索引
NGRAM 索引
通配符搜索、文本字段中的子串匹配
不适用
不适用于数字/范围筛选器
提示：
您可以将这些方法结合起来--例如，使用 JSON 切碎来加速广泛查询，使用 JSON 索引来处理高频数组键，使用 NGRAM 索引来进行灵活的文本搜索。
有关实施细节，请参阅
JSON 索引
JSON 切碎
NGRAM
常见问题
JSON 字段的大小有限制吗？
有。每个 JSON 字段的大小限制为 65,536 字节。
JSON 字段是否支持设置默认值？
不支持，JSON 字段不支持默认值。不过，您可以在定义字段时设置
nullable=True
，以允许空条目。
详情请参阅 "
可空和默认
"。
JSON 字段键有任何命名约定吗？
有，以确保与查询和索引的兼容性：
在 JSON 键中只使用字母、数字和下划线。
避免使用特殊字符、空格或点（
.
,
/
等）。
不兼容的键可能会导致过滤表达式出现解析问题。
Milvus 如何处理 JSON 字段中的字符串值？
Milvus 完全按照 JSON 输入中的字符串值进行存储，不进行语义转换。引号不当的字符串可能会在解析过程中导致错误。
有效字符串示例
"a\"b", "a'b", "a\\b"
无效字符串示例
'a"b', 'a\'b'