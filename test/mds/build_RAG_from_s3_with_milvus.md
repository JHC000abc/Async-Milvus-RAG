构建 RAG 管道：将数据从 S3 载入 Milvus
本教程将指导您使用 Milvus 和亚马逊 S3 构建检索增强生成（RAG）管道。您将学习如何高效地从 S3 存储桶中加载文档，将其分割成易于管理的块，并将其向量嵌入存储到 Milvus 中，以便进行快速、可扩展的检索。为了简化这一过程，我们将使用 LangChain 作为工具，从 S3 加载数据并将其存储到 Milvus 中。
准备工作
依赖和环境
$
pip install --upgrade --quiet pymilvus milvus-lite openai requests tqdm boto3 langchain langchain-core langchain-community langchain-text-splitters langchain-milvus langchain-openai bs4
如果您使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
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
"your-openai-api-key"
S3 配置
从 S3 加载文档需要以下配置：
AWS 访问密钥和秘钥
：将它们存储为环境变量，以便安全访问 S3 存储桶：
os.environ[
"AWS_ACCESS_KEY_ID"
] =
"your-aws-access-key-id"
os.environ[
"AWS_SECRET_ACCESS_KEY"
] =
"your-aws-secret-access-key"
S3 桶和文档
：指定桶名和文档名作为
S3FileLoader
类的参数。
from
langchain_community.document_loaders
import
S3FileLoader

loader = S3FileLoader(
    bucket=
"milvus-s3-example"
,
# Replace with your S3 bucket name
key=
"WhatIsMilvus.docx"
,
# Replace with your document file name
aws_access_key_id=os.environ[
"AWS_ACCESS_KEY_ID"
],
    aws_secret_access_key=os.environ[
"AWS_SECRET_ACCESS_KEY"
],
)
加载文档
：配置完成后，就可以将文档从 S3 加载到管道中：
documents = loader.load()
此步骤可确保文档成功从 S3 加载，并准备好在 RAG 管道中进行处理。
将文档分割成块
加载文档后，使用 LangChain 的
RecursiveCharacterTextSplitter
将内容分割成易于管理的块：
from
langchain_text_splitters
import
RecursiveCharacterTextSplitter
# Initialize a RecursiveCharacterTextSplitter for splitting text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=
2000
, chunk_overlap=
200
)
# Split the documents into chunks using the text_splitter
docs = text_splitter.split_documents(documents)
# Let's take a look at the first document
docs[
1
]
Document(metadata={'source': 's3://milvus-s3-example/WhatIsMilvus.docx'}, page_content='Milvus offers three deployment modes, covering a wide range of data scales—from local prototyping in Jupyter Notebooks to massive Kubernetes clusters managing tens of billions of vectors: \n\nMilvus Lite is a Python library that can be easily integrated into your applications. As a lightweight version of Milvus, it’s ideal for quick prototyping in Jupyter Notebooks or running on edge devices with limited resources. Learn more.\nMilvus Standalone is a single-machine server deployment, with all components bundled into a single Docker image for convenient deployment. Learn more.\nMilvus Distributed can be deployed on Kubernetes clusters, featuring a cloud-native architecture designed for billion-scale or even larger scenarios. This architecture ensures redundancy in critical components. Learn more. \n\nWhat Makes Milvus so Fast\U0010fc00 \n\nMilvus was designed from day one to be a highly efficient vector database system. In most cases, Milvus outperforms other vector databases by 2-5x (see the VectorDBBench results). This high performance is the result of several key design decisions: \n\nHardware-aware Optimization: To accommodate Milvus in various hardware environments, we have optimized its performance specifically for many hardware architectures and platforms, including AVX512, SIMD, GPUs, and NVMe SSD. \n\nAdvanced Search Algorithms: Milvus supports a wide range of in-memory and on-disk indexing/search algorithms, including IVF, HNSW, DiskANN, and more, all of which have been deeply optimized. Compared to popular implementations like FAISS and HNSWLib, Milvus delivers 30%-70% better performance.')
在此阶段，您的文档已从 S3 加载并分割成较小的块，可在检索-增强生成（RAG）管道中进行进一步处理。
使用 Milvus 向量存储构建 RAG 链
我们将用文档初始化一个 Milvus 向量存储，将文档加载到 Milvus 向量存储中，并在引擎盖下建立索引。
from
langchain_milvus
import
Milvus
from
langchain_openai
import
OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

