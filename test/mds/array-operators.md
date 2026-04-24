数组操作符
Milvus 提供功能强大的操作符来查询数组字段，允许你根据数组内容过滤和检索实体。
数组中的所有元素必须是同一类型，数组中的嵌套结构将被视为纯字符串。因此，在使用 ARRAY 字段时，建议避免过深的嵌套，并确保数据结构尽可能扁平，以获得最佳性能。
可用的 ARRAY 操作符
ARRAY 操作符允许在 Milvus 中对数组字段进行精细查询。这些操作符包括
ARRAY_CONTAINS(identifier, expr)
检查数组字段中是否存在特定元素。
ARRAY_CONTAINS_ALL(identifier, expr)
：确保指定列表中的所有元素都存在于数组字段中。
ARRAY_CONTAINS_ANY(identifier, expr)
：检查指定列表中的任何元素是否存在于数组字段中。
ARRAY_LENGTH(identifier)
ARRAY_CONTAINS: 返回数组字段中元素的个数，可与比较操作符结合使用，用于筛选。
ARRAY_CONTAINS
ARRAY_CONTAINS
操作符用于检查数组字段中是否存在特定元素。当您想查找数组中存在给定元素的实体时，它非常有用。
示例
假设有一个数组字段
history_temperatures
，其中包含不同年份的最低气温记录。要查找数组中包含值
23
的所有实体，可以使用以下过滤表达式：
filter
=
'ARRAY_CONTAINS(history_temperatures, 23)'
这将返回
history_temperatures
数组包含
23
值的所有实体。
array_contains_all
ARRAY_CONTAINS_ALL
操作符可确保指定列表中的所有元素都出现在数组字段中。当您要匹配数组中包含多个值的实体时，此操作符非常有用。
示例
如果要查找
history_temperatures
数组同时包含
23
和
24
的所有实体，可以使用 ：
filter
=
'ARRAY_CONTAINS_ALL(history_temperatures, [23, 24])'
这将返回
history_temperatures
数组同时包含指定值的所有实体。
array_contains_any
ARRAY_CONTAINS_ANY
操作符会检查数组字段中是否存在指定列表中的任何元素。当您想匹配数组中至少包含一个指定值的实体时，此操作非常有用。
示例
要查找
history_temperatures
数组包含
23
或
24
的所有实体，可以使用 ：
filter
=
'ARRAY_CONTAINS_ANY(history_temperatures, [23, 24])'
这将返回
history_temperatures
数组至少包含
23
或
24
其中一个值的所有实体。
ARRAY_LENGTH
ARRAY_LENGTH
返回数组字段的长度（元素个数）。它只接受一个参数：数组字段标识符。
示例
查找
history_temperatures
数组中元素少于 10 个的所有实体：
filter
=
'ARRAY_LENGTH(history_temperatures) < 10'
这将返回
history_temperatures
数组中元素少于 10 个的所有实体。