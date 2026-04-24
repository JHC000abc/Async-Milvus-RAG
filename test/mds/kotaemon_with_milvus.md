使用 Milvus 的 Kotaemon RAG
Kotaemon
是一款开源、简洁、可定制的 RAG UI，用于与您的文档聊天。它的构建同时考虑到了最终用户和开发人员。
Kotaemon 提供了一个可定制的多用户文档 QA Web-UI，支持本地和基于 API 的 LLMs。它提供了一个具有全文和向量检索功能的混合 RAG 管道、针对带有图表的文档的多模式 QA 以及带有文档预览功能的高级引用。它支持 ReAct 和 ReWOO 等复杂的推理方法，并为检索和生成提供可配置的设置。
本教程将指导您如何使用
Milvus
自定义 kotaemon 应用程序。
前提条件
安装
我们推荐使用这种方式安装 kotaemon：
#
optional (setup
env
)
conda create -n kotaemon python=3.10
conda activate kotaemon

git clone https://github.com/Cinnamon/kotaemon
cd kotaemon

pip install -e "libs/kotaemon[all]"
pip install -e "libs/ktem"
除此以外，还有其他一些安装 kotaemon 的方法。详情请参考
官方文档
。
将 Milvus 设置为默认向量存储空间
要将默认向量存储改为 Milvus，必须修改
flowsettings.py
文件，将
KH_VECTORSTORE
切换为：
"__type__"
:
"kotaemon.storages.MilvusVectorStore"
设置环境变量
您可以通过
.env
文件配置模型，其中包含连接到 LLMs 和嵌入模型所需的信息。例如，OpenAI、Azure、Ollama 等。
运行 Kotaemon
设置好环境变量并更改向量存储后，就可以通过运行以下命令来运行 Kotaemon：
python app.py
默认用户名/密码为
admin
/
admin
使用 kotaemon 启动 RAG
1.添加人工智能模型
在
Resources
选项卡中，您可以添加和设置您的 LLMs 和 Embeddings 模型。您可以添加多个模型，并将它们设置为活动或非活动。您只需提供至少一个。您也可以提供多个模型，以便在它们之间切换。
2.上传文件
为了对文档进行质量保证，您需要先将文档上传到应用程序。导航到
File Index
选项卡，您就可以上传和管理自定义文档。
默认情况下，所有应用程序数据都存储在
./ktem_app_data
文件夹中。Milvus 数据库数据存储在
./ktem_app_data/user_data/vectorstore
中。你可以备份或复制该文件夹，以便将安装转移到新机器上。
3.与文档聊天
现在返回
Chat
选项卡。聊天 "选项卡由 3 个区域组成："对话设置面板"，用于管理对话和文件引用；"聊天面板"，用于与聊天机器人互动；以及 "信息面板"，用于显示支持证据、置信度分数和答案的相关性评级。
您可以在对话设置面板中选择文件。然后，只需在输入框中键入一条信息，就可以用文档启动 RAG，并将其发送给聊天机器人。
如果你想深入了解如何使用 kotaemon，可以从
官方文档
中获得全面指导。