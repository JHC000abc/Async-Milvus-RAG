检索增强生成：使用 Apify 抓取网站并将数据保存到 Milvus 以用于问题解答
本教程介绍如何使用 Apify 的网站内容抓取器抓取网站，并将数据保存到 Milvus/Zilliz 向量数据库，以便日后用于问题解答。
Apify
是一个网络抓取和数据提取平台，提供一个拥有两千多个现成云工具（称为 Actors）的应用程序市场。这些工具非常适合从电子商务网站、社交媒体、搜索引擎、在线地图等处提取结构化数据。
例如，
网站内容
抓取
器
Actor 可以深入抓取网站，通过移除 cookie 模态、页脚或导航来清理 HTML，然后将 HTML 转换为 Markdown。
针对 Milvus/Zilliz 的 Apify 集成可以轻松地将数据从网络上传到向量数据库。
开始之前
在运行本笔记本之前，请确保您具备以下条件：
Apify 帐户和
APIFY_API_TOKEN
。
一个 OpenAI 账户和
OPENAI_API_KEY
一个
Zilliz Cloud 账户
（Milvus 的全面管理云服务）。
Zilliz 数据库 URI 和令牌
安装依赖项
$ pip install --upgrade --quiet  apify==
1.7
.2
langchain-core==
0.3
.5
langchain-milvus==
0.1
.5
langchain-openai==
0.2
.0
设置 Apify 和开放式 API 密钥
import
os
from
getpass
import
getpass

os.environ[
"APIFY_API_TOKEN"
] = getpass(
"Enter YOUR APIFY_API_TOKEN"
)
os.environ[
"OPENAI_API_KEY"
] = getpass(
"Enter YOUR OPENAI_API_KEY"
)
Enter YOUR APIFY_API_TOKEN··········
Enter YOUR OPENAI_API_KEY··········
设置 Milvus/Zilliz URI、令牌和 Collections 名称
你需要 Milvus/Zilliz 的 URI 和令牌来设置客户端。
如果你在
Docker 或 Kubernetes
上自行部署了 Milvus 服务器，请使用服务器地址和端口作为 URI，例如
http://localhost:19530
。如果在 Milvus 上启用了身份验证功能，请使用 "
:
" 作为令牌，否则令牌留为空字符串。
如果您使用
Zilliz Cloud
（Milvus 的全托管云服务），请调整
uri
和
token
，它们与 Zilliz Cloud 中的
公共端点和 API 密钥
相对应。
请注意，Collection 不需要事先存在。数据上传到数据库时，它会自动创建。
os.environ[
"MILVUS_URI"
] = getpass(
"Enter YOUR MILVUS_URI"
)
os.environ[
"MILVUS_TOKEN"
] = getpass(
"Enter YOUR MILVUS_TOKEN"
)

MILVUS_COLLECTION_NAME =
"apify"
Enter YOUR MILVUS_URI··········
Enter YOUR MILVUS_TOKEN··········
使用网站内容抓取器从 Milvus.io 抓取文本内容
接下来，我们将在 Apify Python SDK 中使用网站内容抓取器。我们先定义 actor_id 和 run_input，然后指定要保存到向量数据库的信息。
actor_id="apify/website-content-crawler"
是网站内容爬虫的标识符。爬虫的行为可以通过 run_input 参数完全控制（详情请查看
输入页面
）。在本例中，我们将抓取不需要 JavaScript 渲染的 Milvus 文档。因此，我们设置
crawlerType=cheerio
，定义
startUrls
，并通过设置
maxCrawlPages=10
来限制抓取页面的数量。
from
apify_client
import
ApifyClient

client = ApifyClient(os.getenv(
"APIFY_API_TOKEN"
))

actor_id =
"apify/website-content-crawler"
run_input = {
"crawlerType"
:
"cheerio"
,
"maxCrawlPages"
:
10
,
"startUrls"
: [{
"url"
:
"https://milvus.io/"
}, {
"url"
:
"https://zilliz.com/"
}],
}

