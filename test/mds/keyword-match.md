文本匹配
Milvus 的文本匹配功能可根据特定术语精确检索文档。该功能主要用于满足特定条件的过滤搜索，并可结合标量过滤功能来细化查询结果，允许在符合标量标准的向量内进行相似性搜索。
文本匹配侧重于查找查询术语的精确出现，而不对匹配文档的相关性进行评分。如果您想根据查询词的语义和重要性检索最相关的文档，我们建议您使用
全文搜索
。
概述
Milvus 整合了
Tantivy
来支持其底层的倒排索引和基于术语的文本搜索。对于每个文本条目，Milvus 都会按照以下程序建立索引：
分析器
：分析器将输入文本标记化为单个词或标记，然后根据需要应用过滤器。这样，Milvus 就能根据这些标记建立索引。
编制索引
：文本分析完成后，Milvus 会创建一个倒排索引，将每个独特的标记映射到包含该标记的文档。
当用户进行文本匹配时，倒排索引可用于快速检索包含该术语的所有文档。这比逐个扫描每个文档要快得多。
关键词匹配
启用文本匹配
文本匹配对
VARCHAR
字段类型，它在 Milvus 中本质上是字符串数据类型。要启用文本匹配，请将
enable_analyzer
和
enable_match
都设置为
True
，然后在定义 Collections Schema 时选择性地配置文本
分析的分析器
。
将
enable_analyzer
和
enable_match
要启用特定
VARCHAR
字段的文本匹配，请在定义字段 Schema 时将
enable_analyzer
和
enable_match
参数设置为
True
。这将指示 Milvus 对文本进行标记化处理，并为指定字段创建反向索引，从而实现快速高效的文本匹配。
Python
Java
Go
NodeJS
cURL
from
pymilvus
import
MilvusClient, DataType

schema = MilvusClient.create_schema(enable_dynamic_field=
False
)
schema.add_field(
    field_name=
"id"
,
    datatype=DataType.INT64,
    is_primary=
True
,
    auto_id=
True
)
schema.add_field(
    field_name=
'text'
, 
    datatype=DataType.VARCHAR, 
    max_length=
1000
, 
    enable_analyzer=
True
,
# Whether to enable text analysis for this field
enable_match=
True
# Whether to enable text match
)
schema.add_field(
    field_name=
"embeddings"
,
    datatype=DataType.FLOAT_VECTOR,
    dim=
5
)
import
io.milvus.v2.common.DataType;
import
io.milvus.v2.service.collection.request.AddFieldReq;
import
io.milvus.v2.service.collection.request.CreateCollectionReq;

CreateCollectionReq.
CollectionSchema
schema
=
CreateCollectionReq.CollectionSchema.builder()
        .enableDynamicField(
false
)
        .build();
schema.addField(AddFieldReq.builder()
        .fieldName(
"id"
)
        .dataType(DataType.Int64)
        .isPrimaryKey(
true
)
        .autoID(
true
)
        .build());
schema.addField(AddFieldReq.builder()
        .fieldName(
"text"
)
        .dataType(DataType.VarChar)
        .maxLength(
1000
)
        .enableAnalyzer(
true
)
        .enableMatch(
true
)
        .build());
schema.addField(AddFieldReq.builder()
        .fieldName(
"embeddings"
)
        .dataType(DataType.FloatVector)
        .dimension(
5
)
        .build());
import
"github.com/milvus-io/milvus/client/v2/entity"
schema := entity.NewSchema().WithDynamicFieldEnabled(
false
)
schema.WithField(entity.NewField().
    WithName(
"id"
).
    WithDataType(entity.FieldTypeInt64).
    WithIsPrimaryKey(
true
).
    WithIsAutoID(
true
),
).WithField(entity.NewField().
    WithName(
"text"
).
    WithDataType(entity.FieldTypeVarChar).
    WithEnableAnalyzer(
true
).
    WithEnableMatch(
true
).
    WithMaxLength(
1000
),
).WithField(entity.NewField().
    WithName(
"embeddings"
).
    WithDataType(entity.FieldTypeFloatVector).
    WithDim(
5
),
)
const
schema = [
  {
name
:
"id"
,
data_type
:
DataType
.
Int64
,
is_primary_key
:
true
,
  },
  {
name
:
"text"
,
data_type
:
"VarChar"
,
enable_analyzer
:
true
,
enable_match
:
true
,
max_length
:
1000
,
  },
  {
name
:
"embeddings"
,
data_type
:
DataType
.
FloatVector
,
dim
:
5
,
  },
];
export
schema=
'{
        "autoId": true,
        "enabledDynamicField": false,
        "fields": [
            {
                "fieldName": "id",
                "dataType": "Int64",
                "isPrimary": true
            },
            {
                "fieldName": "text",
                "dataType": "VarChar",
                "elementTypeParams": {
                    "max_length": 1000,
                    "enable_analyzer": true,
                    "enable_match": true
                }
            },
            {
                "fieldName": "embeddings",
                "dataType": "FloatVector",
                "elementTypeParams": {
                    "dim": "5"
                }
            }
        ]
    }'
