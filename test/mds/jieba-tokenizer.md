词霸
jieba
标记符号转换器可将中文文本分解为单词。
jieba
令牌转换器在输出中保留标点符号作为独立令牌。例如，
"你好！世界。"
变成
["你好", "！", "世界", "。"]
。要删除这些独立的标点符号，请使用
removepunct
过滤器。
配置
Milvus 支持
jieba
令牌生成器的两种配置方法：简单配置和自定义配置。
简单配置
使用简单配置，只需将标记符设置为
"jieba"
。例如
Python
Java
NodeJS
Go
cURL
# Simple configuration: only specifying the tokenizer name
analyzer_params = {
"tokenizer"
:
"jieba"
,
# Use the default settings: dict=["_default_"], mode="search", hmm=True
}
Map<String, Object> analyzerParams =
new
HashMap
<>();
analyzerParams.put(
"tokenizer"
,
"jieba"
);
const
analyzer_params = {
"tokenizer"
:
"jieba"
,
};
analyzerParams =
map
[
string
]any{
"tokenizer"
:
"jieba"
}
# restful
analyzerParams=
'{
  "tokenizer": "jieba"
}'
此简单配置等同于以下自定义配置：
Python
Java
NodeJS
Go
cURL
# Custom configuration equivalent to the simple configuration above
analyzer_params = {
"type"
:
"jieba"
,
# Tokenizer type, fixed as "jieba"
"dict"
: [
"_default_"
],
# Use the default dictionary
"mode"
:
"search"
,
# Use search mode for improved recall (see mode details below)
"hmm"
:
True
# Enable HMM for probabilistic segmentation
}
Map<String, Object> analyzerParams =
new
HashMap
<>();
analyzerParams.put(
"type"
,
"jieba"
);
analyzerParams.put(
"dict"
, Collections.singletonList(
"_default_"
));
analyzerParams.put(
"mode"
,
"search"
);
analyzerParams.put(
"hmm"
,
true
);
// javascript
analyzerParams =
map
[
string
]any{
"type"
:
"jieba"
,
"dict"
: []any{
"_default_"
},
"mode"
:
"search"
,
"hmm"
:
true
}
# restful
有关参数的详细信息，请参阅
自定义配置
。
自定义配置
为获得更多控制权，您可以提供自定义配置，允许您指定自定义字典、选择分割模式以及启用或禁用隐马尔可夫模型（HMM）。例如
Python
Java
NodeJS
Go
cURL
# Custom configuration with user-defined settings
analyzer_params = {
"tokenizer"
: {
"type"
:
"jieba"
,
# Fixed tokenizer type
"dict"
: [
"customDictionary"
],
# Custom dictionary list; replace with your own terms
"mode"
:
"exact"
,
# Use exact mode (non-overlapping tokens)
"hmm"
:
False
# Disable HMM; unmatched text will be split into individual characters
}
}
Map<String, Object> analyzerParams =
new
HashMap
<>();                                                                          
analyzerParams.put(
"tokenizer"
,
new
HashMap
<String, Object>() {{
  put(
"type"
,
"jieba"
);                                                                                                      
  put(
"dict"
, Arrays.asList(
"customDictionary"
));             
  put(
"mode"
,
"exact"
);
  put(
"hmm"
,
false
);
}});
// javascript
analyzerParams :=
map
[
string
]
interface
{}{
"tokenizer"
:
map
[
string
]
interface
{}{
"type"
:
"jieba"
,
"dict"
: []
string
{
"customDictionary"
},
"mode"
:
"exact"
,
"hmm"
:
false
,
  },
}
# restful
参数
参数
默认值
type
标记符类型。固定为
"jieba"
。
"jieba"
dict
分析器将作为词汇源加载的词典列表。内置选项：
"_default_"
:加载引擎内置的简体中文词典。详情请参阅
dict.txt
。
"_extend_default_"
:加载
"_default_"
中的所有内容以及额外的繁体中文补充。详情请参阅
dict.txt.big
。
您也可以将内置词典与任意数量的自定义词典混合使用。示例：
["_default_", "结巴分词器"]
。
["_default_"]
mode
分段模式。可能的值：
"exact"
:尝试以最精确的方式分割句子，是文本分析的理想选择。
"search"
:在精确模式的基础上进一步分解长词以提高召回率，适合搜索引擎标记化。
更多信息，请参阅
Jieba GitHub 项目
。
"search"
hmm
布尔标志，表示是否启用隐马尔可夫模型（HMM）对字典中找不到的单词进行概率分割。
true
定义
analyzer_params
后，您可以在定义 Collections Schema 时将其应用到
VARCHAR
字段。这样，Milvus 就能使用指定的分析器对该字段中的文本进行处理，以实现高效的标记化和过滤。有关详情，请参阅
示例使用
。
示例
在将分析器配置应用到 Collections 模式之前，请使用
run_analyzer
方法验证其行为。
分析器配置
Python
Java
NodeJS
Go
cURL
analyzer_params = {
"tokenizer"
: {
"type"
:
"jieba"
,
"dict"
: [
"结巴分词器"
],
"mode"
:
"exact"
,
"hmm"
:
False
}
}
Map<String, Object> analyzerParams =
new
HashMap
<>();                                                                          
analyzerParams.put(
"tokenizer"
,
new
HashMap
<String, Object>() {{
  put(
"type"
,
"jieba"
);                                                                                                      
  put(
"dict"
, Arrays.asList(
"结巴分词器"
));                   
  put(
"mode"
,
"exact"
);
  put(
"hmm"
,
false
);
}});
// javascript
analyzerParams :=
map
[
string
]
interface
{}{
"tokenizer"
:
map
[
string
]
interface
{}{
"type"
:
"jieba"
,
"dict"
: []
string
{
"结巴分词器"
},
"mode"
:
"exact"
,
"hmm"
:
false
,
  },
}
# restful
验证使用
run_analyzer
Compatible with Milvus 2.5.11+
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
(
    MilvusClient,
)

