使用 Milvus 和 LangChain 的检索增强生成（RAG）
本指南演示了如何使用 LangChain 和 Milvus 构建检索-增强生成（RAG）系统。
RAG 系统结合了检索系统和生成模型，可根据给定提示生成新文本。该系统首先使用 Milvus 从语料库中检索相关文档，然后使用生成模型根据检索到的文档生成新文本。
LangChain
是一个开发由大型语言模型（LLMs）驱动的应用程序的框架。
Milvus
是世界上最先进的开源向量数据库，用于支持嵌入式相似性搜索和人工智能应用。
前提条件
在运行本笔记本之前，请确保您已安装以下依赖项：
pip install --upgrade --quiet  langchain langchain-core langchain-community langchain-text-splitters langchain-milvus milvus-lite langchain-openai bs4
如果使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
我们将使用 OpenAI 的模型。您应将
api key
OPENAI_API_KEY
作为环境变量。
import
os

os.environ[
"OPENAI_API_KEY"
] =
"sk-***********"
准备数据
我们使用 Langchain WebBaseLoader 从网络源加载文档，并使用 RecursiveCharacterTextSplitter 将文档分割成块。
import
bs4
from
langchain_community.document_loaders
import
WebBaseLoader
from
langchain_text_splitters
import
RecursiveCharacterTextSplitter
# Create a WebBaseLoader instance to load documents from web sources
loader = WebBaseLoader(
    web_paths=(
"https://lilianweng.github.io/posts/2023-06-23-agent/"
,
"https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/"
,
    ),
    bs_kwargs=
dict
(
        parse_only=bs4.SoupStrainer(
            class_=(
"post-content"
,
"post-title"
,
"post-header"
)
        )
    ),
)
# Load documents from web sources using the loader
documents = loader.load()
# Initialize a RecursiveCharacterTextSplitter for splitting text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=
2000
, chunk_overlap=
200
)
# Split the documents into chunks using the text_splitter
docs = text_splitter.split_documents(documents)
# Let's take a look at the first document
docs[
1
]
Document(page_content='Fig. 1. Overview of a LLM-powered autonomous agent system.\nComponent One: Planning#\nA complicated task usually involves many steps. An agent needs to know what they are and plan ahead.\nTask Decomposition#\nChain of thought (CoT; Wei et al. 2022) has become a standard prompting technique for enhancing model performance on complex tasks. The model is instructed to “think step by step” to utilize more test-time computation to decompose hard tasks into smaller and simpler steps. CoT transforms big tasks into multiple manageable tasks and shed lights into an interpretation of the model’s thinking process.\nTree of Thoughts (Yao et al. 2023) extends CoT by exploring multiple reasoning possibilities at each step. It first decomposes the problem into multiple thought steps and generates multiple thoughts per step, creating a tree structure. The search process can be BFS (breadth-first search) or DFS (depth-first search) with each state evaluated by a classifier (via a prompt) or majority vote.\nTask decomposition can be done (1) by LLM with simple prompting like "Steps for XYZ.\\n1.", "What are the subgoals for achieving XYZ?", (2) by using task-specific instructions; e.g. "Write a story outline." for writing a novel, or (3) with human inputs.\nAnother quite distinct approach, LLM+P (Liu et al. 2023), involves relying on an external classical planner to do long-horizon planning. This approach utilizes the Planning Domain Definition Language (PDDL) as an intermediate interface to describe the planning problem. In this process, LLM (1) translates the problem into “Problem PDDL”, then (2) requests a classical planner to generate a PDDL plan based on an existing “Domain PDDL”, and finally (3) translates the PDDL plan back into natural language. Essentially, the planning step is outsourced to an external tool, assuming the availability of domain-specific PDDL and a suitable planner which is common in certain robotic setups but not in many other domains.\nSelf-Reflection#', metadata={'source': 'https://lilianweng.github.io/posts/2023-06-23-agent/'})
正如我们所看到的，文档已经分割成块。而数据内容是关于人工智能 Agents 的。
使用 Milvus 向量存储构建 RAG 链
我们将用文档初始化一个 Milvus 向量存储，将文档加载到 Milvus 向量存储中，并在引擎盖下建立索引。
from
langchain_milvus
import
Milvus
from
langchain_openai
import
OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

