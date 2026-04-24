在 AnythingLLM 中使用 Milvus
AnythingLLM
是一款功能强大、注重隐私的一体化人工智能桌面应用程序，支持各种 LLMs、文档类型和向量数据库。它能让您建立一个类似于 ChatGPT 的私人助理，可以在本地运行，也可以远程托管，让您可以与您提供的任何文档进行智能聊天。
本指南将指导您在 AnythingLLM 中配置 Milvus 作为向量数据库，使您能够嵌入、存储和搜索您的文档，进行智能检索和聊天。
本教程基于官方 AnythingLLM 文档和实际使用步骤。如果用户界面或步骤有变化，请参考最新的官方文档，并随时提出改进建议。
1.前提条件
本地已安装
Milvus
或有
Zilliz Cloud
账户
已安装
AnythingLLM 桌面
准备好上传和嵌入的文档或数据源（PDF、Word、CSV、网页等）
2.将 Milvus 配置为向量数据库
打开 AnythingLLM，点击左下角的
设置
图标
打开设置
在左侧菜单中选择
AI Providers
>
Vector Database
选择向量数据库
在向量数据库提供者下拉菜单中，选择
Milvus
（或 Zilliz Cloud）
选择 Milvus
填写 Milvus 连接详情（本地 Milvus）。下面是一个例子：
Milvus DB 地址
：
http://localhost:19530
Milvus 用户名：
root
Milvus 密码：
Milvus
Milvus 连接
如果使用 Zilliz Cloud，请输入您的集群端点和 API 令牌：
Zilliz Cloud 连接
单击
保存更改
应用您的设置。
3.创建工作区并上传文档
输入工作区并单击
上传
图标打开文档上传对话框
打开上传对话框
您可以上传多种数据源：
本地文件
：PDF、Word、CSV、TXT、音频文件等。
网页
：粘贴 URL 并直接获取网站内容。
上传文件
上传或获取后，单击 "
移动到工作区
"将文档或数据移动到当前工作区
移动到工作区
选择文档或数据，点击 "
保存并嵌入
"。AnythingLLM 会自动将您的内容分块、嵌入并存储到 Milvus 中。
保存并嵌入
4.聊天并从 Milvus 获取答案
返回工作区聊天界面并提问。AnythingLLM 将搜索您的 Milvus 向量数据库中的相关内容，并使用 LLM 生成答案
与文档聊天