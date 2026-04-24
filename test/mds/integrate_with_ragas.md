使用 Ragas 进行评估
本指南演示了如何使用 Ragas 评估基于
Milvus
的检索增强生成（RAG）管道。
RAG 系统结合了检索系统和生成模型，可根据给定提示生成新文本。该系统首先使用 Milvus 从语料库中检索相关文档，然后使用生成模型根据检索到的文档生成新文本。
Ragas
是一个帮助您评估 RAG 管道的框架。现有的工具和框架可以帮助您构建这些管道，但评估和量化管道性能可能很难。这就是 Ragas（RAG 评估）的用武之地。
前提条件
在运行本笔记本之前，请确保您已安装以下依赖项：
$
pip install --upgrade pymilvus milvus-lite openai requests tqdm pandas ragas
如果您使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
在本例中，我们将使用 OpenAI 作为 LLM。您应将
api key
OPENAI_API_KEY
作为环境变量。
import
os

os.environ[
"OPENAI_API_KEY"
] =
"sk-***********"
定义 RAG 管道
我们将定义使用 Milvus 作为向量存储、OpenAI 作为 LLM 的 RAG 类。该类包含
load
方法（将文本数据加载到 Milvus）、
retrieve
方法（检索与给定问题最相似的文本数据）和
answer
方法（使用检索到的知识回答给定问题）。
from
typing
import
List
from
tqdm
import
tqdm
from
openai
import
OpenAI
from
pymilvus
import
MilvusClient
class
RAG
:
"""
    RAG (Retrieval-Augmented Generation) class built upon OpenAI and Milvus.
    """
def
__init__
(
self, openai_client: OpenAI, milvus_client: MilvusClient
):
self
._prepare_openai(openai_client)
self
._prepare_milvus(milvus_client)
def
_emb_text
(
self, text:
str
) ->
List
[
float
]:
return
(
self
.openai_client.embeddings.create(
input
=text, model=
self
.embedding_model)
            .data[
0
]
            .embedding
        )
def
_prepare_openai
(
self,
        openai_client: OpenAI,
        embedding_model:
str
=
"text-embedding-3-small"
,
        llm_model:
str
=
"gpt-3.5-turbo"
,
):
self
.openai_client = openai_client
self
.embedding_model = embedding_model
self
.llm_model = llm_model
self
.SYSTEM_PROMPT =
"""
Human: You are an AI assistant. You are able to find answers to the questions from the contextual passage snippets provided.
"""
self
.USER_PROMPT =
"""
Use the following pieces of information enclosed in <context> tags to provide an answer to the question enclosed in <question> tags.
<context>
{context}
</context>
<question>
{question}
</question>
"""
def
_prepare_milvus
(
self, milvus_client: MilvusClient, collection_name:
str
=
"rag_collection"
):
self
.milvus_client = milvus_client
self
.collection_name = collection_name
if
self
.milvus_client.has_collection(
self
.collection_name):
self
.milvus_client.drop_collection(
self
.collection_name)
        embedding_dim =
len
(
self
._emb_text(
"foo"
))
self
.milvus_client.create_collection(
            collection_name=
self
.collection_name,
            dimension=embedding_dim,
            metric_type=
"IP"
,
# Inner product distance
consistency_level=
"Bounded"
,
# Strong consistency level
)
def
load
(
self, texts:
List
[
str
]
):
"""
        Load the text data into Milvus.
        """
data = []
for
i, line
in
enumerate
(tqdm(texts, desc=
"Creating embeddings"
)):
            data.append({
"id"
: i,
"vector"
:
self
._emb_text(line),
"text"
: line})
self
.milvus_client.insert(collection_name=
self
.collection_name, data=data)
def
retrieve
(
self, question:
str
, top_k:
int
=
3
) ->
List
[
str
]:
"""
        Retrieve the most similar text data to the given question.
        """
search_res =
self
.milvus_client.search(
            collection_name=
self
.collection_name,
            data=[
self
._emb_text(question)],
            limit=top_k,
            search_params={
"metric_type"
:
"IP"
,
"params"
: {}},
# Inner product distance
output_fields=[
"text"
],
# Return the text field
)
        retrieved_texts = [res[
"entity"
][
"text"
]
for
res
in
search_res[
0
]]
return
retrieved_texts[:top_k]
def
answer
(
self,
        question:
str
,
        retrieval_top_k:
int
=
3
,
        return_retrieved_text:
bool
=
False
,
):
"""
        Answer the given question with the retrieved knowledge.
        """
retrieved_texts =
self
.retrieve(question, top_k=retrieval_top_k)
        user_prompt =
self
.USER_PROMPT.
format
(
            context=
"\n"
.join(retrieved_texts), question=question
        )
        response =
self
.openai_client.chat.completions.create(
            model=
self
.llm_model,
            messages=[
                {
"role"
:
"system"
,
"content"
:
self
.SYSTEM_PROMPT},
                {
"role"
:
"user"
,
"content"
: user_prompt},
            ],
        )
if
not
return_retrieved_text:
return
response.choices[
0
].message.content
else
:
return
response.choices[
0
].message.content, retrieved_texts
让我们用 OpenAI 和 Milvus 客户端初始化 RAG 类。
openai_client = OpenAI()
milvus_client = MilvusClient(uri=
"./milvus_demo.db"
)

my_rag = RAG(openai_client=openai_client, milvus_client=milvus_client)
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
（Milvus 的完全托管云服务），请调整
uri
和
token
，它们与 Zilliz Cloud 中的
公共端点和 Api 密钥
相对应。
运行 RAG 管道并获取结果
我们使用
Milvus 开发指南
作为 RAG 中的私有知识，它是简单 RAG 管道的良好数据源。
下载并将其加载到 RAG 管道中。
import
os
import
urllib.request

