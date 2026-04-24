小写
lowercase
过滤器将标记符号生成器生成的术语转换为小写，使搜索不区分大小写。例如，它可以将
["High", "Performance", "Vector", "Database"]
转换为
["high", "performance", "vector", "database"]
。
配置
lowercase
过滤器内置于 Milvus。要使用它，只需在
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
"standard"
,
"filter"
: [
"lowercase"
],
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
, Collections.singletonList(
"lowercase"
));
const
analyzer_params = {
"tokenizer"
:
"standard"
,
"filter"
: [
"lowercase"
],
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
"lowercase"
}}
# restful
analyzerParams=
'{
  "tokenizer": "standard",
  "filter": [
    "lowercase"
  ]
}'
lowercase
过滤器对标记符生成的术语进行操作，因此必须与标记符结合使用。
定义
analyzer_params
后，您可以在定义 Collections Schema 时将其应用到
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
: [
"lowercase"
],
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
, Collections.singletonList(
"lowercase"
));
// javascript
analyzerParams :=
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
"The Lowercase Filter Ensures Uniformity In Text Processing."
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
"The Lowercase Filter Ensures Uniformity In Text Processing."
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
"The Lowercase Filter Ensures Uniformity In Text Processing."
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
'the'
,
'lowercase'
,
'filter'
,
'ensures'
,
'uniformity'
,
'in'
,
'text'
,
'processing'
]