Milvus 混合搜索检索器
混合搜索结合了不同搜索范式的优势，以提高检索的准确性和鲁棒性。它既能利用密集向量搜索和稀疏向量搜索的能力，也能利用多种密集向量搜索策略的组合，确保对各种查询进行全面而精确的检索。
本图展示了最常见的混合搜索方案，即密集+稀疏混合搜索。在这种情况下，使用语义向量相似性和精确关键词匹配两种方法检索候选内容。来自这些方法的结果会被合并、Rerankers 并传递给 LLM 以生成最终答案。这种方法兼顾了精确性和语义理解，对各种查询场景都非常有效。
除了密集+稀疏混合搜索，混合策略还可以结合多个密集向量模型。例如，一种密集向量模型可能专门捕捉语义的细微差别，而另一种则侧重于上下文嵌入或特定领域的表征。通过合并这些模型的结果并重新排序，这种类型的混合搜索可确保检索过程更加细致入微、更能感知上下文。
LangChain Milvus集成提供了实现混合搜索的灵活方式，它支持任意数量的向量场，以及任意自定义的密集或稀疏嵌入模型，这使得LangChain Milvus能够灵活适应各种混合搜索使用场景，同时兼容LangChain的其他功能。
在本教程中，我们将从最常见的密集+稀疏情况开始，然后介绍各种通用的混合搜索使用方法。
MilvusCollectionHybridSearchRetriever
是使用 Milvus 和 LangChain 进行混合搜索的另一种实现，
即将被弃用
。请使用本文档中的方法来实现混合搜索，因为它更灵活，而且与 LangChain 兼容。
前提条件
在运行本笔记本之前，请确保已安装以下依赖项：
$
pip install --upgrade --quiet  langchain langchain-core langchain-community langchain-text-splitters langchain-milvus langchain-openai bs4 pymilvus[model]
#langchain-voyageai
如果您使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
我们将使用 OpenAI 的模型。您应准备好
OpenAI
的环境变量
OPENAI_API_KEY
。
import
os

os.environ[
"OPENAI_API_KEY"
] =
"sk-***********"
指定您的 Milvus 服务器
URI
（可选
TOKEN
）。有关如何安装和启动 Milvus 服务器，请参阅本
指南
。
URI =
"http://localhost:19530"
# TOKEN = ...
准备一些示例文档，即按主题或流派分类的虚构故事摘要。
from
langchain_core.documents
import
Document

docs = [
    Document(
        page_content=
"In 'The Whispering Walls' by Ava Moreno, a young journalist named Sophia uncovers a decades-old conspiracy hidden within the crumbling walls of an ancient mansion, where the whispers of the past threaten to destroy her own sanity."
,
        metadata={
"category"
:
"Mystery"
},
    ),
    Document(
        page_content=
"In 'The Last Refuge' by Ethan Blackwood, a group of survivors must band together to escape a post-apocalyptic wasteland, where the last remnants of humanity cling to life in a desperate bid for survival."
,
        metadata={
"category"
:
"Post-Apocalyptic"
},
    ),
    Document(
        page_content=
"In 'The Memory Thief' by Lila Rose, a charismatic thief with the ability to steal and manipulate memories is hired by a mysterious client to pull off a daring heist, but soon finds themselves trapped in a web of deceit and betrayal."
,
        metadata={
"category"
:
"Heist/Thriller"
},
    ),
    Document(
        page_content=
"In 'The City of Echoes' by Julian Saint Clair, a brilliant detective must navigate a labyrinthine metropolis where time is currency, and the rich can live forever, but at a terrible cost to the poor."
,
        metadata={
"category"
:
"Science Fiction"
},
    ),
    Document(
        page_content=
"In 'The Starlight Serenade' by Ruby Flynn, a shy astronomer discovers a mysterious melody emanating from a distant star, which leads her on a journey to uncover the secrets of the universe and her own heart."
,
        metadata={
"category"
:
"Science Fiction/Romance"
},
    ),
    Document(
        page_content=
"In 'The Shadow Weaver' by Piper Redding, a young orphan discovers she has the ability to weave powerful illusions, but soon finds herself at the center of a deadly game of cat and mouse between rival factions vying for control of the mystical arts."
,
        metadata={
"category"
:
"Fantasy"
},
    ),
    Document(
        page_content=
"In 'The Lost Expedition' by Caspian Grey, a team of explorers ventures into the heart of the Amazon rainforest in search of a lost city, but soon finds themselves hunted by a ruthless treasure hunter and the treacherous jungle itself."
,
        metadata={
"category"
:
"Adventure"
},
    ),
    Document(
        page_content=
"In 'The Clockwork Kingdom' by Augusta Wynter, a brilliant inventor discovers a hidden world of clockwork machines and ancient magic, where a rebellion is brewing against the tyrannical ruler of the land."
,
        metadata={
"category"
:
"Steampunk/Fantasy"
},
    ),
    Document(
        page_content=
"In 'The Phantom Pilgrim' by Rowan Welles, a charismatic smuggler is hired by a mysterious organization to transport a valuable artifact across a war-torn continent, but soon finds themselves pursued by deadly assassins and rival factions."
,
        metadata={
"category"
:
"Adventure/Thriller"
},
    ),
    Document(
        page_content=
"In 'The Dreamwalker's Journey' by Lyra Snow, a young dreamwalker discovers she has the ability to enter people's dreams, but soon finds herself trapped in a surreal world of nightmares and illusions, where the boundaries between reality and fantasy blur."
,
        metadata={
"category"
:
"Fantasy"
},
    ),
]
密集嵌入 + 稀疏嵌入
方案 1（推荐）：密集嵌入 + Milvus BM25 内置功能
使用密集嵌入 + Milvus BM25 内置函数组装混合检索向量存储实例。
from
langchain_milvus
import
Milvus, BM25BuiltInFunction
from
langchain_openai
import
OpenAIEmbeddings


