语言识别器
Compatible with Milvus v2.5.15+
language_identifier
是一个专门的标记符号器，旨在通过自动语言分析过程来增强 Milvus 的文本搜索功能。它的主要功能是检测文本字段的语言，然后动态应用最适合该语言的预配置分析器。这对于处理多种语言的应用程序来说尤为重要，因为它消除了根据每次输入手动分配语言的需要。
通过智能地将文本数据路由到适当的处理管道，
language_identifier
可简化多语言数据的摄取，并确保为后续搜索和检索操作提供准确的标记化。
语言检测工作流程
language_identifier
执行一系列步骤来处理文本字符串，这个工作流程对于用户了解如何正确配置至关重要。
语言检测工作流程
输入：
工作流程以文本字符串作为输入开始。
语言检测：
首先将该字符串传递给语言检测引擎，尝试识别语言。Milvus 支持两种引擎：
Whatlang
和
lingua
。
分析器选择：
成功：
如果语言检测成功，系统会检查检测到的语言名称是否在
analyzers
字典中配置了相应的分析器。如果找到匹配，系统就会将指定的分析器应用于输入文本。例如，检测到的 "普通话 "文本将被路由到
jieba
标记器。
回退：
如果检测失败，或者如果成功检测到一种语言，但您没有为其提供特定的分析器，系统会默认使用预先配置的
默认分析器
。这是需要说明的关键点；
default
分析仪是检测失败和没有匹配分析仪时的后备选择。
选择合适的分析器后，文本将被标记化并处理，从而完成工作流程。
可用的语言检测引擎
Milvus 提供两种语言检测引擎供选择：
whatlang
lingua
选择取决于您应用程序的具体性能和准确性要求。
引擎
速度
精确度
输出格式
最适合
whatlang
快速
适合大多数语言
语言名称（如
"English"
,
"Mandarin"
,
"Japanese"
)
参考：
支持语言表中的语言栏
速度至关重要的实时应用
lingua
较慢
精度更高，尤其是短文本
英文名称（如
"English"
,
"Chinese"
,
"Japanese"
)
参考：
支持的语言列表
精度比速度更重要的应用
一个重要的考虑因素是引擎的命名约定。虽然两个引擎都以英文返回语言名称，但它们对某些语言使用不同的术语（例如，
whatlang
返回
Mandarin
，而
lingua
返回
Chinese
）。分析仪的关键字必须与所选检测引擎返回的名称完全匹配。
配置
要正确使用
language_identifier
标记符号生成器，必须采取以下步骤来定义和应用其配置。
第 1 步：选择语言和分析器
设置
language_identifier
的核心是根据计划支持的特定语言定制分析器。系统的工作原理是将检测到的语言与正确的分析器相匹配，因此这一步对于准确处理文本至关重要。
下面是推荐的语言与 Milvus 分析器的映射表。该表是连接语言检测引擎输出和最佳工具的桥梁。
语言（检测器输出）
推荐分析器
语言
English
type: english
标准英语标记化，带词干和停止词过滤。
Mandarin
(通过 whatlang）或
Chinese
（通过 lingua）
tokenizer: jieba
针对非空间分隔文本的中文分词。
Japanese
tokenizer: icu
适用于复杂脚本（包括日文）的强大标记化器。
French
type: standard
,
filter: ["lowercase", "asciifolding"]
可处理法语重音和字符的自定义配置。
匹配是关键：
分析器的名称
必须与
检测引擎的语言输出
完全匹配
。例如，如果使用
whatlang
，则中文文本的密钥必须是
Mandarin
。
最佳实践：
上表提供了几种常见语言的推荐配置，但并非详尽无遗。有关选择分析仪的更全面指南，请参阅
为您的用例选择正确的分析仪
。
检测器输出
：有关检测引擎返回的语言名称的完整列表，请参阅
Whatlang 支持的语言表
和
Lingua 支持的语言列表
。
第 2 步：定义分析器参数
要在 Milvus 中使用
language_identifier
标记器，请创建一个包含这些关键组件的字典：
必备组件：
analyzers
config set - 包含所有分析器配置的字典，其中必须包括
default
- 语言检测失败或找不到匹配分析器时使用的后备分析器
特定语言分析器
- 每个
分析器
定义为
<analyzer_name>: <analyzer_config>
，其中：
analyzer_name
与您选择的检测引擎输出相匹配（如
"English"
,
"Japanese"
）。
analyzer_config
遵循标准分析器参数格式（请参阅
分析器概述）
可选组件：
identifier
- 指定要使用的语言检测引擎（
whatlang
或
lingua
）。如果未指定，默认为
whatlang
mapping
- 为您的分析器创建自定义别名，允许您使用描述性名称，而不是检测引擎的精确输出格式。
标记器的工作原理是首先检测输入文本的语言，然后从配置中选择合适的分析器。如果检测失败或没有匹配的分析器，它会自动返回到
default
分析器。
推荐使用：直接名称匹配
分析器名称应与所选语言检测引擎的输出完全匹配。这种方法比较简单，可以避免潜在的混淆。
对于
whatlang
和
lingua
，请使用各自文档中显示的语言名称：
whatlang 支持的语言
（使用
"语言
"列）
lingua 支持的语言
analyzer_params = {
"tokenizer"
: {
"type"
:
"language_identifier"
,
# Must be `language_identifier`
"identifier"
:
"whatlang"
,
# or `lingua`
"analyzers"
: {
# A set of analyzer configs
"default"
: {
"tokenizer"
:
"standard"
# fallback if language detection fails
},
"English"
: {
# Analyzer name that matches whatlang output
"type"
:
"english"
},
"Mandarin"
: {
# Analyzer name that matches whatlang output
"tokenizer"
:
"jieba"
}
        }
    }
}
替代方法：带有映射的自定义名称
如果喜欢使用自定义分析器名称，或需要保持与现有配置的兼容性，可以使用
mapping
参数。这将为您的分析器创建别名--原始检测引擎名称和自定义名称均可使用。
analyzer_params = {
"tokenizer"
: {
"type"
:
"language_identifier"
,
"identifier"
:
"lingua"
,
"analyzers"
: {
"default"
: {
"tokenizer"
:
"standard"
},
"english_analyzer"
: {
# Custom analyzer name
"type"
:
"english"
},
"chinese_analyzer"
: {
# Custom analyzer name
"tokenizer"
:
"jieba"
}
        },
"mapping"
: {
"English"
:
"english_analyzer"
,
# Maps detection output to custom name
"Chinese"
:
"chinese_analyzer"
}
    }
}
定义
analyzer_params
后，您可以在定义 Collections Schema 时将它们应用到
VARCHAR
字段。这样，Milvus 就能使用指定的分析器处理该字段中的文本，从而实现高效的标记化和过滤。有关详情，请参阅
示例使用
。
示例
下面是一些常见情况下的即用配置。每个示例都包含配置和验证代码，因此您可以立即对设置进行测试。
英语和中文检测
from
pymilvus
import
MilvusClient
# Configuration
analyzer_params = {
"tokenizer"
: {
"type"
:
"language_identifier"
,
"identifier"
:
"whatlang"
,
"analyzers"
: {
"default"
: {
"tokenizer"
:
"standard"
},
"English"
: {
"type"
:
"english"
},
"Mandarin"
: {
"tokenizer"
:
"jieba"
}
        }
    }
}
# Test the configuration
client = MilvusClient(
    uri=
"http://localhost:19530"
,
    token=
"root:Milvus"
)
# English text
result_en = client.run_analyzer(
"The Milvus vector database is built for scale!"
, analyzer_params)
print
(
"English:"
, result_en)
# Output:
# English: ['The', 'Milvus', 'vector', 'database', 'is', 'built', 'for', 'scale']
# Chinese text
result_cn = client.run_analyzer(
"Milvus向量数据库专为大规模应用而设计"
, analyzer_params)
print
(
"Chinese:"
, result_cn)
# Output:
# Chinese: ['Milvus', '向量', '数据', '据库', '数据库', '专', '为', '大规', '规模', '大规模', '应用', '而', '设计']
带重音规范化的欧洲语言
# Configuration for French, German, Spanish, etc.
analyzer_params = {
"tokenizer"
: {
"type"
:
"language_identifier"
,
"identifier"
:
"lingua"
,
"analyzers"
: {
"default"
: {
"tokenizer"
:
"standard"
},
"English"
: {
"type"
:
"english"
},
"French"
: {
"tokenizer"
:
"standard"
,
"filter"
: [
"lowercase"
,
"asciifolding"
]
            }
        }
    }
}
# Test with accented text
result_fr = client.run_analyzer(
"Café français très délicieux"
, analyzer_params)
print
(
"French:"
, result_fr)
# Output:
# French: ['cafe', 'francais', 'tres', 'delicieux']
使用说明
每个字段使用一种语言：
它将字段作为单一、同质的文本单元进行操作符。其设计目的是处理不同数据记录中的不同语言，例如一条记录包含英语句子，而另一条记录包含法语句子。
无混合语言字符串：
它
不能
处理包含多种语言文本的单一字符串。例如，包含英语句子和日语短语的
VARCHAR
字段将作为单一语言处理。
主导语言处理：
在混合语言情况下，检测引擎可能会识别主要语言，并将相应的分析器应用于整个文本。这将导致嵌入的外文文本标记化效果不佳或没有标记化。