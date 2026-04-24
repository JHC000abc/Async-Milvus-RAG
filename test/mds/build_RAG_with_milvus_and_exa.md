使用 Exa 和 Milvus 构建双源 RAG Agent
本教程演示了如何构建一个同时搜索
公共网络
（通过
Exa
）和
私人知识库
（通过
Milvus
），然后合成统一答案的 Agents。该代理使用 OpenAI 的函数调用功能，根据用户的问题自动决定查询哪个来源。
Exa
是专为人工智能应用设计的搜索 API，它由
Zilliz Cloud
（全面管理 Milvus）提供技术支持，这也是
Zilliz Cloud
的骄傲。与传统的基于关键字的搜索引擎不同，Exa 支持语义（神经）搜索--您用自然语言描述您想要什么，它就能理解您的意图。它还提供内容提取、高亮显示和基于类别的过滤功能。
Milvus
是为可扩展的相似性搜索而构建的开源向量数据库。通过将它们与 LLM Agents 相结合，您就可以在一个工作流中建立一个既能检索内部专有数据又能检索最新网络信息的系统。
前提条件
在运行本笔记本之前，请确保已安装以下依赖项：
$
pip install exa_py pymilvus openai
如果使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
您需要
Exa
和
OpenAI
的 API 密钥。将它们设置为环境变量：
import os

os.environ["EXA_API_KEY"] = "***********"
os.environ["OPENAI_API_KEY"] = "sk-***********"
初始化客户端
设置 Exa、OpenAI 和 Milvus 客户端。我们使用 OpenAI 的
text-embedding-3-small
模型生成向量嵌入，并使用 Milvus Lite 进行本地向量存储，基础设施设置为零。
import
json
from
openai
import
OpenAI
from
pymilvus
import
MilvusClient, DataType
from
exa_py
import
Exa

llm = OpenAI()
exa = Exa(api_key=os.environ[
"EXA_API_KEY"
])
milvus = MilvusClient(uri=
"./milvus_exa_demo.db"
)

EMBED_MODEL =
"text-embedding-3-small"
EMBED_DIM =
1536
COLLECTION =
"private_kb"
至于
MilvusVectorAdapter
和
MilvusClient
的参数：
将
uri
设置为本地文件，如
./milvus.db
，是最方便的方法，因为它会自动利用
Milvus Lite
将所有数据存储在此文件中。
如果你有大规模数据，比如超过一百万个向量，你可以在
Docker 或 Kubernetes
上设置性能更强的 Milvus 服务器。在此设置中，请使用服务器地址和端口作为 uri，例如
http://localhost:19530
。如果在 Milvus 上启用了身份验证功能，请使用 "
:
" 作为令牌，否则不要设置令牌。
如果您想使用
Zilliz Cloud
（Milvus 的全托管云服务），请调整
uri
和
token
，它们与 Zilliz Cloud 中的
公共端点和 Api 密钥
相对应。
定义生成 Embeddings 的辅助函数。我们将在笔记本的索引和查询中重复使用该函数：
def
embed_text
(
text:
str
|
list
[
str
]
) ->
list
:
"""Generate embedding vector(s) using OpenAI."""
resp = llm.embeddings.create(
input
=text
if
isinstance
(text,
list
)
else
[text],
        model=EMBED_MODEL,
    )
