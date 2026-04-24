多语言分析器
Compatible with Milvus 2.5.11+
Milvus 执行文本分析时，通常会在 Collections 的整个文本字段中应用单个分析器。如果该分析器针对英语进行了优化，那么在处理其他语言（如中文、西班牙语或法语）所需的完全不同的标记化和词干规则时就会很吃力，从而导致召回率降低。例如，搜索西班牙语单词
"teléfono"
（意为
"电话"）
时，以英语为重点的分析器会被绊倒：它可能会去掉重音，不应用西班牙语特定的词干，导致相关结果被忽略。
多语言分析器解决了这个问题，它允许你在一个 Collections 中为一个文本字段配置多个分析器。这样，你就可以在一个文本字段中存储多语言文档，Milvus 会根据每个文档的相应语言规则分析文本。
限制
此功能仅适用于基于 BM25 的文本检索和稀疏向量。更多信息，请参阅
全文检索
。
单个 Collections 中的每个文档只能使用一个分析器，由其语言标识符字段值决定。
性能可能会因分析器的复杂程度和文本数据的大小而有所不同。
概述
下图显示了在 Milvus 中配置和使用多语言分析器的工作流程：
多语言分析器工作流程
配置多语言分析器
：
使用格式设置多语言分析器：
<analyzer_name>: <analyzer_config>
，其中每个
analyzer_config
都遵循
分析仪概述
中所述的标准
analyzer_params
配置。
定义一个特殊标识符字段，用于确定每个文档的分析仪选择。
配置
default
分析器，用于处理未知语言。
创建 Collections
：
定义包含基本字段的 Schema：
primary_key
：唯一文档标识符。
text_field：文本字段
：存储原始文本内容。
identifier_字段
：表示对每个文档使用哪个分析器。
vector_field
：存储将由 BM25 函数生成的稀疏嵌入。
配置 BM25 函数和索引参数。
插入带有语言标识符的数据
：
添加包含各种语言文本的文档，其中每个文档都包含一个标识符值，指定要使用的分析器。
Milvus 根据标识符字段选择适当的分析器，标识符未知的文档使用
default
分析器。
使用特定语言分析器搜索
：
提供指定分析器名称的查询文本，Milvus 会使用指定的分析器处理查询。
根据特定语言规则进行标记化，并根据相似度返回适合语言的搜索结果。
第 1 步：配置多分析器参数
multi_analyzer_params
是一个单独的 JSON 对象，它决定了 Milvus 如何为每个实体选择合适的分析器：
Python
Java
NodeJS
Go
cURL
multi_analyzer_params = {
# Define language-specific analyzers
# Each analyzer follows this format: <analyzer_name>: <analyzer_params>
"analyzers"
: {
"english"
: {
"type"
:
"english"
},
# English-optimized analyzer
"chinese"
: {
"type"
:
"chinese"
},
# Chinese-optimized analyzer
"default"
: {
"tokenizer"
:
"icu"
}
# Required fallback analyzer
},
"by_field"
:
"language"
,
# Field determining analyzer selection
"alias"
: {
"cn"
:
"chinese"
,
# Use "cn" as shorthand for Chinese
"en"
:
"english"
# Use "en" as shorthand for English
}
}
Map<String, Object> analyzerParams =
new
HashMap
<>();
analyzerParams.put(
"analyzers"
,
new
HashMap
<String, Object>() {{
    put(
"english"
,
new
HashMap
<String, Object>() {{
        put(
"type"
,
"english"
);
    }});
    put(
"chinese"
,
new
HashMap
<String, Object>() {{
        put(
"type"
,
"chinese"
);
    }});
    put(
"default"
,
new
HashMap
<String, Object>() {{
        put(
"tokenizer"
,
"icu"
);
    }});
}});
analyzerParams.put(
"by_field"
,
"language"
);
analyzerParams.put(
"alias"
,
new
HashMap
<String, Object>() {{
    put(
"cn"
,
"chinese"
);
    put(
"en"
,
"english"
);
}});
const
multi_analyzer_params = {
// Define language-specific analyzers
// Each analyzer follows this format: <analyzer_name>: <analyzer_params>
"analyzers"
: {
"english"
: {
"type"
:
"english"
},          #
English
-optimized analyzer
"chinese"
: {
"type"
:
"chinese"
},          #
Chinese
-optimized analyzer
"default"
: {
"tokenizer"
:
"icu"
}          #
Required
fallback analyzer
  },
"by_field"
:
"language"
,                    #
Field
determining analyzer selection
"alias"
: {
"cn"
:
"chinese"
,                         #
Use
"cn"
as
shorthand
for
Chinese
"en"
:
"english"
#
Use
"en"
as
shorthand
for
English
}
}
multiAnalyzerParams :=
map
[
string
]any{
"analyzers"
:
map
[
string
]any{
"english"
:
map
[
string
]
string
{
"type"
:
"english"
},
"chinese"
:
map
[
string
]
string
{
"type"
:
"chinese"
},
"default"
:
map
[
string
]
string
{
"tokenizer"
:
"icu"
},
    },
"by_field"
:
"language"
,
"alias"
:
map
[
string
]
string
{
"cn"
:
"chinese"
,
"en"
:
"english"
,
    },
}
# restful
export
multi_analyzer_params=
'{
  "analyzers": {
    "english": {
      "type": "english"
    },
    "chinese": {
      "type": "chinese"
    },
    "default": {
      "tokenizer": "icu"
    }
  },
  "by_field": "language",
  "alias": {
    "cn": "chinese",
    "en": "english"
  }
}'
参数
是否需要？
说明
规则
analyzers
是
列出 Milvus 可用于处理文本的每种特定语言分析器。
analyzers
中的每个分析器都遵循以下格式：
<analyzer_name>: <analyzer_params>
。
使用标准
analyzer_params
语法定义每个分析器（请参阅
分析器概述
）。
添加一个关键字为
default
的条目；只要存储在
by_field
中的值与任何其他分析器名称不匹配，Milvus 就会返回到该分析器。
by_field
是
为每个文档存储 Milvus 应使用的语言（即分析器名称）的字段名称。
必须是 Collections 中定义的
VARCHAR
字段。
每一行的值必须与
analyzers
中列出的分析器名称（或别名）之一完全匹配。
如果某一行的值缺失或找不到，Milvus 会自动应用
default
分析器。
alias
无
为分析器创建快捷方式或替代名称，使它们更容易在代码中引用。每个分析器可以有一个或多个别名。
每个别名必须映射到现有的分析器键。
第 2 步：创建 Collections
创建支持多语言的 Collections 需要配置特定字段和索引：
添加字段
在这一步中，用四个基本字段定义 Collections Schema：
主键字段
(
id
)：Collections 中每个实体的唯一标识符。设置
auto_id=True
可使 Milvus 自动生成这些 ID。
语言指示符字段
(
language
)：此 VARCHAR 字段对应于
multi_analyzer_params
中指定的
by_field
。它存储每个实体的语言标识符，告诉 Milvus 使用哪种分析器。
文本内容字段
(
text
)：这个 VARCHAR 字段存储要分析和搜索的实际文本数据。设置
enable_analyzer=True
至关重要，因为它可以激活该字段的文本分析功能。
multi_analyzer_params
配置直接连接到该字段，在文本数据和特定语言分析仪之间建立连接。
向量字段
(
sparse
)：该字段将存储 BM25 函数生成的稀疏向量。这些向量代表文本数据的可分析形式，也是 Milvus 实际搜索的内容。
Python
Java
NodeJS
Go
cURL
# Import required modules
from
pymilvus
import
MilvusClient, DataType, Function, FunctionType
# Initialize client
client = MilvusClient(
    uri=
"http://localhost:19530"
,
)
# Initialize a new schema
schema = client.create_schema()
# Step 2.1: Add a primary key field for unique document identification
schema.add_field(
    field_name=
"id"
,
# Field name
datatype=DataType.INT64,
# Integer data type
is_primary=
True
,
# Designate as primary key
auto_id=
True
# Auto-generate IDs (recommended)
)
# Step 2.2: Add language identifier field
# This MUST match the "by_field" value in language_analyzer_config
schema.add_field(
    field_name=
"language"
,
# Field name
datatype=DataType.VARCHAR,
# String data type
max_length=
255
# Maximum length (adjust as needed)
)
# Step 2.3: Add text content field with multi-language analysis capability
schema.add_field(
    field_name=
"text"
,
# Field name
datatype=DataType.VARCHAR,
# String data type
max_length=
8192
,
# Maximum length (adjust based on expected text size)
enable_analyzer=
True
,
# Enable text analysis
multi_analyzer_params=multi_analyzer_params
# Connect with our language analyzers
)
# Step 2.4: Add sparse vector field to store the BM25 output
schema.add_field(
    field_name=
"sparse"
,
# Field name
datatype=DataType.SPARSE_FLOAT_VECTOR
# Sparse vector data type
)
import
com.google.gson.JsonObject;
import
io.milvus.common.clientenum.FunctionType;
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.common.DataType;
import
io.milvus.v2.common.IndexParam;
import
io.milvus.v2.service.collection.request.AddFieldReq;
import
io.milvus.v2.service.collection.request.CreateCollectionReq;
import
io.milvus.v2.service.collection.request.DropCollectionReq;
import
io.milvus.v2.service.utility.request.FlushReq;
import
io.milvus.v2.service.vector.request.InsertReq;
import
io.milvus.v2.service.vector.request.SearchReq;
import
io.milvus.v2.service.vector.request.data.EmbeddedText;
import
io.milvus.v2.service.vector.response.SearchResp;
MilvusClientV2
client
=
new
MilvusClientV2
(ConnectConfig.builder()
        .uri(
"http://localhost:19530"
)
        .build());
        
