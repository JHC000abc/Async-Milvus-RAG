MCP + Milvus：连接人工智能与向量数据库
简介
模型上下文协议（MCP）
是一种开放式协议，可使人工智能应用程序（如 Claude 和 Cursor）与外部数据源和工具进行无缝交互。无论您是要构建自定义 AI 应用程序、集成 AI 工作流，还是要增强聊天界面，MCP 都能提供一种标准化的方式，将大型语言模型 (LLM) 与相关上下文数据连接起来。
本教程将指导您
为 Milvus 设置 MCP 服务器
，让人工智能应用能够使用
自然语言命令
执行向量搜索、管理 Collections 和检索数据，
而无需
编写自定义数据库查询。
前提条件
在设置 MCP 服务器之前，请确保您拥有
Python 3.10 或更高版本
运行中的
Milvus
实例
uv
（建议用于运行服务器）
开始使用
使用此 MCP 服务器的推荐方法是直接使用 uv 运行，无需安装。在下面的示例中，Claude Desktop 和 Cursor 就是这样配置的。
如果要克隆版本库：
git
clone
https://github.com/zilliztech/mcp-server-milvus.git
cd
mcp-server-milvus
则可直接运行服务器：
uv run src/mcp_server_milvus/server.py --milvus-uri http://localhost:19530
支持的应用程序
此 MCP 服务器可与各种支持模型上下文协议的 AI 应用程序配合使用，例如
克劳德桌面
：Anthropic 的克劳德桌面应用程序
光标
：人工智能代码编辑器，其 Composer 功能支持 MCP
其他自定义 MCP 客户端
任何执行 MCP 客户端规范的应用程序
将 MCP 与 Claude Desktop 结合使用
安装
Claude Desktop
。
打开 Claude 配置文件：
在 macOS 上：
~/Library/Application Support/Claude/claude_desktop_config.json
添加以下配置：
{
"mcpServers"
:
{
"milvus"
:
{
"command"
:
"/PATH/TO/uv"
,
"args"
:
[
"--directory"
,
"/path/to/mcp-server-milvus/src/mcp_server_milvus"
,
"run"
,
"server.py"
,
"--milvus-uri"
,
"http://localhost:19530"
]
}
}
}
重新启动 Claude Desktop 以应用更改。
在 Cursor 中使用 MCP
Cursor
还通过 Composer 中的 Agents 功能支持 MCP 工具。您可以通过两种方式将 Milvus MCP 服务器添加到 Cursor：
选项 1：使用 Cursor 设置用户界面
打开
Cursor Settings
→
Features
→
MCP
。
单击
+ Add New MCP Server
。
填写：
类型：
stdio
名称：
milvus
命令：
/PATH/TO/uv --directory /path/to/mcp-server-milvus/src/mcp_server_milvus run server.py --milvus-uri http://127.0.0.1:19530
⚠️ 提示：使用
127.0.0.1
而不是
localhost
，以避免潜在的 DNS 解析问题。
选项 2：使用特定于项目的配置（推荐）
在
项目根目录
下创建
.cursor/mcp.json
文件：
{
"mcpServers"
:
{
"milvus"
:
{
"command"
:
"/PATH/TO/uv"
,
"args"
:
[
"--directory"
,
"/path/to/mcp-server-milvus/src/mcp_server_milvus"
,
"run"
,
"server.py"
,
"--milvus-uri"
,
"http://127.0.0.1:19530"
]
}
}
}
重新启动 Cursor 以应用配置。
添加服务器后，您可能需要按下 MCP 设置中的刷新按钮来填充工具列表。当与您的查询相关时，Composer Agent 将自动使用 Milvus 工具。
验证集成
确保 MCP 服务器设置正确：
对于光标
转到
Cursor Settings
→
Features
→
MCP
。
确认
"Milvus"
出现在 MCP 服务器列表中。
检查是否列出了 Milvus 工具（如
milvus_list_collections
,
milvus_vector_search
）。
如果出现错误，请参阅下面的
故障排除
部分。
Milvus 的 MCP 服务器工具
该 MCP 服务器提供多种工具，用于
搜索、查询和管理 Milvus 中的向量数据
。有关详细信息，请参阅
mcp-server-milvus
文档。
搜索和查询工具
milvus-text-search
→ 使用全文检索搜索文档。
milvus-vector-search
→ 在 Collections 上执行向量相似性搜索。
milvus-hybrid-search
→ 结合向量相似性和属性过滤执行混合搜索。
milvus-multi-vector-search
→ 使用多个查询向量执行向量相似性搜索。
milvus-query
→ 使用过滤表达式查询 Collections。
milvus-count
→ 对集合中的实体进行计数。
📁 Collections 管理
milvus-list-collections
→ 列出数据库中的所有 Collections。
milvus-collection-info
→ 获取有关某个 Collection 的详细信息。
milvus-get-collection-stats
→ 获取有关 Collections 的统计数据。
milvus-create-collection
→ 使用指定的 Schema 创建新 Collection。
milvus-load-collection
→ 将 Collections 加载到内存中，以便搜索和查询。
milvus-release-collection
→ 从内存中释放一个 Collection。
milvus-get-query-segment-info
→ 获取有关查询段的信息。
milvus-get-collection-loading-progress
→ 获取 Collections 的加载进度。
数据操作符
milvus-insert-data
→ 将数据插入 Collections。
milvus-bulk-insert
→ 分批插入数据以提高性能。
milvus-upsert-data
→ 向上插入数据到 Collections 中（如果存在，则插入或更新）。
milvus-delete-entities
→ 根据过滤表达式从 Collections 中删除实体。
milvus-create-dynamic-field
→ 向现有 Collections 添加动态字段。
⚙️ 索引管理
milvus-create-index
→ 在向量字段上创建索引。
milvus-get-index-info
→ 获取集合中的索引信息。
环境变量
MILVUS_URI
→ Milvus 服务器 URI（可以设置为
--milvus-uri
）。
MILVUS_TOKEN
→ 可选的身份验证令牌。
MILVUS_DB
→ 数据库名称（默认为 "default"）。
开发
直接运行服务器：
uv run server.py --milvus-uri http://localhost:19530
示例
使用克劳德桌面
示例 1：列出 Collection
What are the collections
I
have in my Milvus DB?
Claude 将使用 MCP 在我们的 Milvus DB 上检查这些信息。
I
'll check what collections are available in your Milvus database.
> View result
from
milvus-list-collections
from
milvus (local)

