模式解释
Schema 定义了 Collections 的数据结构。在创建一个 Collection 之前，你需要设计出它的 Schema。本页将帮助你理解 Collections 模式，并自行设计一个示例模式。
概述
在 Milvus 上，Collection Schema 是关系数据库中一个表的组合，它定义了 Milvus 如何组织 Collection 中的数据。
设计良好的 Schema 至关重要，因为它抽象了数据模型，并决定能否通过搜索实现业务目标。此外，由于插入 Collections 的每一行数据都必须遵循 Schema，因此有助于保持数据的一致性和长期质量。从技术角度来看，定义明确的 Schema 会带来组织良好的列数据存储和更简洁的索引结构，从而提升搜索性能。
Collections Schema 有一个主键、至少一个向量字段和几个标量字段。下图说明了如何将文章映射到模式字段列表。
Schema 设计剖析
搜索系统的数据模型设计包括分析业务需求，并将信息抽象为模式表达的数据模型。例如，搜索一段文本必须通过 "嵌入 "将字面字符串转换为向量并启用向量搜索，从而实现 "索引"。除了这一基本要求外，可能还需要存储出版时间戳和作者等其他属性。有了这些元数据，就可以通过过滤来完善语义搜索，只返回特定日期之后或特定作者发表的文本。您还可以检索这些标量与主文本，以便在应用程序中呈现搜索结果。每个标量都应分配一个唯一标识符，以整数或字符串的形式组织这些文本片段。这些元素对于实现复杂的搜索逻辑至关重要。
请参考
Schema Design Hands-On
，了解如何制作一个精心设计的模式。
创建 Schema
以下代码片段演示了如何创建模式。
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
MilvusClient, DataType

schema = MilvusClient.create_schema()
import
io.milvus.v2.service.collection.request.CreateCollectionReq;

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
const
schema = []
import
"github.com/milvus-io/milvus/client/v2/entity"
schema := entity.NewSchema()
export
schema=
'{
    "fields": []
}'
添加主字段
Collections 中的主字段唯一标识一个实体。它只接受
Int64
或
VarChar
值。以下代码片段演示了如何添加主字段。
Python
Java
NodeJS
Go
cURL
schema.add_field(
    field_name=
"my_id"
,
    datatype=DataType.INT64,
is_primary=
True
,
auto_id=
False
,
)
import
io.milvus.v2.common.DataType;
import
io.milvus.v2.service.collection.request.AddFieldReq; 

schema.addField(AddFieldReq.builder()
        .fieldName(
"my_id"
)
        .dataType(DataType.Int64)
.isPrimaryKey(
true
)
.autoID(
false
)
.build());
schema.
push
({
name
:
"my_id"
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
autoID
:
false
});
schema.WithField(entity.NewField().WithName(
"my_id"
).
    WithDataType(entity.FieldTypeInt64).
WithIsPrimaryKey(
true
).
WithIsAutoID(
false
),
)
export
primaryField=
'{
    "fieldName": "my_id",
    "dataType": "Int64",
    "isPrimary": true
}'
export
schema=
'{
    \"autoID\": false,
    \"fields\": [
        $primaryField
    ]
}'
添加字段时，可以通过将
is_primary
属性设置为
True
来明确说明该字段是主字段。主字段默认接受
Int64
值。在这种情况下，主字段值应为整数，类似于
12345
。如果选择在主字段中使用
VarChar
值，则其值应为字符串，类似于
my_entity_1234
。
您也可以将
autoId
属性设置为
True
，使 Milvus 在插入数据时自动分配主字段值。
建议您在所有情况下都使用
autoId
，除非手动设置主键是有益的。
详情请参阅 "
主字段和自动 ID
"。
添加向量字段
向量字段接受各种稀疏和密集向量嵌入。在 Milvus 上，你可以向一个 Collections 添加四个向量字段。以下代码片段演示了如何添加向量字段。
Python
Java
NodeJS
Go
cURL
schema.add_field(
    field_name=
"my_vector"
,
    datatype=DataType.FLOAT_VECTOR,
dim=
5
)
schema.addField(AddFieldReq.builder()
        .fieldName(
"my_vector"
)
        .dataType(DataType.FloatVector)
.dimension(
5
)
.build());
schema.
push
({
name
:
"my_vector"
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
});
schema.WithField(entity.NewField().WithName(
"my_vector"
).
    WithDataType(entity.FieldTypeFloatVector).
WithDim(
5
),
)
export
vectorField=
'{
    "fieldName": "my_vector",
    "dataType": "FloatVector",
    "elementTypeParams": {
        "dim": 5
    }
}'
export
schema=
"{
    \"autoID\": false,
    \"fields\": [