vectorstore = Milvus.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(),
    builtin_function=BM25BuiltInFunction(),
# output_field_names="sparse"),
vector_field=[
"dense"
,
"sparse"
],
    connection_args={
"uri"
: URI,
    },
    consistency_level=
"Bounded"
,
# Supported values are (`"Strong"`, `"Session"`, `"Bounded"`, `"Eventually"`). See https://milvus.io/docs/consistency.md#Consistency-Level for more details.
drop_old=
False
,
)
当您使用
BM25BuiltInFunction
时，请注意全文检索在 Milvus Standalone 和 Milvus Distributed 中可用，但在 Milvus Lite 中不可用，尽管它已在未来加入的路线图上。它也将很快在 Zilliz Cloud（全面管理 Milvus）中提供。更多信息请联系
support@zilliz.com
。
在上面的代码中，我们定义了
BM25BuiltInFunction
的一个实例，并将其传递给
Milvus
对象。
BM25BuiltInFunction
是一个轻量级封装类。
Function
的轻量级封装类。我们可以将它与
OpenAIEmbeddings
一起使用，初始化密集+稀疏混合搜索 Milvus 向量存储实例。
BM25BuiltInFunction
Milvus "不要求客户端传递语料或训练，所有这些都在 Milvus 服务器端自动处理，因此用户无需关心任何词汇和语料。此外，用户还可以定制
分析器
，在 BM25 中实现自定义文本处理。
有关
BM25BuiltInFunction
的更多信息，请参阅《
全文搜索
》（
Full-Text-Search
）和《
使用 LangChain 和 Milvus 进行全文搜索
》（
Using
Full-Text Search
with LangChain and Milvus
）。
方案 2：使用密集和定制的 LangChain 稀疏嵌入
您可以从
langchain_milvus.utils.sparse
继承类
BaseSparseEmbedding
，并实现
embed_query
和
embed_documents
方法来定制稀疏嵌入过程。这样，您就可以自定义任何基于词频统计（如
BM25
）或神经网络（如
SPADE
）的稀疏嵌入方法。
下面是一个例子：
from
typing
import
Dict
,
List
from
langchain_milvus.utils.sparse
import
BaseSparseEmbedding
class
MyCustomEmbedding
(
BaseSparseEmbedding
):
# inherit from BaseSparseEmbedding
def
__init__
(
self, model_path
): ...
# code to init or load model
def
embed_query
(
self, query:
str
) ->
Dict
[
int
,
float
]:
        ...
# code to embed query
return
{
# fake embedding result
1
:
0.1
,
2
:
0.2
,
3
:
0.3
,
# ...
}
def
embed_documents
(
self, texts:
List
[
str
]
) ->
List
[
Dict
[
int
,
float
]]:
        ...
# code to embed documents
return
[
# fake embedding results
{
1
:
0.1
,
2
:
0.2
,
3
:
0.3
,
# ...
}
        ] *
len
(texts)
在
langchain_milvus.utils.sparse
中，我们有一个从
BaseSparseEmbedding
继承而来的演示类
BM25SparseEmbedding
。您可以将其传递到 Milvus 向量存储实例的初始化嵌入列表中，就像传递其他 langchain 密集嵌入类一样。
# BM25SparseEmbedding is inherited from BaseSparseEmbedding
from
langchain_milvus.utils.sparse
import
BM25SparseEmbedding

embedding1 = OpenAIEmbeddings()