vectorstore = Milvus.from_documents(
    documents=docs,
    embedding=embeddings,
    connection_args={
"uri"
:
"./milvus_demo.db"
,
    },
    drop_old=
False
,
# Drop the old Milvus collection if it exists
)
对于
connection_args
：
将
uri
设置为本地文件，如
./milvus.db
，是最方便的方法，因为它会自动利用
Milvus Lite
将所有数据存储到这个文件中。
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
，它们对应于 Zilliz Cloud 中的
公共端点和 Api 密钥
。
使用测试查询问题搜索 Milvus 向量存储中的文档。让我们看看排名前 1 的文档。
query =
"What is self-reflection of an AI Agent?"
vectorstore.similarity_search(query, k=
1
)
[Document(page_content='Self-Reflection#\nSelf-reflection is a vital aspect that allows autonomous agents to improve iteratively by refining past action decisions and correcting previous mistakes. It plays a crucial role in real-world tasks where trial and error are inevitable.\nReAct (Yao et al. 2023) integrates reasoning and acting within LLM by extending the action space to be a combination of task-specific discrete actions and the language space. The former enables LLM to interact with the environment (e.g. use Wikipedia search API), while the latter prompting LLM to generate reasoning traces in natural language.\nThe ReAct prompt template incorporates explicit steps for LLM to think, roughly formatted as:\nThought: ...\nAction: ...\nObservation: ...\n... (Repeated many times)', metadata={'source': 'https://lilianweng.github.io/posts/2023-06-23-agent/', 'pk': 449281835035555859})]
from
langchain_core.runnables
import
RunnablePassthrough
from
langchain_core.prompts
import
PromptTemplate
from
langchain_core.output_parsers
import
StrOutputParser
from
langchain_openai
import
ChatOpenAI
# Initialize the OpenAI language model for response generation
llm = ChatOpenAI(model_name=
"gpt-3.5-turbo"
, temperature=
0
)
# Define the prompt template for generating AI responses
PROMPT_TEMPLATE =
"""
Human: You are an AI assistant, and provides answers to questions by using fact based and statistical information when possible.
Use the following pieces of information to provide a concise answer to the question enclosed in <question> tags.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
<context>
{context}
</context>

<question>
{question}
</question>

The response should be specific and use statistics or numbers when possible.

Assistant:"""
# Create a PromptTemplate instance with the defined template and input variables
prompt = PromptTemplate(
    template=PROMPT_TEMPLATE, input_variables=[
"context"
,
"question"
]
)
# Convert the vector store to a retriever
retriever = vectorstore.as_retriever()
# Define a function to format the retrieved documents
def
format_docs
(
docs
):
return
"\n\n"
.join(doc.page_content
for
doc
in
docs)
使用 LCEL（LangChain Expression Language）构建 RAG 链。
# Define the RAG (Retrieval-Augmented Generation) chain for AI response generation
rag_chain = (
    {
"context"
: retriever | format_docs,
"question"
: RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
# rag_chain.get_graph().print_ascii()
# Invoke the RAG chain with a specific question and retrieve the response
res = rag_chain.invoke(query)
res
"Self-reflection of an AI agent involves the process of synthesizing memories into higher-level inferences over time to guide the agent's future behavior. It serves as a mechanism to create higher-level summaries of past events. One approach to self-reflection involves prompting the language model with the 100 most recent observations and asking it to generate the 3 most salient high-level questions based on those observations. This process helps the AI agent optimize believability in the current moment and over time."
恭喜您！您已经构建了由 Milvus 和 LangChain 支持的基本 RAG 链。
元数据过滤
我们可以使用
Milvus 标量过滤规则
来根据元数据过滤文档。我们从两个不同的来源加载了文档，可以通过元数据过滤文档
source
。
vectorstore.similarity_search(
"What is CoT?"
,
    k=
1
,
    expr=
"source == 'https://lilianweng.github.io/posts/2023-06-23-agent/'"
,
)
# The same as:
# vectorstore.as_retriever(search_kwargs=dict(
#     k=1,
#     expr="source == 'https://lilianweng.github.io/posts/2023-06-23-agent/'",
# )).invoke("What is CoT?")
[Document(page_content='Fig. 1. Overview of a LLM-powered autonomous agent system.\nComponent One: Planning#\nA complicated task usually involves many steps. An agent needs to know what they are and plan ahead.\nTask Decomposition#\nChain of thought (CoT; Wei et al. 2022) has become a standard prompting technique for enhancing model performance on complex tasks. The model is instructed to “think step by step” to utilize more test-time computation to decompose hard tasks into smaller and simpler steps. CoT transforms big tasks into multiple manageable tasks and shed lights into an interpretation of the model’s thinking process.\nTree of Thoughts (Yao et al. 2023) extends CoT by exploring multiple reasoning possibilities at each step. It first decomposes the problem into multiple thought steps and generates multiple thoughts per step, creating a tree structure. The search process can be BFS (breadth-first search) or DFS (depth-first search) with each state evaluated by a classifier (via a prompt) or majority vote.\nTask decomposition can be done (1) by LLM with simple prompting like "Steps for XYZ.\\n1.", "What are the subgoals for achieving XYZ?", (2) by using task-specific instructions; e.g. "Write a story outline." for writing a novel, or (3) with human inputs.\nAnother quite distinct approach, LLM+P (Liu et al. 2023), involves relying on an external classical planner to do long-horizon planning. This approach utilizes the Planning Domain Definition Language (PDDL) as an intermediate interface to describe the planning problem. In this process, LLM (1) translates the problem into “Problem PDDL”, then (2) requests a classical planner to generate a PDDL plan based on an existing “Domain PDDL”, and finally (3) translates the PDDL plan back into natural language. Essentially, the planning step is outsourced to an external tool, assuming the availability of domain-specific PDDL and a suitable planner which is common in certain robotic setups but not in many other domains.\nSelf-Reflection#', metadata={'source': 'https://lilianweng.github.io/posts/2023-06-23-agent/', 'pk': 449281835035555858})]
如果我们想在不重建链的情况下动态更改搜索参数，可以
配置运行时链内部结构
。让我们用动态配置定义一个新的检索器，并用它来构建一个新的 RAG 链。
from
langchain_core.runnables
import
ConfigurableField
# Define a new retriever with a configurable field for search_kwargs
retriever2 = vectorstore.as_retriever().configurable_fields(
    search_kwargs=ConfigurableField(
id
=
"retriever_search_kwargs"
,
    )
)
# Invoke the retriever with a specific search_kwargs which filter the documents by source
retriever2.with_config(
    configurable={
"retriever_search_kwargs"
:
dict
(
            expr=
"source == 'https://lilianweng.github.io/posts/2023-06-23-agent/'"
,
            k=
1
,
        )
    }
).invoke(query)
[Document(page_content='Self-Reflection#\nSelf-reflection is a vital aspect that allows autonomous agents to improve iteratively by refining past action decisions and correcting previous mistakes. It plays a crucial role in real-world tasks where trial and error are inevitable.\nReAct (Yao et al. 2023) integrates reasoning and acting within LLM by extending the action space to be a combination of task-specific discrete actions and the language space. The former enables LLM to interact with the environment (e.g. use Wikipedia search API), while the latter prompting LLM to generate reasoning traces in natural language.\nThe ReAct prompt template incorporates explicit steps for LLM to think, roughly formatted as:\nThought: ...\nAction: ...\nObservation: ...\n... (Repeated many times)', metadata={'source': 'https://lilianweng.github.io/posts/2023-06-23-agent/', 'pk': 449281835035555859})]
# Define a new RAG chain with this dynamically configurable retriever
rag_chain2 = (
    {
"context"
: retriever2 | format_docs,
"question"
: RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
让我们用不同的过滤条件试试这个可动态配置的 RAG 链。
# Invoke this RAG chain with a specific question and config
rag_chain2.with_config(
    configurable={
"retriever_search_kwargs"
:
dict
(
            expr=
"source == 'https://lilianweng.github.io/posts/2023-06-23-agent/'"
,
        )
    }
).invoke(query)
"Self-reflection of an AI agent involves the process of synthesizing memories into higher-level inferences over time to guide the agent's future behavior. It serves as a mechanism to create higher-level summaries of past events. One approach to self-reflection involves prompting the language model with the 100 most recent observations and asking it to generate the 3 most salient high-level questions based on those observations. This process helps the AI agent optimize believability in the current moment and over time."
当我们改变搜索条件，用第二个来源过滤文档时，由于这个博客来源的内容与查询问题无关，我们得到的答案没有相关信息。
rag_chain2.with_config(
    configurable={
"retriever_search_kwargs"
:
dict
(
            expr=
"source == 'https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/'"
,
        )
    }
).invoke(query)
"I'm sorry, but based on the provided context, there is no specific information or statistical data available regarding the self-reflection of an AI agent."
本教程重点介绍 Milvus LangChain 集成的基本用法和简单的 RAG 方法。有关更高级的 RAG 技术，请参阅
高级 RAG Bootcamp
。