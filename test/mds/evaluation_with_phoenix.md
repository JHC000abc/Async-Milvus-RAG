使用 Arize Pheonix 进行评估
本指南演示了如何使用
Arize Pheonix
评估基于
Milvus
的检索增强生成（RAG）管道。
RAG 系统将检索系统与生成模型相结合，根据给定提示生成新文本。该系统首先使用 Milvus 从语料库中检索相关文档，然后使用生成模型根据检索到的文档生成新文本。
Arize Pheonix 是一个帮助您评估 RAG 管道的框架。现有的工具和框架可以帮助您构建这些管道，但评估和量化管道性能可能很难。这就是 Arize Pheonix 的用武之地。
前提条件
在运行本笔记本之前，请确保已安装以下依赖项：
$ pip install --upgrade pymilvus milvus-lite openai requests tqdm pandas
"arize-phoenix>=4.29.0"
nest_asyncio
如果使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
在本例中，我们将使用 OpenAI 作为 LLM。您应将
api key
OPENAI_API_KEY
作为环境变量。
import
os
# os.environ["OPENAI_API_KEY"] = "sk-*****************"
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
    RAG(Retrieval-Augmented Generation) class built upon OpenAI and Milvus.
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
"gpt-4o-mini"
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
"demo"
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
            consistency_level=
"Bounded"
,
# Supported values are (`"Strong"`, `"Session"`, `"Bounded"`, `"Eventually"`). See https://milvus.io/docs/consistency.md#Consistency-Level for more details.
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
# inner product distance
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
urllib.request
import
os

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

text_lines = file_text.split(
"# "
)
my_rag.load(text_lines)
Creating embeddings: 100%|██████████| 47/47 [00:12<00:00,  3.84it/s]
让我们定义一个关于开发指南文档内容的查询问题。然后使用
answer
方法获取答案和检索到的上下文文本。
question =
"what is the hardware requirements specification if I want to build Milvus and run from source code?"
my_rag.answer(question, return_retrieved_text=
True
)
('The hardware requirements specification to build and run Milvus from source code are:\n\n- 8GB of RAM\n- 50GB of free disk space',
 ['Hardware Requirements\n\nThe following specification (either physical or virtual machine resources) is recommended for Milvus to build and run from source code.\n\n```\n- 8GB of RAM\n- 50GB of free disk space\n```\n\n##',
  'Building Milvus on a local OS/shell environment\n\nThe details below outline the hardware and software requirements for building on Linux and MacOS.\n\n##',
  "Software Requirements\n\nAll Linux distributions are available for Milvus development. However a majority of our contributor worked with Ubuntu or CentOS systems, with a small portion of Mac (both x86_64 and Apple Silicon) contributors. If you would like Milvus to build and run on other distributions, you are more than welcome to file an issue and contribute!\n\nHere's a list of verified OS types where Milvus can successfully build and run:\n\n- Debian/Ubuntu\n- Amazon Linux\n- MacOS (x86_64)\n- MacOS (Apple Silicon)\n\n##"])
现在，让我们准备一些问题及其相应的地面实况答案。我们从 RAG 管道中获取答案和上下文。
from
datasets
import
Dataset
import
pandas
as
pd

question_list = [
"what is the hardware requirements specification if I want to build Milvus and run from source code?"
,
"What is the programming language used to write Knowhere?"
,
"What should be ensured before running code coverage?"
,
]
ground_truth_list = [
"If you want to build Milvus and run from source code, the recommended hardware requirements specification is:\n\n- 8GB of RAM\n- 50GB of free disk space."
,
"The programming language used to write Knowhere is C++."
,
"Before running code coverage, you should make sure that your code changes are covered by unit tests."
,
]
contexts_list = []
answer_list = []
for
question
in
tqdm(question_list, desc=
"Answering questions"
):
    answer, contexts = my_rag.answer(question, return_retrieved_text=
True
)
    contexts_list.append(contexts)
    answer_list.append(answer)

df = pd.DataFrame(
    {
"question"
: question_list,
"contexts"
: contexts_list,
"answer"
: answer_list,
"ground_truth"
: ground_truth_list,
    }
)
rag_results = Dataset.from_pandas(df)
df
/Users/eureka/miniconda3/envs/zilliz/lib/python3.9/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html
  from .autonotebook import tqdm as notebook_tqdm
Answering questions: 100%|██████████| 3/3 [00:03<00:00,  1.04s/it]
.dataframe tbody tr th:only-of-type { vertical-align: middle; }<pre><code translate="no">.dataframe tbody tr th {
    vertical-align: top;
}

