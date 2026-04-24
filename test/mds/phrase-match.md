短语匹配
Compatible with Milvus 2.5.17+
短语匹配可让您搜索包含精确短语查询词的文档。默认情况下，单词必须以相同的顺序出现，并且彼此直接相邻。例如，
"机器人机器学习 "
的查询会匹配"
...典型的机器人机器学习模型... "
这样的文本，其中
"机器人"、
"
机器 "
和
"学习 "
依次出现，中间没有其他词。
然而，在现实世界中，严格的短语匹配可能过于死板。您可能希望匹配的文本是
"......机器人技术中广泛采用的机器学习模型.
....."。在这种情况下，相同的关键词会出现，但不会并排出现，也不会按照原来的顺序排列。为了处理这种情况，短语匹配支持一个
slop
参数，从而增加了灵活性。
slop
的值定义了短语中的词语之间允许多少次位置移动。例如，当
slop
为 1 时，
"机器学习 "
查询可以匹配
"......机器深度学习...... "
这样的文本，其中一个单词（
"deep"）
分隔了原始术语。
概述
短语匹配由
Tantivy
搜索引擎库提供支持，通过分析文档中单词的位置信息来实现。下图说明了这一过程：
短语匹配工作流程
文档标记化
：将文档插入 Milvus 时，使用分析器将文本分割成标记（单个词或术语），并记录每个标记的位置信息。例如，
doc_1
被标记为
["machine" (pos=0), "learning" (pos=1), "boosts" (pos=2), "efficiency" (pos=3)]
。有关分析器的更多信息，请参阅
分析器概述
。
反向索引创建
：Milvus 建立一个倒排索引，将每个标记映射到出现该标记的文档以及标记在这些文档中的位置。
短语匹配
：当执行短语查询时，Milvus 会查找倒排索引中的每个标记，并检查它们的位置，以确定它们是否以正确的顺序和相邻关系出现。
slop
参数控制匹配标记之间允许的最大位置数：
slop = 0
表示词组必须
以完全相同的顺序
出现
，并且紧邻
（即中间没有多余的字）。
在本例中，只有
doc_1
（
"machine "
在
位置 0
，
"learning "
在
位置 1
）完全匹配。
slop = 2
允许匹配词之间最多有两个位置的灵活性或重新排列。
这就允许颠倒顺序（
"学习机器"）
或在词组之间留出小间隙。
因此，
doc_
1
、
doc_2
（
"learning "
在
位置=0
，
"machine "
在
位置=1
）和
doc_3
（
"learning "
在
位置=1
，
"machine
"
在
位置=2
）全部匹配。
启用短语匹配
短语匹配适用于
VARCHAR
字段类型，即 Milvus 中的字符串数据类型。要启用短语匹配，请配置您的 Collections Schema，将
enable_analyzer
和
enable_match
参数都设置为
True
，类似于
文本匹配
。
设置
enable_analyzer
和
enable_match
要启用特定
VARCHAR
字段的短语匹配，请在定义字段 Schema 时将
enable_analyzer
和
enable_match
参数设置为
True
。该配置指示 Milvus 对文本进行标记化，并创建一个具有位置信息的反向索引，以实现高效的短语匹配。
下面是启用短语匹配的 Schema 定义示例：
from
pymilvus
import
MilvusClient, DataType
# Create a schema for a new collection
schema = MilvusClient.create_schema(enable_dynamic_field=
False
)
schema.add_field(
    field_name=
"id"
,
    datatype=DataType.INT64,
    is_primary=
True
,
    auto_id=
True
)
# Add a VARCHAR field configured for phrase matching
schema.add_field(
    field_name=
'text'
,
# Name of the field
datatype=DataType.VARCHAR,
# Field data type set as VARCHAR (string)
max_length=
1000
,
# Maximum length of the string
enable_analyzer=
True
,
# Enables text analysis (tokenization)
enable_match=
True
# Enables inverted indexing for phrase matching
)
schema.add_field(
    field_name=
"embeddings"
,
    datatype=DataType.FLOAT_VECTOR,
    dim=
5
)
可选：配置分析器
短语匹配的准确性在很大程度上取决于用于标记文本数据的分析器。不同的分析器适用于不同的语言和文本格式，会影响标记化和定位的准确性。根据具体使用情况选择合适的分析器，可以优化短语匹配结果。
默认情况下，Milvus 使用标准分析器，根据空白和标点符号对文本进行标记化，删除长度超过 40 个字符的标记，并将文本转换为小写。默认用法不需要额外参数。详情请参阅
标准分析器
。
如果您的应用程序需要特定的分析器，请使用
analyzer_params
参数进行配置。例如，以下是如何配置
english
分析器，用于英文文本中的短语匹配：
# Define analyzer parameters for English-language tokenization
analyzer_params = {
"type"
:
"english"
}
# Add the VARCHAR field with the English analyzer enabled
schema.add_field(
    field_name=
'text'
,
# Name of the field
datatype=DataType.VARCHAR,
# Field data type set as VARCHAR
max_length=
1000
,
# Maximum length of the string
enable_analyzer=
True
,
# Enables text analysis
analyzer_params=analyzer_params,
# Specifies the analyzer configuration
enable_match=
True
# Enables inverted indexing for phrase matching
)
Milvus 支持针对不同语言和用例定制的多种分析器。有关详细信息，请参阅
分析器概述
。
使用短语匹配
为 Collections Schema 中的
VARCHAR
字段启用匹配后，就可以使用
PHRASE_MATCH
表达式执行短语匹配。
PHRASE_MATCH
表达式不区分大小写。可以使用
PHRASE_MATCH
或
phrase_match
。
PHRASE_MATCH 表达式语法
搜索时，使用
PHRASE_MATCH
表达式指定字段、短语和可选的灵活性 (
slop
)。语法如下
PHRASE_MATCH(field_name, phrase, slop)
field_name
:
执行短语匹配的
VARCHAR
字段名称。
phrase
:
要搜索的确切短语。
slop
(可选）
：
一个整数，指定匹配标记中允许的最大位置数。
0
(默认）：只匹配精确短语。例如
机器学习 "
过滤器将精确匹配
"
machine learning"
，但不匹配
"machine boosts learning "
或
"learning machine"。
1
:允许细微变化，例如多一个词或位置上的细微变化。例如
机器学习 "
过滤器将匹配
"machine boosts learning"
（
"machine "
和
"learning "
之间有一个标记
）
，但不匹配
"learning machine"
（术语颠倒）。
2
:允许更多的灵活性，包括术语顺序颠倒或最多在两个词组之间。例如
机器学习 "
过滤器将匹配
"学习机器"
（词序颠倒）或
"机器快速促进学习"
（
"机器 "
和
"学习 "
之间有两个词组
）
。
数据集示例
假设您有一个名为
tech_articles 的
Collections，其中包含以下五个实体：
doc_id
text
1
"机器学习提高了大规模数据分析的效率
2
"学习基于机器的方法对现代人工智能的发展至关重要" 3
3
"深度学习机器架构优化了计算负荷"
4
"机器迅速提高持续学习的模型性能"
5
"学习先进的机器算法，扩展人工智能能力
短语匹配查询
使用
query()
方法时，
PHRASE_MATCH 充当
标量过滤器。只有包含指定短语的文档才会返回（取决于允许的斜率）。
示例：slop = 0（精确匹配）
此示例返回包含精确短语
"machine learning "
的文档，中间不包含任何额外标记。
# Match documents containing exactly "machine learning"
filter
=
"PHRASE_MATCH(text, 'machine learning')"
result = client.query(
    collection_name=
"tech_articles"
,
filter
=
filter
,
    output_fields=[
"id"
,
"text"
]
)
预期匹配结果
doc_id
text
1
"机器学习提高了大规模数据分析的效率
只有文档 1 按指定顺序包含精确短语
"machine learning"
，且没有额外标记。
使用短语匹配进行搜索
在搜索操作中，
PHRASE_MATCH
用于在应用向量相似性排序之前过滤文档。这种两步法首先通过文本匹配缩小候选集的范围，然后根据向量嵌入重新对这些候选集进行排序。
示例：斜率 = 1
这里，我们允许斜率为 1。该过滤器适用于包含
"学习机 "
短语的文档，并略有灵活性。
# Example: Filter documents containing "learning machine" with slop=1
filter_slop1 =
"PHRASE_MATCH(text, 'learning machine', 1)"
result_slop1 = client.search(
    collection_name=
"tech_articles"
,
    anns_field=
"embeddings"
,
    data=[query_vector],
filter
=filter_slop1,
    search_params={
"params"
: {
"nprobe"
:
10
}},
    limit=
10
,
    output_fields=[
"id"
,
"text"
]
)
匹配结果
doc_id
text
2
"学习基于机器的方法对现代人工智能的进步至关重要"
3
"深度学习机器架构优化了计算负荷" 4
5
"学习先进的机器算法可扩展人工智能能力" 6
示例：斜率 = 2
此示例允许 2 个斜率，即在
"机器 "
和
"学习 "
之间允许最多两个额外的词块（或反义词）
。
# Example: Filter documents containing "machine learning" with slop=2
filter_slop2 =
"PHRASE_MATCH(text, 'machine learning', 2)"
result_slop2 = client.search(
    collection_name=
"tech_articles"
,
    anns_field=
"embeddings"
,
# Vector field name
data=[query_vector],
# Query vector
filter
=filter_slop2,
# Filter expression
search_params={
"params"
: {
"nprobe"
:
10
}},
    limit=
10
,
# Maximum results to return
output_fields=[
"id"
,
"text"
]
)
匹配结果
doc_id
text
1
"机器学习提高了大规模数据分析的效率
3
"深度学习机器架构优化了计算负荷"
示例：斜率 = 3
在本例中，斜率为 3 提供了更大的灵活性。该过滤器搜索
"机器学习"
，词与词之间最多允许有三个标记位置。
# Example: Filter documents containing "machine learning" with slop=3
filter_slop3 =
"PHRASE_MATCH(text, 'machine learning', 3)"
result_slop2 = client.search(
    collection_name=
"tech_articles"
,
    anns_field=
"embeddings"
,
# Vector field name
data=[query_vector],
# Query vector
filter
=filter_slop3,
# Filter expression
search_params={
"params"
: {
"nprobe"
:
10
}},
    limit=
10
,
# Maximum results to return
output_fields=[
"id"
,
"text"
]
)
匹配结果
doc_id
text
1
"机器学习提高了大规模数据分析的效率
2
"学习基于机器的方法对现代人工智能的进步至关重要"
3
"深度学习机器架构优化了计算负荷" 4
5
"学习先进的机器算法可扩展人工智能能力" 6
注意事项
为字段启用短语匹配会触发倒排索引的创建，从而消耗存储资源。在决定是否启用此功能时，请考虑对存储的影响，因为它根据文本大小、唯一标记和所使用的分析器而有所不同。
在 Schema 中定义分析器后，其设置将永久适用于该 Collections。如果您认为不同的分析器更适合您的需要，可以考虑删除现有的 Collections，然后使用所需的分析器配置创建一个新的 Collections。
短语匹配性能取决于文本标记化的方式。在将分析器应用到整个 Collections 之前，请使用
run_analyzer
方法查看标记化输出。有关详细信息，请参阅
分析器概述
。
filter
表达式中的转义规则：
表达式中用双引号或单引号括起来的字符被解释为字符串常量。如果字符串常量包含转义字符，则必须使用转义序列来表示转义字符。例如，用
\\
表示
\
，用
\\t
表示制表符
\t
，用
\\n
表示换行符。
如果字符串常量由单引号括起来，常量内的单引号应表示为
\\'
，而双引号可表示为
"
或
\\"
。 示例：
'It\\'s milvus'
。
如果字符串常量由双引号括起来，常量中的双引号应表示为
\\"
，而单引号可表示为
'
或
\\'
。 示例：
"He said \\"Hi\\""
。