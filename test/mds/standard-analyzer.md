标准分析器
standard
分析器是 Milvus 的默认分析器，如果没有指定分析器，它将自动应用于文本字段。它使用基于语法的标记化，对大多数语言都很有效。
standard
分析器适用于依赖分隔符（如空格、标点符号）作为单词边界的语言。但是，中文、日文和韩文等语言需要基于词典的标记化。在这种情况下，使用特定语言的分析器，如
chinese
或带有专门标记符号化器的自定义分析器（如
lindera
,
icu
）和过滤器，以确保准确的标记化和更好的搜索结果。
定义
standard
分析器包括
标记化器
：使用
standard
标记符号化器，根据语法规则将文本分割成离散的单词单元。更多信息，请参阅
标准标记符
。
过滤器
：使用
lowercase
过滤器将所有标记转换为小写，从而实现不区分大小写的搜索。更多信息，请参阅
小写
。
standard
分析器的功能相当于以下自定义分析器配置：
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
analyzerParams=
'{
  "tokenizer": "standard",
  "filter": [
    "lowercase"
  ]
}'
配置
要将
standard
分析器应用到一个字段，只需在
analyzer_params
中将
type
设置为
standard
，并根据需要加入可选参数即可。
Python
Java
NodeJS
Go
cURL
analyzer_params = {
"type"
:
"standard"
,
# Specifies the standard analyzer type
}
Map<String, Object> analyzerParams =
new
HashMap
<>();
analyzerParams.put(
"type"
,
"standard"
);
const
analyzer_params = {
"type"
:
"standard"
,
// Specifies the standard analyzer type
}
analyzerParams =
map
[
string
]any{
"type"
:
"standard"
}
# restful
analyzerParams=
'{
  "type": "standard"
}'
standard
分析器接受以下可选参数：
参数
说明
stop_words
一个数组，包含将从标记化中删除的停用词列表。默认为
_english_
，这是一组内置的常用英语停止词。
自定义停止词配置示例：
Python
Java
NodeJS
Go
cURL
analyzer_params = {
"type"
:
"standard"
,
# Specifies the standard analyzer type
"stop_words"
, [
"of"
]
# Optional: List of words to exclude from tokenization
}
Map<String, Object> analyzerParams =
new
HashMap
<>();
analyzerParams.put(
"type"
,
"standard"
);
analyzerParams.put(
"stop_words"
, Collections.singletonList(
"of"
));
analyzer_params = {
"type"
:
"standard"
,
// Specifies the standard analyzer type
"stop_words"
, [
"of"
]
// Optional: List of words to exclude from tokenization
}
analyzerParams =
map
[
string
]any{
"type"
:
"standard"
,
"stop_words"
: []
string
{
"of"
}}
# restful
定义
analyzer_params
后，您可以在定义 Collections Schema 时将其应用到
VARCHAR
字段。这样，Milvus 就能使用指定的分析器处理该字段中的文本，从而实现高效的标记化和过滤。有关详细信息，请参阅
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
"type"
:
"standard"
,
# Standard analyzer configuration
"stop_words"
: [
"for"
]
# Optional: Custom stop words parameter
}
Map<String, Object> analyzerParams =
new
HashMap
<>();
analyzerParams.put(
"type"
,
"standard"
);
analyzerParams.put(
"stop_words"
, Collections.singletonList(
"for"
));
// javascript
analyzerParams =
map
[
string
]any{
"type"
:
"standard"
,
"stop_words"
: []
string
{
"for"
}}
# restful
analyzerParams=
'{
  "type": "standard",
  "stop_words": [
    "of"
  ]
}'
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
Standard analyzer output: ['the', 'milvus', 'vector', 'database', 'is', 'built', 'scale']