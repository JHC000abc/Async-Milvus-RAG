开始使用 Dynamiq 和 Milvus
Dynamiq
是一个功能强大的 Gen AI 框架，可简化人工智能应用的开发。凭借对检索增强生成（RAG）和大型语言模型（LLM）Agent 的强大支持，Dynamiq 使开发人员能够轻松高效地创建智能动态系统。
在本教程中，我们将探讨如何将 Dynamiq 与
Milvus
（专为 RAG 工作流打造的高性能向量数据库）无缝结合使用。Milvus 擅长向量嵌入的高效存储、索引和检索，是要求快速、精确访问上下文数据的人工智能系统不可或缺的组件。
本分步指南将涵盖两个核心 RAG 工作流程：
文档索引流程
：了解如何处理输入文件（如 PDF），将其内容转换为向量嵌入，并存储到 Milvus 中。利用 Milvus 的高性能索引功能，可确保您的数据随时可供快速检索。
文档检索流程
：了解如何查询 Milvus 中的相关文档嵌入，并利用它们与 Dynamiq 的 LLM Agents 一起生成有洞察力的上下文感知响应，从而创建无缝的人工智能驱动的用户体验。
本教程结束时，您将对 Milvus 和 Dynamiq 如何协同工作，根据您的需求量身打造可扩展的上下文感知人工智能系统有一个扎实的了解。
准备工作
下载所需程序库
$
pip install dynamiq pymilvus milvus-lite
如果使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
配置 LLM Agent
在本例中，我们将使用 OpenAI 作为 LLM。您应将
api key
OPENAI_API_KEY
设置为环境变量。
import
os

