反转
当您需要对数据执行频繁的过滤查询时，
INVERTED
索引可显著提高查询性能。Milvus 使用倒排索引来快速查找与过滤条件相匹配的准确记录，而不是扫描所有文档。
何时使用反转索引
需要时使用反转索引：
通过特定值进行筛选
：查找某个字段等于特定值的所有记录（例如
category == "electronics"
)
过滤文本内容
：在
VARCHAR
字段上执行高效搜索
查询 JSON 字段值
：对 JSON 结构中的特定键进行过滤
性能优势
：INVERTED 索引无需进行全 Collectionions 扫描，可将大型数据集的查询时间从几秒缩短到几毫秒。
INVERTED 索引如何工作
Milvus 中的
INVERTED 索引
将每个唯一字段值（术语）映射到出现该值的文档 ID 集。这种结构可以快速查找具有重复或分类值的字段。
如图所示，该过程分为两个步骤：
前向映射（ID → 术语）：
每个文档 ID 都指向其包含的字段值。
反向映射（术语 → ID）：
Milvus Collections 收集唯一术语，并从每个术语到包含该术语的所有 ID 建立反向映射。
例如，值
"electronics "
映射到 ID
1
和
3
，而
"books "
映射到 ID
2
和
5
。
反向索引如何工作
当你过滤特定值（例如
category == "electronics"
）时，Milvus 只需在索引中查找该术语，并直接检索匹配的 ID。这就避免了扫描整个数据集，并实现了快速过滤，尤其是对分类或重复值的过滤。
INVERTED 索引支持所有标量字段类型，如
BOOL
、
INT8
、
INT16
、
INT32
、
INT64
、
FLOAT
、
DOUBLE
、
VARCHAR
、
JSON
和
ARRAY
。不过，索引 JSON 字段的索引参数与普通标量字段略有不同。
在非 JSON 字段上创建索引
要在非 JSON 字段上创建索引，请按照以下步骤操作：
准备索引参数：
from
pymilvus
import
MilvusClient

client = MilvusClient(uri=
"http://localhost:19530"
)
# Replace with your server address
# Create an empty index parameter object
index_params = client.prepare_index_params()
添加
INVERTED
索引：
index_params.add_index(
    field_name=
"category"
,
# Name of the field to index
index_type=
"INVERTED"
,
# Specify INVERTED index type
index_name=
"category_index"
# Give your index a name
)
创建索引：
client.create_index(
    collection_name=
"my_collection"
,
# Replace with your collection name
index_params=index_params
)
在 JSON 字段上创建索引
Compatible with Milvus 2.5.11+
您还可以在 JSON 字段内的特定路径上创建 INVERTED 索引。这需要额外的参数来指定 JSON 路径和数据类型：
# Build index params
index_params.add_index(
    field_name=
"metadata"
,
# JSON field name
index_type=
"INVERTED"
,
index_name=
"metadata_category_index"
,
params={
"json_path"
:
"metadata[\"category\"]"
,
# Path to the JSON key
"json_cast_type"
:
"varchar"
# Data type to cast to during indexing
}
)
# Create index
client.create_index(
    collection_name=
"my_collection"
,
# Replace with your collection name
index_params=index_params
)
有关 JSON 字段索引的详细信息，包括支持的路径、数据类型和限制，请参阅
JSON 索引
。
删除索引
使用
drop_index()
方法从 Collections 中删除现有索引。
在
v2.6.3
或更早版本中，删除标量索引前必须释放 Collections。
从
v2.6.4
或更高版本开始，一旦不再需要标量索引，就可以直接删除，无需先释放 Collections。
client.drop_index(
    collection_name=
"my_collection"
,
# Name of the collection
index_name=
"category_index"
# Name of the index to drop
)
最佳实践
加载数据后创建索引
：在已包含数据的 Collections 上建立索引，以提高性能
使用描述性索引名称
：选择能清楚表明字段和目的的名称
监控索引性能
：在创建索引前后检查查询性能
考虑您的查询模式
：在您经常过滤的字段上创建索引
下一步
了解
其他索引类型
有关
JSON
索引的高级应用场景，请参阅 JSON 索引