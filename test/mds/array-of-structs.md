结构体数组
Compatible with Milvus 2.6.4+
实体中的 "结构数组 "字段存储了一组有序的结构元素。数组中的每个 Struct 都共享相同的预定义 Schema，由多个向量和标量字段组成。
下面是一个包含 Array of Structs 字段的 Collections 实体示例。
{
'id'
:
0
,
'title'
:
'Walden'
,
'title_vector'
:
[
0.1
,
0.2
,
0.3
,
0.4
,
0.5
]
,
'author'
:
'Henry David Thoreau'
,
'year_of_publication'
:
1845
,
'chunks'
:
[
{
'text'
:
'When I wrote the following pages
,
or rather the bulk of them...'
,
'text_vector'
:
[
0.3
,
0.2
,
0.3
,
0.2
,
0.5
]
,
'chapter'
:
'Economy'
,
}
,
{
'text'
:
'I would fain say something
,
not so much concerning the Chinese and...'
,
'text_vector'
:
[
0.7
,
0.4
,
0.2
,
0.7
,
0.8
]
,
'chapter'
:
'Economy'
}
]
// hightlight-end
}
在上面的示例中，
chunks
字段是一个数组结构体字段，每个结构体元素都包含自己的字段，即
text
、
text_vector
和
chapter
。
限制
数据类型
创建 Collections 时，可以使用 Struct 类型作为 Array 字段中元素的数据类型。但是，您不能将 Struct 数组添加到现有的 Collections 中，而且 Milvus 不支持使用 Struct 类型作为 Collections 字段的数据类型。
数组字段中的 Struct 共享相同的 Schema，这应该在创建数组字段时定义。
Struct 模式包含向量和标量字段，如下表所示：
字段类型
数据类型
向量
FLOAT_VECTOR
标量
VARCHAR
INT8/16/32/64
FLOAT
DOUBLE
BOOLEAN
保持 Collections 层面和 Structs 组合中的向量字段数量不大于或等于 10。
可归零和默认值
数组结构体字段不可为空，也不接受任何默认值。
函数
不能使用函数从 Struct 中的标量字段派生出向量字段。
索引类型和度量类型
必须为 Collections 中的所有向量场建立索引。要对 Structs 数组中的向量场进行索引，Milvus 使用嵌入列表来组织每个 Struct 元素中的向量嵌入，并对整个嵌入列表作为一个整体进行索引。
你可以使用
AUTOINDEX
或
HNSW
作为索引类型，并使用下面列出的任何度量类型来为一个 Array of Structs 字段中的嵌入列表建立索引。
索引类型
度量类型
备注
AUTOINDEX
(或
HNSW
)
MAX_SIM_COSINE
适用于以下类型的嵌入列表：
FLOAT_VECTOR
MAX_SIM_IP
MAX_SIM_L2
结构数组字段中的标量字段不支持索引。
倒插数据
结构体在合并模式下不支持向上插入。但是，您仍然可以在覆盖模式下执行上插入操作，以更新 Structs 中的数据。有关合并模式下的
upsert
和覆盖模式下的
upsert
之间差异的详细信息，请参阅 "
upsert 实体
"。
标量过滤
在搜索和查询的过滤表达式中，不能使用结构体数组或其结构体元素中的任何字段。
添加结构数组
要在 Milvus 中使用结构数组，需要在创建 Collections 时定义一个数组字段，并将其元素的数据类型设置为 Struct。具体过程如下
将字段作为数组字段添加到 Collections Schema 时，将字段的数据类型设置为
DataType.ARRAY
。
将字段的
element_type
属性设置为
DataType.STRUCT
，使字段成为结构数组。
创建一个 Struct 模式并包含所需字段。然后，在字段的
struct_schema
属性中引用 Struct 模式。
将字段的
max_capacity
属性设置为适当的值，以指定每个实体在该字段中可包含的最大 Struct 数量。
(可选
）可以为 Struct 元素中的任何字段设置
mmap.enabled
，以平衡 Struct 中的冷热数据。
下面是如何定义包含 Struct 数组的 Collections 模式：
Python
Java
Go
NodeJS
cURL
from
pymilvus
import
MilvusClient, DataType

client = MilvusClient(
    uri=
"http://localhost:19530"
,
    token=
"root:Milvus"
)

schema = client.create_schema()
# add the primary field to the collection
schema.add_field(field_name=
"id"
, datatype=DataType.INT64, is_primary=
True
, auto_id=
True
)
# add some scalar fields to the collection
schema.add_field(field_name=
"title"
, datatype=DataType.VARCHAR, max_length=
512
)
schema.add_field(field_name=
"author"
, datatype=DataType.VARCHAR, max_length=
512
)
schema.add_field(field_name=
"year_of_publication"
, datatype=DataType.INT64)
# add a vector field to the collection
schema.add_field(field_name=
"title_vector"
, datatype=DataType.FLOAT_VECTOR, dim=
5
)
# Create a struct schema
struct_schema = client.create_struct_field_schema()
# add a scalar field to the struct
struct_schema.add_field(
"text"
, DataType.VARCHAR, max_length=
65535
)
struct_schema.add_field(
"chapter"
, DataType.VARCHAR, max_length=
512
)
# add a vector field to the struct with mmap enabled
struct_schema.add_field(
"text_vector"
, DataType.FLOAT_VECTOR, mmap_enabled=
True
, dim=
5
)
# reference the struct schema in an Array field with its
# element type set to `DataType.STRUCT`
schema.add_field(
"chunks"
, datatype=DataType.ARRAY, element_type=DataType.STRUCT,
struct_schema=struct_schema, max_capacity=
1000
)
import
io.milvus.v2.common.DataType;
import
io.milvus.v2.service.collection.request.AddFieldReq;
import
io.milvus.v2.service.collection.request.CreateCollectionReq;

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
"title"
)
        .dataType(DataType.VarChar)
        .maxLength(
512
)
        .build());
