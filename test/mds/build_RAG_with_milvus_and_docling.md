使用 Milvus 和 Docling 构建 RAG
Docling
简化了人工智能应用对不同格式文档的解析和理解。通过高级 PDF 理解和统一文档表示，Docling 使非结构化文档数据为下游工作流做好了准备。
在本教程中，我们将向您展示如何使用 Milvus 和 Docling 构建一个检索-增强生成（RAG）管道。该管道集成了 Docling（用于文档解析）、Milvus（用于向量存储）和 OpenAI（用于生成具有洞察力的上下文感知响应）。
准备工作
依赖项和环境
开始时，请运行以下命令安装所需的依赖项：
$
pip install --upgrade pymilvus milvus-lite docling openai
如果使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
设置 API 密钥
在本示例中，我们将使用 OpenAI 作为 LLM。应将
OPENAI_API_KEY
设置为环境变量。
import
os

os.environ[
"OPENAI_API_KEY"
] =
"sk-***********"
准备 LLM 和 Embeddings 模型
我们初始化 OpenAI 客户端，以准备嵌入模型。
from
openai
import
OpenAI

openai_client = OpenAI()
定义一个使用 OpenAI 客户端生成文本嵌入的函数。我们以
text-embedding-3-small
模型为例。
def
emb_text
(
text
):
return
(
        openai_client.embeddings.create(
input
=text, model=
"text-embedding-3-small"
)
        .data[
0
]
        .embedding
    )
生成一个测试嵌入，并打印其维度和前几个元素。
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
1536
[0.00988506618887186, -0.005540902726352215, 0.0068014683201909065, -0.03810417652130127, -0.018254263326525688, -0.041231658309698105, -0.007651153020560741, 0.03220026567578316, 0.01892443746328354, 0.00010708322952268645]
使用 Docling 处理数据
Docling 可以将各种文档格式解析为统一的表示形式（Docling Document），然后导出为不同的输出格式。有关支持的输入和输出格式的完整列表，请参阅
官方文档
。
在本教程中，我们将使用 Markdown 文件
（源文件
）作为输入。我们将使用 Docling 提供的
分层分块器（HierarchicalChunker）
处理该文件，生成适合下游 RAG 任务的结构化分层分块。
from
docling.document_converter
import
DocumentConverter
from
docling_core.transforms.chunker
import
HierarchicalChunker

converter = DocumentConverter()
chunker = HierarchicalChunker()
# Convert the input file to Docling Document
source =
"https://milvus.io/docs/overview.md"
doc = converter.convert(source).document
# Perform hierarchical chunking
texts = [chunk.text
for
chunk
in
chunker.chunk(doc)]
for
i, text
in
enumerate
(texts[:
5
]):
print
(
f"Chunk
{i+
1
}
:\n
{text}
\n
{
'-'
*
50
}
"
)
Chunk 1:
Milvus is a high-performance, highly scalable vector database that runs efficiently across a wide range of environments, from a laptop to large-scale distributed systems. It is available as both open-source software and a cloud service.
--------------------------------------------------
Chunk 2:
Milvus is an open-source project under LF AI & Data Foundation distributed under the Apache 2.0 license. Most contributors are experts from the high-performance computing (HPC) community, specializing in building large-scale systems and optimizing hardware-aware code. Core contributors include professionals from Zilliz, ARM, NVIDIA, AMD, Intel, Meta, IBM, Salesforce, Alibaba, and Microsoft.
--------------------------------------------------
Chunk 3:
Unstructured data, such as text, images, and audio, varies in format and carries rich underlying semantics, making it challenging to analyze. To manage this complexity, embeddings are used to convert unstructured data into numerical vectors that capture its essential characteristics. These vectors are then stored in a vector database, enabling fast and scalable searches and analytics.
--------------------------------------------------
Chunk 4:
Milvus offers robust data modeling capabilities, enabling you to organize your unstructured or multi-modal data into structured collections. It supports a wide range of data types for different attribute modeling, including common numerical and character types, various vector types, arrays, sets, and JSON, saving you from the effort of maintaining multiple database systems.
--------------------------------------------------
Chunk 5:
Untructured data, embeddings, and Milvus
--------------------------------------------------
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
检查 Collections 是否已存在，如果存在则删除。
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
from
tqdm
import
tqdm

data = []
for
i, chunk
in
enumerate
(tqdm(texts, desc=
"Processing chunks"
)):
    embedding = emb_text(chunk)
    data.append({
"id"
: i,
"vector"
: embedding,
"text"
: chunk})

milvus_client.insert(collection_name=collection_name, data=data)
Processing chunks: 100%|██████████| 36/36 [00:18<00:00,  1.96it/s]





{'insert_count': 36, 'ids': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35], 'cost': 0}
构建 RAG
为查询检索数据
让我们指定一个关于我们刚刚抓取的网站的查询问题。
question = (
"What are the three deployment modes of Milvus, and what are their differences?"
)
在 Collections 中搜索该问题并检索语义前 3 个匹配项。
search_res = milvus_client.search(
    collection_name=collection_name,
    data=[emb_text(question)],
    limit=
3
,
    search_params={
"metric_type"
:
"IP"
,
"params"
: {}},
    output_fields=[
"text"
],
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
        "Milvus offers three deployment modes, covering a wide range of data scales\u2014from local prototyping in Jupyter Notebooks to massive Kubernetes clusters managing tens of billions of vectors:",
        0.6503741145133972
    ],
    [
        "Milvus Lite is a Python library that can be easily integrated into your applications. As a lightweight version of Milvus, it\u2019s ideal for quick prototyping in Jupyter Notebooks or running on edge devices with limited resources. Learn more.\nMilvus Standalone is a single-machine server deployment, with all components bundled into a single Docker image for convenient deployment. Learn more.\nMilvus Distributed can be deployed on Kubernetes clusters, featuring a cloud-native architecture designed for billion-scale or even larger scenarios. This architecture ensures redundancy in critical components. Learn more.",
        0.6281254291534424
    ],
    [
        "What is Milvus?\nUnstructured Data, Embeddings, and Milvus\nWhat Makes Milvus so Fast\uff1f\nWhat Makes Milvus so Scalable\nTypes of Searches Supported by Milvus\nComprehensive Feature Set",
        0.6117545962333679
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
使用 OpenAI ChatGPT 根据提示生成响应。
response = openai_client.chat.completions.create(
    model=
"gpt-4o"
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
The three deployment modes of Milvus are Milvus Lite, Milvus Standalone, and Milvus Distributed. 

1. **Milvus Lite**: This is a Python library designed for easy integration into applications. It is lightweight and ideal for quick prototyping in Jupyter Notebooks or for use on edge devices with limited resources.

2. **Milvus Standalone**: This deployment mode involves a single-machine server with all components bundled into a single Docker image for convenient deployment.

3. **Milvus Distributed**: This mode can be deployed on Kubernetes clusters and is built for larger-scale scenarios, including managing billions of vectors. It features a cloud-native architecture that ensures redundancy in critical components, making it suited for extensive scalability.