Lindera
lindera
tokenizer 可进行基于词典的形态分析。它专为日语和韩语设计，在这两种语言中，单词不以空格分隔，语法标记（微粒）直接附加在单词上。
适用于中文文本
：虽然
lindera
通过
cc-cedict
词典支持中文，但我们建议使用
jieba
tokenizer 代替。Jieba 专为中文分词而设计，能提供更好的效果。
概述
日语和韩语是聚合语言：语法标记（称为微粒）直接附着在名词上，形成许多组合。例如
语言
词根
+ 词缀
= 组合形式
意义
韩语
首尔
首尔
首尔
在首尔
日本
東京（東京）
に
东京に
前往东京
lindera
tokenizer：
将文本分割
为单个词素（单词和微粒）
用词典中的语音部分 (POS) 信息
标记每个标记符
应用过滤器
去除不需要的标记符（如微粒、标点符号等）
这个两阶段的过程--先进行分词，再进行基于 POS 的过滤--可以精确控制哪些标记符被编入索引以进行搜索。
前提条件
Milvus 2.6 以上用户
：您可以跳过本节。所有词典都已预编译并包含在正式版本中。
对于 Milvus 2.5.x，您需要在启用特定词典的情况下编译 Milvus。编译时必须明确包含所有词典。
要启用特定词典，请在编译命令中包含这些词典：
make milvus TANTIVY_FEATURES=lindera-ipadic,lindera-ko-dic
可用词典的完整列表：
词典
语言
语言
lindera-ko-dic
韩语
韩语形态词典
（MeCab Ko-dic）
lindera-ipadic
日语
标准形态词典
（MeCab IPADIC）
lindera-ipadic-neologd
日语
包含新词和专有名词的扩展词典
（IPADIC NEologd）
lindera-unidic
日语
学术标准词典
(UniDic
)
lindera-cc-cedict
日语
社区维护的汉英词典
(CC-CEDICT
)
例如，启用所有词典：
make milvus TANTIVY_FEATURES=lindera-ipadic,lindera-ipadic-neologd,lindera-unidic,lindera-ko-dic,lindera-cc-cedict
配置
要配置使用
lindera
标记符号生成器的分析器，请将
tokenizer.type
设置为
lindera
，选择
dict_kind
的字典，并可选择应用过滤器。
Python
Java
Go
NodeJS
cURL
analyzer_params = {
"tokenizer"
: {
"type"
:
"lindera"
,
"dict_kind"
:
"ko-dic"
,
"filter"
: [
            {
"kind"
:
"korean_stop_tags"
,
"tags"
: [
"SP"
,
"SSC"
,
"SSO"
,
"SC"
,
"SE"
,
"SF"
,
"JKS"
,
"JKC"
,
"JKG"
,
"JKO"
,
"JKB"
,
"JKV"
,
"JKQ"
,
"JX"
,
"JC"
,
"UNK"
,
"EP"
,
"ETM"
]
            }
        ]
    }
}
Map<String, Object> analyzerParams =
new
HashMap
<>();                                 
  analyzerParams.put(
"tokenizer"
,
new
HashMap
<String, Object>() {{
      put(
"type"
,
"lindera"
);                                                           
      put(
"dict_kind"
,
"ko-dic"
);                                 
      put(
"filter"
, Arrays.asList(
new
HashMap
<String, Object>() {{
              put(
"kind"
,
"korean_stop_tags"
);
              put(
"tags"
, Arrays.asList(
"SP"
,
"SSC"
,
"SSO"
,
"SC"
,
"SE"
,
"SF"
,
"JKS"
,
"JKC"
,
"JKG"
,
"JKO"
,
"JKB"
,
"JKV"
,
"JKQ"
,
"JX"
,
"JC"
,
"UNK"
,
"EP"
,
"ETM"
));
          }}
      ));
  }});
analyzerParams :=
map
[
string
]
interface
{}{
"tokenizer"
:
map
[
string
]
interface
{}{
"type"
:
"lindera"
,
"dict_kind"
:
"ko-dic"
,
"filter"
: []
interface
{}{
map
[
string
]
interface
{}{
"kind"
:
"korean_stop_tags"
,
"tags"
: []
string
{
"SP"
,
"SSC"
,
"SSO"
,
"SC"
,
"SE"
,
"SF"
,
"JKS"
,
"JKC"
,
"JKG"
,
"JKO"
,
"JKB"
,
"JKV"
,
"JKQ"
,
"JX"
,
"JC"
,
"UNK"
,
"EP"
,
"ETM"
,
                  },
              },
          },
      },
  }