$primaryField
,
$vectorField
]
}"
上述代码片段中的
dim
参数表示向量字段中要保存的向量嵌入的维数。
FLOAT_VECTOR
值表示该向量场持有 32 位浮点数列表，通常用于表示反比例。除此之外，Milvus 还支持以下类型的向量嵌入：
FLOAT16_VECTOR
这种类型的向量场保存一个 16 位半精度浮点数列表，通常适用于内存或带宽受限的深度学习或基于 GPU 的计算场景。
BFLOAT16_VECTOR
这种类型的向量字段保存 16 位浮点数列表，精度有所降低，但指数范围与 Float32 相同。这种类型的数据常用于深度学习场景，因为它能在不明显影响精度的情况下减少内存使用量。
INT8_VECTOR
这种类型的向量字段存储由 8 位有符号整数（int8）组成的向量，每个分量的范围为-128 到 127。它专为量化深度学习架构（如 ResNet 和 EfficientNet）量身定做，可大幅缩小模型大小，提高推理速度，同时只造成极小的精度损失。
注
：该向量类型仅支持 HNSW 索引。
BINARY_VECTOR
这种类型的向量场保存着一个 0 和 1 的列表。在图像处理和信息检索场景中，它们是表示数据的紧凑特征。
SPARSE_FLOAT_VECTOR
该类型的向量场可保存非零数字及其序列号列表，用于表示稀疏向量嵌入。
添加标量字段
在常见情况下，可以使用标量字段来存储 Milvus 中存储的向量嵌入的元数据，并通过元数据过滤进行 ANN 搜索，以提高搜索结果的正确性。Milvus 支持多种标量字段类型，包括
VarChar
、
Boolean
、
Int
、
Float
和
Double
。
添加字符串字段
在 Milvus 中，你可以使用 VarChar 字段来存储字符串。有关 VarChar 字段的更多信息，请参阅
字符串字段
。
Python
Java
NodeJS
Go
cURL
schema.add_field(
    field_name=
"my_varchar"
,
    datatype=DataType.VARCHAR,
max_length=
512
)
schema.addField(AddFieldReq.builder()
        .fieldName(
"my_varchar"
)
        .dataType(DataType.VarChar)
.maxLength(
512
)
.build());
schema.
push
({
name
:
"my_varchar"
,
data_type
:
DataType
.
VarChar
,
max_length
:
512
});
schema.WithField(entity.NewField().WithName(
"my_varchar"
).
    WithDataType(entity.FieldTypeVarChar).
    WithMaxLength(
512
),
)
export
varCharField=
'{
    "fieldName": "my_varchar",
    "dataType": "VarChar",
    "elementTypeParams": {
        "max_length": 512
    }
}'
export
schema=
"{
    \"autoID\": false,
    \"fields\": [
$primaryField
,
$vectorField
,
$varCharField
]
}"
添加数字字段
Milvus 支持的数字类型有
Int8
,
Int16
,
Int32
,
Int64
,
Float
和
Double
。有关数字字段的更多信息，请参阅
数字
字段。
Python
Java
NodeJS
Go
cURL
schema.add_field(
    field_name=
"my_int64"
,
    datatype=DataType.INT64,
)
schema.addField(AddFieldReq.builder()
        .fieldName(
"my_int64"
)
        .dataType(DataType.Int64)
        .build());