.dataframe thead th {
    text-align: right;
}
</code></pre>
问题
上下文
答案
地面真相
0
硬件要求是什么？
[硬件要求（Hardware Requirements/n）：以下是硬件要求规格。
构建Milvus的硬件要求规范...
如果您想构建 Milvus 并从源代码中运行...
1
用什么编程语言来编写Milvus...
[CMake & Conan\n\nMilvus 的算法库...
编写 Knowherus 的编程语言是什么？
用来编写知乎的编程语言...
2
运行代码覆盖前应确保什么？
[代码覆盖（Code coverage）：在提交您的pull...
在运行代码覆盖之前，应该确保...
在运行代码覆盖之前，应该确保 ...
使用 Arize Phoenix 进行评估
我们使用 Arize Phoenix 来评估我们的检索增强生成（RAG）管道，重点关注两个关键指标：
幻觉评估
：确定内容是事实还是幻觉（没有上下文依据的信息），确保数据完整性。
幻觉解释
：解释回复是否符合事实的原因。
QA 评估
：评估输入查询的模型答案的准确性。
QA 解释
：详细说明答案正确或不正确的原因。
Phoenix 跟踪概述
Phoenix 为 LLM 应用程序提供
与 OTEL 兼容的跟踪
功能，并与
Langchain
、
LlamaIndex
等框架以及
OpenAI
和
Mistral
等 SDK 集成。跟踪功能可捕获整个请求流，深入了解以下内容：
应用程序延迟
：识别并优化缓慢的 LLM 调用和组件性能。
令牌使用情况
：分解令牌消耗，优化成本。
运行时异常
：捕捉速率限制等关键问题。
检索文档
分析文档检索、得分和顺序。
利用 Phoenix 的跟踪功能，您可以
识别瓶颈
、
优化资源
，并
确保
各种框架和语言的
系统可靠性
。
import
phoenix
as
px
from
phoenix.trace.openai
import
OpenAIInstrumentor
# To view traces in Phoenix, you will first have to start a Phoenix server. You can do this by running the following:
session = px.launch_app()
# Initialize OpenAI auto-instrumentation
OpenAIInstrumentor().instrument()
🌍 To view the Phoenix app in your browser, visit http://localhost:6006/
📖 For more information on how to use Phoenix, check out https://docs.arize.com/phoenix
文本
import
nest_asyncio
from
phoenix.evals
import
HallucinationEvaluator, OpenAIModel, QAEvaluator, run_evals

nest_asyncio.apply()
# This is needed for concurrency in notebook environments
# Set your OpenAI API key
eval_model = OpenAIModel(model=
"gpt-4o"
)
# Define your evaluators
hallucination_evaluator = HallucinationEvaluator(eval_model)
qa_evaluator = QAEvaluator(eval_model)
# We have to make some minor changes to our dataframe to use the column names expected by our evaluators
# for `hallucination_evaluator` the input df needs to have columns 'output', 'input', 'context'
# for `qa_evaluator` the input df needs to have columns 'output', 'input', 'reference'
df[
"context"
] = df[
"contexts"
]
df[
"reference"
] = df[
"contexts"
]
df.rename(columns={
"question"
:
"input"
,
"answer"
:
"output"
}, inplace=
True
)
assert
all
(
    column
in
df.columns
for
column
in
[
"output"
,
"input"
,
"context"
,
"reference"
]
)
# Run the evaluators, each evaluator will return a dataframe with evaluation results
# We upload the evaluation results to Phoenix in the next step
hallucination_eval_df, qa_eval_df = run_evals(
    dataframe=df,
    evaluators=[hallucination_evaluator, qa_evaluator],
    provide_explanation=
True
,
)
run_evals |██████████| 6/6 (100.0%) | ⏳ 00:03<00:00 |  1.64it/s
results_df = df.copy()
results_df[
"hallucination_eval"
] = hallucination_eval_df[
"label"
]
results_df[
"hallucination_explanation"
] = hallucination_eval_df[
"explanation"
]
results_df[
"qa_eval"
] = qa_eval_df[
"label"
]
results_df[
"qa_explanation"
] = qa_eval_df[
"explanation"
]
results_df.head()
.dataframe tbody tr th:only-of-type { vertical-align: middle; }<pre><code translate="no">.dataframe tbody tr th {
    vertical-align: top;
}

.dataframe thead th {
    text-align: right;
}
</code></pre>
输入
上下文
输出
地面实况
上下文
参考
幻觉评估
幻觉解释
qa_eval
qa_explanation
0
硬件要求是什么？
[硬件要求（Hardware Requirements/n...
构建Milvus的硬件要求规范...
如果您想从源代码中构建并运行Milvus...
[硬件要求（Hardware Requirements）：以下是对硬件要求的具体说明。
[硬件要求（Hardware Requirements）：以下是对硬件要求的具体说明...
事实
要确定答案是事实还是幻...
正确
要确定答案是否正确，我们需要...
1
用什么编程语言编写...
[CMake & Conan\n\nThe algorithm library of Mil...
编写知乎的编程语言是什么？
用来编写知乎的编程语言是什么？
[CMake & Conan\n\nThe algorithm library of Mil...
[CMake & Conan\nThe algorithm library of Mil...
事实
确定答案是事实性的还是含糊...
正确
要确定答案是否正确，我们需要...
2
运行代码覆盖前应确保什么？
[代码覆盖（Code coverage/n/n）在提交您的 pull ...
在运行代码覆盖之前，应该确保...
在运行代码覆盖之前，应该确保 ...
[在提交你的 pull 之前...
[在运行代码覆盖之前，应该确保 ...
事实
参考文献规定，在运行代码覆盖之前...
正确
要确定答案是否正确，我们需要...