collectionSchema.addField(AddFieldReq.builder()
        .fieldName(
"author"
)
        .dataType(DataType.VarChar)
        .maxLength(
512
)
        .build());
collectionSchema.addField(AddFieldReq.builder()
        .fieldName(
"year_of_publication"
)
        .dataType(DataType.Int64)
        .build());
collectionSchema.addField(AddFieldReq.builder()
        .fieldName(
"title_vector"
)
        .dataType(DataType.FloatVector)
        .dimension(
5
)
        .build());

Map<String, String> params =
new
HashMap
<>();
params.put(
"mmap_enabled"
,
"true"
);
collectionSchema.addField(AddFieldReq.builder()
        .fieldName(
"chunks"
)
        .dataType(DataType.Array)
        .elementType(DataType.Struct)
        .maxCapacity(
1000
)
        .addStructField(AddFieldReq.builder()
                .fieldName(
"text"
)
                .dataType(DataType.VarChar)
                .maxLength(
65535
)
                .build())
        .addStructField(AddFieldReq.builder()
                .fieldName(
"chapter"
)
                .dataType(DataType.VarChar)
                .maxLength(
512
)
                .build())
        .addStructField(AddFieldReq.builder()
                .fieldName(
"text_vector"
)
                .dataType(DataType.FloatVector)
                .dimension(VECTOR_DIM)
                .typeParams(params)
                .build())
        .build());
