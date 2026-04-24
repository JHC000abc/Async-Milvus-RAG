使用 Milvus 和 Gemini 构建 RAG
Gemini API
和
Google AI Studio
可帮助您开始使用 Google 的最新模型，并将您的想法转化为可扩展的应用程序。Gemini 可以访问
Gemini-2.5-Flash
和
Gemini-2.5-Pro
等强大的语言模型，用于文本生成、文档处理、视觉、音频分析等任务。它还提供
Gemini Embedding 2
，这是一种多模态 Embeddings 模型，支持文本、图像、视频、音频和 PDF 文档，通过 Matryoshka 表征学习实现灵活的输出维度。通过 API，您可以输入包含数百万个标记的长上下文，针对特定任务对模型进行微调，生成 JSON 等结构化输出，并利用语义检索和代码执行等功能。
在本教程中，我们将向您展示如何使用 Milvus 和 Gemini 构建 RAG（检索-增强生成）管道。我们将使用 Gemini 模型根据给定查询生成响应，并用从 Milvus 检索到的相关信息进行增强。
准备工作
依赖和环境
首先，安装所需的软件包：
$
pip install --upgrade pymilvus milvus-lite google-genai requests tqdm
如果使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
首先应登录 Google AI Studio 平台，并将
api key
GEMINI_API_KEY
作为环境变量。
import
os

os.environ[
"GEMINI_API_KEY"
] =
"***********"
准备数据
我们使用
Milvus 文档 2.4.x
中的常见问题页面作为 RAG 中的私有知识，这对于简单的 RAG 管道来说是一个很好的数据源。
下载 zip 文件并将文档解压缩到
milvus_docs
文件夹中。
$
wget https://github.com/milvus-io/milvus-docs/releases/download/v2.4.6-preview/milvus_docs_2.4.x_en.zip
$
unzip -q milvus_docs_2.4.x_en.zip -d milvus_docs
我们从
milvus_docs/en/faq
文件夹中加载所有标记文件。对于每个文档，我们只需简单地使用 "#"来分隔文件中的内容，这样就能大致分隔出 markdown 文件中每个主要部分的内容。
from
glob
import
glob

text_lines = []
for
file_path
in
glob(
"milvus_docs/en/faq/*.md"
, recursive=
True
):
with
open
(file_path,
"r"
)
as
file:
        file_text = file.read()

    text_lines += file_text.split(
"# "
)
准备 LLM 和嵌入模型
我们使用
gemini-2.5-flash
作为 LLM，使用
gemini-embedding-2-preview
作为嵌入模型。
gemini-embedding-2-preview
是 Google 最新的多模态嵌入模型，通过 Matryoshka 表征学习，支持文本、图片、视频、音频和 PDF 文档，输出维度灵活（128-3072）。
让我们尝试用 LLM 生成一个测试响应：
from
google
import
genai

client = genai.Client(api_key=os.environ[
"GEMINI_API_KEY"
])

response = client.models.generate_content(
    model=
"gemini-2.5-flash"
, contents=
"who are you"
)
print
(response.text)
I am a large language model, trained by Google.

I'm designed to process and generate human-like text based on the vast amount of data I was trained on. This allows me to:

*   Answer questions
*   Provide summaries
*   Generate creative content
*   Translate languages
*   And much more

I don't have personal experiences, feelings, or consciousness. I'm a tool designed to be helpful and informative.
生成测试 Embeddings 并打印其维度和前几个元素。
test_embeddings = client.models.embed_content(
    model=
"gemini-embedding-2-preview"
, contents=[
"This is a test1"
,
"This is a test2"
]
)

embedding_dim =
len
(test_embeddings.embeddings[
0
].values)
print
(embedding_dim)
print
(test_embeddings.embeddings[
0
].values[:
10
])
3072
[-0.016769307, 0.013630492, 0.020277105, 0.0035285393, 0.003968259, -0.013498845, 0.028525498, 0.025498547, -0.021553498, 0.015233516]
将数据载入 Milvus
创建 Collections
让我们初始化 Milvus 客户端并设置我们的 Collections：
from
pymilvus
import
MilvusClient

milvus_client = MilvusClient(uri=
"./milvus_demo.db"
)

collection_name =
"my_rag_collection"
至于
MilvusClient
的参数：
将
uri
设置为本地文件，例如
./milvus.db
，这是最方便的方法，因为它会自动利用
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
检查 Collections 是否已存在，如果已存在，则删除它。
if
milvus_client.has_collection(collection_name):
    milvus_client.drop_collection(collection_name)