schema.
push
({
name
:
"my_int64"
,
data_type
:
DataType
.
Int64
,
});
schema.WithField(entity.NewField().WithName(
"my_int64"
).
    WithDataType(entity.FieldTypeInt64),
)
export
int64Field=
'{
    "fieldName": "my_int64",
    "dataType": "Int64"
}'
export
schema=
"{
    \"autoID\": false,
    \"fields\": [
$primaryField
,
$vectorField
,
$varCharField
,
$int64Field
]
}"
添加布尔字段
Milvus 支持布尔字段。以下代码片段演示了如何添加布尔字段。
Python
Java
NodeJS
Go
cURL
schema.add_field(
    field_name=
"my_bool"
,
    datatype=DataType.BOOL,
)
schema.addField(AddFieldReq.builder()
        .fieldName(
"my_bool"
)
        .dataType(DataType.Bool)
        .build());
schema.
push
({
name
:
"my_bool"
,
data_type
:
DataType
.
Boolean
,
});
schema.WithField(entity.NewField().WithName(
"my_bool"
).
    WithDataType(entity.FieldTypeBool),
)
export
boolField=
'{
    "fieldName": "my_bool",
    "dataType": "Boolean"
}'
export
schema=
"{
    \"autoID\": false,
    \"fields\": [
$primaryField
,
$vectorField
,
$varCharField
,
$int64Field
,
$boolField
]
}"
添加复合字段
在 Milvus 中，复合字段是指可以划分为更小的子字段的字段，例如 JSON 字段中的键或数组字段中的索引。
添加 JSON 字段
JSON 字段通常存储半结构化的 JSON 数据。有关 JSON 字段的更多信息，请参阅
JSON 字段
。
Python
Java
NodeJS
Go
cURL
schema.add_field(
    field_name=
"my_json"
,
    datatype=DataType.JSON,
)
schema.addField(AddFieldReq.builder()
        .fieldName(
"my_json"
)
        .dataType(DataType.JSON)
        .build());
schema.
push
({
name
:
"my_json"
,
data_type
:
DataType
.
JSON
,
});
schema.WithField(entity.NewField().WithName(
"my_json"
).
    WithDataType(entity.FieldTypeJSON),
)
export
jsonField=
'{
    "fieldName": "my_json",
    "dataType": "JSON"
}'
export
schema=
"{
    \"autoID\": false,
    \"fields\": [
$primaryField
,
$vectorField
,
$varCharField
,
$int64Field
,
$boolField
,
$jsonField
]
}"
添加数组字段
数组字段存储元素列表。数组字段中所有元素的数据类型应相同。有关数组字段的更多信息，请参阅
数组
字段。
Python
Java
NodeJS
Go
cURL
schema.add_field(
    field_name=
"my_array"
,
    datatype=DataType.ARRAY,
    element_type=DataType.VARCHAR,
    max_capacity=
5
,
    max_length=
512
,
)
schema.addField(AddFieldReq.builder()
        .fieldName(
"my_array"
)
        .dataType(DataType.Array)
        .elementType(DataType.VarChar)
        .maxCapacity(
5
)
        .maxLength(
512
)
        .build());
schema.
push
({
name
:
"my_array"
,
data_type
:
DataType
.
Array
,
element_type
:
DataType
.
VarChar
,
max_capacity
:
5
,
max_length
:
512
});
schema.WithField(entity.NewField().WithName(
"my_array"
).
    WithDataType(entity.FieldTypeArray).
    WithElementType(entity.FieldTypeInt64).
    WithMaxLength(
512
).
    WithMaxCapacity(
5
),
)
export
arrayField=
'{
    "fieldName": "my_array",
    "dataType": "Array",
    "elementDataType": "VarChar",
    "elementTypeParams": {
        "max_length": 512
    }
}'
export
schema=
"{
    \"autoID\": false,
    \"fields\": [
$primaryField
,
$vectorField
,
$varCharField
,
$int64Field
,
$boolField
,
$jsonField
,
$arrayField
]
}"