// go
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
milvusClient =
new
MilvusClient
(
"http://localhost:19530"
);
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
INT64
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
"title"
,
data_type
:
DataType
.
VARCHAR
,
max_length
:
512
,
  },
  {
name
:
"author"
,
data_type
:
DataType
.
VARCHAR
,
max_length
:
512
,
  },
  {
name
:
"year_of_publication"
,
data_type
:
DataType
.
INT64
,
  },
  {
name
:
"title_vector"
,
data_type
:
DataType
.
FLOAT_VECTOR
,
dim
:
5
,
  },
{
name
:
"chunks"
,
data_type
:
DataType
.
ARRAY
,
element_type
:
DataType
.
STRUCT
,
fields
: [
{
name
:
"text"
,
data_type
:
DataType
.
VARCHAR
,
max_length
:
65535
,
},
{
name
:
"chapter"
,
data_type
:
DataType
.
VARCHAR
,
max_length
:
512
,
},
{
name
:
"text_vector"
,
data_type
:
DataType
.
FLOAT_VECTOR
,
dim
:
5
,
mmap_enabled
:
true
,
},
],
max_capacity
:
1000
,
},
];
# restful
SCHEMA=
'{
  "autoID": true,
  "fields": [
    {
      "fieldName": "id",
      "dataType": "Int64",
      "isPrimary": true
    },
    {
      "fieldName": "title",
      "dataType": "VarChar",
      "elementTypeParams": { "max_length": "512" }
    },
    {
      "fieldName": "author",
      "dataType": "VarChar",
      "elementTypeParams": { "max_length": "512" }
    },
    {
      "fieldName": "year_of_publication",
      "dataType": "Int64"
    },
    {
      "fieldName": "title_vector",
      "dataType": "FloatVector",
      "elementTypeParams": { "dim": "5" }
    }
  ],
  "structArrayFields": [
    {
      "name": "chunks",
      "description": "Array of document chunks with text and vectors",
      "elementTypeParams":{
         "max_capacity": 1000
      },
      "fields": [
        {
          "fieldName": "text",
          "dataType": "VarChar",
          "elementTypeParams": { "max_length": "65535" }
        },
        {
          "fieldName": "chapter",
          "dataType": "VarChar",
          "elementTypeParams": { "max_length": "512" }
        },
        {
          "fieldName": "text_vector",
          "dataType": "FloatVector",
          "elementTypeParams": {
            "dim": "5",
            "mmap_enabled": "true"
          }
        }
      ]
    }
  ]
}'
上述代码示例中高亮显示的几行说明了在 Collections 模式中包含 Struct 数组的过程。
设置索引参数
所有向量字段都必须设置索引，包括 Collections 中的向量字段和元素 Struct 中定义的向量字段。
适用的索引参数因使用的索引类型而异。有关适用索引参数的详细信息，请参阅
Index Explained
和所选索引类型的特定文档页面。
要为嵌入列表建立索引，需要将其索引类型设为
AUTOINDEX
或
HNSW
，并使用
MAX_SIM_COSINE
作为 Milvus 的度量类型，以衡量嵌入列表之间的相似性。
Python
Java
Go
NodeJS
cURL
# Create index parameters
index_params = client.prepare_index_params()
# Create an index for the vector field in the collection
index_params.add_index(
    field_name=
"title_vector"
,
    index_type=
"AUTOINDEX"
,
    metric_type=
"L2"
,
)
# Create an index for the vector field in the element Struct
index_params.add_index(
field_name=
"chunks[text_vector]"
,
index_type=
"AUTOINDEX"
,
metric_type=
"MAX_SIM_COSINE"
,
)
import
io.milvus.v2.common.IndexParam;

List<IndexParam> indexParams =
new
ArrayList
<>();
indexParams.add(IndexParam.builder()
        .fieldName(
"title_vector"
)
        .indexType(IndexParam.IndexType.AUTOINDEX)
        .metricType(IndexParam.MetricType.L2)
        .build());
indexParams.add(IndexParam.builder()
        .fieldName(
"chunks[text_vector]"
)
        .indexType(IndexParam.IndexType.AUTOINDEX)
        .metricType(IndexParam.MetricType.MAX_SIM_COSINE)
        .build());
// go
await
milvusClient.
createCollection
({
collection_name
:
"books"
,
fields
: schema,
});
const
indexParams = [
  {
field_name
:
"title_vector"
,
index_type
:
"AUTOINDEX"
,
metric_type
:
"L2"
,
  },
{
field_name
:
"chunks[text_vector]"
,
index_type
:
"AUTOINDEX"
,
metric_type
:
"MAX_SIM_COSINE"
,
},
];
# restful
INDEX_PARAMS=
'[
  {
    "fieldName": "title_vector",
    "indexName": "title_vector_index",
    "indexType": "AUTOINDEX",
    "metricType": "L2"
  },
  {
    "fieldName": "chunks[text_vector]",
    "indexName": "chunks_text_vector_index",
    "indexType": "AUTOINDEX",
    "metricType": "MAX_SIM_COSINE"
  }
]'
创建 Collections
Schema 和索引准备就绪后，就可以创建一个包含 Array of Structs 字段的 Collection。
Python
Java
Go
NodeJS
cURL
client.create_collection(
    collection_name=
"my_collection"
,
    schema=schema,
    index_params=index_params
)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.service.collection.request.CreateCollectionReq;
MilvusClientV2
client
=
new
MilvusClientV2
(ConnectConfig.builder()
        .uri(
"http://localhost:19530"
)
        .token(
"root:Milvus"
)
        .build());
