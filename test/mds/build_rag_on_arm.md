在 Arm 架构上构建 RAG
Arm
CPU 广泛应用于各种应用，包括传统的机器学习 (ML) 和人工智能 (AI) 用例。
在本教程中，您将学习如何在基于 Arm 的基础架构上构建检索增强生成 (RAG) 应用程序。在向量存储方面，我们利用了全面管理的 Milvus 向量数据库
Zilliz Cloud
。Zilliz Cloud 可在 AWS、GCP 和 Azure 等主流云上使用。在本演示中，我们使用部署在 AWS 上的 Zilliz Cloud 和 Arm 机器。对于 LLM，我们在基于 Arm 的 AWS 服务器 CPU 上使用
Llama-3.1-8B
模型，
llama.cpp
。
前提条件
要运行本示例，我们建议您使用
AWS Graviton
，它为在基于 Arm 的服务器上运行 ML 工作负载提供了一种经济高效的方法。本笔记本在装有 Ubuntu 22.04 LTS 系统的 AWS Graviton3
c7g.2xlarge
实例上进行了测试。
运行此示例至少需要四个内核和 8GB 内存。配置磁盘存储至少达到 32 GB。我们建议您使用规格相同或更高的实例。
启动实例后，连接并运行以下命令准备环境。
在服务器上安装 python：
$
sudo
apt update
$
sudo
apt install python-is-python3 python3-pip python3-venv -y
创建并激活虚拟环境：
$ python -m venv venv
$
source
venv/bin/activate
安装所需的 python 依赖项：
$
pip install --upgrade pymilvus openai requests langchain-huggingface huggingface_hub tqdm
离线数据加载
创建 Collections
我们使用部署在 AWS 上的
Zilliz Cloud
与基于 Arm 的机器来存储和检索向量数据。要快速启动，只需在 Zilliz Cloud 上免费
注册一个账户
。
除了 Zilliz Cloud，自托管 Milvus 也是一种选择（设置较为复杂）。我们还可以在基于 ARM 的机器上部署
Milvus Standalone
和
Kubernetes
。有关 Milvus 安装的更多信息，请参阅
安装文档
。
我们将
uri
和
token
设置为 Zilliz Cloud 中的
公共端点和 Api 密钥
。
from
pymilvus
import
MilvusClient

milvus_client = MilvusClient(
    uri=
"<your_zilliz_public_endpoint>"
, token=
"<your_zilliz_api_key>"
)

collection_name =
"my_rag_collection"
检查 Collections 是否已存在，如果已存在，则删除它。
if
milvus_client.has_collection(collection_name):
    milvus_client.drop_collection(collection_name)
使用指定参数创建新 Collections。
如果我们不指定任何字段信息，Milvus 会自动为主键创建一个默认的
id
字段，并创建一个
vector
字段来存储向量数据。保留的 JSON 字段用于存储非 Schema 定义的字段及其值。
milvus_client.create_collection(
    collection_name=collection_name,
    dimension=
384
,
    metric_type=
"IP"
,
# Inner product distance
consistency_level=
"Bounded"
,
# Supported values are (`"Strong"`, `"Session"`, `"Bounded"`, `"Eventually"`). See https://milvus.io/docs/consistency.md#Consistency-Level for more details.
)
我们使用内积距离作为默认度量类型。有关距离类型的更多信息，请参阅 "
相似度量 "页面。
准备数据
我们使用
Milvus 文档 2.4.x
中的常见问题页面作为 RAG 中的私有知识，这对于简单的 RAG 管道来说是一个很好的数据源。
下载 zip 文件并将文档解压缩到
milvus_docs
文件夹。
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
插入数据
我们准备一个简单但高效的嵌入模型
all-MiniLM-L6-v2
，它可以将文本转换为嵌入向量。
from
langchain_huggingface
import
HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name=
"all-MiniLM-L6-v2"
)
遍历文本行，创建嵌入，然后将数据插入 Milvus。
这里有一个新字段
text
，它是 Collections Schema 中的一个未定义字段。它将自动添加到预留的 JSON 动态字段中，在高层次上可将其视为普通字段。
from
tqdm
import
tqdm

