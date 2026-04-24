与 Milvus 和 SiliconFlow 一起构建 RAG
SiliconFlow
致力于构建一个可扩展、标准化和高性能的人工智能 Infra 平台。 SiliconCloud 是 SiliconFlow 的旗舰产品之一，被描述为模型即服务（MaaS）平台。它为部署各种人工智能模型（包括大型语言模型（LLMs）和嵌入模型）提供了一个全面的环境。SiliconCloud 聚合了众多开源模型，使用户能够轻松访问和利用这些资源，而无需大量的基础设施设置。
在本教程中，我们将向您展示如何使用 Milvus 和 SiliconFlow 构建 RAG（检索-增强生成）管道。
准备工作
依赖和环境
$
pip install --upgrade pymilvus milvus-lite openai requests tqdm
如果您使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "Runtime "菜单，从下拉菜单中选择 "Restart session"）。
SiliconFlow 支持 OpenAI 风格的 API。您可以登录其官方网站，并将
api key
SILICON_FLOW_API_KEY
作为环境变量。
import
os

os.environ[
"SILICON_FLOW_API_KEY"
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
文件夹中加载所有标记文件。对于每个文件，我们只需简单地使用 "#"来分隔文件中的内容，这样就能大致分隔出 markdown 文件中每个主要部分的内容。
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
准备嵌入模型
我们初始化一个客户端来准备嵌入模型。SiliconFlow 启用了 OpenAI 风格的 API，您可以稍作调整后使用相同的 API 来调用嵌入模型和 LLM。
from
openai
import
OpenAI

siliconflow_client = OpenAI(
    api_key=os.environ[
"SILICON_FLOW_API_KEY"
], base_url=
"https://api.siliconflow.cn/v1"
)
定义一个函数，使用客户端生成文本嵌入。我们以
BAAI/bge-large-en-v1.5
模型为例。
def
emb_text
(
text
):
return
(
        siliconflow_client.embeddings.create(
input
=text, model=
"BAAI/bge-large-en-v1.5"
)
        .data[
0
]
        .embedding
    )
生成一个测试嵌入并打印其维度和前几个元素。
test_embedding = emb_text(
"This is a test"
)
embedding_dim =
len
(test_embedding)
print
(embedding_dim)
print
(test_embedding[:
10
])
1024
[0.011475468054413795, 0.02982141077518463, 0.0038535362109541893, 0.035921916365623474, -0.0159175843000412, -0.014918108470737934, -0.018094222992658615, -0.002937349723652005, 0.030917132273316383, 0.03390815854072571]
将数据载入 Milvus
创建 Collections
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
consistency_level=
"Bounded"
,
# Supported values are (`"Strong"`, `"Session"`, `"Bounded"`, `"Eventually"`). See https://milvus.io/docs/consistency.md#Consistency-Level for more details.
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
: emb_text(line),
"text"
: line})

milvus_client.insert(collection_name=collection_name, data=data)
Creating embeddings: 100%|██████████| 72/72 [00:04<00:00, 16.97it/s]





{'insert_count': 72, 'ids': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71], 'cost': 0}
构建 RAG
为查询检索数据
让我们指定一个关于 Milvus 的常见问题。
question =
"How is data stored in milvus?"
在 Collections 中搜索该问题并检索语义前 3 个匹配项。
search_res = milvus_client.search(
    collection_name=collection_name,
    data=[
        emb_text(question)
    ],
# Use the `emb_text` function to convert the question to an embedding vector
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
        0.833885133266449
    ],
    [
        "How does Milvus flush data?\n\nMilvus returns success when inserted data are loaded to the message queue. However, the data are not yet flushed to the disk. Then Milvus' data node writes the data in the message queue to persistent storage as incremental logs. If `flush()` is called, the data node is forced to write all data in the message queue to persistent storage immediately.\n\n###",
        0.812842607498169
    ],
    [
        "Does the query perform in memory? What are incremental data and historical data?\n\nYes. When a query request comes, Milvus searches both incremental data and historical data by loading them into memory. Incremental data are in the growing segments, which are buffered in memory before they reach the threshold to be persisted in storage engine, while historical data are from the sealed segments that are stored in the object storage. Incremental data and historical data together constitute the whole dataset to search.\n\n###",
        0.7714196443557739
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
为 Lanage 模型定义系统和用户提示。该提示与从 Milvus 检索到的文档组装在一起。
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
使用 SiliconCloud 提供的
deepseek-ai/DeepSeek-V2.5
模型，根据提示生成响应。
response = siliconflow_client.chat.completions.create(
    model=
"deepseek-ai/DeepSeek-V2.5"
,
    messages=[
        {
"role"
:
"system"
,
"content"
: SYSTEM_PROMPT},
        {
"role"
:
"user"
,
"content"
: USER_PROMPT},
    ],
)
print
(response.choices[
0
].message.content)
In Milvus, data is stored in two main categories: inserted data and metadata.

- **Inserted Data**: This includes vector data, scalar data, and collection-specific schema, which are stored in persistent storage as incremental logs. Milvus supports various object storage backends such as MinIO, AWS S3, Google Cloud Storage (GCS), Azure Blob Storage, Alibaba Cloud OSS, and Tencent Cloud Object Storage (COS).

- **Metadata**: This is generated within Milvus, with each module having its own metadata stored in etcd, a distributed key-value store.
很好！我们利用 Milvus 和 SiliconFlow 成功构建了一个 RAG 管道。