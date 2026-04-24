中文
chinese
分析器专为处理中文文本而设计，提供有效的分段和标记化功能。
定义
chinese
分析器包括
标记化器
：使用
jieba
标记化器，根据词汇和上下文将中文文本分割成标记。更多信息，请参阅
Jieba
。
过滤器
：使用
cnalphanumonly
过滤器删除包含任何非汉字的标记。更多信息，请参阅
Cnalphanumonly
。
chinese
分析器的功能相当于以下自定义分析器配置：
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
]
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
]
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
配置
要将
chinese
分析器应用到一个字段，只需在
analyzer_params
中将
type
设置为
chinese
即可。
Python
Java
NodeJS
Go
cURL
analyzer_params = {
"type"
:
"chinese"
,
}
Map<String, Object> analyzerParams =
new
HashMap
<>();
analyzerParams.put(
"type"
,
"chinese"
);
const
analyzer_params = {
"type"
:
"chinese"
,
}
analyzerParams =
map
[
string
]any{
"type"
:
"chinese"
}
# restful
analyzerParams=
'{
  "type": "chinese"
}'
chinese
分析器不接受任何可选参数。
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
"chinese"
,
}
Map<String, Object> analyzerParams =
new
HashMap
<>();
analyzerParams.put(
"type"
,
"chinese"
);
// javascript
analyzerParams =
map
[
string
]any{
"type"
:
"chinese"
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

client = MilvusClient(uri=
"http://localhost:19530"
)
# Sample text to analyze
sample_text =
"Milvus 是一个高性能、可扩展的向量数据库！"
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
"Milvus 是一个高性能、可扩展的向量数据库！"
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
"Milvus 是一个高性能、可扩展的向量数据库！"
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
Chinese analyzer output: [
'Milvus'
,
'是'
,
'一个'
,
'高性'
,
'性能'
,
'高性能'
,
'可'
,
'扩展'
,
'的'
,
'向量'
,
'数据'
,
'据库'
,
'数据库'
]