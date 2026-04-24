与 Milvus 一起使用 NLWeb
微软的 NLWeb
是一个拟议的框架，可使用
Schema.org
、RSS 等格式和新兴的 MCP 协议为网站提供自然语言界面。
Milvus
作为 NLWeb 中的向量数据库后端，支持嵌入存储和高效向量相似性搜索，从而为自然语言处理应用实现强大的上下文检索功能。
本文档主要基于官方
快速入门
文档。如果您发现任何过时或不一致的内容，请优先使用官方文档，并随时向我们提出问题。
使用方法
NLWeb 可以配置为使用 Milvus 作为检索引擎。以下是如何使用 Milvus 设置和使用 NLWeb 的指南。
安装
克隆版本库并设置环境：
git
clone
https://github.com/microsoft/NLWeb
cd
NLWeb
python -m venv .venv
source
.venv/bin/activate
# or `.venv\Scripts\activate` on Windows
cd
code
pip install -r requirements.txt
pip install pymilvus
# Add Milvus Python client
配置 Milvus
要使用
Milvus
，请更新配置。
更新配置文件
code/config
打开
config_retrieval.yaml
文件，添加 Milvus 配置：
preferred_endpoint:
milvus_local
endpoints:
milvus_local:
database_path:
"../data/milvus.db"
# Set the collection name to use
index_name:
nlweb_collection
# Specify the database type
db_type:
milvus
加载数据
配置完成后，使用 RSS 源加载内容。
从
code
目录加载内容：
python -m tools.db_load https://feeds.libsyn.com/121695/rss Behind-the-Tech
这将把内容摄取到你的 Milvus Collections 中，同时存储文本数据和向量嵌入。
运行服务器
要启动 NLWeb，请从
code
目录运行：
python app-file.py
现在，您可以使用 http://localhost:8000/ 的网络用户界面或直接通过与 MCP 兼容的 REST API，通过自然语言查询内容。
更多阅读
Milvus 文档
NLWeb 源
聊天查询的生命
通过更改提示修改行为
修改控制流
修改用户界面