CreateCollectionReq.
CollectionSchema
collectionSchema
=
CreateCollectionReq.CollectionSchema.builder()
        .build();
        
collectionSchema.addField(AddFieldReq.builder()
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
        
collectionSchema.addField(AddFieldReq.builder()
        .fieldName(
"language"
)
        .dataType(DataType.VarChar)
        .maxLength(
255
)
        .build());

collectionSchema.addField(AddFieldReq.builder()
        .fieldName(
"text"
)
        .dataType(DataType.VarChar)
        .maxLength(
8192
)
        .enableAnalyzer(
true
)
        .multiAnalyzerParams(analyzerParams)
        .build());
        
collectionSchema.addField(AddFieldReq.builder()
        .fieldName(
"sparse"
)
        .dataType(DataType.SparseFloatVector)
        .build());
import
{
MilvusClient
,
DataType
,
FunctionType
}
from
"@zilliz/milvus2-sdk-node"
;
// Initialize client
const
client =
new
MilvusClient
({
address
:
"http://localhost:19530"
,
});
// Initialize schema array
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
auto_id
:
true
,
  },
  {
name
:
"language"
,
data_type
:
DataType
.
VarChar
,
max_length
:
255
,
  },
  {
name
:
"text"
,
data_type
:
DataType
.
VarChar
,
max_length
:
8192
,
enable_analyzer
:
true
,
analyzer_params
: multi_analyzer_params,
  },
  {
name
:
"sparse"
,
data_type
:
DataType
.
SparseFloatVector
,
  },
];
import
(
"context"
"fmt"
"github.com/milvus-io/milvus/client/v2/column"
"github.com/milvus-io/milvus/client/v2/entity"
"github.com/milvus-io/milvus/client/v2/index"
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

schema := entity.NewSchema()

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
"language"
).
    WithDataType(entity.FieldTypeVarChar).
    WithMaxLength(
255
),
).WithField(entity.NewField().
    WithName(
"text"
).
    WithDataType(entity.FieldTypeVarChar).
    WithMaxLength(
8192
).
    WithEnableAnalyzer(
true
).
    WithMultiAnalyzerParams(multiAnalyzerParams),
).WithField(entity.NewField().
    WithName(
"sparse"
).
    WithDataType(entity.FieldTypeSparseVector),
)
# restful
export
TOKEN=
"root:Milvus"
export
CLUSTER_ENDPOINT=
"http://localhost:19530"
export
idField=
'{
  "fieldName": "id",
  "dataType": "Int64",
  "isPrimary": true,
  "autoID": true
}'
export
languageField=
'{
  "fieldName": "language",
  "dataType": "VarChar",
  "elementTypeParams": {
    "max_length": 255
  }
}'
export
textField=
'{
  "fieldName": "text",
  "dataType": "VarChar",
  "elementTypeParams": {
    "max_length": 8192,
    "enable_analyzer": true，
    "multiAnalyzerParam": '
"
$multi_analyzer_params
"
'
  },
}'
export
sparseField=
'{
  "fieldName": "sparse",
  "dataType": "SparseFloatVector"
}'
定义 BM25 函数
定义一个 BM25 函数，以便从原始文本数据中生成稀疏向量表示：
Python
Java
NodeJS
Go
cURL
# Create the BM25 function
bm25_function = Function(
    name=
"text_to_vector"
,
# Descriptive function name
function_type=FunctionType.BM25,
# Use BM25 algorithm
input_field_names=[
"text"
],
# Process text from this field
output_field_names=[
"sparse"
]
# Store vectors in this field
)
# Add the function to our schema
schema.add_function(bm25_function)
CreateCollectionReq.
Function
function
=
CreateCollectionReq.Function.builder()
        .functionType(FunctionType.BM25)
        .name(
"text_to_vector"
)
        .inputFieldNames(Collections.singletonList(
"text"
))
        .outputFieldNames(Collections.singletonList(
"sparse"
))
        .build();
