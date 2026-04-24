用 Milvus 推荐电影
在本笔记本中，我们将探讨如何使用 OpenAI 生成电影描述的 Embeddings，并在 Milvus 中利用这些 Embeddings 来推荐符合您偏好的电影。为了增强搜索结果，我们将利用过滤功能来执行元数据搜索。本示例中使用的数据集来自 HuggingFace 数据集，包含 8000 多个电影条目，为电影推荐提供了丰富的选择。
依赖项和环境
运行以下命令即可安装依赖项：
$ pip install openai pymilvus datasets tqdm
如果您使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
在本例中，我们将使用 OpenAI 作为 LLM。您应将
api 密钥
OPENAI_API_KEY
作为环境变量。
import
os

os.environ[
"OPENAI_API_KEY"
] =
"sk-***********"
初始化 OpenAI 客户端和 Milvus
初始化 OpenAI 客户端。
from
openai
import
OpenAI

openai_client = OpenAI()
为 Embeddings 设置 Collections 名称和维度。
COLLECTION_NAME =
"movie_search"
DIMENSION =
1536
BATCH_SIZE =
1000
连接 Milvus。
from
pymilvus
import
MilvusClient
# Connect to Milvus Database
client = MilvusClient(
"./milvus_demo.db"
)
至于
url
和
token
的参数：
将
uri
设置为本地文件，如
./milvus.db
，是最方便的方法，因为它会自动利用
Milvus Lite
将所有数据存储在此文件中。
如果你有大规模数据，比如超过一百万个向量，你可以在
Docker 或 Kubernetes
上设置性能更强的 Milvus 服务器。在此设置中，请使用服务器地址和端口作为 uri，例如
http://localhost:19530
。如果在 Milvus 上启用了身份验证功能，请使用 "
:
" 作为令牌，否则不要设置令牌。
如果您想使用
Zilliz Cloud
（Milvus 的全托管云服务），请调整
uri
和
token
，它们与 Zilliz Cloud 中的
公共端点和 Api 密钥
相对应。
# Remove collection if it already exists
if
client.has_collection(COLLECTION_NAME):
    client.drop_collection(COLLECTION_NAME)
定义 Collections 的字段，包括 id、标题、类型、发布年份、评级和描述。
from
pymilvus
import
DataType
# Create collection which includes the id, title, and embedding.
# 1. Create schema
schema = MilvusClient.create_schema(
    auto_id=
True
,
    enable_dynamic_field=
False
,
)
# 2. Add fields to schema
schema.add_field(field_name=
"id"
, datatype=DataType.INT64, is_primary=
True
)
schema.add_field(field_name=
"title"
, datatype=DataType.VARCHAR, max_length=
64000
)
schema.add_field(field_name=
"type"
, datatype=DataType.VARCHAR, max_length=
64000
)
schema.add_field(field_name=
"release_year"
, datatype=DataType.INT64)
schema.add_field(field_name=
"rating"
, datatype=DataType.VARCHAR, max_length=
64000
)
schema.add_field(field_name=
"description"
, datatype=DataType.VARCHAR, max_length=
64000
)
schema.add_field(field_name=
"embedding"
, datatype=DataType.FLOAT_VECTOR, dim=DIMENSION)
# 3. Create collection with the schema
client.create_collection(collection_name=COLLECTION_NAME, schema=schema)
在 Collections 上创建索引并加载。
# Create the index on the collection and load it.
# 1. Prepare index parameters
index_params = client.prepare_index_params()
# 2. Add an index on the embedding field
index_params.add_index(
    field_name=
"embedding"
, metric_type=
"IP"
, index_type=
"AUTOINDEX"
, params={}
)
# 3. Create index
client.create_index(collection_name=COLLECTION_NAME, index_params=index_params)
# 4. Load collection
client.load_collection(collection_name=COLLECTION_NAME, replica_number=
1
)
数据集
Milvus 启动并运行后，我们就可以开始抓取数据了。
Hugging Face Datasets
是一个拥有许多不同用户数据集的集线器，在这个示例中，我们使用 HuggingLearners 的 netflix-shows 数据集。该数据集包含 8000 多部电影及其元数据对。我们将嵌入每条描述，并将其与标题、类型、发行年份和评分一起存储在 Milvus 中。
from
datasets
import
load_dataset

