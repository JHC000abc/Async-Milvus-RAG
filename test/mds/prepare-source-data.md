准备源数据
本页讨论的是在开始将数据批量插入 Collections 之前应该考虑的事项。
开始之前
目标 Collections 需要将源数据映射到其 Schema。下图显示了如何将可接受的源数据映射到目标 Collections 的模式。
将数据映射到 Schema
您应仔细检查数据，并据此设计目标 Collections 的模式。
以上图中的 JSON 数据为例，行列表中有两个实体，每个行有六个字段。Collections 模式选择性地包括四个：
ID
、
向量
、
标量_1
和
标量_2
。
在设计 Schema 时，还有两点需要考虑：
是否启用自动识别
id
字段作为 Collections 的主字段。要使主字段自动递增，可以在 Schema 中启用
AutoID
。在这种情况下，应从源数据的每一行中排除
id
字段。
是否启用动态字段
如果模式启用了动态字段，目标 Collections 还可以存储其预定义模式中未包含的字段。
$meta
字段是一个预留 JSON 字段，用于以键值对形式保存动态字段及其值。在上图中，字段
dynamic_field_1
和
dynamic_field_2
及其值将作为键值对保存在
$meta
字段中。
下面的代码展示了如何为上图所示的 Collections 设置 Schema。
要获取更多信息，请参阅
create_schema()
和
add_field()
以获取更多信息。
要获取更多信息，请参阅
CollectionSchema
以获取更多信息。
Python
Java
from
pymilvus
import
MilvusClient, DataType
# You need to work out a collection schema out of your dataset.
schema = MilvusClient.create_schema(
    auto_id=
False
,
    enable_dynamic_field=
True
)

DIM =
512
schema.add_field(field_name=
"id"
, datatype=DataType.INT64, is_primary=
True
),
schema.add_field(field_name=
"bool"
, datatype=DataType.BOOL),
schema.add_field(field_name=
"int8"
, datatype=DataType.INT8),
schema.add_field(field_name=
"int16"
, datatype=DataType.INT16),
schema.add_field(field_name=
"int32"
, datatype=DataType.INT32),
schema.add_field(field_name=
"int64"
, datatype=DataType.INT64),
schema.add_field(field_name=
"float"
, datatype=DataType.FLOAT),
schema.add_field(field_name=
"double"
, datatype=DataType.DOUBLE),
schema.add_field(field_name=
"varchar"
, datatype=DataType.VARCHAR, max_length=
512
),
schema.add_field(field_name=
"json"
, datatype=DataType.JSON),
schema.add_field(field_name=
"array_str"
, datatype=DataType.ARRAY, max_capacity=
100
, element_type=DataType.VARCHAR, max_length=
128
)
schema.add_field(field_name=
"array_int"
, datatype=DataType.ARRAY, max_capacity=
100
, element_type=DataType.INT64)
schema.add_field(field_name=
"float_vector"
, datatype=DataType.FLOAT_VECTOR, dim=DIM),
schema.add_field(field_name=
"binary_vector"
, datatype=DataType.BINARY_VECTOR, dim=DIM),
schema.add_field(field_name=
"float16_vector"
, datatype=DataType.FLOAT16_VECTOR, dim=DIM),
# schema.add_field(field_name="bfloat16_vector", datatype=DataType.BFLOAT16_VECTOR, dim=DIM),
schema.add_field(field_name=
"sparse_vector"
, datatype=DataType.SPARSE_FLOAT_VECTOR)