collectionSchema.addFunction(function);
const
functions = [
  {
name
:
"text_bm25_emb"
,
description
:
"bm25 function"
,
type
:
FunctionType
.
BM25
,
input_field_names
: [
"text"
],
output_field_names
: [
"sparse"
],
params
: {},
  },
];
function := entity.NewFunction()
schema.WithFunction(function.WithName(
"text_to_vector"
).
    WithType(entity.FunctionTypeBM25).
    WithInputFields(
"text"
).
    WithOutputFields(
"sparse"
))
# restful
export
function
=
'{
  "name": "text_to_vector",
  "type": "BM25",
  "inputFieldNames": ["text"],
  "outputFieldNames": ["sparse"]
}'
export
schema=
"{
  \"autoID\": true,
  \"fields\": [
$idField
,
$languageField
,
$textField
,
$sparseField
],
  \"functions\": [
$function
]
}"
该函数会根据每个文本条目的语言标识符自动应用相应的分析器。有关基于 BM25 的文本检索的更多信息，请参阅
全文检索
。
配置索引参数
为实现高效搜索，请在稀疏向量场上创建索引：
Python
Java
NodeJS
Go
cURL
# Configure index parameters
index_params = client.prepare_index_params()
# Add index for sparse vector field
index_params.add_index(
    field_name=
"sparse"
,
# Field to index (our vector field)
index_type=
"AUTOINDEX"
,
# Let Milvus choose optimal index type
metric_type=
"BM25"
# Must be BM25 for this feature
)
List<IndexParam> indexes =
new
ArrayList
<>();
indexes.add(IndexParam.builder()
        .fieldName(
"sparse"
)
        .indexType(IndexParam.IndexType.AUTOINDEX)
        .metricType(IndexParam.MetricType.BM25)
        .build());
