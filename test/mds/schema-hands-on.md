搜索数据模型设计
信息检索系统（又称搜索引擎）是各种人工智能应用（如检索增强生成（RAG）、可视化搜索和产品推荐）的关键。这些系统的核心是精心设计的数据模型，用于组织、索引和检索信息。
Milvus 允许您通过 Collect schema 指定搜索数据模型，组织非结构化数据、它们的密集或稀疏向量表示以及结构化元数据。无论您处理的是文本、图像还是其他数据类型，本实践指南都将帮助您理解和应用关键的 Schema 概念，在实践中设计搜索数据模型。
数据模型剖析
数据模型
搜索系统的数据模型设计包括分析业务需求，并将信息抽象为模式表达的数据模型。定义明确的 Schema 对于使数据模型与业务目标保持一致、确保数据一致性和服务质量非常重要。  此外，选择适当的数据类型和索引对于经济地实现业务目标也很重要。
分析业务需求
要有效满足业务需求，首先要分析用户将执行的查询类型，并确定最合适的搜索方法。
用户查询：
确定用户预期执行的查询类型。这有助于确保您的 Schema 支持真实世界的用例并优化搜索性能。这些查询可能包括
检索与自然语言查询相匹配的文档
查找与参考图片相似或匹配文本描述的图片
根据名称、类别或品牌等属性搜索产品
根据结构化元数据（如出版日期、标签、评级）过滤项目
在混合查询中结合多种标准（例如，在视觉搜索中，同时考虑图像及其说明的语义相似性）
搜索方法：
根据用户将执行的查询类型选择适当的搜索技术。不同的方法服务于不同的目的，通常可以结合使用以获得更强大的结果：
语义搜索
：使用密集向量相似性来查找具有相似含义的项目，非常适合文本或图像等非结构化数据。
全文搜索
：用关键字匹配补充语义搜索。  全文搜索可以利用词法分析，避免将长词分解成零散的标记，在检索过程中抓住特殊术语。
元数据过滤
：在向量搜索的基础上，应用日期范围、类别或标签等约束条件。
将业务需求转化为搜索数据模型
下一步是将业务需求转化为具体的数据模型，方法是确定信息的核心组件及其搜索方法：
定义需要存储的数据，如原始内容（文本、图像、音频）、相关元数据（标题、标签、作者）和上下文属性（时间戳、用户行为等）。
为每个元素确定适当的数据类型和格式。例如
文本描述 → 字符串
图像或文档 Embeddings → 密集或稀疏向量
类别、标签或标志 → 字符串、数组和 bool
价格或评级等数字属性 → 整数或浮点数
结构化信息，如作者详细信息 -> json
明确定义这些元素可确保数据的一致性、搜索结果的准确性以及与下游应用逻辑集成的便捷性。
Schema 设计
在 Milvus 中，数据模型通过 Collections Schema 表达。在 Collections 模式中设计正确的字段是实现有效检索的关键。每个字段都定义了存储在 Collections 中的特定数据类型，并在搜索过程中扮演着不同的角色。在高层次上，Milvus 支持两种主要类型的字段：
向量字段
和
标量字段
。
现在，您可以将数据模型映射到字段 Schema 中，包括向量和任何辅助标量字段。确保每个字段都与数据模型中的属性相关联，尤其要注意向量类型（密集型或标量型）及其维度。
向量字段
向量字段存储文本、图像和音频等非结构化数据类型的嵌入。这些嵌入可能是密集型、稀疏型或二进制型，具体取决于数据类型和使用的检索方法。通常，密集向量用于语义搜索，而稀疏向量则更适合全文或词性匹配。当存储和计算资源有限时，二进制向量很有用。一个 Collections 可能包含多个向量场，以实现多模式或混合检索策略。有关该主题的详细指南，请参阅
多向量混合检索
。
Milvus 支持向量数据类型：
FLOAT_VECTOR
表示
密集
向量，
SPARSE_FLOAT_VECTOR
表示
稀疏向量
，
BINARY_VECTOR
表示
二进制向量
标量字段
标量字段存储原始的结构化值，通常称为元数据，如数字、字符串或日期。这些值可以与向量搜索结果一起返回，对于筛选和排序至关重要。它们允许你根据特定属性缩小搜索结果的范围，比如将文档限制在特定类别或定义的时间范围内。
Milvus 支持标量类型，如
BOOL
,
INT8/16/32/64
,
FLOAT
,
DOUBLE
,
VARCHAR
,
JSON
和
ARRAY
，用于存储和过滤非向量数据。这些类型提高了搜索操作的精度和定制化程度。
在模式设计中利用高级功能
在设计 Schema 时，仅仅使用支持的数据类型将数据映射到字段是不够的。必须全面了解字段之间的关系以及可用的配置策略。在设计阶段牢记关键功能，可确保 Schema 不仅能满足当前的数据处理要求，还具有可扩展性和适应性，以满足未来的需求。通过精心整合这些功能，您可以构建一个强大的数据架构，最大限度地发挥 Milvus 的功能，并支持您更广泛的数据策略和目标。以下是创建 Collections Schema 的主要功能概述：
主键
主键字段是 Schema 的基本组成部分，因为它能唯一标识 Collections 中的每个实体。必须定义主键。它必须是整数或字符串类型的标量字段，并标记为
is_primary=True
。可选择为主键启用
auto_id
，主键会自动分配整数，随着更多数据被采集到 Collections 中，整数也会随之增长。
有关详细信息，请参阅
主字段和自动 ID
。
分区
为了加快搜索速度，可以选择打开分区。通过为分区指定一个特定的标量字段，并在搜索过程中根据该字段指定过滤条件，可以有效地将搜索范围限制在相关的分区中。这种方法通过缩小搜索域，大大提高了检索操作的效率。
更多详情，请参阅
使用 Partition Key
。
分析器
分析器是处理和转换文本数据的重要工具。它的主要功能是将原始文本转换为标记，并对其进行结构化处理，以便编制索引和进行检索。具体做法是对字符串进行标记化处理，去掉停顿词，并将单个词的词干转化为标记。
更多详情，请参阅
分析器概述
。
功能
Milvus 允许你定义内置函数作为 Schema 的一部分，以自动推导出某些字段。例如，您可以添加内置 BM25 函数，从
VARCHAR
字段生成稀疏向量，以支持全文搜索。这些函数派生字段可简化预处理，并确保 Collections 保持自足和查询就绪。
更多详情，请参阅
全文检索
。
真实世界示例
在本节中，我们将概述上图所示多媒体文档搜索应用程序的 Schema 设计和代码示例。该 Schema 设计用于管理包含文章的数据集，文章数据映射到以下字段：
字段
数据源
搜索方法使用
主键
分区键
分析器
函数输入/输出
article_id (
INT64
)
启用后自动生成
auto_id
使用 "获取 "进行查询
Y
N
N
N
标题 (
VARCHAR
)
文章标题
文本匹配
N
N
Y
N
时间戳 (
INT32
)
发布日期
按分区密钥过滤
N
Y
N
N
文本 (
VARCHAR
)
文章原始文本
多向量混合搜索
N
N
Y
输入
文本密集向量 (
FLOAT_VECTOR
)
由文本 Embeddings 模型生成的密集向量
基本向量搜索
N
N
N
N
文本稀疏向量 (
SPARSE_FLOAT_VECTOR
)
由内置 BM25 函数自动生成的稀疏向量
全文搜索
N
N
N
输出
有关
Schema 的
更多信息以及添加各类字段的详细指导，请参阅
Schema Explained
。
初始化模式
首先，我们需要创建一个空模式。这一步为定义数据模型建立了基础结构。
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
MilvusClient