使用指定参数创建新 Collections。
如果我们不指定任何字段信息，Milvus 会自动创建一个主键的默认
id
字段，以及一个存储向量数据的
vector
字段。保留的 JSON 字段用于存储非 Schema 定义的字段及其值。
milvus_client.create_collection(
    collection_name=collection_name,
    dimension=embedding_dim,
    metric_type=
"IP"
,
# Inner product distance
# Strong consistency waits for all loads to complete, adding latency with large datasets
# consistency_level="Strong",  # Strong consistency level
)
插入数据
遍历文本行，创建 Embeddings，然后将数据插入 Milvus。
这里有一个新字段
text
，它是 Collections Schema 中的一个非定义字段。它将自动添加到保留的 JSON 动态字段中，在高层次上可将其视为普通字段。
from
tqdm
import
tqdm

data = []

doc = client.models.embed_content(model=
"gemini-embedding-2-preview"
, contents=text_lines)
for
i, line
in
enumerate
(tqdm(text_lines, desc=
"Creating embeddings"
)):
    data.append({
"id"
: i,
"vector"
: doc.embeddings[i].values,
"text"
: line})

milvus_client.insert(collection_name=collection_name, data=data)
Creating embeddings: 100%|██████████| 72/72 [00:00<00:00, 337796.30it/s]





{'insert_count': 72, 'ids': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71], 'cost': 0}
构建 RAG
为查询检索数据
让我们指定一个关于 Milvus 的常见问题。
question =
"How is data stored in milvus?"
在 Collections 中搜索该问题并检索语义前 3 个匹配项。
quest_embed = client.models.embed_content(model=
"gemini-embedding-2-preview"
, contents=question)

search_res = milvus_client.search(
    collection_name=collection_name,
    data=[quest_embed.embeddings[
0
].values],
    limit=
3
,
# Return top 3 results
search_params={
"metric_type"
:
"IP"
,
"params"
: {}},
# Inner product distance
output_fields=[
"text"
],
# Return the text field
)
让我们看看查询的搜索结果
import
json

retrieved_lines_with_distances = [
    (res[
"entity"
][
"text"
], res[
"distance"
])
for
res
in
search_res[
0
]
]
print
(json.dumps(retrieved_lines_with_distances, indent=
4
))
[
    [
        " Where does Milvus store data?\n\nMilvus deals with two types of data, inserted data and metadata. \n\nInserted data, including vector data, scalar data, and collection-specific schema, are stored in persistent storage as incremental log. Milvus supports multiple object storage backends, including [MinIO](https://min.io/), [AWS S3](https://aws.amazon.com/s3/?nc1=h_ls), [Google Cloud Storage](https://cloud.google.com/storage?hl=en#object-storage-for-companies-of-all-sizes) (GCS), [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs), [Alibaba Cloud OSS](https://www.alibabacloud.com/product/object-storage-service), and [Tencent Cloud Object Storage](https://www.tencentcloud.com/products/cos) (COS).\n\nMetadata are generated within Milvus. Each Milvus module has its own metadata that are stored in etcd.\n\n###",
        0.864
    ],
    [
        "Why is there no vector data in etcd?\n\netcd stores Milvus module metadata; MinIO stores entities.",
        0.7923
    ],
    [
        "What is the maximum dataset size Milvus can handle?\n\n  \nTheoretically, the maximum dataset size Milvus can handle is determined by the hardware it is run on, specifically system memory and storage:\n\n- Milvus loads all specified collections and partitions into memory before running queries. Therefore, memory size determines the maximum amount of data Milvus can query.\n- When new entities and and collection-related schema (currently only MinIO is supported for data persistence) are added to Milvus, system storage determines the maximum allowable size of inserted data.\n\n###",
        0.7857
    ]
]
使用 LLM 获取 RAG 响应
将检索到的文档转换为字符串格式。
context =
"\n"
.join(
    [line_with_distance[
0
]
for
line_with_distance
in
retrieved_lines_with_distances]
)
为语言模型定义系统和用户提示。该提示与从 Milvus 检索到的文档组装在一起。
from
google.genai
import
types

SYSTEM_PROMPT =
"""
Human: You are an AI assistant. You are able to find answers to the questions from the contextual passage snippets provided.
"""
USER_PROMPT =
f"""
Use the following pieces of information enclosed in <context> tags to provide an answer to the question enclosed in <question> tags.
<context>
{context}
</context>
<question>
{question}
</question>
"""
使用 Gemini 根据提示生成响应。
response = client.models.generate_content(
    model=
"gemini-2.5-flash"
,
    config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    contents=USER_PROMPT,
)
print
(response.text)
Milvus stores data in two main ways:

1.  **Inserted Data:** This includes vector data, scalar data, and collection-specific schema. This type of data is stored in persistent storage as an incremental log. Milvus supports various object storage backends for this, such as MinIO, AWS S3, Google Cloud Storage (GCS), Azure Blob Storage, Alibaba Cloud OSS, and Tencent Cloud Object Storage (COS).
2.  **Metadata:** Metadata is generated within Milvus by its various modules. Each module's metadata is stored in etcd.
多模式搜索
由于
gemini-embedding-2-preview
将文本、图像和其他模态映射到同一个 Embeddings 空间，因此我们可以进行跨模态搜索--例如，使用文本查询来查找最相关的图像。
准备图像数据
我们从 Milvus Bootcamp 存储库中下载一组 RAG 架构图作为图像数据集。
import
urllib.request
from
pathlib
import
Path

image_dir = Path(
"images"
)
image_dir.mkdir(exist_ok=
True
)

image_files = [
"vanilla_rag.png"
,
"hyde.png"
,
"query_routing.png"
,
"self_reflection.png"
,
"hybrid_and_rerank.png"
,
"hierarchical_index.png"
,
]

base_url =
"https://raw.githubusercontent.com/milvus-io/bootcamp/master/pics/advanced_rag/"
for
fname
in
image_files:
    path = image_dir / fname
if
not
path.exists():
        urllib.request.urlretrieve(base_url + fname, path)
print
(
f"Downloaded
{fname}
"
)
else
:
print
(
f"Already exists
{fname}
"
)
print
(
f"\nTotal images:
{
len
(image_files)}
"
)
Downloaded vanilla_rag.png
Downloaded hyde.png
Downloaded query_routing.png
Downloaded self_reflection.png
Downloaded hybrid_and_rerank.png
Downloaded hierarchical_index.png

Total images: 6
嵌入图像并存储在 Milvus 中
我们以字节形式读取每张图片，并将其传递给
gemini-embedding-2-preview
以生成嵌入，然后将其存储到一个新的 Milvus Collections 中。
from
google.genai
import
types

image_data = []
for
fname
in
image_files:
    path = image_dir / fname
with
open
(path,
"rb"
)
as
f:
        image_bytes = f.read()

    result = client.models.embed_content(
        model=
"gemini-embedding-2-preview"
,
        contents=types.Part.from_bytes(data=image_bytes, mime_type=
"image/png"
),
    )
    image_data.append(
        {
"id"
:
len
(image_data),
"vector"
: result.embeddings[
0
].values,
"filename"
: fname,
        }
    )
print
(
f"Embedded
{fname}
"
)
# Create a new collection for images
image_collection =
"image_collection"
if
milvus_client.has_collection(image_collection):
    milvus_client.drop_collection(image_collection)

milvus_client.create_collection(
    collection_name=image_collection,
    dimension=
len
(image_data[
0
][
"vector"
]),
    metric_type=
"IP"
,
)

milvus_client.insert(collection_name=image_collection, data=image_data)
print
(
f"\nInserted
{
len
(image_data)}
image embeddings (dim=
{
len
(image_data[
0
][
'vector'
])}
)"
)
Embedded vanilla_rag.png
Embedded hyde.png
Embedded query_routing.png
Embedded self_reflection.png
Embedded hybrid_and_rerank.png
Embedded hierarchical_index.png

Inserted 6 image embeddings (dim=3072)
跨模态搜索：文本查询 → 图像结果
现在，让我们使用文本查询跨图像嵌入进行搜索。由于文本和图像都映射到了同一个嵌入空间，因此我们可以直接对它们进行比较。
from
IPython.display
import
display, Image

text_queries = [
"How does a basic RAG pipeline work?"
,
"What is the hypothetical document embedding approach?"
,
"How to combine hybrid search with reranking?"
,
]
for
query
in
text_queries:
    query_embed = client.models.embed_content(
        model=
"gemini-embedding-2-preview"
, contents=query
    )

    results = milvus_client.search(
        collection_name=image_collection,
        data=[query_embed.embeddings[
0
].values],
        limit=
1
,
        search_params={
"metric_type"
:
"IP"
,
"params"
: {}},
        output_fields=[
"filename"
],
    )

    best = results[
0
][
0
]
print
(
f"\nQuery:
{query}
"
)
print
(
f"Match:
{best[
'entity'
][
'filename'
]}
(score:
{best[
'distance'
]:
.4
f}
)"
)
    display(Image(filename=
str
(image_dir / best[
"entity"
][
"filename"
]), width=
600
))
Query: How does a basic RAG pipeline work?
Match: vanilla_rag.png (score: 0.5132)
香草 RAG 管道
Query: What is the hypothetical document embedding approach?
Match: hyde.png (score: 0.4756)
混合检索
Query: How to combine hybrid search with reranking?
Match: hybrid_and_rerank.png (score: 0.5271)
混合检索和 Rerankers
太棒了！我们利用 Milvus 和 Gemini 成功构建了一个 RAG 管道，并演示了使用文本查询检索相关图像的跨模态搜索--所有这些都由
gemini-embedding-2-preview
的统一嵌入空间提供支持。