corpus = [doc.page_content
for
doc
in
docs]
embedding2 = BM25SparseEmbedding(
    corpus=corpus
)
# pass in corpus to initialize the statistics
vectorstore = Milvus.from_documents(
    documents=docs,
    embedding=[embedding1, embedding2],
    vector_field=[
"dense"
,
"sparse"
],
    connection_args={
"uri"
: URI,
    },
    consistency_level=
"Bounded"
,
# Supported values are (`"Strong"`, `"Session"`, `"Bounded"`, `"Eventually"`). See https://milvus.io/docs/consistency.md#Consistency-Level for more details.
drop_old=
False
,
)
虽然这是使用 BM25 的一种方法，但它要求用户管理语料库以进行词频统计。我们建议改用 BM25 内置函数（选项 1），因为它能在 Milvus 服务器端处理一切事务。这样，用户就无需关心管理语料库或训练词汇的问题。更多信息，请参阅《
使用 LangChain 和 Milvus 进行全文检索
》。
定义多个任意向量场
在初始化 Milvus 向量存储时，你可以传入 Embeddings 列表（将来也会传入内置函数列表）来实现多路检索，然后对这些候选者进行 Rerankers。 下面是一个例子：
# from langchain_voyageai import VoyageAIEmbeddings
embedding1 = OpenAIEmbeddings(model=
"text-embedding-ada-002"
)
embedding2 = OpenAIEmbeddings(model=
"text-embedding-3-large"
)
# embedding3 = VoyageAIEmbeddings(model="voyage-3")  # You can also use embedding from other embedding model providers, e.g VoyageAIEmbeddings
vectorstore = Milvus.from_documents(
    documents=docs,
    embedding=[embedding1, embedding2],
# embedding3],
builtin_function=BM25BuiltInFunction(output_field_names=
"sparse"
),
# `sparse` is the output field name of BM25BuiltInFunction, and `dense1` and `dense2` are the output field names of embedding1 and embedding2
vector_field=[
"dense1"
,
"dense2"
,
"sparse"
],
    connection_args={
"uri"
: URI,
    },
    consistency_level=
"Bounded"
,
# Supported values are (`"Strong"`, `"Session"`, `"Bounded"`, `"Eventually"`). See https://milvus.io/docs/consistency.md#Consistency-Level for more details.
drop_old=
False
,
)

vectorstore.vector_fields
['dense1', 'dense2', 'sparse']
在这个例子中，我们有三个向量场。其中，
sparse
被用作
BM25BuiltInFunction
的输出字段，而其他两个，
dense1
和
dense2
，则被自动分配为两个
OpenAIEmbeddings
模型的输出字段（根据顺序）。
为多向量字段指定索引参数
默认情况下，每个向量场的索引类型将由嵌入类型或内置函数自动决定。不过，您也可以指定每个向量字段的索引类型，以优化搜索性能。
dense_index_param_1 = {
"metric_type"
:
"COSINE"
,
"index_type"
:
"HNSW"
,
}
dense_index_param_2 = {
"metric_type"
:
"IP"
,
"index_type"
:
"HNSW"
,
}
sparse_index_param = {
"metric_type"
:
"BM25"
,
"index_type"
:
"AUTOINDEX"
,
}

vectorstore = Milvus.from_documents(
    documents=docs,
    embedding=[embedding1, embedding2],
    builtin_function=BM25BuiltInFunction(output_field_names=
"sparse"
),
    index_params=[dense_index_param_1, dense_index_param_2, sparse_index_param],
    vector_field=[
"dense1"
,
"dense2"
,
"sparse"
],
    connection_args={
"uri"
: URI,
    },
    consistency_level=
"Bounded"
,
# Supported values are (`"Strong"`, `"Session"`, `"Bounded"`, `"Eventually"`). See https://milvus.io/docs/consistency.md#Consistency-Level for more details.
drop_old=
False
,
)

vectorstore.vector_fields
['dense1', 'dense2', 'sparse']
请将索引参数列表的顺序与
vectorstore.vector_fields
的顺序保持一致，以免混淆。
对候选数据重新排名
第一阶段检索结束后，我们需要对候选数据重新排名，以获得更好的结果。您可以根据自己的要求选择
加权排名器（WeightedRanker
）或
重新
排名
器（RRFRanker）
。您可以参考
Reranking
了解更多信息。
以下是加权重排的示例：
vectorstore = Milvus.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(),
    builtin_function=BM25BuiltInFunction(),
    vector_field=[
"dense"
,
"sparse"
],
    connection_args={
"uri"
: URI,
    },
    consistency_level=
"Bounded"
,
# Supported values are (`"Strong"`, `"Session"`, `"Bounded"`, `"Eventually"`). See https://milvus.io/docs/consistency.md#Consistency-Level for more details.
drop_old=
False
,
)