os.environ[
"OPENAI_API_KEY"
] =
"sk-***********"
RAG - 文档索引流程
本教程演示了以 Milvus 为向量数据库编制文档索引的检索增强生成（RAG）工作流程。该工作流程接收输入的 PDF 文件，将其处理成较小的块，使用 OpenAI 的嵌入模型生成向量嵌入，并将嵌入存储在 Milvus Collections 中，以便高效检索。
本工作流程结束时，您将拥有一个可扩展的高效文档索引系统，可支持语义搜索和问题解答等未来的 RAG 任务。
导入所需库并初始化工作流
# Importing necessary libraries for the workflow
from
io
import
BytesIO
from
dynamiq
import
Workflow
from
dynamiq.nodes
import
InputTransformer
from
dynamiq.connections
import
(
    OpenAI
as
OpenAIConnection,
    Milvus
as
MilvusConnection,
    MilvusDeploymentType,
)
from
dynamiq.nodes.converters
import
PyPDFConverter
from
dynamiq.nodes.splitters.document
import
DocumentSplitter
from
dynamiq.nodes.embedders
import
OpenAIDocumentEmbedder
from
dynamiq.nodes.writers
import
MilvusDocumentWriter
# Initialize the workflow
rag_wf = Workflow()
定义 PDF 转换器节点
converter = PyPDFConverter(document_creation_mode=
"one-doc-per-page"
)
converter_added = rag_wf.flow.add_nodes(
    converter
)
# Add node to the DAG (Directed Acyclic Graph)
定义文档分割器节点
document_splitter = DocumentSplitter(
    split_by=
"sentence"
,
# Splits documents into sentences
split_length=
10
,
    split_overlap=
1
,
    input_transformer=InputTransformer(
        selector={
"documents"
:
f"$
{[converter.
id
]}
.output.documents"
,
        },
    ),
).depends_on(
    converter
)
# Set dependency on the PDF converter
splitter_added = rag_wf.flow.add_nodes(document_splitter)
# Add to the DAG
定义 Embeddings 节点
embedder = OpenAIDocumentEmbedder(
    connection=OpenAIConnection(api_key=os.environ[
"OPENAI_API_KEY"
]),
    input_transformer=InputTransformer(
        selector={
"documents"
:
f"$
{[document_splitter.
id
]}
.output.documents"
,
        },
    ),
).depends_on(
    document_splitter
)
# Set dependency on the splitter
document_embedder_added = rag_wf.flow.add_nodes(embedder)
# Add to the DAG
定义 Milvus 向量存储节点
vector_store = (
    MilvusDocumentWriter(
        connection=MilvusConnection(
            deployment_type=MilvusDeploymentType.FILE, uri=
"./milvus.db"
),
        index_name=
"my_milvus_collection"
,
        dimension=
1536
,
        create_if_not_exist=
True
,
        metric_type=
"COSINE"
,
    )
    .inputs(documents=embedder.outputs.documents)
# Connect to embedder output
.depends_on(embedder)
# Set dependency on the embedder
)
milvus_writer_added = rag_wf.flow.add_nodes(vector_store)
# Add to the DAG
2024-11-19 22:14:03 - WARNING - Environment variable 'MILVUS_API_TOKEN' not found
2024-11-19 22:14:03 - INFO - Pass in the local path ./milvus.db, and run it using milvus-lite
2024-11-19 22:14:04 - DEBUG - Created new connection using: 0bef2849fdb1458a85df8bb9dd27f51d
2024-11-19 22:14:04 - INFO - Collection my_milvus_collection does not exist. Creating a new collection.
2024-11-19 22:14:04 - DEBUG - Successfully created collection: my_milvus_collection
2024-11-19 22:14:05 - DEBUG - Successfully created an index on collection: my_milvus_collection
2024-11-19 22:14:05 - DEBUG - Successfully created an index on collection: my_milvus_collection
Milvus 提供两种部署类型，以满足不同的使用情况：
MilvusDeploymentType.FILE
本地原型
或
小规模数据
存储的理想选择。
将
uri
设置为本地文件路径（如
./milvus.db
），以利用
Milvus Lite
，它可自动将所有数据存储到指定文件中。
这是
快速设置
和
实验的
便捷选项。
MilvusDeploymentType.HOST
专为
大规模数据
场景设计，例如管理超过一百万个向量。
自托管服务器
使用
Docker 或 Kubernetes
部署高性能 Milvus 服务器。
将服务器地址和端口配置为
uri
（如
http://localhost:19530
）。
如果启用了身份验证：
提供
<your_username>:<your_password>
作为
token
。
如果禁用了身份验证：
不设置
token
。
Zilliz Cloud（托管服务）
要获得全面管理、基于云的 Milvus 体验，请使用
Zilliz Cloud
。
根据 Zilliz Cloud 控制台提供的
公共端点和 API 密钥
设置
uri
和
token
。
定义输入数据并运行工作流
file_paths = [
"./pdf_files/WhatisMilvus.pdf"
]
input_data = {
"files"
: [BytesIO(
open
(path,
"rb"
).read())
for
path
in
file_paths],
"metadata"
: [{
"filename"
: path}
for
path
in
file_paths],
}
# Run the workflow with the prepared input data
inserted_data = rag_wf.run(input_data=input_data)
/var/folders/09/d0hx80nj35sb5hxb5cpc1q180000gn/T/ipykernel_31319/3145804345.py:4: ResourceWarning: unclosed file <_io.BufferedReader name='./pdf_files/WhatisMilvus.pdf'>
  BytesIO(open(path, "rb").read()) for path in file_paths
