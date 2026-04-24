过滤说明
Milvus 提供强大的过滤功能，可精确查询数据。过滤表达式允许你针对特定的标量字段，用不同的条件细化搜索结果。本指南介绍如何在 Milvus 中使用过滤表达式，并以查询操作符为例。您还可以在搜索和删除请求中应用这些过滤器。
基本操作符
Milvus 支持几种用于过滤数据的基本操作符：
比较操作符
：
==
,
!=
,
>
,
<
,
>=
, 和
<=
允许基于数字或文本字段进行筛选。
范围过滤器
：
IN
和
LIKE
可帮助匹配特定的值范围或集合。
算术操作符
：
+
,
-
,
*
,
/
,
%
, 和
**
用于涉及数字字段的计算。
逻辑操作符
：
AND
,
OR
, 和
NOT
将多个条件组合成复杂的表达式。
IS NULL 和 IS NOT NULL 操作符
：
IS NULL
和
IS NOT NULL
操作符用于根据字段是否包含空值（无数据）来筛选字段。有关详细信息，请参阅
基本操作符
。
示例按颜色筛选
要在标量字段
color
中查找具有三原色（红色、绿色或蓝色）的实体，请使用以下过滤表达式：
filter
=
'color in ["red", "green", "blue"]'
示例：按颜色过滤过滤 JSON 字段
Milvus 允许在 JSON 字段中引用键。例如，如果您有一个带有键
price
和
model
的 JSON 字段
product
，并想查找具有特定模型且价格低于 1,850 的产品，请使用此过滤表达式：
filter
=
'product["model"] == "JSN-087" AND product["price"] < 1850'
示例：过滤数组字段
如果有一个数组字段
history_temperatures
，其中包含自 2000 年以来各观测站报告的平均气温记录，要查找 2009 年（第 10 次记录）气温超过 23°C 的观测站，请使用此表达式：
filter
=
'history_temperatures[10] > 23'
有关这些基本操作符的更多信息，请参阅
基本操作符
。
过滤表达式模板
使用中日韩字符进行筛选时，由于字符集较大且编码不同，处理过程可能会更加复杂。这会导致性能变慢，尤其是使用
IN
操作符时。
Milvus 引入了过滤表达式模板，以优化处理中日韩字符时的性能。通过将动态值从过滤器表达式中分离出来，查询引擎能更有效地处理参数插入。
示例
要查找居住在 "北京"（北京）或 "上海"（上海）的 25 岁以上的个人，请使用以下模板表达式：
filter
=
"age > 25 AND city IN ['北京', '上海']"
为提高性能，可使用这种带参数的变体：
filter
=
"age > {age} AND city in {city}"
,
filter_params = {
"age"
:
25
,
"city"
: [
"北京"
,
"上海"
]}
这种方法可减少解析开销，提高查询速度。更多信息，请参阅
过滤器模板
。
特定数据类型操作符
Milvus 为特定数据类型（如 JSON、ARRAY 和 VARCHAR 字段）提供高级过滤操作符。
特定于 JSON 字段的操作符
Milvus 为查询 JSON 字段提供高级操作符，可在复杂的 JSON 结构中进行精确过滤：
JSON_CONTAINS(identifier, jsonExpr)
:检查字段中是否存在 JSON 表达式。
# JSON data: {"tags": ["electronics", "sale", "new"]}
filter
=
'json_contains(tags, "sale")'
JSON_CONTAINS_ALL(identifier, jsonExpr)
:确保 JSON 表达式的所有元素都存在。
# JSON data: {"tags": ["electronics", "sale", "new", "discount"]}
filter
=
'json_contains_all(tags, ["electronics", "sale", "new"])'
JSON_CONTAINS_ANY(identifier, jsonExpr)
:筛选 JSON 表达式中至少存在一个元素的实体。
# JSON data: {"tags": ["electronics", "sale", "new"]}
filter
=
'json_contains_any(tags, ["electronics", "new", "clearance"])'
有关 JSON 操作符的更多详情，请参阅
JSON 操作符
。
ARRAY 字段特定操作符
Milvus 为数组字段提供了高级过滤操作符，如
ARRAY_CONTAINS
,
ARRAY_CONTAINS_ALL
,
ARRAY_CONTAINS_ANY
, 和
ARRAY_LENGTH
，可对数组数据进行精细控制：
ARRAY_CONTAINS
:过滤包含特定元素的实体。
filter
=
"ARRAY_CONTAINS(history_temperatures, 23)"
ARRAY_CONTAINS_ALL
:过滤包含列表中所有元素的实体。
filter
=
"ARRAY_CONTAINS_ALL(history_temperatures, [23, 24])"
ARRAY_CONTAINS_ANY
:过滤包含列表中任何元素的实体。
filter
=
"ARRAY_CONTAINS_ANY(history_temperatures, [23, 24])"
ARRAY_LENGTH
:根据数组长度进行筛选。
filter
=
"ARRAY_LENGTH(history_temperatures) < 10"
有关数组操作符的更多详情，请参阅
ARRAY Operators
。
VARCHAR 字段专用操作符
Milvus 提供专门的操作符，用于对 VARCHAR 字段进行基于文本的精确搜索：
TEXT_MATCH
操作符
TEXT_MATCH
操作符允许根据特定查询词精确检索文档。它对于结合标量过滤器和向量相似性搜索的过滤搜索特别有用。与语义搜索不同，文本匹配侧重于精确的术语出现。
Milvus 使用 Tantivy 支持倒排索引和基于术语的文本搜索。过程包括
分析器
：标记化和处理输入文本。
索引
：创建将唯一标记映射到文档的倒排索引。
有关详细信息，请参阅
文本匹配
。
PHRASE_MATCH
操作符
Compatible with Milvus 2.6.x
PHRASE_MATCH
操作符可根据精确的短语匹配结果精确检索文档，同时考虑查询词的顺序和相邻关系。
更多详情，请参阅
短语匹配
。