const
index_params = [{
field_name
:
"sparse"
,
index_type
:
"AUTOINDEX"
,
metric_type
:
"BM25"
}];
idx := index.NewAutoIndex(index.MetricType(entity.BM25))
indexOption := milvusclient.NewCreateIndexOption(
"multilingual_documents"
,
"sparse"
, idx)
# restful
export
IndexParams=
'[
  {
    "fieldName": "sparse",
    "indexType": "AUTOINDEX",
    "metricType": "BM25",
    "params": {}
  }
]'
索引通过组织稀疏向量来提高搜索性能，从而实现高效的 BM25 相似性计算。
创建 Collections
最后的创建步骤将您之前的所有配置汇集在一起：
collection_name="multilang_demo"
为你的 Collection 命名，以备将来参考。
schema=schema
应用您定义的字段结构和功能。
index_params=index_params
实施索引策略，实现高效搜索。
Python
Java
NodeJS
Go
cURL
# Create collection
COLLECTION_NAME =
"multilingual_documents"
# Check if collection already exists
if
client.has_collection(COLLECTION_NAME):
    client.drop_collection(COLLECTION_NAME)
# Remove it for this example
print
(
f"Dropped existing collection:
{COLLECTION_NAME}
"
)
# Create the collection
client.create_collection(
    collection_name=COLLECTION_NAME,
# Collection name
schema=schema,
# Our multilingual schema
index_params=index_params
# Our search index configuration
)
client.dropCollection(DropCollectionReq.builder()
        .collectionName(
"multilingual_documents"
)
        .build());
