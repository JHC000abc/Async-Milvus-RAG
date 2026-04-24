在 PrivateGPT 中使用 Milvus
PrivateGPT
是一个可投入生产的人工智能项目，它能让用户在没有互联网连接的情况下，使用大型语言模型对其文档提出问题，同时确保 100% 的隐私。PrivateGPT 提供的应用程序接口分为高级和低级区块。它还提供了一个 Gradio UI 客户端以及批量模型下载脚本和摄取脚本等实用工具。从概念上讲，PrivateGPT 封装了一个 RAG 管道并公开了其基元，可随时使用并提供 API 和 RAG 管道的完整实现。
在本教程中，我们将向您展示如何使用 Milvus 作为 PrivateGPT 的后端向量数据库。
本教程主要参考
PrivateGPT
官方安装指南。如果您发现本教程有过时的部分，可以优先参考官方指南，并向我们提出问题。
运行 PrivateGPT 的基本要求
1.克隆 PrivateGPT 仓库
克隆版本库并导航至版本库：
$
git
clone
https://github.com/zylon-ai/private-gpt
$
cd
private-gpt
2.安装诗歌
安装用于依赖关系管理的
Poetry
：按照 Poetry 官方网站上的说明进行安装。
3. （可选）安装 make
要运行各种脚本，需要安装 make。
macOS（使用 Homebrew）：安装 make：
$
brew install make
Windows （使用 Chocolatey）：
$
choco install make
安装可用模块
PrivateGPT 允许自定义设置某些模块，例如 LLM、Embeddings、向量存储、用户界面。
在本教程中，我们将使用以下模块：
LLM
: Ollama
Embeddings
：Ollama
向量存储
：Milvus
用户界面
Gradio
运行以下命令，使用诗歌来安装所需的模块依赖项：
$
poetry install --extras
"llms-ollama embeddings-ollama vector-stores-milvus ui"
启动 Ollama 服务
访问
ollama.ai
，按照说明在机器上安装 Ollama。
安装完成后，确保关闭 Ollama 桌面应用程序。
现在，启动 Ollama 服务（它将启动本地推理服务器，同时为 LLM 和 Embeddings 服务）：
$
ollama serve
安装要使用的模型，默认
settings-ollama.yaml
配置为用户
llama3.1
8b LLM (~4GB) 和
nomic-embed-text
Embeddings (~275MB)
默认情况下，PrivateGPT 会根据需要自动提取模型。可以通过修改
ollama.autopull_models
属性来改变这种行为。
无论如何，如果您想手动提取模型，请运行以下命令：
$
ollama pull llama3.1
$
ollama pull nomic-embed-text
您可以选择在
settings-ollama.yaml
文件中更改到您最喜欢的模型，然后手动拉取它们。
更改 Milvus 设置
在
settings-ollama.yaml
文件中，将 vectorstore 设置为 milvus：
vectorstore:
database:
milvus
你也可以添加一些累积的 Milvus 配置来指定你的设置。 像这样：
milvus:
uri:
http://localhost:19530
collection_name:
my_collection
可用的配置选项有
字段 选项
说明
uri
默认设置为 "local_data/private_gpt/milvus/milvus_local.db"，作为本地文件；你也可以在 docker 或 k8s 上设置性能更高的 Milvus 服务器，例如 http://localhost:19530，作为你的 uri；要使用
Zilliz Cloud
，请将 uri 和 token 调整为 Zilliz Cloud 中的
公共端点和 API 密钥
。
令牌
与 docker 或 k8s 上的 Milvus 服务器配对，或与 Zilliz Cloud 的 api 密钥配对。
集合名称
Collections 的名称，默认设置为 "milvus_db"。
覆盖
覆盖 Collection 中已存在的数据，默认设置为 "true"。
启动 PrivateGPT
完成所有设置后，即可通过 Gradio UI 运行 PrivateGPT。
PGPT_PROFILES=ollama make run
用户界面的网址是
http://0.0.0.0:8001
。
您可以玩转用户界面，并就您的文档提出问题。
更多详情，请参阅
PrivateGPT
官方文档。