dataset = load_dataset(
"hugginglearners/netflix-shows"
, split=
"train"
)
插入数据
现在我们的机器上已经有了数据，我们可以开始嵌入数据并将其插入 Milvus。嵌入函数接收文本，并以列表格式返回嵌入结果。
def
emb_texts
(
texts
):
    res = openai_client.embeddings.create(
input
=texts, model=
"text-embedding-3-small"
)
return
[res_data.embedding
for
res_data
in
res.data]
下一步是实际插入。我们会遍历所有条目，并创建批次，一旦达到设定的批次大小，就会插入这些条目。循环结束后，如果还存在最后一个批次，则插入该批次。
from
tqdm
import
tqdm
# batch (data to be inserted) is a list of dictionaries
batch = []
# Embed and insert in batches
for
i
in
tqdm(
range
(
0
,
len
(dataset))):
    batch.append(
        {
"title"
: dataset[i][
"title"
]
or
""
,
"type"
: dataset[i][
"type"
]
or
""
,
"release_year"
: dataset[i][
"release_year"
]
or
-
1
,
"rating"
: dataset[i][
"rating"
]
or
""
,
"description"
: dataset[i][
"description"
]
or
""
,
        }
    )
if
len
(batch) % BATCH_SIZE ==
0
or
i ==
len
(dataset) -
1
:
        embeddings = emb_texts([item[
"description"
]
for
item
in
batch])
for
item, emb
in
zip
(batch, embeddings):
            item[
"embedding"
] = emb

        client.insert(collection_name=COLLECTION_NAME, data=batch)
        batch = []
查询数据库
数据安全地插入 Milvus 后，我们就可以执行查询了。查询将输入一个元组，其中包括要搜索的电影描述和要使用的过滤器。有关过滤器的更多信息，请
点击此处
。搜索首先会打印出描述和过滤器表达式。然后，我们会为每个结果打印得分、标题、类型、发行年份、评分和结果电影的描述。
import
textwrap
def
query
(
query, top_k=
5
):
    text, expr = query

    res = client.search(
        collection_name=COLLECTION_NAME,
        data=emb_texts(text),
filter
=expr,
        limit=top_k,
        output_fields=[
"title"
,
"type"
,
"release_year"
,
"rating"
,
"description"
],
        search_params={
"metric_type"
:
"IP"
,
"params"
: {},
        },
    )
print
(
"Description:"
, text,
"Expression:"
, expr)
for
hit_group
in
res:
print
(
"Results:"
)
for
rank, hit
in
enumerate
(hit_group, start=
1
):
            entity = hit[
"entity"
]
print
(
f"\tRank:
{rank}
Score:
{hit[
'distance'
]:}
Title:
{entity.get(
'title'
,
''
)}
"
)
print
(
f"\t\tType:
{entity.get(
'type'
,
''
)}
"
f"Release Year:
{entity.get(
'release_year'
,
''
)}
"
f"Rating:
{entity.get(
'rating'
,
''
)}
"
)
            description = entity.get(
"description"
,
""
)
print
(textwrap.fill(description, width=
88
))
print
()


my_query = (
"movie about a fluffly animal"
,
'release_year < 2019 and rating like "PG%"'
)

query(my_query)
Description: movie about a fluffly animal Expression: release_year < 2019 and rating like "PG%"
Results:
    Rank: 1 Score: 0.42213767766952515 Title: The Adventures of Tintin
        Type: Movie Release Year: 2011 Rating: PG
This 3-D motion capture adapts Georges Remi's classic comic strip about the adventures
of fearless young journalist Tintin and his trusty dog, Snowy.

    Rank: 2 Score: 0.4041026830673218 Title: Hedgehogs
        Type: Movie Release Year: 2016 Rating: PG
When a hedgehog suffering from memory loss forgets his identity, he ends up on a big
city journey with a pigeon to save his habitat from a human threat.

    Rank: 3 Score: 0.3980264663696289 Title: Osmosis Jones
        Type: Movie Release Year: 2001 Rating: PG
Peter and Bobby Farrelly outdo themselves with this partially animated tale about an
out-of-shape 40-year-old man who's the host to various organisms.

    Rank: 4 Score: 0.39479154348373413 Title: The Lamb
        Type: Movie Release Year: 2017 Rating: PG
A big-dreaming donkey escapes his menial existence and befriends some free-spirited
animal pals in this imaginative retelling of the Nativity Story.

    Rank: 5 Score: 0.39370301365852356 Title: Open Season 2
        Type: Movie Release Year: 2008 Rating: PG
Elliot the buck and his forest-dwelling cohorts must rescue their dachshund pal from
some spoiled pets bent on returning him to domesticity.