CreateCollectionReq
requestCreate
=
CreateCollectionReq.builder()
        .collectionName(
"multilingual_documents"
)
        .collectionSchema(collectionSchema)
        .indexParams(indexes)
        .build();
client.createCollection(requestCreate);
const
COLLECTION_NAME
=
"multilingual_documents"
;
// Create the collection
await
client.
createCollection
({
collection_name
:
COLLECTION_NAME
,
schema
: schema,
index_params
: index_params,
functions
: functions
});
err = client.CreateCollection(ctx,
    milvusclient.NewCreateCollectionOption(
"multilingual_documents"
, schema).
        WithIndexOptions(indexOption))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
# restful
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/collections/create"
\
--header
"Authorization: Bearer
${TOKEN}
"
\
--header
"Content-Type: application/json"
\
--data
"{
  \"collectionName\": \"multilingual_documents\",
  \"schema\":
$schema
,
  \"indexParams\":
$IndexParams
}"
此时，Milvus 会创建一个支持多语言分析器的空 Collections，随时准备接收数据。
第 3 步：插入示例数据
向多语言 Collections 添加文档时，每个文档都必须包含文本内容和语言标识符：
Python
Java
NodeJS
Go
cURL
# Prepare multilingual documents
documents = [
# English documents
{
"text"
:
"Artificial intelligence is transforming technology"
,
"language"
:
"english"
,
# Using full language name
},
    {
"text"
:
"Machine learning models require large datasets"
,
"language"
:
"en"
,
# Using our defined alias
},
# Chinese documents
{
"text"
:
"人工智能正在改变技术领域"
,
"language"
:
"chinese"
,
# Using full language name
},
    {
"text"
:
"机器学习模型需要大型数据集"
,
"language"
:
"cn"
,
# Using our defined alias
},
]
# Insert the documents
result = client.insert(COLLECTION_NAME, documents)
# Print results
inserted = result[
"insert_count"
]
print
(
f"Successfully inserted
{inserted}
documents"
)
print
(
"Documents by language: 2 English, 2 Chinese"
)
# Expected output:
# Successfully inserted 4 documents
# Documents by language: 2 English, 2 Chinese
List<String> texts = Arrays.asList(
"Artificial intelligence is transforming technology"
,
"Machine learning models require large datasets"
,
"人工智能正在改变技术领域"
,
"机器学习模型需要大型数据集"
);
List<String> languages = Arrays.asList(
"english"
,
"en"
,
"chinese"
,
"cn"
);

