标准标记符
Milvus 中的
standard
令牌分割器根据空格和标点符号分割文本，适用于大多数语言。
配置
要配置使用
standard
令牌转换器的分析器，请在
analyzer_params
中将
tokenizer
设置为
standard
。
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
const
analyzer_params = {
"tokenizer"
:
"standard"
,
};
analyzerParams =
map
[
string
]any{
"tokenizer"
:
"standard"
}
# restful
analyzerParams=
'{
  "tokenizer": "standard"
}'
standard
标记符号分析器可与一个或多个过滤器结合使用。例如，以下代码定义了一个使用
standard
标记器和
lowercase
过滤器的分析器：
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
]
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
为了简化设置，您可以选择使用
standard
分析器
，它将
standard
标记符和
lowercase
过滤器
。
定义
analyzer_params
后，可以在定义 Collections Schema 时将其应用到
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
"standard"
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
"standard"
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
"standard"
,
"filter"
: []any{
"lowercase"
}}
# restful
验证使用
run_analyzer
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
"The Milvus vector database is built for scale!"
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
['the', 'milvus', 'vector', 'database', 'is', 'built', 'for', 'scale']