if
isinstance
(text,
list
):
return
[item.embedding
for
item
in
resp.data]
return
resp.data[
0
].embedding
构建私有知识库（Milvus）
我们模拟了一组公司内部文档，包括产品规格、政策、收益报告和 API 文档，这些文档不会出现在公共网络上。在真实场景中，这些文档可能来自内部维基、数据库或文档管理系统。
private_docs = [
    {
"id"
:
1
,
"text"
: (
"Acme Widget Pro supports up to 10,000 concurrent connections. "
"It uses a proprietary compression algorithm (AcmeZip v3) that "
"reduces payload size by 72% compared to gzip."
),
"source"
:
"product-spec.pdf"
,
    },
    {
"id"
:
2
,
"text"
: (
"Our return policy allows customers to return any product within "
"30 days of purchase for a full refund. After 30 days, only store "
"credit is offered. Damaged items must be reported within 48 hours."
),
"source"
:
"return-policy.md"
,
    },
    {
"id"
:
3
,
"text"
: (
"Q3 2025 revenue was $4.2M, up 18% from Q2. The growth was "
"primarily driven by enterprise customers adopting Widget Pro. "
"Churn rate dropped to 3.1%."
),
"source"
:
"q3-earnings.pdf"
,
    },
    {
"id"
:
4
,
"text"
: (
"Internal API rate limits: free tier 100 req/min, pro tier "
"5,000 req/min, enterprise tier 50,000 req/min. Rate limit "
"headers are X-RateLimit-Remaining and X-RateLimit-Reset."
),
"source"
:
"api-docs.md"
,
    },
    {
"id"
:
5
,
"text"
: (
"Employee onboarding checklist: 1) Sign NDA, 2) Set up VPN access, "
"3) Enroll in mandatory security training, 4) Request Jira and "
"Confluence access from IT, 5) Schedule 1:1 with manager."
),
"source"
:
"onboarding-guide.md"
,
    },
]
使用明确的 Schema 创建 Collections，嵌入文档并插入它们：
if
milvus.has_collection(COLLECTION):
    milvus.drop_collection(COLLECTION)

schema = milvus.create_schema(auto_id=
False
, enable_dynamic_field=
True
)
schema.add_field(field_name=
"id"
, datatype=DataType.INT64, is_primary=
True
)
schema.add_field(field_name=
"vector"
, datatype=DataType.FLOAT_VECTOR, dim=EMBED_DIM)
schema.add_field(field_name=
"text"
, datatype=DataType.VARCHAR, max_length=
65535
)
schema.add_field(field_name=
"source"
, datatype=DataType.VARCHAR, max_length=
512
)

index_params = milvus.prepare_index_params()
index_params.add_index(
    field_name=
"vector"
, index_type=
"AUTOINDEX"
, metric_type=
"COSINE"
)

milvus.create_collection(
    collection_name=COLLECTION,
    schema=schema,
    index_params=index_params,
# consistency_level="Strong",
)
# Embed all documents in one batch call
embeddings = embed_text([doc[
"text"
]
for
doc
in
private_docs])

milvus.insert(
    collection_name=COLLECTION,
    data=[
        {
"id"
: doc[
"id"
],
"vector"
: emb,
"text"
: doc[
"text"
],
"source"
: doc[
"source"
],
        }
for
doc, emb
in
zip
(private_docs, embeddings)
    ],
)
print
(
f"Inserted
{
len
(private_docs)}
documents into Milvus."
)
Inserted 5 documents into Milvus.
让我们通过快速测试查询来验证检索是否有效：
query =
"What is the return policy?"
results = milvus.search(
    collection_name=COLLECTION,
    data=[embed_text(query)],
    limit=
2
,
    output_fields=[
"text"
,
"source"
],
)
for
hit
in
results[
0
]:
print
(
f"[score=
{hit[
'distance'
]:
.3
f}
] (
{hit[
'entity'
][
'source'
]}
)"
)
print
(
f"
{hit[
'entity'
][
'text'
][:
120
]}
..."
)
print
()
[score=0.665] (return-policy.md)
  Our return policy allows customers to return any product within 30 days of purchase for a full refund. After 30 days, on...

[score=0.119] (q3-earnings.pdf)
  Q3 2025 revenue was $4.2M, up 18% from Q2. The growth was primarily driven by enterprise customers adopting Widget Pro. ...