data = []

text_embeddings = embedding_model.embed_documents(text_lines)
for
i, (line, embedding)
in
enumerate
(
    tqdm(
zip
(text_lines, text_embeddings), desc=
"Creating embeddings"
)
):
    data.append({
"id"
: i,
"vector"
: embedding,
"text"
: line})

milvus_client.insert(collection_name=collection_name, data=data)
Creating embeddings: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 72/72 [00:18<00:00,  3.91it/s]
在 Arm 上启动 LLM 服务
在本节中，我们将在基于 Arm 的 CPU 上构建并启动
llama.cpp
服务。
Llama 3.1 模型和 llama.cpp
来自 Meta 的
Llama-3.1-8B 模型
属于 Llama 3.1 模型系列，可免费用于研究和商业用途。在使用该模型之前，请访问 Llama
网站
并填写表格申请访问权限。
llama.cpp
是一个开源的C/C++项目，可在本地和云端的各种硬件上实现高效的LLM推理。您可以使用
llama.cpp
方便地托管 Llama 3.1 模型。
下载并构建 llama.cpp
运行以下命令安装 make、cmake、gcc、g++ 以及从源代码构建 llama.cpp 所需的其他基本工具：
$
sudo
apt install make cmake -y
$
sudo
apt install gcc g++ -y
$
sudo
apt install build-essential -y
现在您可以开始构建
llama.cpp
。
克隆 llama.cpp 的源码库：
$ git
clone
https://github.com/ggerganov/llama.cpp
默认情况下，
llama.cpp
只在 Linux 和 Windows 上为 CPU 构建。您不需要提供任何额外的开关，就能为运行它的 Arm CPU 构建它。
运行
make
进行编译：
$
cd
llama.cpp
$ make GGML_NO_LLAMAFILE=1 -j$(
nproc
)
运行 help 命令检查
llama.cpp
是否已正确编译：
$ ./llama-cli -h
如果
llama.cpp
已正确编译，则会显示帮助选项。输出片段如下：
example usage:

    text generation:     ./llama-cli -m your_model.gguf -p "I believe the meaning of life is" -n 128

    chat (conversation): ./llama-cli -m your_model.gguf -p "You are a helpful assistant" -cnv
现在可以使用 HuggingFace cli 下载模型了：
$ huggingface-cli download cognitivecomputations/dolphin-2.9.4-llama3.1-8b-gguf dolphin-2.9.4-llama3.1-8b-Q4_0.gguf --local-dir . --local-dir-use-symlinks False
由 llama.cpp 团队推出的 GGUF 模型格式使用压缩和量化技术将权重精度降低到 4 位整数，大大降低了计算和内存需求，使 Arm CPU 有效地用于 LLM 推理。
重新量化模型权重
要重新量化，运行
$ ./llama-quantize --allow-requantize dolphin-2.9.4-llama3.1-8b-Q4_0.gguf dolphin-2.9.4-llama3.1-8b-Q4_0_8_8.gguf Q4_0_8_8
这将输出一个新文件
dolphin-2.9.4-llama3.1-8b-Q4_0_8_8.gguf
，其中包含重新配置的权重，使
llama-cli
可以使用 SVE 256 和 MATMUL_INT8 支持。
这种重新量化专门针对 Graviton3 而优化。对于 Graviton2，最佳的重量化应在
Q4_0_4_4
格式中进行，而对于 Graviton4，
Q4_0_4_8
格式最适合重量化。
启动 LLM 服务
您可以利用 llama.cpp 服务器程序，通过与 OpenAI 兼容的 API 发送请求。这样，您就可以开发与 LLM 进行多次交互的应用程序，而无需反复启动和停止 LLM。此外，您还可以从另一台通过网络托管 LLM 的机器上访问服务器。
通过命令行启动服务器，服务器会监听 8080 端口：
$
./llama-server -m dolphin-2.9.4-llama3.1-8b-Q4_0_8_8.gguf -n 2048 -t 64 -c 65536  --port 8080
'main: server is listening on 127.0.0.1:8080 - starting the main loop
您还可以调整已启动 LLM 的参数，使其与服务器硬件相适应，从而获得理想的性能。有关更多参数信息，请参阅
llama-server --help
命令。
如果在执行此步骤时遇到困难，可参阅
官方文档
获取更多信息。
您已经在基于 Arm 的 CPU 上启动了 LLM 服务。接下来，我们直接使用 OpenAI SDK 与服务交互。
在线 RAG
LLM 客户端和 Embeddings 模型
我们初始化 LLM 客户端并准备嵌入模型。
对于 LLM，我们使用 OpenAI SDK 请求之前启动的 Llama 服务。我们不需要使用任何 API 密钥，因为它实际上就是我们本地的 llama.cpp 服务。
from
openai
import
OpenAI