CreateCollectionReq
requestCreate
=
CreateCollectionReq.builder()
        .collectionName(
"my_collection"
)
        .collectionSchema(collectionSchema)
        .indexParams(indexParams)
        .build();
client.createCollection(requestCreate);
// go
await
milvusClient.
createCollection
({
collection_name
:
"books"
,
fields
: schema,
indexes
: indexParams,
});
# restful
curl -X POST
"http://localhost:19530/v2/vectordb/collections/create"
\
  -H
"Content-Type: application/json"
\
  -d
"{
    \"collectionName\": \"my_collection\",
    \"description\": \"A collection for storing book information with struct array chunks\",
    \"schema\":
$SCHEMA
,
    \"indexParams\":
$INDEX_PARAMS
}"
插入数据
创建 Collections 后，您可以按如下方式插入包含 Structs 数组的数据。
Python
Java
Go
NodeJS
cURL
# Sample data
data = {
'title'
:
'Walden'
,
'title_vector'
: [
0.1
,
0.2
,
0.3
,
0.4
,
0.5
],
'author'
:
'Henry David Thoreau'
,
'year_of_publication'
:
1845
,
'chunks'
: [
        {
'text'
:
'When I wrote the following pages, or rather the bulk of them...'
,
'text_vector'
: [
0.3
,
0.2
,
0.3
,
0.2
,
0.5
],
'chapter'
:
'Economy'
,
        },
        {
'text'
:
'I would fain say something, not so much concerning the Chinese and...'
,
'text_vector'
: [
0.7
,
0.4
,
0.2
,
0.7
,
0.8
],
'chapter'
:
'Economy'
}
    ]
}
# insert data
client.insert(
    collection_name=
"my_collection"
,
    data=[data]
)
import
com.google.gson.Gson;
import
com.google.gson.JsonArray;
import
com.google.gson.JsonObject;
import
io.milvus.v2.service.vector.request.InsertReq;
import
io.milvus.v2.service.vector.response.InsertResp;
Gson
gson
=
new
Gson
();
JsonObject
row
=
new
JsonObject
();
row.addProperty(
"title"
,
"Walden"
);
row.add(
"title_vector"
, gson.toJsonTree(Arrays.asList(
0.1f
,
0.2f
,
0.3f
,
0.4f
,
0.5f
)));
row.addProperty(
"author"
,
"Henry David Thoreau"
);
row.addProperty(
"year_of_publication"
,
1845
);
JsonArray
structArr
=
new
JsonArray
();
JsonObject
struct1
=
new
JsonObject
();
struct1.addProperty(
"text"
,
"When I wrote the following pages, or rather the bulk of them..."
);
struct1.add(
"text_vector"
, gson.toJsonTree(Arrays.asList(
0.3f
,
0.2f
,
0.3f
,
0.2f
,
0.5f
)));
struct1.addProperty(
"chapter"
,
"Economy"
);
structArr.add(struct1);
JsonObject
struct2
=
new
JsonObject
();
struct2.addProperty(
"text"
,
"I would fain say something, not so much concerning the Chinese and..."
);
struct2.add(
"text_vector"
, gson.toJsonTree(Arrays.asList(
0.7f
,
0.4f
,
0.2f
,
0.7f
,
0.8f
)));
struct2.addProperty(
"chapter"
,
"Economy"
);
structArr.add(struct2);

row.add(
"chunks"
, structArr);
InsertResp
insertResp
=
client.insert(InsertReq.builder()
        .collectionName(
"my_collection"
)
        .data(Collections.singletonList(row))
        .build());
// go
{
id
:
0
,
title
:
"Walden"
,
title_vector
: [
0.1
,
0.2
,
0.3
,
0.4
,
0.5
],
author
:
"Henry David Thoreau"
,
"year-of-publication"
:
1845
,
chunks
: [
      {
text
:
"When I wrote the following pages, or rather the bulk of them..."
,
text_vector
: [
0.3
,
0.2
,
0.3
,
0.2
,
0.5
],
chapter
:
"Economy"
,
      },
      {
text
:
"I would fain say something, not so much concerning the Chinese and..."
,
text_vector
: [
0.7
,
0.4
,
0.2
,
0.7
,
0.8
],
chapter
:
"Economy"
,
      },
    ],
  },
];
await
milvusClient.
insert
({
collection_name
:
"books"
,
data
: data,
});
# restful
curl -X POST
"http://localhost:19530/v2/vectordb/entities/insert"
\
  -H