探索 Exa 的搜索功能
在构建代理之前，让我们先来探索一下 Exa 的搜索功能。Exa 支持多种搜索模式，适用于不同场景。
带内容提取的
语义搜索
--Exa 不仅能返回链接，还能在单个请求中返回文章文本、关键要点和人工智能生成的摘要：
web_results = exa.search_and_contents(
    query=
"latest trends in AI agents 2026"
,
type
=
"auto"
,
    num_results=
3
,
    text={
"max_characters"
:
3000
},
    highlights={
"num_sentences"
:
3
},
)
for
r
in
web_results.results:
print
(
f"[
{r.title}
]"
)
print
(
f"  URL:
{r.url}
"
)
if
r.highlights:
print
(
f"  Highlight:
{r.highlights[
0
][:
150
]}
..."
)
print
()
[The AI Trends Shaping 2026. A month into the new year is as good a… | by ODSC - Open Data Science | Mar, 2026 | Medium]
  URL: https://odsc.medium.com/the-ai-trends-shaping-2026-34078dad4d49
  Highlight:  ahead. January brought Claude CoWork, Anthropic’s “AI coworker” that turns agents into desktop collaborators; OpenClaw (formerly Moltbot, formerly Cl...

[AI agent trends 2026 report]
  URL: https://cloud.google.com/resources/content/ai-agent-trends-2026
  Highlight: >. The era of simple prompts is over. We're witnessing the agent leap—where AI orchestrates complex, end-to-end workflows semi-autonomously. For enter...

[The Rise of Agentic AI: Why 2026 is the Year AI Started 'Doing']
  URL: https://www.marketdrafts.com/2026/02/rise-of-agentic-ai-2026-trends.html?m=1
  Highlight:  The era of "Generative AI" (which creates content) is being superseded by "Agentic AI" (which executes actions). We are witnessing a fundamental arch...
基于类别的过滤
--您可以将结果限制为特定的内容类型，如
"research paper"
、
"news"
、
"company"
或
"tweet"
。这在您需要高质量来源并希望避免噪音时非常有用：
filtered_results = exa.search_and_contents(
    query=
"retrieval augmented generation real world applications"
,
    category=
"research paper"
,
    num_results=
3
,
    highlights={
"num_sentences"
:
2
},
)
for
r
in
filtered_results.results:
print
(
f"-
{r.title}
"
)
print
(
f"
{r.url}
\n"
)
- 10 RAG examples and use cases from real companies
  https://www.evidentlyai.com/blog/rag-examples

- Implementing Retrieval-Augmented Generation (RAG) with Real-World Constraints
  https://dev.to/dextralabs/implementing-retrieval-augmented-generation-rag-with-real-world-constraints-3ajm

- 
  https://www.arxiv.org/pdf/2502.14930
查找类似文章
--给定 URL 后，Exa 可以查找内容类似的其他文章。这有助于从一个良好的起点扩展研究：
if
web_results.results:
    source_url = web_results.results[
0
].url
    similar = exa.find_similar_and_contents(
        url=source_url,
        num_results=
3
,
        highlights={
"num_sentences"
:
2
},
    )
print
(
f"Articles similar to:
{source_url}
\n"
)
for
r
in
similar.results:
print
(
f"-
{r.title}
"
)
print
(
f"
{r.url}
\n"
)
Articles similar to: https://odsc.medium.com/the-ai-trends-shaping-2026-34078dad4d49

- AI Trends 2026: From Agent Demos to Production Reality
  https://opendatascience.com/the-ai-trends-shaping-2026/

- The Most Important AI Trends to Watch in 2026
  https://medium.com/the-ai-studio/the-most-important-ai-trends-to-watch-in-2026-54af64d45021
定义 Agents 工具
现在我们来定义 Agents 将使用的两个工具功能。私人知识库工具使用向量相似性搜索 Milvus，而网络工具则通过 Exa 搜索公共互联网：
def
search_private_kb
(
query:
str
) ->
str
:
"""Search the internal knowledge base using Milvus vector search."""
results = milvus.search(
        collection_name=COLLECTION,
        data=[embed_text(query)],
        limit=
3
,
        output_fields=[
"text"
,
"source"
],
    )
    chunks = []
for
hit
in
results[
0
]:
        chunks.append(
f"[
{hit[
'entity'
][
'source'
]}
]
{hit[
'entity'
][
'text'
]}
"
)
return
"\n\n"
.join(chunks)
if
chunks
else
"No relevant internal documents found."
def
search_web
(
query:
str
) ->
str
:
"""Search the public web using Exa for up-to-date information."""
results = exa.search_and_contents(
        query=query,
type
=
"auto"
,
        num_results=
3
,
        highlights={
"num_sentences"
:
3
},
    )
    items = []
