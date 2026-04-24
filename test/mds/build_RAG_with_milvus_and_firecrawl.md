利用 Milvus 和 Firecrawl 构建 RAG
Firecrawl
使开发人员能够利用从任何网站刮取的干净数据构建人工智能应用程序。Firecrawl 具有先进的刮取、抓取和数据提取功能，可简化将网站内容转换为下游人工智能工作流所需的干净标记符或结构化数据的过程。
在本教程中，我们将向您展示如何使用 Milvus 和 Firecrawl 构建检索-增强生成（RAG）管道。该管道集成了用于网络数据搜刮的 Firecrawl、用于向量存储的 Milvus 和用于生成有洞察力的上下文感知响应的 OpenAI。
准备工作
依赖项和环境
要开始使用，请运行以下命令安装所需的依赖项：
$
pip install firecrawl-py pymilvus milvus-lite openai requests tqdm
如果使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
设置 API 密钥
要使用 Firecrawl 从指定 URL 抓取数据，需要获取
FIRECRAWL_API_KEY
，并将其设置为环境变量。此外，在本例中我们将使用 OpenAI 作为 LLM。您也应将
OPENAI_API_KEY
设置为环境变量。
import
os

os.environ[
"FIRECRAWL_API_KEY"
] =
"fc-***********"
os.environ[
"OPENAI_API_KEY"
] =
"sk-***********"
准备 LLM 和 Embeddings 模型
我们初始化 OpenAI 客户端以准备嵌入模型。
from
openai
import
OpenAI

openai_client = OpenAI()
定义一个使用 OpenAI 客户端生成文本嵌入的函数。我们以
text-embedding-3-small
模型为例。
def
emb_text
(
text
):
return
(
        openai_client.embeddings.create(
input
=text, model=
"text-embedding-3-small"
)
        .data[
0
]
        .embedding
    )
生成测试嵌入并打印其尺寸和前几个元素。
test_embedding = emb_text(
"This is a test"
)
embedding_dim =
len
(test_embedding)
print
(embedding_dim)
print
(test_embedding[:
10
])
1536
[0.009889289736747742, -0.005578675772994757, 0.00683477520942688, -0.03805781528353691, -0.01824733428657055, -0.04121600463986397, -0.007636285852640867, 0.03225184231996536, 0.018949154764413834, 9.352207416668534e-05]
使用 Firecrawl 抓取数据
初始化 Firecrawl 应用程序
我们将使用
firecrawl
库从指定的 URL 以 markdown 格式抓取数据。首先初始化 Firecrawl 应用程序：
from
firecrawl
import
FirecrawlApp

app = FirecrawlApp(api_key=os.environ[
"FIRECRAWL_API_KEY"
])
抓取目标网站
从目标 URL 抓取内容。网站
LLM-powered Autonomous Agents
深入探讨了使用大型语言模型（LLMs）构建的自主代理系统。我们将利用这些内容构建一个 RAG 系统。
# Scrape a website:
scrape_status = app.scrape_url(
"https://lilianweng.github.io/posts/2023-06-23-agent/"
,
    params={
"formats"
: [
"markdown"
]},
)

markdown_content = scrape_status[
"markdown"
]
处理抓取的内容
为了使抓取的内容便于管理，以便插入 Milvus，我们只需使用 "#"来分隔内容，这样就能大致分隔出抓取的标记文件的每个主要部分的内容。
def
split_markdown_content
(
content
):
return
[section.strip()
for
section
in
content.split(
"# "
)
if
section.strip()]
# Process the scraped markdown content
sections = split_markdown_content(markdown_content)
# Print the first few sections to understand the structure
for
i, section
in
enumerate
(sections[:
3
]):
print
(
f"Section
{i+
1
}
:"
)
print
(section[:
300
] +
"..."
)
print
(
"-"
*
50
)
Section 1:
Table of Contents

