词干
stemmer
过滤器可将单词还原为其基本形式或词根形式（称为词干化），从而更容易匹配不同词性中含义相似的单词。
stemmer
过滤器支持多种语言，可在各种语言环境中进行有效搜索和索引。
配置
stemmer
过滤器是 Milvus 的自定义过滤器。要使用它，请在过滤器配置中指定
"type": "stemmer"
，并使用
language
参数选择所需的语言进行词干处理。
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
"stemmer"
,
# Specifies the filter type as stemmer
"language"
:
"english"
,
# Sets the language for stemming to English
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
"stemmer"
);
                    put(
"language"
,
"english"
);
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
"stemmer"
,
// Specifies the filter type as stop
"language"
:
"english"
, 
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
"stemmer"
,
"language"
:
"english"
,
    }}}
# restful
analyzerParams=
'{
  "tokenizer": "standard",
  "filter": [
    {
      "type": "stemmer",
      "language": "english"
    }
  ]
}'
stemmer
过滤器接受以下可配置参数。
参数
参数
language
指定词干处理的语言。支持的语言包括
"arabic"
,
"danish"
,
"dutch"
,
"english"
,
"finnish"
,
"french"
,
"german"
,
"greek"
,
"hungarian"
,
"italian"
,
"norwegian"
,
"portuguese"
,
"romanian"
,
"russian"
,
"spanish"
,
"swedish"
,
"tamil"
、
"turkish"
stemmer
过滤器对标记符生成的术语进行操作，因此必须与标记符结合使用。
定义
analyzer_params
后，可以在定义 Collections Schema 时将它们应用到
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
"stemmer"
,
# Specifies the filter type as stemmer
"language"
:
"english"
,
# Sets the language for stemming to English
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
"stemmer"
);
                    put(
"language"
,
"english"
);
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
"stemmer"
,
"language"
:
"english"
,
    }}}
# restful
analyzerParams=
'{
  "tokenizer": "standard",
  "filter": [
    {
      "type": "stemmer",
      "language": "english"
    }
  ]
}'
验证使用
run_analyzer
Compatible with Milvus 2.5.11+
Python
Java
NodeJS
Go
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
"running runs looked ran runner"
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
"running runs looked ran runner"
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
"running runs looked ran runner"
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
not support yet
预期输出
[
'run'
,
'run'
,
'look'
,
'ran'
,
'runner'
]