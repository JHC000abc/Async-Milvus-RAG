基本操作符
Milvus 提供丰富的基本操作符，帮助您高效地过滤和查询数据。这些操作符允许您根据标量字段、数字计算、逻辑条件等来完善搜索条件。了解如何使用这些操作符对于建立精确查询和最大限度地提高搜索效率至关重要。
比较操作符
比较操作符用于根据相等、不等或大小过滤数据。它们适用于数字和文本字段。
支持的比较操作符：
==
等于
!=
(不等于）
>
大于
<
小于
>=
(大于或等于）
<=
(小于或等于）
例 1：使用 "等于 "进行筛选 (
==
)
假设有一个名为
status
的字段，您想查找
status
为 "活动 "的所有实体。您可以使用相等操作符
==
：
filter
=
'status == "active"'
例 2：使用不等于 (
!=
) 过滤
查找
status
不是 "非活动 "的实体：
filter
=
'status != "inactive"'
例 3：使用大于 (
>
) 进行筛选
如果要查找
age
大于 30 的所有实体：
filter
=
'age > 30'
例 4：使用小于进行筛选
要查找
price
小于 100 的实体：
filter
=
'price < 100'
例 5：使用大于或等于 (
>=
) 过滤
如果要查找
rating
大于或等于 4 的所有实体：
filter
=
'rating >= 4'
例 6：使用小于或等于进行筛选
要查找
discount
小于或等于 10% 的实体：
filter
=
'discount <= 10'
范围操作符
范围操作符有助于根据特定的值集或范围过滤数据。
支持的范围操作符：
IN
:用于匹配特定集合或范围内的值。
LIKE
:用于匹配模式（主要用于文本字段）。  Milvus 允许在 VARCHAR 或 JSON 字段上建立
NGRAM
索引，以加速文本查询。有关详细信息，请参阅
NGRAM
。
例 1：使用
IN
匹配多个值
如果要查找
color
为 "红色"、"绿色 "或 "蓝色 "的所有实体：
filter
=
'color in ["red", "green", "blue"]'
当您要检查一个值列表中的成员资格时，这很有用。
例 2：使用
LIKE
进行模式匹配
LIKE
操作符用于字符串字段中的模式匹配。它可以匹配文本中不同位置的子串：
前缀
、
后缀
或
后缀
。
LIKE
操作符使用
%
符号作为通配符，可以匹配任意数量的字符（包括 0）。
在大多数情况下，
下缀
或
后缀
匹配要比前缀匹配慢得多。如果对性能要求很高，请谨慎使用。
前缀匹配（从开始）
要执行
前缀
匹配（字符串以给定模式开始），可以将模式放在开头，然后使用
%
匹配其后的任何字符。例如，要查找
name
以 "Prod "开头的所有产品：
filter
=
'name LIKE "Prod%"'
这将匹配名称以 "Prod "开头的任何产品，如 "Product A"、"Product B "等。
后缀匹配（以 "结束 "结尾）
在
后缀
匹配中，如果字符串以给定的模式结尾，则将
%
符号放在模式的开头。例如，查找
name
以 "XYZ "结尾的所有产品：
filter
=
'name LIKE "%XYZ"'
这将匹配名称以 "XYZ "结尾的任何产品，如 "ProductXYZ"、"SampleXYZ "等。
后缀匹配（包含）
要执行
词缀
匹配，即模式可以出现在字符串的任何位置，可以在模式的开头和结尾处都加上
%
符号。例如，要查找
name
中包含 "Pro "一词的所有产品：
filter
=
'name LIKE "%Pro%"'
这将匹配名称包含子串 "Pro "的任何产品，如 "Product"、"ProLine "或 "SuperPro"。
算术操作符
算术操作符允许您根据涉及数字字段的计算创建条件。
支持的算术操作符：
+
加法
-
减法
*
乘法
/
除法
%
模乘
**
幂
例 1：使用模数 (
%
)
查找
id
是偶数（即能被 2 整除）的实体：
filter
=
'id % 2 == 0'
例 2：使用幂级数 (
**
)
查找
price
升为 2 的幂大于 1000 的实体：
filter
=
'price ** 2 > 1000'
逻辑操作符
逻辑操作符用于将多个条件组合成更复杂的过滤表达式。这些运算符包括
AND
,
OR
, 和
NOT
。
支持的逻辑操作符：
AND
:组合必须全部为真的多个条件。
OR
:组合至少一个必须为真的条件。
NOT
:否定一个条件。
例 1：使用
AND
合并条件
查找
price
大于 100 且
stock
大于 50 的所有产品：
filter
=
'price > 100 AND stock > 50'
例 2：使用
OR
合并条件
查找
color
为 "红色 "或 "蓝色 "的所有产品：
filter
=
'color == "red" OR color == "blue"'
例 3：使用
NOT
排除条件
查找
color
不是 "绿色 "的所有产品：
filter
=
'NOT color == "green"'
IS NULL 和 IS NOT NULL 操作符
IS NULL
和
IS NOT NULL
操作符用于根据字段是否包含空值（无数据）过滤字段。
IS NULL
:识别特定字段包含空值（即值不存在或未定义）的实体。
IS NOT NULL
:识别特定字段包含除空值以外的任何值的实体，即字段具有有效的定义值。
操作符不区分大小写，因此可以使用
IS NULL
或
is null
，以及
IS NOT NULL
或
is not null
。
具有空值的正则标量字段
Milvus 允许过滤带空值的常规标量字段，如字符串或数字。
空字符串
""
不会被视为
VARCHAR
字段的空值。
检索
description
字段为空值的实体：
filter
=
'description IS NULL'
检索
description
字段不是空值的实体：
filter
=
'description IS NOT NULL'
检索
description
字段不是空值且
price
字段大于 10 的实体：
filter
=
'description IS NOT NULL AND price > 10'
具有空值的 JSON 字段
Milvus 允许过滤包含空值的 JSON 字段。在以下情况下，JSON 字段会被视为空值：
整个 JSON 对象被明确设置为 None（空），例如
{"metadata": None}
。
实体中完全没有 JSON 字段。
如果 JSON 对象中的某些元素（如单个键）为空，则字段仍被视为非空。例如，尽管
category
关键字为空，但
\{"metadata": \{"category": None, "price": 99.99}}
不会被视为空字段。
为进一步说明 Milvus 如何处理带有空值的 JSON 字段，请考虑以下带有 JSON 字段
metadata
的示例数据：
data = [
  {
"metadata"
: {
"category"
:
"electronics"
,
"price"
:
99.99
,
"brand"
:
"BrandA"
},
"pk"
:
1
,
"embedding"
: [
0.12
,
0.34
,
0.56
]
  },
  {
"metadata"
:
None
,
# Entire JSON object is null
"pk"
:
2
,
"embedding"
: [
0.56
,
0.78
,
0.90
]
  },
  {
# JSON field `metadata` is completely missing
"pk"
:
3
,
"embedding"
: [
0.91
,
0.18
,
0.23
]
  },
  {
"metadata"
: {
"category"
:
None
,
"price"
:
99.99
,
"brand"
:
"BrandA"
},
# Individual key value is null
"pk"
:
4
,
"embedding"
: [
0.56
,
0.38
,
0.21
]
  }
]
示例 1：检索元数据为空的实体
查找
metadata
字段丢失或明确设置为 "无 "的实体：
filter
=
'metadata IS NULL'
# Example output:
# data: [
#     "{'metadata': None, 'pk': 2}",
#     "{'metadata': None, 'pk': 3}"
# ]
例 2：检索元数据不为空的实体
查找
metadata
字段不是空值的实体：
filter
=
'metadata IS NOT NULL'
# Example output:
# data: [
#     "{'metadata': {'category': 'electronics', 'price': 99.99, 'brand': 'BrandA'}, 'pk': 1}",
#     "{'metadata': {'category': None, 'price': 99.99, 'brand': 'BrandA'}, 'pk': 4}"
# ]
具有空值的 ARRAY 字段
Milvus 允许对包含空值的 ARRAY 字段进行过滤。ARRAY 字段在以下情况下会被视为空值：
整个 ARRAY 字段明确设置为 None（空），例如
"tags": None
。
实体中完全没有 ARRAY 字段。
ARRAY 字段不能包含部分空值，因为 ARRAY 字段中的所有元素必须具有相同的数据类型。有关详细信息，请参阅
数组字段
。
为进一步说明 Milvus 如何处理带有空值的 ARRAY 字段，请考虑以下带有 ARRAY 字段
tags
的示例数据：
data = [
  {
"tags"
: [
"pop"
,
"rock"
,
"classic"
],
"ratings"
: [
5
,
4
,
3
],
"pk"
:
1
,
"embedding"
: [
0.12
,
0.34
,
0.56
]
  },
  {
"tags"
:
None
,
# Entire ARRAY is null
"ratings"
: [
4
,
5
],
"pk"
:
2
,
"embedding"
: [
0.78
,
0.91
,
0.23
]
  },
  {
# The tags field is completely missing
"ratings"
: [
9
,
5
],
"pk"
:
3
,
"embedding"
: [
0.18
,
0.11
,
0.23
]
  }
]
示例 1：检索标签为空的实体
要检索
tags
字段缺失或明确设置为
None
的实体：
filter
=
'tags IS NULL'
# Example output:
# data: [
#     "{'tags': None, 'ratings': [4, 5], 'embedding': [0.78, 0.91, 0.23], 'pk': 2}",
#     "{'tags': None, 'ratings': [9, 5], 'embedding': [0.18, 0.11, 0.23], 'pk': 3}"
# ]
例 2：检索 tags 不为空的实体
检索
tags
字段不为空的实体：
filter
=
'tags IS NOT NULL'
# Example output:
# data: [
#     "{'metadata': {'category': 'electronics', 'price': 99.99, 'brand': 'BrandA'}, 'pk': 1}",
#     "{'metadata': {'category': None, 'price': 99.99, 'brand': 'BrandA'}, 'pk': 4}"
# ]
在 JSON 和 ARRAY 字段中使用基本操作符的提示
虽然 Milvus 的基本操作符用途广泛，可以应用于标量字段，但它们也可以有效地与 JSON 和 ARRAY 字段中的键和索引一起使用。
例如，如果
product
字段包含多个键，如
price
、
model
和
tags
，则始终直接引用键：
filter
=
'product["price"] > 1000'
要查找记录温度的数组中第一个温度超过特定值的记录，请使用：
filter
=
'history_temperatures[0] > 30'
结论
Milvus 提供了一系列基本操作符，让您可以灵活地过滤和查询数据。通过结合比较、范围、算术和逻辑操作符，您可以创建功能强大的过滤表达式，以缩小搜索结果的范围，并高效检索所需的数据。
常见问题
筛选条件中匹配值列表的长度有限制吗（例如，filter='color in ["red", "green", "blue"]' ）？如果列表太长该怎么办？
Zilliz Cloud 不会对筛选条件中的匹配值列表施加长度限制。不过，过长的列表会严重影响查询性能。 如果您的筛选条件包括一个长的匹配值列表或一个包含许多元素的复杂表达式，我们建议您使用
筛选器模板
来提高查询性能。