List<JsonObject> rows =
new
ArrayList
<>();
for
(
int
i
=
0
; i < texts.size(); i++) {
JsonObject
row
=
new
JsonObject
();
    row.addProperty(
"text"
, texts.get(i));
    row.addProperty(
"language"
, languages.get(i));
    rows.add(row);
}
client.insert(InsertReq.builder()
        .collectionName(
"multilingual_documents"
)
        .data(rows)
        .build());
// Prepare multilingual documents
const
documents = [
// English documents
{
text
:
"Artificial intelligence is transforming technology"
,
language
:
"english"
,
  },
  {
text
:
"Machine learning models require large datasets"
,
language
:
"en"
,
  },
// Chinese documents
{
text
:
"人工智能正在改变技术领域"
,
language
:
"chinese"
,
  },
  {
text
:
"机器学习模型需要大型数据集"
,
language
:
"cn"
,
  },
];
// Insert the documents
const
result =
await
client.
insert
({
collection_name
:
COLLECTION_NAME
,
data
: documents,
});
// Print results
const
inserted = result.
insert_count
;
console
.
log
(
`Successfully inserted
${inserted}
documents`
);
console
.
log
(
"Documents by language: 2 English, 2 Chinese"
);
// Expected output:
// Successfully inserted 4 documents
// Documents by language: 2 English, 2 Chinese
column1 := column.NewColumnVarChar(
"text"
,
    []
string
{
"Artificial intelligence is transforming technology"
,
"Machine learning models require large datasets"
,
"人工智能正在改变技术领域"
,
"机器学习模型需要大型数据集"
,
    })
column2 := column.NewColumnVarChar(
"language"
,
    []
string
{
"english"
,
"en"
,
"chinese"
,
"cn"
})

_, err = client.Insert(ctx, milvusclient.NewColumnBasedInsertOption(
"multilingual_documents"
).
    WithColumns(column1, column2),
)
if
err !=
nil
{
    fmt.Println(err.Error())
// handle err
}
# restful
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/entities/insert"
\
--header
"Authorization: Bearer
${TOKEN}
"
\
--header
"Content-Type: application/json"
\
--data
'{
  "collectionName": "multilingual_documents",
  "data": [
    {
      "text": "Artificial intelligence is transforming technology",
      "language": "english"
    },
    {
      "text": "Machine learning models require large datasets",
      "language": "en"
    },
    {
      "text": "人工智能正在改变技术领域",
      "language": "chinese"
    },
    {
      "text": "机器学习模型需要大型数据集",
      "language": "cn"
    }
  ]
}'
在插入过程中，Milvus
读取每个文档的
language
字段
对
text
字段应用相应的分析器
通过 BM25 函数生成稀疏向量表示法
存储原始文本和生成的稀疏向量
您无需直接提供稀疏向量；BM25 函数会根据您的文本和指定的分析器自动生成稀疏向量。
步骤 4：执行搜索操作符
使用英文分析器
使用多语言分析器搜索时，
search_params
包含关键配置：
metric_type="BM25"
必须与您的索引配置相匹配。
analyzer_name="english"
指定对查询文本应用哪种分析器。这与存储文档中使用的分析器无关。
params={"drop_ratio_search": "0"}
控制特定于 BM25 的行为；在这里，它会保留搜索中的所有术语。更多信息，请参阅
稀疏向量
。
Python
Java
NodeJS
Go
cURL
search_params = {
"metric_type"
:
"BM25"
,
# Must match index configuration
"analyzer_name"
:
"english"
,
# Analyzer that matches the query language
"drop_ratio_search"
:
"0"
,
# Keep all terms in search (tweak as needed)
}
# Execute the search
english_results = client.search(
    collection_name=COLLECTION_NAME,
# Collection to search
data=[
"artificial intelligence"
],
# Query text
anns_field=
"sparse"
,
# Field to search against
search_params=search_params,
# Search configuration
limit=
3
,
# Max results to return
output_fields=[
"text"
,
"language"
],
# Fields to include in the output
consistency_level=
"Bounded"
,
# Data‑consistency guarantee
)
# Display English search results
print
(
"\n=== English Search Results ==="
)
for
i, hit
in
enumerate
(english_results[
0
]):
print
(
f"
{i+
1
}
. [
{hit.score:
.4
f}
]
{hit.entity.get(
'text'
)}
"
f"(Language:
{hit.entity.get(
'language'
)}
)"
)
# Expected output:
# === English Search Results ===
# 1. [2.7881] Artificial intelligence is transforming technology (Language: english)
Map<String,Object> searchParams =
new
HashMap
<>();
searchParams.put(
"metric_type"
,
"BM25"
);
searchParams.put(
"analyzer_name"
,
"english"
);
searchParams.put(
"drop_ratio_search"
,
0
);
SearchResp
searchResp
=
client.search(SearchReq.builder()
        .collectionName(
"multilingual_documents"
)
        .data(Collections.singletonList(
new
EmbeddedText
(
"artificial intelligence"
)))
        .annsField(
"sparse"
)
        .topK(
3
)
        .searchParams(searchParams)
        .outputFields(Arrays.asList(
"text"
,
"language"
))
        .build());

