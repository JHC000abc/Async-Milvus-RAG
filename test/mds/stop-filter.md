停止词
stop
过滤器会从标记化文本中移除指定的停止词，帮助剔除常见的、意义不大的词。您可以使用
stop_words
参数配置停用词列表。
配置
stop
过滤器是 Milvus 的自定义过滤器。要使用它，请在过滤器配置中指定
"type": "stop"
以及提供停用词列表的
stop_words
参数。
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
:[{
"type"
:
"stop"
,
# Specifies the filter type as stop
"stop_words"
: [
"of"
,
"to"
,
"_english_"
],
# Defines custom stop words and includes the English stop word list
}],
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
        Collections.singletonList(
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
, Arrays.asList(
"of"
,
"to"
,
"_english_"
));
                }}
        )
);
const
analyzer_params = {
"tokenizer"
:
"standard"
,
"filter"
:[{
"type"
:
"stop"
, #
Specifies
the filter type
as
stop
"stop_words"
: [
"of"
,
"to"
,
"_english_"
], #
Defines
custom stop words and includes the
English
stop word list
    }],
};
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
map
[
string
]any{
"type"
:
"stop"
,
"stop_words"
: []
string
{
"of"
,
"to"
,
"_english_"
},
    }}}
# restful
analyzerParams=
'{
  "tokenizer": "standard",
  "filter": [
    {
      "type": "stop",
      "stop_words": [
        "of",
        "to",
        "_english_"
      ]
    }
  ]
}'
stop
过滤器接受以下可配置参数。
参数
说明
stop_words
要从标记化中删除的单词列表。默认情况下，过滤器使用内置的
_english_
词典。您可以通过三种方式覆盖或扩展它：
内置词典
- 提供以下语言别名之一，以使用预定义词典：
"_english_"
,
"_danish_"
,
"_dutch_"
,
"_finnish_"
,
"_french_"
,
"_german_"
,
"_hungarian_"
,
"_italian_"
,
"_norwegian_"
,
"_portuguese_"
,
"_russian_"
,
"_spanish_"
、
"_swedish_"
自定义列表
- 传递您自己的术语数组，如
["foo", "bar", "baz"]
。
混合列表
- 结合别名和自定义术语，如
["of", "to", "_english_"]
。
有关每个预定义词典的具体内容，请参阅
stop_words
。
stop
过滤器对标记化器生成的术语进行操作，因此必须与标记化器结合使用。有关 Milvus 中可用的标记符列表，请参阅
标准
标记符及其同类页面。
定义
analyzer_params
后，可以在定义 Collections Schema 时将其应用到
VARCHAR
字段。这样，Milvus 就可以使用指定的分析器对该字段中的文本进行处理，从而实现高效的标记化和过滤。有关详情，请参阅
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
:
"standard"
,
"filter"
:[{
"type"
:
"stop"
,
# Specifies the filter type as stop
"stop_words"
: [
"of"
,
"to"
,
"_english_"
],
# Defines custom stop words and includes the English stop word list
}],
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
        Collections.singletonList(
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
, Arrays.asList(
"of"
,
"to"
,
"_english_"
));
                }}
        )
);
// javascript
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
map
[
string
]any{
"type"
:
"stop"
,
"stop_words"
: []
string
{
"of"
,
"to"
,
"_english_"
},
    }}}
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

client = MilvusClient(uri=
"http://localhost:19530"
)
# Sample text to analyze
sample_text =
"The stop filter allows control over common stop words for text processing."
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
"The stop filter allows control over common stop words for text processing."
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
"The stop filter allows control over common stop words for text processing."
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
'The'
,
'stop'
,
'filter'
,
'allows'
,
'control'
,
'over'
,
'common'
,
'stop'
,
'words'
,
'text'
,
'processing'
]