schema = MilvusClient.create_schema()
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.service.collection.request.CreateCollectionReq;
// 1. Connect to Milvus server
ConnectConfig
connectConfig
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
(connectConfig);
// 2. Create an empty schema
CreateCollectionReq.
CollectionSchema
schema
=
client.createSchema();
import
{
MilvusClient
,
DataType
}
from
"@zilliz/milvus2-sdk-node"
;
//Skip this step using JavaScript
import
"github.com/milvus-io/milvus/client/v2/entity"
schema := entity.NewSchema()
# Skip this step using cURL
添加字段
创建 Schema 后，下一步就是指定构成数据的字段。每个字段都与各自的数据类型和属性相关联。
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
DataType

schema.add_field(field_name=
"article_id"
, datatype=DataType.INT64, is_primary=
True
, auto_id=
True
, description=
"article id"
)
schema.add_field(field_name=
"title"
, datatype=DataType.VARCHAR, enable_analyzer=
True
, enable_match=
True
, max_length=
200
, description=
"article title"
)
schema.add_field(field_name=
"timestamp"
, datatype=DataType.INT32, description=
"publish date"
)
schema.add_field(field_name=
"text"
, datatype=DataType.VARCHAR, max_length=
2000
, enable_analyzer=
True
, description=
"article text content"
)
schema.add_field(field_name=
"text_dense_vector"
, datatype=DataType.FLOAT_VECTOR, dim=
768
, description=
"text dense vector"
)
schema.add_field(field_name=
"text_sparse_vector"
, datatype=DataType.SPARSE_FLOAT_VECTOR, description=
"text sparse vector"
)
import
io.milvus.v2.common.DataType;
import
io.milvus.v2.service.collection.request.AddFieldReq;

schema.addField(AddFieldReq.builder()
        .fieldName(
"article_id"
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
"title"
)
        .dataType(DataType.VarChar)
        .maxLength(
200
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
"timestamp"
)
        .dataType(DataType.Int32)
        .build())
schema.addField(AddFieldReq.builder()
        .fieldName(
"text"
)
        .dataType(DataType.VarChar)
        .maxLength(
2000
)
        .enableAnalyzer(
true
)
        .build());
schema.addField(AddFieldReq.builder()
        .fieldName(
"text_dense_vector"
)
        .dataType(DataType.FloatVector)
        .dimension(
768
)
        .build());
schema.addField(AddFieldReq.builder()
        .fieldName(
"text_sparse_vector"
)
        .dataType(DataType.SparseFloatVector)
        .build());
