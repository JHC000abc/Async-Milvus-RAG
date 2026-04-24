正则表达式
Compatible with Milvus 2.5.11+
regex
过滤器是一种正则表达式过滤器：令牌生成器生成的任何令牌只有在与您提供的表达式匹配时才会被保留，否则都会被丢弃。
配置
regex
过滤器是 Milvus 的自定义过滤器。要使用它，请在过滤器配置中指定
"type": "regex"
，并使用
expr
参数指定所需的正则表达式。
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
: [{
"type"
:
"regex"
,
"expr"
:
"^(?!test)"
# keep tokens that do NOT start with "test"
}]
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
        Arrays.asList(
new
HashMap
<String, Object>() {{
                    put(
"type"
,
"regex"
);
                    put(
"expr"
,
"^(?!test)"
);
                }})
);
// node
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
"regex"
,
"expr"
:
"^(?!test)"
,
        }}}
# curl
regex
过滤器接受以下可配置参数。
参数
参数
expr
应用于每个标记的正则表达式模式。有关 regex
语法
的详情，请参阅语法。
regex
过滤器对标记符号生成器生成的术语进行操作，因此必须与标记符号生成器结合使用。
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
明文
Java
NodeJS
Go
cURL
analyzer_params = {
    "tokenizer": "standard",
    "filter": [{
        "type": "regex",
        "expr": "^(?!test)"
    }]
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
"regex"
);
            put(
"expr"
,
"^(?!test)"
);
        }}));
// node
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
"regex"
,
"expr"
:
"^(?!test)"
,
        }}}
# curl
使用
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
"testItem apple testCase banana"
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
"testItem apple testCase banana"
);
RunAnalyzerResp
resp
=
client.runAnalyzer(RunAnalyzerReq.builder()
        .texts(texts)
        .analyzerParams(analyzerParams)
        .build());
List<RunAnalyzerResp.AnalyzerResult> results = resp.getResults();
// node
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
"testItem apple testCase banana"
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
# curl
预期输出
[
'apple'
,
'banana'
]