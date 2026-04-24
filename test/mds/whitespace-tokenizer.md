空格
只要单词之间有空格，
whitespace
标记符号器就会将文本划分为术语。
配置
要配置使用
whitespace
标记符号生成器的分析器，请在
analyzer_params
中将
tokenizer
设置为
whitespace
。
Python
Java
NodeJS
Go
cURL
analyzer_params = {
"tokenizer"
:
"whitespace"
,
}
Map<String, Object> analyzerParams =
new
HashMap
<>();
analyzerParams.put(
"tokenizer"
,
"whitespace"
);
const
analyzer_params = {
"tokenizer"
:
"whitespace"
};
analyzerParams =
map
[
string
]any{
"tokenizer"
:
"whitespace"
}
# restful
analyzerParams=
'{
  "tokenizer": "whitespace"
}'
空白标记符可以与一个或多个过滤器结合使用。例如，下面的代码定义了一个使用
whitespace
标记符和
lowercase
过滤器
的分析器：
Python
Java
NodeJS
Go
cURL
analyzer_params = {
"tokenizer"
:
"whitespace"
,
"filter"
: [
"lowercase"
]
}
Map<String, Object> analyzerParams =
new
HashMap
<>();
analyzerParams.put(
"tokenizer"
,
"whitespace"
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
"whitespace"
,
"filter"
: [
"lowercase"
]
};
analyzerParams =
map
[
string
]any{
"tokenizer"
:
"whitespace"
,
"filter"
: []any{
"lowercase"
}}
# restful
analyzerParams=
'{
  "tokenizer": "whitespace",
  "filter": [
    "lowercase"
  ]
}'
定义
analyzer_params
后，可以在定义 Collections Schema 时将它们应用到
VARCHAR
字段。这样，Milvus 就能使用指定的分析器对该字段中的文本进行处理，从而实现高效的标记化和过滤。有关详情，请参阅
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
"whitespace"
,
"filter"
: [
"lowercase"
]
}
Map<String, Object> analyzerParams =
new
HashMap
<>();
analyzerParams.put(
"tokenizer"
,
"whitespace"
);
analyzerParams.put(
"filter"
, Collections.singletonList(
"lowercase"
));
// javascript
analyzerParams =
map
[
string
]any{
"tokenizer"
:
"whitespace"
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
"The Milvus vector database is built for scale!"
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
"The Milvus vector database is built for scale!"
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
"The Milvus vector database is built for scale!"
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
['the', 'milvus', 'vector', 'database', 'is', 'built', 'for', 'scale!']