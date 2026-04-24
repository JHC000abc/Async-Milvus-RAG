用于人工智能代理的 Milvus
Milvus 提供代理友好界面，允许人工智能编码代理和自主代理系统以编程方式与向量数据库交互。无论您是要构建 RAG 管道、语义搜索还是代理记忆系统，Milvus 都能为代理提供多种连接和操作方法。
Agents 工具
Milvus 技能
Claude Code 的一项代理技能，教 LLMs 使用 PyMilvus 进行向量数据库操作。
MCP 服务器
模型上下文协议服务器，可让任何兼容 MCP 的 Agents 直接与 Milvus 交互。
克劳德上下文 MCP
为克劳德代码设计的 MCP 服务器，提供上下文感知的 Milvus 文档访问。
人工智能提示
经过编辑的提示，可帮助人工智能编码助手编写正确的 Milvus 代码。每个提示都包含防止最常见错误的规则和模式。
如何使用
从任何提示页面的 "完整提示 "部分
复制
一个提示。
将其
保存
到人工智能工具所需的文件中（见下
表
）。
您的人工智能助手在生成或审查 Milvus 代码时将自动应用这些规则。
提示页面
Agents.md
任何人工智能编码代理的顶级规则。如果您只需要一个文件，请从这里开始。
Python SDK
正确的连接模式、MilvusClient 使用和 ORM API 禁止。
Schema 设计
字段类型、主键、Schema 不变性和 BM25 配置。
搜索模式
带有关键约束规则的 ANN、混合和全文搜索。
索引选择
用于 AUTOINDEX、HNSW、DiskANN 和 IVF_FLAT 的决策树。
RAG 管道
使用 Milvus 的端到端检索增强生成流程。
在不同环境中使用
使用环境
提示位置
说明
光标
.cursor/rules/*.md
配置项目规则
GitHub 副驾驶
.github/copilot-instructions.md
自定义说明
克劳德代码
CLAUDE.md
克劳德代码文档
JetBrains 集成开发环境
guidelines.md
自定义指南
双子座 CLI
GEMINI.md
双子座 CLI 代码实验室
VS 代码
.instructions.md
配置 .instructions.md
风帆
guidelines.md
配置指南.md
推荐的 Agents 部署
选择合适的 Milvus 部署取决于你的开发阶段。
阶段
部署
为什么
原型开发
Milvus Lite
零配置，进程中。可在 Python 运行的任何地方运行，是快速代理原型开发的理想选择。
开发
Milvus 单机版
单节点 Docker 部署。适合本地开发和实际数据量测试。
生产
Zilliz Cloud
全面管理的无服务器 Milvus。无需管理基础设施 - Agents 只需连接和操作。
自托管生产
分布式 Milvus
多节点 Kubernetes 部署，适用于需要完全控制基础设施的团队。
对于代理工作负载，建议在生产中使用
Zilliz Cloud
。Agents 通常不管理基础设施，因此无服务器部署可消除操作开销，并提供自动扩展功能。