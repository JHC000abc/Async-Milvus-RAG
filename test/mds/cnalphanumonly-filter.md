Cnalphanumonly
cnalphanumonly
过滤器会删除包含除汉字、英文字母或数字以外的任何字符的标记。
配置
cnalphanumonly
过滤器内置于 Milvus 中。要使用它，只需在
analyzer_params
中的
filter
部分指定其名称即可。
Python
Java
NodeJS
Go
cURL
analyzer_params = {
"tokenizer"
:
"jieba"
,
"filter"
: [
"cnalphanumonly"
],
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
analyzerParams.put(
"filter"
, Collections.singletonList(
"cnalphanumonly"
));
const
analyzer_params = {
"tokenizer"
:
"jieba"
,
"filter"
: [
"cnalphanumonly"
],
};
analyzerParams =
map
[
string
]any{
"tokenizer"
:
"jieba"
,
"filter"
: []any{
"cnalphanumonly"
}}
# restful
analyzerParams=
'{
  "tokenizer": "jieba",
  "filter": [
    "cnalphanumonly"
  ]
}'
cnalphanumonly
过滤器对标记符生成的术语进行操作，因此必须与标记符结合使用。有关 Milvus 中可用的标记化器列表，请参阅
Jieba
及其同类页面。
定义
analyzer_params
后，可以在定义 Collections Schema 时将其应用到
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
"tokenizer"
:
"jieba"
,
"filter"
: [
"cnalphanumonly"
],
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
analyzerParams.put(
"filter"
, Collections.singletonList(
"cnalphanumonly"
));
// javascript
analyzerParams =
map
[
string
]any{
"tokenizer"
:
"jieba"
,
"filter"
: []any{
"cnalphanumonly"
}}
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
"Milvus 是 LF AI & Data Foundation 下的一个开源项目，以 Apache 2.0 许可发布。"
# Run the jieba tokenizer with the defined configuration
result = client.run_analyzer(sample_text, analyzer_params)
print
(
"Analyzer output:"
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
"Milvus 是 LF AI & Data Foundation 下的一个开源项目，以 Apache 2.0 许可发布。"
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
"Milvus 是 LF AI & Data Foundation 下的一个开源项目，以 Apache 2.0 许可发布。"
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
'Milvus'
,
'是'
,
'LF'
,
'AI'
,
'Data'
,
'Foundation'
,
'下的一个开源项目'
,
'以'
,
'Apache'
,
'2'
,
'0'
,
'许可发布'
]