"Content-Type: application/json"
\
  -d
'{
    "collectionName": "my_collection",
    "data": [
      {
        "title": "Walden",
        "title_vector": [0.1, 0.2, 0.3, 0.4, 0.5],
        "author": "Henry David Thoreau",
        "year_of_publication": 1845,
        "chunks": [
          {
            "text": "When I wrote the following pages, or rather the bulk of them...",
            "text_vector": [0.3, 0.2, 0.3, 0.2, 0.5],
            "chapter": "Economy"
          },
          {
            "text": "I would fain say something, not so much concerning the Chinese and...",
            "text_vector": [0.7, 0.4, 0.2, 0.7, 0.8],
            "chapter": "Economy"
          }
        ]
      }
    ]
  }'
需要更多数据？
import
json
import
random
from
typing
import
List
,
Dict
,
Any
# Real classic books (title, author, year)
BOOKS = [
    (
"Pride and Prejudice"
,
"Jane Austen"
,
1813
),
    (
"Moby Dick"
,
"Herman Melville"
,
1851
),
    (
"Frankenstein"
,
"Mary Shelley"
,
1818
),
    (
"The Picture of Dorian Gray"
,
"Oscar Wilde"
,
1890
),
    (
"Dracula"
,
"Bram Stoker"
,
1897
),
    (
"The Adventures of Sherlock Holmes"
,
"Arthur Conan Doyle"
,
1892
),
    (
"Alice's Adventures in Wonderland"
,
"Lewis Carroll"
,
1865
),
    (
"The Time Machine"
,
"H.G. Wells"
,
1895
),
    (
"The Scarlet Letter"
,
"Nathaniel Hawthorne"
,
1850
),
    (
"Leaves of Grass"
,
"Walt Whitman"
,
1855
),
    (
"The Brothers Karamazov"
,
"Fyodor Dostoevsky"
,
1880
),
    (
"Crime and Punishment"
,
"Fyodor Dostoevsky"
,
1866
),
    (
"Anna Karenina"
,
"Leo Tolstoy"
,
1877
),
    (
"War and Peace"
,
"Leo Tolstoy"
,
1869
),
    (
"Great Expectations"
,
"Charles Dickens"
,
1861
),
    (
"Oliver Twist"
,
"Charles Dickens"
,
1837
),
    (
"Wuthering Heights"
,
"Emily Brontë"
,
1847
),
    (
"Jane Eyre"
,
"Charlotte Brontë"
,
1847
),
    (
"The Call of the Wild"
,
"Jack London"
,
1903
),
    (
"The Jungle Book"
,
"Rudyard Kipling"
,
1894
),
]
# Common chapter names for classics
CHAPTERS = [
"Introduction"
,
"Prologue"
,
"Chapter I"
,
"Chapter II"
,
"Chapter III"
,
"Chapter IV"
,
"Chapter V"
,
"Chapter VI"
,
"Chapter VII"
,
"Chapter VIII"
,
"Chapter IX"
,
"Chapter X"
,
"Epilogue"
,
"Conclusion"
,
"Afterword"
,
"Economy"
,
"Where I Lived"
,
"Reading"
,
"Sounds"
,
"Solitude"
,
"Visitors"
,
"The Bean-Field"
,
"The Village"
,
"The Ponds"
,
"Baker Farm"
]
# Placeholder text snippets (mimicking 19th-century prose)
TEXT_SNIPPETS = [
"When I wrote the following pages, or rather the bulk of them..."
,
"I would fain say something, not so much concerning the Chinese and..."
,
"It is a truth universally acknowledged, that a single man in possession..."
,
"Call me Ishmael. Some years ago—never mind how long precisely..."
,
"It was the best of times, it was the worst of times..."
,
"All happy families are alike; each unhappy family is unhappy in its own way."
,
"Whether I shall turn out to be the hero of my own life, or whether that station..."
,
"You will rejoice to hear that no disaster has accompanied the commencement..."
,
"The world is too much with us; late and soon, getting and spending..."
,
"He was an old man who fished alone in a skiff in the Gulf Stream..."
]
def
random_vector
() ->
List
[
float
]:
return
[
round
(random.random(),
1
)
for
_
in
range
(
5
)]
def
generate_chunk
() ->
Dict
[
str
,
Any
]:
return
{
"text"
: random.choice(TEXT_SNIPPETS),
"text_vector"
: random_vector(),
"chapter"
: random.choice(CHAPTERS)
    }
