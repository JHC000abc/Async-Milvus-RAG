使用 Milvus 和 OpenAI 进行语义搜索
本指南展示了如何将
OpenAI 的 Embedding API
与 Milvus 向量数据库结合使用，对文本进行语义搜索。
开始
在开始之前，请确保您已准备好 OpenAI API 密钥，或者您可以从
OpenAI 网站
获取一个。
本示例中使用的数据是书名。你可以
在这里
下载数据集，并将其放在运行以下代码的同一目录下。
首先，安装 Milvus 和 OpenAI 的软件包：
pip install --upgrade openai pymilvus milvus-lite
如果您使用的是 Google Colab，为了启用刚刚安装的依赖项，您可能需要
重启运行时
。(点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
这样，我们就可以生成 Embeddings 并使用向量数据库进行语义搜索了。
使用 OpenAI 和 Milvus 搜索书名
在下面的示例中，我们从下载的 CSV 文件中加载书名数据，使用 OpenAI 嵌入模型生成向量表示，并将其存储在 Milvus 向量数据库中进行语义搜索。
from
openai
import
OpenAI
from
pymilvus
import
MilvusClient

MODEL_NAME =
"text-embedding-3-small"
# Which model to use, please check https://platform.openai.com/docs/guides/embeddings for available models
DIMENSION =
1536
# Dimension of vector embedding
# Connect to OpenAI with API Key.
openai_client = OpenAI(api_key=
"<YOUR_OPENAI_API_KEY>"
)

docs = [
"Artificial intelligence was founded as an academic discipline in 1956."
,
"Alan Turing was the first person to conduct substantial research in AI."
,
"Born in Maida Vale, London, Turing was raised in southern England."
,
]

vectors = [
    vec.embedding
for
vec
in
openai_client.embeddings.create(
input
=docs, model=MODEL_NAME).data
]
# Prepare data to be stored in Milvus vector database.
# We can store the id, vector representation, raw text and labels such as "subject" in this case in Milvus.
data = [
    {
"id"
: i,
"vector"
: vectors[i],
"text"
: docs[i],
"subject"
:
"history"
}
for
i
in
range
(
len
(docs))
]
# Connect to Milvus, all data is stored in a local file named "milvus_openai_demo.db"
# in current directory. You can also connect to a remote Milvus server following this
# instruction: https://milvus.io/docs/install_standalone-docker.md.
milvus_client = MilvusClient(uri=
"milvus_openai_demo.db"
)
COLLECTION_NAME =
"demo_collection"
# Milvus collection name
# Create a collection to store the vectors and text.
if
milvus_client.has_collection(collection_name=COLLECTION_NAME):
    milvus_client.drop_collection(collection_name=COLLECTION_NAME)
milvus_client.create_collection(collection_name=COLLECTION_NAME, dimension=DIMENSION)
# Insert all data into Milvus vector database.
res = milvus_client.insert(collection_name=
"demo_collection"
, data=data)
print
(res[
"insert_count"
])
至于
MilvusClient
的参数：
将
uri
设置为本地文件，如
./milvus.db
，是最方便的方法，因为它会自动利用
Milvus Lite
将所有数据存储在此文件中。
如果数据规模较大，可以在
docker 或 kubernetes
上设置性能更强的 Milvus 服务器。在此设置中，请使用服务器 uri，例如
http://localhost:19530
，作为您的
uri
。
如果你想使用
Zilliz Cloud
（Milvus 的全托管云服务），请调整
uri
和
token
，它们与 Zilliz Cloud 中的
公共端点和 Api 密钥
相对应。
有了 Milvus 向量数据库中的所有数据，我们现在就可以通过为查询生成向量 Embeddings 来执行语义搜索，并进行向量搜索。
queries = [
"When was artificial intelligence founded?"
]

query_vectors = [
    vec.embedding
for
vec
in
openai_client.embeddings.create(
input
=queries, model=MODEL_NAME).data
]

res = milvus_client.search(
    collection_name=COLLECTION_NAME,
# target collection
data=query_vectors,
# query vectors
limit=
2
,
# number of returned entities
output_fields=[
"text"
,
"subject"
],
# specifies fields to be returned
)
for
q
in
queries:
print
(
"Query:"
, q)
for
result
in
res:
print
(result)
print
(
"\n"
)
输出结果如下：
[
    {
"id"
:
0
,
"distance"
: -
0.772376537322998
,
"entity"
: {
"text"
:
"Artificial intelligence was founded as an academic discipline in 1956."
,
"subject"
:
"history"
,
        },
    },
    {
"id"
:
1
,
"distance"
: -
0.58596271276474
,
"entity"
: {
"text"
:
"Alan Turing was the first person to conduct substantial research in AI."
,
"subject"
:
"history"
,
        },
    },
]