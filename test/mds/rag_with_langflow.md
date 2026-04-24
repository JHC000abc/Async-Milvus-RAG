使用 Langflow 和 Milvus 构建 RAG 系统
本指南演示了如何使用
Langflow
与
Milvus
一起构建检索增强生成（RAG）管道。
RAG 系统首先从知识库中检索相关文档，然后根据上下文生成新的响应，从而增强文本生成功能。Milvus 用于存储和检索文本嵌入，而 Langflow 则有助于将检索和生成整合到可视化工作流程中。
Langflow 可以轻松构建 RAG 管道，将文本块嵌入其中，存储在 Milvus 中，并在进行相关查询时进行检索。这样，语言模型就能根据上下文生成响应。
Milvus 是一个可扩展的向量数据库，可以快速找到语义相似的文本，而 Langflow 则允许您管理管道处理文本检索和生成响应的方式。它们共同为基于文本的增强型应用提供了构建强大 RAG 管道的有效方法。
前提条件
在运行本笔记本之前，请确保您已安装以下依赖项：
$
python -m pip install langflow -U
教程
安装所有依赖项后，请输入以下命令启动 Langflow 面板：
$
python -m langflow run
然后会弹出一个仪表盘，如下所示：
langflow
我们要创建一个
Vector Store
项目，所以首先要点击
新建项目
按钮。这时会弹出一个面板，我们选择
向量存储 RAG
选项：
panel
Vector Store Rag 项目创建成功后，默认的向量存储是 AstraDB，而我们想使用 Milvus。因此，我们需要用 Milvus 替换这两个 astraDB 模块，以便使用 Milvus 作为向量存储。
astraDB
用 Milvus 替换 astraDB 的步骤：
删除现有的向量存储卡。点击上图中标红的两张 AstraDB 卡，按
退格
键删除它们。
点击侧边栏中的
Vector Store
选项，选择 Milvus 并将其拖入画布。这样做两次，因为我们需要 2 个 Milvus 卡，一个用于存储文件处理工作流，一个用于搜索工作流。
将 Milvus 模块链接到其余组件。请参考下图。
为两个 Milvus 模块配置 Milvus 凭据。最简单的方法是使用 Milvus Lite，将连接 URI 设置为 milvus_demo.db。如果您有自主部署的 Milvus 服务器或在 Zilliz Cloud 上，请将连接 URI 设置为服务器端点，将连接密码设置为令牌（对于 Milvus 是连接 "
:
"，对于 Zilliz Cloud 是 API Key）。请参考下图：
Milvus 结构演示
将知识嵌入 RAG 系统
通过左下角的文件模块上传文件作为 LLM 的知识库。这里我们上传了一个包含 Milvus 简介的文件
按右下角 Milvus 模块上的运行按钮，运行插入工作流程。这将把知识插入 Milvus 向量存储中。
测试知识是否在内存中。打开 playground，询问与上传文件相关的任何问题。
为什么选择 Milvus？