ResourceWarning: Enable tracemalloc to get the object allocation traceback
2024-11-19 22:14:09 - INFO - Workflow 87878444-6a3d-43f3-ae32-0127564a959f: execution started.
2024-11-19 22:14:09 - INFO - Flow b30b48ec-d5d2-4e4c-8e25-d6976c8a9c17: execution started.
2024-11-19 22:14:09 - INFO - Node PyPDF File Converter - 6eb42b1f-7637-407b-a3ac-4167bcf3b5c4: execution started.
2024-11-19 22:14:09 - INFO - Node PyPDF File Converter - 6eb42b1f-7637-407b-a3ac-4167bcf3b5c4: execution succeeded in 58ms.
2024-11-19 22:14:09 - INFO - Node DocumentSplitter - 5baed580-6de0-4dcd-bace-d7d947ab6c7f: execution started.
/Users/jinhonglin/anaconda3/envs/myenv/lib/python3.11/site-packages/websockets/legacy/__init__.py:6: DeprecationWarning: websockets.legacy is deprecated; see https://websockets.readthedocs.io/en/stable/howto/upgrade.html for upgrade instructions
  warnings.warn(  # deprecated in 14.0 - 2024-11-09
/Users/jinhonglin/anaconda3/envs/myenv/lib/python3.11/site-packages/pydantic/fields.py:804: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'is_accessible_to_agent'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.7/migration/
  warn(
2024-11-19 22:14:09 - INFO - Node DocumentSplitter - 5baed580-6de0-4dcd-bace-d7d947ab6c7f: execution succeeded in 104ms.
2024-11-19 22:14:09 - INFO - Node OpenAIDocumentEmbedder - 91928f67-a00f-48f6-a864-f6e21672ec7e: execution started.
2024-11-19 22:14:09 - INFO - Node OpenAIDocumentEmbedder - d30a4cdc-0fab-4aff-b2e5-6161a62cb6fd: execution started.
2024-11-19 22:14:10 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2024-11-19 22:14:10 - INFO - Node OpenAIDocumentEmbedder - d30a4cdc-0fab-4aff-b2e5-6161a62cb6fd: execution succeeded in 724ms.
2024-11-19 22:14:10 - INFO - Node MilvusDocumentWriter - dddab4cc-1dae-4e7e-9101-1ec353f530da: execution started.
2024-11-19 22:14:10 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2024-11-19 22:14:10 - INFO - Node MilvusDocumentWriter - dddab4cc-1dae-4e7e-9101-1ec353f530da: execution succeeded in 66ms.
2024-11-19 22:14:10 - INFO - Node OpenAIDocumentEmbedder - 91928f67-a00f-48f6-a864-f6e21672ec7e: execution succeeded in 961ms.
2024-11-19 22:14:10 - INFO - Flow b30b48ec-d5d2-4e4c-8e25-d6976c8a9c17: execution succeeded in 1.3s.
2024-11-19 22:14:10 - INFO - Workflow 87878444-6a3d-43f3-ae32-0127564a959f: execution succeeded in 1.3s.
通过这个工作流程，我们成功实现了一个文档索引管道，使用 Milvus 作为向量数据库，并使用 OpenAI 的 Embeddings 模型进行语义表示。这一设置实现了快速、准确的基于向量的检索，为语义搜索、文档检索和上下文人工智能驱动的交互等 RAG 工作流程奠定了基础。
借助 Milvus 的可扩展存储功能和 Dynamiq 的协调功能，该解决方案既可用于原型开发，也可用于大规模生产部署。现在，您可以扩展这一管道，将基于检索的问题解答或人工智能驱动的内容生成等额外任务纳入其中。
RAG 文档检索流程
在本教程中，我们将实现一个检索-增强生成（RAG）文档检索工作流。该工作流接收用户查询，为其生成向量嵌入，从 Milvus 向量数据库中检索最相关的文档，并使用大型语言模型（LLM）根据检索到的文档生成详细的、上下文感知的答案。
通过遵循这一工作流程，您将创建一个用于语义搜索和问题解答的端到端解决方案，将基于向量的文档检索功能与 OpenAI 高级 LLMs 的能力结合起来。这种方法可利用文档数据库中存储的知识，对用户查询做出高效、智能的响应。
导入所需库并初始化工作流程
from
dynamiq
import
Workflow
from
dynamiq.connections
import
(
    OpenAI
as
OpenAIConnection,
    Milvus
as
MilvusConnection,
    MilvusDeploymentType,
)
from
dynamiq.nodes.embedders
import
OpenAITextEmbedder
from
dynamiq.nodes.retrievers
import
MilvusDocumentRetriever
from
dynamiq.nodes.llms
import
OpenAI
from
dynamiq.prompts
import
Message, Prompt
# Initialize the workflow
retrieval_wf = Workflow()
定义 OpenAI 连接和文本嵌入器
# Establish OpenAI connection
openai_connection = OpenAIConnection(api_key=os.environ[
"OPENAI_API_KEY"
])
# Define the text embedder node
embedder = OpenAITextEmbedder(
    connection=openai_connection,
    model=
"text-embedding-3-small"
,
)
# Add the embedder node to the workflow
embedder_added = retrieval_wf.flow.add_nodes(embedder)
定义 Milvus 文档检索器
document_retriever = (
    MilvusDocumentRetriever(
        connection=MilvusConnection(
            deployment_type=MilvusDeploymentType.FILE, uri=
"./milvus.db"
),
        index_name=
"my_milvus_collection"
,
        dimension=
1536
,
        top_k=
5
,
    )
    .inputs(embedding=embedder.outputs.embedding)
# Connect to embedder output
.depends_on(embedder)
# Dependency on the embedder node
)
# Add the retriever node to the workflow
milvus_retriever_added = retrieval_wf.flow.add_nodes(document_retriever)
2024-11-19 22:14:19 - WARNING - Environment variable 'MILVUS_API_TOKEN' not found
2024-11-19 22:14:19 - INFO - Pass in the local path ./milvus.db, and run it using milvus-lite
2024-11-19 22:14:19 - DEBUG - Created new connection using: 98d1132773af4298a894ad5925845fd2
2024-11-19 22:14:19 - INFO - Collection my_milvus_collection already exists. Skipping creation.
定义提示模板
# Define the prompt template for the LLM
prompt_template =
"""
Please answer the question based on the provided context.

Question: {{ query }}

Context:
{% for document in documents %}
- {{ document.content }}
{% endfor %}
"""
# Create the prompt object
prompt = Prompt(messages=[Message(content=prompt_template, role=
"user"
)])
定义答案生成器
answer_generator = (
    OpenAI(
        connection=openai_connection,
        model=
"gpt-4o"
,
        prompt=prompt,
    )
    .inputs(
        documents=document_retriever.outputs.documents,
        query=embedder.outputs.query,
    )
    .depends_on(
        [document_retriever, embedder]
    )
# Dependencies on retriever and embedder
)
# Add the answer generator node to the workflow
answer_generator_added = retrieval_wf.flow.add_nodes(answer_generator)
运行工作流
# Run the workflow with a sample query
sample_query =
"What is the Advanced Search Algorithms in Milvus?"
result = retrieval_wf.run(input_data={
"query"
: sample_query})

answer = result.output.get(answer_generator.
id
).get(
"output"
, {}).get(
"content"
)
print
(answer)
2024-11-19 22:14:22 - INFO - Workflow f4a073fb-dfb6-499c-8cac-5710a7ad6d47: execution started.
2024-11-19 22:14:22 - INFO - Flow b30b48ec-d5d2-4e4c-8e25-d6976c8a9c17: execution started.
2024-11-19 22:14:22 - INFO - Node OpenAITextEmbedder - 47afb0bc-cf96-429d-b58f-11b6c935fec3: execution started.
2024-11-19 22:14:23 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
2024-11-19 22:14:23 - INFO - Node OpenAITextEmbedder - 47afb0bc-cf96-429d-b58f-11b6c935fec3: execution succeeded in 474ms.
2024-11-19 22:14:23 - INFO - Node MilvusDocumentRetriever - 51c8311b-4837-411f-ba42-21e28239a2ee: execution started.
2024-11-19 22:14:23 - INFO - Node MilvusDocumentRetriever - 51c8311b-4837-411f-ba42-21e28239a2ee: execution succeeded in 23ms.
2024-11-19 22:14:23 - INFO - Node LLM - ac722325-bece-453f-a2ed-135b0749ee7a: execution started.
2024-11-19 22:14:24 - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2024-11-19 22:14:24 - INFO - Node LLM - ac722325-bece-453f-a2ed-135b0749ee7a: execution succeeded in 1.8s.
2024-11-19 22:14:25 - INFO - Flow b30b48ec-d5d2-4e4c-8e25-d6976c8a9c17: execution succeeded in 2.4s.
2024-11-19 22:14:25 - INFO - Workflow f4a073fb-dfb6-499c-8cac-5710a7ad6d47: execution succeeded in 2.4s.


The advanced search algorithms in Milvus include a variety of in-memory and on-disk indexing/search algorithms such as IVF (Inverted File), HNSW (Hierarchical Navigable Small World), and DiskANN. These algorithms have been deeply optimized to enhance performance, delivering 30%-70% better performance compared to popular implementations like FAISS and HNSWLib. These optimizations are part of Milvus's design to ensure high efficiency and scalability in handling vector data.