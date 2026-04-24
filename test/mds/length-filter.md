长度
length
过滤器可移除不符合指定长度要求的标记，让您可以控制文本处理过程中保留的标记长度。
配置
length
过滤器是 Milvus 中的自定义过滤器，通过在过滤器配置中设置
"type": "length"
来指定。您可以在
analyzer_params
中将其配置为字典，以定义长度限制。
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
"length"
,
# Specifies the filter type as length
"max"
:
10
,
# Sets the maximum token length to 10 characters
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
"length"
);
            put(
"max"
,
10
);
        }}));
cosnt analyzer_params = {
"tokenizer"
:
"standard"
,
"filter"
:[{
"type"
:
"length"
, #
Specifies
the filter type
as
length
"max"
:
10
, #
Sets
the maximum token length to
10
characters
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
"length"
,
"max"
:
10
,
    }}}
# restful
analyzerParams=
'{
  "tokenizer": "standard",
  "filter": [
    {
      "type": "length",
      "max": 10
    }
  ]
}'
length
过滤器接受以下可配置参数。
参数
说明
max
设置最大标记长度。超过此长度的标记将被删除。
length
过滤器对标记符生成器生成的术语进行操作，因此必须与标记符结合使用。有关 Milvus 中可用的标记符列表，请参阅
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
"length"
,
# Specifies the filter type as length
"max"
:
10
,
# Sets the maximum token length to 10 characters
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
"length"
);
            put(
"max"
,
10
);
        }}));
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
"length"
,
"max"
:
10
,
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
"The length filter allows control over token length requirements for text processing."
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
"The length filter allows control over token length requirements for text processing."
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
"The length filter allows control over token length requirements for text processing."
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
'length'
,
'filter'
,
'allows'
,
'control'
,
'over'
,
'token'
,
'length'
,
'for'
,
'text'
,
'processing'
]