for
r
in
results.results:
        highlight = r.highlights[
0
]
if
r.highlights
else
"No snippet available."
items.append(
f"[
{r.title}
](
{r.url}
)\n
{highlight}
"
)
return
"\n\n"
.join(items)
if
items
else
"No web results found."
TOOL_FNS = {
"search_private_kb"
: search_private_kb,
"search_web"
: search_web,
}
构建代理
Agents 使用 OpenAI 的
函数调用
来决定调用哪个工具。它遵循一个简单的循环：LLM 接收用户查询，决定调用哪些工具（如果有的话），执行这些工具，然后根据检索到的上下文合成最终答案。
TOOLS = [
    {
"type"
:
"function"
,
"function"
: {
"name"
:
"search_private_kb"
,
"description"
: (
"Search the company's internal knowledge base (product docs, "
"policies, earnings, API docs, HR guides). Use this for any "
"question about internal/proprietary information."
),
"parameters"
: {
"type"
:
"object"
,
"properties"
: {
"query"
: {
"type"
:
"string"
,
"description"
:
"The search query"
}
                },
"required"
: [
"query"
],
            },
        },
    },
    {
"type"
:
"function"
,
"function"
: {
"name"
:
"search_web"
,
"description"
: (
"Search the public web for up-to-date external information - "
"news, trends, competitor analysis, open-source projects, etc. "
"Use this when the question is about the outside world."
),
"parameters"
: {
"type"
:
"object"
,
"properties"
: {
"query"
: {
"type"
:
"string"
,
"description"
:
"The search query"
}
                },
"required"
: [
"query"
],
            },
        },
    },
]

SYSTEM_PROMPT =
"""You are a helpful assistant with access to two search tools:

1. **search_private_kb** - searches the company's internal knowledge base.
2. **search_web** - searches the public internet via Exa.

Routing rules:
- Questions about internal products, policies, metrics, or processes: use search_private_kb.
- Questions about external trends, news, competitors, or general knowledge: use search_web.
- Questions that need both internal and external context: call BOTH tools, then synthesize.

Always cite your sources. For internal docs, mention the filename. For web results, include the URL."""
def
run_agent
(
user_query:
str
) ->
str
:
"""Run the agent loop: LLM -> tool calls -> LLM -> final answer."""
messages = [
        {
"role"
:
"system"
,
"content"
: SYSTEM_PROMPT},
        {
"role"
:
"user"
,
"content"
: user_query},
    ]
print
(
f"User:
{user_query}
\n"
)
# First LLM call - may request tool calls
response = llm.chat.completions.create(
        model=
"gpt-4o"
,
        messages=messages,
        tools=TOOLS,
    )
    msg = response.choices[
0
].message
    messages.append(msg)
# If no tool calls, return directly
if
not
msg.tool_calls:
print
(
f"Agent (no tools used):
{msg.content}
"
)
return
msg.content
# Execute each tool call
for
tc
in
msg.tool_calls:
        fn_name = tc.function.name
        fn_args = json.loads(tc.function.arguments)
print
(
f"  -> Calling
{fn_name}
(query=
{fn_args[
'query'
]!r}
)"
)

        result = TOOL_FNS[fn_name](**fn_args)
        messages.append(
            {
"role"
:
"tool"
,
"tool_call_id"
: tc.
id
,
"content"
: result,
            }
        )
# Second LLM call - synthesize final answer
response = llm.chat.completions.create(
        model=
"gpt-4o"
,
        messages=messages,
        tools=TOOLS,
    )
    answer = response.choices[
0
].message.content
print
(
f"\nAgent:\n
{answer}
"
)
return
answer
演示
现在，让我们用三种场景来测试 Agents，展示不同的路由行为。
场景 A：内部问题（路由至 Milvus）
询问有关内部政策的问题--代理应调用
search_private_kb
并从我们的私人文档中检索答案：
run_agent(
"What is the return policy for Acme products?"
)
User: What is the return policy for Acme products?



  -> Calling search_private_kb(query='return policy Acme products')



Agent:
The Acme products return policy allows customers to return any product within 30 days of purchase for a full refund. After 30 days, only store credit is offered. It's important to note that damaged items must be reported within 48 hours of receipt ([source: return-policy.md]).