def
generate_record
(
record_id:
int
) ->
Dict
[
str
,
Any
]:
    title, author, year = random.choice(BOOKS)
    num_chunks = random.randint(
1
,
5
)
# 1 to 5 chunks per book
chunks = [generate_chunk()
for
_
in
range
(num_chunks)]
return
{
"title"
: title,
"title_vector"
: random_vector(),
"author"
: author,
"year_of_publication"
: year,
"chunks"
: chunks
    }
# Generate 1000 records
data = [generate_record(i)
for
i
in
range
(
1000
)]
# Insert the generated data
client.insert(collection_name=
"my_collection"
, data=data)
针对 Structs 数组字段进行向量搜索
您可以对 Collections 和 Array of Structs 中的向量字段执行向量搜索。
具体来说，你应该将 Array of Structs 字段的名称和 Struct 元素中目标向量字段的名称串联起来，作为搜索请求中
anns_field
参数的值，并使用
EmbeddingList
来整齐地组织查询向量。
Milvus 提供的
EmbeddingList
可以帮助你更整齐地组织针对 Structs 数组中的 Embeddings 列表进行搜索的查询向量。每个
EmbeddingList
至少包含一个向量嵌入，并期望返回若干 topK 实体。
不过，
EmbeddingList
只能用于没有范围搜索或分组搜索参数的
search()
请求，更不用说
search_iterator()
请求了。
Python
Java
Go
NodeJS
cURL
from
pymilvus.client.embedding_list
import
EmbeddingList
# each query embedding list triggers a single search
embeddingList1 = EmbeddingList()
embeddingList1.add([
0.2
,
0.9
,
0.4
, -
0.3
,
0.2
])

embeddingList2 = EmbeddingList()
embeddingList2.add([-
0.2
, -
0.2
,
0.5
,
0.6
,
0.9
])
embeddingList2.add([-
0.4
,
0.3
,
0.5
,
0.8
,
0.2
])
# a search with a single embedding list
results = client.search(
    collection_name=
"my_collection"
,
    data=[ embeddingList1 ],
    anns_field=
"chunks[text_vector]"
,
    search_params={
"metric_type"
:
"MAX_SIM_COSINE"
},
    limit=
3
,
    output_fields=[
"chunks[text]"
]
)
import
io.milvus.v2.service.vector.request.data.EmbeddingList;
import
io.milvus.v2.service.vector.request.data.FloatVec;
EmbeddingList
embeddingList1
=
new
EmbeddingList
();
embeddingList1.add(
new
FloatVec
(
new
float
[]{
0.2f
,
0.9f
,
0.4f
, -
0.3f
,
0.2f
}));
EmbeddingList
embeddingList2
=
new
EmbeddingList
();
embeddingList2.add(
new
FloatVec
(
new
float
[]{-
0.2f
, -
0.2f
,
0.5f
,
0.6f
,
0.9f
}));
embeddingList2.add(
new
FloatVec
(
new
float
[]{-
0.4f
,
0.3f
,
0.5f
,
0.8f
,
0.2f
}));

Map<String, Object> params =
new
HashMap
<>();
params.put(
"metric_type"
,
"MAX_SIM_COSINE"
);
SearchResp
searchResp
=
client.search(SearchReq.builder()
        .collectionName(
"my_collection"
)
        .annsField(
"chunks[text_vector]"
)
        .data(Collections.singletonList(embeddingList1))
        .searchParams(params)
        .limit(
3
)
        .outputFields(Collections.singletonList(
"chunks[text]"
))
        .build());
