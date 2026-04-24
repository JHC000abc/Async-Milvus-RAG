Milvus WebUI
Milvus Web UI 是 Milvus 的图形化管理工具。它以简单直观的界面增强了系统的可观察性。您可以使用 Milvus Web UI 观察 Milvus 组件和依赖关系的统计和指标，检查数据库和 Collections 的详细信息，并列出详细的 Milvus 配置。
概述
Milvus Web UI 与 Birdwatcher 和 Attu 不同，它是一个内置工具，以简单直观的界面提供整体系统可观察性。
下表比较了 Milvus Web UI 和 Birdwatcher/Attu 的功能：
功能
Milvus 网络用户界面
Birdwatcher
Attu
操作符
图形用户界面
CLI
图形用户界面
目标用户
维护人员、开发人员
维护人员
开发人员
安装
内置
独立工具
独立工具
依赖关系
Milvus
Milvus / etcd
Milvus
主要功能
运行环境、数据库/ Collections 详情、段、通道、任务和慢查询请求
元数据检查和 Milvus API 执行
数据库管理和操作任务
自
v2.5.0
v2.0.0
v0.1.8
从 v2.5.0 起，你可以在运行中的 Milvus 实例上使用以下 URL 访问 Milvus Web UI：
http://
${MILVUS_PROXY_IP}
:9091/webui
功能
Milvus Web UI 提供以下功能：
Milvus Web UI 概述
主页
你可以找到关于当前运行的 Milvus 实例、其组件、连接的客户端和依赖关系的信息。
Collections
可查看 Milvus 当前的数据库和 Collections 列表，并检查其详细信息。
查询
您可以查看收集到的查询节点和查询协调器在网段、通道、副本和资源组方面的统计数据。
数据
您可以查看收集到的数据节点在网段和通道方面的统计数据。
任务
可以查看 Milvus 中运行的任务列表，包括 Querycoord 调度器任务、压缩任务、索引构建任务、导入任务和数据同步任务。
慢速请求
可以查看 Milvus 中的慢请求列表，包括请求类型、请求持续时间和请求参数。
配置
可以查看 Milvus 配置及其值的列表。
工具
您可以从 Web UI 访问两个内置工具，即 pprof 和 Milvus 数据可视化工具。
主页
在主页上，您可以找到以下信息：
Milvus Web UI 主页
系统信息
：查看系统信息，包括部署模式、部署中使用的映像和相关信息。
组件信息
：查看 Milvus 中组件的状态和指标，包括查询节点、数据节点、索引节点、协调器和代理的状态和指标。
已连接客户端
：查看已连接的客户端及其信息，包括 SDK 类型和版本、用户名及其访问历史记录。
系统依赖关系
：查看 Milvus 依赖项的状态和指标，包括元存储、消息队列和对象存储的状态和指标。
Collections
在 "Collections "页面，您可以查看 Milvus 当前的数据库和 Collections 列表，并检查它们的详细信息。
Milvus Web UI 集合
数据库
：查看当前 Milvus 中的数据库列表及其详细信息。
Collections
：查看每个数据库中的 Collection 列表及其详细信息。
可以点击某个 Collection 查看其详细信息，包括字段数量、分区、索引等详细信息。
Milvus Web UI Collectionions 详情
查询
Milvus Web UI 查询页面
分段
：查看分段列表及其详细信息，包括分段 ID、对应的 Collections、状态、大小等。
通道
：查看通道列表及其详细信息，包括通道名称、对应的 Collections 等。
副本
查看副本列表及其详细信息，包括副本 ID、对应的 Collections 等。
资源组
：查看资源组列表及其详细信息，包括资源组名称、组内查询节点数量及其配置等。
数据
Milvus Web UI 数据页面
分段
：查看数据节点/协调器的分段列表及其详细信息，包括分段 ID、对应的 Collections、状态、大小等。
通道
：查看数据节点/协调器的通道列表及其详细信息，包括通道名称、对应的 Collections 等。
任务
Milvus Web UI 任务页面
任务
：查看在 Milvus 中运行的任务列表，包括任务类型、状态和操作。
QueryCoord 任务
：查看所有 QueryCoord 调度器任务，包括过去 15 分钟内的平衡器、索引/区段/通道/领导者检查器。
压缩任务
：查看过去 15 分钟内来自数据协调器的所有压缩任务。
索引建立任务
：查看数据协调人员在过去 30 分钟内执行的所有索引建立任务。
导入任务
：查看过去 30 分钟内数据协调人员的所有导入任务。
数据同步任务
：查看过去 15 分钟内数据节点的所有数据同步任务。
慢请求
Milvus Web UI 慢请求页面
慢请求
：慢请求是指延迟时间超过配置中指定的
proxy.slowQuerySpanInSeconds
值的搜索或查询。慢速请求列表显示最近 15 分钟内的所有慢速请求。
配置
Milvus Web UI 配置页面
配置
：查看 Milvus 运行时配置及其值的列表。
工具
pprof
：访问用于剖析和调试 Milvus 的 pprof 工具。
Milvus 数据可视化工具
：访问 Milvus 数据可视化工具，以可视化 Milvus 中的数据。