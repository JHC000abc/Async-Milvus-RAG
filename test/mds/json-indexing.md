JSON 索引
JSON 字段为在 Milvus 中存储结构化元数据提供了一种灵活的方式。如果没有索引，对 JSON 字段的查询需要全 Collection 扫描，随着数据集的增长，扫描速度也会变慢。JSON 索引通过在 JSON 数据中创建索引来实现快速查询。
JSON 索引适用于
具有一致、已知键的结构化 Schema
特定 JSON 路径上的等价和范围查询
需要精确控制索引键的情况
对目标查询进行高效存储加速
对于具有不同查询模式的复杂 JSON 文档，可考虑将
JSON 切碎
作为替代方案。
JSON 索引语法
创建 JSON 索引时，需要指定
JSON 路径
：要索引的数据的确切位置
数据类型
：如何解释和存储索引值
可选类型转换
：如果需要，在索引过程中转换数据
下面是索引 JSON 字段的语法：
# Prepare index params
index_params = MilvusClient.prepare_index_params()

index_params.add_index(
    field_name=
"<json_field_name>"
,
# Name of the JSON field
index_type=
"AUTOINDEX"
,
# Must be AUTOINDEX or INVERTED
index_name=
"<unique_index_name>"
,
# Index name
params={
"json_path"
:
"<path_to_json_key>"
,
# Specific key to be indexed within JSON data
"json_cast_type"
:
"<data_type>"
,
# Data type to use when interpreting and indexing the value
# "json_cast_function": "<cast_function>"  # Optional: convert key values into a target type at index time
}
)
参数
说明
值/示例
field_name
Collections Schema 中 JSON 字段的名称。
"metadata"
index_type
对于 JSON 索引，必须是
"AUTOINDEX"
或
"INVERTED"
。
"AUTOINDEX"
index_name
该索引的唯一标识符。
"category_index"
json_path
您希望在 JSON 对象中索引的键的路径。
顶级键：
'metadata["category"]'
嵌套键：
'metadata["supplier"]["contact"]["email"]'
整个 JSON 对象：
"metadata"
子对象：
'metadata["supplier"]'
json_cast_type
解释和索引值时要使用的数据类型。必须与键的实际数据类型相匹配。
有关可用类型的列表，请参阅
下面的
支持的类型
。
"VARCHAR"
json_cast_function
(可选）
在索引时将原始键值转换为目标类型。只有当键值以错误的格式存储，且需要在索引过程中转换数据类型时，才需要使用此配置。
有关可用的转换函数列表，请参阅
下面的支持的转换函数
。
"STRING_TO_DOUBLE"
支持的数据类型
Milvus 支持以下数据类型在索引时进行转换。这些类型可确保正确解释数据，从而实现高效过滤。
数据类型
描述
示例 JSON 值
BOOL
/
bool
用于索引布尔值，以便根据真/假条件进行查询。
true
,
false
DOUBLE
/
double
用于数值，包括整数和浮点数。它可以根据范围或相等条件进行筛选（如
>
,
<
,
==
）。
42
,
99.99
VARCHAR
/
varchar
用于索引字符串值，常见于基于文本的数据，如名称、类别或 ID。
"electronics"
,
"BrandA"
ARRAY_BOOL
/
array_bool
用于索引布尔值数组。
[true, false, true]
ARRAY_DOUBLE
/
array_double
用于索引数值数组。
[1.2, 3.14, 42]
ARRAY_VARCHAR
/
array_varchar
用于索引字符串数组，是标签或关键字列表的理想选择。
["tag1", "tag2", "tag3"]
JSON
/
json
整个 JSON 对象或子对象，具有自动类型推断和扁平化功能。
索引整个 JSON 对象会增加索引大小。对于多键情况，可考虑使用
JSON Shredding
。
任何 JSON 对象
数组应包含相同类型的元素，以优化索引。有关详细信息，请参阅
数组字段
。
支持的铸入函数
如果您的 JSON 字段键包含格式不正确的值（例如，以字符串形式存储的数字），您可以向
json_cast_function
参数传递铸型函数，以便在索引时转换这些值。
转换函数不区分大小写。支持以下函数：
转换函数
转换自 → 转换为
使用案例
STRING_TO_DOUBLE
/
string_to_double
字符串 → 数值（双）
将
"99.99"
转换为
99.99
如果转换失败（如非数字字符串），该值将被跳过，不会被索引。
创建 JSON 索引
本节通过实际示例演示如何在不同类型的 JSON 数据上创建索引。所有示例都使用了下图所示的 JSON 结构示例，并假设您已经建立了与
MilvusClient
的连接，并正确定义了 Collections
Schema
。
JSON 结构示例
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
基本设置
在创建任何 JSON 索引之前，请准备好索引参数：
# Prepare index params
index_params = MilvusClient.prepare_index_params()
例 1：索引一个简单的 JSON 键
在
category
字段上创建索引，以便按产品类别快速筛选：
index_params.add_index(
    field_name=
"metadata"
,
index_type=
"AUTOINDEX"
,
# Must be set to AUTOINDEX or INVERTED for JSON path indexing
index_name=
"category_index"
,
# Unique index name
params={
"json_path"
:
'metadata["category"]'
,
# Path to the JSON key
"json_cast_type"
:
"varchar"
# Data cast type
}
)
例 2：索引嵌套键
在深度嵌套的
email
字段上创建索引，用于搜索供应商联系人：
# Index the nested key
index_params.add_index(
    field_name=
"metadata"
,
index_type=
"AUTOINDEX"
,
# Must be set to AUTOINDEX or INVERTED for JSON path indexing
index_name=
"email_index"
,
# Unique index name
params={
"json_path"
:
'metadata["supplier"]["contact"]["email"]'
,
# Path to the nested JSON key
"json_cast_type"
:
"varchar"
# Data cast type
}
)
例 3：索引时转换数据类型
有时，数字数据会被错误地存储为字符串。使用
STRING_TO_DOUBLE
转换功能进行正确转换和索引：
# Convert string numbers to double for indexing
index_params.add_index(
    field_name=
"metadata"
,
index_type=
"AUTOINDEX"
,
# Must be set to AUTOINDEX or INVERTED for JSON path indexing
index_name=
"string_to_double_index"
,
# Unique index name
params={
"json_path"
:
'metadata["string_price"]'
,
# Path to the JSON key to be indexed
"json_cast_type"
:
"double"
,
# Data cast type
"json_cast_function"
:
"STRING_TO_DOUBLE"
# Cast function; case insensitive
}
)
重要
： 如果任何文档的转换失败（例如，非数字字符串，如
"invalid"
），该文档的值将被排除在索引之外，不会出现在筛选结果中。
示例 4：索引整个对象
索引整个 JSON 对象，以便对其中的任何字段进行查询。使用
json_cast_type="JSON"
时，系统会自动
使 JSON 结构扁平化
：将嵌套对象转换为扁平路径，以实现高效索引
推断数据类型
：根据每个值的内容自动将其归类为数值、字符串、布尔值或日期值
创建全面的覆盖范围
：对象中的所有键和嵌套路径均可搜索
对于上述
示例 JSON 结构
，可对整个
metadata
对象进行索引：
# Index the entire JSON object
index_params.add_index(
    field_name=
"metadata"
,
    index_type=
"AUTOINDEX"
,
    index_name=
"metadata_full_index"
,
    params={
"json_path"
:
"metadata"
,
"json_cast_type"
:
"JSON"
}
)
您也可以只索引 JSON 结构的一部分，例如所有
supplier
信息：
# Index a sub-object
index_params.add_index(
    field_name=
"metadata"
,
    index_type=
"AUTOINDEX"
, 
    index_name=
"supplier_index"
,
    params={
"json_path"
:
'metadata["supplier"]'
,
"json_cast_type"
:
"JSON"
}
)
应用索引配置
定义好所有索引参数后，将其应用到 Collections 中：
# Apply all index configurations to the collection
MilvusClient.create_index(
    collection_name=
"your_collection_name"
,
    index_params=index_params
)
索引完成后，您的 JSON 字段查询将自动使用这些索引，以提高性能。
常见问题
如果查询的过滤表达式使用的类型与索引的铸型类型不同，会发生什么情况？
如果你的过滤表达式使用的类型与索引的
json_cast_type
不同，Milvus 将不会使用索引，如果数据允许，可能会退回到较慢的暴力扫描。为获得最佳性能，请始终将过滤表达式与索引的铸型类型保持一致。例如，如果使用
json_cast_type="double"
创建了数字索引，则只有数字过滤条件会利用该索引。
创建 JSON 索引时，如果不同实体的 JSON 键的数据类型不一致怎么办？
不一致的类型会导致
部分索引
。例如，如果
metadata["price"]
字段同时以数字（
99.99
）和字符串（
"99.99"
）的形式存储，并且您使用
json_cast_type="double"
创建了索引，那么只有数字值会被索引。字符串形式的条目将被跳过，不会出现在过滤结果中。
能否在同一个 JSON 关键字上创建多个索引？
不能，每个 JSON 关键字只支持一个索引。您必须选择一个与您的数据相匹配的
json_cast_type
。不过，您可以为整个 JSON 对象创建索引，也可以为该对象中的嵌套键创建索引。
JSON 字段是否支持设置默认值？
不，JSON 字段不支持默认值。不过，您可以在定义字段时设置
nullable=True
，以允许空条目。有关详细信息，请参阅 "
可为空和默认值
"。