NGRAM
Milvus 中的
NGRAM
索引是为了加速对
VARCHAR
字段或
JSON
字段内特定 JSON 路径的
LIKE
查询而建立的。在建立索引之前，Milvus 会将文本分割成固定长度为
n
的重叠短子串，称为
n-gram
。例如，
n = 3
时，单词
"Milvus "
会被拆分成 3 个词组：
"Mil"、
"ilv"、"
lvu "
和
"vus"。
然后，这些 n 个词组被存储在一个倒排索引中，该索引将每个词组映射到出现该词组的文档 ID。在查询时，该索引允许 Milvus 将搜索范围迅速缩小到一小部分候选词，从而大大加快了查询执行速度。
当你需要快速过滤前缀、后缀、前后缀或通配符时，请使用它：
name LIKE "data%"
title LIKE "%vector%"
path LIKE "%json"
有关过滤表达式语法的详细信息，请参阅
基本操作符
。
工作原理
Milvus 分两个阶段实现
NGRAM
索引：
建立索引
：为每个文档生成 n-grams，并在摄取过程中建立倒排索引。
加速查询
：使用索引筛选出一个小的候选集，然后验证精确匹配。
第 1 阶段：建立索引
在数据摄取过程中，Milvus 通过两个主要步骤建立 NGRAM 索引：
将文本分解为 n 个词组
：Milvus 在目标字段中的每个字符串上滑动一个
n
的窗口，提取重叠的子串或
n-gram
。这些子串的长度在一个可配置的范围内，
[min_gram, max_gram]
.
min_gram
:要生成的最短 n-gram。这也定义了可从索引中获益的最小查询子串长度。
max_gram
:要生成的最长 n-gram。在查询时，它也被用作分割长查询字符串时的最大窗口大小。
例如，在
min_gram=2
和
max_gram=3
的情况下，字符串
"AI database"
的拆分情况如下：
建立 Ngram 索引
- **2-grams:** `AI`, `I_`, `_d`, `da`, `at`, ...

- **3-grams:** `AI_`, `I_d`, `_da`, `dat`, `ata`, ...

<div class="alert note">

- For a range `[min_gram, max_gram]`, Milvus generates all n-grams for every length between the two values (inclusive). For example, with `[2,4]` and the word `"text"`, Milvus generates:

- **2-grams:** `te`, `ex`, `xt`

- **3-grams:** `tex`, `ext`

- **4-grams:** `text`

- N-gram decomposition is character-based and language-agnostic. For example, in Chinese, `"向量数据库"` with `min_gram = 2` is decomposed into: `"向量"`, `"量数"`, `"数据"`, `"据库"`.

- Spaces and punctuation are treated as characters during decomposition.

- Decomposition preserves original case, and matching is case-sensitive. For example, `"Database"` and `"database"` will generate different n-grams and require exact case matching during queries.

</div>
建立倒排索引
：创建一个
倒排索引
，将每个生成的 n-gram 映射到包含该 n-gram 的文档 ID 列表。
例如，如果 2-gram
"AI"
出现在 ID 为 1、5、6、8 和 9 的文档中，索引就会记录
{"AI": [1, 5, 6, 8, 9]}
。查询时可使用该索引快速缩小搜索范围。
构建 Ngram 索引 2
<div class="alert note">

