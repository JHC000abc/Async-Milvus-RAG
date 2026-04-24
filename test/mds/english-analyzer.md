英语
Milvus 中的
english
分析器旨在处理英文文本，应用特定语言规则进行标记化和过滤。
定义
english
分析器使用以下组件：
标记化器
：使用
standard
标记化器
将文本分割成离散的单词单位。
过滤器
：包括多个过滤器，用于全面处理文本：
lowercase
:将所有标记转换为小写，从而实现不区分大小写的搜索。
stemmer
:将单词还原为词根形式，以支持更广泛的匹配（例如，"running "变为 "run"）。
stop_words
:删除常见的英文停止词，以便集中搜索文本中的关键词语。
english
分析器的功能相当于以下自定义分析器配置：
Python
Java
NodeJS
Go
cURL
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
}, {
"type"
:
"stop"
,
"stop_words"
:
"_english_"
}
        ]
}
Map<String, Object> analyzerParams =
new
HashMap
<>();
analyzerParams.put(
"tokenizer"
,
"standard"
);
analyzerParams.put(
"filter"
,
        Arrays.asList(
"lowercase"
,
new
HashMap
<String, Object>() {{
                    put(
"type"
,
"stemmer"
);
                    put(
"language"
,
"english"
);
                }},
new
HashMap
<String, Object>() {{
                    put(
"type"
,
"stop"
);
                    put(
"stop_words"
, Collections.singletonList(
"_english_"
));
                }}
        )
);
const
analyzer_params = {
"type"
:
"standard"
,
// Specifies the standard analyzer type
"stop_words"
, [
"of"
]
// Optional: List of words to exclude from tokenization
}
analyzerParams =
map
[
string
]any{
"tokenizer"
:
"standard"
,
"filter"
: []any{
"lowercase"
,
map
[
string
]any{
"type"
:
"stemmer"
,
"language"
:
"english"
,
        },
map
[
string
]any{
"type"
:
"stop"
,
"stop_words"
:
"_english_"
,
        }}}
# restful
analyzerParams=
'{
  "tokenizer": "standard",
  "filter": [
    "lowercase",
    {
      "type": "stemmer",
      "language": "english"
    },
    {
      "type": "stop",
      "stop_words": "_english_"
    }
  ]
}'
配置
要将
english
分析器应用到一个字段，只需在
analyzer_params
中将
type
设置为
english
，并根据需要加入可选参数即可。
Python
Java
NodeJS
Go
cURL
analyzer_params = {
"type"
:
"english"
,
}
Map<String, Object> analyzerParams =
new
HashMap
<>();
analyzerParams.put(
"type"
,
"english"
);
const
analyzer_params = {
"type"
:
"english"
,
}
analyzerParams =
map
[
string
]any{
"type"
:
"english"
}
# restful
analyzerParams=
'{
  "type": "english"
}'
english
分析器接受以下可选参数：
参数
说明
stop_words
一个数组，包含将从标记化中删除的停用词列表。默认为
_english_
，这是一组内置的常用英语停止词。
自定义停止词配置示例：
Python
Java
NodeJS
Go
cURL
analyzer_params = {
"type"
:
"english"
,
"stop_words"
: [
"a"
,
"an"
,
"the"
]
}
Map<String, Object> analyzerParams =
new
HashMap
<>();
analyzerParams.put(
"type"
,
"english"
);
analyzerParams.put(
"stop_words"
, Arrays.asList(
"a"
,
"an"
,
"the"
));
const
analyzer_params = {
"type"
:
"english"
,
"stop_words"
: [
"a"
,
"an"
,
"the"
]
}
analyzerParams =
map
[
string
]any{
"type"
:
"english"
,
"stop_words"
: []
string
{
"a"
,
"an"
,
"the"
}}
# restful
analyzerParams=
'{
  "type": "english",
  "stop_words": [
    "a",
    "an",
    "the"
  ]
}'
定义
analyzer_params
后，您可以在定义 Collections Schema 时将其应用到
VARCHAR
字段。这样，Milvus 就能使用指定的分析器处理该字段中的文本，从而实现高效的标记化和过滤。有关详情，请参阅
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
"type"
:
"english"
,
"stop_words"
: [
"a"
,
"an"
,
"the"
]
}
Map<String, Object> analyzerParams =
new
HashMap
<>();
analyzerParams.put(
"type"
,
"english"
);
analyzerParams.put(
"stop_words"
, Arrays.asList(
"a"
,
"an"
,
"the"
));
// javascript
analyzerParams =
map
[
string
]any{
"type"
:
"english"
,
"stop_words"
: []
string
{
"a"
,
"an"
,
"the"
}}
# restful
analyzerParams=
'{
  "type": "english",
  "stop_words": [
    "a",
    "an",
    "the"
  ]
}'
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

client = MilvusClient(uri=
"http://localhost:19530"
)
# Sample text to analyze
sample_text =
"Milvus is a vector database built for scale!"
# Run the standard analyzer with the defined configuration
result = client.run_analyzer(sample_text, analyzer_params)
print
(
"English analyzer output:"
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
"Milvus is a vector database built for scale!"
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
"Milvus is a vector database built for scale!"
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
English analyzer output: [
'milvus'
,
'vector'
,
'databas'
,
'built'
,
'scale'
]