可选：配置分析器
关键词匹配的性能和准确性取决于所选的分析器。不同的分析器适用于不同的语言和文本结构，因此选择正确的分析器会极大地影响特定用例的搜索结果。
默认情况下，Milvus 使用
standard
分析器，该分析器根据空白和标点符号对文本进行标记，删除长度超过 40 个字符的标记，并将文本转换为小写。应用此默认设置无需额外参数。更多信息，请参阅
标准
。
如果需要不同的分析器，可以使用
analyzer_params
参数进行配置。例如，应用
english
分析器处理英文文本：
Python
Java
Go
NodeJS
cURL
analyzer_params = {
"type"
:
"english"
}
schema.add_field(
    field_name=
'text'
,
    datatype=DataType.VARCHAR,
    max_length=
200
,
    enable_analyzer=
True
,
    analyzer_params = analyzer_params,
    enable_match =
True
,
)
Map<String, Object> analyzerParams =
new
HashMap
<>();
analyzerParams.put(
"type"
,
"english"
);
schema.addField(AddFieldReq.builder()
        .fieldName(
"text"
)
        .dataType(DataType.VarChar)
        .maxLength(
200
)
        .enableAnalyzer(
true
)
        .analyzerParams(analyzerParams)
        .enableMatch(
true
)
        .build());
analyzerParams :=
map
[
string
]any{
"type"
:
"english"
}
schema.WithField(entity.NewField().
    WithName(
"text"
).
    WithDataType(entity.FieldTypeVarChar).
    WithEnableAnalyzer(
true
).
    WithEnableMatch(
true
).
    WithAnalyzerParams(analyzerParams).
    WithMaxLength(
200
),
)
const
schema = [
  {
name
:
"id"
,
data_type
:
DataType
.
Int64
,
is_primary_key
:
true
,
  },
  {
name
:
"text"
,
data_type
:
"VarChar"
,
enable_analyzer
:
true
,
enable_match
:
true
,
max_length
:
1000
,
analyzer_params
: {
type
:
'english'
},
  },
  {
name
:
"embeddings"
,
data_type
:
DataType
.
FloatVector
,
dim
:
5
,
  },
];
export
schema=
'{
        "autoId": true,
        "enabledDynamicField": false,
        "fields": [
            {
                "fieldName": "id",
                "dataType": "Int64",
                "isPrimary": true
            },
            {
                "fieldName": "text",
                "dataType": "VarChar",
                "elementTypeParams": {
                    "max_length": 200,
                    "enable_analyzer": true,
                    "enable_match": true,
                    "analyzer_params": {"type": "english"}
                }
            },
            {
                "fieldName": "embeddings",
                "dataType": "FloatVector",
                "elementTypeParams": {
                    "dim": "5"
                }
            }
        ]
    }'