// go
const
embeddingList1 = [[
0.2
,
0.9
,
0.4
, -
0.3
,
0.2
]];
const
embeddingList2 = [
  [-
0.2
, -
0.2
,
0.5
,
0.6
,
0.9
],
  [-
0.4
,
0.3
,
0.5
,
0.8
,
0.2
],
];
const
results =
await
milvusClient.
search
({
collection_name
:
"books"
,
data
: embeddingList1,
anns_field
:
"chunks[text_vector]"
,
search_params
: {
metric_type
:
"MAX_SIM_COSINE"
},
limit
:
3
,
output_fields
: [
"chunks[text]"
],
});
# restful
embeddingList1=
'[[0.2,0.9,0.4,-0.3,0.2]]'
embeddingList2=
'[[-0.2,-0.2,0.5,0.6,0.9],[-0.4,0.3,0.5,0.8,0.2]]'
curl -X POST
"http://localhost:19530/v2/vectordb/entities/search"
\
  -H
"Content-Type: application/json"
\
  -d
"{
    \"collectionName\": \"my_collection\",
    \"data\": [
$embeddingList1
],
    \"annsField\": \"chunks[text_vector]\",
    \"searchParams\": {\"metric_type\": \"MAX_SIM_COSINE\"},
    \"limit\": 3,
    \"outputFields\": [\"chunks[text]\"]
  }"
上述搜索请求使用
chunks[text_vector]
来引用 Struct 元素中的
text_vector
字段。您可以使用此语法设置
anns_field
和
output_fields
参数。
输出将是三个最相似实体的列表。
输出
# [
#     [
#         {
#             'id': 461417939772144945,
#             'distance': 0.9675756096839905,
#             'entity': {
#                 'chunks': [
#                     {'text': 'The world is too much with us; late and soon, getting and spending...'},
#                     {'text': 'All happy families are alike; each unhappy family is unhappy in its own way.'}
#                 ]
#             }
#         },
#         {
#             'id': 461417939772144965,
#             'distance': 0.9555778503417969,
#             'entity': {
#                 'chunks': [
#                     {'text': 'Call me Ishmael. Some years ago—never mind how long precisely...'},
#                     {'text': 'He was an old man who fished alone in a skiff in the Gulf Stream...'},
#                     {'text': 'When I wrote the following pages, or rather the bulk of them...'},
#                     {'text': 'It was the best of times, it was the worst of times...'},
#                     {'text': 'The world is too much with us; late and soon, getting and spending...'}
#                 ]
#             }
#         },
#         {
#             'id': 461417939772144962,
#             'distance': 0.9469035863876343,
#             'entity': {
#                 'chunks': [
#                     {'text': 'Call me Ishmael. Some years ago—never mind how long precisely...'},
#                     {'text': 'The world is too much with us; late and soon, getting and spending...'},
#                     {'text': 'He was an old man who fished alone in a skiff in the Gulf Stream...'},
#                     {'text': 'Call me Ishmael. Some years ago—never mind how long precisely...'},
#                     {'text': 'The world is too much with us; late and soon, getting and spending...'}
#                 ]
#             }
#         }
#     ]
# ]
您还可以在
data
参数中包含多个嵌入列表，以检索每个嵌入列表的搜索结果。
Python
Java
Go
NodeJS
cURL
# a search with multiple embedding lists
results = client.search(
    collection_name=
"my_collection"
,
    data=[ embeddingList1, embeddingList2 ],
    anns_field=
"chunks[text_vector]"
,
    search_params={
"metric_type"
:
"MAX_SIM_COSINE"
},
    limit=
3
,
    output_fields=[
"chunks[text]"
]
)
print
(results)
Map<String, Object> params =
new
HashMap
<>();
params.put(
"metric_type"
,
"MAX_SIM_COSINE"
);
SearchResp
searchResp
=
client.search(SearchReq.builder()
        .collectionName(
"my_collection"
)
        .annsField(
"chunks[text_vector]"
)
        .data(Arrays.asList(embeddingList1, embeddingList2))
        .searchParams(params)
        .limit(
3
)
        .outputFields(Collections.singletonList(
"chunks[text]"
))
        .build());
        