query =
"What are the novels Lila has written and what are their contents?"
vectorstore.similarity_search(
    query, k=
1
, ranker_type=
"weighted"
, ranker_params={
"weights"
: [
0.6
,
0.4
]}
)
[Document(metadata={'pk': 454646931479252186, 'category': 'Heist/Thriller'}, page_content="In 'The Memory Thief' by Lila Rose, a charismatic thief with the ability to steal and manipulate memories is hired by a mysterious client to pull off a daring heist, but soon finds themselves trapped in a web of deceit and betrayal.")]
下面是 RRFerankers 的示例：
vectorstore.similarity_search(query, k=
1
, ranker_type=
"rrf"
, ranker_params={
"k"
:
100
})
[Document(metadata={'category': 'Heist/Thriller', 'pk': 454646931479252186}, page_content="In 'The Memory Thief' by Lila Rose, a charismatic thief with the ability to steal and manipulate memories is hired by a mysterious client to pull off a daring heist, but soon finds themselves trapped in a web of deceit and betrayal.")]
如果不传递任何有关 Reranker 的参数，则默认使用平均加权 Reranker 策略。
在 RAG 中使用混合搜索和重排
在 RAG 的应用场景中，混合搜索最普遍的方法是密集+稀疏检索，然后是 Rerankers。下面的示例演示了直接的端到端代码。
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
Document(metadata={'source': 'https://lilianweng.github.io/posts/2023-06-23-agent/'}, page_content='Fig. 1. Overview of a LLM-powered autonomous agent system.\nComponent One: Planning#\nA complicated task usually involves many steps. An agent needs to know what they are and plan ahead.\nTask Decomposition#\nChain of thought (CoT; Wei et al. 2022) has become a standard prompting technique for enhancing model performance on complex tasks. The model is instructed to “think step by step” to utilize more test-time computation to decompose hard tasks into smaller and simpler steps. CoT transforms big tasks into multiple manageable tasks and shed lights into an interpretation of the model’s thinking process.\nTree of Thoughts (Yao et al. 2023) extends CoT by exploring multiple reasoning possibilities at each step. It first decomposes the problem into multiple thought steps and generates multiple thoughts per step, creating a tree structure. The search process can be BFS (breadth-first search) or DFS (depth-first search) with each state evaluated by a classifier (via a prompt) or majority vote.\nTask decomposition can be done (1) by LLM with simple prompting like "Steps for XYZ.\\n1.", "What are the subgoals for achieving XYZ?", (2) by using task-specific instructions; e.g. "Write a story outline." for writing a novel, or (3) with human inputs.\nAnother quite distinct approach, LLM+P (Liu et al. 2023), involves relying on an external classical planner to do long-horizon planning. This approach utilizes the Planning Domain Definition Language (PDDL) as an intermediate interface to describe the planning problem. In this process, LLM (1) translates the problem into “Problem PDDL”, then (2) requests a classical planner to generate a PDDL plan based on an existing “Domain PDDL”, and finally (3) translates the PDDL plan back into natural language. Essentially, the planning step is outsourced to an external tool, assuming the availability of domain-specific PDDL and a suitable planner which is common in certain robotic setups but not in many other domains.\nSelf-Reflection#')
将文档加载到 Milvus 向量存储中
如上介绍，我们将准备好的文档初始化并加载到 Milvus 向量存储中，其中包含两个向量字段：
dense
用于 OpenAI 嵌入，
sparse
用于 BM25 函数。
vectorstore = Milvus.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(),
    builtin_function=BM25BuiltInFunction(),
    vector_field=[
"dense"
,
"sparse"
],
    connection_args={
"uri"
: URI,
    },
    consistency_level=
"Bounded"
,
# Supported values are (`"Strong"`, `"Session"`, `"Bounded"`, `"Eventually"`). See https://milvus.io/docs/consistency.md#Consistency-Level for more details.
drop_old=
False
,
)
构建 RAG 链
我们准备好 LLM 实例和提示，然后使用 LangChain 表达式语言将它们结合到 RAG 管道中。
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
"gpt-4o"
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
使用 LCEL（LangChain 表达式语言）构建 RAG 链。
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
使用特定问题调用 RAG 链并获取响应
query =
"What is PAL and PoT?"
res = rag_chain.invoke(query)
res
'PAL (Program-aided Language models) and PoT (Program of Thoughts prompting) are approaches that involve using language models to generate programming language statements to solve natural language reasoning problems. This method offloads the solution step to a runtime, such as a Python interpreter, allowing for complex computation and reasoning to be handled externally. PAL and PoT rely on language models with strong coding skills to effectively perform these tasks.'
恭喜您！您已经构建了由 Milvus 和 LangChain 支持的混合（密集向量 + 稀疏 bm25 函数）搜索 RAG 链。