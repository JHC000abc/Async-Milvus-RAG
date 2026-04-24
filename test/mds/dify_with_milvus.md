使用 Milvus 部署 Dify
Dify
是一个开源平台，旨在通过将 Backend-as-a-Service 与 LLMOps 相结合来简化人工智能应用程序的构建。它支持主流 LLMs，提供直观的提示协调界面、高质量的 RAG 引擎和灵活的 AI Agents 框架。凭借低代码工作流、易用的界面和 API，Dify 使开发人员和非技术用户都能专注于创建创新的、真实世界的人工智能解决方案，而无需处理复杂的问题。
在本教程中，我们将向您展示如何使用 Milvus 部署 Dify，以实现高效检索和 RAG 引擎。
本文档主要基于
Dify
官方
文档
。如果您发现任何过时或不一致的内容，请优先使用官方文档，并随时向我们提出问题。
先决条件
克隆资源库
克隆 Dify 源代码到本地计算机：
git clone https://github.com/langgenius/dify.git
准备环境配置
导航至 Dify 源代码中的 Docker 目录
cd dify/docker
复制环境配置文件
cp .env.example .env
部署选项
你可以使用两种不同的方法通过 Milvus 部署 Dify。请选择最适合您需求的一种：
方案 1：使用 Milvus 和 Docker
该选项使用 Docker Compose 在本地计算机上运行 Milvus 容器和 Dify。
配置环境变量
用以下 Milvus 配置编辑
.env
文件：
VECTOR_STORE=milvus
MILVUS_URI=http://host.docker.internal:19530
MILVUS_TOKEN=
MILVUS_URI
使用
host.docker.internal:19530
，允许 Docker 容器通过 Docker 的内部网络访问在主机上运行的 Milvus。
MILVUS_TOKEN
可以留空，用于本地 Milvus 部署。
启动 Docker 容器
使用
milvus
配置文件启动容器，以包含 Milvus 服务：
docker compose --profile milvus up -d
此命令将与
milvus-standalone
、
etcd
和
minio
容器一起启动 Dify 服务。
选项 2：使用 Zilliz Cloud
此选项将 Dify 连接到 Zilliz Cloud 上受管理的 Milvus 服务。
配置环境变量
使用 Zilliz Cloud 连接详细信息编辑
.env
文件：
VECTOR_STORE
=milvus
MILVUS_URI
=YOUR_ZILLIZ_CLOUD_ENDPOINT
MILVUS_TOKEN
=YOUR_ZILLIZ_CLOUD_API_KEY
用 Zilliz Cloud 的
公共端点
替换
YOUR_ZILLIZ_CLOUD_ENDPOINT
。
用 Zilliz Cloud 的
API 密钥
替换
YOUR_ZILLIZ_CLOUD_API_KEY
。
启动 Docker 容器
只启动 Dify 容器，不启动 Milvus 配置文件：
docker compose up -d
访问 Dify
登录 Dify
打开浏览器，进入 Dify 安装页面，您可以在这里设置您的管理员账户：
http://localhost/install
，然后登录 Dify 主页面以进一步使用。
更多使用方法和指导，请参阅
Dify 文档
。