"The Acme products return policy allows customers to return any product within 30 days of purchase for a full refund. After 30 days, only store credit is offered. It's important to note that damaged items must be reported within 48 hours of receipt ([source: return-policy.md])."
情景 B：外部问题（路由至 Exa）
询问外部趋势 - Agents 应致电
search_web
，从公共互联网上获取最新信息：
run_agent(
"What are the latest AI agent frameworks trending in 2026?"
)
User: What are the latest AI agent frameworks trending in 2026?



  -> Calling search_web(query='latest AI agent frameworks 2026')



Agent:
In 2026, several AI agent frameworks are trending, each offering unique features and capabilities that cater to various needs. Here are some of the most prominent ones:

1. **LangChain and LangGraph**: These frameworks remain highly popular for building large language model (LLM)-powered applications. LangGraph, in particular, models agents as state graphs, which is useful for action-oriented workflows. LangChain continues to dominate due to its comprehensive feature set for production-grade control and orchestration.

2. **LangSmith Agent Builder**: Released into general availability in 2026, this tool allows teams to create AI agents using natural language, simplifying the process of agent development.

3. **Semantic Kernel and AutoGen**: These have been integrated into Azure AI Foundry, creating a unified framework. Semantic Kernel uses a plugin-based middleware pattern, enhancing existing applications with AI capabilities efficiently.

4. **OpenClaw**: An open-source framework that operates locally, OpenClaw transforms your computer into an autonomous agent host, differing from cloud-based solutions by keeping data and operations localized. This framework supports a large community and includes extensive skills for customization.

These frameworks cater to various requirements, whether it's production-grade solutions, open-source options, or frameworks focused on local deployment. Each framework has its strengths, depending on the use case and the existing ecosystem it fits into.