actor_call = client.actor(actor_id).call(run_input=run_input)
网站内容抓取程序将彻底抓取网站，直到达到
maxCrawlPages
预先设定的限制。抓取的数据将存储在 Apify 平台的
Dataset
中。要访问和分析这些数据，可以使用
defaultDatasetId
dataset_id = actor_call[
"defaultDatasetId"
]
dataset_id
'P9dLFfeJAljlePWnz'
以下代码可从 Apify
Dataset
获取刮擦数据，并显示第一个刮擦的网站
item = client.dataset(dataset_id).list_items(limit=
1
).items
item[
0
].get(
"text"
)
'The High-Performance Vector Database Built for Scale\nStart running Milvus in seconds\nfrom pymilvus import MilvusClient client = MilvusClient("milvus_demo.db") client.create_collection( collection_name="demo_collection", dimension=5 )\nDeployment Options to Match Your Unique Journey\nMilvus Lite\nLightweight, easy to start\nVectorDB-as-a-library runs in notebooks/ laptops with a pip install\nBest for learning and prototyping\nMilvus Standalone\nRobust, single-machine deployment\nComplete vector database for production or testing\nIdeal for datasets with up to millions of vectors\nMilvus Distributed\nScalable, enterprise-grade solution\nHighly reliable and distributed vector database with comprehensive toolkit\nScale horizontally to handle billions of vectors\nZilliz Cloud\nFully managed with minimal operations\nAvailable in both serverless and dedicated cluster\nSaaS and BYOC options for different security and compliance requirements\nTry Free\nLearn more about different Milvus deployment models\nLoved by GenAI developers\nBased on our research, Milvus was selected as the vector database of choice (over Chroma and Pinecone). Milvus is an open-source vector database designed specifically for similarity search on massive datasets of high-dimensional vectors.\nWith its focus on efficient vector similarity search, Milvus empowers you to build robust and scalable image retrieval systems. Whether you’re managing a personal photo library or developing a commercial image search application, Milvus offers a powerful foundation for unlocking the hidden potential within your image collections.\nBhargav Mankad\nSenior Solution Architect\nMilvus is a powerful vector database tailored for processing and searching extensive vector data. It stands out for its high performance and scalability, rendering it perfect for machine learning, deep learning, similarity search tasks, and recommendation systems.\nIgor Gorbenko\nBig Data Architect\nStart building your GenAI app now\nGuided with notebooks developed by us and our community\nRAG\nTry Now\nImage Search\nTry Now\nMultimodal Search\nTry Now\nUnstructured Data Meetups\nJoin a Community of Passionate Developers and Engineers Dedicated to Gen AI.\nRSVP now\nWhy Developers Prefer Milvus for Vector Databases\nScale as needed\nElastic scaling to tens of billions of vectors with distributed architecture.\nBlazing fast\nRetrieve data quickly and accurately with Global Index, regardless of scale.\nReusable Code\nWrite once, and deploy with one line of code into the production environment.\nFeature-rich\nMetadata filtering, hybrid search, multi-vector and more.\nWant to learn more about Milvus? View our documentation\nJoin the community of developers building GenAI apps with Milvus, now with over 25 million downloads\nGet Milvus Updates\nSubscribe to get updates on the latest Milvus releases, tutorials and training from Zilliz, the creator and key maintainer of Milvus.'
要将数据上传到 Milvus 数据库，我们使用
Apify Milvus 集成
。首先，我们需要为 Milvus 数据库设置参数。接下来，我们选择要存储到数据库中的字段 (
datasetFields
)。在下面的示例中，我们要保存
text
字段和
metadata.title
。
milvus_integration_inputs = {
"milvusUri"
: os.getenv(
"MILVUS_URI"
),
"milvusToken"
: os.getenv(
"MILVUS_TOKEN"
),
"milvusCollectionName"
: MILVUS_COLLECTION_NAME,
"datasetFields"
: [
"text"
,
"metadata.title"
],
"datasetId"
: actor_call[
"defaultDatasetId"
],
"performChunking"
:
True
,
"embeddingsApiKey"
: os.getenv(
"OPENAI_API_KEY"
),
"embeddingsProvider"
:
"OpenAI"
,
}
现在，我们将调用
apify/milvus-integration
来存储数据
actor_call = client.actor(
"apify/milvus-integration"
).call(
    run_input=milvus_integration_inputs
)
现在，所有搜刮到的数据都存储在 Milvus 数据库中，可以进行检索和问题解答了
检索和 LLM 生成管道
接下来，我们将使用 Langchain 定义检索增强管道。该管道分两个阶段工作：
向量存储（Milvus）：Langchain 通过匹配查询嵌入和存储的文档嵌入，从 Milvus 中检索相关文档。
LLM 响应：检索到的文档为 LLM（如 GPT-4）提供上下文，以便生成有依据的答案。
有关 RAG 链的更多详情，请参阅
Langchain 文档
。
from
langchain_core.output_parsers
import
StrOutputParser
from
langchain_core.prompts
import
PromptTemplate
from
langchain_core.runnables
import
RunnablePassthrough
from
langchain_milvus.vectorstores
import
Milvus
from
langchain_openai
import
ChatOpenAI, OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model=
"text-embedding-3-small"
)

vectorstore = Milvus(
    connection_args={
"uri"
: os.getenv(
"MILVUS_URI"
),
"token"
: os.getenv(
"MILVUS_TOKEN"
),
    },
    embedding_function=embeddings,
    collection_name=MILVUS_COLLECTION_NAME,
)

prompt = PromptTemplate(
    input_variables=[
"context"
,
"question"
],
    template=
"Use the following pieces of retrieved context to answer the question. If you don't know the answer, "
"just say that you don't know. \nQuestion: {question} \nContext: {context} \nAnswer:"
,
)
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


rag_chain = (
    {
"context"
: vectorstore.as_retriever() | format_docs,
"question"
: RunnablePassthrough(),
    }
    | prompt
    | ChatOpenAI(model=
"gpt-4o-mini"
)
    | StrOutputParser()
)
一旦数据库中有了数据，我们就可以开始提问了
question =
"What is Milvus database?"
rag_chain.invoke(question)
'Milvus is an open-source vector database specifically designed for billion-scale vector similarity search. It facilitates efficient management and querying of vector data, which is essential for applications involving unstructured data, such as AI and machine learning. Milvus allows users to perform operations like CRUD (Create, Read, Update, Delete) and vector searches, making it a powerful tool for handling large datasets.'
结论
在本教程中，我们演示了如何使用 Apify 抓取网站内容，将数据存储在 Milvus 向量数据库中，并使用检索增强管道来执行问题解答任务。通过将 Apify 的网络抓取功能与用于向量存储的 Milvus/Zilliz 和用于语言模型的 Langchain 相结合，您可以构建高效的信息检索系统。
为了改进数据库中的数据 Collections 和更新，Apify 集成提供
增量更新
，根据校验和只更新新的或修改过的数据。此外，它还能自动
删除
在指定时间内未抓取的
过时
数据。这些功能有助于保持向量数据库的优化，并确保您的检索增强管道保持高效和最新，只需最少的人工。
有关 Apify-Milvus 集成的更多详情，请参阅
Apify Milvus 文档
和
集成 README 文件
。