const
fields = [
    {
name
:
"article_id"
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
},
    {
name
:
"title"
,
data_type
:
DataType
.
VarChar
,
max_length
:
200
,
enable_analyzer
:
true
,
enable_match
:
true
},
    {
name
:
"timestamp"
,
data_type
:
DataType
.
Int32
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
2000
,
enable_analyzer
:
true
},
    {
name
:
"text_dense_vector"
,
data_type
:
DataType
.
FloatVector
,
dim
:
768
},
    {
name
:
"text_sparse_vector"
,
data_type
:
DataType
.
SparseFloatVector
}
]
schema.WithField(entity.NewField().
    WithName(
"article_id"
).
    WithDataType(entity.FieldTypeInt64).
    WithIsPrimaryKey(
true
).
    WithIsAutoID(
true
).
    WithDescription(
"article id"
),
).WithField(entity.NewField().
    WithName(
"title"
).
    WithDataType(entity.FieldTypeVarChar).
    WithMaxLength(
200
).
    WithEnableAnalyzer(
true
).
    WithEnableMatch(
true
).
    WithDescription(
"article title"
),
).WithField(entity.NewField().
    WithName(
"timestamp"
).
    WithDataType(entity.FieldTypeInt32).
    WithDescription(
"publish date"
),
).WithField(entity.NewField().
    WithName(
"text"
).
    WithDataType(entity.FieldTypeVarChar).
    WithMaxLength(
2000
).
    WithEnableAnalyzer(
true
).
    WithDescription(
"article text content"
),
).WithField(entity.NewField().
    WithName(
"text_dense_vector"
).
    WithDataType(entity.FieldTypeFloatVector).
    WithDim(
768
).
    WithDescription(
"text dense vector"
),
).WithField(entity.NewField().
    WithName(
"text_sparse_vector"
).
    WithDataType(entity.FieldTypeSparseVector).
    WithDescription(
"text sparse vector"
),
)
export
fields=
'[
    {
        "fieldName": "article_id",
        "dataType": "Int64",
        "isPrimary": true
    },
    {
        "fieldName": "title",
        "dataType": "VarChar",
        "elementTypeParams": {
            "max_length": 200,
            "enable_analyzer": true,
            "enable_match": true
        }
    },
    {
        "fieldName": "timestamp",
        "dataType": "Int32"
    },
    {
       "fieldName": "text",
       "dataType": "VarChar",
       "elementTypeParams": {
            "max_length": 2000,
            "enable_analyzer": true
        }
    },
    {
       "fieldName": "text_dense_vector",
       "dataType": "FloatVector",
       "elementTypeParams": {
            "dim": 768
        }
    },
    {
       "fieldName": "text_sparse_vector",
       "dataType": "SparseFloatVector",
    }
]'
export
schema=
"{
    \"autoID\": true,
    \"fields\":
$fields
}"
在本例中，为字段指定了以下属性：
主键：
article_id
用作主键，可自动为输入实体分配主键。
Partition Key：
timestamp
被指定为分区键，允许通过分区进行过滤。这可能是
文本分析器：文本分析器应用于 2 个字符串字段
title
和
text
，分别支持文本匹配和全文搜索。
(可选）添加功能
为增强数据查询功能，可在 Schema 中加入函数。例如，可以创建一个函数来处理与特定字段相关的数据。
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
Function, FunctionType

bm25_function = Function(
    name=
"text_bm25"
,
    input_field_names=[
"text"
],
    output_field_names=[
"text_sparse_vector"
],
    function_type=FunctionType.BM25,
)

schema.add_function(bm25_function)
import
io.milvus.common.clientenum.FunctionType;
import
io.milvus.v2.service.collection.request.CreateCollectionReq.Function;
import
java.util.*;

schema.addFunction(Function.builder()
        .functionType(FunctionType.BM25)
        .name(
"text_bm25"
)
        .inputFieldNames(Collections.singletonList(
"text"
))
        .outputFieldNames(Collections.singletonList(
"text_sparse_vector"
))
        .build());
import
FunctionType
from
"@zilliz/milvus2-sdk-node"
;
const
functions = [
    {
name
:
'text_bm25'
,
description
:
'bm25 function'
,
type
:
FunctionType
.
BM25
,
input_field_names
: [
'text'
],
output_field_names
: [
'text_sparse_vector'
],
params
: {},
    },
]；
function := entity.NewFunction().
    WithName(
"text_bm25"
).
    WithInputFields(
"text"
).
    WithOutputFields(
"text_sparse_vector"
).
    WithType(entity.FunctionTypeBM25)
schema.WithFunction(function)
export
myFunctions=
'[
    {
        "name": "text_bm25",
        "type": "BM25",
        "inputFieldNames": ["text"],
        "outputFieldNames": ["text_sparse_vector"],
        "params": {}
    }
]'
export
schema=
"{
    \"autoID\": true,
    \"fields\":
$fields
\"functions\":
$myFunctions
}"
本例在 Schema 中添加了一个内置 BM25 函数，利用
text
字段作为输入，并将生成的稀疏向量存储在
text_sparse_vector
字段中。
下一步
创建 Collection
更改 Collections 字段