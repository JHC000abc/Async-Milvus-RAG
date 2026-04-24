ICU
Compatible with Milvus 2.5.11+
icu
tokenizer 基于
Unicode 国际化组件
（ICU）开源项目构建，该项目为软件国际化提供了关键工具。通过使用 ICU 的分词算法，令牌转换器可以准确地将世界上大多数语言的文本分割成单词。
icu
标记符号转换器会在输出中保留标点符号和空格作为单独的标记符号。例如，
"Привет! Как дела?"
变成
["Привет", "!", " ", "Как", " ", "дела", "?"]
。要删除这些独立的标点符号，请使用
removepunct
过滤器。
配置
要配置使用
icu
令牌转换器的分析器，请在
analyzer_params
中将
tokenizer
设置为
icu
。
Python
Java
NodeJS
Go
cURL
analyzer_params = {
"tokenizer"
:
"icu"
,
}
Map<String, Object> analyzerParams =
new
HashMap
<>();
analyzerParams.put(
"tokenizer"
,
"icu"
);
// node
analyzerParams =
map
[
string
]any{
"tokenizer"
:
"icu"
}
# curl
icu
令牌分析器可与一个或多个过滤器结合使用。例如，下面的代码定义了一个使用
icu
标记器和
移除标点过滤器
的分析器：
Python
Java
NodeJS
Go
cURL
analyzer_params = {
"tokenizer"
:
"icu"
,
"filter"
: [
"removepunct"
]
}
Map<String, Object> analyzerParams =
new
HashMap
<>();
analyzerParams.put(
"tokenizer"
,
"icu"
);
analyzerParams.put(
"filter"
, Collections.singletonList(
"removepunct"
));
// node
analyzerParams =
map
[
string
]any{
"tokenizer"
:
"icu"
,
"filter"
: []
string
{
"removepunct"
}}
# curl
定义
analyzer_params
后，您可以在定义 Collections Schema 时将它们应用到
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
"icu"
,
}
Map<String, Object> analyzerParams =
new
HashMap
<>();
analyzerParams.put(
"tokenizer"
,
"icu"
);
// node
analyzerParams =
map
[
string
]any{
"tokenizer"
:
"icu"
}
# curl
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

client = MilvusClient(uri=
"http://localhost:19530"
)
# Sample text to analyze
sample_text =
"Привет! Как дела?"
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
"Привет! Как дела?"
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
"Привет! Как дела?"
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
['Привет', '!', ' ', 'Как', ' ', 'дела', '?']