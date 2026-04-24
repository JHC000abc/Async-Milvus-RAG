使用 Milvus 和 Ollama 构建 RAG
Ollama
是一个开源平台，可简化大型语言模型 (LLM) 的本地运行和定制。它提供了用户友好的无云体验，无需高级技术技能即可轻松实现模型下载、安装和交互。凭借不断增长的预训练 LLMs 库（从通用型到特定领域型），Ollama 可以轻松管理和定制各种应用的模型。它确保了数据的私密性和灵活性，使用户能够完全在自己的机器上微调、优化和部署人工智能驱动的解决方案。
在本指南中，我们将向您展示如何利用 Ollama 和 Milvus 高效、安全地构建 RAG（检索-增强生成）管道。
准备工作
依赖关系和环境
$
pip install pymilvus milvus-lite ollama
如果使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
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
--2024-11-26 21:47:19--  https://github.com/milvus-io/milvus-docs/releases/download/v2.4.6-preview/milvus_docs_2.4.x_en.zip
Resolving github.com (github.com)... 140.82.112.4
Connecting to github.com (github.com)|140.82.112.4|:443... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://objects.githubusercontent.com/github-production-release-asset-2e65be/267273319/c52902a0-e13c-4ca7-92e0-086751098a05?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20241127%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241127T024720Z&X-Amz-Expires=300&X-Amz-Signature=7808b77cbdaa7e122196bcd75a73f29f2540333a350c4830bbdf5f286e876304&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3Dmilvus_docs_2.4.x_en.zip&response-content-type=application%2Foctet-stream [following]
--2024-11-26 21:47:20--  https://objects.githubusercontent.com/github-production-release-asset-2e65be/267273319/c52902a0-e13c-4ca7-92e0-086751098a05?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20241127%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241127T024720Z&X-Amz-Expires=300&X-Amz-Signature=7808b77cbdaa7e122196bcd75a73f29f2540333a350c4830bbdf5f286e876304&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3Dmilvus_docs_2.4.x_en.zip&response-content-type=application%2Foctet-stream
Resolving objects.githubusercontent.com (objects.githubusercontent.com)... 185.199.109.133, 185.199.111.133, 185.199.108.133, ...
Connecting to objects.githubusercontent.com (objects.githubusercontent.com)|185.199.109.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 613094 (599K) [application/octet-stream]
Saving to: ‘milvus_docs_2.4.x_en.zip’

milvus_docs_2.4.x_e 100%[===================>] 598.72K  1.20MB/s    in 0.5s    

2024-11-26 21:47:20 (1.20 MB/s) - ‘milvus_docs_2.4.x_en.zip’ saved [613094/613094]
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
准备 LLM 和 Embeddings 模型
Ollama 支持基于 LLM 任务和嵌入生成的多种模型，这使得开发检索增强生成（RAG）应用变得非常容易。在此设置中
我们将使用
Llama 3.2 (3B)
作为文本生成任务的 LLM。
对于嵌入生成，我们将使用
mxbai-embed-large
，这是一个针对语义相似性优化的 334M 参数模型。
在开始之前，请确保这两个模型都已拉到本地：
! ollama pull mxbai-embed-large
[?25lpulling manifest ⠋ [?25h[?25l[2K[1Gpulling manifest ⠙ [?25h[?25l[2K[1Gpulling manifest ⠹ [?25h[?25l[2K[1Gpulling manifest ⠸ [?25h[?25l[2K[1Gpulling manifest ⠼ [?25h[?25l[2K[1Gpulling manifest ⠴ [?25h[?25l[2K[1Gpulling manifest 
pulling 819c2adf5ce6... 100% ▕████████████████▏ 669 MB                         
pulling c71d239df917... 100% ▕████████████████▏  11 KB                         
pulling b837481ff855... 100% ▕████████████████▏   16 B                         
pulling 38badd946f91... 100% ▕████████████████▏  408 B                         
verifying sha256 digest 
writing manifest 
success [?25h
! ollama pull llama3
.2
[?25lpulling manifest ⠋ [?25h[?25l[2K[1Gpulling manifest ⠙ [?25h[?25l[2K[1Gpulling manifest ⠹ [?25h[?25l[2K[1Gpulling manifest ⠸ [?25h[?25l[2K[1Gpulling manifest ⠼ [?25h[?25l[2K[1Gpulling manifest ⠴ [?25h[?25l[2K[1Gpulling manifest 
pulling dde5aa3fc5ff... 100% ▕████████████████▏ 2.0 GB                         
pulling 966de95ca8a6... 100% ▕████████████████▏ 1.4 KB                         
pulling fcc5a6bec9da... 100% ▕████████████████▏ 7.7 KB                         
pulling a70ff7e570d9... 100% ▕████████████████▏ 6.0 KB                         
pulling 56bb8bd477a5... 100% ▕████████████████▏   96 B                         
pulling 34bb5ab01051... 100% ▕████████████████▏  561 B                         
verifying sha256 digest 
writing manifest 
success [?25h
准备好这些模型后，我们就可以开始实施 LLM 驱动的生成和基于嵌入的检索工作流程了。
import
ollama
def
emb_text
(
text
):
    response = ollama.embeddings(model=
"mxbai-embed-large"
, prompt=text)
return
response[
"embedding"
]
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
[0.23276396095752716, 0.4257211685180664, 0.19724100828170776, 0.46120673418045044, -0.46039995551109314, -0.1413791924715042, -0.18261606991291046, -0.07602324336767197, 0.39991313219070435, 0.8337644338607788]
将数据加载到 Milvus 中
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
Creating embeddings: 100%|██████████| 72/72 [00:03<00:00, 22.56it/s]





{'insert_count': 72, 'ids': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71], 'cost': 0}
构建 RAG
为查询检索数据
让我们指定一个关于 Milvus 的常见问题。
question =
"How is data stored in milvus?"
在 Collections 中搜索该问题，并检索语义前 3 个匹配项。
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
        231.9398193359375
    ],
    [
        "How does Milvus flush data?\n\nMilvus returns success when inserted data are loaded to the message queue. However, the data are not yet flushed to the disk. Then Milvus' data node writes the data in the message queue to persistent storage as incremental logs. If `flush()` is called, the data node is forced to write all data in the message queue to persistent storage immediately.\n\n###",
        226.48316955566406
    ],
    [
        "What is the maximum dataset size Milvus can handle?\n\n  \nTheoretically, the maximum dataset size Milvus can handle is determined by the hardware it is run on, specifically system memory and storage:\n\n- Milvus loads all specified collections and partitions into memory before running queries. Therefore, memory size determines the maximum amount of data Milvus can query.\n- When new entities and and collection-related schema (currently only MinIO is supported for data persistence) are added to Milvus, system storage determines the maximum allowable size of inserted data.\n\n###",
        210.60745239257812
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
使用 Ollama 提供的
llama3.2
模型，根据提示生成响应。
from
ollama
import
chat
from
ollama
import
ChatResponse

response: ChatResponse = chat(
    model=
"llama3.2"
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
(response[
"message"
][
"content"
])
According to the provided context, data in Milvus is stored in two types:

1. **Inserted data**: Storing data in persistent storage as incremental log. It supports multiple object storage backends such as MinIO, AWS S3, Google Cloud Storage (GCS), Azure Blob Storage, Alibaba Cloud OSS, and Tencent Cloud Object Storage.

2. **Metadata**: Generated within Milvus and stored in etcd.
很好！我们利用 Milvus 和 Ollama 成功构建了 RAG 管道。