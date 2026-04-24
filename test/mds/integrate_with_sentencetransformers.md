使用 Milvus 和 SentenceTransformers 进行电影搜索
在本示例中，我们将使用 Milvus 和 SentenceTransformers 库搜索电影情节摘要。我们将使用的数据集是
维基百科电影情节与摘要
，托管在 HuggingFace 上。
让我们开始吧！
所需库
在本例中，我们将使用
pymilvus
连接使用 Milvus，使用
sentence-transformers
生成向量嵌入，使用
datasets
下载示例数据集。
pip install pymilvus sentence-transformers datasets tqdm
from
datasets
import
load_dataset
from
pymilvus
import
MilvusClient
from
pymilvus
import
FieldSchema, CollectionSchema, DataType
from
sentence_transformers
import
SentenceTransformer
from
tqdm
import
tqdm
我们将定义一些全局参数、
embedding_dim =
384
collection_name =
"movie_embeddings"
下载和打开数据集
只需一行，
datasets
就能让我们下载并打开数据集。库将在本地缓存数据集，并在下次运行时使用该副本。每一行都包含一部电影的详细信息，该电影在维基百科上有相应的文章。我们使用
Title
、
PlotSummary
、
Release Year
和
Origin/Ethnicity
列。
ds = load_dataset(
"vishnupriyavr/wiki-movie-plots-with-summaries"
, split=
"train"
)
print
(ds)
连接数据库
此时，我们要开始设置 Milvus。具体步骤如下
在本地文件中创建 Milvus Lite 数据库。(将此 URI 替换为 Milvus Standalone 和 Milvus Distributed 的服务器地址）。
client = MilvusClient(uri=
"./sentence_transformers_example.db"
)
创建数据 Schema。这将指定构成元素的字段，包括向量 Embeddings 的维度。
fields = [
    FieldSchema(name=
"id"
, dtype=DataType.INT64, is_primary=
True
, auto_id=
True
),
    FieldSchema(name=
"title"
, dtype=DataType.VARCHAR, max_length=
256
),
    FieldSchema(name=
"embedding"
, dtype=DataType.FLOAT_VECTOR, dim=embedding_dim),
    FieldSchema(name=
"year"
, dtype=DataType.INT64),
    FieldSchema(name=
"origin"
, dtype=DataType.VARCHAR, max_length=
64
),
]

schema = CollectionSchema(fields=fields, enable_dynamic_field=
False
)
client.create_collection(collection_name=collection_name, schema=schema)
定义向量搜索索引算法。Milvus Lite 支持 FLAT 索引类型，而 Milvus Standalone 和 Milvus Distributed 实现了多种方法，如 IVF、HNSW 和 DiskANN。对于本演示中的小规模数据，任何搜索索引类型都已足够，因此我们在此使用最简单的 FLAT 索引类型。
index_params = client.prepare_index_params()
index_params.add_index(field_name=
"embedding"
, index_type=
"FLAT"
, metric_type=
"IP"
)
client.create_index(collection_name, index_params)
完成这些步骤后，我们就可以将数据插入 Collections 并执行搜索了。任何添加的数据都将自动编入索引，并立即可供搜索。如果数据非常新，搜索可能会慢一些，因为将对仍在索引过程中的数据使用暴力搜索。
插入数据
在本例中，我们将使用 SentenceTransformers miniLM 模型来创建情节文本的嵌入。该模型可返回 384 维嵌入。
model = SentenceTransformer(
"all-MiniLM-L12-v2"
)
我们循环浏览数据行，嵌入情节摘要字段，并将实体插入向量数据库。一般来说，应该像我们这里一样，在成批数据项上执行这一步骤，以最大限度地提高嵌入模型的 CPU 或 GPU 吞吐量。
for
batch
in
tqdm(ds.batch(batch_size=
512
)):
    embeddings = model.encode(batch[
"PlotSummary"
])
    data = [
        {
"title"
: title,
"embedding"
: embedding,
"year"
: year,
"origin"
: origin}
for
title, embedding, year, origin
in
zip
(
            batch[
"Title"
], embeddings, batch[
"Release Year"
], batch[
"Origin/Ethnicity"
]
        )
    ]
    res = client.insert(collection_name=collection_name, data=data)
上述操作相对耗时，因为嵌入需要时间。在 2023 MacBook Pro 上使用 CPU 执行此步骤大约需要 2 分钟，而使用专用 GPU 则会更快。休息一下，喝杯咖啡吧！
执行搜索
将所有数据插入 Milvus 后，我们就可以开始执行搜索了。在本例中，我们将根据维基百科的情节摘要搜索电影。由于我们进行的是批量搜索，因此搜索时间将在电影搜索中共享。(你能猜到我想根据查询描述文本检索哪部电影吗？）
queries = [
'A shark terrorizes an LA beach.'
,
'An archaeologist searches for ancient artifacts while fighting Nazis.'
,
'Teenagers in detention learn about themselves.'
,
'A teenager fakes illness to get off school and have adventures with two friends.'
,
'A young couple with a kid look after a hotel during winter and the husband goes insane.'
,
'Four turtles fight bad guys.'
]
# Search the database based on input text
def
embed_query
(
data
):
    vectors = model.encode(data)
return
[x
for
x
in
vectors]


query_vectors = embed_query(queries)

res = client.search(
    collection_name=collection_name,
    data=query_vectors,
filter
=
'origin == "American" and year > 1945 and year < 2000'
,
    anns_field=
"embedding"
,
    limit=
3
,
    output_fields=[
"title"
],
)
for
idx, hits
in
enumerate
(res):
print
(
"Query:"
, queries[idx])
print
(
"Results:"
)
for
hit
in
hits:
print
(hit[
"entity"
].get(
"title"
),
"("
,
round
(hit[
"distance"
],
2
),
")"
)
print
()
结果如下
Query: An archaeologist searches for ancient artifacts while fighting Nazis.
Results:
Love Slaves of the Amazons ( 0.4 )
A Time to Love and a Time to Die ( 0.39 )
The Fifth Element ( 0.39 )

Query: Teenagers in detention learn about themselves.
Results:
The Breakfast Club ( 0.54 )
Up the Academy ( 0.46 )
Fame ( 0.43 )

Query: A teenager fakes illness to get off school and have adventures with two friends.
Results:
Ferris Bueller's Day Off ( 0.48 )
Fever Lake ( 0.47 )
Losin' It ( 0.39 )

Query: A young couple with a kid look after a hotel during winter and the husband goes insane.
Results:
The Shining ( 0.48 )
The Four Seasons ( 0.42 )
Highball ( 0.41 )

Query: Four turtles fight bad guys.
Results:
Teenage Mutant Ninja Turtles II: The Secret of the Ooze ( 0.47 )
Devil May Hare ( 0.43 )
Attack of the Giant Leeches ( 0.42 )