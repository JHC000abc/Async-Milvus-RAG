在 DocsGPT 中使用 Milvus
DocsGPT
是一种先进的开源解决方案，它通过集成强大的 GPT 模型简化了项目文档中信息的查找。它能让开发人员轻松获得有关项目问题的准确答案，消除耗时的手动搜索。
在本教程中，我们将向你展示如何使用 Milvus 作为 DocsGPT 的后台向量数据库。
本教程主要参考
DocsGPT
官方安装指南。如果你发现本教程有过时的部分，可以优先参考官方指南，并向我们提出问题。
安装要求
确保已安装
Docker
克隆版本库
克隆版本库并导航到它：
$
git
clone
https://github.com/arc53/DocsGPT.git
$
cd
DocsGPT
添加依赖关系
在
application
文件夹下的
requirements.txt
文件中添加
langchain-milvus
依赖关系：
$
echo
"\nlangchain-milvus==0.1.6"
>> ./application/requirements.txt
设置环境变量
将
VECTOR_STORE=milvus
,
MILVUS_URI=...
,
MILVUS_TOKEN=...
添加到
docker-compose.yaml
文件中
backend
和
worker
服务的环境变量中，就像这样：
backend:
build:
./application
environment:
-
VECTOR_STORE=milvus
-
MILVUS_URI=...
-
MILVUS_TOKEN=...
worker:
build:
./application
command:
celery
-A
application.app.celery
worker
-l
INFO
-B
environment:
-
VECTOR_STORE=milvus
-
MILVUS_URI=...
-
MILVUS_TOKEN=...
对于
MILVUS_URI
和
MILVUS_TOKEN
，您既可以使用完全托管的
Zilliz Cloud
(Recommended) 服务，也可以手动启动 Milvus 服务。
对于完全托管的 Zilliz 云服务：我们推荐使用 Zilliz Cloud 服务。您可以在
Zilliz Cloud
上注册一个免费试用账户。之后，您将获得
MILVUS_URI
和
MILVUS_TOKEN
，它们与
公共端点和 API 密钥
相对应。
用于手动启动 Milvus 服务：如果要设置 Milvus 服务，可以按照
Milvus 官方文档
设置 Milvus 服务器，然后从服务器获取
MILVUS_URI
和
MILVUS_TOKEN
。
MILVUS_URI
和
MILVUS_TOKEN
的格式应分别为
http://<your_server_ip>:19530
和
<your_username>:<your_password>
。
启动服务
运行：
./setup.sh
然后导航至 http://localhost:5173/。
您可以在用户界面上进行操作，并询问有关文件的问题。
alt文本
如果要停止服务，运行：
$
docker compose down
有关详细信息和更高级的设置，请参阅
DocsGPT
官方文档。