Here are the collections
in
your Milvus database:
1
. rag_demo
2
. test
3
. chat_messages
4
. text_collection
5
. image_collection
6
. customized_setup
7
. streaming_rag_demo
示例 2：搜索文件
Find documents in
my
text_collection that mention
"machine learning"
克劳德将使用 Milvus 的全文搜索功能查找相关文档：
I
'll search for documents about machine learning in your text_collection.
> View result
from
milvus-
text
-search
from
milvus (local)

Here are the documents I found that mention machine learning:
[Results will appear here based
on
your actual data]
使用光标
示例：创建 Collections
在 Cursor 的 Composer 中，你可以询问：
Create a
new
collection called
'articles'
in
Milvus
with
fields
for
title
(
string
),
content
(
string
),
and
a vector
field
(
128
dimensions
)
Cursor 将使用 MCP 服务器执行此操作：
I
'll create a new collection called 'articles' with the specified fields.
> View result
from
milvus-create-collection
from
milvus (local)

Collection
'articles' has been created successfully with the following schema:
- title:
string
- content:
string
- vector: float vector[
128
]
故障排除
常见问题
连接错误
如果看到类似 "连接 Milvus 服务器失败 "的错误：
验证你的 Milvus 实例是否正在运行：
docker ps
（如果使用 Docker）
检查配置中的 URI 是否正确
确保没有防火墙规则阻止连接
尝试在 URI 中使用
127.0.0.1
而不是
localhost
身份验证问题
如果出现身份验证错误
验证
MILVUS_TOKEN
是否正确
检查你的 Milvus 实例是否需要身份验证
确保您有正确的权限来执行您尝试执行的操作符
找不到工具
如果 MCP 工具没有出现在克劳德桌面或光标中：
重新启动应用程序
检查服务器日志是否有任何错误
确认 MCP 服务器运行正常
按下 MCP 设置中的刷新按钮（适用于 Cursor）
获取帮助
如果您继续遇到问题：
查看
GitHub Issues
中的类似问题
加入
Zilliz 社区 Discord
寻求支持
提交一个新问题，并详细说明您的问题
结论
通过本教程，你现在已经可以运行
MCP 服务器
，在 Milvus 中启用人工智能驱动的向量搜索了。无论您使用的是
Claude Desktop
还是
Cursor
，现在都可以使用
自然语言命令
查询、管理和搜索 Milvus 数据库，
而无需
编写数据库代码！