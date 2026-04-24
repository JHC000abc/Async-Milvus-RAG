根据使用案例选择正确的分析仪
本指南侧重于分析仪选择的实际决策。有关分析仪组件和如何添加分析仪参数的技术细节，请参阅
分析仪概述
。
在 2 分钟内了解分析仪
在 Milvus 中，分析器处理存储在该字段中的文本，使其可用于
全文搜索
(BM25)、
短语匹配
或
文本匹配
等功能的搜索。可以把它想象成一个文本处理器，把原始内容转换成可搜索的标记。
分析器通过一个简单的两阶段管道工作：
分析器工作流程
标记化（必需）：
初始阶段应用
标记化器
，将连续的文本字符串分解成离散的、有意义的单元（称为标记）。标记化方法会因语言和内容类型的不同而有很大差异。
标记过滤（可选）：
标记化之后，应用
过滤器
来修改、删除或完善标记。这些操作可包括将所有标记符转换为小写、删除常见的无意义词语（如停止词）或将词语还原为词根形式（词干化）。
举例说明
：
Input: "Hello World!" 
       1. Tokenization → ["Hello", "World", "!"]
       2. Lowercase & Punctuation Filtering → ["hello", "world"]
为什么分析器的选择很重要
选择错误的分析器会导致相关文档无法搜索或返回不相关的结果。
下表总结了分析器选择不当导致的常见问题，并提供了诊断搜索问题的可行解决方案。
问题
症状
示例（输入和输出）
原因（不良分析仪）
解决方案（好的分析仪）
过度标示
技术术语、标识符或 URL 的文本查询无法找到相关文档。
"user_id"
→
['user', 'id']
"C++"
→
['c']
standard
分析器
使用
whitespace
标记符；与
alphanumonly
过滤器。
标记不足
搜索多词短语的一个组成部分时，无法返回包含完整短语的文档。
"state-of-the-art"
→
['state-of-the-art']
带有
whitespace
标记化器
使用
standard
标记符来分割标点符号和空格；使用自定义
regex
过滤器。
语言不匹配
特定语言的搜索结果不合理或不存在。
中文文本：
"机器学习"
→
['机器学习']
（一个标记）
english
分析器
使用特定语言的分析器，如
chinese
.
第一个问题需要选择分析器吗？
对于许多用例，您不需要做任何特别的事情。让我们来判断您是否属于这种情况。
默认行为：
standard
分析器
如果在使用全文检索等文本检索功能时没有指定分析器，Milvus 会自动使用
standard
分析器。
standard
分析器：
根据空格和标点符号分割文本
将所有标记转换为小写字母
删除一组内置的常用英文停顿词和大部分标点符号
转换示例
：
Input:  "The Milvus vector database is built for scale!"
Output: ['the', 'milvus', 'vector', 'database', 'is', 'built', 'scale']
判定标准：快速检查
使用本表可快速确定
standard
默认分析器是否满足您的需求。如果不符合，则需要选择其他路径。
您的内容
标准分析仪可以吗？
为什么
您的需求
英文博客文章
✅ 是
默认行为即可。
使用默认行为（无需配置）。
中文文档
❌ 否
中文单词没有空格，将被视为一个标记。
使用内置
chinese
分析器。
技术文档
❌否
标点符号会从
C++
等术语中去除。
创建带有
whitespace
标记符和
alphanumonly
过滤器。
空格分隔语言，如法语/西班牙语文本
⚠️ 可能
重音字符 (
café
与
cafe
) 可能不匹配。
建议使用带有
asciifolding
的自定义分析器可获得更好的结果。
多语种或未知语言
❌ 否
standard
分析仪缺乏处理不同字符集和标记化规则所需的特定语言逻辑。
使用带有
icu
标记化器进行单编码标记化。
或者，考虑配置
多语言分析器
或
语言标识符
，以便更精确地处理多语言内容。
如果默认的
standard
分析器不能满足您的要求，您就需要实施一个不同的分析器。您有两种选择：
使用内置分析器
或
创建自定义分析器
路径 A：使用内置分析器
内置分析器是为常用语言预先配置的解决方案。当默认的标准分析器不适合时，它们是最简单的入门方法。
可用的内置分析器
分析器
语言支持
组件
注释
standard
大多数空格分隔语言（英语、法语、德语、西班牙语等）
分词器
standard
过滤器：
lowercase
用于初始文本处理的通用分析器。对于单语场景，特定语言分析器（如
english
）可提供更好的性能。
english
专用于英语，可应用词干和停顿词去除，以实现更好的英语语义匹配
分词器：
standard
过滤器
lowercase
,
stemmer
、
stop
推荐用于纯英文内容，超过
standard
。
chinese
中文
Tokenizer：
jieba
过滤器：
cnalphanumonly
目前默认使用简体中文字典。
实施示例
要使用内置分析器，只需在定义字段模式时在
analyzer_params
中指定其类型即可。
# Using built-in English analyzer
analyzer_params = {
"type"
:
"english"
}
# Applying analyzer config to target VARCHAR field in your collection schema
schema.add_field(
    field_name=
'text'
,
    datatype=DataType.VARCHAR,
    max_length=
200
,
    enable_analyzer=
True
,
analyzer_params=analyzer_params,
)
有关详细用法，请参阅
全文搜索
、
文本匹配
或
短语匹配
。
路径 B：创建自定义分析器
当
内置选项
无法满足您的需求时，您可以通过将标记符与一组过滤器相结合来创建自定义分析器。这样就可以完全控制文本处理管道。
第 1 步：根据语言选择标记符
根据内容的主要语言选择标记符：
西方语言
对于空格分隔的语言，您有以下选项：
标记符
如何使用
最适合
示例
standard
根据空格和标点符号分割文本
一般文本，混合标点符号
输入：
"Hello, world! Visit example.com"
输出：
['Hello', 'world', 'Visit', 'example', 'com']
whitespace
仅根据空白字符分割
预处理内容、用户格式文本
输入： 输出
"user_id = get_user_data()"
输出
['user_id', '=', 'get_user_data()']
东亚语言
以字典为基础的语言需要专门的标记化器来正确分词：
中文
分词器
工作原理
最适合
实例
jieba
基于词典的中文智能分词算法
推荐用于中文内容
--结合词典和智能算法，专为中文设计
输入
"机器学习是人工智能的一个分支"
输出：
['机器', '学习', '是', '人工', '智能', '人工智能', '的', '一个', '分支']
lindera
基于中文词典的纯词典形态分析
(cc-cedict
)
与
jieba
相比，以更通用的方式处理中文文本
输入：输出
"机器学习算法"
输出：
["机器", "学习", "算法"]
日语和韩语
语言
分词器
词典选项
最适合
例子
日语
lindera
ipadic
（通用）、ipadic-
neologd
（现代术语）、
unidic
（学术术语）
处理专有名词的词形分析
输入
"東京都渋谷区"
输出：
["東京", "都", "渋谷", "区"]
韩语
lindera
ko-dic
韩语形态分析
输入
"안녕하세요"
输出
["안녕", "하", "세요"]
多语言或未知语言
适用于文档中语言不可预测或混合的内容：
分词器
工作原理
最适合
示例
icu
识别统一码的标记化（统一码国际组件）
混合脚本、未知语言，或只需简单的标记化即可
输入
"Hello 世界 مرحبا"
输出
['Hello', ' ', '世界', ' ', 'مرحبا']
何时使用 icu
：
语言识别不切实际的混合语言。
您不需要
多语言分析器
或
语言识别器
的开销。
内容以一种语言为主，偶尔出现对整体意义影响不大的外来词（例如，英文文本中偶尔出现日文或法文的品牌名称或技术术语）。
其他方法
：要更精确地处理多语言内容，可考虑使用多语言分析器或语言识别器。详情请参阅
多语言分析器
或
语言标识符
。
第 2 步：添加过滤器以提高精确度
选择标记符后
，根据具体的搜索要求和内容特征应用过滤器。
常用过滤器
这些过滤器对于大多数空格分隔的语言配置（英语、法语、德语、西班牙语等）至关重要，可显著提高搜索质量：
过滤器
如何使用
何时使用
示例
lowercase
将所有标记转换为小写
通用 - 适用于所有有大小写区分的语言
输入
["Apple", "iPhone"]
输出：
[['apple'], ['iphone']]
stemmer
将单词还原为词根形式
有词性变化的语言（英语、法语、德语等）
英语
输入
["running", "runs", "ran"]
输出：
[['run'], ['run'], ['ran']]
stop
删除常见的无意义词语
大多数语言--对空格分隔的语言尤其有效
输入：
["the", "quick", "brown", "fox"]
输出：
[[], ['quick'], ['brown'], ['fox']]
对于东亚语言（中文、日文、韩文等），应将重点放在
特定语言过滤器
上。这些语言通常使用不同的文本处理方法，可能不会从词干处理中明显受益。
文本规范化过滤器
这些筛选器可将文本变化标准化，以提高匹配的一致性：
过滤器
如何使用
何时使用
举例说明
asciifolding
将重音字符转换为 ASCII 对应字符
国际内容、用户生成的内容
输入
["café", "naïve", "résumé"]
输出
[['cafe'], ['naive'], ['resume']]
标记过滤
根据字符内容或长度控制保留哪些标记：
过滤
工作原理
何时使用
示例
removepunct
删除独立的标点符号
清除
jieba
,
lindera
,
icu
标记化器的输出，这些标记化器会将标点符号作为单个标记返回
输入
["Hello", "!", "world"]
输出：
[['Hello'], ['world']]
alphanumonly
只保留字母和数字
技术内容，纯文本处理
输入： 输出： 只保留字母和数字
["user123", "test@email.com"]
输出：
[['user123'], ['test', 'email', 'com']]
length
删除指定长度范围之外的标记
过滤噪音（过长标记符）
输入
["a", "very", "extraordinarily"]
输出：
[['a'], ['very'], []]
(如果
max=10）
regex
基于模式的自定义过滤
特定领域的标记要求
输入
["test123", "prod456"]
输出：
[[], ['prod456']]
(如果
expr="^prod"
)
特定语言过滤器
这些过滤器可处理特定的语言特点：
过滤器
语言
工作原理
举例说明
decompounder
德语
将复合词拆分成可搜索的成分
输入：
["dampfschifffahrt"]
输出：
[['dampf', 'schiff', 'fahrt']]
cnalphanumonly
中文
保留汉字 + 字母数字
输入：
["Hello", "世界", "123", "!@#"]
输出
[['Hello'], ['世界'], ['123'], []]
cncharonly
中文
只保留汉字
输入：
["Hello", "世界", "123"]
输出： 中文
[[], ['世界'], []]
步骤 3：组合并执行
要创建自定义分析器，您需要在
analyzer_params
字典中定义标记符和过滤器列表。筛选器将按照列出的顺序应用。
# Example: A custom analyzer for technical content
analyzer_params = {
"tokenizer"
:
"whitespace"
,
"filter"
: [
"lowercase"
,
"alphanumonly"
]
}
# Applying analyzer config to target VARCHAR field in your collection schema
schema.add_field(
    field_name=
'text'
,
    datatype=DataType.VARCHAR,
    max_length=
200
,
    enable_analyzer=
True
,
analyzer_params=analyzer_params,
)
最后：测试
run_analyzer
在应用到 Collections 之前，请务必验证您的配置：
# Sample text to analyze
sample_text =
"The Milvus vector database is built for scale!"
# Run analyzer with the defined configuration
result = client.run_analyzer(sample_text, analyzer_params)
print
(
"Analyzer output:"
, result)
需要检查的常见问题：
过度标示
：技术术语被错误分割
标示不足
：短语未正确分隔
缺失标记
：重要术语被过滤掉
有关详细用法，请参阅
run_analyzer
。
按用例推荐的配置
本节为在 Milvus 中使用分析器时的常见用例提供了推荐的标记符和过滤器配置。请选择最符合您的内容类型和搜索要求的组合。
在将分析器应用到 Collections 之前，我们建议您使用
run_analyzer
来测试和验证文本分析性能。
带重音符号的语言（法语、西班牙语、德语等）
使用带有小写转换、特定语言词干和停止词去除功能的
standard
标记符号器。通过修改
language
和
stop_words
参数，此配置也适用于其他欧洲语言。
# French example
analyzer_params = {
"tokenizer"
:
"standard"
,
"filter"
: [
"lowercase"
,
"asciifolding"
,
# Handle accent marks
{
"type"
:
"stemmer"
,
"language"
:
"french"
},
        {
"type"
:
"stop"
,
"stop_words"
: [
"_french_"
]
        }
    ]
}
# For other languages, modify the language parameter:
# "language": "spanish" for Spanish
# "language": "german" for German
# "stop_words": ["_spanish_"] or ["_german_"] accordingly
英文内容
用于英语文本处理和综合过滤。您还可以使用内置的
english
分析器：
analyzer_params = {
"tokenizer"
:
"standard"
,
"filter"
: [
"lowercase"
,
        {
"type"
:
"stemmer"
,
"language"
:
"english"
},
        {
"type"
:
"stop"
,
"stop_words"
: [
"_english_"
]
        }
    ]
}
# Equivalent built-in shortcut:
analyzer_params = {
"type"
:
"english"
}
中文内容
使用
jieba
标记器并应用字符过滤器，只保留汉字、拉丁字母和数字。
analyzer_params = {
"tokenizer"
:
"jieba"
,
"filter"
: [
"cnalphanumonly"
]
}
# Equivalent built-in shortcut:
analyzer_params = {
"type"
:
"chinese"
}
对于简体中文，
cnalphanumonly
删除除汉字、字母数字文本和数字以外的所有标记。这样可以防止标点符号影响搜索质量。
日语内容
使用
lindera
标记器和日语词典及过滤器来清除标点符号并控制标记长度：
analyzer_params = {
"tokenizer"
: {
"type"
:
"lindera"
,
"dict"
:
"ipadic"
# Options: ipadic, ipadic-neologd, unidic
},
"filter"
: [
"removepunct"
,
# Remove standalone punctuation
{
"type"
:
"length"
,
"min"
:
1
,
"max"
:
20
}
    ]
}
韩文内容
与日语类似，使用
lindera
标记符和韩语词典：
analyzer_params =
{
"tokenizer"
:
{
"type"
:
"lindera"
,
"dict"
:
"ko-dic"
}
,
"filter"
:
[
"removepunct"
,
{
"type"
:
"length"
,
"min"
:
1
,
"max"
:
20
}
]
}
混合或多语言内容
在处理跨多种语言或不可预测地使用脚本的内容时，可从
icu
分析器开始。这种识别 Unicode 的分析器能有效处理混合脚本和符号。
基本多语言配置（无词干）
：
analyzer_params = {
"tokenizer"
:
"icu"
,
"filter"
: [
"lowercase"
,
"asciifolding"
]
}
高级多语言处理
：
为了更好地控制不同语言的标记行为：
使用
多语言分析仪
配置。详情请参阅
多语言分析器
。
在内容中使用
语言标识符
。详情请参阅
语言标识符
。
与文本检索功能集成
选择分析器后，您可以将其与 Milvus 提供的文本检索功能集成。
全文检索
分析器通过生成稀疏向量直接影响基于 BM25 的全文检索。索引和查询使用相同的分析器，以确保标记化的一致性。与通用分析器相比，特定语言分析器通常能提供更好的 BM25 评分。有关实施细节，请参阅
全文搜索
。
文本匹配
文本匹配操作根据您的分析器输出在查询和索引内容之间执行精确的标记匹配。有关实施细节，请参阅
文本匹配
。
短语匹配
短语匹配要求对多词表达式进行一致的标记化，以保持短语的边界和含义。有关实施细节，请参阅
短语匹配
。