schema.verify()
print
(schema)
import
com.google.gson.Gson;
import
com.google.gson.JsonObject;
import
io.milvus.bulkwriter.BulkImport;
import
io.milvus.bulkwriter.RemoteBulkWriter;
import
io.milvus.bulkwriter.RemoteBulkWriterParam;
import
io.milvus.bulkwriter.common.clientenum.BulkFileType;
import
io.milvus.bulkwriter.common.clientenum.CloudStorage;
import
io.milvus.bulkwriter.connect.S3ConnectParam;
import
io.milvus.bulkwriter.connect.StorageConnectParam;
import
io.milvus.bulkwriter.request.describe.MilvusDescribeImportRequest;
import
io.milvus.bulkwriter.request.import_.MilvusImportRequest;
import
io.milvus.bulkwriter.request.list.MilvusListImportJobsRequest;
import
io.milvus.common.utils.Float16Utils;
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.common.DataType;
import
io.milvus.v2.service.collection.request.*;
import
java.io.IOException;
import
java.nio.ByteBuffer;
import
java.util.*;
import
java.util.concurrent.TimeUnit;
private
static
final
String
MINIO_ENDPOINT
=
CloudStorage.MINIO.getEndpoint(
"http://127.0.0.1:9000"
);
private
static
final
String
BUCKET_NAME
=
"a-bucket"
;
private
static
final
String
ACCESS_KEY
=
"minioadmin"
;
private
static
final
String
SECRET_KEY
=
"minioadmin"
;
private
static
final
Integer
DIM
=
512
;
private
static
final
Gson
GSON_INSTANCE
=
new
Gson
();
private
static
CreateCollectionReq.CollectionSchema
createSchema
()
{
    CreateCollectionReq.
CollectionSchema
schema
=
CreateCollectionReq.CollectionSchema.builder()
        .enableDynamicField(
true
)
        .build();
    schema.addField(AddFieldReq.builder()
            .fieldName(
"id"
)
            .dataType(io.milvus.v2.common.DataType.Int64)
            .isPrimaryKey(Boolean.TRUE)
            .autoID(
false
)
            .build());
    schema.addField(AddFieldReq.builder()
            .fieldName(
"bool"
)
            .dataType(DataType.Bool)
            .build());
    schema.addField(AddFieldReq.builder()
            .fieldName(
"int8"
)
            .dataType(DataType.Int8)
            .build());
    schema.addField(AddFieldReq.builder()
            .fieldName(
"int16"
)
            .dataType(DataType.Int16)
            .build());
    schema.addField(AddFieldReq.builder()
            .fieldName(
"int32"
)
            .dataType(DataType.Int32)
            .build());
    schema.addField(AddFieldReq.builder()
            .fieldName(
"int64"
)
            .dataType(DataType.Int64)
            .build());
    schema.addField(AddFieldReq.builder()
            .fieldName(
"float"
)
            .dataType(DataType.Float)
            .build());
    schema.addField(AddFieldReq.builder()
            .fieldName(
"double"
)
            .dataType(DataType.Double)
            .build());
    schema.addField(AddFieldReq.builder()
            .fieldName(
"varchar"
)
            .dataType(DataType.VarChar)
            .maxLength(
512
)
            .build());
    schema.addField(AddFieldReq.builder()
            .fieldName(
"json"
)
            .dataType(io.milvus.v2.common.DataType.JSON)
            .build());
    schema.addField(AddFieldReq.builder()
            .fieldName(
"array_int"
)
            .dataType(io.milvus.v2.common.DataType.Array)
            .maxCapacity(
100
)
            .elementType(io.milvus.v2.common.DataType.Int64)
            .build());
    schema.addField(AddFieldReq.builder()
            .fieldName(
"array_str"
)
            .dataType(io.milvus.v2.common.DataType.Array)
            .maxCapacity(
100
)
            .elementType(io.milvus.v2.common.DataType.VarChar)
            .maxLength(
128
)
            .build());
    schema.addField(AddFieldReq.builder()
            .fieldName(
"float_vector"
)
            .dataType(io.milvus.v2.common.DataType.FloatVector)
            .dimension(DIM)
            .build());
    schema.addField(AddFieldReq.builder()
            .fieldName(
"binary_vector"
)
            .dataType(io.milvus.v2.common.DataType.BinaryVector)
            .dimension(DIM)
            .build());
    schema.addField(AddFieldReq.builder()
            .fieldName(
"float16_vector"
)
            .dataType(io.milvus.v2.common.DataType.Float16Vector)
            .dimension(DIM)
            .build());
    schema.addField(AddFieldReq.builder()
            .fieldName(
"sparse_vector"
)
            .dataType(io.milvus.v2.common.DataType.SparseFloatVector)
            .build());
return
schema;
}
设置 BulkWriter
BulkWriter
是一种工具，用于将原始数据集转换为适合通过 RESTful Import API 导入的格式。它提供两种类型的写入器：
本地写入器（LocalBulkWriter
）：读取指定的数据集，并将其转换为易于使用的格式。
远程批量写入器
：执行与 LocalBulkWriter 相同的任务，但会将转换后的数据文件额外传输到指定的远程对象存储桶。
RemoteBulkWriter
与
LocalBulkWriter
的不同之处在于，
RemoteBulkWriter
会将转换后的数据文件传输到目标对象存储桶。
设置 LocalBulkWriter
LocalBulkWriter
会追加源数据集中的行，并将其提交到指定格式的本地文件中。
Python
Java
from
pymilvus.bulk_writer
import
LocalBulkWriter, BulkFileType
# Use `from pymilvus import LocalBulkWriter, BulkFileType`
# when you use pymilvus earlier than 2.4.2
writer = LocalBulkWriter(
    schema=schema,
    local_path=
'.'
,
    segment_size=
512
*
1024
*
1024
,
# Default value
file_type=BulkFileType.PARQUET
)
import
io.milvus.bulkwriter.LocalBulkWriter;
import
io.milvus.bulkwriter.LocalBulkWriterParam;
import
io.milvus.bulkwriter.common.clientenum.BulkFileType;
LocalBulkWriterParam
localBulkWriterParam
=
LocalBulkWriterParam.newBuilder()
    .withCollectionSchema(schema)
    .withLocalPath(
"."
)
    .withChunkSize(
512
*
1024
*
1024
)
    .withFileType(BulkFileType.PARQUET)
    .build();
