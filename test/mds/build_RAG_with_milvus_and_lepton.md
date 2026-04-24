利用 Milvus 和 Lepton AI 构建 RAG
About to Deprecate
Lepton AI
可让开发人员和企业在几分钟内高效运行人工智能应用程序，并达到可投入生产的规模。 Lepton AI 允许您以 Python 原生方式构建模型，在本地调试和测试模型，只需一条命令即可将模型部署到云中，并通过简单灵活的 API 在任何应用程序中使用模型。它为部署各种人工智能模型（包括大型语言模型（LLMs）和扩散模型）提供了一个全面的环境，而无需大量的基础设施设置。
在本教程中，我们将向您展示如何使用 Milvus 和 Lepton AI 构建 RAG（检索-增强生成）管道。
准备工作
依赖和环境
$
pip install --upgrade pymilvus[model] openai requests tqdm
如果您使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
Lepton 支持 OpenAI 风格的 API。您可以登录其官方网站，并将
api key
LEPTONAI_TOKEN
作为环境变量。
import
os

os.environ[
"LEPTONAI_TOKEN"
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
准备 LLM 和 Embeddings 模型
Lepton 支持 OpenAI 风格的 API，你可以使用相同的 API 并稍作调整来调用 LLM。
from
openai
import
OpenAI

lepton_client = OpenAI(
    api_key=os.environ[
"LEPTONAI_TOKEN"
],
    base_url=
"https://mistral-7b.lepton.run/api/v1/"
,
)
定义一个嵌入模型，使用
milvus_model
生成文本嵌入。我们以
DefaultEmbeddingFunction
模型为例，这是一个经过预训练的轻量级嵌入模型。
from
pymilvus
import
model
as
milvus_model

embedding_model = milvus_model.DefaultEmbeddingFunction()
生成一个测试嵌入，并打印其维度和前几个元素。
test_embedding = embedding_model.encode_queries([
"This is a test"
])[
0
]
embedding_dim =
len
(test_embedding)
print
(embedding_dim)
print
(test_embedding[:
10
])
768
[-0.04836066  0.07163023 -0.01130064 -0.03789345 -0.03320649 -0.01318448
 -0.03041712 -0.02269499 -0.02317863 -0.00426028]
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

doc_embeddings = embedding_model.encode_documents(text_lines)
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
: doc_embeddings[i],
"text"
: line})

milvus_client.insert(collection_name=collection_name, data=data)
Creating embeddings: 100%|██████████| 72/72 [00:00<00:00, 1090216.20it/s]





{'insert_count': 72,
 'ids': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71],
 'cost': 0}
构建 RAG
为查询检索数据
让我们指定一个关于 Milvus 的常见问题。
question =
"How is data stored in milvus?"
在 Collections 中搜索该问题，并检索语义前 3 个匹配项。
search_res = milvus_client.search(
    collection_name=collection_name,
    data=embedding_model.encode_queries(
        [question]
    ),
# Convert the question to an embedding vector
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
        0.6572665572166443
    ],
    [
        "How does Milvus flush data?\n\nMilvus returns success when inserted data are loaded to the message queue. However, the data are not yet flushed to the disk. Then Milvus' data node writes the data in the message queue to persistent storage as incremental logs. If `flush()` is called, the data node is forced to write all data in the message queue to persistent storage immediately.\n\n###",
        0.6312146186828613
    ],
    [
        "How does Milvus handle vector data types and precision?\n\nMilvus supports Binary, Float32, Float16, and BFloat16 vector types.\n\n- Binary vectors: Store binary data as sequences of 0s and 1s, used in image processing and information retrieval.\n- Float32 vectors: Default storage with a precision of about 7 decimal digits. Even Float64 values are stored with Float32 precision, leading to potential precision loss upon retrieval.\n- Float16 and BFloat16 vectors: Offer reduced precision and memory usage. Float16 is suitable for applications with limited bandwidth and storage, while BFloat16 balances range and efficiency, commonly used in deep learning to reduce computational requirements without significantly impacting accuracy.\n\n###",
        0.6115777492523193
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
使用 Lepton AI 提供的
mistral-7b
模型，根据提示生成响应。
response = lepton_client.chat.completions.create(
    model=
"mistral-7b"
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
Inserted data in Milvus, including vector data, scalar data, and collection-specific schema, are stored in persistent storage as incremental logs. Milvus supports multiple object storage backends such as MinIO, AWS S3, Google Cloud Storage, Azure Blob Storage, Alibaba Cloud OSS, and Tencent Cloud Object Storage (COS). Metadata are generated within Milvus and stored in etcd.
太棒了！我们利用 Milvus 和 Lepton AI 成功构建了一个 RAG 管道。