System.out.println(
"\n=== English Search Results ==="
);
List<List<SearchResp.SearchResult>> searchResults = searchResp.getSearchResults();
for
(List<SearchResp.SearchResult> results : searchResults) {
for
(SearchResp.SearchResult result : results) {
        System.out.printf(
"Score: %f, %s\n"
, result.getScore(), result.getEntity().toString());
    }
}
// Execute the search
const
english_results =
await
client.
search
({
collection_name
:
COLLECTION_NAME
,
data
: [
"artificial intelligence"
],
anns_field
:
"sparse"
,
params
: {
metric_type
:
"BM25"
,
analyzer_name
:
"english"
,
drop_ratio_search
:
"0"
,
  },
limit
:
3
,
output_fields
: [
"text"
,
"language"
],
consistency_level
:
"Bounded"
,
});
// Display English search results
console
.
log
(
"\n=== English Search Results ==="
);
english_results.
results
.
forEach
(
(
hit, i
) =>
{
console
.
log
(
`
${i +
1
}
. [
${hit.score.toFixed(
4
)}
]
${hit.entity.text}
`
+
`(Language:
${hit.entity.language}
)`
);
});
annSearchParams := index.NewCustomAnnParam()
annSearchParams.WithExtraParam(
"metric_type"
,
"BM25"
)
annSearchParams.WithExtraParam(
"analyzer_name"
,
"english"
)
annSearchParams.WithExtraParam(
"drop_ratio_search"
,
0
)