Milvus 还提供适合不同语言和场景的其他各种分析器。有关详细信息，请参阅
分析器概述
。
使用文本匹配
为 Collections Schema 中的 VARCHAR 字段启用文本匹配后，就可以使用
TEXT_MATCH
表达式执行文本匹配。
文本匹配表达式语法
TEXT_MATCH
表达式用于指定要搜索的字段和术语。其语法如下：
TEXT_MATCH(field_name, text)
field_name
:要搜索的 VARCHAR 字段的名称。
text
:要搜索的术语。根据语言和配置的分析器，多个术语可以用空格或其他适当的分隔符分隔。
默认情况下，
TEXT_MATCH
使用
OR
匹配逻辑，即返回包含任何指定术语的文档。例如，要搜索
text
字段中包含
machine
或
deep
的文档，请使用以下表达式：
Python
Java
Go
NodeJS
cURL
filter
=
"TEXT_MATCH(text, 'machine deep')"
String
filter
=
"TEXT_MATCH(text, 'machine deep')"
;
filter :=
"TEXT_MATCH(text, 'machine deep')"
const
filter =
"TEXT_MATCH(text, 'machine deep')"
;
export
filter=
"\"TEXT_MATCH(text, 'machine deep')\""
您还可以使用逻辑操作符组合多个
TEXT_MATCH
表达式来执行
AND
匹配。
要搜索
text
字段中同时包含
machine
和
deep
的文档，请使用以下表达式：
Python
Java
Go
NodeJS
cURL
filter
=
"TEXT_MATCH(text, 'machine') and TEXT_MATCH(text, 'deep')"
String
filter
=
"TEXT_MATCH(text, 'machine') and TEXT_MATCH(text, 'deep')"
;
filter :=
"TEXT_MATCH(text, 'machine') and TEXT_MATCH(text, 'deep')"
const
filter =
"TEXT_MATCH(text, 'machine') and TEXT_MATCH(text, 'deep')"
export
filter=
"\"TEXT_MATCH(text, 'machine') and TEXT_MATCH(text, 'deep')\""
要搜索
text
字段中同时包含
machine
和
learning
但不包含
deep
的文档，请使用以下表达式：
Python
Java
Go
NodeJS
cURL
filter
=
"not TEXT_MATCH(text, 'deep') and TEXT_MATCH(text, 'machine') and TEXT_MATCH(text, 'learning')"
String
filter
=
"not TEXT_MATCH(text, 'deep') and TEXT_MATCH(text, 'machine') and TEXT_MATCH(text, 'learning')"
;
filter :=
"not TEXT_MATCH(text, 'deep') and TEXT_MATCH(text, 'machine') and TEXT_MATCH(text, 'learning')"
const
filter =
"not TEXT_MATCH(text, 'deep') and TEXT_MATCH(text, 'machine') and TEXT_MATCH(text, 'learning')"
;
export
filter=
"\"not TEXT_MATCH(text, 'deep') and TEXT_MATCH(text, 'machine') and TEXT_MATCH(text, 'learning')\""
使用文本匹配搜索
文本匹配可与向量相似性搜索结合使用，以缩小搜索范围并提高搜索性能。通过在向量相似性搜索前使用文本匹配过滤 Collections，可以减少需要搜索的文档数量，从而加快查询速度。
在本例中，
filter
表达式过滤了搜索结果，使其只包含与指定术语
keyword1
或
keyword2
匹配的文档。然后在此过滤后的文档子集中执行向量相似性搜索。
通过配置文本高亮显示器，可以在搜索结果中高亮显示匹配的术语。有关详情，请参阅
文本高亮显示器
。
Python
Java
Go
NodeJS
cURL
# Match entities with `keyword1` or `keyword2`
filter
=
"TEXT_MATCH(text, 'keyword1 keyword2')"
# Assuming 'embeddings' is the vector field and 'text' is the VARCHAR field
result = client.search(
    collection_name=
"my_collection"
,
# Your collection name
anns_field=
"embeddings"
,
# Vector field name
data=[query_vector],
# Query vector
filter
=
filter
,
search_params={
"params"
: {
"nprobe"
:
10
}},
    limit=
10
,
# Max. number of results to return
output_fields=[
"id"
,
"text"
]
# Fields to return
)
String
filter
=
"TEXT_MATCH(text, 'keyword1 keyword2')"
;
SearchResp
searchResp
=
client.search(SearchReq.builder()
        .collectionName(
"my_collection"
)
        .annsField(
"embeddings"
)
        .data(Collections.singletonList(queryVector)))
.filter(filter)
.topK(
10
)
        .outputFields(Arrays.asList(
"id"
,
"text"
))
        .build());