List<List<SearchResp.SearchResult>> searchResults = searchResp.getSearchResults();
for
(
int
i
=
0
; i < searchResults.size(); i++) {
    System.out.println(
"Results of No."
+ i +
" embedding list"
);
    List<SearchResp.SearchResult> results = searchResults.get(i);
for
(SearchResp.SearchResult result : results) {
        System.out.println(result);
    }
}
// go
const
results2 =
await
milvusClient.
search
({
collection_name
:
"books"
,
data
: [embeddingList1, embeddingList2],
anns_field
:
"chunks[text_vector]"
,
search_params
: {
metric_type
:
"MAX_SIM_COSINE"
},
limit
:
3
,
output_fields
: [
"chunks[text]"
],
});
# restful
curl -X POST
"http://localhost:19530/v2/vectordb/entities/search"
\
  -H
"Content-Type: application/json"
\
  -d
"{
    \"collectionName\": \"my_collection\",
    \"data\": [
$embeddingList1
,
$embeddingList2
],
    \"annsField\": \"chunks[text_vector]\",
    \"searchParams\": {\"metric_type\": \"MAX_SIM_COSINE\"},
    \"limit\": 3,
    \"outputFields\": [\"chunks[text]\"]
  }"
输出将是每个嵌入列表中三个最相似实体的列表。
输出
# [
#   [
#     {
#       'id': 461417939772144945,
#       'distance': 0.9675756096839905,
#       'entity': {
#         'chunks': [
#           {'text': 'The world is too much with us; late and soon, getting and spending...'},
#           {'text': 'All happy families are alike; each unhappy family is unhappy in its own way.'}
#         ]
#       }
#     },
#     {
#       'id': 461417939772144965,
#       'distance': 0.9555778503417969,
#       'entity': {
#         'chunks': [
#           {'text': 'Call me Ishmael. Some years ago—never mind how long precisely...'},
#           {'text': 'He was an old man who fished alone in a skiff in the Gulf Stream...'},
#           {'text': 'When I wrote the following pages, or rather the bulk of them...'},
#           {'text': 'It was the best of times, it was the worst of times...'},
#           {'text': 'The world is too much with us; late and soon, getting and spending...'}
#         ]
#       }
#     },
#     {
#       'id': 461417939772144962,
#       'distance': 0.9469035863876343,
#       'entity': {
#         'chunks': [
#           {'text': 'Call me Ishmael. Some years ago—never mind how long precisely...'},
#           {'text': 'The world is too much with us; late and soon, getting and spending...'},
#           {'text': 'He was an old man who fished alone in a skiff in the Gulf Stream...'},
#           {'text': 'Call me Ishmael. Some years ago—never mind how long precisely...'},
#           {'text': 'The world is too much with us; late and soon, getting and spending...'}
#         ]
#       }
#     }
#   ],
#   [
#     {
#       'id': 461417939772144663,
#       'distance': 1.9761409759521484,
#       'entity': {
#         'chunks': [
#           {'text': 'It was the best of times, it was the worst of times...'},
#           {'text': 'It is a truth universally acknowledged, that a single man in possession...'},
#           {'text': 'Whether I shall turn out to be the hero of my own life, or whether that station...'},
#           {'text': 'He was an old man who fished alone in a skiff in the Gulf Stream...'}
#         ]
#       }
#     },
#     {
#       'id': 461417939772144692,
#       'distance': 1.974656581878662,
#       'entity': {
#         'chunks': [
#           {'text': 'It is a truth universally acknowledged, that a single man in possession...'},
#           {'text': 'Call me Ishmael. Some years ago—never mind how long precisely...'}
#         ]
#       }
#     },
#     {
#       'id': 461417939772144662,
#       'distance': 1.9406685829162598,
#       'entity': {
#         'chunks': [
#           {'text': 'It is a truth universally acknowledged, that a single man in possession...'}
#         ]
#       }
#     }
#   ]
# ]
在上述代码示例中，
embeddingList1
是一个向量的嵌入列表，而
embeddingList2
包含两个向量。每个嵌入列表都会触发一个单独的搜索请求，并期望得到前 K 个相似实体的列表。
下一步工作
本地结构数组数据类型的开发代表着 Milvus 处理复杂数据结构能力的重大进步。为更好地了解其使用案例并最大限度地利用这一新功能，我们建议您阅读《
使用结构数组的 Schema 设计
》。