client = MilvusClient(
    uri=
"http://localhost:19530"
,
    token=
"root:Milvus"
)
# Sample text to analyze
sample_text =
"milvus结巴分词器中文测试"
# Run the standard analyzer with the defined configuration
result = client.run_analyzer(sample_text, analyzer_params)
print
(
"Standard analyzer output:"
, result)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.service.vector.request.RunAnalyzerReq;
import
io.milvus.v2.service.vector.response.RunAnalyzerResp;
ConnectConfig
config
=
ConnectConfig.builder()
        .uri(
"http://localhost:19530"
)
        .token(
"root:Milvus"
)
        .build();
MilvusClientV2
client
=
new
MilvusClientV2
(config);

List<String> texts =
new
ArrayList
<>();
texts.add(
"milvus结巴分词器中文测试"
);
RunAnalyzerResp
resp
=
client.runAnalyzer(RunAnalyzerReq.builder()
        .texts(texts)
        .analyzerParams(analyzerParams)
        .build());
List<RunAnalyzerResp.AnalyzerResult> results = resp.getResults();
// javascript
import
(
"context"
"encoding/json"
"fmt"
"github.com/milvus-io/milvus/client/v2/milvusclient"
)

client, err := milvusclient.New(ctx, &milvusclient.ClientConfig{
    Address:
"localhost:19530"
,
    APIKey:
"root:Milvus"
,
})
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}

bs, _ := json.Marshal(analyzerParams)
texts := []
string
{
"milvus结巴分词器中文测试"
}
option := milvusclient.NewRunAnalyzerOption(texts).
    WithAnalyzerParams(
string
(bs))

result, err := client.RunAnalyzer(ctx, option)
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
# restful
预期输出
[
'milvus'
,
'结巴分词器'
,
'中'
,
'文'
,
'测'
,
'试'
]