使用 Milvus 和 BentoML 的检索增强生成（RAG）
简介
本指南演示了如何使用 BentoCloud 上的开源嵌入模型和大型语言模型以及 Milvus 向量数据库来构建 RAG（检索增强生成）应用程序。 BentoCloud 是面向快速发展的人工智能团队的人工智能推理平台，为模型推理提供量身定制的全面管理基础设施。它与开源模型服务框架 BentoML 配合使用，便于轻松创建和部署高性能模型服务。在本演示中，我们使用 Milvus Lite 作为向量数据库，它是 Milvus 的轻量级版本，可以嵌入到您的 Python 应用程序中。
开始之前
Milvus Lite 可在 PyPI 上获取。您可以在 Python 3.8 以上版本中通过 pip 安装它：
$ pip install -U pymilvus milvus-lite bentoml
如果您使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "Runtime"（运行时）菜单，从下拉菜单中选择 "Restart session"（重启会话））。
登录 BentoCloud 后，我们可以在 "部署"（Deployments）中与已部署的 BentoCloud 服务交互，相应的END_POINT 和 API 位于 Playground -> Python。 您可以
在此处
下载城市数据。
使用 BentoML/BentoCloud 服务 Embeddings
要使用该端点，请导入
bentoml
，并通过指定端点和令牌（如果在 BentoCloud 上打开
Endpoint Authorization
）使用
SyncHTTPClient
设置 HTTP 客户端。或者，您也可以使用
Sentence Transformers Embeddings
资源库通过 BentoML 提供相同的模型。
import
bentoml

BENTO_EMBEDDING_MODEL_END_POINT =
"BENTO_EMBEDDING_MODEL_END_POINT"
BENTO_API_TOKEN =
"BENTO_API_TOKEN"
embedding_client = bentoml.SyncHTTPClient(
    BENTO_EMBEDDING_MODEL_END_POINT, token=BENTO_API_TOKEN
)
连接到 embedding_client 后，我们需要处理数据。我们提供了几个函数来执行数据分割和嵌入。
读取文件并将文本预处理为字符串列表。
# naively chunk on newlines
def
chunk_text
(
filename:
str
) ->
list
:
with
open
(filename,
"r"
)
as
f:
        text = f.read()
    sentences = text.split(
"\n"
)
return
sentences
首先，我们需要下载城市数据。
import
os
import
requests
import
urllib.request
# set up the data source
repo =
"ytang07/bento_octo_milvus_RAG"
directory =
"data"
save_dir =
"./city_data"
api_url =
f"https://api.github.com/repos/
{repo}
/contents/
{directory}
"
response = requests.get(api_url)
data = response.json()
if
not
os.path.exists(save_dir):
    os.makedirs(save_dir)
for
item
in
data:
if
item[
"type"
] ==
"file"
:
        file_url = item[
"download_url"
]
        file_path = os.path.join(save_dir, item[
"name"
])
        urllib.request.urlretrieve(file_url, file_path)
接下来，我们将对每个文件进行处理。
# please upload your data directory under this file's folder
cities = os.listdir(
"city_data"
)
# store chunked text for each of the cities in a list of dicts
city_chunks = []
for
city
in
cities:
    chunked = chunk_text(
f"city_data/
{city}
"
)
    cleaned = []
for
chunk
in
chunked:
if
len
(chunk) >
7
:
            cleaned.append(chunk)
    mapped = {
"city_name"
: city.split(
"."
)[
0
],
"chunks"
: cleaned}
    city_chunks.append(mapped)
将字符串列表分割成嵌入列表，每个嵌入列表分组 25 个文本字符串。
def
get_embeddings
(
texts:
list
) ->
list
:
if
len
(texts) >
25
:
        splits = [texts[x : x +
25
]
for
x
in
range
(
0
,
len
(texts),
25
)]
        embeddings = []
for
split
in
splits:
            embedding_split = embedding_client.encode(sentences=split)
            embeddings += embedding_split
return
embeddings
return
embedding_client.encode(
        sentences=texts,
    )
现在，我们需要将 embeddings 和文本块匹配起来。由于列表嵌入和句子列表应按索引匹配，因此我们可以通过
enumerate
任一列表进行匹配。
entries = []
for
city_dict
in
city_chunks:
# No need for the embeddings list if get_embeddings already returns a list of lists
embedding_list = get_embeddings(city_dict[
"chunks"
])
# returns a list of lists
# Now match texts with embeddings and city name
for
i, embedding
in
enumerate
(embedding_list):
        entry = {
"embedding"
: embedding,
"sentence"
: city_dict[
"chunks"
][
                i
            ],
# Assume "chunks" has the corresponding texts for the embeddings
"city"
: city_dict[
"city_name"
],
        }
        entries.append(entry)