- [Agent System Overview](#agent-system-overview)
- [Component One: Planning](#component-one-planning)  - [Task Decomposition](#task-decomposition)
  - [Self-Reflection](#self-reflection)
- [Component Two: Memory](#component-two-memory)  - [Types of Memory](#types-of-memory)
  - [...
--------------------------------------------------
Section 2:
Agent System Overview [\#](\#agent-system-overview)

In a LLM-powered autonomous agent system, LLM functions as the agent’s brain, complemented by several key components:

- **Planning**
  - Subgoal and decomposition: The agent breaks down large tasks into smaller, manageable subgoals, enabling effi...
--------------------------------------------------
Section 3:
Component One: Planning [\#](\#component-one-planning)

A complicated task usually involves many steps. An agent needs to know what they are and plan ahead.

#...
--------------------------------------------------
将数据载入 Milvus
创建 Collections
from
pymilvus
import
MilvusClient

milvus_client = MilvusClient(uri=
"./milvus_demo.db"
)
collection_name =
"my_rag_collection"
至于
MilvusClient
的参数：
将
uri
设置为本地文件，如
./milvus.db
，是最方便的方法，因为它会自动利用
Milvus Lite
将所有数据存储在此文件中。
如果数据规模较大，可以在
docker 或 kubernetes
上设置性能更强的 Milvus 服务器。在此设置中，请使用服务器 uri，例如
http://localhost:19530
，作为您的
uri
。
如果你想使用
Zilliz Cloud
（Milvus 的全托管云服务），请调整
uri
和
token
，它们与 Zilliz Cloud 中的
公共端点和 Api 密钥
相对应。
检查 Collections 是否已存在，如果已存在，则删除它。
if
milvus_client.has_collection(collection_name):
    milvus_client.drop_collection(collection_name)
使用指定参数创建新 Collections。
如果我们没有指定任何字段信息，Milvus 会自动创建一个主键的默认
id
字段，以及一个存储向量数据的
vector
字段。保留的 JSON 字段用于存储非 Schema 定义的字段及其值。
milvus_client.create_collection(
    collection_name=collection_name,
    dimension=embedding_dim,
    metric_type=
"IP"
,
# Inner product distance
consistency_level=
"Bounded"
,
# Supported values are (`"Strong"`, `"Session"`, `"Bounded"`, `"Eventually"`). See https://milvus.io/docs/consistency.md#Consistency-Level for more details.
)
插入数据
from
tqdm
import
tqdm

data = []
for
i, section
in
enumerate
(tqdm(sections, desc=
"Processing sections"
)):
    embedding = emb_text(section)
    data.append({
"id"
: i,
"vector"
: embedding,
"text"
: section})
# Insert data into Milvus
milvus_client.insert(collection_name=collection_name, data=data)
Processing sections: 100%|██████████| 17/17 [00:08<00:00,  2.09it/s]





{'insert_count': 17, 'ids': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], 'cost': 0}
构建 RAG
为查询检索数据
让我们指定一个关于我们刚刚抓取的网站的查询问题。
question =
"What are the main components of autonomous agents?"
在 Collections 中搜索该问题并检索语义前 3 个匹配项。
search_res = milvus_client.search(
    collection_name=collection_name,
    data=[emb_text(question)],
    limit=
3
,
    search_params={
"metric_type"
:
"IP"
,
"params"
: {}},
    output_fields=[
"text"
],
)
让我们看看查询的搜索结果
import
json

retrieved_lines_with_distances = [
    (res[
"entity"
][
"text"
], res[
"distance"
])
for
res
in
search_res[
0
]
]
print
(json.dumps(retrieved_lines_with_distances, indent=
4
))
[
    [
        "Agent System Overview [\\#](\\#agent-system-overview)\n\nIn a LLM-powered autonomous agent system, LLM functions as the agent\u2019s brain, complemented by several key components:\n\n- **Planning**\n  - Subgoal and decomposition: The agent breaks down large tasks into smaller, manageable subgoals, enabling efficient handling of complex tasks.\n  - Reflection and refinement: The agent can do self-criticism and self-reflection over past actions, learn from mistakes and refine them for future steps, thereby improving the quality of final results.\n- **Memory**\n  - Short-term memory: I would consider all the in-context learning (See [Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/)) as utilizing short-term memory of the model to learn.\n  - Long-term memory: This provides the agent with the capability to retain and recall (infinite) information over extended periods, often by leveraging an external vector store and fast retrieval.\n- **Tool use**\n  - The agent learns to call external APIs for extra information that is missing from the model weights (often hard to change after pre-training), including current information, code execution capability, access to proprietary information sources and more.\n\n![](agent-overview.png)Fig. 1. Overview of a LLM-powered autonomous agent system.",
        0.6343474388122559
    ],
    [
        "Table of Contents\n\n- [Agent System Overview](#agent-system-overview)\n- [Component One: Planning](#component-one-planning)  - [Task Decomposition](#task-decomposition)\n  - [Self-Reflection](#self-reflection)\n- [Component Two: Memory](#component-two-memory)  - [Types of Memory](#types-of-memory)\n  - [Maximum Inner Product Search (MIPS)](#maximum-inner-product-search-mips)\n- [Component Three: Tool Use](#component-three-tool-use)\n- [Case Studies](#case-studies)  - [Scientific Discovery Agent](#scientific-discovery-agent)\n  - [Generative Agents Simulation](#generative-agents-simulation)\n  - [Proof-of-Concept Examples](#proof-of-concept-examples)\n- [Challenges](#challenges)\n- [Citation](#citation)\n- [References](#references)\n\nBuilding agents with LLM (large language model) as its core controller is a cool concept. Several proof-of-concepts demos, such as [AutoGPT](https://github.com/Significant-Gravitas/Auto-GPT), [GPT-Engineer](https://github.com/AntonOsika/gpt-engineer) and [BabyAGI](https://github.com/yoheinakajima/babyagi), serve as inspiring examples. The potentiality of LLM extends beyond generating well-written copies, stories, essays and programs; it can be framed as a powerful general problem solver.",
        0.5715497732162476
    ],
    [
        "Challenges [\\#](\\#challenges)\n\nAfter going through key ideas and demos of building LLM-centered agents, I start to see a couple common limitations:\n\n- **Finite context length**: The restricted context capacity limits the inclusion of historical information, detailed instructions, API call context, and responses. The design of the system has to work with this limited communication bandwidth, while mechanisms like self-reflection to learn from past mistakes would benefit a lot from long or infinite context windows. Although vector stores and retrieval can provide access to a larger knowledge pool, their representation power is not as powerful as full attention.\n\n- **Challenges in long-term planning and task decomposition**: Planning over a lengthy history and effectively exploring the solution space remain challenging. LLMs struggle to adjust plans when faced with unexpected errors, making them less robust compared to humans who learn from trial and error.\n\n- **Reliability of natural language interface**: Current agent system relies on natural language as an interface between LLMs and external components such as memory and tools. However, the reliability of model outputs is questionable, as LLMs may make formatting errors and occasionally exhibit rebellious behavior (e.g. refuse to follow an instruction). Consequently, much of the agent demo code focuses on parsing model output.",
        0.5009307265281677
    ]
]
使用 LLM 获取 RAG 响应
将检索到的文档转换为字符串格式。
context =
"\n"
.join(
    [line_with_distance[
0
]
for
line_with_distance
in
retrieved_lines_with_distances]
)
为 Lanage 模型定义系统和用户提示。该提示与从 Milvus 检索到的文档组装在一起。
SYSTEM_PROMPT =
"""
Human: You are an AI assistant. You are able to find answers to the questions from the contextual passage snippets provided.
"""
USER_PROMPT =
f"""
Use the following pieces of information enclosed in <context> tags to provide an answer to the question enclosed in <question> tags.
<context>
{context}
</context>
<question>
{question}
</question>
"""
使用 OpenAI ChatGPT 根据提示生成响应。
response = openai_client.chat.completions.create(
    model=
"gpt-4o"
,
    messages=[
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
: USER_PROMPT},
    ],
)
print
(response.choices[
0
].message.content)
The main components of a LLM-powered autonomous agent system are the Planning, Memory, and Tool use. 

1. Planning: The agent breaks down large tasks into smaller, manageable subgoals, and can self-reflect and learn from past mistakes, refining its actions for future steps.

2. Memory: This includes short-term memory, which the model uses for in-context learning, and long-term memory, which allows the agent to retain and recall information over extended periods. 

3. Tool use: This component allows the agent to call external APIs for additional information that is not available in the model weights, like current information, code execution capacity, and access to proprietary information sources.