url =
"https://raw.githubusercontent.com/milvus-io/milvus/master/DEVELOPMENT.md"
file_path =
"./Milvus_DEVELOPMENT.md"
if
not
os.path.exists(file_path):
    urllib.request.urlretrieve(url, file_path)
with
open
(file_path,
"r"
)
as
file:
    file_text = file.read()
# We simply use "# " to separate the content in the file, which can roughly separate the content of each main part of the markdown file.
text_lines = file_text.split(
"# "
)
my_rag.load(text_lines)
# Load the text data into RAG pipeline
Creating embeddings: 100%|██████████| 27/27 [00:20<00:00,  1.34it/s]
让我们定义一个关于开发指南文档内容的查询问题。然后使用
answer
方法获取答案和检索到的上下文文本。
question =
"what is the hardware requirements specification if I want to build Milvus and run from source code?"
my_rag.answer(question, return_retrieved_text=
True
)
('The hardware requirements specification for building Milvus and running it from source code is as follows:\n\n- 8GB of RAM\n- 50GB of free disk space',
 ['Hardware Requirements\n\nThe following specification (either physical or virtual machine resources) is recommended for Milvus to build and run from source code.\n\n```yaml\n- 8GB of RAM\n- 50GB of free disk space\n```\n\n##',
  'Building Milvus on a local OS/shell environment\n\nThe details below outline the hardware and software requirements for building on Linux and MacOS.\n\n##',
  "Software Requirements\n\nAll Linux distributions are available for Milvus development. However a majority of our contributor worked with Ubuntu or CentOS systems, with a small portion of Mac (both x86_64 and Apple Silicon) contributors. If you would like Milvus to build and run on other distributions, you are more than welcome to file an issue and contribute!\n\nHere's a list of verified OS types where Milvus can successfully build and run:\n\n- Debian/Ubuntu\n- Amazon Linux\n- MacOS (x86_64)\n- MacOS (Apple Silicon)\n\n##"])
现在，让我们准备一些问题及其相应的地面实况答案。我们从 RAG 管道中获取答案和上下文。
from
ragas
import
EvaluationDataset
from
datasets
import
Dataset
import
pandas
as
pd

user_input_list = [
"what is the hardware requirements specification if I want to build Milvus and run from source code?"
,
"What is the programming language used to write Knowhere?"
,
"What should be ensured before running code coverage?"
,
]
reference_list = [
"If you want to build Milvus and run from source code, the recommended hardware requirements specification is:\n\n- 8GB of RAM\n- 50GB of free disk space."
,
"The programming language used to write Knowhere is C++."
,
"Before running code coverage, you should make sure that your code changes are covered by unit tests."
,
]
retrieved_contexts_list = []
response_list = []
for
user_input
in
tqdm(user_input_list, desc=
"Answering questions"
):
    response, retrieved_context = my_rag.answer(user_input, return_retrieved_text=
True
)
    retrieved_contexts_list.append(retrieved_context)
    response_list.append(response)

df = pd.DataFrame(
    {
"user_input"
: user_input_list,
"retrieved_contexts"
: retrieved_contexts_list,
"response"
: response_list,
"reference"
: reference_list,
    }
)
rag_results = EvaluationDataset.from_pandas(df)
df
Answering questions: 100%|██████████| 3/3 [00:04<00:00,  1.37s/it]
.dataframe tbody tr th:only-of-type { vertical-align: middle; }<pre><code translate="no">.dataframe tbody tr th {
    vertical-align: top;
}

.dataframe thead th {
    text-align: right;
}
</code></pre>
用户输入
检索到的上下文
响应
参考
0
硬件要求是什么？
[硬件要求（Hardware Requirements/n...
硬件要求规范（...
如果您想构建Milvus并从源代码运行...
1
用什么编程语言来编写Milvus...
[CMake & Conan\n\nMilvus 的算法库...
编写 Knowherus 的编程语言是什么？
用来编写知乎的编程语言...
2
运行代码覆盖前应确保什么？
[代码覆盖（Code coverage）：在提交您的pull...
在运行代码覆盖之前，应该确保...
运行代码覆盖之前，应确保 ...
使用 Ragas 进行评估
我们使用 Ragas 来评估 RAG 管道结果的性能。
Ragas 提供了一套易于使用的度量指标。我们将
Answer relevancy
、
Faithfulness
、
Context recall
和
Context precision
作为评估 RAG 管道的指标。有关指标的更多信息，请参阅
Ragas 指标
。
from
ragas
import
evaluate
from
ragas.metrics
import
AnswerRelevancy, Faithfulness, ContextRecall, ContextPrecision
from
ragas.llms
import
LangchainLLMWrapper
from
langchain_openai
import
ChatOpenAI

llm = ChatOpenAI(model=
"gpt-4o-mini"
)
evaluator_llm = LangchainLLMWrapper(llm)

results = evaluate(
    dataset=rag_results,
    metrics=[
        AnswerRelevancy(llm=evaluator_llm),
        Faithfulness(llm=evaluator_llm),
        ContextRecall(llm=evaluator_llm),
        ContextPrecision(llm=evaluator_llm),
    ],
)
results
Evaluating: 100%|██████████| 12/12 [00:10<00:00,  1.11it/s]





{'answer_relevancy': 0.9894, 'faithfulness': 1.0000, 'context_recall': 1.0000, 'context_precision': 1.0000}