llm_client = OpenAI(base_url=
"http://localhost:8080/v1"
, api_key=
"no-key"
)
生成测试 Embeddings 并打印其尺寸和前几个元素。
test_embedding = embedding_model.embed_query(
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
384
[0.03061249852180481, 0.013831384479999542, -0.02084377221763134, 0.016327863559126854, -0.010231520049273968, -0.0479842908680439, -0.017313342541456223, 0.03728749603033066, 0.04588735103607178, 0.034405000507831573]
为查询检索数据
让我们指定一个关于 Milvus 的常见问题。
question =
"How is data stored in milvus?"
在 Collections 中搜索该问题，并检索语义前 3 个匹配项。
search_res = milvus_client.search(
    collection_name=collection_name,
    data=[
        embedding_model.embed_query(question)
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
        0.6488019824028015
    ],
    [
        "How does Milvus flush data?\n\nMilvus returns success when inserted data are loaded to the message queue. However, the data are not yet flushed to the disk. Then Milvus' data node writes the data in the message queue to persistent storage as incremental logs. If `flush()` is called, the data node is forced to write all data in the message queue to persistent storage immediately.\n\n###",
        0.5974207520484924
    ],
    [
        "What is the maximum dataset size Milvus can handle?\n\n  \nTheoretically, the maximum dataset size Milvus can handle is determined by the hardware it is run on, specifically system memory and storage:\n\n- Milvus loads all specified collections and partitions into memory before running queries. Therefore, memory size determines the maximum amount of data Milvus can query.\n- When new entities and and collection-related schema (currently only MinIO is supported for data persistence) are added to Milvus, system storage determines the maximum allowable size of inserted data.\n\n###",
        0.5833579301834106
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
Define system and user prompts for the Language Model. This prompt is assembled with the retrieved documents from Milvus.

SYSTEM_PROMPT = """
Human: You are an AI assistant. You are able to find answers to the questions from the contextual passage snippets provided.
"""
USER_PROMPT = f"""
Use the following pieces of information enclosed in <context> tags to provide an answer to the question enclosed in <question> tags.
<context>
{context}
</context>
<question>
{question}
</question>
"""
使用 LLM 根据提示生成响应。我们将
model
参数设置为
not-used
，因为它是 llama.cpp 服务的多余参数。
response = llm_client.chat.completions.create(
    model=
"not-used"
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
Milvus stores data in two types: inserted data and metadata. Inserted data, including vector data, scalar data, and collection-specific schema, are stored in persistent storage as incremental log. Milvus supports multiple object storage backends such as MinIO, AWS S3, Google Cloud Storage (GCS), Azure Blob Storage, Alibaba Cloud OSS, and Tencent Cloud Object Storage (COS). Metadata are generated within Milvus and each Milvus module has its own metadata that are stored in etcd.
恭喜您您已经在基于 Arm 的基础架构之上构建了一个 RAG 应用程序。