JSON 操作符
Milvus 支持用于查询和过滤 JSON 字段的高级操作符，使其成为管理复杂结构化数据的完美工具。这些操作符可实现对 JSON 文档的高效查询，允许您根据 JSON 字段中的特定元素、值或条件检索实体。本节将指导你在 Milvus 中使用特定于 JSON 的操作符，并提供实际示例来说明它们的功能。
JSON 字段无法处理复杂的嵌套结构，而是将所有嵌套结构视为纯字符串。因此，在使用 JSON 字段时，建议避免过深的嵌套，并确保数据结构尽可能扁平，以获得最佳性能。
可用的 JSON 操作符
Milvus 提供了几个强大的 JSON 操作符，帮助过滤和查询 JSON 数据，这些操作符是
JSON_CONTAINS(identifier, expr)
:过滤在字段中找到指定 JSON 表达式的实体。
JSON_CONTAINS_ALL(identifier, expr)
:确保字段中包含指定 JSON 表达式的所有元素。
JSON_CONTAINS_ANY(identifier, expr)
:筛选字段中至少存在一个 JSON 表达式成员的实体。
让我们通过示例来了解这些操作符在实际场景中的应用。
JSON_CONTAINS
json_contains
操作符检查 JSON 字段中是否存在特定元素或子阵。当你想确保一个 JSON 数组或对象包含一个特定值时，它就非常有用了。
示例
假设您有一个产品 Collections，每个 Collections 都有一个
tags
字段，其中包含一个由字符串组成的 JSON 数组，如
["electronics", "sale", "new"]
。您想过滤带有
"sale"
标记的产品。
# JSON data: {"tags": ["electronics", "sale", "new"]}
filter
=
'json_contains(product["tags"], "sale")'
在此示例中，Milvus 将返回
tags
字段包含
"sale"
元素的所有产品。
json_contains_all
json_contains_all
操作符可确保目标字段中包含指定 JSON 表达式的所有元素。当需要匹配 JSON 数组中的多个值时，该操作符尤其有用。
示例
继续使用产品标记方案，如果要查找具有
"electronics"
、
"sale"
和
"new"
标记的所有产品，可以使用
json_contains_all
操作符。
# JSON data: {"tags": ["electronics", "sale", "new", "discount"]}
filter
=
'json_contains_all(product["tags"], ["electronics", "sale", "new"])'
此查询将返回
tags
数组包含所有三个指定元素的所有产品：
"electronics"
,
"sale"
, 和
"new"
。
json_contains_any
json_contains_any
操作符可过滤字段中至少存在一个 JSON 表达式成员的实体。当您想根据多个可能值中的任意一个值来匹配实体时，该操作符非常有用。
示例
假设您想过滤至少有一个标签
"electronics"
,
"sale"
, 或
"new"
的产品。您可以使用
json_contains_any
操作符来实现这一目的。
# JSON data: {"tags": ["electronics", "sale", "new"]}
filter
=
'json_contains_any(tags, ["electronics", "new", "clearance"])'
在这种情况下，Milvus 将返回列表
["electronics", "new", "clearance"]
中至少有一个标签的所有产品。即使产品只有其中一个标签，也会包含在结果中。