print
(entries)
将数据插入向量数据库以便检索
准备好嵌入和数据后，我们就可以将向量连同元数据一起插入 Milvus Lite，以便稍后进行向量搜索。本节的第一步是通过连接 Milvus Lite 来启动客户端。我们只需导入
MilvusClient
模块并初始化一个 Milvus Lite 客户端，它将连接到你的 Milvus Lite 向量数据库。维度大小来自嵌入模型的大小，例如，Sentence Transformers 模型
all-MiniLM-L6-v2
产生的向量维度为 384。
from
pymilvus
import
MilvusClient

COLLECTION_NAME =
"Bento_Milvus_RAG"
# random name for your collection
DIMENSION =
384
# Initialize a Milvus Lite client
milvus_client = MilvusClient(
"milvus_demo.db"
)
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
或者使用旧的 connections.connect API（不推荐）：
from
pymilvus
import
connections

connections.connect(uri=
"milvus_demo.db"
)
创建 Milvus Lite Collections
使用 Milvus Lite 创建 Collections 包括两个步骤：首先是定义 Schema，其次是定义索引。在本节中，我们需要一个模块：DataType 告诉我们字段中的数据类型。我们还需要使用两个函数来创建模式和添加字段：create_schema()：创建 Collections 模式，add_field()：向 Collection 的模式中添加字段。
from
pymilvus
import
MilvusClient, DataType, Collection
# Create schema
schema = MilvusClient.create_schema(
    auto_id=
True
,
    enable_dynamic_field=
True
,
)
# 3.2. Add fields to schema
schema.add_field(field_name=
"id"
, datatype=DataType.INT64, is_primary=
True
)
schema.add_field(field_name=
"embedding"
, datatype=DataType.FLOAT_VECTOR, dim=DIMENSION)
现在，我们已经创建了模式并成功定义了数据字段，我们需要定义索引。就搜索而言，"索引 "定义了我们如何映射数据以供检索。在本项目中，我们使用默认的 "
AUTOINDEX
"为数据建立索引。
接下来，我们用之前给定的名称、Schema 和索引创建 Collections。最后，插入之前处理过的数据。
# prepare index parameters
index_params = milvus_client.prepare_index_params()
# add index
index_params.add_index(
    field_name=
"embedding"
,
    index_type=
"AUTOINDEX"
,
# use autoindex instead of other complex indexing method
metric_type=
"COSINE"
,
# L2, COSINE, or IP
)
# create collection
if
milvus_client.has_collection(collection_name=COLLECTION_NAME):
    milvus_client.drop_collection(collection_name=COLLECTION_NAME)
milvus_client.create_collection(
    collection_name=COLLECTION_NAME, schema=schema, index_params=index_params
)
# Outside the loop, now you upsert all the entries at once
milvus_client.insert(collection_name=COLLECTION_NAME, data=entries)
为 RAG 设置 LLM
要创建 RAG 应用程序，我们需要在 BentoCloud 上部署 LLM。让我们使用最新的 Llama3 LLM。启动并运行后，只需复制该模型服务的端点和令牌，并为其设置客户端即可。
BENTO_LLM_END_POINT =
"BENTO_LLM_END_POINT"
llm_client = bentoml.SyncHTTPClient(BENTO_LLM_END_POINT, token=BENTO_API_TOKEN)
LLM 说明
现在，我们用提示、上下文和问题设置 LLM 指令。下面是作为 LLM 的函数，它会以字符串格式返回客户端的输出。
def
dorag
(
question:
str
, context:
str
):

    prompt = (
f"You are a helpful assistant. The user has a question. Answer the user question based only on the context:
{context}
. \n"
f"The user question is
{question}
"
)

    results = llm_client.generate(
        max_tokens=
1024
,
        prompt=prompt,
    )

    res =
""
for
result
in
results:
        res += result
return
res
RAG 示例
现在我们可以提问了。该函数只需接收一个问题，然后通过 RAG 从背景信息中生成相关上下文。然后，我们将上下文和问题传递给 dorag() 并得到结果。
question =
"What state is Cambridge in?"
def
ask_a_question
(
question
):
    embeddings = get_embeddings([question])
    res = milvus_client.search(
        collection_name=COLLECTION_NAME,
        data=embeddings,
# search for the one (1) embedding returned as a list of lists
anns_field=
"embedding"
,
# Search across embeddings
limit=
5
,
# get me the top 5 results
output_fields=[
"sentence"
],
# get the sentence/chunk and city
)

    sentences = []
for
hits
in
res:
for
hit
in
hits:
print
(hit)
            sentences.append(hit[
"entity"
][
"sentence"
])
    context =
". "
.join(sentences)
return
context


context = ask_a_question(question=question)
print
(context)
实现 RAG
print
(dorag(question=question, context=context))
对于询问剑桥处于哪个州的示例问题，我们可以从 BentoML 中打印出整个回复。不过，如果我们花点时间解析一下，就会发现它看起来更漂亮，而且应该能告诉我们剑桥位于马萨诸塞州。