const
analyzer_params = {
"tokenizer"
: {
"type"
:
"lindera"
,
"dict_kind"
:
"ko-dic"
,
"filter"
: [
            {
"kind"
:
"korean_stop_tags"
,
"tags"
: [
"SP"
,
"SSC"
,
"SSO"
,
"SC"
,
"SE"
,
"SF"
,
"JKS"
,
"JKC"
,
"JKG"
,
"JKO"
,
"JKB"
,
"JKV"
,
"JKQ"
,
"JX"
,
"JC"
,
"UNK"
,
"EP"
,
"ETM"
]
            }
        ]
    }
};
# restful
参数
参数
type
标记符类型。固定为
"lindera"
。
dict_kind
用于定义词汇的字典。可能的值：
ko-dic
:韩语 - 韩语形态词典
（MeCab Ko-dic）
ipadic
:日语 - 标准形态词典
(MeCab IPADIC
)
ipadic-neologd
:日语新词词典（扩展）- 包括新词和专有名词
(IPADIC NEologd
)
unidic
:日语 UniDic（扩展）- 包含详细语言信息的学术标准词典
(UniDic
)
cc-cedict
:中文普通话（繁体/简体） - 社区维护的汉英词典
(CC-CEDICT
)
filter
在分段后应用的标记符号级过滤器列表。每个过滤器都是一个对象，具有
kind
:过滤器类型。支持的值：
korean_stop_tags
:移除与指定的韩国 POS 标记相匹配的标记。
japanese_stop_tags
:移除与指定日语 POS 标记匹配的词组。
tags
:要过滤掉的 POS 标记列表。可用标记取决于
kind
：
对于
korean_stop_tags
：使用精确的标记代码（如
JKS
,
JKO
,
SF
）。韩语标记需要精确匹配。有关基于世宗标记集的完整列表，请参阅
Lindera Korean stop tags source
。
对于
japanese_stop_tags
：使用精确的标记代码（如
助詞,格助詞
,
助詞,係助詞
,
助動詞
）。日语标记需要精确匹配。有关完整列表 (IPADIC)，请参阅
日语 POS 标记参考
。
定义
analyzer_params
后，可以在定义 Collections Schema 时将它们应用到
VARCHAR
字段。这样，Milvus 就能使用指定的分析器处理该字段中的文本，以实现高效的标记化和过滤。有关详情，请参阅
示例使用
。
示例
在将分析器配置应用到 Collections 模式之前，请使用
run_analyzer
方法验证其行为。
韩语示例
Python
Java
Go
NodeJS
cURL
from
pymilvus
import
MilvusClient

client = MilvusClient(uri=
"http://localhost:19530"
)

analyzer_params = {
"tokenizer"
: {
"type"
:
"lindera"
,
"dict_kind"
:
"ko-dic"
,
"filter"
: [
            {
"kind"
:
"korean_stop_tags"
,
"tags"
: [
"SP"
,
"SSC"
,
"SSO"
,
"SC"
,
"SE"
,
"SF"
,
"JKS"
,
"JKC"
,
"JKG"
,
"JKO"
,
"JKB"
,
"JKV"
,
"JKQ"
,
"JX"
,
"JC"
,
"UNK"
,
"EP"
,
"ETM"
]
            }
        ]
    }
}
# Sample Korean text: "서울에서 맛있는 음식을 먹었습니다" (I ate delicious food in Seoul)
sample_text =
"서울에서 맛있는 음식을 먹었습니다"
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

Map<String, Object> analyzerParams =
new
HashMap
<>();                                                                          
analyzerParams.put(
"tokenizer"
,
new
HashMap
<String, Object>() {{
  put(
"type"
,
"lindera"
);                                                                                                    
  put(
"dict_kind"
,
"ko-dic"
);                                 
  put(
"filter"
, Arrays.asList(
new
HashMap
<String, Object>() {{
          put(
"kind"
,
"korean_stop_tags"
);
          put(
"tags"
, Arrays.asList(
"SP"
,
"SSC"
,
"SSO"
,
"SC"
,
"SE"
,
"SF"
,
"JKS"
,
"JKC"
,
"JKG"
,
"JKO"
,
"JKB"
,
"JKV"
,
"JKQ"
,
"JX"
,
"JC"
,
"UNK"
,
"EP"
,
"ETM"
));
      }}
  ));
}});

List<String> texts =
new
ArrayList
<>();
texts.add(
"서울에서 맛있는 음식을 먹었습니다"
);
RunAnalyzerResp
resp
=
client.runAnalyzer(RunAnalyzerReq.builder()
        .texts(texts)
        .analyzerParams(analyzerParams)
        .build());
List<RunAnalyzerResp.AnalyzerResult> results = resp.getResults();
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

analyzerParams :=
map
[
string
]
interface
{}{
"tokenizer"
:
map
[
string
]
interface
{}{
"type"
:
"lindera"
,
"dict_kind"
:
"ko-dic"
,
"filter"
: []
interface
{}{
map
[
string
]
interface
{}{
"kind"
:
"korean_stop_tags"
,
"tags"
: []
string
{
"SP"
,
"SSC"
,
"SSO"
,
"SC"
,
"SE"
,
"SF"
,
"JKS"
,
"JKC"
,
"JKG"
,
"JKO"
,
"JKB"
,
"JKV"
,
"JKQ"
,
"JX"
,
"JC"
,
"UNK"
,
"EP"
,
"ETM"
,
              },
          },
      },
  },
}

