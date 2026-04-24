用 Milvus 和 EmbedAnything 构建 RAG
EmbedAnything
是用 Rust 构建的快速、轻量级嵌入管道，支持文本、PDF、图像、音频等。
在本教程中，我们将演示如何使用 EmbedAnything 和
Milvus
一起构建检索增强生成（RAG）管道。EmbedAnything 使用可插拔的
适配器
系统，而不是与任何特定数据库紧密耦合--适配器作为封装器，定义了嵌入数据的格式化、索引和在目标向量存储中的存储方式。
通过将 EmbedAnything 与 Milvus 适配器配对，只需几行代码，您就可以从不同的文件类型生成嵌入信息，并将其高效地存储到 Milvus 中。
⚠️ 注：虽然 EmbedAnything 中的适配器可以处理插入 Milvus 的问题，但它并不支持开箱即用的搜索。要建立一个完整的 RAG 管道，您还需要单独实例化一个 MilvusClient，并将检索逻辑（如向量的相似性搜索）作为应用程序的一部分来实现。
准备工作
依赖关系和环境
$
pip install -qU pymilvus milvus-lite openai embed_anything
如果使用的是 Google Colab，要启用刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
克隆存储库并加载适配器
接下来，我们将克隆
EmbedAnything
软件仓库，并将
examples/adapters
目录添加到 Python 路径中。这是我们存储自定义 Milvus 适配器实现的地方，它允许 EmbedAnything 与 Milvus 通信以插入向量。
import
sys
# Clone the EmbedAnything repository if not already cloned
![ -d
"EmbedAnything"
] || git clone https://github.com/StarlightSearch/EmbedAnything.git
# Add the `examples/adapters` directory to the Python path
sys.path.append(
"EmbedAnything/examples/adapters"
)
print
(
"✅ EmbedAnything cloned and adapter path added."
)
✅ EmbedAnything cloned and adapter path added.
我们将在此 RAG 管道中使用 OpenAI 作为 LLM。您应将
api key
OPENAI_API_KEY
作为环境变量。
import
os
from
openai
import
OpenAI

os.environ[
"OPENAI_API_KEY"
] =
"sk-***********"
openai_client = OpenAI()
构建 RAG
初始化 Milvus
在嵌入任何文件之前，我们需要准备两个与 Milvus 交互的组件：
MilvusVectorAdapter
- 这是用于 EmbedAnything 的 Milvus 适配器，
仅用于向量摄取
（即插入嵌入和创建索引）。它目前
不
支持搜索操作符。
MilvusClient
- 这是来自
pymilvus
的官方客户端，可
完全访问
Milvus 功能，包括向量搜索、过滤和 Collections 管理。
为避免混淆：
将
MilvusVectorAdapter
视为用于存储向量的 "只写 "工具。
将
MilvusClient
视为 "读取-搜索 "引擎，用于为 RAG 实际执行查询和检索文档。
import
embed_anything
from
embed_anything
import
(
    WhichModel,
    EmbeddingModel,
)
from
milvus_db
import
MilvusVectorAdapter
from
pymilvus
import
MilvusClient
# Official Milvus client for full operations
milvus_client = MilvusClient(uri=
"./milvus.db"
, token=
""
)
# EmbedAnything adapter for pushing embeddings into Milvus
index_name =
"embed_anything_milvus_collection"
milvus_adapter = MilvusVectorAdapter(
    uri=
"./milvus.db"
, token=
""
, collection_name=index_name
)
# Delete existing collection if it exists
if
milvus_client.has_collection(index_name):
    milvus_client.drop_collection(index_name)
# Create a new collection with dimension matching the embedding model later used
milvus_adapter.create_index(dimension=
384
)
Ok - Milvus DB connection established.
Collection 'embed_anything_milvus_collection' created with index.
至于
MilvusVectorAdapter
和
MilvusClient
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
初始化嵌入模型并嵌入 PDF 文档
现在我们将初始化 Embeddings 模型。我们将使用 Sentence-transformers 库中的
all-MiniLM-L12-v2 model
，它是一个轻量级但功能强大的文本嵌入模型。它能生成 384 维的嵌入模型，因此与我们将 Milvus Collections 维数设置为 384 的做法一致。这种对齐至关重要，可以确保存储在 Milvus 中的向量维度与模型生成的向量维度之间的兼容性。
EmbedAnything 支持更多的嵌入模型。更多详情，请参阅
官方文档
。
# Initialize the embedding model
model = EmbeddingModel.from_pretrained_hf(
    WhichModel.Bert, model_id=
"sentence-transformers/all-MiniLM-L12-v2"
)
现在，让我们嵌入一个 PDF 文件。EmbedAnything 可以轻松处理 PDF（和更多）文档，并将其嵌入直接存储在 Milvus 中。
# Embed a PDF file
data = embed_anything.embed_file(
"./pdf_files/WhatisMilvus.pdf"
,
    embedder=model,
    adapter=milvus_adapter,
)
Converted 12 embeddings for insertion.
Successfully inserted 12 embeddings.
检索和生成响应
同样，EmbedAnything 的
MilvusVectorAdapter
目前只是一个轻量级抽象，仅用于向量摄取和索引。它
不支持搜索
或检索查询。因此，为了搜索相关文档以建立我们的 RAG 管道，我们必须直接使用
MilvusClient
实例 (
milvus_client
) 来查询我们的 Milvus 向量存储。
定义一个从 Milvus 检索相关文档的函数。
def
retrieve_documents
(
question, top_k=
3
):
    query_vector =
list
(
        embed_anything.embed_query([question], embedder=model)[
0
].embedding
    )
    search_res = milvus_client.search(
        collection_name=index_name,
        data=[query_vector],
        limit=top_k,
        output_fields=[
"text"
],
    )
    docs = [(res[
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
return
docs
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
"How does Milvus search for similar documents?"
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
Question: How does Milvus search for similar documents?
Answer: Milvus searches for similar documents primarily through Approximate Nearest Neighbor (ANN) search, which finds the top K vectors closest to a given query vector. It also supports various other types of searches, such as filtering search under specified conditions, range search within a specified radius, hybrid search based on multiple vector fields, and keyword search based on BM25. Additionally, it can perform reranking to adjust the order of search results based on additional criteria, refining the initial ANN search results.