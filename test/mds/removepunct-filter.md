移除标点符号
Compatible with Milvus 2.5.11+
removepunct
过滤器可从标记流中移除独立的标点符号标记。当您需要更简洁的文本处理时，可以使用该过滤器，重点处理有意义的内容词而不是标点符号。
该过滤器对
jieba
、
lindera
和
icu
标记符号化器最有效，它们将标点符号保留为单独的标记符号（如
"Hello!"
→
["Hello", "!"]
）。其他标记符号化器，如
standard
和
whitespace
会在标记符号化过程中丢弃标点符号，因此
removepunct
对它们没有影响。
配置
removepunct
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
"jieba"
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
"jieba"
,
"filter"
: []any{
"removepunct"
}}
# restful
removepunct
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
['Привет', 'Как', 'дела']