利用 Milvus 和 Unstructured 创建 RAG
Unstructured
提供了一个平台和工具，用于为检索增强生成（RAG）和模型微调摄取和处理非结构化文档。它提供无代码 UI 平台和无服务器 API 服务，允许用户在 Unstructured 托管的计算资源上处理数据。
在本教程中，我们将使用 Unstructured 采集 PDF 文档，然后使用 Milvus 构建 RAG 管道。
准备工作
依赖和环境
$
pip install -qU
"unstructured[pdf]"
pymilvus milvus-lite openai
安装选项：
用于处理所有文档格式：
pip install "unstructured[all-docs]"
用于特定格式（如 PDF）：
pip install "unstructured[pdf]"
更多安装选项，请参阅
Unstructured 文档
如果使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
在本例中，我们将使用 OpenAI 作为 LLM。您应将
api key
OPENAI_API_KEY
作为环境变量。
import
os

os.environ[
"OPENAI_API_KEY"
] =
"sk-***********"
准备 Milvus 和 OpenAI 客户端
您可以使用 Milvus 客户端创建 Milvus Collections 并向其中插入数据。
from
pymilvus
import
MilvusClient, DataType
# Initialize Milvus client
milvus_client = MilvusClient(uri=
"./milvus_demo.db"
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
将所有数据存储到此文件中。
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
检查 Collections 是否已经存在，如果存在则删除。
collection_name =
"my_rag_collection"
if
milvus_client.has_collection(collection_name):
    milvus_client.drop_collection(collection_name)
准备一个 OpenAI 客户端来生成嵌入和生成响应。
from
openai
import
OpenAI

openai_client = OpenAI()
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
[0.009889289736747742, -0.005578675772994757, 0.00683477520942688, -0.03805781528353691, -0.01824733428657055, -0.04121600463986397, -0.007636285852640867, 0.03225184231996536, 0.018949154764413834, 9.352207416668534e-05]
创建 Milvus Collections
我们将创建一个具有以下 Schema 的 Collection：
id
主键：主键是每个文档的唯一标识符。
vector
主键：文档的 Embeddings。
text
文档的文本内容。
metadata
文档的元数据。
然后，我们在
vector
字段上建立
AUTOINDEX
索引。然后创建 Collections。
# Create schema
schema = milvus_client.create_schema(auto_id=
False
, enable_dynamic_field=
False
)
# Add fields to schema
schema.add_field(field_name=
"id"
, datatype=DataType.INT64, is_primary=
True
)
schema.add_field(field_name=
"vector"
, datatype=DataType.FLOAT_VECTOR, dim=embedding_dim)
schema.add_field(field_name=
"text"
, datatype=DataType.VARCHAR, max_length=
65535
)
schema.add_field(field_name=
"metadata"
, datatype=DataType.JSON)
index_params = MilvusClient.prepare_index_params()
index_params.add_index(
    field_name=
"vector"
,
    metric_type=
"COSINE"
,
    index_type=
"AUTOINDEX"
,
)
milvus_client.create_collection(
    collection_name=collection_name,
    schema=schema,
    index_params=index_params,
    consistency_level=
"Bounded"
,
)

milvus_client.load_collection(collection_name=collection_name)
从 Unstructured 中加载数据
Unstructured 提供了灵活而强大的摄取管道，可以处理各种文件类型，包括 PDF、HTML 等。 我们将对本地 PDF 文件进行分区和分块。然后将数据加载到 Milvus 中。
import
warnings
from
unstructured.partition.auto
import
partition

warnings.filterwarnings(
"ignore"
)

elements = partition(
    filename=
"./pdf_files/WhatisMilvus.pdf"
,
    strategy=
"hi_res"
,
    chunking_strategy=
"by_title"
,
)
# Replace with the path to your PDF file
让我们检查 PDF 文件中的分区元素。每个元素代表 Unstructured 分区过程中提取的内容块。
for
element
in
elements:
print
(element)
break
What is Milvus?

Milvus is a high-performance, highly scalable vector database that runs efficiently across a wide range of environments, from a laptop to large-scale distributed systems. It is available as both open-source software and a cloud service.
将数据插入 Milvus。
data = []
for
i, element
in
enumerate
(elements):
    data.append(
        {
"id"
: i,
"vector"
: emb_text(element.text),
"text"
: element.text,
"metadata"
: element.metadata.to_dict(),
        }
    )
milvus_client.insert(collection_name=collection_name, data=data)
{'insert_count': 29, 'ids': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28], 'cost': 0}
检索和生成响应
定义一个函数，从 Milvus 中检索相关文件。
def
retrieve_documents
(
question, top_k=
3
):
    search_res = milvus_client.search(
        collection_name=collection_name,
        data=[emb_text(question)],
        limit=top_k,
# search_params={"metric_type": "IP", "params": {}},
output_fields=[
"text"
],
    )
return
[(res[
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
]]
定义一个函数，使用 RAG 管道中检索到的文档生成响应。
def
generate_rag_response
(
question
):
    retrieved_docs = retrieve_documents(question)
    context =
"\n"
.join([
f"Text:
{doc[
0
]}
\n"
for
doc
in
retrieved_docs])
    system_prompt = (
"You are an AI assistant. Provide answers based on the given context."
)
    user_prompt =
f"""
    Use the following pieces of information to answer the question. If the information is not in the context, say you don't know.
    
    Context:
{context}
Question:
{question}
"""
response = openai_client.chat.completions.create(
        model=
"gpt-4o-mini"
,
        messages=[
            {
"role"
:
"system"
,
"content"
: system_prompt},
            {
"role"
:
"user"
,
"content"
: user_prompt},
        ],
    )
return
response.choices[
0
].message.content
让我们用一个示例问题来测试 RAG 管道。
question =
"What is the Advanced Search Algorithms in Milvus?"
answer = generate_rag_response(question)
print
(
f"Question:
{question}
"
)
print
(
f"Answer:
{answer}
"
)
Question: What is the Advanced Search Algorithms in Milvus?
Answer: The Advanced Search Algorithms in Milvus include a wide range of in-memory and on-disk indexing/search algorithms such as IVF, HNSW, and DiskANN. These algorithms have been deeply optimized, and Milvus delivers 30%-70% better performance compared to popular implementations like FAISS and HNSWLib.