bs, _ := json.Marshal(analyzerParams)
texts := []
string
{
"서울에서 맛있는 음식을 먹었습니다"
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
import
{
MilvusClient
}
from
"@zilliz/milvus2-sdk-node"
;
const
client =
new
MilvusClient
({
uri
:
"http://localhost:19530"
,
});
const
analyzer_params = {
tokenizer
: {
type
:
"lindera"
,
dict_kind
:
"ko-dic"
,
filter
: [
      {
kind
:
"korean_stop_tags"
,
tags
: [
"SP"
,
"SSC"
,
"SSO"
,
"SC"
,
"SE"
,
"SF"
,
"JKS"
,
"JKC"
,
"JKG"
,
"JKO"
,
"JKB"
,
"JKV"
,
"JKQ"
,
"JX"
,
"JC"
,
"UNK"
,
"EP"
,
"ETM"
,
        ],
      },
    ],
  },
};
const
sample_text =
"서울에서 맛있는 음식을 먹었습니다"
;
const
result =
await
client.
run_analyzer
(sample_text, analyzer_params);
console
.
log
(
"Analyzer output:"
, result);
# restful
预期输出
：
['서울', '맛있', '음식', '먹', '습니다']
如果没有
korean_stop_tags
，输出将包括
에서
(in)、
는
(主题标记) 和
을
(对象标记) 等微粒，这些微粒通常对搜索无用。
日语示例
Python
Java
Go
NodeJS
cURL
from
pymilvus
import
MilvusClient

client = MilvusClient(uri=
"http://localhost:19530"
)

analyzer_params = {
"tokenizer"
: {
"type"
:
"lindera"
,
"dict_kind"
:
"ipadic"
,
"filter"
: [
            {
"kind"
:
"japanese_stop_tags"
,
"tags"
: [
"接続詞"
,
"助詞,格助詞"
,
"助詞,格助詞,一般"
,
"助詞,格助詞,引用"
,
"助詞,格助詞,連語"
,
"助詞,係助詞"
,
"助詞,終助詞"
,
"助詞,接続助詞"
,
"助詞,特殊"
,
"助詞,副助詞"
,
"助詞,副助詞／並立助詞／終助詞"
,
"助詞,連体化"
,
"助詞,副詞化"
,
"助詞,並立助詞"
,
"助動詞"
,
"記号,一般"
,
"記号,読点"
,
"記号,句点"
,
"記号,空白"
,
"記号,括弧閉"
,
"記号,括弧開"
,
"その他,間投"
,
"フィラー"
,
"非言語音"
]
            }
        ]
    }
}
# Sample Japanese text: "東京スカイツリーの最寄り駅はとうきょうスカイツリー駅です"
sample_text =
"東京スカイツリーの最寄り駅はとうきょうスカイツリー駅です"
result = client.run_analyzer(sample_text, analyzer_params)
print
(
"Analyzer output:"
, result)
// java
// go
import
{
MilvusClient
}
from
"@zilliz/milvus2-sdk-node"
;
const
client =
new
MilvusClient
({
uri
:
"http://localhost:19530"
,
});
const
analyzer_params = {
"tokenizer"
: {
"type"
:
"lindera"
,
"dict_kind"
:
"ipadic"
,
"filter"
: [
            {
"kind"
:
"japanese_stop_tags"
,
"tags"
: [
"接続詞"
,
"助詞,格助詞"
,
"助詞,格助詞,一般"
,
"助詞,格助詞,引用"
,
"助詞,格助詞,連語"
,
"助詞,係助詞"
,
"助詞,終助詞"
,
"助詞,接続助詞"
,
"助詞,特殊"
,
"助詞,副助詞"
,
"助詞,副助詞／並立助詞／終助詞"
,
"助詞,連体化"
,
"助詞,副詞化"
,
"助詞,並立助詞"
,
"助動詞"
,
"記号,一般"
,
"記号,読点"
,
"記号,句点"
,
"記号,空白"
,
"記号,括弧閉"
,
"記号,括弧開"
,
"その他,間投"
,
"フィラー"
,
"非言語音"
]
            }
        ]
    }
}
// Sample Japanese text: "東京スカイツリーの最寄り駅はとうきょうスカイツリー駅です"
const
sample_text =
"東京スカイツリーの最寄り駅はとうきょうスカイツリー駅です"
const
result =
await
client.
run_analyzer
(sample_text, analyzer_params);
console
.
log
(
"Analyzer output:"
, result);
# restful
预期输出：
['東京', 'スカイ', 'ツリー', '最寄り駅', 'とう', 'きょう', 'スカイ', 'ツリー', '駅']
如果没有
japanese_stop_tags
，输出将包括
の
（所有格）、
は
（主题标记）和
です
（共轭词）等语素。