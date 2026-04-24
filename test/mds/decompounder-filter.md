分词器
decompounder
过滤器可根据指定词典将复合词拆分成单个成分，从而更方便地搜索复合词的各个部分。该过滤器对德语等经常使用复合词的语言尤其有用。
配置
decompounder
过滤器是 Milvus 的自定义过滤器。要使用它，请在过滤器配置中指定
"type": "decompounder"
，同时指定
word_list
参数，该参数提供了要识别的单词成分字典。
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
"decompounder"
,
# Specifies the filter type as decompounder
"word_list"
: [
"dampf"
,
"schiff"
,
"fahrt"
,
"brot"
,
"backen"
,
"automat"
],
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
"decompounder"
);
                    put(
"word_list"
, Arrays.asList(
"dampf"
,
"schiff"
,
"fahrt"
,
"brot"
,
"backen"
,
"automat"
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
"decompounder"
,
// Specifies the filter type as decompounder
"word_list"
: [
"dampf"
,
"schiff"
,
"fahrt"
,
"brot"
,
"backen"
,
"automat"
],
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
"decompounder"
,
"word_list"
: []
string
{
"dampf"
,
"schiff"
,
"fahrt"
,
"brot"
,
"backen"
,
"automat"
},
    }}}
# restful
analyzerParams=
'{
  "tokenizer": "standard",
  "filter": [
    {
      "type": "decompounder",
      "word_list": [
        "dampf",
        "schiff",
        "fahrt",
        "brot",
        "backen",
        "automat"
      ]
    }
  ]
}'
decompounder
过滤器接受以下可配置参数。
参数
说明
word_list
用于拆分复合词的单词成分列表。该字典决定了如何将复合词分解为单个术语。
decompounder
过滤器对标记化器生成的术语进行操作，因此必须与标记化器结合使用。有关 Milvus 中可用的标记化器列表，请参阅
标准
标记化器及其同类页面。
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
"decompounder"
,
# Specifies the filter type as decompounder
"word_list"
: [
"dampf"
,
"schiff"
,
"fahrt"
,
"brot"
,
"backen"
,
"automat"
],
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
"decompounder"
);
                    put(
"word_list"
, Arrays.asList(
"dampf"
,
"schiff"
,
"fahrt"
,
"brot"
,
"backen"
,
"automat"
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
"decompounder"
,
"word_list"
: []
string
{
"dampf"
,
"schiff"
,
"fahrt"
,
"brot"
,
"backen"
,
"automat"
},
    }}}
# restful
analyzerParams=
'{
  "tokenizer": "standard",
  "filter": [
    {
      "type": "decompounder",
      "word_list": [
        "dampf",
        "schiff",
        "fahrt",
        "brot",
        "backen",
        "automat"
      ]
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
"dampfschifffahrt brotbackautomat"
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
"dampfschifffahrt brotbackautomat"
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
"dampfschifffahrt brotbackautomat"
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
'dampf'
,
'schiff'
,
'fahrt'
,
'brotbackautomat'
]