filter :=
"TEXT_MATCH(text, 'keyword1 keyword2')"
resultSets, err := client.Search(ctx, milvusclient.NewSearchOption(
"my_collection"
,
// collectionName
10
,
// limit
[]entity.Vector{entity.FloatVector(queryVector)},
).WithANNSField(
"embeddings"
).
    WithFilter(filter).
    WithOutputFields(
"id"
,
"text"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
// Match entities with `keyword1` or `keyword2`
const
filter =
"TEXT_MATCH(text, 'keyword1 keyword2')"
;
// Assuming 'embeddings' is the vector field and 'text' is the VARCHAR field
const
result =
await
client.
search
(
collection_name
:
"my_collection"
,
// Your collection name
anns_field
:
"embeddings"
,
// Vector field name
data
: [query_vector],
// Query vector
filter
: filter,
params
: {
"nprobe"
:
10
},
limit
:
10
,
// Max. number of results to return
output_fields
: [
"id"
,
"text"
]
//Fields to return
);
export
filter=
"\"TEXT_MATCH(text, 'keyword1 keyword2')\""
export
CLUSTER_ENDPOINT=
"http://localhost:19530"
export
TOKEN=
"root:Milvus"
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/entities/search"
\
--header
"Authorization: Bearer
${TOKEN}
"
\
--header
"Content-Type: application/json"
\
-d
'{
    "collectionName": "my_collection",
    "annsField": "embeddings",
    "data": [[0.19886812562848388, 0.06023560599112088, 0.6976963061752597, 0.2614474506242501, 0.838729485096104]],
    "filter": '
"
$filter
"
',
    "searchParams": {
        "params": {
            "nprobe": 10
        }
    },
    "limit": 10,
    "outputFields": ["text","id"]
}'
使用文本匹配进行查询
文本匹配还可用于查询操作中的标量过滤。通过在
query()
方法的
expr
参数中指定
TEXT_MATCH
表达式，可以检索与给定术语匹配的文档。
下面的示例检索了
text
字段包含
keyword1
和
keyword2
这两个术语的文档。
Python
Java
Go
NodeJS
cURL
# Match entities with both `keyword1` and `keyword2`
filter
=
"TEXT_MATCH(text, 'keyword1') and TEXT_MATCH(text, 'keyword2')"
result = client.query(
    collection_name=
"my_collection"
,
filter
=
filter
,
output_fields=[
"id"
,
"text"
]
)
String
filter
=
"TEXT_MATCH(text, 'keyword1') and TEXT_MATCH(text, 'keyword2')"
;
QueryResp
queryResp
=
client.query(QueryReq.builder()
        .collectionName(
"my_collection"
)
.filter(filter)
.outputFields(Arrays.asList(
"id"
,
"text"
))
        .build()
);
filter =
"TEXT_MATCH(text, 'keyword1') and TEXT_MATCH(text, 'keyword2')"
resultSet, err := client.Query(ctx, milvusclient.NewQueryOption(
"my_collection"
).
    WithFilter(filter).
    WithOutputFields(
"id"
,
"text"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
// Match entities with both `keyword1` and `keyword2`
const
filter =
"TEXT_MATCH(text, 'keyword1') and TEXT_MATCH(text, 'keyword2')"
;
const
result =
await
client.
query
(
collection_name
:
"my_collection"
,
filter
: filter,
output_fields
: [
"id"
,
"text"
]
)
export
filter=
"\"TEXT_MATCH(text, 'keyword1') and TEXT_MATCH(text, 'keyword2')\""
export
CLUSTER_ENDPOINT=
"http://localhost:19530"
export
TOKEN=
"root:Milvus"
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/entities/query"
\
--header
"Authorization: Bearer
${TOKEN}
"
\
--header
"Content-Type: application/json"
\
-d
'{
    "collectionName": "my_collection",
    "filter": '
"
$filter
"
',
    "outputFields": ["id", "text"]
}'
注意事项
为字段启用术语匹配会触发倒排索引的创建，从而消耗存储资源。在决定是否启用此功能时，请考虑对存储的影响，因为它根据文本大小、唯一标记和所使用的分析器而有所不同。
在 Schema 中定义分析器后，其设置将永久适用于该 Collections。如果您认为不同的分析器更适合您的需要，您可以考虑删除现有的 Collections，然后使用所需的分析器配置创建一个新的 Collections。
filter
表达式中的转义规则：
表达式中用双引号或单引号括起来的字符被解释为字符串常量。如果字符串常量包含转义字符，则必须使用转义序列来表示转义字符。例如，用
\\
表示
\
，用
\\t
表示制表符
\t
，用
\\n
表示换行符。
如果字符串常量由单引号括起来，常量内的单引号应表示为
\\'
，而双引号可表示为
"
或
\\"
。 示例：
'It\\'s milvus'
。
如果字符串常量由双引号括起来，常量中的双引号应表示为
\\"
，而单引号可表示为
'
或
\\'
。 示例：
"He said \\"Hi\\""
。