Sources:
- [Agentic AI Frameworks: The Complete Guide (2026)](https://aiagentskit.com/blog/agentic-ai-frameworks/)
- [OpenClaw: The Open-Source AI Agent Framework That Runs Your Life Locally](https://www.clawbot.blog/blog/openclaw-the-open-source-ai-agent-framework-that-runs-your-life-locally)
- [The Best AI Agent Frameworks for 2026](https://medium.com/data-science-collective/the-best-ai-agent-frameworks-for-2026-tier-list-b3a4362fac0d)





"In 2026, several AI agent frameworks are trending, each offering unique features and capabilities that cater to various needs. Here are some of the most prominent ones:\n\n1. **LangChain and LangGraph**: These frameworks remain highly popular for building large language model (LLM)-powered applications. LangGraph, in particular, models agents as state graphs, which is useful for action-oriented workflows. LangChain continues to dominate due to its comprehensive feature set for production-grade control and orchestration.\n\n2. **LangSmith Agent Builder**: Released into general availability in 2026, this tool allows teams to create AI agents using natural language, simplifying the process of agent development.\n\n3. **Semantic Kernel and AutoGen**: These have been integrated into Azure AI Foundry, creating a unified framework. Semantic Kernel uses a plugin-based middleware pattern, enhancing existing applications with AI capabilities efficiently.\n\n4. **OpenClaw**: An open-source framework that operates locally, OpenClaw transforms your computer into an autonomous agent host, differing from cloud-based solutions by keeping data and operations localized. This framework supports a large community and includes extensive skills for customization.\n\nThese frameworks cater to various requirements, whether it's production-grade solutions, open-source options, or frameworks focused on local deployment. Each framework has its strengths, depending on the use case and the existing ecosystem it fits into.\n\nSources:\n- [Agentic AI Frameworks: The Complete Guide (2026)](https://aiagentskit.com/blog/agentic-ai-frameworks/)\n- [OpenClaw: The Open-Source AI Agent Framework That Runs Your Life Locally](https://www.clawbot.blog/blog/openclaw-the-open-source-ai-agent-framework-that-runs-your-life-locally)\n- [The Best AI Agent Frameworks for 2026](https://medium.com/data-science-collective/the-best-ai-agent-frameworks-for-2026-tier-list-b3a4362fac0d)"
情景 C：混合问题（同时访问两者）
提出一个既需要内部规格又需要外部基准的问题--Agent 应同时调用这两种工具并进行综合比较：
run_agent(
"How does our Widget Pro's throughput compare to "
"open-source alternatives on the market?"
)
User: How does our Widget Pro's throughput compare to open-source alternatives on the market?



  -> Calling search_private_kb(query='Widget Pro throughput comparison')


  -> Calling search_web(query='open-source widget throughput comparison')



Agent:
The throughput of our Widget Pro is quite competitive when compared to open-source alternatives on the market. Here's a detailed comparison:

### Widget Pro

- **Concurrent Connections**: Supports up to 10,000 concurrent connections.
- **Compression**: Utilizes AcmeZip v3, a proprietary compression algorithm that reduces payload size by 72% compared to gzip (source: [product-spec.pdf]).
- **API Rate Limits**: Offers different tiers:
  - Free tier: 100 requests/minute.
  - Pro tier: 5,000 requests/minute.
  - Enterprise tier: 50,000 requests/minute (source: [api-docs.md]).

### Open-Source Alternatives

From the available resources, open-source widget solutions such as Chatwoot and Tiledesk are popular in handling customer engagement with a flexible and customizable approach (source: [ChatMaxima article](https://chatmaxima.com/blog/15-open-source-free-live-chat-widget-solutions-to-boost-your-customer-engagement-in-2024/)). However, specific throughput metrics such as maximum concurrent connections or API limits are generally not highlighted in open-source product descriptions unless directly benchmarked.

These alternatives often emphasize customization, control, and integration with AI-driven capabilities but do not always specify throughput in terms comparable with Widget Pro. They might be more suited for organizations looking to tailor solutions to specific needs rather than focusing solely on throughput efficiency.

In conclusion, Widget Pro appears to offer high throughput suitable for enterprises with robust API support, while open-source options offer flexibility and customization with varying degrees of performance metrics.





"The throughput of our Widget Pro is quite competitive when compared to open-source alternatives on the market. Here's a detailed comparison:\n\n### Widget Pro\n\n- **Concurrent Connections**: Supports up to 10,000 concurrent connections.\n- **Compression**: Utilizes AcmeZip v3, a proprietary compression algorithm that reduces payload size by 72% compared to gzip (source: [product-spec.pdf]).\n- **API Rate Limits**: Offers different tiers:\n  - Free tier: 100 requests/minute.\n  - Pro tier: 5,000 requests/minute.\n  - Enterprise tier: 50,000 requests/minute (source: [api-docs.md]).\n\n### Open-Source Alternatives\n\nFrom the available resources, open-source widget solutions such as Chatwoot and Tiledesk are popular in handling customer engagement with a flexible and customizable approach (source: [ChatMaxima article](https://chatmaxima.com/blog/15-open-source-free-live-chat-widget-solutions-to-boost-your-customer-engagement-in-2024/)). However, specific throughput metrics such as maximum concurrent connections or API limits are generally not highlighted in open-source product descriptions unless directly benchmarked.\n\nThese alternatives often emphasize customization, control, and integration with AI-driven capabilities but do not always specify throughput in terms comparable with Widget Pro. They might be more suited for organizations looking to tailor solutions to specific needs rather than focusing solely on throughput efficiency.\n\nIn conclusion, Widget Pro appears to offer high throughput suitable for enterprises with robust API support, while open-source options offer flexibility and customization with varying degrees of performance metrics."
清理
完成后，删除 Collections 以释放资源。
milvus.drop_collection(COLLECTION)
结论
在本教程中，我们构建了一个双源 RAG 代理，它结合了用于私人知识检索的 Milvus 和用于公共网络搜索的 Exa。其主要组件包括
Milvus
通过向量相似性搜索存储和检索内部文档，确保专有数据保持私密性和可搜索性。
Exa
提供语义网络搜索，具有类别过滤、内容提取和类似文章发现等功能。
OpenAI 函数调用
使 LLM 能够根据问题的意图将查询自动路由到正确的来源，或同时路由到这两个来源。
这种模式适用于人工智能助手需要访问机密内部文件和实时外部信息的企业用例。