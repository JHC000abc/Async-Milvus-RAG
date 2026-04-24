使用 Milvus 的知识表
Knowledge Table
由
WhyHow AI
开发，是一个开源软件包，旨在促进从非结构化文档中提取和探索结构化数据。它为用户提供了一个类似电子表格的界面，并能通过自然语言查询界面创建表格和图形等知识表征。该软件包包括可定制的提取规则、格式选项和通过出处进行的数据追踪，使其适用于各种应用。它支持无缝集成到 RAG 工作流中，既满足了需要用户友好界面的企业用户的需求，也满足了需要灵活后端来高效处理文档的开发人员的需求。
默认情况下，Knowledge Table 使用 Milvus 数据库来存储和检索提取的数据。这样，用户就可以利用 Milvus 的强大功能轻松搜索、过滤和分析数据。在本教程中，我们将介绍如何开始使用 Knowledge Table 和 Milvus。
先决条件
装载机
Docker Compose
克隆项目
$
git
clone
https://github.com/whyhow-ai/knowledge-table.git
设置环境
你可以在项目根目录下找到
.env.example
文件。将该文件复制到
.env
，并填写所需的环境变量。
对于 Milvus，应设置
MILVUS_DB_URI
和
MILVUS_DB_TOKEN
环境变量。以下是一些提示：
将
MILVUS_DB_URI
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
MILVUS_DB_URI
和
MILVUS_DB_TOKEN
，它们与 Zilliz Cloud 中的
公共端点和 Api 密钥
相对应。
除 Milvus 外，您还应设置其他环境，如
OPENAI_API_KEY
。您可以从相关网站获取这些信息。
启动应用程序
$ docker compose up -d --build
停止应用程序
$ docker compose down
访问项目
前台可从
http://localhost:3000
访问，后台可从
http://localhost:8000
访问。
您可以玩转用户界面，并尝试使用自己的文档。
如需进一步了解演示用法，请参阅官方
知识表文档
。