LocalBulkWriter
localBulkWriter
=
new
LocalBulkWriter
(localBulkWriterParam);
创建
LocalBulkWriter
时，你应该
在
schema
中引用已创建的 Schema。
将
local_path
设置为输出目录。
将
file_type
设置为输出文件类型。
如果您的数据集包含大量记录，建议您将
segment_size
设置为适当的值，以分割数据。
有关参数设置的详细信息，请参阅 SDK 参考资料中的
LocalBulkWriter
。
创建
LocalBulkWriter
时，应
在
CollectionSchema()
中引用已创建的 Schema 。
在
withLocalPath()
中设置输出目录。
在
withFileType()
中设置输出文件类型。
如果您的数据集包含大量记录，建议您通过将
withChunkSize()
设置为适当的值来分割数据。
有关参数设置的详细信息，请参阅 SDK 参考资料中的 LocalBulkWriter。
设置 RemoteBulkWriter
RemoteBulkWriter
不会将添加的数据提交到本地文件，而是将它们提交到远程存储桶。因此，在创建
RemoteBulkWriter
之前，你应该先设置一个
ConnectParam
对象。
Python
Java
from
pymilvus.bulk_writer
import
RemoteBulkWriter
# Use `from pymilvus import RemoteBulkWriter`
# when you use pymilvus earlier than 2.4.2
# Third-party constants
ACCESS_KEY=
"minioadmin"
SECRET_KEY=
"minioadmin"
BUCKET_NAME=
"a-bucket"
# Connections parameters to access the remote bucket
conn = RemoteBulkWriter.S3ConnectParam(
    endpoint=
"localhost:9000"
,
# the default MinIO service started along with Milvus
access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    bucket_name=BUCKET_NAME,
    secure=
False
)
from
pymilvus.bulk_writer
import
BulkFileType
# Use `from pymilvus import BulkFileType`
# when you use pymilvus earlier than 2.4.2
writer = RemoteBulkWriter(
    schema=schema,
    remote_path=
"/"
,
    connect_param=conn,
    file_type=BulkFileType.PARQUET
)
print
(
'bulk writer created.'
)
private
static
RemoteBulkWriter
createRemoteBulkWriter
(CreateCollectionReq.CollectionSchema collectionSchema)
throws
IOException {
StorageConnectParam
connectParam
=
S3ConnectParam.newBuilder()
            .withEndpoint(MINIO_ENDPOINT)
            .withBucketName(BUCKET_NAME)
            .withAccessKey(ACCESS_KEY)
            .withSecretKey(SECRET_KEY)
            .build();
RemoteBulkWriterParam
bulkWriterParam
=
RemoteBulkWriterParam.newBuilder()
            .withCollectionSchema(collectionSchema)
            .withRemotePath(
"/"
)
            .withConnectParam(connectParam)
            .withFileType(BulkFileType.PARQUET)
            .build();
return
new
RemoteBulkWriter
(bulkWriterParam);
}
一旦连接参数准备就绪，你就可以在
RemoteBulkWriter
中引用它，如下所示：
Python
Java
from
pymilvus.bulk_writer
import
BulkFileType
# Use `from pymilvus import BulkFileType`
# when you use pymilvus earlier than 2.4.2
writer = RemoteBulkWriter(
    schema=schema,
    remote_path=
"/"
,
    connect_param=conn,
    file_type=BulkFileType.PARQUET
)
import
io.milvus.bulkwriter.RemoteBulkWriter;
import
io.milvus.bulkwriter.RemoteBulkWriterParam;
RemoteBulkWriterParam
remoteBulkWriterParam
=
RemoteBulkWriterParam.newBuilder()
    .withCollectionSchema(schema)
    .withConnectParam(storageConnectParam)
    .withChunkSize(
512
*
1024
*
1024
)
    .withRemotePath(
"/"
)
    .withFileType(BulkFileType.PARQUET)
    .build();