A wider `[min_gram, max_gram]` range creates more grams and larger mapping lists. If memory is tight, consider mmap mode for very large posting lists. For details, refer to [Use mmap](https://zilliverse.feishu.cn/wiki/P3wrwSMNNihy8Vkf9p6cTsWYnTb).

</div>
第 2 阶段：加速查询
当执行
LIKE
过滤器时，Milvus 使用 NGRAM 索引加速查询，具体步骤如下：
加速查询
提取查询词：
从
LIKE
表达式中提取不含通配符的连续子串（例如，
"%database%"
变成
"database"
）。
分解查询词：
根据查询词的长度 (
L
) 以及
min_gram
和
max_gram
的设置，将查询词分解为
n 个词组
。
如果
L < min_gram
，则无法使用索引，查询将退回到全扫描。
如果设置为
min_gram ≤ L ≤ max_gram
，则整个查询词被视为一个 n-gram，无需进一步分解。
如果是
L > max_gram
，查询词将被分解为多个重叠克，窗口大小等于
max_gram
。
例如，如果
max_gram
设置为
3
，查询词为
"database"
，长度为
8
，则会被分解为
"dat"
,
"ata"
,
"tab"
等 3 个克的子串。
查找每个语法并进行交集
：Milvus 在倒排索引中查找每个查询语法，然后与得到的文档 ID 列表进行交集，找出一小组候选文档。这些候选文档包含查询的所有语法。
验证并返回结果：
然后将原始的
LIKE
过滤器作为最后检查只应用于小的候选集，以找到完全匹配的结果。
创建 NGRAM 索引
可以在
VARCHAR
字段或
JSON
字段内的特定路径上创建 NGRAM 索引。
例 1：在 VARCHAR 字段上创建
对于
VARCHAR
字段，只需指定
field_name
并配置
min_gram
和
max_gram
即可。
from
pymilvus
import
MilvusClient

client = MilvusClient(uri=
"http://localhost:19530"
)
# Replace with your server address
# Assume you have defined a VARCHAR field named "text" in your collection schema
# Prepare index parameters
index_params = client.prepare_index_params()
# Add NGRAM index on the "text" field
index_params.add_index(
field_name=
"text"
,
# Target VARCHAR field
index_type=
"NGRAM"
,
# Index type is NGRAM
index_name=
"ngram_index"
,
# Custom name for the index
min_gram=
2
,
# Minimum substring length (e.g., 2-gram: "st")
max_gram=
3
# Maximum substring length (e.g., 3-gram: "sta")
)
# Create the index on the collection
client.create_index(
    collection_name=
"Documents"
,
    index_params=index_params
)
此配置会为
text
中的每个字符串生成 2-gram 和 3-gram，并将其存储在反转索引中。
例 2：在 JSON 路径上创建
对于
JSON
字段，除了克设置外，还必须指定
params.json_path
- 指向要索引的值的 JSON 路径。
params.json_cast_type
- 必须是
"varchar"
（不区分大小写），因为 NGRAM 索引操作符是字符串。
# Assume you have defined a JSON field named "json_field" in your collection schema, with a JSON path named "body"
# Prepare index parameters
index_params = client.prepare_index_params()
# Add NGRAM index on a JSON field
index_params.add_index(
field_name=
"json_field"
,
# Target JSON field
index_type=
"NGRAM"
,
# Index type is NGRAM
index_name=
"json_ngram_index"
,
# Custom index name
min_gram=
2
,
# Minimum n-gram length
max_gram=
4
,
# Maximum n-gram length
params={
"json_path"
:
"json_field[\"body\"]"
,
# Path to the value inside the JSON field
"json_cast_type"
:
"varchar"
# Required: cast the value to varchar
}
)
# Create the index on the collection
client.create_index(
    collection_name=
"Documents"
,
    index_params=index_params
)
在此示例中
只索引
json_field["body"]
中的值。
在进行 N-gram 标记化之前，该值会被转换为
VARCHAR
。
Milvus 会生成长度为 2 到 4 的子串，并将它们存储在反转索引中。
有关如何索引 JSON 字段的更多信息，请参阅
JSON 索引
。
通过 NGRAM 加速查询
要应用 NGRAM 索引：
查询必须以具有
NGRAM
索引的
VARCHAR
字段（或 JSON 路径）为目标。
LIKE
模式的字面部分长度必须至少为
min_gram
个字符
（例如，如果最短的预期查询项为 2 个字符，则在创建索引时设置 min_gram=2）。
支持的查询类型：
前缀匹配
# Match any string that starts with the substring "database"
filter
=
'text LIKE "database%"'
后缀匹配
# Match any string that ends with the substring "database"
filter
=
'text LIKE "%database"'
后缀匹配
# Match any string that contains the substring "database" anywhere
filter
=
'text LIKE "%database%"'
通配符匹配
Milvus 支持
%
（0 个或多个字符）和
_
（正好一个字符）。
# Match any string where "st" appears first, and "um" appears later in the text
filter
=
'text LIKE "%st%um%"'
JSON 路径查询
filter
=
'json_field["body"] LIKE "%database%"'
有关过滤表达式语法的更多信息，请参阅
基本操作符
。
删除索引
使用
drop_index()
方法从 Collections 中删除现有索引。
client.drop_index(
    collection_name=
"Documents"
,
# Name of the collection
index_name=
"ngram_index"
# Name of the index to drop
)
使用注意事项
字段类型
：支持
VARCHAR
和
JSON
字段。对于 JSON，请同时提供
params.json_path
和
params.json_cast_type="varchar"
。
Unicode
：NGRAM 分解以字符为基础，与语言无关，包括空白和标点符号。
时空权衡
：更宽的克范围
[min_gram, max_gram]
会产生更多的克和更大的索引。如果内存紧张，可考虑使用
mmap
模式处理大型张贴列表。更多信息，请参阅
使用 mmap
。
不变性
：
min_gram
和
max_gram
不能就地更改，需要重新构建索引才能调整。
最佳实践
选择 min_gram 和 max_gram 以匹配搜索行为
从
min_gram=2
,
max_gram=3
开始。
将
min_gram
设置为用户希望键入的最短文字。
将
max_gram
设置为接近有意义子字符串的典型长度；较大的
max_gram
可以提高过滤效果，但会增加空间。
避免低选择性语法
高度重复的模式（如
"aaaaaa"
）过滤效果较弱，收益有限。
统一规范化
如果您的用例需要，对摄取的文本和查询字面采用相同的规范化处理（如小写、修剪）。