vectorstore = Milvus.from_documents(
    documents=docs,
    embedding=embeddings,
    connection_args={
"uri"
:
"./milvus_demo.db"
,
    },
    drop_old=
False
,
# Drop the old Milvus collection if it exists
)
对于
connection_args
：
将
uri
设置为本地文件，如
./milvus.db
，是最方便的方法，因为它会自动利用
Milvus Lite
将所有数据存储到这个文件中。
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
，它们对应于 Zilliz Cloud 中的
公共端点和 Api 密钥
。
使用测试查询问题搜索 Milvus 向量存储中的文档。让我们看看排名前 1 的文档。
query =
"How can Milvus be deployed"
vectorstore.similarity_search(query, k=
1
)
[Document(metadata={'pk': 455631712233193487, 'source': 's3://milvus-s3-example/WhatIsMilvus.docx'}, page_content='Milvus offers three deployment modes, covering a wide range of data scales—from local prototyping in Jupyter Notebooks to massive Kubernetes clusters managing tens of billions of vectors: \n\nMilvus Lite is a Python library that can be easily integrated into your applications. As a lightweight version of Milvus, it’s ideal for quick prototyping in Jupyter Notebooks or running on edge devices with limited resources. Learn more.\nMilvus Standalone is a single-machine server deployment, with all components bundled into a single Docker image for convenient deployment. Learn more.\nMilvus Distributed can be deployed on Kubernetes clusters, featuring a cloud-native architecture designed for billion-scale or even larger scenarios. This architecture ensures redundancy in critical components. Learn more. \n\nWhat Makes Milvus so Fast\U0010fc00 \n\nMilvus was designed from day one to be a highly efficient vector database system. In most cases, Milvus outperforms other vector databases by 2-5x (see the VectorDBBench results). This high performance is the result of several key design decisions: \n\nHardware-aware Optimization: To accommodate Milvus in various hardware environments, we have optimized its performance specifically for many hardware architectures and platforms, including AVX512, SIMD, GPUs, and NVMe SSD. \n\nAdvanced Search Algorithms: Milvus supports a wide range of in-memory and on-disk indexing/search algorithms, including IVF, HNSW, DiskANN, and more, all of which have been deeply optimized. Compared to popular implementations like FAISS and HNSWLib, Milvus delivers 30%-70% better performance.')]
from
langchain_core.runnables
import
RunnablePassthrough
from
langchain_core.prompts
import
PromptTemplate
from
langchain_core.output_parsers
import
StrOutputParser
from
langchain_openai
import
ChatOpenAI
# Initialize the OpenAI language model for response generation
llm = ChatOpenAI(model_name=
"gpt-3.5-turbo"
, temperature=
0
)
# Define the prompt template for generating AI responses
PROMPT_TEMPLATE =
"""
Human: You are an AI assistant, and provides answers to questions by using fact based and statistical information when possible.
Use the following pieces of information to provide a concise answer to the question enclosed in <question> tags.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
<context>
{context}
</context>

<question>
{question}
</question>

The response should be specific and use statistics or numbers when possible.

Assistant:"""
# Create a PromptTemplate instance with the defined template and input variables
prompt = PromptTemplate(
    template=PROMPT_TEMPLATE, input_variables=[
"context"
,
"question"
]
)
# Convert the vector store to a retriever
retriever = vectorstore.as_retriever()
# Define a function to format the retrieved documents
def
format_docs
(
docs
):
return
"\n\n"
.join(doc.page_content
for
doc
in
docs)
使用 LCEL（LangChain Expression Language）构建 RAG 链。
rag_chain = (
    {
"context"
: retriever | format_docs,
"question"
: RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


res = rag_chain.invoke(query)
res
'Milvus can be deployed in three different modes: Milvus Lite for local prototyping and edge devices, Milvus Standalone for single-machine server deployment, and Milvus Distributed for deployment on Kubernetes clusters. These deployment modes cover a wide range of data scales, from small-scale prototyping to massive clusters managing tens of billions of vectors.'