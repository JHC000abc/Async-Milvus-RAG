Milvus SDK 代码助手指南
概述
⚡️ 一次配置，永久提高效率！
还在为 LLM 过时的结果而苦恼吗？厌倦了 LLM 在版本更新后仍输出过时内容？试试这个 mcp，一劳永逸地解决开发 Milvus 相关代码时的信息滞后问题！
Milvus 官方 SDK 代码助手已经上线--只需找到对应的 AI IDE，配置一次，就让 AI 为你编写
官方推荐的
Milvus 代码。彻底告别过时的框架！
➡️ 现在就跳转：
快速入门
效果显示
下图比较了使用和不使用 Milvus SDK 代码助手生成代码的效果。如果不使用 Milvus SDK 代码助手，编写的代码会沿用旧的 ORM SDK 方法，这已不再推荐。以下是使用和未使用代码助手 MCP 的代码截图对比：
已启用
MCP 代码助手
禁用
MCP 代码助手
使用官方推荐的最新 MilvusClient 接口创建 Collections
不推荐使用旧版 ORM 界面创建 Collections。
快速启动
查找您的 AI IDE，一键配置，开启无忧编码之旅。
光标
转到
Settings
->
Cursor Settings
->
Tools & Intergrations
->
Add new global MCP server
光标麦克风设置
建议将以下配置粘贴到 Cursor
~/.cursor/mcp.json
文件中。您也可以通过在项目文件夹中创建
.cursor/mcp.json
来安装特定项目。更多信息请参见
Cursor MCP 文档
。
{
"mcpServers"
:
{
"sdk-code-helper"
:
{
"url"
:
"https://sdk.milvus.io/mcp/"
,
"headers"
:
{
"Accept"
:
"text/event-stream"
}
}
}
}
克劳德桌面
添加到您的 Claude Desktop 配置中：
{
"mcpServers"
:
{
"sdk-code-helper"
:
{
"url"
:
"https://sdk.milvus.io/mcp/"
,
"headers"
:
{
"Accept"
:
"text/event-stream"
}
}
}
}
克劳德代码
Claude Code 支持通过 JSON 配置直接添加 MCP 服务器，包括远程 URL 类型的服务器。使用以下命令向 Claude Code 添加配置：
claude mcp
add
-
json sdk
-
code
-
helper
--json '{
"url": "https://sdk.milvus.io/mcp/",
  "headers": {
    "Accept": "text/event-stream"
  }
}
'
Windsurf
Windsurf 支持通过 JSON 文件配置 MCP。将以下配置添加到 Windsurf MCP 设置中：
{
"mcpServers"
:
{
"sdk-code-helper"
:
{
"url"
:
"https://sdk.milvus.io/mcp/"
,
"headers"
:
{
"Accept"
:
"text/event-stream"
}
}
}
}
VS 代码
CodeIndexer MCP 服务器可通过 MCP 兼容扩展与 VS Code 一起使用。在 VS Code MCP 设置中添加以下配置：
{
"mcpServers"
:
{
"sdk-code-helper"
:
{
"url"
:
"https://sdk.milvus.io/mcp/"
,
"headers"
:
{
"Accept"
:
"text/event-stream"
}
}
}
}
Cherry Studio
Cherry Studio 允许通过其设置界面对 MCP 服务器进行可视化配置。虽然它不直接支持手动 JSON 配置，但你可以通过图形用户界面添加新服务器：
导航至设置 → MCP 服务器 → 添加服务器。
填写服务器详细信息：
名称：
sdk code helper
类型
Streamable HTTP
URL：
https://sdk.milvus.io/mcp/
标题：
"Accept": "text/event-stream"
保存配置以激活服务器。
Cherry Studio Mcp 设置
Cline
Cline 使用 JSON 配置文件管理 MCP 服务器。要整合所提供的 MCP 服务器配置，请
打开 Cline，点击顶部导航栏中的 MCP 服务器图标。
选择 "已安装 "选项卡，然后单击 "高级 MCP 设置"。
在
cline_mcp_settings.json
文件中，添加以下配置：
{
"mcpServers"
:
{
"sdk-code-helper"
:
{
"url"
:
"https://sdk.milvus.io/mcp/"
,
"headers"
:
{
"Accept"
:
"text/event-stream"
}
}
}
}
增强
按 Cmd/Ctrl Shift P 或转到 Augment 面板中的汉堡包菜单
选择编辑设置
在 "高级 "下，单击 settings.json 中的 "编辑
将服务器配置添加到
augment.advanced
对象中的
mcpServers
数组：
{
  "mcpServers": {
"sdk-code-helper": {
      "url": "https://sdk.milvus.io/mcp/",
      "headers": {
        "Accept": "text/event-stream"
      }
    }
  }
}
双子座 CLI
Gemini CLI 需要通过 JSON 文件手动配置：
创建或编辑
~/.gemini/settings.json
文件。
添加以下配置：
{
"mcpServers"
:
{
"sdk-code-helper"
:
{
"url"
:
"https://sdk.milvus.io/mcp/"
,
"headers"
:
{
"Accept"
:
"text/event-stream"
}
}
}
}
保存文件并重启 Gemini CLI 以应用更改。
Roo 代码
Roo 代码
Roo 代码为 MCP 服务器使用 JSON 配置文件：
打开 Roo 代码，导航至设置 → MCP 服务器 → 编辑全局配置。
在
mcp_settings.json
文件中，添加以下配置：
{
"mcpServers"
:
{
"sdk-code-helper"
:
{
"url"
:
"https://sdk.milvus.io/mcp/"
,
"headers"
:
{
"Accept"
:
"text/event-stream"
}
}
}
}
保存文件以激活服务器。