RemoteBulkWriter
remoteBulkWriter
=
new
RemoteBulkWriter
(remoteBulkWriterParam);
除了
connect_param
之外，创建
RemoteBulkWriter
的参数与创建
LocalBulkWriter
的参数基本相同。有关参数设置的详细信息，请参阅 SDK 参考资料中的
RemoteBulkWriter
和
ConnectParam
。
除
StorageConnectParam
外，创建
RemoteBulkWriter
的参数与创建
LocalBulkWriter
的参数基本相同。有关参数设置的详细信息，请参阅 SDK 参考资料中的 RemoteBulkWriter 和 StorageConnectParam。
开始写入
BulkWriter
有两个方法：
append_row()
从源数据集添加记录，以及
commit()
将添加的记录提交到本地文件或远程存储桶。
BulkWriter
有两个方法：
appendRow()
从源数据集添加行，
commit()
将添加的行提交到本地文件或远程数据桶。
为演示起见，下面的代码添加了随机生成的数据。
Python
Java
import
random, string, json
import
numpy
as
np
import
tensorflow
as
tf
def
generate_random_str
(
length=
5
):
    letters = string.ascii_uppercase
    digits = string.digits
return
''
.join(random.choices(letters + digits, k=length))
# optional input for binary vector:
# 1. list of int such as [1, 0, 1, 1, 0, 0, 1, 0]
# 2. numpy array of uint8
def
gen_binary_vector
(
to_numpy_arr
):
    raw_vector = [random.randint(
0
,
1
)
for
i
in
range
(DIM)]
if
to_numpy_arr:
return
np.packbits(raw_vector, axis=-
1
)
return
raw_vector
# optional input for float vector:
# 1. list of float such as [0.56, 1.859, 6.55, 9.45]
# 2. numpy array of float32
def
gen_float_vector
(
to_numpy_arr
):
    raw_vector = [random.random()
for
_
in
range
(DIM)]
if
to_numpy_arr:
return
np.array(raw_vector, dtype=
"float32"
)
return
raw_vector
# # optional input for bfloat16 vector:
# # 1. list of float such as [0.56, 1.859, 6.55, 9.45]
# # 2. numpy array of bfloat16
# def gen_bf16_vector(to_numpy_arr):
#     raw_vector = [random.random() for _ in range(DIM)]
#     if to_numpy_arr:
#         return tf.cast(raw_vector, dtype=tf.bfloat16).numpy()
#     return raw_vector
# optional input for float16 vector:
# 1. list of float such as [0.56, 1.859, 6.55, 9.45]
# 2. numpy array of float16
def
gen_fp16_vector
(
to_numpy_arr
):
    raw_vector = [random.random()
for
_
in
range
(DIM)]
if
to_numpy_arr:
return
np.array(raw_vector, dtype=np.float16)
return
raw_vector
# optional input for sparse vector:
# only accepts dict like {2: 13.23, 45: 0.54} or {"indices": [1, 2], "values": [0.1, 0.2]}
# note: no need to sort the keys
def
gen_sparse_vector
(
pair_dict:
bool
):
    raw_vector = {}
    dim = random.randint(
2
,
20
)
if
pair_dict:
        raw_vector[
"indices"
] = [i
for
i
in
range
(dim)]
        raw_vector[
"values"
] = [random.random()
for
_
in
range
(dim)]
else
:
for
i
in
range
(dim):
            raw_vector[i] = random.random()
