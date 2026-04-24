将 Milvus 与 SambaNova 结合使用
SambaNova
是一个创新的人工智能技术平台，可加速部署先进的人工智能和深度学习功能。该平台专为企业使用而设计，使企业能够利用生成式人工智能来提高性能和效率。通过提供 SambaNova 套件和 DataScale 等尖端解决方案，该平台使企业能够从数据中提取有价值的洞察力，推动操作改进并促进人工智能领域的新机遇。
SambaNova AI 入门套件
是开源资源的 Collections，旨在帮助开发人员和企业利用 SambaNova 部署 AI 驱动的应用程序。这些工具包提供了实用的示例和指南，有助于实施各种人工智能用例，使用户更容易利用 SambaNova 的先进技术。
本教程利用 SambaNova AI 入门套件中的 Milvus 集成，构建一个类似于 RAG（Retrieval-Augmented Generation）的企业知识检索系统，用于基于企业私有文档的检索和回答。
本教程主要参考
SambaNova AI Starter Kits
官方指南。如果您发现本教程有过时的部分，可以优先参考官方指南，并向我们提出问题。
前提条件
我们建议使用 Python >= 3.10 和 < 3.12。
访问
SambaNova 云
获取 SambaNova API 密钥。
克隆版本库
$
git
clone
https://github.com/sambanova/ai-starter-kit.git
$
d ai-starter-kit/enterprise_knowledge_retriever
更改向量存储类型
通过在
create_vector_store()
和
src/document_retrieval.py
中的
load_vdb()
函数中设置
db_type='milvus'
来更改向量存储。
...
vectorstore =
self
.vectordb.create_vector_store(
    ..., db_type=
'milvus'
)
...
vectorstore =
self
.vectordb.load_vdb(..., db_type=
'milvus'
, ...)
安装依赖项
运行以下命令安装所需的依赖项：
python3 -m venv enterprise_knowledge_env
source enterprise_knowledge_env/bin/activate
pip install -r requirements.txt
启动应用程序
使用以下命令启动应用程序：
$ streamlit run streamlit/app.py --browser.gatherUsageStats
false
之后，您将在浏览器中看到用户界面：
http://localhost:8501/
在用户界面中设置 SambaNova API 密钥后，您就可以使用用户界面并就文档提问。
更多详情，请参阅
SambaNova AI 入门套件的企业知识检索
官方文档。