resultSets, err := client.Search(ctx, milvusclient.NewSearchOption(
"multilingual_documents"
,
// collectionName
3
,
// limit
[]entity.Vector{entity.Text(
"artificial intelligence"
)},
).WithANNSField(
"sparse"
).
    WithAnnParam(annSearchParams).
    WithOutputFields(
"text"
,
"language"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
for
_, resultSet :=
range
resultSets {
for
i :=
0
; i <
len
(resultSet.Scores); i++ {
        text, _ := resultSet.GetColumn(
"text"
).GetAsString(i)
        lang, _ := resultSet.GetColumn(
"language"
).GetAsString(i)
        fmt.Println(
"Score: "
, resultSet.Scores[i],
"Text: "
, text,
"Language:"
, lang)
    }
}
# restful
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
--data
'{
  "collectionName": "multilingual_documents",
  "data": ["artificial intelligence"],
  "annsField": "sparse",
  "limit": 3,
  "searchParams": {
    "metric_type": "BM25",
    "analyzer_name": "english",
    "drop_ratio_search": "0"  
  },
  "outputFields": ["text", "language"],
  "consistencyLevel": "Bounded"
}'
使用中文分析器
本示例演示了针对不同的查询文本切换到中文分析器（使用其别名
"cn"
）。所有其他参数保持不变，但现在使用特定于中文的标记化规则处理查询文本。
Python
Java
NodeJS
Go
cURL
search_params[
"analyzer_name"
] =
"cn"
chinese_results = client.search(
    collection_name=COLLECTION_NAME,
# Collection to search
data=[
"人工智能"
],
# Query text
anns_field=
"sparse"
,
# Field to search against
search_params=search_params,
# Search configuration
limit=
3
,
# Max results to return
output_fields=[
"text"
,
"language"
],
# Fields to include in the output
consistency_level=
"Bounded"
,
# Data‑consistency guarantee
)
# Display Chinese search results
print
(
"\n=== Chinese Search Results ==="
)
for
i, hit
in
enumerate
(chinese_results[
0
]):
print
(
f"
{i+
1
}
. [
{hit.score:
.4
f}
]
{hit.entity.get(
'text'
)}
"
f"(Language:
{hit.entity.get(
'language'
)}
)"
)
# Expected output:
# === Chinese Search Results ===
# 1. [3.3814] 人工智能正在改变技术领域 (Language: chinese)
searchParams.put(
"analyzer_name"
,
"cn"
);
searchResp = client.search(SearchReq.builder()
        .collectionName(
"multilingual_documents"
)
        .data(Collections.singletonList(
new
EmbeddedText
(
"人工智能"
)))
        .annsField(
"sparse"
)
        .topK(
3
)
        .searchParams(searchParams)
        .outputFields(Arrays.asList(
"text"
,
"language"
))
        .build());

System.out.println(
"\n=== Chinese Search Results ==="
);
searchResults = searchResp.getSearchResults();
for
(List<SearchResp.SearchResult> results : searchResults) {
for
(SearchResp.SearchResult result : results) {
        System.out.printf(
"Score: %f, %s\n"
, result.getScore(), result.getEntity().toString());
    }
}
// Execute the search
const
cn_results =
await
client.
search
({
collection_name
:
COLLECTION_NAME
,
data
: [
"人工智能"
],
anns_field
:
"sparse"
,
params
: {
metric_type
:
"BM25"
,
analyzer_name
:
"cn"
,
drop_ratio_search
:
"0"
,
  },
limit
:
3
,
output_fields
: [
"text"
,
"language"
],
consistency_level
:
"Bounded"
,
});
// Display Chinese search results
console
.
log
(
"\n=== Chinese Search Results ==="
);
cn_results.
results
.
forEach
(
(
hit, i
) =>
{
console
.
log
(
`
${i +
1
}
. [
${hit.score.toFixed(
4
)}
]
${hit.entity.text}
`
+
`(Language:
${hit.entity.language}
)`
);
});
annSearchParams.WithExtraParam(
"analyzer_name"
,
"cn"
)

resultSets, err = client.Search(ctx, milvusclient.NewSearchOption(
"multilingual_documents"
,
// collectionName
3
,
// limit
[]entity.Vector{entity.Text(
"人工智能"
)},
).WithANNSField(
"sparse"
).
    WithAnnParam(annSearchParams).
    WithOutputFields(
"text"
,
"language"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
for
_, resultSet :=
range
resultSets {
for
i :=
0
; i <
len
(resultSet.Scores); i++ {
        text, _ := resultSet.GetColumn(
"text"
).GetAsString(i)
        lang, _ := resultSet.GetColumn(
"language"
).GetAsString(i)
        fmt.Println(
"Score: "
, resultSet.Scores[i],
"Text: "
, text,
"Language:"
, lang)
    }
}
# restful
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
--data
'{
  "collectionName": "multilingual_documents",
  "data": ["人工智能"],
  "annsField": "sparse",
  "limit": 3,
  "searchParams": {
    "analyzer_name": "cn"
  },
  "outputFields": ["text", "language"],
  "consistencyLevel": "Bounded"
}'