return
raw_vector
for
i
in
range
(
10000
):
    writer.append_row({
"id"
: np.int64(i),
"bool"
:
True
if
i %
3
==
0
else
False
,
"int8"
: np.int8(i%
128
),
"int16"
: np.int16(i%
1000
),
"int32"
: np.int32(i%
100000
),
"int64"
: np.int64(i),
"float"
: np.float32(i/
3
),
"double"
: np.float64(i/
7
),
"varchar"
:
f"varchar_
{i}
"
,
"json"
: json.dumps({
"dummy"
: i,
"ok"
:
f"name_
{i}
"
}),
"array_str"
: np.array([
f"str_
{k}
"
for
k
in
range
(
5
)], np.dtype(
"str"
)),
"array_int"
: np.array([k
for
k
in
range
(
10
)], np.dtype(
"int64"
)),
"float_vector"
: gen_float_vector(
True
),
"binary_vector"
: gen_binary_vector(
True
),
"float16_vector"
: gen_fp16_vector(
True
),
# "bfloat16_vector": gen_bf16_vector(True),
"sparse_vector"
: gen_sparse_vector(
True
),
f"dynamic_
{i}
"
: i,
    })
if
(i+
1
)%
1000
==
0
:
        writer.commit()
print
(
'committed'
)
print
(writer.batch_files)
private
static
byte
[] genBinaryVector() {
Random
ran
=
new
Random
();
int
byteCount
=
DIM /
8
;
ByteBuffer
vector
=
ByteBuffer.allocate(byteCount);
for
(
int
i
=
0
; i < byteCount; ++i) {
        vector.put((
byte
) ran.nextInt(Byte.MAX_VALUE));
    }
return
vector.array();
}
private
static
List<Float>
genFloatVector
()
{
Random
ran
=
new
Random
();
    List<Float> vector =
new
ArrayList
<>();
for
(
int
i
=
0
; i < DIM; ++i) {
        vector.add(ran.nextFloat());
    }
return
vector;
}
private
static
byte
[] genFloat16Vector() {
    List<Float> originalVector = genFloatVector();
return
Float16Utils.f32VectorToFp16Buffer(originalVector).array();
}
private
static
SortedMap<Long, Float>
genSparseVector
()
{
Random
ran
=
new
Random
();
    SortedMap<Long, Float> sparse =
new
TreeMap
<>();
int
dim
=
ran.nextInt(
18
) +
2
;
// [2, 20)
for
(
int
i
=
0
; i < dim; ++i) {
        sparse.put((
long
)ran.nextInt(
1000000
), ran.nextFloat());
    }
return
sparse;
}
private
static
List<String>
genStringArray
(
int
length)
{
    List<String> arr =
new
ArrayList
<>();
for
(
int
i
=
0
; i < length; i++) {
        arr.add(
"str_"
+ i);
    }
return
arr;
}
private
static
List<Long>
genIntArray
(
int
length)
{
    List<Long> arr =
new
ArrayList
<>();
for
(
long
i
=
0
; i < length; i++) {
        arr.add(i);
    }
return
arr;
}
private
static
RemoteBulkWriter
createRemoteBulkWriter
(CreateCollectionReq.CollectionSchema collectionSchema)
throws
IOException {
StorageConnectParam
connectParam
=
S3ConnectParam.newBuilder()
            .withEndpoint(MINIO_ENDPOINT)
            .withBucketName(BUCKET_NAME)
            .withAccessKey(ACCESS_KEY)
            .withSecretKey(SECRET_KEY)
            .build();
RemoteBulkWriterParam
bulkWriterParam
=
RemoteBulkWriterParam.newBuilder()
            .withCollectionSchema(collectionSchema)
            .withRemotePath(
"/"
)
            .withConnectParam(connectParam)
            .withFileType(BulkFileType.PARQUET)
            .build();
return
new
RemoteBulkWriter
(bulkWriterParam);
}
private
static
List<List<String>>
uploadData
()
throws
Exception {
    CreateCollectionReq.
CollectionSchema
collectionSchema
=
createSchema();
try
(
RemoteBulkWriter
remoteBulkWriter
=
createRemoteBulkWriter(collectionSchema)) {
for
(
int
i
=
0
; i <
10000
; ++i) {
JsonObject
rowObject
=
new
JsonObject
();

            rowObject.addProperty(
"id"
, i);
            rowObject.addProperty(
"bool"
, i %
3
==
0
);
            rowObject.addProperty(
"int8"
, i %
128
);
            rowObject.addProperty(
"int16"
, i %
1000
);
            rowObject.addProperty(
"int32"
, i %
100000
);
            rowObject.addProperty(
"int64"
, i);
            rowObject.addProperty(
"float"
, i /
3
);
            rowObject.addProperty(
"double"
, i /
7
);
            rowObject.addProperty(
"varchar"
,
"varchar_"
+ i);
            rowObject.addProperty(
"json"
, String.format(
"{\"dummy\": %s, \"ok\": \"name_%s\"}"
, i, i));
            rowObject.add(
"array_str"
, GSON_INSTANCE.toJsonTree(genStringArray(
5
)));
            rowObject.add(
"array_int"
, GSON_INSTANCE.toJsonTree(genIntArray(
10
)));
            rowObject.add(
"float_vector"
, GSON_INSTANCE.toJsonTree(genFloatVector()));
            rowObject.add(
"binary_vector"
, GSON_INSTANCE.toJsonTree(genBinaryVector()));
            rowObject.add(
"float16_vector"
, GSON_INSTANCE.toJsonTree(genFloat16Vector()));
            rowObject.add(
"sparse_vector"
, GSON_INSTANCE.toJsonTree(genSparseVector()));
            rowObject.addProperty(
"dynamic"
,
"dynamic_"
+ i);

            remoteBulkWriter.appendRow(rowObject);
if
((i+
1
)%
1000
==
0
) {
                remoteBulkWriter.commit(
false
);
            }
        }

        List<List<String>> batchFiles = remoteBulkWriter.getBatchFiles();
        System.out.println(batchFiles);
return
batchFiles;
    }
catch
(Exception e) {
throw
e;
    }
}
public
static
void
main
(String[] args)
throws
Exception {
    List<List<String>> batchFiles = uploadData();
}
验证结果
要检查结果，可以通过打印写入器的
batch_files
属性来获取实际输出路径。
要检查结果，可通过打印写入器的
getBatchFiles()
方法获取实际输出路径。
Python
Java
print
(writer.batch_files)
# [['d4220a9e-45be-4ccb-8cb5-bf09304b9f23/1.parquet'],
#  ['d4220a9e-45be-4ccb-8cb5-bf09304b9f23/2.parquet']]
// localBulkWriter.getBatchFiles();
remoteBulkWriter.getBatchFiles();
//
// Close the BulkWriter
try
{
    localBulkWriter.close();
    remoteBulkWriter.close();            
}
catch
(Exception e) {
//
TODO:
handle exception
e.printStackTrace();
}
BulkWriter
会生成一个 UUID，在提供的输出目录中使用 UUID 创建一个子文件夹，并将所有生成的文件放入该子文件夹中。
单击此处
下载准备好的示例数据。
可能的文件夹结构如下
# JSON
├── folder
│   └── 45ae1139-1d87-4aff-85f5-0039111f9e6b
│       └── 1.json
# Parquet
├── folder
│   └── 45ae1139-1d87-4aff-85f5-0039111f9e6b
│       └── 1.parquet